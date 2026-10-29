---
name: new-joinee
description: Use when someone asks for thorough onboarding, says "I am new here" or "This is my first task", has never used Claude Code, does not understand MCP, wants "Help me understand the company workflow", or shows confusion about the AI system. Thorough onboarding for absolute beginners and non-technical employees.
argument-hint: [role or first-task context]
allowed-tools: Read, Glob, Grep, Write
---

## What This Skill Does

Thorough onboarding for absolute beginners, non-technical employees, and student-level learners. Teaches the complete Company AI Workflow Architecture from top to bottom. Only completes when the employee can work independently.

## Process

### Step 0: Check for Prior `/start` Progress

Before Step 1, check whether `onboarding-output/completion-summary.md` exists (written by the `/start` skill).

- If it exists: acknowledge it — mention the role and confidence score recorded there — and ask via AskUserQuestion whether they want to (a) skip ahead, treating layers 1-5 as a quick recap only and moving faster into the seven-layer additions (Human Review, Evidence) and role-specific depth, or (b) run the full onboarding from Step 1 regardless.
- If it doesn't exist: proceed to Step 1 normally. `new-joinee` is fully standalone and never requires `/start` first.

### Step 1: Welcome & Learner Calibration

If `$ARGUMENTS` is provided, use it as role or first-task context. Otherwise ask, in order:

1. What's your name? (free text)
2. What's your role? (free text -- roles span far more than any 4-option menu could cover; dev, PM, designer, support, sales, data, student, etc. are illustrative examples, not the full set)
3. What's your first assigned task or project? (free text)
4. `AskUserQuestion`: "Have you used AI tools, coding assistants, or command-line tools before?" -- options `No, none of these` / `Some familiarity` / `Yes, I'm experienced`. Mark `No, none of these (Recommended)` unless their role or task answer already signals technical experience (e.g. a dev/data role), in which case mark the matching option instead -- defaulting to "assume nothing" is the safer calibration per the guardrails below.

Set calibration from question 4's answer:
- **Zero knowledge:** Assume nothing, define every term
- **Some familiarity:** Shorten basics but still require all checks
- **Experienced/advanced:** Note it but do not skip required stages

### Step 2: Motivation

Explain why this matters:
- "AI tools like Claude are changing how companies work"
- "You don't need to be technical to use them"
- "This session will teach you the complete workflow so you can work independently"
- Connect to their specific role and first task

### Step 3: Architecture Overview

Teach the seven-layer model. Use the restaurant analogy from company-workflow.md:

| Layer | Restaurant | Your System |
|-------|-----------|-------------|
| 1. Data/Tools | Kitchen, ingredients | Company databases, APIs, files |
| 2. MCP | Waiter taking orders | Connectors to your tools |
| 3. Claude Code + Skills | Chef with recipes | AI with task instructions |
| 4. Processing | Cooking the meal | Claude transforming data |
| 5. Output | Meal served | Results, files, responses |
| 6. Human Review | Customer tastes it | You check the work |
| 7. Evidence | Receipt, order record | Logs, saved outputs |

**Check-in:** "Can you name one thing from each layer?"

### Step 4: Each Layer Explained

For each layer, explain and check understanding. Consult `glossary.md` for the precise, beginner-friendly definition of any technical term (MCP, API, skill, slash command, etc.) before introducing it — per the "define all technical terms" guardrail below:

**Layer 1 — Data/Tools:** Where company information lives. Examples: databases, spreadsheets, APIs, SaaS tools.

**Layer 2 — MCP:** The bridge between Claude and your tools. Without MCP, Claude can't access your company data.

**Layer 3 — Claude Code + Skills:** CLAUDE.md = always-on rules. Skills = task-specific recipes. Slash commands = shortcuts.

**Layer 4 — Processing:** Claude reads the data, follows the skill instructions, transforms it into what you need.

**Layer 5 — Output:** Text in chat, files on disk, commands executed, visual output.

**Layer 6 — Human Review:** You check Claude's work. Never trust output blindly.

**Layer 7 — Evidence:** Saved outputs, logs, completion records.

**Check-in after each layer:** Ask a simple question. Re-teach if they don't understand. Do not proceed until they do.

### Step 5: Generic Workflow Example

