---
name: poteto-help
description: Explain pstack for Codex and route the user to a skill, playbook or principle.
  Use for pstack help and usage questions.
---

# Poteto help

Read [Codex runtime contract](../../CODEX-RUNTIME.md) and the relevant sibling skill before answering.

Use [poteto-mode](../poteto-mode/SKILL.md) as the primary entry point. The user can select the skill from the host's skill picker or refer to it as $poteto-mode, depending on the host. Do not promise a particular slash menu, keyboard shortcut, automatic persistent mode or installation on another device. Start each new task by invoking the skill explicitly.

Give one example with a goal and a checkable done condition:

```text
Use pstack-for-codex:poteto-mode to reproduce this bug, fix its root cause, and verify the user-visible behavior.
```

No setup is required for inherited-model defaults. [setup-pstack](../setup-pstack/SKILL.md) writes project preferences loaded explicitly by poteto-mode. The host, not this plugin, controls available models and tools.

Use [ketchup](../ketchup/SKILL.md) to catch up on this chat since the user’s last message, with enough context to decide each action item. Recall covers recent work across chats when the host exposes that history.

Route explanations to how, motivation/history to why, design to architect, competing attempts to arena, coverage slices to swarm, adversarial review to interrogate, bug-test-first work to tdd, comments to no-comments, prose to unslop, and runtime harness creation to create-verification-skill. Read their frontmatter when a finer distinction matters. Principles are the principle-* sibling skills. Playbooks live in [poteto-mode/playbooks](../poteto-mode/playbooks/); they are not separate commands.

Native agents are conditional on the host's capabilities and rules. Without them, phases run sequentially. Inherited-model review is not model diversity. No cloud runner, scheduler, connector, webhook or browser is installed by this plugin. External tools remain independently configured. Source attribution and conversion limitations are in [the compatibility report](../../COMPATIBILITY.md).
