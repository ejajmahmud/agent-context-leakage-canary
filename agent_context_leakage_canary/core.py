"""Core context leakage canary implementation."""
import secrets
import time
from typing import Dict, List, Optional

class CanaryToken:
    def __init__(self, session_id: str, token_str: str):
        self.session_id = session_id
        self.token_str = token_str
        self.created_at = time.time()

class LeakageAudit:
    def __init__(self, leaked: bool, source_session: Optional[str] = None, detected_token: Optional[str] = None):
        self.leaked = leaked
        self.source_session = source_session
        self.detected_token = detected_token

class CanaryManager:
    def __init__(self):
        self.registry: Dict[str, CanaryToken] = {}

    def generate_canary(self, session_id: str) -> CanaryToken:
        raw_hex = secrets.token_hex(8)
        token_str = f"CANARY_HONEY_{session_id}_{raw_hex}"
        canary = CanaryToken(session_id, token_str)
        self.registry[token_str] = canary
        return canary

    def audit_text_stream(self, text: str, current_session_id: str) -> LeakageAudit:
        for token_str, canary in self.registry.items():
            if token_str in text:
                # If found in a session other than its creator, it is a leak!
                if canary.session_id != current_session_id:
                    return LeakageAudit(
                        leaked=True,
                        source_session=canary.session_id,
                        detected_token=token_str
                    )
        return LeakageAudit(leaked=False)
