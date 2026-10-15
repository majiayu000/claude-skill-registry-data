---
name: pb-project-new
description: >-
  Start a new private GitHub project the AOS way: create the private repo,
  bootstrap AOS (project card, AGENTS.md, wiki, memory, CI choice), push
  after GO, and confirm the first CI run is green and the repo is still
  private. Use for "new project", "start a repo", "bootstrap a project".
category: bdb-core
kind: playbook
trigger: ["new project", "start a new repo", "bootstrap a project"]
inputs: [name, owner, local_folder, "upstream_url?"]
requires:
  skills: [github, aos-project-init, pb-ci-fix, "gh (external)"]
  agents: []
  mcps: []
  store: []
go_points: [gh repo create, git push -u origin main]
outputs: [".aos/project.json", "AGENTS.md", ".openwiki/", "production_artifacts/pb-project-new-<date>.md"]
verify: "gh repo view <owner>/<name> --json visibility -q .visibility == PRIVATE"
difficulty: intermediate
est_time: 20-40 min
---

# New private AOS project
What you get: a private GitHub repo with AOS bootstrapped, pushed, and a first CI run checked.

## Inputs
- name, owner — asked in step 1
- local_folder — where the clone goes, asked in step 1
- upstream_url (optional) — a repo to track as `upstream`, asked in step 1

## Steps
1. Ask — name, owner, local folder, optional upstream URL → run log header in the start directory (`production_artifacts/pb-project-new-<date>.md`, never committed) — all answered
2. [GO] github — from the parent of `<local_folder>` (`cd` there first; the clone lands in `<name>/`), `gh repo create <owner>/<name> --private --clone` → repo and local clone — The run stops here until the human types GO.
3. github — `gh repo view <owner>/<name> --json visibility -q .visibility` → value in the run log — must equal `PRIVATE`; otherwise fail-stop: write the value to the run log, tell the user, push nothing, and do not delete or change the repo (destructive actions need the user's confirmation)
4. Upstream given → `git remote add upstream <url>` — `git remote -v` shows it; never push to `upstream` (no `gh repo fork`: a fork of a public repo cannot be private)
5. aos-project-init — folder → `.aos/project.json`, `AGENTS.md` and symlinks, OpenWiki, memB project card, Synapse, CI choice (it may create triage labels and write `../WORKTREE.md`; aos-project-init asks for its own write-list approval) — doctor rows green or exceptions named, `.openwiki/` present; accept aos-project-init's own commit if it makes one, step 6 commits only what is left, never the run log
6. git commit `chore: bootstrap AOS project` — remaining bootstrap files → SHA — commit succeeds (any hook failure is reported, never bypassed with --no-verify) (skip if nothing is left)
7. [GO] `git branch -M main`, then git push -u origin main — SHA → remote — The run stops here until the human types GO.
8. pb-ci-fix — only if CI was chosen in step 5: run its step 10 (watch the run on the pushed SHA) → conclusion `success`; if red, hand over to `/pb-ci-fix` from its step 1 (it has its own GO); then re-run the step 3 check — still `PRIVATE`

Run log: `production_artifacts/pb-project-new-<date>.md` in the start directory, outside the new repo

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- GO is by contract in every harness. The go-gate hook is only a backstop on Claude Code, OpenCode and agy (Codex: unverified; Cursor, Kimi: none). A missing hook is never permission to proceed.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
