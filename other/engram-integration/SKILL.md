---
name: engram-integration
description: Engram embedded + MCP fallback. Topic key conventions. Load when touching anything memory-related or starting/closing a session.
triggers:
  - engram
  - memory
  - "mem_save"
  - "mem_search"
  - "session summary"
  - topic_key
---

# Engram integration

Engram is first-class memory for nyxterm. Not an optional MCP plugin — a core capability with MCP fallback.

## Layers (in order of preference)

1. **Embedded Engram library** (preferred): linked into the binary, local sqlite store at `~/.local/share/nyxterm/engram.db`. Zero subprocess overhead.
2. **MCP fallback**: when a remote Engram server is configured (`engram mcp --tools=agent`), use that — useful for shared team memory.
3. **Offline mode**: no memory persistence. Warns the user once at startup.

Configurable in Settings → Memory.

## When to save (PROACTIVE — don't wait to be asked)

Call `mem_save` immediately after:

- A user decision or stated preference.
- A bug fixed (with root cause).
- A non-obvious discovery about the codebase or environment.
- A convention established.
- A workflow change.
- A user-confirmed recommendation ("dale", "go with that").

Self-check after every task: *"Did I learn or decide something non-obvious? If yes → save NOW."*

## Topic key conventions

Stable, hierarchical, kebab-case:

- `nyxterm/architecture` — top-level architecture decisions
- `nyxterm/pty/sigwinch` — specific gotcha
- `nyxterm/theme/tokyo-night` — palette decisions
- `nyxterm/ai/provider-routing` — multi-provider config
- `nyxterm/multiplex/keybinds` — keybind decisions
- `nyxterm/nix/flake-structure` — packaging

Different topics MUST NOT overwrite each other. Same topic evolving → use same key (upsert via `mem_save` with same `topic_key` or `mem_update` by id).

When unsure of the right key, call `mem_suggest_topic_key` first.

## When to search

- On any "remember", "recall", "what did we decide", "how did we solve" from the user.
- On the user's FIRST message of a session if it references a feature or problem.
- Before claiming "X was decided" or "Y exists" — verify.

Two-step pattern:
1. `mem_search(query)` → list of candidates with truncated content.
2. `mem_get_observation(id)` → full untruncated content.

## Session close (MANDATORY)

Before saying "done" / "listo" / closing a session, call `mem_session_summary`:

```markdown
## Goal
[What this session was working on]

## Discoveries
- [Non-obvious findings]

## Accomplished
- [Completed items with key details]

## Next Steps
- [Pending work for next session]

## Relevant Files
- path/to/file — [what it does or what changed]
```

Skipping this means the next session starts blind. Don't skip.

## What NOT to save

These are derivable from the codebase — don't pollute memory:

- File paths, function signatures, public API.
- Git history, who-changed-what.
- Specific fix recipes (the commit/PR has the context).
- Ephemeral task state (use TaskCreate, not Engram).
- Anything documented in `AGENTS.md` or skills.

Save only what is **non-obvious** and would be lost without explicit persistence.

## After compaction (if you see a compaction marker)

1. Immediately `mem_session_summary` with the compacted content — persist what was done before compaction.
2. `mem_context` to recover prior session context.
3. Only then continue work.

## Topic upsert vs new entry

- Same topic, evolving: use same `topic_key`, content replaces (or appends if you set update flag).
- New facet of an existing topic: new key (e.g., `nyxterm/pty/coalescing` vs `nyxterm/pty/sigwinch`).
- Unsure → `mem_suggest_topic_key`.
