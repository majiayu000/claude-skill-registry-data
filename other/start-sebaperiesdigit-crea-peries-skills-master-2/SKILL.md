---
name: start
description: Use when someone asks to be onboarded, says "I'm new here" or "onboard me", wants "explain how this works" or "how does our AI system work", or shows confusion about MCP/Skills while asking a task question. Interactive training session for new employees.
allowed-tools: Read, Glob, Grep, Write
---

## What This Skill Does

Guides new employees through an interactive onboarding session that teaches how Claude Code + MCP + Skills work together. Checks understanding after each section and personalizes examples to their role.

## Process

### Step 0: Check for Prior Progress or Completion

Before Step 1, check in this order:

1. Does `onboarding-output/onboarding-progress.md` exist with status `IN PROGRESS`? If so, ask via AskUserQuestion: **Resume from the next incomplete step** / **Restart onboarding from Step 1** / **View saved progress** (just show its contents, then ask again).
2. Otherwise, does `onboarding-output/completion-summary.md` exist? If so, ask via AskUserQuestion whether they want a full re-run or a quick refresher (skip straight to Step 10, Role Personalization).
3. Otherwise (first run), proceed to Step 1 normally.

### Step 1: Role & Calibration

Ask the user:
1. What's your role? (free text — dev, PM, designer, support, sales, data, etc. are illustrative examples, not the full set)
2. `AskUserQuestion`: "Have you used Claude Code, MCP, or AI coding tools before?" — options `No, this is new to me (Recommended)` / `Yes, I've used similar tools before`.

Use their answers to:
- Adapt examples throughout, drawing from `company-workflow.md`'s "Common Tasks by Role" section (dev gets code/PR examples, support gets ticket examples, etc.)
- If their role isn't dev/PM/designer/support/sales/data, ask one follow-up: "What kind of tasks would you bring to Claude day-to-day?" (free text) and build examples from that answer instead of guessing a proxy role.
- Calibrate quiz difficulty (beginner gets recall questions, experienced gets applied questions)
- If they answered "Yes" above, offer via `AskUserQuestion`: "Skip ahead to Role Personalization and Real Project Files (Recommended)" / "Go through the full walkthrough anyway"

### Step 2: Big Picture

Teach the four-layer model using three delivery methods in sequence, then one comprehension check.

**A. Diagram first** — Render this architecture diagram:

```
┌──────────────────────────────────────────────────┐
│  YOU: "Show me this week's orders"               │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│  LAYER 4 — OUTPUT                                │
│  📄 Report  📊 Chart  📋 Table  💬 Response     │
└────────────────────▲─────────────────────────────┘
                     │
┌────────────────────┴──────────────────────────────┐
│  LAYER 3 — CLAUDE CODE + SKILLS                   │
│  🧠 Claude reads your request                     │
│  📋 Loads the matching skill (recipe book)        │
│  🔧 Follows instructions                          │
└────────────────────▲──────────────────────────────┘
                     │
┌────────────────────┴──────────────────────────────┐
│  LAYER 2 — MCP (Bridge / Waiter)                  │
│  🔗 Asks database via connector                   │
│  🔗 Sends API requests                            │
│  🔗 Reads/writes files                            │
└────────────────────▲──────────────────────────────┘
                     │
┌────────────────────┴──────────────────────────────┐
│  LAYER 1 — DATA & TOOLS (Kitchen / Ingredients)   │
│  🗄️  Databases  🌐 APIs  📁 Files                │
└───────────────────────────────────────────────────┘
```

**B. Then the restaurant analogy:**

| Layer | Restaurant | Your System |
|-------|-----------|-------------|
| **Data/Tools** | Kitchen, ingredients, equipment | Company data, APIs, databases |
| **MCP** | Waiter taking orders to kitchen | Connectors that link Claude to your tools |
| **Claude Code + Skills** | Chef with recipes (skills) | AI with instructions for specific tasks |
| **Output** | Meal served to customer | Results, files, responses |

