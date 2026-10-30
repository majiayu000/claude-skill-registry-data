---
name: reliable-automation
description: >
  Four proven patterns for reliable automation, extracted from an
  auto-registration stack and generalized: 1) swappable mailbox pool,
  2) OAuth device flow without loopback, 3) anti-detection browser automation
  techniques, 4) bounded retries per stage. Use for tasks with email
  verification, OAuth login and browser automation where it's important not to
  get detected and not to crash.
---

# Reliable Automation — 4 patterns

> Patterns extracted from an auto-registration analysis and generalized. The value is in
> reproducibility, not in the tool itself (mass registration = ToS abuse, we don't do that).

---

## 1. Mailbox pool — swappable source of verification codes

**Essence:** verification codes come from different places (REST API, IMAP, MS Graph).
The registrar/flow should not know where from — only the interface.

**When to apply:** any service with email verification, temp-mail testing, recovery access,
bypassing one-time limits.

```python
class VerificationMailbox(Protocol):
    def wait_for_code(self, timeout: int = 180, interval: int = 3) -> str | None: ...

class MailboxSource(Protocol):
    def create_mailbox(self) -> VerificationMailbox: ...
```

**Implementations:**
- **REST API** (DuckMail-style): `POST /create` with Bearer → get address → poll
  `GET /messages` or `/code` with interval, timeout ~180s.
- **IMAP** (`outlook.office365.com:993`, port 993): login by email+password,
  scan incoming messages across fallback folders (INBOX + 3–4 spares), parse code with regex.
- **MS Graph**: refresh_token → access_token → `GET /v1.0/me/messages`, depth at least 15.

**Gotchas:**
- Account file format: delimiter `----`, NOT `|` — refresh token can contain `|`.
  `email----password----clientId----refreshToken----imap/graph/auto`
- Token could expire — on error from MS return a clear cause
  ("refresh token expired"), not a bare 401.
- Polling — always with interval and total timeout, not sleep at fixture time.

---

## 2. OAuth device flow instead of PKCE loopback (RFC 8628)

**Essence:** environment without a stable callback port (CLI, headless, console) —
not PKCE, but device flow: `device/code` → user authorizes on a page →
we poll the token endpoint.

**When to apply:** CLI clients, scripts, services without a public URL.

```python
import time, requests

ISS = "https://auth.example.com"
CID = "<client-id>"
SCOPE = "openid profile email offline_access api:access"

discovery = requests.get(f"{ISS}/.well-known/openid-configuration").json()
dev = requests.post(discovery["device_authorization_endpoint"],
                    data={"client_id": CID, "scope": SCOPE}).json()
# → to user: open dev["verification_uri_complete"] in browser
deadline = time.time() + dev.get("expires_in", 1800)
interval = max(dev.get("interval", 5), 1)
while time.time() < deadline:
    time.sleep(interval)
    r = requests.post(discovery["token_endpoint"], data={
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "device_code": dev["device_code"], "client_id": CID})
    if r.status_code == 200:
        tok = r.json()  # access_token, refresh_token, id_token
        break
    # else: authorization_pending / slow_down / expired — handle by code
```

**Gotchas:**
- Polling with bounded retries: transport limit (3 consecutive empty errors — stop),
  time limit (30 min), don't loop on `slow_down` without increasing interval.
- If consent page requires submit — with real mouse events:
  `form.requestSubmit()` can give `Invalid action` (button has no `action`).
- Validate endpoints from discovery: only https and trusted host, otherwise fallback.

**Ready module:** a small RFC 8628 client — discovery GET with host validation,
bounded-retry polling, `slow_down` handling, refresh, usable as a CLI and as a
library. Verified against a live discovery document from a public provider.
For an xAI/Grok target the issuer is `https://auth.x.ai`, the scope is
`openid profile email offline_access`, and the client id comes from the provider's
own console — never hardcoded.

---

## 3. Anti-detection browser automation techniques

**Essence:** bots get caught by small fingerprints: click coordinates, shared profiles,
repeating IPs, logs with real data.

**When to apply:** browser automation against captcha/anti-fraud
(DrissionPage, Playwright, CDP).

- **Click coordinates.** CDP emulation gives `screenX/screenY = 0` — this is detected.
  Patch getters in emulation:
  ```js
  (function(){
    Object.defineProperty(MouseEvent.prototype, 'screenX', {
      configurable: true, get(){ return 800 + Math.floor(Math.random()*400); } });
    Object.defineProperty(MouseEvent.prototype, 'screenY', {
      configurable: true, get(){ return 400 + Math.floor(Math.random()*300); } });
  })();
  ```
  Load this script before the page loads.
- **Profile isolation.** Each run — fresh temp profile + `--incognito`.
  Never reuse user-data between "personalities".
- **Proxy rotation without reuse.** Pool of endpoints from file (HOST:PORT / http(s)://),
  each round — random unused, on retry — new. Don't return used ones in the same run.
- **Desensitize logs.** In logs — only masked proxies/tokens/emails.
- **Process management:** kill only own (PID + create_time), not
  `killall chrome`.

**Gotchas:** headless is unstable on Turnstile — visible browser is more reliable;
dismiss cookie banner BEFORE clicking on the form.

---

## 4. Bounded retries per stage

**Essence:** a flow of steps (click → wait → submit). An error in one stage
does NOT restart the entire flow — retry only that stage, with limits.

**When to apply:** any multi-step flow with external dependencies
(network, captcha, email, third-party APIs).

```python
STAGES = ("open_form", "click_signup", "wait_code", "confirm", "wait_session")

def run_flow(max_retries=3):
    for stage in STAGES:
        for attempt in range(1, max_retries + 1):
            try:
                STAGE_HANDLERS[stage]()
                break                    # stage passed → next
            except RetryableError as e:
                if attempt == max_retries:
                    raise FlowFailed(stage, e) from e
                time.sleep(2 ** attempt) # bounded backoff
```

**Rules:**
- Classify errors: retryable (network, captcha-glitch, "not ready") vs terminal
  (service refusal, invalid data) — terminal is not retried.
- Each stage has its own retry limit; total deadline on the entire flow.
- After stopping — clean up: close browser/session, don't leave background processes.
- Stages with names + overlay/progress logic, so you can see where it got stuck.

---

## Source

- The patterns come from a client-independent Python automation stack, split into
  four modules: an OAuth exchange module, a mail-source module (three
  implementations behind one interface), a browser-core module (profile, proxy and
  click handling) and a per-provider flow module that wires them together.
- Attribution for the original analysis lives in the private workspace; the
  generalized form above is what this skill ships.
