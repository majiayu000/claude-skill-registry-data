---
name: qa-argus-ready
section: pipeline
description: "Argus QA readiness wizard; safe alias for qa-ready that avoids old qa-agent command collisions"
---

# qa-argus-ready

Run this command after installing the plugin from a zip:

```text
/qa-argus-ready
```

This is the collision-safe readiness entry point for this plugin. It exists because some machines may already have an older plugin that owns `/qa-ready` or `/qa-setup`.

## Behavior

Execute the readiness flow from:

```text
skills/qa-ready/SKILL.md
```

Follow that file exactly, with these command-name substitutions in user-facing output:

- Say `/qa-argus-ready` for readiness checks and repairs.
- Say `/qa-argus-setup` for the full setup wizard.
- Say `/qa-argus` when telling the user how to start the audit.
- Do not mention `/qa-agent`.

## Supported Forms

```text
/qa-argus-ready
/qa-argus-ready --check
/qa-argus-ready --repair
/qa-argus-ready --secrets
```