Walk through the flow: You (customer) -> MCP (waiter) takes your order -> Chef (Claude + Skills) follows a recipe -> Kitchen (Data) has ingredients -> Waiter brings the meal (Output).

**C. Then the short table explaining each layer:**

| Layer | What it does |
|-------|-------------|
| **Data/Tools** | Where your company information lives — databases, APIs, spreadsheets |
| **MCP** | The standard bridge that lets Claude talk to those tools safely |
| **Claude Code + Skills** | The AI brain with reusable recipe books (skills) for each task |
| **Output** | The final result — a file, a chart, a summary, a command |

**D. Comprehension check** (one question via AskUserQuestion, then move on):

Ask: "Which pair correctly matches a layer to what it does?" with one correct option (e.g. "MCP — the bridge that connects Claude to your tools") and 2-3 plausible mismatches (e.g. pairing MCP with "the AI brain that follows recipes," or Output with "where company data lives").

If they answer correctly, praise and proceed. If they pick a distractor, re-explain using the restaurant analogy before continuing.

Also offer an interactive visual for hands-on exploration of the four-layer model, via `AskUserQuestion`: **Open the local file (Recommended)** / **Use the published artifact link** / **No thanks, skip this**. Local file: `output/skill-documentation/inputs/combined-workflow-cycle-start.html`. Link: https://claude.ai/public/artifacts/26d37fe5-9ec7-4c51-a020-0c9aa3cc3505

### Step 3: Data Layer

Explain where company data lives and how Claude accesses it:
- CLAUDE.md = project-wide rules (always loaded)
- Skills = task-specific procedures (loaded when invoked)
- MCP connectors = bridges to external tools

**Check-in (AskUserQuestion):** "If you wanted Claude to follow a coding style rule, where would you put it?" — correct: CLAUDE.md; distractors: a skill file, MCP config, an output file.

### Step 4: MCP Layer

Explain MCP (Model Context Protocol):
- What it is: A standard way for Claude to talk to external tools
- How it works: Connector sits between Claude and the tool
- Examples: Database queries, API calls, file system access

**Check-in (AskUserQuestion):** "Why can't Claude just directly call a database without MCP?" — correct: MCP provides a standard, safe bridge/connector between Claude and each tool; distractors: "Claude doesn't know SQL," "Databases are too slow for Claude," "It's a licensing restriction."

### Step 5: Claude Code + Skills

Explain how skills work:
- Skills = reusable instructions (SOPs for Claude)
- Invoked via `/slash-command` or natural language
- CLAUDE.md rules always apply inside skills
- Supporting files load only when needed

**Check-in (AskUserQuestion):** "What's the difference between CLAUDE.md and a skill?" — correct: CLAUDE.md is always-loaded project-wide rules, a skill is task-specific instructions loaded only when invoked; distractors: "CLAUDE.md is for code, skills are for chat," "They're the same thing, just different file names," "Skills override CLAUDE.md."

### Step 6: Output Layer

Explain what Claude produces:
- Text responses in conversation
- Files written to disk
- Commands executed
- Visual output (HTML, charts)

**Check-in (AskUserQuestion):** "Which of these is NOT a type of output Claude can produce?" — correct answer to select: a distractor like "A direct edit to a live production database with no file trail"; genuine output types (text response, written file, executed command, visual/HTML) serve as the other options.

### Step 7: Full Workflow Example

Walk through a complete example using a sales-report scenario (adapt to user's role):

1. User types: "Generate a monthly sales report"
2. Claude detects this matches the `sales-report` skill
3. Skill loads: instructions for pulling data, formatting, outputting
4. MCP connectors fetch data from database
5. Claude processes and formats the report
6. Output: Sales report file in `output/sales-report/`

**Check-in (AskUserQuestion):** "Which layer was doing the actual work of fetching data?" — correct: MCP (Layer 2); distractors: Claude Code + Skills (Layer 3), Output (Layer 4), Data & Tools (Layer 1 — the source, not the fetcher).

### Step 7.5: Real Project Files (Optional)

`AskUserQuestion`: "Would you like to see what this looks like in your actual project?" — options `Yes (Recommended)` / `No, skip this`.

If yes, read (read-only, never print sensitive content):
- `.claude/skills/` directory — show what skills exist
- MCP configuration — describe what's connected (don't print raw config/keys)
- CLAUDE.md — show project-specific rules

