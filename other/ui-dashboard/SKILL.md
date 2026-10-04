---
name: ui-dashboard
description: Compose a full dashboard layout from a data schema — KPI cards, charts, data tables, filters. AUTO-TRIGGERS when
  user asks for "dashboard", "admin panel", "monitoring dashboard", "analytics view", "KPIs", "Übersichts-Seite", "Statistiken
  anzeigen", "metrics view", or wants to visualize metrics from a data source.
version: 1.0.0
author: Yuno (Hermes Agent) — based on KIMI K2 UI-Factory-Pattern 2026-06-30
license: MIT
metadata:
  hermes:
    tags:
    - ui
    - dashboard
    - kpi
    - charts
    - data-visualization
    - monitoring
    - admin-panel
    - analytics
    related_skills:
    - ui-design-system
    - ui-component-library
    - ui-color-system
    - ui-data-table
    - ui-chart-builder
    - ui-factory
    part_of: ui-factory
    triggers:
    - dashboard
    - admin panel
    - monitoring dashboard
    - analytics view
    - KPIs
    - Übersichts-Seite
    - Statistiken anzeigen
    - metrics view
    - Admin-Page
    - Übersicht
    - Stats
    - Monitoring-View
    - visualize metrics
lane: worker-vision
reasoning_effort: xhigh
---
## 🚨 AUTO-TRIGGER

Dieser Skill triggert **automatisch** wenn the user's Input nach Dashboard/Data-Visualization fragt. Auch ohne expliziten Aufruf — wenn die Trigger-Phrasen matchen, wird dieser Skill geladen.

**Trigger-Keywords (deutsch + englisch):** dashboard, admin panel, monitoring, analytics, KPI, Übersicht, Statistik, Stats, metrics, visualize, data view, Monitoring-View, charts, graph, Auswertung, Übersichts-Seite

Wenn the user nach **mehreren UI-Aspekten** fragt (z.B. "komplettes UI mit Dashboard + Components + Tokens"), wird stattdessen `ui-factory` getriggert (orchestriert die ganze Chain).

# ui-dashboard

> **Atom:** Composes a complete dashboard layout (KPI cards, charts, tables, filters) from a data schema. The "molecule" that combines all UI atoms into a working view.

## When to use

- User asks for a "dashboard", "admin panel", "monitoring UI"
- Want to visualize metrics (users, revenue, errors, latency)
- Need a real-time data view with filters and date-range
- Combining multiple data sources into one cohesive view

## Inputs

```yaml
data_schema:
  metrics:
    - name: "users"
      type: "count"  # count | sum | avg | custom
      source: "users table"
      format: "number"  # number | currency | percent | duration
    - name: "revenue"
      type: "sum"
      source: "orders.amount"
      format: "currency:USD"
      trend: "vs_last_week"
  charts:
    - name: "revenue_trend"
      type: "line"  # line | bar | area | pie | scatter
      x_axis: "date"
      y_axis: "revenue"
      period: "30d"
    - name: "users_by_plan"
      type: "pie"
      dimensions: ["plan", "user_count"]
  tables:
    - name: "recent_errors"
      columns: ["timestamp", "endpoint", "error_code", "message"]
      sortable: true
      filterable: true
      pagination: 20

filters:
  date_range: "last_30_days | last_7_days | custom"
  custom_filters: ["plan_type", "region", "user_role"]

framework: "react | vue | svelte | vanilla-html"
chart_lib: "recharts | chart.js | d3 | apexcharts"
```

## Output

**Single-file dashboard** with:
- Header (title, date-range picker, user-menu)
- KPI grid (4-6 cards)
- Charts row (1-2 charts)
- Data table (recent events/logs/errors)
- Sidebar (filters, navigation)
- Responsive layout (mobile: stack, desktop: grid)

## Workflow

### Step 1: Layout-Planning (2 min)

Standard dashboard grid:
```
┌─────────────────────────────────────────────────────────┐
│  HEADER (logo, title, date-range, user-menu)            │
├──────────┬──────────────────────────────────────────────┤
│          │  KPI 1    KPI 2    KPI 3    KPI 4           │
│  SIDEBAR ├──────────────────────────────────────────────┤
│  (filters│  Chart 1 (large)        │  Chart 2         │
│  + nav)  │                         │  (side panel)    │
│          ├──────────────────────────────────────────────┤
│          │  Data Table (recent events, paginated)       │
└──────────┴──────────────────────────────────────────────┘
```

**Responsive behavior:**
- **Desktop (≥1024px):** 4-column KPI grid, 2-column charts, sidebar visible
- **Tablet (768-1023px):** 2-column KPI grid, 1-column charts, sidebar collapsible
- **Mobile (<768px):** 1-column stack, sidebar = drawer, KPI cards = scrollable row

