---
name: dynamic-skill-manager
description: |
  Track and manage OpenClaw skills usage, find idle skills, and safely uninstall unused ones.
  
  Use when:
  - User wants to see what skills are installed or track usage
  - User wants to find skills that haven't been used recently
  - User wants to uninstall or cleanup unused skills
  - User mentions "skill management", "dynamic skill", "skill lifecycle"
  - Agent needs to check skill usage statistics
version: 0.2.0
metadata:
  clawdbot:
    emoji: "🧩"
    requires:
      bins:
        - python3
    homepage: https://github.com/openclaw/openclaw
---

# Dynamic Skill Manager

Track skill usage, find idle skills, and safely manage skill lifecycle.

## ⚠️ Security Notice

**v0.2.0** includes critical security fixes:
- Path traversal vulnerability fixed in `uninstall_skill()`
- Input validation for all skill names
- Symlink attack prevention
- System skill protection

## Core Concepts

| 概念 | 说明 |
|------|------|
| **Dynamic Skill** | 按需安装的 skill，可清理 |
| **Pinned Skill** | 系统 skill，受保护不可删除 |
| **Registry** | skill 元数据存储 |

**自动保护的系统 Skills**：`self-improving-agent`, `pahf`, `error-log-selfcheck`, `dynamic-skill-manager`

## Quick Start

```bash
# 同步已安装 skills 到注册表
python3 ~/.openclaw/workspace/skills/dynamic-skill-manager/scripts/skill_manager.py sync

# 列出所有 skills（📌 = pinned）
python3 ~/.openclaw/workspace/skills/dynamic-skill-manager/scripts/skill_manager.py list

# 查看系统 skills
python3 ~/.openclaw/workspace/skills/dynamic-skill-manager/scripts/skill_manager.py pinned

# 查找闲置 skills（N 天未使用）
python3 ~/.openclaw/workspace/skills/dynamic-skill-manager/scripts/skill_manager.py idle 30

# 安全卸载 skill（有输入验证）
python3 ~/.openclaw/workspace/skills/dynamic-skill-manager/scripts/skill_manager.py uninstall <skill-name>

# 记录 skill 使用
python3 ~/.openclaw/workspace/skills/dynamic-skill-manager/scripts/skill_manager.py track <skill> "<context>"
```

## Data Location

```
~/.openclaw/workspace/.skill-manager/
├── registry.json      # Skill 元数据
├── usage-log.jsonl    # 使用历史
└── archive/           # 已卸载 skill 的元数据
```

## Registry Schema

```json
{
  "skills": {
    "skill-name": {
      "installed_at": "2026-03-07T03:00:00Z",
      "source": "clawhub",
      "usage_count": 5,
      "last_used": "2026-03-07T03:00:00Z",
      "context_keywords": ["keyword1"],
      "pinned": false
    }
  }
}
```

## Integration Points

- **After skill use**: `track_usage(skill_name, context_summary)`
- **On user request**: `list_skills()`, `find_idle_skills(days)`

## Security Features

The `uninstall_skill()` function includes multiple safety checks:

1. **Input Validation**: Skill names must be alphanumeric with dashes/underscores only
2. **Path Traversal Prevention**: Resolves paths and verifies containment within skills directory
3. **Symlink Detection**: Rejects symlinks to prevent attacks
4. **System Skill Protection**: Prevents accidental deletion of critical skills

## Script Reference

See `scripts/skill_manager.py` for implementation.