If no real files exist, say: "There's nothing connected yet in this project — that's normal, here's what it'll look like once there is."

### Step 8: Comprehension Check

Run a comprehension check via AskUserQuestion, adjusted to their skill level:
- **Beginner:** Recall questions with plausible distractors (e.g. "What does MCP stand for?" with 3 wrong expansions alongside "Model Context Protocol")
- **Experienced:** Applied questions with plausible distractors (e.g. "Why would this task fail without the MCP step?" with wrong-but-plausible failure reasons alongside the correct one)

Re-teach any weak spots before moving on. Don't skip this gate.

### Step 9: Generate Cheat Sheet

Before writing, confirm via `AskUserQuestion`: *"I'd like to save a cheat sheet to `onboarding-output/cheat-sheet.md` — is that okay?"* — options `Yes, save it (Recommended)` / `No, don't save`. Only write after they say yes.

Use this fixed template, filling in their specific details:

```markdown
# Onboarding Cheat Sheet
**Role:** {{ role }}
**Date:** {{ date }}

## The Four-Layer Model
```
┌──────────────────────────────────────────────────┐
│  LAYER 4 — OUTPUT                                │
│  Files, charts, summaries, commands              │
├──────────────────────────────────────────────────┤
│  LAYER 3 — CLAUDE CODE + SKILLS                  │
│  AI brain + recipe books for each task           │
├──────────────────────────────────────────────────┤
│  LAYER 2 — MCP (Bridge)                          │
│  Connectors linking Claude to tools/data         │
├──────────────────────────────────────────────────┤
│  LAYER 1 — DATA & TOOLS                          │
│  Databases, APIs, spreadsheets, files            │
└──────────────────────────────────────────────────┘
```

## Key Commands
- `/start` — Start this onboarding session
- `/skill-name` — Run a specific skill (replace `skill-name` with the actual skill name)
- Natural language also works — just describe what you need

## My Weak Spots (re-taught in session)
- {{ weak-spot-1 }}
- {{ weak-spot-2 }}

## Layer Summary
| Layer | What it does |
|-------|-------------|
| **Data/Tools** | Company info — databases, APIs, files |
| **MCP** | Standard bridge to connect Claude to tools |
| **Claude + Skills** | AI brain following recipe instructions |
| **Output** | Final result you see or use |
```

**Important:** After writing, tell the user the file was saved and where to find it.

Write to `onboarding-output/cheat-sheet.md`. Never write anywhere else.

### Step 10: Role Personalization

Explain what this means for their specific job, grounding it in `company-workflow.md`'s "Common Tasks by Role" section for their stated role (or their Step 1 follow-up answer if their role wasn't listed there):
- What tasks they'll commonly ask Claude to do
- Which skills are most relevant to their role
- What output files they'll work with
- Who to ask for help if something breaks

### Step 11: Confidence Check + Close

`AskUserQuestion`: "How confident do you feel using this system?" — options `Very confident (4-5)` / `Somewhat confident (3)` / `Not very confident (1-2)`. No option is marked Recommended -- this is a genuine self-assessment, not a quiz with a correct answer.

- **Very confident (4-5):** Ask via `AskUserQuestion`: "Want a completion summary saved before we wrap up?" — options `Yes, save one (Recommended)` / `No thanks, I'm ready to go`
- **Somewhat confident (3):** Re-teach the weakest area, then re-check
- **Not very confident (1-2):** Ask via `AskUserQuestion`: "Want to pause and continue later, or re-teach from the start?" — options `Pause and resume later (Recommended)` / `Re-teach from the start` (Pause routes to "Pausing Mid-Session" below)

