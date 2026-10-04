---
license: Apache-2.0
name: data-viz-2025
description: State-of-the-art data visualization for React/Next.js/TypeScript with Tailwind CSS. Creates compelling, tested, and accessible visualizations following Tufte principles and NYT Graphics standards. Activate on "data viz", "chart", "graph", "visualization", "dashboard", "plot", "Recharts", "Nivo", "D3". NOT for static images, print graphics, or basic HTML tables.
allowed-tools: Read,Write,Edit,Bash
category: Data & Analytics
tags:
  - data-visualization
  - '2025'
  - charts
  - d3
  - interactive
---

# Data Visualization 2025: The Art & Science of Visual Communication

Create visualizations that marry NYT Graphics rigor with modern web performance and accessibility standards.

## DECISION POINTS

### Primary Library Selection Tree

```
What type of chart are you building?
├─ Exploratory analysis / rapid prototyping
│  ├─ Data size < 5K points → Observable Plot
│  └─ Data size > 5K points → D3.js with sampling
│
├─ Standard business charts (bars, lines, areas)
│  ├─ Need it fast & simple → Recharts
│  ├─ Premium aesthetics required → Nivo
│  └─ Custom interactions needed → Visx
│
├─ Complex/novel visualizations
│  ├─ React component structure preferred → Visx
│  └─ Maximum control needed → D3.js
│
└─ Dashboard with many charts
   ├─ Tailwind design system → Tremor
   └─ Consistent theming → Nivo
```

### Performance Optimization Branch

```
How many data points?
├─ < 1K points
│  ├─ Need crisp scaling → SVG rendering
│  └─ Need interactivity → SVG with event handlers
│
├─ 1K - 10K points
│  ├─ Simple shapes → SVG (acceptable)
│  ├─ Complex animations → Canvas
│  └─ Mobile performance critical → Canvas
│
└─ > 10K points
   ├─ Static display → Canvas with aggregation
   ├─ Interactive exploration → WebGL (via deck.gl)
   └─ Real-time updates → Canvas with data sampling
```

### Accessibility Decision Matrix

```
Is this for production use?
├─ Yes → Must implement ALL accessibility features
│  ├─ Keyboard navigation for all interactive elements
│  ├─ Screen reader support with data tables
│  ├─ Color-blind safe palettes (test with simulators)
│  └─ Respect prefers-reduced-motion
│
└─ Internal tool/prototype → Implement core features
   ├─ Alt text for chart images
   ├─ Sufficient color contrast (4.5:1 minimum)
   └─ Keyboard access for primary interactions
```

### Mobile Responsiveness Strategy

```
What's the screen breakpoint?
├─ Mobile (< 640px)
│  ├─ Many data points → Aggregate to top 5-7 items
│  ├─ Time series → Show last 30 days, add "View All" button
│  ├─ Multi-series → Use small multiples instead of overlays
│  └─ Complex legends → Replace with direct labels
│
├─ Tablet (640px - 1024px)
│  ├─ Reduce axis labels by 50%
│  ├─ Simplify gridlines (remove minor ticks)
│  └─ Increase touch targets to 44px minimum
│
└─ Desktop (> 1024px)
   └─ Show full detail, all interactions enabled
```

## FAILURE MODES

### 1. "Rainbow Vomit" (Visual Overload)
**Symptom:** Chart has 8+ colors, tiny legend, impossible to distinguish series
**Diagnosis:** Trying to show too many categories simultaneously
**Fix:** 
- Limit to 5 categories maximum
- Use "Other" bucket for remaining items
- Consider small multiples instead of single overloaded chart
- Apply semantic color coding (red=bad, green=good)

### 2. "Misleading Scale" (Graphical Dishonesty)
**Symptom:** Bar chart with Y-axis starting at 95 instead of 0, making 2% difference look like 200%
**Diagnosis:** Truncated axes exaggerating small differences
**Fix:**
- Bar charts MUST start Y-axis at 0
- Line charts can use truncated scales (with clear annotation)
- Add reference lines to show context
- Use percentage change annotations when showing growth

### 3. "Mobile Pancake" (Responsiveness Failure)
**Symptom:** Desktop chart squished to mobile width, text unreadable, interactions broken
**Diagnosis:** No responsive design strategy, one-size-fits-all approach
**Fix:**
- Implement breakpoint-specific layouts
- Aggregate data for mobile (top 5 instead of 20 items)
- Replace hover with touch-friendly interactions
- Consider chart type changes (horizontal bars instead of vertical)

### 4. "Loading Desert" (Poor Loading States)
**Symptom:** White screen for 3+ seconds, then chart appears suddenly
**Diagnosis:** No skeleton loading, blocking data fetch
**Fix:**
- Show skeleton that matches final chart structure
- Implement progressive loading (axes first, then data)
- Add loading animations with spring physics
- Cache data when possible to reduce perceived load time

### 5. "Accessibility Afterthought" (Exclusion by Design)
**Symptom:** Screen reader announces "image" with no context, keyboard navigation broken
**Diagnosis:** Visual-only design, no programmatic access to data
**Fix:**
- Add comprehensive alt text describing trends and insights
- Provide data table alternative with show/hide toggle
- Implement keyboard navigation for interactive elements
- Test with actual screen reader (NVDA, JAWS, VoiceOver)

## WORKED EXAMPLES

### Example 1: Multi-Series Mobile Chart

**Scenario:** Executive dashboard showing revenue by 8 product lines over 12 months, needs to work on mobile.

