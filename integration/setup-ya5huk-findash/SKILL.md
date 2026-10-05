---
name: setup
description: Use when the user says "set up findash", "onboard", "first-time setup", "get findash running", "configure findash", or is installing the plugin for the first time. Runs findash-doctor's safe auto-fixes, prepares the local React dashboard, then guides the human through only the optional integrations they choose — local secrets, Drive OAuth, and bank-scraper browser seeding.
---

# setup

First-time onboarding for findash. You **automate everything safe and local**, then **guide the human** through everything that needs them. You never enter the user's secrets yourself and never run anything that captures their passwords through this session — you tell them exactly what to put where, and they do it. Local financial directories are mode 700 and their files mode 600; `findash-doctor` enforces this through `scripts/harden_permissions.py`.

## Steps

### 1. Run the doctor's auto-fixes

Run the `findash-doctor` skill (diagnose → auto-fix → report). It creates `data/ inbox/ .secrets/`, fixes file modes, installs the React dashboard dependencies, and initializes the DB. It installs bank-scraper dependencies only after the user opts into a bank source. Read its report: the **🚫 Blockers** and **⚠️ Optional** lines are exactly the steps below that the human still has to do. See [`../findash-doctor/SKILL.md`](../findash-doctor/SKILL.md).

### 2. Secrets — one file, filled in by the user

The examples below are deliberately unusable placeholders. Leaving a section
unfinished is equivalent to omitting it: the doctor and runtime require all of
that integration's values to be non-placeholder before enabling it.

Tell the user to create `.secrets/findash` and `chmod 600` it. Give them this single block to paste and edit — they keep only the sections they need:

```ini
# .secrets/findash — chmod 600. Omit any section you don't use.
[drive]
root_folder_id=<from your vault folder's Drive URL: drive.google.com/drive/folders/<ID>>

[hapoalim]
user_code=<your hapoalim user code>
password=<your hapoalim password>

[cal]
username=<your cal username>
password=<your cal password>

[pdf-passwords]
<payslip-filename-pattern>=<password>

[ibkr]
# IBKR auth is the official Interactive Brokers connector you add in Claude (no
# password here). The account IBKR maps onto is resolved automatically by
# /findash:fetch-investments and stored in the DB — nothing to set here.
# account_name=<legacy override only — pre-existing installs>
# account_ids=<comma-separated IBKR account ids>
# base_currency=ILS
```

Then: `chmod 600 .secrets/findash`.

**Do not collect these values in the conversation or write the file yourself** — the user pastes their own secrets in. Drive authorization lives in the Google Drive connector the user adds in Claude (step 3), not here.

**Coming from the old per-file layout?** Legacy `.secrets/{drive,hapoalim,cal,pdf-passwords}` files are **no longer read**. Tell the user to copy each value into the matching `[section]` of `.secrets/findash` and delete the old files — until they do, that integration won't work. Don't move their secrets for them.

### 3. Steps only the human can do

These need a browser or an interactive terminal — you cannot do them, so print the exact commands and let the user run them:

- **Google Drive connector (only after the user chooses Drive):** Drive access is Anthropic's official **Google Drive connector**, added through Claude's own connector directory — no token ever lands in this checkout. In Claude: `+` → **Connectors** → **Add connector** → **Browse connectors**, search **"Google Drive"**, pick it, and sign in with the Google account that owns the vault. Confirm with `/mcp` and restart Claude Code so the session picks it up. Then the user creates the vault folder in Drive and puts its ID in `[drive] root_folder_id`; doctor creates/validates every fixed public vault folder idempotently through the connector. Drive powers manual-drop ingest; without it the full sync still runs degraded, so this step can be deferred.
- **Bank-scraper browser seeding (only if you use fetch):** one interactive run per source to seed the trusted-device cookie:
  ```
  node scripts/fetch_bank.js --company=hapoalim --setup
  node scripts/fetch_bank.js --company=visaCal --setup
  ```
  Log in, complete OTP / CAPTCHA, trust the device, then press Enter. The profile is saved under `~/.cache/findash/chromium-profile/<companyId>/` and reused silently afterward.
  Chromium's sandbox remains enabled. Only inside a trusted isolated container
  running as root, append `--disable-browser-sandbox` if Chromium cannot launch.
- **IBKR portfolio (only if you use Interactive Brokers):** IBKR is **not** a findash MCP server — it's Anthropic's official **Interactive Brokers connector**, added through Claude's own connector directory. It is reachable only from a signed-in Claude session, so the full sync attempts it best-effort and a session without it skips with a warning.
  1. **Add the connector once:** in Claude, `+` → **Connectors** → **Add connector** → **Browse connectors**, search **"ibkr"**, pick **Interactive Brokers (IBKR)** (under *Anthropic & Partners*), and log in with your IBKR credentials. Confirm with `/mcp` (`Interactive Brokers (IBKR) · connected`), and restart Claude Code so the session picks it up.
  2. **Account mapping is automatic.** `fetch-investments` resolves which findash account IBKR
     feeds (attaching to an existing broker when the ledgers clearly match — some brokers are
     IBKR wrappers underneath — creating one for IBKR-only users, asking only when genuinely
     ambiguous) and persists the choice in the DB. There is nothing to configure by hand.
  3. **Pull your trades:** run `/findash:fetch-investments` in an interactive session. It ingests your IBKR trade history onto the mapped account (so you stop screenshotting trades) plus a reconciliation snapshot. It's read-only — deny any tool that would place an order or move funds. The account it maps onto is resolved automatically (see step 2). If you don't use IBKR, skip this entirely.

### 4. Re-run the doctor

Run `findash-doctor` again and confirm it reports all-systems-go (or only optional gaps for features the user doesn't want). Point the user at [`docs/setup.md`](../../docs/setup.md) for the full reference.

Finish with the two independent entry points:

- `/findash:sync-finance-data` — fetch and ingest every configured source.
- `./run_dashboard.sh` — run the localhost React dashboard; its server refreshes market references every 30 minutes.

## Principles

- **You automate the safe, local, idempotent work; the human owns secrets and OAuth.** Never type the user's passwords / tokens for them, never add connectors or run any `--setup` on their behalf (these need a human at a browser), never print secret values.
- **One secrets file.** `.secrets/findash` is the only place findash reads credentials from — there is no per-file fallback.
