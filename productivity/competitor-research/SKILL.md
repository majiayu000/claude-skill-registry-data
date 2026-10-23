---
name: competitor-research
description: >-
  Full competitor deep-dive on a company by its domain — site parsing (products, customers, pricing), community sentiment, ads from transparency libraries, SEO, team, PR, Parallel deep research — ending in a knowledge base and an HTML report with satellite pages. Use for "research competitor X", "full dossier on X", "build a knowledge base on X", "competitor teardown of X". For a single layer use the narrower skills instead (ads-parser, ahrefs, parallel-research).
---

# Competitor research — the full pipeline

A multi-skill: it orchestrates the whole pipeline and uses three sub-skills on their layers:

- **parallel-research** — deep-research tasks (briefs, submit, background polling);
- **ads-parser** — ads from LinkedIn, Google and Meta libraries (and the LinkedIn traps);
- **ahrefs** — SEO data (quick lookups for a domain).

Keys needed: `PARALLEL_API_KEY`, `SEARCHAPI_KEY`, `AHREFS_MCP_KEY` (see `connections/`). The pipeline still works without Ahrefs — the SEO layer becomes a gap in the report.

Typical cost of one run: 8–9 Parallel `ultra` tasks, a few dozen SearchApi calls, a few hundred to a few thousand Ahrefs units, and ~15–20 subagents of model time. Tell the user the expected cost before starting.

## Order of work

Phases, agent prompt templates and the folder structure are in `references/pipeline.md` — read it before starting. In short:

0. **Foundation.** Check memory and past reports — don't rebuild what is already known. Get the sitemap and cluster the URLs. Try `/llms.txt` on the docs subdomain.
1. **Deep research.** Submit 8–9 `ultra` tasks from `references/parallel-briefs.md` (placeholder `{ANCHOR}`) **before** the collection phase — they run 30–60 minutes on Parallel's side. Start one background poller.
2. **Collection.** ~15–17 subagents in parallel: site ×6, community ×7, ads, SEO, team ×2. Each writes one file and returns `{file, key_findings, gaps}`.
3. **Synthesis.** Three agents: positioning + ICP + sales points; company dossier; battlecard only if explicitly asked.
4. **Report.** A main `report.html` plus satellite pages (launches, ads, PR, tutorials, community) linked with card buttons. Paste the style contract from `references/report-rules.md` **verbatim into every writing agent's prompt**.
5. **Memory.** Save where everything lives and the main facts, so the next run starts from them.

### Running many agents

- If workflows are available in your Claude Code, run phase 2 as one Workflow with all agents in `parallel()` and a schema `{file, key_findings, gaps}`. If it stops on a usage limit, resume it with the same run id — finished agents come back from cache.
- Otherwise launch the subagents with the Agent tool, 5–6 per message, and wait for each batch. Same prompts, same output contract.

## Execution rules

- **Checkpoints with the user.** After collection, show the key findings. The report is iterated on feedback; the first version is never final.
- **Raw is separate from analysis.** `raw/` keeps JSON, HTML and screenshots; every fact in the report is checked against raw.
- **The report is about the competitor only.** No comparisons with the user's own company and no "what this means for us" sections unless explicitly asked.
- **Never log in anywhere.** Public pages, public libraries and search results only.
- **Publishing.** Pages are standalone HTML files. If you publish them as Artifacts, replace relative links between pages with the published URLs.

## Adapt it

- Replace the agent list with the layers that matter in your market. A B2C app needs app-store reviews and TikTok more than GitHub and Hacker News.
- Your own report feedback is the most valuable part: after every review, add the corrections to `references/report-rules.md`. That file is how the next report comes out right the first time.
