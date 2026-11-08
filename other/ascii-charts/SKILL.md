---
name: ascii-charts
description: Build charts as plain Unicode-block text — bar, range, bullet, gap-bracket, star-histogram, heatmap, line, Venn, pie, donut and scatter — with a dependency-free Python script, for anywhere only monospace text survives (newsletter code blocks, Markdown, terminals, plain-text email, chat). Use when a chart has to embed as literal text instead of an image or a third-party chart service, or when you want a hand-made terminal look with no branding footer.
---

# ASCII charts

Terminal-style charts built from plain Unicode block characters and embedded as literal text:
a fenced code block in Markdown, a `<pre>` tag in HTML. No chart service, no "made with"
footer, no external account, and they render identically wherever monospace renders.

`scripts/ascii_chart.py` has one function per chart type. Run `python3 scripts/ascii_chart.py`
to print one example of every type as a sanity check.

Two things here were measured rather than assumed, and both had been wrong at first: at a 390px
phone viewport, rows past ~44 characters clip off the right edge, and a "round" circle in
monospace needs a horizontal aspect correction of about **2.49** (not 2.0). See Sizing and the
Pie/donut section.

Newsletter platforms differ in how they paste code blocks. Before relying on one, paste a test
chart into a real draft and check web, app and email renderings.

## Character set

- `█` `▓` `▒` `░` (U+2588, U+2593, U+2592, U+2591 — full/dark/medium/light
  shade) — fill density, from "most" to "least." Bars use `█`/`░` only
  (filled vs. track); pie/donut use all four (plus `▚`/`▞`/`▤`/`▥` if there
  are more than 4 slices) as distinct per-slice fills; the heatmap uses all
  four plus `·` (middle dot, not a blank space) for the lowest level, so a
  "quiet" cell still reads as an intentional part of the grid, not a gap.
- digits `1`–`7` — Venn region codes (a bitmask of which set(s) a region
  belongs to — see Venn below)
- `+` — open-ended flag on a range bar that could run higher than the shown
  ceiling (don't stretch the bar itself to fake a number you don't have)
- `┃` — bullet-chart target tick, drawn over whatever fill/shading is
  underneath so it's always visible
- `└─┘` — gap-bracket, spanning between two bar-ends
- `★`/`☆` — filled/open star, doubling as the star-histogram's row label
- box-drawing (`─│╭╮╰╯`) — line-chart and trend-line connectors
- `●` — scatter point marker

No color, anywhere. That's the medium, not a limitation to work around — a
pasted Substack code block is literal characters, nothing else survives (no
inline CSS, no styled spans). Any distinction a chart needs to make lives in
the character/digit/legend, not an unavailable color channel.

## Chart-type menu

| Job | Function | Use for |
|---|---|---|
| Magnitude comparison, several categories, all start at 0 | `bar(value, max_value, width)` + `render()` | Gas fill-up (5 min) vs. DC fast charge (45 min) |
| A min–max range, one category | `range_bar(start, end, scale_max, width, open_ended=)` + `render()` | "$100k–$300k+ installed" |
| Two values, before/after | Plain text: `f"{start} → {end}"` | "Wholesale $220 → taproom $650" — a bar doesn't add anything; the arrow *is* the chart |
| One measure vs. a benchmark band + a target | `bullet(value, scale_max, target=, benchmark=)` + `render()` | "Your rating: 4.2, normal band 3.8–4.5, target 4.7" |
| Explicitly call out the gap between two bars | `gap_bracket(a, b, scale_max, width, label=)` via `render(bracket=)` | "You vs. market median" — the report's signature move |
| A 1–5 (or similar) rating distribution | `star_histogram(counts)` | Google/Yelp star breakdown, one row per star count |
| Two categorical axes, shaded by intensity | `heatmap(matrix, row_labels, col_ticks=)` | Foot traffic by day × hour — "when are you busy/dead" |
| Trend over time, one series | `line_chart(values, height, x_labels=)` | Monthly revenue, review count over a year |
| Trend, inline in a sentence | `sparkline(values)` | "Reviews per month: ▂▃▅▆█▇▅▃, up 3x since March" |
| 2 or 3 named sets, where the *degree* of overlap is itself the finding | `venn(labels)` | "38% of your one-star reviews also mention wait time" — overlap size is the point |
| Parts of a whole, one snapshot | `pie(slices, radius)` | Revenue mix: coffee / hot food / drinks / lottery |
| Parts of a whole, with a headline total | `donut(slices, radius, center_text=)` | Same, with "247 reviews" sitting in the hollow center |
| Two numeric variables, is there a relationship | `scatter(points, width, height)` | Price vs. rating across competitors |
| Same, plus "and here's the trend" | `scatter_with_trend(points, width, height)` | Same, with a fitted line proving the correlation |

