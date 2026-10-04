---
name: smart-analytics
description: "Business analytics dashboard with real-time metrics, custom reports, and data visualization. Supports multiple data sources."
triggers:
  - "analytics dashboard"
  - "business metrics"
  - "数据分析"
  - "业务指标"
  - "generate report"
---

# Smart Analytics

Business intelligence and analytics platform.

## Features

- 📊 **Real-time Dashboards** — Live metrics and KPIs
- 📈 **Custom Reports** — Build custom analytics
- 🔗 **Multi-source** — Connect databases, APIs, CSV
- 📱 **Responsive** — Works on all devices
- 🔔 **Alerts** — Threshold-based notifications

## Data Sources

| Source | Type | Status |
|--------|------|--------|
| PostgreSQL | Database | ✅ |
| MySQL | Database | ✅ |
| MongoDB | Database | ✅ |
| REST API | API | ✅ |
| CSV/Excel | File | ✅ |
| Google Analytics | Service | ✅ |

## Usage

### Create Dashboard

```bash
# Create from template
hermes analytics create --template ecommerce

# Create custom
hermes analytics create --name "Sales Dashboard" \
  --metrics revenue,orders,conversion \
  --period 30d
```

### Generate Reports

```bash
# Weekly report
hermes analytics report --type weekly

# Custom report
hermes analytics report \
  --metrics revenue,users \
  --group-by region \
  --format pdf
```

### Real-time Monitoring

```bash
# Start live dashboard
hermes analytics live --port 3001

# Monitor specific metrics
hermes analytics watch --metric api_response_time
```

## Visualization Types

- 📊 Bar/Line/Area Charts
- 🥧 Pie/Donut Charts
- 📈 Sparklines
- 🗺️ Geographic Maps
- 📋 Data Tables
- 🎯 Gauge Charts

## Alert Configuration

```yaml
# analytics-alerts.yml
alerts:
  - name: "High Error Rate"
    metric: error_rate
    condition: "> 5%"
    notify: [telegram, email]
  
  - name: "Low Conversion"
    metric: conversion_rate
    condition: "< 2%"
    notify: [slack]
```

## Pitfalls

1. **Data Volume** — Large datasets may need pagination
2. **Real-time Costs** — Live queries can be expensive
3. **Cache Strategy** — Balance freshness vs performance
