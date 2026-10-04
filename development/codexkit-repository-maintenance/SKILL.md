---
name: codexkit-repository-maintenance
description: Use when maintaining or improving the GameStudio-CodexKIT source repository, including CI, governance, catalog, generators, adapters, packaging, documentation, versioning, or release readiness.
---

# CodexKIT Repository Maintenance

## Overview

Maintain and improve this repository without confusing kit-source work with game-project work. Keep the main thread responsible for repository integration, route specialist analysis to existing distributed skills, edit canonical sources, and bind every verdict to evidence.

## Repository identity gate

Before any write, resolve the repository root and verify all of these facts:

- `.codex-plugin/plugin.json` exists and declares `game-studio-codex-kit`.
- `registry/capabilities.yaml` exists.
- `scripts/validate.py` exists.
- `skills/` exists.

If any check fails, stop with `BLOCKED: repository identity mismatch`. Do not reinterpret another repository as CodexKIT and do not apply this workflow to a game project that merely installed the plugin.

## Scope

Use this skill for repository architecture, skill or agent authoring, registries, packs, personas, generators, adapters, project initialization, GitHub Actions, tests, packaging, documentation, versioning decisions, release readiness, and evidence-backed technical-debt cleanup.

Keep gameplay, content, services, assets, and operational changes in consuming game projects outside this workflow. Treat private studio projects, `.research/`, and external repositories as read-only unless a separate explicit request authorizes their use.

## Intake

1. Record repository path, branch, requested outcome, owned write scope, do-not-touch scope, and current tracked or untracked changes.
2. Read `AGENTS.md` and the relevant canonical files before selecting an edit.
3. Classify the request using the routing table.
4. Preserve unrelated work and assign one writer per file, shared registry, or generated output.

## Routing

| Maintenance class | Route or evidence source |
|---|---|
| Failure, regression, CI, or unexpected behavior | `evidence-first-debugging` and the exact failing command or Actions log |
| Skill creation, revision, trigger collision, provenance, or maturity | `skill-authoring-and-audit` |
| Build, test, package, runtime, or cross-platform verification | `build-and-runtime-verification` |
| Broad diff or independent review | `review-swarm` with read-only review lanes |
| Candidate readiness or semantic-version decision | `release-candidate-preflight` |
| Multi-agent ownership | `studio-agent-orchestration` after repository scope is fixed |

Routing does not transfer repository integration ownership. Reuse the specialist workflow; do not copy it into this skill.

## Maintenance workflow

1. Reproduce the failure or collect concrete evidence for the requested improvement.
   Completion criterion: the current behavior, gap, or drift is observable and classified as `Verified`, `Snapshot`, `Unverified`, or `BLOCKED`.
2. Trace the root cause to a canonical source, registry, generator, test contract, environment, or CI platform boundary.
   Completion criterion: the selected owner explains the observed evidence without relying on a generated-file patch.
3. Define the smallest complete write scope and restore path.
   Completion criterion: owned paths and do-not-touch paths are explicit, and unrelated work remains preserved.
4. Write or update failing tests before production behavior when the task changes executable behavior.
   Completion criterion: the test fails for the missing behavior rather than a fixture or syntax error.
5. Edit canonical sources only.
   Completion criterion: no generated adapter, pack, or `skills/*/scripts/` file was hand-patched.
6. Regenerate only affected resources and inspect the visible diff.
   Completion criterion: generated outputs match their canonical owners and unmanaged project-local files remain untouched.
7. Run focused verification, then every local gate required by `AGENTS.md`.
   Completion criterion: each command has an exit code and any artifact path required for a PASS claim.
8. Inspect distribution and version impact.
   Completion criterion: internal maintenance files remain outside registries, packs, adapters, scaffold templates, and plugin version changes unless the distributed payload actually changed. Any plugin version change remains `BLOCKED` for deploy or release readiness until every required GitHub Actions job for the exact pushed commit and version reaches terminal PASS; local PASS is not a substitute.
9. Produce the handoff.
   Completion criterion: the report contains scope, changes, evidence, risks, restore information, and separately authorized next actions.

## Canonical ownership rules

- Change a distributed skill under `skills/`, then synchronize its bundled resources through `scripts/sync_skill_resources.py`.
- Change root helpers under `scripts/`; never patch mirrored `skills/*/scripts/` copies.
- Change agent-role catalog entries through `agents/` and `registry/agent-roles.yaml`; never patch scaffold copies directly.
- Change plugin metadata only when distribution changes require it.
- Keep `.agents/skills/codexkit-repository-maintenance/` and `.codex/agents/codexkit-maintainer.toml` repository-local. Never add either ID to registries, packs, adapters, or project scaffold templates.

## Verification ladder

Start with the narrowest affected test, then run:

```text
python -B scripts/sync_skill_resources.py . --check
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate.py .
python -B scripts/route_eval.py .
python -B scripts/secret_scan.py .
python -B scripts/policy_check.py .
python -B scripts/external_collision_eval.py .
python -B scripts/doctor.py --check --root .
```

Run lifecycle audits and governed dogfood commands when their evidence is required. Unavailable upstream content, model runners, session history, or live projects remain `BLOCKED`; they never become PASS.

## Handoff

Return repository path, branch, goal, owned scope, do-not-touch scope, changed files, commands and exit codes, artifacts, `Verified` results, `Snapshot` assumptions, `Unverified` hypotheses, `BLOCKED` items, failures, decisions, restore information, next actions, and a reactivation prompt. Commit, push, publish, deploy, and release remain separate actions requiring explicit authorization.
