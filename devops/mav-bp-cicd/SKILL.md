---
name: mav-bp-cicd
description: Platform-agnostic CI/CD conventions. Covers pipeline stages, quality gates, environment promotion, secrets management, artifact handling, and deployment boundaries. Applied when configuring or reviewing CI/CD pipelines.
user-invocable: false
disable-model-invocation: true
---

# CI/CD Standards

Pipeline standards and the post-push monitoring loop. CI is the last
line of defence for autonomous work: it does not hallucinate, skip
steps, or declare success prematurely.

## Maverick's Rules

- **Every stage gates the next**; cheapest checks first (lint/typecheck),
  expensive last. **Never skip stages** — no `[skip ci]`, no conditional
  bypasses for "quick fixes".
- **Build once, promote the same artifact** — never rebuild for
  production; only environment config changes between environments.
- **Secrets come from the platform's secret store**, never the
  repository. Pin action/image versions.
- **Production deploys are human-gated.** Hotfixes follow the same
  pipeline, just expedited.
- Failing gates are fixed, never bypassed — no `--no-verify`, no force
  merge, no editing gate config to get green (gate configuration is
  infrastructure; see Boundaries).

## Monitoring CI After Push

After every push, monitor the pipeline with the platform CLI, read the
failed job's logs, fix locally, and re-push. From a `do-issue-*`
workflow, use the bounded wait: `uv run maverick pr wait <repo> <pr-num>
--checks --timeout 30m`.

| Platform | Status | Logs |
| --- | --- | --- |
| GitHub Actions | `gh run list --branch <br>` / `gh pr checks <pr>` | `gh run view <id> --log-failed` |
| GitLab CI | `glab ci status` | `glab ci trace <job>` |
| Azure DevOps | `az pipelines runs list --branch <br>` | `az pipelines runs show --id <id>` |
| Bitbucket Pipelines | `curl .../2.0/repositories/<ws>/<repo>/pipelines/?sort=-created_on` | pipeline page / API step logs |

Anything genuinely project-specific (required checks, runner quirks,
deploy targets) belongs in the project skill, not here.

## Project Implementation Lookup

Check `docs/maverick/skills/cicd/SKILL.md` for the project's pipeline
platform, stages, required checks, and deployment targets. If present,
it wins on specifics. If missing, proceed with these standards and note
the gap in your summary — do not trigger skill generation mid-task.

## Detecting CI/CD Issues in Code Review

| Pattern | Issue | Fix |
| ------- | ----- | --- |
| No CI pipeline in repository | No automated quality enforcement | Add pipeline with validate/build/test stages |
| Pipeline has no lint/typecheck stage | Style and type errors reach main | Add validate stage before build |
| Tests run but failures don't block merge | False confidence | Make test stage a required gate |
| Secrets in pipeline YAML or repo files | Security risk | Move to platform secret store |
| Pipeline rebuilds for each environment | Inconsistent artifacts | Build once, promote artifact |
| No manual gate for production deploy | Risk of unreviewed production changes | Add manual approval step |
| Pipeline takes >15 minutes | Developer productivity drain | Profile and optimise, add caching |
| Unpinned action/image versions | Non-reproducible builds | Pin to specific versions/SHAs |

## Boundaries

Never, without explicit issue authorization (per
`mav-scope-boundaries`): create or modify pipeline
configuration, change stages/jobs/gates, touch CI secrets or environment
variables, or trigger production deployments. Always: monitor CI after
pushing and fix failures before declaring work complete.

<!-- maverick-plugin-version: 4.0.2-dev -->
