---
name: internal-link-graph-architect
description: Design intentional internal link graphs for SEO, UX, and LLM-readable sites. Use this skill when the user asks for links between short briefs, longform articles, topics, projects, author pages, breadcrumbs, source trails, related stories, orphan-page checks, overlink checks, anchor intent, or validation that a link graph reinforces the canonical content model without creating duplicate story bodies or hidden links.
---

# Internal Link Graph Architect

Use this skill after `information-architecture-seo` has defined page roles and canonical policy.

Read [references/link-graph-rules.md](references/link-graph-rules.md) before producing a full graph.

## Owns

- intentional internal link graph;
- brief-to-longform and longform-to-brief links;
- breadcrumbs;
- topic, project, author, community, and source-trail links;
- anchor intent;
- orphan-page checks;
- overlink and duplicate-intent risk checks.

## Does Not Own

- canonical and hreflang policy;
- final URL architecture;
- external backlink placement;
- hidden links;
- visual UI layout;
- schema implementation.

## Workflow

1. Read `url-map.yaml`, page roles, canonical model, language groups, and content model.
2. Identify required structural links: breadcrumbs, brief-longform pairs, topic/project/author/entity links.
3. Add source-trail links only when they are visible and useful to users.
4. Assign `link_type`, `anchor_intent`, `user_reason`, `seo_reason`, and `risk`.
5. Flag orphan pages, circular links without purpose, irrelevant exact-match anchors, and duplicated story-body routes.
6. Produce `internal-link-graph.yaml` using [assets/internal-link-graph.template.yaml](assets/internal-link-graph.template.yaml).
7. Hand off schema/head implications to `technical-seo-schema-engineer` and rendered navigation checks to `ui-ux-llm-product-architect`.

## Link Rules

- Every link must have a user reason.
- A short brief should link to its one longform article when a longform exists.
- A longform article should link back to its brief when the brief remains a standalone news surface.
- Topic pages organize related pages with summaries; they do not duplicate story bodies.
- Author and project links support trust and entity understanding.
- Breadcrumbs clarify hierarchy; they are not keyword stuffing.
- Related links should be sparse and defensible.
- External authority placement is out of scope.

## Safety And Privacy Boundaries

- Do not recommend hidden links, cloaked links, injected footers, irrelevant exact-match anchors, or link stuffing.
- Do not link public pages to admin, private API, private analytics, raw IP logs, staging URLs, secret files, or unpublished drafts.
- Do not create extra public story pages to increase link count.
- Do not weaken UX or accessibility for SEO anchors.

## Validation

Before marking work complete:

- every link has source URL, target URL, type, anchor intent, user reason, SEO reason, and risk;
- every page expected to be discoverable has at least one logical incoming link;
- brief and longform pages are paired without creating extra story bodies;
- topic/project/author links have entity or navigation purpose;
- hidden or irrelevant link recommendations are absent.

Validate skill edits with:

```bash
python3 <codex-skills-dir>/senior-skill-architect/scripts/lint_production_skill.py ./skills/internal-link-graph-architect
python3 ./plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py .
```

Forward tests live in [evals.json](evals.json).

## Output Shape

Return:

1. Link graph summary.
2. Required structural links.
3. Optional related links.
4. Orphan/overlink risks.
5. Handoff notes for technical SEO/schema and UX.

