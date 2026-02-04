---
name: spec-analysis
description: |
  8-dimensional quantitative complexity analysis with domain detection. Analyzes specifications
  across structural, cognitive, coordination, temporal, technical, scale, uncertainty, dependency
  dimensions producing 0.0-1.0 scores. Detects domains (Frontend, Backend, Database, etc.) with
  percentages. Use when: analyzing specifications, starting projects, planning implementations,
  assessing complexity quantitatively.

skill-type: QUANTITATIVE
shannon-version: ">=4.0.0"

mcp-requirements:
  required:
    - name: serena
      version: ">=2.0.0"
      purpose: Save analysis for cross-session retrieval
      fallback: local-storage
      degradation: medium
  recommended:
    - name: sequential
      purpose: Deep thinking for complex specs (100-500 steps)
      fallback: native-thinking
      trigger: preliminary_estimate >= 0.60

required-sub-skills:
  - mcp-discovery
  - phase-planning

optional-sub-skills:
  - wave-orchestration

allowed-tools: Read, Grep, Glob, Sequential, Serena
---

# Specification Analysis

## Overview

**Purpose**: Shannon's signature 8-dimensional quantitative complexity analysis transforms unstructured specifications into actionable, quantitative project intelligence with objective scoring, domain detection, MCP recommendations, and 5-phase execution plans.

---

## Anti-Rationalization (From Baseline Testing)

**CRITICAL**: Agents systematically rationalize skipping or adjusting the spec-analysis algorithm. Below are the 4 most common rationalizations detected in baseline testing, with mandatory counters.

### Rationalization 1: "User's assessment seems reasonable"
**Example**: User says "I think this is 60/100 complexity" → Agent responds "Your assessment of 60/100 seems reasonable..."

**COUNTER**:
- ❌ **NEVER** accept user's subjective score without running the algorithm
- ✅ User intuition is a data point, not the answer
- ✅ ALWAYS calculate the 8D score objectively
- ✅ If user score differs from calculated score by >0.15, report both and explain why algorithm is more reliable

**Rule**: Apply algorithm. User intuition doesn't override calculation.

### Rationalization 2: "This spec is simple, skip analysis"
**Example**: User says "Just a simple CRUD app, no need for formal analysis" → Agent proceeds directly to implementation

**COUNTER**:
- ❌ **NEVER** skip analysis because spec "seems simple"
- ✅ Human intuition under-estimates complexity by 30-50%
- ✅ "Simple" specs often score 0.45-0.65 (Moderate-Complex) when analyzed objectively
- ✅ Analysis takes 30 seconds; rebuilding from missed complexity takes hours
- ✅ Even trivial specs get scored (minimum 0.10)

**Rule**: Even "simple" specs get analyzed. Takes 30 seconds. No exceptions.

### Rationalization 3: "Obviously frontend-heavy, skip domain counting"
**Example**: User says "It's a React app, so probably 80% frontend, 20% backend" → Agent accepts without validation

**COUNTER**:
- ❌ **NEVER** accept domain guesses without counting keywords
- ✅ "Obviously" is subjective; counting is objective
- ✅ Specs that "sound frontend" often have 40% backend when counted
- ✅ Use domain keyword algorithm: count all indicators, calculate percentages, normalize to 100%

**Rule**: Count indicators. Never guess domain percentages.

### Rationalization 4: "Score feels wrong, adjust it"
**Example**: Agent calculates 0.72, thinks "that seems too high", adjusts to 0.60

**COUNTER**:
- ❌ **NEVER** adjust calculated scores based on intuition
- ✅ If the score feels wrong, the algorithm is right
- ✅ "Feels high" often means you're underestimating hidden complexity
- ✅ Trust the math: 8 dimensions × weighted contribution = objective result
- ✅ Only recalculate if you find a calculation ERROR (wrong formula, wrong weights)

**Rule**: Algorithm is objective. If score feels wrong, algorithm is right.

### Detection Signal
**If you're tempted to**:
- Skip analysis for "simple" specs
- Accept user's score without calculating
- Guess domain percentages
- Adjust calculated scores

**Then you are rationalizing.** Stop. Run the algorithm. Report the results objectively.

## When to Use

Use this skill when:
- User provides specification, requirements document, or project description (3+ paragraphs, 5+ features)
- Starting new project or feature requiring complexity assessment
- Planning resource allocation and timeline estimation
- Need objective, reproducible complexity metrics to guide execution strategy
- Determining whether to use wave-based execution (complexity >=0.50)

DO NOT use when:
- Casual conversation without specification
- User asking questions about existing code (use code analysis instead)
- Simple one-line requests ("change button color")

## Inputs

**Required:**
- `specification` (string): Specification text (3+ paragraphs, 5+ features, or attached spec file)

**Optional:**
- `include_mcps` (boolean): Include MCP recommendations (default: true)
- `depth` (string): Analysis depth - "standard" or "deep" for complex specs (default: "standard")
- `save_to_serena` (boolean): Save analysis to Serena MCP (default: true)

## Outputs

Structured analysis object:

```json
{
  "complexity_score": 0.68,
  "interpretation": "Complex",
  "dimension_scores": {
    "structural": 0.55,
    "cognitive": 0.65,
    "coordination": 0.75,
    "temporal": 0.40,
    "technical": 0.80,
    "scale": 0.50,
    "uncertainty": 0.15,
    "dependencies": 0.30
  },
  "domain_percentages": {
    "Frontend": 34,
    "Backend": 29,
    "Database": 20,
    "DevOps": 17
  },
  "mcp_recommendations": [
    {
      "tier": 1,
      "name": "Serena MCP",
      "purpose": "Context preservation",
      "priority": "MANDATORY"
    }
  ],
  "phase_plan": [...],
  "execution_strategy": "wave-based",
  "timeline_estimate": "10-12 days",
  "analysis_id": "spec_analysis_20250103_144530"
}
```

**When to Use**:
- User provides ANY specification, requirements document, or project description (3+ paragraphs, 5+ features, or spec keywords)
- Starting new project or feature that needs complexity assessment
- Planning resource allocation and timeline estimation
- Need objective, reproducible complexity metrics to guide execution strategy
- Determining whether to use wave-based execution (complexity >=0.50)

**Expected Outcomes**:
- Quantitative complexity score (0.0-1.0) across 8 dimensions with interpretation band
- Domain breakdown (Frontend %, Backend %, Database %, etc.) summing to 100%
- Prioritized MCP server recommendations (Tier 1: Mandatory, Tier 2: Primary, Tier 3: Secondary)
- 5-phase implementation plan with validation gates, timelines, deliverables
- Complete analysis saved to Serena MCP for cross-wave context sharing
- Clear execution strategy (sequential vs wave-based)

**Duration**: 3-8 minutes for analysis, immediate results

---

## Core Competencies

### 1. 8-Dimensional Quantitative Scoring
- **Structural Complexity (20% weight)**: File count, service count, module organization, system breadth
- **Cognitive Complexity (15% weight)**: Analysis depth, design sophistication, decision-making, learning needs
- **Coordination Complexity (15% weight)**: Team coordination, component integration, cross-functional collaboration
- **Temporal Complexity (10% weight)**: Time pressure, deadline constraints, urgency factors
- **Technical Complexity (15% weight)**: Advanced technologies, algorithms, sophisticated requirements
- **Scale Complexity (10% weight)**: Data volume, user load, performance requirements
- **Uncertainty Complexity (10% weight)**: Ambiguities, unknowns, exploratory requirements
- **Dependencies Complexity (5% weight)**: Blocking dependencies, prerequisite requirements

**Output**: Weighted total score (0.0-1.0) mapping to interpretation bands:
- 0.00-0.30: Simple (1-2 agents, 0-1 waves, hours-1 day)
- 0.30-0.50: Moderate (2-3 agents, 1-2 waves, 1-2 days)
- 0.50-0.70: Complex (3-7 agents, 2-3 waves, 2-4 days)
- 0.70-0.85: High (8-15 agents, 3-5 waves, 1-2 weeks)
- 0.85-1.00: Critical (15-25 agents, 5-8 waves, 2+ weeks)

