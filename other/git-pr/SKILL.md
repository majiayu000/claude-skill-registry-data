---
name: git-pr
description: Kiểm định thay đổi remote-first; tạo Pull Request team hoặc hướng dẫn Human push solo
user-invocable: true
---

# Git Push / Pull Request Operator (`/git-pr`)

**Output language:** Mirror the invoking prompt. Status tokens, Git/GitHub output and identifiers remain language-invariant.

Prepares remote delivery. `Project Ownership: solo` does not create a PR: Agent validates local readiness and tells the Human owner how to push. `Project Ownership: team` creates a PR after Human confirmation and remote validation. Agent never pushes on behalf of a human. Agent Execution does not affect delivery behavior.

## Project ownership detection

Read `# Project Ownership: team|solo` and `# Agent Execution: direct|orchestrated` in `.sdd/shared_context.md`. `--project-ownership=solo|team` overrides delivery ownership only. Use canonical settings only when both headers exist exactly once and are valid. When both canonical headers are absent, use exactly one valid legacy source: exactly one `# Collaboration Mode: solo|team` header or exactly one `--team-size=solo|team`; duplicate, malformed or coexisting sources are `BLOCKED`. The valid source maps `solo` to solo/direct and `team` to team/orchestrated; emit a migration warning and do not silently rewrite governance. Missing, duplicate or malformed canonical headers are `BLOCKED`; never fallback legacy. When either canonical header exists, `--team-size` is `BLOCKED`; the alias is valid only when both canonical headers are absent. `--team-size` cannot be combined with `--project-ownership` or `--agent-execution`; the conflict is `BLOCKED`. A legacy header alongside canonical headers is ignored for resolution and recorded for migration cleanup.

## Parameters

- `--base=<branch>`: Target branch; default is `origin` default branch.
- `--head=<branch>`: Source branch; default current branch.
- `--feature=<feature-slug>`: Optional validator input.
- `--draft`: Create draft PR (team ownership only).
- `--issue=<id>`: Optional issue linked in PR body (team ownership only).
- `--project-ownership=solo|team`: Optional delivery-policy override.
- `--team-size=solo|team`: Deprecated composite alias for one transition release.

## Solo ownership flow

1. Check `git status --short`, `git branch --show-current`, and `git remote -v`.
2. Block detached HEAD, dirty worktree, unfinished Git operation or protected delivery branch.
3. Do not fetch/push for the Human. Validate local source with `/git-validate --scope=pr --project-ownership=solo` against `origin/<base>...HEAD`.
4. After `READY`, provide but do not execute:

   ```bash
   git push -u origin <head>
   ```

5. After the Human push, a repeat invocation may verify `HEAD == origin/<head>` and remote diff.

## Team ownership flow

1. Check repository status, remote and `gh auth status`.
2. Fetch remote, resolve base/head, and require local commit already pushed by a Human.
3. Block protected head, detached/dirty/unfinished state, missing/empty remote diff, existing PR, conflict, failing required check or `CHANGES_REQUESTED`.
4. Run `/git-validate --scope=pr --base=<base> --head=<head> --feature=<feature-slug> --strict --project-ownership=team`.
5. Build conventional imperative title/body with summary, validation evidence, test plan and related issue.
6. Ask the user to confirm the outward-facing PR content. Only after confirmation and `READY`, run `gh pr create`; never merge, close, force-push or bypass checks.

## Failure handling

- Rejected push: Human resolves under repository policy, then revalidates.
- Validation blocker: report remediation; do not push or create PR.
- `gh` auth/API failure: report once; do not retry indefinitely.
- Conflict: stop; do not auto-resolve or force-push.

## Output

```text
✓ project ownership: solo | team
✓ validation: READY | BLOCKED
✓ delivery: Human must run git push -u origin <head> | pull request: <url>
✓ remote verification: pending Human push | HEAD == origin/<head>
```

## Hướng dẫn sử dụng
- **Khi dùng:** Chuẩn bị remote delivery: solo chỉ kiểm tra sẵn sàng, team tạo PR sau Human confirmation.
- **Không dùng:** Không dùng để push, merge, force-push, close PR, resolve conflict hoặc bypass checks.
- **Input:** `--base`, `--head`, tùy chọn feature/draft/issue/ownership; reject ambiguous remote target and unpushed team head.
- **Điều kiện trước:** Ownership resolve, branch/worktree/remote hợp lệ, local commit đã có; team cần Human-confirmed title/body và `git-validate --scope=pr --strict` `READY`.
- **Evidence:** Branch/remote state, validation report, `HEAD` comparison or pending Human push, PR URL when created.
- **Dừng khi:** Detached/dirty/protected state, missing remote diff, auth/API failure, conflict, failed check hoặc missing Human confirmation.
- **Human quyết định:** Human owns push; team Human confirms outward-facing PR content before `gh pr create`.
- **Lệnh tiếp theo:** Solo `git push -u origin <head>`; team chỉ `gh pr create` after persisted confirmation and `READY`.
- **Ví dụ:** `/git-pr --base=main --head=feat/orders --feature=feat-orders --draft` trong team flow sau Human push.

## Completion output

Use the [Completion output contract](../_shared/ai-review-protocol.md). Summarize ownership, branch/remote state, validation evidence, PR/remote verification state and unresolved delivery condition. Solo `READY` may only `continue` with the displayed Human `git push -u origin <head>` command. Team PR creation is `Human decision required` until outward-facing title/body is confirmed; auth/API/conflict/protected branch/required-check failure is `BLOCKED`. Never auto-push, force-push, merge, close or resolve conflicts.
