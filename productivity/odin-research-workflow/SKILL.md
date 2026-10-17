---
name: odin-research-workflow
description: Orchestration doctrine for the Research workflow — the strategist role manages the research task across one or more bounded rounds, with reconsideration based on reviewed findings.
---

# Research Workflow

## Purpose

Define the orchestration doctrine for the Research workflow — an adaptive, trigger-gated workflow where Kvasir manages the research task across one or more bounded rounds. Each round decomposes (or reconsiders) the research question into parallel-executable clusters, executes them as reviewed research streams, and then Kvasir may recommend further investigation or declare the research sufficient for the report.

The workflow packages the "(Kvasir Plan/Reconsider → Research A → Review ∥ Research B → Review ∥ ...) → [Sufficient? → Report] or [Continue? → Next Round]" pattern from the Orchestration Patterns table in your system prompt, and is distinct from a one-shot "Research → Review → Report": the workflow guarantees one upfront Kvasir consultation whose decomposition plan is surfaced to the user as a steering checkpoint before execution commits, and permits bounded reconsideration across multiple rounds based on reviewed findings. Parallelism is an emergent property of the decomposition, not a command-level feature: independent clusters run in parallel; dependent chains run in sequence.

**Fixed Deliverable (per § Deliverables and § Deliverable Determination in your system prompt):** a Response (the research report drafted by Bragi, step 4) and an Artifact (the persisted report file, persisted by Brokk, step 5). This fixes the Deliverable at Odin's top level: `source=workflow-fixed`, no inference on invoke.

## When to Use

- When the Research check verdict is **invoke** — via the `/yggdrasil/research` command or explicit research/investigate/analyze-into language in the request, per the Trigger Thresholds in your Communication Policy.

This workflow carries its own mandatory Kvasir consultation as step 1 (the decomposition).

## Workflow

1. **Decomposition (mandatory).** Dispatch Kvasir with the `kvasir-research-decomposition` skill and the research topic. Kvasir writes a decomposition plan to a Workfile — N clusters with per-cluster investigation questions (N may be 1). This consultation is mandatory on every invoke. Records the Kvasir session ID for potential reconsideration across multiple rounds (bounded by a hard cap, default 3, to prevent unbounded looping).
2. **Plan checkpoint (steering).** Surface the decomposition plan to the user as a readable summary — *"I will research these N aspects: [list]. This will take a few minutes."* The user may accept, modify, or redirect before execution begins. Whether to pause for steering input or auto-proceed is governed by your Communication Policy; when auto-proceeding, continue unless the plan is obviously defective. If the plan indicates multiple rounds may be needed, surface the round cap and allow the user to adjust it.
3. **Parallel research.** For each cluster in the current round's plan, dispatch Mimir with the cluster's investigation questions and its `mimir-research-convention` skill. Parallelize genuinely independent clusters; sequence dependent chains. Each Mimir writes `NN-research-cluster-<name>.md`. After all streams are reviewed, Odin may resume the Kvasir session (via the recorded session ID) with the reviewed findings to determine if further rounds are needed or if research is sufficient for the report.
4. **Deliverable (Response).** Dispatch Bragi with all reviewed cluster Workfiles and its `bragi-research-report` skill to consolidate them and draft the user-facing research report in one pass — a concise, question-targeted report, organized around the question rather than the sources, that explicitly states: what was covered, what was not covered, what remains uncertain, and what the user should verify externally. Writes the report Workfile.
5. **Deliverable (Artifact).** Dispatch Brokk to persist the report as an Artifact at a user-visible path.

**Review-skill assignment:** the standing reviews this workflow generates (per § Review & Quality Gates in your system prompt — one per research stream, and the Final Review Gate) are not numbered above. The stream reviews use the `heimdall-research-review` skill; each stream review writes `NN-review-cluster-<name>.md`. The Final Review Gate brief for this workflow must additionally verify that the report faithfully consolidates all reviewed cluster Workfiles — no reviewed finding relevant to the question silently dropped (off-topic omissions, honestly made and named in the boundaries, are sanctioned), no cross-stream contradiction silently merged, boundaries preserved — by checking the report against the cluster Workfiles and their reviews.

## Quality Criteria

- **Bounded reconsideration.** Kvasir may be consulted again after each round's reviewed findings, but the total number of rounds is capped (default 3, user-adjustable at the steering checkpoint) to prevent unbounded looping. Each reconsideration is based on reviewed findings from the prior round, not on new user input mid-execution.
- **N is bounded by the decomposition** — typically 2–5 for heavy research, 1 for a light question; adaptive, never a fixed default.
- **Cost (total dispatches — including the standing reviews and the Final Review Gate, which are not numbered steps):** `2N + 4 + (R-1)*(2M + 1)` where N = initial clusters, R = total rounds, M = average clusters per subsequent round (Kvasir reconsultation per round after the first). Single-round research (R=1) costs `2N + 4`; e.g., N=1 → 6, N=3 → 10.
- **The steering checkpoint always happens** — whether to pause for steering input or auto-proceed is governed by your Communication Policy.
- **Every research stream is independently reviewed** before the report consumes it, with fresh-session distinct-subtask isolation.
- **The report names its own boundaries** — covered, not covered, uncertain, and what to verify externally.

## Anti-Patterns

- **Unbounded research looping.** Reconsideration must be bounded by the round cap; if Kvasir recommends further rounds after the cap is reached, Odin escalates to the user rather than continuing silently. Each reconsideration must be based on concrete findings from the prior round, not on vague "more research would be nice" reasoning.
- **Skipping the decomposition.** The Kvasir consultation is mandatory on invoke — even when the topic looks simple (N=1 is a valid decomposition outcome). Only an infrastructure failure of the dispatch itself triggers the own-judgment fallback.
- **Hiding the plan.** Executing the decomposition without surfacing the steering checkpoint — the visible, steerable plan is what makes the mandatory consultation additive.
- **Re-decomposing mid-flight.** If execution reveals the plan is wrong, that is Mid-Execution Consultation territory, not a second run of the decomposition skill.
- **Restating skill internals in briefs.** Name the specialist skill and the inputs; do not copy its methodology into the dispatch brief.
- **Reviewing streams with a shared or resumed reviewer session.** Each cluster review uses a fresh session (distinct-subtask isolation); anchored reviewers defeat independent validation.
- **Reporting unreviewed streams.** No research Workfile enters the report without a passing review.
- **Source-organized report.** The report is organized around the question; a per-cluster or per-source digest is not a report.
- **Boundary-free reporting.** A report that does not state what was not covered and what remains uncertain overstates its own authority.
- **Skipping the Final Review Gate.** The Deliverable (Response + Artifact) is user-facing output and must pass the gate like any other.
