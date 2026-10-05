---
name: server-log-crawler-analyst
description: Analyze credential-free public website monitoring evidence from server access logs, HTTP fetches, robots/llms/sitemap checks, and exported summaries while protecting raw IP and private query data. Use this skill when the user asks whether crawlers or AI bots reached a site, whether public SEO/LLM discovery files respond, or how to separate observed facts from unknown Search Console, rank, analytics, or citation claims.
---

# Server Log Crawler Analyst

Use this skill when credential-free monitoring evidence is enough, or when credentialed
Search Console, rank tracking, analytics, or assistant citation tools are unavailable.

Read [references/data-source-tiers.md](references/data-source-tiers.md) before producing a monitoring report.

## Owns

- credential-free monitoring baseline;
- server access-log summary with IP privacy protection;
- crawler/user-agent observation reports;
- public HTTP checks for robots, llms.txt, sitemaps, RSS, and representative URLs;
- data-source tiering;
- monitoring limitations and unknowns;
- backlog handoff for Search Console, rank/SERP, analytics, and LLM citation monitoring.

## Does Not Own

- credentialed Search Console or analytics API work;
- scraping search engines;
- bypassing bot protections;
- live firewall or WAF changes;
- claims about rankings or assistant citations without direct evidence;
- storing raw IP logs in public artifacts.

## Workflow

1. Identify available evidence: public URL fetches, access-log snippet, exported summary, or synthetic fixture.
2. Label the evidence tier and collection time.
3. If logs are provided, summarize requests by path, status, user-agent class, and redacted IP hash.
4. Separate known crawler hits from unknown bot-like traffic.
5. Check public discovery endpoints when requested.
6. Record limitations: no Search Console, no rank data, no assistant citation data unless explicitly provided.
7. Produce a monitoring report using [assets/crawler-monitor-report.template.md](assets/crawler-monitor-report.template.md).
8. Hand off credentialed or citation tasks to the backlog.

## Non-Negotiables

- Do not publish raw IP addresses.
- Do not store credentials, cookies, API keys, or private analytics exports in skill files.
- Do not infer ranking, indexing, or citation success from server logs alone.
- Do not claim a user-agent is verified Google/OpenAI/Claude/Perplexity unless verification method is documented.
- Do not scrape SERPs or assistants against terms of service.
- Do not change firewall, WAF, robots, or server config from this skill.

## Safety And Privacy Boundaries

- Treat raw logs as private by default.
- Use aggregated counts and redacted identifiers.
- Keep exact timestamps only when needed for evidence; otherwise aggregate by hour/day.
- If the user asks to publish a report, remove raw IP, query strings, session IDs, auth paths, and admin URLs unless explicitly needed and safe.
- Public reports should say "observed in provided logs" rather than "definitely crawled by" unless bot verification is complete.

## Evidence Labels

- `Observed`: directly in log, HTTP response, or exported report.
- `Verified`: observed and checked by an accepted verification method.
- `Inferred`: likely based on user-agent/path/status, but not verified.
- `Open`: no evidence available in this run.

## Validation

Validate skill edits with:

```bash
python3 <codex-skills-dir>/senior-skill-architect/scripts/lint_production_skill.py ./skills/server-log-crawler-analyst
python3 ./skills/server-log-crawler-analyst/scripts/analyze_access_log.py ./skills/server-log-crawler-analyst/fixtures/sample-access.log --report <tmp-dir>/server-log-crawler-report.json
python3 ./plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py .
```

Forward tests live in [evals.json](evals.json).

## Output Shape

Return:

1. Evidence source and timestamp.
2. Data tier and privacy handling.
3. Observed crawler/user-agent classes.
4. Public endpoint status checks if performed.
5. Suspicious or irrelevant bot traffic summary.
6. Unknowns and claims refused.
7. Monitoring backlog and next evidence needed.
