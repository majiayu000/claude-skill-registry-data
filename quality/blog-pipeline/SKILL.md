---
name: blog-pipeline
description: Master orchestrator for the content creation pipeline. Dispatches each stage as a fresh subagent so the parent context never overflows. Runs research through preview for a target keyword and surfaces stage failures cleanly. The /quality-check floors+panel gate decides publish.
allowed-tools: Read, Write, Bash, Agent, Glob
---

# Blog Pipeline (Master Orchestrator)

Take a keyword and produce a publish-ready article. The orchestrator does NOT inline-fork via the
Skill tool — that fails with `Prompt is too long` once the parent context has any history. Each
stage is dispatched as a fresh `general-purpose` Agent with a self-contained brief.

The chain is deliberately lean (Ryan Law's method — short skills, no redundant stages). The
skeptical "is this good enough?" read is NOT a separate stage; it lives inside `/quality-check`'s
3-reviewer panel. There are no `*-adversarial` stages.

## HARD-FAIL GATES — non-negotiable

Between every stage transition, run:

```bash
python scripts/pipeline_gate.py <stage-key> <slug>
```

Stage keys: `research`, `reference`, `outline`, `annotated`, `draft`, `squeeze`, `cited`, `components`,
`quality`, `visuals`, `preview`, `publish`, `deliverable`. The exit code is authoritative —
non-zero means HALT, do NOT advance. Print the stderr summary.

Specific halt conditions:

- **`components`** — runs `scripts/lint_components.py` against `6-drafts-cited/{slug}.md` and HALTS
  on any hard error in the `:::component` fences / inline tokens (unclosed or orphan fence, unknown
  fence name, missing required attribute, illegal nesting, exceeded caps — `nutshell`/`methodology`/
  `key-takeaways` ≤1 and `cta` ≤2 — or unbalanced `{lead}`/`==` tokens). It runs **after `cited` and
  before `quality`/`publish`**, so a malformed or over-decorated article cannot publish as broken
  text. Soft issues (>8 callouts, back-to-back callouts) are WARN-only and do not halt.

- **`quality`** — verdict FAIL is a HALT. PASS requires BOTH the completeness floors AND the
  3-reviewer panel (see `/quality-check`). The autonomous revision loop addresses a FAIL; if the
  budget (2) is spent and it still FAILs, write `9-needs-review/{slug}.md` and STOP — never publish
  a FAIL.
- **`visuals`** — **ON** (wired 2026-06-29; `BLOG_AGENT_VISUALS=on` by default). `/generate-visuals`
  realizes every typed `[VISUAL:...]` into an on-brand asset (deterministic charts/diagrams/tables/
  covers/annotations + screenshots/action-shots/external captures + the gated AI infographic/
  concept-illustration lanes), rewrites the draft to `![alt](images/{slug}/file.png)`, and records a
  manifest. **No silent fallback:** a type that can't be produced is recorded `failed`/`manual` and
  its placeholder is kept in the draft. A *captured* visual still owes the `VISUAL-CRITIQUE-LOOP.md`
  vision gate before publish. Set `BLOG_AGENT_VISUALS=off` for a text-only dry run (legacy no-op:
  placeholders left in place, nothing generated). `/format-for-publish` converts any *surviving*
  placeholder (failed/manual/deferred) to an invisible `<!-- VISUAL-TODO: ... -->` marker.
- **`publish`** — `8-publish/{slug}/{article.md, article.json, README.md}` must all exist. (Any
  leftover `[VISUAL:...]` for a failed/manual/deferred visual is converted by `/format-for-publish`
  to `<!-- VISUAL-TODO: ... -->` rather than failing.)
- **`deliverable`** — for issue-driven runs (PAPERCLIP_TASK_ID set), a deliverable comment with the
  slug + verdict must be posted to the trigger issue.

**Never claim a stage succeeded just because the agent dispatched cleanly.** The gate is the source
of truth.

## Invocation

```
/blog-pipeline <keyword> [--context "free-form direction"]
```

`--context` is Ryan's highest-leverage lever: front-loaded human direction (angle, emphasis,
features to feature) beats heavy editing at the end. Examples:
- `/blog-pipeline character ai no filter --context "Lead with the privacy angle. Feature the memory system early."`
- `/blog-pipeline ai girlfriend apps --context "Audience is first-timers. Use a worked setup example throughout."`

