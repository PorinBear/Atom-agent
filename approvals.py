import hashlib
import json

ALWAYS_APPROVE_ACTIONS = {"send", "submit", "purchase", "payment", "delete", "cancel", "sign", "change_permissions", "publish", "upload", "download_execute"}
RISK_TERMS = {"pay", "payment", "purchase", "buy now", "place order", "bank transfer", "send money", "delete", "remove", "cancel subscription", "accept contract", "sign contract", "publish", "send message", "submit", "invite", "permission", "maksa", "maksu", "osta", "tilaa", "pankkisiirto", "poista", "irtisano", "hyväksy sopimus", "lähetä", "julkaise", "käyttöoikeus"}


def approval_fingerprint(action: dict) -> str:
    raw = json.dumps(action, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:20]


def requires_approval(action: dict) -> bool:
    if action.get("risk") == "high" or action.get("action") in ALWAYS_APPROVE_ACTIONS:
        return True
    blob = " ".join(str(value) for value in action.values()).lower()
    return any(term in blob for term in RISK_TERMS)


class ApprovalGate:
    def __init__(self, store=None, task_id=None):
        self.store = store
        self.task_id = task_id

    def authorize(self, action: dict) -> bool:
        if not requires_approval(action):
            return True
        fingerprint = approval_fingerprint(action)
        if self.store and self.task_id:
            return self.store.consume_approval(self.task_id, fingerprint)
        print("\n⚠️ Hyväksyntä vaaditaan:")
        print(json.dumps(action, ensure_ascii=False, indent=2))
        return input("Suoritetaanko? [y/N]: ").strip().lower() in {"y", "yes", "j", "kyllä", "kylla"}
