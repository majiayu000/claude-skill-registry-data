---
model_tier: high
name: image-analyser
description: "Use to analyse a character image down to the smallest mole and diff against a canon — per-feature spec, OCR-reads tattoo text, flags drift. Triggers 'analyse this image', 'match the canon'."
personas:
  - hollywood-director
domain: product
workspaces:
  - small-business
packs:
  - ai-video
lifecycle: experimental
trust:
  level: experimental
install:
  default: false
  removable: true
---

# image-analyser

> Read a character image, extract **every** feature (face marks, per-location
> tattoos incl. lettered text, exact hair split, per-eye colour, jewelry,
> asymmetry), and diff it against the character's canon so drift is caught
> **before** it ships. Output feeds [`image-creator`](../image-creator/SKILL.md)
> and the fidelity loop. Schema + rubric + loop: [`canon-spec.md`](canon-spec.md).

## When to use

- "Analyse this image / character", "does this match the canon", "check
  character accuracy", "find what's wrong with this render".
- As the verify step of the fidelity loop (after `image-creator` generates).
- To bootstrap a Canon Spec from an authoritative portrait (the *image wins
  over the text*).

NOT for: scene/motion review (→ `video-director`), non-character art
(→ `canvas-design`), cross-scene token locking (→ `character-consistency`,
which consumes this skill's output).

## Input

- Image **path or public URL** (per the `vision-analyze` shape).
- Optional: a reference Canon Spec / character id (e.g.
  `agents/reference/ai-video/<project>/characters/<id>.json`) to diff against.
- **Input gate** (per the `image-ocr` contract): refuse blurry / sub-resolution
  / unreadable inputs with a clear reason rather than guessing.

## Procedure

1. **Read the image.** A vision-capable model views it directly. No new
   dependency; if a cloud-vision/OCR backend is wanted, ask first
   (`missing-tool-handling`).
2. **Section-by-section extraction** (the "down to the smallest mole" pass) —
   one pass per section: `physique`, `face` (+ marks/scars/moles), `hair`
   (colour, split line, length, braids, shaved areas), `eyes` (per-eye colour,
   heterochromia, ring, kohl), `tattoos` (per body location: motif, style,
   and **text** if lettered), `jewelry`, `outfit`, cross-feature `asymmetry`.
3. **OCR sub-pass for lettered tattoos** — read runic/block text exactly
   (knuckle runes, `S-U-S-I`, scalp runes, mic glyph), never approximate.
4. **Hard-feature enhancement** — for a faint mole, an unclear hair-split line,
   or heterochromia in shadow: re-pass on a crop/zoom of that region **before**
   marking it. Only then mark genuinely unresolvable features `unverifiable`.
5. **Emit the `observation` layer** (Layer 2 in `canon-spec.md`): observed value
   + `confidence` (high|medium|low) per feature + `unverifiable[]`. Confidence
   lives here, **never** written back onto the canon (Layer 1).
6. **If a reference is given — diff + score** per the rubric: per-feature
   `match|partial|miss`, the **canon-breaking hard gate**, per-section scores,
   advisory roll-up, and `low`-confidence misses flagged `needs-better-image`
   (not a hard fail). Emit concrete correction directives per miss.

## The one rule that overrides everything

**The image wins over the text.** When extracting from an authoritative portrait
and the canon text disagrees, record what is *visible*. When verifying a
candidate against the canon, the canon's `identity` is the truth. Never invent a
feature the image does not show (per `direct-answers` — no invented facts); mark
it `unverifiable` instead.

## Output format

1. **Observation JSON** (Layer 2) — observed features + per-feature confidence + `unverifiable[]`.
2. **Diff table** (only if a reference was given): `feature · severity · expected · observed · verdict (match/partial/miss) · confidence · fix`.
3. **Verdict line:** `GATE: pass|FAIL (canon-breaking misses: …)` + per-section scores + advisory roll-up.

## Example (safe vs unsafe)

- Safe: `eyes — canon-breaking — expected blue-left/green-right — observed both blue — MISS (high) — fix: regenerate with heterochromia anchor front-loaded`.
- Unsafe: reporting `eyes — match` when the green eye is out of frame. If unseen → `unverifiable`, not `match`.

## Gotchas

- Hands/knuckles often out of frame → tattoo text `unverifiable`, not a miss.
- A strong face must not mask a broken hair split — that is why scores are
  per-section, not one number.
- Symmetric characters (Sigrún, Bjørn) vs the asymmetric one (Veikko): check
  the left/right invariant explicitly for the Loki-marked character.

## Do NOT

- Do NOT score an unseen feature as `match` — if it is out of frame or
  unresolvable, mark it `unverifiable` (per `direct-answers`, no invented facts).
- Do NOT write `confidence` / `unverifiable` back onto the canon (Layer 1) — they
  are the analyser's epistemic state (Layer 2) and never mutate the truth layer.
- Do NOT collapse the rubric to a single number — a strong face must never mask a
  canon-breaking hair/eye miss; scores stay per-section with a hard gate.
- Do NOT approximate lettered tattoo text — OCR it exactly or mark it `unverifiable`.
- Do NOT analyse a real-person likeness without routing through
  `media-governance-routing` first.

## Policies

Character images can carry a real person's likeness. Before analysing a
real-person likeness, route through `media-governance-routing` and consult
`agents/settings/policies/media/likeness.md` + `public-figures.md`. Fictional
characters (e.g. the odins-beard trio) are exempt; the routing decision is the
agent's, in-session.

## Related skills

- [`image-creator`](../image-creator/SKILL.md) — consumes the diff; the loop partner.
- [`character-consistency`](../character-consistency/SKILL.md) — consumes the load-bearing token subset of the `identity` layer.
- [`canon-spec.md`](canon-spec.md) — schema, rubric, fidelity loop.
- [`screenshot-hygiene`](../screenshot-hygiene/SKILL.md) — reuses this skill's OCR text-read to detect sensitive data in a documentation screenshot before it ships.
