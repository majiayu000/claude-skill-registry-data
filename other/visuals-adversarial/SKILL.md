---
name: visuals-adversarial
description: Skeptical pushback on visual placement — both density and quality. Reads the annotated outline plus the visuals manifest and asks (a) whether the article hits the density target from editorial-principles-visuals.md, (b) whether each [VISUAL:...] earns its place, (c) whether sections without one would benefit. One revision pass on FAIL (BLOG_AGENT_VISUALS_REVISION_BUDGET, default 1).
allowed-tools: Read, Write, Bash, Task
---

# Visuals Adversarial Skill

Phase 3 of PLEAA-392 (PLEAA-418, 2026-05-06; rebalanced PLEAA-499, 2026-05-07).
Two failure modes are now in scope: **decorative over-density** (visuals that
don't carry information) and **flat under-density** (articles below the
density target with low type diversity, leaving the reader staring at long
unbroken prose). The bar shifted in PLEAA-499: the reference is the
ahrefs-style article — ~10 high-value visuals across 4–7 sections, with
type diversity. This skill enforces both directions of the rule.

The orchestrator dispatches this skill **after** stage 9 (`/generate-visuals`)
writes the manifest and **before** stage 10 (`/preview`). Stage 11
(`/capture-visuals`) may run between — if so, the adversarial reads the
post-capture manifest. On `FAIL` with budget remaining, the orchestrator
re-dispatches `/generate-visuals` with the critique (specifically: which
visuals to strip and which to add) and re-runs this skill.

## Dependency on PLEAA-417

This skill is most useful **after** PLEAA-417 (visuals broadening) lands. Until
then, most external visuals fall to manual capture, so the adversarial mostly
flags decorative auto-captured screenshots — still useful, but the full value
shows up once Reddit / news / competitor-UI captures are real assets the
adversarial can judge on its own merits.

In degraded mode (PLEAA-417 not landed yet), the adversarial should still:

- Strip decorative auto-captures of pleasur.ai pages.
- Flag manual-capture entries that the editorial rule says don't earn a visual
  at all (so they drop, not move from `manual` to `none`).
- Skip the "is this external screenshot the right crop" question — the assets
  don't exist yet.

## Input

For slug `{slug}`:

- `content-pipeline/4-outlines-annotated/{slug}.md` (the annotated outline —
  source of truth for which sections asked for which visuals)
- `content-pipeline/6-drafts-cited/{slug}.md` (the cited draft, post-visuals
  rewrite — to see where visuals actually landed)
- `content-pipeline/images/{slug}/manifest.json` (status of each visual)
- `content-pipeline/images/{slug}/manual-capture.md` (if present — entries
  routed to manual)
- `templates/editorial-principles-visuals.md` (THE rule)
- `templates/visual-types.md`

## Process

1. Spawn a `Task` sub-agent with the brief below.
2. Combine into `content-pipeline/quality-checks/{slug}-visuals-adversarial.md`.
3. Print the verdict + CRITICAL count.

## Adversarial sub-agent brief

