---
name: architecture-review
description: "Reviews the system architecture for structural issues, dependency cycles, layer violations, scalability concerns, and single points of failure. Use for periodic health checks or before major new features."
argument-hint: "[component, module, or 'full' for entire project]"
allowed-tools: Read, Grep, Glob, Bash
---

# Architecture Review

## Project Structure
!`find . -type f -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/vendor/*" -not -path "*/__pycache__/*" -not -path "*/target/*" -not -path "*/bin/*" -not -path "*/obj/*" -not -path "*/.next/*" -not -path "*/dist/*" -not -path "*/build/*" 2>/dev/null | head -80`

## Directory Layout
!`tree -L 3 -I "node_modules|.git|vendor|__pycache__|target|bin|obj|.next|dist|build" 2>/dev/null || find . -type d -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/vendor/*" -maxdepth 3 2>/dev/null`

## Package/Module Config
!`cat package.json go.mod Cargo.toml pyproject.toml requirements.txt *.csproj pom.xml 2>/dev/null | head -60`

---

## Review Areas

### 1. Project Structure & Organization
- Is the directory layout clear and consistent?
- Does it follow established conventions for the stack? (e.g., src/, app/, lib/, pkg/)
- Are related files co-located or scattered?
- Is there a clear entry point?

### 2. Dependency Architecture
- Map the dependency graph between major modules/packages
- Identify **circular dependencies** — modules that import each other
- Check for **layer violations** — e.g., presentation layer importing directly from data layer
- Look for **god modules** — modules that everything depends on
- Assess coupling: can modules be changed independently?

### 3. Separation of Concerns
- Is business logic separated from framework/transport code?
- Are side effects (I/O, network, database) isolated at boundaries?
- Is configuration separated from code?
- Are there clear interfaces between layers?

### 4. Scalability Considerations
- Stateless vs stateful components — which components hold state?
- Are there bottlenecks that would fail under load?
- Database query patterns — are they efficient at scale?
- Caching strategy — what is cached, where, and when invalidated?
- Background job handling — how are long-running tasks managed?

### 5. Reliability & Resilience
- **Single points of failure**: What happens if any component goes down?
- **Error boundaries**: Where do errors propagate, and are they caught?
- **Retry logic**: For external service calls, is there retry with backoff?
- **Graceful degradation**: Does the system handle partial failures?
- **Health checks**: Are there endpoints or mechanisms to monitor health?

### 6. Security Architecture
- Authentication and authorization boundaries
- Where is input validation enforced?
- How are secrets managed?
- API rate limiting and abuse prevention

---

## Output Format

### Architecture Diagram (ASCII)
```
┌─────────┐     ┌─────────┐     ┌──────────┐
│ Frontend │────▶│   API   │────▶│ Database │
└─────────┘     └─────────┘     └──────────┘
                     │
                     ▼
               ┌───────────┐
               │  External  │
               │  Services  │
               └───────────┘
```

### Findings Table
| # | Area | Finding | Severity | Recommendation |
|---|------|---------|----------|----------------|

### Top Recommendations
Prioritized list of the most impactful architectural improvements.

### Overall Health
Rate: Healthy / Needs Attention / At Risk — with reasoning.
