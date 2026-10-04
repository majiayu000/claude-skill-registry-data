---
name: post-meeting
description: |
  Post-meeting intelligence layer. Pulls a Granola meeting, extracts structured insights, and rewrites the project's living PPP document in _product-brain/. Triggers on: "post meeting", "process meeting", "update project from meeting", "/post-meeting", "just had a meeting about X".
---

# Post-Meeting Intelligence Skill

Processes a Granola meeting and rewrites the relevant project's living document in `_product-brain/`. Extracts decisions, progress, plans, problems, and open questions. Maintains an append-only changelog at the bottom.

## When to Activate

- User says "post meeting", "process meeting", "update project"
- User says "just had a meeting about X"
- User says "/post-meeting"
- User wants to capture meeting outcomes into project state

## Input

The user provides ONE of:
- **Meeting name/topic**: "post-meeting Ad Tech Sync"
- **Person name**: "post-meeting with Sebastian" (skill finds the latest meeting with them)
- **Nothing**: skill lists recent Granola meetings and asks which one to process

Optionally:
- **Project name**: if the meeting covers a known project. If omitted, the skill infers from meeting content.

## Execution

### Step 0: Get the Meeting

Use the Granola MCP to fetch the meeting:

```
1. If user gave a topic/person:
   → mcp__claude_ai_Granola__query_granola_meetings with the search term
   → Pick the most recent match

2. If user gave nothing:
   → mcp__claude_ai_Granola__list_meetings (last 5)
   → Present list, ask user to pick one

3. Once identified:
   → mcp__claude_ai_Granola__get_meeting_transcript for the full content
```

### Step 1: Identify Target Project(s)

Check which project(s) this meeting relates to:

1. **Scan `_product-brain/` for existing project files** (glob `_product-brain/*.md`, exclude PULSE.md)
2. **Match meeting content against project names/topics**
3. **If no match**: ask the user: "This meeting doesn't match an existing project. Create a new one? What should I call it?"
   - If yes, create using the new-project template (see Step 4 below)
4. **If multiple matches**: the meeting touches multiple projects; update each one

### Step 2: Extract Structured Insights

From the meeting transcript, extract:

| Field | What to look for |
|:------|:-----------------|
| **Progress** | What was accomplished, shipped, completed, resolved since last update |
| **Plans** | What's coming next, commitments made, timelines mentioned |
| **Problems** | Blockers, risks, concerns raised, dependencies, escalations |
| **Open Questions** | Unresolved questions, things needing investigation, decisions pending |
| **Decisions** | Anything explicitly decided or agreed upon |
| **Changelog entry** | One-line summary: date, meeting name, key outcome |

Guidelines for extraction:
- Be specific: "Sebastian to share algorithm by Thursday" not "algorithm discussion"
- Attribute when relevant: "Finance wants X", "Ric suggested Y"
- Capture commitments with owners and dates when mentioned
- Flag escalations or urgent items explicitly

### Step 3: Rewrite the Project Document

Read the existing project file from `_product-brain/{project}.md`.

**Rewrite rules:**
- **Current State**: Update to reflect where the project is RIGHT NOW after this meeting
- **Progress**: Replace with current progress items. Move completed items to changelog.
- **Plans**: Replace with current forward-looking items
- **Problems**: Replace with current blockers/risks. If a problem was resolved, remove it (note resolution in changelog)
- **Open Questions**: Replace with current open questions. If answered, remove (note in changelog)
- **Changelog**: APPEND ONLY. Add one dated entry summarizing this meeting's impact. Never edit old entries.
- **Status line**: Update if the project phase changed
- **Updated line**: Set to today's date and meeting name

### Step 4: New Project Template

If creating a new project doc, use this template:

```markdown
# {Project Name}

**Status:** {Discovery | Planning | In Progress | Blocked | On Hold | Complete}
**Updated:** {date} (from: {meeting name})
**Owner:** {who owns this, default to "you"}

## Current State
{One paragraph: what is this project and where is it right now}

## Progress
- {initial items from this meeting}

## Plans
- {what's planned next}

## Problems
- {any blockers or risks identified}

## Open Questions
- {unresolved questions}

---

## Changelog
- **{date}:** Project created from {meeting name}. {Brief context}.
```

### Step 5: Confirm and Present

After rewriting, show the user:

1. **Which project(s) were updated**
2. **Key extractions** (decisions, new problems, commitments) as a quick summary
3. **The changelog entry** that was added
4. If any items seem urgent or need escalation, flag them explicitly

Do NOT show the full rewritten document unless the user asks. Just confirm what changed.

## Multi-Project Meetings

Some meetings (like Big Room Planning, Product Sync) touch multiple projects. In this case:

1. Identify all affected projects
2. Extract project-specific insights for each
3. Rewrite each project doc independently
4. Report: "Updated 3 project docs: heimdall, kas-bugs, matchmaker"

## Edge Cases

- **Meeting has no clear project**: Ask the user. It might be a new project, or it might be a general sync that doesn't need a project doc.
- **Project exists but meeting adds nothing new**: Don't rewrite. Report: "No material updates for {project} from this meeting."
- **Conflicting information**: If the meeting contradicts the current doc state, update to the latest and note the change in changelog: "Revised: previously X, now Y per {meeting}."

## Output Location

All project docs live in: `_product-brain/{project-slug}.md`

Naming: lowercase, hyphens, no spaces. Examples:
- `heimdall.md`
- `kas-bugs.md`
- `lead-scoring.md`
- `wisebox.md`
