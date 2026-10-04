---
name: story-clarifier
description: Draft, synthesize, rewrite, tighten, or split rough tickets, conversations, user stories, feature definitions, and acceptance criteria into testable story cards or split story sets, or audit existing story inputs with a separate readiness report. Use for ambiguous story-level product behavior or when supplied discussion and artifacts must be consolidated without interviewing; not for PRDs, test strategy, repository scouting, implementation planning, or coding.
---

# Story Clarifier

Turn rough product intent into a compact story artifact whose behavior and
boundaries are explicit enough for repository scouting and implementation
planning.

## Modes

- **Draft:** create an artifact from rough intent; infer only low-risk details
  and label them as assumptions.
- **Synthesize:** consolidate supplied conversation, artifacts, and material
  comments without interviewing. Return a non-ready artifact when the sources
  are insufficient or materially conflict; do not invent a resolution.
- **Rewrite:** replace the source while preserving its scope, meaning, and
  supplied constraints; call out intentional semantic changes.
- **Tighten:** remove repetition and sharpen oracles without adding behavior.
- **Audit:** report findings against source sections or criterion IDs; do not
  rewrite unless asked.
- **Split:** create ordered, independently useful vertical slices; materialize
  each near-term slice with the complete Story Card contract.

## Workflow

1. Select the mode. Read the full authorized referenced source and the material
   comments, replies, and revisions needed to interpret it before asking the
   user to repeat information. Preserve supplied paths, issue URLs, external
   identifiers, and version or revision labels exactly.
2. Map the story breadth-first before drilling into one branch: extract the
   actor, beneficiary, or operating situation; trigger or need; outcome and
   value; behavior and visible state; permissions; success, failure, and edge
   branches; constraints; dependencies; assumptions; non-goals; and unknowns.
3. Preserve supplied technical, policy, compliance, and interface constraints.
   Separate them from inferred implementation suggestions and never silently
   weaken or replace them. Never turn a material unverified claim into an
   assumption.
4. Resolve contradictions and replace vague language with observable behavior.
   Label only safe, reversible inferences as assumptions. Classify every
   material unknown using the format below.
5. In **Audit**, report questions as findings rather than starting an interview
   unless the user requested one. For other modes except **Synthesize**, build
   the question frontier from sharp
   decisions whose prerequisites are settled. Ask at most three independent
   frontier questions per batch, do not ask a downstream question alongside
   its unresolved prerequisite, and recompute the frontier after each answer.
   In **Synthesize**, do not interview; if a frontier remains, preserve it and
   return the truthful non-ready status.
6. Choose the artifact shape, apply its contract, and run the ready check. Keep
   unresolved material visible.

Format every non-empty Open Questions item as one of:

- `[Fact]` unknown - `Owner`, `Prerequisite`, and `Next action`. Inspect an
  authorized supplied source first; route repository facts to
  `story-repo-scout` rather than asking the user to speculate. Ask the user
  only when they are the authoritative source or control the required access.
- `[Decision]` sharp choice - `Owner`, `Prerequisite`, `Next action`, and an
  evidence-backed `Recommendation` or `None`. A recommendation is not an
  accepted answer unless the decision owner explicitly delegates it.
- `[Not yet specifiable]` in-scope area - `Owner`, unresolved `Prerequisite`,
  and `Next action` that could make the question sharp. Do not fabricate a
  question or pre-slice this area.

## Artifact State Contract

Begin every produced or revised pipeline story artifact with:

~~~markdown
Artifact Type: Story Card | Split Story Set
Status: Ready | Needs Input | Blocked
Reason: None | <concise readiness reason>
~~~

**Artifact Type** describes shape, not readiness; a split set can be **Ready**.

- **Ready:** clear enough for scouting and planning, with no critical product or
  non-functional decision unresolved.
- **Needs Input:** a named answer, evidence action, or prerequisite resolution
  can make the artifact ready; put the smallest blocking items in Open Questions.
- **Blocked:** a required authority, source, or decision is unavailable, so a
  truthful artifact cannot yet be produced.

Always state **Reason** and every required contract field. Write **None** rather
than omitting an empty field or section.

`Source` is required on Story Cards and Split Story Sets. Use `inline` or
`conversation` when that is the actual source; otherwise preserve each supplied
path, issue URL, external identifier, and version or revision. List multiple
sources without replacing their identifiers with a summary. Use `None` only
when no source is available, and never invent provenance. Use `inherited from
parent Split Story Set` only on a Story Card while it remains nested in that
set. The outer set and an audit identify their concrete source directly; when a
slice is materialized as a standalone card, replace the inheritance marker with
the parent's exact source list.

## Story Card Contract

Use this complete schema for a single card and every materialized slice:

~~~markdown
Artifact Type: Story Card
Status: Ready | Needs Input | Blocked
Reason: None | <concise readiness reason>
Source: <inline | conversation | path | issue URL | external identifier and revision | inherited from parent Split Story Set | None>

## Title
<Short, action-oriented title>

## Intent
Format: User Story | Job Story | Task Brief
<As a ... / When ... / direct brief naming an actor or operating situation,
trigger or need, and desired outcome>

## Feature Definition
<Concrete behavior, trigger or need, any relevant state change, and visible
outcome>

## Acceptance Criteria
- AC-1: <observable pass/fail behavior>
- AC-2: <required boundary or failure behavior>

## Out of Scope
- None

## Constraints
- None

## Dependencies and Assumptions
- Dependencies: None
- Assumptions: None

## Open Questions
- None

## Validation Notes
- AC-1: <test or manual probe for this criterion>
~~~

