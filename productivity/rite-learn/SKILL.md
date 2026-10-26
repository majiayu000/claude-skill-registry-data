---
name: rite-learn
description: Review recurring cross-feature evidence and propose durable project guidance.
argument-hint: "[\"<lesson or rejected direction>\"]"
user-invocable: true
disable-model-invocation: true
---
<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/documentation.md","devrites-lib/reference/standards/tooling.md"],"workspace":["state.md","decisions.md","drift.md","evidence.md","review.md","seal.md","questions.md"],"workspaceByRole":{"retrospector":["state.md","decisions.md","drift.md","evidence.md","review.md","seal.md","questions.md"]},"triggers":{"agents":["devrites-lib/reference/standards/agents.md"]}} -->
> Read-set manifest: `devrites-engine context <slug> --skill rite-learn` (no workspace: `--out <path>`) bundles every file named below into one deduplicated read.

# /rite-learn: review durable lessons

Use reviewed Markdown/native memory, not miners or registries. This proposes maintenance
of one authority; it cannot promote a rule alone.

## Modes

- `/rite-learn` reviews recurring evidence across shipped work.
- `/rite-learn "<lesson>"` evaluates one lesson or rejected direction.

## Workflow

1. Read [durable promotion](../devrites-lib/reference/standards/documentation.md#promote-durable-guidance).
   Before bounding, fixed-string search all of `.devrites/archive/` and active
   `decisions.md` for `rite-learn: accepted` and `rite-learn: declined`; read every hit
   whole. Then bound the archive; inspect applicable `AGENTS.md`/`CLAUDE.md`, accepted ADRs, and relevant `.devrites/archive/*/{decisions,drift,review,seal}.md`.
   Over the same window, collect reverts (`git log --grep='^Revert'`), repeat fixes to the same
   paths, and (when `gh` is authenticated) merged-PR review comments into one scratch excerpt; each is an external signal.
   **Failing case:** a declined proposal returns because its feature fell outside the bound.
2. Broad mode dispatches exact fresh/read-only `devrites-retrospector` with the archive paths and history excerpt; reconcile its claims against cited files.
   A missing, failed, timed-out, or malformed result reports `Candidate: NOT-RUN
   (unavailable: <reason>)` as a gap, never `Candidate: none`; an unavailable role stops
   for HITL per [`agents.md`](../devrites-lib/reference/standards/agents.md) (trigger `agents`).
3. Keep corrections repeated in two features (a `## Carry-forward constraints` rule recurring in two archived `decisions.md` qualifies), a judgement call made twice, or a defect class seen twice; drop one-off preferences, task-specific detail, generic advice.
   Broad mode also proposes **retirements**: a rule found via a `rite-learn: accepted`
   marker whose cited failing case or owner no longer exists in live source, whose
   review-by date passed unverified, or that is a model-default no-op. Zero is valid but
   names the searched scope; a rule still guarding a live failing case is never retired.
4. Verify claims against live authoritative sources; state currentness signal, applies/does-not-apply scope, `unknown` where unverifiable.
   **Research promotion requires:** each external claim carries a dated citation per
   [[`tooling.md`](../devrites-lib/reference/standards/tooling.md) § Research provenance](../devrites-lib/reference/standards/tooling.md#research-provenance-staleness-and-cost).
   **Failing case:** "best practice is X" with no source → reject promotion.
5. Apply durable promotion's recoverability test; search same/contrary rules, choose one existing owner (nearest instruction/standard, ADR, or feature `decisions.md`), and name discovery.
6. Show the exact edit + duplicate/conflict/supersession disposition; update/narrow/replace/retire contradictions; apply only after user approval of exact edits.

## Rules

- Live repository evidence outranks memory; unverifiable is unknown, not false.
- A lesson's premise is graded **established / working / open** with its source
  (retrospector output): only established premises — or working premises whose
  confirming check is named — may be proposed; open premises return as recorded
  assumptions, not lessons.
- Never create a learning ledger/index/queue, score, timeline, or parallel authority; rejected directions return only when evidence changes their rationale.
- A declined lesson persists as a declined decision entry (reason recorded) in the
  nearest owning decisions file **in the same round** — a refusal recorded only in
  conversation or on an unmerged branch is lost and will be re-litigated.
  **Failing case:** the same rejected proposal returns next round because no tracked
  entry exists.
- Every disposition entry carries the fixed marker `rite-learn: accepted` or
  `rite-learn: declined`, its evidence refs, and (accepted) owner path plus a review-by
  date. A later round reuses a matching declined record instead of re-proposing.
- A lesson needs an **external signal** (user correction, failing test/gate, review
  finding) with its source; self-critique or model reflection alone never changes guidance.
- Promotion path is fixed: lesson → artifact type (retrospector class) → one canonical
  owner → human approval of the exact edit. A skipped stage is no promotion.
- **Recurrence ⇒ mechanism.** When `Authority: existing <path>` already holds the violated
  rule, the candidate is the highest-level mechanism that works (removed possibility, type, check, gate, template slot, or default) at that owner
  ([`skill-authoring.md`](../devrites-lib/reference/standards/skill-authoring.md#match-form-to-failure) § Match form to failure),
  never a reworded, bolder, or relocated copy; otherwise record `no mechanical form
  possible: <reason>` and narrow the proposal. An unwired or broken existing check is
  itself the candidate. **Failing case:** a round accepts a bolder copy of an `AGENTS.md`
  rule that two archived features already violated.
- A lesson proposing a new recurring check names its **controls**: the real past
  instance it would have caught (positive) and a near-miss class it must not fire on
  (negative). Before approval, run the check: it fails on the positive, passes on the
  negative and the current tree; record command and output. **Failing case:** a trigger
  patterned on an imagined command that never matched real history.
- Contradiction outranks staleness: actively misleading guidance outranks merely old guidance.
- A proposal names the **retrospective failing case**: the concrete past feature/artifact the
  rule would have caught. None → generic advice — drop.
- ≤3 accepted lessons per round; proposals extend/narrow but never lower an existing bar (revisions show old text beside new); duplicates consolidate into one canonical edit — simplification (deletions/merges) counts toward the cap.
  Net growth cap: a round adds at most 3 net rules across all owners (additions minus
  retirements). A round whose approved edits add net bytes to an owner states the
  retirement search it ran.
- An accepted lesson ships with a **follow-through owner and deadline**: the exact edit
  lands in the named canonical file in the same round; a lesson unapplied at round end
  returns to candidates with its blocker recorded. **Failing case:** an accepted lesson
  with no applied edit and no recorded blocker — promotion failed; re-raise it.
  Still unapplied at a second round end, it becomes an apply-or-decline decision; a
  decline takes the `rite-learn: declined` record, so no lesson is carried a third time.

## Output

```text
Done: reviewed <scope>.
Changed: none (proposal only)
Candidate: <specific proposal | none | NOT-RUN (unavailable: <reason>)>
Retirements: <candidates | none — searched <scope>>
Currentness: <live source + signal | unknown>
Scope: applies <trigger>; does not apply <boundary>
Authority: existing <path|none>; canonical <path>; consumers/discovery <route>
Disposition: <no conflict | update/narrow/replace/retire path + reason>
Evidence: <feature/file references>
Awaiting: <approval for exact edits | none>
Next: <single action>
Record: <nearest owning decisions file | chat-only only when the round made no accepted/declined disposition>
```
