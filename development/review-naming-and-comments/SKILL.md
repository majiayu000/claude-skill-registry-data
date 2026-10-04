---
name: review-naming-and-comments
kind: skill
status: ready
provenance:
  principles:
  - P004
  - P032
  - P014
  - P002
  claims:
  - C00187
  - C00188
  - C00190
  - C00192
  - C00193
  - C00199
  - C00202
  - C00205
  - C00209
  - C00210
  - C00242
  - C00244
  - C00247
  - C00249
  - C00353
  - C00354
  source_anchors:
  - 5e67c59e0e18-c0002
  - 5e67c59e0e18-c0003
  - aca1f3444508-c0001
  authored_from_digest: 00bfdf88ed04cd67425a4822038dc3a176bc41504cd4f9129f3f4a9b8008c2c2
---

# Review Naming and Comments

## Purpose

Assess the naming and commenting practices within a code artefact systematically, producing
a prioritised list of findings in which the most costly weakness appears first. Each finding
is traced to a governing principle, classified by type, and paired with the smallest bounded
recommendation that would improve clarity without introducing unrelated changes.

Names are the primary communication medium in source code. A name that reveals its holder's
purpose, behaviour, and reason for existence reduces the work a reader must do and diminishes
the need for supplementary comments (PRC-016; clm-043). When a precise, intention-revealing
name cannot be found readily, this is a diagnostic signal: the underlying entity may be
poorly bounded or carry mixed responsibilities — not merely a vocabulary problem (clm-021).

Comments add value only when they capture what code cannot express on its own — design
rationale, intended constraints, units, or the reasoning behind an unusual choice. A comment
that restates what the code already shows adds noise without information, and a comment that
exists to apologise for confusing code is a signal to improve the code rather than keep the
comment (PRC-017; clm-019; clm-047).

## When to use

- A function, class, or module is submitted for review and the team wants a principled
  assessment of whether its names communicate intent clearly.
- Comments in a code artefact are suspected to be stale, redundant, or masking structural
  problems rather than adding genuine information.
- A reviewer has identified a nonobvious code block and wants to determine whether a comment
  or a refactoring is the correct remedy.
- An interface's comments — or absence of them — are preventing a reader from understanding
  the design rationale behind a module's choices.
- The codebase shows inconsistent naming patterns and the team wants an assessment of whether
  this inconsistency is causing measurable cognitive overhead.

## Procedure

### Step 1 — Gather context

1. Identify the artefact type: a single function, a class, a module, or a cross-cutting
   review spanning several files.
2. Note any complexity symptoms already reported: names that have required explanation
   during code review, comments found to be inaccurate, or code that demands deep reading
   before its intent becomes clear.
3. Record the team's established naming and commenting conventions, if any. A local
   inconsistency mandated by an external API may be legitimate; one that has simply drifted
   is not (clm-022).
4. Note the artefact's anticipated lifetime and change frequency; findings in a frequently
   modified long-lived module warrant more urgent action than those in a short-lived
   throwaway script.

### Step 2 — Assess each name for intention-revealing precision

For every significant named entity in the artefact — variables, parameters, functions,
methods, classes, modules, and types — apply the following tests in order:

1. **Purpose test.** Does the name communicate why this entity exists? A reader who sees
   the name alone, with no other context, should be able to form a correct first impression
   of what it is for (PRC-016; clm-043).
2. **Precision test.** Does the name create a clear image? A name so broad it could apply
   to many different things, or so abbreviated it requires decoding, fails this test
   (clm-021).
3. **Hard-to-pick test.** When the reviewer struggles to propose a better name — when no
   precise alternative comes readily to mind — this is a diagnostic signal that the entity
   itself may be poorly bounded or carry mixed responsibilities. Flag the entity and
   recommend clarifying or splitting its scope before attempting a rename (PRC-016; clm-021).

For each name assessed, record one of three dispositions:

| Disposition | Meaning | Action |
|---|---|---|
| **Clear** | The name passes both tests; no change needed | Record as clear and move on |
| **Imprecise** | The name is vague or misleading but the entity is well-defined | Recommend a more precise alternative |
| **Hard to name** | No precise alternative is readily available | Flag as a potential design signal; recommend clarifying or splitting the entity |

Do not flag short conventional identifiers that are idiomatic and locally obvious — loop
indices, universally recognised abbreviations in a narrow domain — unless the convention
has been applied inconsistently.

### Step 3 — Classify each comment

For every comment in the artefact, classify it into one of the types below, then apply
the corresponding action (PRC-017):

