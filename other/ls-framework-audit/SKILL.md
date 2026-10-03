---
name: ls-framework-audit
description: "Run doc, link, skill matrix, and version/facts checks before release. Single entrypoint script; output to user-specified path only; no in-repo default. Use when user says 'run audit', 'run framework audit', or before release."
metadata:
  version: "1.0"
compatibility: "Python 3.12+ and PyYAML via the framework dependency helper. Skill-sandbox smoke entries depend on ls-skill-sandbox-tester tooling (create_sandbox.py, run_smoke.py); repo-root smoke entries run directly from the repository root."
---

# Framework audit

**Purpose:** One atomic skill and entrypoint to run a release-ready audit: doc checks, link checks, skill matrix smoke checks, version/facts, and optional maintainer-ref flagging. Output is written only to a user-provided path (CLI or env); no default in-repo. Exit 0 only when there are zero errors.

## When to use

- User says "run audit", "run framework audit", or "before release".
- Pre-release: lock in for release; zero errors and zero unexplained warnings.

## Workflow

1. **Run the entrypoint** from repo root: `python ls/skills/ls-framework-audit/scripts/run_framework_audit.py [--output /path/to/report]` or set `LOCALSETUP_AUDIT_OUTPUT` to a writable path. If no output path is given, the script prints a short summary to stdout only; no file is written in the repo. For installed packages, run the package script from the target repo or pass `--repo-root /path/to/repo`; pass `--framework-root /path/to/source/ls` only when auto-detection cannot find the framework source.
2. **Phases:** Root prerequisites; doc checks; local Markdown target and supported ATX-heading anchor checks; plain-text refs to docs/ or ls/ as conversion warnings; skill matrix; version/facts with invalid existing facts treated as errors; and private release refs. Markdown checks skip external URLs, fenced examples, generated/dependency trees, LocalSetup project virtual environments (`.venv/` and `.venv-*/`), and private runtime state.
3. **Report:** Contains every maintainer-reference finding and a `requires_review` / `human_decision` section for items that need user resolution. The script is non-interactive; the agent presents the report and asks the user.
4. **Doc-only skills:** The smoke list marks them as `N/A`. The script does not run tooling for those. The **agent** (not the script) produces an enumerated one-sentence/paragraph per logical step and flags logic gaps for user resolution, per SKILL.md of each doc-only skill.

## Markdown source ownership

Link and maintainer-reference scans exclude root `build/` and `dist/` outputs.
Nested authored paths such as `docs/build/` remain in scope. Retained SDK Markdown
is exempt only when the SDK manifest verifier establishes its exact unchanged
upstream ownership; there is no blanket `vendor/` exemption. New wrapper documents,
locally patched Markdown and authored links into retained files remain checked.
Failed SDK ownership verification is an audit error and grants no exemptions.
Use the SDK payload validator separately for complete vendored-content integrity.

## Smoke list (skill matrix)

- **Path:** `ls/tests/skill_smoke_commands.yaml`
- **Schema:** YAML map: `skill_id` (directory name under ls/skills/) -> `command` string, `"N/A"`, or a mapping shaped like `{cwd: skill-sandbox|repo-root, command: "..."}`. String commands and `cwd: skill-sandbox` mappings run with cwd = sandbox copy of the skill. `cwd: repo-root` mappings run directly from the repository root for tool-backed skills whose executable lives outside the skill directory. `N/A` = doc-only; no runnable smoke; audit uses agent step summary only.
- One entry per skill in `ls/skills/*`. The audit script reads this file as single source of truth for which skills have tooling to smoke.

## Dependencies (framework invariant)

- **PyYAML:** The entrypoint calls the shared `lib.deps.require_deps(["yaml"])` helper at startup, so a missing dependency exits with an actionable install message instead of a bare import failure. Sync framework dependencies with `uv sync --locked --no-dev` or rerun install with `--sync-env`.
- **Sandbox tooling:** The audit may call `ls/skills/ls-skill-sandbox-tester/scripts/create_sandbox.py` and `run_smoke.py` to run skill smoke commands in an isolated copy. Both the audit skill and the sandbox-tester skill ship with the framework; no external dependency.

## Tooling

| Item | Purpose |
|------|---------|
| `scripts/run_framework_audit.py` | Single entrypoint: doc, link, skill matrix, version/facts; output path from CLI or env; exit 0 only if no errors. |

**Quick start:**

```bash
# Output to file
python ls/skills/ls-framework-audit/scripts/run_framework_audit.py --output /path/to/audit_report.md

# Or env
export LOCALSETUP_AUDIT_OUTPUT=/path/to/audit_report.md
python ls/skills/ls-framework-audit/scripts/run_framework_audit.py

# Summary only (no file written)
python ls/skills/ls-framework-audit/scripts/run_framework_audit.py

# Installed package, run from the repo being audited
python ~/.local/share/localsetup/packages/ls-framework-audit/scripts/run_framework_audit.py --output /path/to/audit_report.md

# Explicit target repo and framework source
python ~/.local/share/localsetup/packages/ls-framework-audit/scripts/run_framework_audit.py \
  --repo-root /path/to/repo \
  --framework-root ~/.local/share/localsetup/source/ls \
  --output /path/to/audit_report.md
```

## Errors vs warnings

- **Error:** Invalid repository/framework prerequisites, smoke non-zero/crash, syntax/lint failure, missing required doc, missing local Markdown target or supported anchor, or an existing invalid/versionless facts file. Exit non-zero.
- **Warning:** Missing optional facts, plain-link conversion candidate, N/A, maintainer reference, or another item to fix or explicitly accept; every logical warning is counted and logged in the report. Zero errors and zero unexplained warnings before release.

## References

- ls/docs/TOOLING_POLICY.md (lint/quality; audit uses for tooling expectations)
- ls/docs/INPUT_HARDENING_STANDARD.md (script follows for all external input)
- ls/tests/skill_smoke_commands.yaml (smoke list path and schema)
