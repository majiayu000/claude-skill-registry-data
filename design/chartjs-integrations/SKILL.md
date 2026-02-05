---
name: chartjs-integrations
description: This skill should be used when the user asks "Chart.js React", "react-chartjs-2", "Chart.js Vue", "vue-chartjs", "Chart.js Angular", "ng2-charts", "Chart.js Rails", "Chart.js Rails 8", "Chart.js importmaps", "Chart.js Stimulus", "Chart.js Turbo", "Chart.js Hotwire", "Chart.js SSR", "Chart.js Next.js", "Chart.js Nuxt", or needs help integrating Chart.js v4.5.1 with frontend frameworks.
---

# Chart.js Framework Integrations (v4.5.1)

Complete guide to integrating Chart.js with React, Vue, Angular, Rails 8, and other frameworks.

## React Integration (react-chartjs-2)

### Installation

```bash
npm install react-chartjs-2 chart.js
```

### Basic Usage

```jsx
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Register components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function BarChart() {
  const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: 'Sales',
      data: [12, 19, 3, 5, 2],
      backgroundColor: 'rgba(54, 162, 235, 0.5)'
    }]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Monthly Sales' }
    }
  };

  return <Bar data={data} options={options} />;
}
```

### Available Components

```jsx
import {
  Bar,
  Line,
  Pie,
  Doughnut,
  Radar,
  PolarArea,
  Bubble,
  Scatter
} from 'react-chartjs-2';
```

### Chart Reference

```jsx
import { useRef } from 'react';
import { Bar, getElementAtEvent } from 'react-chartjs-2';

function InteractiveChart() {
  const chartRef = useRef();

  const handleClick = (event) => {
    const element = getElementAtEvent(chartRef.current, event);
    if (element.length > 0) {
      const { datasetIndex, index } = element[0];
      console.log('Clicked:', datasetIndex, index);
    }
  };

  return (
    <Bar
      ref={chartRef}
      data={data}
      onClick={handleClick}
    />
  );
}
```

### Dynamic Updates

```jsx
import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

function LiveChart() {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [{
      label: 'Live Data',
      data: [],
      borderColor: 'rgb(75, 192, 192)'
    }]
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setChartData(prev => ({
        ...prev,
        labels: [...prev.labels, new Date().toLocaleTimeString()].slice(-10),
        datasets: [{
          ...prev.datasets[0],
          data: [...prev.datasets[0].data, Math.random() * 100].slice(-10)
        }]
      }));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return <Line data={chartData} />;
}
```

## Vue Integration (vue-chartjs)

### Installation

```bash
npm install vue-chartjs chart.js
```

### Vue 3 Composition API

```vue
<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const chartData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
  datasets: [{
    label: 'Sales',
    data: [12, 19, 3, 5, 2],
    backgroundColor: 'rgba(54, 162, 235, 0.5)'
  }]
};

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'top' }
  }
};
</script>
```

### Vue 3 Options API

```vue
<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script>
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default {
  components: { Bar },
  data() {
    return {
      chartData: {
        labels: ['Jan', 'Feb', 'Mar'],
        datasets: [{ label: 'Sales', data: [10, 20, 30] }]
      },
      chartOptions: {
        responsive: true
      }
    };
  }
};
</script>
```

### Reactive Updates in Vue

```vue
<template>
  <Line :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { ref, watch } from 'vue';
import { Line } from 'vue-chartjs';

const chartData = ref({
  labels: ['Jan', 'Feb', 'Mar'],
  datasets: [{
    label: 'Data',
    data: [10, 20, 30]
  }]
});

// Chart will automatically update when chartData changes
function updateData(newData) {
  chartData.value = {
    ...chartData.value,
    datasets: [{
      ...chartData.value.datasets[0],
      data: newData
    }]
  };
}
</script>
```

## Angular Integration (ng2-charts)

### Installation

```bash
npm install ng2-charts chart.js
```

### Module Setup

```typescript
// app.module.ts
import { NgModule } from '@angular/core';
import { NgChartsModule } from 'ng2-charts';

@NgModule({
  imports: [NgChartsModule]
})
export class AppModule {}
```

### Component Usage

```typescript
// chart.component.ts
import { Component } from '@angular/core';
import { ChartConfiguration, ChartType } from 'chart.js';

@Component({
  selector: 'app-chart',
  template: `
    <canvas baseChart
      [data]="barChartData"
      [options]="barChartOptions"
      [type]="barChartType">
    </canvas>
  `
})
export class ChartComponent {
  barChartType: ChartType = 'bar';

  barChartData: ChartConfiguration<'bar'>['data'] = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: 'Sales',
      data: [12, 19, 3, 5, 2],
      backgroundColor: 'rgba(54, 162, 235, 0.5)'
    }]
  };

  barChartOptions: ChartConfiguration<'bar'>['options'] = {
    responsive: true,
    plugins: {
      legend: { position: 'top' }
    }
  };
}
```

### Standalone Component (Angular 17+)

```typescript
import { Component } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-chart',
  standalone: true,
  imports: [BaseChartDirective],
  template: `
    <canvas baseChart
      [data]="chartData"
      [options]="chartOptions"
      type="bar">
    </canvas>
  `
})
export class ChartComponent {
  // ...
}
```

## Rails 8 Integration

Rails 8 offers multiple approaches for Chart.js integration.

### Option 1: Importmaps (Recommended)

```bash
# Pin Chart.js
bin/importmap pin chart.js
```

