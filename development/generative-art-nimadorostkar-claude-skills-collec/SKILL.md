---
name: generative-art
description: Use when creating algorithmic or generative visual art. Covers composition through code, controlled randomness, colour systems, and building work that is varied without being arbitrary.
metadata:
  category: design
  version: 1.0.0
  tags: [generative, algorithmic-art, creative-coding, randomness, canvas]
---

# Generative Art

## Purpose

Create visual work through code, where the interesting output comes from constrained randomness rather than unconstrained noise. Pure randomness produces mush; the craft is in the constraints.

## When to Use

- Creating algorithmic or procedural visual work.
- Building a generative system that produces a family of related outputs.
- Data-driven visual work.
- Exploring composition computationally.

## Capabilities

- Controlled randomness: distributions, noise fields, seeded reproducibility.
- Composition: grids, subdivision, packing, flow fields.
- Colour systems for generative palettes.
- Output at print resolution.

## Inputs

- The visual idea or the underlying system.
- Constraints: palette, format, medium.
- Whether outputs must be reproducible (they should be).

## Outputs

- A system producing a family of related, non-identical works.
- Seeded, reproducible output.
- Assets at the resolution the medium requires.

## Workflow

1. **Seed the randomness** — Always. An unseeded generative system produces something beautiful once and can never produce it again. This is the first thing to get right and the most commonly skipped.
2. **Constrain the space** — Randomness within a structure. A grid whose cells vary, a palette whose members are sampled, an angle that jitters within a range. Unconstrained randomness is visual noise.
3. **Use noise, not uniform random, for anything spatial** — Perlin or simplex noise produces coherent variation. `Math.random()` per pixel produces static.
4. **Build the palette as a system** — Sample from a small set, or from a ramp. Per-element random colour destroys any coherence the composition had.
5. **Generate many, select few** — The output of a generative system is a distribution. Produce a hundred, choose the ones that work, and adjust the constraints toward them.
6. **Render at the output resolution** — Not scaled up afterwards. A generative composition designed at 800px and upscaled to print looks exactly like that.

## Best Practices

- An unseeded system is a system that cannot be reproduced, iterated on, or printed at a different size. Seed it from the start.
- Perlin and simplex noise are what make generative work look organic rather than random. The difference between `random()` and `noise(x, y)` is the difference between static and a landscape.
- Constrain the colour: sample from a palette of four, or from a single ramp. Fully random colour is the most reliable way to make generative work look amateurish.
- Symmetry and repetition give the eye something to hold. Pure variation with no structure is exhausting to look at.
- The best generative systems have one or two parameters that meaningfully change the output. A system with forty knobs is unexplorable.
- Produce original systems. Do not reimplement a recognizable artist's signature work.

## Examples

**Seeded, constrained, and using noise for coherence:**

```javascript
import { createNoise2D } from "simplex-noise";
import Alea from "alea";

// Seeded: this exact image can be regenerated, at any resolution, forever.
const SEED = "2026-07-14-a";
const prng = new Alea(SEED);
const noise2D = createNoise2D(prng);

// A palette, sampled — not random colour per element.
const PALETTE = ["#0f172a", "#1e40af", "#0891b2", "#f59e0b"];
const PAPER = "#faf8f3";

function draw(ctx, width, height) {
  ctx.fillStyle = PAPER;
  ctx.fillRect(0, 0, width, height);

  const GRID = 48;
  const cell = width / GRID;

  for (let x = 0; x < GRID; x++) {
    for (let y = 0; y < GRID; y++) {
      // Noise, not random: adjacent cells are RELATED, which is what makes
      // the field read as a structure rather than as static.
      const n = noise2D(x * 0.06, y * 0.06);          // -1..1, spatially coherent
      const angle = n * Math.PI;                       // a flow field
      const length = cell * (0.4 + Math.abs(n) * 0.9); // varies with the field

      // Colour is sampled from the palette, indexed by the field — so colour
      // varies coherently too, rather than speckling.
      const colour = PALETTE[Math.floor(((n + 1) / 2) * PALETTE.length * 0.999)];

      // Sparse: skip cells where the field is weak. Negative space is composition.
      if (Math.abs(n) < 0.18) continue;

      const cx = x * cell + cell / 2;
      const cy = y * cell + cell / 2;

      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(angle);
      ctx.strokeStyle = colour;
      ctx.lineWidth = cell * 0.14;
      ctx.lineCap = "round";
      ctx.beginPath();
      ctx.moveTo(-length / 2, 0);
      ctx.lineTo(length / 2, 0);
      ctx.stroke();
      ctx.restore();
    }
  }
}

// Print: render at the final resolution, not upscaled.
// A2 at 300 DPI = 4961 x 7016 px. The grid and line widths scale with `width`,
// so the same seed produces the same composition at any size.
```

## Notes

- The line `if (Math.abs(n) < 0.18) continue;` is doing a disproportionate amount of the compositional work: it creates negative space where the field is weak, which gives the piece structure. A generative system that fills every cell is almost always worse than one that does not.
- Seeded PRNGs (Alea, and similar) are essential. `Math.random()` cannot be seeded in JavaScript, which makes any system built on it irreproducible.
- Generate in batches and curate. The system's output is a distribution; your job is to shape the distribution and then choose from it.
