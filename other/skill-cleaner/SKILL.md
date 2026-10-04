---
name: skill-cleaner
description: Audit installed skills for duplicate ownership, stale triggers, prompt cost, and safe deletion.
disable-model-invocation: true
---

# Skill Cleaner

Use this only for an explicit skill library audit. The report is evidence, not an automatic deletion list.

Run the analyzer without transcripts first. `--root` is exclusive; repeat it to audit several roots:

```bash
node --experimental-strip-types ~/.agents/skills/skill-cleaner/scripts/skill-cleaner.ts \
  --root ~/.agents/skills \
  --root ~/.pi/agent/skills \
  --context-tokens 272000 \
  --budget-percent 2 \
  --no-logs
```

Use transcript scanning only when Charlie explicitly asks for usage evidence. Session logs can contain credentials, customer data, and private production material. Prune session paths before any content search and never copy raw transcript content into an audit report.

Review the output in this order:

1. Duplicate names and bodies.
2. Model visible description cost.
3. Stale or unreachable source roots.
4. Skills with overlapping ownership.
5. Usage evidence, when approved.

Before removing or merging a skill, read its body and references. Confirm the replacement exists, matches the current tools, and preserves unique project or operational knowledge. Rare use is not proof that a skill is useless.

Archive unversioned skill directories before mutation. Remove broken cross-runtime symlinks. Keep package owned skills with their package. Treat generated plugin caches as package state rather than hand-edited source.

Return one decision per skill, the resulting ownership map, changed paths, and any choice that belongs to Charlie. Do not commit or publish unless the request includes that authority.
