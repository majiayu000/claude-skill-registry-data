---
name: pb-open-source
description: >-
  Prepare a project for open sourcing: a sanitized fork with secrets and
  internal references stripped, a sanitizer verdict, README and LICENSE, then a
  new PRIVATE GitHub repo created and pushed only after GO. The playbook never
  makes the repo public. Use for "open source this project", "make a sanitized
  fork", "prepare a public release".
category: engineering-method
kind: playbook
trigger: ["open source this project", "sanitized fork", "prepare a public release"]
inputs: [source_repo, target_name, owner, license]
requires:
  skills: [github-repo, readme, github, "gh (external)"]
  agents: [opensource-forker, opensource-sanitizer]
  mcps: []
  store: []
go_points: ["gh repo create", "git push"]
outputs: ["<fork dir>", "<sanitizer report>", "production_artifacts/pb-open-source-<date>.md"]
verify: "sanitizer verdict PASS or PASS-WITH-WARNINGS logged; gh repo view <owner>/<name> --json visibility -q .visibility == PRIVATE; LICENSE and README.md exist on the pushed default branch (gh api repos/<owner>/<name>/contents/LICENSE and README.md return 200)"
difficulty: advanced
est_time: 1-3 h
---

# Sanitized fork in a new private repo
What you get: a sanitized copy of the project with README and LICENSE in a new private GitHub repo, with the sanitizer verdict logged. Going public stays your own action, outside this run.

## Inputs
- source_repo — the local checkout to fork, asked if missing
- target_name — the new repo name, asked if missing
- owner — the GitHub user or org for the new repo, asked if missing
- license — the license id for the LICENSE file (for example MIT or Apache-2.0), asked if missing

## Steps
1. opensource-forker (agent) — source_repo → fork dir `<scratch>/<target_name>` (`<scratch>` = `mktemp -d`) and `.env.example`, secrets and internal references stripped, git history cleaned — fork dir exists; the source repo is untouched (`git -C <source_repo> status --short` is unchanged)
2. opensource-sanitizer (agent) — fork dir → report with the verdict PASS, FAIL or PASS-WITH-WARNINGS in the run log — FAIL stops the run: the findings are logged, nothing is created or pushed
3. github-repo + readme — fork dir, license → README.md and LICENSE in the fork dir following the repo standards — stops for approval (the human reads both files and the warnings from step 2)
4. git — `git -C <fork dir> rev-parse --git-dir` (not a repo → `git -C <fork dir> init`), then `git -C <fork dir> add README.md LICENSE` plus each file the forker produced, listed by explicit path (never `-A` or `.`), then `git -C <fork dir> commit -m "Initial sanitized release"` → commit SHA in the run log — `git -C <fork dir> status --short` is empty and README.md and LICENSE are in `git -C <fork dir> ls-tree -r HEAD --name-only`
5. [GO] gh repo create — `gh repo create <owner>/<target_name> --private` — the WAITING FOR GO line names owner, name and `--private`. The run stops here until the human types GO. (`gh repo create` is not hook-guarded; this GO is its only guard.)
6. github — `gh repo view <owner>/<target_name> --json visibility -q .visibility` → run log line — equals `PRIVATE`, else stop
7. [GO] git push — `git -C <fork dir> remote add origin <url>` is part of this step, then the push of the default branch to `origin` — the WAITING FOR GO line names the remote URL, the branch and the commit SHA from step 4. The run stops here until the human types GO. (The hook guards `git push`; the other commands here are not hook-guarded.)
8. github — `gh repo view <owner>/<target_name> --json visibility -q .visibility`, then `gh api repos/<owner>/<target_name>/contents/LICENSE` and `.../contents/README.md` → final run log line — LICENSE and README.md both return 200 on the default branch, else stop; the run log ends with the sanitizer verdict and the line "visibility stays PRIVATE; flipping it is the human's own action"

Run log: `production_artifacts/pb-open-source-<date>.md` in the start directory, never committed

Rules
- This playbook never runs `gh repo edit --visibility` or any other command that changes visibility.
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
