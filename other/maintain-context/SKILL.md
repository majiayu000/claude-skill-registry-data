---
name: maintain-context
description: Create or revise shared context, task skills or system guidance.
---

1. Read [Responsibilities](../../context/contracts-and-instructions.md) and [Documentation standards](../../context/documentation-standards.md). Choose platform, module or system as the canonical owner. Inspect its README and relevant sources before editing.
2. Write standing knowledge in context and task procedures in skills/<name>/SKILL.md. Give each skill a precise description, necessary inputs, ordered decisions and observable completion criteria. Keep substantial conditional reference behind a trigger.
3. Update the owner's README and affected callers. Module skill routes belong in module.ts skills with a relative path and when trigger. Preserve unrelated module skills.
4. Run yarn studio sync and sync --check. Walk through intended triggers, disabled modules and unrelated systems. Verify links and declarations; report canonical sources changed and unresolved checks.
