---
name: grill-me
description: Pressure-test an existing plan or design artifact until it is coherent enough for the next workflow step or plainly blocked. Use when the user wants to be grilled on a plan, design doc, PRD, ADR, rollout plan, migration runbook, rolling-wave project shape, or slice contract; when they say "grill me"; or when Codex should interrogate a source-of-truth artifact, inspect code and adjacent docs before asking, auto-answer evidence-backed questions, ask only about conflicts or low-confidence recommendations, edit the original file in place, preserve the artifact's existing format, and keep conclusions, blockers, readiness, and deferred work synchronized in the document.
---

# Grill Me

Pressure-test one source-of-truth artifact until it is coherent enough to proceed or plainly blocked.
Edit the artifact directly. Do not keep critical state only in chat.

## Required Workflow

1. Select one source-of-truth file.
- Use the file the user names.
- If the user does not name a file and there is exactly one credible candidate, state that selection and proceed.
- If multiple plausible files exist, force explicit selection before editing.
- Prefer repairing the existing artifact. Create a new artifact only when no usable source exists or the format is unsafe to edit directly.

2. Inspect before asking.
- Read the artifact first.
- Read relevant code, docs, tests, configs, or adjacent plans aggressively whenever they can answer a question from evidence instead of user memory.
- Resolve anything you can from disk before asking the user.
- Classify the artifact scope before grilling:
  - `project-shape`: `docs/rolling-wave/{project}/project.md` or an artifact with finish line, success criteria, scope, and roadmap.
  - `slice-contract`: `docs/rolling-wave/{project}/slices/NNN-slug.md` or an artifact with original slice contract, acceptance criteria, and implementation notes.
  - `other-plan`: any other source-of-truth plan.
- Keep the interrogation depth matched to that scope.

### Project-Shape Scope

When grilling a rolling-wave `project.md` or other project-shape artifact, focus on global shape:
- finish line
- success criteria
- scope and non-goals
- constraints and assumptions
- roadmap order
- slice granularity
- dependency flow between slices
- whether broad slices should split into separate review decisions or become child rolling-wave projects
- cross-slice risks, decisions, and open questions

Do not grill deep future slices for behavior, file choices, implementation approach, exact tests, edge cases, or detailed acceptance criteria unless that detail changes the global finish line, scope, roadmap order, dependency structure, or reviewability of the slice map. Future slice details belong to `prepare-next-slice` when that slice becomes current.

For project-shape artifacts, a slice is good enough when it is a concrete implementation step fitting one bounded human review decision. Multiple independently useful, executable, or revertible chunks may stay together when one intent or transformation recipe, risk class, and verification strategy cover them. Mechanical batches may cross domains. Split separate approval decisions, unrelated mental models, distinct risk classes, or materially different verification strategies. It does not need a full slice contract yet.

For project-shape artifacts, stop once the global finish line, scope, roadmap order, and next slice are clear enough for `prepare-next-slice`. Do not keep grilling just because future slices still have implementation uncertainty.

### Slice-Contract Scope

When grilling a slice contract, grill slice-level behavior, verification intent, expected intermediate state, minimum implementation, execution fit, risks, and scope boundaries until the slice is ready to implement.

### Prepare-Review Mode

Use this bounded mode only when `prepare-next-slice` explicitly requests `prepare-review`.

- Apply the preparation readiness bar, not the full generic grill checklist.
- Read the slice, parent project, direct dependencies, and supplied neutral evidence index first.
- Check behavior and scope, dependency order, user-facing or irreversible decisions, review coherence, safe deferrals, and one credible failure mode.
- Validate representative high-risk claims. Do not recreate exhaustive consumer, import, generated-registration, or dependency inventories unless implementation requires an exact finite list.
- Use a soft budget of about three minutes and twelve repository queries. Batch searches. When the budget is exhausted, return the highest-leverage `question`, `blocked`, or `redirect` instead of continuing broad exploration.
- Return `redirect` only when a prerequisite or replacement slice is required for an honest contract. Draft that slice, update material roadmap/dependency state, keep it `pending`, and include a neutral evidence index.
- Stop as soon as required branches are resolved or safely deferred. Optional polish and final completeness proof do not block readiness.

