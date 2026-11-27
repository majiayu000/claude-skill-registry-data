---
name: hoa-skill-review
description: >-
  Audit one SKILL.md, its diff or candidate replies without editing the subject. When scoring
  answers against a rubric or reviewing behavior, inspect referenced files, trace actual downstream
  consumers and separate proven findings from untested risks. Not for hoa-skill-set-audit.
metadata:
  revision: "5"
  areas: "software-development,work-management,self-management"
  targets: "runtime-agnostic"
  summary: "review skill behavior and changes against consumer evidence without editing the target"
  summary_zh: "依据消费者证据审计 skill 行为与修改，不改动被审查对象"
  kind: "entry"
---

# hoa-skill-review

**Outcome:** Give the skill author or output decision-maker an evidence-ranked assessment of whether the intended behavior works for its next consumer, and the smallest supported decisions to make.

**Done:** The relevant contract and its reachable consumer path have been examined in proportion to the request; every finding meets its evidence floor; and the report separates paths actually verified from those not verified.

**Safe failure:** When a source, consumer, host, candidate context, or independent judge is unavailable, identify the exact limit and narrow the conclusion. Do not invent evidence, grade an unobservable result, claim an unrun behavior, or edit the reviewed subject.

## Boundary and review path

This is a read-only audit, change review, and output-judging skill. Inspect the subject, relevant references, fixtures, and consumer contracts. Non-writing checks or isolated prompts are useful only when their effects are known; do not modify the reviewed asset or its environment.

Start with the user's question and the smallest relevant boundary. For a changed block, inspect its diff, enough surrounding instructions to understand its contract, and the tests or fixtures that exercise that contract. Trace the relevant output into its next consumer when the finding depends on interpretation, parsing, activation, or handoff. For a whole-skill audit, inspect the main instructions and only the references and consumers reached by the behavior under review. Expand beyond that boundary only when evidence points to another dependency; a named diff does not require a full-repository audit.

Scale the review to the claim and consequence. Start with the target's contract and affected path; expand to consumers, fixtures, or real execution when the claim depends on them or a failure would be material. Before calling a rule missing or redundant, trace what it changes, account for the runtime and harness that may mask behavior, and diagnose the gap before prescribing a fix. A hypothetical already decided by a stated condition is not a finding.

Check what evidence actually demonstrates. A fixture may assert an intended rule without exercising its runtime. A forced skill invocation tests its body, not automatic activation. A mock or prompt simulation tests only the simulated interaction, not a real consumer, host, tool call, or protocol transition. Identify harness assumptions that could bake in the expected answer or omit the relevant context.

When behavior cannot be settled from available artifacts, or when candidate replies need grading, read [behavioral evaluation](references/evaluate.md). Static review alone is sufficient when it establishes the claim and consumer consequence without an execution-dependent assumption.

## Findings

Classify each finding by its evidence, not by how plausible it sounds. Order findings within each class by user or consumer impact.

- **Change** — A demonstrated gap. Cite a reproduced failure or the exact path that necessarily fails, explain the resulting user or consumer consequence, identify the owning layer, and state the smallest condition-based correction. Static evidence supports this class only when the failure follows necessarily from the inspected path.
- **Verify** — A concrete risk that could change the conclusion but still needs a named reproduction or trace. State what is uncertain and the specific check that would resolve it; do not prescribe a fix yet.
- **Consider** — An unproved improvement. Explain its plausible value and why the evidence does not establish a defect or required change.

Do not turn a missing observation into a Change. If the necessary path cannot be reproduced or shown to fail, classify it as Verify. Do not report an enhancement as a defect merely because another design is possible.

## Report

Return the conclusion, the scope actually inspected, and findings under Change, Verify, and Consider as applicable. For each item, include the affected file/block or candidate, the evidence, and the consequence; a Change also needs its owner and smallest condition-based fix. Keep the rationale complete enough for a separate author to act without reconstructing unstated assumptions.

List **Verified paths** and **Unverified paths** separately. A deterministic static trace may verify that an inspected path necessarily fails; label it **statically established**, not runtime-exercised. Reserve **runtime-verified** for an observed run. Name the host, consumer, fixture, simulation, or static trace and make its evidence boundary explicit. Put unavailable hosts, unexecuted triggers, mocked boundaries, ambiguous candidate contexts, and runtime or consumer behavior conclusions based only on static inspection under Unverified paths. Never imply that a simulation proves automatic activation or real downstream behavior.

## Protocol integrity of one workflow skill

When asked to make a workflow skill more general, check whether one protocol lives in several
files and has drifted. Keep the judgment scoped to the skill under review:

1. **Inventory the protocol.** Count lines in the body, references and profiles. Read headings
   of named peers to see whether they restate the same stage order or gate.
2. **Count copies.** Search the skill tree for a distinctive role marker, wrapper command or
   gate script name. Inspect hits to distinguish independent definitions from references.
3. **Check current defaults.** Compare stated transports, commands and configuration with
   their effective values. Report stale claims as Change findings.
4. **Compare same-purpose scripts.** Normalize whitespace to spot copies, then verify behavior
   and callers before recommending deletion.
5. **Check profiles against real projects.** Verify that active projects have needed profiles and
   that profiles carry only local deltas, not competing protocol definitions.
6. **Check recovery where interruption matters.** Verify persistent per-increment state and a
   ledger that records review rounds and durations.

Deliver counts, duplication and drift evidence, and two or three options sized by effort. Do not
rewrite the skill during review.

## Optional routes

Use `hoa-skill-create` when the user requests skill creation or evolution; this review does not
acquire write authority from that handoff. For keep, merge or cut verdicts across a skill set,
suggest the user run the explicit-only `hoa-skill-set-audit`; the model cannot invoke it. For
qualifying recurring work from history, suggest the user run the explicit-only `hoa-practice-retro`
instead. If a route is unavailable, finish within this skill's boundary and report the limit.

## Provenance

The portable package and progressive-disclosure conventions follow the [Agent Skills specification](https://agentskills.io/specification). The evidence-based Change, Verify, and Consider findings and risk-scaled diagnose-before-prescribing method adapt the public [CE Skill Work review guidance](https://github.com/EveryInc/compound-engineering-plugin/blob/main/.agents/skills/ce-skill-work/references/review-skill.md). The evaluation discipline adapts the public [Anthropic skill-creator evaluation guidance](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md); this package is an independent adaptation of those principles.