| Type | Description | Action |
|---|---|---|
| **Rationale** | Explains why a design choice was made, or why an obvious alternative was rejected | Keep; this is the primary value a comment can add (clm-019) |
| **Intent** | Summarises what a block achieves at a higher level than the code itself | Keep if the abstraction genuinely helps; challenge if better names would make it redundant |
| **Unit / constraint** | Records units, assumed value ranges, or non-obvious invariants | Keep; these cannot be expressed in most type systems without additional tooling |
| **Restatement** | Paraphrases what the code already shows, or explains a block that is confusing because the code is unclear | Remove; first try extracting and naming the block so the code explains itself (clm-047; clm-071) |

When a comment is classified as **restatement**, apply the extract-and-name test before
recommending deletion:

1. Can the confusing block be given its own named function or variable whose name makes the
   comment unnecessary? If yes, recommend the extraction and flag the comment for removal
   (clm-071).
2. If extraction is impractical — for example, the block is a single expression that already
   has a clear name — recommend rephrasing the surrounding code to reduce the need for the
   comment rather than deleting it immediately.

Do not penalise legal headers, licence notices, or comments required by a project-wide
policy; record these as **policy-required** and skip the classification test.

### Step 4 — Check for missing interface comments that hide rationale

Scan the public interface of each function, class, and module. For each interface element,
ask whether a reader can understand its intended contract — what it promises to callers,
what it expects from them, and why it exists — without reading the implementation (clm-019).

When a rationale-bearing comment is absent from a public interface and the implementation
is non-trivial, flag the gap and recommend writing the interface comment before the next
modification to the implementation. Interface-level commenting done as part of design —
written before or alongside the code rather than afterwards — tends to surface design
problems earlier and at lower cost (clm-020). Frame this recommendation as a design act,
not a documentation chore: if writing the interface comment is difficult, the interface
itself may need reconsideration.

### Step 5 — Check obviousness and cognitive load

Review each non-trivial code block from the perspective of a reader unfamiliar with the
local context. Ask: would a competent developer understand this block without needing to
trace execution through multiple files, consult implementation details from a different
module, or hold undocumented assumptions in mind? (PRC-018; clm-023)

Flag any block where the answer is no as **nonobvious**. For each nonobvious block,
determine which remedy is most appropriate:

- **Rename first.** If the block is nonobvious primarily because its name or the names of
  its local variables are imprecise, recommend renaming as the first remedy (PRC-016).
- **Extract and name second.** If the block contains a coherent sub-task not yet given a
  name, recommend extracting it into a named function so the name carries the explanation
  (clm-071).
- **Add a rationale comment last.** Only when the code is as clear as it can reasonably
  be made — and the residual complexity arises from an external constraint, an algorithm,
  or a business rule that cannot be simplified — recommend adding a rationale comment
  explaining the non-obvious aspect (PRC-017; clm-019).

Nonobvious code raises cognitive load directly and can produce unknown unknowns — side
effects or constraints that a reader would not predict from the visible interface — which
are among the most costly forms of complexity (clm-023).

### Step 6 — Check naming and commenting consistency

Scan the artefact for inconsistency against the surrounding codebase (clm-022; clm-041):

1. **Naming pattern consistency.** Are similar concepts named with the same vocabulary and
   grammatical form? For example, are boolean accessors consistently prefixed, are event
   handlers consistently verb-noun, are collections consistently plural?
2. **Commenting pattern consistency.** Are interface comments present or absent in a
   consistent manner? Are in-line comments used for the same class of information throughout?
3. **Casing and style consistency.** Does the artefact follow the established conventions
   for identifier casing, abbreviation, and compound-word separation?

For each inconsistency found, record whether it is:
- A **drift** — an unintentional deviation that should be corrected — or
- A **legitimate exception** — a deliberate local departure clearly signposted, for example
  a naming convention imposed by an external API.

Flag drifts as findings. Consistent conventions reduce the cognitive effort of reading a
codebase because a reader transfers what they have learnt in one area to every other area
without re-examination (clm-041; PRC-018).

### Step 7 — Rank findings and compose the critique

Reorder all collected findings on two axes, most costly first:

1. **Cognitive load impact** (primary): Does this finding force a reader to work harder than
   necessary, create unknown unknowns, or slow future modification? Nonobvious code and
   hard-to-pick names that signal a design problem rank highest (clm-023; PRC-001).
2. **Maintenance effort impact** (secondary): Does this finding, if left unaddressed,
   produce ongoing confusion, stale comments, or inconsistency that compounds over time?
   (PRC-002)