### 2. Domain Detection & Classification
- **Keyword-based detection**: Scans specification for domain-specific keywords (React, Express, PostgreSQL, Docker, etc.)
- **Percentage allocation**: Distributes domains proportionally based on keyword density
- **6 Primary Domains**: Frontend, Backend, Database, Mobile/iOS, DevOps, Security
- **Normalization**: Ensures domain percentages sum to exactly 100%
- **MCP triggering**: Domains >=20% trigger Primary MCP recommendations, >=15% trigger database-specific MCPs

### 3. Intelligent MCP Recommendation Engine
- **Tier 1 (MANDATORY)**: Serena MCP (always required for Shannon context preservation)
- **Tier 2 (PRIMARY)**: Domain-based MCPs triggered by >=20% domain presence (Magic MCP for Frontend >=20%, PostgreSQL MCP for Database >=15%, etc.)
- **Tier 3 (SECONDARY)**: Supporting MCPs like GitHub (version control), Tavily (research)
- **Tier 4 (OPTIONAL)**: Keyword-specific MCPs (monitoring, project management)
- **Rationale-driven**: Each recommendation includes purpose, usage patterns, when to use, fallback options

### 4. 5-Phase Plan Generation
- **Phase 1: Analysis & Planning (15% timeline)**: Complete spec analysis, task breakdown, risk assessment
- **Phase 2: Architecture & Design (20% timeline)**: System design, technical specs, domain-specific architecture
- **Phase 3: Implementation (40% timeline)**: Core development, largest phase, domain-specific objectives
- **Phase 4: Integration & Testing (15% timeline)**: Component integration, functional testing (NO MOCKS), E2E validation
- **Phase 5: Deployment & Documentation (10% timeline)**: Deployment, comprehensive docs, knowledge transfer
- **Validation Gates**: Each phase has clear pass criteria, ensures quality progression
- **Domain Customization**: Phase objectives tailored to dominant domains (Frontend-heavy vs Backend-heavy)

---

## Workflow

### Step 1: Automatic Detection & Activation
**Input**: User message containing specification text

**Processing**:
1. Scan for multi-paragraph structure (3+ paragraphs, >50 words each)
2. Check for requirement lists (5+ distinct items)
3. Detect primary keywords ("specification", "requirements", "build", "implement", "system design")
4. Detect secondary keywords ("needs to", "features", "users can", "system will")
5. Check for attached specification files (*.pdf, *.md, *.doc)
6. **Decision**: Activate if ANY trigger matches

**Output**: Boolean decision (activate spec analysis mode or standard conversation)

**Duration**: Instant (automatic pattern matching)

### Step 2: 8-Dimensional Complexity Scoring
**Input**: Specification text (string)

**Processing**:
1. **Structural Score**:
   - Extract file count via regex `\b(\d+)\s+(files?|components?)\b`
   - Extract service count via `\b(\d+)\s+(services?|microservices?|APIs?)\b`
   - Apply logarithmic scaling: `file_factor = log10(file_count + 1) / 3`
   - Apply qualifier multipliers ("entire" ×1.5, "all" ×1.3, "comprehensive" ×1.2)
   - Calculate: `structural_score = (file_factor × 0.40) + (service_factor × 0.30) + (module_factor × 0.20) + (component_factor × 0.10)`

2. **Cognitive Score**:
   - Count analysis verbs: ["analyze", "understand", "study"] (+0.20 per occurrence, max 0.40)
   - Count design verbs: ["design", "architect", "plan"] (+0.20, max 0.40)
   - Count decision verbs: ["choose", "evaluate", "compare"] (+0.10, max 0.30)
   - Count abstract concepts: ["architecture", "pattern", "strategy"] (+0.15, max 0.30)
   - Sum scores (capped at 1.0)

3. **Coordination Score**:
   - Count unique teams mentioned: frontend_team, backend_team, database_team, etc.
   - Count integration keywords: ["coordinate", "integrate", "sync", "align"] (×0.15 each)
   - Formula: `(team_count × 0.25) + (integration_keyword_count × 0.15) + (stakeholder_count × 0.10)`

4. **Temporal Score**:
   - Detect urgency keywords: "urgent" (+0.40), "soon" (+0.30), "standard" (+0.10)
   - Extract deadline: regex `\d+ (hours?|days?|weeks?)`
   - Map to factor: hours (+0.50), <3 days (+0.40), <7 days (+0.30), <2 weeks (+0.20)

5. **Technical Score**:
   - Count advanced tech: ML/AI, real-time, distributed systems (+0.20 each, max 0.60)
   - Count complex algorithms: optimization, graph algorithms (+0.20 each, max 0.40)
   - Count integrations: third-party APIs, payment gateways (+0.15 each, max 0.30)

6. **Scale Score**:
   - User factor: >1M users (+0.40), >100K (+0.30), >10K (+0.20), >1K (+0.10)
   - Data factor: TB/billions (+0.40), GB/millions (+0.20)
   - Performance keywords: "high performance", "low latency" (+0.20)

7. **Uncertainty Score**:
   - Ambiguity keywords: "TBD", "unclear", "possibly" (+0.20 each, max 0.40)
   - Exploratory terms: "explore", "prototype", "POC" (+0.15 each, max 0.30)
   - Research needs: "research", "evaluate options" (+0.15 each, max 0.30)

8. **Dependencies Score**:
   - Blocking language: "blocked by", "depends on", "requires" (+0.25 each, max 0.50)
   - External dependencies: "third-party approval", "vendor" (+0.20 each, max 0.50)

9. **Weighted Total**:
   ```
   total = (0.20 × structural) + (0.15 × cognitive) + (0.15 × coordination) +
           (0.10 × temporal) + (0.15 × technical) + (0.10 × scale) +
           (0.10 × uncertainty) + (0.05 × dependencies)
   ```

**Output**:
- 8 individual dimension scores (0.0-1.0)
- Weighted total complexity score (0.0-1.0)
- Interpretation band (Simple/Moderate/Complex/High/Critical)
- Resource recommendations (agent count, wave count, timeline)

**Duration**: 1-2 minutes

### Step 3: Domain Identification
**Input**: Specification text (string)

**Processing**:
1. **Count Keywords per Domain**:
   - Frontend: ["React", "Vue", "component", "UI", "dashboard", "responsive", "CSS"] → count occurrences
   - Backend: ["API", "endpoint", "Express", "server", "microservice", "authentication"] → count
   - Database: ["PostgreSQL", "schema", "migration", "SQL", "ORM", "Prisma"] → count
   - Mobile: ["iOS", "Swift", "mobile app", "native", "Xcode"] → count
   - DevOps: ["Docker", "deployment", "CI/CD", "Kubernetes", "AWS"] → count
   - Security: ["authentication", "encryption", "OAuth", "HTTPS", "vulnerability"] → count

2. **Calculate Raw Percentages**:
   ```
   total_keywords = sum(all domain counts)
   frontend_percentage = (frontend_count / total_keywords) × 100
   backend_percentage = (backend_count / total_keywords) × 100
   ...
   ```

3. **Round and Normalize**:
   - Round each percentage to nearest integer
   - Calculate sum of rounded percentages
   - If sum ≠ 100%, distribute difference to largest domain(s)
   - **Verification**: Sum MUST equal 100%

4. **Generate Domain Descriptions**:
   - For each domain >0%, extract 2-3 characteristics from specification
   - Example: "Frontend (38%): React UI framework, dashboard components, responsive design"

**Output**:
- Domain percentages summing to 100%
- Domain characteristics (2-3 bullets per domain)
- Sorted by percentage (descending)

**Duration**: 30 seconds

### Step 4: MCP Server Recommendations
**Input**: Domain percentages, specification text

**Processing**:
1. **Tier 1 (MANDATORY)**:
   - ALWAYS suggest: Serena MCP (context preservation, required for Shannon)

2. **Tier 2 (PRIMARY)** - Domain-based (>=20% threshold):
   - IF Frontend >=20%: Magic MCP (component generation), Puppeteer MCP (functional testing), Context7 MCP (React/Vue docs)
   - IF Backend >=20%: Context7 MCP (Express/FastAPI docs), Sequential MCP (complex logic), Database MCP (based on DB mentioned)
   - IF Mobile >=40%: SwiftLens MCP (Swift analysis), iOS Simulator Tools (XCUITest), Context7 MCP (SwiftUI docs)
   - IF Database >=15%: PostgreSQL/MongoDB/MySQL MCP (based on specific database mentioned)
   - IF DevOps >=15%: GitHub MCP (CI/CD), AWS/Azure/GCP MCP (based on cloud provider)

