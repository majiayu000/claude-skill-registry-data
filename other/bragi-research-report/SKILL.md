---
name: bragi-research-report
description: Render the Research workflow's reviewed cluster Workfiles into its final user-facing report — faithful consolidation, question-targeted structure, and concise, boundary-naming communication.
---

# Research Report

## Purpose

Render the Research workflow's reviewed cluster Workfiles into the final user-facing research report. This is consolidation and faithful communication of reviewed findings, not re-research: the report merges the reviewed streams into one answer to the research question, introduces no new claims, and is organized around the question rather than around the sources.

## When to Use

- **Only when dispatched as the Research workflow's deliverable step.** This skill is invoked by the dispatching orchestrator after all research streams have passed their reviews; it is not a general-purpose drafting or communication heuristic.
- The inputs are all reviewed `NN-research-cluster-<name>.md` Workfiles, together with their review Workfiles.
- The output is one concise, question-targeted report that names its own boundaries.

## Workflow

1. **Read every reviewed cluster Workfile in full** before writing anything — and its review, so the verdict's caveats shape what the report states. If an input's review verdict was BLOCKED — or its review is otherwise missing or incomplete — do not consolidate that material as if it were verified: either exclude it and name the exclusion in the boundaries, or flag it to the dispatching orchestrator in your reply.
2. **Identify the core answer** to the research question that the reviewed findings support.
3. **Consolidate.**
   - Deduplicate overlapping findings across streams.
   - Reconcile cross-stream points of contact — surface contradictions between streams, never silently resolve them.
   - Introduce no new claims: nothing enters the report that was not present in the reviewed Workfiles.
4. **Draft the report answer-first (BLUF).** State the core answer within the first two sentences; organize the sections around the research question, not around the clusters or sources; make the structure scannable — headings, bullets, and tables where they aid the reader.
5. **State the four boundaries explicitly:** what was covered, what was not covered, what remains uncertain, and what the user should verify externally.
6. **Calibrate length to the question, not to the input volume** — a report is complete when the question is answered, not when every finding has been reproduced.
7. **Return the full report in your reply to the dispatching orchestrator, and write it to the designated Workfile path.** The orchestrator relies on the content you return to carry the report forward; omitting it silently breaks the pipeline.

## Quality Criteria

- The primary answer appears within the first two sentences.
- Every section serves the research question; no section exists to summarize a source or a cluster.
- The structure is scannable — someone can get the gist in seconds.
- No irrelevant information is included.
- No reviewed finding is silently dropped — the covered / not covered / uncertain contract reflects the streams, and cross-stream contradictions are surfaced, not merged away.
- A reviewed finding that does not serve the question is omitted as off-topic and named in the boundaries — a compact exclusion note, one line per exclusion, topic only, no elaboration; an honest exclusion, never misrepresented as uncertain or not covered; the no-silent-drop guarantee applies to findings relevant to the question.
- No new claims appear beyond the reviewed Workfiles.
- Length is proportional to the question's weight, not to the volume of findings.

## Anti-Patterns

- **Data dump** — reproducing every finding because it was reviewed, with no consolidation into an answer.
- **Buried lede** — making the reader dig through background before the answer appears.
- **Source-organized report** — a per-cluster or per-source digest is not a report; the report is organized around the question.
- **Re-researching** — investigating the topic further instead of consolidating the reviewed findings.
- **Injecting unreviewed claims** — adding conclusions, implications, or facts that were not present in the reviewed Workfiles.
- **Silently merging contradictions** — resolving a disagreement between streams in the report's favor without surfacing it.
- **Boundary-free reporting** — a report that does not state what was not covered and what remains uncertain overstates its own authority.
- **Padding to completeness** — reproducing every reviewed finding at full length instead of answering the question.