## Why agent dispatch, not slash-command fork

The `Skill` tool forks with the parent's context and hits `Prompt is too long` after any
compaction. The `Agent` tool starts each stage with a clean window. Every stage MUST be an Agent
dispatch, not a Skill invocation.

## Autonomous mode (BLOG_AGENT_AUTONOMOUS=1)

Set by auto-blog-loop; cron runs inherit it from Doppler.

- **Skip-or-regenerate**: never asks. If a stage's output exists, skip it (resume-from-failure);
  `--regenerate` overwrites. No prompt.
- **Quality FAIL**: never bails. Auto-revise loop with budget `BLOG_AGENT_REVISION_BUDGET` (2).
  After the budget is spent, write `content-pipeline/9-needs-review/{slug}.md` and abort the chain
  (do NOT continue to verify-claims/visuals/publish on a FAIL).
- **Format-for-publish**: auto-runs with `--auto-publish` (publishedAt = now).
- **Final report**: "Auto-published to <Strapi URL>" + audit log row.

When unset (interactive/dev), the prompts below are the interactive default; format-for-publish
never auto-runs (editor owns the preview→publish gap).

## Process

1. **Parse** the keyword (before `--context`) and the context string (after it).
2. **Slugify**: `python scripts/slugify.py "<keyword>"`.
3. **Capture context** (REQUIRED for quality): write `content-pipeline/0-context/{slug}.md` with the
   context string verbatim. If no `--context` was given, write a short brief yourself (angle,
   audience, must-feature products) — the draft stage reads this file.
4. **Check status**: `python scripts/pipeline_status.py {slug}`. Autonomous → skip existing stages
   unless `--regenerate`. Interactive → ask skip-or-regenerate.
5. **Run the chain** (see Stage briefs):
   - **Parallel:** Stage 1 (`/research`) + Stage 2 (`/brand-reference`). Wait for both; verify
     outputs on disk; stop on either failure.
   - **Sequential:** Stage 3 (`/outline`) → Stage 4 (`/product-mentions`) → Stage 5 (`/draft`) → Stage 5b (`/squeeze-max-traffic`).
   - **Quality gate:** Stage 6 (`/quality-check`). Read the verdict.
     - **Autonomous:** on FAIL → dispatch Stage 6b targeted-revision (address every CRITICAL+HIGH
       punch-list item along its route: prose → /draft edit; structural → /outline then re-draft the
       affected sections). Re-run quality-check. Repeat up to `BLOG_AGENT_REVISION_BUDGET` (2). Still
       FAIL after budget → write `9-needs-review/{slug}.md`, abort, emit verdict=QUARANTINED.
     - **Interactive:** on FAIL → stop and surface the routed punch list. On PASS → continue.
   - **Sequential:** Stage 7 (`/verify-claims`) → Stage 8 (`/generate-visuals`) → Stage 9 (`/preview`).
6. **Verify each stage's output file exists** before advancing — an agent claiming success without
   the file on disk is a failure.
7. **`/format-for-publish`**: autonomous → auto-run as Stage 10 with `--auto-publish`, then
   `python scripts/auto_publish_check.py {slug}`; on verification failure write `9-needs-review/` and
   emit QUARANTINED. Interactive → never auto-run.

**Multi-author byline + visuals (cross-cutting):**
- **`/draft` selects the author persona** from the content-type (per `examples/authors.md`) and **stamps the byline** as the first line of the draft: `<!-- byline: <Byline Name> | persona: <persona-slug> -->`. **`/format-for-publish` reads that stamp and attaches the Strapi author relation** (persona slug → Author `documentId`); no byline ⇒ author left unset, no crash. Keep the byline comment format byte-exact across `/draft`, `/format-for-publish`, and the visuals stage.
- **Visuals are ON (2026-06-29):** the visuals stage realizes every typed `[VISUAL:...]` into an on-brand asset and rewrites the draft to `![alt](images/{slug}/file.png)`. It does **not** hard-gate the run, but each captured visual owes the `VISUAL-CRITIQUE-LOOP.md` vision gate before publish; failed/manual entries keep their placeholder, which `/format-for-publish` converts to an invisible `<!-- VISUAL-TODO: ... -->` marker. Set `BLOG_AGENT_VISUALS=off` for a text-only dry run (legacy no-op). Stage **order is unchanged**.