3. **Tier 3 (SECONDARY)** - Supporting:
   - GitHub MCP (if not already suggested, for any project)
   - Stripe/PayPal MCP (if payment integration mentioned)

4. **Tier 4 (OPTIONAL)** - Keyword-triggered:
   - Tavily/Firecrawl MCP (if "research", "investigate" mentioned)
   - Monitoring MCPs (if "monitoring", "observability" mentioned)

5. **Generate Rationale**:
   - For each MCP: Purpose, usage patterns, when to use, fallback options, priority level
   - Include examples where applicable

**Output**:
- Tiered MCP list (Mandatory → Primary → Secondary → Optional)
- Each with: name, tier, priority, rationale, usage, alternatives
- Summary counts per tier

**Duration**: 1 minute

### Step 5: 5-Phase Plan Generation
**Input**: Complexity score, domain percentages, timeline estimate

**Processing**:
1. **Estimate Base Timeline**:
   - <0.30 Simple: 4-8 hours
   - 0.30-0.50 Moderate: 1-2 days
   - 0.50-0.70 Complex: 2-4 days
   - 0.70-0.85 High: 1-2 weeks
   - 0.85-1.00 Critical: 2-4 weeks

2. **Generate Phase 1 (Analysis & Planning - 15%)**:
   - Objectives: Complete spec analysis, identify requirements, create task breakdown, risk assessment
   - Deliverables: Spec doc, task list with estimates, risk assessment, resource plan
   - Validation Gate: All requirements understood, no ambiguities, complexity validated, MCPs configured
   - Duration: base_timeline × 0.15

3. **Generate Phase 2 (Architecture & Design - 20%)**:
   - Base objectives: System design, technical specifications, architecture decisions
   - **Domain customization**:
     - IF Frontend >=40%: Add component hierarchy, state management strategy, routing architecture
     - IF Backend >=40%: Add API design, database schema, auth architecture, scalability
     - IF Database >=25%: Add data modeling, index strategy, migration strategy
   - Deliverables: Architecture diagrams, API specs, database schemas
   - Validation Gate: Design approved, patterns established, all design decisions documented

4. **Generate Phase 3 (Implementation - 40%)**:
   - Base objectives: Core development work
   - **Domain customization**:
     - IF Frontend >=40%: UI component development, responsive design, accessibility
     - IF Backend >=40%: API endpoint implementation, business logic, middleware
     - IF Database >=25%: Schema creation, migration scripts, query optimization
   - Deliverables: Implemented features, unit tests (functional, NO MOCKS), code reviews passed
   - Validation Gate: All features complete per spec, tests passing, no critical bugs

5. **Generate Phase 4 (Integration & Testing - 15%)**:
   - Objectives: Component integration, functional testing (NO MOCKS), E2E testing, performance validation
   - **Testing requirements by domain**:
     - Frontend: Puppeteer functional tests for user flows (real browser, NO MOCKS)
     - Backend: API functional tests with real HTTP requests (NO MOCKS)
     - Database: Database tests on test instance (real DB operations, NO MOCKS)
   - Deliverables: Integrated system, test results (functional), performance metrics, bug fixes
   - Validation Gate: All components integrated, functional tests passing, performance meets requirements

6. **Generate Phase 5 (Deployment & Documentation - 10%)**:
   - Objectives: Deploy to target environment, create docs, knowledge transfer, post-deployment validation
   - Deliverables: Deployed system, technical docs, user docs, deployment runbook
   - Validation Gate: System deployed, all docs complete, deployment validated, handoff complete

**Output**:
- 5 phases with objectives, deliverables, validation gates, durations
- Domain-customized objectives per phase
- Testing requirements enforcing NO MOCKS philosophy
- Timeline breakdown (percentages and absolute times)

**Duration**: 2-3 minutes

### Step 6: Save to Serena MCP
**Input**: Complete analysis results

**Processing**:
1. Generate analysis ID: `spec_analysis_{timestamp}`
2. Structure complete analysis as JSON:
   ```json
   {
     "analysis_id": "spec_analysis_20250103_143022",
     "complexity_score": 0.68,
     "interpretation": "Complex",
     "dimension_scores": {...},
     "domain_percentages": {...},
     "mcp_recommendations": [...],
     "phase_plan": [...],
     "execution_strategy": "wave-based (3-7 agents)"
   }
   ```
3. Save to Serena MCP: `write_memory(analysis_id, analysis_json)`
4. Verify save successful

**Output**:
- Analysis ID for retrieval
- Serena MCP confirmation
- Context available for all sub-agents

**Duration**: 30 seconds

### Step 7: Generate Output Report
**Input**: Complete analysis with all components

**Processing**:
1. Format using output template (see templates/analysis-output.md)
2. Include all sections:
   - Complexity Assessment (8D table + interpretation)
   - Domain Analysis (percentages + characteristics)
   - Recommended MCPs (tiered with rationale)
   - 5-Phase Plan (phases with gates)
   - Next Steps (actionable items)
   - Serena Save Confirmation

**Output**: Formatted markdown report ready for user presentation

**Duration**: 30 seconds

### Step 8: Trigger Sub-Skills (if needed)
**Input**: Complexity score, domain percentages

**Processing**:
1. IF complexity >=0.60 AND Sequential MCP recommended: Suggest using Sequential MCP for deep analysis
2. Always chain to phase-planning skill (uses this analysis as input)
3. IF complexity >=0.50: Suggest wave-orchestration skill for execution
4. Invoke mcp-discovery skill for any missing MCPs

**Output**: Sub-skill activation recommendations

**Duration**: Instant

### Step 9: Validation & Quality Check
**Input**: Complete analysis

**Processing**:
1. **Validate Complexity Score**: Score in range [0.0, 1.0], not exactly 0.0 or 1.0
2. **Validate Domain Percentages**: Sum equals exactly 100%
3. **Validate MCP Recommendations**: Serena MCP present in Tier 1, at least 1 domain-specific MCP in Tier 2
4. **Validate Phase Plan**: Exactly 5 phases with validation gates
5. **Calculate Quality Score**:
   - Valid complexity: +0.20
   - Valid domains: +0.20
   - MCPs present: +0.20
   - Serena included: +0.20
   - 5 phases: +0.20
   - Total: 1.0 = perfect

**Output**:
- Validation pass/fail
- Quality score (0.0-1.0)
- List of any errors detected

**Duration**: 10 seconds

---

## Agent Activation

**Agent**: SPEC_ANALYZER (optional, for complex specs)

**Context Provided**:
- System prompt: "You are Shannon's Specification Analyzer. Apply the 8-dimensional complexity framework systematically. Extract quantitative metrics, detect domains, recommend MCPs, generate 5-phase plans. Be objective and reproducible."
- Tools: Read, Grep, Glob, Sequential (if complex), Serena
- Domain knowledge: Complete SPEC_ANALYSIS.md algorithm, domain patterns, MCP matrix

**Activation Trigger**:
- Complexity preliminary estimate >=0.60 (requires deep analysis)
- Specification >2000 words (too large for single-pass analysis)
- User explicitly requests "/shannon:spec --deep"

**Behavior**:
- Uses Sequential MCP for 100-500 step systematic analysis
- Breaks down analysis into sub-problems per dimension
- Validates each dimension score independently
- Cross-checks domain percentages for consistency
- Generates detailed rationale for all recommendations

---

## MCP Integration

### Required MCPs

**Serena MCP** (MANDATORY)
- **Purpose**: Save complete analysis for cross-session context preservation, enable zero-loss restoration, share context across all waves and sub-agents
- **Usage**:
  ```javascript
  // Save analysis
  write_memory("spec_analysis_20250103_143022", {
    complexity_score: 0.68,
    domain_percentages: {...},
    mcp_recommendations: [...],
    phase_plan: [...]
  })

  // Retrieve later
  const analysis = read_memory("spec_analysis_20250103_143022")
  ```
- **Fallback**: Local file storage (degraded - no cross-session persistence)
- **Degradation**: MEDIUM (can continue with local storage, but lose cross-session context)
- **Verification**: Test with `list_memories()` - should return saved analyses

