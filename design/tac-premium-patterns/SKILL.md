---
name: tac-premium-patterns
description: >-
  Catalog of paste-ready premium composition patterns that score 9-10/10 on the tac-ui-rubric. Use this skill when designing or building any user-facing surface — landing hero, KPI dashboard, data table, status timeline, scan card, drawer, command palette, empty state, error boundary. Each pattern is fully tokenized (Violet Grid v6), has an animation spec, defines its loading/empty/error states, and includes file:line precedents from the existing codebase. Trigger on "build a hero", "make this card premium", "design a KPI tile", "lay out this dashboard page", "polish this section", "I need a premium [X]".
---

# TAC Express — Premium Composition Patterns

> Each pattern below is a **full template** — markup, tokens, motion, and all four states (loaded / loading / empty / error). Paste, then adapt the data. These are the patterns that score 9-10 on `tac-ui-rubric`.

> **Read first:** `tac-ui-authoring`, `tac-design-tokens`. **Always close:** `tac-ui-rubric` against the result.

---

## Pattern Index

| Surface | Pattern |
|---|---|
| Hero | § 1 Marketing Display Hero · § 2 Mission-Control Hero |
| KPI | § 3 KPI Tile (single) · § 4 KPI Constellation (asymmetric grid) |
| Data | § 5 Mono Table · § 6 Status Timeline · § 7 Scan Result Card |
| Page Shell | § 8 Sector Header · § 9 PageShell with Toolbar |
| State | § 10 Empty State · § 11 Error Boundary · § 12 Stale-Data Banner |
| Surface | § 13 Drawer · § 14 Command Palette · § 15 Drop Notification |

---

## 1. Marketing Display Hero (apps/web)

```tsx
<section className="tac-hero-bleed relative bg-background">
  {/* Atmospheric layer — DO NOT remove, this is what makes it feel expensive */}
  <div aria-hidden className="absolute inset-0 tac-scanline pointer-events-none motion-reduce:hidden" />
  <div aria-hidden className="absolute inset-x-0 bottom-0 h-px bg-border" />

  <div className="container py-24 lg:py-32 grid grid-cols-12 gap-6">
    {/* Asymmetric — 7/5 not 6/6 — reads as engineered */}
    <div className="col-span-12 lg:col-span-7">
      <span className="t-overline text-primary animate-in fade-in-0 duration-slow">
        North-East Corridor · Logistics
      </span>
      <h1 className="t-display t-gradient-hero mt-6 dark:text-glow-primary
                     animate-in fade-in-0 slide-in-from-bottom-4 duration-slow delay-100">
        Move faster than the road.
      </h1>
      <p className="t-body mt-6 max-w-prose text-muted-foreground
                    animate-in fade-in-0 slide-in-from-bottom-3 duration-slow delay-200">
        Real-time tracking, predictive arrival, mission-grade ops.
      </p>
      <div className="mt-8 flex items-center gap-3
                      animate-in fade-in-0 slide-in-from-bottom-2 duration-slow delay-300">
        <Button size="lg" variant="default">Start tracking</Button>
        <Button size="lg" variant="outline">Watch demo</Button>
      </div>
    </div>

    {/* The 5/12 column carries data, not decoration */}
    <div className="col-span-12 lg:col-span-5 lg:col-start-9">
      <dl className="tac-fui-panel p-6 grid grid-cols-2 gap-4">
        {[
          { label: "On-time rate", value: "98.7%", tone: "success" },
          { label: "Lanes active", value: "47" },
          { label: "Avg transit", value: "2.4 days" },
          { label: "Hubs", value: "12" },
        ].map((stat) => (
          <div key={stat.label} className="border-l border-border pl-3">
            <dt className="tac-mono-label">{stat.label}</dt>
            <dd className={cn("t-data-sm mt-1",
              stat.tone === "success" && "t-gradient-success")}>{stat.value}</dd>
          </div>
        ))}
      </dl>
    </div>
  </div>
</section>
```

**Why it scores premium:** asymmetric 7/5 grid (not 6/6), hero gradient + glow on dark, staggered fade-in choreography, mission-control stat panel earning its space, scanline overlay (motion-reduce safe).

---

## 2. Mission-Control Hero (apps/dashboard)

