---
name: library-fitness-review
description: Trigger a comprehensive whole-collection library-fitness review with a project-defined catalogue of persona reviewers when a documentation collection (the parent case is a governance/security documentation library) undergoes a major change or reaches its minimum review cadence, quarterly by default unless the adopting project records a different interval. The parent GRC library's major-change triggers are a new domain directory, a new document type, multiple governance rule additions, and a major restructure. Each invocation dispatches a fan-out of independent persona subagents (for example an executive reader, a security practitioner, an auditor, a newcomer) who review every page from a fresh-reader perspective without inheriting maintainer mental models. Catches comprehensibility, usability, logical-structure, standardization, domain quality, auditability, maintainability, and reader-experience gaps that per-change validation sweeps and mechanical audit gates do not detect. Surfaces prioritized recommendations and a discrete remediation backlog the maintainer drives through subsequent changes.
derives_from: ../../governance/trust-recovery-escalation.md
---

# Library Fitness Review

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Persona catalogue and severity model: the activity convention document in the consuming project's working state (the persona briefs with per-persona scope and
  exclusions, the severity-model definitions, the per-run file format, and the
  operational guidance; the parent catalogue defines ten personas, labelled `A` through `J`).
- Run-record path pattern: a dated per-run record in the consuming project's working state, one combined
  report per run, with `rN` the run ordinal that day.
- History register: the fitness-review invocation history register in the consuming project's working state (the invocation history table,
  whose `Personas` column records the personas dispatched, written in the register as `A, B, C, D, E, F, G, H, I, J (all 10)` for a full dispatch, plus the
  open remediation backlog tracking table).
- Remediation-backlog id scheme: `FR-N` (`FR-1`, `FR-2`, ...), carried into TODO entries
  and referenced from the CHANGELOG entry of each PR that closes an item.
- Mechanical baseline command: `tools/run_all_audits.sh`, the parent library's full
  audit suite.
- Citation-accuracy boundary: the corpus Citation Verification Specification (its §14
  records that the library does not verify standard content against library
  interpretation), which bounds what a fitness review judges.

An adopting project maps each bullet to its own records and registers; the procedure below refers to them generically.

## Overview

A documentation library (the parent case: a governance, risk, and compliance library) accumulates content over months and years. Per-PR validation sweeps catch drift introduced by recent changes; mechanical audit gates catch structural defects (broken links, stale gate counts, missing metadata, version-bump omissions). Neither catches the slower, harder failure modes: a page that *technically* passes every gate but no human can act on; a control objective that an auditor cannot evidence; terminology that has drifted such that different documents use different words for the same concept; a workflow that's documented for the author's mental model but unusable by an operational reader; a pattern of "we wrote this for ourselves" that survives because no fresh reader has tested it.

The fitness review is the periodic, multi-perspective evaluation of *what's there*, complementing the validation-sweep's evaluation of *what changed*. It runs heavyweight (the full configured persona catalogue dispatched in parallel; whole-collection scope) and at the adopting project's configured cadence, and produces a report in the configured record format. The parent GRC library uses major-change plus quarterly triggers and an eight-section combined report.

The discipline this skill encodes is **fresh-reader review at scale**: every persona reviews every page without inheriting the maintainer's context. Persona diversity surfaces failure modes that a single reader (or single AI agent without persona instruction) misses systematically. The output is not a pass/fail gate; it is a prioritized remediation backlog with concrete recommendations.

## When to Use

- **After a major change to the review collection**: the adopting project's change-shape trigger fires. In the parent GRC library that means a new domain directory ships, a new document type is introduced, three or more governance rules are added, or a major restructure lands. The first fitness review after a major change verifies that the addition is consistent with the rest of the collection and reachable for adopters.
- **Quarterly minimum (the default cadence)**: run a review at least once a quarter even when no major change triggered it. An adopting project may record a justified alternative minimum (with its rationale); absent one, quarterly is the floor. Slow drift accumulates; a periodic review catches it before adopters notice.
- **Pre-publication / pre-external-share**: before the library is shared with a wider audience, relied on operationally (the parent case: used as the basis for a real GRC programme), or cited externally. Fresh-reader review is the gate.
- **Pre-audit**: when the library will be used as evidence in an audit, run a fitness review specifically with the auditor persona's lens centred so the maintainer can address audit-readiness gaps before the auditor arrives.
- **On demand**: when the maintainer's gut says "I'm not sure this is in shape" but doesn't have specific findings to point at. The full persona fan-out surfaces what the maintainer's recall does not.

