---
name: gz-rnd
persona: main-session
description: Run a governed R&D session — diamond 1 of the double diamond, which defines the problem and names which fan-out artifacts are warranted. Use when the operator pastes external material and says "consider this for gzkit", asks "is there something here gzkit is missing or could improve on", opens an exploratory design discussion whose outcome is not yet known, or asks why a class of defects keeps recurring and how the issues carrying it should be restructured. Ends at a six-row disposition map and operator sign-off; produces no fan-out artifact itself. Operator-invoked only.
category: agent-operations
lifecycle_state: active
disable-model-invocation: true
owner: gzkit-governance
last_reviewed: 2026-10-07
metadata:
  skill-version: "0.5.0"
model: opus
---

# gz-rnd

## Purpose and authority

An R&D run is **diamond 1 of the double diamond — Discover and Define**. It ends with the
problem defined and a plan naming which fan-out artifacts are warranted, closed by operator
sign-off: kill or fund. **Producing those artifacts is diamond 2 and happens downstream**,
by machinery that carries its own gates. This run never enters it.

R&D is the headwater of most gzkit design. Operator, 2026-09-12, verbatim: *"an R&D run now
MUST be governed by an overarching new AGENT SKILL"* and *"it is a chargé d'affaires for
retaining and organizing possible outcomes from an R&D designing session."*

