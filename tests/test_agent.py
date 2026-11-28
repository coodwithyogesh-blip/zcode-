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

    def test_inspect_url_requires_written_scope(self):
        result = main.run_tool('inspect_url', {'url':'https://example.com'}, False, '')
        self.assertIn('error', result)
        self.assertIn('authorized scope', result['error'])

    def test_private_urls_are_rejected(self):
        with self.assertRaises(ValueError):
            main.safe_public_url('https://127.0.0.1/admin')


    def test_workspace_files_can_be_promoted_to_training_knowledge(self):
        (main.WORK_DIR / 'KHUDA_training.md').write_text('Follow my supplied review workflow.', encoding='utf-8')
        indexed = main.index_workspace_files()
        self.assertEqual(len(indexed), 1)
        self.assertEqual(indexed[0]['name'], 'KHUDA_training.md')
        training = main.training_context()
        self.assertIn('Follow my supplied review workflow.', training)
        self.assertIn('KHUDA_training.md', training)

    def test_agent_training_context_includes_saved_knowledge(self):
        main.index_text('my-rules.md', 'Use the user's project conventions and report test evidence.', 'test')
        training = main.training_context()
        self.assertIn('my-rules.md', training)
        self.assertIn("report test evidence", training)

if __name__ == '__main__':
    unittest.main()
