---
name: continuous-learning
description: "Learning system v1 — học từ session patterns, tạo reusable skills/commands từ repeated workflows. Phiên bản cũ hơn continuous-learning-v2."
origin: ECC
user-invocable: true
---

# Continuous Learning (v1)

> Phiên bản v1. Xem `continuous-learning-v2` để có instinct-based architecture với project scoping.

Học từ session Claude Code để tạo reusable skills và commands từ repeated workflows.

## Khi nào dùng

- Muốn extract patterns từ các session cũ
- Setup basic learning mà không cần full v2 infrastructure
- Import instincts từ người khác

## Khác biệt v1 vs v2

| | v1 | v2 |
|-|----|----|
| Observation | Stop hook (session end) | Pre/PostToolUse (100%) |
| Analysis | Main context | Background Haiku agent |
| Granularity | Full skills | Atomic instincts |
| Confidence | Không có | 0.3–0.9 scored |
| Project scope | Global only | Per-project isolated |

## Setup v1

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{ "type": "command", "command": "~/.claude/skills/continuous-learning/hooks/extract.sh" }]
    }]
  }
}
```

## Nâng cấp lên v2

```bash
# Migrate instincts từ v1 sang v2
bash skills/continuous-learning-v2/scripts/migrate-homunculus.sh
```

## Xem thêm

- `continuous-learning-v2` — phiên bản đầy đủ (khuyến nghị)
- `instinct-based-learning` — quick reference
- Source: https://github.com/affaan-m/ECC
