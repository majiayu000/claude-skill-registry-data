---
name: matplotlib-python
description: >-
  Use for writing, reviewing, debugging, or testing static Python visualization
  with Matplotlib, including Figure, Axes, Axis, Artist, transforms, layouts,
  dates, categorical scales, annotations, color normalization, image export,
  and headless rendering. Do not use for Plotly interactivity, Altair/Vega-Lite
  specifications, dashboard state, or analysis without a Matplotlib artifact.
argument-hint: "[figure intent, data shape, output format, and verification]"
---

# Matplotlib figure construction

Use the explicit object interface for reusable code:

```text
Figure -> one or more Axes -> Axis objects and data/annotation Artists
```

`pyplot` may create the Figure and Axes, but pass `ax` through helpers rather
than relying on hidden current-figure state.

## Workflow

1. Define the perceptual question, audience, output dimensions, medium, units,
   accessibility needs, and whether axes are shared.
2. Inspect data shape, missing values, category order, datetime timezone,
   uncertainty, and scale. Do not let implicit string categories or date parsing
   silently determine order.
3. Create `fig, ax = plt.subplots(...)`; use Axes methods for marks, labels,
   limits, scales, annotations, and legends. Return Figure/Axes or save the
   artifact; do not bury global display side effects inside helpers.
4. Use data coordinates for values, axes coordinates for annotations tied to
   the panel, and figure coordinates only for figure-level layout.
5. Set layout and export deliberately. For automation, select a noninteractive
   backend before importing pyplot, save with explicit size/DPI/format, and
   close figures created in loops or tests.
6. Verify semantics and rendering: series count, data values, labels, limits,
   scale, legend, accessible colors, output dimensions, and nonempty image.

## Invariants

- A Figure is the complete canvas; an Axes is one plotting region; an Axis owns
  ticks and scale; almost every visible item is an Artist.
- Do not mix stateful current-Axes calls with explicit Axes ownership in a
  reusable function.
- Do not truncate a quantitative bar baseline without explicit disclosure and
  a defensible reason.
- Use one shared normalization for color values that must be comparable across
  panels.
- Use Seaborn only as a statistical plotting layer when its aggregation and
  uncertainty semantics are intended; verify the resulting Matplotlib objects.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
ax.plot(months, values, marker="o", label="Observed")
ax.set(title="Monthly throughput", xlabel="Month", ylabel="Orders")
ax.legend()
fig.savefig("throughput.svg", metadata={"Title": "Monthly throughput"})
plt.close(fig)
```

Read [the object and coordinate model](references/object-model.md), [chart and
scale decisions](references/decisions.md), and [render verification](references/testing.md).