If nothing in this table fits, stop and think it through rather than forcing
a shape that doesn't fit — a chart that's technically renderable but
confusing is worse than falling back to the Chrome-headless PNG pipeline.

## The 2-second test for charts

A chart answers to the same standard a good sentence does: get
understood by a tired reader on their phone, on the first look, no
re-reading, no decoding. Apply the test before picking a chart type, not
after building one.

**The 2-second test:** could the intended reader — a small-business
owner, not a data analyst — say what this chart means within 2 seconds,
without reading a legend first? If understanding even one region or
slice requires decoding a legend first, that's the visual equivalent of
jargon: technically precise, but it makes the reader do work instead of
pulling them forward.

**Caught on a real issue**, by the editor reading the rendered post cold:
- The 3-set Venn digit-bitmask diagram required reading a 7-line legend
  before any region meant anything. The editor: they didn't
  understand it, so a regular business owner wouldn't either. The
  underlying fact — "you need all three of these, not just one" — is one
  sentence, and the numbered list right after the diagram already said it
  in plain English. The diagram added decode cost without adding
  information the prose didn't already carry more clearly. **Fix: cut
  it, let the sentence + list do the job.**
- The DC-fast-charger cost range bar (a single bar, no axis, no
  comparison point) had nothing to compare against. A bar's value comes
  from showing a magnitude *relative to something* — a scale, another
  bar, a benchmark. A lone bar with no reference point is decorative, not
  informative. The number it illustrated ($100k–$300k+) was already
  stated plainly one sentence earlier. **Fix: cut it too.**

**Rules that follow:**
- A chart that needs its own legend to be read is a warning sign — not
  just for Venn. A heatmap with unlabeled axes, or a pie with more slices
  than a reader can hold in their head, fails the same way.
- If a plain sentence states the fact as clearly as the chart would,
  skip the chart. Same instinct as swapping "several/many/various" for
  the actual count in prose: reach for a visual because a *comparison* or
  *trend* is the point, not just because the data has a shape.
