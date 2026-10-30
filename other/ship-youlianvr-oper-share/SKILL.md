---
name: ship
description: >-
  Delivering changes safely: release preparation, dependency audits and scoped
  updates, secrets hygiene, changelog generation, Git conventions and worktrees,
  GitHub Actions, PR comment handling and CI repair, Cloudflare and Vercel
  deploys, technical-change and technical-debt tracking, operational runbooks.
  One contract; parts under parts/.
---

# ship — delivering and maintaining releases

> Home branch in Memora: `root/skill/ship`.
>
> Safety rail across every part: publishing, tagging and deploying are separate
> authorizations. A part may prepare everything and still stop before the public
> action.

## Choosing a part

**Releasing and dependencies**

| Part | What it covers |
|---|---|
| `parts/release/` | Prepare a named version: preflight, version consistency, build/package, smoke test, checksums and notes — stops before any public release action |
| `parts/dependency-auditor/` | Audit dependencies across multi-language projects: vulnerabilities, licenses |
| `parts/dependency-update/` | Scoped dependency updates: release notes first, explicit scope only, no update-everything |
| `parts/env-secrets-manager/` | Environment-variable hygiene and secrets safety, local to production |

**Deploys**

| Part | What it covers |
|---|---|
| `parts/cloudflare-deploy/` | Workers, Pages, D1/R2, wrangler flows and Workers compatibility checks |
| `parts/vercel-deploy/` | Vercel projects, environment variables, build settings and preview deployments |

**VCS and change tracking**

| Part | What it covers |
|---|---|
| `parts/git/` | Git mechanics on top of `BOOT.md` §6: conventional commits, branch naming, staging hygiene |
| `parts/git-worktree-manager/` | Parallel feature work via worktrees: branch isolation, safe cleanup |
| `parts/github-actions-docs/` | Workflow syntax, caching, matrices, common gotchas |
| `parts/gh-fix-ci/` | Read a failing check, reproduce it, repair the cause |
| `parts/gh-address-comments/` | Work through review comments on a PR without losing the thread |
| `parts/changelog-generator/` | Release notes from conventional commits |
| `parts/tc-tracker/` | Technical-change records as Memora nodes: what, why, tested how, where work stands |
| `parts/tech-debt-tracker/` | Scan for debt, prioritize it, and keep the backlog in Memora across snapshots |

**Operations**

| Part | What it covers |
|---|---|
| `parts/runbook-generator/` | Operational runbooks from a service name: deploy, incident response, maintenance |

## Rules

- **Commit and push rules live in `BOOT.md` §6.** `parts/git/` adds mechanics
  (conventional subjects, branch names, staging hygiene) and never overrides the
  runbook; push, deploy, PR and tag need the owner's word, one action each.
- **Release covers both worlds.** Our projects publish through
  the project's own publish procedure (subtree split into their own repository); an outside
  package follows its registry flow. `parts/release/` names which path applies
  before it starts.
- **Trackers write to Memora.** A technical change and a debt item are nodes
  under `root/project/<name>` (or `root/skill/ship` for workspace-wide work);
  the JSON/Markdown registries of the old parts are not the source of truth, and
  the retired `docs/` layer is never recreated.
- **Large parts are read by section.** `cloudflare-deploy` alone is 2.1 MB: open
  the section the task needs, never the whole tree, and never paste it into
  context "for background".
- **Forks worth `ask_questions`**: a version number that is not in the request, a
  dependency bump that changes public behavior, a deploy target, anything paid,
  and any publish or tag. Preparation is silent, publication is not.
- **Secrets** never appear in logs, commits or chat; key names live in `TOOLS.md`.

## Related

`dev` (writing the code), `loops` (unattended work never deploys), `review`
(`verify`), `mcp` (tool surface for CI and repositories).
