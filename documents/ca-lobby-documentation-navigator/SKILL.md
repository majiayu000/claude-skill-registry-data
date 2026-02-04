---
name: CA Lobby Documentation Navigator
description: Navigate CA Lobby documentation structure quickly. Use when searching for CA Lobby docs, finding phase reports, locating master plan, or user says "find documentation". Provides instant access to project documentation.
version: 1.0.0
---

# CA Lobby Documentation Navigator

## Purpose
Provide quick navigation and discovery of CA Lobby project documentation.

## When This Activates
- User says "find documentation", "where is", "show me docs"
- User searching for specific documents
- User needs documentation reference

## CA Lobby Documentation Map

### Primary Documents

**Master Plan (START HERE):**
- `Documentation/General/MASTER_PROJECT_PLAN.md`
- Current status, phases, objectives

**Commit Strategy:**
- `Documentation/General/COMMIT_STRATEGY.md`
- Granular commit guidelines

**Skills System:**
- `Documentation/General/SKILLS_SYSTEM_SUMMARY.md`
- Skills system overview and status

### Phase Documentation

**Phase Plans:**
- `Documentation/Phase1/Plans/` - Phase 1 planning docs
- `Documentation/Phase2/Plans/` - Phase 2 planning docs

**Phase Reports:**
- `Documentation/Phase1/Reports/` - Phase 1 completion reports
- `Documentation/Phase2/Reports/` - Phase 2 completion reports

### Deployment Documentation

**Deployment Guides:**
- `Documentation/Deployment/DEPLOYMENT_REFERENCE.md`
- `Documentation/Deployment/VERCEL_DEPLOYMENT_REPORT.md`
- `Documentation/Deployment/BIGQUERY_COMPLETE_IMPLEMENTATION_GUIDE.md`

### Testing Documentation

**Testing Resources:**
- `Documentation/Testing/QUICK_TEST_REFERENCE.md`
- `Documentation/Testing/TEST_DATA_SEARCH_CASES.md`

### Feature Documentation

**Feature Specs:**
- `Documentation/Features/ORGANIZATION_PROFILE_PAGE_SPECIFICATION.md`

## Quick Reference Paths

| What You Need | Path |
|---------------|------|
| Master Plan | `Documentation/General/MASTER_PROJECT_PLAN.md` |
| Latest Phase Plan | `Documentation/Phase2/Plans/` (check most recent) |
| Latest Completion Report | `Documentation/Phase2/Reports/` (check most recent) |
| Deployment Info | `Documentation/Deployment/` |
| Testing Info | `Documentation/Testing/` |

## Search Tips

**By Phase:**
```bash
ls Documentation/Phase2/Plans/
ls Documentation/Phase2/Reports/
```

**By Type:**
```bash
find Documentation -name "*PLAN.md"
find Documentation -name "*REPORT.md"
```

---

## Changelog
### Version 1.0.0 (2025-10-20)
- Initial CA Lobby implementation
- Complete documentation map
- Quick reference paths

---

**End of Skill**
