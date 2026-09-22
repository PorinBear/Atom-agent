import ipaddress
import socket
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

SELECTABLE = "a,button,input,textarea,select,[role=button],[contenteditable=true]"


class BrowserController:
    def __init__(self, config: dict, workspace):
        self.config = config
        self.workspace = workspace
        self.pw = self.context = self.page = None

    def start(self):
        self.pw = sync_playwright().start()
        self.context = self.pw.chromium.launch_persistent_context(
            user_data_dir=str(self.workspace.profile_dir),
            headless=self.config.get("headless", True), accept_downloads=True,
            viewport=self.config.get("viewport", {"width": 1440, "height": 1000}),
            downloads_path=str(self.workspace.downloads_dir),
        )
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        self.page.set_default_timeout(int(self.config.get("timeout_ms", 15000)))

    def stop(self):
        try:
            if self.context:
                self.context.close()
        finally:
            if self.pw:
                self.pw.stop()

    def _validate_url(self, url: str):
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("Vain http/https-osoitteet ovat sallittuja.")
        if self.config.get("allow_private_network", False):
            return
        try:
            for info in socket.getaddrinfo(parsed.hostname, None):
                ip = ipaddress.ip_address(info[4][0])
                if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                    raise ValueError("Yksityisverkon osoite estettiin.")
        except socket.gaierror as exc:
            raise ValueError("Verkko-osoitetta ei voitu ratkaista.") from exc

    def read_page(self):
        body = self.page.locator("body").inner_text(timeout=10000)[:20000]
        elements, items = self.page.locator(SELECTABLE), []
        for index in range(min(elements.count(), int(self.config.get("max_elements", 140)))):
            el = elements.nth(index)
            try:
                items.append({"i": index, "tag": el.evaluate("(e)=>e.tagName.toLowerCase()"), "text": (el.inner_text() or "").strip()[:180], "aria": (el.get_attribute("aria-label") or "")[:120], "name": (el.get_attribute("name") or "")[:120], "placeholder": (el.get_attribute("placeholder") or "")[:120], "href": (el.get_attribute("href") or "")[:220], "type": (el.get_attribute("type") or "")[:60]})
            except Exception:
                pass
        return {"title": self.page.title(), "url": self.page.url, "body": body, "elements": items}

    def _loc(self, action):
        if action.get("selector"):
            return self.page.locator(action["selector"]).first
        index = int(action["index"])
        if index < 0 or index >= self.page.locator(SELECTABLE).count():
            raise ValueError("Virheellinen elementti-indeksi.")
        return self.page.locator(SELECTABLE).nth(index)

    def execute(self, action: dict):
        name = action.get("action")
        if name == "goto":
            self._validate_url(action["url"])
            self.page.goto(action["url"], wait_until="domcontentloaded")
            return {"url": self.page.url, "title": self.page.title()}
        if name == "click":
            self._loc(action).click()
            return {"ok": True, "url": self.page.url}
        if name == "type":
            loc = self._loc(action)
            loc.fill(action.get("text", "")) if action.get("clear", True) else loc.type(action.get("text", ""))
            return {"ok": True}
        if name == "press":
            self._loc(action).press(action.get("key", "Enter")); return {"ok": True}
        if name == "scroll":
            self.page.mouse.wheel(0, int(action.get("amount", 700))); return {"ok": True}
        if name == "wait":
            self.page.wait_for_timeout(min(int(action.get("ms", 1000)), 10000)); return {"ok": True}
        if name == "screenshot":
            path = self.workspace.safe_output_path(action.get("filename", "latest.png"), self.workspace.logs_dir)
            self.page.screenshot(path=str(path), full_page=bool(action.get("full_page", False)))
            return {"path": str(path)}
        if name == "upload":
            path = self.workspace.safe_input_path(action["filename"])
            self._loc(action).set_input_files(str(path)); return {"uploaded": path.name}
        if name == "read":
            return self.read_page()
        raise ValueError(f"Tuntematon toiminto: {name}")
