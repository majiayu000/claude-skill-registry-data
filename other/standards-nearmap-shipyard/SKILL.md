---
name: standards
description: >-
  Resolve authoritative repository engineering policy for implementation, or run a
  cited conformance review. Loads only the mode-specific procedure and relevant rules.
argument-hint: "[resolve|review] [scope]"
---

Resolve policy without inventing or duplicating it.

$ARGUMENTS

Choose one mode, then load only its reference:

```text
resolve <scope> → references/resolve.md
review <scope>  → references/review.md
```

If mode is omitted: `/sy:spec` and `/sy:ship` normally mean `resolve`; `sy:gate` means `review`.

Authority order is always: dedicated repo standards skill → repository-maintained standards docs/rules → Shipyard fallback. Lower authority never overrides higher authority.

Keep returns compact and source-pointed. Human-facing plans may explain unusual constraints clearly; agent-facing standards contracts contain only task-relevant rules, primitives, lenses, and conflicts.

Every subagent dispatch resolves its model from config and passes it as the `Agent` invocation's actual model override, per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/model-dispatch.md`; a nested dispatch inherits nothing and must resolve again.
