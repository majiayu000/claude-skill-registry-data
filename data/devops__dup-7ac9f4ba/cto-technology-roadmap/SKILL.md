---
name: cto-technology-roadmap
description: Expert methodology for creating strategic technology roadmaps aligned with business goals, including multi-horizon planning, capacity planning, and OKR frameworks.
---

# CTO Technology Roadmap Skill

## Purpose

This skill provides a comprehensive approach to creating technology roadmaps that align engineering with business strategy. Use it to build multi-year technical visions, quarterly execution plans, balance competing priorities, and communicate strategy effectively.

## When to Use

Trigger this skill when you need to:

- Create annual or multi-year technology strategy
- Plan quarterly engineering initiatives
- Align engineering roadmap with product/business goals
- Communicate technical strategy to board or executives
- Balance innovation, technical debt, and feature delivery
- Plan infrastructure and platform investments
- Forecast engineering capacity and resource needs
- Evaluate emerging technologies and strategic bets

## Core Methodology

Follow this systematic approach to roadmap creation:

### Phase 1: Establish Strategic Context

1. **Understand Business Strategy**

   - What are company's strategic goals for next 1-3 years?
   - What's the target market and growth trajectory?
   - What's the competitive landscape?
   - What are the key business metrics we're optimizing for?

2. **Assess Current Technical State**

   - What's our current architecture and tech stack?
   - What's working well?
   - What are the pain points and bottlenecks?
   - What technical debt exists?
   - What's our team's capability and capacity?

3. **Identify Technical Enablers**
   - What technical capabilities are required to achieve business goals?
   - What are the dependencies and prerequisites?
   - What are the risks if we don't address technical needs?

Use `references/frameworks/strategic-alignment-framework.md` for structured analysis.

---

### Phase 2: Define Planning Horizons

Structure roadmap across three time horizons:

#### Horizon 1: Tactical (0-12 months)

**Focus**: Execution, delivery, near-term goals

**Characteristics**:

- High certainty and specificity
- Quarterly milestones
- Committed resources
- Clear success metrics

**Content**:

- Specific features and projects
- Team assignments
- Sprint-level planning
- Defined deliverables

---

#### Horizon 2: Strategic (1-3 years)

**Focus**: Platform, capabilities, strategic investments

**Characteristics**:

- Medium certainty
- Themes and initiatives vs specific features
- Resource allocation guidance
- Strategic bets

**Content**:

- Major platform investments
- Architecture transformations
- Team growth and skill development
- Technology strategy shifts

---

#### Horizon 3: Visionary (3-5 years)

**Focus**: Direction, possibilities, north star

**Characteristics**:

- Low certainty, high ambiguity
- Directional guidance
- Technology trends and opportunities
- Strategic positioning

**Content**:

- Technical vision
- Emerging technology exploration
- Market and competitive positioning
- Future capabilities

Use `references/templates/three-horizon-roadmap.md` for structure.

---

### Phase 3: Balance the Portfolio

Allocate resources across competing priorities:

#### The 70-20-10 Framework

**70% - Core Business** (Horizon 1)

- Features that serve current customers
- Revenue-generating initiatives
- Business-critical improvements
- Customer commitments

**20% - Strategic Investments** (Horizon 2)

- Platform and infrastructure
- Technical debt reduction
- Developer productivity
- Scalability and performance

**10% - Innovation & Exploration** (Horizon 3)

- Emerging technologies (AI, blockchain, etc.)
- Proof of concepts
- Competitive research
- Future capabilities

**Adjust based on company stage**:

| Stage               | Core | Strategic | Innovation |
| ------------------- | ---- | --------- | ---------- |
| Early Startup (PMF) | 85%  | 10%       | 5%         |
| Growth Stage        | 70%  | 20%       | 10%        |
| Scale/Enterprise    | 60%  | 30%       | 10%        |
| Innovation-Focused  | 50%  | 30%       | 20%        |

Use `references/frameworks/portfolio-balancing.md` for detailed guidance.

---

### Phase 4: Create the Roadmap

Build a visual, communicable roadmap:

#### Roadmap Components

1. **Strategic Themes** (3-5 themes)

   - Platform Modernization
   - AI-Powered Features
   - Developer Experience
   - Enterprise Readiness
   - Global Scale

2. **Key Initiatives** (under each theme)

   - Specific projects or workstreams
   - Aligned to theme
   - Clear owners

3. **Timeline**

   - Quarters or half-years
   - Dependencies visible
   - Critical path highlighted

4. **Success Metrics**

   - How will we measure success?
   - Business outcomes
   - Technical outcomes

5. **Resource Requirements**
   - Team size and composition
   - Budget implications
   - Hiring needs

Use `references/templates/roadmap-visualization.md` for formats.

---

### Phase 5: Align and Communicate

Tailor roadmap communication for each audience:

#### For Board/Investors

