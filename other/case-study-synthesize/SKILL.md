---
name: case-study-synthesize
description: Synthesize all captured observation data into a case study draft and a harness guide improvement plan. Invoke when the user runs /case-study-synthesize at build completion or at any milestone where a synthesis snapshot is useful.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, WebFetch
---

# Synthesize Case Study and Improvement Plan

Read all observation data captured by the case study harness, analyze it, and produce two Markdown
deliverables. Follow these steps in order.

## Step 1: Locate the harness engineering guide

The improvement plan must reference actual guide chapters, sections, and templates by name. To do
this accurately you need access to the guide's content. Ask the user:

> To write an accurate improvement plan, I need to reference the actual chapters and sections in the
> harness engineering guide. Do you have the guide repository cloned locally? If so, provide the
> path (e.g., `~/source/harness-engineering-guide`). Otherwise, I'll fetch what I need from the
> public GitHub repository.

Then:

- **If the user provides a local path:** Use `Read` to read `README.md` and files under `guide/`
  from that path. This is the preferred option -- it is faster, works offline, and always reflects
  the user's current version.
- **If the user says no or wants the remote option:** Use `WebFetch` to fetch from
  `https://github.com/brandonavant/harness-engineering-guide`. Start with the README for the
  chapter listing, then fetch specific chapters under `guide/` as needed.

At minimum, read the guide's `README.md` (which contains the full chapter listing and structure
overview). Then read specific chapters that are relevant to the observations found in the data --
you do not need to read all 11 chapters, only those you will reference in the improvement plan.

Keep the guide content available in context for Steps 5 and 6.

## Step 2: Run the reader script

Invoke the script to read, validate, merge, and summarize all observation data:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/read_observations.py"
```

The script reads all seven JSONL log files, merges entries chronologically, computes summary
statistics, and outputs a single JSON object to stdout with two keys:

- `"summary"` -- statistics (entry counts by type, session count, date range, friction tool
  breakdown, harness change file breakdown, manual observation category breakdown, tool use
  breakdown)
- `"entries"` -- all entries merged and sorted by timestamp

If the script reports errors or missing files, note which event types have no data but continue with
whatever data is available.

## Step 3: Analyze the data

Using the script's output, work through these analytical lenses:

- **User intent trail:** What did the user ask for at each turn? How did requests evolve over the
  course of the build? Were there corrections or pivots? Use `user_prompt` entries to reconstruct
  the narrative arc of what the user was trying to accomplish.
- **Tool usage patterns:** Which tools were used most frequently? What files were touched most
  often? Look for Read-then-Edit chains that indicate exploration followed by action. Use
  `tool_use` entries to understand the agent's working patterns.
- **Harness evolution:** How did harness files (`.claude/`, `CLAUDE.md`) change over time? What was
  added, modified, or removed? Were changes concentrated early or spread throughout?
- **Friction patterns:** What types of failures occurred? Were they clustered around specific tools,
  tasks, or time periods? Were any recurring?
- **Session rhythm:** How many sessions occurred? How long were they (based on turn counts between
  session boundaries)? Were there sessions with unusually high friction?
- **Manual observations:** What did the user flag as noteworthy? Group by category.
- **Successful patterns vs. friction:** Which harness decisions produced good outcomes? Which produced
  friction or required human intervention?

## Step 4: Create the output directory

```bash
mkdir -p case-study-harness/output
```

## Step 5: Write the case study draft

Write the case study to `case-study-harness/output/case-study-draft.md`.

### Title

Use this format:

```markdown
# Case Study: [Project Name] -- Building with Harness Engineering
```

Use the project name from the repository if identifiable; otherwise use a generic title.

### Required sections

1. **Executive Summary** -- 2-3 paragraph overview of the project, the harness approach used, and the
   headline results.

2. **Project Context** -- What was built. What harness mechanisms were used (CLAUDE.md, rules, skills,
   hooks). How many sessions the build spanned.

3. **Harness Evolution** -- How the harness changed over the course of the build. Cite specific
   `harness_change` entries by timestamp. Note what was added early vs. what emerged later.

4. **What Worked** -- Successful patterns and effective harness decisions. Cite `manual` entries with
   category `successful_pattern` and any `harness_change` entries that correlate with reduced
   friction. Use `user_prompt` entries to provide context for why a decision was made. Each claim
   must reference at least one log entry.

5. **What Failed and How It Was Addressed** -- Friction events, human overrides, and how they were
   resolved. Cite `friction` entries and `manual` entries with category `human_override` or
   `friction`. Use `user_prompt` and `tool_use` entries to reconstruct the sequence of events
   leading to and resolving the failure. Describe the failure, the resolution, and whether a
   harness change resulted.

6. **Context Architecture Observations** -- How context was distributed across CLAUDE.md, rules,
   skills, and hooks. Cite `manual` entries with category `context_architecture` and relevant
   `harness_change` entries. Note any placement decisions that worked well or poorly.

7. **Lessons Learned** -- Key takeaways distilled from the evidence above. Each lesson must cite at
   least one supporting log entry.

### Citation format

Cite log entries inline using this format: `[event_type @ timestamp]`

Examples:
- `[friction @ 2026-04-01T14:30:22+00:00]`
- `[manual/successful_pattern @ 2026-04-02T09:15:00+00:00]`
- `[harness_change @ 2026-04-01T10:00:00+00:00]`

For manual observations, include the category after a slash as shown above.

## Step 6: Write the improvement plan

Write the improvement plan to `case-study-harness/output/improvement-plan.md`.

### Title

```markdown
# Harness Guide Improvement Plan
```

### Required sections

1. **Summary** -- Brief overview of proposed changes and their motivation.

2. **Recommendations** -- A numbered list of specific, actionable changes to the harness engineering
   guide. Each recommendation must include:
   - **What to change** -- the specific guide chapter, template, or section affected. Use the actual
     chapter titles and section headings from the guide content you read in Step 1. Do NOT guess or
     invent chapter names.
   - **Why** -- the evidence from this build that motivates the change
   - **Evidence** -- one or more log entry citations using the `[event_type @ timestamp]` format
   - **Priority** -- high, medium, or low based on how frequently the issue occurred or how severe
     its impact was

3. **Patterns to Document** -- Successful patterns discovered during the build that the guide does
   not currently cover. Cite the supporting evidence.

4. **Antipatterns to Warn About** -- Mistakes or friction patterns that the guide should warn
   against. Cite the supporting evidence.

## Step 7: Confirm

Report to the user:
- How many total log entries were processed
- Entry count per event type
- How many recommendations the improvement plan contains
- The paths to both output files
