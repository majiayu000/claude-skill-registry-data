---
name: write-decision-ready-technical-reports
description: Turn technical investigations, plans, audits, and status updates into clear decision-ready reports without losing evidence. Use when asked to "make this plan decision-ready", "write a technical status report", "show the before and after", or clarify what is true now, what changed, what decision is needed, what each option costs, or what work remains.
license: Apache-2.0
---

# Write Decision-Ready Technical Reports

<purpose>

Make a technical report easy to skim, verify, and act on. Preserve detailed evidence, but put a
small decision layer before it. A cold reader should be able to identify the current state,
recommended action, alternatives, consequences, and unresolved evidence without reconstructing
the investigation.

</purpose>

<requirements>

## P0 requirements

1. **REPORT-REQ001-lead-with-reader-outcome.** State the artifact's purpose, audience, current
   status, scope, evidence date or revision, and decisions needed in the first screen.
2. **REPORT-REQ002-separate-now-history-target.** Never mix the reproduced past, verified current
   state, and selected target. Use explicit `Before`, `Now`, and `Target` labels.
3. **REPORT-REQ003-separate-cause-consequence.** Put the technical mechanism and user-visible
   consequence in different columns. Keep each cell to one claim.
4. **REPORT-REQ004-label-evidence-state.** Use a small stable vocabulary such as `observed`,
   `reproduced`, `confirmed`, `selected`, `implemented`, `verified`, `blocked`, `deferred`,
   `rejected`, and `superseded`. Do not use “fixed” for code that has not passed its completion
   gate.
5. **REPORT-REQ005-make-decisions-answerable.** Phrase each decision as a concrete question and
   include the recommendation, serious alternatives, consequence of each choice, evidence needed,
   and present decision status.
6. **REPORT-REQ006-name-baselines-and-versions.** Identify the relevant commit, package, schema,
   running process, configuration, dataset, workload, or date. State when source, install, and live
   process differ.
7. **REPORT-REQ007-preserve-evidence-by-link.** Keep reproductions, logs, calculations, and design
   rationale in a detailed evidence section or companion artifact. Add an overview; do not replace
   evidence with a lossy summary.
8. **REPORT-REQ008-distinguish-artifact-roles.** Say whether a file is an evidence log, decision
   brief, implementation plan, status report, benchmark report, or handoff. Do not let one file
   silently act as all six.
9. **REPORT-REQ009-show-before-after-contract.** For proposed work, show current behavior, target
   behavior, user consequence, compatibility or migration effect, and completion proof.
10. **REPORT-REQ010-quantify-with-context.** Give every important number a counted thing, unit,
    baseline, environment or workload, and evidence source. Distinguish measurements from
    requirements and hypotheses.
11. **REPORT-REQ011-progressively-disclose-detail.** Order content as decision dashboard, current
    truth, options, execution map, then detailed evidence. Introduce terms before using them.
12. **REPORT-REQ012-preserve-complexity-tradeoffs.** State relevant time, peak and retained memory,
    I/O, latency, concurrency, and output-growth effects when a decision can change them.
13. **REPORT-REQ013-separate-input-from-instruction.** Distinguish information that should change
    the report's conclusions from information used to author, execute, or evaluate the reporting
    method.
14. **REPORT-REQ014-end-with-decidable-next-step.** End the decision layer with the exact choice,
    approval, experiment, or implementation gate needed next.

</requirements>

<workflow>

## 1. Classify the artifact

Choose one primary job:

| Artifact | Reader's question | Required center |
| --- | --- | --- |
| Evidence log | What happened, and how do we know? | Reproduction, environment, observations, ruled-out causes |
| Decision brief | What should we choose? | Options, recommendation, consequences, evidence |
| Implementation plan | How will the selected outcome be delivered? | Dependencies, tests, work packages, done conditions |
| Status report | What is true now, and what changed? | Baseline, current state, deltas, blockers |
| Benchmark report | What changed under the same workload? | Before/after measurements, uncertainty, resource effects |
| Handoff | What must the next maintainer know or do? | Current truth, exact state, risks, first action |

If one file must serve several jobs, label the sections and declare which section has current
authority.

## 2. Build the decision dashboard

Start with these compact tables, omitting only rows that do not apply.

| Field | Answer |
| --- | --- |
| Purpose | One sentence |
| Current status | One precise state |
| Evidence baseline | Date, revision, environment, or workload |
| In scope | Bounded surfaces or components |
| Out of scope | Nearby work not authorized or not selected |
| Decision needed | Exact answerable question, or `none` |

Then show the smallest useful state transition:

| Area | Before or reproduced issue | Now | Target | User consequence |
| --- | --- | --- | --- | --- |
| One capability | Prior behavior | Verified current behavior | Selected behavior | Why the difference matters |

Do not repeat the same facts in both tables.

## 3. Make decisions explicit

Use one row per independent choice:

| ID | Decision question | Recommendation | Serious alternative | Consequence | Status or closing evidence |
| --- | --- | --- | --- | --- | --- |
| DEC-1 | A concrete question | Selected mechanism | Keep current or another viable design | User and system effect | Ready, blocked, or evidence required |

Separate a prerequisite experiment from the decision it informs. If no decision remains, say so
and identify the implementation gate instead.

## 4. Map execution without hiding tradeoffs

For each accepted work package, use:

- **Where:** authoritative owner and affected adapters.
- **Current:** verified behavior, not stale plan text.
- **Target:** exact externally visible and internal contract.
- **Why:** user consequence and architectural rationale.
- **Tests first:** smallest failing reproduction and cross-surface regressions.
- **Complexity:** present and target time, memory, I/O, latency, concurrency, and output bounds.
- **Compatibility:** migration, versioning, default, and rollback effects.
- **Done when:** observable completion gate.
- **Dependencies:** prior decisions, work packages, or external action.

## 5. Streamline and verify

1. Remove repeated conclusions while retaining unique evidence.
2. Split cause from consequence and current state from interpretation.
3. Keep tables narrow; move multi-paragraph reasoning below the table.
4. Use bold sparingly for the user-visible impact or selected choice.
5. Check every status word against its proof.
6. Ask a cold reader to answer: What is true now? What changes? Why? What can I decide? What
   remains uncertain? Where is the proof?
7. If any answer requires scanning the detailed evidence, repair the dashboard.

</workflow>

<output_contract>

Deliver a report whose first section is sufficient to make the named decision and whose later
sections are sufficient to audit it. Include:

- a document contract and evidence baseline;
- a `Before / Now / Target / consequence` view;
- an explicit decision register or the statement `No decision remains`;
- an implementation or verification map;
- links to preserved evidence;
- precise next action.

Do not present a roadmap as current status, a hypothesis as a defect, implementation as
verification, a shortened view as complete evidence, or a large table as a substitute for a
decision.

</output_contract>
