---
name: code-foundation-stinger
description: "Read-only repo health audit: Wasp Nest setup, agent readiness, CI, tests, lint, lockfiles, secrets, governance. Writes contract-shaped foundation findings and measures. Never edits the repo."
license: AGPL-3.0-or-later
compatibility: Claude Code 2.1 or newer, Cursor 2.4 or newer, Codex, Cowork. Scripts need Python 3.11 and git; gh is optional (read-only checks); project test commands run only in a throwaway copy.
metadata:
  author: Legion Code Inc.
  hive-drone: code-foundation-wasp-drone
  pair-drone: code-foundation-wasp-drone
  domain: repository foundation audit
  version: 1.0.0
  research-window: 2026-03-30 to 2026-09-30
---

# Code Foundation Stinger

## Purpose

Answer one question for the `/audit-my-code` run: is this repository set up so humans and AI agents can work in it safely? This is the Foundation dimension every audit tier runs first. It measures the repository against the baseline that `get-started-stinger` establishes (Library Schema v2 tree, `wasp-nest.lock`, CI, dependency automation, CODEOWNERS, README and policy files, `.gitignore` and `.env.example`) and extends it with current repository health practice: OpenSSF Scorecard style checks, whether tests exist and pass, lint and typecheck configuration, lockfile consistency, runtime pins, committed secrets, branch protection, and AI agent readiness (AGENTS.md or CLAUDE.md, size and accuracy). It runs `get-started-stinger` in assess-only mode: where get-started would create something, a finding names the exact step that would fix it. It produces `findings.jsonl`, `metrics.json` and `notes.md` for `00-foundation/` under the Audit My Code contract 1.0 and changes nothing in the audited repository.

## When to use

- The orchestrator dispatches the Foundation dimension for any tier (`foundation`, `vibe`, `basic`, `full`, `mario`)
- "Is this repo healthy?", "do we have CI and tests?", "will an AI agent be able to work in this repo?"
- Before a security or quality audit, to learn whether the build, tests and lockfile are sound enough to audit

## When not to use

- Setting the repository up or fixing what the audit finds: that is `get-started-stinger` (writes files) or the `mario` tier's remediation step
- Vulnerability analysis, exploitability, secret rotation: `security-stinger` and `security-wasp-drone`
- Duplicate, dead or bloated code: `code-bloat-wasp-drone`
- Implementation versus PRD checks: `quality-stinger`
- CI pipeline design depth: `ci-release-stinger`; detailed GitHub settings scoring across eight dimensions: `github-repo-health-stinger`
- README authorship: `readme-writing-stinger`

## Procedure

1. Read [guides/00-scoping-and-read-only-rules.md](guides/00-scoping-and-read-only-rules.md) first. It fixes the hard rules: never modify the audited repository, run project code only in the throwaway copy, GitHub access read-only, secrets redacted.
2. Read `<workspace>/intake.json`. Check tools (`python3`, `git`, `gh auth status`) and record caps.
3. Run `scripts/foundation_scan.py --repo <repo> --gh --out <workspace>/00-foundation/raw/foundation_scan.json` (drop `--gh` if gh is unavailable). It makes the file-presence and API checks and emits contract-shaped findings and measures.
4. Follow guides 01 to 04 in order, reading only what the scanner cannot judge and resolving every finding tagged `needs-drone-read`: [01 Wasp Nest readiness](guides/01-wasp-nest-readiness.md), [02 CI, tests, lint and typecheck](guides/02-ci-tests-lint-typecheck.md) (run commands with `scripts/run_in_copy.py`), [03 dependencies, lockfiles and secrets](guides/03-dependencies-lockfiles-secrets.md), [04 repository governance](guides/04-repository-governance.md).
5. Follow [05 writing metrics and findings](guides/05-writing-metrics-and-findings.md): write `judgment.jsonl` and `measures-extra.json`, run `scripts/assemble_foundation.py` until it validates, write `notes.md`, index the raw artifacts.
6. Return a short report: verdict, counts by severity, measures in `at-risk` or `critical`, caps, output paths.

## References map

| Path | Load when |
| --- | --- |
| `guides/00-scoping-and-read-only-rules.md` | Every run, first |
| `guides/01-wasp-nest-readiness.md` | Library, lock, agent file checks |
| `guides/02-ci-tests-lint-typecheck.md` | Workflow review and running tests, lint, typecheck in the copy |
| `guides/03-dependencies-lockfiles-secrets.md` | Lockfiles, update automation, runtime pins, env files, secret-shaped strings |
| `guides/04-repository-governance.md` | README, license, CODEOWNERS, branch protection, Scorecard view |
| `guides/05-writing-metrics-and-findings.md` | Producing and validating the output files |
| `references/REFERENCE.md` | Map of every reference file |
| `references/foundation-checklist.md` | Every check id, default severity, owner, get-started step |
| `references/get-started-assess-map.md` | Naming the get-started step; what a healthy initialized repo has |
| `references/measures-and-bands.md` | Bands for every `metrics.json` measure |
| `references/scorecard-mapping.md` | Which Scorecard checks are approximated and how |
| `references/gh-readonly-calls.md` | Before any `gh` call |
| `references/detection-patterns.md` | Manual workflow, secrets, lockfile and agent-file checks |
| `references/runtime-eol-table.md` | End-of-life Node and Python pins |
| `references/finding-templates.md` | Writing judgment findings |
| `references/research/distilled-foundation.md` | Verifying a claim or resolving a conflict |
| Source research archive (not shipped with the plugin) | Source-repository only; the shipped distillation summarizes it, do not require it |
| `scripts/foundation_scan.py` | Step 3: deterministic scan, read-only |
| `scripts/run_in_copy.py` | Running project commands in the throwaway copy only |
| `scripts/assemble_foundation.py` | Step 5: validate and write the three output files |
| `scripts/test_foundation.py` | After any script edit: `python3 scripts/test_foundation.py` |

## Related drones and stingers

- [code-foundation-wasp-drone](../../agents/code-foundation-wasp-drone.md) - The paired Drone that runs this Stinger and writes `00-foundation/`.
- [audit-my-code-stinger](../audit-my-code-stinger) - Owns the run contract, tiers and workspace this Stinger writes into.
- `get-started-stinger` - Defines the baseline in assess mode; this Stinger never runs its write steps. Ships with the core Wasp Nest plugin, not this pack.
- `github-repo-health-stinger` - Source of the read-only branch protection and settings checks; use it for the full eight-dimension GitHub hygiene report.
- `security-stinger` - Receives handoffs for committed secrets and workflow injection.
- `dependency-audit-stinger` - Deeper supply-chain triage beyond lockfile and update-tool presence.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - `get-started-stinger` - Baseline for a correctly initialized repository; read in full before the first run.
  - `github-repo-health-stinger` - Read-only GitHub hygiene checks to borrow.
  - `security-stinger` - Where committed-secret and workflow findings go next.

<!-- Ship Gate removed: research-only stinger, produces no committable code. -->
