---
name: playbook-creator
description: "Guide for designing and creating high-quality, reusable workflows using the playbook tool group. Use this skill when: (1) You want to capture a successful multi-step process for future reuse, (2) A user asks to 'create a playbook', 'automate this task', '세션 플레이북', or 'session playbook', (3) You need to design a structured automation workflow with clear inputs, outputs, and success criteria. Triggers: 'create playbook', 'automate this process', 'design workflow', '세션 플레이북', '세션 playbook', 'session playbook'."
---

# Playbook Creator

This skill provides a structured framework for designing and implementing High-Quality (HQ) reusable workflows. Playbooks transform transient task execution into persistent, repeatable automation.

## Core Workflow

To create an effective playbook, follow these sequential steps:

### 1. Identify the Goal and Success Criteria

A high-quality playbook must have a specific, measurable objective.
- **Goal**: What is the final state? (e.g., "Successfully deploy a React app to GitHub Pages")
- **Success Criteria**: What artifacts prove success? (e.g., "A 200 OK response from the live URL", "A 'build/' directory exists")

### 2. Design Atomic Steps

Break down the task into the smallest possible units of work that map to available tools.
- Each step should ideally call ONE tool.
- Use the **Pattern Reference** for common task structures: [workflow-patterns.md](references/workflow-patterns.md)

### 3. Map Data Flow and Dependencies

Define how data moves between steps using outputVariable and requiredData.
- **outputVariable**: Name the result of a step clearly (e.g., "extracted_source_code").
- **requiredData**: List the names of variables from previous steps that this step needs as input.
- Refer to the **Schema Reference** for JSON field details: [playbook-schema.md](references/playbook-schema.md)

### 4. Target Session & Pinning ("세션 플레이북")

Determine whether this playbook should be pinned to the active session or start a fresh session:
- **Session Playbook ("세션 플레이북" / "session playbook")**: When the user asks for a session playbook or asks to automate/save the current session's workflow, **always set `defaultTargetSession: { mode: 'pin' }`**.
  - `sessionId` can be omitted; the backend will automatically bind the caller's session ID.
- **Generic / Standalone Playbook**: Omit `defaultTargetSession` (or use `{ mode: 'self' }`) so clicking Start creates a fresh session.

### 5. Implementation and Registration

1. Draft the playbook JSON using the [playbook-template.json](assets/playbook-template.json) asset.
2. Call playbook__createPlaybook with your completed definition (include `defaultTargetSession: { mode: 'pin' }` if requested for this session).
3. (Optional) Test the playbook immediately using playbook__selectPlaybook.

## Best Practices

- **Granularity**: Avoid monolithic steps. Granular steps allow for better error recovery and observability.
- **Explicit Success**: Always define requiredArtifacts. This allows the system to verify completion automatically.
- **Traceability**: Use meaningful IDs for stepId (e.g., "npm_install" instead of "step_1") and outputVariable names.

## Quick Links

- [Playbook Schema & Tool Reference](references/playbook-schema.md)
- [High-Quality Workflow Patterns](references/workflow-patterns.md)
- [Playbook JSON Template](assets/playbook-template.json)
