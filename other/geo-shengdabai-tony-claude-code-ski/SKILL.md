---
name: geo
description: "Route GEO and generative engine optimization requests to an available GEOHub capability. Use for GEO, AI search visibility, citation readiness, AI 搜索优化、AI 搜索可见度、生成式引擎优化、引用准备度, GEOHub workflow selection, capability checks, or requests spanning discovery, brand/site/page diagnosis, content, strategy, knowledge, publishing, SEO planning, and measurement. Do not use for geospatial, geolocation, maps, GIS, or GeoJSON tasks."
---

# GEOHub

## Workflow

1. Use this Skill directory as the working directory, then read `references/routing-contract.md` and the suite resolver contract at `references/RESOLVER.md`.
2. Run the deterministic `.venv/bin/python scripts/run_route.py --text "<request>"` wrapper.
3. Dispatch only when the JSON result has 'runnable: true' and a non-null 'entry'; read the reported provider entry and follow it using this Skill directory as the working directory.
4. For 'pending-implementation' or 'planned', return the registry status and suggested available route exactly as reported.

## Output contract

Return the selected skill ID, lifecycle status, runnable flag, reason, entry path, suggestion, and optional stable workflow DAG. Preserve uncertainty when two routes have the same score.

## Boundaries

This skill selects capabilities. It does not generate discovery artifacts or simulate unavailable stages.