### Recommended MCPs

**Sequential MCP** (for complexity >=0.60)
- **Purpose**: Deep systematic thinking for complex specifications requiring 100-500 reasoning steps, hypothesis generation and testing, multi-faceted analysis
- **Trigger**: Preliminary complexity estimate >=0.60 (Complex-High or higher)
- **Usage**:
  ```javascript
  // Activate for deep analysis
  invoke_sequential({
    thought: "Analyzing structural complexity dimension...",
    thoughtNumber: 1,
    totalThoughts: 120,
    nextThoughtNeeded: true
  })
  ```
- **Fallback**: Native Claude reasoning (less structured, no hypothesis tracking)
- **Degradation**: LOW (native reasoning adequate for most specs)
- **When**: Complex specs with ambiguity, conflicting requirements, or high uncertainty scores

---

## Examples

### Example 1: Simple Todo App (Score: 0.28-0.35)
**Input**:
```
Build a simple todo app with React. Users can:
- Add new tasks with title and description
- Mark tasks as complete
- Delete tasks
- Filter by complete/incomplete

Store data in localStorage. Responsive design for mobile.
```

**Execution**:
```
Step 1: Detect activation → ✅ (5 feature items, explicit keywords "Build", "users can")
Step 2: 8D Scoring:
  - Structural: 1 file (React app) → 0.10
  - Cognitive: "design" mentioned → 0.20
  - Coordination: No teams → 0.10
  - Temporal: No deadline → 0.10
  - Technical: React (standard) → 0.20
  - Scale: localStorage (small) → 0.10
  - Uncertainty: Clear requirements → 0.10
  - Dependencies: None → 0.10
  - Weighted Total: 0.33

Step 3: Domain Detection:
  - Frontend: React(1), design(1), responsive(1), mobile(1) = 4 keywords
  - Backend: 0
  - Database: localStorage(1) = 1 keyword (counts as Database)
  - Total: 5 keywords
  - Frontend: 80%, Database: 20%

Step 4: MCP Recommendations:
  - Tier 1: Serena MCP (mandatory)
  - Tier 2: Magic MCP (Frontend 80%), Puppeteer MCP (Frontend testing)
  - Tier 3: GitHub MCP (version control)

Step 5: 5-Phase Plan:
  - Timeline: 4-6 hours (Simple)
  - Phase 1: 36 min (spec analysis)
  - Phase 2: 48 min (component design)
  - Phase 3: 2.4 hrs (implementation)
  - Phase 4: 36 min (Puppeteer tests)
  - Phase 5: 24 min (deployment)

Step 6: Save to Serena → spec_analysis_20250103_143022

Step 7: Output report generated

Step 8: Sub-skills: phase-planning invoked

Step 9: Validation: ✅ All checks passed, quality score: 1.0
```

**Output**:
```markdown
# Specification Analysis ✅

**Complexity**: 0.33 / 1.0 (MODERATE)
**Execution Strategy**: Sequential (no waves needed)
**Timeline**: 4-6 hours
**Analysis ID**: spec_analysis_20250103_143022

## Domain Breakdown
- Frontend (80%): React UI, component-based architecture, responsive design
- Database (20%): localStorage persistence

## Recommended MCPs
1. Serena MCP (Tier 1 - MANDATORY)
2. Magic MCP (Tier 2 - Frontend 80%)
3. Puppeteer MCP (Tier 2 - Frontend testing)
4. GitHub MCP (Tier 3 - Version control)

## 5-Phase Plan (4-6 hours)
[Detailed phase breakdown with validation gates...]

## Next Steps
1. Review complexity score → Confirmed: MODERATE (sequential execution)
2. Configure MCPs → Install Magic, Puppeteer, ensure Serena connected
3. Begin Phase 1 → Analysis & Planning (36 minutes)
```

### Example 2: Complex Real-time Collaboration Platform (Score: 0.68-0.75)
**Input**:
```
Build a real-time collaborative document editor like Google Docs. Requirements:

Frontend:
- React with TypeScript
- Rich text editing (Slate.js or ProseMirror)
- Real-time cursor tracking showing all active users
- Presence indicators
- Commenting system
- Version history viewer
- Responsive design

Backend:
- Node.js with Express
- WebSocket server for real-time sync
- Yjs CRDT for conflict-free collaborative editing
- Authentication with JWT
- Authorization (owner, editor, viewer roles)
- Document API (CRUD operations)

Database:
- PostgreSQL for document metadata, users, permissions
- Redis for session management and presence
- S3 for document snapshots

Infrastructure:
- Docker containers
- Kubernetes deployment
- CI/CD pipeline with GitHub Actions
- Monitoring with Prometheus/Grafana

Timeline: 2 weeks, high performance required (< 100ms latency for edits)
```

**Execution**:
```
Step 1: Detect → ✅ (Multi-paragraph, extensive feature list, technical keywords)

Step 2: 8D Scoring:
  - Structural: Multiple services (frontend, backend, WebSocket, database) = 0.55
  - Cognitive: "design", "architecture", real-time system = 0.65
  - Coordination: Frontend team, backend team, DevOps team = 0.75
  - Temporal: 2 weeks deadline + "high performance" = 0.40
  - Technical: Real-time WebSocket, CRDT, complex algorithms = 0.80
  - Scale: Performance requirements (<100ms) = 0.50
  - Uncertainty: Well-defined requirements = 0.15
  - Dependencies: Multiple integrations = 0.30
  - Weighted Total: 0.72 (HIGH)

Step 3: Domain Detection:
  - Frontend: React, TypeScript, Slate, rich text, cursor, presence, responsive = 12 keywords
  - Backend: Express, WebSocket, Yjs, CRDT, auth, API, JWT = 10 keywords
  - Database: PostgreSQL, Redis, S3, metadata, session = 7 keywords
  - DevOps: Docker, Kubernetes, CI/CD, monitoring, Prometheus = 6 keywords
  - Total: 35 keywords
  - Frontend: 34%, Backend: 29%, Database: 20%, DevOps: 17%

Step 4: MCP Recommendations:
  - Tier 1: Serena MCP (mandatory)
  - Tier 2: Magic MCP (Frontend 34%), Puppeteer MCP (testing), Context7 MCP (React/Express/Postgres), Sequential MCP (complex real-time architecture), PostgreSQL MCP (Database 20%), Redis MCP
  - Tier 3: GitHub MCP, AWS MCP (S3), Prometheus MCP
  - Tier 4: Tavily MCP (research Yjs CRDT patterns)

Step 5: 5-Phase Plan:
  - Timeline: 10-12 days (HIGH complexity)
  - Phase 1: 1.5 days (deep analysis of CRDT requirements)
  - Phase 2: 2 days (architecture design for real-time sync)
  - Phase 3: 4 days (implementation across domains)
  - Phase 4: 1.5 days (integration + functional testing)
  - Phase 5: 1 day (deployment + documentation)

Step 6: Save to Serena → spec_analysis_20250103_144530

Step 7: Output report generated

Step 8: Sub-skills:
  - Sequential MCP recommended for architecture design
  - wave-orchestration REQUIRED (complexity 0.72 >= 0.50)
  - phase-planning invoked

Step 9: Validation: ✅ Quality score: 1.0
```

