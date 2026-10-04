---
name: kaizen-cause-and-effect
description: Fishbone diagram across the 6M cause categories.
argument-hint: problem description
---

# Cause and Effect Analysis

Apply Fishbone (Ishikawa) diagram analysis to systematically explore all potential causes of a problem across multiple categories.

## Description
Systematically examine potential causes across six categories: People, Process, Technology, Environment, Methods, and Materials. Creates structured "fishbone" view identifying contributing factors.

## Usage
`/cause-and-effect [problem_description]`

## Variables
- PROBLEM: Issue to analyze (default: prompt for input)
- CATEGORIES: Categories to explore (default: all six)

## Steps
1. State the problem clearly (the "head" of the fish)
2. For each category, brainstorm potential causes:
   - **People**: Skills, training, communication, team dynamics
   - **Process**: Workflows, procedures, standards, reviews
   - **Technology**: Tools, infrastructure, dependencies, configuration
   - **Environment**: Workspace, deployment targets, external factors
   - **Methods**: Approaches, patterns, architectures, practices
   - **Materials**: Data, dependencies, third-party services, resources
3. For each potential cause, ask "why" to dig deeper
4. Identify which causes are contributing vs. root causes
5. Prioritize causes by impact and likelihood
6. Propose solutions for highest-priority causes

## Examples

### Example 1: API Response Latency

```
Problem: API responses take 3+ seconds (target: <500ms)

PEOPLE
├─ Team unfamiliar with performance optimization
├─ No one owns performance monitoring
└─ Frontend team doesn't understand backend constraints

PROCESS
├─ No performance testing in CI/CD
├─ No SLA defined for response times
└─ Performance regression not caught in code review

TECHNOLOGY
├─ Database queries not optimized
│  └─ Why: No query analysis tools in place
├─ N+1 queries in ORM
│  └─ Why: Eager loading not configured
├─ No caching layer
│  └─ Why: Redis not in tech stack
└─ Synchronous external API calls
   └─ Why: No async architecture in place

ENVIRONMENT
├─ Production uses smaller database instance than needed
├─ No CDN for static assets
└─ Single region deployment (high latency for distant users)

METHODS
├─ REST API design requires multiple round trips
├─ No pagination on large datasets
└─ Full object serialization instead of selective fields

MATERIALS
├─ Large JSON payloads (unnecessary data)
├─ Uncompressed responses
└─ Third-party API (payment gateway) is slow
   └─ Why: Free tier with rate limiting

ROOT CAUSES:
- No performance requirements defined (Process)
- Missing performance monitoring tooling (Technology)
- Architecture doesn't support caching/async (Methods)

SOLUTIONS (Priority Order):
1. Add database indexes (quick win, high impact)
2. Implement Redis caching layer (medium effort, high impact)
3. Make external API calls async with webhooks (high effort, high impact)
4. Define and monitor performance SLAs (low effort, prevents regression)
```

## Notes
- Fishbone reveals systemic issues across domains
- Multiple causes often combine to create problems
- Don't stop at first cause in each category—dig deeper
- Some causes span multiple categories (mark them)
- Root causes usually in Process or Methods (not just Technology)
- Use with `/why` command for deeper analysis of specific causes
- Prioritize solutions by: impact × feasibility ÷ effort
- Address root causes, not just symptoms

