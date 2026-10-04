---
name: claude-jev-coding
description: "Select bounded repository context with Jev file-relevance judgments before implementing a coding task (feature, fix, refactor, tests) in the current Claude Code session. Use when the user asks for Jev context selection or claude-jev-coding in a Git checkout."
---

# Claude Code + Jev

You (the current Claude Code session) implement, review and test the change with your normal tools. Jev only judges which repository files are relevant. Do not start Codex, Astra or another coding agent for generation. This Skill does not change your model or effort.

## Entrypoint and credentials

The supported runtime is the prebuilt Go executable in `bin/astra-jev`. Python and Go are not needed during coding. Build once with `scripts/build-native.sh` (Go 1.26+ and a C compiler), or use the matching platform release archive. Do not rebuild, benchmark or run model comparisons during normal coding. The historical `.py` files remain development references.


Run `"<base directory of this Skill>/scripts/context.sh" <command> ...` using the absolute base directory shown when the Skill loads. Quote it; it may contain spaces. The wrapper resolves its symlink to `bin/astra-jev claude-code` in the linked Harness checkout. `doctor` reports the checkout and whether a key is available, without calling a provider or printing the key.

An existing `TYPESAFE_API_KEY` takes precedence. On macOS the helper can read login Keychain service `astra-jev-harness`, account `TYPESAFE_API_KEY`, into its own process only. Never print keys, pass them as arguments, search `.env` files, or forward them. A missing key blocks new Jev requests, not valid cached judgments or otherwise authorized local work. A Keychain timeout does not prove the key is absent.

## Workflow choice

Jev supplies relevance judgments; it is not a prerequisite for every authorized coding action. A user's no-Jev/local choice applies to the current task and its in-scope follow-ups until they change it. Do not ask for the same permission again or run Jev planning or credential checks merely to satisfy this Skill.

When required files exceed planning limits, credentials are unavailable, or a provider fails, stop the affected Jev operation. State the reason and **“Jev selection unverified / Jev未検証 — continuing locally”** once, then continue already-authorized investigation, implementation and tests using [Local continuation](references/workflow.md#local-continuation). If successful Jev evaluation is an explicit acceptance condition, keep that item incomplete while independent local work continues. Repository safety rules and external-action boundaries still apply.

## Context workflow

1. Confirm the task and checkout. Read its CLAUDE.md/AGENTS.md, check branch, HEAD and status, and preserve existing changes.
2. On the Jev path, before reading implementation file bodies, write a focused task file outside the target and run `plan --repo <absolute-root> --task-file <file> --out <new-dir-outside-target>`. Read `PLAN.md` only (not `plan.json`). Untracked files need repeated `--include-file`; pin known task-critical files with `--focus-file`. For large repositories, scoping, or planning failures, read `references/workflow.md`. During local continuation, a sufficient existing plan is optional; bounded native reads may supply the real task scope.
3. On the Jev path, run `select --plan <plan-dir> --out <new-selection-dir> --max-calls <n> --mode auto` within the existing authorization and request cap. `auto` keeps all candidates and skips Jev under 12,000 source bytes; it is not an offline guarantee. Use `--mode jev` when a real Jev evaluation is requested, and `--mode local` for local continuation with a sufficient plan. Claude's wrapper supports local select/check/read directly. The cap defaults to 4 (maximum 24). An external-call ban rules out new Jev requests. The helper makes no automatic retries, and a failed attempt may still be billed. Preserve failure receipts before continuing locally.
4. When using a selection, read `REPORT.md` and only the metadata you need from `selection.json`: `decisions`, `unjudged_paths` and `metrics`. Do not dump `context.json`. Read bodies with `read --selection <dir> --path <relative-path> --start-line <n> --end-line <n>` (default 80 lines, maximum 200 lines or 24 KB). Uncertain, unjudged and dependency files are retained on purpose. A relevance score is not a security check.
5. Run `check --selection <dir>` before editing from a selection, or recheck local contents when using native reads. Then implement and test directly in this session within the user's scope. The plan and selection grant no permission to edit, commit, push or take external actions.
6. On the Jev path, source changes require a fresh plan for more context. During local continuation, refresh local source/freshness checks without forcing a return to Jev. Inspect saved attempts before deciding whether another run is necessary; never blindly repeat a potentially completed operation.

Keep routine replies focused on changes, verification and actionable blockers. Do not append or aggregate Jev request counts, token usage, cache reuse, cost or output-byte statistics for narration. Show accounting only when explicitly requested, using saved receipts without extra calls or benchmarks. Keep attempts, completed calls, reuse and missing usage distinct. Internal receipts remain available for limits and failure recovery. Report implementation and tests independently of selection; the helper cannot measure Claude Code conversation tokens or cost, and a smaller context is not a proven saving.

The helper rejects plans and selections from the Codex Desktop or CLI surfaces. It has no `run`, `verify` or `apply` commands. Selection artifacts contain source text. Keep them outside the target repository and out of Git.

For offline policy comparison (`compare`), evidence packets, caches and scope limits, read `references/workflow.md`.
