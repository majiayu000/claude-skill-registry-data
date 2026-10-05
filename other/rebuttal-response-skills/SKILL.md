---
name: rebuttal-response-skills
description: Use when planning, drafting, revising, compressing, or auditing conference rebuttals and author responses in OpenReview Markdown or PDF. Supports exact reviewer mapping, evidence and experiment integration, guided risk decisions, venue-format validation, and blind reviewer/AC audits.
license: MIT
---

# Rebuttal Response Skills

## Goal

Produce reviewer-specific responses that are direct, easy to verify, and
strictly grounded in the submitted paper or approved rebuttal evidence. Keep
internal risk control rigorous without turning the visible response into a
stream of disclaimers.

## Choose the Workflow

Use the **full workflow** for a complete rebuttal, multiple reviewers, new
evidence or experiments, a meta-review, or a final acceptance audit. Maintain
four internal artifact classes in the task's rebuttal directory:

1. Exact review archive, such as `reviews.md`.
2. Concern/evidence map with a shared decision ledger, such as
   `concern_map.md`.
3. One response per reviewer.
4. Final audit record, such as `rebuttal_audit.md`.

Use the **lightweight workflow** for a bounded sentence rewrite, one isolated
question, or minor formatting. Edit inline and create no files unless the user
asks. Preserve the original technical meaning and claim strength by default.
The supplied sentence is sufficient for a pure prose edit; ask for context only
when clarity would require changing a factual claim, number, quotation, or
scope statement.

Read [references/response-patterns.md](references/response-patterns.md) when
drafting a full response, integrating experiments, resolving a risk marker,
running a blind audit, or performing final format verification.

## Establish Sources of Truth

1. Treat the complete review text supplied by the user as the review source of
   truth. If the user later supplies a revised version, use it and record the
   replacement. Check the platform only when text is incomplete, versions
   conflict, or the user asks. Do not draft a full response from a review
   summary; request the exact weaknesses, questions, score, and confidence.
2. Read the submitted paper and supplement as the reviewer saw them. Prefer the
   submitted PDF for claims and values; use source files to locate content only
   when their submitted status is verified.
3. For rebuttal-only work, treat the submission as immutable evidence. Record
   its hash or version before work and verify it is unchanged at the end. Edit
   it only under a separate explicit request.
4. Determine the official response mode, per-response or shared limit,
   anonymity rules, Markdown/LaTeX support, and link or attachment policy.
   Verify current official instructions when the venue is known and the user
   has not supplied them.

## Map Every Concern

Read each review sentence by sentence before drafting. For every substantive
point, record:

- exact original sentence and source section;
- premise and actual concern;
- explicit request or score-shifting condition;
- submitted and rebuttal evidence, with exact source locations;
- evidence gap and proposed response mode;
- one coverage status: `fully answered`, `partially answered`,
  `untested boundary`, or `pending evidence`.

Keep a separate map per reviewer and a shared decision ledger for
user-confirmed values, prohibited wording, excluded experiments, cross-reviewer
terminology, and stop decisions.

- Preserve the review's visible order unless the user explicitly requests a
  different order. A meta-review may change emphasis, not sequence.
- Match labels to the source. Use `W1`, `Q1`, and similar labels rather than
  generic `C1` labels.
- Prefer the reviewer's complete decisive sentence or sentences as the
  heading. Shorten only for precision or a binding format limit.
- Never place a paraphrase or stitched fragment inside quotation marks.
- Merge true duplicates internally. Preserve separate headings when overlapping
  questions contain distinct requests.
- Every substantive point must be answered, explicitly combined with a
  duplicate, marked as an untested boundary, or held for one necessary user
  decision.

## Build the Response

Start each reviewer response with at most two short sentences that state the
answer order. Restore method context only when the answer would otherwise be
hard to understand; do not mechanically re-explain the paper.

For every issue:

