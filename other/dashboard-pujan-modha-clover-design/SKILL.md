---
name: dashboard
mode: prototype
preview: html
inputs:
  - name: appName
    type: string
    label: App Name
  - name: metricCards
    type: integer
    label: Number of Metric Cards
parameters:
  - name: sidebarWidth
    type: number
    min: 200
    max: 320
    label: Sidebar Width
outputs:
  primary: index.html
---

# Dashboard UI Skill

Generate a professional analytics dashboard interface.

## Rules
- Sidebar navigation with icons + labels
- Top bar with search, notifications, user avatar
- Metric cards row (2-4 cards)
- Main chart area (line or bar chart using Chart.js or pure SVG)
- Recent activity / transactions table
- NO emojis as icons — use Lucide-style SVG icons
- Dark mode support via CSS custom properties
- Clean data tables with proper alignment

## Structure
1. Sidebar (collapsible on mobile)
2. Top bar
3. Metric cards
4. Charts section
5. Data table
6. Quick actions / shortcuts

## Technical
- Single-file HTML
- CSS Grid for layout
- CSS custom properties for colors
- Accessible table markup