## Stage briefs

Each Agent dispatch is self-contained (the spawned agent has no memory of this conversation).
Include: project root `{ROOT}`, slug, keyword, the SKILL path, input/output paths, the editorial
constraints for that stage, and "return a 250–400 word summary, not a content dump."

### Stage 1 — Research

```
You are running stage 1 at {ROOT}. Keyword: "{KEYWORD}". Slug: {SLUG}. Brand: see brand-config.md.

Your job: produce content-pipeline/1-research/{SLUG}.md per .claude/skills/research/SKILL.md. Read the SKILL first.

- Read .claude/skills/research/references/ahrefs-mcp-cheatsheet.md FIRST — use the real Ahrefs MCP tools (mcp__ahrefs__*); params are comma-separated strings not arrays, select + country required, call doc {tool:"..."} before any unfamiliar tool. Semrush/DataForSEO are retired — never call them. Ahrefs is mandatory: if the MCP is unavailable use the Ahrefs REST API (same source, lowercase country=us) and surface it loudly; if NO Ahrefs at all, HARD-FAIL and STOP. See the cheat sheet's outage policy.
- Pull keyword data (keywords-explorer-overview for volume/KD/CPC/parent-topic/intents; matching-terms + related-terms for the variation pool and FAQ themes; serp-overview for ranking URLs and People-Also-Ask).
- Extract the top 5-8 ranking pages via Firecrawl (FIRECRAWL_API_KEY; WebFetch fallback); build the SERP benchmark: per-page word counts, H2 lists, formats, item counts, table/visual counts.
- Deep research via OpenRouter: doppler run -- python .claude/skills/research/scripts/openrouter_research.py --keyword "{KEYWORD}" --slug "{SLUG}".
- Emit content-pipeline/1-research/{SLUG}-data.json with chartable numbers (schema in the research SKILL).
- The dossier MUST end with "## BEAT SPEC" (target word count, format + item count, table requirement, must-cover topics, information gain, secondary keywords) — the outline and quality gate are bound by it. Read 0-context/{SLUG}.md if present and honor its angle.

Return: word count, recommended angle (one sentence), the BEAT SPEC headline numbers, 3 most surprising findings, any failures. Under 400 words.
```

### Stage 2 — Brand reference

```
You are running stage 2 at {ROOT}. Slug: {SLUG}. Keyword: "{KEYWORD}". Brand: see brand-config.md.

Your job: produce content-pipeline/2-reference/{SLUG}.md per .claude/skills/brand-reference/SKILL.md. Read the SKILL first.

- Refresh the Strapi inventory: doppler run -- python .claude/skills/brand-reference/scripts/fetch_strapi_inventory.py
- Score articles, take top 3-5; catalog reusable modules + product-led examples + internal-linking opportunities by H2. 300-700 words.

Return: inventory size, relevant count, top 3 internal-linking opportunities, any failures. Under 250 words.
```

### Stage 3 — Outline

