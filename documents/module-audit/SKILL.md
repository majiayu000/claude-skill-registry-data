---
name: module-audit
description: Survey a codebase for shallow modules and produce a ranked report of consolidation opportunities with before-and-after diagrams.
disable-model-invocation: true
argument-hint: "/module-audit [path] [--html]"
allowed-tools: "Read, Grep, Glob, Bash, Agent, Skill"
---

## Overview

Find the parts of the codebase where the interface is doing too little work for the implementation it presents, and recommend consolidations that hide complexity behind smaller interfaces. Output is a Markdown report by default; `--html` produces an HTML variant for browser viewing.

## When to Use

- Understanding one concept in an area means opening many small files, and changes there keep touching all of them.
- Before a `/refactor` of module boundaries, to rank which consolidation pays off first.
- `/investigate` reported that a bug had no correct seam for its regression test.
- For broad architecture debt across the whole project, use `/assessment` first; for executing a chosen consolidation, use `/refactor`.

## Vocabulary

Use these terms consistently in every finding. Full definitions in [`VOCABULARY.md`](VOCABULARY.md).

- **Module.** Anything with an interface and an implementation. A function, a class, a package, a layer of slice. Scale-agnostic.
- **Interface.** Everything a caller has to know to use the module correctly. Types, invariants, error modes, ordering constraints, configuration, performance characteristics. Not only the type signature.
- **Implementation.** What lives inside.
- **Depth.** How much behavior a caller can drive per unit of interface they have to learn. A module is **deep** when the interface is small and the implementation is large. A module is **shallow** when the interface is nearly as large as the implementation.
- **Seam.** The place an interface lives. A spot where behavior can change without editing the call site.
- **Adapter.** A concrete thing that satisfies an interface at a seam.

Two principles drive every finding:

- **Deletion test.** Mentally delete the module. If complexity vanishes, the module was a pass-through. If complexity reappears across N callers, the module was earning its keep.
- **One adapter is hypothetical, two are real.** A seam is worth its cost only when at least two concrete implementations live behind it. A single-adapter seam is just indirection.

## Process

### 1. Scope the survey

With a path argument, survey that path and skip the inference below.

With no path, find the hot spots first. Consolidating a module pays off by making its next change cheaper, so weight the files that keep changing:

```bash
git log --since=<window> --name-only --format= | sort | uniq -c | sort -rn | head -30
```

The window defaults to `6.months`. When the top of the list is flat, with no file or directory clearly ahead, widen the window once, then survey the directories the top entries share.

### 2. Read the glossary and the ADRs

If a `GLOSSARY.md` exists at the project root, or a `GLOSSARY-INDEX.md` points at per-context glossaries, load it. Use its domain terms in every finding instead of generic words like "service" or "component". See [`rules/project-glossary.md`](../../rules/project-glossary.md).

If no glossary exists, proceed and use the names the code itself uses.

Read every ADR under `docs/adr/` that touches the scoped area before walking the code. An accepted ADR records a decision this audit does not re-litigate; a candidate that contradicts one is reported only when the friction justifies reopening it.

Collect prior rejections before proposing anything. Sources are ADRs, any `decisions.md` in the project, and pull requests closed without merge:

```bash
GH_TOKEN=$(gh auth token --user <account>) gh pr list --state closed --search "<area keywords> is:unmerged" --json number,title,closedAt,url --limit 50
```

A candidate rejected before with a stated reason is not proposed again unless that reason no longer holds. When it no longer holds, the finding names the prior rejection, quotes its reason, and states what changed.

### 3. Walk the code

Read every file in scope in full with the Read tool. For breadth, delegate slices to a `general-purpose` subagent whose brief requires full reads with the Read tool and `file:line` evidence; never send this analysis to `Explore`, which reads excerpts, per [`rules/verification.md`](../../rules/verification.md). Note where the model experiences friction:

- Understanding one concept requires bouncing between many tiny modules.
- A module's interface is almost as large as its implementation.
- A module exists only to forward arguments to one downstream call.
- Two adjacent layers expose the same vocabulary.
- A test for the module mocks every collaborator, so the test exercises the mocks instead of the module.
- Pure functions were extracted only for testability, while the bugs live in how they are called, so the tests pass and the call sites stay untested.
- A code path that the user describes as "always changes together" lives in N separate files.

For each candidate, apply the deletion test silently. If deletion concentrates complexity, keep the candidate. If deletion just shifts it, discard the candidate.

### 4. Classify dependencies

For every candidate, classify the dependencies the consolidated module would need to talk to. See [`REFACTOR-STRATEGY.md`](REFACTOR-STRATEGY.md):

