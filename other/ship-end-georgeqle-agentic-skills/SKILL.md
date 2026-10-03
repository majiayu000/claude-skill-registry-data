---
name: ship-end
description: Wrap up the current session — update docs, commit, and push
type: shipping
version: v0.15
argument-hint: "[--no-deploy] [--save-conversation] [--save-all-conversations]"
---

# Ship End

Wrap up the current session: mark progress, commit, and push. If `$ARGUMENTS` contains `--save-conversation`, save the current conversation to `conversations/`. If `$ARGUMENTS` contains `--save-all-conversations`, export all past conversations to `conversations/`.

## Process

1. **Check for changes:**
   - Run `git status` and `git diff` to see all changes.
   - If the working tree is clean and no unpushed commits: report "nothing to ship" and stop.

2. **Update task tracking:**
   - Update `tasks/todo.md` — mark completed items as done, note any outstanding items or blockers.
   - Update milestone progress in `tasks/roadmap.md` if criteria were met.
   - Check `tasks/manual-todo.md` (if it exists) — note the status of manual tasks (how many checked vs unchecked). Do NOT modify checked items.
   - Check `tasks/record-todo.md` and `tasks/recurring-todo.md` if they exist — note unchecked advisory counts only. Do NOT treat them as blockers unless an item has been promoted into `tasks/todo.md`.
   - Update `tasks/history.md` — append a brief record of what was accomplished this session (phase/step completed, key changes). Create it if it doesn't exist.
   - If `tasks/todo.md`, `tasks/roadmap.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, or `tasks/recurring-todo.md` changed and `scripts/audit-task-docs.mjs` exists, run `node scripts/audit-task-docs.mjs` and fix any failures before final next-work routing.

3. **Deploy (skip if `--no-deploy`):**
   - If the current session work is not already merged into the current primary branch, defer deployment until after ready-PR publication and explicit review/`/github-pr merge`. Never deploy development state from the work branch.
   After shipping, deploy only when the project has an explicit manual deploy contract.
   - **Check for deploy contract.** Look for `deploy.md` or `tasks/deploy.md`.
   - If neither file exists, skip deploy and report `Deploy skipped: no explicit manual deploy contract (deploy.md or tasks/deploy.md)`.
   - If a deploy contract exists, continue.
   - **Invoke `/deploy`** (release-ops pack) targeting the default environment (staging).
   - Pass the deploy contract context to `/deploy`.
   - Skip ledger recording and staleness reporting — those are for standalone `/deploy` invocations only.
   - If `/deploy` (release-ops pack) reports failure, report the error. Do not retry.

4. **Save conversation (skip if `--save-conversation` and `--save-all-conversations` both absent):**
   - Run `scripts/save-conversation.sh` to export the current Claude Code conversation as a markdown file in `conversations/`. If the script is not found or fails (e.g., not running in Claude Code, no local conversation history), warn and continue — do not block shipping. Include the generated file in the shipping boundary.
   - If `$ARGUMENTS` contains `--save-all-conversations`, run `scripts/save-conversation.sh --all` instead.

5. **Ship the session changes:**
   - Use `/commit-and-push-by-feature` with `docs/github-delivery-contract.md`: group logical commits on the issue-backed non-primary branch, publish it, and create or update one ready pull request without merging it.
   - **Pack install artifact boundary:** Treat `.agents/project.json` as the committed project designation. When pack configuration changed, include `.agents/project.json` in the shipping boundary. Treat `.claude/skills/**` and `.codex/skills/**` as generated local skill roots recreated by `scripts/pack.sh refresh`; generated skill roots must not be staged or committed. If those roots are untracked, leave them uncommitted and report them as generated local artifacts. If any path under those roots is already tracked or modified as a tracked file, stop unless the current task explicitly includes repository hygiene to untrack or ignore generated skill roots.

6. **Report session summary:**
   - What was accomplished
   - Deploy status (if deployed)
   - Test status — explicitly state whether any failing tests are expected (red phase: tests written before implementation) or unexpected (regressions/bugs that need fixing)
   - What's outstanding
   - Branch and commit list
   - Confirm working tree is clean

## Output

```
## Session Summary
- **Accomplished**: [what was done]
- **Deploy**: [status]
- **Tests**: [pass/fail — expected or unexpected]
- **Manual tasks**: [X/Y complete, or "none"]
- **Advisory tasks**: [record/recurring counts, or "none"]
- **Outstanding**: [remaining work]
- **Branch**: [branch name]
- **Commits**: [list]
- **Working tree**: clean
- **Next work:** [specific task, blocker, verification gap, or "none"]
- **Recommended next command:** [one command or route]
```

## Next-Step Routing

Before closing out the session, identify the next concrete work item from project state, then recommend the executor and invocation.

Output exactly two lines beyond the normal session summary:

- **Next work:** <specific task name, manual blocker, verification gap, or "none">
- **Recommended next command:** <one command or route>

Rules:

- Make the next work item primary. Derive it from `tasks/todo.md`, `tasks/manual-todo.md`, deploy status, validation gaps, smoke-test gaps, outstanding session work, or the absence of any remaining work. Do not use agent mode itself as the next work item.
- Treat `tasks/todo.md` as the only executable current-task surface. Historical roadmap entries and unchecked advisory/manual/record/recurring items are reconciliation candidates, not next executable work, unless the current active todo section explicitly promotes them.
- Use `./scripts/agent-mode.sh` only to choose command text. If it is missing, unset, or non-zero, infer routing from the current invocation and task type instead of asking the user to select a mode by default.
- Prefer an owning workflow/domain route over execution-loop defaults. If the next work item names a research, alignment, design, UI, UX, prototype-test, or copy-audit artifact or review page, recommend the specific owning skill, required user review, or compiled-YAML step directly. Use `/exec` only when no narrower installed skill, artifact contract, or review route owns the next action.
- Inference defaults:
  - Hybrid execution handoff → check `.agents/project.json.enabled_packs` for `agent-bridge` — if `agent-bridge` is not enabled, recommend `npx skillpacks install agent-bridge` from the project shell first; if `agent-bridge` is enabled, recommend `/delegate $exec`.
  - Claude-only or orchestration-heavy work → after applying owning-route precedence above, recommend `/exec`.
  - Codex-only execution → after applying owning-route precedence above, recommend `$exec`.
  - External human-only manual work (browser/auth/DNS/service dashboard work with no reliable authenticated CLI/API path, paid account setup, real-device checks, or production smoke-test work needing human sign-off) → check `.agents/project.json.enabled_packs` for `guided-walkthrough` — if `guided-walkthrough` is not enabled, recommend `npx skillpacks install guided-walkthrough` from the project shell first; if `guided-walkthrough` is enabled, recommend `/guide` — or a Claude-guided manual step rather than `/exec`.
  - Agent-executable work misfiled in `tasks/manual-todo.md`, task-doc bookkeeping, stale `tasks/manual-todo.md` cleanup, or reconciliation against repo/history reality → check `.agents/project.json.enabled_packs` for `docs-health` — if `docs-health` is not enabled, recommend `npx skillpacks install docs-health` from the project shell first; if `docs-health` is enabled, recommend `/reconcile-dev-docs fix tasks` — promotion to `tasks/todo.md`, or a direct dev-doc audit, not `/guide`.
- Only present multiple commands when the ambiguity materially changes execution safety or there are equally valid next work items. Otherwise choose the best route and mention degraded mode lookup inline.

## Constraints

- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, include `npx skillpacks install <pack-name>` from the project shell as the prerequisite.
- **Fix unrelated issues:** If any step surfaces errors, warnings, or lint issues — even ones unrelated to the current work — investigate and fix them before continuing. Commit these fixes separately with a descriptive message.
- Do NOT modify CLAUDE.md. CLAUDE.md is for project conventions and config only — not progress tracking.
- Progress and active work go in `tasks/todo.md`. Completed work history goes in `tasks/history.md`.
- Do not execute or block wrap-up on `tasks/record-todo.md` or `tasks/recurring-todo.md` items unless they were explicitly promoted into `tasks/todo.md`.
- When task docs changed, do not finish with a next-work recommendation until `node scripts/audit-task-docs.mjs` passes, if that script exists.
- Do not switch branches or create new branches unless the current state requires it.
- Do not amend or rewrite history.
- Do not commit secrets.
- Do not commit on or push mutations directly to the primary branch. Use `/commit-and-push-by-feature` to ensure and publish the issue-backed work branch and ready pull request.
- If pre-commit hooks fail, fix and retry.
- Never use GitHub Actions for deployment. Only use manual deploy scripts, Makefiles, or CLI commands.
- Never deploy to production without explicit user confirmation.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
