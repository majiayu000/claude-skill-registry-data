---
name: performance-budget-enforcer
description: Monitors Lighthouse scores and JavaScript bundle sizes across deployments with automated alerts when performance thresholds are exceeded. This skill should be used when setting up performance monitoring, enforcing bundle size limits, tracking Lighthouse metrics, or adding performance regression detection. Use for performance budgets, bundle size, Lighthouse CI, performance monitoring, regression detection, or web vitals tracking.
---

# Performance Budget Enforcer

Implement automated performance monitoring and budget enforcement to prevent performance regressions in worldbuilding applications.

## Overview

To enforce performance budgets:

1. Define performance budgets for key metrics (bundle size, Lighthouse scores, Web Vitals)
2. Set up automated monitoring in CI/CD pipeline
3. Configure alerts for threshold violations
4. Generate performance reports and trends
5. Block deployments that exceed budgets

## Performance Metrics

### JavaScript Bundle Size

To monitor bundle sizes:

- **Initial Bundle**: First-load JS (target: <200KB)
- **Route Bundles**: Per-page JS (target: <50KB per route)
- **Total Bundle**: All JS combined (target: <500KB)
- **Vendor Bundle**: Third-party libraries (target: <150KB)

### Lighthouse Scores

To track Lighthouse metrics:

- **Performance**: Overall performance score (target: >90)
- **Accessibility**: A11y compliance (target: >90)
- **Best Practices**: Web standards compliance (target: >90)
- **SEO**: Search engine optimization (target: >90)

### Core Web Vitals

To measure user experience:

- **LCP** (Largest Contentful Paint): <2.5s
- **FID** (First Input Delay): <100ms
- **CLS** (Cumulative Layout Shift): <0.1
- **TTFB** (Time to First Byte): <600ms
- **FCP** (First Contentful Paint): <1.8s

Consult `references/performance-targets.md` for detailed target definitions and industry benchmarks.

## Budget Configuration

### Define Budgets

Create `performance-budget.json`:

```json
{
  "bundles": {
    "maxInitialBundle": 204800,
    "maxRouteBundle": 51200,
    "maxTotalBundle": 512000,
    "maxVendorBundle": 153600
  },
  "lighthouse": {
    "performance": 90,
    "accessibility": 90,
    "bestPractices": 90,
    "seo": 90
  },
  "webVitals": {
    "lcp": 2500,
    "fid": 100,
    "cls": 0.1,
    "ttfb": 600,
    "fcp": 1800
  },
  "assets": {
    "maxImageSize": 102400,
    "maxFontSize": 51200,
    "maxCssSize": 51200
  }
}
```

Use `scripts/generate_budget.py` to create initial budget configuration based on current metrics.

### Budget Levels

Define severity levels:

- **Error**: Block deployment (>20% over budget)
- **Warning**: Alert but allow (10-20% over budget)
- **Info**: Track but continue (<10% over budget)

## CI/CD Integration

### GitHub Actions Setup

To add performance checks to CI:

```yaml
name: Performance Budget

on:
  pull_request:
    branches: [main, master]

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build

      - name: Analyze bundle size
        run: npx @next/bundle-analyzer

      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun

      - name: Check performance budgets
        run: python scripts/check_budgets.py

      - name: Comment results on PR
        uses: actions/github-script@v7
        with:
          script: |
            const results = require('./performance-results.json');
            // Comment logic here
```

Use `assets/github-workflow.yml` for complete workflow template.

### Lighthouse CI Configuration

Create `lighthouserc.json`:

```json
{
  "ci": {
    "collect": {
      "startServerCommand": "npm run start",
      "url": ["http://localhost:3000", "http://localhost:3000/entities"],
      "numberOfRuns": 3
    },
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.9 }],
        "first-contentful-paint": ["error", { "maxNumericValue": 1800 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }]
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

Reference `assets/lighthouserc.json` for complete configuration.

## Bundle Analysis

### Next.js Bundle Analyzer

To analyze bundle composition:

```bash
# Install analyzer
npm install --save-dev @next/bundle-analyzer

# Add to next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // Next.js config
});

# Run analysis
ANALYZE=true npm run build
```

### Size Tracking

Use `scripts/track_bundle_size.py` to track bundle size over time:

```bash
python scripts/track_bundle_size.py --record
```

Store results in `performance-history/bundle-sizes.json` for trend analysis.

## Automated Alerts

### Threshold Violations

To configure alerts:

```typescript
// scripts/check_budgets.ts
interface BudgetCheck {
  metric: string;
  current: number;
  budget: number;
  status: 'pass' | 'warning' | 'error';
  percentOver: number;
}

