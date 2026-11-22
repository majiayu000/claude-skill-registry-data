---
name: governance
description: Run Yuzu's Codex governance review pipeline on a commit range with slash-name parity to Claude `/governance`. Use when the user says `/governance <range>`, "full governance", or asks for the multi-gate security/docs/domain/ops review on commits or a PR.
---

# Governance

Run Yuzu governance as a Codex-native review fanout. This skill may use Codex subagents because invoking `/governance` is an explicit request for delegated review. Keep each delegated role bounded to review only; do not let review agents edit files.

## Range

- Default range: `dev..HEAD`.
- Treat a bare commit like `HEAD` as `HEAD~1..HEAD`.
- If `dev..HEAD` is empty on branch `dev`, ask whether `origin/dev..HEAD` is intended.

## Gates

1. Change Summary: write this locally from `git log`, `git diff --stat`, and targeted diffs.
2. Mandatory review: launch `security-guardian` and `docs-writer` in parallel.
3. Domain review: select roles by changed files and launch them in parallel.
4. Correctness review: launch `happy-path`, `unhappy-path`, and `consistency-auditor` in parallel.
5. Chaos analysis: run only if Gate 4 produced unhappy-path or consistency findings.
6. Operational review: launch `compliance-officer`, `sre`, and `enterprise-readiness` in parallel.
7. Findings resolution: consolidate findings and fix blocking items.
8. Iteration and ledger: re-run affected gates, record deferrals, and make the blocking decision.

Blocking contract: **identical to the Claude runner — load it, do not restate it.** Read the "Shared preamble" severity block in `.claude/skills/governance/SKILL.md` and apply it verbatim: severity is DERIVED from TRIGGER + IMPACT + EXPOSURE + EPISTEMIC STATUS per that block's own closed lists (do not enumerate the IMPACT/EXPOSURE codes here — a second copy of the list is exactly the restatement the next line forbids), `BLOCKING` = a derived band of CRITICAL or HIGH, and the policy floors gate independently of the derivation. MEDIUM/SHOULD findings need either a fix or an explicit deferral with an issue.

