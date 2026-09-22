import html
import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from task_store import TaskStore

app = FastAPI(title="ATOM Control")
store = TaskStore(os.getenv("ATOM_DATABASE", "data/atom.db"))


def page():
    rows = []
    for task in store.list():
        action = ""
        if task["status"] == "awaiting_approval":
            action = f"<form method='post' action='/tasks/{task['id']}/approve'><button class='ok'>Hyväksy kerran</button></form> <form method='post' action='/tasks/{task['id']}/deny'><button class='no'>Hylkää</button></form>"
        detail = html.escape(task.get("result") or task.get("approval_action") or "")
        rows.append(f"<article><b>#{task['id']} {html.escape(task['workspace'])}</b><span>{task['status']}</span><p>{html.escape(task['prompt'])}</p><small class='result'>{detail}</small>{action}</article>")
    return f"""<!doctype html><html lang='fi'><meta name='viewport' content='width=device-width,initial-scale=1,viewport-fit=cover'><meta name='theme-color' content='#071018'><meta name='apple-mobile-web-app-capable' content='yes'><meta name='apple-mobile-web-app-status-bar-style' content='black-translucent'><meta name='apple-mobile-web-app-title' content='ATOM'><link rel='manifest' href='/manifest.webmanifest'><title>ATOM Control</title><style>
    body{{font:16px system-ui;background:#071018;color:#eef5ff;max-width:900px;margin:auto;padding:22px}}h1{{color:#75e4ff}}form{{display:inline}}input,select,button{{font:inherit;padding:12px;border-radius:9px;border:1px solid #355}}input{{width:min(560px,90%)}}article{{background:#101e2b;margin:14px 0;padding:16px;border-radius:14px}}article span{{float:right;color:#79d}}small{{display:block;white-space:pre-wrap;color:#9ab;margin:8px 0}}button{{background:#28b6d8;color:#00131a;font-weight:700}}.no{{background:#ef7181}}.ok{{background:#55d39a}}</style>
    <h1>ATOM Control</h1><form method='post' action='/tasks'><input id='prompt' name='prompt' placeholder='Mitä ATOM tekee?' required><button type='button' id='mic' aria-label='Puheesta tekstiksi'>🎙️</button><select name='workspace'><option>tommi-hq</option><option>ewalahti</option><option>future-atom</option></select><button>Lisää tehtävä</button></form><button type='button' id='speak'>🔊 Lue uusin vastaus</button>{''.join(rows)}
    <script>
    const field=document.getElementById('prompt'), mic=document.getElementById('mic');
    const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;
    if(SpeechRecognition){{const r=new SpeechRecognition();r.lang='fi-FI';r.interimResults=true;r.onresult=e=>{{field.value=Array.from(e.results).map(x=>x[0].transcript).join(' ')}};mic.onclick=()=>r.start()}}else{{mic.disabled=true;mic.title='Puheentunnistus ei ole tässä selaimessa käytettävissä'}}
    document.getElementById('speak').onclick=()=>{{const items=document.querySelectorAll('.result');if(items.length){{speechSynthesis.cancel();speechSynthesis.speak(new SpeechSynthesisUtterance(items[0].textContent))}}}}
    if('serviceWorker' in navigator){{navigator.serviceWorker.register('/sw.js')}}
    </script></html>"""


@app.get("/", response_class=HTMLResponse)
def index(): return page()


@app.post("/tasks")
def create_task(prompt: str = Form(...), workspace: str = Form("tommi-hq")):
    if not prompt.strip() or len(prompt) > 6000: raise HTTPException(400, "Virheellinen tehtävä")
    store.create(prompt.strip(), workspace); return RedirectResponse("/", status_code=303)


@app.post("/tasks/{task_id}/approve")
def approve(task_id: int):
    if not store.approve(task_id): raise HTTPException(409, "Ei hyväksyttävää toimintoa")
    return RedirectResponse("/", status_code=303)


@app.post("/tasks/{task_id}/deny")
def deny(task_id: int): store.deny(task_id); return RedirectResponse("/", status_code=303)


@app.get("/api/tasks")
def tasks(): return store.list()


@app.get("/api/memories/{workspace}")
def memories(workspace: str): return store.memories(workspace)


@app.get("/manifest.webmanifest")
def manifest():
    return {"name": "ATOM Team Agent", "short_name": "ATOM", "description": "Oppiva puheohjattu tiimiagentti", "start_url": "/", "display": "standalone", "background_color": "#071018", "theme_color": "#071018"}


@app.get("/sw.js", response_class=PlainTextResponse)
def service_worker():
    return "self.addEventListener('install',()=>self.skipWaiting());self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));"
