---
name: story-repo-scout
description: Inspect a repository for story-specific implementation evidence, applicable decisions, validation prior art, and bounded planning-critical external primary sources, then produce compact Repo Context. Use for pre-implementation file discovery and greenfield path grounding; use tester-mindset for test strategy and avoid requirements clarification, implementation planning, broad context management, security review, or code changes.
---

# Story Repo Scout

Turn a searchable change request into evidence-backed `Repo Context`. This skill
owns that artifact; it does not clarify product intent, design the solution, or
implement the change.

## Required Input

Accept a story card, ticket, issue, acceptance criteria, or rough request when
it provides at least one distinctive search anchor, such as an observable
behavior, domain term, route, command, UI label, error, config key, data field,
or known symbol. A complete story card is useful but not required.

When the input names a path, issue, or URL, treat that source as part of the
input rather than relying on its title or excerpt. Read the full accessible,
authorized body plus material comments and linked decisions. Record its stable
identifier and exposed revision, update time, or commit. If access is partial
or unavailable, record the exact gap and its planning consequence.

If the intended behavior is too ambiguous to establish a search boundary, use
`story-clarifier`. If repository access or every available input lacks a
searchable anchor, return a truthful non-ready artifact instead of guessing.

## Workflow

1. **Establish scope.** From the required input, identify the repository,
   likely workspace or component, requested change, search anchors, and
   provenance or access gap.
2. **Read governing instructions and decisions.** Inspect the applicable root
   and nested `AGENTS.md` files or equivalent repository policy before drawing
   boundaries. As candidate paths emerge, read any more-specific instructions
   that govern them. Follow relevant current domain glossaries, ADRs, and design
   decisions, including supersession links. Record each item's exact scope,
   status, and planning consequence. A decision record is a hard boundary only
   when its authority, current status, and scope establish one; do not treat all
   ADRs or design notes as do-not-edit rules.
3. **Map the repository cheaply.** Use a fast file listing such as `rg --files`
   when available, then inspect enough root docs, manifests, workspace
   definitions, directory structure, and repository metadata to understand how
   the project is organized. Discover the layout generically; do not assume a
   language, build system, or fixed set of workspace directory names.
4. **Search evidence-first.** Search exact anchors and their path or naming
   variants, then follow imports, registrations, callers, tests, docs, config,
   schemas, history, or neighboring conventions only where observed evidence
   points. Tests may be early anchors when their names or assertions express
   the requested behavior; do not defer them to a final pass.
5. **Inspect every candidate.** Include an existing path only after inspecting
   its content or directory listing for support. Record the observed symbol,
   route, assertion, key, phrase, ownership rule, or structural convention. A
   filename alone is not evidence.
6. **Classify useful evidence.** Give each existing path a role, planning
   priority, reason, and evidence strength. Docs, generated sources, vendored
   code, fixtures, and migrations are legitimate when their role matters;
   distinguish source-of-truth, generated-output, ownership, and integration
   roles rather than rejecting categories wholesale. Apply the external-
   evidence contract below to bounded planning-critical claims.
7. **Ground greenfield paths.** When the change needs a file that does not yet
   exist, list it under `Proposed Paths`, never as existing evidence. Support it
   with an inspected parent directory, sibling pattern, manifest, registration
   point, or documented convention. If no such basis exists, state the missing
   decision as an open question instead of inventing a path.
8. **Separate boundaries from distractions.** Treat a path as an
   `Authoritative Constraint / Do Not Edit` only when a user instruction,
   applicable repository policy, ownership rule, source-generation rule, or
   similarly authoritative source establishes that boundary. Put tempting but
   apparently unrelated paths in optional `Nearby Non-targets`; do not turn
   scout inference into a hard constraint.
9. **Reconcile language and classify gaps.** Surface material conflicts between
   request terms and repository terms, behavior, or structure. Do not silently
   rewrite the request to match the code. Label inspectable evidence work as a
   `[Fact]` action and resolve it through authorized inspection; never ask the
   user to speculate about a repository fact the scout can inspect. Label an
   authority choice as a `[Decision]` question and name its owner. When a
   material fact cannot be inspected, record the access or evidence gap and
   make the artifact non-ready.
10. **Stop on diminishing returns.** Keep evidence that changes where an
    implementer would read, edit, add, or validate. Do not target a model-based
    path quota, summarize whole files, or keep collecting equivalent weak hits.
11. **Write idempotently.** Return an appendable artifact. When the user asks
    to update a source file that already contains `Repo Context`, replace that
    artifact in place while preserving surrounding content; never append a
    second copy.

## Artifact Contract

Start every output with this common header:

