---
name: pb-docs-site
description: >-
  Publish a project's docs as a static HTML manual on GitHub Pages: check
  that Pages is enabled, bring the wiki up to date, list the doc gaps, build
  the site, preview it locally and push it after GO. Use for "publish the
  docs", "docs site", "put the manual on GitHub Pages".
category: design-ui-ux
kind: playbook
trigger: ["publish the docs", "docs site", "manual on GitHub Pages"]
inputs: [repo, source]
requires:
  skills: [openwiki-skill, readme, documentation, bdbhtmlmanueldocs, github, "gh (external)"]
  agents: []
  mcps: []
  store: []
go_points: ["git push"]
outputs: ["docs/", "production_artifacts/pb-docs-site-<date>.md"]
verify: "gh api repos/<owner>/<repo>/pages -q .status == built; curl -sI <pages_url> returns 200"
difficulty: intermediate
est_time: 30-90 min
---

# Publish a docs site
What you get: the project's docs as a static HTML manual on GitHub Pages, pushed only after your GO.

## Inputs
- repo — the local checkout, default the current directory; `<owner/repo>` comes from `git -C <repo> remote get-url origin`
- source — where the content lives: OpenWiki pages, the README, or `docs/`

## Steps
1. Preflight — `gh auth status`, then `gh api repos/<owner>/<repo>/pages` → run log header — gh missing, unauthenticated or no GitHub remote → log it, give the `gh auth login` / remote hint, stop; 404 → stop with "Pages not enabled: enable it in repo settings", this playbook does not enable Pages; a private repo whose Pages call is refused for plan reasons → stop with "Pages on a private repo needs a paid plan", and never change the repo's visibility. Then openwiki-skill — wiki refreshed or confirmed current → log line — Pages answered and the wiki is current
2. readme and documentation — `source` against the code → list of doc gaps in the run log — stops for approval
3. bdbhtmlmanueldocs — approved content → site files in `docs/` (or the Pages source path the step 1 response names) — files written, nothing committed; the skill's Pages build-type switch (`gh api -X PUT .../pages`) and its Pages deploy workflow are NOT run here, only the site files are written
4. Preview — a local preview link or the path to the built `index.html` in the run log — link or path given
5. [GO] git push — the site files committed to the branch and path the step 1 response names as the Pages source; the WAITING FOR GO line names the branch and the file list. The WAITING FOR GO line also says: a Pages site of a private repo is public. The run stops here until the human types GO. The hook guards `git push`; it does not guard `gh api` settings writes, so no Pages setting or workflow is changed in this playbook.
6. github — `gh api repos/<owner>/<repo>/pages -q .status` equals `built` (poll, at most 5 minutes), then `curl -sI <pages_url>` → status line in the run log — returns 200

Run log: `production_artifacts/pb-docs-site-<date>.md` in the start directory, never committed

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
