---
name: chart-animation
description: This skill should be used when the user asks to "make a bar chart race", "turn a CSV into a video", "build an animated data visualization", "create an animated statistics video", "animate a chart/graph", "make a number counter/ticker", "animate a ranking over time", or "batch-render one chart template across many datasets". Covers data-driven keyframing, value interpolation, rank transitions, counters, pacing, annotation, and template×data batch output.
version: 0.1.0
---

# Data Video

Turn a dataset into a chart that moves with intent: a bar chart race, a growing line, a count-up stat. The craft is mapping numbers to pixels every frame, easing the *value* (not just the opacity), and pacing the data so a viewer can actually read it.

## When to use

- Bar chart race / ranking-over-time (the headline use case).
- Animated line/area reveal, animated counters and number tickers.
- One chart design rendered across many datasets (template × CSV → N videos).

## The one rule that prevents 90% of bugs

**Drive every value from the current frame — never from wall-clock time or a library's internal animation loop.** A video frame is rendered deterministically; if a bar's height comes from a CSS transition or a D3/GSAP/Chart.js animation, it flickers or desyncs because the renderer and the animation clock disagree. Compute the displayed value as a pure function of frame.

```js
import { useCurrentFrame, interpolate } from "remotion";
const frame = useCurrentFrame();
const value = interpolate(frame, [0, 60], [0, 1287], { extrapolateRight: "clamp" });
```

In Remotion, disable all third-party chart animations (`animation: false` in Chart.js, no D3 `.transition()`) and let `useCurrentFrame()` be the only clock. D3 is still great for *scales and shapes* (`scaleLinear`, `scaleBand`, `line()`) — just not its timers.

## Map data → pixels

A chart is two functions: a value scale and a frame interpolator. Keep them separate.

| Layer | Tool | Job |
|---|---|---|
| Value scale | `scaleLinear` / `scaleBand` | data units → px (height, x-position) |
| Frame interpolation | `interpolate` / `spring` | frame → eased progress 0→1 |
| Display value | `round` + `Intl.NumberFormat` | progress → the number a human reads |

```js
import { scaleLinear } from "d3-scale";
const yScale = scaleLinear().domain([0, maxValue]).range([0, chartHeight]);
const barHeight = yScale(interpolate(frame, [0, 45], [0, datum.value], { extrapolateRight: "clamp" }));
```

## Easing value changes

Ease the value the same way you'd ease motion. For a count-up or a bar growing in, `easeOutCubic` reads as "settling on a number." For rank changes, prefer `spring` so a bar that overtakes another has a little weight.

```js
const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);
const t = easeOutCubic(interpolate(frame, [start, end], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
const shown = from + (to - from) * t;
```

Never linearly interpolate a value the viewer is reading unless it's a steady time axis (a clock, a year counter) — linear motion on a headline number feels robotic.

## Counters / number tickers

Interpolate the underlying number, then format on render. Two musts: **round before formatting** (no `1287.4013`), and **fix the digit box** so the layout doesn't jump as digits change.

```js
const n = Math.round(interpolate(frame, [0, 50], [0, 1287], { extrapolateRight: "clamp" }));
const label = new Intl.NumberFormat("en-US").format(n); // "1,287"
// CSS: font-variant-numeric: tabular-nums; line-height: 1;  → no width jitter, no clipping
```

For currency/percent use `Intl.NumberFormat("en-US", { style: "currency", currency: "USD" })`. Tabular figures keep each digit the same width so the number doesn't wiggle.

## Bar chart race — rank transitions

The signature move. Real datasets are sparse (yearly/monthly rows); a smooth race needs **interpolated keyframes between data rows** plus bars that slide to new ranks. The y-position comes from a rank that is itself interpolated, so an overtake animates as a glide, not a jump.

```js
// frame → continuous time between sparse rows, then rank each item by its interpolated value
const t = frame / fps;                  // seconds
const i = Math.min(Math.floor(t), rows.length - 2);
const f = easeInOut(t - i);             // 0→1 within the current row pair
const vals = items.map((it) => ({
  it,
  v: rows[i][it] + (rows[i + 1][it] - rows[i][it]) * f, // interpolated value
}));
vals.sort((a, b) => b.v - a.v);         // rank this frame
vals.forEach((d, rank) => { d.y = rank * (barH + gap); }); // y from interpolated rank
```

Render with stable keys per item (so React tracks each bar across reorders), animate `y` and `width` off the per-frame value, and show a moving year/date label. See `references/bar-chart-race.md` for a complete, runnable Remotion component.

## Pacing data over time

Animation that's too fast is unreadable. Budget time per data event, not per second of polish.

| Beat | Budget | Why |
|---|---|---|
| Intro / first frame | hold 1–1.5s | let the viewer read axes + units before motion |
| Per data row (race) | 0.3–0.6s | fast enough to feel alive, slow enough to track the leader |
| A highlighted moment | +0.5–1s slow-down | dwell on the crossover / record / inflection |
| Final state | hold 2–3s | the takeaway needs to land and be screenshot-able |

