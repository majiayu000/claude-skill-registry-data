---
name: using-semantic-seo-geek
description: Route broad or ambiguous semantic SEO requests to the smallest suitable specialist workflow. Use for multi-part SEO work, requests that ask which specialist to use, or tasks spanning technical SEO, site architecture, entity modeling, titles and headings, visuals, AI-search visibility, content production, or content review.
---

# Route Semantic SEO Work

## Scope

Route work; do not replace specialist judgment.

Use this skill to:

- identify the user's primary deliverable;
- select the minimum specialist set that covers it;
- order dependent work and define handoffs;
- surface missing inputs that materially change the route.

Do not use this router to perform a specialist audit, strategy, rewrite, or implementation.

## Explicit-request rule

Honor every explicitly named specialist.

Never replace, suppress, or reinterpret an explicit specialist request because another route seems preferable.

If the requested specialist appears mismatched, use it and state the concern; add a supporting handoff only when useful.

If the user names several specialists, retain all of them and follow the user's order unless a dependency makes that impossible.

## Evidence labels

Apply these labels whenever the routing decision depends on facts:

- **Observed** — directly verified in a supplied site, file, report, or dataset.
- **Sourced** — supported by a cited current primary source.
- **Inferred** — reasoned from Observed or Sourced evidence; state the reasoning.
- **Unknown** — not verified; state what evidence would resolve it.

Do not present an Inferred or Unknown claim as Observed.

## Routing map

- Crawlability, indexability, rendering, canonicals, sitemaps, redirects, or structured-data delivery: `technical-seo`.
- Site hierarchy, topic coverage, page relationships, URLs, or internal-link planning: `topical-map-architect`.
- Entity identification, disambiguation, attributes, values, or Schema.org mapping: `eav-optimizer`.
- Title elements, main headings, heading outlines, or title-link diagnostics: `title-heading-optimizer`.
- Image purpose, alternative text, image discovery, visual metadata, or visual accessibility: `visual-semantics`.
- Visibility, citations, crawler controls, or reputation across AI search and answer systems: `aiseo-strategist`.
- Page creation that combines several on-page requirements: `page-production`.
- Drafting or rewriting prose: `algorithmic-writer`.
- Content quality, compliance, or gap review: `content-auditor`.
- Human voice and removal of formulaic copy: `content-humanizer`.

Do not invoke an unrelated specialist merely to make the workflow look comprehensive.

## Workflow

1. Restate the requested outcome in one sentence.
2. Record any specialist explicitly named by the user.
3. Separate deliverables that can run independently from those with dependencies.
4. Match each deliverable to the routing map.
5. Choose one primary specialist for the immediate outcome.
6. Add supporting specialists only for distinct deliverables or required prerequisites.
7. Order prerequisites before dependent tasks.
8. Ask a question only when a missing answer would materially change the route.
9. Otherwise, proceed with a stated, low-risk assumption.
10. Apply each selected specialist's own output contract.

## Common sequencing

- For a site rebuild: technical access review, architecture, entity model, templates, then page production.
- For an existing-page improvement: audit the requested surface first, then write or implement only if asked.
- For structured data: model truthful page-visible facts before technical implementation and validation.
- For AI-search work: verify access and source clarity before proposing measurement or content expansion.
- For image-heavy pages: classify image purpose before writing alternative text or metadata.

These are defaults, not mandatory stages.

## Exact output contract

For a routing-only request, return exactly these sections in this order:

1. `Selected specialist` — one skill name, or the explicitly requested set.
2. `Reason` — one concise sentence tied to the requested deliverable.
3. `Inputs` — available inputs and material Unknowns.
4. `Sequence` — ordered specialist names; omit if only one is needed.
5. `Handoffs` — downstream deliverable, receiving specialist, and trigger condition.

For a request to do the work, do not stop at a routing memo.

Execute the selected specialist workflow and use that specialist's exact output contract.

For a request to do the work, append a `Handoffs` section only when another specialist has a
concrete next deliverable. For a routing-only request with no handoff, return `Handoffs: None`.

## Handoffs

Pass the user goal, scope, evidence register, unresolved Unknowns, and accepted decisions.

Do not ask the next specialist to rediscover verified evidence without a reason.

Keep fact gathering distinct from recommendations so later specialists can challenge Inferred claims.

## Guardrails

- Do not promise rankings, traffic, indexing, rich results, or AI citations.
- Do not fabricate observations, sources, tool output, or specialist availability.
- Do not describe an unsupported tactic as a ranking factor.
- Do not invent statistics, fixed content lengths, or universal thresholds.
- Do not route toward deceptive markup, fake mentions, doorway pages, or scaled low-value content.
- Cite current primary documentation for claims about a platform's behavior.
- State uncertainty and provider-specific differences instead of blending them.
