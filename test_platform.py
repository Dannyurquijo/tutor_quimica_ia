"""Pruebas aisladas: python -m unittest test_platform -v."""
import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

_data = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
os.environ['DATABASE_URL'] = 'sqlite:///' + _data.name + '/test.db'
os.environ['CHROMA_PATH'] = _data.name + '/chroma'
from fastapi.testclient import TestClient
import main
import ai_gateway
from database import SessionLocal
from schemas import ChatMessage
import auth


class PlatformTests(unittest.TestCase):
    def test_complete_flow_and_access(self):
        with TestClient(main.app) as student, TestClient(main.app) as teacher, TestClient(main.app) as outsider:
            self.assertEqual(outsider.get('/api/me').status_code, 401)
            self.assertEqual(outsider.get('/dashboard-teacher', follow_redirects=False).status_code, 302)
            self.assertEqual(outsider.post('/api/register', json=dict(nombre='A', apellido='B', email='invalid', password='123456', rol='admin')).status_code, 422)
            payload = dict(nombre='Prueba', apellido='Alumno', email='flow@example.test', password='test-password', rol='alumno')
            self.assertEqual(student.post('/api/register', json=payload).status_code, 200)
            uid = student.get('/api/me').json()['id']
            self.assertEqual(student.get('/dashboard', follow_redirects=False).headers['location'], '/onboarding')
            self.assertEqual(student.get('/api/teacher/students').status_code, 403)
            diagnostic = dict(id_alumno='forged-id', grado='2do Bachillerato', nivel_academico='Básico', conocimiento_previo='Átomos', dificultades='Enlaces', estilo_aprendizaje='Visual')
            self.assertEqual(outsider.post('/api/diagnostic', json=diagnostic).status_code, 401)
            with patch('services.vector_collection') as vectors, patch('database.vector_collection', vectors):
                vectors.get.return_value = {'documents': ['Perfil de prueba']}
                self.assertEqual(student.post('/api/diagnostic', json=diagnostic).status_code, 200)
                self.assertEqual(vectors.upsert.call_args.kwargs['ids'], [f'diag_{uid}'])
                self.assertEqual(student.get('/dashboard').status_code, 200)
                self.assertEqual(student.get('/learning').status_code, 200)
                with SessionLocal() as db:
                    db.add(ChatMessage(session_id='shared', id_alumno='other-user', role='user', content='PRIVATE'))
                    db.add(ChatMessage(session_id='shared', id_alumno=str(uid), role='model', content='Pregunta previa'))
                    db.commit()
                chat = dict(id_alumno='other-user', session_id='shared', mensaje_alumno='¿Qué es un enlace?')
                with patch.object(ai_gateway.ai_router.llm, 'chat', return_value='¿Qué observas en los electrones?') as llm:
                    self.assertEqual(student.post('/api/tutor', json=chat).status_code, 200)
                    self.assertNotIn('PRIVATE', str(llm.call_args))
                    self.assertEqual(llm.call_args.args[0][0]['role'], 'assistant')
                    self.assertEqual(student.post('/api/tutor', json=chat).status_code, 200)
                self.assertEqual(student.get('/api/me').json()['alumno']['total_sesiones'], 1)
                with patch.object(ai_gateway.ai_router.llm, 'chat', side_effect=ai_gateway.AIUnavailableError('Intenta de nuevo')):
                    self.assertEqual(student.post('/api/tutor', json=chat).status_code, 503)
                self.assertEqual(outsider.post('/api/tutor', json=chat).status_code, 401)
                self.assertNotIn('PRIVATE', student.get('/api/chat/history', params={'session_id': 'shared'}).text)
                with SessionLocal() as db:
                    auth.register_user(db, 'Docente', 'Prueba', 'teacher@example.test', 'teacher-password', 'maestro')
                self.assertEqual(teacher.post('/api/login', json=dict(email='teacher@example.test', password='teacher-password')).status_code, 200)
                vectors.get.return_value = {'ids': [f'diag_{uid}'], 'documents': ['Enlaces: perfil guardado']}
                page = teacher.get('/dashboard-teacher')
                self.assertEqual(page.status_code, 200)
                self.assertIn('Enlaces: perfil guardado', page.text)
                self.assertEqual(teacher.get('/api/teacher/students').json()['students'][0]['sessions'], 1)
            student.get('/logout')
            self.assertEqual(student.get('/api/me').status_code, 401)
            self.assertEqual(student.post('/api/login', json=dict(email=payload['email'], password=payload['password'])).status_code, 200)
            self.assertEqual(student.get('/health').status_code, 200)

    def test_gateway_fallback_and_empty_content(self):
        answer = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='¿Qué sabes?'))])
        with patch.multiple(ai_gateway, AI_PROVIDER='nvidia', NVIDIA_API_KEY='test', OPENROUTER_API_KEY='test'), patch.object(ai_gateway, 'OpenAI') as client:
            create = client.return_value.__enter__.return_value.chat.completions.create
            create.side_effect = [TimeoutError(), answer]
            self.assertEqual(ai_gateway.LLMService().chat([]), '¿Qué sabes?')
            self.assertEqual(client.call_count, 2)
            self.assertEqual(client.call_args.kwargs['max_retries'], 0)
            create.side_effect = [SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=None))]), TimeoutError()]
            with self.assertRaises(ai_gateway.AIUnavailableError):
                ai_gateway.LLMService().chat([])


if __name__ == '__main__':
    unittest.main()
