---
name: cite-algorithm
description: Before implementing any non-trivial physics, sampling, or numerical algorithm in Astroray, locate the canonical paper and a license-compatible reference implementation, save research notes to .astroray_plan/docs/, and cite the source in the code. Enforces CLAUDE.md §6 — no invented algorithms.
---

# cite-algorithm

CLAUDE.md §6 is a hard rule for this project: Cycles, Mitsuba, PBRT, LuxCore, RAPTOR, ipole, GYOTO, and the Blender Foundation have already solved the rendering and GR problems Astroray inherits. Re-deriving their solutions is expensive and almost always worse, and the closing journal article must cite real provenance.

This skill is the gate that runs **before** writing code for any non-trivial algorithm.

## What counts as "non-trivial"

Non-trivial (skill required):
- Sampling distributions (MIS, ReSTIR, equiangular, NEE strategies)
- Path-space algorithms (bidirectional, MLT, path guiding)
- BSDFs / closures beyond Lambertian + Schlick
- Spectral upsampling / colour management
- GR integrators, metric-aware tracing, Kerr coordinate transforms
- Plasma/synchrotron emission, polarised radiative transfer
- Denoising, neural caches, wavefront/queue scheduling
- Tone mapping beyond simple gamma, filtering kernels beyond box/Gaussian

Trivial (skip skill):
- Undergraduate-textbook math, well-known closed forms
- Lambertian cosine, Schlick Fresnel approx, Halton/Sobol low-discrepancy basics
- Language utilities, container glue, RAII wrappers

When in doubt, treat as non-trivial.

## Procedure

1. **State what you're about to implement** in one sentence. Identify which Astroray area it touches (cite a file under `src/` or a package under `.astroray_plan/packages/`).

2. **Search for the canonical paper.** Use `WebSearch` for the technique name + "paper" or "siggraph"/"eurographics". Aim for the original publication, not a blog post. Capture: title, authors, year, DOI or arXiv ID, venue.

3. **Find a license-compatible reference implementation.** Use `WebSearch` / `WebFetch` to locate the source. Acceptable licenses:
   - Apache-2.0, BSD-2/3-Clause, MIT, MPL-2.0, public domain / CC0
   - GPLv2 / GPLv3 — **only if** consistent with Astroray's license; check `LICENSE` and stop to ask if unsure.
   - Reject: proprietary, "research only", non-commercial, license unstated.
   Capture the repo URL, the commit/tag you read, and the specific file paths you'll mirror.

4. **Write research notes** to `.astroray_plan/docs/<topic>-research.md` (match the naming of existing entries — `caustics-research.md`, `restir-temporal-spatial-design.md`, `disney-energy-compensation-research.md`, etc.). Use the template below.

5. **Cite in the code itself.** Every translation unit that ports the algorithm gets a header comment block:
   ```cpp
   // Source: <Author> et al., "<Title>", <Venue> <Year>. DOI:<doi> / arXiv:<id>
   // Reference impl: <repo>@<commit> — <path/to/file.cpp> §<section or function>
   // License: <SPDX id> (compatible with Astroray's LICENSE).
   ```
   Inline citations on individual functions reference paper sections: `// Eq. 17 of Zeltner 2020`.

6. **Update `.astroray_plan/docs/external-references.md`** with a one-line pointer to the new research note, so the bibliography stays discoverable.

## Research-note template

Save to `.astroray_plan/docs/<topic>-research.md`:

```markdown
# <Topic> — Research

## Paper
- **Title:** ...
- **Authors:** ...
- **Year / Venue:** ...
- **DOI / arXiv:** ...
- **PDF:** <stable URL>

## Reference implementation
- **Repo:** <url>
- **Commit / tag:** <sha or tag>
- **License:** <SPDX> — compatible with Astroray's <LICENSE> because <reason>.
- **Files we mirror:**
  - `path/to/file.cpp` — <which function / section>
  - `path/to/header.h` — <which struct / API>

## What we reproduce
- Equations: <list, e.g. "Eq. 12–17 (importance weights)">
- Data structures: <list>
- Differences from the reference: <intentional simplifications, integration with Astroray's spectral path, etc.>

## What we deliberately do NOT take
- <e.g. their tile scheduler — we already have a wavefront queue>

## Integration plan in Astroray
- Files to add/edit: `src/...`, `python/...`
- Package: `.astroray_plan/packages/pkgNN-...`
- Tests / parity check: `tests/...` or `benchmarks/...`

## Open questions
- <anything to verify with the user before coding>
```

## Anti-patterns

- Implementing first, citing later: provenance becomes guesswork and the citation block ends up wrong.
- Citing a blog post or Wikipedia as the primary source for a non-trivial algorithm.
- Copying GPL code into Astroray without checking license compatibility against `LICENSE` and `THIRD_PARTY.md`.
- Skipping the research note because "it's a small change" — the rule applies per algorithm, not per LOC.
- Inventing an "improvement" over the reference. If the deviation is real, the research note must justify it explicitly under *Differences from the reference*.

## When to invoke

Either invoke explicitly (`/cite-algorithm`) before starting work on a new sampler/integrator/BSDF/emission model, or trigger automatically when a task description mentions implementing a named technique (e.g. "add ReSTIR DI", "port Cycles' principled hair", "implement Kerr-Schild coordinates"). The skill outputs the research note path and the code citation block; it does not write the implementation.
