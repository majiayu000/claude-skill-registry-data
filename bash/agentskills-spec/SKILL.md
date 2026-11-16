---
name: agentskills--spec
description: "Specification và docs cho Agent Skills format — chuẩn open format để extend AI agent capabilities. Dùng khi viết SKILL.md mới hoặc cần hiểu spec."
allowed-tools: Read
user-invocable: true
---

Agent Skills là lightweight open format do Anthropic phát triển, được adopt bởi 70+ agent tools.

## Spec cơ bản

```
my-skill/
├── SKILL.md    # Required: frontmatter metadata + instructions
├── scripts/    # Optional: executable code
├── references/ # Optional: docs
└── assets/     # Optional: templates
```

## SKILL.md frontmatter tối thiểu

```yaml
---
name: my-skill
description: "One-line description — used for activation matching"
---
```

## Progressive disclosure

1. **Discovery** — agent load name + description only
2. **Activation** — khi task match, load full SKILL.md
3. **Execution** — follow instructions, chạy scripts nếu có

## Install any skill

```bash
npx skills add <owner>/<repo>
```

## Source

https://github.com/agentskills/agentskills · ⭐19.8K
https://agentskills.io
