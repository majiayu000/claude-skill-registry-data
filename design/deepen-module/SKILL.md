---
name: deepen-module
description: Use when a person asks to design a new module's interface or to rework an existing module so that it hides much behind little, in any tier (backend, frontend, test support, tooling), or says a module's callers know too much about it. Produces a module document in aiview, how a caller uses it, its one public entry point as signatures, what stays outside and the gap from today, discussed with the person until agreed. Not for writing the task that carries the rework out (orchestrate's tasks) and not for the rework itself.
---

# Deepen a module

**The goal is to hide accidental complexity**: the codebase knows the module's entry and nothing behind it, as if it were a package that has not been published.

**A building block is not a deep module**: a module other modules are built from, one job, several callers, no module document of its own. It still has an entry, held to the same rule as a deep module's (*The entry*, below).

**One `module` document per module, written from the first finding, never in chat.** Through the `aiview` skill: kind `module`, file `YYYY-MM-DD-<module>.module.md`, tags = module name, in the plan's group when a plan waits on it. Each stage below writes its sections into it.

## Discover

**For an existing module, discover its actual boundaries before designing.** Its code may be scattered across the codebase. Document its files, its callers and its application dependencies in *Today*. A new module starts at Design.

## Design

**Sections in this order, each marked provisional where an open decision could change it.**

1. **Usage**: the complete code a caller writes to use the module; for a component, its tag with its inputs and outputs. It carries the caller's intent and no accidental complexity: no wiring, ordering, configuration or knowledge of internals.
2. **The entry**: one logical public entry point per case the callers are in: a file, a component, a factory or a package entry. Callers bound by different rules get an entry each, named for their case, over a core they cannot import. All public access goes through an entry, each surface stays cohesive, and each is written as signatures without bodies.
3. **Outside**: what stays in the project: its data, and the one binding that passes the project's names to the module.
4. **The conditions**, each marked held or broken today:
   - all access to the module goes through the entry
   - the module imports nothing from the application, and receives any collaborator it drives
   - it reads no environment and no global state
   - every project-specific name, path or setting is an option with a working default
   - its tuning numbers (a limit, a retry count, a default, a threshold) are named once in one constants file beside its entry, never written as a literal in a branch or a schema bound
   - its tests go through the entry only, and a boundary test enforces these conditions
5. **The gap**: what changes from *Today* to reach the design: exports, imports, and every caller. Changing the callers is part of the work. A large gap is drawn, who depends on whom before and after, through the `write-diagrams` skill.
6. **The open decisions**, numbered, each with its options and a recommendation.

## Discuss

**Resolve the open decisions with the `interview` skill**, writing each answer into the section it changes. Challenge every export: what no caller clearly needs stays inside.

## Agree

**The document is agreed when the list is empty and the person says so.** The date goes in its header, and the entry is frozen: a later change to it is a new decision.

## Implement

**The rework is a task, and it quotes the agreed entry word for word.**

## Red flags

| Thought | Reality |
|---|---|
| "I'll add an option for that" | An option nobody passes is surface. |
| "One entry, an option picks the mode" | Neither the import nor the call says which rules apply. One entry per case. |
| "Callers may need this helper" | Name the caller. One that exists only in the tests is served by the entry. |
| "It's only a 3, it reads fine inline" | The same 3 in a second file drifts from the first. Name it in the constants file. |
