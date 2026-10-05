---
name: information-architecture-seo
description: Convert a semantic core into crawlable SEO and LLM-friendly information architecture. Use this skill when the user asks for URL structure, page taxonomy, canonical rules, hreflang groups, page roles, pillar/topic/news/article/blog/project separation, multilingual route strategy, or a durable content model such as one short brief plus one longform article. It prevents duplicate public content bodies and hands link-graph work to internal-link-graph-architect.
---

# Information Architecture SEO

Use this skill after `semantic-core-architect` and before internal linking, schema, or LLM-readable layers.

Read [references/url-architecture.md](references/url-architecture.md) before producing a full URL map.

## Owns

- URL strategy;
- page taxonomy;
- page roles and content ownership;
- canonical model;
- hreflang groups;
- index/noindex policy;
- pillar/topic/news/article/blog/project role separation;
- duplicate-content prevention.

## Does Not Own

- semantic core creation;
- final page copy;
- internal link graph details;
- JSON-LD implementation;
- rendered UI design;
- external backlinks.

## Workflow

1. Read the semantic core, entity-topic map, site constraints, languages, and content model.
2. Identify the canonical page role for each cluster/entity/topic.
3. Define route patterns before individual URLs.
4. Set canonical policy per page role.
5. Define hreflang groups for localized equivalents.
6. Mark page status: `planned`, `draft`, `published`, `noindex`, or `deferred`.
7. Record duplicate-content risks and ownership boundaries.
8. Produce `url-map.yaml` using [assets/url-map.template.yaml](assets/url-map.template.yaml).
9. Hand off to `internal-link-graph-architect` and `technical-seo-schema-engineer`.

## Canonical Rules

- A page can be self-canonical when it has a distinct user/search role and visible content.
- A short news brief and one expanded longform article can both be self-canonical when the brief is the fast news surface and the longform is the durable explanation surface.
- Do not canonicalize a standalone brief to its longform by default.
- Do not create extra public story variants beyond the declared model.
- Topic and pillar pages must summarize and organize; they must not duplicate article bodies.
- Locale alternates use `hreflang`; they do not replace canonical self-reference.

## Multilingual Rules

- Default language owns `x-default` unless the site has a separate language selector page.
- Every localized page must declare its own canonical URL.
- Hreflang groups must contain only true equivalents, not loosely related pages.
- If translation quality is unknown, mark the localized page as `draft` or `deferred`, not published.

## Safety And Privacy Boundaries

- Do not expose admin, API, private dashboards, raw analytics, raw IP logs, secret files, or staging URLs as public indexable pages.
- Use `noindex` or blocked internal routing for low-value utility pages; do not rely on public navigation hiding.
- Do not weaken authentication, access control, or security headers for crawlability.
- Do not place private source URLs, credentials, tokens, unpublished drafts, or internal notes in `url-map.yaml`, sitemap plans, or public LLM-facing artifacts.

## Validation

Before marking work complete:

- every page has URL, page type, locale, canonical, index policy, and rationale;
- every language alternate has a coherent hreflang group;
- every story has at most one brief and one longform per language;
- topic pages do not duplicate article bodies;
- final link graph details are left for `internal-link-graph-architect`;
- schema implementation is left for `technical-seo-schema-engineer`.

Validate skill edits with:

```bash
python3 <codex-skills-dir>/senior-skill-architect/scripts/lint_production_skill.py ./skills/information-architecture-seo
python3 ./plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py .
```

Forward tests live in [evals.json](evals.json).

## Output Shape

Return:

1. URL strategy summary.
2. Page role table.
3. Canonical and hreflang policy.
4. Duplicate-content risks.
5. Handoff notes for internal linking and technical SEO/schema.