If they scored 4-5 or otherwise completed this session, mention that `/new-joinee` exists as an optional next step for deeper, role-specific onboarding with hands-on assessments — not required, just available if they want it.

If they wanted a completion summary, confirm the write via `AskUserQuestion`: *"I'll save a completion summary to `onboarding-output/completion-summary.md` — okay?"* — options `Yes, save it (Recommended)` / `No, don't save`.

Only write after they say yes. If an `onboarding-output/onboarding-progress.md` file exists from an earlier paused session, delete it once completion-summary.md is written — the progress file is superseded by completion. Use this fixed template:

```markdown
# Onboarding Completion Summary
**Role:** {{ role }}
**Date:** {{ date }}
**Confidence Score:** {{ score }}/5

## Sections Re-Taught
- {{ section-1 }}
- {{ section-2 }}

## Next Steps for {{ role }}
1. {{ next-step-1 }}
2. {{ next-step-2 }}
3. {{ next-step-3 }}

## Notes
Generated by the `/start` onboarding skill.
```

**Important:** After writing, tell the user the file was saved and where to find it.

Write to `onboarding-output/completion-summary.md`. Never write anywhere else.

### Pausing Mid-Session

Triggered by the Step 11 low-confidence (1-2) path, or anytime the user goes quiet or says "this is too much" (per Session Guidelines). Confirm via `AskUserQuestion`: *"I'll save your progress to `onboarding-output/onboarding-progress.md` so you can resume later — okay?"* — options `Yes, save it (Recommended)` / `No, don't save`. Only write after they say yes.

```markdown
# Onboarding Progress
**Status:** IN PROGRESS
**Role:** {{ role }}
**Task context:** {{ what they said they'd bring to Claude, if role was unlisted }}
**Last completed step:** {{ step number/name }}
**Next step:** {{ step number/name }}
**Assessment scores so far:** {{ correct/missed check-ins }}
**Date:** {{ date }}
```

Write to `onboarding-output/onboarding-progress.md`. This is the one file this skill may write before Step 9 — every other file still waits until its named step.

## File-Writing Safety

- The only files this skill may write are:
  - `onboarding-output/onboarding-progress.md` (on pause, any step, with user confirmation)
  - `onboarding-output/cheat-sheet.md` (Step 9, with user confirmation)
  - `onboarding-output/completion-summary.md` (Step 11, with user confirmation; deletes onboarding-progress.md if present)
- Never create `cheat-sheet.md` or `completion-summary.md` before the user reaches their named step (Step 9 / Step 11) — `onboarding-progress.md` is the sole exception, written only on an explicit pause
- Always ask for confirmation before writing any file
- Write only inside `onboarding-output/` — never elsewhere
- Never modify project source files, .claude/ configuration, MCP settings, credentials, or external systems
- Never print raw config contents, keys, or tokens
- Never run destructive commands

## Session Guidelines

- Default to a lean pace (~15 min), but allow longer if the employee is genuinely confused
- Never fabricate company-specific facts not present in company-workflow.md or CLAUDE.md
- If user goes quiet or says "this is too much", offer to pause (see "Pausing Mid-Session") or simplify
- Step 7.5 reads are opt-in only, never automatic
- Clickable-question convention: Steps 2-8's comprehension checks already used `AskUserQuestion` (correctly with no "(Recommended)" tag, since it's a quiz); Step 0's resume/refresher choices already did too. Converted the remaining plain-text asks (Step 1's prior-experience question and advanced-skip offer, the Step 2 visual-exploration choice, Step 7.5's opt-in, Step 9's and Step 11's write confirmations, Step 11's confidence check and its pause/re-teach branch, and the mid-session pause confirmation). Role intake (Step 1) and the unlisted-role follow-up stay free text.