```markdown
Artifact Type: Repo Context
Status: Ready | Needs Input | Blocked
Reason: None | <concise readiness reason>
```

Always include all three fields. Use `Reason: None` for `Ready`; otherwise name
the input, access, or evidence gap that prevents readiness.

Status reflects whether the artifact can support honest planning, not how many
files were found:

- `Ready`: the search produced enough existing evidence and, when needed,
  grounded proposed paths for a planner to proceed without inventing context.
  Any open repo questions are explicitly non-blocking to planning, and every
  material external claim has applicable primary-source support.
- `Needs Input`: scouting produced a useful partial or no-hit result, but a
  named answer, scope decision, or additional repository evidence is required
  before planning because an unresolved unknown affects paths, authoritative
  boundaries, or planning feasibility.
- `Blocked`: scouting could not be performed truthfully because required
  repository or planning-critical primary-source access, readable inputs, or
  search capability was unavailable.

A `Ready` artifact may contain `Open Repo Questions` only when every question
is labeled non-blocking and states why planning can proceed without its answer.
If an unresolved question could change path selection, an authoritative
boundary, or whether a plan is feasible, use `Needs Input`; use `Blocked` when
the required input, repository access, or search capability is unavailable.

Apply these presence labels to every Repo Context section. Keep the output
headings exactly as shown in the template.

| Section | Presence | Rule |
|---|---|---|
| Scope and Instructions | Required | Always record the input basis, searched scope, and applicable scoped instructions. |
| Search Record | Required | Always record anchors, the evidence trail, and material gaps or negative results. |
| Existing Evidence | Required | Always include; an honest empty section is valid only for a no-hit, non-ready result. A Ready greenfield result records its inspected convention basis here. |
| External Evidence | Conditional | Include only for planning-critical, story-specific external claims supported by an owning primary source. |
| Proposed Paths | Conditional | Include only when one or more new paths are proposed from an inspected basis. |
| Documented Validation | Conditional | Include when trusted repository evidence identifies analogous tests, an observable seam, a documented command or probe, or other relevant prior art. |
| Authoritative Constraints / Do Not Edit | Required | Always include; write `None identified` when no authoritative boundary exists. |
| Nearby Non-targets | Optional | Include only when an attractive but unrelated lead would otherwise distract planning. |
| Open Repo Questions | Conditional | Include only when unresolved repository questions remain; apply the readiness rules above. |

Use this structure, omitting conditional or optional sections only when their
stated inclusion condition does not apply. When
`story-to-plan-orchestrator` embeds the artifact in a Preparation Packet, it
may shift internal Markdown heading levels by one while preserving every
heading label, field, and section order:

```markdown
Artifact Type: Repo Context
Status: Ready
Reason: None

## Scope and Instructions
- Input source and revision: story, ticket, criterion, or request identifier; revision when exposed, otherwise `no stable revision exposed`, or the exact access gap.
- Repository scope: repository, workspace, package, or component searched.
- Applicable instructions: source path and the scoped rule that affects this work.
- Domain language and decisions: glossary, ADR, or design source; current status, exact scope, and planning consequence.

## Search Record
- Anchors: concrete terms and variants searched.
- Evidence trail: short note on the passes or relationships followed.
- Gaps: searches that produced no useful hit and plausible next leads.

## Existing Evidence
| Role | Priority | Path | Observed Evidence | Why It Matters | Evidence Strength |
|---|---|---|---|---|---|
| behavior owner | Primary | path/to/file.ext | Opened symbol, route, assertion, key, phrase, or rule. | Planning consequence. | Direct |

## External Evidence
| Evidence ID | Claim | Owning Primary Source and Section | Applicable Version/Date | Planning Consequence |
|---|---|---|---|---|
| EXT-1 | Planning-critical API, specification, vendor, or platform fact. | Stable source and owning section. | Version, effective date, or retrieval date when no version exists. | Constraint, compatibility consequence, or validation implication. |

## Proposed Paths
| Proposed Path | Intended Role | Existing Basis | Why It Is Plausible |
|---|---|---|---|
| path/to/new_file.ext | test or implementation role | Inspected path or convention from Existing Evidence. | Planning consequence. |

## Documented Validation
| Evidence Type | Source | Observable Seam or Behavior | Prior-Art Basis and Limits |
|---|---|---|---|
| analogous test, observable seam, or documented command/probe | Inspected path and symbol, or sourced command | Behavior the evidence can observe | Convention it supports and what remains undecided |

## Authoritative Constraints / Do Not Edit
- `None identified`, or path/scope: authoritative source and boundary reason.

## Nearby Non-targets
- path: why it is an attractive but currently unrelated lead.

## Open Repo Questions
- `[Fact][Non-blocking]` evidence action: source to inspect and why planning can proceed meanwhile.
- `[Decision][Non-blocking]` owner and authority question: why planning can proceed without the choice.
```

