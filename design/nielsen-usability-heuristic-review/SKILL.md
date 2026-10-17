---
name: nielsen-usability-heuristic-review
description: Reviews concrete interfaces, components, states, and user tasks using Jakob Nielsen's ten usability heuristics. Use when the user asks for a heuristic evaluation, usability review, interaction critique, task-flow assessment, or evidence-backed findings about feedback, consistency, error prevention, recovery, efficiency, minimalist design, or help.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository or artifact access. A live interface is preferred for behavioral claims; screenshots, prototypes, recordings, source, and existing findings may support a bounded review.
metadata:
  category: ui-ux-polish
  task_type: review
  audience: product-designers-ux-researchers-and-frontend-developers
  tags:
    - usability
    - heuristic-evaluation
    - nielsen-heuristics
    - interaction-design
    - user-flows
    - error-recovery
  status: draft
  side_effects: none
---

# Nielsen Usability Heuristic Review

## Purpose

Review an actual interface through Jakob Nielsen's ten usability heuristics and identify evidence-backed problems that impair a specific user task, state transition, outcome, or recovery path.

Use the heuristics as diagnostic lenses, not as ten independent issue quotas. Consolidate observations around root problems, preserve valid mappings to other frameworks, and return findings that can stand alone or feed a coordinated inclusive-interface audit.

## When to use this skill

Use this skill when:

- The user asks for a Nielsen heuristic evaluation, usability review, or interaction critique.
- A page, product, component, prototype, or flow needs review across normal, loading, empty, validation, error, success, cancellation, and recovery states.
- Users may struggle to understand system status, terminology, available actions, conventions, errors, shortcuts, or help.
- A release review needs task-specific usability findings rather than a generic checklist.
- Existing audit findings need a Nielsen-heuristic mapping without duplicating their root issues.
- An orchestrated accessibility and UX audit selects usability heuristics as one specialist lens.

Do not use this skill when:

- The user wants only a general explanation of the ten heuristics.
- No concrete interface, user task, flow, state, or representative artifact is available.
- The request is solely a WCAG conformance audit, visual-style critique, user-research study, or implementation task.
- The requested conclusion depends on participant behavior, frequency, analytics, or production conditions that the available evidence cannot establish.

## Operating rules

- Review representative user tasks and observable states, not heuristic names in isolation.
- Do not manufacture one finding for each heuristic. Record no issue when the inspected task supports no finding.
- Do not claim that expert review proves how all users behave or replaces usability testing.
- Do not infer dynamic behavior, timing, focus, persistence, or recovery from a static screenshot.
- Do not label a heuristic issue as a WCAG failure. Preserve a valid WCAG mapping established by dedicated accessibility evidence, but do not create one from heuristic similarity alone.
- Do not duplicate one root problem across heuristics, screens, personas, occurrences, or frameworks. Keep one stable root finding and attach all valid mappings and occurrences.
- Keep severity, confidence, status, and framework mappings distinct. Framework overlap does not increase severity by itself.
- Recommend outcomes and interaction behavior. Do not edit files or mutate the reviewed interface.

## Inputs to inspect

Start with the smallest evidence set that can establish the requested tasks and states:

- The review goal, target users, context of use, critical tasks, and completion conditions.
- Live pages, applications, components, prototypes, screenshots, recordings, or supplied interface artifacts.
- Entry, happy-path, alternate, cancellation, failure, and recovery flows.
- Default, hover, focus, active, selected, expanded, disabled, loading, empty, validation, error, success, partial-success, offline, timeout, permission, and undo states when relevant.
- Labels, navigation, controls, content, notifications, dialogs, forms, search, settings, help, and documentation involved in the task.
- Relevant source, routes, state management, validation, error handling, tests, stories, fixtures, requirements, and design specifications.
- Existing findings from accessibility, Universal Design, Norman-principle, support, research, or other usability reviews.

Record the evidence type, target version, environment, state, method, and important limitations. Do not read an entire repository when representative routes, components, stories, and task implementations are sufficient.

## Finding contract and framework boundary

