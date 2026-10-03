---
name: ls-context
description: "LocalSetup framework context - overview, invariants, resolver rules, install layout, and skills index. Load first when working in a repo that uses LocalSetup."
metadata:
  version: "1.8"
---

# LocalSetup - Framework Context

## Overview

LocalSetup is a repo-local framework for agent context, skills, workflows, adapter materialization, and install/repair tooling. The source checkout may physically contain `ls/`, but `ls/*` is a source layout, not a deployed path contract for agents.

Agents should treat `ls-context` as the broad entry point for framework behavior. Use it before changing LocalSetup-managed assets, generated docs, adapters, package materialization, doctor repair, or install validation.

Related skill: `ls-requesting-code-review` - Use when requesting code review before merge or after substantial changes; provide focused requirements, diff range, and severity-calibrated review instructions.

## Layout Definitions

- **Source root:** the LocalSetup source checkout passed with `--source-root` or inferred by the local tool entrypoint.
- **Framework root:** `<source-root>/ls`; this contains framework code, source skills, source workflows, docs, templates, tools, and config.
- **Docs root:** `<framework-root>/docs`; public framework documentation and generated docs live here.
- **Tools root:** `<framework-root>/tools`; thin tool entrypoints live here.
- **Package root:** the managed user-level package library from `pack.yaml` (`global.package_root`), normally `~/.local/share/localsetup/packages`.
- **Target repo:** the repository being attached, verified, repaired, or converted. It may be different from the LocalSetup source root.

The Linux baseline is Python 3.12+, POSIX paths, non-interactive shells, custom `$HOME`, custom `--source-root`, paths with spaces, user-level install roots, and both symlink and portable adapter modes.

## Resolver Contract

Use resolver-backed paths for agent-facing instructions and deployed package surfaces.

Commands:

```bash
localsetup path --json
localsetup path source-root
localsetup path framework-root
localsetup path docs-root
localsetup path tools-root
localsetup path package-root
localsetup path package ls-context SKILL.md
localsetup path doc WORKFLOW_REGISTRY.md
localsetup path tool tmux_ops
```

`localsetup path --json` writes and prints `~/.local/share/localsetup/paths.json`. Install, self-refresh, register-shell, and doctor repair also refresh that manifest through LocalSetup-native tooling. If the source root or home changes, rerun one of those commands.

Resolver tokens are allowed in source-authored package files:

- `localsetup://doc/WORKFLOW_REGISTRY.md`
- `localsetup://tool/tmux_ops`
- `localsetup://package/ls-context/SKILL.md`
- `localsetup://package/<package>/<relative/path>`

During package materialization, resolver tokens are replaced with absolute paths derived from the current resolver manifest and package root. Deployed packages must not contain unresolved `localsetup://...` tokens.

## Path Safety Rules

LocalSetup validates external path inputs at boundaries. Reject NUL bytes, parent traversal, empty path segments, absolute Windows drive paths, home escapes, and unsafe relative segments.

Python subprocess calls should pass argv lists with `shell=False`. Shell snippets must quote absolute paths safely and avoid unquoted variable expansion.

Do not add symlink fanout into target repos. Use the managed package root and adapter materialization model.

## Adapter And Package Model

Source packages live under `localsetup://package/<name>/...` only after materialization. Source skill and workflow directories under `<framework-root>/skills` and `<framework-root>/workflows` are authoring inputs.

Adapters such as `.codex/skills`, `.claude/skills`, `.cursor/skills`, `.kilo/skills`, `.openclaw/skills`, and `.opencode/skills` are shared surfaces. Preserve custom adapter content by default. Same-directory custom skills, collisions, or unmanaged content require a repair decision, not silent relocation.

Package materialization copies source packages into the managed package root, rewrites public doc references, bundles public doc closure under `references/localsetup/docs`, writes a reference-bundle manifest, and validates the deployed package surface.

Materialization omits Python bytecode (`*.pyc`, `*.pyo`, and `__pycache__/` trees),
matching the source archive's bytecode boundary. It preserves other source assets,
including hidden files and package data; it does not use blanket Git-ignore filtering.

## Recursive Path Contract

Whole-project reprocessing treats every tracked text-bearing file as a complete unit. It excludes `.git`, caches, private maintenance state, build artifacts, and ignored runtime state.

Targets include Markdown, Python, shell, YAML, JSON, TOML, text files, executable wrappers, templates, generated docs, workflow manifests, skills, references, scripts, assets, and docs.

