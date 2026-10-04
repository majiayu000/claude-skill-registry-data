---
name: review-llm-annotations-and-improve-prompt
description: Analyze development-set disagreements between human annotations and one Coval text LLM judge, then propose a focused prompt revision. Use coval-calibrate-metric for independent trust measurements.
argument-hint: "<project-id> <metric-id>"
---

# Improve a metric from reviewed disagreements

Use this for development, not to declare a judge calibrated. When the goal is a
trust or release claim, use `coval-calibrate-metric` if installed. This workflow
remains usable by itself with the boundaries below.

Confirm organization/workspace and one text judge metric. Read its definition,
version, project and completed human annotations using current CLI `context`
and `--help`. Binary, categorical and numerical text judges require different
error analysis; don't silently coerce one type into another.

Collect actual completed human labels and reviewer notes, exact machine output
IDs/versions and the relevant transcripts. Paginate the public reviews API when
the CLI can't prove completeness. Zero is a valid label; null or pending is
missing. AI-suggested labels are not human ground truth. Multiple reviewers on
one call need adjudication, not duplicate counting. Annotation `simulation_output_id` can identify an uploaded
conversation; retain the source collection and retrieve original metrics through
its matching public API/CLI resource.

Separate related calls into train (prompt examples), development and untouched
test groups before tuning. Inspect only the development disagreements and an
agreement sample. For binary judges include failure detection and pass recall,
not just raw agreement. For numerical judges fix tolerance before inspecting
scores; don't widen it to improve agreement. For categorical judges show the
actual confusion counts.

Read each disagreement against the rubric. The human or the judge may be wrong;
a domain expert must adjudicate a disputed human label. Never offer “make all
human labels match the machine” as a shortcut. Preserve original labels and notes.

Draft the smallest prompt change supported by observed evidence. Preserve the
criterion, output type and successful boundaries. Include only train examples;
never leak held-out examples into the prompt. Show the old/new prompt and affected
failure pattern before seeking any missing update authority. Prefer a separate
candidate metric so production defaults and historical comparison stay intact.

Use a bounded `coval --agent metrics test <candidate-id>
--simulation-output-ids <ids>` request to score existing outputs when authorized.
Inspect per-item responses and poll each returned `metric_output_ulid` using
`simulated-conversations metric-detail <simulation-id> <output-ulid>` or
`GET /v1/conversations/simulated/{simulation_id}/metrics/{metric_output_id}`.
The API exposes `explanation`; don't print credentials or use an invented nested
outputs route. Count re-scores against the agreed metric budget and stop on
ambiguity rather than enqueueing duplicates.

Report development changes and remaining errors. Freeze the candidate before
measuring it once on untouched human-labeled groups. Without that evidence, say
“prompt candidate improved on development examples,” not “validated judge.” No
automatic resimulation, human-label edits, default attachment or notifications.