Read `inclusive-interface-audit-orchestrator` before reviewing when it is available. Use its current shared finding contract, severity model, terminology, and synthesis rules.

When the orchestrator is unavailable, use this embedded contract for every finding:

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier; preserve an existing root ID when enriching a prior finding |
| `target` | Route, component, flow, task step, state, role, environment, and occurrence as applicable |
| `evidence` | Evidence type, method, locator, environment, starting state, action, and reproducible observation |
| `user_impact` | Affected users, impaired task, consequence, and available workaround |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk` |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact |
| `confidence` | `high`, `medium`, or `low`, with the reason and missing evidence |
| `framework_mappings` | Zero or more valid Nielsen heuristics or other framework criteria, each with rationale and provenance when inherited |
| `recommendation` | Outcome-focused remediation guidance, constraints, and responsible interface surface |
| `verification` | Retest setup, steps, expected result, method, environment, and closure evidence |

Use `source_skill`, `related_ids`, and `root_cause` as optional traceability fields.

Apply these framework boundaries:

- Add one or more Nielsen heuristic mappings to a root finding only when each mapping explains the observed behavior and user impact.
- Select one primary heuristic when it best explains the problem. Treat other heuristics as supporting mappings, not additional findings.
- Preserve valid existing framework mappings and their rationale when consolidating findings.
- Leave unsupported mappings empty. Put possible relationships that need specialist evidence in coverage gaps, not in the validated mapping list.
- Preserve a specific WCAG mapping only when a dedicated accessibility review supplied adequate criterion-level evidence. This heuristic review must not independently declare a WCAG failure.
- Keep similar symptoms separate when they have different root causes, user consequences, remedies, or verification methods.

## Review model

Apply every heuristic to the relevant task steps and states. Record findings only where evidence supports a consequential breakdown.

### 1. Visibility of system status

Determine whether the interface communicates current state, receipt of action, progress, scope, success, failure, and persistence in useful time. Inspect loading, saving, uploading, processing, optimistic updates, background refreshes, route changes, delayed outcomes, and transient feedback.

### 2. Match between the system and the real world

Determine whether language, concepts, ordering, groupings, units, icons, and workflows match the user's domain and expected sequence. Distinguish an implementation model from the mental model the interface teaches.

### 3. User control and freedom

Determine whether users can leave unwanted states and recover from accidental actions through cancel, back, close, edit, undo, retry, restore, or safe interruption. Check for traps, unexpected mode changes, premature commitment, and irreversible actions.

### 4. Consistency and standards

Determine whether the same words, controls, behaviors, placements, and outcomes mean the same thing across the product. Check established platform, web, domain, and product conventions while allowing intentional deviations that improve the task and are clearly signified.

### 5. Error prevention

Determine whether the interface prevents likely slips and misunderstandings before they become errors. Inspect constraints, safe defaults, previews, input boundaries, validation timing, destructive scope, duplicate submission, ambiguity, and confirmation only where consequence justifies interruption.

### 6. Recognition rather than recall

Determine whether options, instructions, context, prior choices, constraints, and next steps remain visible or easy to retrieve when needed. Check whether the task unnecessarily requires remembering information across screens, modes, time, or documentation.

### 7. Flexibility and efficiency of use

Determine whether both infrequent and experienced users can complete repeated or complex tasks efficiently. Inspect accelerators, shortcuts, sensible defaults, saved preferences, bulk actions, search, filtering, autofill, customization, and learnable expert paths without weakening the primary path.

### 8. Aesthetic and minimalist design

Determine whether each visible element supports the current task or competes with more important information and actions. Review hierarchy, progressive disclosure, density, redundancy, interruption, and signal-to-noise. Do not equate minimalism with removing necessary context, status, labels, help, or recovery controls.

### 9. Help users recognize, diagnose, and recover from errors

Determine whether errors are noticeable, expressed in task language, tied to the affected action or field, and paired with a viable next step. Check whether the interface preserves work, distinguishes temporary from permanent failure, explains partial or unknown outcomes, and supports recovery without exposing raw implementation details as the only explanation.

### 10. Help and documentation

Determine whether users can find concise, task-focused help when the interface cannot reasonably be self-explanatory. Inspect contextual guidance, onboarding, examples, search, support routes, troubleshooting, terminology, and instructions for complex, unfamiliar, or infrequent tasks. Do not require documentation to compensate for a preventable interface problem.

## Workflow

1. **Frame the review.**
   - Identify the target, user, context, primary decision, critical tasks, and completion conditions.
   - Define in-scope routes, components, roles, devices, input methods, states, and evidence.
   - State exclusions and evidence limitations.
   - Establish whether the shared contract comes from the orchestrator or the embedded fallback.

2. **Select representative tasks and states.**
   - Prioritize critical, frequent, error-prone, recovery-sensitive, and unfamiliar tasks.
   - Include the primary path plus relevant loading, empty, cancellation, validation, error, partial-success, permission, timeout, destructive, undo, and recovery states.
   - For large systems, sample materially different templates, roles, and interaction patterns and record expansion triggers.

3. **Trace each task end to end.**
   - Record the user's goal, starting state, available cues and actions, expected result, observed response, next step, and recovery option.
   - Inspect transitions between screens and states, not only static layouts.
   - Separate direct observations, source-supported behavior, documented intent, and inference.

4. **Apply the ten heuristics at task steps.**
   - Ask which heuristics explain an observed point of friction, error risk, uncertainty, delay, abandonment, or recovery failure.
   - Capture evidence before assigning a heuristic.
   - Record effective behavior worth preserving as well as supported problems.
   - Mark a heuristic `not-verifiable` when the evidence cannot establish its relevant behavior.

5. **Consolidate root findings.**
   - Merge observations that share the same root cause, affected task, user consequence, remedy, and verification method.
   - Preserve all occurrences and valid framework mappings on the merged finding.
   - Reuse an existing root ID when this review adds a Nielsen mapping to a finding from another specialist.
   - Split findings when the remedy or closure evidence must be independently owned or tested.

6. **Assign status, severity, and confidence.**
- Base severity on task criticality, consequence, breadth, persistence, workaround quality, reversibility, and potential harm.
- Use `critical` for catastrophic or unsafe failure in a critical task with no practical recovery; `high` for a blocked or materially corrupted important task; `medium` for substantial but recoverable friction or error risk; `low` for localized friction; and `advisory` for an evidence gap or improvement without demonstrated task impairment.
- Assign confidence from the strength and reproducibility of evidence, and state what is missing.
- Treat `accepted-risk` as a documented product decision, not a status the reviewer assigns unilaterally.
- Do not use the number of heuristic mappings as severity.

7. **Recommend the smallest coherent correction.**
   - Tie the recommendation to the root cause and affected task.
   - State what should change, where and when it should appear, and what users should be able to understand, predict, complete, or recover from afterward.
   - Preserve effective conventions and name trade-offs introduced by added feedback, flexibility, constraint, or content.
   - Avoid vague advice such as `make it intuitive`, `simplify`, or `improve usability`.

8. **Define verification.**
   - Specify starting conditions, user goal, action sequence, relevant role and state, environment, expected response, and evidence required to close the finding.
   - Use task-based participant testing when a recommendation depends on comprehension or performance that expert inspection cannot prove.
   - Keep untested assumptions visible.

9. **Report coverage and synthesis.**
   - Summarize affected tasks and cross-cutting root causes before heuristic counts.
   - Provide a task-scoped heuristic coverage record linked to evidence and finding IDs.
   - List unreviewed tasks, states, roles, environments, and evidence gaps.
   - Do not present representative sampling as complete product coverage.

## Output format

Return:

```md
## Review brief

