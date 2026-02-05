---
name: skill-indexer
description: Build a combined index of available skills and support auto-registration by scanning repo and Codex skill directories; use when asked to list or catalog skills quickly.
---

# Skill Indexer

Use this skill to generate a combined skills index file and verify auto-registration.

## Workflow

1) Run the index script:

```bash
python skills/system/skill-indexer/scripts/index_skills.py
```

2) Review the output file at `skills/INDEX.json`.
3) If Codex skills are missing, verify `CODEX_HOME` or `~/.codex/skills` exists.

## Output expectations

- Provide the index file path and entry count.
