---
name: rite-zoom-out
description: "User-invoked read-only structural map of unfamiliar code: modules, callers, callees, and relevant decisions."
argument-hint: "[symbol | file | area to map]"
user-invocable: true
disable-model-invocation: true
---
<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/tooling.md"],"workspace":["spec.md","plan.md","decisions.md","state.md"],"rootOnly":["devrites-lib/reference/standards/code-index.md"]} -->
> Read-set manifest: `devrites-engine context <slug> --skill rite-zoom-out` (no workspace: `--out <path>`) bundles every file named below into one deduplicated read.

# /rite-zoom-out: step up one abstraction layer

When the agent (or the user) is staring at unfamiliar code without a working mental
model of how it fits the larger system. Stops the "open more files" reflex by returning
a single, structured map instead.

Read `.claude/skills/devrites-lib/reference/standards/core.md` first: chiefly its existing-conventions
discipline, which keeps the map in the project's own language. The other rule files load
on demand.

## What this skill returns

A **structural map**: terse. One pass should answer:

- **The area:** what this code is for, in one sentence, using the project's own
  vocabulary.
- **Modules in scope:** the related files / packages / slices, with a one-line
  purpose each.
- **Callers (in):** who calls into this area from outside. Keep to the highest-signal
  3-6; collapse the rest.
- **Calls (out):** what this area depends on downstream.
- **Decisions touching it:** ADRs (under `docs/adr/` if present) or notes in
  `.devrites/work/<slug>/decisions.md` that pre-decide something here.
- **Smallest sensible change-scope:** where a fix would naturally land, so the next
  step doesn't drift into a project-wide refactor.

## Prefer codebase-memory-mcp (if available)

Apply `.claude/skills/devrites-lib/reference/standards/code-navigation.md`:
`get_architecture` (`aspects: ["overview"]`, `path` = the area) for modules,
`trace_path` (`direction: "inbound"` / `"outbound"`) for callers and calls, then fall
back to LSP and file search. Do not repeat a query merely to confirm the same map.

## Vocabulary discipline

Use the **project's** domain language: `CONTEXT.md`, glossaries, the active feature's
`spec.md` / `decisions.md`. Don't invent fresh names for things the project already
names. If you notice a fuzzy or overloaded term while mapping, flag it as a FYI at the
end; don't try to fix it here.

## When NOT to use

- You already have a clear mental model: zooming out is just tax.
- The question is a literal text lookup (a string, a comment, an error message): use
  `Grep`.
- You need to design or change something. That's `/rite-spec` (new feature) or
  `/rite-define` (plan an approved spec).
- You want a project-wide architecture audit: use the project's normal architecture
  review process; this skill is a read-only feature-area map.

```
Done: mapped <area> in the project's vocabulary.
Changed: none (read-only)
Evidence: modules <n>; callers <n>; callees <n>; decisions <n>
Open: <none | fuzzy term | suspected drift | open question>
Next: <single recommended command>
Record: not applicable (paths printed only)
↻ Hygiene: /clear if this was only orientation; /rite-handoff if it informs active work
```

Print the path of any decisions/ADR files referenced so the user can open them.

**Empty or not found.** When the argument resolves to no symbol, file, or area, or maps zero
modules, never print `Done: mapped` or `modules 0`: print `Done: not mapped — <argument> not
found` with the searches run (index and file search), `Open:` the nearest candidates or
`none`, and `Next:` a corrected argument.
