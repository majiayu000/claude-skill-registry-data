---
name: pb-harness-work
description: >-
  Change the agent harness itself (AOS, AO or CBS hooks, gates, memory,
  permissions, delegation, plugins, bootstrap) the safe way: look up the
  matching harness pattern, design against its gotchas, build with
  /startcycle and a live trail, check every harness, open a PR after GO.
  Use for "change a hook", "fix the go-gate", "harness work", "plugin change".
category: bdb-core
kind: playbook
trigger: ["harness work", "change a hook", "fix the go-gate", "plugin change"]
inputs: [goal, repo, area]
requires:
  skills: [agentic-harness-patterns, startcycle, agenttrail, verification-before-completion, git-pr-review, github, "gh (external)"]
  agents: [architect, techlead, reviewer]
  mcps: []
  store: []
go_points: [git push + gh pr create]
outputs: ["production_artifacts/00_execution_plan.md", "production_artifacts/pb-harness-work-<date>.md"]
verify: "npm test exit 0 on the pushed SHA; gh pr view <branch> --json state -q .state == OPEN"
difficulty: advanced
est_time: 1-3 h
---

# Change the harness safely
What you get: a harness change that was designed against the known gotchas, built and reviewed, tested on every harness, and opened as a PR after your GO.

## Inputs
- goal — what should change, asked in step 1
- repo — the local checkout, asked in step 1
- area — memory, permissions, hooks, delegation, context, skills/plugins, tools or bootstrap, asked in step 1

## Steps
1. Ask + preflight (run everything from `<repo>`) — goal, repo, area → run log; default branch: `default=$(git -C <repo> symbolic-ref --short refs/remotes/origin/HEAD); default=${default#origin/}` (the command prints `origin/main`); if `git -C <repo> branch --show-current` equals it, `git -C <repo> switch -c feat/<slug>` — on a feature branch (gh missing or unauthenticated → log it, give the `gh auth login` hint, stop)
2. agentic-harness-patterns — area → section and reference file, named in the run log; files live in `skills/global_config/agentic-harness-patterns/references/` (installed copy: the matching directory):
   - memory → `memory-persistence-pattern.md`
   - permissions → `permission-gate-pattern.md`
   - hooks → `hook-lifecycle-pattern.md`
   - delegation → `agent-orchestration-pattern.md` and `task-decomposition-pattern.md`
   - context → `context-engineering-pattern.md`
   - skills/plugins → `skill-runtime-pattern.md`
   - tools → `tool-registry-pattern.md`
   - bootstrap → `bootstrap-sequence-pattern.md`
   - check: the gotcha titles that apply are listed as a checklist (titles only, no copied content)
3. startcycle (Architect) — goal and gotcha checklist → `production_artifacts/00_execution_plan.md` with agenttrail components, each with a `files:` line — every listed gotcha is marked addressed or n/a with a reason; a component without `files:` → back to Architect
4. agenttrail — `aos-trail . --plan production_artifacts/00_execution_plan.md --no-open` → URL in the run log, before the build nodes start — URL printed; a no-op if startcycle already started the trail (it is safe to run twice)
5. startcycle (TechLead → build → Reviewer) — the dispatcher is the main session; the agents never call each other → code and review file — no open `blocking` finding
6. Cross-harness check → table in the run log, one row per harness (affected yes/no, file, evidence):
   - Claude: `.claude/hooks/*.mjs`, settings hooks
   - agy: `hooks.json` via installer `mergeAntigravityHooks`
   - OpenCode: `.opencode/plugins/bdb-aos.js`
   - Codex: `.codex/agents/*.toml`, `~/.codex/hooks` and `[features] hooks` in `~/.codex/config.toml` (both written by `installer.js`)
   - check: every "yes" row has a test in `npm test` or a named manual check
7. verification-before-completion — `npm test` (and `node scripts/validate-skills.mjs` if skills changed) → fresh output pasted in the run log — exit 0
8. git commit — compare `git -C <repo> status --porcelain` with the plan's `files:` lines; unlisted changes outside `production_artifacts/` → stop and ask; stage only the listed files (never the run log or `production_artifacts/`) → SHA in the run log — the commit hook passes
9. git-pr-review — commits → PR body in `production_artifacts/pb-harness-work-<date>-pr.md` — body written, nothing posted
10. [GO] github — `git -C <repo> push -u origin <branch>`, then `gh pr create -R <owner/repo> --base <default> --head <branch> --title "<title>" --body-file <body>` (`<owner/repo>` from `git -C <repo> remote get-url origin`) — the WAITING FOR GO line names branch, base and title. The run stops here until the human types GO. The hook guards the push only; the PR create is GO by contract.

Run log: `production_artifacts/pb-harness-work-<date>.md` in the repo's start directory, never committed

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
