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
- `../../../templates/visual-types.md` + `../../../templates/editorial-principles-visuals.md` (visual decisions)
- `examples/` — read `examples/README.md`, then 1 structure example + 1 niche example closest to this content type

## Process

1. **Read all inputs.** Restate the BEAT SPEC numbers at the top of your outline file so the draft stage sees them without re-opening the dossier.
2. **Choose the article title.** Direct, includes the primary keyword early, under 60 characters when possible.
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
   - **Visuals** — one or more typed micro-specs (`screenshot` / `action-shot` / `image` / `table` / `chart` / `video` / `external` / `gif` / `none`), format:
     ```
     **Visuals:**
       Visual 1: {type: image, sub: concept-illustration, prompt: <specific structured prompt>, safety: sfw}
       Visual 2: {type: screenshot, target: create, what: voice profile selector, annotate: arrow on speaker icon}
     ```
     Apply the decision sequence in `templates/editorial-principles-visuals.md`. The default for any non-trivial section (>300 words) is "this section deserves a visual; what kind?". For brand-product UI: `screenshot` if a single URL shows the state, `action-shot` if it takes clicks (routed to `/capture-visuals`). For quoted Reddit/tweets/news: `external` with a `selector`.
7. **Comparison table (when the beat spec requires one).** Spec it as a real markdown table skeleton in the outline: columns (from the beat spec's required-columns list), one row per item, plus a `Visual: {type: table}` entry on the section. The draft authors the table in GFM markdown; `/format-for-publish` converts it for the site renderer. Do NOT pre-degrade tables into bullet lists at outline or draft time.
8. **Plan the intro.** Hook + thesis + preview. 150–200 words. The hook earns attention with something specific, surprising, or contrarian — never "In today's digital age".
9. **Plan the conclusion.** Restated thesis + one next step (often a `2-reference/` link). 80–150 words.
10. **Run the visual sanity check (two-way)** — for every H2 with a visual, confirm it earns its place (concrete info lost without it, supports the BLUF, MECE across sections); for every `none` section, check whether a labeled diagram/screenshot/chart/table would make it twice as good. Density target per `editorial-principles-visuals.md` (5/8/10/12 for <1.2k / 1.2–2k / 2–3k / >3k words), ≥3 distinct types.
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
- [ ] Word targets sum to beat-spec total ±10%
- [ ] Coverage map: every consensus topic → a section
- [ ] `[GAIN]` section present
- [ ] Table skeleton present iff beat spec requires
- [ ] Visual density within range, ≥3 distinct types
- [ ] Intro = hook + thesis + preview; conclusion = restated thesis + next step
- [ ] Zero forbidden phrases (brand-config)

## Common failure modes to avoid

- **Compression** — the SERP demands 9 items and you outline 4 "best picks". That's how we shipped a 1,100-word listicle into a 2,500-word SERP. Match or beat; never shrink.
- **Section overlap** — "Why X matters" and "Benefits of X" are the same section. Pick one.
- **Consensus amnesia** — research lists must-cover topics; outline silently drops two. The coverage map exists to make that impossible.
- **Skipping the BLUF** — throat-clearing openers lose skim-readers.
- **Hook that says nothing** — "In today's competitive landscape…" is not a hook.
