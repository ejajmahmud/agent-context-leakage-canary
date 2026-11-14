"""Unit tests for agent-context-leakage-canary."""
import unittest
from agent_context_leakage_canary.core import CanaryManager

class TestCanaryManager(unittest.TestCase):
    def setUp(self):
        self.mgr = CanaryManager()

    def test_canary_detection_foreign_session(self):
        c = self.mgr.generate_canary("sess_1")
        audit = self.mgr.audit_text_stream(f"Contains {c.token_str}", current_session_id="sess_2")
        self.assertTrue(audit.leaked)
        self.assertEqual(audit.source_session, "sess_1")

    def test_canary_same_session_not_flagged(self):
        c = self.mgr.generate_canary("sess_1")
        audit = self.mgr.audit_text_stream(f"Contains {c.token_str}", current_session_id="sess_1")
        self.assertFalse(audit.leaked)
