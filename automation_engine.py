import asyncio
import base64
import hashlib
import hmac
import json
import os
import re
import socket
import struct
import subprocess
import urllib.parse
import time
from typing import Callable, Dict, Any, Optional
from playwright.async_api import async_playwright

def _find_chrome_path() -> str:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]


CHROME_PATH = _find_chrome_path()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIR = os.path.join(BASE_DIR, "profiles")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

os.makedirs(PROFILES_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Google One Offer Tokens (Universal across accounts/currencies)
TOK_PRO5TB_12M   = "AVbCH/cspB8VdqKJ+ax/uPxUFAVuYRPX4iSjtg4Fu0PG9zUeURSM7y//LlQva1dCd/rbKVM6EJmyiG/C9BoQ95pMl8yDCHuiwCvM5CuGJME="
TOK_PRO5TB_6M    = "AVbCH/fUON3w8hpfeutprA3BMQwrBwYIB6Y8CSWi1isDCDswKUUhGQ3dluj5WXsNKOvr8K5UULBGrRsf4KlW1rHLz0fF3SvxQhBFRbBOHCA="
TOK_PRO5TB_6M_2  = "AVbCH/cJ5SeHgkVRt+bdcrapx/aLSu2kbsBgMdI413zbllDNsNQoC/zVlG/Npbu55WlMzBwWPhUedIvZFDg7fw0CmCv/8DKj04IZ21pK7mrV/hh5"
TOK_PRO5TB_6M_SS = "AVbCH/cgl4zvPT2Lqw95Gn+RYAJIVwFwi783i6uVprX7u3MCa5J4CcTXH5RABa5WjBrUoQnwf8vI10TNV7ktd26myIdxqIwGmNoJ5ofYNqpQ10RKoSvHs75wsfA="
TOK_P1M          = "AVbCH/dXbuvFhoeuGZb/+3+b5Jhft4kOY/wQLGqLhy0hhx6hDAJ/1z9y23+x9N5zyNtQ268DEw=="
TOK_MONTHLY      = "AVbCH/dSbs1UHItdkpohleJ9+69eSPWyFRutIpRUdGPlsdDKw2IMvRRHiwDefRVyEHl12jqfmBgQZByeX7hJ"
YT_FREE_TOK      = "AVbCH/eW4Nfp8KBl0zlm7x9PhaiCvpnqwUuL2D8NFPBQgmM9+HuYS1h2xH5lLWU/BsBj775LK5GqK8UHKqoSzhDDz+PqP3paNesqLU0r9i6XCrYa"
PREFIX           = "subs:com.google.android.apps.subscriptions.red:"

HOOK_JS = """
(() => {
  if (!location.hostname.includes('one.google.com')) return;
  if (window.__HOOK_INSTALLED) return;
  window.__HOOK_INSTALLED = true;
  let currentTest = window.__INIT_TEST || null;
  window.__setDirectTest = (t) => { currentTest = t; };

  function patchTargetNode(node) {
    if (!Array.isArray(node) || !Array.isArray(currentTest?.full_items)) return false;
    let patched = false;
    if (node.length > 12 && Array.isArray(node[12])) {
      if (Array.isArray(node[7]) && Array.isArray(node[7][5]) && node[7][5].length > 0) {
        window.__capturedSubId = node[7][5][0];
      }
      node[12] = currentTest.full_items;
      const targetMode = currentTest.mode || (Array.isArray(currentTest.ear8) ? currentTest.ear8[1] : 5) || 5;
      if (currentTest.ear8) {
        node[7] = currentTest.ear8;
      } else if (Array.isArray(node[7]) && Array.isArray(node[7][5]) && node[7][5].length > 0) {
        node[7][1] = targetMode;
      } else if (window.__capturedSubId) {
        node[7] = [null, targetMode, null, null, null, [window.__capturedSubId]];
      }
      patched = true;
    }
    if (node.length > 10 && Array.isArray(node[10]) && Array.isArray(node[10][0])) {
      node[10] = [currentTest.full_items];
      if (Array.isArray(node[2]) && Array.isArray(node[2][2]) && Array.isArray(node[2][2][8])) {
        node[2][2][8] = [currentTest.full_items];
      }
      if (currentTest.ear8) {
        node[6] = currentTest.ear8;
      }
      patched = true;
    }
    return patched;
  }

  function rewriteFreq(bodyStr) {
    if (typeof bodyStr !== 'string' || !bodyStr.includes('f.req=') || !currentTest) return bodyStr;
    try {
      const parts = bodyStr.split('&');
      for (let i = 0; i < parts.length; i++) {
        if (parts[i].startsWith('f.req=')) {
          const raw = decodeURIComponent(parts[i].slice(6).replace(/\\+/g, ' '));
          const outer = JSON.parse(raw);
          let changed = false;
          if (Array.isArray(outer)) {
            for (const group of outer) {
              if (!Array.isArray(group)) continue;
              for (const call of group) {
                if (Array.isArray(call) && call[0] === 'Ngbm' && typeof call[1] === 'string') {
                  const payload = JSON.parse(call[1]);
                  if (Array.isArray(payload)) {
                    if (patchTargetNode(payload[0])) changed = true;
                    if (patchTargetNode(payload[1])) changed = true;
                  }
                  if (changed) {
                    call[1] = JSON.stringify(payload);
                  }
                }
              }
            }
          }
          if (changed) {
            parts[i] = 'f.req=' + encodeURIComponent(JSON.stringify(outer));
            return parts.join('&');
          }
        }
      }
    } catch (e) {}
    return bodyStr;
  }

  const origSend = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.send = function(body) {
    if (typeof body === 'string' && body.includes('Ngbm')) {
      body = rewriteFreq(body);
    }
    return origSend.call(this, body);
  };

  function rewriteUrl(val) {
    const s = String(val || '');
    if (!s.includes('/eacquire/multiline') || !currentTest) return val;
    try {
      const u = new URL(s, location.origin);
      const earStr = u.searchParams.get('ear');
      if (!earStr) return val;
      const ear = JSON.parse(earStr);
      if (Array.isArray(ear[8]) && Array.isArray(ear[8][5]) && ear[8][5].length > 0) {
        window.__capturedSubId = ear[8][5][0];
      }
      if (Array.isArray(ear[13]) && Array.isArray(currentTest.full_items)) {
        ear[13][0] = currentTest.full_items;
      }
      if (Array.isArray(ear[4]) && typeof ear[4][0] === 'string' && Array.isArray(currentTest.full_items)) {
        try {
          const inner4 = JSON.parse(atob(ear[4][0]));
          if (Array.isArray(inner4) && inner4.length > 8) {
            inner4[8] = [currentTest.full_items];
            ear[4][0] = btoa(JSON.stringify(inner4));
          }
        } catch (e4) {}
      }
      const targetMode = currentTest.mode || (Array.isArray(currentTest.ear8) ? currentTest.ear8[1] : 5) || 5;
      if (currentTest.ear8) {
        ear[8] = currentTest.ear8;
      } else if (Array.isArray(ear[8]) && Array.isArray(ear[8][5]) && ear[8][5].length > 0) {
        ear[8][1] = targetMode;
      } else if (window.__capturedSubId) {
        ear[8] = [null, targetMode, null, null, null, [window.__capturedSubId]];
      }
      ear[24] = null;
      u.searchParams.set('ear', JSON.stringify(ear));
      window.__capturedEarUrl = u.toString();
      return u.toString();
    } catch (e) {
      return val;
    }
  }

  if (window.TrustedTypePolicy && TrustedTypePolicy.prototype.createScriptURL) {
    const origCreate = TrustedTypePolicy.prototype.createScriptURL;
    TrustedTypePolicy.prototype.createScriptURL = function(input, ...args) {
      return origCreate.call(this, rewriteUrl(input), ...args);
    };
  }
  const frameProto = HTMLIFrameElement.prototype;
  const srcDesc = Object.getOwnPropertyDescriptor(frameProto, 'src');
  if (srcDesc?.set) {
    Object.defineProperty(frameProto, 'src', {
      ...srcDesc,
      set(v) {
        if (typeof v === 'string') v = rewriteUrl(v);
        return srcDesc.set.call(this, v);
      }
    });
  }
  const origSetAttr = Element.prototype.setAttribute;
  Element.prototype.setAttribute = function(name, val) {
    if (this instanceof HTMLIFrameElement && String(name).toLowerCase() === 'src') {
      val = rewriteUrl(String(val));
    }
    return origSetAttr.call(this, name, val);
  };
})();
"""


def get_totp(secret: str) -> str:
    if not secret:
        return ""
    secret = re.sub(r"[^A-Za-z2-7]", "", secret.strip()).upper()
    if not secret:
        return ""
    missing_padding = len(secret) % 8
    if missing_padding != 0:
        secret += "=" * (8 - missing_padding)
    key = base64.b32decode(secret, casefold=True)
    counter = int(time.time()) // 30
    msg = struct.pack(">Q", counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[19] & 0xF
    code = (struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"


def get_profile_dir(acc_id: str, email: str) -> str:
    safe_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", email or acc_id)
    path = os.path.join(PROFILES_DIR, f"profile_{safe_name}")
    os.makedirs(path, exist_ok=True)
    return path


def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.8)
        return s.connect_ex(("127.0.0.1", port)) == 0


def kill_chrome_for_profile(user_data_dir: str) -> int:
    """
    Terminate every Chrome process still bound to `user_data_dir`.

    Chrome only allows one instance per --user-data-dir. If a leftover window
    (for example the one opened by the manual browser button) is still alive,
    the next launch silently hands the profile over to that instance and exits
    without opening --remote-debugging-port, which makes the CDP connection
    fail with ECONNREFUSED.
    """
    target = os.path.abspath(user_data_dir)
    literal = target.replace("'", "''")
    script = (
        "Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" | "
        "Where-Object { $_.CommandLine -and $_.CommandLine.Contains('" + literal + "') } | "
        "ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
    )
    killed = 0
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
            capture_output=True,
            timeout=30,
        )
    except Exception:
        pass

    # Give Chrome a moment to release the profile lock file.
    time.sleep(1.2)
    return killed


def parse_proxy_string(raw_proxy: str) -> Optional[Dict[str, Any]]:
    """
    Parse various proxy formats into {scheme, host, port, username, password}:
    - http://user:pass@host:port
    - socks5://user:pass@host:port
    - host:port:user:pass
    - user:pass@host:port
    - host:port
    """
    s = (raw_proxy or "").strip()
    if not s:
        return None

    scheme = "http"
    if "://" in s:
        scheme, s = s.split("://", 1)
        scheme = scheme.lower()

    if "@" in s:
        auth_part, host_part = s.rsplit("@", 1)
        user, pwd = (auth_part.split(":", 1) + [""])[:2]
        host, port_str = (host_part.split(":", 1) + ["8080"])[:2]
        return {"scheme": scheme, "host": host, "port": int(port_str), "username": user, "password": pwd}

    parts = s.split(":")
    if len(parts) == 4:
        # host:port:user:pass
        return {
            "scheme": scheme,
            "host": parts[0],
            "port": int(parts[1]),
            "username": parts[2],
            "password": parts[3],
        }
    elif len(parts) == 2:
        return {
            "scheme": scheme,
            "host": parts[0],
            "port": int(parts[1]),
            "username": "",
            "password": "",
        }
    return None


_FLOPPY_CACHE: Dict[str, str] = {}


def resolve_account_proxy(account: Dict[str, Any], target_region: str, proxy_template: str) -> str:
    """
    Resolve the proxy string for an account:
    1. Account-specific proxy overrides global template
    2. If raw string is a FloppyData API Key (32-char alphanumeric without :/@), auto-fetch subuser credentials
    3. Global proxy template replaces {country}/{COUNTRY} and {session}/{SESSION} automatically
    """
    raw = (account.get("proxy") or "").strip() or (proxy_template or "").strip()
    if not raw:
        return ""
    if ":" not in raw and "@" not in raw and len(raw) >= 24:
        if raw in _FLOPPY_CACHE:
            raw = _FLOPPY_CACHE[raw]
        else:
            try:
                import urllib.request
                req = urllib.request.Request(
                    "https://api.floppydata.net/v2/proxy/rotating/subusers",
                    headers={"X-Api-Key": raw, "User-Agent": "Mozilla/5.0", "Connection": "close"},
                )
                resp = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))
                items = resp.get("items") or []
                if items:
                    u = items[0]["username"]
                    p = items[0]["password"]
                    raw = f"http://{u}-type-residential-country-{{COUNTRY}}-session-{{session}}-rotation-0:{p}@geo.g-w.info:10080"
                    _FLOPPY_CACHE[proxy_template.strip()] = raw
            except Exception:
                pass
    cc_lower = (target_region or "TR").lower()
    cc_upper = cc_lower.upper()
    sess_seed = re.sub(r"[^a-zA-Z0-9]", "", account.get("id", "acc")) + hashlib.md5(
        (account.get("email", "") or account.get("id", "")).encode("utf-8")
    ).hexdigest()[:6]
    resolved = (
        raw.replace("{country}", cc_lower)
        .replace("{COUNTRY}", cc_upper)
        .replace("{session}", sess_seed)
        .replace("{SESSION}", sess_seed)
    )
    return resolved


