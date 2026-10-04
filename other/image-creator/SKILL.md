---
model_tier: high
name: image-creator
description: "Use to generate a character image to spec — max-fidelity reproducible prompt from a Canon Spec, anchors-first, provider/governance-gated. Triggers 'generate this character', 'render to spec'."
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

# image-creator

> Turn a **Canon Spec** + a scene into a maximally-detailed, reproducible
> generation prompt that renders a character to spec — then hand the result to
> [`image-analyser`](../image-analyser/SKILL.md) to verify. The loop partner.
> Schema + rubric + loop: [`canon-spec.md`](../image-analyser/canon-spec.md).

## When to use

- "Generate / render / create this character", "render Veikko in scene X to
  spec", "make the image match the canon".
- Inside the fidelity loop, fed by `image-analyser`'s correction directives.

NOT for: scene blocking / motion (→ `video-director`, `motion-choreographer`,
which take a verified still from here), non-character art (→ `canvas-design`).

## Input

- Character id / Canon Spec (`agents/reference/ai-video/<project>/characters/<id>.json`).
- Scene brief (setting + pose). Optional: prior `image-analyser` diff (loop mode).

## Procedure

1. **Governance gate FIRST** (per `media-governance-routing`): if the character
   is a real-person likeness, consult `agents/settings/policies/media/likeness.md`
   + `public-figures.md` + `disclosure.md` before emitting anything. Fictional
   characters (odins-beard trio) are exempt; the routing decision is in-session.
2. **Provider gate** (per `provider-lifecycle-discipline`): read the resolved
   provider's tier; if non-stable (experimental/deprecated/community), surface
   the tier and ask before running. Never default to a non-stable provider
   silently. Name the provider + tier in the run summary.
3. **Assemble the prompt from the spec — anchors first.** Order matters: the
   hard-to-render `identity_anchors` go at the TOP (the canon's lesson —
   heterochromia + hair-split get forgotten if buried). Then physique, face
   (+ marks), per-location tattoos (incl. exact `text`), outfit, jewelry.
4. **Asymmetry block** — for split / heterochromatic characters, an explicit
   left/right section ("LEFT half black / RIGHT half blond", "blue LEFT eye /
   green RIGHT eye") with concrete comparison refs for engines that drop it.
5. **Negative block + engine settings** — reuse the canon's proven structure
   (negatives that kill "single hair colour", "both eyes same colour", etc.;
   per-engine `--ar`/`--style`/CFG/steps). Do not reinvent; the character book's
   prompt format is the template.
6. **Generate** through the existing provider/adapter layer
   (`scripts/ai-video/adapters/`, the `/video|image` surface). Do **not** add a
   new provider path where one exists.
7. **Verify** — hand the output to `image-analyser`; in loop mode, fold its
   correction directives into the next prompt (see the loop in `canon-spec.md`).

## Anchors-first — why

The fidelity-loss evidence (`img_2.png`): Veikko's split hair + heterochromia
were missed because they are hard for the engine and were not front-loaded. The
analyser-derived fixes go to the TOP of the next prompt, with negatives, and the
loop re-verifies — that is how the smallest mole comes back.

## Output format

1. **Generation prompt** — anchors block · positive · asymmetry (if any) · negative · engine settings.
2. **Provider + tier line** (the audit entry).
3. **Verify call** — the `image-analyser` invocation on the result + the loop stop-state.

## Example (anchors-first vs buried)

- Safe (Veikko): prompt opens with `HAIR: exact vertical centre split, LEFT pitch-black, RIGHT platinum-blond` + `EYES: heterochromia — LEFT ice-blue, RIGHT forest-green`, then the rest.
- Unsafe: physique/outfit first, the split + heterochromia in a trailing sentence → the engine drops them (the observed `img_2.png` failure).

## Gotchas

- Never claim "canon-perfect" without an `image-analyser` pass (per `verify-before-complete`).
- DALL-E drops heterochromia + split hair — use concrete comparisons; expect multiple generations.
- Keep the spec the single source: regenerate from the Canon Spec, never paraphrase it into a fresh prompt.

## Do NOT

- Do NOT claim "canon-perfect" / "matches the canon" without an `image-analyser`
  pass on the output (per `verify-before-complete` — no completion without evidence).
- Do NOT bury the `identity_anchors` — the hard-to-render features (heterochromia,
  hair-split) go at the TOP of the prompt, never in a trailing sentence.
- Do NOT default to a non-stable provider silently — surface the tier and ask
  first (per `provider-lifecycle-discipline`).
- Do NOT emit a prompt for a real-person likeness before the governance gate
  (step 1) clears it.
- Do NOT add a new provider/generation path where the existing adapter layer
  (`scripts/ai-video/adapters/`) already covers it.
- Do NOT paraphrase the Canon Spec into a fresh prompt — regenerate from the spec
  so it stays the single source of truth.

## Policies

`media-governance-routing` + `agents/settings/policies/media/` (likeness, style,
public-figures, disclosure) — consulted in step 1 before any prompt is emitted
for a real-person likeness.

## Related skills

- [`image-analyser`](../image-analyser/SKILL.md) — the verify/loop partner.
- [`character-consistency`](../character-consistency/SKILL.md) — supplies the locked identity tokens.
- [`video-director`](../video-director/SKILL.md) / [`motion-choreographer`](../motion-choreographer/SKILL.md) — take the verified still into scene + motion.