Reveal progressively — one series, then the next — instead of all data at once; viewers can only track one moving thing at a time.

## Labeling & annotation

Numbers without context are noise. Always render: an always-visible **value label** on each bar/point (it animates with the value), a **time indicator** (year/date), and **axis units once**. Add a callout only at the moment it matters (a crossover, a peak) — annotate the inflection, then let it fade.

## Template × data — batch output

The payoff of code-driven charts: one design, many datasets. Make the dataset an input prop, never a hardcoded constant, then render once per file.

```jsx
// Remotion: data is a prop; same composition, different CSV → different video
export const Race = ({ data }) => { /* …reads `data`, hardcodes nothing… */ };
```
```bash
# render the same template for every dataset in /data
for f in data/*.json; do
  name=$(basename "$f" .json)
  npx remotion render Race "out/$name.mp4" --props="$f"
done
```

Keep colors/fonts/layout in a single theme object so 50 videos stay brand-consistent and only the numbers change. See `references/data-pipeline.md` for CSV→props parsing, validation, and the full batch script.

## Output checklist

- Every animated value is a pure function of `useCurrentFrame()`; no library timers.
- Numbers are rounded and formatted (`Intl.NumberFormat`), digits use `tabular-nums`.
- Race bars carry stable keys; rank changes glide via interpolated rank.
- Axes/units labeled once; value labels animate with their value.
- Intro hold, readable per-row pace, final hold ≥2s.
- Dataset is an input prop — one template renders every CSV in the folder.

## Deliver & verify (rendered stills → MP4)

> **Packaged helper** (`scripts/`): tile your stills with `scripts/contact-sheet.sh sheet.png f-hook.png f-mid.png f-end.png`, then assert the encode with `scripts/probe-mp4.sh out.mp4 [WxH] [fps]`. See `scripts/README.md`.

Remotion is frame-deterministic — every bar height, counter value, and rank is a pure function of `useCurrentFrame()`, so you can render any exact frame headlessly with no seek harness. The deliverable is an MP4 carrying **exact numbers**, so still-inspection is non-negotiable here: a one-pixel layout bug is forgivable, a wrong digit is not.

**Output contract:**
- A Remotion project with the chart registered (`<Composition>` + zod `schema` + `defaultProps`), all motion frame-driven (no timers / `Date.now()` / `Math.random()`, no Chart.js/D3 `.transition()` clocks).
- Deliverable = the rendered `out/*.mp4` (plus the project, so the user can re-render with new datasets).
- Data-dependent duration (N rows × frames/row)? compute it in `calculateMetadata`, not by hand.

**Verify loop — render stills → inspect → encode.** Render single frames first (cheap, no video encode), then encode only once the numbers and layout are right.

```bash
# 1. Frame-exact stills at start / mid / end (PNG, headless, fast) — with the SHIPPED props
npx remotion still Race out/f-start.png --frame=0   --props='{"data":[...]}'
npx remotion still Race out/f-mid.png   --frame=90  --props='{"data":[...]}'
npx remotion still Race out/f-end.png   --frame=149 --props='{"data":[...]}'  # last = durationInFrames - 1

# 2. Inspect each PNG — FIDELITY (axis labels, value labels, year/date, ranks, units all EXACT —
#    round + tabular-nums working, no 1287.4013) AND artifacts (bar overflow, off-canvas label,
#    clipped safe-area, missing font, wrong data binding / wrong column mapped).

# 3. Only after the stills check out, encode:
npx remotion render Race out/race.mp4 --props='{"data":[...]}'
```

- Use `npx remotion compositions` to read each chart's `durationInFrames`/`fps` and pick the end frame.
- **Data-driven / batch (the headline case)**: verify ONE representative dataset via stills *before* batch-rendering all N files — a height-scale or column-mapping bug caught once beats finding it in 50 MP4s.
- **README demo GIF for free**: `npx remotion render Race out/demo.gif --codec=gif`.

**Before you finish:**
1. `npx remotion still` renders cleanly at frame 0, mid, and last — no errors, no missing fonts/assets.
2. Every number is **exact** (rounded, `Intl.NumberFormat`, `tabular-nums`) and inside the safe area at each frame.
3. Frame-driven only — no `Date.now()` / `Math.random()` / library timers (determinism holds in CI).
4. The **shipped** dataset props render correctly (not just `defaultProps`) — right column mapped, right scale.
5. Full MP4 encoded and plays; (optional) GIF rendered for the README.

## Reference files

- `references/bar-chart-race.md` — a complete runnable Remotion bar-chart-race component: sparse-row keyframe interpolation, per-frame ranking, gliding y-positions, animated value labels, and a D3-scale axis. Plus a vanilla canvas variant.
- `references/data-pipeline.md` — CSV/JSON → typed props parsing and validation, the theme object pattern, animated counters/line-reveal recipes, and the template×data batch render script for N videos.
