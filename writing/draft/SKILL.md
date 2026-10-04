---
name: draft
description: Expand an annotated outline into full article prose using brand voice anchored in example articles, hitting the outline's per-section depth targets. Triggered after /product-mentions.
allowed-tools: Read, Write, Glob
---

# Draft Skill

Turn the annotated outline into a publishable first draft. The draft is **not** final — `quality-check`, `verify-claims`, `generate-visuals`, `preview`, `format-for-publish` follow. But it should be 80% there.

## What changed (2026-06-12) — read this if you remember the old rules

The old skill enforced numeric voice quotas (24–35-word paragraphs, em-dashes per 1,000 words, you-words per 1,000 words). Optimizing those quotas produced metric-compliant, soulless prose: uniform 2-sentence paragraphs, choppy rhythm, one rhetorical tic repeated eight times — exactly the AI tells we're paid to avoid. **Those quotas are gone.** Voice now comes from the example articles, depth comes from the outline's word targets, and the only mechanical rules left are the ones that catch real failure (crutch repetition, forbidden phrases, throat-clearing).

## The three commitments

1. **Depth.** Hit every section's word target ±20%, and the article total ±15% of the beat-spec target (restated at the top of the outline). If you finish a section 40% under target, you skipped evidence or specifics — go back to the dossier and add the missing concrete material. Never pad with abstractions to hit a number; depth = more specifics, not more words about words.
2. **Specificity.** Every section earns its length with concrete material: named tools, real numbers (cited), steps a reader can follow, first-hand product detail, real user language from the deep-research file. A paragraph with no specific noun or number in it is a candidate for deletion.
3. **Voice from examples.** Before writing a word: read `examples/README.md`, then **2 voice articles from `examples/voice/` in full, plus the 1 structure/niche example closest to this content type**. The prose in those files is the spec. Rules below are guardrails only.

## Input

For slug `{slug}`:
- `content-pipeline/4-outlines-annotated/{slug}.md` (required — outline with product annotations; includes beat-spec restatement + per-section word targets)
- `content-pipeline/0-context/{slug}.md` (if exists — user direction; wins all conflicts)
- `content-pipeline/2-reference/{slug}.md` (brand context, internal-link opportunities)
- `content-pipeline/1-research/{slug}.md` + `{slug}-deep.md` (evidence, stats, user quotes)
- `brand-config.md` (voice, audience, products, **forbidden phrases**)
- `references/voice-guide.md` (structural voice rules) + `references/prose-patterns.md` (sentence-level patterns)
- `../../../templates/visual-types.md` (controlled vocabulary for `[VISUAL:...]` placeholders)
- `examples/` per commitment #3

## Process

