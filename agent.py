import argparse
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv

from approvals import ApprovalGate, approval_fingerprint
from browser import BrowserController
from logger import AgentLogger
from planner import Planner
from task_store import TaskStore
from workspaces import Workspace


def load_config(path: str = "config.json") -> dict:
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    if os.getenv("ATOM_HEADLESS"):
        cfg["headless"] = os.getenv("ATOM_HEADLESS", "false").lower() == "true"
    if os.getenv("ATOM_MAX_STEPS"):
        cfg["max_steps"] = int(os.getenv("ATOM_MAX_STEPS"))
    return cfg


def run_task(task: str, workspace_name: str, config: dict, store=None, task_id=None) -> str:
    workspace = Workspace(workspace_name, config.get("data_dir", "data"))
    browser = BrowserController(config, workspace)
    planner = Planner(os.getenv("OPENAI_MODEL", "gpt-5.6"))
    logger = AgentLogger(str(workspace.logs_dir))
    gate = ApprovalGate(store=store, task_id=task_id)
    history = []

    try:
        browser.start()
        if config.get("start_url"):
            browser.execute({"action": "goto", "url": config["start_url"]})
        for step in range(1, int(config.get("max_steps", 50)) + 1):
            state = browser.read_page()
            memories = store.memories(workspace_name) if store else []
            action = planner.next_action(task, state, history, memories)
            logger.write({"task_id": task_id, "step": step, "action": action})
            if action.get("action") == "done":
                summary = action.get("summary", "Valmis.")
                if store and task_id:
                    for item in action.get("memories", [])[:8]:
                        if isinstance(item, str):
                            store.remember(workspace_name, item, "lesson", task_id)
                    store.complete(task_id, summary)
                return summary
            if not gate.authorize(action):
                if store and task_id:
                    store.request_approval(task_id, action, approval_fingerprint(action))
                    return "Odottaa hyväksyntää"
                continue
            try:
                result = browser.execute(action)
            except Exception as exc:
                result = {"error": f"{type(exc).__name__}: {exc}"}
            history.append({"action": action, "result": result})
            history = history[-12:]
            logger.write({"task_id": task_id, "step": step, "result": result})
        summary = "Maksimivaihemäärä saavutettiin."
        if store and task_id:
            store.fail(task_id, summary)
        return summary
    finally:
        browser.stop()


def worker(config: dict, once: bool = False):
    store = TaskStore(config.get("database", "data/atom.db"))
    while True:
        item = store.claim_next()
        if item:
            try:
                run_task(item["prompt"], item["workspace"], config, store, item["id"])
            except Exception as exc:
                store.fail(item["id"], f"{type(exc).__name__}: {exc}")
        if once:
            return
        time.sleep(float(config.get("worker_poll_seconds", 2)))


def main():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY") and os.getenv("ATOM_PLANNER") != "copilot":
        raise SystemExit("OPENAI_API_KEY puuttuu. Käytä API-avainta tai ATOM_PLANNER=copilot.")
    parser = argparse.ArgumentParser(description="ATOM autonomous browser worker")
    parser.add_argument("prompt", nargs="*")
    parser.add_argument("--workspace", default="tommi-hq")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    config = load_config()
    if args.worker:
        worker(config, args.once)
        return
    prompt = " ".join(args.prompt).strip() or input("ATOM tehtävä> ").strip()
    if not prompt:
        raise SystemExit("Tehtävä puuttuu.")
    print(run_task(prompt, args.workspace, config))


if __name__ == "__main__":
    main()