### Step 2: Component-Loading (1 min)

Use `ui-component-library` outputs:
- `<KpiCard>` from components
- `<Chart>` (recharts/chart.js adapter)
- `<DataTable>` from ui-data-table
- `<FilterPanel>` for sidebar
- `<DateRangePicker>` from ui-form-builder

### Step 3: KPI-Cards (3-5 min)

```tsx
// KpiCard.tsx
import { Card, Badge } from '@/components/ui';
import { ArrowUp, ArrowDown } from '@/icons';

interface KpiCardProps {
  label: string;
  value: string | number;
  trend?: {
    direction: 'up' | 'down' | 'flat';
    value: string; // "+12.5%"
    isPositive?: boolean; // override (e.g., error count going up is bad)
  };
  sparklineData?: number[];
}

export const KpiCard = ({ label, value, trend, sparklineData }: KpiCardProps) => {
  const trendColor = trend?.isPositive === false ? 'error' : 
                     trend?.direction === 'up' ? 'success' : 
                     trend?.direction === 'down' ? 'error' : 'neutral';
  
  return (
    <Card padding="lg">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{value}</div>
      {trend && (
        <div className={`kpi-trend trend-${trendColor}`}>
          {trend.direction === 'up' && <ArrowUp />}
          {trend.direction === 'down' && <ArrowDown />}
          <span>{trend.value}</span>
        </div>
      )}
      {sparklineData && <Sparkline data={sparklineData} />}
    </Card>
  );
};
```

### Step 4: Charts (5-10 min)

```tsx
// RevenueChart.tsx (recharts example)
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { color } from '@/tokens';

interface RevenueChartProps {
  data: Array<{ date: string; revenue: number }>;
}

export const RevenueChart = ({ data }: RevenueChartProps) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke={color.neutral[200]} />
        <XAxis dataKey="date" stroke={color.neutral[500]} />
        <YAxis stroke={color.neutral[500]} />
        <Tooltip 
          contentStyle={{ 
            backgroundColor: color.neutral[900],
            border: 'none',
            borderRadius: '0.5rem',
            color: color.neutral[50]
          }} 
        />
        <Line 
          type="monotone" 
          dataKey="revenue" 
          stroke={color.primary[500]} 
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 6, fill: color.primary[500] }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};
```

### Step 5: Data-Table (3-5 min)

Use `ui-data-table` skill for sortable/filterable/paginated tables:
```tsx
<RecentErrorsTable
  columns={[
    { key: 'timestamp', label: 'Time', sortable: true, format: 'datetime' },
    { key: 'endpoint', label: 'Endpoint', filterable: true },
    { key: 'error_code', label: 'Code', sortable: true, align: 'right' },
    { key: 'message', label: 'Message', truncate: 80 },
  ]}
  pageSize={20}
  onRowClick={(row) => openErrorDetails(row.id)}
/>
```

### Step 6: Filters + Sidebar (3-5 min)

```tsx
// FilterPanel.tsx
export const FilterPanel = ({ filters, onChange }) => {
  return (
    <aside className="filter-panel" aria-label="Filters">
      <h2>Filters</h2>
      <FilterGroup title="Date Range">
        <RadioGroup value={filters.dateRange} onChange={(v) => onChange({ ...filters, dateRange: v })}>
          <Radio value="7d">Last 7 days</Radio>
          <Radio value="30d">Last 30 days</Radio>
          <Radio value="90d">Last 90 days</Radio>
          <Radio value="custom">Custom range</Radio>
        </RadioGroup>
      </FilterGroup>
      <FilterGroup title="Plan">
        <MultiSelect
          options={['Free', 'Pro', 'Enterprise']}
          value={filters.plans}
          onChange={(v) => onChange({ ...filters, plans: v })}
        />
      </FilterGroup>
      <FilterGroup title="Region">
        <MultiSelect
          options={['US', 'EU', 'APAC']}
          value={filters.regions}
          onChange={(v) => onChange({ ...filters, regions: v })}
        />
      </FilterGroup>
    </aside>
  );
};
```

### Step 7: Empty-States + Loading (2 min)

Every dashboard section needs:
- **Loading state:** Skeleton placeholder (shimmer animation)
- **Empty state:** Illustration + helpful message + CTA
- **Error state:** Red banner + retry button + error details

```tsx
{loading && <KpiCardSkeleton />}
{!loading && data.length === 0 && <EmptyState 
  title="No data for this period"
  description="Try a different date range or check your filters"
  action={<Button onClick={resetFilters}>Reset filters</Button>}
/>}
{error && <ErrorBanner error={error} onRetry={refetch} />}
```

