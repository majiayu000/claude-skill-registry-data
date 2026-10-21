---
name: proposal-architect
description: Write technical proposals, design docs, RFCs, and architecture decision records in progressive layers. Starts as a one-page brief and deepens only on request, one layer per iteration, freezing decisions as it goes so later detail never reopens settled questions. Final layer emits decoupled, dependency-ordered implementation tasks derived from interface contracts rather than from guesswork. Use whenever the user wants to author or extend a proposal, design doc, RFC, ADR, one-pager, or technical brief; whenever they say "go deeper", "next iteration", "expand section X", or "break this into tasks"; and whenever they need a written design artifact that a senior review audience will approve or block. Not for reviewing someone else's proposal.
---

# Proposal Architect

## Operating rules

These hold at every layer. Violating them is a defect, not a style choice.

- **Output is always a Markdown file.** Never DOCX. Never an artifact. One file per proposal, extended in place across iterations.
- **Never include time or effort estimates.** No hours, days, sprints, weeks, person-months, t-shirt sizes, or story points. Phase by dependency order only. This overrides the E and T letters in INVEST/SMART below.
- **Never silently edit an existing file.** Every iteration appends to a `## Changelog` section at the bottom naming exactly what changed, under a version heading.
- **No em dashes.** Use commas, periods, or split the sentence.
- **Never start a sentence with "So".**
- **Write the trade-off, not the tour.** A document that says how it will be implemented without saying what was traded away is an implementation manual, and an implementation manual is a sign the code should have been written instead.

## The core mechanic: layered freeze

The proposal is written in five layers. Layer 0 ships first and stands alone. Each later layer is produced only when the user asks to go deeper.

The mechanism that makes this work is the **freeze**. Every layer ends by recording the decisions it settled in a `### Frozen at L<n>` block. Later layers may add detail *inside* the frozen envelope. They may not quietly contradict it.

Without this, progressive elaboration degenerates: layer 3 reopens a layer 1 decision, layer 4 reopens layer 2, and the document oscillates instead of converging. The freeze is what distinguishes deepening from rewriting.

**When a later layer genuinely needs to break a freeze**, do not edit the frozen block in place. Add an `### Amendment` entry naming the frozen decision, what forced the change, and what it costs. This mirrors how design docs actually age in large orgs, accumulating amendments rather than being silently rewritten, and it leaves the reasoning legible to whoever reads the doc later.

State at the end of every iteration which layer is now current and what the next one would add. Do not volunteer the next layer unasked.

---

## L0: The brief

**One page. Hard limit.** This is the whole deliverable until the user asks for more. Most proposals should be allowed to die here cheaply, and a one-pager that gets rejected has cost almost nothing.

Sections, in order:

```markdown
# <Title>

## Context
Objective background only. What exists today, what the landscape is. No opinions,
no proposal. Assume the reader knows the domain. Link out for detail.

## Problem
One paragraph. What is actually broken or missing, stated so that someone who
disagrees can say precisely what they disagree with.

## Goals
3 to 5 bullets.

## Non-goals
Things that could reasonably have been goals and are deliberately excluded.
Not negated goals. "Must not crash" is not a non-goal. "Multi-region failover"
is a non-goal.

## Proposal
Two or three paragraphs. The shape of the solution, not its mechanics.

## Decision requested
Name the exact decision and who makes it. Approve a direction, approve a build,
approve a spend, ratify something already shipped. The bar differs enormously
and the reader needs to know which one they are being asked for.

### Frozen at L0
- <decision>: <what was settled>
```

Goals and non-goals do the heaviest lifting in the entire document. Non-goals are what let a reviewer stop arguing about scope and start evaluating the design.

---

## L1: The shape

Produced on request. Adds structure without committing to mechanics.

- **System context.** Where this sits in the existing landscape. A diagram in Mermaid, showing the new system and the systems it touches. Context diagrams let readers anchor new work against what they already know.
- **Components.** The major pieces and their responsibilities. One line each. Not classes, not files.
- **The central trade-off.** Every design worth writing down has one. Name it explicitly.
- **Alternatives considered.** At least two real ones, plus "do nothing" when the status quo is functional. Each gets what it optimizes for and why it lost. This section is the most load-bearing in the document, because it shows why the chosen design beats the ones the reader is already thinking about. Strawmen here destroy the document's credibility.
- **Degree of constraint.** State whether this is greenfield (solution space wide, needs rules to narrow it) or constrained (solutions enumerable, the difficulty is combining them). The two shapes need different arguments.

Freeze: component boundaries, the chosen alternative.

---

## L2: The contracts

**This layer is what makes the eventual tasks decoupled.** Everything else is commentary.

Tasks do not become independent by being written as separate tickets. They become independent when every seam between them is specified before anyone starts. Define the seams here and the task split falls out mechanically. Skip this layer and L4 produces tasks that are decoupled on paper and serialized in practice, which is the most common way a work breakdown fails.

For each boundary identified at L1:

- **Interface.** Shape of the call or message. Enough to implement against, not a pasted schema. Verbose formal definitions in a design doc go stale and bury the parts that matter.
- **Data shape.** What crosses the boundary, in rough form.
- **Failure semantics.** What happens on timeout, retry, duplicate delivery, partial write. Idempotence assumptions stated explicitly, because every unstated one becomes a production incident.
- **Invariants.** What must be true on both sides, and who enforces it.
- **Ownership.** Which component owns the data, which only reads it.

Pseudo-code only for genuinely novel algorithms. Link a prototype instead where one exists, since a working prototype is among the strongest arguments a design doc can make.