3. Preserve the artifact's native format while making it usable as a source of truth.
- Do not rewrite the artifact into this skill's preferred template.
- Keep the document's existing section names, ordering, style, and level of formality unless that structure is actively hiding contradictions or unresolved decisions.
- Add missing tracking information where it naturally belongs in the current format: readiness, blockers, open questions, assumptions, dependencies, deferred work, or explicit out-of-scope items.
- If the artifact already has equivalents for those concepts, update those existing sections instead of creating new standardized sections.
- Add a new section only when there is no reasonable place for the information and the missing state would otherwise live only in chat.
- Reorganize only the smallest necessary part when the current structure hides dependencies, duplicates one decision across sections, or makes the plan impossible to verify.

4. Run a strict interrogation loop.
- Resolve evidence-backed branches from the artifact or codebase before involving the user.
- Auto-answer and continue when the recommended answer is defensible from existing research, code, docs, tests, configs, or artifact text.
- Surface auto-answers in chat and in the artifact, but do not require user confirmation for them.
- Ask the user only when evidence conflicts, the recommendation depends on unstated intent, or confidence in the recommended answer is low.
- Sync the source file before each question or auto-continued branch so it remains the source of truth.
- In chat, state `current node`, `auto-resolved`, `evidence`, `next question`, and `recommended answer` as applicable. Skip empty parts. Always include a recommended answer when asking.
- If the user replies `lgtm`, treat that as accepting the most recent recommended answer unless they also include conflicting instructions.
- Ask at most one question per message. If no question is needed, continue resolving the next highest-risk branch without stopping.
- Choose the next branch dynamically by risk and dependency leverage. Use the checklist in [references/checklist.md](references/checklist.md) as coverage control except in bounded `prepare-review` mode.
- If the scoped artifact is project-shape, choose branches from global project and roadmap risk. Do not choose a branch solely because a deep future slice lacks implementation detail.
- If the scoped artifact is project-shape, default to at most 1-3 high-leverage user questions in one grill pass. Ask more only when unresolved issues materially change finish line, scope, first slice, public behavior, reversibility, or major project risk.
- Ask what would have to be true for the current branch to fail whenever a branch starts to look settled and cannot be answered confidently from evidence. In `prepare-review`, do this once for the highest-risk branch.

5. Reject weak answers.
- Treat vague, evasive, or hand-wavy answers as insufficient.
- Say why the answer is weak and ask the sharper follow-up needed to force a real decision.
- Accept deferral only when it is concrete: record what is deferred, why it is safe to defer, what it blocks, who owns it, and what trigger or later PR forces resolution.
- Record cross-PR deferrals in `Explicitly Not Solved Here`.

6. Keep the file truthful.
- Edit the original file directly. Do not create a parallel "grilled" copy.
- Rewrite or delete obsolete or contradictory text immediately.
- Reopen an earlier branch immediately if later evidence invalidates it.
- Write unresolved questions into the artifact as first-class state only when they block progress, are explicitly deferred, or must be visible to a future agent. Do not add low-value open questions just to prove the grill was exhaustive.
- Separate facts, assumptions, and decisions whenever the document starts to conflate them.
- Record concise file references when evidence materially affects a conclusion.

7. Stay inside planning mode.
- Inspect code aggressively for evidence, except when bounded `prepare-review` calls for targeted validation.
- Do not implement code or make product changes while using this skill.
- Do not drift into brainstorming by default. Propose an alternative only when the current branch is internally inconsistent, clearly under-specified, or dominated by a better option.

## Tone

- Be blunt, skeptical, and unsentimental.
- Do not praise, reassure, or soften the critique with filler.
- Do not hedge when the document is weak. State the weakness plainly.

## Completion

- Stop when all material branches in scope are resolved, explicitly deferred, ruled out as irrelevant, or the artifact is ready enough for the next workflow step.
- For project-shape artifacts, "ready enough" means `prepare-next-slice` can safely prepare the next planned slice with any remaining uncertainty recorded as assumptions, risks, or safe deferrals.
- Stop earlier if the user tells you to stop.
- End with a short closeout in chat: whether the scoped plan is ready to proceed, what remains unresolved, and which file is the source of truth.
- Omit routine caveats for planning-doc-only edits. Do not say that no code tests were run or that the edited planning path is gitignored unless the user asked about verification, persistence, or file visibility, or unless an attempted validation step failed.