### Step 8: Live-Data-Integration (optional, 5-10 min)

Für **Live-Dashboards mit echten Daten** gibt es zwei Patterns:

#### Pattern A: SSE/WebSocket (React/Svelte)
```tsx
useEffect(() => {
  const eventSource = new EventSource('/api/metrics/stream');
  eventSource.addEventListener('update', (e) => {
    const update = JSON.parse(e.data);
    setLiveData(prev => [...prev.slice(-29), update]);
  });
  return () => eventSource.close();
}, []);
```

#### Pattern B: Python Data-Provider + fetch-Polling (Vanilla HTML)

Wenn das Dashboard als **static HTML** läuft aber echte Daten braucht (z.B. Hermes-Stats, System-Metriken):

**Architektur:**
```
Browser (live.html)
  ├── fetch() alle 10s → localhost:PORT/api/data
  │                          ↑
  │                    server.py (Python HTTPServer)
  │                     ├── subprocess → CLI-Befehle (hermes skills list, etc.)
  │                     ├── urllib → API-Endpoints (z.B. /api/status)
  │                     ├── psutil → System-Stats (CPU, RAM, Disk, Temp)
  │                     └── File-Scans (Memory-Files, Session-DBs)
```

**Schritte:**
1. **Data-Provider `server.py`** schreiben (siehe `references/live-data-provider-pattern.md`)
2. **Client-side `fetch()`** mit 10s Polling-Interval
3. **Auto-Refresh-Indicator** (Progress-Bar oben die sich über 10s füllt)
4. **Error-Banner** wenn Server nicht erreichbar
5. **Loading-States** (skeleton-shimmer bei ersten Load)
6. **Start-Skript** (`start.sh`) das Data-Provider + HTML-Server + Browser-Open kombiniert

**Key Insight — Hermes API-Surface (2026-07-01):**
- `/api/status` ist der **einzige no-auth Endpoint** — liefert Version, Gateway-State, Platforms, Active-Sessions
- Alle anderen `/api/*` Endpoints geben **HTTP 401 ohne Auth-Token**
- Für Skills/Profiles/Cron-Daten → `hermes` CLI via `subprocess` nutzen (braucht keinen Token)
- Für System-Stats → `psutil` (Python-Library, kein Auth nötig)
- **Caching** wichtig: CLI-Output alle 30-60s cachen, nicht bei jedem Request neu ausführen

**Template:** `templates/live-data-server.py` — fertiger Python-Server für Hermes-Stats

### Step 9: Interactive Accordion-Cards + KPI-as-Buttons (v3-Pattern, 2026-07-01)

User-Präferenz (explizit geäußert): **"alle tabs sollen anklickbar sein wo sich ein untermenü mit details die dazu passen es soll richtig übersichtlich sein"** — Dashboards sollen nicht alle Details sofort zeigen, sondern **Progressive Disclosure** nutzen: kompakte KPIs oben, klickbare Cards die aufklappen.

#### Accordion-Card Pattern

Jede Card ist ein `<article class="card">` mit:
- **`.card-header`** = klickbar (`role="button"`, `tabindex="0"`, `aria-expanded`)
- **`.card-body`** = `max-height: 0` → beim Aufklappen `max-height: 2000px` mit CSS-Transition
- **`.card-chevron`** = ▼ das sich um 180° dreht beim Aufklappen

```css
.card-body { max-height: 0; overflow: hidden; transition: max-height 0.3s ease; }
.card.expanded .card-body { max-height: 2000px; transition: max-height 0.5s ease; }
.card-chevron { transition: transform 0.3s ease; }
.card.expanded .card-chevron { transform: rotate(180deg); }
```

```javascript
// Toggle beim Klick oder Enter/Space
document.querySelectorAll('.card-header').forEach(header => {
    const toggle = () => {
        const card = header.closest('.card');
        const expanded = card.classList.toggle('expanded');
        header.setAttribute('aria-expanded', expanded);
    };
    header.addEventListener('click', (e) => { e.stopPropagation(); toggle(); });
    header.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
});
```

#### KPI-as-Button Pattern (KPI-Cards die Details öffnen)

KPI-Cards oben (die kleinen Übersichts-Karten) sind **klickbar** und öffnen die zugehörige Detail-Card:

```html
<article class="kpi-card" data-target="card-system" tabindex="0" role="button">
  <div class="kpi-label">RAM</div>
  <div class="kpi-value" id="kpi-ram">9.8 / 15.3 GB</div>
</article>
<!-- ... später im Dokument ... -->
<article class="card" id="card-system">...</article>
```

