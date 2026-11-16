---
name: instinct-based-learning
description: "Học hành vi từ session thực tế — tạo atomic instincts với confidence scoring, tự động activate khi gặp pattern tương tự. Bản đơn giản hơn continuous-learning-v2."
origin: ECC
user-invocable: true
---

# Instinct-Based Learning

Học từ các session thực tế để tạo ra behavioral patterns (instincts) nhỏ, có confidence score.

## Khi nào dùng

- Muốn Claude ghi nhớ pattern từ session hiện tại
- Muốn xem instincts đã học được
- Muốn export/import patterns giữa projects

## Instinct là gì

```yaml
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
scope: project
```

- **Atomic** — 1 trigger, 1 action
- **Confidence** — 0.3 (tentative) → 0.9 (near-certain)
- **Scoped** — project (isolated) hoặc global (shared)

## Commands

```
/instinct-status   # Xem tất cả instincts + confidence
/evolve            # Cluster instincts thành skills
/instinct-export   # Export ra file
/instinct-import   # Import từ file khác
/promote           # Nâng project instinct lên global
/projects          # List projects và instinct count
```

## Setup hooks

```json
{
  "hooks": {
    "PreToolUse":  [{ "matcher": "*", "hooks": [{ "type": "command", "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh" }] }],
    "PostToolUse": [{ "matcher": "*", "hooks": [{ "type": "command", "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh" }] }]
  }
}
```

Hooks fire 100% thời gian (khác với skills chỉ ~50-80%).

## Confidence scale

| Score | Ý nghĩa |
|-------|---------|
| 0.3 | Tentative — gợi ý |
| 0.5 | Moderate — áp dụng khi phù hợp |
| 0.7 | Strong — auto-apply |
| 0.9 | Near-certain — core behavior |

## Xem thêm

- `continuous-learning-v2` — bản đầy đủ với project scoping v2.1
- `continuous-learning` — phiên bản v1 đơn giản hơn
- Source: https://github.com/affaan-m/ECC
