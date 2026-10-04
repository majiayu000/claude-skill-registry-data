---
name: "skill-sync"
description: "当用户想检查、同步、发布或排查 Codex 技能同步器时使用。"
---

# 技能同步器

使用本地 `skill-sync` CLI 或桌面应用管理多台电脑之间的 Codex 技能同步。

优先使用这些命令：

```bash
node ./bin/skill-sync.js status
node ./bin/skill-sync.js sync
node ./bin/skill-sync.js doctor
```

安全规则：

- 不要同步 token、登录态、缓存或整个 `~/.codex` 目录。
- 日常同步优先运行 `skill-sync sync`，让 Git 先保存本机版本再合并远程版本。
- 如果同步报告冲突，保留本机版本并检查冲突目录，不要直接使用 `--force` 覆盖。
- 安装到用户级 Codex 配置文件前，先征得用户确认。
