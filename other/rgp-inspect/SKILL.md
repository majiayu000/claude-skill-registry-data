---
name: rgp-inspect
description: Decode and analyze existing AMD Radeon GPU Profiler (.rgp) traces from the command line, including gfx1201/RDNA 4 SQTT instruction timing, stalls, embedded code-object disassembly, RDF metadata, and JSON or CSV evidence. Use when Codex needs to inspect a trace, compare captured kernel variants, attribute shader stalls to ISA, or replace GUI-only instruction analysis with reproducible output.
---

# RGP Inspect

Use the shared `rgp-inspect` CLI to extract evidence from an existing `.rgp`
capture. Do not recapture a workload unless the trace lacks the required data.

## Workflow

1. Run `rgp-inspect doctor` to locate the full Radeon Developer Tool Suite, `amdgpu-dis`, and the patched decoder.
2. If the native decoder is absent, read [references/build.md](references/build.md) and build the pinned decoder visibly.
3. Run `rgp-inspect decode CAPTURE.rgp --out REPORT.json --csv REPORT.csv`.
4. Check `resolution_ratio`, `decoder_info`, and stream validation before interpreting hot instructions.
5. Reject traces with impossible CU/SIMD identifiers or less than 95% ISA resolution.
6. Compare traces only when capture mode, workload shape, dispatch selection, and clock policy match.
7. Report the capture type and distinguish wave-aggregated shader cycles from kernel wall time.

## Commands

```powershell
rgp-inspect doctor
rgp-inspect decode trace.rgp --out trace.json --csv trace.csv
```

The decoder build and gfx12 token format are revision-sensitive. Do not silently
substitute another `rocprof-trace-decoder` revision. Read
[references/format.md](references/format.md) before changing RDF extraction,
address resolution, or report semantics.

## Interpretation rules

- Treat instruction-trace values as shader cycles unless trustworthy clock calibration is present.
- Do not convert summed per-wave instruction cycles into kernel wall time.
- Report instruction duration, stall, and scheduler idle separately.
- Use RGP event timing or benchmark events for kernel wall time.
- State whether evidence came from instruction tracing, counter capture, event timing, or an ordinary benchmark.
- Do not infer named GUI counter formulas from raw SPM identifiers without a verified mapping.

If no suitable trace exists, use the `rgp-capture` skill rather than embedding
capture lifecycle logic here.
