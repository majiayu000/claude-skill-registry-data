---
name: pb-redesign-app
description: >-
  Overhaul one app's UI against an audit: UX audit and UI review of the
  running app, current versus proposed design tokens, a before/after visual
  plan, a startcycle build, point fixes, accessibility and browser tests,
  delivered as a PR after GO. Use for "redesign this app", "design overhaul",
  "audit and fix the UI", "give the app a new look".
category: design-ui-ux
kind: playbook
trigger: ["redesign this app", "design overhaul", "audit and fix the UI"]
inputs: [repo, app_url, scope]
requires:
  skills: [ux-audit, ui-review, ui-tokens, godmode-ui-ux, plan-canvas, bdb-visual-edit, startcycle, wcag-audit-patterns, webapp-testing, github, "gh (external)"]
  agents: [architect, techlead, reviewer]
  mcps: [chrome-devtools]
  store: []
go_points: ["git push + gh pr create"]
outputs: ["production_artifacts/pb-redesign-app-<date>.md", "production_artifacts/pb-redesign-app-<date>/audit.md", "production_artifacts/pb-redesign-app-<date>/tokens-diff.md"]
verify: "repo test/lint scripts exit 0 on the pushed SHA; gh pr view <branch> --json state -q .state == OPEN; every audit finding marked fixed or deferred in the run log"
difficulty: advanced
est_time: 2-4 h
---

# Redesign one app
What you get: one app's UI overhauled against a written audit, new design tokens and a before/after plan, delivered as a pull request after your GO.

## Inputs
- repo — the app's checkout, default the current directory
- app_url — the running local dev URL (not a remote or production site)
- scope — the screens or flows to redesign, asked once

## Steps
1. ux-audit and ui-review — `app_url` opened and screenshotted per screen in scope with chrome-devtools (`puppeteer_navigate`, `puppeteer_screenshot`) → `production_artifacts/pb-redesign-app-<date>/audit.md` with numbered findings — app_url unreachable or chrome-devtools unavailable → log it and stop; every finding has a screenshot or a file reference
2. ui-tokens — current tokens read from the repo versus proposed DTCG tokens → `tokens-diff.md` in the same folder — diff written, nothing applied yet
3. plan-canvas (Plan Builder mode) — before/after per screen in scope → plan link or file in the run log — stops for approval
4. startcycle (architect, techlead, reviewer) — the approved plan and audit → build on a new branch; godmode-ui-ux rules apply to the UI work — reviewer reports no open `blocking` finding
5. bdb-visual-edit — point fixes the human annotates in the running app via `aos-plan-canvas annotate`, each after its diff plan is approved → edited files in the run log — only the picked files change
6. wcag-audit-patterns and webapp-testing — accessibility pass plus a browser test of the changed screens, then the repo's lint and test scripts → results in the run log — all exit 0; each audit finding marked fixed or deferred
7. [GO] git push -u origin <branch> and gh pr create — one combined GO; the WAITING FOR GO line names the branch, base branch, PR title and the head SHA. The run stops here until the human types GO. The hook guards `git push`; `gh pr create` is not hook-guarded, so this GO is its only guard. Afterwards `gh pr view <branch> --json state -q .state` equals `OPEN` and the PR URL is logged.

Run log: `production_artifacts/pb-redesign-app-<date>.md` in the start directory, never committed

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
