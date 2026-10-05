---
slug: openclow-skill-manager
version: 1.0.2
displayName: 技能管理器（Openclow Skill Manager）
summary: 管理 OpenClaw 技能：以表格形式列出所有技能、显示功能介绍、找出功能重复的技能。当用户想知道安装了哪些技能、某个技能的功能或想找出重复功能的技能时使用。
tags: clawhub
---

# Skill Manager

OpenClaw Skills 管理工具 - 列表形式展示

## 功能

### 1. 列出所有 Skills（表格形式）

| Skill | 功能 |
|-------|------|
| characteristic-voice | 让语音更自然、更有感情 |
| chat-with-anyone | 和任何人对话，用他们的声音回复 |
| clawsucker | Clawsucker 团队 AI 助手 |
| daily-news-caster | 新闻播客生成 |
| github | GitHub CLI 管理 |
| memory-system | 🧠 长期记忆系统 |
| n8n-workflow-automation | n8n 工作流设计 |
| pg | PostgreSQL 查询优化 |
| pgvector | 向量数据库 |
| proactive-agent | 🦞 主动型 AI |
| skill-finder | 智能搜索 skill |
| surrealdb | 文档/图数据库 |
| tavily-search | AI 优化搜索 |
| tts | 文字转语音 |
| video-stt | 视频转文字 |
| video-translation | 视频翻译配音 |

### 2. 功能分类

| 分类 | Skills |
|------|--------|
| 🎙️ 语音/视频 | tts, characteristic-voice, chat-with-anyone, video-stt, video-translation, daily-news-caster |
| 🧠 记忆 | memory-system, proactive-agent |
| 💾 数据库 | pg, pgvector, surrealdb |
| 🔧 工具 | github, skill-finder, tavily-search, truth-search |
| ⚙️ 自动化 | n8n-workflow-automation |

### 3. 功能重复的 Skills

| 功能 | 重复 Skills |
|------|-------------|
| 搜索/查找 | skill-finder, tavily-search, truth-search |
| 文字转语音 | tts, characteristic-voice (characteristic-voice 依赖 tts) |
| 记忆系统 | memory-system, proactive-agent |
| 数据库 | pg, pgvector, surrealdb |

## 使用命令

```bash
# 列出所有 skills
python scripts/list_skills.py

# 分类显示
python scripts/list_skills.py --category
```

## 常用 Skills 推荐

- **语音相关**: tts, characteristic-voice
- **视频处理**: video-stt, video-translation
- **记忆系统**: memory-system, proactive-agent
- **数据库**: pg, pgvector

---
更新于: 2026-03-08