```tsx
<section className="border-b border-border bg-card">
  <div className="container py-6 grid grid-cols-12 gap-4">
    <div className="col-span-12 lg:col-span-8">
      <div className="flex items-center gap-3">
        <span className="tac-mono-label">Sector · Active</span>
        <span aria-hidden className="size-2 bg-accent-success tac-blink motion-reduce:animate-none" />
      </div>
      <h1 className="t-h1 mt-2">North-East Corridor · DEL → BLR</h1>
      <p className="t-body-sm text-muted-foreground mt-1">
        12 hubs · 47 active lanes · last sync <span className="font-mono tabular-nums">14:23:08</span>
      </p>
    </div>

    <div className="col-span-12 lg:col-span-4 flex items-end justify-end gap-4">
      <KpiInline label="ON-TIME" value="98.7%" tone="success" />
      <KpiInline label="ALERTS"  value="3"     tone="warning" />
      <KpiInline label="DUE"     value="42"    tone="info" />
    </div>
  </div>
</section>
```

`KpiInline` = `<div className="border-l border-border pl-3"><dt className="tac-mono-label">{label}</dt><dd className="t-data-sm">{value}</dd></div>`

---

## 3. KPI Tile (single)

```tsx
<div data-slot="kpi-tile" className="tac-fui-panel tac-hover-lift p-5 flex flex-col gap-2">
  <header className="flex items-center justify-between">
    <span className="tac-mono-label">{label}</span>
    <RiArrowUpLine aria-hidden className="size-4 text-accent-success" />
  </header>
  <div className="t-data text-foreground">{value}</div>
  <footer className="flex items-baseline justify-between">
    <span className="t-caption text-muted-foreground">{period}</span>
    <span className="t-mono-sm text-accent-success">+{delta}</span>
  </footer>
</div>
```

**States:**
- **Loading**: replace inner with `<div className="animate-skeleton-pulse h-7 w-24 bg-muted" />`
- **Empty**: `value = "—"` (em-dash, mono-aligned)
- **Error**: border-l shifts to `border-l-accent-danger`, value reads `ERR`, footer shows error code

---

## 4. KPI Constellation (asymmetric)

```tsx
{/* 12-col asymmetric — 5/4/3 — reads as deliberate, not template */}
<div className="grid grid-cols-12 gap-4">
  <div className="col-span-12 lg:col-span-5"><KpiTile label="ACTIVE MANIFESTS" value={128} hero /></div>
  <div className="col-span-6  lg:col-span-4"><KpiTile label="ON-TIME RATE" value="98.7%" tone="success" /></div>
  <div className="col-span-6  lg:col-span-3"><KpiTile label="ALERTS" value={3} tone="warning" /></div>
</div>
```

The `hero` variant for the lead KPI makes its `t-data` 1.25× larger and adds a sparkline. Never use 4 equal-width KPI cards — that is the AI-slop default grid.

---

## 5. Mono Table (data list)

```tsx
<table className="w-full border-separate border-spacing-0">
  <thead>
    <tr className="border-b border-border">
      {["AWB", "Service", "Origin", "Destination", "Status", "ETA"].map((h, i) => (
        <th key={h} scope="col"
            className={cn("tac-mono-label text-left py-2 px-3",
              i === 0 && "border-l border-border")}>
          {h}
        </th>
      ))}
    </tr>
  </thead>
  <tbody>
    {rows.map((row) => (
      <tr key={row.id}
          className="group border-b border-border tac-fui-hover cursor-pointer">
        <td className="font-mono tabular-nums py-2 px-3 text-primary">{formatAWB(row.awb)}</td>
        <td className="t-body-sm py-2 px-3">{row.service}</td>
        <td className="font-mono text-xs py-2 px-3">{row.origin}</td>
        <td className="font-mono text-xs py-2 px-3">{row.destination}</td>
        <td className="py-2 px-3"><StatusBadge status={row.status} /></td>
        <td className="font-mono tabular-nums text-xs py-2 px-3 text-muted-foreground">{row.eta}</td>
      </tr>
    ))}
  </tbody>
</table>
```

**Skeleton:** map 8 ghost rows with `<td><div className="animate-skeleton-pulse h-4 bg-muted" /></td>`.
**Empty:** § 10 pattern. **Error:** § 11 pattern.

---

