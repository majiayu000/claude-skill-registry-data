---
name: meta-rigor
description: >-
  Light operator pack for adjustable rigor: when to engage, rigor tiers,
  config-from-any-harness, gates map, little-ask playbook. Load references
  on demand — do not bloat SessionStart. Use with emperor rigor-judge /
  emperor config / ask-spec emit auto-detect.
license: MIT
metadata:
  version: 0.4.170
  part-of: emperor-time
---

# Meta rigor (operator)

Not archaeology. Paths only — open what you need:

1. `references/meta/when-to-engage.md`
2. `references/meta/rigor-tiers.md`
3. `references/meta/config-from-any-harness.md`
4. `references/meta/gates-map.md`
5. `references/meta/little-ask-playbook.md`

## Commands

```
scripts/emperor rigor-judge --ask "<ask>"
scripts/emperor rigor-judge --ask "<ask>" --effort-class full   # override wins
scripts/emperor config show|get|set|edit
scripts/emperor ask-spec --emit "<ask>" --write .emperor/tasks/<id>/ask-spec.md
```

User override always wins. No LLM loop on tiny. Optional judgment provider: not in this leaf.
