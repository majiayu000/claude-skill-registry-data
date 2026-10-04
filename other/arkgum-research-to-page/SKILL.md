---
name: arkgum-research-to-page
description: >-
  Autonomously orchestrate a source-grounded topic-to-page workflow through
  Google NotebookLM: create or reuse a notebook, run Deep Research, import and
  verify sources, produce a cited research report, rank audience/content
  opportunities, create a page brief, and return a final prompt for Google AI
  Studio or another page builder. Use when the user asks to research a topic
  and turn it into a landing page, website, lead-generation page, product page,
  content-gap strategy, or builder-ready specification, or explicitly invokes
  arkgum-research-to-page. Codex performs the NotebookLM work itself; do not use
  this skill for simple notebook questions or deployment-only tasks.
---

# Arkgum Research to Page

Turn one topic into a grounded page-building package. Own the NotebookLM work end to end; do not make the user shuttle prompts, sources, or answers between services.

## Operating contract

- Use the configured NotebookLM MCP as the primary execution layer.
- Treat invocation as authorization to create one task-specific notebook, add task-relevant sources, run research, query the notebook, and write local run artifacts.
- Do not delete, rename, share, publish, or change access to notebooks without an explicit request.
- Never ask the user to open NotebookLM, paste prompts, import sources, or copy results as part of the normal flow.
- Ask the user to intervene only when Google authentication is missing or an external side effect needs separate authorization.
- Keep NotebookLM outputs and local artifacts in Russian unless the user requests another language. Preserve source titles, URLs, and quoted text in their original language.
- Ground factual claims in imported sources. Mark inference, uncertainty, missing evidence, and conflicting sources explicitly.
- Do not invent keyword volume, competition, traffic, rankings, testimonials, statistics, pricing, or product capabilities.
- Never expose cookies, tokens, session data, or other credentials in output or saved artifacts.

## Load resources

Resolve `<skill-root>` as the directory containing this `SKILL.md`, then read:

- `<skill-root>/references/notebooklm-routing.md` before any NotebookLM action;
- `<skill-root>/references/prompts.md` before querying NotebookLM;
- `<skill-root>/references/output-contract.md` before writing artifacts or running QA.

## Inputs and defaults

Required input: a research topic.

Use conversation context to infer optional inputs:

- audience and market/region;
- page goal and conversion action;
- offer, product, or resource being presented;
- user-provided sources or an existing notebook ID/URL;
- target builder and output language.

Defaults:

- research mode: `deep` on the web;
- output language: Russian;
- builder: Google AI Studio Build;
- page type: evidence-led landing page;
- missing offer or CTA: keep an explicit placeholder instead of inventing one;
- missing audience: infer a narrow likely audience and record that it is an assumption.

Ask one concise question only when different answers would materially change the research corpus or page proposition. Otherwise proceed with recorded assumptions.

## Required workflow

### 1. Initialize the run

Create a durable run workspace outside the skill directory:

```bash
python3 <skill-root>/scripts/init_run.py \
  --topic "<topic>" \
  --audience "<audience-or-empty>" \
  --page-goal "<goal-or-empty>" \
  --offer "<offer-or-empty>" \
  --cta "<cta-or-empty>" \
  --builder "<builder>"
```

Use the printed absolute path as `<run-dir>`. Keep every artifact listed in `references/output-contract.md` there. Do not write run data into the skill folder.

### 2. Create or reuse a NotebookLM notebook

- Reuse a notebook only when the user supplies its exact ID/URL or explicitly requests reuse.
- Otherwise create `R2P — <topic> — <YYYY-MM-DD>`.
- Record the full notebook ID and URL in `<run-dir>/manifest.json` and `10-research-plan.md`.
- Add user-provided URLs and text sources before Deep Research.
- Poll notebook details until added sources are ready. Report a blocker rather than silently dropping a failed source.

### 3. Run Deep Research

Build a focused research question from the topic, audience, region, current date, and page goal. Request current primary sources, independent validation, audience questions, pain points, alternatives, objections, examples, and contradictory evidence.

Use this sequence:

1. `research_start` with `source=web`, `mode=deep`, and the full notebook ID.
2. Poll `research_status` for at most 45 seconds per call; communicate progress between long polls.
3. When complete, inspect the full report and source list with `compact=false`.
4. Exclude obvious duplicates, thin affiliate pages, irrelevant results, and unsupported SEO filler.
5. Import the selected source indices with `research_import`.
6. Read notebook details and wait until the imported sources are usable.

Run one additional focused research pass only when a material evidence gap remains. Do not pad the notebook to a numeric target.

### 4. Verify the source corpus

Write `20-source-manifest.md` with source title, URL or source ID, type, date when available, role in the research, and any limitation.

Require:

- primary or official sources for core factual claims when available;
- more than one independent source for consequential claims;
- recent sources for time-sensitive facts;
- explicit notation when only marketing, raw, or weak evidence exists;
- conflicting evidence preserved rather than averaged away.

If the corpus cannot support the requested page, stop before generation and explain the missing evidence.

### 5. Generate the grounded research report

Query the imported sources with the `Grounded research report` template from `references/prompts.md`. Use explicit source IDs when the tool supports them.

Save the complete response, including citations, to `30-grounded-report.md`. This report is the factual authority for downstream artifacts. Do not replace it with a model-memory summary.

### 6. Generate and rank opportunities

Query the notebook with the `Opportunity matrix` template. Save the result to `40-opportunity-matrix.md`.

Rank opportunities by:

1. strength of source evidence;
2. audience pain and decision relevance;
3. differentiation from existing coverage;
4. fit with the stated page goal and offer;
5. feasibility without invented claims.

Treat search demand, keyword difficulty, and ranking potential as unknown unless supplied by a real SEO dataset. Select the highest-ranked non-disqualified opportunity and record the selection plus rationale in the manifest. When several options are effectively tied and imply different products, ask the user to choose.

### 7. Create the page brief and builder prompt

Use separate NotebookLM queries:

1. `Evidence-led page brief` → save to `50-page-brief.md`.
2. `Final builder prompt` → save to `60-builder-prompt.md`.

The builder prompt must specify:

- audience, job-to-be-done, page goal, offer, and CTA;
- information architecture and section order;
- grounded copy and evidence placement;
- visual direction and component behavior;
- responsive and mobile behavior;
- technical SEO without ranking guarantees;
- accessibility, performance, analytics events, and acceptance criteria;
- placeholders for business inputs that were not provided;
- a ban on fabricated claims, metrics, testimonials, and citations.

### 8. Perform QA

Audit the brief and builder prompt against the source manifest and grounded report. Write `70-qa.md` with PASS/FAIL for every gate in `references/output-contract.md` and fix failures before handoff.

Run the static validator:

```bash
python3 <skill-root>/scripts/validate_run.py <run-dir>
```

This is a file/content validation, not a product test suite. Do not execute generated page tests unless the user explicitly requests them.

### 9. Optional page build

By default, deliver the builder-ready package and final prompt.

If the user also asks to build the page, hand `60-builder-prompt.md` and the grounded artifacts to the relevant builder capability. Keep NotebookLM as the factual source of truth. Do not publish, deploy, purchase a domain, connect production data, or make the page public without explicit authorization.

## NotebookLM failure handling

- Missing auth: state that Google authentication is required and use the configured authentication flow. Do not ask the user to do the research manually.
- MCP unavailable: apply the `notebooklm-api` skill and use its full-path CLI fallback.
- Deep Research failure: retry once with a narrower query; then report the blocker.
- Source import failure: preserve the failed source in the manifest with its error; continue only if it is non-critical.
- No grounded report: stop. Do not create an opportunity matrix or page prompt from memory.
- Rate limit or long-running research: preserve the run directory and notebook ID so the same run can resume.

## Handoff

Return:

- the chosen opportunity and why it won;
- the NotebookLM notebook URL;
- clickable paths to `30-grounded-report.md`, `40-opportunity-matrix.md`, `50-page-brief.md`, `60-builder-prompt.md`, and `70-qa.md`;
- any unresolved evidence gaps or placeholders;
- whether an actual page was built or only the builder package was produced.

End substantial runs by asking which learned preference or recurring rule should be incorporated into the skill permanently.