**Focus**: Strategic positioning, competitive advantage, risk management

**Format**: 3-5 year vision, key strategic bets, why we'll win

Use `references/templates/board-roadmap-presentation.md`

---

#### For CEO/Executives

**Focus**: Business alignment, resource requirements, dependencies

**Format**: Annual plan with quarterly milestones, business impact

Use `references/templates/executive-roadmap-presentation.md`

---

#### For Product Team

**Focus**: Feature enablement, platform capabilities, dependencies

**Format**: Integrated product + tech roadmap, shared milestones

Use `references/templates/product-tech-alignment.md`

---

#### For Engineering Team

**Focus**: Technical details, team assignments, skill development

**Format**: Detailed initiative breakdown, team roadmaps, learning paths

Use `references/templates/engineering-team-roadmap.md`

---

### Phase 6: Execute and Iterate

1. **Quarterly Planning**

   - Review progress on roadmap
   - Adjust based on learnings
   - Commit to next quarter's initiatives
   - Update roadmap and communicate changes

2. **Monthly Check-ins**

   - Track initiative progress
   - Identify blockers and risks
   - Ensure alignment with business changes

3. **Annual Strategy Review**
   - Major strategy refresh
   - Incorporate market changes
   - Adjust 3-year vision
   - Reset priorities

Use `references/frameworks/roadmap-governance.md` for process.

---

## Key Principles

- **Business-Aligned**: Every technical initiative should tie to business outcomes
- **Flexible, Not Rigid**: Roadmap is a plan, not a promise - adjust as needed
- **Multi-Horizon**: Balance short-term delivery with long-term vision
- **Resource-Aware**: Be realistic about capacity and dependencies
- **Transparent**: Share roadmap broadly, explain trade-offs
- **Outcome-Focused**: Define success by impact, not output

## Bundled Resources

**Frameworks** (`references/frameworks/`):

- `strategic-alignment-framework.md` - Connect tech to business strategy
- `portfolio-balancing.md` - Allocate resources across priorities
- `technology-radar.md` - Track emerging technologies (adopt/trial/assess/hold)
- `wardley-mapping.md` - Strategic technology positioning
- `roadmap-governance.md` - Process for maintaining and updating roadmap

**Templates** (`references/templates/`):

- `three-horizon-roadmap.md` - Structure for tactical/strategic/visionary planning
- `roadmap-visualization.md` - Visual formats (timeline, swim lanes, now-next-later)
- `board-roadmap-presentation.md` - Board-ready strategy presentation
- `executive-roadmap-presentation.md` - CEO/executive format
- `engineering-team-roadmap.md` - Detailed team-facing roadmap
- `okr-framework.md` - Engineering OKRs aligned with roadmap

**Examples** (`references/examples/`):

- Real roadmaps from startups to enterprises
- Before/after roadmap improvements
- Multi-year strategic plans
- Quarterly execution plans

## Usage Patterns

**Example 1**: User says "Create 12-month technology roadmap for our Series B SaaS company"

→ Load `references/frameworks/strategic-alignment-framework.md`
→ Gather context: business goals, current state, team size
→ Define 3-5 strategic themes
→ Use `references/templates/three-horizon-roadmap.md` structure
→ Balance portfolio: 70% core, 20% strategic, 10% innovation
→ Create quarterly milestones with success metrics
→ Generate executive presentation

---

**Example 2**: User says "Align engineering roadmap with product roadmap"

→ Load `references/templates/product-tech-alignment.md`
→ Map product features to required platform capabilities
→ Identify dependencies (what tech must be ready first)
→ Highlight shared milestones
→ Show trade-offs and capacity constraints
→ Create integrated timeline

---

**Example 3**: User says "We need to balance features vs technical debt vs innovation"

→ Load `references/frameworks/portfolio-balancing.md`
→ Assess current allocation (likely skewed toward features)
→ Apply 70-20-10 framework adjusted for stage
→ Identify highest-value technical debt items
→ Allocate innovation time for emerging tech
→ Create balanced quarterly plan

---

**Example 4**: User says "Present technology strategy to board"

→ Load `references/templates/board-roadmap-presentation.md`
→ Focus on: strategic positioning, competitive advantage, key bets
→ 3-5 year vision with major milestones
→ Explain how tech enables business strategy
→ Address risks and mitigation
→ Keep to 5-7 slides with clear narrative

---

## Roadmap Anti-Patterns

### ❌ Anti-Pattern 1: Feature List Masquerading as Strategy

**What it looks like**: "Q1: Feature A, B, C; Q2: Feature D, E, F"

**Why it's bad**: No strategic themes, no platform investment, reactive not proactive

**Fix**: Group features under strategic themes, include platform work

---

### ❌ Anti-Pattern 2: Over-Commitment

**What it looks like**: 100% of capacity allocated to committed work, no buffer

