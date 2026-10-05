---
name: paperbanana
description: Use when creating architecture, methodology, system, data-flow, deployment, or schema diagrams, statistical plots or charts, or multi-figure publication packages via PaperBanana - including GCP-branded Google Cloud architecture diagrams - or when iterating on, refining, or evaluating generated figures against a reference. Also use when the user mentions PaperBanana, figure generation, batch diagram generation, or configuring Gemini as an image generation provider.
user-invocable: true
allowed-tools:
  - mcp__paperbanana__generate_diagram
  - mcp__paperbanana__generate_plot
  - mcp__paperbanana__continue_diagram
  - mcp__paperbanana__continue_plot
  - mcp__paperbanana__batch_diagrams
  - mcp__paperbanana__batch_plots
  - mcp__paperbanana__orchestrate_figures
  - mcp__paperbanana__evaluate_diagram
  - mcp__paperbanana__evaluate_plot
  - mcp__paperbanana__download_references
  - Read
  - "Bash(paperbanana *)"
---

# PaperBanana

Generate publication-quality diagrams and statistical plots through the **PaperBanana MCP server** —
a visualizer↔critic pipeline that plans, renders, and self-critiques figures.

Prefer the MCP tools. They are faster than the CLI, keep run state for cheap refinement, and are
what this skill is built around. The CLI, Python API, and pipeline internals are in
[references/cli.md](references/cli.md).

For GCP-branded architecture diagrams built by **direct Vertex AI image generation with official
icon overlay** — a different toolchain from PaperBanana — use the `gcp-diagram` skill instead.

## Models

> **PaperBanana's own defaults are stale.** As of v0.3.0 it ships
> `IMAGE_MODEL=gemini-3-pro-image-preview`, which Google **shut down on 2026-06-25**. Image
> generation fails out of the box until you set `IMAGE_MODEL`. Its VLM default,
> `gemini-2.5-flash`, still works.

### Recommended defaults

| Slot | Model | Why |
|---|---|---|
| `IMAGE_MODEL` | `gemini-3.1-flash-image` | Nano Banana 2 — Pro-level quality at Flash cost, 4K, strong text rendering. The stable replacement for the retired `-preview` ID. |
| `VLM_MODEL` | `gemini-3.7-flash` | Latest stable Flash (GA 2026-08-13). Cheapest of the 3.x Flash tier under introductory pricing through 2026-12-31. |

Set both on the MCP server (`IMAGE_MODEL` / `VLM_MODEL` in its `env` block — see
[references/cli.md](references/cli.md)) so single-figure tools need no model arguments.
**Batch, orchestrate, and continue tools fall back to their own defaults**, so pass models
explicitly there:

```
image_model="gemini-3.1-flash-image", vlm_model="gemini-3.7-flash", image_provider="gemini", vlm_provider="gemini"
```

### Switching models

Both slots are free to change — pick per job:

| Instead of the default, use | When |
|---|---|
| `gemini-3.1-flash-lite-image` | Cheapest image tier (~$0.034 per 1K image, ~4s). Rapid ideation, high-volume batches. |
| `gemini-3-pro-image` | Highest fidelity — reasoning-heavy composition, complex multi-turn edits, up to 14 reference inputs. Costs materially more per image. |
| `gemini-3.5-flash` / `gemini-3.6-flash` | Pinning to a proven earlier Flash generation. |
| `gemini-2.5-flash` | Most conservative VLM: PaperBanana's own default and the only one in its cost table (below). |

Avoid any `*-preview` image ID — `gemini-3.1-flash-image-preview` and `gemini-3-pro-image-preview`
were both shut down 2026-06-25 — and `gemini-2.0-flash`, shut down 2026-06-01.

### Two caveats

- **Cost tracking is incomplete.** `paperbanana/core/pricing.py` only prices the retired
  `-preview` image IDs and Flash models up to `gemini-3-pro`. Runs on the recommended models
  report **$0**, which is a gap in the estimate, not a free run.
- **`thinking_budget` is dated.** PaperBanana sends `thinking_budget=8192` for every model matching
  `gemini-2.5+`, while Gemini 3.x expects the `thinking_level` enum. This applies equally to
  3.5/3.6/3.7 Flash, so it is not a reason to prefer one over another — but if you see thinking
  config rejected, `gemini-2.5-flash` is the fallback that matches PaperBanana's call path.

## Tools

| Tool | Use for | Pass models? |
|---|---|---|
| `generate_diagram` | one methodology / architecture / system / data-flow diagram from text | no (server env) |
| `generate_plot` | one statistical plot / chart from JSON data | no (server env) |
| `continue_diagram` / `continue_plot` | refine an existing run by `run_id` (skips retrieval + planning) | **yes** |
| `batch_diagrams` / `batch_plots` | many figures from a YAML/JSON manifest | **yes** |
| `orchestrate_figures` | plan + generate a full figure package from a paper | **yes** |
| `evaluate_diagram` / `evaluate_plot` | score a figure against a reference (4 dimensions) | no |
| `download_references` | one-time: fetch reference set for better in-context examples | no |

