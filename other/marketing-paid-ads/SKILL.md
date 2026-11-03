---
name: marketing-paid-ads
description: Plan paid advertising campaigns — platform choice, campaign and ad-group structure, targeting, keywords, budget, bidding and an optimization playbook. Use when the user wants to start or fix their spending on Google, Meta, LinkedIn or other ad platforms. Not for writing the ad copy itself; see /marketing-ad-creative.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: marketing
  phase: 3
  artifact: 03-convert.md
---

# Paid Ads

Plan paid advertising campaigns for "$ARGUMENTS". Design campaign structure, targeting, budget allocation, and optimization strategy.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"marketing-paid-ads","workflow":"marketing","phase":3,"project":"<project>","event":"skipped","artifact":"03-convert.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 3 (Convert) of the RACE Framework workflow (`marketing`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `marketing` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"marketing-paid-ads","workflow":"marketing","phase":3,"project":"<project>","event":"refused","artifact":"03-convert.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"marketing-paid-ads","workflow":"marketing","phase":3,"project":"<project>","event":"started","artifact":"03-convert.md","note":""}`.

Read `.singularskills/marketing/<project>/00-strategy.md`. If this file does not exist, tell the user:

> Phase 0 (Strategy) has not been completed for "<project>". Run `/marketing-customer-research <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context:**
   - Read `.singularskills/marketing/<project>/00-strategy.md` for audience, positioning, and competitors
   - Read `.singularskills/marketing/<project>/02-act.md` if it exists (for landing page and copy context)
   - Read `references/campaign-plan-template.md` for structure

2. **Platform selection:**
   - Which platforms? Google Ads, Meta (Facebook/Instagram), LinkedIn, X, TikTok, Reddit
   - Match platform to audience and intent (search intent vs. interruption marketing)
   - Budget allocation per platform

3. **Campaign structure:**
   - Campaign hierarchy: campaigns → ad groups → ads
   - Targeting strategy per campaign: keywords, audiences, demographics, interests
   - Match types (for search): broad, phrase, exact
   - Negative keyword strategy
   - Retargeting setup: website visitors, cart abandoners, engaged users

4. **Budget and bidding:**
   - Recommended daily/monthly budget
   - Bidding strategy: manual CPC, target CPA, maximize conversions
   - Budget pacing and scaling plan
   - Expected CPC and CPA ranges for the category

5. **Optimization plan:**
   - Key metrics to monitor: CTR, CPC, CPA, ROAS, quality score
   - Optimization cadence (daily, weekly, monthly actions)
   - When to scale, pause, or restructure campaigns
   - Testing plan: ad copy, audiences, landing pages

6. **Write the artifact** — append to `.singularskills/marketing/<project>/03-convert.md` under a `## Paid Ads` section. Create the file with a `# Convert — <project>` heading if it does not exist; if a `## Paid Ads` section already exists, replace only that section. The section contains:
   - **Platform Strategy** — selected platforms with rationale
   - **Campaign Structure** — hierarchy, targeting, match types
   - **Budget Plan** — allocation, bidding, pacing
   - **Ad Copy Direction** — messaging angles per campaign
   - **Optimization Playbook** — metrics, cadence, scaling rules

## Output

Paid ads strategy appended to `.singularskills/marketing/<project>/03-convert.md`. Present a summary highlighting:
- Recommended platforms and budget split
- Campaign structure overview
- Expected CPA range

**Record the run.** After you have written your section, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"marketing-paid-ads","workflow":"marketing","phase":3,"project":"<project>","event":"finished","artifact":"03-convert.md","note":""}`.

This artifact is shared by every skill of phase 3 (Convert). The frontmatter is written once, by whoever creates the file: if you create it, open it with the block below (`skill` is the phase title, `started` the time of that first write; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`); if it already exists, leave the block alone except to update `finished` and to set `gate` to the worst value among the sections (`skipped` over `passed`).

```yaml
---
skill: Convert
workflow: marketing
phase: 3
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

Open your `## Paid Ads` section with one italic line, `*<skill name> · <ISO timestamp> · gate: <passed|skipped>*` (your skill name is `marketing-paid-ads`).

End your section with `### Decisions` and `### Open questions` (one level under your `## Paid Ads` heading, so the section stays one block), in this shape:

```markdown
### Decisions
- <what was chosen> — <why> — <what was rejected>

### Open questions
- <what the next phase or a reviewer must settle>
```
