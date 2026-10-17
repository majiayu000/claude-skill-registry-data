---
name: agent-self-maintenance
description: Set up automated periodic agent self-maintenance — Python scripts for Skills/MEMORY.md health management, cron job chaining with context_from, and backup/dedup/archive pipelines
triggers:
  - "设置定时维护任务"
  - "自动清理 skills / auto cleanup skills"
  - "维护 MEMORY.md / maintain memory file"
  - "定时任务链 / cron job chain"
  - "agent 自检 / agent maintenance routine"
  - "skills 归档 / archive old skills"
  - "记忆文件备份 / memory backup"
  - "creation_nudge_interval"
  - "每日自检 / daily self-check"
  - "工作区 git 仓库 / workspace git repo"
  - "agent 工作区版本管理 / version control workspace"
tags:
  - devops
  - maintenance
  - cron
  - skills
  - memory
  - best-practice
---

# Agent Self-Maintenance Setup Guide

> **Reference files**: `references/interactive-skill-audit.md` — manual/interactive skill audit methodology (complementary to the automated cron approach below).

## Overview

Set up a cron job chain for ongoing agent health:
1. **Skills maintenance** — detect duplicates, archive old skills (>60 days untouched), scan for description overlap
2. **MEMORY.md maintenance** — backup with date stamp, deduplicate entries, monitor char limit, flag overuse
3. **Cron job chaining** — use `context_from` to pipe maintenance output into the daily health check

## Architecture

```
07:30 ── skills-memory-maintenance ──→ Python script (diagnostic + cleanup)
                    │                      (backup, dedup, archive candidates)
                    ↓ context_from
08:00 ── daily-self-check ──→ inherits maintenance report + runs workspace/system checks
```

## Step 1: Create the Python Maintenance Script

Place at `~/.hermes/scripts/skills-memory-maintenance.py` (relative path for cron `script` parameter).

### Key components:

```python
# 1. MEMORY.md health
#    - Check size (warning > 6KB) and char count (limit ~2200)
#    - Backup to ~/.hermes/memories/backups/MEMORY.md.YYYYMMDD
#    - Deduplicate entries by removing exact duplicate lines
#    - Recommend candidates for trimming when usage > 90%

# 2. Skills health (recursive scan)
#    - Count all user skills (exclude hermes/, mcp/, _archive/)
#    - Flag candidates: skills unmodified > 60 days → archive to _archive/
#    - Detect overlapping descriptions (keyword intersection ratio ≥ 50%)
#    - Report total, warnings, recommendations

# 3. Temp file cleanup
#    - Remove *.tmp, *.pyc, __pycache__, .pytest_cache, .mypy_cache, .ruff_cache

# 4. Output JSON + readable stderr summary
```

### Critical paths to scan:

```python
HERMES_HOME = Path.home() / ".hermes"
SKILLS_DIR = HERMES_HOME / "skills"
MEMORIES_DIR = HERMES_HOME / "memories"
BACKUP_DIR = MEMORIES_DIR / "backups"
ARCHIVE_DIR = SKILLS_DIR / "_archive"

# Skills are nested: ~/.hermes/skills/<category>/<skill-name>/SKILL.md
# Use os.walk() to recurse, exclude hermes/, mcp/, _archive/
```

### Key thresholds:
- **Skills warn limit**: 50 (above → flag in report)
- **Skills archive**: 60 days unmodified → archive candidate
- **MEMORY.md warn**: 6KB file size
- **MEMORY.md char limit**: 2200 (99% → urgent)
- **Description overlap**: ≥ 50% keyword intersection → potential duplicate

## Step 2: Create the Cron Chain

### Job 1: Maintenance script (runs first)

```bash
cronjob action=create \
  name="skills-memory-maintenance" \
  schedule="30 7 * * *" \
  script="skills-memory-maintenance.py" \
  deliver="local"
```

The `script` parameter points to `~/.hermes/scripts/<filename>`. Its stdout is injected into the prompt as context.

### Job 2: Daily self-check (runs second, inherits maintenance output)

```bash
cronjob action=update \
  job_id="<daily_check_id>" \
  context_from=["<maintenance_job_id>"]
```

This chains the jobs: maintenance output is available when daily check runs.

