---
name: ls-skill-sandbox-tester
description: "Test normalized skills in a bounded temporary staging copy before production. Creates a provenance-marked copy under platform temp, rejects symlinked inputs, runs smoke checks with a minimal environment, and uses ls-debug-pro on failure; no writes return to the repo until user approval. Use when validating a framework-compliant skill end-to-end on a supported platform."
metadata:
  version: "1.0"
compatibility: "Python 3.12+ for any bundled tooling. Sandbox paths follow platform temp (Linux /tmp, macOS /tmp or $TMPDIR, Windows %TEMP%). Resolves skill paths per ls/docs/PLATFORM_REGISTRY.md. Tooling must follow ls/docs/TOOLING_POLICY.md and INPUT_HARDENING_STANDARD.md."
---

# Skill Sandbox Tester

**Purpose:** Validate skills in a bounded temporary staging copy so bugs are found and fixed before production promotion. The helpers enforce copy provenance, temporary-root containment, symlink rejection, and environment minimization; **ls-debug-pro** owns the fix loop. No changes return to the repository until the user approves.

## When to use this skill

- User wants to "test this skill," "validate the skill after import," "run the skill in a sandbox," or "make sure the skill works before we use it."
- After a skill has been vetted and normalized (not right after import), user wants to run it safely in a sandbox and fix any issues before production.
- User wants to confirm a skill runs correctly on a supported platform listed in PLATFORM_REGISTRY without affecting the repo.

## How it actually works

**Testing:** The skill does not run a built-in test suite. You (the agent) choose a **smoke command** that should succeed if the skill is healthy: for example, run the skill's main script with `--help`, a dry-run/list mode, or the verification command documented by its SKILL.md. The tooling copies the skill to a provenance-marked directory under platform temp, rejects source and staged symlinks, and runs that command from the copy with an allowlisted environment and sandbox-local home and temp paths. **Pass** = exit 0. **Fail** = non-zero exit or crash.

**Debugging:** When the smoke command fails, this skill does not implement the fix. You **load ls-debug-pro** and follow its 7-step protocol (reproduce, isolate, hypothesize, instrument, verify, fix, regression). The important rule: **all reproduction and edits happen in the sandbox copy only.** You run the failing command in the sandbox, inspect logs or add print/debugger, change code in the sandbox, then run the same smoke command again from the sandbox. Repeat until the smoke command exits 0. Only then do you summarize the changes and **ask the user** to approve copying those fixes from the sandbox into the real skill directory (e.g. `ls/skills/<name>/`). No writes to the repo until the user says so.

**End-to-end flow:**

1. Create sandbox: copy the skill to a temp dir (e.g. via `create_sandbox.py`).
2. Run smoke: execute your chosen command in that dir (e.g. via `run_smoke.py`). Check exit code.
3. If exit 0: report "smoke passed"; done unless the user wants more checks.
4. If non-zero: load debug-pro, reproduce and fix **inside the sandbox**, re-run the same smoke command in the sandbox until it passes.
5. After it passes: summarize what you changed in the sandbox and ask the user to approve applying those changes to the real skill; only then copy back and (if needed) run deploy.

The sandbox tester provides bounded **staging and run** behavior; debug-pro provides the **how to fix** when that command fails. This is not an OS security sandbox: a command can still use absolute paths, spawn processes, access the network, or mutate external systems. Choose non-destructive smoke commands and obtain every approval those effects require.

## Rule ownership

This skill owns post-normalization skill validation behavior. Public validation docs describe patterns and examples; this skill is the execution contract for sandbox creation, smoke selection, debug handoff, and copy-back approval.

- Never run sandbox testing before vetting and normalization have completed.
- Never write sandbox fixes back to the repo without user approval.
- Smoke commands must run inside the staged copy and be selected not to write outside it. The helper minimizes cwd and environment exposure but cannot enforce filesystem, process, network, or external-service confinement.

## Design: use debug-pro in conjunction

This skill does **not** duplicate the debugging methodology. When a smoke run fails:

1. **Do not** write fixes back to the repo.
2. **Load and follow ls-debug-pro** for the 7-step protocol (Reproduce, Isolate, Hypothesize, Instrument, Verify, Fix, Regression Test) and for language-specific debugging (Python, Node, Swift, network, git bisect).
3. Apply fixes in the **sandbox copy** of the skill only; re-run smoke in the sandbox until it passes.
4. Only after smoke passes, present a summary and ask the user to approve writing changes back (e.g. from sandbox to `ls/skills/<name>/` or the deployed path).