Use a user story only for a genuine user or stakeholder capability, a job story
for situation-driven behavior, and a task brief for system-to-system,
maintenance, or enabling work. Never invent a persona such as “the system,”
“the database,” or a developer who does not receive the capability.
A task brief does not need literal user-story syntax, but it must name either a
real actor or beneficiary or an operating situation, plus the trigger or need
and desired outcome.

Keep criterion IDs stable when meaning is unchanged and assign new IDs to new
behavior. In a split set, use slice-prefixed IDs such as **S1-AC-1**. Put
required edge, invalid, empty, permission, unavailable, timeout, and retry
behavior in Acceptance Criteria. Validation Notes must cite the criteria they
probe and cannot substitute for required behavior.

## Split Story Set Contract

~~~markdown
Artifact Type: Split Story Set
Status: Ready | Needs Input | Blocked
Reason: None | <concise readiness reason>
Source: <inline | conversation | path | issue URL | external identifier and revision | None>

## Shared Context
- Constraints: None
- Dependencies: None
- Assumptions: None
- Out of Scope: None
- Open Questions: None

## Slice Order
1. S1 - <first shippable outcome and why it comes first>

## Slice Dependencies
- S1:
  - Blocking slices: None
  - External prerequisites: None

## Story Slices
### S1 - <title>
<Complete Story Card contract with S1-prefixed criterion IDs>

## Deferred Work
- None
~~~

Do not replace materialized slices with abbreviated bullets. Give every
materialized slice exactly one `Slice Dependencies` entry with separate
`Blocking slices` and `External prerequisites`. Reference only declared slice
IDs, reject cycles and unknown IDs, and keep `Slice Order` topological. This
section declares gates; it does not claim they are currently satisfied. The
orchestrator owns current satisfaction evidence and derives the executable
frontier when selecting a slice. A split set cannot be **Ready** with an
invalid or incomplete dependency graph.

Derive the set status from shared context and its slices: **Ready** requires
every materialized slice to be ready; otherwise use the most severe applicable
status.
When nesting a complete Story Card beneath a slice heading, shift its internal
Markdown heading levels as needed so they remain children of that slice while
preserving every heading label, field, and section order.

Split first by a demoable, independently verifiable vertical workflow or state
outcome, then by business rule, permission, data variation, or external
dependency. Each slice must remain demonstrable and verifiable once its listed
dependencies are satisfied. Use a discovery task brief when an unknown must be
resolved before delivery. Do not split by frontend, backend, database, or setup
layer unless that technical slice is itself the smallest honest deliverable.

Keep boundary categories distinct: `Deferred Work` is defined in-scope behavior
deliberately postponed beyond the materialized slices; `Out of Scope` is
excluded from this effort and never enters the dependency graph; `[Not yet
specifiable]` is in scope but cannot become a slice or deferred commitment until
its prerequisite makes the question sharp. Record an item in only one category.

## Ready and Ambiguity Rules

An artifact is **Ready** only when:

- the chosen intent names a real actor or beneficiary or an operating situation,
  plus an explicit trigger or need and desired outcome;
- required behavior, any relevant state change, and the observable result are
  explicit;
- criteria give observable pass/fail oracles for required success and failure
  behavior;
- all contract fields are present, supplied constraints are preserved, and no
  hidden or critical unknown remains; and
- every material claim is supplied or verified, every material decision is
  accepted by its owner or explicitly delegated, and no material `[Not yet
  specifiable]` area remains.

Replace terms such as “fast,” “simple,” “secure,” “easy,” “correct,” and
“handles errors” with a measurable oracle or an open question. Unknown critical
performance, security, privacy, accessibility, compliance, availability, or
data-loss requirements prevent **Ready**; never demote them to assumptions.
An unanswered sharp question stays `[Decision]` even when its owner is currently
unavailable; an area stays `[Not yet specifiable]` only while an unresolved
prerequisite prevents a precise question. Neither is `Out of Scope`, and either
prevents **Ready** when material. A material `[Fact]` remains non-ready until its
claim is verified from an authorized source or supplied by its authoritative
owner.
Keep criteria independent of UI, API, storage, or architecture unless that
surface is required. Flag contradictions and split multiple independent
workflows, personas, triggers, or outcome branches that lack one coherent
outcome.

## Audit Output

For **Audit**, emit an audit report without presenting the findings as a
replacement Story Card or Split Story Set:

~~~markdown
Artifact Type: Story Audit
Status: Ready | Needs Input | Blocked
Reason: None | <concise assessed-readiness reason>
Assessed Artifact Type: Story Card | Split Story Set | Unstructured Story Input
Source: <inline | conversation | path | issue URL | external identifier and revision | None>

## Audit Findings
- <severity> | <section or AC ID> | <problem> | <smallest corrective action>

## Questions
- None
~~~

`Status` and `Reason` assess the source's readiness using the common family
meanings; they do not describe whether the audit report was successfully
written. Use `Unstructured Story Input` when the source does not conform to a
pipeline artifact shape, and identify the assessed source without inventing
provenance. Check ambiguity, contradiction, testability, failure behavior,
scope coupling, and lost constraints. Do not emit a replacement artifact unless
the request also asks for rewrite, tighten, or split.

## Composition Boundaries

- `story-clarifier` owns Story Card and Split Story Set semantics; its output is
  consumed by `story-repo-scout`.
- Do not discover or invent repository paths, symbols, or architecture. Preserve
  supplied repository-specific constraints for the scout.
- Use `story-to-plan-orchestrator` when work spans clarification, repository
  scouting, implementation planning, packet resumption, or packet validation.
- Use documentation skills for PRDs and long specifications,
  `tester-mindset` for test strategy, `story-repo-scout` for repository
  evidence, and `story-implementation-planner` for plans. Do not implement
  code with this skill.
