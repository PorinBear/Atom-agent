import json
from datetime import datetime
from pathlib import Path

class AgentLogger:
    def __init__(self, logs_dir="logs"):
        self.dir = Path(logs_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}.jsonl"

    def write(self, event: dict):
        event = {"ts": datetime.now().isoformat(), **event}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