1. **Read examples first** (commitment #3). Then the outline thoroughly — you're not re-architecting; the outline is the spec. Then context, references, research, brand-config.
2. **Draft the intro** (150–200 words): hook (direct claim, surprising cited stat, opinion, or problem-naming), thesis, preview.
3. **Draft each H2 in order:**
   - Open with the section's BLUF (or a sentence capturing the same idea)
   - Develop key points using `references/prose-patterns.md`; pull the evidence the outline specified — stats carry a `[link]` placeholder when you lack the exact URL (verify-claims resolves them; they must NOT survive past that stage)
   - Hit the section word target ±20% with specifics, per commitments #1–2
   - Product mentions exactly where annotated — "show, don't sell"
   - Internal links from `2-reference/` inline as `[anchor](URL)`
   - Close with a transition
4. **Tables are content, not decoration.** Where the outline specs a comparison table, author it as a real GFM markdown table with every column and row filled from research. `/format-for-publish` handles site-renderer conversion (PLEAA-567) — never pre-degrade a table into bullets at draft time. The preview and the editor see the real table.
5. **Insert typed visual placeholders** — one per `Visual N:` entry in the annotated outline, at natural break points. Forms (full field reference + selector cheatsheet in `templates/visual-types.md`):
   - `[VISUAL:type=screenshot;target=<product-slug>;what=<UI element>;annotate=<optional>]`
   - `[VISUAL:type=action-shot;url=<starting URL>;goal=<explicit click-path under 60 words>;what=<caption>]` — `/capture-visuals` drives Chrome (pinned to Sonnet); write the goal like briefing a human who has never seen the site
   - `[VISUAL:type=image;sub=<concept-illustration|diagram|flow-diagram|comparison|lifestyle>;prompt=<specific structured prompt>;style=<illustration|photorealistic|flat-vector|isometric>;safety=<sfw|adult>]` — prompts name every labeled component; `safety=adult` routes to manual capture
   - `[VISUAL:type=chart;data=<research.key>;style=<bar|line|pie>;title=<title>]`
   - `[VISUAL:type=external;sub=<reddit-comment|tweet|news-quote|competitor-ui|chart>;url=<source>;selector=<CSS>;crop=padded;what=<caption>]` — auto-captured (PLEAA-417); Reddit comments are `#t1_<id>`, tweets `article[data-testid="tweet"]`
   - `[VISUAL:type=video;url=<…>;what=<…>]`, `[VISUAL:type=gif;what=<…>]`
6. **Draft the conclusion** (80–150 words): thesis restated fresh + one next step.
7. **Self-edit pass — the human-editor read.** Read the full draft top to bottom and fix:
   - **Crutch repetition (the #1 tell):** any distinctive word or rhetorical move used 3+ times ("honest", "Here's the thing", "stated plainly", a verdict-sentence formula repeated per section). Two uses max; rewrite the rest with different constructions.
   - **Uniform rhythm:** if every paragraph is 1–3 short sentences, merge and vary. Good prose mixes one-sentence punches with 4–6-sentence developed paragraphs (look at how the example articles breathe). Avoid walls of text past ~90 words too — but vary, don't cap.
   - **Forbidden phrases** (brand-config list) — zero tolerance.
   - Sentences starting with "Furthermore", "Moreover", "It is important to note".
   - Filler intensifiers ("very", "really", "quite", "actually", "simply") where they carry no weight.
   - Every section opens with its BLUF; no section opens with throat-clearing.
   - Product mentions demonstrate, never list features.
   - **The empty-paragraph test:** any paragraph with no concrete noun, number, step, or example → cut it or make it concrete.
8. **Depth gate (replaces the old metrics gate).** Count words per section against the outline targets. Any section <80% of target → return to the dossier/deep file and add real material (an example, a number, a step, a user quote). Article total within ±15% of the beat-spec target. Only then save.
9. **Save** to `content-pipeline/5-drafts/{slug}.md` — H1 title, then prose. No metadata header.

## Output

`content-pipeline/5-drafts/{slug}.md` — word count per the beat spec (typically 1,800–4,000 words).

## Quality checklist

Before saving, confirm:
- [ ] Read 2 voice examples + 1 structure/niche example this run (not from memory)
- [ ] Every outline section drafted; word targets hit ±20%; total ±15% of beat-spec target
- [ ] Listicle item count matches the outline (no compression)
- [ ] Comparison table authored as real markdown (when specced)
- [ ] No crutch word/move used 3+ times; paragraph rhythm varied
- [ ] Zero forbidden phrases; zero "Furthermore/Moreover/It is important to note" openers
- [ ] Every numerical claim cited or carrying `[link]` for verify-claims
- [ ] Product mentions only where annotated, demonstrative
- [ ] All visual placeholders typed per the controlled vocabulary
- [ ] Internal links from `2-reference/` woven in with descriptive anchors

## When the draft feels off

- **Sounds generic** → you didn't anchor in the examples. Re-read them, rewrite the worst two sections.
- **Sounds salesy** → cut product mentions that fail the "competent reader" test.
- **Sounds choppy** → rhythm is uniform. Merge paragraphs, vary sentence length.
- **Sounds thin** → it IS thin. Back to the dossier for specifics; never pad.

If two voice-fix passes don't help, the problem is upstream — fix the outline or the research, not the prose.