```
You are running stage 3 at {ROOT}. Slug: {SLUG}. Brand: see brand-config.md.

Your job: produce content-pipeline/3-outlines/{SLUG}.md per .claude/skills/outline/SKILL.md. Read the SKILL first.

Read in order: outline/SKILL.md; outline/references/bluf-mece-rules.md; templates/outline-template.md; templates/visual-strategy.md (THE governing spec for visuals); templates/visual-types.md; content-pipeline/1-research/{SLUG}.md (+ {SLUG}-deep.md); content-pipeline/2-reference/{SLUG}.md; 0-context/{SLUG}.md; brand-config.md; examples/README.md + 1 structure/niche example matching the type.

Editorial requirements:
- The outline is bound by the dossier's BEAT SPEC — restate it at the top; section count sized by the SERP (listicles get one section per item, item count ≥ the spec); per-section word targets sum to the spec total ±10%.
- Coverage map at the bottom: every must-cover topic → which H2 covers it; one section marked [GAIN].
- Comparison table specced as a markdown skeleton when the beat spec requires one.
- Each H2: BLUF + 2-4 key points + evidence source + transition + typed Visuals + word target; MECE.
- Visuals: need-driven per templates/visual-strategy.md — plan a [VISUAL:] where a section must SHOW value text + native ::: components can't (proof/data/example/concept). value-first ~80/20 = screenshot the SPECIFIC tool/product/site/real artifact the point is about (competitor-ui screenshots + charts + diagrams are the BULK; serp/reddit are OCCASIONAL — only when a search result or a real user's words IS the point, never the default/filler); our-product screenshot/action-shot only when on-topic; charts/diagrams point at a real research.<key> or authored config=. Plan native ::: for stats/quotes/tables/callouts (never a [VISUAL:] for those). No AI-generated imagery (type=image retired). No density QUOTA, but CALIBRATE to Ahrefs density (~1 visual/150–200 words, show nearly everything you reference; a long post with 3–4 visuals is under-visualized).
- Title under 60 chars, includes primary keyword.

Return: title, one-sentence thesis, H2 list (one line each), beat-spec compliance line (sections / items / total words / table Y-N), visual count by type, structural concerns. Under 350 words.
```

### Stage 4 — Product mentions

```
You are running stage 4 at {ROOT}. Slug: {SLUG}. Brand: see brand-config.md.

Your job: produce content-pipeline/4-outlines-annotated/{SLUG}.md per .claude/skills/product-mentions/SKILL.md. Read the SKILL first — including the Constraint reconciliation pass.

BEFORE annotating, scan the outline for contradictions on coming-soon products; delete contradicting bullets and log under "## Pre-flight reconciliation". 

- Aim for 3-5 product-mention annotations across all H2s — don't shoehorn. Each specifies HOW (walkthrough / inline / tip box). Hold the brand to the SAME critical lens as competitors — no promotional register the competitor sections don't get. No coming-soon products in walkthrough/evergreen sections.

Return: sections annotated, the H2-by-H2 product plan as a table, reconciliation deletions, rejected mentions with reason. Under 250 words.
```

### Stage 5 — Draft

```
You are running stage 5 at {ROOT}. Slug: {SLUG}. Brand: see brand-config.md.

Your job: produce content-pipeline/5-drafts/{SLUG}.md per .claude/skills/draft/SKILL.md. Read the SKILL first — the three commitments (depth / specificity / voice-from-examples).

Read before drafting: draft/SKILL.md; draft/references/voice-guide.md; draft/references/prose-patterns.md; brand-config.md (forbidden phrases); examples/authors.md (persona map + content-type→persona rule + byline contract); content-pipeline/4-outlines-annotated/{SLUG}.md; 2-reference/{SLUG}.md; 1-research/{SLUG}.md (+ {SLUG}-deep.md); 0-context/{SLUG}.md; examples/README.md then the SELECTED persona's persona.md + 1–2 type-matched anchors from examples/voice/<persona>/ + 1 from examples/structure or niche.

Hard requirements (these gate the save):
- PERSONA + BYLINE: select the author persona from the content-type via examples/authors.md (fallback theo-hart); draft in that persona's craft + OUR register; **stamp the byline as the very first line of the draft file** before the H1 — exactly `<!-- byline: <Byline Name> | persona: <persona-slug> -->`. /format-for-publish reads this line to attach the Strapi author relation, so keep it byte-exact.
- Hit each section's word target ±20%; article total within ±15% of the BEAT SPEC; listicle item count per the outline — never compress; comparison table as real GFM markdown when specced.
- VOICE: lead with reader-felt reality (the real decision the reader faces), not a feature spec — match the examples/voice/ register. No crutch word/phrase used 3+ times; vary paragraph rhythm (mix one-line punches with developed passages).
- Every section opens with a BLUF. No forbidden phrases. Cut "Furthermore/Moreover/It is important to note/very/really/quite/simply" when not load-bearing.
- Show, don't sell — product mentions follow the annotated slot plan exactly. Internal links from 2-reference woven inline. Stat citations as [link] markers. Typed [VISUAL:...] placeholders per templates/visual-strategy.md: resolvable data (chart/diagram point at a real research.<key> or authored config= — NO invented keys), no native-component duplication (no PNG of a stat/quote/table/callout already in a ::: directive), value-first ~80/20 = screenshot the specific tool/product/artifact the point discusses + charts + diagrams (that's the bulk — NOT serp/reddit, which are occasional only when a search result / a real user's words IS the point); our-product only when on-topic; calibrate to Ahrefs density (~1 visual/150–200 words — sparse reads thin). Mark the information-gain section with [GAIN].

Self-check before save: per-section word counts vs targets (any <80% → add concrete material from the dossier, never pad); scan for crutch repetition + uniform rhythm and fix.

Return: persona chosen + byline-stamp confirmed as first line, word count vs target, section count vs outline, table Y/N, [link] count, [VISUAL] count, [GAIN] present, confirmation no forbidden phrases or out-of-slot mentions. Under 400 words.
```