> You are a skeptical art director reviewing the visual placement for
> `{slug}`. The principle is in `templates/editorial-principles-visuals.md`:
> the article should feel like the ahrefs reference — high density of
> *high-value* visuals (concept-illustration `image`s, screenshots, charts,
> external citations, occasional video/gif), with type diversity. Two
> failure modes: decorative visuals that add nothing (strip), and
> low-density / monotype articles that leave the reader staring at unbroken
> prose (add).
>
> Read in order:
> 1. `templates/editorial-principles-visuals.md`
> 2. `templates/visual-types.md`
> 3. `content-pipeline/4-outlines-annotated/{slug}.md`
> 4. `content-pipeline/6-drafts-cited/{slug}.md`
> 5. `content-pipeline/images/{slug}/manifest.json`
> 6. `content-pipeline/images/{slug}/manual-capture.md` (if it exists)
>
> Compute first:
> - Article word count (cited draft).
> - Density target from the table in `editorial-principles-visuals.md`
>   (5 / 8 / 10 / 12 for <1.2k / 1.2–2k / 2–3k / >3k word articles).
> - Actual non-`none` visual count from manifest (`status=captured` only).
> - Distinct type count (target ≥3).
>
> Push back on six questions:
>
> 1. **Density.** Is the captured visual count below the target band? If
>    yes, this is the headline issue — the article reads thin. List
>    specifically which sections deserve a visual but currently have none,
>    and what type each should be.
> 2. **Type diversity.** Are fewer than 3 distinct types present? If the
>    article is all `screenshot` or all `chart`, it reads narrow. Suggest
>    which type to add (most often `image` sub=concept-illustration for
>    explanatory diagrams, or `external` for citing real-world sources).
> 3. **Decorative visuals.** For each visual that landed, ask: does it
>    carry information the prose doesn't? A screenshot of a static
>    marketing page when the prose already describes it is decorative. A
>    lifestyle `image` with no specific labels is decorative. List
>    specific decorative entries — these should be stripped *or* upgraded
>    to a more informative type.
> 4. **Wrong type.** Is any visual the wrong type? (A screenshot where a
>    `chart` would carry the data; a `chart` where a side-by-side `image`
>    sub=comparison would beat it; a vague `image` lifestyle prompt where
>    a `image` concept-illustration with labels would be far better.)
> 5. **Crop / framing.** For captured assets, does the crop highlight the
>    moment that adds value, or is it a full-page screenshot with the
>    relevant detail buried? Be specific by file path.
> 6. **Manual fallthrough.** Any entries in `manual-capture.md` that, by
>    the rule, shouldn't have been requested at all? These should drop
>    rather than be chased.
>
> Output:
>
> - 4–10 findings tagged `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
>   - `CRITICAL` = the article ships either (a) below the density target
>     by 2+ visuals (reads thin / monotype), or (b) with a visual that
>     actively hurts (decorative in a serious section; chart whose data
>     contradicts the prose; comparison forced into paragraph form).
>     Each missing-density `CRITICAL` should name a specific H2 + the
>     suggested type so the revision loop has a placeholder to add.
>   - `HIGH` = density is exactly 1 below target (within the acceptable
>     range floor but tight), or a visual is low-value but not actively
>     harmful.
> - At least 2 visuals that genuinely earn their place (call out the good).
> - A one-line **Verdict: PASS** or **Verdict: FAIL**. **FAIL** if density
>   is below target by 2+ OR if any CRITICAL is open. The FAIL and
>   CRITICAL thresholds are deliberately aligned: a 2-below-target FAIL
>   always carries at least one CRITICAL density finding, so the revision
>   loop's Add step has something concrete to act on.
>
> Do NOT capture replacement visuals or rewrite the draft. Under 700 words.

## Output

`content-pipeline/quality-checks/{slug}-visuals-adversarial.md`. Same skeleton
as the other adversarial skills. `## Verdict:` line must be exact.

## How the orchestrator handles FAIL

Same loop as the other adversarial skills with stage key `visuals`:

1. `python scripts/adversarial_runlog.py can-revise {slug} visuals`
2. If budget remains: increment, dispatch a revision pass.
   - The revision is **two operations** rather than re-running stage 9 wholesale:
     - **Strip:** for each `CRITICAL` decorative finding, edit
       `content-pipeline/6-drafts-cited/{slug}.md` to remove the
       `![alt](images/{slug}/...)` line and merge the surrounding paragraphs.
       Mark the corresponding manifest entry `status=stripped` with the
       adversarial finding ID as the reason.
     - **Add:** for each `CRITICAL` missing-visual / density finding, append
       new typed `[VISUAL:...]` placeholders to the cited draft at the named
       H2(s) and re-run `/generate-visuals` for those placeholders. Prefer
       `image` (sub=concept-illustration) for "section needs explanation"
       gaps — fastest to generate and adds the most type diversity. Use
       `external` for "section quotes a real source but has no visual
       evidence". Use `chart` for "section cites a stat but has no chart".
3. If exhausted: write `9-needs-review/{slug}.md` and HALT.

## Why this skill exists

A draft can fail visually in two ways: (1) ship with 8 decorative
screenshots that read like AI slop, or (2) ship with only 2 lonely visuals
clustered at the bottom and 2,500 words of unbroken prose between them.
Both fail the reader. The editorial principles in
`templates/editorial-principles-visuals.md` set the bar (ahrefs density,
type diversity, every visual carrying information) but nobody enforces it
after the visuals land — the orchestrator advances if the manifest shows
everything captured, regardless of whether half are wallpaper or whether
the article is 4 visuals short of target. This skill enforces the rule in
both directions.

Historical note (PLEAA-499, 2026-05-07): earlier framing of this skill
biased it toward stripping. Pre-PLEAA-499 articles routinely shipped with
2/4 visuals stripped on aesthetic grounds, leaving 1–2 captures total —
materially below the editorial bar. The rebalanced version strips the
bias: missing visuals at the density target are a CRITICAL finding equal
in weight to a decorative visual that hurts.
