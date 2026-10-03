---
name: visual-check
description: Read a render output (and optionally a reference) using Claude's multimodal capability and produce a short qualitative inspection note.
invocation: /visual-check <render-path> [<reference-path>]
---

# /visual-check \<render-path\> [\<reference-path\>]

Use Claude's multimodal `Read` tool to inspect the named render. If a
reference path is also given, compare the two.

## Output format

Produce a concise inspection note (5–10 lines) covering:

1. **Overall impression**: exposure, contrast, colour balance
2. **Artifacts**: fireflies, banding, NaN pixels (magenta/black spikes),
   aliasing, moire
3. **Material fidelity**: are metals metallic, glass transparent, diffuse
   surfaces diffuse?
4. **Spectral signature** (if applicable): visible dispersion, chromatic
   effects, band-specific artefacts
5. **Comparison delta** (if reference given): what changed, better or worse,
   any regressions

## Examples

```
/visual-check tests/reference/disney_contact_sheet_post_compensation.png
/visual-check test_results/optix_before.png test_results/optix_after.png
/visual-check benchmarks/showcase/output/cornell_spectral_512spp.png
```

## Note

This is a qualitative pass — use it to quickly flag obvious problems or
confirm a fix. It does not replace the numerical gates in the hardware
verifier. When something looks wrong here but the numbers pass, escalate
to `gate-failure-reviewer`.
