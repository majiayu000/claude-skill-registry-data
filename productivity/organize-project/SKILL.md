---
name: organize-project
description: PLAN-FIRST 10/10 project organization & reconciliation. Use when Priscila says "organize this project", "10/10 organize", "organize these tasks", "reconcile this project", or "/organize-project". Produces a read-only reconciled task ledger + backlog and STOPS for approval — makes NO changes until she says GO. Do not use for simple task logging (use /capture or the Inbox tab) or for catching up on a chat (use /sync-me-up).
---

# Organize Project — PLAN-FIRST 10/10 Reconciliation

Turn a messy, multi-surface project into ONE reconciled, dependency-ordered backlog with a single named source of truth. Works identically in Claude Code and Codex.

## State machine (precise — do not blur these)

1. **TRIGGER → read-only audit.** On any trigger phrase, you are in PLAN mode. Inventory + reconcile + propose. **Change NO file, sheet, doc, calendar event, or code.** Output the plan and stop at the approval checkpoint.
2. **GO → approved execution.** Only after Priscila explicitly says "GO" (or "approved", "do it") do you write anything. Back up affected surfaces first, then execute only what was approved.
3. **Scope-changing conflict found mid-execution → re-report, do not silently expand.** If during GO execution you discover something that changes scope (new dependency, conflicting requirement, missing data), STOP that branch, update the report, and wait for a fresh GO on the delta. Never widen scope on your own.

## When NOT to use
- Simple "save this idea/link" → `/capture` or 📥 Inbox tab.
- "Catch me up on this chat / what's pending" → `/sync-me-up`.
- Start/end-of-day planning → `/day-planner`, `/session-start`, `/session-exit`.

## STEP 0 — Read first (don't ask Priscila; go here)
- `~/AGENTS.md` and `~/.claude/CLAUDE.md` (operating rules; Codex reads AGENTS.md).
- `~/.claude/projects/-Users-priscilahigashi/memory/MEMORY.md` (+ any project-specific memory files it indexes).
- `reference_active_connections.md` (route matrix) before claiming anything is blocked.
- ⭐ **TASKS IN PROGRESS — Trackers** folder (Marketing shared drive, starred): `https://drive.google.com/drive/folders/1GSW79O-eUkHSeDKwGJqhEbG8kP96bWnz` — START here for navigation, then **follow each shortcut to the ORIGINAL source-of-truth file**. The shortcut is a pointer, never the authority.

