---
name: commit
description: Use when preparing or executing git commits in this repo and the commit message must follow the emoji conventional template, especially for auto-commit or "just commit" requests that might bypass it.
---

# Commit

## Overview
Use the embedded commit message template whenever a git commit is required in this repo.

## Template
```
<emoji> <type>: <summary>

- <bullet>
```
Title stays within 72 characters.

## Example (Template Shape)
```
✨ feat: 并发限流改为租约模式（ZSET+2m TTL）

- reqcount:v3 采用 ZSET 保存 lease_id/chat_id，score=joined_at，窗口(now-2m,+inf)过滤并发
- 租约 TTL 2 分钟自动回收，无续租；key 设双倍 TTL 防止遗留
- /internal/v1/concurrency 返回明细（chat_id、joined_at/expire_at 可读时间）
- 更新 NewConcurrencyLimiter 签名及示例，模型调用路径不变
```

## Emoji Map
- ✨ feat
- 🐛 fix
- 📚 docs
- 💎 style
- 📦 refactor
- 🚀 perf
- 🚨 test
- 🔧 chore

## Quick Reference
| Rule | Action |
| --- | --- |
| Commit needed | Use the template above |
| Compose message | Emoji + type + summary + bullet body |

## Rationalizations to Reject
| Excuse | Reality |
| --- | --- |
| "User said just commit" | Template is still required. |
| "Small change" | Template is still required. |
| "I already know the format" | Always follow the embedded template. |

## Red Flags - STOP and Fix
- Skipping the embedded template
- Writing a one-line message
- Missing required sections from the template

## Common Mistakes
- Using a custom format
- Omitting the bullet list body
- Missing emoji or type (per template)
