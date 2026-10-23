---
name: gz-design
persona: main-session
description: Use for "design X", "let's design", "brainstorm X" or "I want to build X"; a dialogue that produces ADR artifacts.
category: adr-lifecycle
metadata:
  skill-version: "1.9.1"
  govzero-framework-version: "v6"
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
model: opus
---

# gz-design

Collaborative design dialogue that exits into GovZero artifacts — not superpowers specs, not flat plans.


> **Self-Escalation (opus-tier).** The dialogue with the operator stays in the main session: a subagent cannot ask the operator a question or hear the answer, and what the operator adds is this skill's primary input. When the session model is below opus-tier, you may spawn an `Agent` with `model="opus"` for a bounded drafting or QC track that needs no operator input — pass the operator's words verbatim and the relevant context (ADR IDs, OBPI IDs, prior decisions), and treat what it returns as a draft you verify, not as the operator-facing result.

### Common Rationalizations

| Thought | Reality |
|---------|---------|
| "The user already knows what they want, just code it" | Design dialogue surfaces constraints, alternatives, and consequences the user hasn't articulated. Skipping it ships unexamined decisions. |
| "This is a small feature, it doesn't need a design phase" | Small features that skip design produce ADRs with weak rationale. The interview forcing functions are proportional to complexity. |
| "I'll create the ADR now and refine the design during implementation" | Design refinement during implementation is scope creep. The ADR captures the decision before code exists. |
| "The pool has a similar idea, I'll just implement that" | Pool ADRs are stubs, not designs. Promote or supersede -- don't treat a stub as a spec. |
| "The user said 'let's design X' but I can see the answer is obvious" | Your obvious answer lacks the user's context. One question at a time surfaces what you don't know. |

### Red Flags

- Agent writes implementation code during the design skill
- Multiple clarifying questions bundled into a single message
- ADR booked without user approval of the design
- No overlap check against existing pool ADRs and in-flight ADRs
- gz-adr-evaluate skipped after ADR creation
- Agent writes to `docs/superpowers/` (removed surface)

---

## Persona

**Active persona:** `main-session` — read `.gzkit/personas/main-session.md` and adopt its behavioral identity before executing this skill. You are a skeptical design partner, not a compliant note-taker. Lead with your recommendation. Push back on unstated assumptions. One question at a time surfaces what you don't know.

## Work order (operator ruling, verbatim canon)

- Work feature ADRs in ascending semver order: the lowest version with unlanded OBPIs is in flight. Do not work, author, or recommend a higher feature ADR ahead of it. The campaign selects work but cannot override that order. If campaign sequencing conflicts, semver governs; surface the conflict to the operator rather than silently resolving it. “One feature at a time” does not authorize swapping the order. An ADR in flight may be revised to take more OBPIs. The revision updates the document (an Intent amendment, a Decision item, a checklist item and the scorecard baseline) and the briefs table in the same change. A Validated ADR is not revised: scope missed from one enters the in-flight ADR as a repair assignment that cites the obligation it repairs. An item off the ADR's theme is labelled as such in the Intent amendment. The (m)ADR is a stopgap: a release-increment bucket, meant to be thematically cohesive. Its successor is a feature bundle between an enhancement proposal and a feature specification. Names are chosen later. This replaces the exception of 2026-09-29 (GHI #871), by which a correction to a Validated ADR took the next unallocated feature semver and could be worked ahead of the in-flight ADR; that route is retired (operator rulings 2026-10-04: 'the new loosening law here is we need to be able to revise an adr to allow for more obpis - the document and briefs table gets updated'; 'A, in-flight only'; the wording and the retirement, each 'A').

