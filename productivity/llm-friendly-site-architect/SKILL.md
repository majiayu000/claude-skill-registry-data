---
name: llm-friendly-site-architect
description: Design human-visible, machine-readable website layers for AI assistants, RAG, and agentic search. Use this skill when the user asks for llms.txt, LLM discovery plans, visible TLDR or direct-answer blocks, source trails, entity pages, markdown alternates, AI crawler policy, topic-to-URL maps, assistant-readable public content, or LLM-friendly architecture that must preserve canonical SEO strategy without hidden bot-only facts or duplicate story bodies.
---

# LLM Friendly Site Architect

Use this skill after semantic core, URL architecture, internal link graph, and technical SEO/schema foundations exist.

Read [references/llm-readable-architecture.md](references/llm-readable-architecture.md) before producing a full LLM discovery plan.

## Owns

- `llms.txt` structure;
- LLM discovery plan;
- visible answer blocks and concise summaries;
- source trails;
- entity pages and topic maps for agents;
- markdown alternate policy;
- AI crawler policy handoff;
- no-duplicate-content guardrails for LLM-readable surfaces.

## Does Not Own

- Search Console or assistant citation monitoring execution;
- technical schema implementation;
- URL/canonical decisions;
- hidden content;
- external authority placement.

## Workflow

1. Read `url-map.yaml`, `internal-link-graph.yaml`, schema/head policy, and visible content model.
2. Identify canonical public pages that should be discoverable by assistants.
3. Draft or audit `llms.txt` sections with only public useful URLs.
4. Define visible direct-answer, TLDR, facts, source, or FAQ blocks only where page role supports them.
5. Define source-trail and citation-ready evidence surfaces.
6. Define markdown alternate rules for longform/docs pages when useful, with noindex or alternate policy as appropriate.
7. Define entity pages and topic pages that clarify who, what, and how the site works.
8. Record crawler policy items that need current primary-source verification.
9. Produce an LLM discovery report using [assets/llm-discovery-report.template.md](assets/llm-discovery-report.template.md).

## Non-Negotiables

- Human-visible content first.
- No hidden bot-only facts.
- No doorway pages.
- No FAQPage schema unless FAQ is visible.
- No automatic TLDR on every short news page by default.
- No extra public story bodies beyond the declared content model.
- `llms.txt` is a helpful convention, not a guaranteed ranking or citation factor.
- Crawler names, policies, and IPs require primary-source verification before production changes.

## Page Role Guidance

- `news_brief`: concise visible summary, source link, paired longform link when available. Do not force TLDR if the brief already is the short form.
- `longform_article`: can include visible summary, key facts, source trail, topic/entity links, and markdown alternate.
- `topic`: good candidate for direct answer and entity/topic explanation.
- `project`: good candidate for capability summary, repository links, evidence, and related stories.
- `author`: good candidate for Person/entity context and trust signals.
- `home`: can include a concise site purpose and section map.

## Safety And Privacy Boundaries

- Do not include admin, API, private dashboards, raw analytics, raw IP logs, secrets, unpublished drafts, staging URLs, or internal planning notes in `llms.txt`, markdown alternates, source trails, or entity maps.
- Do not relax WAF, auth, CSP, CORS, cookies, rate limits, or private-content boundaries for assistant access.
- Do not claim that a crawler, AI assistant, or search engine will cite the site without timestamped evidence.

## Validation

Before marking work complete:

- every LLM-facing URL is public, canonical, useful, and non-private;
- every answer/source block is visible to humans;
- every markdown alternate has a corresponding canonical HTML page;
- no duplicate public story body is introduced;
- crawler policy items are marked as verified or requiring verification;
- citation/monitoring claims are handed off to a monitoring task.

Validate skill edits with:

```bash
python3 <codex-skills-dir>/senior-skill-architect/scripts/lint_production_skill.py ./skills/llm-friendly-site-architect
python3 ./plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py .
```

Forward tests live in [evals.json](evals.json).

## Output Shape

Return:

1. LLM-readable architecture summary.
2. `llms.txt` section plan.
3. Visible answer/source/entity block plan.
4. Markdown alternate policy.
5. Crawler verification needs.
6. Refused or deferred items.

