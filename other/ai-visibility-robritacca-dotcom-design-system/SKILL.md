---
name: ai-visibility
description: "Monthly loop that measures how findable robertritacca.com is to search engines and AI assistants, and trends it run over run. Runs the SEO sweep, pulls the search and AI-referral slice from GA, probes llms.txt from outside, ranks the target queries, and writes the trend report. Use when asked to run the AI visibility loop. Off-property actions are proposals only; never pushes, merges, or deploys."
icon: query_stats
displayDescription: "Measures whether the site is getting more findable, by search engines and by AI assistants, and turns one-off checks into a trend. Each run sweeps the technical SEO surface, pulls the search and AI-referral traffic slice, probes the public agent surfaces from outside, records where the target queries actually rank, and compares it all with the last run. The deliverable is the trend report; anything off-property is a proposal. One of the loops described on the Loops page."
invoke: ["run the ai visibility loop","/ai-visibility"]
---

# ai-visibility

Monthly measurement loop for one goal: robertritacca.com findable on the first page for its target queries, by search engines and by AI assistants. The individual instruments already exist — this loop runs them together on a cadence and keeps the trend, because a single ranking check is an anecdote and the same check monthly is a direction. **The trend report is the deliverable. Off-property actions are proposals only, and nothing pushes, merges, or deploys.**

## Target queries

This list is the loop's one owned fact — edit it here deliberately, never inline in a run:

- `product designer Toronto AI`
- `AI product designer Toronto`
- `Rob Ritacca`
- `Rob Ritacca designer`

## When invoked

Run when asked to "run the AI visibility loop" (`/ai-visibility`), or by a scheduled task once one is created.

## Scope guardrails (read first)

- **Measurement first.** A run that changes nothing but records the numbers is the normal case, not a failure.
- **On-site fixes go only through the `seo-audit` skill**, under its own guardrails (behind-the-scenes only, crawl-policy changes report-only, branch `seo/YYYY-MM-DD-<slug>`). This loop adds no second editing path.
- **No copy written for rankings.** Words on the site exist for readers and follow `content-design.md`; a ranking motive never justifies a keyword-shaped sentence. Copy changes belong to the growth loop, driven by engagement data.
- **Off-property moves are proposals.** Directory listings, backlinks, profile updates, posting anywhere — named in the report with a reason, never performed.

## The loop

### 0. Read the trend

Read the previous `ai-visibility-*.md` reports in `ga-analysis/loop-reports/` (git-ignored, local-only) — the run-over-run comparison is the whole point. Also check for unmerged `seo/*` branches from earlier runs; an unmerged fix still pending is context, not something to redo. First run: this report becomes the baseline, and say so.

### 1. Sweep the technical surface

Run the `seo-audit` skill (`.claude/skills/seo-audit/SKILL.md`). It owns the metadata/sitemap/robots/structured-data checks, fixes the safely-fixable on its own branch, and reports — fold its outcome into this run's report rather than repeating its work.

### 2. Pull the discovery traffic

Pull GA with the `ga-report` skill's judgment (it owns the bot list and baselines; it and the GA venv live on Rob's Mac). The slice this loop cares about: organic search sessions and their landing pages, plus referrals from AI surfaces — chatgpt.com, perplexity.ai, gemini.google.com, claude.ai and kin. Note the blind spot in the report: agents fetching `llms.txt` never execute the analytics snippet, so GA structurally undercounts agent traffic. Absence of AI referrals is weak evidence of absence.

### 3. Probe the agent surfaces from outside

Live requests against production, as a stranger's agent would make them, against the canonical apex host (`SITE_URL` in `website/src/config/site.ts`, which `node scripts/site-config.mjs` prints — the `www` host is a redirect, and probing it would measure the redirect chain rather than the canonical surface): `/llms.txt` returns 200 and every link it advertises resolves. There is no MCP endpoint to probe here any more; it went to rift-ds.com with the design system, and that site owns its own visibility. This surface is how an AI assistant learns the site exists — a quiet regression here is invisible to every other check, including GA.

### 4. Rank the target queries

Web-search each target query and record where robertritacca.com lands (position, or "not in the first page"), plus which competing results outrank it. Then the AI half: ask an assistant-shaped question per query ("who is Rob Ritacca, the product designer?" and one query-phrased variant) via web search and note whether the site is cited or paraphrased. Record the method beside the numbers — rankings are noisy and personalized, and the trend only means something when consecutive runs measured the same way.

### 5. Report

Save to `ga-analysis/loop-reports/ai-visibility-YYYY-MM-DD.md` **and** repeat in full in the final message. Plain English, four parts: the **trend table** (this run beside the previous ones — rankings, organic sessions, AI referrals, agent-surface status), **what changed** since last run and the likely why, **what the seo-audit leg did** (its branch, if any), and **proposals** — the off-property moves that would help, each with its reason, for the user to act on or ignore. End with the reminder that nothing is pushed or deployed.
