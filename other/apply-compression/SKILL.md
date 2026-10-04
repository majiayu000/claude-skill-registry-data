---
name: apply-compression
description: Use when applying dynamic compression to any audio source to control dynamics or add punch and glue
source: Mike Senior "Mixing Secrets for the Small Studio" (2011), Bob Katz "Mastering Audio" (2002), Roey Izhaki "Mixing Audio" (2017)
tags: [music, mixing, compression, dynamics, attack, release, parallel-compression, glue]
verified: true
---

# Apply Compression

Set compression parameters with intention — using attack, release, ratio, and threshold to achieve a specific dynamic and tonal goal.

## Why This Is Best Practice

**Adopted by:** Every professional mixer uses compression; Mike Senior's methodology is the most widely cited beginner-to-intermediate reference in English
**Impact:** Studies in music perception (Danielsen et al.) show that dynamic envelope shaping via compression is the primary tool for groove manipulation — attack time determines perceived "punch" more than any other parameter

**Why best:** Compression is misunderstood more than any other mixing tool. Most beginners over-compress, removing the dynamics that make music feel alive. The correct approach starts from the musical goal (control peaks, add punch, create glue, add sustain) and works backward to settings. Every compression decision should be audible when bypassed but not audible as "compression" when engaged.

## Steps

1. **Define the compression goal** — Choose one: peak control (tame transients), leveling (consistent volume), punch (enhance attack), sustain (extend decay), glue (blend a bus). Each goal has different optimal settings.
2. **Set the threshold** — Play the source at typical level; lower the threshold until the gain reduction meter shows 3-6dB of gain reduction on peaks. More than 8dB GR means the threshold is too low.
3. **Set the ratio** — Peak control: 4:1 to 8:1. Leveling: 2:1 to 4:1. Glue: 2:1 to 4:1. Hard limiting: 10:1 to ∞. Higher ratio = more aggressive control.
4. **Set the attack** — Fast attack (1-5ms) = tames transients, reduces punch. Slow attack (30-100ms) = lets transient through, adds punch. For drums: use slow attack to preserve the initial hit.
5. **Set the release** — Match the release to the musical tempo. Rule of thumb: release should allow gain reduction to return to 0 before the next note or beat. Too slow = pumping; too fast = chattering.
6. **Apply makeup gain** — Compression reduces level; add makeup gain to match the bypassed volume for accurate A/B comparison. Many compressors have an auto-gain option.
7. **Check with bypass at matched loudness** — The compressed version should sound more controlled and punchy, not quieter or "squashed." If it sounds worse, adjust attack or ratio.
8. **Consider parallel compression** — Blend heavily compressed signal (8:1, low threshold, all dynamics removed) with the dry signal for punch + sustain simultaneously. New York compression technique.

## Rules

- Never compress without a specific goal — "compressing because you should" produces flat, lifeless dynamics.
- Gain reduction of 3-6dB is the sweet spot; more than 8dB consistently is over-compression.
- Always A/B at matched loudness — louder always sounds better; loudness bias masks compression flaws.
- Parallel compression works on drums and buses; it rarely improves isolated melodic instruments.

## Examples

Snare drum compression for punch: Ratio 4:1, threshold -18dB, attack 30ms (let transient through), release 60ms (releases before next hit at 120 BPM). Makeup gain +4dB. Result: snare transient preserved, body sustains longer, consistent between soft and loud hits.

## Common Mistakes

- Fast attack on drums — kills the transient click that makes drums sound punchy; the compressed version sounds flat and distant.
- Too-slow release — causes gain reduction to "pump" in tempo with the music, creating an audible rhythmic wobble.
- Compressing every track with the same settings — different sources have different dynamic profiles; ratios and attack times must be adjusted per source.
- Not using makeup gain for A/B comparison — the uncompressed version will always sound "better" if it's louder; match levels before judging.

## When NOT to Use

- When the source is a classical or acoustic ensemble recording where preserving wide natural dynamics is essential to the performance's musical integrity.
- When dealing with MIDI instruments whose dynamics are already perfectly uniform and compression would only reduce headroom without controlling anything meaningful.
- When the mix is already printing for a mastering engineer who has explicitly requested uncompressed, full-dynamic stem deliveries.
