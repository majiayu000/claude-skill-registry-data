---
name: weekly-ai-workflow-review
description: "Analyze weekly Claude interaction notes to reveal delegation patterns, effective prompts, and optimization areas. Use for weekly AI workflow review, reflecting on Claude usage, improving prompts. Triggers: 'weekly ai workflow review', 'review my claude interactions', 'еженедельный обзор AI-задач', 'паттерны работы с Claude'."
version: 1.0.0
---

# Weekly AI Workflow Review

This skill analyzes weekly notes about tasks delegated to Claude and produces a structured reflection report: what worked, what needed rework, recurring task types, and recommended prompt templates for the next week.

**Input:**
- Markdown file or pasted text with weekly Claude task log (task descriptions, prompts or their summaries, outcomes: used / edited / discarded)

**Output:**
- Structured markdown reflection report (inline in chat or saved as `weekly-ai-review-YYYY-MM-DD.md` on request)

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

**Localization note:** When responding in Russian, translate all section headers and prompts in the Output Format template:
- "Weekly AI Workflow Review" → "Еженедельный обзор AI-рабочего процесса"
- "Period" → "Период", "Tasks analyzed" → "Задач проанализировано"
- "Patterns of the Week" → "Паттерны недели"
- "What Worked Well" → "Что работало хорошо"
- "Areas for Improvement" → "Зоны улучшения"
- "Recommended Prompt Templates" → "Рекомендованные промпт-шаблоны"
- "Takeaway" → "Итог"

---

## Instructions

### Step 1: Validate and Parse Input

1. Check that input contains at least 1 task description or prompt
   - If input is empty or contains only a file header: stop and return: "Task log not found. Please paste your weekly list of tasks delegated to Claude."
   - If input appears unrelated to AI/Claude interactions (e.g., general journal, shopping list): return: "No Claude-related tasks found in the provided notes. Please include descriptions of tasks you delegated to Claude this week."

2. Parse entries from the input
   - Accept both structured (markdown list) and unstructured (plain text) formats
   - Extract for each entry: task description, prompt or summary, outcome if noted (used / edited / discarded / unclear)
   - If entries are unstructured plain text: attempt to identify task boundaries by paragraph, line break, or numbered list patterns
   - If task boundaries cannot be clearly identified (continuous spaghetti text): request a minimal structure: "Unable to parse task boundaries from the text. Please provide tasks as a list (bullet points, numbers, or line breaks between entries) so I can analyze them accurately."

3. Note sample size
   - If fewer than 3 tasks identified: continue but add a note in the report: "Small sample (N tasks) — patterns are indicative; consider logging at least 5 tasks per week for reliable trends."

### Step 2: Classify Tasks by Type

1. Group parsed entries into task types:
   - **Content / Writing** — posts, emails, documents, summaries
   - **Analysis** — data review, comparison, synthesis
   - **Research** — topic exploration, fact-finding
   - **Formatting / Editing** — structure, grammar, style
   - **Ideation** — brainstorming, generation of options
   - **Other** — anything that doesn't fit above categories

2. Count tasks per type; identify the dominant type(s)

3. Note recurring tasks — any task type or topic that appears 2+ times

**Edge Cases:**
- If no outcome is noted for any task: skip outcome-based analysis; analyze task types and prompt patterns only; mark report section as "Outcome data unavailable"
- If all tasks belong to a single type: note in report, skip cross-type comparison

### Step 3: Identify Successful Interactions

1. Mark as **successful** any task where:
   - Outcome is explicitly noted as "used" or "no edits"
   - Or: description implies result was accepted (e.g., "sent it", "published", "approved")

2. Extract the prompt pattern for each successful interaction (verb + object + context)

3. Note what made these prompts effective: specificity, role assignment, format instruction, example provided

### Step 4: Identify Pain Points

1. Mark as **problematic** any task where:
   - Outcome is noted as "edited significantly", "multiple iterations", "discarded", or "not used"
   - Or: description implies significant rework (e.g., "rewrote half of it", "had to redo")

2. For each problematic task: diagnose the likely cause from the prompt/description:
   - Vague request (no format, audience, or length specified)
   - Missing context (no background or constraints)
   - Scope too broad (asked for too much at once)
   - Wrong tone or style (no style guidance provided)

3. Generate a specific improvement recommendation for each pain point

### Step 5: Generate Prompt Templates

1. For each recurring task type (2+ occurrences): draft a reusable prompt template
   - Template structure: `[Action] + [Object] + [Format/length] + [Audience/tone] + [Constraints]`
   - Fill from successful interactions or improve from pain points
   - Keep templates general enough to reuse, specific enough to be actionable

2. Prioritize templates for task types that had both recurrence and pain points

### Step 6: Compose Report

1. Build the structured report using Output Format below
2. Populate all sections; if a section has no data, write "None found" — do not omit the section
3. If user asks to save: write output to `weekly-ai-review-YYYY-MM-DD.md` using today's date

---

## Output Format

```markdown
## Weekly AI Workflow Review
**Period:** [week or date range if provided]  **Tasks analyzed:** N

---

### Patterns of the Week
- Dominant task type: [type] (N tasks, X%)
- Successful interactions: N (X%)
- Tasks requiring rework: N (X%)
- Recurring topics: [list or "None"]

---

### What Worked Well
- **[Task type]:** [Description of successful interaction]. Prompt pattern: "[excerpt or reconstruction]"
- **[Task type]:** [Second example if available]

---

### Areas for Improvement
- **[Task]:** Required [N iterations / significant edits]. Likely cause: [diagnosis]. Recommendation: [specific prompt fix]
- **[Task]:** [Second example if available]

---

### Recommended Prompt Templates
1. For [task type]: "[Template: action + object + format + constraints]"
2. For [task type]: "[Template]"

---

### Takeaway
[1–2 sentences summarizing the week's AI workflow: what to keep, what to change]
```

**Field rules:**
- Prompt templates must be specific and actionable (not "be more specific" but an actual template)
- Diagnoses must be concrete (one of: vague request / missing context / scope too broad / wrong tone)
- Takeaway is 1–2 sentences only; no bullet points

---

## Negative Cases

- If input is empty or header-only: stop with "Task log not found. Please paste your weekly list of tasks delegated to Claude."
- If input contains no AI/Claude-related content: stop with "No Claude-related tasks found. Please include descriptions of tasks you delegated to Claude this week."
- If prompt patterns cannot be inferred from descriptions alone: note in report "Prompt patterns could not be inferred — consider logging actual prompts for richer analysis."
