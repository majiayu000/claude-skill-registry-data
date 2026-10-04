---
name: templateclaw-dashboard
description: "Generate a modern admin dashboard with charts, tables, and KPI cards. Supports admin, analytics, monitoring, and CRM styles. Uses glassmorphism design with dark theme."
allowed-tools: Read, Write, Edit
argument-hint: "[style: admin|analytics|monitoring|crm]"
---

# TemplateClaw — Dashboard Generator

Generate a production-ready dashboard with modern data visualization design.

## When Invoked

1. If argument provided (e.g., `/templateclaw-dashboard analytics`), generate that style
2. If no argument, ask: "What type of dashboard? (admin / analytics / monitoring / crm)"

## Dashboard Styles

### Admin Dashboard
- Sidebar navigation (collapsible) with icons
- Top bar with search, notifications, user avatar
- KPI cards row (4 cards: Users, Revenue, Orders, Growth)
- Main chart area (CSS-only bar chart or line indicators)
- Recent activity table
- Quick actions panel

### Analytics Dashboard
- Date range picker header
- KPI cards with sparkline trends (CSS-only)
- Large area chart placeholder (gradient fill)
- Breakdown pie/donut chart (CSS conic-gradient)
- Top pages/items table with progress bars
- Real-time visitors counter (animated)

### System Monitoring Dashboard
- Status indicator header (green/yellow/red)
- Server health cards (CPU, Memory, Disk, Network)
- Uptime timeline (CSS grid blocks)
- Alert feed (scrollable, severity-colored)
- Service status table
- Response time chart placeholder

### CRM Dashboard
- Pipeline stages (kanban-style horizontal)
- Deal value KPIs
- Recent contacts table with avatars
- Activity timeline
- Conversion funnel (CSS trapezoid shapes)
- Tasks/reminders sidebar

## Design System

```css
/* Dashboard-specific */
--sidebar-width: 260px;
--sidebar-collapsed: 72px;
--topbar-height: 64px;
--card-radius: 16px;
--transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

/* Chart Colors */
--chart-1: #7C3AED;
--chart-2: #EC4899;
--chart-3: #3B82F6;
--chart-4: #10B981;
--chart-5: #F59E0B;
```

## Output Requirements

- Single HTML file with embedded CSS and JS
- Tailwind CSS via CDN
- CSS-only charts (no Chart.js dependency) — use gradients, conic-gradient, flexbox
- Sidebar toggle (collapsed ↔ expanded)
- Responsive: sidebar becomes bottom nav on mobile
- Dark mode default
- Sample data hardcoded (easily replaceable)
- Smooth transitions on all interactive elements
- Grid layout for dashboard cards

## Data Placeholders

Use realistic sample data:
```javascript
const sampleData = {
  users: 12847,
  revenue: "$48,352",
  growth: "+12.5%",
  orders: 1284
};
```

Mark data injection points:
```html
<!-- DATA: KPI values -->
<!-- DATA: Chart data -->
<!-- DATA: Table rows -->
```