This file MUST NOT carry its own copy of the severity rule. The two runners advertise parity; a second copy is how they drifted into enforcing different gates (found in #2623 re-review).

## Gate 1 Output

Include:

- commits in scope: sha, subject, branch/push state if known
- files touched: path and behavioral delta
- interfaces affected: REST, stores, proto, plugin ABI, CLI/env, CI, docs
- security surface: opened, closed, or net neutral
- Resource Ledger for C++ changes: every new or modified fd, HANDLE, SOCKET, `FILE*`, `sqlite3_stmt*`, `sqlite3*`, OpenSSL object, BCrypt handle, allocated C string, mapped library, temp path, subprocess, callback context, and thread; for each, name the owner type, acquisition point, release point, transfer behavior, and failure cleanup
- user-facing impact and compatibility notes
- validation already performed with exact commands and exit status
- Gate 3 roles selected and why

## Role Prompts

Use compact role prompts and include the Gate 1 summary plus prior gate findings as context.

- `security-guardian`: read every modified file; check authz, ownership, validation, audit, command execution, path handling, crypto, secret handling, sibling handler parity, and new error branches. For C++ diffs, also require an ownership proof for every raw resource boundary: fd, HANDLE, SOCKET, `FILE*`, `sqlite3_stmt*`, `sqlite3*`, OpenSSL/BCrypt object, allocated C string, thread, callback context, subprocess, mapped library, and temp path must have exactly one owner; manual cleanup must be wrapped in a small RAII/scope guard; every early return between acquire and release must be checked. Findings use CRITICAL/HIGH/MEDIUM/LOW/INFO with file:line and recommended fix. Gating is decided by the canonical derived band and policy floors, never by this prompt.
- `docs-writer`: check REST docs, user manual, CHANGELOG, upgrade notes, permission/audit/error tables, and operator workflow docs. Findings use BLOCKING/SHOULD-FIX/NICE-TO-HAVE.
- `architect`: public contracts, stores, REST boundaries, schema, lifecycle, coupling, and hard-to-reverse design.
- `cpp-expert`: C++23 correctness, idioms, standard-library use, ABI boundaries, threading primitives, and cross-compiler portability across GCC, Clang, MSVC, and Apple Clang.
- `cpp-safety`: RAII ownership, lifetime, move/copy semantics, C ABI boundaries, `std::string_view`/`std::span` validity, cast safety, thread lifetime, syscall/process boundaries, shell execution, and sanitizer coverage. Leaks, double-close risk, UAF risk, unjoined/detached thread ambiguity, unsafe shell construction and borrowed data escaping its owner are policy floors under the canonical rule — report them; the floor, not this prompt, is what gates.
- `quality-engineer`: test seams, integration coverage, fixture isolation, flaky patterns, temp DB/path hygiene, weak assertions. For C++ safety-sensitive changes, require coverage for cleanup paths, partial failure, short read/write, EINTR, failed `pclose`, failed `CloseHandle`, failed `sqlite3_prepare`, and concurrent teardown where relevant; for new RAII wrappers, require a test or compile-time assertion covering move-only/non-copyable behavior when feasible.
- `build-ci`: Meson, vcpkg, workflows, release scripts, runner assumptions, cache behavior.
- `plugin-developer`: plugin descriptors, SDK boundaries, YAML definitions, plugin execution behavior.
- `gateway-erlang`: rebar3, OTP supervision, cowboy/gun/gpb, gateway proto mirrors, EUnit/CT/Dialyzer implications.
- `dsl-engineer`: CEL, scope DSL, YAML DSL, trigger templates, validation and backward compatibility.
- `cross-platform`: Darwin, Linux, Windows/MSVC, paths, sockets, filesystem, service behavior.
- `performance`: SQLite hot paths, BFS/graph traversals, authz loops, gateway throughput, allocations.
- `release-deploy`: Docker, packages, systemd, installers, upgrade and rollback behavior.
- `happy-path`: trace normal request/store/plugin/gateway flows end to end and call out idempotency.
- `unhappy-path`: produce a risk register with ID, trigger, symptom, severity, and chaos candidate.
- `consistency-auditor`: check sibling parity, error/audit naming, schema/docs/tests drift, and CHANGELOG ordering.
- `chaos-injector`: convert Gate 4 risk registers into executable chaos test designs; do not run them.
- `compliance-officer`: SOC 2 control alignment, evidence chain, audit traceability, retention, approvals.
- `sre`: health/readiness, metrics, alerts, recovery, capacity, backpressure, runbooks.
- `enterprise-readiness`: pilot-visible rough edges, upgrade notes, breaking changes, customer assurance.

## Domain Routing

Always include `quality-engineer` for feature or bug-fix changes. Always include `architect` for public store contracts or REST API surfaces. Always include `performance` for `get_*_ids`, SQLite BFS/graph traversal, or per-authz hot paths.

Always include `cpp-expert` and `cpp-safety` when C++ files change. Also include `cpp-safety` for any diff that introduces or modifies `popen`, `system`, shell strings, `fork`/`exec`, `CreateProcess`, `dlopen`, `LoadLibrary`, `open`, `socket`, `sqlite3_prepare`, `EVP_*_new`, `BCrypt*`, `LocalAlloc`, `yuzu_ctx_*`, `raw()`, `release()`, `reinterpret_cast`, `const_cast`, or a background thread/callback that stores a pointer or reference. Run `rg` over changed C++ files for raw resource APIs and verify owning raw resource boundary hits appear in the Resource Ledger.

Use `$yuzu-proto`, `$yuzu-plugin-abi`, `$yuzu-meson`, `$yuzu-windows-msvc`, and `$yuzu-build` when the changed files touch their domains.

## Ledger

Write the per-finding JSONL fragment exactly as the canonical skill specifies — the recipe
and the field table both live in `.claude/skills/governance/SKILL.md` under Gate 8, and are
deliberately not restated here. Default location `governance.d/`, committed with the work
it reviews; `YUZU_GOV_LOG_DIR` redirects a throwaway local run outside the tree. A Codex
governance pass that produces no fragment has not finished.

Then end with a human-readable governance ledger:

- Gate status table: role, result, blocking count, deferred count
- Blocking findings with owner/fix status
- Deferred findings with issue number or explicit rationale
- Re-review scope and result
- Final decision: PASS / PASS WITH DEFERRED / BLOCKED
