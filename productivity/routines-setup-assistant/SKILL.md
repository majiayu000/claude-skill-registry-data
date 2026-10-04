---
name: routines-setup-assistant
description: "Interview-style setup for Claude Cowork Scheduled Tasks. Turns your recurring tasks into ready-to-paste automation prompts. Use when automating weekly reports, digests, or reviews. Triggers: 'set up routines', 'automate my recurring tasks', 'настрой рутины', 'помоги создать scheduled tasks'."
version: 1.0.0
---

# Routines Setup Assistant

This skill interviews you about your recurring tasks and generates ready-to-use Scheduled Tasks prompts for Claude Cowork. Provide a brief description of what you do on a regular schedule — daily, weekly, or monthly — and receive copy-pasteable prompts configured for the Cowork Scheduled Tasks UI.

**Input:**
- Your description of recurring tasks (conversational, no specific format required)

**Output:**
- Structured Markdown block with one Routine prompt + frequency per task, plus setup instructions for Cowork

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

Apply the detected language to **all** user-facing output: greetings, clarifying questions, notes, warnings, the final summary block labels, and the "Next steps" section. Do not mix languages.

---

## Instructions

### Step 1: Open the Interview

1. Greet the user and explain the goal:
   > "I'll help you set up Claude Cowork Scheduled Tasks. Tell me about one recurring task you'd like to automate — something you do daily, weekly, or monthly."

2. If the user provides no description at all:
   - Re-prompt once: "To get started, describe one recurring task — for example, 'summarize my weekly notes every Friday' or 'generate a status report every Monday morning'."
   - If still no input: stop and return: "No task provided. Please describe a recurring task to set up."

### Step 2: Collect Task Details

For each task the user describes, ask these 3 clarifying questions (can be combined in one message):

1. **Input:** "What files or information does this task need? (e.g., files in a specific folder, nothing — Claude runs from memory)"
2. **Output:** "What should Claude produce? (e.g., a summary saved to a file, a report in the chat, a checklist)"
3. **Frequency:** "How often and at what time? (e.g., every Monday at 08:00, daily at 17:00, first of each month)"

If the user's original description already answers some of these, skip those questions.

### Step 3: Classify and Map Task

1. Identify the task type from the description:
   - **Digest/Report:** Compiling or summarizing information from files → use "Read → Compile → Save" pattern
   - **Review/Audit:** Checking files for issues or status → use "Scan → Flag → Report" pattern
   - **Generator:** Creating new content from a template or prompt → use "Generate → Format → Save" pattern
   - **Reminder/Tracker:** Status updates or tracking recurring items → use "Read → Update → Summarize" pattern

2. Select the appropriate Routine prompt structure based on task type.

**Edge Cases:**
- If task requires an external connector (e.g., reading email, fetching Slack messages): include a note in output: "⚠️ This task needs a connected tool. Enable the relevant connector in Cowork → Plugins before scheduling."
- If task description is still vague after clarification: ask one more targeted follow-up: "What specific output should Claude produce — a summary, a checklist, a report, or something else?"

### Step 4: Validate Frequency

1. Map the user's frequency input to a supported Cowork schedule:
   - Supported: daily (specific time), weekly (specific day + time), monthly (specific date + time)
   - Not supported: every N minutes, every N hours, custom intervals

2. If the user requests an unsupported frequency:
   - Note: "Cowork Scheduled Tasks support daily, weekly, and monthly schedules. I'll use the closest match: [suggested frequency]."

### Step 5: Generate Routine Prompt

1. Construct the Routine prompt using this formula:
   **[Action verb] + [source/scope] + [output format] + [destination]**

   Examples:
   - "Scan all files in /projects for overdue tasks and generate a weekly action list saved to overdue-tasks.md."
   - "Compile all notes added to /weekly-notes this week into a structured digest saved to digests/YYYY-MM-DD.md."
   - "Review /team-updates for this week's entries and generate a people-centric status report saved to reports/week-status.md."

2. Ensure the prompt:
   - Starts with an action verb (Scan, Compile, Review, Generate, Read, Summarize)
   - Specifies the source (folder path or "from memory")
   - Specifies the output format (md file, markdown in chat, checklist)
   - Specifies the destination (file path or "in the chat")

### Step 6: Loop for Additional Tasks

1. After generating one Routine, ask: "Do you have another recurring task to automate? (Say 'done' or 'no' when finished)"
2. If yes: return to Step 2
3. If no: proceed to Step 7

**Edge Case:** If user provides 6+ tasks in one session, process all and add a note: "You've set up a large number of routines. Consider grouping related tasks (e.g., all weekly reviews) into a single scheduled workflow to reduce overhead."

### Step 7: Output Final Summary

1. Compile all generated Routine prompts into a single formatted block.
2. Include setup instructions for Cowork.

---

## Output Format

Conversational exchange ending with a structured Markdown summary block:

```markdown
## Your Routines Setup

**Routine 1:** Every Monday at 08:00
> Scan all files in /projects for overdue tasks across all project plans and generate a concise action list saved to weekly-overdue.md.

**Routine 2:** Every Friday at 17:00
> Compile all files added to /notes/week this week into a structured weekly digest saved to digests/YYYY-MM-DD.md.

---

**Next steps:**
1. Open Claude Cowork → Scheduled Tasks
2. Click "New Task" and paste each prompt above
3. Set the frequency as shown (e.g., "Every Monday at 08:00")
4. Save and test with a manual run first
```

**Prompt quality rules:**
- Each prompt must start with an action verb
- Source folder or input must be specified (or explicitly "from memory/context")
- Output format must be stated (saved file with path, or "in the chat")
- No bracketed placeholders — prompts must be copy-pasteable as-is

---

## Negative Cases

- **No input provided after re-prompt:** Stop and return "No task provided. Please describe a recurring task to set up."
- **Policy-violating task requested:** Decline normally. Do not generate the Routine prompt for that task. Continue with remaining tasks if any.

---

## Edge Cases Summary

| # | Condition | Behavior |
|---|-----------|----------|
| EC1 | Task needs external connector (email, Slack) | Add ⚠️ note; include prompt anyway |
| EC2 | Description too vague after clarification | One more targeted follow-up question |
| EC3 | Unsupported frequency (e.g., every 10 min) | Note limitation; suggest closest supported schedule |
| EC4 | 6+ tasks in one session | Process all; add note about grouping |
