---
name: fleet-design-pattern-selection
description: How the architect selects design patterns — when each fits, when it doesn't, and how the choice flows into design_input contributions that engineers must follow.
---

# Design Pattern Selection — Architect's Decision Framework

You don't just "use a pattern." You SELECT a pattern based on the problem's constraints, justify the selection, and communicate it as a design_input contribution that the engineer treats as a requirement.

## The Selection Process

### Step 1: Identify the Problem Category

Before choosing a pattern, categorize what you're solving:

| Category | Characteristic | Candidate Patterns |
|----------|---------------|-------------------|
| External dependency | Code talks to API, database, or service | Adapter, Repository, Gateway |
| Complex creation | Object construction has many steps or variants | Builder, Factory, Abstract Factory |
| Event-driven behavior | Actions trigger reactions across components | Observer, Mediator, Event Bus |
| Algorithm variation | Same interface, different implementations | Strategy, Template Method |
| Access control | Need to control or enhance access to something | Proxy, Decorator |
| Structural simplification | Complex subsystem needs a simple interface | Facade, Adapter |
| State management | Object behavior depends on internal state | State, FSM |

### Step 2: Evaluate Against Fleet Constraints

The fleet has specific architectural principles that constrain pattern selection:

**Onion architecture:** Inner layers (core/) MUST NOT depend on outer layers (infra/). This means:
- Repository pattern for data access: core/ defines interface, infra/ implements
- Adapter pattern for external services: core/ defines port, infra/ provides adapter
- NO direct imports from infra/ in core/ — even for "convenience"

**Single Responsibility:** Each module/class does ONE thing. A "service" that reads config, calls an API, transforms data, AND writes results is 4 responsibilities. Split it.

**Dependency direction:** Always inward. `fleet/mcp/tools.py` calls `fleet/core/contributions.py`, never the reverse. If core needs something from mcp, define an interface in core and inject from mcp.

### Step 3: Select and Justify

Your design_input contribution must include:
1. **Pattern name** — what you chose
2. **Why this pattern** — what problem characteristic matches
3. **Why NOT alternatives** — what you considered and rejected
4. **Target files** — where the pattern applies (specific paths)
5. **Constraints** — what the engineer MUST follow (dependency direction, interface boundaries)

### Common Patterns in the Fleet Codebase

| Pattern | Where It's Used | Why |
|---------|----------------|-----|
| Repository | mc_client.py, plane_client.py | Isolate data access from business logic |
| Adapter | gh_client.py, ntfy_client.py | External services behind stable interfaces |
| Builder | event_chain.py (chain builders) | Complex event chains built step by step |
| Strategy | backend_router.py | Multiple routing strategies, same interface |
| Observer | _emit_event() pattern | Tools emit, multiple systems react |
| Facade | context_assembly.py | Complex multi-source data behind one call |
| Template Method | role_providers.py | Base provider pattern, role-specific overrides |
| Mediator | ChainRunner | Coordinates operations across 6 surfaces |

### Anti-Patterns to Flag

When you see these in a task's codebase area, flag them in your design_input:

- **God class** — one module doing everything. Split by responsibility.
- **Circular dependency** — A imports B, B imports A. Introduce interface.
- **Leaky abstraction** — core/ code that knows about HTTP status codes or SQL syntax.
- **Premature abstraction** — Abstract base class with exactly one implementation. Wait for the second case.
- **Config in code** — Magic numbers, hardcoded URLs. These belong in config/ YAML files (fleet's IaC principle).

## Phase-Appropriate Design Depth

| Phase | Design Depth | What to Include |
|-------|-------------|----------------|
| poc | Minimal. Pick the obvious pattern. | "Use Repository for data access. Target: X.py" |
| mvp | Moderate. Consider alternatives. | Pattern + why + 1 alternative rejected + constraints |
| staging | Thorough. Full evaluation. | Pattern + 3 alternatives + performance implications + migration path |
| production | Complete. Production-grade. | Everything above + scalability analysis + failure modes + monitoring hooks |

Your `arch_design_contribution` group call reads the delivery phase and adjusts the template accordingly. Follow its guidance on depth.
