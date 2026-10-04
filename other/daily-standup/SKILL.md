---
name: daily-standup
description: >
  Alias for /daily-standup-with-cache. Start a daily session: fetch remote branches,
  report latest remote branch worked on, then cache + TODO + briefing.
argument-hint: "Optional focus, e.g. 'tests', 'deploy', 'chains', 'template-deploy'"
user-invocable: true
disable-model-invocation: false
---

# Daily Standup (alias)

Same workflow as `/daily-standup-with-cache`. Follow [`.grok/skills/daily-standup-with-cache/SKILL.md`](../daily-standup-with-cache/SKILL.md) exactly.

**Mandatory first actions** (before cache): `git fetch origin --prune`, then identify **latest remote branch worked on** (`remote-last`: newest `origin/*` by committer date) per daily-standup-with-cache Step 2. Report current vs remote-last vs local-last vs TODO branch.

Keep all standup responses concise.