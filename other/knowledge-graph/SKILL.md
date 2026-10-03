---
name: knowledge-graph
description: How to read and update the hand-curated knowledge graph at .claude/knowledge-graph/ (architecture decisions, module purpose, footguns, external dependencies). Use before a broad exploration pass to avoid rediscovering known context, and after any change that reveals something a future session would otherwise have to relearn.
---

# Knowledge graph

`.claude/knowledge-graph/` holds the things about this codebase that aren't visible
just from reading the code: *why* a decision was made, what a module is actually for,
what's fragile, what depends on what externally. It's plain markdown, versioned with
the code, and complements (doesn't replace) the generated `.claude/code-graph/`
(structure) and your own cross-session user memory (preferences/feedback, not
project facts).

## Layout

```
.claude/knowledge-graph/
  index.md            # entry point: list of entries with one-line descriptions
  decisions/           # one file per non-obvious decision
  modules/             # one file per module/subsystem worth explaining
```

## Entry format

Each entry is a short markdown file with frontmatter:

```markdown
---
name: kebab-case-slug
type: decision | module | dependency | footgun
related: [other-slug, other-slug]
---

One paragraph, max. State the fact/decision, then why, then how it should shape
future changes. Link related entries by slug via `related:` rather than repeating
their content.
```

Keep entries short — a few sentences. This is a graph of judgment calls and
non-obvious facts, not a changelog or a design doc archive.

## When to read it

Before a broad exploration pass on unfamiliar territory in this repo — check
`index.md` first; it's usually faster and more reliable than re-deriving the same
context from scratch.

## When to update it

Whenever a change reveals something a future session (yours or another agent's)
would otherwise have to rediscover the hard way: a non-obvious constraint, a
decision that looks wrong until you know the reason, a new external dependency, a
footgun you just avoided or hit. The `graph-keeper` subagent does this automatically
after non-trivial changes (see `/graph-update`) — but add an entry yourself in the
moment if you're not delegating to it.

Update stale entries rather than only adding new ones. A wrong entry actively misleads
a future session; a missing one just costs a re-discovery.
