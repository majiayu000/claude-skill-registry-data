---
name: git-commit
description: Stage và commit thay đổi sau validation; Agent dừng trước remote delivery
user-invocable: true
---

# Git Commit Operator (`/git-commit`)

**Output language:** All output mirrors the language of the invoking prompt. Vietnamese prompt → Vietnamese output; English prompt → English output. Status tokens (`READY`, `BLOCKED`, `NO-OP`), Git output, and code identifiers are language-invariant.

Dùng để tạo commit an toàn. Không chạy `git commit` trước khi `/git-validate --scope=commit` trả `READY`. Cả solo và team mode, Agent chỉ commit khi Human yêu cầu; Agent không `git push`. Human thực hiện delivery remote theo `Project Ownership` sau commit/validation.

## Project ownership detection

Đọc `# Project Ownership: team|solo` và `# Agent Execution: direct|orchestrated` trong `.sdd/shared_context.md`. `--project-ownership=solo|team` override explicit cho invocation hiện tại. Chỉ dùng canonical khi mỗi header tồn tại đúng một lần và hợp lệ. Khi cả hai canonical header đều vắng mặt, chỉ dùng đúng một legacy source hợp lệ: đúng một `# Collaboration Mode: solo|team` hoặc đúng một `--team-size=solo|team`; source duplicate, malformed hoặc coexist là `BLOCKED`. Source hợp lệ map `solo` thành solo/direct và `team` thành team/orchestrated; báo migration warning, không tự rewrite governance. Thiếu, trùng hoặc malformed canonical header là `BLOCKED`, không fallback legacy. Khi có một trong hai canonical header, `--team-size` là `BLOCKED`; alias chỉ hợp lệ khi cả hai canonical header đều vắng mặt. `--team-size` cũng không được kết hợp `--project-ownership` hoặc `--agent-execution`; conflict là `BLOCKED`. Legacy header tồn tại cùng canonical headers không dùng để resolve và phải ghi migration cleanup.

Solo ownership bỏ PR overhead; Agent Execution không ảnh hưởng Git delivery, không nới outbound safety gate và không ủy quyền Agent push.

## Tham số

- `--message=<message>`: Commit message; thiếu thì đề xuất từ diff và yêu cầu user xác nhận.
- `--type=<feat|fix|perf|docs|test|refactor|chore|build|ci>`: Tùy chọn.
- `--scope=<scope>`: Tùy chọn.
- `--feature=<feature-slug>`: Tùy chọn, truyền tiếp cho validator.
- `--files=<path,...>`: Tùy chọn; chỉ stage path này. Không có thì hiển thị danh sách và yêu cầu xác nhận trước khi stage intended changes.
- `--project-ownership=solo|team`: Tùy chọn; override delivery ownership.
- `--team-size=solo|team`: Deprecated composite alias trong một transition release; báo migration warning.

## Quy trình

1. Đọc `AGENTS.md`, `CONSTITUTION.md`, `CLAUDE.md` và skill reference liên quan.
2. Kiểm tra worktree:

   ```bash
   git status --short
   git diff --stat
   git diff --name-only
   ```

3. Không stage forbidden file: `.env`, private key, credential, secret, `node_modules/`, `dist/`; không stage thay đổi ngoài scope user yêu cầu.
4. Stage path đã xác nhận:

   ```bash
   git add -- <path>...
   git diff --cached --stat
   git diff --cached --name-only
   ```

5. Tách thay đổi khác type/scope; tách code, test, docs, dependency/config khi không cùng intent. Hơn mười file không liên quan thì chia nhiều commit. File `.claude/` chỉ dùng prefix `feat`, `fix` hoặc `perf`.
6. Commit message theo `type(scope): description`, dưới 72 ký tự, imperative/present tense, không dấu chấm cuối và không AI attribution. Feature SDD thêm feature/spec version khi `add-execute` yêu cầu.
7. Chạy gate ngay trước commit:

   ```text
   /git-validate --scope=commit --feature=<feature-slug>
   ```

   Gate phải trả `GIT VALIDATION: READY`; `BLOCKED` thì dừng, không tự sửa, reset, amend hoặc bypass check.
8. Sau `READY` và user xác nhận commit message, chạy:

   ```bash
   git commit -m "type(scope): description"
   git rev-parse --short HEAD
   git log -1 --format=%s
   ```

9. Báo commit hash, branch và Human delivery command đề xuất; không chạy `git push`:

   ```bash
   git push -u origin <head>
   ```

## Safety gates

- Không có thay đổi: báo `NO-OP`, không commit.
- Có secret/forbidden file: block, chỉ hiện path/pattern đã mask.
- Validation/commit hook fail: block, báo lỗi nguyên văn và giữ nguyên worktree; không retry vô hạn.
- `main`, `master`, `production`, `prod`, `release/*`: không force-push hoặc bypass protection.
- Destructive operation như `reset`, `checkout`, `clean`, `amend` cần explicit confirmation.

## Output

```text
✓ staged: N files (+X/-Y lines)
✓ validation: READY
✓ commit: HASH type(scope): description
✓ delivery: Human must run git push after reviewing remote target
```

## Hướng dẫn sử dụng
- **Khi dùng:** Tạo local commit sau khi staged scope đã được Human xác nhận và validator trả `READY`.
- **Không dùng:** Không dùng để push, merge, reset, amend hoặc stage secret/ngoài scope; không tự chọn message khi cần xác nhận.
- **Input:** `--message` (hoặc yêu cầu xác nhận), tùy chọn type/scope/feature/files/ownership; reject credential paths and destructive flags without confirmation.
- **Điều kiện trước:** Governance hợp lệ, intended paths đã xác nhận, staged diff non-empty, `/git-validate --scope=commit` trả `READY` và user xác nhận message.
- **Evidence:** Staged diff, validator report, commit hash/subject/branch và displayed Human delivery command.
- **Dừng khi:** Secret/forbidden file, validation/hook fail, dirty or protected state, missing confirmation hoặc empty diff.
- **Human quyết định:** Human xác nhận scope/message và tự thực hiện remote delivery; Agent không push.
- **Lệnh tiếp theo:** Sau commit chỉ hiển thị `git push -u origin <head>` để Human chạy; validation fail thì dùng remediation trong report.
- **Ví dụ:** `/git-commit --files=.claude/skills/sdd-context/SKILL.md --message="docs(sdd): clarify context usage"` sau `READY`.

## Completion output

Use the [Completion output contract](../_shared/ai-review-protocol.md). Summarize staged scope, validation evidence, commit hash/branch when created and the Human-owned delivery route. No staged changes remains `NO-OP` with no further command; a missing user confirmation, secret/forbidden path, validation failure or hook failure is `BLOCKED`, reported without resetting, amending or retrying blindly. `continue` after commit is only the displayed Human `git push -u origin <head>` command; the Agent never runs it.
