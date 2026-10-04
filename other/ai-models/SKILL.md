---
name: ai-models
description: List and inspect Frontline AI models from the CLI, and choose valid model IDs for agent settings.
allowed-tools: Bash(frontline:*)
---

# AI Models

List available text models:

```bash
frontline ai-models list --type TEXT --table
```

List transcription models:

```bash
frontline ai-models list --type TRANSCRIPTION
```

List file-analysis models (used by the automation `FILE_ANALYSIS` / OCR node):

```bash
frontline ai-models list --type FILE_ANALYSIS
```

Get the default model:

```bash
frontline ai-models default --type TEXT
```

Inspect a model:

```bash
frontline ai-models describe <aiModelId>
```

Use only `TEXT` model IDs as `aiModelId` in agent settings:

```bash
frontline agents agent-setting update --data '{"aiModelId":1,"instructions":"Answer concisely.","temperature":0.2}'
```

When sending IDs of other objects in CLI payloads, prefer commands that validate
references in the same execution. `frontline agents agent-setting update`
preflights `aiModelId` and `customToolIds` when the
Public API exposes those resources, then sends the update. The backend remains
the source of truth for every existence and ownership check.

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