1. Give the direct answer in the first sentence.
2. Explain only the mechanism, definition, or setup needed for that issue.
3. Present evidence before interpretation.
4. State the narrow implication supported by that evidence.
5. Add a concrete camera-ready clarification only when the submitted wording
   actually needs correction.

Writing rules:

- Prefer short declarative sentences and terminology already used in the
  submission. Introduce a new term only when necessary and define it once.
- Use the order direct answer, evidence, and supported impact. Avoid opening or
  closing with an apology, “we acknowledge,” or a pre-emptive concession when the
  evidence is already clear.
- When a table fully reports a secondary metric or tradeoff, point to the measured
  value and explain its impact only if it changes the reviewer's question, the
  comparison's fairness, or the claim's applicability. Do not manufacture a
  negative rhetorical ending from a table-visible value.
- If the review relies on an incorrect or incomplete premise, correct it
  politely with submitted evidence, then answer the underlying concern.
- Stay within that reviewer's explicit concerns. Shared evidence may be reused,
  but do not import another reviewer's limitations, baselines, or side issues.
- Acknowledge an especially useful or decision-critical question once when it
  improves the exchange. Avoid routine praise and repeated gratitude.
- Use a closing contribution synthesis only for a low-score review or when it
  is needed to change the overall assessment.
- Never promise an experiment, release, revision, capability, or positive
  future result merely to make the response sound complete.

These are style constraints, not a way to evade a review. A reviewer-requested
negative result, evidence gap, or boundary remains part of the answer; state it
plainly and narrow the claim when necessary.

## Present Experiments and Numbers

- State a shared dataset, model pair, and setup once near the beginning. Mark
  local exceptions beside the relevant table.
- Use a normal Markdown table when the reviewer must compare several conditions
  or metrics. Use prose for only one or two values.
- Define every rebuttal-specific condition, schedule, statistic, and
  nonstandard metric at first use. For a derived metric, give its calculation,
  unit, and whether higher or lower is better. Do not re-define standard paper
  metrics unnecessarily.
- Keep shared values and definitions identical across reviewers. Crop a shared
  table to reviewer-relevant rows or columns when useful.
- Do not present pending runs, placeholders, expected trends, or partial
  outputs as results.

## Enforce Evidence Discipline

- Use submitted PDF/LaTeX values for submitted claims. Use matched controls from
  the same protocol for a new rebuttal experiment.
- If a reproduction materially conflicts with the submission, stop and ask the
  user. Pause the affected claim, table, and every dependent response; continue
  only work that does not depend on the conflict. Do not silently choose,
  average, or substitute values. Treat a conflict as material when it could
  change a reviewer-facing conclusion, comparison ordering, or claim boundary.
- Before proposing a new experiment, inspect the main paper, appendix, and
  supplement. When reusing submitted evidence, cite its exact location and
  summarize the observation relevant to the concern; do not write only
  "see Appendix."
- A logically matched proxy is acceptable. Define what it measures once and do
  not describe it as direct evidence for an unmeasured quantity.
- Separate measured results, analytical derivations, architectural reasoning,
  dataset facts, and future directions.
- Use `$research-evidence` when an answer depends on external literature,
  dataset facts, novelty positioning, or citation authenticity. Never invent a
  citation.

For capability or deployment questions, distinguish:

1. what the method design permits;
2. what the submitted implementation supports;
3. what the experiments evaluate.

Use the paper description first. Inspect code or configuration when the paper
cannot answer an explicitly implementation-specific question or the user asks.
Do not turn an architectural extension into an implemented or evaluated claim.

## Control New Evidence and Risks

Before starting any new experiment, give the user the minimal design, the
review concern it answers, the comparison and controls, and the outcome
criteria. Run it only after explicit approval.

Retain every predeclared condition in the internal evidence record. Do not
silently remove a mixed or negative condition. Mark high-impact uncertainty as:

`[REVIEW NEEDED | Ideal: ... | Observed: ... | Decision: ...]`

