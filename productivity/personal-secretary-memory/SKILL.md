---
name: personal-secretary-memory
description: Maintain or recover a user's dated personal-assistant memory and prepare a cross-assistant handoff. Use only for explicit memory updates, continuity recovery, or handoff work; ordinary career, video, website, or life tasks alone do not trigger it. Includes job-search tracking as one topic area; read references/job-search.md when applications, deadlines, or interviews are the subject.
version: 1.1.0
---

# Personal Secretary Memory

Support a long-running personal-secretary project through one factual memory source. The active vault and area are defined by the local project AGENTS.md; this public Skill does not assume a home-machine path.

1. Read AGENTS.md and the memory index to locate the active vault. Read only the current status and task-relevant topic; do not load the whole vault.
   If the task is about an ongoing job or internship search, also read [references/job-search.md](references/job-search.md) and keep its three layers apart.
2. For changes or exports, preserve event date, recording date, source type, uncertainty, latest corrections, and authorization boundaries.
3. Update only affected canonical files. Historical packages and exported snapshots are evidence, not competing current-state stores.
4. Separate user statements, original material, summaries, assistant suggestions, and reproducible tool checks. Never invent missing dates, metrics, credentials, or outcomes.
5. For structural checks, run scripts/validate_memory.py (it needs PyYAML, install with pip install pyyaml first) with the actual vault and area. The check is read-only and does not prove historical truth or user acceptance.
6. Report changed files, actual outputs, checks, and unresolved coverage. Do not claim automatic ingestion, cross-device sync, complete chat recovery, or acceptance without evidence.

Private memory stays local. Do not publish credentials, webhook values, tokens, identity documents, private chat transcripts, or unrelated company material.

## Example

One entry, dated, with its source marked:

```markdown
## 2026-10-07（记录日期 2026-10-07）
- 收到诗悦 AE 岗笔试，已回信申请转评 AIGC 岗  [来源：本人陈述]
- 蓝标实习至 12 月中旬  [来源：offer 邮件]
- 米哈游一面时间未定  [来源：未确认，待核]
```

"未确认" is written as unconfirmed, never filled in with a plausible date.
