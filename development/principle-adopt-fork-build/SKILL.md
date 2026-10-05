---
name: principle-adopt-fork-build
description: "Adopt/Fork/Build"
---

# Adopt/Fork/Build

Restate a proposed idea, search for serious existing projects, and produce a recommendation on whether to adopt, fork, or build. Treat this as a pre-development architecture review, not an implementation task.

## Rules

- Warn the user before searching if the idea appears sensitive, proprietary, or commercially confidential. Ask them to anonymize it first if needed.
- Use existing search capabilities (Perplexity / Google deep research / web search) and focused `site:` queries. Do not invent custom API integrations.
- Search GitHub first for every request. Do not skip directly to package indexes or model hubs.
- Keep the search narrow and evidence-based. Inspect only the strongest candidates instead of scraping large result sets.
- For each serious GitHub candidate, inspect repository structure and at least 1 to 3 implementation files. Do not rely on `README`, repo description, or tags alone to judge actual capabilities.
- Include a real clickable URL for every project, package, model, or dataset mentioned.
- Do not fabricate popularity, maintenance, or capability claims. If evidence is weak, say so explicitly.
- Use current maintenance and adoption signals. Prefer real recency indicators, stars, forks, downloads, model likes, or similar ecosystem-specific traction signals when available.
- Stop and ask for confirmation after the GitHub phase and again after the secondary-platform phase before continuing to a broader search or final synthesis.

## Use when

Use this skill proactively when the user is clearly about to build a complete product, subsystem, or workflow from scratch, even if they did not explicitly ask for a build-vs-buy review yet.

Strong trigger patterns:

- "I want to build", "help me build", "I am going to make", "create a project for"
- complete systems such as auth, upload, queue, editor, parser, crawler, chat, scheduling, feature flags, developer portals, agent frameworks, or workflow engines
- requests that imply a reusable product rather than a one-off script or tiny fix
- "from scratch", "without dependencies", "implement my own", "no framework"

High-frequency wheel-making areas:

- auth and permissions
- parsing and document extraction
- infrastructure and workflow orchestration
- common business subsystems such as billing, uploads, editors, dashboards, or notifications
- AI agent frameworks, automation runners, and multimodal pipelines

Do not trigger by default when:

- the user explicitly says the task is for learning, teaching, or practice
- the user is debugging or modifying an existing codebase
- the request is a narrow algorithm, regex, or function-level question
- the user has already chosen a concrete upstream project and wants help using it
- the task is obviously local and one-off rather than a reusable product decision

## Platform selection

Use primary search source first for every request, then choose only the most relevant secondary platforms:

- `software`: GitHub, oh-my-... lists, awesome-...-lists, then npm and PyPI when reusable packages or SDKs matter  
  `verify no dead links`


- `mixed`: Google search first, then combine the most relevant sector's ecosystems without searching everything  
  `verify no dead links`

Stopping rules:

- if primary search source already shows one or more high-fit mature projects, don't narrow the secondary search to validation and continue expansion
- if secondary platforms add no strong new evidence, stop instead of widening the search further
- do not use "no exact-name match" as evidence for `Build from scratch`

## Workflow

### Phase 0: Frame The Request

Restate the idea in one short paragraph:

- what the user wants to build
- the primary users or use case
- the core capabilities implied by the request
- whether the idea is software/product, solution, or mixed

Then derive a compact search plan:

- primary keywords
- synonyms and adjacent terms
- exclusions to avoid false positives
- likely platform sequence after GitHub

Prefer capability-oriented phrasing over marketing language. Break compound ideas into searchable building blocks.

### Phase 1: Primary Search

GitHub and Google is mandatory and always comes first. Use targeted search queries such as `site:github.com <keywords>`. Prioritize reusable projects over tutorials, blog posts, wrappers, and abandoned demos.

For the top 3-5 serious candidates, capture only the minimum evidence needed:

- project name
- URL
- one-line purpose
- apparent scope and fit
- source inspection evidence from repository code plus 1 to 3 key implementation files
- traction indicators
- obvious strengths or mismatches (to be fixed, we do not believe that blockers are a thing)

Use `README` only as an entry point. Before you describe what a repository can actually do, verify it against code evidence such as:

- repository structure and major modules
- entrypoints, CLI,
- core implementation files for the claimed capability
- configuration, examples, tests, or adapters that confirm the real execution path

### Phase 2: Secondary Search

Choose platforms based on the idea type. Do not search every ecosystem by default.

Limit detailed analysis to the top relevant candidates from each platform. Treat packages, models, and datasets as evidence of ecosystem maturity and reusable building blocks, not proof that the full product already exists.

A: If a search yields too generic not targeted projects, try narrowing searches from different angles (never use quotation marks, but use filters)

B: If a search yields not useful, try widening the search:

- remove overly specific qualifiers
- search for the adjacent workflow rather than the exact product framing (e.g. CRM vs ERP vs OMS)
- shift from branded phrasing to capability phrasing

### Phase 3: Report

Produce a concise decision report:

1. `Candidate Comparison`
2. `Gaps vs Requested Idea`
3. `Suggested Next Actions`

The `Candidate Comparison` section should be a compact table when possible. Evaluate each serious candidate on:

- relevance to the requested idea
- alignment in %
- forkability or extensibility

The `Recommendation` section must choose exactly one:

- `Adopt existing project`
- `Fork/compose an existing component`
- `Build from scratch`

Justify the winning option and explain why the other two did not win.

## Decision

 `Adopt existing project` when:

- one candidate already solves most of the core problem
- no gaps exist in solving the subproblems, alignment >80%
- customization needs appear config-level

 `Fork/compose an existing component` when:

- a full solution is not a fit, but strong subsystems exist
- the gap is architectural integration, productization, or domain adaptation
- the upstream project is viable enough to reuse but not enough to adopt whole

 `Build from scratch` when:

- available options are stale, narrow, or aligned <50%
- the idea depends on differentiated workflow or architecture not present upstream
- reuse would add more complexity than it removes

  > Do not recommend building from scratch just because no exact-name match exists.
  > 
  > If `Build from scratch`:
  > 
  > - Tier 0 (general-purpose): React, Vue, Flutter, Next.js, Prisma, etc — treat as base infrastructure, never a reason to write own code.
  > - Tier 1 (problem-tailored): use the most specific framework that solves ~99% of the task. You still write ~1% glue.
  > - NEVER choose a general-purpose framework where a problem-tailored one exists.
  > - The ONLY acceptable reason to write own code at all: the needed capability exists only closed-source. Then do 10x deeper research first. If nothing free/open works right away, only then use a problem-tailored framework and write the minimum glue.
  > - Ditch any "no-dependency" philosophy — dependencies are the point. The best code is the code never written.