function checkBudget(current: number, budget: number): BudgetCheck['status'] {
  const percentOver = ((current - budget) / budget) * 100;

  if (percentOver > 20) return 'error';
  if (percentOver > 10) return 'warning';
  return 'pass';
}
```

### Notification Channels

To send alerts:

- **GitHub PR Comments**: Automated comments with performance report
- **Slack**: Webhook notifications for violations
- **Email**: Digest of performance trends
- **Build Status**: Fail builds on error-level violations

Use `scripts/send_alerts.py` to integrate notification channels.

## Performance Monitoring

### Real User Monitoring (RUM)

To track real user metrics:

```typescript
// lib/web-vitals.ts
import { onCLS, onFID, onLCP, onFCP, onTTFB } from 'web-vitals';

export function reportWebVitals() {
  onCLS((metric) => sendToAnalytics(metric));
  onFID((metric) => sendToAnalytics(metric));
  onLCP((metric) => sendToAnalytics(metric));
  onFCP((metric) => sendToAnalytics(metric));
  onTTFB((metric) => sendToAnalytics(metric));
}

function sendToAnalytics(metric: Metric) {
  // Send to analytics service
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify(metric),
  });
}
```

Enable in `app/layout.tsx`:

```typescript
import { reportWebVitals } from '@/lib/web-vitals';

export default function RootLayout({ children }: { children: ReactNode }) {
  useEffect(() => {
    reportWebVitals();
  }, []);

  return <html>{children}</html>;
}
```

### Synthetic Monitoring

To run scheduled Lighthouse audits:

```yaml
# .github/workflows/scheduled-performance.yml
name: Scheduled Performance Audit

on:
  schedule:
    - cron: '0 0 * * *' # Daily at midnight

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - name: Run Lighthouse
        run: lhci autorun --config=lighthouserc.json

      - name: Store results
        run: python scripts/store_performance_data.py
```

## Performance Reports

### PR Comments

To generate PR comments with results:

```markdown
## Performance Report

### Bundle Size

- Initial Bundle: 185KB ([OK] under 200KB budget)
- Total Bundle: 480KB ([OK] under 500KB budget)

### Lighthouse Scores

- Performance: 92/100 ([OK] meets 90 target)
- Accessibility: 95/100 ([OK] meets 90 target)
- Best Practices: 88/100 ([WARN] below 90 target)

### Core Web Vitals

- LCP: 2.1s ([OK] under 2.5s)
- FID: 85ms ([OK] under 100ms)
- CLS: 0.05 ([OK] under 0.1)

### Bundle Comparison

| Route            | Current | Previous | Change  |
| ---------------- | ------- | -------- | ------- |
| /                | 185KB   | 180KB    | +5KB    |
| /entities        | 45KB    | 45KB     | No change |
| /entities/[id]   | 38KB    | 40KB     | -2KB [OK] |

[View detailed report](https://lighthouse-report-url)
```

Use `scripts/generate_pr_comment.py` to create formatted reports.

### Trend Analysis

To visualize performance trends:

```bash
python scripts/generate_trends.py --days 30 --output performance-trends.html
```

Generate charts showing:

- Bundle size over time
- Lighthouse scores history
- Web Vitals percentiles
- Performance budget compliance rate

Reference `assets/trend-visualization.html` for dashboard template.

## Optimization Strategies

### Bundle Size Reduction

To reduce bundle sizes:

1. **Code Splitting**: Split large components into separate chunks
2. **Tree Shaking**: Remove unused code with proper imports
3. **Dynamic Imports**: Load components on demand
4. **Lazy Loading**: Defer non-critical resources
5. **Compression**: Enable gzip/brotli compression
6. **Minification**: Ensure production builds are minified

### Image Optimization

To optimize images:

```typescript
import Image from 'next/image';

<Image
  src="/entity-map.png"
  alt="World Map"
  width={800}
  height={600}
  quality={75}
  loading="lazy"
  placeholder="blur"
/>
```

### Font Optimization

To optimize fonts:

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <html className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
```

### Third-Party Scripts

To optimize third-party scripts:

```typescript
import Script from 'next/script';

<Script
  src="https://analytics.example.com/script.js"
  strategy="lazyOnload"
/>
```

Consult `references/optimization-techniques.md` for comprehensive optimization guide.

## Best Practices

1. **Set Realistic Budgets**: Base on current metrics, improve gradually
2. **Monitor Continuously**: Track metrics on every deployment
3. **Act on Violations**: Investigate and fix budget overages promptly
4. **Educate Team**: Share performance impact of code changes
5. **Review Regularly**: Adjust budgets as app evolves
6. **Prioritize UX**: Focus on metrics that impact user experience
7. **Test Real Devices**: Verify performance on target devices

## Troubleshooting

Common issues:

- **Fluctuating Scores**: Run multiple Lighthouse audits, use median scores
- **CI vs Local**: Ensure CI environment matches production setup
- **False Positives**: Adjust budgets for legitimate growth
- **Missing Metrics**: Verify analytics integration and data collection
- **Slow CI**: Cache dependencies and optimize build process
- **Bundle Size Spikes**: Use bundle analyzer to identify culprits
