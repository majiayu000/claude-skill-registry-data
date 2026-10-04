---
name: pulumi
description: Preview and manage Pulumi infrastructure as code stacks
activation_keywords: [pulumi, iac, infrastructure, stack, preview, resource]
execution_mode: client
---

# Pulumi Skill

Provides read-only Pulumi operations via local CLI:
- List stacks and check their status
- Preview changes (diff)
- List stack resources
- Get stack outputs and config
- Check stack history

Use `builtin_pulumi` tool with fields:
- `operation`: one of "list_stacks", "preview", "resources", "outputs", "config", "history"
- `stack`: stack name (default: current active stack)
- `path`: path to Pulumi project directory (default: current directory)
- `extra_args`: additional Pulumi CLI arguments

Note: Requires Pulumi CLI (pulumi) installed.
All operations are read-only.
