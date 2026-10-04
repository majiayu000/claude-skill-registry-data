---
name: design-stereo-field
description: Use when placing elements in the stereo field or designing spatial depth in a mix
source: David Gibson "The Art of Mixing" (2005), Bob Katz "Mastering Audio" (2002), Haas Effect research (Haas 1949)
tags: [music, mixing, stereo, panning, mid-side, haas-effect, spatial-audio, depth]
verified: true
---

# Design Stereo Field

Place audio elements in the stereo field to create width, depth, and separation without sacrificing mono compatibility.

## Why This Is Best Practice

**Adopted by:** David Gibson's three-dimensional mix visualization is taught in audio engineering programs worldwide; mastering engineers universally require mono-compatible mixes
**Impact:** Gibson's "The Art of Mixing" documents that spatial placement is perceived as emotional distance — elements panned center feel more intimate; wide elements feel distant or environmental. This is not metaphor; it is perceptual psychology.

**Why best:** A flat, center-panned mix is fatiguing and lacks dimension. Strategic stereo field design creates the auditory illusion of a physical space — instruments in specific locations, depth from front to back. However, every width decision must be verified in mono because streaming services, phone speakers, and many club systems sum to mono, collapsing unchecked stereo into phase cancellation artifacts.

## Steps

1. **Anchor the center** — Kick, snare, bass, lead vocal, and lead melody always stay at or near center (panned 0). These are the harmonic and rhythmic pillars; moving them off-center destabilizes the mix.
2. **Build symmetrical width** — Pan guitars, keyboards, and secondary instruments in symmetric pairs (Guitar L 30% ↔ Guitar R 30%). Asymmetric panning creates a lopsided mix that sounds amateur on mono systems.
3. **Use depth via reverb pre-delay and level** — Close elements (dry, loud, short reverb pre-delay 0-20ms). Distant elements (wet, quieter, longer pre-delay 30-80ms). Depth is perceived front-to-back; panning is left-right.
4. **Apply the Haas effect for width** — Delay a copy of a mono source by 20-30ms and pan it opposite the original. The brain fuses them and perceives width, not echo. Mono-check: sums cleanly because the delay is sub-40ms.
5. **Use mid-side (M/S) processing on buses** — On the stereo bus or drum bus, M/S EQ can widen or narrow the image: boost the Side channel in upper mids for width; cut the Side channel at low frequencies to keep bass mono.
6. **Keep bass mono below 120Hz** — Bass frequencies are non-directional below ~120Hz; stereo bass wastes headroom and causes phase issues on mono systems. Use a mono filter or M/S technique to collapse sub-frequencies.
7. **Check in mono** — Sum the full mix to mono. Elements that disappear or change tone significantly have phase cancellation issues. Any cancellation must be resolved before the mix is finished.
8. **Reference on earbuds and a Bluetooth speaker** — These are the listening environments where mono-compatibility failures are most audible; a mix that survives these translates everywhere.

## Rules

- Kick, snare, bass, and lead vocal must be mono at the center — no exceptions for commercial music.
- Never pan a single instrument hard left or right without a counterpart on the opposite side — it creates imbalance.
- All stereo width decisions must pass the mono check before the mix is finalized.
- Sub-bass frequencies (below 120Hz) must be mono in any mix destined for club playback or streaming.

## Examples

Pop mix stereo layout: Center (0): kick, snare, bass, lead vocal. L15/R15: acoustic guitar doubles, piano. L40/R40: electric guitar layers, synth pads. L60/R60: hi-hats (alternating takes), percussion fills. L100/R100: ambience reverb tail only (not dry signal). Depth: lead vocal closest (short reverb, loud). Background vocals behind (more reverb, -3dB). Room reverb on drums farthest back.

## Common Mistakes

- Bass guitar panned off-center — creates mono playback imbalance; bass must be anchored at center.
- Width added via stereo widening plugins without mono check — stereo widening creates phase issues that collapse badly in mono.
- No depth dimension — all elements at the same perceived distance create a flat, 2D mix; reverb pre-delay creates the front-to-back illusion.
- Panning everything hard left or right — full-pan elements dominate one side; reserves hard pan for accents and FX, not primary instruments.

## When NOT to Use

- When delivering a mono-only format such as a podcast bed, mono broadcast stem, or any output that will be permanently summed before playback.
- When mixing for immersive audio formats (Dolby Atmos, Ambisonics) where the stereo panning paradigm is replaced by three-dimensional object positioning tools.
- When the source recording is a single mono microphone and artificial stereo widening would introduce phase artifacts not present in the original performance.
