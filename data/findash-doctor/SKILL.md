---
name: findash-doctor
description: Use when the user says "doctor", "finance doctor", "check finance setup", "what's missing", or any "is everything set up?" equivalent. Audits binaries, configs, secrets, npm deps, DB, live Drive connectivity, and Chromium profiles. Auto-fixes safe local gaps and prints exact commands for everything that needs human action.
---

# findash-doctor

You audit setup, fix what's safe, print a short scannable report. **Diagnose → auto-fix → report.** Anything needing the user goes into the report, not into a shell call.

## Where things live

- Run from the project root (the dir holding `CLAUDE.md`, `scripts/`, `docs/`). Paths below are relative.
- Drive root ID: `root_folder_id=…` in `.secrets/findash` under `[drive]` (chmod 600, gitignored).
- Seed script: `scripts/init-db.sql`. npm manifests: `scripts/package.json` (bank fetch) and `dashboard/package.json` (React app).

## Checks

| # | Category | What | Auto-fix? |
|---|---|---|---|
| 1 | Binaries | Python ≥3.10; feature-gated `qpdf` and Node ≥22.13.0 | No |
| 2 | Private state | local dirs exist at mode 700; files under `data/`, `inbox/`, `.secrets/`, plus browser-profile files, are mode 600 | `python3 scripts/harden_permissions.py --include-browser-profile` |
| 3 | Drive connector | when `[drive]` is configured or explicitly selected: the official Google Drive connector's tools are discoverable (ToolSearch by function) in this session | No — print the add-connector steps |
| 4 | Drive root ID | `.secrets/findash` `[drive]` has a non-placeholder `root_folder_id=` | Perms only |
| 5 | Secrets | `.secrets/findash` exists + mode 600; note which `[sections]` are filled | Perms only |
| 6 | Bank npm deps | when `[hapoalim]` or `[cal]` is configured: `scripts/node_modules/` populated and `npm ls --omit=dev` succeeds | `scripts/install_node_deps.sh` |
| 7 | DB | `data/finance.db` exists, passes integrity/FK checks, and is at the current schema version | `python3 scripts/migrate_db.py --init` when missing; `python3 scripts/migrate_db.py` when outdated |
| 8 | Chromium profiles | `~/.cache/findash/chromium-profile/{hapoalim,visaCal}/` (only when matching secrets exist) | No |
| 9 | Drive live + layout | with the connector present: the metadata tool reaches the root from `python3 scripts/drive_root.py`, then every fixed public folder from `docs/drive-layout.md` exists directly under it | Fixed folders only |
| 10 | IBKR connector | optional — the official Interactive Brokers connector is added in Claude (claude.ai), not findash config; sessions without it skip the investments feed | No |
| 11 | React dashboard | `dashboard/node_modules/` populated and `npm --prefix dashboard run build` succeeds | `scripts/install_dashboard_deps.sh` |

Run `python3 scripts/check_config.py` for checks 4–6 and the optional-integration
gates. Its output contains booleans and known section names only—never values.
A section is configured only when every required value is non-empty and not a
setup placeholder; a header by itself does not count.

Versions: parse `node --version` (major ≥23, or major=22 with minor ≥13) and `python3 --version` (≥3.10). Perms: anything with non-zero group/others digit is wrong. For Drive live, resolve the root with `python3 scripts/drive_root.py`, call the connector's metadata tool on that id, then list the root by `parentId` (with `excludeContentSnippets: true`) and compare folder titles against the fixed layout. If the root ID is missing or still a placeholder, skip both and let check #4 own it. Never search outside the vault, call recent-files, or print a vault listing.

