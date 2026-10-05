---
name: dash
version: 1.0.0
description: Build production-grade interactive dashboards with Plotly Dash - enterprise
  features, callbacks, and scalable deployment
type: reference
author: workspace-hub
category: data-analysis
capabilities:
- Production-ready dashboard development
- Reactive callbacks for interactivity
- Plotly visualization integration
- Multi-page application architecture
- Authentication and authorization
- Enterprise deployment options
- Custom components and extensions
tools:
- dash
- plotly
- dash-bootstrap-components
- dash-ag-grid
tags:
- dash
- dashboard
- plotly
- callbacks
- enterprise
- production
- interactive
- visualization
platforms:
- python
- web
related_skills:
- plotly
- streamlit
- polars
- pandas-data-processing
requires: []
scripts_exempt: true
---

# Dash

## When to Use This Skill

### USE Dash when:

- **Production dashboards** - Building dashboards for business users
- **Complex interactivity** - Need fine-grained control over updates
- **Enterprise requirements** - Authentication, scaling, reliability needed
- **Plotly ecosystem** - Already using Plotly for visualizations
- **Custom components** - Need to extend with JavaScript/React
- **Long-term projects** - Dashboard will be maintained and extended
- **Multi-user access** - Multiple concurrent users accessing dashboards
### DON'T USE Dash when:

- **Quick prototypes** - Use Streamlit for faster iteration
- **Simple visualizations** - Static reports may suffice
- **No interactivity needed** - Use static HTML/PDF reports
- **Limited Python knowledge** - Steeper learning curve than Streamlit
- **Single-user tools** - Jupyter notebooks may be simpler

## Prerequisites

```bash
# Basic installation
pip install dash

# With common extras
pip install dash plotly pandas dash-bootstrap-components

# Full installation
pip install dash plotly pandas polars dash-bootstrap-components dash-ag-grid gunicorn

# Using uv (recommended)
uv pip install dash plotly pandas dash-bootstrap-components dash-ag-grid
```

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Core application structure
  - Callbacks and interactivity
  - Layout components (HTML, DCC, Bootstrap)
  - Multi-page applications
  - Authentication patterns
  - Complete dashboard examples
  - Real-time monitoring example
  - AG Grid integration
  - Deployment patterns
  - Best practices and troubleshooting

## Resources

- **Official Docs**: https://dash.plotly.com/
- **Components**: https://dash.plotly.com/dash-core-components
- **Bootstrap Components**: https://dash-bootstrap-components.opensource.faculty.ai/
- **AG Grid**: https://dash.plotly.com/dash-ag-grid
- **Enterprise**: https://plotly.com/dash/
- **GitHub**: https://github.com/plotly/dash

---

**Build enterprise-grade interactive dashboards with Python and Plotly!**

## Sub-Skills

- [1. Basic Application Structure](1-basic-application-structure/SKILL.md)
- [2. Callbacks and Interactivity](2-callbacks-and-interactivity/SKILL.md)
- [3. Layout Components](3-layout-components/SKILL.md)
- [4. Bootstrap Components](4-bootstrap-components/SKILL.md)
- [5. Multi-Page Applications](5-multi-page-applications/SKILL.md)
- [6. Authentication](6-authentication/SKILL.md)
- [1. Optimize Callback Performance (+3)](1-optimize-callback-performance/SKILL.md)
- [Common Issues](common-issues/SKILL.md)

## Sub-Skills

- [Example 1: Sales Analytics Dashboard (+2)](example-1-sales-analytics-dashboard/SKILL.md)
- [Gunicorn Production Server (+2)](gunicorn-production-server/SKILL.md)