Not when:

- The change is per-PR. That's `validation-sweep-pr-scoped` territory.
- The change is a typo or single-line fix. The cost (a full persona fan-out) doesn't match the scope.
- The maintainer wants a security audit specifically. That's a focused security review, not a generalist fitness review.
- The maintainer wants to verify external standard accuracy. That's the citation-verification process, not a fitness review (per the citation-accuracy boundary named in the project wiring, the library does not verify standard content vs. library interpretation).

## Process

### 1. Establish mechanical baseline

Run the project's full mechanical audit suite standalone. The fitness review starts from a
review collection that passes its configured mechanical checks; fix uncorrected failures
first.

### 2. Identify scope and run ordinal

The scope is the **whole configured review collection**, normally every page reachable
from the project's configured entry or index surfaces. Do not scope down except by explicit
maintainer authorization recorded in the run history.

The run ordinal is the next `N` after the most recent entry in the history register named in the project wiring. Multiple runs in one calendar day increment `r1 → r2 → r3`.

### 3. Dispatch the configured persona catalogue in parallel

Each persona is dispatched as an independent subagent. The orchestrator's brief to each subagent must:

- **Strip orchestrator context**: tell the subagent the persona's role, the corpus scope, and the review brief. Do NOT tell the subagent what the maintainer expects to find, what recent changes have shipped, or what the prior fitness review concluded. Fresh-reader requires fresh context.
- **State the persona's scope, focus questions, and explicit exclusions**: the persona briefs in the catalogue document named in the project wiring are the canonical source for the project's personas. Each brief includes WHAT the persona reviews and WHAT IT DOES NOT (to prevent cross-persona overlap).
- **Require structured findings**: each finding is a block with persona identifier, ruleId, severity (High / High[critical] / Medium / Low / FYI), location (file path + section heading or line where possible), evidence (a quoted excerpt or specific pointer), impact, recommended remediation, retention decision (retain / revise / merge / split / rename / retire / relocate).
- **Demand evidence**: a finding without quoted evidence or a specific location reference is a hypothesis, not a finding. Reject and re-dispatch with the evidence requirement re-emphasized.

In the parent library the persona catalogue (the document named in the project wiring) defines these lenses; an adopting project defines its own:

1. **First-time executive reader**, strategic comprehension; can a non-expert executive understand purpose, audience, required action?
2. **Security practitioner**, technical security adequacy; OWASP/ASVS alignment, threat-model coverage, cryptography currency.
3. **GRC practitioner**, governance/risk/compliance discipline; risk and control ownership clarity, evidence expectations.
4. **Auditor / assurance reviewer**, audit-readiness; what must be true, who is responsible, where is evidence, how often reviewed.
5. **Policy and standards editor**, editorial consistency; naming conventions, requirement-language, terminology.
6. **Process owner / operational user**, usability for execution; explicit roles, actionable procedures, sufficient templates.
7. **Skeptical reader**, ambiguity, contradictions, gaps, "so what?" tests, where readers lose trust.
8. **Adoption practitioner**, real-world use; can I set up a programme from this? What's missing for small orgs / large orgs / regulated sectors?
9. **Privacy / data protection officer**, privacy-specific obligations; data subject rights, jurisdiction-aware, DPIA triggers, breach thresholds.
10. **Newcomer / onboarding engineer**, zero-knowledge entry; jargon-free comprehension, navigation friction, minimum reading order.

Dispatch the full catalogue on every full run. Skipping a persona is the same class of discipline failure that the validation-sweep's Rule 5.6 names (dispatch declaration must be recorded; silent absence cannot be reconstructed). The only sanctioned exception is a maintainer-authorized scoped run recorded in the history-row Summary.

### 4. Synthesize findings