- Target and version:
- User and context:
- Critical tasks:
- In scope:
- Out of scope:
- Evidence and methods:
- Contract source: `inclusive-interface-audit-orchestrator` | embedded fallback
- Limitations:

## Task and state coverage

| Task ID | User goal | Path and states reviewed | Evidence method | Limitations |
|---|---|---|---|---|

## Root findings

### NUH-001 — Concise root problem

- **id:** `NUH-001`
- **target:** Route, component, flow, task step, state, role, environment, and occurrences.
- **evidence:** Evidence type, locator, setup, action, expected behavior, and observed result.
- **user_impact:** Affected users, impaired task, consequence, and workaround.
- **status:** confirmed | provisional | needs-validation | not-reproduced | resolved | accepted-risk
- **severity:** critical | high | medium | low | advisory
- **confidence:** high | medium | low — reason and missing evidence.
- **framework_mappings:**
  - Nielsen heuristic — rationale.
  - Preserved valid mapping with provenance and rationale, when applicable.
- **recommendation:** Outcome-focused change, constraints, and responsible surface.
- **verification:** Retest setup, steps, expected result, method, environment, and closure evidence.
- **source_skill:** `nielsen-usability-heuristic-review`
- **related_ids:** Optional existing or related root IDs.
- **root_cause:** Optional concise cause shared by the occurrences.