### Stage 5b — Squeeze max traffic (Lesson 5 part 3)

```
You are running stage 5b at {ROOT}. Slug: {SLUG}. Brand: see brand-config.md.

Your job: expand content-pipeline/5-drafts/{SLUG}.md to capture the FULL keyword family per .claude/skills/squeeze-max-traffic/SKILL.md. Read the SKILL first. This runs AFTER /draft and BEFORE /quality-check, in place on 5-drafts/{SLUG}.md, so the gate judges the squeezed draft.

If content-pipeline/5-drafts/{SLUG}-squeeze.md already exists, this slug was already squeezed this run — NO-OP and return.

Pull (a) the page's keyword family (parent-topic related/matching terms + the winning page's organic keywords) via Ahrefs, and (b) the Content Gap (keywords competitors rank for but we don't) by reusing /content-gap-analysis (keyword-ideas.csv + cache/competitors.json). Triage to same-intent, on-topic, SERVABLE terms; weave the worthwhile ones in as NATURAL added paragraphs/sub-sections — NOT keyword stuffing (STRATEGY.md anti-pattern #10). Preserve the persona voice, the byline first line, the [GAIN] information-gain element, and the authority element. Re-save in place to 5-drafts/{SLUG}.md; write the audit trail to 5-drafts/{SLUG}-squeeze.md. Non-fatal: if nothing worthwhile to add, NO-OP and say so.

Return: keywords folded in (count + examples), sections added/expanded, confirmation byline first line + [GAIN] + voice intact — or NO-OP with reason. Under 300 words.
```

### Stage 6 — Quality check (the publish gate)

```
You are running stage 6 at {ROOT}. Slug: {SLUG}. This is the publish gate — it has NO score.

Your job: produce content-pipeline/quality-checks/{SLUG}.md per .claude/skills/quality-check/SKILL.md. Read the SKILL first. PASS requires BOTH halves:

1. FLOORS — run: python .claude/skills/quality-check/scripts/quality_check.py {SLUG}  (exit 0 = FLOORS_OK). Any failed floor → FAIL; route the fix (missing consensus topic / thin depth / missing table → /outline or /research; prose/voice → /draft). Do not run the panel on a draft that fails a floor.
2. PANEL — spawn THREE independent Task sub-agents, each a skeptical expert who has read every page-1 result for "{KEYWORD}", each given 1-research/{SLUG}.md (BEAT SPEC + top-page summaries), the draft, and 1-2 examples/voice/ articles. Lenses: (A) competitiveness, (B) voice & readability vs the examples, (C) reader intent & information gain. Each returns "VERDICT: KEEP_OURS|KEEP_COMPETITOR|TOSS_UP" (default KEEP_COMPETITOR/TOSS_UP if unsure) + 3-sentence why + 5 weakest things vs what's ranking + 1 that works. Save to quality-checks/{SLUG}-panel.md. Distrust all-praise verdicts under 200 words — re-run that lens sharper. Panel passes iff ≥2 KEEP_OURS AND none KEEP_COMPETITOR.

Write content-pipeline/quality-checks/{SLUG}.md with the verdict line FIRST: "## Verdict: **PASS**" iff FLOORS_OK AND panel passes, else "## Verdict: **FAIL**". Then the floor summary, the 3 panel verdicts, and a punch list — each fix tagged with a route (/draft for prose, /outline or /research for structure).

Return: verdict, failed floors (if any), the 3 panel verdicts, top 3 punch-list items, proceed/iterate/halt.
```

