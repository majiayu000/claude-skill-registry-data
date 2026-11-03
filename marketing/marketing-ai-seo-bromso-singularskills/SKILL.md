---
name: marketing-ai-seo
description: Optimize a brand's visibility in AI search — ChatGPT, Perplexity, Google AI Overviews — by checking where it is cited and planning LLM-friendly content and entity signals. Use when the user asks why AI assistants do not mention their product or how to get cited in AI answers. Not for classic Google rankings; see /marketing-seo-audit.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: marketing
  phase: 1
  artifact: 01-reach.md
---

# AI SEO

Optimize "$ARGUMENTS" for AI-powered search — LLM citations, Google AI Overviews, ChatGPT, Perplexity, and other AI search surfaces.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"marketing-ai-seo","workflow":"marketing","phase":1,"project":"<project>","event":"skipped","artifact":"01-reach.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Reach) of the RACE Framework workflow (`marketing`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `marketing` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"marketing-ai-seo","workflow":"marketing","phase":1,"project":"<project>","event":"refused","artifact":"01-reach.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"marketing-ai-seo","workflow":"marketing","phase":1,"project":"<project>","event":"started","artifact":"01-reach.md","note":""}`.

Read `.singularskills/marketing/<project>/00-strategy.md`. If this file does not exist, tell the user:

> Phase 0 (Strategy) has not been completed for "<project>". Run `/marketing-customer-research <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context:**
   - Read `.singularskills/marketing/<project>/00-strategy.md` for positioning and audience
   - Read `.singularskills/marketing/<project>/01-reach.md` if it exists (for content and SEO context)
   - Read `references/seo-checklist.md` for AI search section

2. **Audit current AI visibility:**
   - Use WebSearch to check if "<project>" appears in AI-generated answers
   - Test key queries in multiple AI search tools
   - Note which competitors are being cited by AI

3. **Analyze AI citation patterns:**
   - What content structure gets cited by LLMs? (lists, definitions, comparisons, data)
   - Which domains are most frequently cited in the category?
   - What makes content "LLM-friendly"? (clear structure, authoritative sources, direct answers)

4. **Develop optimization strategy:**
   - Content structure recommendations (clear H2s, direct answers, FAQ format)
   - Entity optimization (be clearly identifiable as an entity with consistent naming)
   - E-E-A-T signals (experience, expertise, authority, trust markers)
   - Structured data to aid AI understanding
   - Citation-worthy content types (original research, data, tools, definitions)

5. **Write the artifact** — append to `.singularskills/marketing/<project>/01-reach.md` under a `## AI SEO` section. Create the file with a `# Reach — <project>` heading if it does not exist; if a `## AI SEO` section already exists, replace only that section. The section contains:
   - **Current AI Visibility** — where "<project>" appears (or doesn't) in AI answers
   - **Citation Patterns** — what gets cited in this category
   - **Optimization Strategy** — content structure, entity, E-E-A-T recommendations
   - **Content Recommendations** — specific content to create for AI visibility
   - **Monitoring Plan** — how to track AI search presence

## Output

AI SEO strategy appended to `.singularskills/marketing/<project>/01-reach.md`. Present a summary highlighting:
- Current AI search visibility status
- Top 3 optimization opportunities
- Most impactful content type to create

**Record the run.** After you have written your section, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"marketing-ai-seo","workflow":"marketing","phase":1,"project":"<project>","event":"finished","artifact":"01-reach.md","note":""}`.

This artifact is shared by every skill of phase 1 (Reach). The frontmatter is written once, by whoever creates the file: if you create it, open it with the block below (`skill` is the phase title, `started` the time of that first write; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`); if it already exists, leave the block alone except to update `finished` and to set `gate` to the worst value among the sections (`skipped` over `passed`).

```yaml
---
skill: Reach
workflow: marketing
phase: 1
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

Open your `## AI SEO` section with one italic line, `*<skill name> · <ISO timestamp> · gate: <passed|skipped>*` (your skill name is `marketing-ai-seo`).

End your section with `### Decisions` and `### Open questions` (one level under your `## AI SEO` heading, so the section stays one block), in this shape:

```markdown
### Decisions
- <what was chosen> — <why> — <what was rejected>

### Open questions
- <what the next phase or a reviewer must settle>
```