**Why it's bad**: No room for urgent work, incidents, tech debt, learning

**Fix**: Plan to 70-80% of capacity, leave buffer for unexpected

---

### ❌ Anti-Pattern 3: Set-and-Forget Roadmap

**What it looks like**: Annual roadmap created in January, never updated

**Why it's bad**: Business changes, roadmap becomes fiction

**Fix**: Quarterly reviews and adjustments, transparent communication

---

### ❌ Anti-Pattern 4: Technical Jargon for Business Audience

**What it looks like**: "Migrate from REST to gRPC, implement event sourcing"

**Why it's bad**: Business stakeholders don't understand value

**Fix**: Frame in business outcomes: "Improve API performance by 50%, enable real-time features"

---

### ❌ Anti-Pattern 5: All Short-Term Tactical

**What it looks like**: Detailed plan for next 2 quarters, vague beyond that

**Why it's bad**: No strategic direction, technology doesn't support long-term vision

**Fix**: Add strategic and visionary horizons, even if less detailed

---

## Technology Radar

Track emerging technologies to inform roadmap:

**Adopt** - Ready for production use

- Kubernetes for container orchestration
- React for frontend development
- PostgreSQL for relational data

**Trial** - Worth pursuing in pilots

- AI code assistants (Copilot, etc.)
- Edge computing for global latency
- Vector databases for AI features

**Assess** - Interesting, keep watching

- WebAssembly for performance-critical code
- Decentralized identity systems
- Quantum-resistant cryptography

**Hold** - Proceed with caution or deprioritize

- Blockchain for non-financial use cases
- Microservices for small teams
- NoSQL when SQL would suffice

Use `references/frameworks/technology-radar.md` for detailed methodology.

---

## Capacity Planning

Realistic roadmap requires understanding capacity:

### Calculate Available Capacity

```
Team Size: 20 engineers
Weeks per Quarter: 13 weeks
Theoretical Capacity: 20 × 13 × 40 hours = 10,400 hours

Subtract:
- Holidays and PTO: 10% = -1,040 hours
- Meetings and coordination: 15% = -1,560 hours
- Incidents and support: 10% = -1,040 hours
- Context switching: 5% = -520 hours

Realistic Capacity: 6,240 hours (60% of theoretical)

For new initiatives: 4,680 hours (75% of realistic, 25% buffer)
```

### Estimate Initiative Size

Small: 200-400 hours (1-2 person-months)
Medium: 400-800 hours (2-4 person-months)
Large: 800-1,600 hours (4-8 person-months)
Extra Large: 1,600+ hours (8+ person-months)

### Plan Quarterly Initiatives

Q1 Capacity: 4,680 hours available

Committed:

- Platform migration (Large): 1,200 hours
- New feature A (Medium): 600 hours
- New feature B (Medium): 600 hours
- Tech debt sprint (Small): 300 hours
- Team onboarding (2 new hires): 400 hours

Total: 3,100 hours (66% of capacity) ✅

Remaining: 1,580 hours for bugs, incidents, unplanned work ✅

---

## Strategic Themes Examples

### Theme: Platform Modernization

**Why**: Current monolith limits team autonomy and deployment speed
**Initiatives**:

- Extract billing service (Q1-Q2)
- Extract auth service (Q2-Q3)
- Implement service mesh (Q3-Q4)
- API gateway migration (Q4)

**Success Metrics**:

- Deployment frequency: 3x/week → daily
- Service independence: 0 → 3 independent services
- Team autonomy: 1 monolith team → 3 service teams

---

### Theme: AI-First Product

**Why**: AI is transforming our market, need to lead not follow
**Initiatives**:

- AI recommendation engine (Q1-Q2)
- Natural language search (Q2-Q3)
- Smart content generation (Q3-Q4)
- ML infrastructure platform (ongoing)

**Success Metrics**:

- % users using AI features: 0% → 60%
- AI-driven conversion lift: +20%
- Feature development time with AI: -30%

---

### Theme: Developer Velocity

**Why**: Team growing 2x, need to scale productivity
**Initiatives**:

- CI/CD pipeline overhaul (Q1)
- Development environment standardization (Q1-Q2)
- Automated testing expansion (Q2-Q3)
- Developer portal (Q3-Q4)

**Success Metrics**:

- Lead time: 5 days → 2 days
- Developer satisfaction: 7.5 → 8.5
- Time to first contribution (new hires): 3 weeks → 1 week

---

## Writing Style

All outputs should be:

- **Business-Focused**: Lead with business value, not technical details
- **Visual**: Use timelines, charts, diagrams where helpful
- **Realistic**: Be honest about capacity and trade-offs
- **Strategic**: Connect tactical work to long-term vision
- **Flexible**: Frame as living document, not rigid plan

---

**Version**: 1.0.0
**Philosophy**: Align technology with business strategy, balance short and long-term, communicate transparently