Comments that merely restate code rank below naming problems. Naming problems that signal
a needed design split rank above those that require only a vocabulary change.

Assemble findings into the output format described in `## Output`. Open with a one-sentence
verdict naming the single most costly finding, the principle it violates, and a
**proceed / rename-and-refactor / redesign** recommendation.

If no findings are identified after completing Steps 2 through 6, state that the review
was completed across all five check types and no instances were detected. Do not fabricate
findings to fill the output.

## Inputs

| Field | Required | Description |
|---|---|---|
| `artefact` | Yes | The code, interface signatures, or module description to be reviewed |
| `requirements` | Yes | The present known requirements governing the artefact |
| `team_conventions` | No | Established naming, casing, and commenting conventions in the project |
| `observed_symptoms` | No | Reported problems: names needing explanation, comments found inaccurate, code hard to read |
| `lifetime` | No | Anticipated system lifetime; calibrates the urgency of findings |

## Output

A structured review with the following elements, in order:

1. **Verdict line** — one sentence: the single most costly naming or commenting problem
   found, the principle it violates, and a proceed / rename-and-refactor / redesign
   recommendation.
2. **Ranked findings** — one entry per problem, ordered most-costly first. Each entry
   contains:
   - Finding type: name (Clear / Imprecise / Hard-to-name), comment (Rationale / Intent /
     Unit / Restatement / Policy-required / Missing interface), consistency (Drift /
     Legitimate exception), or Nonobvious
   - Location: the specific identifier, comment, or code region
   - Description: what makes this a problem and the cognitive or maintenance cost it imposes
   - Principle(s) violated: cited by principle ID and claim ID
   - Bounded recommendation: the smallest change — rename, extract-and-name, add rationale
     comment, or remove comment — that resolves this finding without introducing unrelated
     scope; no replacement code
3. **Clean-scan confirmation** — an explicit statement that all five check types (naming
   precision, comment classification, missing interface comments, obviousness, consistency)
   were completed, with a note of any area where no problem was detected, so absence is
   recorded rather than assumed.

Suggested names or comment text may be offered as brief illustrative examples, clearly
labelled as suggestions. The output does not include replacement code.

## References

- [`../../references/clean-code-heuristics-summary.md`](../../references/clean-code-heuristics-summary.md) —
  naming heuristics and comment guidelines from the clean-code canon
- [`../../principles/principles.yaml`](../../principles/principles.yaml) —
  PRC-016 (intention-revealing names; vague names as design signals),
  PRC-017 (comments reserved for what code cannot say; extract before commenting),
  PRC-018 (obviousness and consistency as levers against cognitive load)

## Provenance

Authored from distillation-only sources; all content is paraphrased and no verbatim text
is reproduced from any source work.

- **Martin's Clean Code** (clean-code-a-handboo-5b1b9ca3), anchor h0035: intention-revealing
  names communicate purpose, behaviour, and usage, reducing the need for supplementary
  comments (clm-043); anchors h0098, h0099: comments do not compensate for unclear code —
  when the urge to comment arises, first try making the code itself sufficiently clear
  (clm-047).
- **Ousterhout's A Philosophy of Software Design** (a-philosophy-of-soft-5e67c59e),
  anchors h0494, h0506: names should be precise and create a clear image; a name that is
  vague or hard to choose signals that the underlying concept is not cleanly defined
  (clm-021); anchors h0275, h0433: comments should capture what is not obvious from the
  code — rationale, intent, units — not restate it (clm-019); anchors h0524, h0528: writing
  interface comments as part of the design process improves the design and is not
  significantly more costly than adding comments after the code is written (clm-020);
  anchors h0551, h0588: code should be obvious; requiring a reader to work hard to
  understand it raises cognitive load and produces unknown unknowns (clm-023); anchor h0545:
  consistency in names, styles, and patterns reduces complexity by allowing developers to
  reuse what they have already learnt across the codebase (clm-022).
- **Fowler's Refactoring** (martin-fowler-refact-0574f24e), anchor h0156: the impulse to
  comment a block often indicates a structural problem — extract and name the block first so
  the code makes the comment redundant (clm-071).
- **Kanat-Alexander's Code Simplicity** (code-simplicity-the-aca1f344), anchor h0087:
  consistency across a codebase makes it simpler; a reader learns one pattern and applies
  it everywhere without re-examination (clm-041).
- Governing principles: PRC-016, PRC-017, PRC-018.
