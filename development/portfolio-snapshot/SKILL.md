---
name: portfolio-snapshot
description: Export/publish the live portfolio tracker as a static, stripped snapshot into the "Portfolio Snapshot" folder — an empty Trades section (first), the holdings table, and the 1-month-return bar chart baked to static SVG (scatter chart opt-in), with a Publish_Snapshot property. Strips all instruction/engine/log elements (refresh dataviewjs, tip callouts, Upcoming Earnings, Column Legend, Notes, Log). Use when the user says "snapshot the portfolio", "publish the portfolio", "export Live Portfolio", or "portfolio snapshot".
model: sonnet
effort: low
allowed-tools: Read Glob Bash(python3 * date * ls * mkdir * find * cat * head * wc *)
---

Export the live portfolio tracker (`Live Portfolio.md`) as a **static, publishable snapshot** in the `Portfolio Snapshot/` folder. The snapshot keeps only the deliverable content; every instruction/engine/log element is stripped.

**This is a mechanical/export skill — NOT investment analysis.** It produces no conviction or status judgement, so it is in the same load tier as `/numbers`, `/graph`, `/clean`: **do NOT read the `/Mental Models` folder.**

**Engine**: `.claude/skills/portfolio-snapshot/build_snapshot.py` (deterministic, pure stdlib). It parses the Holdings table, bakes the bar chart to SVG by porting the exact math in the tracker's `dataviewjs` block (90th-percentile cap; diverging-from-center bars sorted high→low), assembles the note, and writes the files directly. Following the `/graph` pattern, the large SVG never streams through a model response.

## What the snapshot contains (the contract)

Section order is **Trades first**, then Holdings, then Charts.

| Kept | Dropped (instruction / engine / log) |
|---|---|
| `## Trades` (empty, **FIRST** — for the user to fill in) | `[]()` stub, `> [!tip] How this works` |
| `## Holdings` table (verbatim, markers stripped) | the FMP-refresh `dataviewjs` engine block |
| `## Charts` → **one** static SVG embed: the 1-month-return bar (scatter opt-in) | both chart `> [!tip]` callouts + their `dataviewjs` code |
| Frontmatter: `Publish_Snapshot: true` + provenance | `## Upcoming Earnings`, `## Column Legend`, `## Notes`, `## Log` |

- **`Publish_Snapshot: true`** leads the frontmatter — a YAML boolean renders as a ticked ("filled") checkbox property in Obsidian. Also carries `date`, `snapshot_of: "[[Live Portfolio]]"`, `tags: [portfolio, snapshot]`, `status: active`.
- **Charts are baked from the CURRENT Holdings table** — click Refresh in the live tracker first if you want fresh numbers.
- **Default chart: the `Return 1M` bar only.** The scatter is **omitted by default**; pass `--scatter` to also emit it (defaults `Rev Gr CFY` x vs `EV/EBIT NTM` y). Re-running without `--scatter` deletes any stale scatter asset from an earlier run of the same snapshot.
- **SVGs are theme-independent** (white card, baked hex colors — CSS variables would not resolve in a static export) and preserve `<title>` hover tooltips.

## Naming

- **Default mode `dated`**: files are named by date in **DD-MM-YYYY** form — `Portfolio Snapshot/04-08-2026.md`, plus `04-08-2026 - bar.svg` (and `- scatter.svg` only when `--scatter`). Re-running on the same day overwrites that day's files (idempotent per day); different days accumulate an archive.
- **Mode `single`** (`--mode single`): writes `Portfolio Snapshot.md` + `Portfolio Snapshot - bar.svg`, overwritten every run (no history).

## Step 0: Pre-flight

Lock posture is **read-only** (per `.claude/skills/_shared/preflight.md`): this skill reads only `Live Portfolio.md` (no analytical skill writes it) and writes only into the isolated `Portfolio Snapshot/` folder (no other skill touches it), so the contention surface is nil and no vault lock is taken. Still verify:

1. **Source exists** — `Live Portfolio.md` at vault root. Abort if missing.
2. **Table markers present** (section-existence probe) — `<!--TABLE-START-->` / `<!--TABLE-END-->`. The engine aborts loudly if absent; do not fabricate a table.

```bash
test -f "Live Portfolio.md" && grep -q "TABLE-START" "Live Portfolio.md" \
  && echo "PREFLIGHT_OK" || echo "PREFLIGHT_FAIL"
```

## Step 1: Generate

Pass today's date explicitly so the filename tracks the vault clock (do not rely on the machine clock):

```bash
python3 ".claude/skills/portfolio-snapshot/build_snapshot.py" \
  --date "$(date +%F)" --time "$(date +%H:%M)"
```

Default output is the `Return 1M` bar only. Optional overrides: `--bar-metric "Return 3M"` (any key in the script's `BAR_METRICS`: Returns 1W/1M/3M/1Y, P/E, EV/EBIT, Rev/EPS growth), `--scatter` to also emit the scatter (with `--scatter-x` / `--scatter-y`), `--mode single`.

## Step 2: Verify & report

The script prints a summary (rows parsed, chart metric, output paths). Confirm `holdings rows` matches the live table and the files exist, then report to the user — link the note as a wikilink (e.g. `[[Portfolio Snapshot/04-08-2026.md]]`) and name each SVG asset. Per CLAUDE.md Rule #8, list every file written.

## Safety

- **Read-only on the source** — never modifies `Live Portfolio.md` (its refresh `dataviewjs` and Log stay intact).
- **Never** creates content at vault root; all output lands in `Portfolio Snapshot/`.
- **Archive, don't delete** — old dated snapshots accumulate; removing them is the user's call (or a future `/clean`-style sweep), never automatic here. (The one exception is a same-date stale `- scatter.svg` when scatter is toggled off — that orphan is removed so the folder stays consistent with the note.)
- The `Publish_Snapshot` flag is distinct from the `publish: true` website-sync flag used by Theses/Sectors/Macro — this skill does not touch that pipeline.