For each file, the reprocessor records pre/post hashes and rewrite actions. Source-maintained files may use resolver tokens. Deployed package output must reject `ls/...`, `./ls/...`, `../../docs/...`, unresolved `localsetup://...`, and dangling LocalSetup-owned absolute paths unless the path is intentionally source-only metadata. Preserve Python imports such as `ls.core...`; those are module imports, not filesystem instructions.

## Doctor And Repair

Use `localsetup doctor` and `localsetup doctor repair` before manual edits to managed adapter shapes, package markers, registries, lockfiles, shell shims, and resolver manifests.

Doctor detects missing or stale `paths.json`, stale shell shim exports, old package roots, adapter links pointing at old roots, package marker or registry drift, lockfile mismatch, adapter collisions, package-surface validation failures, and legacy LocalSetup path references.

Repair is conservative:

- report-only first by default,
- explicit apply for mutations,
- journal and backup touched files,
- refuse ambiguous target-project paths,
- preserve repo-owned adapter content,
- rematerialize managed packages instead of patching deployed packages by hand,
- verify after apply.

## Public And Private Context Boundary

Public framework docs, generated docs, templates, tests, examples, and package/catalog surfaces are publishable. Create new private maintenance plans, audits, indexes, credentials, logs, caches, ledgers, and planning transcripts only under `.agents/state/<task-slug>/`; the controller assigns one Git-bound task slug for every agent and tool to reuse. Existing client-specific run directories are historical records and remain in place.

Do not put private task ledgers into `ls/docs/` or package surfaces unless explicitly authorized as public framework documentation.

## Founding Principle: Eliminate Friction and Ambiguity

