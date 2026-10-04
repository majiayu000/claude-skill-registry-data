---
name: review
description: Meta-skill that routes a diff to the right per-lens review skill by blast radius. Does not duplicate any lens; it composes them. Use when you have a diff and want to know which skill to run.
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

# Review (router)

This skill is a router, not a reviewer. It decides which per-lens skill
should run against a diff and produces a routing decision in context;
the implementer or orchestrator then dispatches the chosen lens.

The lenses are not children of this skill; they remain independent and
may be invoked directly when the lens is already known. This skill
exists so the common case ("I have a diff, which lens?") has one
answer.

## Routing table

| Blast-radius signal | Lens |
|---------------------|------|
| Diff touches goroutine creation, channels, cancellation, or shared mutable state | `concurrency-review` |
| Diff adds or changes an exported symbol, imports a new package, or restructures a boundary | `architecture-review` |
| Diff adds authz/authn, secrets handling, network egress, prompt construction, or file-path safety | `secure-change` |
| Diff deletes a `func Test...`, adds a `t.Skip(...)`, drops a coverage line, or weakens an assertion | `test-review` |
| Diff introduces new types, new error sentinels, or grows past the 500/80 LOC soft limit without splitting | `simplification-review` |
| Always | `bug-audit` if the diff is non-trivial and reachable bugs are in scope |
| Diff is a docs-only change | skip; route to `docs-update` instead |

If more than one lens applies, run them in this order: `secure-change`
first (the cost of missing a finding is highest), then
`architecture-review`, then the per-concern lenses, then
`bug-audit`. Each lens runs against the same diff but produces a
disjoint finding set; a synthesised final report merges them.

## Input

A diff (`git diff`, the staged tree, or a `## Done` block from the
builder). The router does not need the diff's body - it reads the file
list and decides which lens fits.

## Output (exact shape)

```text
Routing decision for <diff summary>:
- primary: <lens-name>
- secondary: <lens-name> | none
- skip-rationale: <if a lens from the table is omitted, why>
```

## Disallowed operations

- `write_file`, `search_replace`, `run_command` that mutates state.
- Running any per-lens skill directly. The router decides; the
  implementer dispatches. If the dispatch tool itself runs the lens,
  it runs it as a separate call after this router returns.

## When not to use this skill

- When you already know the lens, dispatch it directly. Routing adds a
  round trip with no value.
- When the diff is empty (a no-op commit). Routing a no-op returns
  "skip; nothing to review."

## Escalation

- **Diff spans more than three packages.** Run `architecture-review`
  even if no single lens would otherwise pick it; multi-package diffs
  almost always have a boundary question.
- **The diff mixes a feature change with a refactor.** Surface this to
  the orchestrator and ask whether to split the commit. Do not review
  a mixed-shape diff as a single unit.

## Report shape

`.agents/skills/review/report-template.md` holds the long form of the routing
decision above. It adds an explicit `Verdict` field, which the short shape does
not carry, plus a rationale per route, the skipped lenses, and the attachments
an escalation carries. Read it with `read_file`
when the run needs that detail; the short shape above stays the default.

This skill routes. It does not merge findings: `review-synthesis` combines the
lens reports into one result.