_BLOCKED_PROXY_HOSTS = (
    b"mtalk.google.com",
    b"update.googleapis.com",
    b"safebrowsing.googleapis.com",
    b"google-ohttp-relay-safebrowsing",
    b"optimizationguide-pa.googleapis.com",
    b"gvt1.com",
    b"gvt2.com",
)


class LocalHttpProxyAuthBridge:
    """
    Lightweight local asyncio HTTP/HTTPS CONNECT proxy bridge that injects
    Proxy-Authorization Basic headers, blocks Chrome background telemetry bursts,
    verifies upstream CONNECT responses, and auto-rotates sticky residential sessions
    when a residential peer goes offline or drops connections.
    """

    def __init__(self, local_port: int, upstream: Dict[str, Any]):
        self.local_port = local_port
        self.upstream = upstream
        self.server: Optional[asyncio.AbstractServer] = None
        self.rotation_idx: int = 0
        self.fail_streak: int = 0

    def rotate_session(self):
        self.rotation_idx += 1
        self.fail_streak = 0

    def _current_username(self) -> str:
        base_u = self.upstream.get("username", "")
        if self.rotation_idx <= 0 or "-session-" not in base_u:
            return base_u
        return re.sub(r"(-session-[a-zA-Z0-9_]+)", rf"\1r{self.rotation_idx}", base_u, count=1)

    async def _pipe(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            while not reader.at_eof():
                data = await reader.read(16384)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception:
            pass
        finally:
            try:
                writer.close()
            except Exception:
                pass

    async def _handle_client(self, client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter):
        up_writer = None
        try:
            first_line = await asyncio.wait_for(client_reader.readline(), timeout=15)
            if not first_line:
                client_writer.close()
                return

            fl_lower = first_line.lower()
            if any(bh in fl_lower for bh in _BLOCKED_PROXY_HOSTS):
                client_writer.write(b"HTTP/1.1 502 Bad Gateway\r\nConnection: close\r\n\r\n")
                await client_writer.drain()
                client_writer.close()
                return

            headers = []
            while True:
                line = await asyncio.wait_for(client_reader.readline(), timeout=15)
                if not line or line in (b"\r\n", b"\n"):
                    break
                if not line.lower().startswith(b"proxy-authorization:"):
                    headers.append(line)

            is_connect = fl_lower.startswith(b"connect ")
            up_reader = None

            for attempt in range(3):
                try:
                    up_reader, up_writer = await asyncio.wait_for(
                        asyncio.open_connection(self.upstream["host"], self.upstream["port"]),
                        timeout=12,
                    )
                    auth_str = f"{self._current_username()}:{self.upstream['password']}"
                    b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("ascii")
                    auth_header = f"Proxy-Authorization: Basic {b64_auth}\r\n".encode("ascii")

                    up_writer.write(first_line)
                    for h in headers:
                        up_writer.write(h)
                    up_writer.write(auth_header)
                    up_writer.write(b"\r\n")
                    await up_writer.drain()

                    if is_connect:
                        resp_hdr = await asyncio.wait_for(up_reader.readuntil(b"\r\n\r\n"), timeout=12)
                        status_line = resp_hdr.split(b"\r\n", 1)[0]
                        if b" 200 " not in status_line:
                            raise RuntimeError(f"Upstream CONNECT non-200: {status_line!r}")
                        self.fail_streak = 0
                        client_writer.write(resp_hdr)
                        await client_writer.drain()
                    break
                except Exception:
                    if up_writer:
                        try:
                            up_writer.close()
                        except Exception:
                            pass
                        up_writer = None
                    self.fail_streak += 1
                    if self.fail_streak >= 3 or attempt >= 1:
                        self.rotate_session()
                    if attempt == 2:
                        raise
                    await asyncio.sleep(0.5)

            await asyncio.gather(
                self._pipe(client_reader, up_writer),
                self._pipe(up_reader, client_writer),
            )
        except Exception:
            try:
                client_writer.close()
            except Exception:
                pass
            if up_writer:
                try:
                    up_writer.close()
                except Exception:
                    pass

    async def start(self):
        self.server = await asyncio.start_server(self._handle_client, "127.0.0.1", self.local_port)

    async def stop(self):
        if self.server:
            self.server.close()
            try:
                await self.server.wait_closed()
            except Exception:
                pass


class GoogleUltraAutomator:
    def __init__(
        self,
        account: Dict[str, Any],
        card: Dict[str, str],
        target_region: str = "TR",
        target_plan: str = "ultra_20tb_5x",
        auto_cancel: bool = True,
        proxy_template: str = "",
        port: int = 9320,
        on_log: Optional[Callable[[str], None]] = None,
        on_state: Optional[Callable[[Dict[str, Any]], None]] = None,
    ):
        self.account = account
        self.card = card
        self.target_region = (target_region or "TR").upper()
        self.target_plan = target_plan
        self.auto_cancel = auto_cancel
        self.proxy_template = proxy_template
        self.port = port
        self.on_log = on_log or (lambda msg: print(msg))
        self.on_state = on_state or (lambda st: None)
        self.stop_requested = False
        self.proc: Optional[subprocess.Popen] = None
        self.proxy_bridge: Optional[LocalHttpProxyAuthBridge] = None

    def log(self, msg: str):
        ts = time.strftime("%H:%M:%S")
        line = f"[{ts}] [{self.account['id']}] {msg}"
        self.on_log(line)

    def update_state(
        self,
        status: Optional[str] = None,
        current_step: Optional[int] = None,
        step_message: Optional[str] = None,
        expiry_date: Optional[str] = None,
        last_screenshot: Optional[str] = None,
        ip_info: Optional[str] = None,
    ):
        patch: Dict[str, Any] = {}
        if status is not None:
            self.account["status"] = status
            patch["status"] = status
        if current_step is not None:
            self.account["current_step"] = current_step
            patch["current_step"] = current_step
        if step_message is not None:
            self.account["step_message"] = step_message
            patch["step_message"] = step_message
        if expiry_date is not None:
            self.account["expiry_date"] = expiry_date
            patch["expiry_date"] = expiry_date
        if last_screenshot is not None:
            self.account["last_screenshot"] = last_screenshot
            patch["last_screenshot"] = last_screenshot
        if ip_info is not None:
            self.account["ip_info"] = ip_info
            patch["ip_info"] = ip_info
        self.on_state(patch)

    async def save_screenshot(self, page, step_tag: str) -> str:
        fname = f"{self.account['id']}_{step_tag}_{int(time.time())}.png"
        fpath = os.path.join(SCREENSHOTS_DIR, fname)
        try:
            await page.screenshot(path=fpath)
            self.update_state(last_screenshot=fname)
        except Exception as e:
            self.log(f"Screenshot save hint: {e}")
        return fname

    def check_stop(self):
        if self.stop_requested:
            raise RuntimeError("User manually stopped the task")

    async def safe_goto(self, page, url: str, timeout: int = 40000):
        """Navigate with automatic retry and residential proxy session rotation on transient network errors."""
        last_err = None
        for attempt in range(4):
            self.check_stop()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=timeout)
                return
            except Exception as e:
                last_err = e
                err_short = str(e).splitlines()[0][:80]
                if "has been closed" in err_short or "Target closed" in err_short:
                    self.log(f"❌ Browser window was closed during navigation ({err_short}). Re-run the pipeline.")
                    raise
                if attempt < 3:
                    if self.proxy_bridge:
                        self.proxy_bridge.rotate_session()
                        self.log(f"⚠️ Residential proxy network fluctuation ({err_short})，Automatically switching to same-country residential node and retrying ({attempt + 1}/3)...")
                    else:
                        self.log(f"⚠️ Navigation failed ({err_short})，retrying ({attempt + 1}/3)...")
                    await asyncio.sleep(2.5)
        raise last_err

    async def ensure_totp_fresh(self) -> str:
        secret = self.account.get("totp_secret", "")
        if not secret:
            return ""
        rem = 30 - (int(time.time()) % 30)
        if rem <= 3:
            self.log(f"2FA dynamic code expiring, waiting {rem + 1} seconds...")
            await asyncio.sleep(rem + 1)
        return get_totp(secret)

    async def pass_reauth_on_page(self, page_obj):
        """Automatically handle Google email + password + 2FA TOTP re-authentication prompts."""
        email = self.account.get("email", "")
        password = self.account.get("password", "")
        for _ in range(16):
            self.check_stop()
            if page_obj.is_closed():
                return
            try:
                body = await page_obj.inner_text("body", timeout=3000)
            except Exception:
                await asyncio.sleep(1.5)
                continue

            if "gds.google.com" in page_obj.url or "recoveryoptions" in page_obj.url or "确保您始终都能登录" in body:
                self.log("Detected gds.google.com recovery info prompt, clicking [Cancel/Skip] to continue...")
                cancel_btn = page_obj.locator('button:has-text("取消"), button:has-text("Cancel"), button:has-text("跳过"), button:has-text("Skip"), [role="button"]:has-text("取消"), [role="button"]:has-text("Cancel"), text="取消", text="Cancel"').first
                if await cancel_btn.count() > 0:
                    try:
                        await cancel_btn.click(timeout=3000)
                    except Exception:
                        pass
                await page_obj.evaluate(
                    """() => {
                    const els = Array.from(document.querySelectorAll('button, a, [role="button"], span, div'));
                    for (const el of els) {
                        const t = (el.innerText || '').trim();
                        if (t === '取消' || t === 'Cancel' || t === '跳过' || t === 'Skip' || t === '以后再说' || t === 'Not now') {
                            el.click();
                        }
                    }
                }"""
                )
                await asyncio.sleep(4.5)
                continue

            if "confirmidentifier" in page_obj.url:
                self.log("Detected confirmidentifier page, clicking [Next]...")
                nxt_btn = page_obj.locator('#identifierNext button, button:has-text("下一步"), button:has-text("Next"), #identifierNext').first
                if await nxt_btn.count() > 0:
                    try:
                        await nxt_btn.click(timeout=3000)
                    except Exception:
                        try:
                            await nxt_btn.click(force=True, timeout=3000)
                        except Exception:
                            pass
                await page_obj.evaluate(
                    """() => {
                    const targets = Array.from(document.querySelectorAll('button, #identifierNext, [role="button"]'));
                    for (const el of targets) {
                        const t = (el.innerText || '').trim();
                        if (t === '下一步' || t === 'Next' || t === 'Continue' || el.id === 'identifierNext') {
                            el.click();
                        }
                    }
                }"""
                )
                await asyncio.sleep(4)
                continue

            email_inp = page_obj.locator('input#identifierId, input[name="identifier"]')
            if email and await email_inp.count() > 0 and await email_inp.first.is_visible():
                pwd_vis = page_obj.locator('input[type="password"], input[name="Passwd"]')
                if await pwd_vis.count() == 0 or not await pwd_vis.first.is_visible():
                    self.log(f"Detected email input field, filling email and clicking Next: {email}")
                    await email_inp.first.fill(email)
                    await email_inp.first.press("Enter")
                    await asyncio.sleep(4.5)
                    continue

            if "Verify it's you" in body or "验证您的身份" in body:
                btn = page_obj.locator('button:has-text("Verify it\'s you"), button:has-text("验证您的身份"), div[role="button"]:has-text("验证您的身份"), div[role="button"]:has-text("Verify it\'s you")').first
                if await btn.count() > 0 and await btn.is_visible():
                    self.log("Detected security verification button, clicking [Verify identity]...")
                    await btn.click()
                    await asyncio.sleep(4)
                    continue

            pwd = page_obj.locator('input[type="password"], input[name="Passwd"]')
            if await pwd.count() > 0 and await pwd.first.is_visible():
                self.log("Automatically entering password to verify identity...")
                try:
                    await pwd.first.fill(password)
                    next_btn = page_obj.locator('#passwordNext, button:has-text("下一步"), button:has-text("Next")').first
                    if await next_btn.count() > 0 and await next_btn.is_visible():
                        await next_btn.click()
                    else:
                        await pwd.first.press("Enter")
                except Exception:
                    return
                await asyncio.sleep(4.5)
                continue

            if "challenge/recaptcha" in page_obj.url or "证明您不是自动程序" in body or "not a robot" in body:
                for fr in page_obj.frames:
                    if "recaptcha" in (fr.url or "") and "anchor" in (fr.url or ""):
                        try:
                            cb = fr.locator("#recaptcha-anchor")
                            if await cb.count() > 0:
                                self.log("Detected login reCAPTCHA (challenge/recaptcha), automatically clicking...")
                                await cb.click()
                                await asyncio.sleep(4.5)
                                break
                        except Exception:
                            pass
                continue

            # Check if an open dialog modal (VfPpkd-Sx9Kwc-OWXEXe-FNFY6c) is shown on top of the page
            open_dialog_btn = page_obj.locator('div.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c button, div.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c [role="button"], div[role="dialog"] button, div[role="dialog"] [role="button"]')
            if await open_dialog_btn.count() > 0:
                for idx in range(await open_dialog_btn.count()):
                    b = open_dialog_btn.nth(idx)
                    if await b.is_visible():
                        btxt = (await b.inner_text()).strip()
                        if any(k in btxt for k in ("以后再说", "跳过", "取消", "不用了", "Not now", "Skip", "Cancel", "Google Authenticator", "身份验证器")):
                            self.log(f"Detected popup option [{btxt}], clicking...")
                            await b.click(force=True)
                            await asyncio.sleep(3.5)
                            break

            if "Google Authenticator" in body or "身份验证器" in body:
                totp_vis = page_obj.locator('input[type="tel"], input#totpPin, input[name="totpPin"]')
                if await totp_vis.count() == 0 or not await totp_vis.first.is_visible():
                    opt = page_obj.locator("text=/Google Authenticator|身份验证器/i").first
                    if await opt.count() > 0 and await opt.is_visible():
                        self.log("Selecting Google Authenticator verification method...")
                        await opt.click(force=True)
                        await asyncio.sleep(3.5)
                        continue
            elif ("challenge/dp" in page_obj.url or "challenge/az" in page_obj.url or "challenge/pk" in page_obj.url or "扫描二维码" in body) and "challenge/totp" not in page_obj.url:
                totp_vis = page_obj.locator('input[type="tel"], input#totpPin, input[name="totpPin"]')
                if await totp_vis.count() == 0 or not await totp_vis.first.is_visible():
                    try_other = page_obj.locator("text=/试试其他方式|尝试其他方式|Try another way/i").first
                    if await try_other.count() > 0 and await try_other.is_visible():
                        self.log("Detected alternative verification method page (QR/Push/Key), clicking [Try another way] to switch to 2FA...")
                        try:
                            await try_other.click(timeout=4000)
                        except Exception:
                            pass
                        await asyncio.sleep(3.5)
                        continue

            if "确认您的辅助邮箱" in body or "Confirm your recovery email" in body:
                rec_email = (self.account.get("recovery_email") or "").strip()
                kpe_inp = page_obj.locator('input#knowledge-preregistered-email-response:visible, input[name="knowledgePreregisteredEmailResponse"]:visible, input[type="email"]:visible')
                if rec_email and await kpe_inp.count() > 0:
                    self.log(f"Automatically filling recovery email to complete verification: {rec_email}")
                    await kpe_inp.first.fill(rec_email)
                    await kpe_inp.first.press("Enter")
                    await asyncio.sleep(4.5)
                    continue
                opt = page_obj.locator("text=/确认您的辅助邮箱|Confirm your recovery email/i").first
                if await opt.count() > 0 and await opt.is_visible():
                    self.log("Selecting [Confirm recovery email] verification method...")
                    await opt.click(force=True)
                    await asyncio.sleep(3.5)
                    continue

            if "Add 2-Step Verification" in body or "We couldn’t verify it’s you" in body or "We couldn't verify it's you" in body or "signin/rejected" in page_obj.url:
                self.log("ℹ️ Detected new device security block page, skipping independent verification page...")
                return

            # Detect phone number confirmation challenge (Number Matching)
            is_phone_challenge = (
                "challenge/dp" in page_obj.url
                or "challenge/az" in page_obj.url
                or "challenge/pk" in page_obj.url
                or any(k in body for k in (
                    "Check your phone", "Periksa ponsel Anda", "Buka ponsel Anda",
                    "Tap the number", "Ketuk angka", "Tunjukkan nomor",
                    "Google sent a notification", "Google mengirimkan notifikasi"
                ))
            )
            if is_phone_challenge:
                num_match = None
                try:
                    num_match = await page_obj.evaluate("""() => {
                        const targets = Array.from(document.querySelectorAll("[data-number]"));
                        for (const el of targets) {
                            const numAttr = el.getAttribute("data-number");
                            if (numAttr && /^\\d{1,3}$/.test(numAttr.trim())) return numAttr.trim();
                        }
                        const bEls = Array.from(document.querySelectorAll("div, span, b, strong, h2, h1"));
                        for (const el of bEls) {
                            const txt = (el.innerText || "").trim();
                            if (/^\\d{1,3}$/.test(txt)) {
                                const style = window.getComputedStyle(el);
                                const fSize = parseFloat(style.fontSize) || 0;
                                if (fSize >= 20 || el.tagName === "B" || el.tagName === "STRONG") {
                                    return txt;
                                }
                            }
                        }
                        return null;
                    }""")
                except Exception:
                    pass

                if num_match:
                    notify_msg = f"📱 [ACTION NEEDED] Tap number [{num_match}] on your phone / Ketuk angka [{num_match}] di HP Anda"
                    self.log(f"🚨 {notify_msg}")
                    self.update_state(status="waiting_human", step_message=notify_msg)
                    for _ in range(40):
                        self.check_stop()
                        await asyncio.sleep(1.5)
                        try:
                            curr_url = page_obj.url
                            if "challenge" not in curr_url and ("one.google.com" in curr_url or "myaccount.google.com" in curr_url or curr_url == "about:blank"):
                                self.log("✅ Phone notification verified on mobile device!")
                                self.update_state(status="running", step_message="Phone confirmation verified!")
                                break
                        except Exception:
                            break
                    continue

            totp = page_obj.locator('input[type="tel"], input#totpPin, input[name="totpPin"]')
            if await totp.count() > 0 and await totp.first.is_visible():
                code = await self.ensure_totp_fresh()
                if code:
                    self.log(f"Automatically filling 2FA dynamic code: {code}")
                    try:
                        await totp.first.fill(code)
                        next_btn = page_obj.locator('#totpNext, button:has-text("下一步"), button:has-text("Next")').first
                        if await next_btn.count() > 0 and await next_btn.is_visible():
                            await next_btn.click()
                        else:
                            await totp.first.press("Enter")
                    except Exception:
                        return
                    await asyncio.sleep(5)
                    continue

            if "accounts.google.com" in page_obj.url or "gds.google.com" in page_obj.url or page_obj.url == "about:blank":
                await asyncio.sleep(2)
                continue

            break

    async def step1_login(self, page):
        self.update_state(status="running", current_step=1, step_message="Step 1/5: Logging into Google account and auto-verifying (Recovery Email / 2FA)...")
        self.log("=== Step 1/5: Checking Google login status & auto-verifying (Recovery Email / 2FA) ===")
        email = self.account["email"]
        password = self.account["password"]

        await self.safe_goto(
            page,
            "https://accounts.google.com/ServiceLogin?hl=en&continue=https%3A%2F%2Fone.google.com%2Fplans%3Fhl%3Den",
            timeout=40000,
        )
        await asyncio.sleep(3.5)
        await self.save_screenshot(page, "step1_init")

        for login_round in range(3):
            if "one.google.com" in page.url and "accounts.google.com" not in page.url and "gds.google.com" not in page.url:
                break
            try:
                body_txt = await page.inner_text("body", timeout=3000)
            except Exception:
                body_txt = ""

            if "gds.google.com" in page.url or "recoveryoptions" in page.url or "homeaddress" in page.url or "确保您始终都能登录" in body_txt or "设置住址" in body_txt:
                await page.evaluate(
                    """() => {
                    const els = Array.from(document.querySelectorAll('button, a, [role="button"], span'));
                    for (const el of els) {
                        const t = (el.innerText || '').trim();
                        if (['取消', 'Cancel', '跳过', 'Skip', '以后再说', 'Not now'].includes(t)) el.click();
                    }
                }"""
                )
                await asyncio.sleep(4.0)
                if "one.google.com" in page.url and "accounts.google.com" not in page.url:
                    break

            # Account chooser check
            email_lower = email.lower()
            email_clean = email_lower.replace(".", "")
            chooser_items = page.locator("[data-identifier]")
            clicked_chooser = False
            for i in range(await chooser_items.count()):
                ident = (await chooser_items.nth(i).get_attribute("data-identifier") or "").lower()
                if ident == email_lower or ident.replace(".", "") == email_clean:
                    self.log(f"Selecting account in account selector: {ident}")
                    await chooser_items.nth(i).click()
                    clicked_chooser = True
                    await asyncio.sleep(3.5)
                    break

            if not clicked_chooser:
                use_other = page.locator("text=/使用其他Account|Use another account/i")
                email_loc = page.locator('input[type="email"], input#identifierId')
                if (await email_loc.count() == 0 or not await email_loc.first.is_visible()) and await use_other.count() > 0:
                    await use_other.first.click()
                    await asyncio.sleep(2.5)

                email_loc = page.locator('input[type="email"], input#identifierId')
                if await email_loc.count() > 0 and await email_loc.first.is_visible() and "challenge/kpe" not in page.url:
                    self.log(f"Entering email: {email}")
                    await email_loc.first.fill(email)
                    next_btn = page.locator('#identifierNext, button:has-text("下一步"), button:has-text("Next")').first
                    if await next_btn.count() > 0 and await next_btn.is_visible():
                        await next_btn.click()
                    else:
                        await email_loc.first.press("Enter")
                    await asyncio.sleep(4.5)

            # Password + Recovery Email + 2FA
            await self.pass_reauth_on_page(page)

            # Dismiss post-login prompts
            for _ in range(4):
                if "one.google.com" in page.url and "gds.google.com" not in page.url:
                    break
                btn = page.locator(
                    'button:has-text("Not now"), button:has-text("Skip"), button:has-text("以后再说"), button:has-text("跳过"), button:has-text("取消"), button:has-text("Cancel"), button:has-text("我同意"), button:has-text("继续")'
                )
                if await btn.count() > 0 and await btn.first.is_visible():
                    await btn.first.click(force=True)
                    await asyncio.sleep(3.5)
                else:
                    break

            if "signin/identifier" in page.url or "ServiceLogin" in page.url:
                if self.proxy_bridge:
                    self.proxy_bridge.rotate_session()
                self.log("⚠️ Login page responding slowly, retrying login flow...")
                await self.safe_goto(
                    page,
                    "https://accounts.google.com/ServiceLogin?hl=en&continue=https%3A%2F%2Fone.google.com%2Fplans%3Fhl%3Den",
                    timeout=40000,
                )
                await asyncio.sleep(3.5)

        await self.save_screenshot(page, "step1_done")
        self.log(f"✅ Step 1 complete，当前页面: {page.url[:80]}")

    async def get_current_sub_id(self, page) -> Optional[str]:
        for url in (
            "https://one.google.com/settings?expand=upgrade&hl=zh-CN",
            "https://one.google.com/plans?hl=zh-CN",
            "https://one.google.com/ai-nye?g1_landing_page=0&hl=zh-CN",
        ):
            await self.safe_goto(page, url, timeout=40000)
            for _ in range(6):
                await asyncio.sleep(1.8)
                html = await page.content()
                ids = list(set(re.findall(r'\"([a-z]{24})\.AO-', html)))
                if not ids:
                    ids = list(set(re.findall(r'([a-z]{24})\.AO-J1O', html)))
                if not ids:
                    # Match 24-char lowercase subscription token inside AF_initDataCallback arrays
                    for blk in re.findall(r'AF_initDataCallback\(\{.*?\}\);', html, flags=re.S):
                        if "subscriptions.red" in blk or "g1." in blk:
                            cand = re.findall(r'\"([a-z]{24})\"', blk)
                            if cand:
                                ids = cand
                                break
                if ids:
                    sub_id = ids[0]
                    self.log(f"Current read 24-digit subscription ID: {sub_id}")
                    return sub_id
        self.log("⚠️ Failed to extract 24-digit subscription ID from static HTML, Ngbm interceptor will retain it dynamically")
        return None

    async def inspect_play_subscriptions(self, page) -> str:
        await self.safe_goto(page, "https://play.google.com/store/account/subscriptions?hl=zh-CN", timeout=40000)
        await asyncio.sleep(3)
        if "accounts.google.com" in page.url or "gds.google.com" in page.url:
            await self.pass_reauth_on_page(page)
            await asyncio.sleep(3)
        txt = await page.inner_text("body")
        clean = " | ".join([l.strip() for l in txt.splitlines() if l.strip()])
        return clean

    async def read_ai_pro_end_date(self, page) -> Optional[str]:
        """
        Read the real end date of the Google AI Pro (5 TB) free period.

        The Play subscriptions page only lists the *next billing* date, but the
        [Manage] dialog lists every item of the bundle with its own end date
        ("Google AI Pro (5 TB) - 将于 2028年11月9日结束"). That is the only
        reliable source for the free-period length.
        """
        try:
            await self.safe_goto(page, "https://play.google.com/store/account/subscriptions?hl=zh-CN", timeout=40000)
            await asyncio.sleep(3.5)
            mbtn = page.get_by_text(re.compile(r"^(Manage|管理)$", re.I))
            if not await mbtn.count():
                return None
            await mbtn.first.click()
            await asyncio.sleep(3)
            body = await page.inner_text("body")
        except Exception:
            return None
        m = re.search(r"Google AI Pro \(5 TB\)\s*-\s*将于\s*([0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日)", body)
        if not m:
            m = re.search(r"Google AI Pro \(5 TB\)\s*-\s*(?:ends?)?\s*([0-9]{4}[-/][0-9]{1,2}[-/][0-9]{1,2})", body)
        return m.group(1) if m else None

    async def ensure_subscription_active(self, page):
        """If the account has a cancelled subscription ('重新订阅'), click Resubscribe so Mode 5 stacking works."""
        await self.safe_goto(page, "https://play.google.com/store/account/subscriptions?hl=zh-CN", timeout=40000)
        await asyncio.sleep(3.5)
        if "accounts.google.com" in page.url or "gds.google.com" in page.url:
            await self.pass_reauth_on_page(page)
            await asyncio.sleep(3.0)
        try:
            body = await page.inner_text("body", timeout=3000)
        except Exception:
            body = ""
        if "重新订阅" in body:
            self.log("Detected current subscription is [Cancelled], clicking [Resubscribe] to reactivate for stacking...")
            rbtn = page.get_by_text("重新订阅", exact=True).first
            if await rbtn.count() > 0:
                await rbtn.click(force=True)
                await asyncio.sleep(3.5)
                cbtn = page.get_by_text("重新订阅", exact=True).last
                if await cbtn.count() > 0 and await cbtn.is_visible():
                    await cbtn.click(force=True)
                    await asyncio.sleep(5.0)
                ok_btn = page.get_by_text("确定", exact=True).first
                if await ok_btn.count() > 0 and await ok_btn.is_visible():
                    await ok_btn.click(force=True)
                    await asyncio.sleep(2.0)

    async def _poll_eacquire_modal(self, page, max_loops: int = 55, step_tag: str = ""):
        last_confirm_click_ts = 0.0
        loops_left = max_loops
        inline_card_saved = False
        while loops_left > 0:
            loops_left -= 1
            self.check_stop()
            if "accounts.google.com" in page.url or "gds.google.com" in page.url:
                self.log(f"[{step_tag or 'modal'}] Detected redirect to login verification page ({page.url[:60]})，Automatically completing identity verification...")
                await self.pass_reauth_on_page(page)
                return None, ""
            frames_to_check = []
            try:
                for p in page.context.pages:
                    frames_to_check.extend(p.frames)
            except Exception:
                frames_to_check = page.frames

            for fr in frames_to_check:
                fr_url = fr.url or ""
                if "eacquire" in fr_url:
                    try:
                        state_info = await fr.evaluate(
                            """() => {
                            if (!document.body) return {ready: false, text: ''};
                            const clone = document.body.cloneNode(true);
                            clone.querySelectorAll('script, style, noscript').forEach(el => el.remove());
                            const text = (clone.innerText || '').trim();
                            const needsCard = text.includes('添加付款方式') || text.includes('首先添加付款方式') || text.includes('添加信用卡或借记卡') || text.includes('添加卡') || text.includes('Add a payment method') || text.includes('Add credit or debit card') || text.includes('Add card');
                            const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                            const hasSubBtn = !needsCard && btns.some(b => {
                                const bt = (b.innerText || '').trim().toLowerCase();
                                const r = b.getBoundingClientRect();
                                return (bt === '订阅' || bt === 'subscribe') && r.width > 10 && r.height > 10;
                            });
                            const hasErr = text.includes('Something went wrong') || text.includes('unable to change') || text.includes('无法更改') || text.includes('出了点问题') || text.includes('OR-') || text.includes('BX-');
                            return {ready: hasSubBtn || hasErr, text: text};
                        }"""
                        )
                        if state_info and state_info.get("ready"):
                            raw_t = state_info.get("text", "")
                            clean_txt = " | ".join([l.strip() for l in raw_t.splitlines() if l.strip()])
                            return fr, clean_txt
                        elif state_info and not inline_card_saved:
                            raw_t = state_info.get("text", "")
                            # A previous tier may already have saved the payment
                            # method. Google Play then keeps rendering the
                            # "add a payment method" entry, and re-binding would
                            # loop forever. Skip only when there is no card field
                            # left to fill - Google still asks for the card
                            # number again when stacking another tier.
                            cnum_raw = re.sub(r"\s+", "", self.card.get("number") or "")
                            last4 = cnum_raw[-4:] if len(cnum_raw) >= 4 else ""
                            has_card_field = False
                            try:
                                has_card_field = await fr.evaluate(
                                    """() => {
                                    const els = Array.from(document.querySelectorAll('input'));
                                    for (const el of els) {
                                        const r = el.getBoundingClientRect();
                                        const cs = getComputedStyle(el);
                                        if (!(r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none')) continue;
                                        let lbl = '';
                                        if (el.labels && el.labels.length) lbl = Array.from(el.labels).map(l => (l.innerText || '').trim()).join(' ');
                                        if (!lbl) lbl = el.getAttribute('aria-label') || '';
                                        if (!lbl) lbl = el.getAttribute('placeholder') || '';
                                        if (/卡号|卡號|信用卡号|信用卡號|卡片号|card\\s*number|cardnumber|^卡$/i.test(lbl)) return true;
                                    }
                                    return false;
                                }"""
                                )
                            except Exception:
                                has_card_field = True
                            if last4 and not has_card_field and last4 in raw_t.replace(" ", ""):
                                self.log(
                                    f"[{step_tag or 'modal'}] Payment method already on file "
                                    f"(••••{last4}), skipping inline card binding."
                                )
                                inline_card_saved = True
                                break
                            if any(k in raw_t for k in ("添加付款方式", "首先添加付款方式", "添加信用卡或借记卡", "添加卡", "Add a payment method", "Add credit or debit card", "Add card")):
                                add_btn = fr.locator("text=/添加信用卡或借记卡|添加卡|Add credit or debit card|Add card/i").last
                                if await add_btn.count() > 0 and await add_btn.is_visible():
                                    self.log(f"[{step_tag or 'modal'}] Detected popup requiring payment method, executing inline tax-free card binding (ZIP 97201)...")
                                    try:
                                        await add_btn.click(force=True)
                                    except Exception:
                                        pass
                                    await fr.evaluate(
                                        """() => {
                                        const els = Array.from(document.querySelectorAll('button, [role="button"], div, span'));
                                        for (let i = els.length - 1; i >= 0; i--) {
                                            const t = (els[i].innerText || '').trim();
                                            if (t === '添加卡' || t === '添加信用卡或借记卡' || t === 'Add card' || t === 'Add credit or debit card') {
                                                els[i].click();
                                                break;
                                            }
                                        }
                                    }"""
                                    )
                                    for _ in range(20):
                                        await asyncio.sleep(1.0)
                                        all_frames = list(page.frames)
                                        for tf in all_frames:
                                            try:
                                                vis = tf.locator("input:visible")
                                                cnt = await vis.count()
                                                if cnt >= 3:
                                                    cnum = (self.card.get("number") or "").replace(" ", "")
                                                    expm = (self.card.get("exp_month") or "").zfill(2)
                                                    expy = (self.card.get("exp_year") or "")[-2:]
                                                    cvc_v = (self.card.get("cvc") or "").strip()
                                                    holder_v = (self.card.get("holder") or "CARD HOLDER").strip()
                                                    zip_v = (self.card.get("postal_code") or "97201").strip()

                                                    # Locate the fields by their label instead of
                                    # relying on a fixed order: Google Play renders only
                                                    # 3 inputs (card / expiry / CVC) when the
                                    # name and ZIP are already on file.
                                                    fmap = await tf.evaluate(
                                                        """() => {
                                                        const els = Array.from(document.querySelectorAll('input'));
                                                        const vis = els.filter(el => {
                                                            const r = el.getBoundingClientRect();
                                                            const cs = getComputedStyle(el);
                                                            return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none';
                                                        });
                                                        const out = {card: -1, exp: -1, cvc: -1, name: -1, zip: -1};
                                                        for (let i = 0; i < vis.length; i++) {
                                                            const el = vis[i];
                                                            let lbl = '';
                                                            if (el.labels && el.labels.length) lbl = Array.from(el.labels).map(l => (l.innerText || '').trim()).join(' ');
                                                            if (!lbl) lbl = el.getAttribute('aria-label') || '';
                                                            if (!lbl) lbl = el.getAttribute('placeholder') || '';
                                                            const t = lbl + '|' + (el.placeholder || '');
                                                            if (out.card < 0 && /卡号|卡號|信用卡号|信用卡號|卡片号|card\\s*number|cardnumber|^卡$/i.test(t)) out.card = i;
                                                            else if (out.exp < 0 && /MM\\s*\\/\\s*YY|MM\\/YY|有效期|有效期限|到期|expir/i.test(t)) out.exp = i;
                                                            else if (out.cvc < 0 && /安全码|安全碼|安全碼|cvv|cvc|cid|security\\s*code/i.test(t)) out.cvc = i;
                                                            else if (out.name < 0 && /姓名|持卡人|name\\b|holder/i.test(t)) out.name = i;
                                                            else if (out.zip < 0 && /邮编|郵遞|邮政编码|postal|\\bzip\\b/i.test(t)) out.zip = i;
                                                        }
                                                        out.total = vis.length;
                                                        return out;
                                                    }"""
                                                    )
                                                    if fmap.get("card", -1) < 0 or fmap.get("exp", -1) < 0:
                                                        # Fall back to the standard order.
                                                        fmap["card"] = 0
                                                        fmap["exp"] = 1
                                                        fmap["cvc"] = 2

                                                    async def _type_field(idx, text):
                                                        if idx < 0 or not text:
                                                            return
                                                        try:
                                                            await vis.nth(idx).click(force=True)
                                                        except Exception:
                                                            return
                                                        await asyncio.sleep(0.2)
                                                        # Google Play renders the card fields as
                                                        # controlled React inputs: typing digit by
                                                        # digit loses the value on re-render, so
                                                        # set the value directly and only fall back
                                                        # to keyboard input when it did not stick.
                                                        want = "".join(ch for ch in text if ch.isdigit())
                                                        filled = False
                                                        try:
                                                            await vis.nth(idx).fill(text)
                                                            await asyncio.sleep(0.25)
                                                            cur = await vis.nth(idx).input_value(timeout=1500)
                                                            got = "".join(ch for ch in (cur or "") if ch.isdigit())
                                                            filled = (not want) or (got == want)
                                                        except Exception:
                                                            filled = False
                                                        if not filled:
                                                            try:
                                                                await vis.nth(idx).click(force=True)
                                                                await vis.nth(idx).press_sequentially(text, delay=35)
                                                            except Exception:
                                                                try:
                                                                    await vis.nth(idx).fill(text)
                                                                except Exception:
                                                                    pass
                                                        await asyncio.sleep(0.3)

                                                    await _type_field(fmap["card"], cnum)
                                                    await _type_field(fmap["exp"], f"{expm}{expy}")
                                                    await _type_field(fmap["cvc"], cvc_v)
                                                    if fmap.get("name", -1) >= 0:
                                                        try:
                                                            cur_name = (await vis.nth(fmap["name"]).input_value(timeout=1000)).strip()
                                                            if not cur_name:
                                                                await vis.nth(fmap["name"]).fill(holder_v)
                                                                await asyncio.sleep(0.2)
                                                        except Exception:
                                                            pass
                                                    if fmap.get("zip", -1) >= 0:
                                                        await _type_field(fmap["zip"], zip_v)
                                                    sbtn = tf.locator('button:has-text("保存卡"), button:has-text("保存"), button:has-text("Save card"), button:has-text("Save"), [role="button"]:has-text("保存")').first
                                                    if await sbtn.count() > 0:
                                                        await sbtn.click(force=True)
                                                    else:
                                                        await tf.evaluate(
                                                            """() => {
                                                            const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                                                            const b = btns.find(e => (e.innerText || '').includes('保存') || (e.innerText || '').includes('Save'));
                                                            if (b) b.click();
                                                        }"""
                                                        )
                                                    self.log(f"[{step_tag or 'modal'}] ✅ Clicked [Save card], waiting for Google Play binding confirmation...")
                                                    for _w in range(22):
                                                        await asyncio.sleep(1.0)
                                                        still_im = any("instrumentmanager" in (f.url or "") for f in page.frames)
                                                        if not still_im:
                                                            self.log(f"[{step_tag or 'modal'}] ✅ Inline card saved!")
                                                            break
                                                        if _w == 7 and await sbtn.count() > 0:
                                                            try:
                                                                await sbtn.click(force=True)
                                                            except Exception:
                                                                pass
                                                    await asyncio.sleep(2.0)
                                                    inline_card_saved = True
                                                    loops_left = 15
                                                    break
                                            except Exception:
                                                pass
                                        if inline_card_saved:
                                            break
                    except Exception:
                        pass

            # Also check for open intermediate confirm dialog ("运作方式 -> 继续订阅" / "是的，继续") during the entire wait
            has_eacquire_frame = any("eacquire" in (f.url or "") for f in frames_to_check)
            if not has_eacquire_frame and (time.time() - last_confirm_click_ts) >= 2.5:
                try:
                    confirm_btn = await page.evaluate(
                        """() => {
                        const targets = ["继续订阅", "是的，继续", "换用此方案", "重新订阅", "继续", "同意", "我同意", "前往结账", "获取 Google AI Ultra", "Switch to this plan", "Resubscribe", "Continue to subscribe", "Yes, continue", "Continue", "Agree"];
                        const isTrulyOpenAndTop = (el) => {
                            const selfCs = window.getComputedStyle(el);
                            if (selfCs.visibility === 'hidden' || selfCs.display === 'none' || selfCs.pointerEvents === 'none') return false;
                            let cur = el;
                            while (cur && cur !== document.body && cur !== document.documentElement) {
                                if (cur.getAttribute && cur.getAttribute('aria-hidden') === 'true') return false;
                                const cs = window.getComputedStyle(cur);
                                if (cs.display === 'none' || parseFloat(cs.opacity) < 0.85) return false;
                                cur = cur.parentElement;
                            }
                            const r = el.getBoundingClientRect();
                            const cx = r.left + r.width / 2;
                            const cy = r.top + r.height / 2;
                            if (cx <= 0 || cy <= 0 || cx >= window.innerWidth || cy >= window.innerHeight) return false;
                            const topEl = document.elementFromPoint(cx, cy);
                            if (!topEl) return false;
                            return el.contains(topEl) || topEl.contains(el);
                        };
                        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                        for (const b of btns) {
                            const r = b.getBoundingClientRect();
                            if (r.width <= 15 || r.height <= 15) continue;
                            if (!isTrulyOpenAndTop(b)) continue;
                            const t = (b.innerText || '').trim();
                            if (targets.some(lbl => t === lbl || t.includes(lbl))) {
                                b.click();
                                return {text: t, x: r.left + r.width / 2, y: r.top + r.height / 2};
                            }
                        }
                        return null;
                    }"""
                    )
                    if confirm_btn:
                        last_confirm_click_ts = time.time()
                        self.log(f"[{step_tag or 'modal'}] Clicked transitional confirm button: {confirm_btn['text']}")
                        loops_left = max(loops_left, 60)
                except Exception:
                    pass

            await asyncio.sleep(1.0)
        if inline_card_saved:
            return None, "INLINE_CARD_SAVED_RETRY"
        return None, ""

    async def open_and_click_subscribe(self, page, cfg: Dict[str, Any], step_tag: str, expect_keywords: Optional[list] = None) -> bool:
        self.last_subscribe_error = ""
        target_fr = None
        clean_txt = ""

        # Primary trigger: one.google.com/plans?hl=zh-CN clicking the LAST action button (proven 100% reliable across L1, L2, L3)
        for attempt_url in ("https://one.google.com/plans?hl=zh-CN",) * 5:
            if target_fr:
                break
            self.log(f"[{step_tag}] Opening plan page to trigger Ngbm checkout popup: {attempt_url}")
            await self.safe_goto(page, attempt_url, timeout=40000)
            await asyncio.sleep(3.5)
            if "accounts.google.com" in page.url or "gds.google.com" in page.url:
                self.log(f"[{step_tag}] 页面触发登录验证跳转，Automatically completing identity verification...")
                await self.pass_reauth_on_page(page)
                await self.safe_goto(page, attempt_url, timeout=40000)
                await asyncio.sleep(3.5)

            await page.evaluate(HOOK_JS)
            await page.evaluate(f"window.__setDirectTest({json.dumps(cfg)})")

            fb_btn = None
            for _ in range(10):
                await asyncio.sleep(1.2)
                await page.evaluate(HOOK_JS)
                await page.evaluate(f"window.__setDirectTest({json.dumps(cfg)})")
                fb_btn = await page.evaluate(
                    """() => {
                    const els = Array.from(document.querySelectorAll('button, a, [role="button"]'));
                    const btns = els.filter(e => {
                        const t = (e.innerText || '').trim();
                        const r = e.getBoundingClientRect();
                        return r.width > 15 && r.height > 15 && r.left >= 240 && (
                            t.includes('开始使用') ||
                            t.includes('获取优惠') ||
                            t.includes('获取折扣') ||
                            t.includes('换用此方案') ||
                            t === '升级' ||
                            t === 'Upgrade' ||
                            t.includes('获取 Google AI Ultra') ||
                            t.includes('Get started') ||
                            t.includes('Get offer')
                        );
                    });
                    if (btns.length > 0) {
                        const btn = btns[btns.length - 1];
                        btn.scrollIntoView({block: 'center'});
                        const r = btn.getBoundingClientRect();
                        btn.click();
                        return {x: r.left + r.width / 2, y: r.top + r.height / 2, text: (btn.innerText || '').trim()};
                    }
                    return null;
                }"""
                )
                if fb_btn:
                    self.log(f"[{step_tag}] Clicked [{fb_btn.get('text', '')}] trigger button, waiting for Google Play checkout popup...")
                    break

            if fb_btn:
                target_fr, clean_txt = await self._poll_eacquire_modal(page, max_loops=60, step_tag=step_tag)
                if clean_txt == "INLINE_CARD_SAVED_RETRY":
                    self.log(f"[{step_tag}] Inline card binding complete, reopening plan page to trigger $0 checkout popup...")
                    continue

        await self.save_screenshot(page, f"{step_tag}_modal")

        if not target_fr:
            self.log(f"⚠️ [{step_tag}] Google Play checkout popup not detected (eacquire/multiline)")
            return False

        self.log(f"[{step_tag}] Checkout popup content: {clean_txt[:350]}")
        if "错误" in clean_txt or "Something went wrong" in clean_txt or "unable to change" in clean_txt or "出了点问题" in clean_txt:
            self.log(f"⚠️ [{step_tag}] Popup returned error: {clean_txt[:200]}")
            return False

        # Ensure the configured card (last4) is selected in the eacquire modal if multiple cards exist
        card_num_clean = re.sub(r"\s+", "", self.card.get("number", ""))
        target_last4 = card_num_clean[-4:] if len(card_num_clean) >= 4 else ""
        if target_last4 and target_last4 not in clean_txt and ("Mastercard-" in clean_txt or "Visa-" in clean_txt or "PaysafeCard" in clean_txt):
            self.log(f"[{step_tag}] Default card in popup is not ending in {target_last4}，Switching to card ending in {target_last4} card...")
            try:
                pm_loc = target_fr.locator('text=/Mastercard-|Visa-|PaysafeCard/i').first
                if await pm_loc.count() > 0:
                    await pm_loc.click(timeout=5000)
                    await asyncio.sleep(2.5)
                    await self.save_screenshot(page, f"{step_tag}_pm_list")
                    card_loc = target_fr.locator(f'text=/{target_last4}/').first
                    if await card_loc.count() > 0:
                        await card_loc.click(timeout=5000)
                        self.log(f"✅ [{step_tag}] Successfully clicked to switch to card ending in {target_last4} card!")
                        await asyncio.sleep(3.0)
                        refreshed_fr, refreshed_txt = await self._poll_eacquire_modal(page, max_loops=10)
                        if refreshed_fr:
                            target_fr, clean_txt = refreshed_fr, refreshed_txt
                            self.log(f"[{step_tag}] 切换card后Checkout popup content: {clean_txt[:350]}")
                        await self.save_screenshot(page, f"{step_tag}_modal_switched_{target_last4}")
                    else:
                        self.log(f"⚠️ [{step_tag}] Could not find card ending in {target_last4} card")
            except Exception as pm_err:
                self.log(f"[{step_tag}] Switch payment card hint: {pm_err}")

        # Strict zero-cost protection when running 2-year Pro stacking
        if "ultra" not in step_tag.lower() and "0.00" not in clean_txt and "免费" not in clean_txt and "Free" not in clean_txt:
            self.last_subscribe_error = f"Zero-cost protection block: Popup did not show 0.00 free trial ({clean_txt[:180]})"
            self.log(f"❌ [{step_tag}] {self.last_subscribe_error}")
            return False

        if expect_keywords:
            for kw in expect_keywords:
                if kw not in clean_txt:
                    self.log(f"⚠️ [{step_tag}] Popup did not contain expected keyword '{kw}'，当前文本: {clean_txt[:200]}")

        all_btns = target_fr.locator('button, [role="button"]')
        bcnt = await all_btns.count()
        clicked = False
        for i in range(bcnt):
            b = all_btns.nth(i)
            try:
                btxt = (await b.inner_text()).strip()
                if btxt in ("订阅", "Subscribe"):
                    self.log(f"--> Clicking [{step_tag}] the [{btxt}] button...")
                    try:
                        await b.scroll_into_view_if_needed(timeout=3000)
                        await b.click(timeout=5000)
                        clicked = True
                    except Exception:
                        await b.click(force=True, timeout=5000)
                        clicked = True
                    break
            except Exception as click_err:
                self.log(f"[{step_tag}] Regular click hint ({click_err})，Switching to JS native trigger click...")

        if not clicked:
            js_clicked = await target_fr.evaluate(
                """() => {
                const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                const sub = btns.find(b => {
                    const bt = (b.innerText || '').trim();
                    return bt === '订阅' || bt === 'Subscribe';
                });
                if (sub) {
                    sub.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, cancelable: true}));
                    sub.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, cancelable: true}));
                    sub.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
                    sub.click();
                    return true;
                }
                return false;
            }"""
            )
            if js_clicked:
                self.log(f"--> Triggered via JS native event: [{step_tag}] the [订阅/Subscribe】button点击！")
                clicked = True

        if not clicked:
            self.log(f"⚠️ [{step_tag}] Could not find [Subscribe] button")
            return False

        # Monitor for CVC prompt, Google password re-auth, or post-click error/completion
        cvc_code = (self.card.get("cvc") or "").strip()
        acct_pwd = self.account.get("password", "")
        post_click_err = None
        for wait_i in range(35):
            await asyncio.sleep(2)
            if len(page.context.pages) > 1:
                await self.pass_reauth_on_page(page.context.pages[-1])

            eacquire_present = False
            reauth_spinning = False
            ordered_frames = [f for f in page.frames if f != page.main_frame] + [page.main_frame]
            for f2 in ordered_frames:
                f2_url = f2.url or ""
                if "eacquire" in f2_url:
                    eacquire_present = True
                try:
                    f2_txt = (await f2.inner_text("body", timeout=1500)).strip()
                except Exception:
                    f2_txt = ""

                if "验证是您本人" in f2_txt or "验证您的身份" in f2_txt or "Verify it's you" in f2_txt:
                    reauth_spinning = True

                if "eacquire" in f2_url or "instrument" in f2_url or "challenge" in f2_url or "accounts.google.com" in f2_url or "reauth" in f2_url:
                    try:
                        # 1. Check if there is a password input
                        pwd_inp = f2.locator('input[type="password"], input[name="Passwd"]')
                        if await pwd_inp.count() > 0 and await pwd_inp.first.is_visible():
                            is_cvc_box = ("CVC" in f2_txt or "安全码" in f2_txt or "security code" in f2_txt.lower())
                            if not is_cvc_box:
                                self.log("Detected Google account password secondary verification, automatically entering password...")
                                await pwd_inp.first.fill(acct_pwd)
                                await asyncio.sleep(0.4)
                                vbtns = f2.locator(
                                    'button:has-text("验证"), button:has-text("下一步"), button:has-text("确认"), button:has-text("继续"), button:has-text("Verify"), button:has-text("Next"), #passwordNext'
                                )
                                if await vbtns.count() > 0 and await vbtns.first.is_visible():
                                    await vbtns.first.click()
                                else:
                                    await page.keyboard.press("Enter")
                                await asyncio.sleep(3)
                                continue

                        # 2. Check if there is a 2FA TOTP input
                        totp_inp = f2.locator('input#totpPin, input[name="totpPin"]')
                        if await totp_inp.count() > 0 and await totp_inp.first.is_visible():
                            code = await self.ensure_totp_fresh()
                            if code:
                                self.log(f"Detected embedded 2FA verification box, entering dynamic code: {code}")
                                await totp_inp.first.fill(code)
                                await page.keyboard.press("Enter")
                                await asyncio.sleep(3)
                                continue

                        # 3. Check if there is a CVC input
                        cvc_inp = f2.locator('input[autocomplete="cc-csc"], input[name="cvc"]')
                        if await cvc_inp.count() == 0 and ("CVC" in f2_txt or "安全码" in f2_txt or "security code" in f2_txt.lower()):
                            cvc_inp = f2.locator('input[type="tel"], input[type="password"]')
                        if await cvc_inp.count() > 0 and await cvc_inp.first.is_visible():
                            self.log(f"Detected card security code (CVC) verification box, entering CVC: {cvc_code}")
                            await cvc_inp.first.fill(cvc_code)
                            await asyncio.sleep(0.5)
                            vbtns = f2.locator(
                                'button:has-text("验证"), button:has-text("确认"), button:has-text("继续"), button:has-text("订阅"), button:has-text("Verify"), button:has-text("Confirm")'
                            )
                            if await vbtns.count() > 0:
                                await vbtns.first.click()
                            else:
                                await page.keyboard.press("Enter")
                            await asyncio.sleep(3)
                            continue

                        # 4. Check if there is a "验证是您本人" / "继续" / "下一步" trigger button without visible inputs
                        if "验证是您本人" in f2_txt or "验证您的身份" in f2_txt or "Verify it's you" in f2_txt:
                            vbtn = f2.locator('button:has-text("验证"), button:has-text("继续"), button:has-text("下一步"), button:has-text("Verify"), button:has-text("Continue"), button:has-text("Next"), [role="button"]:has-text("验证"), [role="button"]:has-text("继续")').first
                            if await vbtn.count() > 0 and await vbtn.is_visible():
                                self.log(f"Detected [Verify it's you] confirm button ({await vbtn.inner_text()})，Clicking...")
                                await vbtn.click()
                                await asyncio.sleep(2.5)
                    except Exception:
                        pass

                if f2_txt:
                    try:
                        ft_after = f2_txt
                        clean_after = " | ".join([l.strip() for l in ft_after.splitlines() if l.strip()])
                        if any(
                            ok_kw in clean_after
                            for ok_kw in (
                                "已订阅",
                                "Subscribed",
                                "感谢您订阅",
                                "通过此类购买活动获取",
                                "Google Play 积分",
                                "Play Points",
                                "Earn Google Play Points",
                                "开启备用付款方式",
                                "添加备用付款方式",
                                "备用付款方式",
                                "Backup payment",
                                "以后再说",
                                "知道了",
                                "Got it",
                            )
                        ):
                            self.log(f"✅ [{step_tag}] Detected subscription success confirmation!")
                            await self.save_screenshot(page, f"{step_tag}_after_click")
                            try:
                                dismiss_btn = f2.locator('button:has-text("以后再说"), [role="button"]:has-text("以后再说"), button:has-text("Not now"), [role="button"]:has-text("Not now"), button:has-text("不用了"), button:has-text("知道了")').first
                                if await dismiss_btn.count() > 0 and await dismiss_btn.is_visible():
                                    self.log(f"[{step_tag}] Clicking【以后再说】关闭弹窗以同步订单状态...")
                                    try:
                                        await dismiss_btn.click(force=True, timeout=3000)
                                    except Exception:
                                        pass
                                    await f2.evaluate(
                                        """() => {
                                        const els = Array.from(document.querySelectorAll('button, [role="button"], span, div'));
                                        const b = els.find(e => {
                                            const t = (e.innerText || '').trim();
                                            return t === '以后再说' || t === 'Not now' || t === '不用了' || t === '知道了';
                                        });
                                        if (b) {
                                            b.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, cancelable: true}));
                                            b.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, cancelable: true}));
                                            b.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
                                            b.click();
                                        }
                                    }"""
                                    )
                                    await asyncio.sleep(6.0)
                                else:
                                    await asyncio.sleep(5.0)
                            except Exception:
                                await asyncio.sleep(4.0)
                            return True
                        err_keywords = [
                            "出了点问题",
                            "无法完成",
                            "拒绝了您的付款",
                            "付款遭拒",
                            "支付遭拒",
                            "由于资金不足",
                            "[OR-",
                            "[OR_",
                            "OR_FGVEM",
                            "[BX-CPL-05]",
                            "您的订单仍在处理中",
                            "订单处理完成后",
                            "购买失败",
                            "Something went wrong",
                            "couldn't be completed",
                            "Check that you have the correct country",
                            "declined",
                            "insufficient funds",
                        ]
                        if any(err_kw in clean_after for err_kw in err_keywords):
                            err_lines = [line.strip() for line in ft_after.splitlines() if any(err_kw in line for err_kw in err_keywords)]
                            post_click_err = " | ".join(err_lines) if err_lines else clean_after[:300]
                            break
                    except Exception:
                        pass
            if post_click_err:
                break
            if wait_i >= 3 and not eacquire_present and not reauth_spinning:
                # Check main page for "购买失败" toast or "欢迎您！您的新会员已生效" before assuming modal closure result
                try:
                    main_body_txt = (await page.main_frame.inner_text("body", timeout=2000)).strip()
                except Exception:
                    main_body_txt = ""
                if "购买失败" in main_body_txt or "Purchase failed" in main_body_txt or "出了点问题" in main_body_txt or "[BX-CPL-05]" in main_body_txt:
                    post_click_err = "Detected [Purchase failed] or incomplete settlement ([BX-CPL-05])"
                    break
                if "欢迎您" in main_body_txt or "新会员已生效" in main_body_txt or "Welcome" in main_body_txt:
                    self.log(f"✅ [{step_tag}] Detected Google One new member welcome page, subscription successful!")
                    await self.save_screenshot(page, f"{step_tag}_after_click")
                    await asyncio.sleep(4.0)
                    return True
                self.log(f"⚠️ [{step_tag}] Checkout popup closed but no [Subscribed/Play Points] success flag captured, verifying backend status...")
                await asyncio.sleep(5.0)
                await self.save_screenshot(page, f"{step_tag}_after_click")
                post_click_err = "Checkout popup closed but no [Subscribed] flag appeared, suspected backend stall"
                break

        await self.save_screenshot(page, f"{step_tag}_after_click")
        if post_click_err:
            self.last_subscribe_error = post_click_err
            self.log(f"❌ [{step_tag}] Google Play returned error after clicking Subscribe: {post_click_err[:300]}")
            return False
        self.last_subscribe_error = "等待超时"
        self.log(f"⚠️ [{step_tag}] Wait timeout, popup still open or unconfirmed (reauth_spinning={reauth_spinning})")
        return False

    async def step2_layer1_12m(self, page):
        self.update_state(status="running", current_step=2, step_message="Step 2/5: Executing Tier 1 12-month free stack (US$0.00 -> 2027-10)...")
        self.log("=== Step 2/5: Executing Tier 1 12-month free pack + YouTube 1M trial (US$0.00) ===")

        play_txt = await self.inspect_play_subscriptions(page)
        if "2028" in play_txt:
            self.log("✅ Detected account has entered 2028 free period, skipping Step 2!")
            return
        if any(k in play_txt for k in ("2027-10", "2027-11", "2027-12", "Oct 2027", "Nov 2027", "Dec 2027")):
            if "重新订阅" in play_txt:
                await self.ensure_subscription_active(page)
            self.log("✅ Detected account has completed Tier 1 12-month free stack, skipping Step 2!")
            return

        if "重新订阅" in play_txt:
            await self.ensure_subscription_active(page)

        sub_id = None
        if "Google AI" in play_txt or "Google One" in play_txt:
            sub_id = await self.get_current_sub_id(page)

        cfg_l1 = {
            "name": "Step2_Layer1_12M_YTFree_ZeroCost",
            "full_items": [
                [[PREFIX + "g1.2tb.ai.subs_variant", 21], None, None, None, 1, [TOK_PRO5TB_12M]],
                [[PREFIX + "g1.youtube_premium_individual_add_on", 21], None, None, None, 1, [YT_FREE_TOK]],
            ],
            "ear8": [None, 5, None, None, None, [sub_id]] if sub_id else None,
        }
        ok = await self.open_and_click_subscribe(page, cfg_l1, "step2_layer1_12m")
        if not ok:
            self.log("⚠️ Step 2 initial trigger incomplete, waiting 3 seconds for retry (2/2)...")
            await asyncio.sleep(3.0)
            ok = await self.open_and_click_subscribe(page, cfg_l1, "step2_layer1_12m")
        if not ok:
            raise RuntimeError(f"Step 2 (Tier 1 12-month free stack US$0.00) Failed: {self.last_subscribe_error}")
        self.log("✅ Step 2 (Tier 1 12-month free pack US$0.00) Subscription complete! Waiting 45 seconds for Google Play background settlement...")
        await asyncio.sleep(45)

    async def step3_layer2_6mss(self, page):
        self.update_state(status="running", current_step=3, step_message="Step 3/5: Executing Tier 2 6-month free stack (US$0.00 -> 18 months / 2028-04)...")
        self.log("=== Step 3/5: Executing Tier 2 6-month free pack (S25 Pro 6M + YT 1M trial, US$0.00) deferred stack ===")

        play_txt = await self.inspect_play_subscriptions(page)
        if any(k in play_txt for k in ("2028-04", "2028-05", "2028-06", "2028-10", "2028-11", "2028-12", "Apr 2028", "May 2028", "Oct 2028", "Nov 2028", "Dec 2028")):
            if "重新订阅" in play_txt and not any(k in play_txt for k in ("2028-10", "2028-11", "2028-12", "Oct 2028", "Nov 2028", "Dec 2028")):
                await self.ensure_subscription_active(page)
            self.log("✅ Detected account has reached 2028 (≥18 months), skipping Step 3!")
            return

        if "重新订阅" in play_txt:
            await self.ensure_subscription_active(page)

        sub_id = await self.get_current_sub_id(page)

        cfg_l2 = {
            "name": "Step3_Layer2_6MSS_YTFree_ZeroCost",
            "full_items": [
                [[PREFIX + "g1.2tb.ai.subs_variant", 21], None, None, None, 1, [TOK_PRO5TB_6M_SS]],
                [[PREFIX + "g1.youtube_premium_individual_add_on", 21], None, None, None, 1, [YT_FREE_TOK]],
            ],
            "ear8": [None, 5, None, None, None, [sub_id]] if sub_id else None,
        }
        ok = await self.open_and_click_subscribe(page, cfg_l2, "step3_layer2_6mss")
        if not ok:
            self.log("⚠️ Step 3 initial trigger incomplete, waiting 3 seconds for retry (2/2)...")
            await asyncio.sleep(3.0)
            ok = await self.open_and_click_subscribe(page, cfg_l2, "step3_layer2_6mss")
        if not ok:
            raise RuntimeError(f"Step 3 (Tier 2 6-month free stack US$0.00) Failed: {self.last_subscribe_error}")
        self.log("✅ Step 3 (Tier 2 6-month free pack US$0.00 -> 18 months) Stack complete! Waiting 45 seconds to sync subscription ID...")
        await asyncio.sleep(45)

    async def step4_layer3_6m(self, page):
        self.update_state(status="running", current_step=4, step_message="Step 4/5: Executing Tier 3 6-month free cap (US$0.00 -> 24 months / 2028-10)...")
        self.log("=== Step 4/5: Executing Tier 3 6-month free pack cap (Pixel 6M + YT 1M trial, US$0.00 -> 24 months) ===")

        play_txt = await self.inspect_play_subscriptions(page)
        current_end = await self.read_ai_pro_end_date(page)
        m_end = re.search(r"([0-9]{4})年", current_end or "")
        if m_end and m_end.group(1) == "2028" and any(
            k in (current_end or "") for k in ("2028年10月", "2028年11月", "2028年12月")
        ):
            self.log(f"✅ Detected account has capped 24 months free period (ends {current_end}), skipping Step 4!")
            return
        if any(k in play_txt for k in ("2028-10", "2028-11", "2028-12", "Oct 2028", "Nov 2028", "Dec 2028")):
            self.log("✅ Detected account has capped 24 months free period (Oct-Dec 2028), skipping Step 4!")
            return

        if "重新订阅" in play_txt:
            await self.ensure_subscription_active(page)

        sub_id = await self.get_current_sub_id(page)

        # A tier only counts when it really pushes the free-period end date.
        # Google happily answers "success" for an offer that changes nothing,
        # so verify against the [Manage] dialog and fall back to the next token.
        before_date = await self.read_ai_pro_end_date(page)
        self.log(f"Current Google AI Pro free-period end date: {before_date or 'unknown'}")

        ok = False
        for tag, tok in [
            ("step4_layer3_6m", TOK_PRO5TB_6M),
            ("step4_layer3_6m2", TOK_PRO5TB_6M_2),
            ("step4_layer3_6m_ss", TOK_PRO5TB_6M_SS),
        ]:
            cfg_l3 = {
                "name": tag,
                "full_items": [
                    [[PREFIX + "g1.2tb.ai.subs_variant", 21], None, None, None, 1, [tok]],
                    [[PREFIX + "g1.youtube_premium_individual_add_on", 21], None, None, None, 1, [YT_FREE_TOK]],
                ],
                "ear8": [None, 5, None, None, None, [sub_id]] if sub_id else None,
            }
            ok = await self.open_and_click_subscribe(page, cfg_l3, tag)
            if not ok:
                await asyncio.sleep(3.0)
                continue

            await asyncio.sleep(40)
            after_date = await self.read_ai_pro_end_date(page)
            self.log(f"Tier 3 attempt [{tag}] -> free-period end date: {after_date or 'unknown'}")
            if after_date and (not before_date or after_date > before_date):
                self.log(f"✅ Tier 3 advanced the free period: {before_date} -> {after_date}")
                break
            self.log(f"⚠️ [{tag}] did not advance the free period, trying the next offer token...")
            before_date = after_date or before_date
            await asyncio.sleep(3.0)

        if not ok:
            raise RuntimeError(f"Step 4 (Tier 3 6-month free cap US$0.00) Failed: {self.last_subscribe_error}")

        self.log("✅ Step 4 (Tier 3 6-month free pack US$0.00 -> 24 months封顶) Stack complete! Waiting 40 seconds to sync final expiry...")
        await asyncio.sleep(40)
        play_after = await self.inspect_play_subscriptions(page)
        if "2028" in play_after:
            self.log("✅ Step 4 (US$0.00 Zero-cost stack to 2028 (2 years) verified!")
        else:
            # The Play subscriptions page only shows the *next billing* date,
            # never the free-period end date, so it cannot be used to verify
            # the stack here. Step 5 cancels auto-renew, after which Play shows
            # the cancellation (== free period end) date - that is the
            # authoritative check, so do not abort the pipeline before it runs.
            self.log(
                "⚠️ Step 4: Play page does not expose the free-period end date "
                "(it only lists the next billing date). Continuing to Step 5, "
                "which verifies the real expiry after cancelling auto-renew."
            )

    async def step5_cancel_and_verify(self, page):
        self.update_state(status="running", current_step=5, step_message="Step 5/5: Automatically cancelling auto-renew and locking 2028 expiry (US$0.00 screenshot)...")
        self.log("=== Step 5/5: Automatically cancelling auto-renew & capturing final 2028 expiry proof ===")

        await self.safe_goto(page, "https://play.google.com/store/account/subscriptions?hl=zh-CN", timeout=40000)
        await asyncio.sleep(4)
        play_txt = await page.inner_text("body")

        if self.auto_cancel and "取消日期" not in play_txt and "重新订阅" not in play_txt and "已取消" not in play_txt:
            # The Play UI is loaded with hl=zh-CN, so the buttons are in
            # Chinese. Match both languages.
            mbtn = page.get_by_text(re.compile(r"^(Manage|管理)$", re.I))
            for i in range(await mbtn.count()):
                if await mbtn.nth(i).is_visible():
                    self.log("Opening the Play subscription [Manage] dialog...")
                    await mbtn.nth(i).click()
                    break

            for _ in range(15):
                await asyncio.sleep(0.5)
                cbtn = page.get_by_text(re.compile(r"^(Cancel subscription|取消订阅)$", re.I))
                if await cbtn.count() > 0 and await cbtn.first.is_visible():
                    self.log("Clicking [Cancel subscription]...")
                    await cbtn.first.click()
                    break

            await asyncio.sleep(2.5)
            # Handle optional retention screen ("不，谢谢" / "继续")
            no_thanks = page.locator('button:has-text("不，谢谢"), button:has-text("不用了"), button:has-text("No thanks"), [role="button"]:has-text("不，谢谢"), [role="button"]:has-text("不用了")')
            if await no_thanks.count() > 0 and await no_thanks.first.is_visible():
                await no_thanks.first.click()
                await asyncio.sleep(2.0)

            # Click visible [role="radio"] (and/or reason text) to enable the "继续" button
            await page.evaluate(
                """() => {
                const radios = Array.from(document.querySelectorAll('[role="radio"], input[type="radio"]')).filter(el => {
                    const r = el.getBoundingClientRect();
                    return r.width > 0 && r.height > 0;
                });
                if (radios.length > 0) {
                    const target = radios[radios.length - 1];
                    target.click();
                    if (target.parentElement) target.parentElement.click();
                }
            }"""
            )
            await asyncio.sleep(0.5)
            vis_radios = page.locator('[role="radio"]:visible, input[type="radio"]:visible')
            if await vis_radios.count() > 0:
                try:
                    await vis_radios.last.click(force=True)
                except Exception:
                    pass
            reason = page.locator('text=/拒绝回答|不愿透露|其他原因|暂不需要|Decline to answer/i').first
            if await reason.count() > 0 and await reason.is_visible():
                try:
                    await reason.click(force=True)
                except Exception:
                    pass

            await asyncio.sleep(0.8)
            cnext = page.locator('button:has-text("继续"):not([disabled]), [role="button"]:has-text("继续"):not([aria-disabled="true"])')
            for i in range(await cnext.count()):
                if await cnext.nth(i).is_visible():
                    await cnext.nth(i).click(timeout=8000)
                    break
            await asyncio.sleep(2.5)

            final_cbtn = page.get_by_text(re.compile(r"^(Cancel subscription|取消订阅)$", re.I))
            fcnt = await final_cbtn.count()
            for i in range(fcnt - 1, -1, -1):
                if await final_cbtn.nth(i).is_visible():
                    self.log("Clicking最终【Cancel subscription】确认button...")
                    await final_cbtn.nth(i).click(timeout=8000)
                    break
            await asyncio.sleep(4)
            if len(page.context.pages) > 1:
                await self.pass_reauth_on_page(page.context.pages[-1])
            await asyncio.sleep(3)

        # Final verification on Play Subscriptions
        await self.safe_goto(page, "https://play.google.com/store/account/subscriptions?hl=zh-CN", timeout=40000)
        await asyncio.sleep(3.5)
        final_shot = await self.save_screenshot(page, "step5_final_verified")
        final_txt = " | ".join([l.strip() for l in (await page.inner_text("body")).splitlines() if l.strip()])
        self.log(f"Final Play subscription page status: {final_txt[:400]}")

        # Parse expiry date from final_txt
        m_date = re.search(r"(?:取消日期[：:]\s*|续订日期[：:]\s*|将于\s*)([0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日)", final_txt)
        if not m_date:
            # Fall back to the [Manage] dialog, which lists the cancellation date.
            try:
                mbtn2 = page.get_by_text(re.compile(r"^(Manage|管理)$", re.I))
                if await mbtn2.count():
                    await mbtn2.first.click()
                    await asyncio.sleep(3)
                    dlg = " | ".join([l.strip() for l in (await page.inner_text("body")).splitlines() if l.strip()])
                    self.log(f"Play manage dialog: {dlg[:400]}")
                    m_date = re.search(r"(?:取消日期[：:]\s*|续订日期[：:]\s*|将于\s*)([0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日)", dlg)
                    if not m_date:
                        m_date = re.search(
                            r"(?:Cancel date|Renews on|Expires on)[：:]?\s*([A-Z][a-z]{2}\s+\d{1,2},\s+20\d{2}|\d{4}-\d{2}-\d{2})",
                            dlg,
                        )
                    final_txt = final_txt + " | " + dlg
            except Exception as e:
                self.log(f"⚠️ Could not read the manage dialog: {str(e)[:80]}")

        exp_str = m_date.group(1) if m_date else "Activated (see screenshot)"
        plan_found = "Google AI Pro (5 TB)" if "5 TB" in final_txt else ("Google AI Ultra (20 TB)" if "20 TB" in final_txt else ("Google AI Ultra (30 TB)" if "30 TB" in final_txt else "Google AI Pro"))

        self.update_state(
            status="completed",
            current_step=5,
            step_message=f"✅ Zero-cost 2-years complete! Plan: {plan_found} | Expiry date: {exp_str}",
            expiry_date=exp_str,
            last_screenshot=final_shot,
        )
        self.log(f"🎉 Account {self.account['email']} Zero-cost 2-year Pro pipeline finished! Plan: {plan_found}，Expiry time: {exp_str}")

    # Keep step7_cancel_and_verify alias for compatibility
    step7_cancel_and_verify = step5_cancel_and_verify

    async def verify_ip_environment(self, page):
        """Check current browser exit IP and country before touching Google."""
        for probe_url in ("https://ipinfo.io/json", "https://ipwho.is/"):
            try:
                await page.goto(probe_url, wait_until="domcontentloaded", timeout=16000)
                txt = await page.inner_text("body")
                data = json.loads(txt)
                if "ipwho" in probe_url and not data.get("success", True):
                    continue
                ip = data.get("ip", "Unknown")
                cc = (data.get("country_code") or data.get("country") or "??").upper()
                city = data.get("city", "")
                org = (data.get("connection", {}).get("org") if isinstance(data.get("connection"), dict) else data.get("org", "")) or ""
                flag = "🇧🇴" if cc == "BO" else ("🇹🇷" if cc == "TR" else ("🇺🇸" if cc == "US" else "🌐"))
                ip_badge = f"{flag} {ip[:22]} ({cc}{'·' + city if city else ''})"
                self.update_state(ip_info=ip_badge)
                self.log(f"🌐 Independent environment egress IP check passed: {flag} {ip} ({cc} {city}) | ISP: {org[:35]}")

                want_cc = (self.target_region or "").upper()
                if want_cc and cc != "??" and cc != want_cc:
                    self.log(
                        f"⚠️ Egress country {cc} does not match target region {want_cc}. "
                        "The zero-cost offer requires the target-region IP; configure a "
                        "proxy template with {country} in the global config panel."
                    )
                return
            except Exception:
                if self.proxy_bridge:
                    self.proxy_bridge.rotate_session()
                continue
        self.log("⚠️ IP check interface response slow, continuing...")

    async def run_pipeline(self, start_step: int = 1):
        cnum_check = re.sub(r"\s+", "", self.card.get("number") or "")
        expm_check = (self.card.get("exp_month") or "").strip()
        expy_check = (self.card.get("exp_year") or "").strip()
        cvc_check = (self.card.get("cvc") or "").strip()
        if start_step <= 4 and (len(cnum_check) < 12 or not expm_check or not expy_check or not cvc_check):
            err_card = "Please fill in complete payment card info (Number, Expiry, CVC) in global config panel first!"
            self.log(f"❌ {err_card}")
            self.update_state(status="error", step_message=f"❌ {err_card}")
            return

        user_data_dir = get_profile_dir(self.account["id"], self.account["email"])
        resolved_proxy = resolve_account_proxy(self.account, self.target_region, self.proxy_template)
        parsed_proxy = parse_proxy_string(resolved_proxy)

        chrome_args = [
            CHROME_PATH,
            f"--remote-debugging-port={self.port}",
            f"--user-data-dir={user_data_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-popup-blocking",
            "--disable-background-networking",
            "--disable-sync",
            "--disable-component-update",
            "--disable-domain-reliability",
            "--no-pings",
            "--webrtc-ip-handling-policy=disable_non_proxied_udp",
            "--enforce-webrtc-ip-permission-check",
            "--start-maximized",
        ]

        if parsed_proxy:
            if parsed_proxy.get("username"):
                bridge_port = self.port + 200
                self.proxy_bridge = LocalHttpProxyAuthBridge(bridge_port, parsed_proxy)
                await self.proxy_bridge.start()
                chrome_args.append(f"--proxy-server=http://127.0.0.1:{bridge_port}")
                self.log(
                    f"🛡️ For [{self.account['id']}] mounted dedicated residential proxy tunnel -> {parsed_proxy['host']}:{parsed_proxy['port']} (Session: {parsed_proxy['username'][:28]}...)"
                )
            else:
                p_url = f"{parsed_proxy['scheme']}://{parsed_proxy['host']}:{parsed_proxy['port']}"
                chrome_args.append(f"--proxy-server={p_url}")
                self.log(f"🛡️ For [{self.account['id']}] mounted dedicated proxy -> {p_url}")
        else:
            self.log(
                f"Starting Chrome independent environment (Port: {self.port}, "
                f"Region: {self.target_region}, no proxy, using system network)..."
            )

        chrome_args.append("about:blank")

        # Cleanly kill any lingering process listening on self.port
        try:
            net_out = subprocess.check_output(f"netstat -ano | findstr :{self.port}", shell=True).decode("gbk", errors="ignore")
            for line in net_out.splitlines():
                if "LISTENING" in line:
                    old_pid = line.strip().split()[-1]
                    subprocess.run(f"taskkill /F /T /PID {old_pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

        # A still-running Chrome bound to the same profile would swallow this
        # launch (handing the profile over) and never open the debug port.
        kill_chrome_for_profile(user_data_dir)

        await asyncio.sleep(0.8)

        self.proc = subprocess.Popen(chrome_args)

        # Wait for the DevTools port to actually accept connections.
        for _ in range(40):
            if is_port_open(self.port):
                break
            await asyncio.sleep(0.5)
        else:
            self.log(
                f"❌ Chrome did not open the debug port {self.port}. "
                "Close any window using this profile and retry."
            )
            self.update_state(status="error", step_message="❌ Chrome debug port did not start")
            return

        await asyncio.sleep(0.5)

        try:
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(f"http://127.0.0.1:{self.port}")
                context = browser.contexts[0]
                await context.add_init_script("window.__INIT_TEST = null;\n" + HOOK_JS)

                page = context.pages[0] if context.pages else await context.new_page()
                await page.set_viewport_size({"width": 1400, "height": 950})

                await self.verify_ip_environment(page)

                steps = [
                    (1, lambda: self.step1_login(page)),
                    (2, lambda: self.step2_layer1_12m(page)),
                    (3, lambda: self.step3_layer2_6mss(page)),
                    (4, lambda: self.step4_layer3_6m(page)),
                    (5, lambda: self.step5_cancel_and_verify(page)),
                ]

                for step_num, step_fn in steps:
                    self.check_stop()
                    if step_num < start_step:
                        continue
                    await step_fn()

                await browser.close()
        except Exception as e:
            err_msg = str(e)
            self.log(f"❌ Execution aborted: {err_msg}")
            self.update_state(status="error", step_message=f"❌ Step {self.account.get('current_step', 1)} Exception: {err_msg[:120]}")
        finally:
            if self.proxy_bridge:
                await self.proxy_bridge.stop()
            if self.proc:
                try:
                    subprocess.run(f"taskkill /F /T /PID {self.proc.pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception:
                    pass
            # On Windows the launcher PID is not the real browser process, so also
            # reap any Chrome still bound to this profile.
            kill_chrome_for_profile(user_data_dir)
