---
name: bl1nk-architect-v2
description: Complete reference for Bl1nk Architect v2.0 - Full-stack GitHub repository analyzer with notifications (Slack, Linear, ClickUp) and beautiful widget reporting. Use when building notification systems, creating analysis reports, integrating team platforms, or deploying analysis workflows. Includes comprehensive API reference, setup guides, integration examples, and troubleshooting.
---

# Bl1nk Architect v2.0 Skill

**Enterprise-grade repository analysis with intelligent notifications and beautiful reporting**

## Quick Reference

**What this Skill provides:**
- Complete Bl1nk Architect v2.0 documentation and implementation guide
- 3 notification platform integrations (Slack, Linear, ClickUp)
- 5 beautiful widget components for reporting
- Enhanced orchestrator with integrated notifications
- Full API reference and integration guides
- Setup procedures, deployment options, and troubleshooting

## When to Use This Skill

Use this Skill when you need to:

1. **Build notification systems** - Integrate Slack, Linear, or ClickUp for team alerts
2. **Create analysis reports** - Generate beautiful widget-based analysis dashboards
3. **Setup repository analysis** - Deploy Bl1nk Architect for GitHub repo analysis
4. **Integrate multiple platforms** - Send notifications across Slack, Linear, ClickUp simultaneously
5. **Deploy to production** - Setup on Modal, Docker, or local environment
6. **Troubleshoot issues** - Resolve notification or widget rendering problems
7. **Migrate from v1** - Upgrade from Bl1nk Architect v1.0 to v2.0
8. **Extend functionality** - Add custom notifications or widgets

## Key Components

### 1. Notification System (3 Platforms)

**Slack Webhooks**
- Rich formatted messages with metric cards
- Color-coded status indicators
- Direct channel delivery
- Setup: 5 minutes

**Linear API (GraphQL)**
- Automatic issue creation
- Field population and team assignment
- Full error handling
- Setup: 10 minutes

**ClickUp API (REST)**
- Task creation in projects
- Priority and status management
- Detailed descriptions
- Setup: 10 minutes

**Notification Manager**
- Multi-channel orchestration
- User preference registry
- Concurrent delivery
- Task ID linking

### 2. Widget System (5 Components)

| Widget | Purpose | Export Formats |
|--------|---------|-----------------|
| AnalysisCard | Display metrics with icons | Markdown, HTML |
| ProgressBar | Visual progress indicators | Markdown, HTML |
| MetricsRow | Data in table format | Markdown, HTML |
| AnalysisPanel | Complete dashboard | Markdown, HTML |
| Report Generator | Pre-built analysis reports | Markdown |

### 3. Enhanced Orchestrator v2

- Integrated notifications after analysis
- Widget-based reporting
- Task ID linking
- 8-step workflow with progress streaming
- Complete error handling

## Quick Start Examples

### Setup Slack Notifications

```python
from src.notifications import get_notification_manager

nm = get_notification_manager()
nm.register_slack(
    user_id="user_123",
    webhook_url="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
)
```

### Create Beautiful Report

```python
from src.widgets import create_analysis_report

report = create_analysis_report(
    title="Repository Analysis",
    repository="my-repo",
    files_count=245,
    duplicates=[{"pattern": "validate", "count": 3}],
    python_deps=["django", "requests"],
    typescript_deps=["react", "axios"]
)
# Returns: Markdown-formatted report with cards, metrics, progress bars
```

### Use Enhanced Orchestrator

```python
from src.orchestrator_v2 import run_architect_workflow_v2

async for chunk in run_architect_workflow_v2(
    user_query="Analyze my repository",
    user_id="user_123",
    task_id="LIN-456"  # Optional task linking
):
    yield fp.PartialResponse(text=chunk)
    # Automatically sends notifications after analysis
```

## Important Files

**Main Documentation:**
- `COMPLETE_DOCUMENTATION.md` (2,001 lines) - Everything you need

**Source Code:**
- `src/notifications/` - Notification system (5 files, 400+ lines)
- `src/widgets/` - Widget components (2 files, 450+ lines)
- `src/orchestrator_v2.py` - Enhanced workflow (250+ lines)

**Navigation:**
- `INDEX.md` - Quick navigation guide

## API Reference

### NotificationManager

```python
nm = get_notification_manager()

# Register channels
nm.register_slack(user_id, webhook_url)
nm.register_linear(user_id, api_key, team_id, project_id)
nm.register_clickup(user_id, api_key, project_id)

# Send notifications
results = await nm.send_analysis_notification(
    user_id, title, summary, details, task_id
)
# Returns: {"slack": True, "linear": True, "clickup": False}

# Manage preferences
prefs = nm.registry.get_user_preferences(user_id)
nm.registry.disable_notification(user_id, channel)
```