Database check (#7): run `python3 scripts/migrate_db.py --check`. A missing database is initialized with `--init`; an outdated populated database is upgraded by running `python3 scripts/migrate_db.py`. Never apply ad-hoc `ALTER TABLE` statements. A migration that reports conflicting same-date balances is a blocker requiring source reconciliation—never pick a value automatically. Verify `PRAGMA foreign_key_check` and `PRAGMA integrity_check` through `scripts/findash_db.py`. If `meta.last_db_backup_at` is older than 14 days, add one ⚠️ line. Apply the same staleness checks to configured sources, using active `account_feeds.provider='ibkr'` rows to decide whether IBKR is onboarded. Every active IBKR feed must point to a non-closed logical account.

Also audit logical-account identity: compare active brokerage accounts' latest holdings and surrounding canonical trades, especially when one account has an IBKR feed. Substantially identical portfolios may be a wrapper and its underlying IBKR account represented twice. Treat a clear duplicate as an accuracy blocker for an interactive `/findash:fetch-investments` reconciliation; never sum it, auto-merge it, or print the matching securities/quantities. Similar amounts or one matching trade are not enough evidence. IBKR connector (#10) remains optional and interactive. Never print account ids, balances, positions, source identifiers, or counterparties.

Audit bank-account transitions too. Multiple same-institution checking rows are an accuracy blocker when their activity does not economically overlap, an exact closing/opening transfer joins their boundary, or pre-boundary manual snapshots on the successor track the predecessor ledger. Treat a bank-renumbering migration as one logical account with separate feeds and recommend the reviewed `reconcile-account` flow. Do not infer identity from a similar balance alone, and never print the private comparison evidence.

Count legacy brokerage `transactions` with `flow_type='investment'` that still lack normalized canonical evidence. Report only the count as a migration warning: where those rows overlap raw trade history, they cannot prove which trade cash they duplicate, so the dashboard preserves the trade-derived legacy treatment and warns. Reconcile them interactively into canonical cash/trade events and add `trade_cash_links` only from full source evidence; never auto-match by amount/date or print row details.

## Auto-fix order

1. `python3 scripts/harden_permissions.py --include-browser-profile` — creates the required private directories and fixes modes without printing private filenames. A refused symlink is a blocker that needs manual inspection; never follow it.
2. When `[drive]` is configured with a usable `root_folder_id` and the connector probe succeeds, create any fixed public folder from `docs/drive-layout.md` that is missing directly under the vault root (create-file with the folder MIME type, exact folder name). Never rename, move, or inspect anything else; report those folders as fixed only when creation succeeds. Nothing is copied for Drive auth — the connector's sign-in lives in the user's Claude account, not in this checkout.
3. Run `python3 scripts/migrate_db.py --init` if the DB is missing/empty; otherwise run `python3 scripts/migrate_db.py` to apply pending migrations transactionally.
4. Only when `[hapoalim]` or `[cal]` credentials are configured, run `scripts/install_node_deps.sh` when `node_modules/` is missing or `(cd scripts && npm ls --omit=dev)` fails (needs valid Node/npm; the wrapper uses `npm ci` with `package-lock.json`; stream stderr). Do not download Puppeteer/Chromium for users who did not opt into automatic bank fetching.
5. Run `scripts/install_dashboard_deps.sh` when `dashboard/node_modules/` is missing or `npm --prefix dashboard ls` fails, then verify with `npm --prefix dashboard run build`.

Re-check after each fix so the report shows post-fix state. **Don't** auto-install OS-level binaries (Homebrew / apt), touch nvm, generate creds, add connectors on the user's behalf, or run anything `--setup`. (Pip / npm installs are fine — they're local, idempotent, and the whole point of auto-fix.)

If the Drive live check's preconditions don't hold (connector tools absent, or no usable root ID), report `skipped — <reason>`, not a fake OAuth error. If the probe succeeds but a fixed folder cannot be created, report `Drive vault layout — could not prepare fixed folders`; do not call that an outage or OAuth failure.

## Blocker vs Optional

- **Blocker** = the local pipeline literally can't run. (`python3`, DB init/migration; `node`/dashboard npm deps for the live app; bank npm deps when bank creds exist; `qpdf` when protected payslips are configured.)
- **Optional** = one feature degrades. (Drive connector / Drive root ID / Drive-live — Drive down just means manual-drop ingest pauses, with `⚠️` warnings; the weekly backup is local and unaffected; bank fetch + dashboard still flow. Likewise the `[pdf-passwords]`, `[hapoalim]`, `[cal]` sections of `.secrets/findash` individually, chromium profile when its source's secrets are absent, and the IBKR connector when not added/connected — gates the investments feed.)
- **Promotion:** chromium profile for a source becomes a blocker the moment that source's credentials land (a `[<source>]` section in `.secrets/findash`) — creds without a trusted cookie → SMS challenge.

## Report format

Emojis, compact, sections only when non-empty. Today's date.

```
🩺 findash — <YYYY-MM-DD>

✅ Fixed
  <comma-separated short phrases on one or two wrapped lines>

🚫 Blockers
  • <thing> — <one-line fix>

⚠️ Optional   (skip if you don't use that feature)
  • <thing> — <what it gates>

✓ OK
  <comma-separated inline list, wrap ~80 cols>
```

Drop the ✅ block if nothing was fixed. If zero blockers AND zero optional gaps, the whole report collapses to:

```
🩺 findash — all systems go.
```

Remediation = exact shell command when possible. Detect OS (`uname -s` → Darwin / Linux) and match install hints (`brew install …` vs `sudo apt install -y …`). For OAuth / `--setup`, name the exact command.

Example on a partially-set-up macOS box:

```
🩺 findash — 2026-05-27

✅ Fixed
  inbox/staging/ created • .secrets/findash chmod 600 (was 644)

⚠️ Optional
  • Drive connector — not added; Claude → Connectors → Google Drive (manual-drop ingest)
  • Drive vault — root folder unreachable; check [drive] root_folder_id and the connector's Google account
  • .secrets/findash [cal] — only for fetching credit-card data
  • chromium-profile/visaCal — not blocking yet (no [cal] creds)
  • IBKR connector — not connected; add it via Claude → Connectors for portfolio snapshots

✓ OK
  qpdf, python3 3.13, node 22.14.0, Drive root ID,
  .secrets/findash ([hapoalim] [pdf-passwords]), finance.db (12 MB), node_modules/
```

## Judgment

- **Don't lie about fixes.** ✅ Fixed = you ran it AND re-checked. A failed attempt goes into 🚫 Blockers with the real error.
- **Diagnose top-down.** If the connector tools are absent, the Drive-live line says "skipped — connector not added", not "OAuth expired".
- **Idempotent.** Second run on a healthy machine = one line. Only list under ✅ Fixed what you actually changed this run.
- **Trust reality over setup prose.** If `scripts/package.json` or its lockfile is missing, flag the missing manifest instead of attempting an install.
- **No new categories silently.** Surprise findings go under a `🔍 Note` line, not into the matrix.