## Heuristic coverage record

| Heuristic | Tasks and states assessed | Result | Evidence or finding IDs |
|---|---|---|---|

Use `supported-finding`, `no-supported-finding`, `not-verifiable`, or `not-applicable` in the result column. This is a task-specific coverage record, not a generic checklist or ten-item issue count.

## Evidence-backed strengths

- Effective behavior and conventions worth preserving.

## Coverage gaps and next verification

- Unreviewed tasks, states, roles, environments, conflicts, and required evidence.
```

Omit optional finding fields when they add no traceability value. If no root findings are supported, say so; still return the reviewed scope, task and heuristic coverage, strengths, and evidence limitations.

## Quality bar

The task is complete only when:

- The review names concrete users, tasks, interfaces, states, transitions, and evidence.
- All ten heuristics are considered against applicable task steps without forcing one issue per heuristic.
- Every finding follows the shared or embedded contract and identifies one evidence-backed root problem.
- Findings preserve occurrences and valid framework mappings without duplicate IDs or issue counts.
- Heuristic findings are not mislabeled as WCAG failures.
- Severity reflects user and task impact; confidence reflects evidence strength; status reflects lifecycle.
- Recommendations are specific, outcome-focused, and paired with reproducible verification.
- Direct observation, source-supported behavior, documented intent, and inference remain distinguishable.
- Strengths, unreviewed scope, and missing evidence are explicit.
- The result remains independently usable when the orchestrator is unavailable.

## Edge cases

- **Static screenshots only:** Review visible wording, hierarchy, apparent conventions, available choices, and captured states. Mark timing, transitions, persistence, recovery, and hidden actions as not verifiable.
- **Source without a runnable interface:** Report source-supported behavior separately from observed experience and require runtime verification for rendered states and timing.
- **Prototype without real services:** Review represented flows and concepts while marking production loading, failure, persistence, permissions, and recovery as unverified.
- **No task definition:** Derive only a provisional task from visible evidence, label the assumption, and avoid product-wide conclusions.
- **Existing normalized findings:** Preserve root IDs, evidence, occurrences, and valid mappings. Add Nielsen mappings only when they explain the same cause and consequence.
- **Multiple roles, locales, or devices:** Separate materially different task paths, then merge only findings with the same root cause and remedy.
- **Intentional friction:** Do not flag necessary safety, privacy, permission, or legal constraints merely because they slow the task. Review whether purpose, scope, and release conditions are understandable.
- **Expert tools:** Preserve efficient density and shortcuts when they serve the target users; assess learnability and recovery without forcing novice-oriented simplification.
- **Help compensates for poor design:** Keep the interface problem as the root finding. Treat documentation as support, not as a substitute for preventable design repair.
- **Potential accessibility overlap:** Record an evidence gap or preserve a mapping from a dedicated accessibility review. Do not make a new WCAG claim.
- **Conflicting evidence:** Keep the conflict visible, lower confidence as appropriate, and specify the evidence needed to resolve it.

## Related skills

- `inclusive-interface-audit-orchestrator` — coordinate specialist scope, shared findings, and final synthesis.
- `norman-interaction-principles-review`
- `interface-state-coverage-review`
- `user-recovery-flow-planner`
- `microcopy-polish`
