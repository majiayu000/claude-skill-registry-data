---
name: syncfusion-vue-range-navigator
description: Complete guide for implementing the Syncfusion Vue Range Navigator component for interactive data visualization and navigation across date or numeric ranges. Use this guide whenever the user mentions Range Navigator, range selection, date-range filtering, period selector, lightweight mode, Range Selector, or Syncfusion Vue range-based navigation/filtering scenarios.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Syncfusion Vue Range Navigator

A comprehensive guide for implementing the Syncfusion Vue Range Navigator component for interactive data-range selection, visualization, and navigation across charts, grids, and dashboards. 

## Table of Contents

- [When to Use This Skill](#when-to-use-this-skill)
- [Component Overview](#component-overview)
- [Documentation](#documentation)
  - [API Reference](#api-reference)
  - [Getting Started](#getting-started)
  - [Series Visualization](#series-visualization)
  - [Period Selector](#period-selector)
  - [Range Selection &amp; Events](#range-selection--events)
  - [Tooltip Customization](#tooltip-customization)
  - [Performance &amp; Accessibility](#performance--accessibility)
  - [Integration Examples](#integration-examples)
- [Quick Start](#quick-start)
  - [Installation](#installation)
  - [Basic Implementation (Vue 3 - Composition API)](#basic-implementation-vue-3---composition-api)
  - [Basic Implementation (Vue 3 - Options API)](#basic-implementation-vue-3---options-api)
- [Common Patterns](#common-patterns)
  - [Pattern 1: Range Navigator with Period Selector](#pattern-1-range-navigator-with-period-selector)
  - [Pattern 2: Synchronizing with Chart](#pattern-2-synchronizing-with-chart)
  - [Pattern 3: Lightweight Mode for Mobile](#pattern-3-lightweight-mode-for-mobile)
- [Key Configuration Properties](#key-configuration-properties)
- [API Reference](#api-reference-1)
- [Corrections Applied](#corrections-applied)

## When to Use This Skill

Use this skill when you need to:  
- **Add interactive range selection** to charts, grids, or dashboards. 
- **Implement date or numeric range filters** for data visualization. 
- **Create period selectors** such as 1M, 3M, 6M, 1Y, and All for quick date-range selection. 
- **Optimize data display for mobile** with lightweight Range Navigator mode. 
- **Synchronize Range Navigator with other components** such as Chart and DataGrid. 
- **Customize tooltips and visual styling** for range-selection feedback. 
- **Enable RTL and accessibility features** for international audiences. 
- **Handle range-change events** and programmatic range updates. 

## Component Overview

The **Range Navigator** is an interactive data-visualization control that enables users to:  
- Scroll and navigate through large datasets. 
- Select specific date or numeric ranges. 
- View data trends across different time periods. 
- Connect with charts and grids for coordinated data display. 
- Quick-select predefined periods through the period selector. 

**Package:** `@syncfusion/ej2-vue-charts` 

## Documentation

### API Reference
📄 **Read:** `references/api-reference.md` for complete API documentation including properties, data models, events, methods, enums, child directives, and modules for the Range Navigator component.

### Getting Started
📄 **Read:** `references/getting-started.md` for installation, package setup, Vue 2 / Vue 3 configuration, basic Range Navigator implementation, and module injection. 

### Series Visualization
📄 **Read:** `references/series-types.md` for Line, Area, and StepLine rendering, supported series configuration, and series styling. 

### Period Selector
📄 **Read:** `references/period-selector.md` for built-in period buttons, custom period configuration, selector positioning, and height settings. The correct settings property is `periods`, not `intervals`. 

### Range Selection & Events
📄 **Read:** `references/range-selection.md` for selecting ranges programmatically, handling the `changed` event, and synchronizing external UI state with the selected range. 

### Tooltip Customization
📄 **Read:** `references/tooltip-customization.md` for enabling tooltips, supported tooltip properties such as `fill`, `border`, `displayMode`, and `textStyle`, and styling patterns. 

### Performance & Accessibility
📄 **Read:** `references/performance-accessibility.md` for lightweight mode, performance-related settings, RTL rendering, and accessibility guidance. 

### Integration Examples
📄 **Read:** `references/integration-examples.md` for integrating Range Navigator with Chart, DataGrid, and other coordinated data-visualization controls. 

## Quick Start

### Installation

```bash
npm install @syncfusion/ej2-vue-charts --save
```

This is the required npm package used by the official Vue Range Navigator getting-started documentation. 

### Basic Implementation (Vue 3 - Composition API)

The corrected Vue 3 Composition API pattern below adds the required module injection, keeps `dataSource` on the series because a series is rendered, and uses the correct `@changed` event rather than `@change`. 

```vue
<template>
  <div class="app-container">
    <ejs-rangenavigator
      :valueType="valueType"
      :value="rangeValue"
      :labelFormat="labelFormat"
      @changed="onRangeChanged"
    >
      <e-rangenavigator-series-collection>
        <e-rangenavigator-series
          :dataSource="data"
          xName="x"
          yName="y"
          type="Area"
          :width="2"
        />
      </e-rangenavigator-series-collection>
    </ejs-rangenavigator>
  </div>
</template>

<script setup>
import { provide, ref } from 'vue';
import {
  RangeNavigatorComponent as EjsRangenavigator,
  RangenavigatorSeriesCollectionDirective as ERangenavigatorSeriesCollection,
  RangenavigatorSeriesDirective as ERangenavigatorSeries,
  AreaSeries,
  DateTime
} from '@syncfusion/ej2-vue-charts';

const valueType = 'DateTime';
const labelFormat = 'MMM-yy';

const rangeValue = ref([new Date(2023, 0, 1), new Date(2023, 11, 31)]);
const data = ref([
  { x: new Date(2023, 0, 1), y: 21 },
  { x: new Date(2023, 0, 2), y: 24 },
  { x: new Date(2023, 0, 3), y: 36 },
  { x: new Date(2023, 0, 4), y: 38 }
]);

const onRangeChanged = (args) => {
  rangeValue.value = [new Date(args.start), new Date(args.end)];
  console.log('Range changed:', args.start, args.end);
};

provide('rangeNavigator', [DateTime, AreaSeries]);
</script>
```

### Basic Implementation (Vue 3 - Options API)

This corrected Options API version uses the same Syncfusion structure: root `ejs-rangenavigator`, an `e-rangenavigator-series-collection`, series-level `dataSource`, and the `changed` event for reactive synchronization. 

```vue
<template>
  <div class="app-container">
    <ejs-rangenavigator
      :valueType="valueType"
      :value="rangeValue"
      :labelFormat="labelFormat"
      @changed="onRangeChanged"
    >
      <e-rangenavigator-series-collection>
        <e-rangenavigator-series
          :dataSource="data"
          xName="x"
          yName="y"
          type="Area"
          :width="2"
        />
      </e-rangenavigator-series-collection>
    </ejs-rangenavigator>
  </div>
</template>

<script>
import {
  RangeNavigatorComponent,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective,
  AreaSeries,
  DateTime
} from '@syncfusion/ej2-vue-charts';

export default {
  name: 'App',
  components: {
    'ejs-rangenavigator': RangeNavigatorComponent,
    'e-rangenavigator-series-collection': RangenavigatorSeriesCollectionDirective,
    'e-rangenavigator-series': RangenavigatorSeriesDirective
  },
  provide: {
    rangeNavigator: [DateTime, AreaSeries]
  },
  data() {
    return {
      valueType: 'DateTime',
      labelFormat: 'MMM-yy',
      rangeValue: [new Date(2023, 0, 1), new Date(2023, 11, 31)],
      data: [
        { x: new Date(2023, 0, 1), y: 21 },
        { x: new Date(2023, 0, 2), y: 24 },
        { x: new Date(2023, 0, 3), y: 36 },
        { x: new Date(2023, 0, 4), y: 38 }
      ]
    };
  },
  methods: {
    onRangeChanged(args) {
      this.rangeValue = [new Date(args.start), new Date(args.end)];
      console.log('Range changed:', args.start, args.end);
    }
  }
};
</script>
```

## Common Patterns

### Pattern 1: Range Navigator with Period Selector

The correct period-selector settings property is `periods`, not `intervals`, and the `PeriodSelector` module must be injected. Also, because this example renders a series, the `dataSource` belongs on `<e-rangenavigator-series>`. 

```vue
<template>
  <ejs-rangenavigator
    :valueType="valueType"
    :value="rangeValue"
    :labelFormat="labelFormat"
    :periodSelectorSettings="periodSettings"
  >
    <e-rangenavigator-series-collection>
      <e-rangenavigator-series
        :dataSource="chartData"
        xName="date"
        yName="value"
        type="Area"
        :width="2"
      />
    </e-rangenavigator-series-collection>
  </ejs-rangenavigator>
</template>

<script setup>
import { provide, ref } from 'vue';
import {
  RangeNavigatorComponent as EjsRangenavigator,
  RangenavigatorSeriesCollectionDirective as ERangenavigatorSeriesCollection,
  RangenavigatorSeriesDirective as ERangenavigatorSeries,
  AreaSeries,
  DateTime,
  PeriodSelector
} from '@syncfusion/ej2-vue-charts';

const valueType = 'DateTime';
const labelFormat = 'MMM-yy';

const rangeValue = ref([new Date(2023, 0, 1), new Date(2023, 11, 31)]);

const periodSettings = ref({
  position: 'Top',
  periods: [
    { text: '1M', interval: 1, intervalType: 'Months' },
    { text: '3M', interval: 3, intervalType: 'Months' },
    { text: '6M', interval: 6, intervalType: 'Months' },
    { text: '1Y', interval: 1, intervalType: 'Years' },
    { text: 'All' }
  ]
});

const chartData = ref([
  { date: new Date(2023, 0, 1), value: 100 },
  { date: new Date(2023, 1, 1), value: 105 },
  { date: new Date(2023, 2, 1), value: 111 },
  { date: new Date(2023, 3, 1), value: 120 }
]);

provide('rangeNavigator', [DateTime, AreaSeries, PeriodSelector]);
</script>
```

### Pattern 2: Synchronizing with Chart

The most reliable integration pattern is to update a reactive range state from the Range Navigator’s `changed` event and let the linked Chart or Grid consume that state through computed filtering or bound axis settings. 

```vue
<template>
  <div>
    <ejs-rangenavigator
      :valueType="valueType"
      :value="rangeValue"
      :labelFormat="labelFormat"
      @changed="onRangeChanged"
    >
      <e-rangenavigator-series-collection>
        <e-rangenavigator-series
          :dataSource="allChartData"
          xName="date"
          yName="value"
          type="Area"
          :width="2"
        />
      </e-rangenavigator-series-collection>
    </ejs-rangenavigator>

    <ejs-chart :primaryXAxis="primaryXAxis">
      <e-series-collection>
        <e-series
          :dataSource="filteredChartData"
          xName="date"
          yName="value"
          type="Line"
          :width="2"
          name="Filtered Data"
        />
      </e-series-collection>
    </ejs-chart>
  </div>
</template>

<script setup>
import { computed, provide, ref } from 'vue';
import {
  RangeNavigatorComponent as EjsRangenavigator,
  RangenavigatorSeriesCollectionDirective as ERangenavigatorSeriesCollection,
  RangenavigatorSeriesDirective as ERangenavigatorSeries,
  ChartComponent as EjsChart,
  SeriesCollectionDirective as ESeriesCollection,
  SeriesDirective as ESeries,
  AreaSeries,
  LineSeries,
  DateTime
} from '@syncfusion/ej2-vue-charts';

const valueType = 'DateTime';
const labelFormat = 'MMM-yy';

const allChartData = ref([
  { date: new Date(2023, 0, 1), value: 100 },
  { date: new Date(2023, 0, 15), value: 110 },
  { date: new Date(2023, 1, 1), value: 105 },
  { date: new Date(2023, 1, 15), value: 120 },
  { date: new Date(2023, 2, 1), value: 130 }
]);

const rangeValue = ref([new Date(2023, 0, 1), new Date(2023, 1, 28)]);

const filteredChartData = computed(() => {
  const [start, end] = rangeValue.value;
  return allChartData.value.filter(item => item.date >= start && item.date <= end);
});

const primaryXAxis = {
  valueType: 'DateTime',
  labelFormat: 'MMM-yy'
};

const onRangeChanged = (args) => {
  rangeValue.value = [new Date(args.start), new Date(args.end)];
};

provide('rangeNavigator', [DateTime, AreaSeries, LineSeries]);
</script>
```

### Pattern 3: Lightweight Mode for Mobile

The supported lightweight pattern is **not** a special set of thumb-only properties. Instead, Syncfusion documents lightweight mode as the state where no series is rendered and data is bound directly on the root Range Navigator with `dataSource`, `xName`, and `yName`. 

```vue
<template>
  <ejs-rangenavigator
    :valueType="valueType"
    :intervalType="intervalType"
    :value="rangeValue"
    :labelFormat="labelFormat"
    :dataSource="dataSource"
    xName="x"
    yName="y"
  />
</template>

<script setup>
import { provide, ref } from 'vue';
import {
  RangeNavigatorComponent as EjsRangenavigator,
  DateTime
} from '@syncfusion/ej2-vue-charts';

const valueType = 'DateTime';
const intervalType = 'Months';
const labelFormat = 'MMM';
const rangeValue = ref([new Date(2023, 5, 1), new Date(2023, 6, 1)]);

const dataSource = ref([
  { x: new Date(2023, 0, 1), y: 10 },
  { x: new Date(2023, 1, 1), y: 14 },
  { x: new Date(2023, 2, 1), y: 18 },
  { x: new Date(2023, 3, 1), y: 15 },
  { x: new Date(2023, 4, 1), y: 22 },
  { x: new Date(2023, 5, 1), y: 25 },
  { x: new Date(2023, 6, 1), y: 27 }
]);

provide('rangeNavigator', [DateTime]);
</script>
```

## Key Configuration Properties

| Property | Purpose | Example |
|---|---|---|
| `value` | Selected range as `[start, end]`.  | `[new Date(2023, 0, 1), new Date(2023, 3, 30)]` |
| `dataSource` | Root data source in lightweight mode, or series-level data source when a series is rendered.  | `[{ x: ..., y: ... }]` |
| `xName` | X-axis field binding.  | `"date"` |
| `yName` | Y-axis field binding.  | `"value"` |
| `type` | Range Navigator series type. Supported values are `Line`, `Area`, and `StepLine`.  | `"Area"` |
| `periodSelectorSettings` | Period-selector configuration object using the `periods` array.  | `{ periods: [...] }` |
| `tooltip` | Tooltip configuration object using supported properties such as `enable`, `displayMode`, `fill`, `border`, `opacity`, `template`, and `textStyle`.  | `{ enable: true, displayMode: 'OnDemand' }` |
| `navigatorBorder` | Border customization for the Range Selector.  | `{ width: 2, color: '#FF0000' }` |
| `enableRtl` | Enables right-to-left rendering.  | `true` |
| `height` | Component height.  | `"100px"` |
| `useGroupingSeparator` | Controls grouping separators in number formatting.  | `true` or `false` |

## API Reference

For detailed API documentation, use the corrected Vue documentation links below:  
- Range Navigator component API: `https://ej2.syncfusion.com/vue/documentation/api/range-navigator/index-default` 
- Range Navigator overview API: `https://ej2.syncfusion.com/vue/documentation/api/range-navigator/overview/` 
- Range Navigator series model API: `https://ej2.syncfusion.com/vue/documentation/api/range-navigator/rangenavigatorseriesmodel` 
- Vue 3 getting started: `https://ej2.syncfusion.com/vue/documentation/range-navigator/vue-3-getting-started` 
- Selecting range: `https://ej2.syncfusion.com/vue/documentation/range-navigator/selecting-range` 
- Series types: `https://ej2.syncfusion.com/vue/documentation/range-navigator/series-types` 
- Period selector: `https://ej2.syncfusion.com/vue/documentation/range-navigator/period-selector` 
- Lightweight mode: `https://ej2.syncfusion.com/vue/documentation/range-navigator/lightweight` 
- Tooltip: `https://ej2.syncfusion.com/vue/documentation/range-navigator/tool-tip` 

## Corrections Applied

- Replaced `@change` with `@changed` for Range Navigator event handling. 
- Added required Vue 3 `provide('rangeNavigator', [...])` module injection in runnable examples. 
- Kept `dataSource` on `e-rangenavigator-series` whenever a series is rendered, and used root-level `dataSource` only for lightweight mode. 
- Replaced `intervals` with the correct period-selector property `periods`. 
- Removed `format` from tooltip examples to align with your requested tooltip-validation rule, while keeping valid root `labelFormat` usage on the Range Navigator itself. 
- Corrected the API reference links to the current Syncfusion Vue documentation URLs. 