### Widget Components

```python
from src.widgets import (
    AnalysisCard, ProgressBar, MetricsRow, 
    AnalysisPanel, create_analysis_report
)

# Each widget supports:
widget.to_markdown()  # Export as Markdown
widget.to_html()      # Export as HTML
```

## Setup Checklist

- [ ] Read COMPLETE_DOCUMENTATION.md → Overview section
- [ ] Install dependencies: `pip install -e ".[dev]"`
- [ ] Setup GitHub App (get APP_ID and PRIVATE_KEY)
- [ ] Get Gemini API key
- [ ] Choose notification platform(s) to setup
- [ ] Test locally: `python modal_app.py`
- [ ] Deploy to production (Modal/Docker/Local)

## Common Tasks

### Task: Add Slack Notifications

1. Get Slack webhook URL from https://api.slack.com/messaging/webhooks
2. Register with notification manager
3. Notifications send automatically after analysis
4. See COMPLETE_DOCUMENTATION.md → Notification System → Slack

### Task: Generate Beautiful Report

1. Collect analysis data
2. Call `create_analysis_report()`
3. Yield report to user
4. See COMPLETE_DOCUMENTATION.md → Widget System

### Task: Deploy to Production

1. Choose deployment option (Modal/Docker/Local)
2. Set environment variables
3. Follow deployment steps
4. See COMPLETE_DOCUMENTATION.md → Deployment

### Task: Troubleshoot Issues

1. Check logs for error details
2. Review relevant troubleshooting section
3. Verify API credentials and URLs
4. Test in isolation
5. See COMPLETE_DOCUMENTATION.md → Troubleshooting

## Documentation Structure

**COMPLETE_DOCUMENTATION.md contains:**

1. Overview - Project description and key features
2. Changelog - Detailed v1.0 vs v2.0 comparison
3. System Architecture - Design patterns and data flow
4. Notification System - Complete Slack/Linear/ClickUp setup
5. Widget System - All 5 components detailed
6. Enhanced Orchestrator - Workflow steps and error handling
7. Installation & Setup - Step-by-step guides
8. API Reference - All methods documented
9. Integration Guides - 3 complete code examples
10. Deployment - Local/Modal/Docker options
11. Testing & QA - Unit, integration, manual tests
12. Troubleshooting - 15+ common issues with solutions
13. Migration Guide - v1 to v2 upgrade path

## Code Examples

**100+ examples throughout documentation:**
- Notification setup (all 3 platforms)
- Widget creation and customization
- Orchestrator usage
- Error handling patterns
- Integration patterns
- Deployment procedures

## Version Information

- **Current Version:** 2.0.0 (December 2024)
- **Status:** ✅ Production Ready
- **Previous Version:** 1.0.0 (stable, still supported)

**What's New in v2.0:**
- ✨ Notification System (3 platforms)
- ✨ Beautiful Widget System (5 components)
- ✨ Enhanced Orchestrator with notifications
- ✅ 2,001 lines comprehensive documentation
- ✅ 100+ code examples
- ✅ Full backward compatibility with v1

## Getting Help

**Step 1:** Check COMPLETE_DOCUMENTATION.md
- Has 90% of answers
- Use Ctrl+F to search

**Step 2:** Navigate with INDEX.md
- Quick links to all sections
- Task-based navigation

**Step 3:** Review examples
- 100+ code examples throughout
- Copy-paste ready

**Step 4:** Check Troubleshooting
- 15+ common issues
- Diagnosis and solutions

## Next Steps

1. Open `/home/user/projects/bl1nk-architect/COMPLETE_DOCUMENTATION.md`
2. Read the Overview section (5 minutes)
3. Follow Quick Start section relevant to your task
4. Use INDEX.md for navigation
5. Reference API sections as needed

## Skills in Action

This Skill automatically activates when you:
- Ask about building notification systems
- Request help with Slack/Linear/ClickUp integration
- Need to create analysis reports
- Want to deploy repository analysis
- Need troubleshooting help
- Are migrating from v1
- Need API reference information

## Production Readiness

✅ Enterprise-grade code quality
✅ Complete error handling
✅ Security best practices
✅ Comprehensive testing guide
✅ Multiple deployment options
✅ Full backward compatibility
✅ Extensive documentation

---

**Start:** COMPLETE_DOCUMENTATION.md → Overview
**Navigate:** INDEX.md
**Reference:** See specific sections as needed

*Bl1nk Architect v2.0 - Ready for production deployment* 🚀
