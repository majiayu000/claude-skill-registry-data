---
name: syncfusion-vue-sankey-chart
description: Always guide when user needs to implement Syncfusion Vue Sankey Chart for flow/energy/process visualization, configure nodes, links, styling, interactivity, accessibility, or handle RTL support in Vue applications. Trigger immediately for any Sankey chart implementation request and data flow diagram creation.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Syncfusion Vue Sankey Chart

A corrected and implementation-ready guide for the Syncfusion Vue Sankey Chart component in Vue 3 using the Composition API.

## Table of Contents
- [When-to-Use-This-Skill](#when-to-use-this-skill)
- [Component-Overview](#component-overview)
- [Documentation](#documentation)
  - [Getting-Started](#getting-started)
  - [Core-Concepts-Nodes-and-Links](#core-concepts-nodes-and-links)
  - [Appearance-and-Styling](#appearance-and-styling)
  - [Labels-and-Tooltips](#labels-and-tooltips)
  - [Legends-and-Titles](#legends-and-titles)
  - [Advanced-Features-and-Events](#advanced-features-and-events)
  - [Accessibility-and-RTL-Support](#accessibility-and-rtl-support)
- [Quick-Start-Example](#quick-start-example)
  - [Minimal-Sankey-Chart-Vue-3-Composition-API](#minimal-sankey-chart-vue-3-composition-api)
  - [Real-World-Example-Energy-Flow-Diagram](#real-world-example-energy-flow-diagram)
- [Common-Patterns](#common-patterns)
  - [Pattern-1-Multi-Stage-Flow-Visualization](#pattern-1-multi-stage-flow-visualization)
  - [Pattern-2-Branching-Flows](#pattern-2-branching-flows)
  - [Pattern-3-Convergence-Flows](#pattern-3-convergence-flows)
  - [Pattern-4-Color-Coded-Categories](#pattern-4-color-coded-categories)
  - [Pattern-5-Interactive-with-Events](#pattern-5-interactive-with-events)
- [Key-Props-Reference](#key-props-reference)
  - [SankeyComponent-Props](#sankeycomponent-props)
  - [Node-Props-e-sankey-node](#node-props-e-sankey-node)
  - [Link-Props-e-sankey-link](#link-props-e-sankey-link)
- [Common-Use-Cases](#common-use-cases)
- [Next-Steps](#next-steps)
- [Combined-Mistakes-and-Future-References](#combined-mistakes-and-future-references)



## When to Use This Skill

Use this skill when the user needs to:

- Set up a Sankey Chart in a Vue 3 project
- Create flow visualizations such as energy flows, process flows, data movement, and allocation maps
- Configure nodes and links with correct IDs, values, labels, and styling
- Customize appearance, dimensions, themes, labels, legends, and tooltips
- Add interactivity through events, hover feedback, legends, and tooltips
- Support accessibility and RTL layouts
- Export or print the visualization
- Troubleshoot rendering, binding, styling, and Composition API integration issues

## Component Overview

The Syncfusion Sankey Chart is a weighted-flow visualization component that uses:

- Nodes to represent stages or categories
- Links to represent movement between nodes
- Proportional thickness to communicate value magnitude

It is most useful when the user wants to show flow relationships instead of static comparison.

Good use cases include:

- Energy generation to consumption
- Supply chain movement
- Budget allocation
- ETL pipelines
- Website traffic flow

Avoid Sankey when the requirement is primarily:

- Category comparison only
- Time-series trend analysis
- Deep hierarchical expansion

## Documentation

### API Reference & Documentation

The Syncfusion Vue 3 Sankey Chart has comprehensive API documentation available at:

- **Official API Docs:** [https://ej2.syncfusion.com/vue/documentation/api/sankey/](https://ej2.syncfusion.com/vue/documentation/api/sankey/)
- **Component Docs:** [https://ej2.syncfusion.com/vue/documentation/sankey/](https://ej2.syncfusion.com/vue/documentation/sankey/)
- **Complete Local API Reference:** [api-reference.md](./references/api-reference.md)
- **API Generation Prompt:** [API_GENERATION_PROMPT.md](./API_GENERATION_PROMPT.md)

#### API Reference Contents

The [api-reference.md](./references/api-reference.md) file includes:

1. **Component Registration** - Vue 3 Composition API and Options API setup
2. **Configuration Properties** - All 30+ configurable properties with links
   - Dimensions, Layout, Titles, Data, Styling, Interactivity
3. **Data Models** - Complete documentation for:
   - SankeyNodeModel, SankeyLinkModel
   - SankeyNodeSettingsModel, SankeyLinkSettingsModel
   - SankeyLabelSettingsModel, SankeyLegendSettingsModel, SankeyTooltipSettingsModel
   - Supporting models (Border, Margin, Location, Animation, Font, Label)
4. **Events** - All 15+ event types with parameters and triggers
5. **Methods** - Component methods (export, print, refresh, setTheme)
6. **Enums** - All enumeration types with values
7. **Child Directives** - Template directive usage and properties
8. **Module Registration** - Service injection for features
9. **Common Usage Patterns** - Practical examples and best practices

Every property, event, method, and model in the API reference includes a direct link to the official Syncfusion Vue documentation.

### API Validation & Cross-Referencing

All API properties documented in [api-reference.md](./references/api-reference.md) are:
- ✅ Verified against the official [Syncfusion Vue Sankey API](https://ej2.syncfusion.com/vue/documentation/api/sankey/)
- ✅ Cross-referenced with actual component usage in the examples below
- ✅ Linked to their official documentation pages
- ✅ Validated for Vue 3 Composition API compliance

For details on how the API reference was generated, see [API_GENERATION_PROMPT.md](./API_GENERATION_PROMPT.md).

### Getting Started

The recommended Vue 3 implementation approach is:

- Use a Vue 3 SFC
- Use `<script setup>`
- Import the Sankey component and required directives from the Syncfusion Vue Charts package
- Import `provide` from `vue`
- Inject only the required Sankey modules
- Bind data with stable IDs between nodes and links
- Use a fixed or responsive container height so the SVG has space to render

### Core Concepts: Nodes and Links

The Sankey component depends on exact ID matching.

Node rules:

- Every node must have a unique `id`
- Labels should be assigned explicitly when readability matters
- Styling can be applied globally or per node
- Node width, padding, and fill are visual controls, not data controls

Link rules:

- `sourceId` must match an existing node ID
- `targetId` must match an existing node ID
- `value` must be numeric and positive
- Link appearance should be configured globally unless a specific override is needed

### Appearance and Styling

The main appearance categories are:

- Chart dimensions
- Node appearance
- Link appearance
- Title and subtitle
- Label formatting
- Theme CSS imports
- Margin and spacing

For production usage:

- Prefer `width="100%"` and a fixed `height`
- Keep `opacity` moderate so overlapping links remain readable
- Use source-based coloring when the flow origin matters most
- Keep node labels short

### Labels and Tooltips

Labels improve readability, but long labels can visually crowd the chart.

Best practices:

- Keep label text concise
- Enable tooltip details for full context
- Use labels for summary and tooltips for specifics
- Avoid forcing too many visible labels into a small chart area

### Legends and Titles

Use legends when colors communicate categories or grouping.

Use titles when the chart is viewed outside of surrounding explanatory text.

Common practice:

- Keep the title concise
- Use the subtitle for measurement context
- Place the legend at the bottom when horizontal space is limited

### Advanced Features and Events

The Sankey component can support:

- Legend-driven highlighting
- Tooltip interaction
- Orientation changes
- RTL display
- Print and export workflows
- Event-driven filtering or drill-down

In Vue 3 Composition API, event handlers should be declared as functions inside `<script setup>` and bound directly in the template.

### Accessibility and RTL Support

For accessibility:

- Ensure color contrast is sufficient
- Avoid using color alone to communicate meaning
- Keep labels meaningful
- Provide titles and contextual descriptions around the chart

For RTL:

- Enable RTL only when the application layout requires it
- Validate label readability and legend layout after enabling RTL

## Quick Start Example

### Minimal Sankey Chart (Vue 3 Composition API)

This version corrects the structural and Composition API issues while keeping the example minimal and runnable.

```vue
<template>
  <div class="container">
    <ejs-sankey
      id="minimal-sankey"
      width="100%"
      :height="chartHeight"
      :tooltip="tooltip"
    >
      <e-sankey-nodes>
        <e-sankey-node id="Source A" :label="{ text: 'Source A' }" />
        <e-sankey-node id="Target B" :label="{ text: 'Target B' }" />
      </e-sankey-nodes>

      <e-sankey-links>
        <e-sankey-link source-id="Source A" target-id="Target B" :value="100" />
      </e-sankey-links>
    </ejs-sankey>
  </div>
</template>

<script setup>
import { provide, ref } from 'vue';
import {
  SankeyComponent as EjsSankey,
  SankeyNodesCollectionDirective as ESankeyNodes,
  SankeyNodeDirective as ESankeyNode,
  SankeyLinksCollectionDirective as ESankeyLinks,
  SankeyLinkDirective as ESankeyLink,
  SankeyTooltip
} from '@syncfusion/ej2-vue-charts';

const chartHeight = ref('420px');
const tooltip = ref({
  enable: true
});

provide('sankey', [SankeyTooltip]);
</script>

<style>

.container {
  width: 100%;
}
</style>
```

### Real-World Example: Energy Flow Diagram

This version keeps the original order and intent, but corrects the Vue 3 Composition API wiring and Syncfusion directive usage.

```vue
<template>
  <div class="energy-diagram">
    <ejs-sankey
      id="energy-flow-sankey"
      width="100%"
      height="500px"
      :title="title"
      :linkStyle="linkStyle"
      :tooltip="tooltip"
      :legendSettings="legendSettings"
    >
      <e-sankey-nodes>
        <e-sankey-node id="Solar" :label="{ text: 'Solar' }" />
        <e-sankey-node id="Wind" :label="{ text: 'Wind' }" />
        <e-sankey-node id="Coal" :label="{ text: 'Coal' }" />
        <e-sankey-node id="Generation" :label="{ text: 'Generation' }" />
        <e-sankey-node id="Distribution" :label="{ text: 'Distribution' }" />
        <e-sankey-node id="Consumption" :label="{ text: 'Consumption' }" />
      </e-sankey-nodes>

      <e-sankey-links>
        <e-sankey-link source-id="Solar" target-id="Generation" :value="300" />
        <e-sankey-link source-id="Wind" target-id="Generation" :value="200" />
        <e-sankey-link source-id="Coal" target-id="Generation" :value="500" />
        <e-sankey-link source-id="Generation" target-id="Distribution" :value="900" />
        <e-sankey-link source-id="Distribution" target-id="Consumption" :value="850" />
      </e-sankey-links>
    </ejs-sankey>
  </div>
</template>

<script setup>
import { provide, ref } from 'vue';
import {
  SankeyComponent as EjsSankey,
  SankeyNodesCollectionDirective as ESankeyNodes,
  SankeyNodeDirective as ESankeyNode,
  SankeyLinksCollectionDirective as ESankeyLinks,
  SankeyLinkDirective as ESankeyLink,
  SankeyTooltip,
  SankeyLegend
} from '@syncfusion/ej2-vue-charts';

const title = ref('Energy Flow System');

const linkStyle = ref({
  opacity: 0.6,
  curvature: 0.55,
  colorType: 'Source'
});

const tooltip = ref({
  enable: true
});

const legendSettings = ref({
  visible: true,
  position: 'Bottom'
});

provide('sankey', [SankeyTooltip, SankeyLegend]);
</script>
```

## Common Patterns

### Pattern 1: Multi-Stage Flow Visualization

**When:** Visualizing a process with multiple intermediate stages

```js
const nodes = [
  { id: 'Supplier A', label: { text: 'Supplier A' } },
  { id: 'Warehouse', label: { text: 'Warehouse' } },
  { id: 'Distribution', label: { text: 'Distribution' } },
  { id: 'Customer', label: { text: 'Customer' } }
];

const links = [
  { sourceId: 'Supplier A', targetId: 'Warehouse', value: 1000 },
  { sourceId: 'Warehouse', targetId: 'Distribution', value: 950 },
  { sourceId: 'Distribution', targetId: 'Customer', value: 900 }
];
```

### Pattern 2: Branching Flows

**When:** One source distributes into multiple targets

```js
const links = [
  { sourceId: 'Power Plant', targetId: 'Residential', value: 600 },
  { sourceId: 'Power Plant', targetId: 'Commercial', value: 400 },
  { sourceId: 'Power Plant', targetId: 'Industrial', value: 300 }
];
```

### Pattern 3: Convergence Flows

**When:** Multiple sources merge into a shared destination

```js
const links = [
  { sourceId: 'Product A', targetId: 'Revenue', value: 500 },
  { sourceId: 'Product B', targetId: 'Revenue', value: 300 },
  { sourceId: 'Service C', targetId: 'Revenue', value: 200 }
];
```

### Pattern 4: Color-Coded Categories

**When:** Color needs to represent the flow origin or type

```js
const linkStyle = {
  colorType: 'Source',
  opacity: 0.7,
  curvature: 0.45
};
```

### Pattern 5: Interactive with Events

**When:** Users need interaction-driven analysis such as drill-down or details-on-hover

```vue
<template>
  <ejs-sankey
    id="interactive-sankey"
    width="100%"
    height="450px"
    :tooltip="{ enable: true }"
    :nodeClick="onNodeClick"
    :mouseMove="onMouseMove"
  >
    <e-sankey-nodes>
      <e-sankey-node id="Input" :label="{ text: 'Input' }" />
      <e-sankey-node id="Processing" :label="{ text: 'Processing' }" />
      <e-sankey-node id="Output" :label="{ text: 'Output' }" />
    </e-sankey-nodes>

    <e-sankey-links>
      <e-sankey-link source-id="Input" target-id="Processing" :value="120" />
      <e-sankey-link source-id="Processing" target-id="Output" :value="110" />
    </e-sankey-links>
  </ejs-sankey>
</template>

<script setup>
import { provide, ref } from 'vue';
import {
  SankeyComponent as EjsSankey,
  SankeyNodesCollectionDirective as ESankeyNodes,
  SankeyNodeDirective as ESankeyNode,
  SankeyLinksCollectionDirective as ESankeyLinks,
  SankeyLinkDirective as ESankeyLink,
  SankeyTooltip,
  SankeyLegend
} from '@syncfusion/ej2-vue-charts';

provide('sankey', [SankeyTooltip, SankeyLegend]);
function onNodeClick(args) {
  console.log('Node clicked:', args);
}

function onMouseMove(args) {
  console.log('Pointer move:', args);
}
</script>
```

## Key Props Reference

### SankeyComponent Props

Complete API reference with all 30+ properties available in [api-reference.md](./references/api-reference.md).

**Official API Link:** [https://ej2.syncfusion.com/vue/documentation/api/sankey/](https://ej2.syncfusion.com/vue/documentation/api/sankey/)

Essential props for basic usage:

| Prop | Type | Official Link | Purpose |
|------|------|---|---------|
| [`width`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#width) | string | Property API | Chart width (default: '100%') |
| [`height`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#height) | string | Property API | Chart height (default: '420px') |
| [`title`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#title) | string | Property API | Main title text |
| [`subTitle`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#subtitle) | string | Property API | Subtitle text |
| [`linkStyle`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#linkstyle) | object | SankeyLinkSettingsModel | Global link styling (opacity, curvature, colorType) |
| [`nodeStyle`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#nodestyle) | object | SankeyNodeSettingsModel | Global node styling (width, padding, fill, stroke) |
| [`tooltip`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#tooltip) | object | SankeyTooltipSettingsModel | Tooltip configuration (enable, format, border, opacity) |
| [`legendSettings`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#legendsettings) | object | SankeyLegendSettingsModel | Legend visibility and placement (visible, position, background) |
| [`labelSettings`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#labelsettings) | object | SankeyLabelSettingsModel | Node label styling (visible, fontFamily, fontSize, color) |
| [`margin`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#margin) | object | MarginModel | Outer spacing around the chart (left, right, top, bottom) |
| [`orientation`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#orientation) | string | Enum | Flow direction ('Horizontal' or 'Vertical') |
| [`enableRtl`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#enablertl) | boolean | Property API | Right-to-left layout support |
| [`theme`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#theme) | string | ChartTheme | Color theme (Material, Bootstrap, Tailwind, etc.) |
| [`animation`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#animation) | object | AnimationModel | Animation settings (enable, duration) |

### Node Props (e-sankey-node / ESankeyNode)

For detailed node API, see [SankeyNode Properties](./references/api-reference.md#sankeynode-properties) and [SankeyNodeModel API](https://ej2.syncfusion.com/vue/documentation/api/sankeynodemodel/).

| Prop | Type | Official Link | Purpose |
|------|------|---|---------|
| [`id`](https://ej2.syncfusion.com/vue/documentation/api/sankeynodemodel/#id) | string | Property API | Unique node identifier (required) |
| [`label`](https://ej2.syncfusion.com/vue/documentation/api/sankeynodemodel/#label) | object | LabelModel | Node label configuration with text, color, fontSize |
| [`color`](https://ej2.syncfusion.com/vue/documentation/api/sankeynodemodel/#color) | string | Property API | Node fill color |
| [`offset`](https://ej2.syncfusion.com/vue/documentation/api/sankeynodemodel/#offset) | number | Property API | Manual vertical positioning adjustment |

### Link Props (e-sankey-link / ESankeyLink)

For detailed link API, see [SankeyLink Properties](./references/api-reference.md#sankeylink-properties) and [SankeyLinkModel API](https://ej2.syncfusion.com/vue/documentation/api/sankeylinkmodel/).

| Prop | Type | Official Link | Purpose |
|------|------|---|---------|
| [`sourceId`](https://ej2.syncfusion.com/vue/documentation/api/sankeylinkmodel/#sourceid) | string | Property API | Source node ID (required) |
| [`targetId`](https://ej2.syncfusion.com/vue/documentation/api/sankeylinkmodel/#targetid) | string | Property API | Target node ID (required) |
| [`value`](https://ej2.syncfusion.com/vue/documentation/api/sankeylinkmodel/#value) | number | Property API | Flow magnitude/weight (required, must be positive) |
| [`color`](https://ej2.syncfusion.com/vue/documentation/api/sankeylinkmodel/#color) | string | Property API | Per-link color override |

## Essential API Properties by Category

### Data Configuration
- **[`nodes`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#nodes)** - Array of [SankeyNodeModel](https://ej2.syncfusion.com/vue/documentation/api/sankeynodemodel/) objects defining chart entities
- **[`links`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#links)** - Array of [SankeyLinkModel](https://ej2.syncfusion.com/vue/documentation/api/sankeylinkmodel/) objects defining flows between nodes

### Styling & Appearance
- **[`nodeStyle`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#nodestyle)** - Global node appearance via [SankeyNodeSettingsModel](https://ej2.syncfusion.com/vue/documentation/api/sankeynodesettingsmodel/) (width, padding, fill, stroke, opacity)
- **[`linkStyle`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#linkstyle)** - Global link appearance via [SankeyLinkSettingsModel](https://ej2.syncfusion.com/vue/documentation/api/sankeylinksettingsmodel/) (opacity, curvature, colorType: 'Source'|'Target'|'Blend')
- **[`theme`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#theme)** - Visual theme selection (Material, Bootstrap, Tailwind, etc.)
- **[`background`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#background)** - Chart container background color
- **[`border`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#border)** - Chart container border styling via [BorderModel](https://ej2.syncfusion.com/vue/documentation/api/bordermodel/)

### Layout & Dimensions
- **[`width`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#width)** - Chart width as CSS value (e.g., '100%', '500px')
- **[`height`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#height)** - Chart height as CSS value (default: '420px')
- **[`margin`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#margin)** - Spacing around chart via [MarginModel](https://ej2.syncfusion.com/vue/documentation/api/marginmodel/) (left, right, top, bottom)
- **[`orientation`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#orientation)** - 'Horizontal' (default) or 'Vertical' flow direction

### Text & Labels
- **[`title`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#title)** - Chart title text
- **[`titleStyle`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#titlestyle)** - Title styling via [SankeyTitleStyleModel](https://ej2.syncfusion.com/vue/documentation/api/sankeytitlestylemodel/) (fontFamily, size, color, fontWeight)
- **[`subTitle`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#subtitle)** - Subtitle text
- **[`labelSettings`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#labelsettings)** - Node label configuration via [SankeyLabelSettingsModel](https://ej2.syncfusion.com/vue/documentation/api/sankeylabelsettingsmodel/) (visible, fontFamily, fontSize, color, padding)

### Interactivity
- **[`tooltip`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#tooltip)** - Tooltip behavior via [SankeyTooltipSettingsModel](https://ej2.syncfusion.com/vue/documentation/api/sankeytooltipsettingsmodel/) (enable, format string, opacity, border)
- **[`legendSettings`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#legendsettings)** - Legend display via [SankeyLegendSettingsModel](https://ej2.syncfusion.com/vue/documentation/api/sankeylegendsettingsmodel/) (visible, position, background, enableHighlight)
- **[`animation`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#animation)** - Animation control via [AnimationModel](https://ej2.syncfusion.com/vue/documentation/api/animationmodel/) (enable, duration in ms)

### Localization & Accessibility
- **[`enableRtl`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#enablertl)** - Right-to-left layout support
- **[`locale`](https://ej2.syncfusion.com/vue/documentation/api/sankey/#locale)** - Localization culture (default: 'en-US')

**See [Complete API Reference](./references/api-reference.md)** for all 30+ properties, methods, events, and data models with full documentation and examples.

**Official API Documentation:** [https://ej2.syncfusion.com/vue/documentation/api/sankey/](https://ej2.syncfusion.com/vue/documentation/api/sankey/)

## Common Use Cases

**Use Case 1: Supply Chain Visualization**  
Map goods from supplier to warehouse to distribution to customer. Use `links` with realistic `value` amounts and `nodeStyle.width` to control node proportions.

**Use Case 2: Energy Flow Diagram**  
Show energy generation sources and how they move through the grid. Use `linkStyle.colorType: 'Source'` to color links by their origin, and `tooltip` to show detailed values.

**Use Case 3: Website Traffic Flow**  
Represent movement from landing pages to internal pages to conversion points. Use `animation` for visual engagement and `legendSettings` to categorize traffic sources.

**Use Case 4: Budget Allocation**  
Display how budget travels from a department into programs and activities. Use `labelSettings` to show currency values and `theme` for professional appearance.

**Use Case 5: Data Pipeline**  
Show how records move through ingestion, transformation, storage, and reporting. Use `orientation: 'Horizontal'` for left-to-right flow and `nodeStyle.opacity` to de-emphasize bottleneck stages.

## Next Steps

1. Start with the minimal example and verify rendering
2. Add real node and link IDs from your business data
3. Turn on tooltip and legend only after the base flow renders correctly
4. Introduce styling after confirming link-node relationships are valid
5. Add events and export behavior only after the chart structure is stable

## Combined Mistakes and Future References

1. **Missing `provide` import in the minimal example**  
   The original example used `provide('sankey', [...])` without importing `provide` from Vue.

2. **Incorrect child directive tag names**  
   The original examples used `e-sankey-nodes-collection` and `e-sankey-links-collection`. The corrected structure uses `e-sankey-nodes` and `e-sankey-links`, which aligns with the directive registration pattern.

3. **Inconsistent directive aliases**  
   The original import aliases were named like collection directives but were paired with nonstandard template tags. The corrected examples keep the imported directives and align them with the proper template usage.

4. **Composition API structure mismatch**  
   The document said Vue 3 Composition API, but some snippets still reflected patterns that would confuse users moving from Vue 2 or Options API.

5. **Template attribute normalization**  
   Link attributes are safer and clearer in kebab-case inside Vue templates, such as `source-id` and `target-id`.

6. **Minimal example lacked enough visible configuration for debugging**  
   Enabling tooltip in the minimal sample makes validation easier during first render testing.

7. **Layout robustness**  
   A Sankey chart may appear broken when the container collapses. Explicit height or min-height prevents false rendering issues.

8. **Pattern 5 was written in Options API style**  
   The original event example used `methods`, which is not the correct presentation style for a Vue 3 `<script setup>` guide.

9. **Documentation consistency issue**  
   The original document mixed implementation guidance, conceptual notes, and partial code conventions. The corrected copy keeps the order intact but makes the code runnable and the guidance Vue 3 specific.

10. **Future reference for troubleshooting**  
    If a Sankey chart does not render correctly, verify these in order:
    - The container has height
    - Node IDs are unique
    - Every link source exists
    - Every link target exists
    - All required modules are injected with `provide`
