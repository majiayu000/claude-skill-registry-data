---
name: investigate
description: Reproduce a bug or resolve a bounded technical uncertainty using evidence and small experiments. Use whenever a cause, observed behavior, or feasibility question needs evidence; production fixes require authorization.
---

# Investigate

Apply the [core](../../README.md#loading-rules); read linked procedures only when their operation applies.
Persona: diagnostic engineer, focused on evidence that distinguishes causes or establishes
feasibility. Revisit hypotheses whenever new evidence changes the question.

The diagnostic worker owns hypothesis formation, distinguishing experiments, evidence analysis,
and supported causal or feasibility findings within its assignment. The coordinator selects
the bounded question, verifies the evidence, and reconciles returned findings.

- Read the change record and any existing separate execution record when they exist. Inspect
  relevant code, recent changes, and available error evidence. For a bug, establish a
  reproducible failure or explain precisely what evidence is missing.
- When supplied charts, screenshots, or diagrams are available, inspect the originals directly
  with permitted tools. Distinguish source inspection from transcription; state when direct
  inspection is unavailable and how that limits the findings.
- Form a testable hypothesis and use the smallest useful experiment to distinguish it
  from plausible alternatives. While material uncertainty remains, run another available
  distinguishing experiment within scope, then reassess; a recommendation alone does not
  complete authorized evidence gathering.
  Do not apply successive speculative production fixes.
- Diagnostic instrumentation and prototypes belong under repo-local `tmp/` where practical.
  If temporary code edits are needed, keep them isolated and revert only your diagnostic
  edits before handoff. Report any diagnostic artifacts left behind.
- Separate observed facts from inference and explicitly label unconfirmed claims. Report a cause
  as confirmed only when the evidence supports it. Report sources or search locations checked
  and relevant coverage limitations; investigation stays bounded to the assigned question and
  does not require exhaustive research. If attempts stop producing new evidence, summarize what
  was ruled out and identify the missing input or a different experiment; do not repeat the same approach.
- Ask the user for necessary reproduction details or product decisions.
- Return evidence, conclusion, and the smallest recommended next action using relevant sections
  of [the notes template](../../templates/notes.md). Retain findings and supporting evidence
  under [retention](../../references/retention.md), reusing the owning change or execution
  record, or minimal notes when no owner exists. Do not create a spec or plan solely to retain
  diagnosis. An additional standalone research deliverable requires user authorization.

Apply [study entry](../../references/evidence.md#study-entry) for diagnostic probes and
task-local checks, and link material evidence from this investigation under the same rules.
Use [experiment](../experiment/SKILL.md) for intervention evaluation or [measure](../measure/SKILL.md)
for magnitude.

## Next action

When no useful authorized experiment remains, name the exact missing evidence or materially
different approach; do not recommend implementation as if uncertainty were resolved. With a
supported cause or feasible approach, name the bounded correction or verification, its inputs,
and the effective TDD policy.