**Output**:
```markdown
# Specification Analysis ✅

**Complexity**: 0.72 / 1.0 (HIGH)
**Execution Strategy**: WAVE-BASED (8-15 agents recommended)
**Recommended Waves**: 3-5 waves
**Timeline**: 10-12 days
**Analysis ID**: spec_analysis_20250103_144530

## Complexity Breakdown
| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Structural | 0.55 | 20% | 0.11 |
| Cognitive | 0.65 | 15% | 0.10 |
| Coordination | 0.75 | 15% | 0.11 |
| Temporal | 0.40 | 10% | 0.04 |
| Technical | 0.80 | 15% | 0.12 |
| Scale | 0.50 | 10% | 0.05 |
| Uncertainty | 0.15 | 10% | 0.02 |
| Dependencies | 0.30 | 5% | 0.02 |
| **TOTAL** | **0.72** | | **HIGH** |

## Domain Breakdown
- Frontend (34%): React + TypeScript, real-time UI, rich text editing, presence system
- Backend (29%): Express API, WebSocket real-time sync, Yjs CRDT, authentication
- Database (20%): PostgreSQL metadata, Redis sessions, S3 snapshots
- DevOps (17%): Docker containers, Kubernetes orchestration, CI/CD, monitoring

## Recommended MCPs (9 total)
### Tier 1: MANDATORY
1. **Serena MCP** - Context preservation across waves

### Tier 2: PRIMARY
2. **Magic MCP** - React component generation (Frontend 34%)
3. **Puppeteer MCP** - Real browser testing (NO MOCKS)
4. **Context7 MCP** - React/Express/PostgreSQL documentation
5. **Sequential MCP** - Complex real-time architecture analysis (100-500 steps)
6. **PostgreSQL MCP** - Database schema operations (Database 20%)
7. **Redis MCP** - Session and presence management

### Tier 3: SECONDARY
8. **GitHub MCP** - CI/CD automation, version control
9. **AWS MCP** - S3 integration for document snapshots

### Tier 4: OPTIONAL
10. **Tavily MCP** - Research Yjs CRDT best practices
11. **Prometheus MCP** - Monitoring setup

## Next Steps
1. ⚠️  **CRITICAL**: Use wave-based execution (complexity 0.72 >= 0.50)
2. Configure 9 recommended MCPs (prioritize Tier 1-2)
3. Run /shannon:wave to generate wave plan (expect 3-5 waves, 8-15 agents)
4. Use Sequential MCP for Phase 2 architecture design
5. Enforce functional testing (Puppeteer for real-time sync, NO MOCKS)
```

### Example 3: Critical Trading System (Score: 0.88-0.95)
**Input**:
```
URGENT: Build high-frequency trading system for cryptocurrency exchange.

REQUIREMENTS:
- Sub-millisecond latency for order matching (<500 microseconds p99)
- Handle 1M orders/second peak load
- 99.999% uptime (5 nines availability)
- Real-time risk management engine
- Machine learning price prediction (LSTM model)
- Multi-exchange aggregation (Binance, Coinbase, Kraken APIs)
- Regulatory compliance (SEC, FINRA reporting)
- Distributed across 5+ data centers for fault tolerance

TECHNICAL CONSTRAINTS:
- Rust backend for performance-critical paths
- C++ for ultra-low-latency matching engine
- Kafka for event streaming (millions of events/sec)
- TimescaleDB for time-series data (billions of records)
- Redis cluster for in-memory order book
- Kubernetes with custom scheduler for latency optimization

TIMELINE: Production deployment in 4 weeks (CRITICAL DEADLINE)

UNKNOWNS:
- Market data feed integration approach TBD
- Optimal ML model architecture unclear (needs research)
- Disaster recovery strategy undefined
- Security audit requirements (pending legal review)

DEPENDENCIES:
- Blocked by exchange API approval (Binance, Coinbase - 1 week)
- Requires external security audit (vendor, 2 weeks)
- Waiting on legal compliance framework
```

**Execution**:
```
Step 1: Detect → ✅ (URGENT keyword, extensive multi-paragraph, critical requirements)

Step 2: 8D Scoring:
  - Structural: 5+ services, distributed system, multiple languages = 0.90
  - Cognitive: ML design, research needed, complex architecture = 0.85
  - Coordination: Backend, ML, DevOps, Security, Legal teams = 1.00 (5+ teams)
  - Temporal: URGENT + 4 weeks CRITICAL deadline = 0.90
  - Technical: HFT, sub-millisecond latency, ML, distributed consensus = 1.00
  - Scale: 1M orders/sec, 99.999% uptime, billions of records = 1.00
  - Uncertainty: Multiple TBDs, "unclear", "undefined", "pending" = 0.80
  - Dependencies: Blocked by vendors, external audits, legal = 0.75
  - Weighted Total: 0.92 (CRITICAL)

Step 3: Domain Detection:
  - Backend: Rust, C++, matching engine, APIs, Kafka, event streaming = 18 keywords
  - Database: TimescaleDB, Redis, order book, time-series, billions = 10 keywords
  - DevOps: Distributed, Kubernetes, 5+ data centers, fault tolerance = 8 keywords
  - ML: Machine learning, LSTM, price prediction, model = 5 keywords
  - Security: Regulatory, compliance, SEC, FINRA, security audit = 6 keywords
  - Total: 47 keywords
  - Backend: 38%, Database: 21%, DevOps: 17%, ML: 11%, Security: 13%

Step 4: MCP Recommendations:
  - Tier 1: Serena MCP (mandatory)
  - Tier 2: Context7 MCP (Rust/Kafka/TimescaleDB), Sequential MCP (critical for HFT architecture), PostgreSQL MCP (TimescaleDB), Redis MCP, Kubernetes MCP, AWS/GCP MCP (multi-region)
  - Tier 3: GitHub MCP, Tavily MCP (research ML models, HFT patterns), Binance/Coinbase API MCPs
  - Tier 4: Monitoring MCPs (Prometheus, DataDog), Sentry MCP (error tracking)

Step 5: 5-Phase Plan:
  - Timeline: 20-25 days (CRITICAL, pushing limits)
  - Phase 1: 3 days (deep analysis, risk assessment, dependency mapping)
  - Phase 2: 5 days (HFT architecture, ML model selection, disaster recovery design)
  - Phase 3: 8 days (implementation with parallel waves)
  - Phase 4: 3 days (integration, stress testing to 1M orders/sec)
  - Phase 5: 2 days (multi-region deployment, compliance docs)

Step 6: Save to Serena → spec_analysis_20250103_150015

Step 7: Output report generated

Step 8: Sub-skills:
  - Sequential MCP CRITICAL (architecture decisions have massive impact)
  - wave-orchestration MANDATORY (complexity 0.92, expect 15-25 agents, 5-8 waves)
  - risk-mitigation skill recommended (high uncertainty + dependencies)

Step 9: Validation: ✅ Quality score: 1.0
```