### Job 2 prompt should include:
1. Parse the maintenance JSON report (passed as context)
2. Memory health check (workspace, git, system)
3. Workspace cleanup (tmp files, empty dirs)
4. Optional MEMORY.md trimming (if usage > 90%)
5. Optional Skills archiving (mv old ones to _archive/)
6. Structured markdown report

## Step 3: Test the Script

```bash
cd ~/.hermes && uv run python scripts/skills-memory-maintenance.py
```

Verify: JSON output, files backed up, duplicates removed.

## Safety Rules

- **Never auto-delete skills** — only move to `_archive/` (reversible)
- **MEMORY.md dedup** only removes exact duplicate lines — never semantic compression without user approval
- **Backup before any write** — MEMORY.md backup goes to `backups/` directory
- **Log actions taken** in the report output

## Step 4: Initialize Git Repository for Agent Workspace

The agent's working directory (`~/.hermes/`) should be under version control to track changes to config, skills, scripts, cron, and memories.

### .gitignore template for agent workspace

Create at `~/.hermes/.gitignore`:

```gitignore
# === 运行时数据库 ===
*.db
*.db-shm
*.db-wal
response_store.db*

# === 会话 & 日志 ===
sessions/
logs/
.hermes_history

# === 缓存 ===
cache/
audio_cache/
image_cache/
checkpoints/
sandboxes/
pastes/

# === 认证 & 敏感信息 ===
auth.json
auth.lock
.env

# === 运行时状态 ===
*.pid
*.lock
gateway_state.json
gateway.pid
processes.json
channel_directory.json
feishu_seen_message_ids.json
models_dev_cache.json
.skills_prompt_snapshot.json
.update_check

# === 临时 ===
pairing/
__pycache__/
*.pyc
.DS_Store

# === 运行时产物（不跟踪）===
cron/output/

# === 历史迁移归档 ===
migration/

# === 子项目（非本仓库管辖）===
hermes-agent/
references/
```

### Initialize and commit

```bash
cd ~/.hermes
git init
git add -A
# Verify gitignore is working — should NOT show: *.db, sessions/, logs/, cache/, auth files, etc.
git status --short
git commit -m "init: workspace baseline"
```

### Set git identity

```bash
git config --global user.name "<github-username>"
git config --global user.email "<github-email>"
```

### (Optional) Create remote private repo and push

```bash
# Create private repo on GitHub
gh repo create hermes-workspace --private \
  --description "Hermes Agent workspace: config, skills, scripts, cron, memories" \
  --push --remote origin --source .

# If the command times out on push, do it manually:
git push -u origin master
```

### Add git maintenance to the daily self-check prompt

In the daily-self-check cron job's prompt, add a section that replaces any old workspace paths:

```markdown
## 📦 3. Git 仓库维护（~/.hermes/）
- 进入 ~/.hermes/，检查 git 仓库状态：
  - 执行 `git status --short` 查看是否有未跟踪或已修改的文件
  - 如果已 tracked 的文件有改动，检查改动内容（`git diff --stat`），确认是合理的工作变更
  - 对合理变更执行 `git add -A && git commit -m "daily: auto-maintenance $(date +%Y-%m-%d)"`
  - 如果存在大量未跟踪文件，检查 .gitignore 是否需要更新
  - **不要 push**，只做本地提交（除非用户明确要求自动 push）
  - 报告 git 仓库状态：分支名、未提交数量、最近一次 commit 时间
```

### Git repo health reporting

Include in every daily health report:
- Branch name
- Uncommitted file count (modified + untracked)
- Days since last commit (warning if > 7 days without change)
- Whether auto-commit was triggered

### Full daily-self-check cron job template

Use this as the prompt when creating the cron job:

