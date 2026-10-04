---
name: team-topologies
description: >
  Knowledge base for Team Topologies concepts — the framework for organizing business and technology teams for fast flow.
  Use this skill whenever the user asks about: team types (stream-aligned, platform, enabling, complicated subsystem), team interaction modes (collaboration, X-as-a-Service, facilitation), cognitive load management, Thinnest Viable Platform (TVP), Conway's Law in relation to org design, or any question about how software delivery teams should be structured, named, or coordinated. Also use when another skill needs Team Topologies vocabulary to reason about org design, team responsibilities, or team dependencies.
---

# Team Topologies Knowledge Base

Team Topologies is an approach to designing team-of-teams organizations for fast flow of value. It provides a shared vocabulary and practical patterns for how to structure, name, and evolve software delivery teams at scale.

The central insight: organizational design is not a one-time event. Teams and their interactions must evolve continuously as products, architectures, and business needs change.

## Four Fundamental Team Types

Every team in the organization should map to exactly one of these types. Hybrids create confusion and slow delivery.

### 1. Stream-aligned team

The primary team type. Delivers direct, continuous value to customers aligned to a business domain or value stream. Owns outcomes end-to-end — no handoffs to other teams to complete delivery.

- Long-lived, stable membership
- Full responsibility for the product/service lifecycle
- Should be the most common team type in the organization
- All other team types exist to serve or support stream-aligned teams

### 2. Platform team

Creates and operates an internal platform — a curated set of services, tools, and APIs — that reduces cognitive load on stream-aligned teams. The platform is treated as a product with its own roadmap and customers (the stream-aligned teams).

- Exposes capabilities via APIs and self-service interfaces
- Avoids building bespoke solutions for individual consumers
- Success metric: stream-aligned teams move faster because of the platform, not in spite of it

### 3. Enabling team

A temporary specialist team that helps other teams acquire missing capabilities. Works *with* a team for a defined period to raise its effectiveness, then moves on — it does not take over work.

- Acts as a coach or consultant, not a dependency
- Focused on capability transfer, not permanent support
- Should make itself unnecessary over time
- Often composed of senior engineers, SREs, or domain specialists

### 4. Complicated Subsystem team

Handles a component so technically complex that it requires dedicated specialist expertise (e.g., complex mathematical models, signal processing, graphics rendering engines). Stream-aligned teams consume the output but cannot reasonably own it.

- Only created when the complexity genuinely exceeds what a stream-aligned team can absorb
- Avoids becoming a bottleneck by providing a clean, well-documented interface
- Should be the rarest team type

## Three Team Interaction Modes

Replaces vague "coordination" mandates with precise, intentional interaction contracts between teams. Every team-to-team relationship should be explicitly categorized as one of these three modes.

### 1. Collaboration

Two teams work closely together for a defined period to discover new things — to explore a problem space, prototype, or learn. High bandwidth, high cost. Suitable for innovation phases but not sustainable long-term.

- Has a clear goal and end date
- Both teams share responsibility for the outcome
- Expected to transition to X-as-a-Service or facilitation once the discovery phase ends

### 2. X-as-a-Service

One team provides a well-defined service; another team consumes it with minimal ongoing interaction. Low coordination overhead, clear boundaries. The "X" is whatever is being provided (platform, library, API, tool).

- Consumer team expects a stable, self-service interface
- Provider team owns reliability and evolution of the service
- The goal of most platform-to-stream-aligned team relationships

### 3. Facilitation

One team (typically an enabling team) helps another team overcome an obstacle, improve practices, or acquire skills. The facilitating team does not own the work — it enables the other team to do the work better.

- Temporary and focused on a specific capability gap
- Success means the other team no longer needs facilitation
- Distinct from collaboration: the receiving team does the work; the facilitating team coaches

## Guiding Principles

These distill the mindset Team Topologies argues for. The book does not publish them as a fixed numbered canon — treat them as recurring principles, not a checklist.

1. **Focus on Flow, Not Structure** — Org structure should serve value delivery speed, not the other way around. Reorganizations that optimize for hierarchy over flow slow organizations down.

2. **High Trust Is Non-Negotiable** — Low trust generates defensive processes and documentation that add friction without adding value. Trust enables fast, lightweight coordination.

3. **Keep Teams Together** — Stable teams accumulate shared context and communication shorthand that dramatically accelerates delivery. Constant team shuffling destroys this capital.

4. **Respect Cognitive Limits** — Teams have finite mental bandwidth. Adding responsibilities without removing others degrades decision quality and delivery speed.

5. **Make Changes Small and Safe** — For both products and team design, incremental continuous improvement outperforms infrequent large-scale changes.

6. **Connect Teams Directly to Customers** — Layers of management between teams and customers distort feedback and slow adaptation. Direct exposure improves prioritization.

7. **Embrace Complexity, Don't Fight It** — Modern sociotechnical systems are complex and adaptive. Design for evolution, not a fixed end state.

8. **Foster Continuous Discovery** — Teams need dedicated exploration time. Innovation comes from team experimentation, not executive mandate.

9. **Eliminate Team Dependencies** — Handoff delays between teams are a primary source of delivery drag. Minimize required coordination paths.

## Recurring Patterns

The practices below recur across Team Topologies adoptions.

### Managing Team Cognitive Load

Actively monitor and reduce unnecessary complexity a team must hold. Signs of overload: slow decisions, missed SLAs, high error rates, team frustration. The platform team's primary value proposition is offloading cognitive load from stream-aligned teams.

### Thinnest Viable Platform (TVP)

Build platforms that provide *just enough* capability to meaningfully accelerate stream-aligned teams — not everything imaginable. Bloated internal platforms become slow, opinionated bottlenecks that impede rather than enable. Start with the minimum and grow based on actual consumer need.

### Flexible Team Boundaries

Team responsibilities should evolve as products and technologies change. Boundaries set today may not be right in six months. Plan for intentional boundary reviews.

### Continuous Adaptation

Organizational design accumulates debt just like software. Build feedback loops into team design: regular team topology reviews, interaction mode retrospectives, cognitive load assessments.

## Related Concepts

**Conway's Law**: Organizations design systems that mirror their own communication structures. Team Topologies uses this deliberately — structure teams to produce the architecture you want, rather than fighting against the communication structures you have.

**Inverse Conway Maneuver**: The deliberate application of Conway's Law — change team and organizational structure first so that it nudges the system toward the desired software architecture, instead of letting an existing org chart dictate (and ossify) the architecture by accident.

**Fracture Planes**: Natural seams along which a software system can be split so each part can be owned by a single team with manageable cognitive load. Common planes include business-domain boundaries, regulatory/compliance, change cadence, team location, risk, performance isolation, and technology. The litmus test: a good fracture plane yields more autonomous teams with reduced cognitive load.

**Team Cognitive Load**: The total amount of mental effort required from a team at any given time. Broken into: intrinsic (core task complexity), extraneous (unnecessary friction), and germane (learning and improvement). Team Topologies aims to minimize extraneous and manage intrinsic load.

**Fast Flow**: The organizational goal — moving work from idea to customer value with minimal organizational friction, handoffs, or waiting time.

**Team API**: The interface a team exposes to the rest of the organization — its code and services, documentation, communication channels, working practices, and principles. A clear Team API reduces the cost of interaction with that team.
