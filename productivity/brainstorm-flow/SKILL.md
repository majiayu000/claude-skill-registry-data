---
name: brainstorm-flow
description: Run Hephaera's persistent pre-planning Brainstorm mode for researched app, game, product, feature, or other idea discovery. Use when the user explicitly says to start or enter Brainstorm mode, asks to continue an active repository-root BRAINSTORM.md, requests the Brainstorm graph or full Markdown, explicitly exits Brainstorm mode, or selects a completed brainstorm element for later planning.
engines: [AGNOSTIC]
---

# Brainstorm Flow

## When to use

Use only after explicit mode activation such as `start Brainstorm mode` or when repository-root `BRAINSTORM.md` already has `Status: active`. An ordinary request that merely uses the verb “brainstorm” does not activate persistent mode.

Brainstorm is an optional discovery stage before planning:

```text
Brainstorm -> Plan -> Task | Goal | Gauntlet
```

## Workflow

1. Resolve the project root and inspect Brainstorm state with `./commands/brainstorm-mode.sh status`.
2. Before activation or resumed idea work, establish exactly three participants: the main agent cast as `computer-science/project-manager` plus two persistent `computer-science/researcher` subagents. If two researcher slots are unavailable, leave durable state unchanged and block idea processing; never substitute sequential or unassisted research.
3. Start with `./commands/brainstorm-mode.sh start` only after the user explicitly activates the mode. On a new session with active state, reconstitute both researchers before processing another idea.
4. Capture each materially distinct user idea as the next unused `IDEA-NNN`. Clarifications refine that element; they do not silently create a second element.
5. Establish baseline understanding through focused questions. Then place the element under the deepest suitable existing `BR-NNN` branch or create the next unused branch with a valid parent.
6. Give both researchers read-only packets with the idea, established understanding, branch context, and research questions:
   - Researcher one investigates the problem, audience, domain, comparable approaches, and precedent.
   - Researcher two investigates feasibility, constraints, dependencies, risks, start conditions, and measurable completeness.
7. Require source URLs for public/current claims and label evidence, inference, disagreements, and unresolved uncertainty. Keep researcher reports ephemeral.
8. Let only the project-manager synthesize and write the element to `BRAINSTORM.md`. Include every required field and subsection, then run `./commands/validate-brainstorm.sh --phase active`.
9. Use `captured`, `clarifying`, `researching`, `plan-ready`, or `parked`. Set plan readiness to `yes` only when every subsection is substantive and research includes at least one HTTP(S) citation.
10. When the user asks to see the brainstorm, run `./commands/show-brainstorm.sh` and present its Mermaid mindmap. If the user explicitly asks for Markdown, run `./commands/show-brainstorm.sh --markdown` and return the entire file.
11. Stop only after explicit user direction with `./commands/brainstorm-mode.sh stop`. This preserves incomplete elements, marks the mode inactive, and regenerates `BRAINSTORM_SUMMARY.md` as the hash-bound branch index.
12. After exit, wait. Start planning only when the user explicitly selects an element; planning may later feed Task, Goal, or Gauntlet flow.

## Output

- Repository-root `BRAINSTORM.md` containing durable mode, session, branch, and full element state.
- Repository-root `BRAINSTORM_SUMMARY.md` generated only on explicit exit as a current hash-bound index.
- A Mermaid mindmap for the default “show brainstorm” request, or verbatim Markdown when explicitly requested.
- A plan-ready element with evidence, start conditions, and a concrete definition of complete.

## Guardrails

- Never create or mutate task, issue, Goal, Gauntlet, implementation, commit, branch-publication, or PR state while Brainstorm is active.
- Never infer activation or deactivation from inactivity, completeness, or an ordinary ideation request.
- Never create task-backed `SUBAGENTS.md` for Brainstorm. The fixed research team is mode-owned and researchers remain read-only.
- Never let researcher subagents write Brainstorm artifacts; the project-manager owns branch placement, reconciliation, and the sole write set.
- Never mark an element plan-ready with pending sections, unsupported current claims, hidden disagreements, or a vague start/finish boundary.
- Never discard, renumber, or reuse branch or element IDs. Preserve incomplete and parked ideas in the full artifact and exit summary.
- Never put credentials, personal data, private-source content, or unsupported legal, financial, or medical conclusions in Brainstorm artifacts.
