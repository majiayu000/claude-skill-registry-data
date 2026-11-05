---
name: writing-skills
description: use when touching skill
---

- avoid coupling between skills where it makes them harder to maintain. when needed, use `/skill-name`; for a `disable-model-invocation: true` skill, link directly to its `SKILL.md` and tell the caller to read and follow it. example:
```md
read and follow [/loop](../loop/SKILL.md) to deliver the PR
```
- `disable-model-invocation: true` must be accompanied by `agents/openai.yaml` with `policy: allow_implicit_invocation: false`
