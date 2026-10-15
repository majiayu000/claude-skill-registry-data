---
name: pb-deploy-saas
description: >-
  Deploy a SaaS app to the BDB fleet: preflight of the fleet skills, a guardrail plan, green CI, the deploy after GO (Incus via
  Forgejo CI, or direct rsync), and a health URL check. Use for "deploy this to the
  fleet", "deploy the SaaS app", "ship to the Incus instance".
category: saas-ops
kind: playbook
trigger: ["deploy this to the fleet", "deploy the SaaS app", "deploy to the Incus instance"]
inputs: [repo, target_instance, path, "version_source?"]
requires:
  skills: [bdb-deploy, pb-ci-fix, "bdbsaashost (external)", "deploy-incus (external)"]
  agents: []
  mcps: []
  store: []
go_points: [deploy]
outputs: ["production_artifacts/pb-deploy-saas-<date>.md"]
verify: "curl -sI <health_url> returns 200; the version marker read in step 5 equals the deployed commit SHA, or the run log says marker absent: unverified"
difficulty: advanced
est_time: 30-90 min
---

# Deploy a SaaS app to the fleet
What you get: the app deployed to the chosen fleet instance after your GO, with a health check logged.
Availability: internal. Needs the bdbsaashost skill (not shipped; lives in aos-internal-staging).

## Inputs
- repo — the current directory, or the one the user names
- target_instance — the fleet instance to deploy to, asked if missing
- path — `incus-ci` (push to Forgejo, the runner deploys to Incus) or `direct` (rsync over SSH), asked if missing
- version_source (optional) — where the app exposes its commit SHA: a `/version`-style URL or a response header name of the health URL, taken from the deploy plan; none given means the app exposes none

## Steps
1. Preflight — bdbsaashost is listed in the harness skill list, or its SKILL.md exists under the harness skills dir (`~/.claude/skills`, `~/.agents/skills`, `~/.codex/skills`, `~/.config/opencode/skills`); same check for deploy-incus (needed only for path = incus-ci) → run log header — bdbsaashost absent → stop with "Missing skill: bdbsaashost (internal, not shipped; lives in aos-internal-staging) — stop"; deploy-incus absent with path = incus-ci → stop with "Missing skill: deploy-incus (installed locally only, not shipped by AOS)."; write nothing except the run log — all probes answered
2. bdbsaashost (external) — repo, target_instance → deploy plan with target, guardrails and the health URL in the run log — stops for approval (the human confirms target, path and health URL)
3. pb-ci-fix — only if `gh run list --commit <HEAD sha> --limit 1 --json conclusion` for the repo is not `success` (a repo with no GitHub CI is logged and skipped) → one pb-ci-fix run, with its own GO for the push — latest run is green, else stop
4. [GO] deploy — path = incus-ci: deploy-incus pushes the repo to the Forgejo remote, the go-gate hook covers the push where it runs (Claude Code, OpenCode, agy); path = direct: bdb-deploy runs `rsync` over SSH to the target, which the hook does not cover (the same goes for `incus` commands), so this GO is the only guard there — RemoteOS approval does not cover a Forgejo push or an rsync, only actions run through its own tools (for example container manage), which this step does not use. The WAITING FOR GO line names the path, target_instance, the exact command, and the commit SHA. The run stops here until the human types GO. One GO = one deploy.
5. Health check — `curl -sI <health_url>` for the status line; then the marker from `version_source` (`curl -s <version_url>` for a URL, or the named header in the `curl -sI` output) → status line and marker in the run log — status 200 and the marker equals the SHA from the step 4 GO line; if `version_source` is empty or returns no marker, log "marker absent: unverified" and accept the 200 alone; a marker that differs from the SHA, or any other status, stops the run and reports, no automatic rollback

Run log: `production_artifacts/pb-deploy-saas-<date>.md` in the start directory, never committed

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
- GO is by contract in every harness. The go-gate hook is only a backstop on Claude Code, OpenCode and agy (Codex: unverified; Cursor, Kimi: none). A missing hook is never permission to proceed.