All are `mcp__paperbanana__*`. If the MCP server is unavailable, fall back to the CLI —
see [references/cli.md](references/cli.md).

## Workflow

1. **Gather** — for a diagram: components and services, connections with protocols and direction,
   logical groupings, and diagram type (system overview, agent hierarchy, data flow, schema,
   deployment). For a plot: the data plus the communicative intent — what the reader should
   conclude.
2. **Generate** — call the matching tool:
   - `generate_diagram(source_context=..., caption=...)`
   - `generate_plot(data_json=..., intent=...)`
   - Keep `auto_refine=false` (or `iterations` low) under the 2 RPM image cap.
3. **Verify** — run the branding and spelling checklist in
   [references/gcp-brand.md](references/gcp-brand.md). For GCP diagrams, `source_context` and
   `caption` must carry the brand phrases and color conventions from that file.
4. **Refine cheaply** — do not regenerate from scratch. Call
   `continue_diagram(run_id=..., feedback=..., image_model="gemini-3.1-flash-image", vlm_model="gemini-3.7-flash")`;
   it reuses retrieval and planning.

## Refinement limits — geometry does not refine

Observed 2026-09-10 on a GCP reference architecture. A `forecast → resolve → evolve` chain had an
outbound arrow the prompt attached to `resolve`; the model drew it leaving `evolve`. **Four**
`continue_diagram` calls failed to move it — one returned `strict_success: true` having changed
nothing, another "fixed" it by breaking two things that were already correct.

The cause is mechanical rather than a bad prompt: an outbound arrow attaches to whichever box is
**spatially last** in the chain, and `continue_*` re-renders from the image rather than editing it.

- **Spend at most one `continue_*` on geometry** — origin, endpoint, routing. Label text, colours
  and added boxes refine fine; geometry does not.
- **Fix it in the layout and regenerate instead.** Reordering to `evolve → forecast → resolve` made
  the arrow correct on the first try, and read better besides.
- **Keep every iteration.** `continue_*` overwrites `final_output.png`, so the good image may be
  `diagram_iter_1.png`. Check `diagram_iter_*.png` before accepting a regression.

### Bands are respected; columns within a band are not

Same session: a separate group sitting beside an `A → B → C` chain got wired to the nearest node in
that chain — twice, ignoring an explicit "nothing else leaves this box". Moving it to its own titled
horizontal band fixed it in one call.

Stack independent subsystems as titled bands one above another and state "there are NO arrows
between bands". A long edge that must cross the whole figure is a layout smell: restructure so it
becomes a *return* arrow beneath a chain, which renders reliably.

## Evaluation

`evaluate_diagram` / `evaluate_plot` score a generated figure against a human reference on four
dimensions: **Faithfulness, Conciseness, Readability, Aesthetics**. Supply the generated image, the
reference image, the source context, and the caption.

## Quota — a separate pool from Vertex

PaperBanana authenticates with `GOOGLE_API_KEY` against the **Gemini Developer API**
(`generativelanguage.googleapis.com`), which is a **separate quota pool** from the **Vertex AI**
project quota. It does **not** contend with a Vertex 2 RPM image cap — verified 2026-07-13 by
generating two diagrams during a live batch with zero failures on either side.

Caveats that still apply:

- The Developer API has its own rate limits (free-tier RPM per key). Under bursty use expect `429` /
  `ClientError`. `auto_refine=true` loops visualizer→critic and issues many image calls, so prefer
  `auto_refine=false` with `iterations=1–2` unless you need refinement. Batches serialize best with
  `concurrency=1`.
- The key must be a valid **Gemini Developer API** key (it lists models at `/v1beta/models?key=…`).

## Common mistakes

| Mistake | Fix |
|---|---|
| Passing `image_model`/`vlm_model` to `generate_diagram`/`generate_plot` | Unsupported — they read the server env; omit. |
| Letting `batch_*` / `orchestrate_*` pick default models | Always pass `image_model="gemini-3.1-flash-image"`, `vlm_model="gemini-3.7-flash"`. |
| Regenerating just to tweak a figure | Use `continue_*` with the `run_id` — except for arrow geometry, which does not refine; fix the layout and regenerate (see Refinement limits). |
| Burning `continue_*` calls on an arrow that will not move | Geometry re-renders rather than edits. One attempt, then change the layout. |
| Assuming PaperBanana eats the Vertex 2 RPM cap | It bills the separate Gemini Developer API pool. |
| Using a `*-preview` image model ID | Both were shut down 2026-06-25 — use the stable IDs in Models above. |
| Trademarked GCP logos render wrong | Expected — generative models approximate icons. Keep every text label spelling-accurate (table in gcp-brand.md). |
| Low-quality CLI output | Add `--optimize --auto`; see [references/cli.md](references/cli.md). |

## References

- [references/cli.md](references/cli.md) — CLI commands, provider setup, batch manifests, Python API, pipeline architecture
- [references/gcp-brand.md](references/gcp-brand.md) — brand colors, spelling table, verification checklist
- GCP icon gallery: https://cloud.google.com/icons
