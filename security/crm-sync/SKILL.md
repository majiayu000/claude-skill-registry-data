---
name: crm-sync
description: >-
  Sync CRM knowledge notes in a vault with the live CRM code repositories: pull the read-only
  repos, detect which changed, and refresh only the affected reverse-engineering notes and the
  keep/drop/decide note. Triggers: "/crm-sync", "refresh CRM knowledge", "what changed in the
  CRM code".
license: MIT
---

# /crm-sync - keep the CRM knowledge layer fresh

The CRM (CHARM) is Anton's proven engine on GitLab. We reverse-engineered it once
(2026-06-19) into a linked vault layer so his digital twin can `/ask` how the CRM
works. Code keeps changing; this skill stops that knowledge from going stale silently.
It is the recurring half of the standing rule `evaluate-recurring-into-routine`.

**What this is NOT:** not a re-decompose-from-scratch. It is a DIFF-DRIVEN refresh:
pull, see what changed, update only the notes that map to the changed code.

## Where everything lives
- **Code (read-only clone, 16 repos):** `<CRM_REPOS_ROOT>` (memory `crm-gitlab`).
- **Decomposition audit (HTML, source of the notes):** `<CRM_REPOS_ROOT>\_AUDIT\`
  (`Functional-Map.html`, `Know-How-Decomposition.html`, `Architecture-Deep.html`).
- **Vault knowledge layer:** `$OBSIDIAN_VAULT/05-Resources/CRM-Engine/`
  - `_CHARM-CRM-Engine-MOC.md` (hub)
  - `crm-architecture-4-layers.md`
  - `crm-mtproto-engine.md`
  - `crm-core-autopilot.md`
  - `crm-admin-panel-api-brain.md`
  - `crm-data-model-mongo.md`
  - `crm-know-how-13-patterns.md`
  - `crm-landing-api-money.md`
  - decision: `$OBSIDIAN_VAULT/02-Decisions/decision-crm-keep-cc-drop-decide.md`

## Repo -> note map (which note to refresh when which code changes)
| Code area in <CRM_REPOS_ROOT> | Note(s) to refresh |
|---|---|
| `admin-panel` / `admin-panel-api` (FastAPI brain, filter-DSL, $facet) | `crm-admin-panel-api-brain` |
| `mtproto-api` (Telethon hands, event-pool, dialog export, FloodWait) | `crm-mtproto-engine` |
| `core` (aiocron autopilot: newsletters, gatekeeper, tapping, calls) | `crm-core-autopilot` |
| `landing-api` (token sale, NOWPayments, CHEATING_MODE, webhook) | `crm-landing-api-money` |
| shared models / Mongo schema (collections, fields) | `crm-data-model-mongo` |
| cross-cutting architecture / generations | `crm-architecture-4-layers` |
| reusable patterns / know-hows | `crm-know-how-13-patterns` |
| any capability added/removed/disabled | `decision-crm-keep-cc-drop-decide` (+ MOC) |

## Procedure
1. **RECALL first (don't duplicate).** Read memory `crm-gitlab` and `_CHARM-CRM-Engine-MOC.md`
   so you refresh, not rewrite. Note the date of the last sync.
2. **Pull the repos.** For each repo dir under `<CRM_REPOS_ROOT>`:
   `git -C "<CRM_REPOS_ROOT>\<repo>" pull --ff-only` (clone is read-only; this only updates).
   Collect the set of repos that actually moved (non-empty pull, or
   `git -C <repo> log --oneline <old>..<new>`). If a pull needs GitLab creds and fails,
   stop and tell Anton (creds in `secrets\`; do NOT hardcode).
3. **No changes -> stop.** If nothing moved since last sync, report "CRM unchanged since
   <date>, 0 notes touched" and exit. (Cheapest correct answer.)
4. **For each changed repo,** re-read ONLY the changed files/areas (use an `Explore`
   subagent with `model: 'sonnet'` - this is grunt extraction, per `model-routing-sonnet-grunt`;
   escalate to Opus only if a judgement call). Ask it to report: what behavior changed vs
   what the mapped note currently says, with file+line evidence.
5. **Backup before writing.** `python "$IMPORTS_ROOT/vault_backup.py"` (rule
   `vault-backup-rule`). NEVER blanket-delete; edit in place.
6. **Update the mapped note(s)** - the "How it works" / "Weak spots" sections only.
   PRESERVE frontmatter, `origin: external`, `authored_by:` (denis-udot / gleb-taigunov),
   and all `[[wikilinks]]`. If a capability moved KEEP<->DROP<->DECIDE, update the decision
   note too. New behavioral pattern worth a concept? Follow `concept-creation-rules` (create
   if >=3 repeats + entity noun + domain), and relink (`no-orphan-notes-rule`).
7. **Verify + reindex.** Run the vault broken-link check; then
   `python "$IMPORTS_ROOT/brain_embed_update.py"` (cooldown 15min; nightly @04:00
   will catch it otherwise) so the refreshed notes are `/ask`-searchable.
8. **Report post-hoc** (not for permission): which repos moved, which notes changed,
   any new concept, any DECIDE item that flipped, and what still needs Anton/Denis.

## Guardrails
- Read-only by default; the only writes are git pull (updates the clone) + the mapped
  vault notes, always backup-first.
- Don't touch the live CRM server or its Mongo - that is the prod-access track, separate.
- AK-47: this is one markdown procedure. If the CRM grew a whole new service, that is a new
  note + MOC link, still just notes - flag it, don't over-build.

## When to run
On demand (after Anton hears the CRM changed), or as a light routine. Pairs with the
`crm-gitlab` DD-audit and the `decision-crm-keep-cc-drop-decide` open items.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
