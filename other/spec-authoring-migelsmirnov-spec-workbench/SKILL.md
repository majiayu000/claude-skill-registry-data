---
name: spec-authoring
description: Guide layered creation and legacy migration of global_spec.json according to SPEC_STANDARD.md, including evidence-first recovery of hidden decisions, while preventing placeholder architecture, majority inference, premature contracts, vague notes, and top-down skeleton specifications.
---

# Spec Authoring

This page is an entry, not the method. The format is [SPEC_STANDARD.md](SPEC_STANDARD.md) and it is
normative. The method reaches you one phase at a time, from the pipeline — do not read ahead.

## How to work

1. Resolve the project: `python tools/workbench.py list`, then `python tools/workbench.py show <project>`.
2. Ask what comes next: `python tools/authoring.py next <project>`. It returns the phase, its **purpose**,
   the **gate** to run, what to **Read** (file and section) and what to **Ask**.
3. Read only what `Read:` names. Those are the sections of the standard and the procedures that bind in
   this phase.
4. Answer every `Ask:` question in the state document. They are the judgement no gate can make.
5. Run the gate. A finding names the rule it enforces and the fix. There are no warnings and no waivers
   (`tools/fence.py`): a finding that is not an error is an undecided fact. Then close the transition
   ([TRANSITION_PROTOCOL.md](TRANSITION_PROTOCOL.md)): what the phase owns, the obligations earlier states
   carried to it (`layer` in `next`), and what it carries on, to whom, confirmed by what. `not_checked` is
   never a pass.
6. Ask a model what the state still leaves open, as the generator would: the `questions:` command of the phase
   (`python tools/design_questions.py ask examples/<case> --state <N>`), States 0–7, one round per change: a
   unit (a section, a decision, a State 7 module prompt) closes when its latest round raised no contradiction
   and every other judged topic has a disposition (`dispose`) — [QUESTIONS.md](QUESTIONS.md). Gates see form; only this
   sees a decision nobody made. After State 5, `next` and Stage 9 admission (`FA019`) stop at any state
   a later edit reopened.
7. Before export, `python tools/design_factory_slices.py examples/<case> --factory-root <factory> --project <name>`
   asks the Factory what it will cut, refuse and resolve — every stop at once, without a run.

## What holds in every phase

- Do not design the next layer while the current one hides an undecided thing behind a generic name, a
  generic type or vague prose. If contracts need a model that does not exist, return to models; if notes
  need behaviour nobody decided, return to rules or module design; if a module needs `utils`, return to
  responsibility design.
- Repair a decision in the earliest state that owns it, propagate it forward, and touch the assembled
  specification last.
- This is a semi-manual process with the owner. Do not produce a whole specification from a short idea,
  and do not silently resolve a recorded open question.
- A value reaches generated code by one of three paths (SPEC_STANDARD §15.3.1): an enum in `models`, a
  data-provider constant, a runtime setting. A fact with no path stays a design decision and does not enter
  the specification.
- The specification language is closed: no sections, note classes or markers beyond the standard.

## Where the rest lives

- Order of phases, and each phase's purpose, reading and questions:
  [authoring_sequence.json](authoring_sequence.json) — the machine source; explained in
  [AUTHORING_SEQUENCE.md](AUTHORING_SEQUENCE.md). A test keeps every named section real and every phase at
  five questions or fewer.
- Evidence procedures (`MODEL_IDENTITY_EVIDENCE.md`, `SECURITY_REVIEW_EVIDENCE.md`,
  `EXTERNAL_CONTRACT_EVIDENCE.md`, `LEGACY_MIGRATION_EVIDENCE.md`) and tool documents under `tools/`: read
  them when `next` names them.
- The 932-line text this page replaced is in git history (`git log -- skills/spec-authoring/SKILL.md`). Its
  requirements became gates, its navigation became `next`, its restatements of the standard became section
  references, and its judgement became the `Ask:` questions.
