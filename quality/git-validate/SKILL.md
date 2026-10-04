---
name: git-validate
description: Validation gate của repository, bắt buộc đạt trước commit, push hoặc Pull Request
user-invocable: true
---

# Git Repository Validation Gate (`/git-validate`)

**Output language:** Mirror the invoking prompt. Canonical tokens, paths and commands remain language-invariant.

Dùng trước commit, push hoặc Pull Request. Gate fail closed: chỉ `READY` khi mọi check bắt buộc đạt.

## Project ownership

Read `# Project Ownership: solo|team` and `# Agent Execution: direct|orchestrated` in `.sdd/shared_context.md`. `--project-ownership=solo|team` overrides only this delivery setting; `Agent Execution` does not affect delivery validation.

Resolve governance fail closed: use canonical settings only when both headers exist exactly once and are valid. Only when both canonical headers are absent may exactly one valid legacy source map to `solo/direct` or `team/orchestrated`: exactly one `# Collaboration Mode: solo|team` header or exactly one `--team-size=solo|team`. Duplicate, malformed or coexisting legacy sources are `BLOCKED`; emit a migration warning and never rewrite governance automatically. Missing, duplicate or malformed canonical headers are `BLOCKED`; never fallback legacy. When either canonical header exists, `--team-size` is `BLOCKED`; the alias is valid only when both canonical headers are absent. `--team-size` cannot be combined with `--project-ownership` or `--agent-execution`; the conflict is `BLOCKED`. A legacy header alongside canonical headers is ignored for resolution and recorded for migration cleanup.

Solo ownership runs the full gate; `--scope=pr` validates direct-delivery readiness before Human push. Team ownership requires `--strict` for `--scope=pr`.

## Parameters

- `--scope=commit|pr`: Required.
- `--feature=<feature-slug>`: Optional; limits SDD checks to feature.
- `--base=<branch>`, `--head=<branch>`: Used with `pr`.
- `--strict`: Turns `WARNING` into `BLOCKED`; required for team PR.
- `--project-ownership=solo|team`: Optional delivery-policy override.
- `--team-size=solo|team`: Deprecated composite alias for one transition release.

## Mandatory rules

1. Do not commit, push, merge, create PR or modify files.
2. Never expose secret values; report only masked path/pattern evidence.
3. Do not report `PASS` for unrun work. Valid results are `PASS`, `FAIL`, or `N/A (reason)`.
4. Missing command/prerequisite is `N/A` with reason; source behavior needing unavailable test command is `FAIL`.
5. Do not auto-fix, reset, checkout, stash, amend or discard changes.
6. Stop at the relevant gate and state remediation on failure.

## Procedure

### 1. Repository and diff source

Read `AGENTS.md`, `CLAUDE.md`, `CONSTITUTION.md`, shared context and `.sdd/architecture-profile.md`.

- `commit`: inspect staged diff; block detached HEAD, active Git operation or empty staged diff.
- `pr` for team or after Human push: use `origin/<base>...origin/<head>`; block missing refs, dirty worktree, local/remote mismatch or empty remote diff.
- `pr` for solo before Human push: use `origin/<base>...HEAD`; stale remote reference is advisory `WARNING`, never claimed as remote verification.

### 2. Security and file policy

Scan the selected diff for credential patterns and forbidden paths from current contract. `.env.example` placeholders are allowed. Block likely real credentials or forbidden files only; do not print values. `CONSTITUTION.md` changes require matching RFC `APPROVED`.

### 3. SDD governance and validation route

- Changed `.sdd/features/*/SPEC.md`: require `/sdd-lint --feature=<slug>`.
- Changed `src/`, `tests/`, feature Plan/Tasks, `CONSTITUTION.md`, `CLAUDE.md`, `AGENTS.md`: require `/sdd-audit` for feature or repository.
- Changed Spec, usecase, test or `@ears`: require `/sdd-trace --feature=<slug> --diff`.
- Changed feature registry or shared context: require `/sdd-sync` first.

Fail for lint/hard-rule audit/trace failure, missing or stale review evidence, unlocked Spec when source/test changes, or source behavior without requirement/test evidence.

### 4. Post-code review

A diff changing implementation behavior, tests, API/public/shared contract, runtime/dependency/security configuration, persistence schema or business state needs `.sdd/reviews/post-code-<feature>-<delivery-or-timestamp>.md` with canonical recommendation, Human Final Review `APPROVED`, changed boundary, `REQ-XXX` coverage, exact result, lint/audit/trace/sync state and residual risk. Docs-only changes do not need post-code review merely because they are Markdown. Ownership does not change this gate.

### 5. Test and quality gate

Run ordered exact approved commands from Architecture Profile: test, lint, typecheck and build. Commands require both approval and manifest/CI evidence. Missing suitable command/test for source behavior is `FAIL`; core-only template without executable source/test is `N/A` with reason; command/profile conflict or execution failure is `FAIL`.

### 6. Result

```text
GIT VALIDATION: READY | BLOCKED
scope: commit | pr
project ownership: solo | team
source: <staged diff | origin/base...origin/head>

[PASS] repository integrity — evidence
[PASS] secret and forbidden-file scan — evidence
[PASS] constitution and RFC policy — evidence
[PASS|N/A] SDD lint/audit/trace/sync — evidence or reason
[PASS|N/A] post-code review — evidence or reason
[PASS|N/A] tests/lint/typecheck/build — command/result/reason

blockers:
- <path:line or command and remediation>
warnings:
- <warning and explicit rationale>
next step:
- <exact remediation command>
```

`READY` requires no `FAIL`, non-empty diff, valid reasons for every `N/A`, required post-code review `APPROVED`, and no unresolved warnings for team PR validation.

## Hướng dẫn sử dụng
- **Khi dùng:** Chạy validation gate trước commit hoặc remote delivery, không thay đổi worktree.
- **Không dùng:** Không dùng để auto-fix, commit, push, merge, reset, stash hoặc claim unrun checks as `PASS`.
- **Input:** Bắt buộc `--scope=commit|pr`; tùy chọn feature/base/head/strict/ownership; reject write/destructive inputs.
- **Điều kiện trước:** Repository guidance/profile accessible; diff source matches scope (staged for commit, remote/local comparison for PR).
- **Evidence:** `GIT VALIDATION` report with each PASS/FAIL/N/A reason, exact commands/results, post-code review and blockers.
- **Dừng khi:** Empty diff, governance/profile conflict, secret, missing review, failed lint/audit/trace/sync/test or unresolved team warning.
- **Human quyết định:** Human resolves blockers and authorizes delivery route; validator never changes files or grants approval.
- **Lệnh tiếp theo:** `git commit` only after commit `READY`; otherwise run the exact remediation named in `next step`.
- **Ví dụ:** `/git-validate --scope=commit --feature=feat-orders` before a local commit.

## Completion output

Use the [Completion output contract](../_shared/ai-review-protocol.md), preserving the existing `GIT VALIDATION` report. Summarize scope/diff source, every `PASS`/`FAIL`/`N/A`, post-code review, exact command results, warnings and blockers. `READY` may only `continue` to the existing Human-confirmed delivery route; `BLOCKED` names the observed remediation from the report and does not auto-fix. Do not commit, push, merge, reset, checkout, stash, amend or discard changes.