Walk through a complete example using a sales-report scenario (adapt to their role):
1. Employee types: "Generate monthly sales report"
2. Claude detects the sales-report skill
3. Skill loads instructions
4. MCP fetches data from database
5. Claude processes and formats
6. Output: Report file in output/sales-report/
7. Employee reviews the output
8. Evidence: Saved report + session log

**Check-in:** "Which layer fetched the actual data?"

### Step 6: Read-Only Project Discovery

Inspect project resources in this order (read-only, never expose secrets):
1. **Bundled reference** — company-workflow.md (always available)
2. **CLAUDE.md** — project rules and conventions
3. **.claude/skills/** — existing skills in this project
4. **MCP configuration** — available connectors (summarize names and purposes only, never print tokens/keys)

If resources are missing, state clearly: "This resource is not set up yet — that's normal for a new project."

### Step 7: Map Employee's First Task

Using what you learned in Step 1 and Step 6, grounded in `company-workflow.md`'s "Common Tasks by Role" section (including its per-role "Typical workflow" line) for their stated role:
1. Restate their role and first assigned task
2. Identify which layers of the architecture are involved
3. Identify which skills or MCP connectors might help
4. Create a simple task map:

```
Task: [description]
Layers involved: [list]
Relevant skills: [list or "none yet"]
MCP connectors needed: [list or "none yet"]
```

### Step 8: Guided Walkthrough

Guide them through completing their first task:
1. Show them what to type
2. Explain what Claude is doing at each step
3. Point out which layer is active
4. Let them see the output being generated
5. Walk through reviewing the output

### Step 9: Solo Attempt

Have them complete a similar task on their own:
1. Give them a task similar to their first one
2. Watch without interfering
3. Note where they struggle
4. Provide hints only if they ask or get stuck

### Step 10: Teach-Back Assessment

Ask them to explain back:
1. "Walk me through what happens when you ask Claude to do something"
2. "What are the seven layers and what does each one do?"
3. "Where would you put a rule that Claude should always follow?"
4. "What should you always do after Claude gives you output?"

Score: Pass or Fail. If fail, re-teach weak areas and retry.

### Step 11: Independent Task Assessment

Have them complete a real task from start to finish:
1. They type the request
2. They identify what Claude is doing
3. They review the output
4. They confirm it's correct

Score: Pass or Fail. If fail, provide targeted correction and retry.

### Step 12: Readiness Decision

Based on both assessments:

| Status | Meaning |
|--------|---------|
| **READY** | Both assessments passed, can work independently |
| **READY WITH SUPPORT** | Passed but needs occasional check-ins |
| **RETRY REQUIRED** | One or both assessments failed, needs more practice |
| **BLOCKED** | Missing resources or permissions prevent completion |
| **ESCALATE** | Role mismatch or authority issues need manager input |

### Step 13: Role-Specific Summary

Explain what this means for their job, grounded in `company-workflow.md`'s "Common Tasks by Role" section for their stated role:
- Common tasks they'll ask Claude to do
- Which skills are most relevant
- What output files they'll work with
- Who to ask for help
- Safety rules for their role

### Step 13.5: Recommended Skills for Your Role

Based on their stated role (Step 1) and `company-workflow.md`'s "Common Tasks by Role" section, identify which skills in `.claude/skills/` are the closest match to what they'll actually do (e.g. data roles → `order-summary-report`/`order-status-summary`; support → `customer-email-reply-drafter`; anyone drafting documents → `markdown-document-formatter`; anyone with a vague task → `first-task-mapper`). List 2-4 skills by name with a one-line reason each. If nothing matches well, say so plainly rather than forcing a fit.

### Step 14: Generate Onboarding Outputs

Before writing anything, confirm via `AskUserQuestion`: *"I'd like to save your onboarding files to `onboarding-output/` — is that okay?"* -- options `Yes, save them (Recommended)` / `No, don't save`. Only write after they say yes.

Create files in `onboarding-output/`:

**Always generate**, using the fixed templates below, filling in their specific details:

`NEW_EMPLOYEE_CHEAT_SHEET.md`:

```markdown
# New Employee Cheat Sheet
**Name:** {{ name }}
**Role:** {{ role }}
**Date:** {{ date }}

## The Seven-Layer Model
| Layer | What it does |
|-------|-------------|
| 1. Data/Tools | Company databases, APIs, files |
| 2. MCP | Connectors to your tools |
| 3. Claude Code + Skills | AI with task instructions |
| 4. Processing | Claude transforming data |
| 5. Output | Results, files, responses |
| 6. Human Review | You check the work |
| 7. Evidence | Logs, saved outputs |

## Your First Task
{{ first-task-map }}

## Key Commands
- `/new-joinee` — Re-run this onboarding session
- `/skill-name` — Run a specific skill (replace `skill-name` with the actual skill name)
- Natural language also works — just describe what you need

## Who to Ask for Help
{{ help-contact-or-not-confirmed }}

## Safety Rules for Your Role
{{ role-safety-notes }}
```

`LEARNING_SUMMARY.md` — a plain record of what they learned: architecture layers covered, check-ins passed/re-taught, and the task map from Step 7. No fixed template required; write it as a clear narrative summary.

**Only generate if BOTH assessments pass:**

`ONBOARDING_COMPLETION_CERTIFICATE.md`:

```markdown
# Onboarding Completion Certificate
**Name:** {{ name }}
**Role:** {{ role }}
**Date Issued:** {{ date }}

This confirms {{ name }} completed the New Joinee onboarding session, covering the
seven-layer Company AI Workflow Architecture, and passed both required assessments:

- Teach-Back Assessment: PASS
- Independent Task Assessment: PASS

**Readiness Decision:** {{ readiness-decision }}

## Notes
Generated by the `/new-joinee` onboarding skill.
```

**Important:** After writing, tell the user which files were saved and where to find them.

## Guardrails

- Project discovery (CLAUDE.md, .claude/skills/, MCP configs) is READ-ONLY — never modify, edit, or create files in these locations
- Onboarding output files may ONLY be created inside `onboarding-output/` AND only after user gives explicit permission to generate them
- Never reveal passwords, API keys, tokens, connection strings, or credentials — summarize connector names and purposes only
- Summarize MCP configuration availability without exposing raw config values, keys, or tokens
- Force comprehension checks — do not skip even if user says they're fine
- Define all technical terms before using them (consult `glossary.md` for the exact definitions)
- Mandatory both teach-back AND independent task to issue certificate
- Never invent project systems, connectors, policies, or company data
- allowed-tools is restricted to Read, Glob, Grep, Write — no Edit, Bash, or subagent execution
- Write may ONLY be used to create files inside `onboarding-output/`, and only after user confirmation (same rule as the output files themselves, above)

## Failure Modes

**User overwhelm:** Reduce to smaller steps, one concept at a time, continue only after simple check.

**Advanced user:** Shorten basics but require project discovery, safety checks, task mapping, teach-back, and independent task.

**Empty project:** Use bundled reference, state clearly what is unavailable, never invent resources.

**Mixed results:** Do not mark complete. Provide targeted correction, repeat only failed assessment.

**Impatient user:** Explain mandatory stages, allow faster pace through familiar material, no skipping safety or comprehension checks.

**Role mismatch:** Confirm actual responsibilities, escalate if mismatch affects permissions or authority.

**Missing access/unavailable MCP:** State what's blocked, continue with available resources, mark BLOCKED if critical.

**Conflicting instructions:** Ask user to clarify, escalate to manager if needed.

**Unclear task ownership:** Ask user to confirm, document assumption.

**Unsafe actions:** Stop immediately, explain why, require explicit permission.

**Missing data:** State what's missing, continue with what's available.

**Incomplete evidence:** Do not issue certificate until both assessments pass.

**Failed output validation:** Re-run assessment with corrections.

## Notes

- The bundled company-workflow.md contains detailed teaching content and examples; term definitions live separately in glossary.md
- See [company-workflow.md](company-workflow.md) for full teaching material
- See [glossary.md](glossary.md) for term definitions
- Output templates (cheat sheet, certificate) are inlined directly in Step 14, not in a separate file
- Keep SKILL.md under 500 lines — detailed content lives in supporting files
- Clickable-question convention: Step 0's resume choice was already `AskUserQuestion`; Step 1's prior-experience question and Step 14's save confirmation now are too. Name, role, and first-task intake (Step 1), all layer check-ins (Steps 3-5), and the Teach-Back Assessment (Step 10) stay free text -- they require an actual recall/explanation in the learner's own words, not a choice among options, which is the point of a comprehension or teach-back check.
