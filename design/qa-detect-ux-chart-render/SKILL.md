---
name: qa-detect-ux-chart-render
section: visual
description: "Detects broken chart rendering — chart container has scaffolding (axes, gridlines, legend) but no actual data marks (no bars, lines, points); orphan tooltips floating with no data point beneath them; chart canvas mostly empty pixels (>90% background). Catches the 'chart loaded but shows nothing' bug class (your Fees & Expenses screenshot)."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
requires: [hasCharts, hasProgressBars, hasGauges]
---

## What it catches — 4 issue types

| issueType | severity | What |
|---|---|---|
| `chartEmptyNoData` | high | Chart container (Recharts/ApexCharts/Chart.js/ECharts/Highcharts/D3) has axes, gridlines, and legend rendered but ZERO data shapes (no `<path d="M…L…">`, no `<rect>` bars, no `<circle>` markers, no canvas pixel variance) |
| `chartTooltipOrphan` | medium | A chart tooltip / hover popover is visibly rendered with no data point beneath its arrow / no active marker — leaks UI state (your Fees & Expenses "Nov" floating gray box) |
| `chartAxisLabelsButNoMarks` | medium | Chart has visible Y-axis numbers (e.g. "1, 1.5, 2") but the plot area has no rendered data marks in those rows |
| `chartLegendButNoSeries` | low | Legend lists series ("Fees", "Expenses") but the chart contains no `<path>` / `<g class*="series">` matching those names — data series silently absent |

## Probe (browser_evaluate)

