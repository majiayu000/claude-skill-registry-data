---
name: signup-agent
description: >-
  Automate account creation on any target domain during bug-bounty work, end to
  end: disposable-inbox creation with the agent-email CLI (the core inbox
  methodology — https://github.com/zaddy6/agent-email), browser-driven signup
  forms (React, Knockout,
  Headless-UI, react-select, intl-tel-input, Knockout wizards), email
  verification (links or codes), onboarding completion incl. file-upload walls,
  and session capture. Use whenever the user wants to "sign up", "create an
  account", "register", "get credentials for", or "use" a target domain while
  hunting — even mid-campaign when a surface is blocked by missing credentials.
  Also handles blocker taxonomy: reCAPTCHA gates, IP-flagged signups, region
  gates — with the exact handoff to ask the user for.
---

# Signup Agent — automated account creation for authorized targets

Prime directive: **only create accounts on targets that are in an authorized
program's scope** (bug bounty program covering the domain, or the user's own
infrastructure). Account creation is normal user activity; security TESTING
still respects the program's scope list — creating an account on a prod host
to test an in-scope staging environment is acceptable, testing the prod host
is not.

## The 6-phase workflow

### Phase 1 — Find the signup path
- Probe common paths: `/signup`, `/register`, `/create-account`, `/users/sign_up`
  (Rails), `/Account/Register` (ASP.NET), `/Applications/CreateAccount` (NEOGOV),
  `/join`, `/start-free-trial`. Check the login page for a "Sign up" / "Create
  account" link — login pages link to registration even when paths differ.
- Identify the framework from the form: React (placeholder-driven inputs),
  Knockout (`data-bind` attrs, "Saving..." indicators), Headless-UI
  (combobox + portal listbox), react-select (`select__control` classes),
  Rails (`authenticity_token` meta), ASP.NET (`__RequestVerificationToken`).

### Phase 2 — Disposable inbox via agent-email (THE core methodology)