### Stage 6b — Targeted revision (autonomous, on FAIL)

```
You are running a surgical revision pass at {ROOT}. Slug: {SLUG}.

The draft FAILed the gate. Read content-pipeline/quality-checks/{SLUG}.md (the routed punch list), 5-drafts/{SLUG}.md, 4-outlines-annotated/{SLUG}.md, brand-config.md, draft/references/voice-guide.md.

Apply each CRITICAL and HIGH item along its route, using Edit calls (not Write): prose/voice items → edit the draft; structural items (missing topic, item shortfall, missing table, thin depth) → say so explicitly, because those go back through /outline then a re-draft of the affected sections, NOT a surgical edit. Preserve all [link] markers, typed [VISUAL] placeholders, [GAIN] marker, internal links. Save back to 5-drafts/{SLUG}.md.

Return: each fix applied (Y/N), word-count delta vs beat spec, whether any item requires a structural re-route. Under 300 words.
```

After 6b, re-dispatch Stage 6 once. PASS → continue; FAIL with budget remaining → loop; FAIL with budget spent → quarantine.

### Stage 7 — Verify claims

```
You are running stage 7 at {ROOT}. Slug: {SLUG}.

Your job: produce content-pipeline/6-drafts-cited/{SLUG}.md per .claude/skills/verify-claims/SKILL.md. Read the SKILL first — the two-tier citation rule (must-cite vs voice-flagged).

Resolve every [link] placeholder with a real source via WebSearch + WebFetch. Wire internal links from 2-reference. Apply the two-tier density check (must-cite ≥60% linked; voice-flagged listed for editor review, never auto-linked). No internal tool/vendor names in reader-facing prose.

Return: [link] placeholders replaced, [CITATION NEEDED] flags remaining, internal links wired, must-cite density %, voice-flagged statements listed. Under 300 words.
```

### Stage 8 — Generate visuals (ON by default)

```
You are running stage 8 at {ROOT}. Slug: {SLUG}.

VISUALS ARE ON (BLOG_AGENT_VISUALS=on by default). Run the dispatcher; it realizes every typed [VISUAL:...] into an on-brand asset, optimizes the PNG, records content-pipeline/images/{SLUG}/manifest.json, and rewrites the cited draft so each captured placeholder becomes ![alt](images/{SLUG}/file.png):
  doppler run -- python .claude/skills/generate-visuals/scripts/generate_visuals.py {SLUG}
(DISPLAY=:99 must be set for the headless-browser engines — the container has it.)

Engines (all run in the container; full interface in .claude/skills/generate-visuals/SKILL.md + the per-type recipe docs):
  chart -> render_chart_web.py | diagram -> render_diagram_web.py | table/comparison -> DROPPED (author a NATIVE ::: component, never a PNG) |
  cover -> cover_hero_engine.js (Ahrefs flat-vector) + logo_stamp (render_cover.py line-art = fallback only) | annotation -> annotate_screenshot.py --strict | screenshot -> capture_screenshot.py |
  action-shot -> action_shot.py | external -> capture_screenshot.py | demo/gif -> animate_demo.py |
  infographic -> infographic_engine.js + composite_logo.py | concept-illustration -> concept_illustration_engine.js.
  (type=image is retired/dropped; type=card uses native blog components and is skipped.)

NO SILENT FALLBACK. A type that can't be produced is recorded failed/manual with a reason; its placeholder stays in the draft (and /format-for-publish later converts a surviving placeholder to an invisible <!-- VISUAL-TODO: ... --> marker — failed/manual visuals therefore do NOT block text publish). Common fixes: chart/diagram status=failed reason=*data_unresolved/*requires_structured_data => the referenced key is missing from content-pipeline/1-research/{SLUG}-data.json — read the dossier, extract the numbers/nodes, append under that key, re-run. action-shot reason=session_required => an authed shot needs the showcase session (setup_auth.py); leave it manual. infographic/concept reason=*generate_failed => check REPLICATE_API_KEY / the Nano-Banana error.

AUTO-CHAIN — finish bot-walled EXTERNAL screenshots (one continuous capture flow, provider-agnostic). The dispatcher captures type=external HEADLESS, which bot walls (Google SERP, Reddit, competitor UIs) block -> those land failed/manual. Immediately retry them with the model-neutral engine (real headed browser on :99 — same outcome on ANY EO model, Claude or Codex):
  DISPLAY=:99 python .claude/skills/capture-visuals/scripts/capture_visuals_resolve.py {SLUG}
Then VISION-CHECK each external it captured per .claude/skills/capture-visuals/SKILL.md — REJECT any bot-block / login / consent / 404 page (never present one as a real cited source; scrutinize a viewport fallback flagged needs_review especially). Only if you ARE a Claude model and a real, reachable external still failed, use that skill's Claude-in-Chrome top-up. Do not invent a substitute for a fabricated/dead source — leave it failed (a fabricated source is a content bug, not a capture bug).

Every CAPTURED visual must pass VISUAL-CRITIQUE-LOOP.md (render -> deterministic check -> vision critique -> fix -> re-render, max 3) before publish — be a strict critic, especially for the gated AI lanes. Set BLOG_AGENT_VISUALS=off only for a text-only dry run (legacy no-op).

Return: captured / manual / failed counts + the manifest path + any failed entries with their reason. Under 250 words.
```

