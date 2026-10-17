---
name: spec-to-ux-tasks
description: |
  Extract UX tasks from a product spec and save as ux-tasks.md in the same spec folder.
  Use this skill when:
  - The user wants to generate UX work items from a spec
  - The user says "UX tasks", "what does UX need to do", "extract UX work", "UX deliverables"
  - The user wants to hand off a spec to the UX/design team
  - The user asks "what screens need designing" or "what UX decisions are open"
created_by: Aman Parmar
last_modified: 20-04-2026
version: 1.2
---

# Spec to UX Tasks

Read a product spec and extract all UX work items into a structured `ux-tasks.md` file in the same spec folder.

## Why this skill exists

Product specs describe functional requirements for engineering, but UX teams need a clear task list of what they must design, decide, or validate. This skill bridges that gap by scanning each spec section and generating prioritised UX tasks with context, acceptance criteria, and open questions.

## Input

The user provides:

1. **Spec source (required)** — one of:
   a. A spec file path (e.g., `docs/specs/NNN-feature-name/feature-name.md`)
   b. A feature name (e.g., "feature X") — resolve to the spec folder using an `epic-to-spec-map.yaml` index (or similar convention)
   c. A wiki/doc URL — pull the spec via your doc-to-markdown converter

2. **Meeting transcript (optional)** — a meeting URL or transcript ID from your meeting tool. If provided, fetch the transcript via the relevant MCP tool and cross-reference it with the spec to capture UX points discussed in the meeting that may not yet be in the spec.

## Output

A file named `ux-tasks.md` saved in the same folder as the spec:
```
NNN-feature-name/
  feature-name.md
  ux-tasks.md        <-- generated
```

## Step 1: Locate and read the spec

1. If the user gave a feature name, read your spec index (e.g., `epic-to-spec-map.yaml`) to resolve the folder path.
2. Read the full spec file.
3. Check `§1.1 Related Document` (or equivalent) for existing Figma links — carry these forward as references in relevant tasks.

## Step 1b: Fetch and cross-reference meeting transcript (if provided)

If the user provided a meeting link:

1. Extract the meeting identifier from the URL.
2. Authenticate with the meeting-tool MCP if not already authenticated.
3. Fetch the transcript using the meeting-tool's `get_meeting_transcript` with the meeting ID.
4. Scan the transcript for UX-relevant discussion points. Look for:
   a. **UX decisions discussed but not yet in spec** -- participants debating screen behaviour, component choices, interaction patterns
   b. **Constraints or requirements mentioned verbally** -- stakeholder remarks that add context to spec sections (e.g., "we won't show split screen on smaller devices because of screen size")
   c. **Action items assigned to UX** -- "[team member] will...", "UX team needs to...", "we'll check with design..."
   d. **Disagreements or open debates** -- where participants had different opinions that need UX resolution
   e. **Practical context** -- offline/online behaviour, device limitations, role-based UI differences
5. For each meeting-sourced point:
   a. If it matches an existing spec-sourced task, add the meeting context to that task's "Context" or "Open questions" field with a `(Meeting source)` tag
   b. If it's a new UX point not in the spec, create a new task with `(Meeting source)` in the context

**Important:** Meeting transcripts contain casual discussion, not formal requirements. Only extract points that have UX implications. Do not log engineering-only concerns (database tagging, API structure) unless they affect the user interface.

## Step 2: Extract UX tasks section by section

Scan the spec top to bottom. Apply these extraction rules per section:

### §1.3 Risks & Assumptions
- Each risk with a visual implication (offline states, fallback displays, error messages, badges) = **Edge Case UX** task.
- Each assumption that constrains the UI (e.g., "max 2 languages on screen") = note it as context in related tasks.

### §2.x Functional Requirements — Logic subsections
- Every new screen, pop-up, modal, toggle, control panel, menu item, badge, toast mentioned = **Screen Design** or **Component Design** task.
- Every state change (enabled/disabled/pending/hidden/greyed-out) = **Component Design** task for that state.
- Every user role with a different view (e.g., admin vs manager vs end-user) = separate **Screen Design** task per role.

### §2.x Functional Requirements — Flowcharts (Mermaid blocks)
- Each decision node (diamond) = a screen state or branch that needs UX treatment.
- Each terminal node = a final screen state that needs design.
- The overall flow = a **User Flow** task to create or validate the UX journey.

### §2.x Functional Requirements — Use Cases
- Each "As a [user], I want to..." = a **Usability Review** task to validate that the designed flow supports this scenario.

### §2.x — Explicit UX callouts
- Any text containing "UX to decide", "TBD by UX", "UX team to", "to be decided by UX", "options to consider" = **Interaction Decision** task.
- List the options from the spec verbatim in the "Open questions" field.

### §3 Personal Information (if present)
- Any new data collection, consent, or profile screens = **Screen Design** task.

### §4 Non-functional Requirements (if present)
- Performance thresholds that affect UX (loading times, response times) = **Edge Case UX** task for loading/skeleton states.
- Accessibility requirements = **Component Design** or **Usability Review** task.

### §5 Differences Table (if present)
- Each row showing platform-specific behaviour (tablet vs mobile vs web) = **Screen Design** task per platform variant.
- Each row showing old vs new behaviour = **Screen Design** task for the new state.