## 6. Status Timeline (vertical, brutalist)

```tsx
<ol className="relative pl-8">
  <div aria-hidden className="absolute left-2 top-2 bottom-2 w-px bg-border" />
  {events.map((e, i) => (
    <li key={e.id} className="relative pb-6 last:pb-0
                              animate-in fade-in-0 slide-in-from-left-2 duration-base"
        style={{ animationDelay: `${i * 60}ms` }}>
      <div aria-hidden
           className={cn("absolute -left-7 top-1.5 size-3 border border-border bg-card",
                         e.tone === "success" && "bg-accent-success border-accent-success",
                         e.tone === "danger"  && "bg-accent-danger  border-accent-danger")} />
      <div className="flex items-baseline justify-between gap-3">
        <span className="t-h4">{e.label}</span>
        <span className="t-mono-sm tabular-nums text-muted-foreground">{e.timestamp}</span>
      </div>
      {e.detail && <p className="t-body-sm text-muted-foreground mt-1">{e.detail}</p>}
    </li>
  ))}
</ol>
```

The square-not-circle dots and 1px line are the entire reason this reads as Violet Grid and not generic template.

---

## 7. Scan Result Card (mission-control immediate feedback)

```tsx
<div data-slot="scan-card"
     className={cn("border border-border bg-card p-4 grid grid-cols-12 gap-3",
                   "animate-in zoom-in-95 fade-in-0 duration-fast",
                   result.ok && "border-l-2 border-l-accent-success",
                   !result.ok && "border-l-2 border-l-accent-danger tac-hazard-stripes")}>
  <div className="col-span-2 flex items-center justify-center">
    {result.ok ? <RiCheckLine className="size-6 text-accent-success" />
               : <RiCloseLine  className="size-6 text-accent-danger" />}
  </div>
  <div className="col-span-7">
    <span className="tac-mono-label">AWB</span>
    <div className="font-mono tabular-nums tracking-pdf-awb text-lg mt-0.5">{formatAWB(result.awb)}</div>
    <div className="t-caption mt-1">{result.message}</div>
  </div>
  <div className="col-span-3 text-right">
    <span className="tac-mono-label">{result.timestamp}</span>
    <div className="t-mono-sm mt-0.5">{result.hub}</div>
  </div>
</div>
```

**Why premium:** uses `tac-hazard-stripes` only on error (not decoration), `tracking-pdf-awb` for the AWB, immediate zoom-in on scan event.

---

## 8. Sector Header (page-level)

```tsx
<header className="border-b border-border bg-card">
  <div className="container flex items-center justify-between py-3">
    <div className="flex items-center gap-3 min-w-0">
      <span className="tac-mono-label">SECTOR</span>
      <span className="font-mono text-sm tabular-nums truncate">DEL · BLR · BOM · MAA</span>
    </div>
    <span className="t-mono-sm text-muted-foreground tabular-nums">
      <time dateTime={now.toISOString()}>{format(now, "yyyy-MM-dd HH:mm:ss")}</time>
    </span>
  </div>
</header>
```

---

## 9. PageShell with Toolbar

```tsx
<PageShell width="page-content" spacing="dashboard">
  <PageHeader>
    <PageTitle>Shipments</PageTitle>
    <PageDescription>{count} active · {breached} breached</PageDescription>
    <PageActions>
      <Button variant="outline" size="sm"><RiFilterLine aria-hidden className="size-4" /> Filter</Button>
      <Button size="sm"><RiAddLine aria-hidden className="size-4" /> New shipment</Button>
    </PageActions>
  </PageHeader>
  <div className="grid grid-cols-12 gap-4 mt-6">
    {/* asymmetric — 8/4, never 9/3 (too narrow) or 6/6 (too even) */}
    <div className="col-span-12 lg:col-span-8">{/* table */}</div>
    <div className="col-span-12 lg:col-span-4">{/* filters / inspector */}</div>
  </div>
</PageShell>
```

---

## 10. Empty State (with intent)

