---
name: static-analysis-checklist
description: Place, author, and validate static-analysis invariants.
---

# Static analysis checklist

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/static-analysis-checklist/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use when changing a static-analysis invariant. Read local `AGENTS.md`, analyzer
documentation, rule inventory, and fixture conventions before selecting an implementation.

1. State the invariant and search for an existing analyzer, rule, or guard that owns it. Prefer the
   narrowest established owner over a parallel scanner.
2. For workflow or action policy, parse YAML instead of text matching. Inspect only intended
   tracked configuration files. A persistent-workspace guard enforces
   [github-actions-checklist](../github-actions-checklist/SKILL.md): reject sparse-checkout inputs
   and unsafe writable workspace mounts, and allow unrelated YAML keys and ordinary read-only
   mounts.
3. Add meaningful accepted and rejected fixtures before the rule. Cover path routing, parser
   boundaries, equivalent YAML forms, and every allowed exception.
4. Keep discovery limited to tracked, intended files. Make suppressions and allowlists narrow,
   justified, and mechanically checked for freshness where practical.
5. Run the focused fixture test and analyzer, then the local aggregate checks. Keep diagnostics
   actionable and deterministic.
6. Update the local inventory or documentation and delete superseded migration artifacts only when
   the replacement invariant is demonstrably enforced.

This skill does not name analyzer roots, fixture locations, commands, suppression syntax, or
rollout policy. A consumer wrapper or local instruction file provides them.