```javascript
// app/javascript/controllers/chart_controller.js
import { Controller } from "@hotwired/stimulus";
import Chart from "chart.js/auto";

export default class extends Controller {
  static targets = ["canvas"];
  static values = {
    type: { type: String, default: "bar" },
    data: Object,
    options: { type: Object, default: {} }
  };

  connect() {
    this.chart = new Chart(this.canvasTarget, {
      type: this.typeValue,
      data: this.dataValue,
      options: this.optionsValue
    });
  }

  disconnect() {
    if (this.chart) {
      this.chart.destroy();
    }
  }

  // Handle Turbo frame updates
  dataValueChanged() {
    if (this.chart) {
      this.chart.data = this.dataValue;
      this.chart.update();
    }
  }
}
```

```erb
<!-- app/views/charts/show.html.erb -->
<div data-controller="chart"
     data-chart-type-value="bar"
     data-chart-data-value="<%= @chart_data.to_json %>"
     data-chart-options-value="<%= @chart_options.to_json %>">
  <canvas data-chart-target="canvas"></canvas>
</div>
```

```ruby
# app/controllers/charts_controller.rb
class ChartsController < ApplicationController
  def show
    @chart_data = {
      labels: %w[Jan Feb Mar Apr May],
      datasets: [{
        label: 'Sales',
        data: [12, 19, 3, 5, 2],
        backgroundColor: 'rgba(54, 162, 235, 0.5)'
      }]
    }

    @chart_options = {
      responsive: true,
      plugins: {
        legend: { position: 'top' }
      }
    }
  end
end
```

### Option 2: esbuild/jsbundling-rails

```bash
# Gemfile
gem 'jsbundling-rails'

# Install
rails javascript:install:esbuild
npm install chart.js
```

```javascript
// app/javascript/application.js
import Chart from 'chart.js/auto';
window.Chart = Chart;
```

### Option 3: Propshaft + CDN

```erb
<!-- app/views/layouts/application.html.erb -->
<head>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
```

### Turbo Compatibility

Handle Turbo Drive page visits:

```javascript
// app/javascript/controllers/chart_controller.js
import { Controller } from "@hotwired/stimulus";
import Chart from "chart.js/auto";

export default class extends Controller {
  static targets = ["canvas"];
  static values = { config: Object };

  connect() {
    this.createChart();
  }

  disconnect() {
    this.destroyChart();
  }

  createChart() {
    const ctx = this.canvasTarget.getContext('2d');
    this.chart = new Chart(ctx, this.configValue);
  }

  destroyChart() {
    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }
  }

  // Re-render on Turbo cache restore
  reconnect() {
    this.destroyChart();
    this.createChart();
  }
}
```

### Turbo Streams Updates

```ruby
# Update chart via Turbo Stream
turbo_stream.replace "sales-chart" do
  render partial: "charts/sales", locals: { data: @new_data }
end
```

```erb
<!-- app/views/charts/_sales.html.erb -->
<div id="sales-chart"
     data-controller="chart"
     data-chart-config-value="<%= config.to_json %>">
  <canvas data-chart-target="canvas"></canvas>
</div>
```

### Rails Helper

```ruby
# app/helpers/chart_helper.rb
module ChartHelper
  def chart_tag(type:, data:, options: {}, **html_options)
    config = { type: type, data: data, options: options }

    content_tag :div,
      data: {
        controller: 'chart',
        chart_config_value: config.to_json
      },
      **html_options do
        content_tag :canvas, '', data: { chart_target: 'canvas' }
      end
  end
end
```

```erb
<%= chart_tag type: 'bar', data: @chart_data, options: @chart_options %>
```

## Vanilla JavaScript Patterns

### Module Pattern

```javascript
// chart-manager.js
export class ChartManager {
  constructor(canvasId, config) {
    this.canvas = document.getElementById(canvasId);
    this.chart = new Chart(this.canvas, config);
  }

  updateData(newData) {
    this.chart.data = newData;
    this.chart.update();
  }

  destroy() {
    this.chart.destroy();
  }
}
```

### Web Component

```javascript
class ChartComponent extends HTMLElement {
  connectedCallback() {
    const canvas = document.createElement('canvas');
    this.appendChild(canvas);

    const config = JSON.parse(this.getAttribute('config'));
    this.chart = new Chart(canvas, config);
  }

  disconnectedCallback() {
    if (this.chart) {
      this.chart.destroy();
    }
  }
}

customElements.define('chart-component', ChartComponent);
```

```html
<chart-component config='{"type":"bar","data":{"labels":["A","B"],"datasets":[{"data":[1,2]}]}}'></chart-component>
```

## Server-Side Rendering (SSR)

Chart.js requires a canvas element. For SSR:

### Next.js

```jsx
'use client';  // Mark as client component

import dynamic from 'next/dynamic';

const Chart = dynamic(
  () => import('react-chartjs-2').then(mod => mod.Bar),
  { ssr: false }
);

export default function Page() {
  return <Chart data={data} options={options} />;
}
```

### Nuxt 3

```vue
<template>
  <ClientOnly>
    <Bar :data="chartData" :options="chartOptions" />
  </ClientOnly>
</template>

<script setup>
import { Bar } from 'vue-chartjs';
// Register Chart.js components...
</script>
```

## Date Adapters

For time-based axes, install a date adapter:

```bash
# date-fns (recommended)
npm install chartjs-adapter-date-fns date-fns

# Moment.js
npm install chartjs-adapter-moment moment

# Luxon
npm install chartjs-adapter-luxon luxon

# Day.js
npm install chartjs-adapter-dayjs-4 dayjs
```

```javascript
// Import after Chart.js
import 'chartjs-adapter-date-fns';
```

## Additional Resources

- See `examples/rails-stimulus.md` for complete Rails 8 examples with Turbo integration
