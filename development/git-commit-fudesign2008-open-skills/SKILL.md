---
name: git-commit
version: "3.0.0"
user-invocable: true
description: Git commit unified entry point. Triggers when user says 「提交代码」「git commit」「帮我提交」「写 commit message」「生成 commit」「提交一下」「git-commit」「自动提交代码」「git-commit-auto」 (commit code / help me commit / write commit message / generate commit / auto commit), or when invoked by jira-fix-workflow phase 7.
---

# Git Commit — Unified Entry (Auto Mode by Default)

## Mode Detection Rules

| Signal | Result |
|--------|--------|
| Caller passes `execute=true`, or triggered by `jira-fix-workflow` phase 7 | Auto mode |
| User says 「手动提交」「只生成命令」「不要执行」「给我命令」 (manual commit / only generate command / don't execute / give me the command) | Manual mode |
| Other triggers or unclear context | Default to auto mode |

## Execution Flow

### Step 1: Collect Commit Info

Fields for the commit message:
- **type**: fix, feat, refactor, perf, style, docs, test
- **scope** (optional): ai-summary, share, auth, api, ui, core
- **subject**: brief description in the user's preferred language, max 50 chars
- **jira_id** (optional): e.g. PROJ-123

(jira_id is optional; other context fields like branch, report_path are passed by the caller and not written into the commit)

### Step 2: Determine Execution Mode

Decide `execute=false` (manual) or `execute=true` (auto). See "Mode Detection Rules" above.

### Step 3: Multi-Project Detection

**Scan rules**:
- Scan scope: first and second-level subdirectories of the workspace root
- Identification: presence of a `.git` directory
- Exclude: `node_modules`, `.cursor`, `dist`, `build`, `.git`, hidden directories (starting with `.`)
- For each candidate directory, run `git status` to verify validity

**Multi-project scenario**: Report files are committed only in the primary project (the first one); each project with changes gets its own commit message.

### Step 4: Generate Commit Message

**Format**:
```
<type>(<scope>): <Jira-ID> <subject>
```

Rules:
- Subject: max 50 chars, in the user's preferred language, must include a verb matching the type (e.g. feat: 新增/Add, fix: 修复/Fix, refactor: 重构/Refactor, perf: 优化/Optimize, style: 格式化/Format, docs: 文档/Docs, test: 测试/Test)
- Jira ID goes before the subject when present
- Omit parentheses when no scope: `<type>: <subject>`
- Commit message contains only the title line, no body

### Step 5: Execute Git Operations

**Manual mode** (`execute=false`): Generate commands, don't execute, prompt user to run manually.

**Auto mode** (`execute=true`): Execute the following commands in order, outputting each command's result or status:

1. **git status** — output current changes summary
2. **Protected branch check** — committing directly to main/master/develop bypasses code review; unreviewed production code lands on main. Warn the user if detected
3. **git add .** — output staged file status
4. **git commit -m "..."** — output commit hash and message
5. **git log -1 --stat** — output commit stats (changed files and line counts)
6. **git push -u origin [branch-name]** — output push result or branch tracking info

For multi-project, execute these steps independently for each project, with a summary table at the end.

## Output Format

**Auto mode** (default):
```
## Git Commit (Auto Mode)

**Project**: backend   **Branch**: fix/PROJ-123
**Commit**: a1b2c3d  **Push**: ✅ Success
**Changes**: +45/-12 (3 files)

**Next**: Create PR → Code Review → Test Verification
```

**Manual mode** (on explicit request):
```
## Git Commit (Manual Mode)

**Generated Commit Message**:
fix(ai-summary): PROJ-123 修复分享链接中AI摘要按钮显示问题

**Commands**:
git status
git add .
git commit -m "fix(ai-summary): PROJ-123 修复分享链接中AI摘要按钮显示问题"
git log -1 --stat
git push -u origin [branch-name]  # optional

**Note**: Please review and execute the above commands manually.
```

For multi-project, output independently for each project, with a summary table at the end.

## Error Handling

| Scenario | Handling |
|----------|----------|
| No uncommitted changes | Manual mode: inform user nothing to commit; Auto mode: output "No changes to commit" or run `git add .` then show "Staging area empty" |
| Branch doesn't exist | Error out, suggest creating a branch first |
| Git operation fails | Show error, provide fallback (suggest "manual commit" to retry) |
| Not in a Git repo | Error out and terminate, suggest checking the directory |
| Multi-project detection fails | Fallback to single-project mode using the current directory |

## Safety Mechanisms (Auto Mode)

- Warn when changes exceed 10 files / 500 lines; warn again at 20 files / 1000 lines (warnings don't block); failure in one project doesn't affect others