- Every bar needs an axis (`render(..., axis=)`) or a second bar on the
  same scale to compare against. A single bar with neither conveys
  nothing — the same failure as a passive-voice sentence with no real
  subject. But once that's satisfied, drop the axis if it would just
  restate a number already sitting in a per-row value label — one
  gas-vs-charging bar dropped its `0 ... 45 min` axis line for exactly
  this reason: both rows already carry their own value ("5 min", "45
  min"), so the axis only repeated "45 min" a second time. Same
  principle as cutting a redundant clause from a sentence.
- Don't chart a number that's already one clean sentence. "$100k–$300k+
  installed" is maximally clear as text; charting it doesn't reveal a
  comparison, trend, or overlap, it just adds a decoding step for no
  payoff.
- Read the finished chart cold, the way the actual reader will — a
  gas-station owner on their phone, not the person who just built it and
  already knows what it's supposed to say.

## Workflow

Use `scripts/ascii_chart.py` rather than hand-aligning characters or
rasterizing geometry yourself — column math and circle/angle math are
exactly the kind of thing that's easy to get subtly wrong by eye and only
shows up as a one-character misalignment or a lopsided circle after the
fact. Run `python3 scripts/ascii_chart.py` any time to print one
example of every chart type as a sanity check.

### Bar / range bar

```python
from ascii_chart import bar, range_bar, render

rows = [
    ("Gas fill-up", bar(5, 45, 24), "5 min"),
    ("DC fast charge", bar(45, 45, 24), "45 min"),
]
print(render(rows, axis=("0", "45 min")))

row = ("DC fast charger", range_bar(100, 300, 300, 24, open_ended=True), "$100k–$300k+")
print(render([row]))
```

`render()` takes `(label, bar_string, value_str)` tuples and handles all
column alignment — pass your own pre-formatted `value_str` (currency,
units, whatever the copy needs); the function only handles geometry.

### Bullet chart

```python
from ascii_chart import bullet, render

rows = [("Avg rating", bullet(4.2, 5.0, target=4.7, benchmark=(3.8, 4.5), width=24), "4.2 (target 4.7)")]
print(render(rows, axis=("0", "5.0")))
```

A solid bar for the measured `value`, drawn over an optional shaded
`benchmark` band (the "normal" range, `▒`) with an optional `target` tick
(`┃`, always drawn last so it stays visible over any fill/shading beneath
it). Answers "am I inside normal, and how far from target" in one glance —
there is still only one real bar (the measure); the band is context.

### Gap bracket

```python
from ascii_chart import bar, gap_bracket, render

rows = [("You", bar(42000, 60000, 24), "$42,000"), ("Market median", bar(58000, 60000, 24), "$58,000")]
print(render(rows, bracket=gap_bracket(42000, 58000, 60000, 24)))
```

A `└─┘` bracket spanning between two bar-ends, with the gap's size
centered inside it (auto-formatted from the two values, or pass `label=`
for your own text). Use the *same* `scale_max`/`width` for the bars and
the bracket, or the span won't line up. This is "you vs. the market,"
made explicit instead of left for the reader to eyeball.

### Star histogram

```python
from ascii_chart import star_histogram

print(star_histogram([(5, 61), (4, 22), (3, 9), (2, 4), (1, 4)]))
```

`counts` is `[(stars, count), ...]` in whatever order you want printed
(usually 5 down to 1). The filled/open star glyphs (`★`/`☆`) double as the
row label — no need to also spell out "5 stars" in text. Built entirely on
`bar()` + `render()`.

### Heatmap

```python
from ascii_chart import heatmap

print(heatmap(matrix, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
              col_ticks=[(0, "12am"), (6, "6am"), (12, "12pm"), (18, "6pm")]))
```

`matrix` is rows × columns of numeric intensity (e.g. 7 days × 24 hours),
normalized across the *whole* matrix (not per-row) so shading is
comparable across rows. `col_ticks` is `[(column_index, label), ...]` — no
auto-spacing, pick positions that won't collide for the labels you pass.

### Line chart / sparkline

```python
from ascii_chart import line_chart, sparkline

print(line_chart([120, 135, 128, 150, 175, 190, 205, 198, 220],
                  height=10, x_labels=("Jan", "Sep")))

print(sparkline([3, 5, 4, 8, 12, 10, 15, 14, 18]))
```

`line_chart` draws a connected line with box-drawing corners (`╭╮╰╯│─`) —
there's no character for an arbitrary in-between slope, so width is fixed
at `len(values) - 1` columns (one per segment). `x_labels`, if given, is
just `(first, last)` printed on the axis row — say the in-between points in
the surrounding prose, don't try to label every tick. `sparkline` is a
single-row 8-level trend (`▁▂▃▄▅▆▇█`) for one clause inside a sentence, not
a standalone chart.

### Venn (2 or 3 sets)

```python
from ascii_chart import venn

diagram, legend = venn(["Highway exit", "Big store", "Grid capacity"])
print(diagram)
print(legend)
```

Rasterizes overlapping circles and fills each region with a **digit**
(a bitmask of which set(s) it belongs to: `1`, `2`, `4` for the plain sets,
`3`/`5`/`6` for pairwise overlaps, `7` for all three) rather than trying to
fit label text inside a curved boundary, which doesn't survive monospace
rendering. The legend (returned separately, print both) maps each digit
back to the real label combination, e.g. `7 = Highway exit + Big store +
Grid capacity <- all of them`. This was originally believed impossible in
ASCII (an early post fell back to a headless-Chrome PNG for its Venn) — the
digit-region technique solves it cleanly; there's no longer a case where
Venn needs the PNG fallback.

**But run it through the 2-second test above before reaching for it —
the digit legend itself is the thing that made one real Venn confusing
for a lay reader.** A Venn earns its place when the *degree* of overlap
is the finding (e.g. "38% of your one-star reviews also mention wait
time"). When the real message is "you need all three together, no partial
credit," a Venn is the wrong tool even when it renders correctly — plain
text does that job with no legend required, e.g.:

```
Highway exit  +  Big store  +  Grid capacity
        miss one of these, skip the site
```

### Pie / donut

```python
from ascii_chart import pie, donut

diagram, legend = pie([("Coffee", 40), ("Hot food", 25), ("Drinks", 20), ("Lottery", 15)], radius=9)
print(diagram); print(legend)

diagram, legend = donut([("Coffee", 40), ("Hot food", 25), ("Drinks", 20), ("Lottery", 15)],
                         radius=9, center_text="247")
print(diagram); print(legend)
```

Slices start at 12 o'clock and go clockwise (standard pie convention), each
gets a distinct fill character (`█▓▒░▚▞▤▥`, never repeated on an adjacent
slice for typical 2–6 slice counts) so boundaries stay legible without
color. `donut` is `pie` with a hollow center — `center_text` puts a
headline number/label there (e.g. a total count), which is the one thing an
ASCII donut can do that a real one usually wastes on empty space. `radius`
is in row-units; the function corrects internally for monospace character
aspect ratio (shared `ASPECT` constant, also used by `venn()`) so the
result is actually round, not a flattened oval — don't hand-tune
width/height separately, just pass `radius`.

**Correction:** `ASPECT` was hardcoded to an assumed `2.0`
and had never actually been checked against a rendered page — measuring
the real character-cell ratio in headless Chrome against the CSS this
skill itself prescribes (13px font, 1.5 line-height) gave `2.49`, not
`2.0`. At the old value every circle (Venn regions, pie/donut) rendered
about 25% taller than it was wide. `ASPECT` is now `2.49` in
`ascii_chart.py` — re-measure and update it again if the embedding CSS's
font-size or line-height ever changes.

### Scatter / scatter with trend

```python
from ascii_chart import scatter, scatter_with_trend

points = [(4.2, 3.8), (4.5, 4.1), (3.9, 3.5), ...]   # (x, y) pairs
print(scatter(points, width=50, height=20))
print(scatter_with_trend(points, width=50, height=20))
```

Plots points on a grid with axis labels at the extremes (min/max on both
axes — same "label the endpoints, not every tick" convention as
`line_chart`). Two points landing in the same cell just overwrite; for the
point counts this is built for (a few dozen at most — comparing competitors,
not plotting a full dataset) that's an honest simplification, not a bug to
chase. `scatter_with_trend` adds a least-squares fit line, computed and
drawn independently per column (reusing `line_chart`'s box-drawing
connector), with real data points drawn on top so they're never hidden by
the fit.

## Sizing

**The real, measured mobile ceiling:** loaded
a page's embedding CSS in headless Chrome at a 390px iPhone
viewport and binary-searched the break point directly (not estimated) —
a `<pre>` row overflows and starts horizontal-scrolling past **45
characters total** at the old CSS (15px font, 16px/18px padding), and the
skill's previous guidance ("~55–60 characters is fine") was simply wrong —
it had never been checked against an actual narrow viewport, only against
a desktop screenshot. A real bar chart (49 chars) and
range bar (57 chars) both failed this in practice: the range bar's dollar
value — the one number the chart existed to show — scrolled completely
off-screen at 390px with no visual hint anything was cut off.

Fixed two things together:
- **Embedding CSS tightened**: `font-size: 15px` → `13px`, `padding: 16px
  18px` → `12px 14px` (see Embedding section below) — raises the real
  ceiling from ~39 to ~45 characters at that viewport.
- **Bar-family default `width` dropped from 24 → 18** (`bar`, `range_bar`,
  `bullet`, `gap_bracket`, `star_histogram`) — a typical short
  label+value (`label_pad=3` + `value_pad=2` overhead) now lands total
  row width in the low-40s, leaving real margin under the 45-char ceiling
  instead of sitting exactly on top of it.

- Bar/range-bar/bullet/gap-bracket `width`: default is now 18 characters.
  **The real constraint is still total row width** (label + bar + value),
  not the bar width alone — long labels or long formatted values (e.g.
  `"$5,000-$10,000"` next to a label like `"Lifetime value (stays)"`) can
  push a row past the 45-char ceiling even with `width=18`. Caught this
  exact failure mode on a CAC-vs-LTV chart:
  shortened `"Lifetime value (stays)"` → `"Repeat patient"` and dropped
  `width` to fix it. **Keep total row width at or under ~42–44
  characters** — leave a few characters of margin below the measured
  45-char ceiling, since a platform's own web/app/email renderers
  may add their own container padding on top of what's tested here.
  If a label or value is long, shorten it or reduce `width` further —
  don't let the row grow past that. Star-histogram inherits this via its
  internal `bar()` call. Count actual characters
  (`len(rendered_row_string)`) rather than eyeballing it — that's how an
  overflow was missed the first time.
- Heatmap columns: one character per column with no separator, so a
  24-column hour grid is already ~24–30 characters wide including the row
  label — comfortably narrow. Don't add spacing between cells; it breaks
  the "grid" read the shade ramp depends on.
- Line/scatter `height`: 8–12 rows is usually enough resolution to show a
  trend without the block feeling long in the post.
- Pie/donut `radius`: 8–10 renders a diagram roughly 17–21 columns wide,
  36–42 columns tall including the legend — reasonable for a Substack code
  block; much larger risks the same mobile-wrapping problem as a wide bar.
- Venn defaults (`width=50, height=22`) are tuned to keep both circles (2-set)
  or the full triangular arrangement (3-set) legible without cramping the
  center overlap region — only override if a specific post's diagram looks
  cramped after rendering, and re-verify visually after changing.

Going noticeably wider/taller than these on any chart risks wrapping on
narrow screens — the one thing that actually breaks an ASCII chart
(misaligned columns/rows read as broken, not stylistic).

## Embedding

**In HTML:** a plain `<pre>` tag, with this rule in the page's `<style>` block:

```css
pre {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 13px;
  line-height: 1.5;
  background: #f6f6f4;
  border-radius: 4px;
  padding: 12px 14px;
  overflow-x: auto;
  white-space: pre;
}
```

(Tightened from 15px/16px 18px — the old sizing let a
45–55-character row overflow a 390px iPhone viewport; see Sizing above.)

HTML entities (`&ndash;`, `&mdash;`) still resolve correctly inside `<pre>` —
only whitespace/linebreaks are preserved literally, markup is still parsed.
For a Venn/pie/donut, print the diagram and legend as one `<pre>` block
(diagram, blank line, legend) so they paste as a single unit.

**In Markdown:** a fenced code block. **Into a newsletter editor:** open the HTML in a
browser, select all, copy, paste into the draft as one action, then preview on a phone.

## Common mistakes

| Mistake | Fix |
|---|---|
| Hand-aligning columns or hand-drawing circles/angles | Use `scripts/ascii_chart.py` — this math is easy to get subtly wrong by hand and only shows up as visible misalignment |
| Stretching a range bar past its real ceiling to "show" it could go higher | Use the `+` open-ended flag instead — bar length should never represent a number you don't have |
| Trying to color a segment for emphasis | Not available in plain text — carry the distinction in the character/label/legend text instead |
| Reusing the same pie/donut slice character on two adjacent slices | Don't hand-pick `SLICE_CHARS` order — the function already avoids this for typical slice counts; if you have 8+ slices, reconsider whether a pie is even the right chart |
| Passing separate width/height to size a pie or Venn "circle" | Pass `radius` (pie/donut) and let the function's built-in aspect correction do its job — hand-tuning width/height separately produces a flattened oval |
| Trying to label every x-axis tick on a line/scatter chart | Only the endpoints get labeled (`x_labels=(first, last)`) — put in-between context in the prose |
| Bar `width` (or line/scatter `height`) much larger than the Sizing guidance | Risks wrapping on mobile/narrow screens, which breaks alignment |
| Using a different `scale_max`/`width` for a `gap_bracket()` than the bars above it | The bracket's span is computed independently — mismatched scale makes it point at the wrong bar edges |
| Adding a second "target" or "benchmark" bar next to the measure in a bullet chart | That's not a bullet chart anymore — the whole point is one real bar plus a shaded band and a tick, not two bars |
| Spacing out heatmap cells or using plain space for the lowest shade level | Breaks the grid read — `heatmap()` already uses `·` (not space) for "quiet," don't override it |
| Long labels/values pushing a row's total width past ~44 characters | Clips silently off the right edge (`overflow-x: auto` scrolls, doesn't wrap) at a 390px mobile viewport, and a desktop screenshot won't show it — check total row width, not just `width=`, and shorten labels/values or reduce `width` |
| Building a Venn/pie/bar because the data has that shape, without asking if a reader needs a legend to parse it | Run the 2-second test above first — if a plain sentence states the fact as clearly, skip the chart |
| A single bar or range bar with no axis and no comparison point | Conveys nothing on its own — always pair with `render(..., axis=)` or a second row on the same scale, or drop the chart and say the number in prose |