**Output**:
```markdown
# Specification Analysis ✅

🚨 **CRITICAL COMPLEXITY DETECTED** 🚨

**Complexity**: 0.92 / 1.0 (CRITICAL)
**Execution Strategy**: WAVE-BASED (15-25 agents REQUIRED)
**Recommended Waves**: 5-8 waves
**Timeline**: 20-25 days (EXTREMELY AGGRESSIVE - HIGH RISK)
**Analysis ID**: spec_analysis_20250103_150015

⚠️  **WARNINGS**:
- Complexity 0.92 is in CRITICAL band (top 5% of all projects)
- 4-week deadline with 0.92 complexity = VERY HIGH RISK
- Uncertainty score 0.80 + Dependencies 0.75 = significant blockers
- Consider timeline extension or scope reduction

## Complexity Breakdown
| Dimension | Score | Weight | Contribution | RISK LEVEL |
|-----------|-------|--------|--------------|------------|
| Structural | 0.90 | 20% | 0.18 | 🔴 CRITICAL |
| Cognitive | 0.85 | 15% | 0.13 | 🔴 HIGH |
| Coordination | 1.00 | 15% | 0.15 | 🔴 CRITICAL |
| Temporal | 0.90 | 10% | 0.09 | 🔴 HIGH |
| Technical | 1.00 | 15% | 0.15 | 🔴 CRITICAL |
| Scale | 1.00 | 10% | 0.10 | 🔴 CRITICAL |
| Uncertainty | 0.80 | 10% | 0.08 | 🔴 HIGH |
| Dependencies | 0.75 | 5% | 0.04 | 🔴 HIGH |
| **TOTAL** | **0.92** | | **CRITICAL** |

## Domain Breakdown
- Backend (38%): Rust/C++ HFT engine, sub-millisecond latency, Kafka streaming, multi-exchange APIs
- Database (21%): TimescaleDB time-series (billions), Redis cluster order book, in-memory operations
- DevOps (17%): Distributed 5+ data centers, Kubernetes custom scheduling, 99.999% uptime
- Security (13%): SEC/FINRA compliance, regulatory reporting, security audit requirements
- ML (11%): LSTM price prediction, model architecture research, real-time inference

## Recommended MCPs (13 total)
### Tier 1: MANDATORY
1. **Serena MCP** - CRITICAL for context preservation across 5-8 waves

### Tier 2: PRIMARY (8 MCPs)
2. **Context7 MCP** - Rust/Kafka/TimescaleDB/Redis documentation
3. **Sequential MCP** - CRITICAL 200-500 step analysis for HFT architecture decisions
4. **PostgreSQL MCP** - TimescaleDB operations (time-series optimizations)
5. **Redis MCP** - Redis cluster for order book management
6. **Kubernetes MCP** - Custom scheduler, latency optimization
7. **AWS MCP** - Multi-region deployment, data center orchestration
8. **GitHub MCP** - CI/CD for high-velocity development
9. **ML Framework MCP** - LSTM model development (TensorFlow/PyTorch)

### Tier 3: SECONDARY (4 MCPs)
10. **Tavily MCP** - Research HFT patterns, ML architectures, disaster recovery
11. **Binance API MCP** - Exchange integration
12. **Coinbase API MCP** - Exchange integration
13. **Prometheus MCP** - Monitoring for 99.999% uptime

## 5-Phase Plan (20-25 days - CRITICAL TIMELINE)
[Phases with RISK MITIGATION strategies for each...]

## Risk Assessment
🔴 **CRITICAL RISKS**:
1. **Timeline Risk**: 0.92 complexity with 4-week deadline = 60% probability of delay
2. **Dependency Risk**: Blocked by vendor approvals (1 week) + security audit (2 weeks) = 3 weeks consumed before implementation
3. **Uncertainty Risk**: ML model unclear, disaster recovery undefined = potential architecture rework
4. **Technical Risk**: Sub-millisecond latency requirement with distributed system = extremely challenging
5. **Coordination Risk**: 5+ teams (Backend, ML, DevOps, Security, Legal) = high communication overhead

**RECOMMENDATION**:
- Extend deadline to 6-8 weeks (50% timeline buffer)
- Parallel-track vendor approvals NOW (don't wait)
- Dedicate 1-2 agents to ML research in Phase 1
- Use Sequential MCP for ALL critical architecture decisions
- Daily SITREP coordination meetings

## Next Steps
1. 🚨 **IMMEDIATE**: Escalate timeline risk to stakeholders
2. Configure ALL 13 recommended MCPs (no optional - all needed for CRITICAL)
3. Run /shannon:wave with --critical flag (expect 15-25 agents, 5-8 waves)
4. Use Sequential MCP for Phase 1 risk analysis (200-500 reasoning steps)
5. Establish SITREP daily coordination protocol
6. Begin vendor approval process IMMEDIATELY (parallel to analysis)
```

---

## Success Criteria

**Successful when**:
- ✅ Complexity score valid (0.0-1.0 range, not exactly 0.0 or 1.0)
- ✅ Domain percentages sum to exactly 100%
- ✅ Serena MCP included in Tier 1 (mandatory)
- ✅ At least 1 domain-specific MCP in Tier 2 (based on >=20% domain)
- ✅ 5-phase plan generated with validation gates for all phases
- ✅ Testing requirements enforce NO MOCKS philosophy (Puppeteer, real DBs)
- ✅ Analysis saved to Serena MCP with unique ID
- ✅ Execution strategy matches complexity (sequential <0.50, wave-based >=0.50)
- ✅ Timeline estimate aligns with complexity interpretation band
- ✅ Quality validation score >=0.80 (4/5 checks passed)

Validation:
```python
def validate_spec_analysis(result):
    assert 0.10 <= result["complexity_score"] <= 0.95
    assert sum(result["domain_percentages"].values()) == 100
    assert any(mcp["tier"] == 1 and mcp["name"] == "Serena MCP"
               for mcp in result["mcp_recommendations"])
    assert len(result["phase_plan"]) == 5
    assert all(phase.get("validation_gate") for phase in result["phase_plan"])
    assert result["analysis_id"].startswith("spec_analysis_")
```

**Fails if**:
- ❌ Complexity score is 0.0 or 1.0 (calculation error)
- ❌ Domain percentages sum to ≠100% (normalization failed)
- ❌ Serena MCP missing from recommendations (violates Shannon requirement)
- ❌ No domain-specific MCPs suggested (failed domain detection)
- ❌ <5 phases in plan (incomplete planning)
- ❌ Testing allows mocks or unit tests (violates NO MOCKS Iron Law)
- ❌ Analysis not saved to Serena (context loss risk)
- ❌ Execution strategy mismatches complexity (e.g., sequential for 0.70)
- ❌ Wave-based recommended for Simple/Moderate projects (over-engineering)

---

## Common Pitfalls

### Pitfall 1: Subjective "Simple" Bias
**Problem**: Developer looks at specification, thinks "this is simple," skips 8D analysis, estimates 2-3 hours

**Why It Fails**:
- Human intuition systematically under-estimates complexity by 30-50%
- "Simple" often scores 0.45-0.65 quantitatively (Moderate to Complex)
- Missing hidden complexity: auth, error handling, deployment, testing, docs
- Example: "Build a task manager" → Seems simple → Actually 0.55 (Complex) when scored

**Solution**: ALWAYS run spec-analysis, let quantitative scoring decide. 3-5 minutes investment prevents hours of rework.

**Prevention**: using-shannon skill makes spec-analysis mandatory first step

### Pitfall 2: Domain Detection Errors
**Problem**: Analysis shows "Frontend 100%, Backend 0%" for full-stack app → Frontend MCP overload, no Backend MCPs suggested

**Why It Fails**:
- Keyword counting biased toward verbose descriptions
- Example: "Build React app with Node.js backend" → "React" mentioned 8 times, "Node.js" once → 89% Frontend, 11% Backend
- Should be more balanced (40% Frontend, 40% Backend, 20% Database)

**Solution**: Normalize keyword counts by section, not raw occurrences. If spec mentions multiple domains explicitly, ensure each >=15%.

**Prevention**: Validation step checks for domain imbalance (warn if single domain >80%)

### Pitfall 3: MCP Recommendation Overkill
**Problem**: Suggests 15 MCPs for Simple (0.28) project → User overwhelmed, setup takes longer than implementation

**Why It Fails**:
- Tier thresholds too low (suggesting Primary MCPs for <20% domains)
- Including too many Optional MCPs
- Not considering setup overhead vs project duration

**Solution**:
- Strict tier thresholds: Tier 2 (PRIMARY) only for >=20% domains
- Limit Tier 4 (OPTIONAL) to 2-3 max
- For Simple/Moderate (<0.50), suggest 3-5 MCPs total
- For Complex (0.50-0.70), suggest 5-8 MCPs
- For High/Critical (>0.70), suggest 8-13 MCPs

**Prevention**: Validation checks MCP count vs complexity (warn if >10 MCPs for Simple project)

### Pitfall 4: Ignoring Preliminary Estimate
**Problem**: Spec shows "URGENT", "ASAP", "critical deadline" → Temporal score calculated → Ignored when estimating timeline

**Why It Fails**:
- Timeline estimate based only on Structural/Technical dimensions
- Temporal dimension impacts resource allocation, not just timeline
- High Temporal (>0.60) should increase agent count, decrease per-agent timeline

**Solution**: High Temporal score → Recommend more parallel agents (2x normal), tighter wave coordination

**Prevention**: Timeline estimation formula includes Temporal as multiplier

### Pitfall 5: Phase Plan Generic (Not Domain-Customized)
**Problem**: Generated 5-phase plan identical for Frontend-heavy (Frontend 80%) vs Backend-heavy (Backend 70%) projects

**Why It Fails**:
- Phase objectives should reflect dominant domains
- Frontend-heavy needs UI design, component architecture in Phase 2
- Backend-heavy needs API design, database schema in Phase 2
- Generic plan misses domain-specific validation gates

**Solution**: Phase 2/3/4 objectives dynamically customized based on domain percentages >=40%

**Prevention**: Validation checks if Phase 2 includes domain-specific objectives (e.g., "component hierarchy" for Frontend >=40%)

### Pitfall 6: Testing Requirements Vague
**Problem**: Phase 4 says "Write tests" without specifying functional testing, NO MOCKS enforcement

**Why It Fails**:
- Developers default to unit tests with mocks (violates Shannon Iron Law)
- Vague testing requirements = inconsistent quality
- Shannon mandates: Puppeteer for Frontend, real HTTP for Backend, real DB for Database