## STEP 1 — Identify the project
- If Priscila named a project, use it.
- If not: infer it from THIS chat + the live surfaces. State the inferred project in one line and proceed (don't stall asking).
- If the chat clearly contains MULTIPLE projects: list them, pick the one with the most current-chat activity as primary, and explicitly note the others are out of scope for this run (offer to run them next). Do not silently merge them.

## STEP 2 — Inventory every relevant surface (enumerate, don't judge)
Only the surfaces that actually apply to the selected project:
- Trackers (from the folder + Spreadsheet Hub `1qDbO6JQX0cKbZ9rHjiM7a4U_p7OOddZ3k3Sp30JJoqo` which indexes every sheet+tab).
- Plans/docs (Flow Plans Tracker `1fggy918FgPfnMQ-dzGQk2zx9uhi2_-uWXMKGW4MA47k` indexes every doc).
- Code / GitHub Actions workflows / scripts.
- Credentials ROUTING (which token/secret — do not read secret values).
- Calendar tasks, 📥 Inbox tab, 🚨 Pipeline Failures tab, 📝 Productivity & Routine doc (`1wVBuNOuOufT8WP4KCrrlVbKWRmQZjKvqmia1soUEBZE`) — **only if the project touches them**.
- Tasks + decisions stated in THE CURRENT CHAT (always include these).

## STEP 3 — Assign source authority (rank on conflict)
1. Requirements Priscila has confirmed (incl. this chat) > 2. live config/implementation > 3. tracker items WITH evidence > 4. master plan > 5. research > 6. old memory. Flag stale/superseded facts; never treat a shortcut, Calendar entry, or Inbox row as automatically canonical — they are evidence, not authority.

## STEP 4 — Reconciled task ledger (right-sized; no extra fields)
Per task: **outcome · source · authority/last-verified · owner · status · dependency · definition-of-done · evidence link.**

## STEP 5 — Reconcile conflicts
Tag each item: `confirmed` / `superseded` / `duplicate` / `unsupported-assumption` / `implemented-but-unverified` / `blocked`. Never delete history — mark obsolete/superseded/deferred.

## STEP 6 — Map requirements → delivery
Each requirement (incl. today's tasks): required data + expected behavior + implementation task + test + acceptance condition.

## STEP 7 — One canonical backlog
Organize by **outcome / workstream + dependency order**. Owner is a FILTER, not the top grouping, so the critical path stays visible. Separate **minimum safe pilot** from **deferred/over-built** scope.

## STEP 8 — Non-destructive report + approval checkpoint
Report what's obsolete / duplicated / missing / conflicting / blocked / ready. Propose improved wording. Name the ONE source of truth going forward. **Change nothing until GO.**

## After GO (execution)
- Back up affected surfaces before writing.
- Execute only approved changes.
- Synchronize **at least two durable sources** (the project tracker + a handoff/Productivity doc) so it self-explains on reopen.
- New spreadsheet/tab → row in **Spreadsheet Hub**. New plan/process doc → row in **Flow Plans Tracker**.
- Never mark a task Done without LIVE evidence (cell ref, file path, run id, commit on remote).

## Credentials routing
Determine FILE OWNERSHIP first: OPC/Priscila surfaces → `SHEETS_TOKEN`; McFolling/Airbnb-owned surfaces → `MCFOLLING_TOKEN`. Never guess the owner; if unclear, check the sheet's location/sharing before choosing a token.

## Safeguards (hard rules)
- Shortcuts = navigation aids, NEVER source authority.
- Calendar & Inbox = evidence sources, not automatically canonical.
- No broad mailbox / personal-data scan unless directly relevant to the selected project.
- No new secrets, OAuth scopes, providers, or parallel routes without flagging them first (per the AGENTS.md ecosystem guardrail).
- Never guess credentials, dependencies, owners, status, or completion.
- Never claim X unlocks Y without proof of the dependency.

## Output style
ADHD-optimized: **summary line first**, the conflict/ready findings second, the backlog last, and **ONE clear next action** at the end. Use the report format: ✅ Done / 🔴 Blocked (exact reason) / ⚠️ Only YOU can do (what/why/where/steps).

## Self-audit checklist (run before presenting the plan, and again after GO)
- [ ] Project correctly identified (named, or inferred + stated; multi-project disambiguated).
- [ ] Every RELEVANT surface inventoried (trackers, plans, code, workflows, creds routing, Calendar/Inbox/Failures/Productivity only if applicable).
- [ ] Source authority assigned on every conflict (ranked).
- [ ] Current-chat work + decisions captured.
- [ ] Duplicates/conflicts reconciled and tagged.
- [ ] Credentials routed by owner (SHEETS_TOKEN vs MCFOLLING_TOKEN), no values read.
- [ ] Minimum safe pilot scope + dependencies defined (no assumed dependencies).
- [ ] Approval checkpoint honored — nothing written before GO.
- [ ] (After GO) durable logging honored — Spreadsheet Hub / Flow Plans Tracker rows added for any new sheet/doc; two durable sources synced.
- [ ] (After GO) final evidence recorded for every Done.

## Durability note — SINGLE SOURCE, NO DRIFT
Canonical source = this file in the repo: `priihigashi/oak-park-ai-hub` → `skills/shared/organize-project/SKILL.md` (git-tracked, durable). The runtime path `~/.agents/skills/organize-project` is a **symlink into the repo working tree** (`~/ClaudeWorkspace/oak-park-ai-hub/skills/shared/organize-project`), and `~/.claude/skills/` + `~/.codex/skills/` symlink to `~/.agents/`. So there is exactly ONE physical file — local edits, repo edits, and Codex-sandbox reads all see the same content; **copies cannot drift** because no copy exists. To change the skill: edit the repo file, commit, push. (Chat memory is NOT persistent for Codex — this file + the repo are the only durable source.) Triggers are also listed in `AGENTS.md` (repo + local mirror) and the 🤖 Skills & Agents directory sheet.
