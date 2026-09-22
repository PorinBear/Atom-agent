from pathlib import Path

from approvals import approval_fingerprint, requires_approval
from task_store import TaskStore


def test_safe_navigation_does_not_require_approval():
    assert not requires_approval({"action": "goto", "url": "https://example.com"})


def test_side_effect_requires_approval():
    assert requires_approval({"action": "click", "reason": "Lähetä tarjous sähköpostilla"})
    assert requires_approval({"action": "upload", "filename": "offer.pdf"})


def test_fingerprint_is_stable():
    action = {"action": "submit", "index": 3, "risk": "high"}
    assert approval_fingerprint(action) == approval_fingerprint(dict(reversed(list(action.items()))))


def test_queue_memory_and_approval(tmp_path: Path):
    store = TaskStore(tmp_path / "atom.db")
    task_id = store.create("Testaa sivu", "test")
    assert store.claim_next()["id"] == task_id
    store.request_approval(task_id, {"action": "submit"}, "abc")
    assert store.approve(task_id)
    assert store.consume_approval(task_id, "abc")
    store.remember("test", "Käytä lyhyitä vastauksia", source_task_id=task_id)
    store.remember("test", "Käytä lyhyitä vastauksia", source_task_id=task_id)
    assert len(store.memories("test")) == 1
