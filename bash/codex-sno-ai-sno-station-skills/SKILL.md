---
name: codex-coder
description: Route production coding tasks to the user-level Shell, TypeScript, Python, or Rust Codex workflow. Use for "codex-coder", "Codex write", "generate with Codex", language migrations, or mixed Shell/TypeScript/Python/Rust implementation when Codex should choose the correct language specialist automatically.
requires:
  programs: []
  harness:
    - {slot: 4.shell, need: required}
    - {slot: 4.file-read-write, need: required}
---

# Codex Coder Router

Carry the task's finite time budget into the coding assignment, including test time.
Require a duration estimate before each targeted test run; full evaluation, unit,
integration, or repository suites require the owner's explicit request, not dispatcher
approval. New security checks require the owner's specific approval; auxiliary checks
must not block the requested function or development work.

Act as a thin dispatcher. Select the language skill, then let that skill own repository discovery, prompting, implementation, verification, and refinement. Do not keep a second copy of language rules here.

## Codex runs with the sandbox off

Keep the owner's configured `sandbox_mode = "danger-full-access"`; do not override it
in a dispatch, config, flag, or profile. A connection or credential error does not identify
its cause. Inspect the effective configuration, actual endpoint, and error; repair the
observed cause within existing authority. Preserve valid results from unaffected tests.

## Route the Target Language

Use this precedence order:

1. The language or destination the user explicitly requested.
2. The files the task must create or change.
3. The repository's manifest, immediate callers, and nearby tests.
4. For a migration, the language being produced; treat the source language as context.
5. For generated code, the maintained source or generator language unless the user explicitly asks to edit generated output.

Ask one concise clarification only when those signals still do not identify the destination. Do not infer a language from personal preference or tool availability.

| Destination | Strong signals | Required skill |
|---|---|---|
| Bash or shell | `.sh`, a Bash shebang, shell CLI, automation, process wrapper, or Git/infra helper | `$shellscript-coder` |
| TypeScript or TSX | `.ts`, `.tsx`, `.mts`, `.cts`, `tsconfig.json`, a typed Node or React target | `$ts-coder` |
| Python | `.py`, `pyproject.toml`, Python service, package, script, or test target | `$python-coder` |
| Rust | `.rs`, `Cargo.toml`, Cargo workspace, crate, Rust CLI, service, library, or FFI target | `$rust-coder` |

JavaScript without a TypeScript target is not automatically TypeScript. An unsupported destination must be surfaced instead of silently routed to the nearest skill.

## Load the Canonical Skill

Resolve the user-level skill root as `${CODEX_HOME:-$HOME/.codex}/skills`. For every selected language:

1. Read the corresponding `SKILL.md` completely.
2. Read every reference that skill marks as required for the task.
3. Follow that skill as the execution contract, including its context gathering, language rules, direct implementation, verification, and correction loop.

The canonical entrypoints are:

- `${CODEX_HOME:-$HOME/.codex}/skills/shellscript-coder/SKILL.md`
- `${CODEX_HOME:-$HOME/.codex}/skills/ts-coder/SKILL.md`
- `${CODEX_HOME:-$HOME/.codex}/skills/python-coder/SKILL.md`
- `${CODEX_HOME:-$HOME/.codex}/skills/rust-coder/SKILL.md`

Do not substitute a generic coding workflow or launch a nested Codex process. The selected language skill executes directly in the current session.
After completing TypeScript or Python implementation, run `$code-simplifier`, when it is installed, on the changed production code before final verification.

## Mixed-Language Work

Use every language skill required by the requested output. Keep one shared task plan and one cross-language contract.

1. Identify the files and contract owned by each language.
2. Settle shared schemas, wire formats, command behavior, and error semantics before implementation.
3. Implement the contract owner first, then its consumers.
4. Apply each language skill only to its language's files.
5. Run each language's focused checks plus the smallest cross-language integration check.

Do not force a mixed task through one specialist and do not launch competing implementations of the same contract.

## Failure Boundary

The language skills are optional. If a selected language skill is not installed, follow the repository's own conventions and say which skill was missing; if an installed skill names a reference that is missing, search its installed roots, read it, and resume. Continue independent repository inspection meanwhile. Ask only for access or an artifact that investigation proves only the owner can supply; do not park the task or emulate unread instructions.
