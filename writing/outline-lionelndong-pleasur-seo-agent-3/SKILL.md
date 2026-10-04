---
name: outline
description: Create a structured H2/H3 outline with BLUF openers and MECE coverage, bound by the research dossier's beat spec. Triggered after /research and /brand-reference.
allowed-tools: Read, Write
---

# Outline Skill

Turn the research dossier into the article's bones. The output is a detailed outline a writer (human or AI) can expand into prose without further research. **The outline is bound by the dossier's BEAT SPEC** — section count, item count, word targets, and required formats come from the SERP, not from habit.

## Input

For slug `{slug}`, reads:
- `content-pipeline/1-research/{slug}.md` (required — especially **BEAT SPEC**, "Recommended angle", consensus/gap topics)
- `content-pipeline/2-reference/{slug}.md` (recommended — brand context)
- `content-pipeline/0-context/{slug}.md` (if exists — user-provided angle; overrides everything else on conflict)
- `brand-config.md` (audience, voice)
- `references/bluf-mece-rules.md` (structural rules — must enforce)
- `../../../templates/outline-template.md` (the file structure)
- `../../../templates/visual-strategy.md` (**THE GOVERNING SPEC for every visual decision — read it first**: need-driven placement, value-first ~80/20, the native-`:::`-vs-`[VISUAL:]` anti-duplication rule, resolvable data)
- `../../../templates/visual-types.md` (the controlled `[VISUAL:]` vocabulary + value-first selection guide; follows visual-strategy.md)
- `examples/component-cheatsheet.md` (**PRIMARY component reference — the writer's menu**: when each component earns its place + the caps; plan from this first per step 6a)
- `examples/ahrefs-components.md` (the deep `:::component` catalog/spec — exact fence names + attributes; consult when the cheatsheet isn't enough)
- `examples/` — read `examples/README.md`, then the **2 examples closest to this content type** (structure + niche). The examples are the structure/voice spec — Ryan's principle: anchor in real high-performing articles, never work from a distilled rule list alone.

## Process

1. **Read all inputs.** Restate the BEAT SPEC numbers at the top of your outline file so the draft stage sees them without re-opening the dossier.
2. **Set a PROVISIONAL working title.** Direct, includes the primary keyword early, under 60 chars when possible — enough to anchor the outline. The FINAL title is chosen at `/draft` step 2a (≥5 headlines brainstormed, shaped in the persona's craft, non-salesy/honest, strongest picked) — so don't over-invest here; this is a placeholder the draft stage replaces.
3. **Write the thesis.** One sentence. The article's central argument.
4. **Decide content type.** Follow the beat spec's format. Deviating from the modal SERP format requires an explicit justification line in the outline ("SERP is listicles; we're doing X because …") — absent that, format parity is mandatory.
5. **Draft the H2 list — sized by the beat spec, not a fixed cap.**
   - Explainer/guide SERPs: typically 5–8 H2s.
   - Listicle/comparison SERPs: **one H2 (or H3 under a roundup H2) per item, item count ≥ beat spec's item target.** A 9-app SERP gets ≥9 apps — never compress to 4 "picks" unless the user's context file explicitly asks for a short list.
   - Every consensus topic from the beat spec maps to a section or a substantial subsection. List which H2 covers which consensus topic in a coverage map at the bottom of the outline.
   - At least one section delivers the beat spec's **information gain** — mark it `[GAIN]`.
   - Read the H2 list aloud as a sequence: does it argue the thesis? Is it MECE?
6. **For each H2, write:**
   - BLUF (one sentence; the section's opening line or close to it)
   - Key points (2–4 bullets)
   - Evidence (stat / quote / example / walkthrough — cite which dossier section it comes from)
   - **Word target** — per-section targets must sum to the beat spec's total ±10%. Weight by SERP attention: comparison/criteria sections get more, boilerplate sections get less.
   - Transition to next section
   - **Visuals — NEED-DRIVEN, not a quota (governed by `templates/visual-strategy.md`).** Plan a `[VISUAL:]` for a section **only when that section needs to SHOW the reader value that text + native `:::` components cannot** — real proof, a data trend, a real example, or a concept/flow. There is **NO "image every N words"** quota — but **calibrate to Ahrefs' real density (~1 visual per 150–200 words, ~15–25 in a long guide): they show nearly everything they reference.** So plan a visual wherever a section names a **showable thing** — a tool, a screen, a number, a process, a real artifact. Many sections earn one; data-dense ones earn two. **If you can't name the concrete value a visual adds *right here*, don't plan it** — but a long outline with only 3–4 planned visuals is UNDER-planned, not tasteful: go find the missed value-moments. Space them sensibly — never stack two back-to-back. (We carry more visuals than older posts only where those posts *missed* a real value-moment — fix the misses, never manufacture filler.)
     - **Value-first ~80/20 — mostly the reader's world, the RIGHT type per point.** Per the Ahrefs evidence in `visual-strategy.md`, ~80% of visuals show a **third party / the reader's world** — but that means **screenshots of the specific tools/products/sites/real artifacts the post discusses** (competitor/tool screenshots ~30%, charts of real data ~17%, real artifacts ~14%, diagrams ~5%), **NOT Google-SERP-and-Reddit** (SERP is only ~4% and Reddit a small slice — **occasional**, only when a search result or a real user's own words IS the point; never the default, never filler). ~20% our own product. **Reserve our-product shots for moments the post is genuinely on-topic about Pleasur.ai** (e.g. a capability we uniquely solve). The same method applies to **any** tool a post covers — if the post is about another product, screenshot and annotate *that* product. A reader who sees a competitor's UI, a real SERP, or a real thread gets value whether or not they ever buy.
     - **Plan NATIVE `:::` for stats / quotes / tables / callouts — NEVER a `[VISUAL:]` for those** (step 6a + the anti-duplication table in `visual-strategy.md` §4). A `:::stat`, `:::pullquote`, `:::table`/`:::decision-table`/`:::feature-matrix`/`:::proscons`, `:::tip`/`:::note`/`:::warning`/`:::key-takeaways` is **always** better than a PNG of the same thing — selectable, accessible, SEO-readable, responsive. A `[VISUAL:]` is only for what text + natives *can't* render: real screenshots, branded charts of real data, concept diagrams/flows, covers, demos/GIFs, embeds.
     - **Each planned visual names three things: its PURPOSE, its value-first SOURCE (prefer third-party/world), and its TYPE.** For any **screenshot-type** visual (`external`, `screenshot`, `action-shot`), also name **WHAT to annotate** — the one thing the screenshot proves — so the placeholder isn't vague (a bare screenshot leaves the reader unsure where to look; strategy §7 = annotate screenshots by default). Self-evident visuals (charts/diagrams) carry no `annotate`. Format:
       ```
       **Visuals:**
         Visual 1: {type: external, sub: competitor-ui, source: Character.AI chat showing the memory failure, purpose: prove the forgetting problem on a real rival, annotate: the repeated/forgotten detail in the reply, self_or_third: third-party}
         Visual 2: {type: chart, data: research.<KEY-THAT-EXISTS>, purpose: show the price-per-action gap, self_or_third: third-party-data}
         Visual 3: {type: screenshot, target: chat, what: the memory panel recalling a fact unprompted, annotate: the recalled fact / "remembers you" badge, purpose: show the capability WE uniquely solve, self_or_third: self (on-topic)}
       ```
       Types: `external` (third-party screenshot — **the workhorse**) / `screenshot` (our product, on-topic only) / `action-shot` (our logged-in product, SFW) / `chart` / `diagram` / `cover` / `video` / `gif` / `none`. **No `image`** — AI image generation is retired. For our product UI: `screenshot` if a single URL shows the state, `action-shot` if it takes clicks (routed to `/capture-visuals`). For a quoted Reddit/tweet/news/competitor: `external` with a `selector`.
6a. **PLAN the Ahrefs components each section carries — with RESTRAINT — from the FULL authored set.** Consult **`examples/component-cheatsheet.md` first — the writer's menu** (when each component earns its place + the caps), dropping to `examples/ahrefs-components.md` (its `## Render contract` has the exact fence names + attributes) when you need the deep spec. For each section, note which `:::component` fence(s) the writer should emit at draft time (the writer EMITS in `/draft`; you PLAN here). Mark them on the section as a `**Components:**` line, e.g. `**Components:** :::stat (the 68% retention figure), :::sidenote (caveat on the sample)`. **Plan for whichever component the section's content + the article's type genuinely calls for — not just the house-standard few.** Restraint is the paramount rule: **1–2 of each per article, only where it genuinely improves scannability — never decorate.** Most sections carry zero. Use the fence names EXACTLY (byte-for-byte, lowercase, hyphenated) as in the cheatsheet. **The pre-publish `components` checker enforces the caps (`nutshell`/`methodology`/`key-takeaways` ≤1, `cta` ≤2) and required attributes — plan within the menu's limits so the draft doesn't trip the gate.**

   **House-standard triggers → component:**
   - the top/one-paragraph answer (plan ONE, directly under the H1) → `:::nutshell`
   - the conclusion's front-loaded takeaways → `:::key-takeaways`
   - one load-bearing number → `:::stat` (2–4 → `:::stat-group`)
   - a data study's data disclosure → `:::methodology` (place right after the intro)
   - an aside / caveat / source-note → `:::sidenote`
   - a named expert's opinion → `:::expert`
   - a deeper subtopic with its own article (mid-article) → `:::further-reading`
   - a memorable line → `:::pullquote`
   - a reader → product push (once high, once low) → `:::cta`
   - a pro shortcut → `:::tip` (easily-missed caveat → `:::note`)

   **High-value additions — plan these by content type + persona, only where they earn their place:**
   - **first mention of the article's core term** → `:::definition term="…"`
   - **a pitfall / must-know** → `:::warning` (hazard / data-loss / money-loss) or `:::important` (must-not-miss prerequisite that isn't a hazard)
   - **a comparison / technical "which should I use" section** → `:::proscons` (one option, `## Pros`/`## Cons`), `:::feature-matrix` (features × products, `yes`/`no`/`partial`), `:::decision-table` (classification grid) + the `:::preferred-order` ranked list that follows it; a one-line call → `:::verdict`
   - **a cited statistics roundup (5+ sourced figures)** → `:::stat-list` (1–4 hero numbers stay `:::stat`/`:::stat-group` — do not plan `:::stat-list` for fewer than 5)
   - **an FAQ section** → `:::faq` (adds FAQPage schema; plain H2/H3 FAQs are fine when schema isn't the goal)
   - **roundup / listicle scaffolding** → `:::jumplinks` (a "skip to the app" anchor menu) + one `:::entry n= name= url= best_for= price=` header per item; a qualitative award → `:::badge kind="…"`
   - **a captioned data figure / diagram** → `:::figure src= source=` / `:::diagram src=` only when a real `src` already exists at draft time. **Visuals are ON (2026-06-29)** and `/generate-visuals` produces the asset from the typed `[VISUAL:]` placeholder, so the default is to plan the `Visual N:` micro-spec (step 6) and let the visuals stage fill it — reach for a `:::figure`/`:::diagram` fence only when you are pointing at an asset that already lives on disk
   - **situational embeds** → `:::tweet url=` (degrade to `:::pullquote` if no live embed) · `:::video src= title=` (rare)

   Note the **inline treatments** the draft will apply (no fence, governed by voice — you don't plan them per-section, but keep them in mind when shaping a section): inline `` `code` `` for formulas/literal values, `{lead}…{/lead}` on the opening paragraph, `==mark==` for the rare highlight, plain-link citations (no superscripts), and a "Final thoughts"/"Bottom line" closer.

   **Per-persona favorites** to bias the plan toward (the draft picks the persona; plan for the likely one): **Sloane Avery** → `:::methodology` / `:::stat` / `:::stat-list` / `:::table` / `:::key-takeaways`; **Theo Hart** → tables / numbered steps / `:::decision-table` / `:::preferred-order` / `:::feature-matrix` / `:::cta` / `:::further-reading`; **Mateo Reyes** → `:::expert` / `:::pullquote` / `:::tweet` / `:::nutshell` / `:::sidenote` / `:::figure`.
7. **Comparison table (when the beat spec requires one).** Spec it as a real markdown table skeleton in the outline: columns (from the beat spec's required-columns list), one row per item, plus a `Visual: {type: table}` entry on the section. The draft authors the table in GFM markdown; `/format-for-publish` converts it for the site renderer. Do NOT pre-degrade tables into bullet lists at outline or draft time.
8. **Plan the intro.** Hook + thesis + preview. 150–200 words. The hook earns attention with something specific, surprising, or contrarian — never "In today's digital age".
9. **Plan the conclusion.** Restated thesis + one next step (often a `2-reference/` link). 80–150 words.
10. **Run the visual sanity check (per `templates/visual-strategy.md` — NOT a density quota).** For every planned `[VISUAL:]`, confirm three things: (a) **need** — name the concrete value it adds *right here*; if you can't, drop it; (b) **no native duplication** — it is NOT a stat/quote/table/callout that a `:::` directive should carry (those are planned as natives, never as `[VISUAL:]`); (c) **resolvable** if it's a chart/diagram — it points at a real `research.<key>` or a `config=` file you'll author, never an invented key. For every **screenshot-type** visual (`external`/`screenshot`/`action-shot`), also confirm it **names what to annotate** — the point it makes — so the shot directs the eye (strategy §7); self-evident charts/diagrams stay un-annotated. Then sweep the whole outline: is the self-vs-third-party mix roughly **~80% third-party / category** and only ~20% our product (unless the post is genuinely about us)? Are the **sources varied** — not the same source over and over (don't lean on Google SERPs; mix Reddit/forums, competitor UIs, reviews, news, real artifacts)? Are any two visuals stacked back-to-back (space them)? There is **no minimum count and no "every N words"** — a missing visual beats a weak or duplicate one. Under-showing a real value-moment and over-showing filler are *both* failures; need-driven placement is the only bar.
11. **Run the structural self-check** in `references/bluf-mece-rules.md`.
12. **Run the beat-spec self-check (NEW, blocking):**
   - [ ] Section word targets sum to target word count ±10%
   - [ ] Item count ≥ beat spec item target (if list-shaped)
   - [ ] Every consensus topic appears in the coverage map
   - [ ] `[GAIN]` section exists and is genuinely not on page 1
   - [ ] Comparison table specced iff required
   If any box fails, fix the outline before saving — do not hand the debt to `/draft`.
13. **Save** to `content-pipeline/3-outlines/{slug}.md` using `templates/outline-template.md` structure (beat-spec restatement at top, coverage map at bottom).

## Output

`content-pipeline/3-outlines/{slug}.md` — typically 600–1,200 words. Detailed enough that `/draft` can expand without re-doing research.

## Quality checklist

- [ ] Title direct, includes primary keyword, <60 chars
- [ ] One-sentence thesis
- [ ] H2 list MECE, supports thesis, **sized by beat spec (no arbitrary 4–7 cap)**
- [ ] Each H2: BLUF, key points, evidence source, word target, transition, typed Visuals
- [ ] Components planned per section (`**Components:**` line) where one earns its place, drawn from the full authored set as the content type calls for it (definition/warning/important/proscons/feature-matrix/decision-table/preferred-order/verdict/stat-list/faq/jumplinks/entry/badge/figure/diagram/tweet/video) — restraint applied (1–2 of each max, most sections zero), fence names exact per `examples/ahrefs-components.md`; a `:::nutshell` planned under the H1 and `:::key-takeaways` for the conclusion when the format warrants
- [ ] Word targets sum to beat-spec total ±10%
- [ ] Coverage map: every consensus topic → a section
- [ ] `[GAIN]` section present
- [ ] Table skeleton present iff beat spec requires
- [ ] Visuals are need-driven (each names purpose + value-first source + type), value-first ~80/20 (mostly third-party/category, our-product only when on-topic), no native-component duplication, charts/diagrams point at a real `research.<key>` or authored `config=` — per `templates/visual-strategy.md`; NO density quota / no "image every N words"
- [ ] Intro = hook + thesis + preview; conclusion = restated thesis + next step
- [ ] Zero forbidden phrases (brand-config)

## Common failure modes to avoid

- **Compression** — the SERP demands 9 items and you outline 4 "best picks". That's how we shipped a 1,100-word listicle into a 2,500-word SERP. Match or beat; never shrink.
- **Section overlap** — "Why X matters" and "Benefits of X" are the same section. Pick one.
- **Consensus amnesia** — research lists must-cover topics; outline silently drops two. The coverage map exists to make that impossible.
- **Skipping the BLUF** — throat-clearing openers lose skim-readers.
- **Hook that says nothing** — "In today's competitive landscape…" is not a hook.