Prefer the existing owner and simplest clear path. Improve or consolidate existing tools, workflows, docs, and checks before creating another one. Add new material or process steps only for a concrete requirement the current owner cannot meet, and keep the addition scoped. See the [founding workflow design principle](../../docs/WORKFLOW_STANDARD.md#founding-design-principle) and follow [Validation Expectations](#validation-expectations) for check scope.

For long-running interactive work, keep the human operator oriented with concise, periodic progress updates. Use the [human progress signal guidance](../ls-communication-and-tools/SKILL.md#human-progress-signals) for terminal/TUI formatting and queue counts.

## Generated Docs And Volatile Facts

When source docs, workflows, skills, pack metadata, or generated-document inputs change, refresh generated docs from the LocalSetup source checkout. Resolve that checkout first so these source-relative paths do not depend on the caller's working directory:

```bash
(
set -euo pipefail
source_root="$(localsetup path source-root)"
cd -- "$source_root"
uv run --locked python ls/tools/generate_docs_artifacts.py --repo-root .
uv run --locked python ls/tools/localsetup.py --source-root . generate-docs
)
```

Before editing latest/current external claims, check `.agents/state/volatile-facts.yaml` if it exists. Verify volatile claims from primary upstream sources and keep the volatile fact index private and untracked.

## Validation Expectations

Use focused validation first, then broaden when shared install, package, doctor, or publish behavior changes.

These installed commands can run from a target repository:

```bash
localsetup doctor
localsetup doctor repair --repair-mode report-only
localsetup verify --level filesystem
localsetup context --markdown
```

The remaining validators and tests are source-checkout-only. Resolve and enter the LocalSetup source root before using their checkout-relative paths:

```bash
(
set -euo pipefail
source_root="$(localsetup path source-root)"
cd -- "$source_root"
uv run --locked python ls/tools/localsetup.py --source-root . validate-catalog
uv run --locked python ls/tools/localsetup.py --source-root . validate-package-surface
uv run --locked python ls/tools/localsetup.py --source-root . generate-docs
uv run --locked python ls/tools/generate_docs_artifacts.py --repo-root .
uv run --locked ls/tests/automated_test.sh
workers="$(uv run --locked python ls/tools/localsetup.py --source-root . test-workers)"
uv run --locked pytest -n "$workers" ls/tests -q
)
```

Run focused pytest files or test functions and matching LocalSetup validators before the full suite. Resolve the permitted worker count with `localsetup test-workers`; [COMMAND_REFERENCE.md](../../docs/COMMAND_REFERENCE.md) owns its formula and aggregate-budget rule. Use the full suite as final consolidation for broad/shared runtime changes, release or publish work, dependency changes, or explicit user requests.

Unless a repository explicitly defines a stricter policy, every unit-test runner—regardless of language or framework—uses one aggregate budget of `max(1, floor(available CPU cores / 3))`. Round down before applying the minimum of one worker; concurrent test processes share the budget.

Before publish, run publish preflight against the intended base and keep generated docs/version sync with the repo tooling.

## Invariants

- Never commit repo-local secrets or PII.
- Use LocalSetup-native tooling before manual edits to managed adapter shapes, symlinks, skills, packages, registries, lockfiles, or installed assets.
- `ls/docs/` is public framework documentation, not private maintenance state.
- Check document status before treating framework docs as authoritative.
- Framework changes follow the active PRD and document lifecycle rules where applicable.
- For dates and times, obtain the actual local machine time before making time-sensitive claims.
- Treat external input as hostile. Sanitize before parsing or output, validate expected format and bounds, and emit actionable errors.
- New or substantially refactored framework tooling is Python-first and Python-only after install/bootstrap; shell and PowerShell stay thin.
- Python architecture: new and substantially refactored Python tooling follows `localsetup://doc/PYTHON_ARCHITECTURE_STANDARD.md`; keep entrypoints thin, package responsibilities explicit, and existing debt baseline-managed.
- Python-first tooling does not mean using Python for normal shell inspection; use `rg`, `sed`, `find`, `wc`, and `git` where appropriate.
- Preserve mature skill/context capability over brevity. Whole-file rewrites require a preservation plan; large reductions require coverage notes and reviewer signoff.

## Output contract (low token, always apply)

- Detect output capability: `markdown-rich`, `markdown-basic`, or `text-basic`.
- If unknown, default to `markdown-basic`.
- Recommendation lists include name/link, short summary, fit reason, notable risks/requirements, and clear next step.
- Use tables only when the output surface clearly supports readable tables.

## Agent Orchestration And Model Budget

Use the smallest capable model for inventory and low-risk scouting. Escalate for security, release blockers, architecture, and high-risk review findings only when uncertainty, risk, or complexity justifies it.

For current model names, routing preferences, pricing, limits, and rate-card handling, verify the provider's official documentation or current product source before making cost-sensitive decisions.

## Skills Catalog

- Current generated catalog: `localsetup://doc/SKILLS.md`.
- Machine-readable generated facts: `localsetup://doc/_generated/facts.json`.
- Skill taxonomy source: `<framework-root>/config/pack.yaml`; generated view: `localsetup://doc/_generated/skill-taxonomy.json`.
- Treat short skill mentions in always-loaded platform context as orientation only; generated catalog and each skill's frontmatter are the current source of truth.
- `ls-nodejs-nextjs`: Node.js/Next.js/React runbook.
- `ls-github-starredrepos`: GitHub starred repository archive workflow.
- `ls-codex-heartbeat`: opt-in heartbeat harness.
- `ls-shadcn-ui`: shadcn/ui component workflow.
- `ls-omniroute-update`: OmniRoute update reporting.
- `ls-typescript-code-quality`: TypeScript/TSX code quality.
- `ls-ui-browser-debugging`: UI review and browser-driven debugging with Chrome DevTools MCP.

## Key Docs

Resolve these with `localsetup path doc <name>` when a directly followable path is needed:

- `AGENTIC_DESIGN_INDEX.md`
- `WORKFLOW_REGISTRY.md`
- `PRD_SCHEMA_EXTERNAL_AGENT_GUIDE.md`
- `DECISION_TREE_WORKFLOW.md`
- `INPUT_HARDENING_STANDARD.md`
- `TOOLING_POLICY.md`
- `PYTHON_ARCHITECTURE_STANDARD.md`

## Task-To-Skill Matching

- Treat as batch when the request has multiple distinct subtasks or asks to run the whole workflow.
- If the user names a specific skill, load it directly.
- If uncertain which skill fits, or the user asks what skill to use, load `ls-task-skill-matcher`.
- Keep matching behavior short here; detailed matching belongs to `ls-task-skill-matcher`.

## Proportional validation and evidence reuse

Run inexpensive checks and focused tests while editing. One successful full
suite for the final candidate is sufficient; authoritative CI may provide it.
Do not run another local suite or repeat a successful suite for the same tested
inputs just because a task moves from PR to main or publication. Record the
commit, environment, command/workflow, and result; invalidate evidence only when
relevant inputs change. Bound long jobs, preserve successful jobs when retrying
an understood failure, and stop automatic retries on an unexplained failure.
Complete source changes and the release record before generating final docs.

LocalSetup's hosted implementation uses eight isolated Python shards with an
all-shards success gate and exact-commit Actions evidence. The publishing workflow
checks that evidence before building instead of running the full suite again.
See [repository maintenance](../../docs/REPO_MAINTENANCE.md#validation-reuse).
