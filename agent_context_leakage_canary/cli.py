"""CLI for agent-context-leakage-canary."""
import argparse
import sys
from .core import CanaryManager

def main():
    parser = argparse.ArgumentParser(description="Agent Context Leakage Canary CLI")
    parser.add_argument("--demo", action="store_true", help="Run context leakage canary demo")
    args = parser.parse_args()

    if args.demo:
        mgr = CanaryManager()
        c_alice = mgr.generate_canary("tenant_alice")
        print(f"[+] Generated honeytoken for Alice: {c_alice.token_str}")

        # Simulate Bob receiving text with Alice's canary
        bob_stream = f"Here is the summary of project data including {c_alice.token_str} from shared cache."
        audit = mgr.audit_text_stream(bob_stream, current_session_id="tenant_bob")

        if audit.leaked:
            print(f"[!] SECURITY ALARM: Context Leakage Detected in tenant_bob!")
            print(f"    Leaked Token: {audit.detected_token}")
            print(f"    Originating Session: {audit.source_session}")
        else:
            print("[+] No context leakage detected.")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