```markdown
执行每日自检任务。请在 10 分钟内完成以下所有检查项，最终输出一份结构化的摘要报告。

---

## 🧠 1. 记忆体检
- 确认 ~/.hermes/memories/ 目录下文件完整性（MEMORY.md, USER.md 是否存在）
- 检查记忆文件大小和行数，判断是否接近上限
- 如果发现异常（文件丢失、损坏、过大）则报告

## 🧹 2. 工作区清理
- 检查 ~/.hermes/ 目录：
  - 查找并删除临时文件（*.tmp, __pycache__/, *.pyc, .pytest_cache/ 等）
  - 检查是否有不必要的空目录
  - 报告工作区文件数量和总大小
  - 注意不要触碰 .git/ 和 tracked 文件

## 📦 3. Git 仓库维护（~/.hermes/）
- 进入 ~/.hermes/，检查 git 仓库状态：
  - 执行 `git status --short` 查看是否有未跟踪或已修改的文件
  - 如果已 tracked 的文件有改动，检查改动内容（`git diff --stat`），确认是合理的工作变更
  - 对合理变更执行 `git add -A && git commit -m "daily: auto-maintenance $(date +%Y-%m-%d)"`
  - 如果存在大量未跟踪文件，检查 .gitignore 是否需要更新
  - **不要 push**，只做本地提交
  - 报告 git 仓库状态：分支名、未提交数量、最近一次 commit 时间

## 💾 4. 系统健康
- 检查磁盘空间：`df -h /` 和 `df -h /mnt/c/`
- 检查内存使用：`free -h`
- 检查 ~/.hermes/logs/ 日志文件大小，如果单个日志超过 100MB 则报告

## 📋 5. 输出摘要报告
输出 markdown 格式摘要，包含：
- ✅ 记忆体检结果
- ✅ 工作区清理小结（删除了什么、当前文件/目录数）
- ✅ Git 状态（分支、未提交数、最近 commit、是否自动提交）
- ✅ 系统健康指标（磁盘、内存、日志）
- ⚠️ 任何异常或需要注意的地方，清晰的 action items
```

### Cron job creation commands

```bash
# === Job 1: Skills & Memory maintenance ===
cronjob action=create \
  name="skills-memory-maintenance" \
  schedule="30 7 * * *" \
  script="skills-memory-maintenance.py" \
  deliver="local"

# === Job 2: Daily self-check (chain from job 1) ===
cronjob action=create \
  name="daily-self-check" \
  schedule="0 8 * * *" \
  context_from=["<maintenance_job_id>"] \
  prompt="<the full template above>" \
  enabled_toolsets='["terminal","file","search","session_search"]' \
  deliver="local"
```

Note: Replace `<maintenance_job_id>` with the actual ID from `cronjob action=list` after creating Job 1.

## Pitfalls

- The old `/home/po/.Hermes/workspace/` path used in earlier daily-check versions is dead — always use `~/.hermes/` instead.
- `cron/output/` changes every run and should be in .gitignore (transient).
- `migration/` contains legacy node_modules — exclude from git.
- Skills with bundled node_modules/schemas (e.g., openclaw-imports) add bloat — only track SKILL.md files and scripts, not generated assets.
- Do NOT `git push` from cron jobs — local commits only, unless user explicitly requests remote backup.
- `gh repo create --push` may time out on large repos — the repo is still created, just push separately with `git push -u origin master`.
- First `git init` commit may include 4000+ files (migration archive, cron output history). Tune `.gitignore` first, then `git add -A && git commit`.

## Interactive Skill Audit (Manual Cleanup)

When the user asks to "list all skills" or "clean up unused skills", use the interactive audit methodology documented in `references/interactive-skill-audit.md`. Key steps:

1. **List**: Use `find ~/.hermes/skills -name "SKILL.md"` — NOT `skills_list` which truncates output for large skill sets.
2. **Analyze staleness**: `find ... -printf "%T+ %p\n" | sort` — modification time is the best proxy for usage when logs don't surface skill names.
3. **Categorize**: Domain relevance trumps age. A 3-month-old devops skill is more valuable than a 1-week-old bioinformatics skill for this user.
4. **Log search caveat**: `grep` on `agent.log` needs `-a` flag (binary detection false-positive). Even then, skill names are embedded in JSON tool-call payloads and hard to extract — file mtime is more reliable.

## Safety Rules

- **Never push to remote from cron** — auto-commits are local only, user pushes manually when ready
- **Do not commit large binary blobs** — if .gitignore is missing an exclusion, update it rather than committing
- **Backup before any write** — MEMORY.md backup goes to `backups/` directory
- **Never auto-delete skills** — only move to `_archive/` (reversible)
- **Log all actions taken** in the report output