**Decision Process:**
1. **Data Analysis:** 8 series × 12 months = 96 data points, acceptable for SVG
2. **Mobile Strategy:** 8 series too many for mobile width
3. **Library Choice:** Recharts for quick implementation, good mobile support

**Desktop Implementation:**
```typescript
<LineChart data={monthlyData} width="100%" height={400}>
  <XAxis dataKey="month" />
  <YAxis />
  <Tooltip />
  <Legend />
  {products.map((product, index) => (
    <Line 
      key={product} 
      dataKey={product} 
      stroke={colors[index]}
      strokeWidth={2}
    />
  ))}
</LineChart>
```

**Mobile Adaptation:**
```typescript
const isMobile = useMediaQuery('(max-width: 640px)');
const topProducts = isMobile 
  ? products.slice(0, 3) // Show only top 3
  : products;

<ResponsiveContainer height={isMobile ? 250 : 400}>
  <LineChart data={monthlyData}>
    <XAxis 
      dataKey="month" 
      interval={isMobile ? 2 : 0} // Every 3rd month on mobile
      tick={{ fontSize: isMobile ? 10 : 12 }}
    />
    <YAxis tick={isMobile ? false : true} />
    <Tooltip />
    {!isMobile && <Legend />}
    {topProducts.map((product, index) => (
      <Line 
        key={product} 
        dataKey={product} 
        stroke={colors[index]}
        strokeWidth={isMobile ? 3 : 2} // Thicker lines for mobile
      />
    ))}
  </LineChart>
</ResponsiveContainer>
```

**Key Decisions Made:**
- Reduced series from 8 to 3 on mobile
- Increased line thickness for better touch interaction
- Removed Y-axis labels to save space
- Showed every 3rd month label instead of all 12

### Example 2: Performance-Critical Sankey Diagram

**Scenario:** User journey flow with 50K user sessions, 12 touchpoints, needs real-time updates.

**Decision Process:**
1. **Data Size:** 50K sessions × 12 steps = 600K transitions, too much for SVG
2. **Performance Requirement:** Real-time updates every 30 seconds
3. **Library Choice:** D3.js with Canvas rendering for performance

**Implementation Strategy:**
```typescript
// Data aggregation first - group similar paths
const aggregatedFlows = useMemo(() => {
  return rawUserJourney
    .reduce((acc, session) => {
      const pathKey = session.path.join('→');
      acc[pathKey] = (acc[pathKey] || 0) + session.count;
      return acc;
    }, {})
    // Keep only paths with 100+ users
    .filter(([path, count]) => count >= 100);
}, [rawUserJourney]);

// Canvas rendering for performance
useEffect(() => {
  const canvas = canvasRef.current;
  const ctx = canvas.getContext('2d');
  
  // Clear and render
  ctx.clearRect(0, 0, width, height);
  
  // Use Web Workers for heavy calculations
  const worker = new Worker('/sankeyWorker.js');
  worker.postMessage({ flows: aggregatedFlows, dimensions: { width, height } });
  
  worker.onmessage = (e) => {
    const { nodes, links } = e.data;
    drawSankey(ctx, nodes, links);
  };
}, [aggregatedFlows]);
```

**Performance Optimizations Applied:**
- Aggregated 600K data points to ~200 significant flows
- Used Canvas instead of SVG for smooth 60fps updates
- Moved calculations to Web Worker to prevent UI blocking
- Implemented data streaming instead of full refreshes

## QUALITY GATES

Before shipping any data visualization, verify ALL conditions:

- [ ] **Data Accuracy**: Chart values match source data (spot-check 5 random points)
- [ ] **Visual Hierarchy**: Most important insight is visually prominent (passes 5-second test)
- [ ] **Mobile Responsive**: Chart readable and interactive on 320px width screen
- [ ] **Accessibility Compliant**: Screen reader announces chart purpose and key trends
- [ ] **Performance Acceptable**: Chart renders in <2 seconds on 3G connection
- [ ] **Error Handling**: Graceful degradation when data is missing/malformed
- [ ] **Loading States**: Skeleton or progress indicator shown during data fetch
- [ ] **Color Contrast**: All text meets WCAG AA standards (4.5:1 ratio minimum)
- [ ] **Keyboard Navigation**: All interactive elements accessible via Tab key
- [ ] **Cross-Browser Tested**: Works correctly in Chrome, Firefox, Safari, Edge

## NOT-FOR BOUNDARIES

**This skill should NOT be used for:**

- **Static image exports** → Use design tools (Figma, Illustrator) or server-side rendering libraries
- **Print-optimized graphics** → Use different color palettes and typography for print medium
- **Basic HTML data tables** → Use semantic `<table>` markup with CSS styling
- **Simple icon displays** → Use icon libraries (Heroicons, Feather) instead
- **Real-time streaming visualization** → For >100 updates/second, use specialized libraries (deck.gl, Three.js)

**When to delegate to other skills:**
- **Backend data processing** → Use [data-pipeline-2025] for ETL and aggregation
- **UI component design** → Use [ui-design-2025] for non-data interface elements  
- **Performance optimization** → Use [react-performance-2025] for general React optimization
- **Testing strategy** → Use [testing-2025] for comprehensive test planning

**Library-specific boundaries:**
- **Observable Plot**: Not for production apps (research/notebooks only)
- **Recharts**: Not for custom/novel chart types (limited flexibility)
- **Nivo**: Not for >10K data points (performance limitations)
- **D3.js**: Not for simple charts (unnecessary complexity)