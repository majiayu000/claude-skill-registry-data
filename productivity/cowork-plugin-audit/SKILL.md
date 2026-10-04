---
name: cowork-plugin-audit
description: "Audit active Cowork plugins and get a keep/disable table. Reduces token usage and cognitive noise. Use when reviewing Cowork setup, adding new plugins, or starting a new project. Triggers: 'audit my plugins', 'cowork plugin audit', 'which plugins to disable', 'аудит плагинов', 'какие плагины отключить'."
version: 1.0.0
---

# Cowork Plugin Audit

This skill audits the active plugins in your Claude Cowork setup and produces a keep/disable/disable-until-needed recommendation table. It compares each installed plugin against your described workflow, flags idle or redundant plugins, and provides a qualitative estimate of potential token savings.

**Input:**
- Your role and workflow description (2–5 sentences)
- List of installed plugins (plain text or markdown list)
- Optional: project context file (`.md`)

**Output:**
- Audit table: plugin → category → recommendation → rationale
- Summary: keep/disable counts + qualitative token-savings estimate
- Optional: ready-made Project Instructions block listing disabled plugins

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Collect Workflow Context

1. Check if a project context file was provided or is readable from the working directory
   - If found: extract role, workflow description, and primary tasks from it
   - If not found: proceed to Step 1.2

2. Check if the user provided a workflow description in their message
   - If yes: extract role and 2–3 primary tasks; proceed to Step 2
   - If no: ask **one** clarifying question: "Please describe 2–3 main tasks you do in Cowork" — wait for the answer before continuing

3. Confirm understanding of workflow in a 1–2 sentence paraphrase (shown inline before the audit table)

### Step 2: Collect Plugin List

1. Check if the user provided a list of installed plugins in their message
   - If yes: parse the list and proceed to Step 3
   - If no: ask the user to paste the list from Cowork Settings → Plugins

2. If the user does not know plugin names, offer the standard reference list of known Cowork plugins:
   - engineering, sales, data, operations, productivity, product-management, finance, skill-planner, skill-builder
   - Ask the user to confirm which ones are installed

**Negative Case — Empty list:** If no plugin list is received after prompting, stop and respond: "Plugin list required. Please paste your installed plugins from Cowork Settings → Plugins."

### Step 3: Classify Each Plugin

For each plugin in the list, assign one of three categories based on the described workflow:

- **core** — used regularly (matches primary tasks described by the user)
- **contextual** — used for specific project types or occasional tasks (not the current main workflow)
- **idle** — not referenced by any task in the described workflow

Classification logic:
- Map plugin domain to the tasks the user mentioned
  - e.g., `sales` → core if user manages deals; idle if user is a solo developer
  - e.g., `engineering` → core for developers; contextual for PMs who sometimes review code; idle for finance team
- When uncertain: prefer `contextual` over `idle`

### Step 4: Evaluate and Recommend

For each plugin classified as `contextual` or `idle`, generate a recommendation:

| Plugin state | Recommendation |
|---|---|
| core | keep |
| contextual, high relevance | keep |
| contextual, low relevance for current project | disable-until-needed |
| idle | disable |

Rationale rule: each rationale must name a specific reason (e.g., "No sales tasks in described workflow" — not just "unused").

**Edge Case — Only one plugin installed:** Output a brief audit note: "Minimum configuration detected — no plugins recommended for removal."

**Edge Case — User's role changes by project:** Mark conflicting plugins explicitly as `contextual (other projects)` and set recommendation to `disable-until-needed`.

**Negative Case — Contradiction:** If the user's workflow clearly requires a plugin they want to disable, flag the conflict: "Your workflow mentions [task] which uses [plugin] — recommend keeping. Please confirm if you still want to disable."

### Step 5: Format and Output

1. Write the Workflow Context summary (1–2 sentences)
2. Render the Audit Table (all plugins)
3. Render the Summary block (counts + token-savings estimate)
4. If any `disable` recommendations exist: render the optional Project Instructions block

**Token savings estimate logic:**
- 0 plugins to disable → no savings estimate needed
- 1–2 plugins disabled → "low" impact
- 3–5 plugins disabled → "moderate" impact
- 6+ plugins disabled → "significant" impact

---

## Output Format

```
## Plugin Audit — [date]

### Workflow Context
[1–2 sentences: role and primary tasks as understood]

### Audit Table

| Plugin | Category | Recommendation | Rationale |
|--------|----------|----------------|-----------|
| engineering | contextual | disable-until-needed | Used only during code review tasks; not part of daily workflow |
| sales | idle | disable | No sales-related tasks in described workflow |
| data | core | keep | Regular data analysis is a primary task |
| product-management | core | keep | Sprint planning and spec writing are primary tasks |
| ...  | ...      | ...            | ... |

### Summary
- **Keep:** N plugins
- **Disable:** N plugins
- **Disable-until-needed:** N plugins
- **Estimated token impact:** [low / moderate / significant] reduction

### Optional: Project Instructions Block
Add the following to your Project Instructions to prevent disabled plugins from being activated:

> Disabled plugins for this project: [plugin-1], [plugin-2]. Do not activate skills from these plugins unless I explicitly ask.
```

**Field rules:**
- Rationale: 1 sentence, specific (not generic)
- Category: exactly one of core / contextual / idle
- Recommendation: exactly one of keep / disable / disable-until-needed
- Token impact: only included when ≥1 plugin is recommended for disable

---

## Negative Cases

- **No plugin list provided after prompting:** Stop. Return: "Plugin list required. Paste your installed plugins from Cowork Settings."
- **No workflow description provided after prompting:** Stop. Return: "Workflow description required. Describe 2–3 main tasks you do in Cowork."
- **User requests disabling a plugin required by their workflow:** Flag the contradiction explicitly before proceeding. Do not silently override the recommendation.