```tsx
<div className="border border-dashed border-border bg-muted/30 py-16 px-8 flex flex-col items-center text-center gap-3">
  <RiInboxLine aria-hidden className="size-10 text-muted-foreground" />
  <div className="tac-mono-label">NO RECORDS</div>
  <h3 className="t-h3">No active shipments in this lane.</h3>
  <p className="t-body-sm text-muted-foreground max-w-prose">
    Shipments appear here within 30 seconds of dispatch. Last sync <span className="font-mono">14:23</span>.
  </p>
  <Button className="mt-2" size="sm" onClick={onCreate}>
    <RiAddLine aria-hidden className="size-4" /> Create shipment
  </Button>
</div>
```

The dashed border is the only place dashed is allowed — it telegraphs "this is a slot waiting to be filled".

---

## 11. Error Boundary

```tsx
<div role="alert" aria-live="assertive"
     className="border border-accent-danger/40 bg-card p-6 grid grid-cols-12 gap-4">
  <div className="col-span-1 pt-0.5">
    <RiErrorWarningLine aria-hidden className="size-6 text-accent-danger" />
  </div>
  <div className="col-span-11">
    <span className="tac-mono-label text-accent-danger">ERROR · {code}</span>
    <h3 className="t-h3 mt-1">Could not load shipments.</h3>
    <p className="t-body-sm text-muted-foreground mt-1">{message}</p>
    <div className="mt-4 flex items-center gap-2">
      <Button size="sm" variant="outline" onClick={retry}>Retry</Button>
      <Button size="sm" variant="ghost"   onClick={openLogs}>View logs</Button>
    </div>
  </div>
</div>
```

---

## 12. Stale-Data Banner (degraded but available)

```tsx
<div role="status" aria-live="polite"
     className="border-l-2 border-l-accent-warning bg-card px-4 py-2 flex items-center justify-between gap-3">
  <div className="flex items-center gap-3 min-w-0">
    <RiTimeLine aria-hidden className="size-4 text-accent-warning shrink-0" />
    <span className="t-body-sm">
      Showing data from <span className="font-mono tabular-nums">14:23:08</span> · Live feed reconnecting…
    </span>
  </div>
  <button onClick={refresh} className="tac-mono-label hover:text-primary transition-colors duration-fast ease-linear">
    REFRESH
  </button>
</div>
```

---

## 13. Drawer (right edge, sharp)

```tsx
<Sheet open={open} onOpenChange={setOpen}>
  <SheetContent side="right" className="w-[480px] sm:max-w-none border-l border-border">
    {/* duration-base, ease-smooth — branded but quick */}
    <SheetHeader className="border-b border-border pb-3">
      <span className="tac-mono-label">SHIPMENT</span>
      <SheetTitle className="t-h2 font-mono tabular-nums">{formatAWB(awb)}</SheetTitle>
    </SheetHeader>
    {/* ... */}
  </SheetContent>
</Sheet>
```

---

## 14. Command Palette

```tsx
<Command>
  <CommandInput placeholder="Type a command or search…" className="font-mono text-sm" />
  <CommandList>
    <CommandEmpty>No results.</CommandEmpty>
    <CommandGroup heading="JUMP TO" className="tac-mono-label">
      {/* heading uses tac-mono-label automatically via the Command primitive override */}
      <CommandItem><RiTruckLine /> Shipments <kbd className="ml-auto t-mono-sm">⌘ S</kbd></CommandItem>
    </CommandGroup>
  </CommandList>
</Command>
```

---

## 15. Drop Notification (toast)

```tsx
<Toaster
  toastOptions={{
    className: "border border-border bg-card !rounded-none shadow-md",
    /* shadow-md = 6px brutalist offset */
    duration: 4000,
  }}
/>
```

Variant tones via `border-l-2 border-l-accent-{success,warning,danger}`. No icons floating freely — anchor them in the left rail.

---

## Pre-Flight Before Shipping a Premium Surface

```
[ ] Ran tac-ui-rubric — score ≥ 90 / 100
[ ] All 4 states designed (loaded / loading / empty / error)
[ ] Asymmetric grid where applicable (avoid 4-equal, 6/6, 3-equal)
[ ] motion-reduce variant tested for any tac-blink / tac-scanline use
[ ] No raw [px] arbitrary values
[ ] Used at least one FUI signature: tac-mono-label, tac-fui-panel, tac-hover-lift, tac-signal-glow,
    or one of the .t-gradient-* / .text-glow-primary on hero
[ ] Cross-checked with tac-accessibility (focus order, aria-live for state changes)
```