### §9 Open Questions (if present)
- Any OQ tagged to UX or design = **Interaction Decision** task.
- Any OQ that implies a screen or flow change = note as open question in the related task.

### Future Scope (scan entire spec)
Scan the entire spec for any mention of future phases, deferred work, or upcoming enhancements that have UX implications. Look for:
- Phrases: "future phase", "future release", "deferred to", "not in current scope", "planned for", "upcoming", "phase 2", "phase 3", "later version", "post-launch", "roadmap"
- Items in §5 Differences table marked as future (e.g., "Web (Future Phase)")
- Open questions that defer a decision to a later date
- Assumptions or risks that mention planned but unbuilt capabilities
- Items explicitly marked as "not in this version" or "not in V1"

Each future scope item = a **Future Scope** entry (NOT a regular task -- these do not have priorities or block current engineering). These are logged so the UX team knows what is coming and can factor it into current designs for forward compatibility.

## Step 3: Assign priority

For each extracted task:

1. **High** — Blocks engineering. No wireframe exists AND engineering cannot start this section without UX output. Includes all Interaction Decision tasks where the spec explicitly says "UX to decide".

2. **Medium** — Engineering can start but needs UX before completion. Edge case states, loading indicators, secondary flows.
3. **Low** — Polish and validation. Usability review of flows that already have wireframes, micro-interactions, animation details.

Cross-check with Figma links from §1.1:
- If a Figma link exists for a section, tasks from that section are at most **Medium** (design exists, may need updates).
- If no Figma link exists, tasks from that section are at least **Medium**.

## Step 4: Deduplicate and group

1. Merge tasks that refer to the same screen or component (e.g., "Admin control panel" from §2.1 logic + §2.1 flowchart + §5 differences = one Screen Design task with all context combined).
2. Group tasks by type in this order: Screen Design, Interaction Decision, User Flow, Component Design, Edge Case UX, Usability Review. Future Scope items go in a separate section at the end (not mixed with active tasks).
3. Number active tasks sequentially: UX-001, UX-002, etc. Number future scope items separately: FS-001, FS-002, etc.

## Step 5: Write ux-tasks.md

Use this exact format:

```markdown
# UX Tasks -- {Feature Name}

> Spec: `NNN-feature-name/feature-name.md`
> Wiki: [{Spec Page Title}]({wiki_url})
> Generated: DD-MM-YYYY
> Total tasks: N (H High, M Medium, L Low)

---

## Summary

| Task Type | Count | High | Medium | Low |
|---|---|---|---|---|
| Screen Design | X | X | X | X |
| Interaction Decision | X | X | X | X |
| User Flow | X | X | X | X |
| Component Design | X | X | X | X |
| Edge Case UX | X | X | X | X |
| Usability Review | X | X | X | X |
| **Total** | **X** | **X** | **X** | **X** |

---

## Screen Design

### UX-001 -- {Task Title}

**Priority:** High
**Spec section:** S2.1.2
**Figma:** [Link](url) or Not started

**Context:**
Brief summary of the functional requirement that drives this task. Written so the UX designer
understands what this screen/component must do without reading the full spec.

**What UX needs to deliver:**
1. Specific deliverable (e.g., "Wireframe for admin control panel showing ON/OFF toggle per role")
2. Another deliverable

**Open questions:**
1. Any UX decisions from the spec that need resolution before or during design
2. Options listed in spec if applicable

**Acceptance criteria:**
1. What "done" looks like (e.g., "Figma screen covers all states: enabled, disabled, pending sync")
2. Engineering can implement from this output without ambiguity

---

## Interaction Decision

### UX-002 -- {Task Title}

...same format...

---

## User Flow

...

## Component Design

...

## Edge Case UX

...

## Usability Review

...

---

## Future Scope

> Items below are NOT active tasks. They are future-phase features mentioned in the spec that will
> require UX work when they move to active development. Listed here so the UX team can factor
> forward compatibility into current designs.

### FS-001 -- {Future Item Title}

**Spec section:** S2.3.1, S5
**Mentioned as:** "future phase" / "deferred to" / "not in current scope"

**What the spec says:**
Verbatim or summarised description of the future capability from the spec.

**UX implication:**
What this means for UX when it becomes active -- new screens, changed interactions, or design
decisions that current designs should keep open for.

**Forward compatibility note:**
Any current design choices that should avoid painting UX into a corner for this future feature.
E.g., "Design the toggle component so it can accommodate a third option without a full redesign."

---
```

## Formatting rules

1. Use numbered lists (`1.`, `2.`), never bullet points (`-`, `*`).
2. Use `--` (double dash), never em-dashes.
3. Section references: use `S` prefix (e.g., S2.1.2, S1.3) since `§` may not render in all tools.
4. Figma links: carry forward from the spec's §1.1 Related Document table. If a Figma link maps to a specific section, attach it to tasks from that section.
5. Wiki/doc link: pull from the spec's `> Source:` line at the top.
6. Date format: DD-MM-YYYY always.

## Step 6: Present summary to user

After writing the file, show:
1. Total task count by type and priority.
2. List of all High-priority tasks (these block engineering).
3. Number of future scope items (if any).
4. The file path where `ux-tasks.md` was saved.
