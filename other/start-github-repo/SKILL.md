---
name: start-github-repo
description: "Scaffold a complete, production-grade GitHub repository from zero for a TypeScript/Node or Cloudflare Workers project, including README, AGENTS.md, LICENSE, CODE_OF_CONDUCT, CHANGELOG, .github issue forms and PR template, hardened workflows, SECURITY.md, SUPPORT.md, CODEOWNERS, env examples, automation scripts, docs/, and a PRD/TRD/TOGAF-ADM/WIREFRAME/DESIGN document spine with a traceability matrix and TDD gates. Use when starting a new repository, bootstrapping or scaffolding a project skeleton, adding the document spine to an existing repo, or auditing a repo against this template. Triggers on 'start a new repo', 'scaffold a repository', 'new project skeleton', 'set up repo structure', 'add PRD and TRD', 'repo template'. For standardizing an existing repo against an external preset catalog, use github-repository-setup instead."
license: MIT
compatibility: "Requires Python 3.9+ (stdlib only) for the bundled scripts. Optional: gh CLI for remote settings, Node 20+ for design.md linting."
metadata:
  version: 1.0.0
  entrypoint: "/start-github-repo"
  argument-hint: "[plan | docs | audit | <profile>]"
  disable-model-invocation: false
  profiles: "worker-service, ts-library, monorepo, docs-site, internal-tool"
---

# Start GitHub Repo

Scaffold a complete repository in one pass. Templates are **bundled** in `assets/templates/` — no
network fetch, no external catalog. Pinned versions live in `assets/versions.json`; never hardcode a
version number in prose.

## Modes

| Invocation | Behaviour |
|---|---|
| `/start-github-repo` | Interview → plan → confirm → scaffold → validate → summarize |
| `/start-github-repo plan` | Print the resolved file list and answers. Write nothing. |
| `/start-github-repo docs` | Emit only the document spine into an existing repo |
| `/start-github-repo audit` | Report missing or stale template artifacts. Never writes. |
| `/start-github-repo <profile>` | Skip the profile question |

## Workflow

1. **Classify.** If the target directory is non-empty, inspect it first and switch to merge
   behaviour: diff every file, never overwrite without showing the diff and getting approval.
2. **Interview.** Ask at most eight questions, each with a default so `--defaults` can skip them:
   project name · description · profile · license · visibility · package manager · CoC reporting
   contact · release tooling. Derive everything else.
3. **Plan.** Run `scripts/scaffold.py --dry-run` and show the tree plus every required secret by
   name and purpose. Get confirmation before writing.
4. **Scaffold.** `scripts/scaffold.py` renders `assets/manifest.json`. Use `--only docs` for docs
   mode, `--force` only after an approved diff.
5. **Validate.** Run `scripts/validate_repo.py` and `scripts/validate_docs.py`. Both must exit 0.
6. **Hand off.** Report unresolved `TODO`/`[NEEDS CLARIFICATION]` markers, required secrets, and
   remote settings still to apply. Remote mutations are a **separate, individually confirmed step**.

## Hard rules

- Never overwrite a file without a diff and explicit approval.
- Never invent commands. Emit only scripts the chosen profile actually supports.
- Never write a secret value. `.env.example` and `.dev.vars.example` carry empty values only.
- Every placeholder must be resolved or reported. Unresolved markers go in the final summary.
- Pin every third-party action to a full-length commit SHA and set least-privilege `permissions:`.
- File generation is local and safe. `gh api` ruleset creation, label sync and repository-settings
  changes each need their own approval.

## References

Read the one that answers the question in front of you. Do not read all of them.

| File | Answers |
|---|---|
| `references/document_spine.md` | Section-by-section specs for PRD, TRD, WIREFRAME, DESIGN, ADRs and the TOGAF ADM-lite `docs/architecture/` set |
| `references/github_platform.md` | Community health file placement, issue forms, PR templates, CODEOWNERS, rulesets, Actions hardening, Dependabot, Scorecard |
| `references/release_and_versioning.md` | changesets vs release-please, Keep a Changelog, SemVer, Conventional Commits, licensing and SPDX |
| `references/cloudflare_worker_repo.md` | wrangler config, `.dev.vars`, `wrangler types`, the Vitest plugin rename, secrets |
| `references/repo_hygiene_and_scripts.md` | `.gitignore`/`.gitattributes`/`.editorconfig`, env layering, secret scanning, hooks, `scripts/` conventions |
| `references/traceability_scheme.md` | The five ID families, the matrix, and commit/PR/test wiring |

## Scripts

All stdlib-only, deterministic, `--output {text,json}`.

| Script | Purpose |
|---|---|
| `scripts/scaffold.py` | Render `assets/manifest.json` into a target dir. `--dry-run --only --force` |
| `scripts/validate_repo.py` | Artifact presence plus structural traps (workflow permissions, SHA pins, ignored `.env`) |
| `scripts/validate_docs.py` | Required headings, ID formats, matrix integrity, unresolved clarification markers |
| `scripts/traceability.py` | Rebuild the matrix from PRD IDs, test names and commit scopes; report orphans both ways |

## Adjacent skills

- `github-repository-setup` — brownfield audit against an external preset catalog. Use it to
  standardize a repo that already exists; use this skill for day zero.
- `spec-driven-workflow`, `tdd`, `togaf-advisor`, `senior-architect` — deepen individual artifacts
  after scaffolding.