The inbox engine for this skill is **agent-email**
(https://github.com/zaddy6/agent-email, npm `@zaddy6/agentemail`) — a Bun CLI
that gives the agent a real disposable inbox powered by Mail.tm. JSON output
everywhere, aliases (`me`/`default`/`active`), and `--wait N` blocking so
scripts never sleep-loop. Full command reference:
`references/agent-email.md`. Install once per machine:

```bash
npm install -g @zaddy6/agentemail   # or: bun install -g @zaddy6/agentemail
agent-email about                    # verify install + version
```

Core loop — one inbox per account:

```bash
agent-email create                          # fresh inbox → {email, password, accountId}
agent-email read me --wait 40               # blocks until mail lands (no sleep loops)
agent-email read me --full --limit 1        # full bodies — ALWAYS --full before parsing
agent-email show me <messageId>             # one specific message
```

- The short `read` listing has NO HTML body — ALWAYS `--full` before extracting
  links/codes.
- `--wait N` makes `read` block until a new message arrives; use it instead of
  shell sleep loops.
- Aliases: any `<email|alias>` slot accepts the raw address, `default`,
  `active`, or `me` — `agent-email read me --full` is the normal call.
- Multi-target campaigns: one inbox per account, managed via the accounts
  subcommands (`accounts list`, `use <email|alias>`,
  `accounts add <email> --password <pwd> --set-default`,
  `accounts remove <email|alias>`) — see references/agent-email.md.
- Config: `~/.config/agent-email/config.json` (override with
  `AGENT_EMAIL_CONFIG=/path/config.json`). Don't delete inboxes
  mid-engagement — verification trails feed audit.log.
- Mail.tm is the upstream provider — respect its terms and attribution.
- Non-inbox paths (user-forwarded mail, manual verification) are FALLBACKS
  only; agent-email is the default for every signup and verification.

### Phase 3 — Fill + submit the form (pick by framework)
Read `references/form-patterns.md` for the exact proven snippets. Rules of thumb:
- **Playwright fill()/selectOption() is the default** — real input events, React
  sees them, values survive re-renders.
- **Native-setter values evaporate on remount** (React controlled inputs revert
  to state). Use only as fallback, and re-verify values after any wait.
- **Headless-UI / react-select dropdowns**: Playwright click often fails
  ("covered"/"no click point"). The proven ladder: (1) Playwright click on the
  VISIBLE display element (placeholder div / control wrapper — never the hidden
  input), (2) real CUA keyboard: click input coords → cua.type filter → cua
  ArrowDown → cua Enter, (3) Tab-navigation from the previous field (real focus).
  A "Something else" survey answer often spawns a mandatory follow-up — prefer
  the specific option.
- **File-upload walls**: construct the file in JS — build Uint8Array → new File
  → DataTransfer → input.files = dt.files → dispatch change. See
  references/form-patterns.md for the minimal-PDF generator.
- **Page re-render churn**: do multi-field fills + submit inside ONE evaluate
  with internal sleeps when values keep evaporating between calls.

### Phase 4 — Email verification
- Retrieve with `agent-email read me --wait 60 --full` (blocks until the
  verification mail lands, returns full bodies ready for parsing).
- Parse the verification email HTML: HTML-unescape, un-wrap `\/`, then extract
  either the confirm link (`/ConfirmAccount?...`, `/verify?token=...`) or the
  code (5-8 digit/uppercase token near "code").
- Links wrapped in tracking redirects (tracking.launchdarkly.com/r/...): find
  the anchor TEXT ("Accept invitation") to pick the right redirect, then open
  the redirect in the browser — it resolves to the real destination.
- Tokens are long (ASP.NET ~464 chars) — extract with the full regex, never
  truncate. Re-extract if a link says "invalid or expired": likely truncated.

### Phase 5 — Onboarding completion
Onboarding walls often gate the real app surface. Iterate: fill each step,
watch for follow-up requirements (survey comboboxes, file uploads, address
lookups), re-inject files after remounts. Track progress by URL — onboarding
steps usually appear in the URL (e.g. /candidate/onboarding/<uuid>).
When a step is genuinely blocked (widget rejects all input), record exactly
what was tried and move to Phase 6.

### Phase 6 — Session capture + records
- Save credentials in the hunt workspace: `<target>/recon/credentials.txt`
  (email, username, password, status) — local only, never paste into reports.
- Inbox inventory: `agent-email accounts list` (JSON) — cross-check against
  credentials.txt so every account maps to a live inbox.
- If automation cannot hold the session, ask the user for "Copy as cURL"
  (F12 → Network → first request → right-click → Copy → Copy as cURL (bash))
  and parse it: `python scripts/parse_curl_cookies.py "<curl>"` — extracts the
  Cookie header for curl replay. Note which domain the session belongs to;
  cookies do NOT transfer across environments (app vs staging are separate).

## Blocker taxonomy — detect, then hand off
| Blocker | Signature | Handoff |
|---|---|---|
| Invisible reCAPTCHA submit gate | recaptcha iframe loads, form fills persist, submit silently aborts, no error | Ask user to complete THAT step in their own browser (human score passes); give them the exact URL + field values |
| reCAPTCHA service unreachable | "Could not connect to the reCAPTCHA service" on page | Reload the page once — transient; if persistent, network-level, hand off |
| reCAPTCHA Enterprise on signup | Submit no-ops silently | Same handoff as invisible reCAPTCHA |
| IP-flagged signup | "Access is temporarily restricted... IP <x>" | User's existing account on another network, or a PAT/token instead of signup |
| Region gate | Trial page renders empty (body < 100 chars), no form fields | Different data source for the same goal (e.g. GitHub instead of Salesforce) |
| Widget rejects all input | 4+ distinct techniques failed on one field | Stop; one user action in their own browser beats an hour of retries |

## Records & hygiene
- Log every signup to the hunt `audit.log`: `[SIGNUP] <domain> <email> created/verified/blocked-<reason>`.
- Credentials stay in the workspace; passwords for test accounts may be
  generated strong (20+ chars) and are disposable.
- Report hygiene: never include test-account passwords in submissions; redact
  any keys/cookies.
