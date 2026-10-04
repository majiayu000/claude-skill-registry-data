---
name: timeframe-research
description: Build a timeframe-bounded research dossier by decomposing a topic into year orchestrators and month-level research passes that each write one condensed paragraph plus sources directly into a target file. Use when the user asks for a dossier, timeline, chronology, release history, or month-by-month research bounded by specific years or months. Not for timeless explainers or single-document summaries with no temporal scope.
---

# Timeframe Research

## What This Skill Does

This skill turns a date-bounded research request into a deterministic execution plan. It is designed for prompts such as:

- Make a dossier about `llama.cpp` in `2023-2026` and store it in `<file>`.
- Research notable local AI milestones from `2024` and write them month by month.
- Build a timeline of `open-weight multimodal models` from `2025-01` through `2026-03`.

The core pattern is fixed:

1. Normalize the requested timeframe.
2. Scaffold the target file with year and month headings.
3. Launch one **year orchestrator** per year in scope.
4. Each year orchestrator launches one **month researcher** per month in scope.
5. Each month researcher writes exactly one condensed paragraph plus sources under the matching heading.
6. Run a final quality pass for date accuracy, completeness, and structure.

If literal nested subagent launching is unavailable in the current tool environment, the agent must preserve the same logic by running isolated month-bounded research passes inside each year pass and explicitly noting that fallback.

## When To Use This Skill

Use this skill when the user asks for:

- A historical dossier, timeline, chronology, or release history
- Research bounded by specific years, quarters, or months
- A month-by-month or year-by-year file written directly into the workspace
- Time-sensitive ecosystem research where exact release dates matter

Do not use this skill for:

- Timeless concept explainers with no date-bounded scope
- Single-document summaries that do not need temporal decomposition
- Short answers where a plain narrative is sufficient

## Required Inputs

Before starting, extract or infer:

- **Topic**: the subject being tracked across time
- **Start date**: year or year-month
- **End date**: year or year-month
- **Target file**: absolute or workspace path where the dossier should be written
- **Expected granularity**: default to year → month unless the user asks for something else

If the user gives years only, interpret them as full calendar years except for the current year, which should stop at the current month unless the user explicitly asks for future placeholders.

## Output Contract

The default output format is:

- One heading per year
- One subheading per month in scope
- One condensed paragraph per month, focused only on that month
- One `Sources:` line per month with 4-8 links

Default paragraph target: **120-220 words**.

## Step 1: Normalize The Timeframe

Convert the user request into an explicit calendar plan.

Rules:

- If the range starts mid-year, include only months from the start month onward.
- If the range ends mid-year, include only months up to the end month.
- If the end year is the current year, stop at the current month unless told otherwise.
- Use Gregorian calendar month names in chronological order.
- Make the month list explicit before launching subagents.

Example:

- Request: `2023-2026`
- Current date: March 2026
- Effective scope: January 2023 through March 2026

## Step 2: Scaffold The Target File

Create or normalize the file structure before research begins.

Requirements:

- Add a title and short scope line if the file is empty or skeletal.
- Insert all year headings and month headings in chronological order.
- Leave deterministic insertion points so month researchers can write safely.
- Do not prefill months with speculative content.

Recommended structure:

```markdown
# <Title>

Scope: <one sentence>

Method: each month is summarized as one condensed paragraph focused only on that month, followed by source links.

# 2023

## January

## February
```

## Step 3: Launch The Year Orchestrators

Launch one year-level subagent for each year in scope.

The year orchestrator's job is coordination, not broad synthesis. It must:

- Work only on its assigned year
- Launch one month researcher per month in that year's scope
- Enforce strict month boundaries
- Write results directly into the target file under the matching headings
- Report ambiguities in dating and how they were resolved

### Year-Orchestrator Prompt Template

Use a prompt with all of the following elements:

- Exact year in scope
- Exact target file path
- Explicit list of months to fill
- Requirement to launch month subagents if available
- Fallback instruction to emulate month subagents with isolated month passes if nested launching is unavailable
- Month output format: one paragraph plus `Sources:` line
- Date verification requirement
- Source diversity requirement

Minimum instruction set:

