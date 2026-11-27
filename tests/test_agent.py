import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault('KHUDA_ALLOW_NO_AUTH', 'true')
from backend import main

class AgentSafetyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        main.WORK_DIR = root / 'workspace'
        main.KNOWLEDGE_DIR = root / 'knowledge'
        main.REPORT_DIR = root / 'reports'
        for folder in (main.WORK_DIR, main.KNOWLEDGE_DIR, main.REPORT_DIR):
            folder.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_path_traversal_is_rejected(self):
        with self.assertRaises(ValueError):
            main.safe_path(main.WORK_DIR, '../../secret.txt')

    def test_write_requires_explicit_permission(self):
        result = main.run_tool('write_file', {'path':'notes/a.txt','content':'hello'}, False, '')
        self.assertIn('error', result)
        self.assertFalse((main.WORK_DIR / 'notes/a.txt').exists())

    def test_write_and_read_workspace_file(self):
        written = main.run_tool('write_file', {'path':'notes/a.txt','content':'hello'}, True, '')
        read = main.run_tool('read_file', {'path':'notes/a.txt'}, False, '')
        self.assertEqual(written['characters'], 5)
        self.assertEqual(read['content'], 'hello')

    def test_knowledge_is_persisted_and_retrievable(self):
        main.index_text('owasp.txt', 'Broken access control and IDOR testing notes', 'test')
        results = main.retrieve('IDOR access control')
        self.assertTrue(results)
        self.assertEqual(results[0]['source'], 'owasp.txt')

    def test_private_urls_are_rejected(self):
        with self.assertRaises(ValueError):
            main.safe_public_url('https://127.0.0.1/admin')

if __name__ == '__main__':
    unittest.main()