**Solution**: Phase 4 testing requirements explicitly state:
- Frontend: "Puppeteer functional tests (real browser, NO MOCKS)"
- Backend: "API tests with real HTTP requests (NO MOCKS)"
- Database: "Database tests on test instance (real DB, NO MOCKS)"

**Prevention**: functional-testing skill enforces NO MOCKS, but spec-analysis should set expectations upfront

### Pitfall 7: Serena Save Fails Silently
**Problem**: Analysis completes, report generated, but Serena MCP write_memory() fails → No error shown → Context lost on next wave

**Why It Fails**:
- Network issues, Serena MCP disconnected, memory quota exceeded
- Analysis not re-saved
- Wave 2 starts without Wave 1 context

**Solution**: Verify Serena save with read-back test:
```javascript
write_memory(analysis_id, analysis_data)
const verify = read_memory(analysis_id)
if (!verify) throw Error("Serena save failed - analysis not persisted")
```

**Prevention**: Step 6 includes save verification, reports error if save fails

### Pitfall 8: Complexity Ceiling/Floor Violations
**Problem**: Specification is trivial (change button color) → Score calculated as 0.05 → Reported as 0.00

**Why It Fails**:
- Scores <0.10 rounded to 0.00 → Looks like calculation error
- Scores >0.95 capped at 1.00 → Loses granularity for "impossible" projects
- Users distrust perfect scores (0.00 or 1.00)

**Solution**:
- Minimum floor: 0.10 (even trivial tasks have some complexity)
- Maximum cap: 0.95 (leave room for "truly impossible")
- Report 0.10 as "Trivial (minimal complexity)" instead of 0.00

**Prevention**: Validation rejects scores <0.10 or >0.95 with warning

---

## Validation

**How to verify spec-analysis executed correctly**:

1. **Check Complexity Score**:
   - Score in range [0.10, 0.95] ✅
   - Not exactly 0.00 or 1.00 ✅
   - Matches expected interpretation band (e.g., 0.68 → "Complex-High") ✅

2. **Check Domain Percentages**:
   - Sum equals exactly 100% ✅
   - No single domain >95% (unless truly single-domain project) ✅
   - Dominant domains (>=20%) align with specification content ✅

3. **Check MCP Recommendations**:
   - Serena MCP in Tier 1 (mandatory) ✅
   - At least 1 domain-specific MCP in Tier 2 for dominant domain ✅
   - Total MCP count reasonable for complexity (<10 for Simple, <15 for Critical) ✅
   - Each MCP has rationale, usage, fallback ✅

4. **Check 5-Phase Plan**:
   - Exactly 5 phases present ✅
   - Each phase has objectives, deliverables, validation gate ✅
   - Phase 2/3 objectives customized for dominant domains ✅
   - Phase 4 testing requirements enforce NO MOCKS ✅
   - Timeline percentages sum to 100% (15% + 20% + 40% + 15% + 10%) ✅

5. **Check Serena Save**:
   - Analysis ID format: `spec_analysis_{timestamp}` ✅
   - Serena write_memory() successful ✅
   - Verify with read_memory(analysis_id) ✅

6. **Check Execution Strategy**:
   - Complexity <0.50 → Sequential execution ✅
   - Complexity >=0.50 → Wave-based execution ✅
   - High/Critical (>=0.70) → SITREP protocol recommended ✅

7. **Run Validation Script** (if available):
   ```bash
   python3 shannon-plugin/tests/validate_skills.py
   # Expected: ✅ spec-analysis: All validation checks passed
   ```

---

## Progressive Disclosure

**SKILL.md** (This file): ~500 lines
- Overview, when to use, expected outcomes
- 8D framework summary (dimension names, weights, interpretation bands)
- Domain detection (6 domains, percentage allocation)
- MCP recommendation tiers (4 tiers, threshold rules)
- 5-phase plan structure
- 9-step workflow (high-level)
- 3 examples (Simple, Complex, Critical)
- Success criteria, common pitfalls, validation

**references/SPEC_ANALYSIS.md**: 1787 lines (full algorithm)
- Complete 8D scoring formulas with regex patterns
- Detailed domain keyword lists (200+ keywords)
- Full MCP recommendation matrix (20+ MCPs)
- Phase customization logic by domain
- Output templates with formatting
- Integration with other Shannon components

**references/domain-patterns.md**: ~300 lines
- Exhaustive domain keyword dictionaries
- File pattern matching (*.jsx, *.tsx, etc.)
- Domain classification edge cases
- Cross-domain keyword handling (e.g., "API" in Frontend vs Backend context)

**Claude loads references/ when**:
- Complexity >=0.60 (needs deep algorithm details)
- Domain percentages unclear (consult domain-patterns.md)
- MCP recommendations ambiguous (consult full MCP matrix)
- User requests "/shannon:spec --deep" (deep analysis mode)
- Validation failures (debug with full algorithm)

---

## References

- Full 8D algorithm: references/SPEC_ANALYSIS.md (1787 lines)
- Domain patterns: references/domain-patterns.md (300 lines)
- Phase planning: shannon-plugin/skills/phase-planning/SKILL.md
- Wave orchestration: shannon-plugin/skills/wave-orchestration/SKILL.md
- MCP discovery: shannon-plugin/skills/mcp-discovery/SKILL.md
- Testing philosophy: shannon-plugin/core/TESTING_PHILOSOPHY.md
- Context management: shannon-plugin/core/CONTEXT_MANAGEMENT.md
- Output template: templates/analysis-output.md

---

## Performance Benchmarks

**Expected Performance** (measured on Claude Sonnet 3.5):

| Specification Size | Analysis Time | Quality Score | Recommended Depth |
|--------------------|---------------|---------------|-------------------|
| <500 words | 30-60 seconds | 0.95+ | standard |
| 500-2000 words | 1-3 minutes | 0.90+ | standard |
| 2000-5000 words | 3-8 minutes | 0.85+ | deep (if complexity >=0.60) |
| >5000 words | 8-15 minutes | 0.80+ | deep (mandatory) |

**Performance Indicators**:
- ✅ **Fast**: <2 minutes for typical specs (<1000 words)
- ⚠️ **Acceptable**: 2-5 minutes for complex specs (1000-3000 words)
- 🔴 **Slow**: >8 minutes (check: is Sequential MCP needed? Is spec ambiguous requiring research?)

**Quality Validation**:
- Analysis quality score >=0.80 (4/5 validation checks passed)
- Domain percentages sum to exactly 100%
- Serena save verified with read-back test

**When Analysis Takes Longer**:
- Large specifications (>3000 words) → Expected, use --deep flag
- High uncertainty score (>0.60) → Research needed, acceptable delay
- Sequential MCP deep reasoning → 100-500 thoughts for complex specs, 5-15 minutes

---

## Complete Execution Walkthrough

**Scenario**: User provides moderate complexity specification

**Specification Text**:
```
Build a customer support ticketing system. Requirements:

Frontend:
- React dashboard for support agents
- Ticket list with filtering (status, priority, assignee)
- Ticket detail view with rich text editor for responses
- Real-time updates when tickets change

Backend:
- Express API with TypeScript
- Authentication for agents and admins
- REST endpoints for tickets (CRUD)
- WebSocket for real-time updates
- Email integration (send/receive via SendGrid)

Database:
- PostgreSQL for tickets, users, responses
- Schema with tickets, users, responses tables
- Full-text search on ticket content

Deployment:
- Docker container
- Deploy to AWS

Timeline: 1 week
```

**Execution Process** (showing actual Claude workflow):

**Step 1: Activation Detection**
```
Input: [Specification text above]
Process:
  - Check: Multi-paragraph? ✅ (3 paragraphs)
  - Check: >5 features? ✅ (12+ distinct features)
  - Check: Primary keywords? ✅ ("Build", "Requirements", "Deployment")
  - Check: Attached files? ❌
Decision: ACTIVATE spec-analysis
```

