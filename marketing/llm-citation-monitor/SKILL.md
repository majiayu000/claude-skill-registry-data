---
name: llm-citation-monitor
description: Plan and record evidence-backed LLM and AI-search citation checks across approved assistant/search surfaces with timestamped queries, locales, modes, cited URLs, snippets, screenshots or transcripts, and caveats. Use this skill when the user asks whether ChatGPT, Perplexity, Claude, Gemini, Copilot, or another assistant cites a target site, but do not claim citation without direct evidence.
---

# LLM Citation Monitor

Use this skill after the target site's SEO/LLM discovery layer exists and the user wants to
measure assistant/search citation visibility.

Read [references/citation-evidence-policy.md](references/citation-evidence-policy.md) before producing a monitoring plan or report.

## Owns

- target question matrix;
- manual observation workflow;
- citation report template;
- assistant/search surface evidence policy;
- competitor citation capture;
- caveats for personalization, locale, freshness, and account state;
- refusal of unsupported citation claims.

## Does Not Own

- assistant account credentials;
- bypassing bot protections;
- scraping assistant/search surfaces without approval;
- changing robots, WAF, auth, or crawler policy;
- ranking claims;
- content/schema implementation.

## Workflow

1. Define target site, page set, audience, locale, and target questions.
2. Classify query intent: brand, topic, problem, comparison, how-to, or citation-check.
3. Choose approved observation mode: manual, exported transcript, screenshot, API/tool report, or public fetch.
4. For each run, record surface, model/search product if visible, date/time, locale, account state, query text, answer summary, cited URLs, quote/snippet, and caveats.
5. Capture competitor citations separately from target citations.
6. Mark missing citations as `not observed`, not as "does not cite anywhere".
7. Produce a report using [assets/citation-report.template.md](assets/citation-report.template.md).
8. Hand off site-content or technical fixes to SEO/LLM architecture skills.

## Non-Negotiables

- Do not claim "ChatGPT cites us" without direct citation evidence.
- Do not treat one personalized answer as universal ranking.
- Do not store assistant credentials, cookies, account tokens, or private conversation data in skill files.
- Do not bypass paywalls, auth, robots, WAF, or tool restrictions.
- Do not scrape surfaces against terms of service.
- Do not publish screenshots/transcripts containing private user data.

## Safety And Privacy Boundaries

- Reports should contain only approved public query text, public cited URLs, and redacted/private-safe snippets.
- If a screenshot or transcript includes account details, remove them before adding to shared artifacts.
- If a user provides a private assistant transcript, summarize it locally and ask before storing it.
- Treat model version, locale, date/time, and account state as part of the evidence, not incidental metadata.

## Evidence Labels

- `Cited`: target URL appears as a cited/source URL in the answer or citation panel.
- `Mentioned`: target brand/page mentioned but not cited.
- `Not observed`: no target citation in this run.
- `Competitor cited`: another domain was cited for the target question.
- `Invalid evidence`: missing timestamp, surface, query, or cited URL.

## Validation

Validate skill edits with:

```bash
python3 <codex-skills-dir>/senior-skill-architect/scripts/lint_production_skill.py ./skills/llm-citation-monitor
python3 ./plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py .
```

Forward tests live in [evals.json](evals.json).

## Output Shape

Return:

1. Monitoring objective and target pages.
2. Query matrix.
3. Approved surfaces and observation mode.
4. Citation evidence table.
5. Competitor citation table.
6. Caveats and limitations.
7. Fix backlog routed to the correct skill owner.
