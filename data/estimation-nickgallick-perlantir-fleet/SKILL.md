---
name: estimation
description: Project estimation and time management for agent-orchestrated builds.
---

# Estimation Framework

## Phase Time Estimates

### Simple project (landing page, 1-3 sections, no backend)
| Phase | Time |
|-------|------|
| Intake | 5 min |
| Research | 10-15 min |
| Design | 15-30 min (1-2 V0 generations) |
| Build | 30-60 min |
| Review | 10-15 min |
| QA | 10-30 min |
| Launch | 15-20 min |
| **Total** | **~2-3 hours** |

### Medium project (multi-page site, some interactivity, basic backend)
| Phase | Time |
|-------|------|
| Intake | 10 min |
| Research | 15-30 min |
| Design | 30-60 min (3-5 screens × V0 generate+review) |
| Build | 1-3 hours |
| Review | 15-30 min |
| Fix loop | 0-60 min (if needed) |
| QA | 15-30 min |
| Launch | 20-30 min |
| **Total** | **~4-8 hours** |

### Complex project (full app, auth, database, multiple user roles)
| Phase | Time |
|-------|------|
| Intake | 15 min |
| Research | 30-60 min |
| Design | 1-2 hours (5-10 screens) |
| Build | 3-8 hours |
| Review | 30-60 min |
| Fix loop | 30-90 min (likely needed) |
| QA | 30-60 min |
| Launch | 30 min |
| **Total** | **~8-24 hours** |

## Actual vs Estimated Log

### Brew & Bean (2026-03-20)
- **Type:** Simple (landing page, 5 sections, no backend)
- **Estimated:** ~2-3 hours
- **Actual:** ~75 min (intake to QA pass) + Launch
- **Variance:** -45 min (faster than estimate)
- **Notes:** Would have been faster without 3x QA loop on scroll animation bug. Wasted ~20 min on scrapped first build (pipeline skip). Fix loops added ~30 min.

## When to Re-Estimate
- Nick changes requirements → re-estimate immediately
- Research reveals unexpected complexity → re-estimate before design
- Forge blocks with 5+ P0 issues → add 1-2 hours for fix loop
- Agent unresponsive → add wait time + escalation buffer

## Changelog
- 2026-03-20: Initial estimation framework
- 2026-03-20: Added Brew & Bean actuals