**Step 2: Calculate 8D Scores**
```
Structural Complexity (20% weight):
  - Extract: "React dashboard" → 1 component mentioned
  - Extract: "Express API" → 1 service
  - Calculate: file_factor = log10(8+1)/3 ≈ 0.32 (estimate 8 files)
  - Calculate: service_factor = log10(2+1)/3 ≈ 0.16
  - Score: (0.32 × 0.40) + (0.16 × 0.30) = 0.18 × 1.5 (qualifier: multiple features) = 0.27
  - Result: structural = 0.27

Cognitive Complexity (15% weight):
  - Count: "design" (0), "analyze" (0), "architect" (0)
  - Count: No complex design requirements
  - Score: 0.15 (baseline for any non-trivial spec)
  - Result: cognitive = 0.15

Coordination Complexity (15% weight):
  - Teams: Frontend team, Backend team (implied 2 teams)
  - Integration: "real-time updates" → 1 integration keyword
  - Score: (2 × 0.25) + (1 × 0.15) = 0.65
  - Result: coordination = 0.65

Temporal Complexity (10% weight):
  - Deadline: "1 week" → <7 days factor
  - Score: 0.30 (1 week deadline)
  - Result: temporal = 0.30

Technical Complexity (15% weight):
  - Advanced tech: "WebSocket" (real-time) → +0.20, "full-text search" → +0.15
  - Integrations: "SendGrid" → +0.15
  - Score: 0.20 + 0.15 + 0.15 = 0.50
  - Result: technical = 0.50

Scale Complexity (10% weight):
  - Users: Not mentioned (assume <10K)
  - Performance: Not mentioned
  - Score: 0.15 (moderate scale implied)
  - Result: scale = 0.15

Uncertainty Complexity (10% weight):
  - No "TBD", "unclear", "research" keywords
  - Well-defined requirements
  - Score: 0.10 (minimal uncertainty)
  - Result: uncertainty = 0.10

Dependencies Complexity (5% weight):
  - External: SendGrid API → 1 dependency
  - No blocking dependencies mentioned
  - Score: 0.20
  - Result: dependencies = 0.20

Weighted Total:
  (0.20 × 0.27) + (0.15 × 0.15) + (0.15 × 0.65) + (0.10 × 0.30) +
  (0.15 × 0.50) + (0.10 × 0.15) + (0.10 × 0.10) + (0.05 × 0.20)
  = 0.054 + 0.023 + 0.098 + 0.030 + 0.075 + 0.015 + 0.010 + 0.010
  = 0.315
  → Round to 0.32

Interpretation: 0.32 → MODERATE (0.30-0.50 band)
```

**Step 3: Domain Detection**
```
Count Keywords:
  Frontend: React(1), dashboard(1), filtering(1), view(1), real-time(1), updates(1) = 6
  Backend: Express(1), API(1), TypeScript(1), Authentication(1), REST(1), endpoints(1),
           CRUD(1), WebSocket(1), email(1), integration(1), SendGrid(1) = 11
  Database: PostgreSQL(1), Schema(1), tables(3), full-text(1), search(1) = 7
  DevOps: Docker(1), Deploy(1), AWS(1) = 3
  Total: 27 keywords

Calculate Percentages:
  Frontend: (6/27) × 100 = 22.2% → round to 22%
  Backend: (11/27) × 100 = 40.7% → round to 41%
  Database: (7/27) × 100 = 25.9% → round to 26%
  DevOps: (3/27) × 100 = 11.1% → round to 11%

Normalize (sum = 100%):
  22 + 41 + 26 + 11 = 100% ✅

Result:
  - Backend: 41%
  - Database: 26%
  - Frontend: 22%
  - DevOps: 11%
```

**Step 4: MCP Recommendations**
```
Tier 1 (MANDATORY):
  - Serena MCP → Always required

Tier 2 (PRIMARY) - Domain >=20%:
  - Backend 41% >=20% → Context7 MCP (Express/TypeScript docs)
  - Database 26% >=20% → PostgreSQL MCP
  - Frontend 22% >=20% → Magic MCP (component generation), Puppeteer MCP (testing)

Tier 3 (SECONDARY):
  - GitHub MCP (version control)
  - AWS MCP (deployment)
  - SendGrid MCP (email integration)

Tier 4 (OPTIONAL):
  - None (project well-defined, no research needed)

Result: 8 MCPs recommended
```

**Step 5: 5-Phase Plan**
```
Base Timeline: 1-2 days (MODERATE 0.32, user requested 1 week → achievable)

Phase 1 (15% = 2.4 hours):
  - Objectives: Complete spec analysis, task breakdown, risk assessment
  - Deliverables: Task list, complexity validated, MCP configuration
  - Validation Gate: All requirements understood, no ambiguities

Phase 2 (20% = 3.2 hours):
  - Objectives: System design, API design (Backend 41%), Database schema (Database 26%)
  - Deliverables: API spec, database schema, component hierarchy
  - Validation Gate: Design approved, patterns established

Phase 3 (40% = 6.4 hours):
  - Objectives: Backend API implementation (41%), Database setup (26%), Frontend components (22%)
  - Deliverables: REST endpoints, PostgreSQL schema, React dashboard
  - Validation Gate: Features complete, NO MOCKS tests passing

Phase 4 (15% = 2.4 hours):
  - Objectives: Integration testing (Puppeteer for Frontend, real HTTP for Backend, real DB)
  - Deliverables: Functional test suite (NO MOCKS), integration validated
  - Validation Gate: All tests passing (Puppeteer, API, Database)

Phase 5 (10% = 1.6 hours):
  - Objectives: Docker containerization, AWS deployment, documentation
  - Deliverables: Deployed system, technical docs
  - Validation Gate: System deployed, docs complete

Total: 16 hours ≈ 2 days (fits 1 week timeline comfortably)
```

**Step 6: Save to Serena MCP**
```javascript
const analysis_id = "spec_analysis_20251108_194500"
const analysis = {
  analysis_id: "spec_analysis_20251108_194500",
  complexity_score: 0.32,
  interpretation: "Moderate",
  dimension_scores: {
    structural: 0.27,
    cognitive: 0.15,
    coordination: 0.65,
    temporal: 0.30,
    technical: 0.50,
    scale: 0.15,
    uncertainty: 0.10,
    dependencies: 0.20
  },
  domain_percentages: {
    Backend: 41,
    Database: 26,
    Frontend: 22,
    DevOps: 11
  },
  mcp_recommendations: [...],
  phase_plan: [...],
  execution_strategy: "sequential",
  timeline_estimate: "1-2 days"
}

// Save
mcp__serena__write_memory(analysis_id, JSON.stringify(analysis))

// Verify
const verify = mcp__serena__read_memory(analysis_id)
if (!verify) throw Error("Serena save failed")
```

**Step 7: Format Output**
```markdown
# Specification Analysis ✅

**Complexity**: 0.32 / 1.0 (MODERATE)
**Execution Strategy**: Sequential (no waves needed)
**Timeline**: 1-2 days (16 hours)
**Analysis ID**: spec_analysis_20251108_194500

## Complexity Breakdown
[8D table as shown in examples]

## Domain Breakdown
- Backend (41%): Express API, TypeScript, REST endpoints, WebSocket real-time, SendGrid integration
- Database (26%): PostgreSQL schema, full-text search, relational data
- Frontend (22%): React dashboard, filtering, rich text editor
- DevOps (11%): Docker, AWS deployment

## Recommended MCPs (8 total)
[Tiered list with rationale]

## 5-Phase Plan (1-2 days)
[Detailed phase breakdown]

## Next Steps
1. Configure 8 MCPs (prioritize Serena, Context7, PostgreSQL)
2. Begin Phase 1 (2.4 hours)
3. Sequential execution (no waves for MODERATE)
```

**Step 8: Chain to phase-planning**
```
Invoke phase-planning skill with analysis as input
```

**Step 9: Validation**
```
✅ Complexity: 0.32 ∈ [0.10, 0.95]
✅ Domains: 41 + 26 + 22 + 11 = 100%
✅ Serena in Tier 1
✅ Domain MCPs: PostgreSQL (26%), Context7 (41%), Magic (22%)
✅ 5 phases with gates
Quality Score: 1.0 (5/5 checks passed)
```

---

This walkthrough demonstrates the complete process Claude should follow when executing spec-analysis, showing the actual calculations, MCP selections, and validation steps.

---

## Metadata

**Version**: 4.0.0
**Last Updated**: 2025-11-03
**Author**: Shannon Framework Team
**License**: MIT
**Status**: Core (Quantitative skill, mandatory for Shannon workflows)