For `Needs Input` or `Blocked`, label each readiness-affecting question
`[Fact][Blocking]` or `[Decision][Blocking]`, state its planning consequence and
required resolution, and align the header `Reason` with that gap. A Fact entry
is an evidence action, not a request for the user to guess; ask the user only
for missing access or a source they control. A Decision entry asks the named
authority to choose.

Use roles such as entry point, behavior owner, interface, schema, migration,
configuration, test, fixture, documentation, generated output, vendor
integration, or validation source. Use priority `Primary`, `Supporting`, or
`Context` according to planning value.

Evidence strength is local to each inspected path:

- `Direct`: content explicitly owns, exercises, configures, or documents the
  requested behavior.
- `Indirect`: content establishes a dependency, registration, boundary, or
  convention that materially constrains the change.
- `Speculative`: inspected content provides a plausible lead, but the
  relationship remains unconfirmed. State the gap and do not make a
  speculative path critical without a follow-up.

For `External Evidence`, cite the source that owns each claim, not a secondary
summary of it. Record the applicable version or date and the specific section
that supports the claim. Give each row a stable `EXT-*` ID so downstream plans
can cite it without copying the claim, URL, and version. If authoritative
sources conflict, or the repository targets a version different from the
available source, keep the conflict visible and use a non-ready status when it
could change the plan.

For a partial or no-hit result, keep the searches tried, useful negative
evidence, inspected conventions, and next leads. An empty `Existing Evidence`
section is honest only for a non-ready no-hit result; a fabricated row is not.
A grounded greenfield result may be `Ready` when no implementation file exists,
but it must record at least one inspected parent, sibling, manifest,
registration point, or documented convention in `Existing Evidence` and cite
that row from each `Proposed Paths` entry.

Keep `Authoritative Constraints / Do Not Edit` and write `None identified` when
no authoritative boundary exists. `Nearby Non-targets` is optional and must
not be promoted into a constraint by the planner or orchestrator.

`Documented Validation` records available evidence, not a selected test
strategy. Capture analogous tests, the behavior or seam they observe, commands
or probes documented by trusted repository sources, and the precise prior-art
basis and limits. Leave test-level, sequencing, and validation-strategy choices
to `story-implementation-planner`.

## Read-Only Boundary

- Use read-only repository inspection while scouting. Access external primary
  sources only when the story-specific lookup is authorized and available.
- Do not run install, build, test, migration, generator, formatter, or
  application commands. You may record commands found in trusted repository
  docs or manifests without executing them.
- Do not edit code or repository configuration. The only permitted write is
  replacing or adding the `Repo Context` artifact when the user explicitly
  asks for that file update.
- Do not create a separate research note or authenticate to gain new access
  unless the user separately authorizes that side effect.
- Never invent files, symbols, commands, policies, or repository structure.

## Composition Boundaries

- Use `story-clarifier` when product behavior, acceptance criteria, or story
  boundaries are the primary unknowns. This scout can start from any searchable
  input and does not require a fully formatted story card.
- Use `story-implementation-planner` after `Repo Context` is ready. The planner
  owns solution steps, file dispositions, sequencing, executor adaptation,
  risks, and validation design.
- Use `story-to-plan-orchestrator` when the request spans clarification,
  scouting, planning, packet resumption, or cross-stage validation. The
  orchestrator coordinates transitions; this skill remains the source of truth
  for the `Repo Context` contract.
- Use `context-engineering` for context packets, retrieval strategy, context
  rot, or long-running handoffs; use this skill to find story-specific
  repository evidence.
- Use `tester-mindset` when the requested artifact is validation strategy,
  coverage judgment, or oracle design; this skill only records existing
  validation seams and prior art for the planner.
- Use `security` when exploit analysis, threat modeling, or security posture is
  the primary task. Ordinary repository scouting for an auth-related story does
  not by itself become a security review.
- Use the relevant implementation guidance when the user wants code or other
  repository changes rather than a pre-implementation evidence artifact.

## Completion Check

Before returning, verify that every existing path was inspected, every proposed
path has an inspected basis, the full accessible supplied source and any
exposed revision were recorded, lack of a stable revision was stated when
applicable, relevant current language and design decisions have their scope and
status, every material external claim has version-appropriate primary evidence,
validation prior art is evidence rather than selected strategy, Fact actions
were not delegated to user speculation, hard boundaries have authoritative
support, status matches downstream usability, and no execution or
implementation side effect occurred.