Apply a six-step synthesis rubric (mirrors the validation-sweep's synthesis discipline at a different scope):

**4.1. Dedupe by `(file_path, normalised_section, claim_type)`**. Different personas may surface the same defect through different lenses (e.g., the executive reader and the newcomer both flag the same unexplained acronym). One dedupe-key tuple, one synthesized finding.

**4.2. Tag each synthesized finding `R | I | K`**: `R` (Real evidence: quoted line or specific reference); `I` (Inference: persona's interpretation pending verification); `K` (Known-issue resurfaced: already in the remediation backlog from a prior run).

**4.3. Adjudicate severity**: pick the higher severity if personas disagree by one level (e.g., Medium vs. Low → Medium). If they disagree by more than one level or split on `[critical]` vs. non-critical, invoke one round of asymmetric debate (4.5).

**4.4. Record persona provenance**: each synthesized finding carries the set of personas that surfaced it (e.g., `personas: [executive, newcomer]`). Coverage gaps are then attributable: if only one persona surfaces a finding repeatedly across runs, the others' briefs may need tuning.

**4.5. Debate for large divergence**: when two personas split on real-vs-false-positive, or by more than one severity level, re-prompt each disagreeing persona with the other's claim attached and ask each to update or hold with rebuttal. One round only. The orchestrator adjudicates the second-round positions; persisted disagreement is flagged `debated: divergence-persisted` in the synthesized finding.

**4.6. Dispatch declaration recorded**: the history-row's `Personas` column declares which personas were dispatched. Per the discipline mirrored from `validation-sweep` Rule 5.6, silent absence cannot be reconstructed; the dispatch declaration is the auditable trail.

### 5. Verify findings, then triage by severity tier

Subagent findings are *unverified by default*. Persona subagents return what their fresh-reader judgement surfaced; the synthesis at step 4 deduplicates and tags by `R|I|K` provenance but does not itself re-read the cited evidence. This verification discipline catches the failure mode where a synthesis-stage approximation propagates downstream as if confirmed (the precedent in the parent library: a run report's summary count and severity tabulation, written from the synthesis narrative rather than recounted mechanically from the finding rows, shipped wrong and was corrected only in a follow-up change; the same failure mode at finding-content granularity would be worse).

Step 5 therefore runs in four sub-steps before any finding lands in the remediation backlog:

**5.1. Output the report with all findings marked `unverified`**. Every per-page finding row in the report's page-by-page findings section (`## Page-by-Page Findings` in the default schema) carries an explicit `verification: unverified` annotation at the time the report is written. The remediation-backlog entries (`## Remediation Backlog` in the default schema) inherit the same annotation. Severity is still tagged (so prioritization can begin) but no finding is treated as actionable until Pass-1 confirms it.

**5.2. Pass-1, orchestrator verification**. The orchestrator (not a subagent) re-reads each cited source location for every finding and applies one of four verdict tags:

- `✅ confirmed-as-stated`: the finding's evidence quote matches the source verbatim and the interpretation is sound.
- `⚠️ confirmed-with-modification`: the underlying issue is real but the persona's framing is partially off (wrong line number, mis-attributed quote, scope drift); the modification is recorded inline.
- `❌ rejected`: the cited evidence does not support the finding, or the persona's interpretation is incorrect; rejection rationale is recorded inline.
- `🤔 ambiguous-needs-maintainer`: the finding is plausible but turns on a judgement the orchestrator cannot make autonomously (a content-policy decision, a domain-specific accuracy call); the ambiguity is captured for Pass-2.

Pass-1 updates the report file in place: each finding's `verification:` annotation flips from `unverified` to one of the four verdict tags. Pass-1 runs in a single sweep through the report; it is not a per-finding interactive loop.

**5.3. Pass-2, maintainer-interactive bucket processing**. The orchestrator surfaces the four tag buckets to the maintainer in chat:

- The `✅` cluster: confirmed-as-stated findings are presented as a batch summary (count, severity distribution, file locations); the maintainer issues a single confirmation to accept the batch.
- The `⚠️` cluster: each confirmed-with-modification finding gets a per-finding prompt with the orchestrator's recommended adjustment plus alternative framings; the maintainer picks one or types a custom resolution.
- The `🤔` cluster: each ambiguous finding gets a per-finding prompt with the orchestrator's analysis and the open question; the maintainer resolves to `✅`, `❌`, or "defer (open follow-up)".
- The `❌` cluster: rejected findings are presented as a batch with their rejection rationales; the maintainer either accepts the orchestrator's rejection or escalates a specific finding back to `✅` or `🤔`.

**5.4. Triage and severity-tier action for confirmed findings only**. Findings that ended Pass-2 as `✅` (or `⚠️` with maintainer-accepted modification) become actionable items:

- **High `[critical]`** (audit failure / regulatory exposure / control failure class) → must-fix-before-next-major-reliance-event; surfaces immediately to the maintainer as a priority backlog item; if remediation is small, may be bundled with the fitness-review close-out PR.
- **High** → must-fix-this-quarter; goes into the remediation backlog with a recommended deadline.
- **Medium** → should-fix-next-review-cycle; remediation backlog with a softer deadline.
- **Low** → editorial; queue for the next routine cleanup PR.
- **FYI** → informational; recorded in the report but not in the remediation backlog.

The fitness review does not auto-defer findings to FYI. Every confirmed finding gets an explicit severity-tier action. Rejected findings are recorded in the report (with rationale) but excluded from the backlog.

**5.5. Trust-recovery routing flag.** When this skill (the parent library's `/fitness`) runs as the second pass of the trust-recovery escalation suite (per [`governance/trust-recovery-escalation.md`](../../governance/trust-recovery-escalation.md)), the routine severity-tier triage of step 5.4 is replaced by the tier's routing convention: every Pass-1-confirmed finding routes to the backlog **tiered by severity (High[critical] and High to the top-priority tier, Medium and Low to the next-priority tier)**, tagged `[fitness]`, with the normal Low-to-routine-cleanup and FYI-to-informational deferral suspended so that **nothing the review surfaces is dropped or shelved as FYI-only**. The rationale is the rule's: the tier exists because the assistant's discretion to discount has been shown unreliable in the window under review, so severity governs the destination tier, not whether a finding is surfaced. Pass-1 apply-time verification and dedupe-against-the-existing-backlog still apply, and the tier terminates only on the maintainer's explicit sign-off (not on an empty finding-set). Outside trust-recovery mode (a routine or quarterly fitness run), step 5.4's normal triage applies unchanged.

**Confirmed findings produce tracked remediation entries** carrying the configured remediation identifier, originating run reference, and verification date. The tracked entry is the bridge between the fitness-review report and the project's change queue.

### 6. Write the combined report

Write one combined report file at the run-record path named in the project wiring (the parent GRC library names it by date and run ordinal; adopters relocate to a project-appropriate location and record format). The report carries every section of the run's report schema, in the schema's order. The default schema is these eight H2 sections, which an adopting project may replace with its own recorded schema (see the catalogue document named in the project wiring for the parent's full content spec):

1. `## Executive Summary`, overall fitness, highest-risk issues, priorities, publication-readiness assessment.
2. `## Review Method`, personas dispatched (with explicit count and identifiers), pages reviewed, evaluation criteria, assumptions or limitations.
3. `## Page-by-Page Findings`, per-page entries: title, path, intended purpose, actual clarity, intended audience, key issues, severity, impact, recommendation, retention decision.
4. `## Cross-Library Findings`, systemic patterns: terminology inconsistencies, structural problems, missing document types, duplicated or conflicting guidance, navigation weaknesses, broken cross-linking, requirement-language drift.
5. `## Severity Model`, explicit definitions used in this run (self-contained restating of the canonical model).
6. `## Recommendations`, priority-grouped with: recommendation, rationale, affected pages, expected benefit, estimated effort (Small/Medium/Large), suggested owner, dependencies, proposed implementation order.
7. `## Standardization Recommendations`, page taxonomy, naming conventions, required metadata, required page sections, requirement-language rules, ownership model, review cadence, cross-linking model, versioning model, status labels, template recommendations.
8. `## Remediation Backlog`, discrete work items with IDs (`FR-1`, `FR-2`, ...), title, description, severity, affected pages, recommended action, acceptance criteria, estimated effort, dependencies.

Optional `## Final Assessment` if sections 1 and 6-8 leave material to summarize (fit-for-use, fit-for-audit-support, fit-for-executive-consumption, fit-for-operational-execution).

### 7. Append the history entry

Append an entry to the configured history register using its ordering, identifier, and column schema. The parent GRC library uses the table below, reverse chronology, `rN` run identifiers, and a detail-file link or `none`; adopters substitute their configured record shape:

| Date | Run | Personas | Findings | Resulting PR | Detail | Summary |
|---|---|---|---|---|---|---|

- **Date** is `YYYY-MM-DD`.
- **Run** is `rN` (run ordinal that day).
- **Personas** is the register's full-dispatch marker for a full-catalogue dispatch, or a comma-separated subset for a scoped run (rare; with authorization reason in the Summary cell).
- **Findings** is a brief count with severity breakdown (e.g., `0`, `7 (2H, 1H[critical], 3M, 1L)`).
- **Resulting PR** is the close-out PR link, or `none` for zero-finding runs (or `pending` if the maintainer hasn't decided which findings to action yet).
- **Detail** is a link to the per-run file at step 6, or the marker `none` for zero-finding runs.
- **Summary** is a one-line description of the run's key findings or "library passes fitness review" for zero-finding runs.

Zero-finding runs still write a history row. The history is the audit trail of every invocation, not just the productive ones.

### 8. Surface issues, recommendations, and choices in chat

The fitness review's actionable layer is the chat surface. After writing the combined report, surface in chat:

- **High [critical] findings**: each named with location and one-line action recommendation; ask the maintainer to confirm immediate-action priority.
- **Configured High-priority shortlist**: name each shortlisted finding with location and recommendation; the parent GRC library surfaces five.
- **Cross-library patterns surfaced**: named with the implicated documents and the proposed standardization; ask whether to pursue.
- **Standardization recommendations**: each with effort estimate; ask the maintainer to triage which to adopt now, defer, or reject.
- **Remediation backlog**: total count of discrete items; ask which to drive in the next PR cycle.

The combined report file is the persistent archive; the chat surface is the prioritization conversation.

### 9. Maintain follow-up tracking

Once the maintainer has triaged the recommendations and assigned remediation IDs to PRs:

- Update the **Open remediation backlog** table in the history register named in the project wiring with each item's status (`pending` / `in-progress` / `closed`) and the assigned PR.
- When a change closes a remediation item, its configured change record references the remediation identifier so the trail back to the originating fitness review is preserved.

## Red Flags

- **A finding without a quoted evidence excerpt or a specific location pointer.** The fitness review's discipline is fresh-reader-grounded judgement; a finding the persona cannot point to is a guess.
- **Reusing the prior run's conclusions to skip current personas.** Each run's findings are evaluated against the current review collection. The prior run's conclusions inform priority, not current findings. "Subagent A returned zero last time, skip this run" is the inference-cascade failure mode the pack's `validate-inference-before-action` rule prevents.
- **Letting maintainer mental models leak into persona briefs.** If the brief telegraphs what the maintainer expects, the subagent confirms expectation rather than testing it. Strip maintainer context from each persona brief.
- **Treating "all gates pass" as evidence the library is in good shape.** The fitness review exists precisely because mechanical gates don't catch what the personas catch. Conflating mechanical pass with quality is the failure mode.
- **Skipping personas because "scope is similar to the prior run".** Persona-specific failure modes recur per-persona; the security practitioner may surface findings the GRC practitioner systematically misses, and vice versa. Full-catalogue dispatch is the default; scoped runs require explicit maintainer authorization recorded in the history-row Summary.
- **Bundling a fitness-review close-out with unrelated work.** The fitness-review PR closes (or surfaces) findings; bundling unrelated work confuses the audit trail. Each substantive remediation gets its own PR; the close-out PR contains only the history-row update + report file + any tiny editorial fixes inline.
- **Treating the remediation backlog as exhaustive.** The fitness review surfaces what the personas catch in one run. Subsequent fitness reviews may surface different findings as the corpus evolves. The backlog is current at write-time; new findings get new IDs.
- **Letting Low/FYI findings crowd out High priority items in the synthesis.** The combined report's Recommendations and Remediation Backlog sections lead with High and High[critical]; Medium and Low items follow; FYI items go in their own clearly-marked section.

## Verification

This skill is complete on a given run when:

- Every persona in the catalogue has been dispatched (or a scoped subset has been authorized by the maintainer with the authorization recorded in the history-row Summary).
- Each persona has returned findings (or "zero findings" with a one-line rationale).
- Synthesis has applied all six rubric steps (dedupe, R/I/K tag, severity adjudicate, persona provenance, debate where applicable, dispatch declaration).
- The combined report contains every section required by the configured report schema (eight in the parent GRC library, plus its optional `## Final Assessment`).
- The history-row has been appended to the history register named in the project wiring with all columns populated.
- The maintainer-facing chat surface has presented the High[critical] findings, the top High findings, the cross-library patterns, the standardization recommendations, and the remediation backlog count for prioritization.
- The full audit programme passes standalone on the post-fitness-review state (no findings the fitness review introduced into the corpus).

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We just ran a fitness review last quarter; the library can't have drifted." | Drift accumulates between runs. The persona briefs are specifically designed to surface what mechanical gates and per-PR sweeps don't. If a quarterly run finds nothing, that is signal: log it and move on. If it finds something, the prior run's clean bill of health is irrelevant; act on the current finding. |
| "A full persona catalogue is overkill for our small library." | The catalogue is tuned to the failure-mode space, not the library size. Each persona catches a class of finding the others systematically miss. Dropping personas drops finding classes. If the library is genuinely small, the run is fast (fewer pages); the catalogue stays constant. |
| "The fitness review surfaces too many findings; we can't action them all." | The fitness review does not require actioning all findings. The remediation backlog is a prioritized list; the maintainer triages. Items left at Low or FYI persist in the backlog until a relevant context arises. The discipline is to capture, not to compulsively close. |
| "Skip the auditor persona; we're not in audit prep." | The auditor persona surfaces audit-readiness defects that bite at audit time, six months before the auditor arrives. Skipping during non-audit periods is exactly when the gaps form. Run the full-catalogue dispatch every time. |
| "The personas overlap; let me consolidate to fewer." | Personas overlap by design at the symptom layer and differ at the lens layer. The executive sees comprehensibility-from-business-context; the newcomer sees comprehensibility-from-zero-knowledge. Same word, different failure modes. Consolidating loses the per-lens specificity. |
| "The remediation backlog is just a list; we don't need IDs." | Stable identifiers from the project's configured scheme create the trail from finding to remediation change. Without them, a change that fixes one finding cannot be linked back to the originating review; the audit trail breaks. |
| "Mechanical gates have improved enough that fitness review is redundant." | Mechanical gates close their specific failure classes (broken links, stale counts, missing metadata). They do not close the persona-shaped classes (executive comprehension, audit-readiness, adoption usability). New mechanical gates can be born from fitness-review findings, but the fitness review itself remains the source of new-failure-class detection. |
| "Personas should evaluate from outside; we should hide the review collection from them." | Subagents need collection access to find evidence. What's stripped is the *maintainer's mental model*, not the collection. The persona reads the collection fresh and reports what they find. |

## See Also

- Canonical rule [`governance/evidence-grounded-completion.md`](../../governance/evidence-grounded-completion.md): the verification discipline this skill applies at corpus scope. Each persona's finding requires evidence (quoted excerpt or location reference); the skill operationalizes evidence-grounded-completion across the catalogue's parallel lenses.
- Related skill [`validation-sweep`](../validation-sweep/SKILL.md): the corpus-wide regression sweep (its per-PR sibling is `validation-sweep-pr-scoped`). Where `validation-sweep` catches what changed, this skill evaluates what's there. Both can coexist; neither replaces the other. See the catalogue document named in the project wiring, its "Relationship to `validation-sweep`" section, for the comparison table.
- Related skill [`fresh-reader-validation`](../fresh-reader-validation/SKILL.md): per-document fresh-reader check. Where `fresh-reader-validation` runs one persona on one document, `library-fitness-review` runs the full persona catalogue on the whole corpus. The single-document skill is the focused follow-up when a fitness review surfaces a specific page that warrants deeper persona-fresh-reader scrutiny.
- Related skill [`skill-authoring-discipline`](../skill-authoring-discipline/SKILL.md): the discipline this skill's own authoring follows. The fitness-review skill catches library-level failure modes; the authoring-discipline skill catches skill-level failure modes during the SKILL.md drafting.
- Related skill [`citation-quote-verification`](../citation-quote-verification/SKILL.md): when a fitness-review finding involves a cited external standard, this is the targeted follow-up that verifies the citation rather than the library's interpretation of it.
- Related skill [`change-tracking-write-entry`](../change-tracking-write-entry/SKILL.md): the fitness review's close-out PR is a tracked change; the CHANGELOG entry follows the change-tracking discipline.
- The activity convention document named in the project wiring (adopters relocate to a project-appropriate location): the canonical source for the project-specific persona catalogue, the severity-model definitions, the per-run file format, and the operational guidance.