### Stage 9 — Preview

```
You are running stage 9 at {ROOT}. Slug: {SLUG}.

Your job: render content-pipeline/7-preview/{SLUG}.html per .claude/skills/preview/SKILL.md. Run:
  python .claude/skills/preview/scripts/render_preview.py {SLUG}

Return: preview path; list any render warnings.
```

### Stage 10 — Format for publish (autonomous only)

```
You are running stage 10 at {ROOT}. Slug: {SLUG}. Autonomous mode.

Your job: per .claude/skills/format-for-publish/SKILL.md (read it first). Run:
  doppler run -- python .claude/skills/format-for-publish/scripts/format_for_strapi.py {SLUG} --auto-publish

The script re-reads quality-checks/{SLUG}.md and refuses to publish on verdict FAIL (belt-and-suspenders), parses the byline stamp from the draft and attaches the Strapi author relation (persona slug → documentId via PERSONA_AUTHORS; unset if no byline — no crash), converts any leftover [VISUAL:...]/[SCREENSHOT:...] placeholders (only failed/manual/deferred visuals survive — visuals are ON, governed by templates/visual-strategy.md) to invisible <!-- VISUAL-TODO: ... --> markers — NOT a failure, builds the Strapi payload, copies images, POSTs with publishedAt = now, prints the public URL. Then run:
  python scripts/auto_publish_check.py {SLUG}
On non-zero, the script writes 9-needs-review/{SLUG}.md — surface that as QUARANTINED, not published.

Return: Strapi article ID, public URL, auto_publish_check exit code, any errors.
```

## Reporting format

Autonomous:

```
✓ Pipeline complete for "{keyword}" (slug: {slug}) — AUTONOMOUS
  ✓ research / brand-reference / outline / product-mentions / draft
  ✓ quality-check   → verdict: PASS (floors + 3-reviewer panel; after N revision passes)
  ✓ verify-claims / generate-visuals / preview
  ✓ format-for-publish → auto-published to <Strapi public URL>
  ✓ auto_publish_check → verified live H1
  Audit row appended: content-pipeline/audit/auto-blog-log.csv
```

Quarantined:

```
✗ Pipeline halted for "{keyword}" (slug: {slug}) — QUARANTINED
  Last good stage: <name>   Failure reason: <one-line>
  Quarantine path: content-pipeline/9-needs-review/{slug}.md
  Audit row appended (action=quarantined).
```

## Quality-check gating

Binary, no score:
- **PASS** (FLOORS_OK AND ≥2/3 panel KEEP_OURS AND none KEEP_COMPETITOR): advance.
- **FAIL** (any failed floor OR panel not satisfied): autonomous → revise along the routed punch
  list within budget 2, then quarantine; interactive → stop and surface the routed punch list.

If a draft sounds generic or AI-flavored, the panel fails it — there is no score to hide behind.

## When a stage's agent fails

Don't skip ahead — surface the failure with stage name + the agent's error. Save partial state so
the run resumes from the failing stage. Do NOT retry automatically.
