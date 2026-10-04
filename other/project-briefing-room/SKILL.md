---
name: project-briefing-room
description: Thin orchestration skill for stakeholder-facing project briefings. Use when the user wants Codex to explain the current repo/task status in plain language, present architecture/progress/requirements/tests/risks as a meeting-style briefing, then use or follow codex-deep-interview for feedback clarification and codex-consensus-plan for the next execution plan. Do not use as a generic code review, repo scanner, requirements interview, or implementation planner.
---

# Project Briefing Room

Use this skill as a thin meeting-style orchestration layer. Codex already knows how to inspect code, interview users, and plan implementation. This skill only defines the briefing shape and when to hand off to those existing abilities.

## Role

Translate the current repo/task situation into a stakeholder briefing, then route the conversation:

1. Codex reads the current repo/task context itself.
2. Codex gives a plain-language stakeholder briefing in chat.
3. Codex uses or follows `$codex-deep-interview` to clarify the user's feedback.
4. Codex uses or follows `$codex-consensus-plan` to form the execution plan.

Do not make the user open generated files before they can respond. Files may be used as evidence after the chat briefing, not as the primary interface.

## Workflow

### 1. Gather Context

Inspect the current workspace before briefing:

- `README.md`, `plan.md`, `DESIGN.md`, release notes, handoff docs, or task docs when present
- `git status`, changed files, recent tests, and relevant artifacts
- source files only as needed to understand architecture, progress, requirements, experiments, and risks

Prefer repo facts over asking the user. Do not run broad or expensive commands unless the task needs them.

### 2. Brief In Chat

Present the briefing directly in the conversation. Keep it concise and stakeholder-facing.

Use this fixed structure:

```markdown
**Project Briefing**
1. Goal: what this project or task is trying to accomplish.
2. Current State: what is done, in progress, blocked, or uncertain.
3. Architecture: the main moving parts and how they relate, in plain language.
4. Requirement Fit: which stated needs appear met, partial, unmet, or unknown.
5. Evidence: tests, artifacts, commands, or files that support the status.
6. Risks: the decisions or uncertainties that could change the next step.
7. Recommended Next Step: what Codex would do next if the user agrees.
```

Use a small diagram only when it makes the architecture or workflow easier to understand. A simple Mermaid diagram in chat is enough.

### 3. Ask For Feedback

After the briefing, ask one open feedback question:

```text
What does not match your expected direction, or what should we adjust first?
```

Do not begin with a checklist of internal workflow questions.

### 4. Clarify Feedback

When the user responds, use or follow `$codex-deep-interview`:

- Restate the user's concern in concrete terms.
- Classify whether it changes direction, scope, priority, requirement, risk, evidence, or acceptance.
- Ask at most one concise follow-up question at a time when clarification is required.
- Explain what decision the answer will change.
- Stop clarifying once the next action is clear.

Do not ask generic questions such as where to write artifacts, which sections should pause, or which comments should block execution unless the user's feedback specifically makes that decision material.

### 5. Plan Execution

When the user's intent is clear, use or follow `$codex-consensus-plan`:

- Produce a decision-complete plan before implementation.
- Include key changes, verification, assumptions, and out-of-scope items.
- Tie plan changes to the stakeholder feedback and repo evidence.
- Ask for confirmation before editing code when the change is high-impact or direction-changing.

### 6. Optional Artifact Capture

Only after the chat flow is useful, optionally write a short meeting record when the user wants one.

Artifacts are secondary and should not be required for the user to understand or answer the briefing.

Acceptable artifacts:

- a short decision record
- a revised `plan.md` section
- a bounded feedback summary
- evidence pointers to relevant files, tests, or generated reports

Do not store secrets, raw audio, full transcripts, cookies, local storage, meeting start URLs, or unredacted provider tokens.

## Boundaries

Do not duplicate existing skills:

- Use Codex's native code reading and review ability for repo inspection.
- Use or follow `$codex-deep-interview` for clarification.
- Use or follow `$codex-consensus-plan` for implementation planning.
- Use or follow `$codex-completion-loop` only if the user asks Codex to carry the work through implementation.

This skill is not a code review, not a standalone planning framework, not a live meeting runtime, and not an automated execution gate.

## Completion Criteria

A successful Project Briefing Room interaction has:

- a stakeholder-readable briefing in chat
- one open feedback prompt after the briefing
- clarified user intent when needed
- a consensus-style execution plan when the user wants to continue
- optional artifacts only after the user-facing conversation is clear
