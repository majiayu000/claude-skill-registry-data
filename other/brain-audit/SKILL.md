---
name: brain-audit
description: "Workflow for Brain Audit"
metadata: {"clawdbot":{"emoji":"🧠","always":false}}
---

# brain-audit

This skill executes the **brain-audit** workflow from `.agent/workflows/brain-audit.md`.

## Usage

```
"Kör brain-audit"
"Run brain-audit"
```

Or via explicit mention:
```
/skill brain-audit
```

## Implementation

When this skill is invoked, the agent should read the workflow definition using the native `view_file` tool:

```
Tool call: view_file (Path: .agent/workflows/brain-audit.md)
```

After reading the context, the agent must strictly follow the operational protocol defined in the workflow (which begins by running `scripts/brain-scanner.ps1`).