This keeps a single source of truth for debugging (debug-pro) and a clear separation: sandbox tester = staging + run + smoke + orchestration; debug-pro = how to fix failures.

## Supported platforms

Skill paths and context loaders are defined in [ls/docs/PLATFORM_REGISTRY.md](../../docs/PLATFORM_REGISTRY.md). The canonical client contract is `ls/config/clients.yaml`; LocalSetup generates `ls/config/platforms.yaml` as the runtime projection. The sandbox tester follows that current adapter model:

| Platform/runtime | Skills root model |
|----------|-------------------------------------|
| Framework source | `ls/skills/ls-*/` (canonical source) |
| Adapter-managed platforms | Use the repository skills root declared by the client registry (currently shared `.agents/skills/` for Codex and OpenClaw, `.agents/skills/` then `.cursor/skills/` for Cursor, plus `.claude/skills/`, `.kilo/skills/`, and `.opencode/skills/` for their owning clients) |

Resolve the skill directory from current context and registry mapping: if working in the framework repo, use `ls/skills/<name>/`; if the user refers to a deployed path, use the adapter path from the generated platform projection. The helper reads that projection when a framework checkout is discoverable and uses a deterministic copy of the same current repository roots when the skill has been copied standalone. Historical `.codex/skills/` is a migration/repair surface, not a current Codex discovery root. Adapter directories are shared or client-owned as declared by the registry; preserve unmanaged entries. Do not assume a bare repo-root `skills/` directory as a default root. Test using the same platform the user is on so behavior matches production.

## Tooling

Python 3.12+ scripts under `scripts/` (per TOOLING_POLICY and INPUT_HARDENING_STANDARD). Run from repo root or from the skill directory; paths below are relative to the skill (e.g. `ls/skills/ls-skill-sandbox-tester/` or deployed equivalent).

| Script | Purpose |
|--------|---------|
| `scripts/create_sandbox.py` | Copy a symlink-free skill into a unique, provenance-marked directory under platform temp. Prints the skill-copy path for `run_smoke.py`. |
| `scripts/run_smoke.py` | Validate that marked copy, reject arbitrary or symlinked directories, and run one command there with an allowlisted environment and sandbox-local home/temp paths. Exit code matches the command. |

**Quick start (by name):**

```bash
SANDBOX=$(python3 ls/skills/ls-skill-sandbox-tester/scripts/create_sandbox.py --skill-name ls-pr-reviewer)
python3 ls/skills/ls-skill-sandbox-tester/scripts/run_smoke.py --sandbox-dir "$SANDBOX" --command "python3 scripts/pr_review.py --help"
```

**By path:**

```bash
SANDBOX=$(python3 ls/skills/ls-skill-sandbox-tester/scripts/create_sandbox.py --skill-path ls/skills/ls-pr-reviewer)
python3 ls/skills/ls-skill-sandbox-tester/scripts/run_smoke.py --sandbox-dir "$SANDBOX" --command "python3 scripts/pr_review.py --help"
```

Smoke passes if the command exits 0. On non-zero, use ls-debug-pro in the sandbox; do not write to the repo until the user approves.

## Workflow (agent steps)

### 1. Identify skill and sandbox need

- **Input:** Skill name (e.g. `ls-pr-reviewer`) or path. Resolve to the skill directory per platform (see above).
- **Read/write need:** If the skill has no scripts or side effects (e.g. doc-only), you can run a lightweight check (e.g. parse SKILL.md, check frontmatter). If the skill has `scripts/` or clearly writes output (state files, reports), treat it as needing a sandbox.
- **Staging only when needed:** Create the bounded temporary copy when the skill will read or write; otherwise a quick static validation may suffice without staging.

### 2. Create unique sandbox (when needed)

- **Location:** Use platform-appropriate temp: Linux `/tmp`; macOS `/tmp` or `$TMPDIR`; Windows `%TEMP%` or `%TMP%`. See ls-safety-and-backup for temp file policy.
- **Naming:** Unique dir to avoid collision, e.g. `skill-sandbox-<skill-name>-<timestamp>` or `mktemp -d` (Bash) / `tempfile.mkdtemp` (Python). Example: `/tmp/skill-sandbox-ls-pr-reviewer-20260220-120000`.
- **Contents:** Copy the complete skill directory after rejecting every source symlink. The helper records source/copy provenance beside the copy; `run_smoke.py` rejects missing, malformed, moved, or inconsistent markers and symlinks introduced after staging.
- **Cleanup:** Remove the sandbox when the test session is done, or leave it for inspection when the user wants to debug; document the path.

