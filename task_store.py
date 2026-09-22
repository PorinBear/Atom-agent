import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def now(): return datetime.now(timezone.utc).isoformat()


class TaskStore:
    def __init__(self, path="data/atom.db"):
        self.path = Path(path); self.path.parent.mkdir(parents=True, exist_ok=True); self._init()

    def connect(self):
        db = sqlite3.connect(self.path, timeout=30); db.row_factory = sqlite3.Row; return db

    def _init(self):
        with self.connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS tasks (
              id INTEGER PRIMARY KEY AUTOINCREMENT, prompt TEXT NOT NULL,
              workspace TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'queued',
              result TEXT, approval_action TEXT, approval_fingerprint TEXT,
              approved_fingerprint TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""")
            db.execute("""CREATE TABLE IF NOT EXISTS memories (
              id INTEGER PRIMARY KEY AUTOINCREMENT, workspace TEXT NOT NULL,
              kind TEXT NOT NULL, content TEXT NOT NULL, source_task_id INTEGER,
              created_at TEXT NOT NULL)""")

    def create(self, prompt, workspace="tommi-hq"):
        stamp = now()
        with self.connect() as db:
            return db.execute("INSERT INTO tasks(prompt,workspace,created_at,updated_at) VALUES(?,?,?,?)", (prompt, workspace, stamp, stamp)).lastrowid

    def list(self, limit=100):
        with self.connect() as db: return [dict(r) for r in db.execute("SELECT * FROM tasks ORDER BY id DESC LIMIT ?", (limit,))]

    def claim_next(self):
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM tasks WHERE status='queued' ORDER BY id LIMIT 1").fetchone()
            if not row: return None
            db.execute("UPDATE tasks SET status='running',updated_at=? WHERE id=?", (now(), row["id"]))
            return dict(row)

    def request_approval(self, task_id, action, fingerprint):
        with self.connect() as db:
            db.execute("UPDATE tasks SET status='awaiting_approval',approval_action=?,approval_fingerprint=?,updated_at=? WHERE id=?", (json.dumps(action, ensure_ascii=False), fingerprint, now(), task_id))

    def approve(self, task_id):
        with self.connect() as db:
            row = db.execute("SELECT approval_fingerprint FROM tasks WHERE id=?", (task_id,)).fetchone()
            if not row or not row[0]: return False
            db.execute("UPDATE tasks SET status='queued',approved_fingerprint=approval_fingerprint,updated_at=? WHERE id=?", (now(), task_id)); return True

    def deny(self, task_id):
        with self.connect() as db: db.execute("UPDATE tasks SET status='failed',result='Toiminto hylättiin',updated_at=? WHERE id=?", (now(), task_id))

    def consume_approval(self, task_id, fingerprint):
        with self.connect() as db:
            row = db.execute("SELECT approved_fingerprint FROM tasks WHERE id=?", (task_id,)).fetchone()
            if row and row[0] == fingerprint:
                db.execute("UPDATE tasks SET approved_fingerprint=NULL,approval_action=NULL,approval_fingerprint=NULL WHERE id=?", (task_id,)); return True
        return False

    def complete(self, task_id, result):
        with self.connect() as db: db.execute("UPDATE tasks SET status='done',result=?,updated_at=? WHERE id=?", (result, now(), task_id))

    def fail(self, task_id, result):
        with self.connect() as db: db.execute("UPDATE tasks SET status='failed',result=?,updated_at=? WHERE id=?", (result, now(), task_id))

    def remember(self, workspace, content, kind="lesson", source_task_id=None):
        clean = " ".join(str(content).split())[:2000]
        if not clean: return
        with self.connect() as db:
            exists = db.execute("SELECT 1 FROM memories WHERE workspace=? AND content=?", (workspace, clean)).fetchone()
            if not exists:
                db.execute("INSERT INTO memories(workspace,kind,content,source_task_id,created_at) VALUES(?,?,?,?,?)", (workspace, kind, clean, source_task_id, now()))

    def memories(self, workspace, limit=40):
        with self.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM memories WHERE workspace=? ORDER BY id DESC LIMIT ?", (workspace, limit))]
