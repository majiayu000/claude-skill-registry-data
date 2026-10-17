---
name: evolution
description: SuperClaw 三触发自进化引擎 — 全自动 FIX/DERIVED/CAPTURED 进化
---

# SuperClaw 自进化系统

## 架构

进化引擎 (`evolution-engine.py`) 作为后台 daemon 运行，自动监听 session 变化并触发进化。

```
session 结束 → 引擎检测 → LLM 分析执行历史 → 触发进化 → 写入 skills/
```

## 三种进化触发

| 触发 | 条件 | 结果 |
|------|------|------|
| **FIX** | skill 被使用但任务失败/出错 | 原地修复 SKILL.md，旧版本存入版本 DAG |
| **DERIVED** | skill 有效但 LLM 发现可优化模式 | 创建增强版 skill（新目录），父 skill 保持活跃 |
| **CAPTURED** | 任务成功但无匹配 skill | 从执行历史捕获全新 skill |

## 数据存储

- **进化数据库**: `/root/openclaw-fusion/data/evolution.db` (SQLite)
  - `skill_records` — 所有 skill 记录（含版本 DAG）
  - `skill_lineage` — 父子关系
  - `skill_metrics` — 使用次数、成功/失败计数
  - `execution_analyses` — 每次 session 的 LLM 分析结果
- **日志**: `/root/.openclaw/logs/evolution-engine.log`

## 版本 DAG

每次 FIX/DERIVED 进化创建新版本节点：
- FIX: 新 ID = `{name}__v{gen}_{hash}`，父节点标记 `is_active=0`
- DERIVED: 新 ID = `{name}__v{gen}_{hash}`，父节点保持 `is_active=1`
- CAPTURED: 新 ID = `{name}__cap_{hash}`，无父节点

## 健康检查

每 10 次 session 后自动扫描所有 skill 指标：
- 失败率 > 40% → 触发 FIX
- 成功率 < 60% → 触发 DERIVED
- 需要 LLM 二次确认才执行

## Agent 无需手动操作

进化引擎完全自动运行。Agent 只需：
1. 执行任务前查阅 `skills/` 目录（进化生成的新 skill 自动出现）
2. 正常执行任务

## 管理命令

```bash
# 查看服务状态
systemctl status evolution-engine

# 查看日志
tail -f /root/.openclaw/logs/evolution-engine.log

# 查看数据库
sqlite3 /root/openclaw-fusion/data/evolution.db "SELECT skill_id, name, origin, generation, is_active FROM skill_records ORDER BY created_at DESC LIMIT 20;"

# 查看进化历史
sqlite3 /root/openclaw-fusion/data/evolution.db "SELECT session_id, task_summary, suggestions FROM execution_analyses ORDER BY timestamp DESC LIMIT 10;"
```

## 旧模块（保留但非必需）

以下旧模块仍可手动调用，但进化引擎已覆盖其功能：
- `memory-manager.py` — 经验记忆（被 execution_analyses 表替代）
- `skill-generator.py` — 技能生成（被 CAPTURED 触发替代）
- `prompt-optimizer.py` — Prompt 优化（被 FIX 触发替代）
- `review-learner.py` — 审查学习（保留为辅助工具）