```javascript
// KPI-Klick → öffnet zugehörige Card + scrollt dorthin
document.querySelectorAll('.kpi-card[data-target]').forEach(kpi => {
    kpi.addEventListener('click', () => {
        const target = document.getElementById(kpi.dataset.target);
        if (target) {
            target.classList.add('expanded');
            target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    });
});
```

#### "Alle auf/zu" Keyboard Shortcut (Ctrl+A)

```javascript
// Ctrl+A klappt alle Cards gleichzeitig auf oder zu
if ((e.ctrlKey || e.metaKey) && e.key === 'a') {
    const cards = document.querySelectorAll('.card');
    const anyCollapsed = [...cards].some(c => !c.classList.contains('expanded'));
    cards.forEach(c => c.classList.toggle('expanded', anyCollapsed));
}
```

#### Mini-Tiles (Detail-Summary in aufgeklappter Card)

Jede aufgeklappte Card enthält am Ende eine **Mini-Tile-Row** mit großen Zahlen:

```html
<div class="detail-section">
  <div class="detail-title">⚡ Quick Stats</div>
  <div class="mini-chart">
    <div class="mini-tile"><div class="mini-tile-value">1</div><div class="mini-tile-label">Sessions</div></div>
    <div class="mini-tile"><div class="mini-tile-value">0</div><div class="mini-tile-label">Agents</div></div>
  </div>
</div>
```

#### Refresh-Rate Empfehlung

| Use Case | Refresh | Begründung |
|----------|---------|------------|
| **System-Monitoring** (CPU/RAM/Disk) | **3s** | User will sehen wie Last sich verändert — the user's Explizit-Wunsch |
| **Hermes-Agent-Status** | 3-5s | Sessions/Agents ändern sich schnell |
| **SaaS-Production-Dashboard** | 10-30s | Metrics ändern sich selten, Server-Last minimieren |
| **Statisches Show-Dashboard** | kein Auto-Refresh | Demo, keine Live-Daten |

**the user's Präferenz:** 3 Sekunden. Die Progress-Bar füllt sich in 2.8s und resettet beim nächsten fetch.

## Validation Checklist

- [ ] Layout responsive (mobile/tablet/desktop)
- [ ] All KPI cards have trend indicators
- [ ] All charts have hover-tooltip with formatted values
- [ ] All tables have sort + filter + pagination
- [ ] All filters actually filter (no dead controls)
- [ ] Loading + Empty + Error states for every section
- [ ] Date-range picker works with timezone handling
- [ ] Real-time updates don't break UI (cleanup on unmount)
- [ ] Color-coded trends (success/error) accessible to color-blind users (icon + text)
- [ ] Mobile: chart axes readable, tables scroll horizontally
- [ ] **Accordion-Cards sind keyboard-accessible** (Tab + Enter/Space)
- [ ] **KPI-Cards sind klickbar** und öffnen zugehörige Detail-Card
- [ ] **`aria-expanded`** korrekt gesetzt bei Accordion-Toggle
- [ ] **Color-coded bars** (grün <70%, gelb 70-90%, rot >90%)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Showing too many KPIs (>6) | Limit to 4-6 most important metrics |
| Charts with arbitrary y-axis scale | Always start at 0 for bar/area, log-scale for exponential |
| Tables without pagination | Always paginate (default 20 rows) |
| Filters that don't actually filter | Test every filter, add validation |
| No loading states | Skeleton loaders for every section |
| Color-only trend indicators | Add ↑/↓ icon + text label for accessibility |
| Long numbers without formatting | Use `Intl.NumberFormat` for 1,234,567 vs 1234567 |

## Companion Skills

- **`claude-design`** — Dashboards sind **Monitor-Surfaces**. claude-design lehrt: "A dashboard is a Monitor surface, not a Decide surface — do not give it a centered hero and three feature cards." Lies das BEVOR du ein Dashboard baust — sonst bekommst du AI-Slop.
- **ui-design-system** — REQUIRED first (tokens)
- **ui-component-library** — Uses Button/Input/Card components
- **ui-color-system** — Generates color palette with contrast checks
- **ui-data-table** — Sortable/filterable/paginated tables
- **ui-chart-builder** — Chart components (bar, line, pie, area)
- **web-design-guidelines** — Vercel's UI review checklist

## Part of UI-Factory

This skill is the **highest-level atom** in the UI-Factory pattern — combines everything below it into a working dashboard. Use after `ui-design-system` + `ui-component-library` + `ui-data-table` + `ui-chart-builder` are scaffolded.

Based on the KIMI K2 UI-Factory-Pattern (2026-06-30).