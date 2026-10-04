---
name: session-handoff-composer
description: "Compose a structured handoff document when your chat session fills up. Extracts decisions, in-progress tasks, open questions, and next steps into a ready-to-paste block for a new session. Triggers: 'compose handoff', 'session handoff', 'составь хэндофф', 'подготовь handoff-документ'."
version: 1.0.0
---

# Session Handoff Composer

This skill composes a structured handoff document for transferring context into a new chat session. It extracts key information from the current conversation — decisions made, ongoing tasks, open questions, files involved, and next steps — and formats everything into a ready-to-paste markdown block.

**Input:** Current conversation context (read automatically); optional additions from the user

**Output:** Structured markdown handoff block + one-line opener for the new session

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Check Session Content

1. Assess whether the current session has meaningful content to hand off
   - If user invoked the skill at the very start with no prior content: respond "Nothing to hand off yet — session has just started. Call this skill when context fills up."
   - If session has fewer than 5 exchanges AND no decisions or tasks were established: respond "Session is short — nothing significant to hand off yet. Call this skill when context fills up."
   - If session has content but is short (< 5 exchanges), proceed to Step 2 and output minimal handoff in Step 4

2. Detect session language
   - If the conversation is primarily in Russian: produce the handoff document in Russian
   - Otherwise: produce the handoff document in English

### Step 2: Extract Session Elements

Scan the conversation and collect the following:

1. **Done** — completed tasks and final decisions made in this session
   - Include decisions that were confirmed, files that were created/edited, analyses completed

2. **In Progress** — tasks started but not finished
   - Note the current state of each (e.g., "draft created, needs review")

3. **Open Questions** — unresolved issues, pending decisions, blockers
   - Include anything that requires follow-up in the next session

4. **Files** — files created, modified, or referenced during the session
   - Format: `filename.ext — what was done`
   - If no files were involved: omit this section

5. **Next Steps** — ordered list of actions to take in the new session
   - Start with the most immediate action

6. **Context for New Session** — 1–2 sentences summarizing what Claude needs to know to continue effectively

### Step 3: Ask One Clarifying Question (if needed)

- If any section is clearly incomplete or ambiguous (e.g., the user mentioned a task but never described its outcome), ask one targeted question
- Do not ask more than one question before generating output
- If there is nothing ambiguous, skip this step entirely

### Step 4: Compose the Handoff Block

1. Build the handoff document using the structure from the Output Format section
2. Sections with no content are marked explicitly (e.g., "— none —") except Files, which is silently omitted when empty
3. Wrap the entire document in a markdown code block for easy copy-paste
4. After the code block, add the one-line opener for the new session

**Edge Cases:**

- **Short session (< 5 exchanges):** Output a minimal handoff — just Topic, status, and one Next Step. Add note: "Session was short — only key intent captured."
- **Multiple parallel topics:** Create a separate subsection per topic inside In Progress and Next Steps; flag which is the primary focus
- **Session in Russian:** Generate all handoff text in Russian (labels, content, and opener)
- **Session near context limit (implicit):** Don't wait to be told — if the session is very long, generate the handoff proactively when the skill is triggered

---

## Negative Cases

- **No prior conversation content:** Respond "I need some session content to compose a handoff. Describe what you've been working on, or start your task first and call this skill when ready to switch sessions."
- **User asks for a handoff for future/speculative work:** Respond "Handoff requires completed work to summarize. Start the task first, then call this skill when ready to continue in a new session."

---

## Output Format

Output a markdown code block containing the handoff document, followed immediately by the opener line.

**Handoff block structure:**

```markdown
## Session Handoff

**Topic:** [1-line description of session topic]
**Date:** YYYY-MM-DD
**Status:** in-progress | paused | blocked

### Done
- [Completed task or confirmed decision]
- [Another completed item]

### In Progress
- [Task — current state description]

### Open Questions
- [Unresolved issue or pending decision]

### Files
- [file-name.ext — what was done]

### Next Steps
1. [First action in the new session]
2. [Second action if applicable]

### Context for New Session
[1–2 sentences: what Claude needs to understand to continue effectively]
```

**After the block (outside the code block):**

> **Start new session with:** *"Continue from: [topic]. Context below."* — then paste the block above.

**Field rules:**
- Done / In Progress / Open Questions: use bullet list; if empty, write `— none —`
- Files: omit section entirely if no files were involved
- Next Steps: numbered list, most immediate action first
- Context for New Session: 1–2 sentences max; focus on what's non-obvious from the handoff alone
- Date: use today's date (YYYY-MM-DD format)