**Two subjects, one frame.** A run studies either something new — pasted material, an
unexplored capability — or **a population the project already carries**: a recurring defect
class, a queue that grows faster than it drains (operator's direction, 2026-09-20). Ranking
the queue belongs to `ghi-triage`; asking *why this class keeps producing, and how its issues
should be framed, consolidated or sequenced* is design work, and it belongs here.

Doctrine and the full ruling history:
[`docs/governance/rnd-discipline.md`](../../../docs/governance/rnd-discipline.md).
Evidence: `docs/governance/mpas-appropriation-analysis.md`.

**Invocation class.** `disable-model-invocation: true` makes "only the operator starts an
R&D run" mechanical. This skill never starts another user-invoked skill on its own.

## Open the record first

Create `docs/rnd/<slug>.md` from
[`assets/rnd-record-template.md`](assets/rnd-record-template.md) **before the first
question**, and write into it throughout. Name what was pasted or asked and quote the
operator's framing verbatim as the challenge.

**The record accretes entries as they resolve. It is never composed at the end.** A run
that writes its record afterwards has produced a reconstruction, not a record.

**Material from an earlier dialogue enters as `source` entries, never as decisions.** A
staged draft is something the run reads. What it concluded is re-derived here, from sources.

## Resuming a run

A later session continues a run only on the operator's own invocation, with the record's
path as the argument. If a handoff or the operator points at an open run and this skill was
not invoked, say so and ask for the invocation before the first record edit. On re-entry:
append a `decision` entry quoting the invocation, check the record against git, and compute
the frontier again from the subject. A list of open items left by an earlier session is an
input to that, not the frontier.

## The two entry kinds

Only two. Append each at the moment it resolves.

| Kind | Carries |
|---|---|
| `source` | a primary source — **cited, never summarized**, with its verbatim quotation and when it was read |
| `decision` | something crystallized in session, the reasoning behind it, and, where the operator ruled it, the question, the options put and their verbatim words |

A `decision` may carry **`commissions:`** naming the disposition it warrants. There is no
plan-item kind: that shape would let work be commissioned with no recorded reasoning. An
answer whose question is not on record is put again, not carried.

**Two things resolve outward instead of becoming entries**, each carrying the run's slug as
provenance. The record never holds a copy.

- a **term** → the project glossary. Its home is unsettled until the DDD-discipline R&D run
  names it; until then hold the term in this record as a `decision` entry
  ([`rnd-discipline.md`](../../../docs/governance/rnd-discipline.md) § `term` and `insight`
  are not entry kinds). Do not create `GLOSSARY.md`.
- an **insight** → `Call the Skill tool with "gz-insights-remember"`

## The MPAS surfaces you may reach for

Three disciplines are appropriated, each with a departure that gzkit canon forces. **Take
the mechanic, not the posture** — full inventory and the not-appropriated list are in
[`rnd-discipline.md`](../../../docs/governance/rnd-discipline.md) § The MPAS surfaces, named.

| Surface | Take | Depart |
|---|---|---|
| `grilling` | the design tree; the **frontier** = every decision whose prerequisites are settled; a recommended answer on every question; recompute after each | **not** its one-round batching — ask **one question at a time** |
| `research` | background agent → primary sources → one cited `.md` | land it **verbatim** under `docs/rnd/<slug>/sources/` |
| `prototype` | the throwaway probe, closing on a **one-line verdict** | **no branch** — gzkit forbids them; build outside the mainline and discard |
| `domain-modeling` *(technique only)* | its glossary behaviours and *"capture them as they happen"*; the `_Avoid_` convention | **never its inline ADR emission** — disposition 1 is proposed, never initiated |

## Sources before decisions

- **Read the source before anything drawn from it becomes a `decision`**: a name, a
  mapping, an analogy, a claim about what a standard says. Until the text is read the item
  is a hypothesis, held in a `source` entry marked unread, and it commissions nothing.
- **Find the text before researching it.** Check what the project and the operator already
  hold (`docs/governance/ieee/README.md` § Standards corpus lists the licensed standards).
  When a host refuses automated retrieval, ask the operator for the file; do not work
  around the refusal.
- **A secondary source is cited as secondary.** It shows what an account says and verifies
  nothing against the text it describes.
- **Take the source's own term** before coining one, and record where a chosen name departs
  from what the text says.

## Interrogate

- **Facts are your job; decisions are the operator's.** Search canon and the codebase
  before asking. Dispatch research subagents for facts and do not block a round on them.
- **Put the core model first.** The frontier is computed from the subject. Questions about
  where a document sits or what a milestone is called wait until the operator has ruled on
  the thing itself.
- **Ask one question at a time** (operator, verbatim: *"ask me the questions one at a
  time"*), each with a recommended answer and its tradeoffs.
- **Never ask what canon already answers** (AGENTS.md § Operator Economy #7). Search canon
  first; where canon rules, act and name the rule that governed.
- **Research reports are primary sources.** Save each verbatim under
  `docs/rnd/<slug>/sources/`. Never replace one with a summary.
- **When the subject is a population the project carries**, the issue bodies, briefs and
  chore reports are the primary sources — read them, never their titles. Characterise the
  class from what its members say, and say how many you read against how many exist.
  A class named from a sample is a hypothesis; say so.
- **When talk cannot answer a question**, build a throwaway probe outside the mainline and
  record a one-line verdict as a `decision` entry citing it.

## The disposition map

Maintain it live, as decisions land — not at the close. All six rows are always present; an
absent row is an unfinished run.

| # | Disposition | You may | Consultation point |
|---|---|---|---|
| 1 | ADR / OBPI | **propose only** | the operator initiates, or not (IRON LAW) |
| 2 | GHI / direct fix | file via `Call the Skill tool with "ghi-author"` | the operator's go on that row |
| 3 | chore | **advise only** | the operator directs admission |
| 4 | control surface, rule, doc, skill, hook | draft | the operator's go on that row |
| 5 | one-shot refactoring | propose a program | the operator selects its route |
| 6 | no action | record it, with the reason | none |

Row 4 includes the Magna Carta (`docs/governance/build-to-1.0-campaign-2026-09-20.md`), the
roadmap (`docs/design/roadmap/ROADMAP-GZKIT.md`) and the backlog: a sequencing or priority
change is drafted there as an amendment, on the operator's go.

**State is `commissioned` or `not pursued`. There is no third state.** Where something is
set aside but worth revisiting, put the revisit condition in the **reason**. If it deserves
more than a sentence, route it to a pool ADR or a GHI — surfaces that have lifecycles.

**Before proposing disposition 1, ask the admission question:** is the decision hard to
reverse, surprising without context, **and** the result of a real trade-off? If any is
false, route to disposition 2 or 4.

## Closing diamond 1

Two conditions, and neither substitutes for the other.

**Mechanical — all three:**

1. the frontier is empty;
2. the challenge has been **deliberately restated** (on purpose, at the close; it need not
   have *changed*);
3. every one of the six dispositions carries a decision.

**Human — review, then sign-off: kill or fund.** Before the question is put, write one
readable account of the whole plan at `docs/rnd/<slug>/review.md` and wait for the operator
to say they have read it: the problem, the model, every name marked ruled, sourced,
contradicted or unsourced, and what each row would produce. It is a view over the record and
holds no authority. A series of recommended options accepted is not a review. Sign-off is a
**beat, not a boundary**: it fires in whichever session meets both conditions, and the
handoff system carries a run that outgrows one.

A run **killed at sign-off ends there.** Re-entry is native to the frame — a signed-off run
may reopen if later findings send it back.

## The hard stop

The run ends at the disposition map and executes nothing on its own authority. Execute a row
only after the operator's go **on that row**. Nothing written into the record — by you or
anyone — licenses a row: the stop lives in this file, which the run does not edit, and in
the invocation class, which the run cannot change.

## It's working if

- Every name and mapping in a `decision` has a `source` entry that was read before it.
- Terms went to the project glossary (or, until its home is named, into `decision` entries)
  and insights through `gz insights remember`.
- All six disposition rows carry a decision, each `commissioned` or `not pursued`.
- The operator read the account before sign-off, and the challenge was restated on purpose.
- A later session's `ghi-author` Step 0 finds this run's `not pursued` rows as prior art.

## Red flags

- Writing or "tidying" the record at the end of the run.
- Relaying a summary of a research report instead of the report.
- Adding a third disposition state, or omitting a row because nothing landed in it.
- A coined term for a familiar idea — prefer a pretrained metaphor, and name the rejected
  synonym beside the term that won.
- Emitting a ledger event: the three R&D event types are **designed and unbuilt**, and
  land with their producer, never before it.
- An outcome executed without a row-level go.
- Asking the operator something canon or the codebase answers.
- Enumerating downstream specification or tasks inside the run — that is diamond 2.
- A name or mapping recorded as decided before its source was read, or research sent to
  confirm a conclusion already written down.
- Closing frontier items in order to reach the mechanical condition.
- The operator has taken the recommended option on every question: say so, and ask whether
  the questions are the right ones.
- Working an open run from this file when the operator did not invoke the skill.