- **In-process.** Pure computation, in-memory state, no I/O. Always consolidatable.
- **Local-substitutable.** A real local instance can run in the test suite, like the database in docker-compose or a temp directory. Test against that instance, never an in-memory substitute, per [`rules/testing.md`](../../rules/testing.md).
- **Remote but owned.** Your own service across a network. Tests run the real service locally in docker-compose, since your own services are never mocked. Define a port only when two production adapters are real.
- **External and not owned.** A third-party API. Inject a port, mock the adapter in tests.

The classification chooses the testing strategy and the seam shape.

### 5. Produce the report

Default output: a Markdown file written to `$TMPDIR/module-audit-<timestamp>.md`. With `--html`, write an HTML file at the same path with `.html` instead of `.md` and open it.

For each candidate, one section:

- **Files.** The modules involved.
- **Friction.** Why the current shape causes pain. Use glossary vocabulary.
- **Recommendation.** What to consolidate, what stays, what new shape the interface takes.
- **Before and after.** Two Mermaid diagrams side by side.
- **Test strategy.** Where the new interface is tested and which dependency category it falls into.
- **Strength.** One of `strong`, `worth exploring`, `speculative`.
- **Tension with existing ADRs.** Only when the recommendation conflicts with an accepted ADR, and only when the conflict is worth reopening.

Order the sections by rank. Rank each candidate on four criteria and show the scores in a table at the top of the report:

| Criterion | Question |
|-----------|----------|
| Leverage | How much downstream code gets cheaper to change |
| Locality | How much scattered complexity the consolidation concentrates in one place |
| Test surface | Whether the deepened interface makes tests simpler and closer to real behavior |
| Cost to value | Whether a small change unlocks a lot, which beats a sprawling rewrite |

End the report with a `Top recommendation` section: which candidate to tackle first and why, citing its scores.

Announce the report path, ask "Which candidate do you want to explore?", and stop. Propose no interface until the user picks one.

### 6. Explore the pick

After the user picks a candidate, switch to [`INTERFACE-OPTIONS.md`](INTERFACE-OPTIONS.md) to generate at least three radically different interface designs in parallel and pick one.

Keep the domain model current while the discussion runs, per [`rules/project-glossary.md`](../../rules/project-glossary.md):

- A consolidated module named after a concept missing from the glossary: add the term to `GLOSSARY.md` in the same turn, creating the file on that first term.
- A fuzzy term sharpened during the discussion: update its entry right there, including the `Avoid:` line.

When the user rejects a candidate for a load-bearing reason, one a future audit would need to avoid suggesting it again, offer an ADR: "Want this recorded as an ADR so later audits skip it?" On yes, call the Skill tool with `plan` and the arguments `adr new <title>`. Skip the offer for a temporary reason such as "not now" and for a self-evident one.

## Common Rationalizations

- "This module is small and tidy, so it is fine": size is not depth. Apply the deletion test and measure behavior per interface element.
- "A port now makes the second adapter cheap later": one adapter is hypothetical. Recommend the port only when two adapters are justified today.
- "That ADR is old, the recommendation can ignore it": an accepted ADR stands. Report the candidate only when its friction justifies reopening the decision, and name the tension.
- "I already see the right interface, I will put it in the report": the report ends at the question. Interfaces come after the pick, as at least three designs from [`INTERFACE-OPTIONS.md`](INTERFACE-OPTIONS.md).
- "`Service` reads clearly enough": findings use the [`VOCABULARY.md`](VOCABULARY.md) terms and the project glossary, so two audits name the same thing the same way.

## Red Flags

- Stop and discard the candidate when the deletion test shows complexity shifting rather than concentrating.
- Stop and drop the port when only one adapter is justified.
- Stop and read the ADRs under `docs/adr/` when a candidate touches an area they cover and they have not been read.
- Stop and rename when a finding says component, service, API, or boundary where VOCABULARY.md has a term.
- Stop and wait for the user's pick once the report path is announced.
- Stop and drop the candidate when an ADR, a `decisions.md`, or a pull request closed without merge rejected it for a reason that still holds.

## Verification

- Every finding uses VOCABULARY.md terms.
- Every finding passes the deletion test.
- Every port introduced has two adapters justified.
- No candidate repeats a prior rejection whose reason still holds, and the report ranks candidates on leverage, locality, test surface, and cost to value.
- The report uses Mermaid for diagrams, never ASCII art.
- Output path is announced to the user.

## Related skills

- `/assessment` find broad architecture debt before this skill drills in.
- `/refactor` execute the recommended consolidation incrementally.
- `/plan adr new` record any non-obvious decision the consolidation rests on, and any rejection a later audit must not repeat.