### 3. Run smoke

- **Entrypoints:** Run the skill's main entrypoints from its SKILL.md with minimal safe arguments such as `--help` or a documented dry-run/list mode. The runner removes inherited `PYTHONPATH` and non-allowlisted variables, then supplies home, XDG, and temp paths under the staged copy. For framework scripts that import `deps`, create the copy with `--shared-deps ls/lib/deps.py`. This explicitly stages only that bounded, regular, nonsymlink file under the sandbox root at `.localsetup-runtime/lib/deps.py` and records its relative path and SHA256 in the provenance marker. Before execution, the runner validates the declaration, file hash, containment, symlink absence, and absence of undeclared library files; it sets `PYTHONPATH` only to that staged library. Without the option, no `PYTHONPATH` is supplied. The helper never injects checkout `ls/lib` or inherited import paths; installed third-party dependencies still come from the selected interpreter. The framework audit supplies this explicit helper for skill-sandbox entries.
- **Smoke criteria:** Exit code 0 for success paths; expected stdout/stderr shape; and no intended writes outside the staged copy. Because this is a staging boundary rather than OS confinement, use only commands whose filesystem, process, network, credential, and external-service behavior is already understood and authorized.
- **Platform:** Run in the same environment the user is on (same OS, same interpreter) so results are valid for that platform.

### 4. On success

- Report that the skill passed smoke and is ready for production use. Optionally suggest one more check (e.g. run one real scenario with user approval). Do not write to the repo unless the user asks to promote or commit.

### 5. On failure (debug loop)

- **Do not write to the repo.** All fixes happen in the sandbox copy.
- **Load ls-debug-pro** and follow its 7-step protocol and language-specific commands. Reproduce in the sandbox, isolate, hypothesize, instrument, verify, fix in sandbox, then re-run smoke in the sandbox.
- **Iterate** until smoke passes. If the user wants to bring in other skills (e.g. ls-receiving-code-review for review of the fix), use them in the loop.
- **After smoke passes:** Summarize changes made in the sandbox. Ask the user to approve applying those changes to the real skill location (e.g. copy fixed files from sandbox to `ls/skills/<name>/`). Only then write to the repo; then run deploy if needed so the platform gets the updated skill.

## Framework standards

- **Tooling:** Any script added to this skill (e.g. a Python helper to create sandbox and run smoke) must be Python 3.12+, per ls/docs/TOOLING_POLICY.md. Shell/PowerShell only for minimal platform entrypoints if required.
- **Input hardening:** Any tool that takes paths, skill names, or env must follow ls/docs/INPUT_HARDENING_STANDARD.md: sanitize input, validate paths and bounds, emit actionable stderr, no silent failure.
- **Documentation:** Keep this SKILL.md and any references in sync with PLATFORM_REGISTRY and the framework docs index.

## Related skills

| Skill | Role |
|-------|------|
| **ls-debug-pro** | Use when smoke fails: 7-step protocol and language-specific debugging. Fix in sandbox; do not duplicate its content here. |
| **ls-safety-and-backup** | Temp file policy (/tmp, mktemp, cleanup); use for sandbox location and cleanup. |
| **ls-skill-vetter** | Security check before normalization; run after import. |
| **ls-skill-normalizer** | Run after vetting. Brings the skill to framework compliance (doc/spec, platform-neutral, tooling). **Run sandbox tester only after normalization is done.** Running it sooner is unsafe: the skill may not comply yet and failures will be noisy and misleading. |
| **ls-skill-importer** | Brings the skill in; then vet and normalize. Do not run sandbox tester right after import. |
| **ls-skill-creator** | New skills can be tested with this skill after they are normalized and ready. |
| **ls-framework-compliance** | If changes are written back to the framework, follow checkpoints and testing after modifications. |

## Reference

- ls/docs/PLATFORM_REGISTRY.md - Supported platforms and skills paths.
- ls/docs/TOOLING_POLICY.md - Python-first tooling, runtime target.
- ls/docs/INPUT_HARDENING_STANDARD.md - Mandatory input handling for any script.
- ls/docs/SKILLS_AND_RULES.md - How skills are loaded and where they live per platform.