```js
() => {
  const sel = el => {
    const id = el.id ? '#' + el.id : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const bb = el => {
    const r = el.getBoundingClientRect();
    return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) };
  };
  const visible = el => {
    if (!el || el.nodeType !== 1) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const out = [];

  // Find chart containers — common libraries first, then generic
  const chartSelectors = [
    '.recharts-wrapper', '.recharts-surface',
    '.apexcharts-canvas', '[id^="apexcharts"]',
    'canvas.chartjs-render-monitor', 'canvas[class*="chart"]',
    '.echarts-for-react', '[_echarts_instance_]',
    '.highcharts-container',
    'svg.chart, svg[class*="chart"]',
    '[class*="chart-container"]', '[class*="chartContainer"]',
    '[class*="line-chart"]', '[class*="bar-chart"]', '[class*="pie-chart"]', '[class*="area-chart"]'
  ];
  const seen = new Set();
  const charts = [];
  for (const s of chartSelectors) {
    for (const el of document.querySelectorAll(s)) {
      if (seen.has(el)) continue;
      // Skip nested matches — only keep outermost
      if ([...seen].some(o => o.contains(el))) continue;
      seen.add(el);
      if (visible(el) && el.getBoundingClientRect().width >= 120) charts.push(el);
    }
  }

  if (charts.length === 0) return out;

  let emptyFlagged = 0;
  let orphanFlagged = 0;
  let axisOnlyFlagged = 0;
  let legendOnlyFlagged = 0;

  for (const chart of charts) {
    if (emptyFlagged >= 3 && orphanFlagged >= 2 && axisOnlyFlagged >= 2 && legendOnlyFlagged >= 2) break;
    const cr = chart.getBoundingClientRect();

    // ── 1. chartEmptyNoData — count data marks vs scaffolding ─────────
    // Data marks: <path d="..."> in plot area, <rect> bars, <circle> with r>1.5
    // Scaffolding: axis lines, gridlines, legend text, axis text, ticks
    //
    // IMPORTANT: smooth/curved line charts (Recharts default, Chart.js, ApexCharts)
    // emit paths using cubic-bezier (C), quadratic-bezier (Q), and smooth shorthand
    // (S, T) commands, NOT just M+L. Count ALL drawing operators to avoid false
    // "chart empty" findings on curved-line charts.
    const allPaths = chart.querySelectorAll('path');
    let dataPathCount = 0;
    for (const p of allPaths) {
      const cls = (p.getAttribute('class') || '').toLowerCase();
      const d = (p.getAttribute('d') || '');
      // Skip explicit grid/axis/tick paths
      if (/grid|axis|tick|cartesian|baseline|domain/.test(cls)) continue;
      // Count ALL path drawing commands: M/L/H/V/C/S/Q/T/A (move, line, curve, arc)
      // — a line chart curve like "M65,242C110,242,...C155,232,..." has 1 M + N C commands.
      const segCount = (d.match(/[MLHVCSQTA]/gi) || []).length;
      if (segCount >= 3 && d.length >= 8) dataPathCount++;
    }
    const allRects = chart.querySelectorAll('rect');
    let dataRectCount = 0;
    for (const r of allRects) {
      const cls = (r.getAttribute('class') || '').toLowerCase();
      if (/grid|axis|background|brush|panel|tooltip/.test(cls)) continue;
      const w = parseFloat(r.getAttribute('width')) || 0;
      const h = parseFloat(r.getAttribute('height')) || 0;
      // Bar marks are usually width<100 and height>3, NOT spanning the whole chart
      if (w > 0 && h > 3 && w < cr.width * 0.5 && h < cr.height * 0.95) dataRectCount++;
    }
    const allCircles = chart.querySelectorAll('circle');
    let dataCircleCount = 0;
    for (const c of allCircles) {
      const r = parseFloat(c.getAttribute('r')) || 0;
      if (r > 1.5 && r < 30) dataCircleCount++;
    }
    const dataMarks = dataPathCount + dataRectCount + dataCircleCount;

    // Detect scaffolding presence
    const hasAxis = !!chart.querySelector('[class*="axis"], [class*="Axis"], g.tick, .recharts-cartesian-axis, .apexcharts-yaxis, .apexcharts-xaxis, .echarts-axis');
    const hasGrid = !!chart.querySelector('[class*="grid"], [class*="Grid"], .recharts-cartesian-grid, .apexcharts-gridline, .echarts-grid, line[stroke-dasharray]');
    const axisTextEls = [...chart.querySelectorAll('text, tspan, [class*="axis-label"], [class*="axisLabel"]')]
      .filter(visible)
      .filter(el => (el.textContent || '').trim().length > 0);
    const hasAxisText = axisTextEls.length >= 2;

    if (dataMarks === 0 && (hasAxis || hasGrid || hasAxisText) && emptyFlagged < 3) {
      emptyFlagged++;
      out.push({
        issueType: 'chartEmptyNoData', severity: 'high',
        selector: sel(chart), bbox: bb(chart),
        description: `Chart ${cr.width.toFixed(0)}×${cr.height.toFixed(0)}px has scaffolding (${hasAxis ? 'axis ' : ''}${hasGrid ? 'gridlines ' : ''}${hasAxisText ? `${axisTextEls.length} axis labels` : ''}) but ZERO data marks (no data paths/bars/points). Chart loaded into the DOM but data is empty or failed to render. Show an explicit empty-state message ("No data for this period") instead of an empty chart skeleton.`
      });
      continue;
    }

    // ── 3. chartAxisLabelsButNoMarks — axis labels present, plot area empty ──
    if (dataMarks === 0 && hasAxisText && axisTextEls.length >= 3 && axisOnlyFlagged < 2) {
      const labels = axisTextEls.slice(0, 4).map(e => (e.textContent || '').trim()).filter(Boolean);
      axisOnlyFlagged++;
      out.push({
        issueType: 'chartAxisLabelsButNoMarks', severity: 'medium',
        selector: sel(chart), bbox: bb(chart),
        description: `Chart shows axis labels (${labels.slice(0, 3).join(', ')}) but the plot area is blank. Either the data is missing or the rendering pipeline failed silently.`
      });
    }

    // ── 4. chartLegendButNoSeries — legend lists series but no <path>/<g> for them ──
    const legendItems = [...chart.querySelectorAll('[class*="legend"] text, [class*="legend"] span, [class*="Legend"] text, [class*="Legend"] span, .apexcharts-legend-text')]
      .filter(visible)
      .map(e => (e.textContent || '').trim())
      .filter(t => t.length > 0 && t.length < 40);
    if (dataMarks === 0 && legendItems.length >= 1 && legendOnlyFlagged < 2) {
      legendOnlyFlagged++;
      out.push({
        issueType: 'chartLegendButNoSeries', severity: 'low',
        selector: sel(chart), bbox: bb(chart),
        description: `Legend lists series (${legendItems.slice(0, 3).join(', ')}) but no data series are rendered in the chart. Either hide the legend when data is empty or show an empty state.`
      });
    }
  }

  // ── 2. chartTooltipOrphan — visible tooltip with no active marker beneath ───
  const tooltipSelectors = '[class*="tooltip"], [role="tooltip"], .recharts-tooltip-wrapper, .apexcharts-tooltip, .echarts-tooltip';
  const tips = [...document.querySelectorAll(tooltipSelectors)].filter(visible);
  for (const tip of tips) {
    if (orphanFlagged >= 2) break;
    const tr = tip.getBoundingClientRect();
    if (tr.width < 20 || tr.height < 12) continue;
    // Find the chart this tooltip belongs to
    const chart = charts.find(c => {
      const cr = c.getBoundingClientRect();
      // Tooltip overlaps the chart's bounding region
      return tr.left < cr.right + 100 && tr.right > cr.left - 100 &&
             tr.top < cr.bottom + 100 && tr.bottom > cr.top - 100;
    });
    if (!chart) continue;
    // Is there an "active" marker inside the chart? (Recharts uses .recharts-active-dot; ApexCharts marks active series)
    const activeMarker = chart.querySelector(
      '.recharts-active-dot, .recharts-tooltip-cursor, ' +
      '.apexcharts-tooltip-marker.apexcharts-active, .apexcharts-active-marker, ' +
      'circle[r="6"], circle[r="8"], [class*="active-dot"], [class*="activeDot"]'
    );
    if (activeMarker && visible(activeMarker)) continue;
    // No active marker — tooltip is orphan
    orphanFlagged++;
    out.push({
      issueType: 'chartTooltipOrphan', severity: 'medium',
      selector: sel(tip), bbox: bb(tip),
      description: `Chart tooltip "${(tip.innerText || '').trim().slice(0, 30)}" is visible at (${Math.round(tr.left)}, ${Math.round(tr.top)}) with no active data marker beneath it. Tooltip should hide when no hover target exists. Likely a leftover state from initial render or chart re-render.`
    });
  }

  return out;
}
```

## Notes

- Self-skips: pages with no chart containers return [] immediately
- Bounded: max 3 empty + 2 orphan + 2 axisOnly + 2 legendOnly = ~9 findings per cell
- Covers Recharts, ApexCharts, Chart.js (canvas), ECharts, Highcharts, and generic SVG charts
- The `chartEmptyNoData` check is the highest-value: catches the "chart skeleton with no data" pattern (your Fees & Expenses screenshot)
- For canvas-based charts (Chart.js), the probe can't see pixels; we infer empty by absence of data-driven inline styles and by chart wrappers that haven't injected `<canvas>` with width/height