Freeze: every interface and its failure semantics. This is the freeze that matters most. Breaking it at L4 means re-cutting the task graph.

---

## L3: Consequences

Produced on request. This is the layer senior reviewers actually read.

- **Cross-cutting concerns.** Security, privacy, observability, operability, data integrity. One short paragraph each saying how the design affects the concern and how it is addressed. Mark the ones that do not apply rather than omitting them silently. Organizations standardize this list precisely so it stops being forgotten.
- **Failure modes.** What breaks, what the blast radius is, what the manual override is.
- **Migration and rollback.** How the system gets from here to there, and what happens if it has to go back.
- **Risks, classified.** Separate the two kinds explicitly, following ATAM's risk/non-risk distinction:
  - *Non-risk*: well-understood area, known solutions exist, the choice among them is open. Record it and move on.
  - *Risk*: ambitious quality goal, novel technology, or genuine uncertainty, where resolving it badly changes the recommendation.
  
  Only risks get mitigations. Treating selection choices as risks inflates the section and trains reviewers to skim it.
- **Reversibility.** Flag every one-way door: public API commitments, lossy migrations, customer-visible billing or compliance artifacts, vendor lock-in, anything that becomes a team boundary. Scrutiny scales with reversibility, and saying which decisions are cheap to undo is what lets the rest move fast.
- **Open questions.** Everything deliberately unresolved, listed. A gap that is written down is deferred. A gap that is not is a defect, and it will be found in review as a defect.

Freeze: the risk classification and the open-questions list.

---

## L4: Tasks

Produced on request. Requires L2, since contracts are the input.

### Generating the split

1. Take each frozen contract from L2. A contract is a seam, and a seam is a valid cut point.
2. Cut the work so that each task touches exactly one side of any seam it crosses, or owns both sides entirely.
3. For each task, record which contracts it **consumes** and which it **produces**. A task that produces a contract blocks every task that consumes it. That relation, and nothing else, is the dependency graph.
4. Order by dependency depth. Never by time.

If a task cannot be expressed in terms of contracts it consumes and produces, L2 is incomplete. Go back rather than guessing.

### Task quality bar

Adapted from INVEST, with the estimation letters removed per the no-estimates rule:

- **Independent.** No ordering dependency beyond the declared contract graph.
- **Negotiable.** States the outcome, not the implementation. The ticket is a promise of a conversation, not a spec.
- **Valuable.** Cuts vertically through layers rather than horizontally. A complete persistence layer with nothing calling it delivers nothing. Horizontal slicing is the default instinct and it is wrong.
- **Small.** Small enough that its scope is fully understood. Measure by whether it splits cleanly, not by duration.
- **Testable.** A verifiable done condition. If nobody can say how to test it, the task is not understood yet.

### Task format

```markdown
### T<n>: <imperative title>

**Outcome**: What is true when this is done.
**Consumes**: <contract ids, or none>
**Produces**: <contract ids, or none>
**Blocked by**: <task ids, or none>
**Done when**: Verifiable condition. Not "implemented", not "works".
**Out of scope**: What a reader might assume is included and is not.
```

Group into phases by dependency depth: Phase 1 is every task with no blockers, Phase 2 is everything unblocked once Phase 1 lands, and so on. Phases are a topological ordering, never a calendar.

---

## Register

Write in institutional architect voice, not personal voice. Flat, declarative, specific. The document outlives the author and may be read by people who have never met them.

- Short declaratives. Vary sentence length so the text does not read as machine-generated.
- Name mechanisms, files, numbers, and systems directly. Never "there may be concurrency concerns"; write "two sessions writing the same output prefix will race".
- Technical terms naked. No parenthetical definitions. The audience is peers.
- Hedge only where real uncertainty exists, and then say what would resolve it.
- Banned: comprehensive, robust, seamless, leverage, end-to-end, stakeholders, nuanced, deep dive, that said, it's important to note, this is where it gets interesting.
- Banned constructions: rule-of-three lists, "not just X but Y", "highlighting the importance of", "underscoring the need for", three consecutive sentences of similar length.
- No preamble, no summary paragraph that restates what was just said.

## Changelog discipline

Every iteration after the first appends to the bottom of the file:

```markdown
## Changelog

### L<n> (<date>)
- Added: <sections>
- Frozen: <decisions newly frozen>
- Amended: <any frozen decision changed, with the reason>
- Unchanged: <layers untouched>
```

List amendments even when they look minor. The amendment record is the part of the document that is still useful two years later.

## Grounding

- **Design Docs at Google** (Malte Ubl, Industrial Empathy): context/goals/non-goals/design/alternatives/cross-cutting structure, the alternatives section as the highest-value part, the 10-20 page ceiling and the legitimacy of a 1-3 page mini doc, and the warning against docs that are implementation manuals. https://www.industrialempathy.com/posts/design-docs-at-google/
- **INVEST and SMART** (Bill Wake, 2003): task quality criteria, and the vertical-slicing argument that a single architectural layer has no value on its own. https://xp123.com/invest-in-good-stories-and-smart-tasks/
- **ATAM** (Kazman, Klein, Clements, SEI/CMU): risk versus non-risk classification used in L3. https://www.sei.cmu.edu/documents/629/2000_005_001_13706.pdf
- **ADRs** (Michael Nygard): context, decision, consequences. A decision recorded without its consequences is incomplete.
- **One-way and two-way doors** (Bezos, 2015 Amazon shareholder letter): reversibility as the scrutiny dial used in L3.

The register above is drawn from documented practice, not from an inferred house style.