> Carried verbatim from root `AGENTS.md` § Operator Doctrine on 2026-09-17 (GHI #921), and into this skill on 2026-09-24 (GHI #1091, sweep finding S06): the ruling governs authoring and recommending, not only working. The corpus `.gzkit/corpus/AGENTS.md.jsonl` keeps the ruling's history.

## Hard Gates

- **DO NOT** write to `docs/superpowers/` — that surface is removed from this project.
- **DO NOT** invoke `superpowers:writing-plans` or `superpowers:executing-plans`.
- **DO NOT** write any implementation code during this skill.
- **DO NOT** book an ADR until the design is approved by the user.
- All artifacts land in GovZero structures: pool ADRs, canonical ADRs, OBPI briefs.

---

## Process

```
Explore context → Clarify (one question at a time) → Propose approaches →
Present design → User approves → Book artifact → gz-adr-evaluate → Hand off
```

### Step 1: Explore Context

**Pre-flight — defect-fix routing.** Apply `AGENTS.md` § Defect-fix routing before scaffolding anything: a GHI authorizes direct repair outright, and without one a small in-flight fix (about ten source lines or two files, one surface, a unit test covers it) is a direct `fix(<scope>): …` commit, not an ADR. Default-to-ceremony for small in-flight defects is the exact over-application pattern GHI #195 authored the routing rule to prevent.

Before asking anything, read the current state:

```bash
uv run gz status --table
uv run gz state --json
```

Also check:
- Any existing pool ADRs related to the topic (`docs/design/adr/pool/`)
- Any in-flight ADRs that overlap
- Relevant source files if the design touches existing code

### Step 2: Clarify — One Question at a Time

Ask questions to understand purpose, constraints, and success criteria.
- One question per message. Never bundle.
- Prefer multiple-choice when the answer space is bounded.
- Stop when you can propose approaches with confidence.

**Anti-patterns that trigger a rephrase:**
- "What do you want X to do and how should it integrate and what's the priority?" → split into three turns.
- Asking about implementation details before intent is clear.

### Step 3: Propose 2–3 Approaches

Present options conversationally with trade-offs. Lead with your recommendation and why.
Each approach should be nameable in 3–5 words.

**Rejected alternatives are required, not optional.**

The chosen approach alone is indistinguishable from a reconstruction of a
destination already picked. Record, for each design, the approaches that
were considered and rejected, with the concrete reason each was rejected.
Interpretability reference: Lindsey et al. 2025, rhyme experiment — a model
that only writes its chosen word is not distinguishable from a model that
picked it first and wrote the line backward.

The ADR authoring step must carry the rejected alternatives into the ADR's
Alternatives Considered section. Empty or cosmetic rejected-alternatives
lists (e.g., "no other options considered") are themselves a failure
signal and should prompt a redesign pass.

### Step 4: Present Design

Section by section, get approval after each:

1. **Command/API interface** — what the user/agent sees
2. **Check pipeline or data flow** — what it does internally
3. **Data model** — Pydantic models, key fields
4. **Output and rendering** — stdout, `--json`, exit codes
5. **Extension points** — future ADRs this will consume or produce

Scale each section to its complexity. Short sections for obvious choices; 200–300 words for nuanced ones.

### Step 5: Book the Artifact

After design approval, ask:

> "Is this ready to book as a canonical ADR, or park as a pool entry for later prioritization?"

**Pool ADR** (idea not yet scheduled):
- Invoke `gz-adr-create` targeting the pool
- Produces `docs/design/adr/pool/ADR-pool.{slug}.md`
- No OBPI briefs yet — pool entries are stubs
- No odometer bump

**Canonical ADR** (ready to implement):
- Confirm: next available ADR semver (check `uv run gz status --table`)
- Confirm: lane (Lite = Gates 1–2; Heavy adds Gate 3 docs and Gate 4 BDD; Gate 5 attestation is universal — every lane, ADR-0.0.36)
- **Confirm: kind (feature/pool).** Feature = release-carrying capability (`0.y.z` and up). Pool = backlog awaiting promotion. **`foundation` is CLOSED for gzkit authoring (ADR-0.34.0 Foundation Sunset)** — `gz plan create --kind foundation` and `gz adr promote --kind foundation` are rejected at the command layer, so do not offer it. The kind remains open for **adopter projects**, whose `gz init` scaffolds it available; when running this skill in an adopter repo, use the invariance test to resolve the edge cases: *"Foundation = without it, we wouldn't be doing the project."* The hexagonal-ports lens clarifies: **ports point to invariance; adapters are features**. See `docs/user/concepts/foundation-feature-invariance-test.md` for worked examples and anti-patterns, and `docs/governance/hexagonal-architecture.md` for Cockburn's source and gzkit's port/adapter mapping.
- Invoke `gz-adr-create` with semver, slug, lane, and OBPI count
- OBPIs are co-created with the ADR — never deferred
- Design content from this conversation populates the ADR's Intent, Decision, Alternatives Considered, and Consequences sections

### Step 6: Quality Check

After the ADR is written, invoke `gz-adr-evaluate` on it:

```
/gz-adr-evaluate ADR-X.Y.Z
```

Any dimension scoring 1 must be revised before proceeding.

**Pool ADRs are exempt.** `gz adr evaluate` resolves an ADR *package*
(canonical/feature/foundation directory structure); a pool ADR is a flat
stub file with no package and no OBPIs yet, so the CLI errors if invoked
on one. The evaluate gate fires at **promotion** (`gz adr promote` builds
the package), not at pool authoring. Skip this step for pool ADRs.

### Step 7: User Reviews

Ask the user to review the booked ADR file before proceeding:

> "ADR booked at `docs/design/adr/<kind-dir>/ADR-{id}-{slug}/`. Please review it and its briefs and confirm before we close the design."

### Step 8: Hand Off

Once the user approves:

- **Pool ADR**: done. No further action. Pool entries are promoted via `gz-adr-promote` later.
- **Canonical ADR**: done. Its OBPI briefs were co-created in Step 5; use
  `gz-obpi-specify` only to finish authoring a brief that is still thin. The
  operator initiates each OBPI through `gz-obpi-pipeline` — this skill does not.

Do NOT invoke any implementation skill. A booked, evaluated, reviewed ADR is the
terminal state.

---

## ADR vs Pool Decision Heuristics

| Signal | Book canonical ADR | Park as pool |
|--------|-------------------|--------------|
| Next OBPI is known | ✓ | |
| Depends on in-flight ADR not yet complete | | ✓ |
| Lane is clear | ✓ | |
| Scope is still fuzzy | | ✓ |
| User says "let's do this now" | ✓ | |
| User says "capture this for later" | | ✓ |

---

## Overlap Checks (Always Run)

Before proposing any design, verify there is no existing ADR (pool or canonical) that already covers the intent:

```bash
uv run gz status --table
ls docs/design/adr/pool/
```

If overlap is found, surface it explicitly:
> "ADR-pool.{slug} already covers part of this — do you want to extend it, supersede it, or scope this as a separate concern?"

---

## Key Principles

- **One question at a time** — never bundle clarifying questions
- **Design lives in the ADR** — not in separate spec files
- **OBPI co-creation is mandatory** for canonical ADRs — never deferred
- **Pool entries are stubs** — design detail goes in canonical ADRs, not pool files
- **gz-adr-evaluate is not optional** — it catches weak intent before implementation begins
- **YAGNI** — remove scope that isn't needed for the current decision