Use this marker for material numeric conflicts, mixed or negative results,
proxy limitations, or a proposed claim/commitment needing approval. Explain
each marker to the user one at a time and remove it only after explicit
confirmation. A submission candidate must contain no marker, placeholder, or
pending result. The user decides the reviewer-facing presentation, but a
reviewer-requested result, a promised condition, or evidence material to a
visible claim cannot be omitted merely because it is negative. Report it or
narrow the claim so the response remains complete and non-misleading.

If the user says to stop an experiment or stop discussing a protocol dispute,
stop immediately. Do not continue the run, internal investigation, or
questioning. Do not add the stopped technical sub-issue to the visible response
unless the user later requests it. This does not authorize silently dropping an
explicit reviewer concern: answer that concern with approved existing evidence
or one concise untested-boundary statement. If the user explicitly directs its
omission, record that decision in the ledger.

For an untested or infeasible request, answer what current evidence or
reasoning supports, state the untested part once, and propose a future direction
only after user approval. Do not guarantee implementation or a favorable
outcome.

## Handle Meta-Review

When a meta-review exists, extract its decision-critical or score-shifting
conditions and map each one to the relevant reviewer response and final AC
audit. Add a condition to a reviewer response only when it directly overlaps
that reviewer's concern. If a meta-only condition has no response entry and no
such overlap, keep it as an internal AC item rather than forcing it into an
unrelated response. Do not change the default reviewer order. Draft a
standalone meta response only when the platform provides an appropriate entry.

## Run a Blind Reviewer and AC Audit

For a high-stakes final response, use fresh subagents when available. If fresh
agents are unavailable, run separate paper-only and response-aware self-audit
passes using the same input isolation, and state internally that independence
was not achieved.

1. **Paper-only phase:** Give each reviewer agent only the submitted paper,
   supplement, venue scoring scale, and public rules. Ask for an independent
   review, score, confidence, and major concerns. Lock this output.
2. **Response phase:** Then give the same agent the corresponding exact official
   review and response. Ask which concerns are answered, whether the score
   changes, and whether a response defect remains.
3. **AC phase:** After reviewer audits, give a fresh AC agent the submitted
   materials, meta-review when present, official reviews, responses, and audit
   outcomes.

Never expose the concern map, decision ledger, author strategy, target score,
suspected weakness, or intended conclusion to blind agents.

Classify audit findings as:

- `Response defect`: missed concern, evasion, unsupported claim,
  contradiction, misleading evidence, or format violation.
- `Unresolved paper limitation`: a real limitation the response cannot remove.
- `Optional strengthening`: a non-blocking improvement.

Only a `Response defect` blocks by default. Each reviewer agent must report its
before/after score, per-concern coverage, and final `ACCEPTABLE` or blocking
defect. The final candidate passes only when every reviewer audit and the AC
audit reports `ACCEPTABLE` with no blocking response defect. Do not expand the
rebuttal for unrelated new concerns unless they expose a fatal factual error,
integrity risk, or direct contradiction.

## Final Verification

Use a fresh format-verifier agent plus deterministic checks. If no fresh agent
is available, run a separate verifier pass using only the final candidate and
official rules. Follow the platform's official counting method; require the
candidate to remain below a character limit and within a page limit.

1. **Coverage:** all mapped concerns retain correct order and labels; no
   reviewer-specific issue has leaked into another response.
2. **Evidence:** every number and factual claim has provenance; comparisons are
   fair; no unapproved commitment or unresolved high-impact decision remains.
3. **Rendering:** enforce the official character or page limit; check Markdown
   tables, LaTeX delimiters, headings, anonymity, machine paths, allowed links,
   and PDF compile/render quality when applicable.
4. **Cleanliness:** search for `REVIEW NEEDED`, `TODO`, `pending`, placeholders,
   and internal artifact paths. Resolve every hit before submission.
5. **Immutability:** verify the submitted paper and supplement version or hash
   is unchanged.

For a follow-up reviewer comment, answer only the new delta unless it changes
the overall strategy.