```text
You own the <YEAR> section of <TARGET_FILE>.

Your job is to complete only these months: <MONTHS>.
Launch one month researcher per month if subagent launching is available. If it is not available, emulate the same process with isolated month-bounded research passes and state that explicitly in your final report.

Each month output must contain:
- one 120-220 word paragraph
- one Sources: line with 4-8 links

Each month must cover only events from that month that materially shaped the topic.
Verify dates carefully and distinguish release date, publication date, repo tag date, and later adoption.
Write results directly into <TARGET_FILE> under the matching heading.
```

## Step 4: Launch The Month Researchers

Each month researcher handles exactly one month.

This is the most important scope rule in the skill:

- Do not let a month agent summarize the whole year.
- Do not let it drift into adjacent months except for one sentence of context when necessary.
- Do not let it pad weak months with generic trend language.

### Month Research Protocol

Every month researcher must:

1. Confirm the exact month boundaries.
2. Identify 2-5 material milestones from that month.
3. Prefer primary or near-primary sources.
4. Cross-check dates across multiple source types.
5. Write one condensed paragraph focused only on that month.
6. Add a `Sources:` line with 4-8 relevant links.

### Source Types To Check

Month researchers should use several of these, depending on the topic:

- Official product, lab, or vendor announcements
- Hugging Face model cards, blog posts, collections, or papers
- GitHub releases, tags, repo creation dates, or dated commits
- arXiv first-posted dates
- Hacker News threads from that month
- Reddit communities relevant to the topic, such as `r/LocalLLaMA`
- Project documentation or release notes
- Press or technical blogs only when primary sources are unavailable

### Date-Resolution Rules

When dates conflict, prefer this order:

1. Official announcement or release note
2. Model card or repository release/tag timestamp
3. Paper posting date
4. Community discussion date

State the ambiguity if it materially affects month placement.

### Month-Writer Prompt Template

```text
Research only <MONTH YEAR> for the topic <TOPIC>.

Focus strictly on that month. Find the notable events, releases, papers, runtime changes, hardware milestones, or community shifts that materially shaped the topic during that month.

Check multiple source types, including official announcements, Hugging Face, GitHub, Hacker News, Reddit, and arXiv where relevant. Verify the actual date of each item and do not pull in adjacent months unless clearly labeled as context.

Write directly into <TARGET_FILE> under the heading for <MONTH YEAR>:
- one condensed paragraph, 120-220 words
- one Sources: line with 4-8 links

No bullets inside the month section. No hype language. Prefer exact project, model, repo, paper, or release names.
```

## Step 5: Writing Standards

Every month entry must satisfy all of the following:

- Covers only that month
- Names specific releases, papers, projects, or hardware where possible
- Explains why the items mattered to the topic
- Uses neutral language with no unsupported superlatives
- Includes a `Sources:` line immediately after the paragraph

Weak example:

```markdown
This month saw many interesting developments in local AI as models kept improving.
```

Strong example pattern:

```markdown
March turned the project from an experiment into a usable local stack: <specific release A>, <specific release B>, and <specific release C> each changed a different layer of the workflow, namely <model>, <runtime>, and <distribution>. The significance was not just another checkpoint refresh; it was that <why this month changed the trajectory>.

Sources: <link>; <link>; <link>
```

## Step 6: Final QA Pass

After all year and month passes are complete, verify:

- Every month in scope has content
- No month outside the requested range is filled accidentally
- Each month has one paragraph and one `Sources:` line
- Month ordering is chronological
- No obvious cross-month leakage exists
- Source links are present and relevant
- Any date ambiguities are resolved or noted

If the workspace has a lint, format, or link-check command that applies to the target file, run it after editing.

## Completion Criteria

The task is complete only when:

- The target file exists
- The requested timeframe is fully populated
- The year → month structure is present and orderly
- Every month section follows the paragraph-plus-sources contract
- The agent reports any fallback from literal nested subagents to isolated month passes
- The final pass finds no missing months in scope

## Example Triggers

This skill should activate for requests like:

- Make a dossier about `llama.cpp` in `2023-2026` and store it in `research/llama-cpp-dossier.md`.
- Research `local inference` from `2024-01` through `2025-09` and write a month-by-month timeline to `notes/local-inference.md`.
- Build a chronology of `Apple silicon LLM tooling` across `2023-2025`.

## Default Decisions

When the user does not specify the details, default to:

- **Granularity**: year → month
- **Month output**: one paragraph plus one `Sources:` line
- **Current year behavior**: stop at the current month
- **Source strategy**: primary sources first, community sources second
- **Execution strategy**: literal year and month subagents when available; otherwise isolated month passes that preserve the same scope discipline
