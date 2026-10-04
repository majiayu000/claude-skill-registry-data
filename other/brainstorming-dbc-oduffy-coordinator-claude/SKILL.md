---
name: brainstorming
description: Shape vague or multi-subsystem asks into requirements. Size first if unsized.
description-budget: 135
version: 1.0.0
allowed-tools: ["Read","Write","Edit","Bash","Grep","Glob","Agent","Skill","AskUserQuestion","TaskCreate","TaskUpdate","TaskGet","TaskList"]
---

# Brainstorming

Turn the PM's intent into a design spec through collaborative dialogue. The PM decides what to
build; the EM shapes feasibility, flags constraints, proposes approaches. Output: a committed spec
that feeds `coordinator:plan`.

**Announce at start:** "Using brainstorming to explore the design before we plan implementation."

**When NOT to invoke:** a well-scoped next step on a known shape goes straight to
`coordinator:plan`, or just do it if trivial. Brainstorming is for genuine ambiguity in shape —
if the request would take 2+ rounds of "what is this even?" clarifying questions, it applies.

**vs. `coordinator:shape`:** siblings, not twins. Brainstorming is for *not knowing what to
build* (produces a solution artifact). `shape` is for *converging on a problem the PM already
holds*. Discriminator: PM wants confirmation you understood a problem → `shape`; PM doesn't know
what to build → `brainstorming`. Both terminate in `coordinator:plan`.

<HARD-GATE>
Once started, do NOT invoke any implementation skill, write code, scaffold a project, or dispatch
an executor until the spec is written and PM-approved. The only exit is a completed spec that
transitions to `coordinator:plan`. If the PM arrived with a clear spec, skip brainstorming
entirely — but once started, see it through.
</HARD-GATE>

The design can be lightweight — a few sentences for simple work — but it must exist and be
PM-approved before implementation. Simple-looking requests are where unexamined assumptions cause
the most rework; "we discussed it earlier" doesn't survive context compaction, the written spec
does.

## Process

```dot
digraph brainstorming {
    "Explore project context" [shape=box];
    "Clarify intent with PM" [shape=box];
    "More questions?" [shape=diamond];
    "Propose 2-3 approaches" [shape=box];
    "PM selects direction" [shape=diamond];
    "Present design sections" [shape=box];
    "PM approves design?" [shape=diamond];
    "Scope check" [shape=diamond];
    "Split into sub-specs" [shape=box];
    "Write spec" [shape=box];
    "Self-review" [shape=box];
    "PM reviews spec" [shape=diamond];
    "Invoke coordinator:plan" [shape=doublecircle];

    "Explore project context" -> "Clarify intent with PM";
    "Clarify intent with PM" -> "More questions?";
    "More questions?" -> "Clarify intent with PM" [label="yes"];
    "More questions?" -> "Propose 2-3 approaches" [label="no"];
    "Propose 2-3 approaches" -> "PM selects direction";
    "PM selects direction" -> "Propose 2-3 approaches" [label="none fit"];
    "PM selects direction" -> "Present design sections" [label="chosen"];
    "Present design sections" -> "PM approves design?";
    "PM approves design?" -> "Present design sections" [label="revise"];
    "PM approves design?" -> "Scope check" [label="approved"];
    "Scope check" -> "Split into sub-specs" [label="multi-subsystem"];
    "Scope check" -> "Write spec" [label="focused"];
    "Split into sub-specs" -> "Write spec";
    "Write spec" -> "Self-review";
    "Self-review" -> "PM reviews spec";
    "PM reviews spec" -> "Write spec" [label="changes"];
    "PM reviews spec" -> "Invoke coordinator:plan" [label="approved"];
}
```

**Terminal state:** the ONLY next step after brainstorming is `coordinator:plan`.

## Understanding Intent

<!-- BEGIN project-rag-preamble (synced from snippets/project-rag-preamble.md) -->

**Code lookup: project-rag first.**
`ToolSearch("select:mcp__project-rag__project_staleness_check,mcp__project-rag__project_symbol,mcp__project-rag__project_symbol_callers,mcp__project-rag__project_symbol_references,mcp__project-rag__project_symbol_brief,mcp__project-rag__project_referencers,mcp__project-rag__project_semantic_search,mcp__project-rag__project_rag_instructions")`
`project_staleness_check`; callers `project_symbol_callers`/`_references`; impact `project_referencers`; else `project_rag_instructions`.
If a project-rag call errors or its tools are absent (daemon down), fall back to Grep/Read and carry on.
Friction: memo `project-rag-em` / `gh issue create -R dbc-oduffy/project-rag`.
<!-- END project-rag-preamble -->

Check accumulated project knowledge first (architecture atlas, wikis, repo map) before reading
source. Clarifying questions: one per message, multiple choice when the decision space is
bounded, probing constraints rather than basics the PM has likely considered. Raise technical
concerns directly — honest counsel, not silent compliance. Independent subsystems each get their
own spec/plan/execution cycle — decompose first, then deep-dive each piece.

## Domain Language Discipline

If `CONTEXT.md` exists at the project root, read it before the first clarifying question; if
absent, proceed silently. Use its canonical terms; when the PM uses an `_Avoid_:`-listed synonym,
substitute and confirm: *"You said X — you mean &lt;canonical-term&gt;?"*

When the PM resolves a term during dialogue, update `CONTEXT.md` inline (don't batch): a `##
Terms` section, `**<Canonical term>** — one-sentence definition.` plus an `_Avoid_:` line of
synonyms actually seen. Lazily create the file on the first resolved term if it doesn't exist —
never scaffold it empty.

## Exploring Approaches, Presenting the Design

2-3 approaches with trade-offs (more creates decision paralysis), leading with your
recommendation — one sentence each on the idea, the trade-off, and when you'd choose it; say so
if one is clearly superior; flag a significant drawback even in a favored option. Scale each
design section to its complexity (a few sentences to ~300 words); ask after each whether it looks
right — incremental approval, not monolithic review. Cover as applicable: architecture,
components, data flow, interfaces, error handling, testing strategy. In existing codebases,
follow established patterns.

## Writing the Spec

**Save to:** `docs/specs/YYYY-MM-DD-<topic>-design.md` (create `docs/` if absent). Must carry
enough context for a cold-start agent to implement without conversation history.

**Self-review before presenting** (fix inline, no separate pass): no TBD/TODO/vague requirements;
no internal contradictions; scope focused enough for a single plan (split now if not); no
requirement readable two ways; `CONTEXT.md` updated for any term resolved in dialogue.

**Commit the spec**, then:

> "Spec written and committed to `<path>`. Please review — I'll hold on implementation until you
> approve."

Wait for PM response; apply changes and re-run self-review if requested.

## Spec Template

```markdown
# [Feature Name] Design Spec

**Date:** YYYY-MM-DD
**Status:** Draft | PM-Approved
**Goal:** [One sentence]

## Context
[What exists today, what problem this solves, why now.]

## Requirements
- [Requirement 1 — concrete, testable]

### Out of Scope
- [Thing we're NOT building and why]

## Design
### Architecture
### Components
### Interfaces
### Error Handling

## Trade-offs
| Decision | Chosen | Alternative | Why |

## Testing Strategy

## Open Questions
[Should be empty before PM approval.]
```

## Transition

Once the PM approves: **REQUIRED SUB-SKILL** `coordinator:plan`, spec file as input. No other
skill is a valid next step.
