---
name: context-analytics
description: |
  Portfolio analytics, metrics calculation, performance tracking, and dashboard data. Use when working with analytics code, files, or integration. Invoke when navigating analytics codebase, searching for analytics files, debugging analytics errors, or discussing analytics patterns. Keywords: analytics, analytics
tags: []
---

# analytics Context

**Files:** 12 files, 2603 LOC

Quick navigation for analytics area. Indexed 2025-11-22.

## Quick Navigation

### Database (Active)
- supabase/migrations/20250925120003_analytics_engine_optimization_notes.sql ✅ CURRENT
- supabase/migrations/20250930201801_add_multi_level_analytics_functions.sql ✅ CURRENT
- supabase/migrations/20250930201803_add_multi_level_analytics_functions.sql ✅ CURRENT

### Frontend (Active)
- frontend/src/services/analyticsApi.ts ✅ CURRENT

### Frontend (Active)
- frontend/src/components/AnalyticsDashboard.tsx ✅ CURRENT

### Backend (Active)
- backend/analytics_supabase.py ✅ CURRENT

### Backend (Active)
- backend/api/analytics_api.py ✅ CURRENT
- backend/api/analytics_api_original.py ✅ CURRENT

### Backend (Active)
- backend/services/analytics_service.py ✅ CURRENT

### Backend (Deprecated)
- backend/api/analytics_api_backup.py ❌ DO NOT EDIT
- backend/api/analytics_api_backup_pre_clerk.py ❌ DO NOT EDIT

### Frontend (Test)
- frontend/src/__tests__/services/analyticsApi.test.ts 

## How to Use This Skill

**When navigating analytics code:**
- Use file paths with line numbers for precise navigation
- Check "CURRENT" markers for actively maintained files
- Avoid "DO NOT EDIT" files (backups, deprecated)
- Look for entry points (classes, main functions)

**Common tasks:**
- Find API endpoints: Look for `*_api.py:*` files
- Find business logic: Look for `*_service*.py` or engine classes
- Find data models: Look for `*_models.py` or schema definitions
- Find tests: Check "Tests" section

## Serena Quick Commands

```python
# Get symbol overview for a file
mcp__serena__get_symbols_overview(
  relative_path="<file_path_from_above>"
)

# Find specific symbol
mcp__serena__find_symbol(
  name_path="ClassName.method_name",
  relative_path="<file_path>",
  include_body=True
)

# Search for pattern
mcp__serena__search_for_pattern(
  substring_pattern="search_term",
  relative_path="<directory>"
)
```

## Maintenance

**Regenerate this skill:**
```bash
scripts/area-context-update analytics
```

**Edit area definition:**
```bash
# Edit .context/area-config.yml
# Then regenerate
scripts/area-context-update analytics
```

---

**Area:** analytics
**Last Updated:** 2025-11-22
**Maintenance:** Manual (regenerate as needed)
**Auto-activation:** Triggers on "analytics", "navigate analytics", "analytics files"
