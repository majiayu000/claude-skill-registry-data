---
name: scbe-gitlab-pond-integration
description: "Integrate GitLab as a second pond (lore/research) alongside GitHub (code/product) for SCBE. Use when tasks involve GitLab repos, cross-pond mirroring/sync, GitLab auth failures, or keeping flows unblocked with a read-only 'pond flush' health check before/after PR/CI work."
---

# SCBE GitLab Pond Integration

This skill treats GitLab as a **separate execution pond** (lore, long-form docs, large research bundles) that feeds GitHub (code + public surfaces) through explicit, safe flows.

The goal is not "one monorepo to rule them all". The goal is **stable inlets/outlets**.

## Configuration (do not leak secrets)

- GitLab token is stored in: `C:\Users\issda\SCBE-AETHERMOORE\config\connector_oauth\.env.connector.oauth`
- Variable name: `GITLAB_TOKEN`
- Never paste tokens into chat, commit logs, or URLs.

## Meridian / Pond Flush (read-only health check)

Run this before triage or mirroring to detect blockages without spending full energy:

```powershell
pwsh -File "C:\Users\issda\SCBE-AETHERMOORE\scripts\gitlab\pond_flush.ps1" `
  -GitLabRepoUrl "https://gitlab.com/<group>/<project>.git" `
  -CheckGhAuth
```

Outputs:
- local time + timezone
- GitLab token validity (via API)
- project visibility/default-branch (if accessible)
- optional GitHub `gh auth status`

## Mirror GitHub -> GitLab (write action)

Use the repo script (token is injected safely; output sanitized):

```powershell
pwsh -File "C:\Users\issda\SCBE-AETHERMOORE\scripts\gitlab\mirror_push.ps1" `
  -GitLabRepoUrl "https://gitlab.com/<group>/<project>.git" `
  -Branch "main"
```

For full mirror:

```powershell
pwsh -File "C:\Users\issda\SCBE-AETHERMOORE\scripts\gitlab\mirror_push.ps1" `
  -GitLabRepoUrl "https://gitlab.com/<group>/<project>.git" `
  -PushAllBranchesAndTags
```

## How this skill interweaves with the GitHub skills

Use these deterministic hooks:

1. If CI is failing and you suspect "it passed locally" drift, run the **pond flush** first.
2. If PR comments request "move docs/lore to GitLab", mirror after the PR is green.
3. If a GitHub Pages funnel page needs long-form evidence, keep the canonical research in GitLab and publish a stable excerpt/entrypoint on GitHub Pages.

## Failure modes + self-healing

- `401/403 from GitLab API`: token missing/expired/scope issue. Fix token in the `.env.connector.oauth` file; rerun pond flush.
- `project not found`: wrong path or token lacks access. Confirm group/project path in `GitLabRepoUrl`.
- `rate limit / 5xx`: pause, rerun pond flush (no need to push).

## Output contract

When using this skill, always report:
- the GitLab repo URL (sanitized; no token)
- whether pond flush passed
- whether mirroring was performed
- what GitHub surface (PR/page/docs) was fed by the mirror

## Smoke test (both ends)

Use this to validate: token -> API -> project -> flush -> push -> verify.

```powershell
pwsh -NoProfile -File "C:\Users\issda\SCBE-AETHERMOORE\scripts\gitlab\smoke_test.ps1" `
  -ProjectName "scbe-pond-mirror-test" `
  -Visibility "private" `
  -Branch "mirror-smoke"
```

Safety:
- Add `-SkipCreate` if you do not want scripts creating new projects.
- Use unique branch names like `agent/<lane>-smoke` to avoid collisions.
