---
name: design
description: "Use when Forge reaches the design phase or the user asks for technical architecture, UI spec, contracts, or code rules before implementation. Trigger on requests for architecture design, component specification, design tokens, interface contracts, or phased pre-build planning."
---

<Purpose>
Phase 2 of the Forge pipeline. CTO and Designer collaborate as a persistent Team
(via TeamCreate + SendMessage) to produce architecture, code rules, interface contracts,
and design specs. Analyst grounds them in the existing codebase before they begin.
Researcher supports external option comparison, but CTO and Designer keep decision
ownership. Every technical claim is verified via context7 before being committed to
the design. No guessing — only evidence-backed decisions. In Autonomous Company Mode,
design is an internal readiness gate by default, not a customer approval checkpoint.
</Purpose>

<Use_When>
- After Phase 1 (discovery) completes
- state.json phase=2
</Use_When>

<Core_Rules>
1. CTO MUST use context7 to verify every framework pattern before deciding
   - No "I think Next.js supports..." — look it up, cite the doc
   - If context7 can't confirm it, flag it as unverified

2. Use Researcher before locking external choices that are still open
   - Researcher compares viable frameworks, packages, vendors, or service options
   - CTO still makes the final architecture call

3. Designer MUST define every component completely:
   - Size, color, spacing, typography, border radius
   - All states: default, hover, active, disabled, loading, error, empty
   - Responsive breakpoints: mobile, tablet, desktop

4. CTO and Designer MUST cross-review each other's work
   - CTO reviews design feasibility: can this be built with chosen stack?
   - Designer reviews architecture: does it support all UI needs?

5. If design and tech conflict → resolve internally first
   - Never silently drop a feature because it's "hard"
   - Never force a design that the architecture can't support
   - Escalate to the client only if the blocker is truly customer-owned:
     - unresolved business priority
     - subjective direction with no responsible default
     - incompatible requirements that only the client can choose between

6. code-rules.md MUST have examples (good + bad) for every rule:

   Example format:
   ```
   Rule: Component files use PascalCase

   GOOD:
   UserProfile.tsx
   PaymentForm.tsx

   BAD:
   userProfile.tsx
   payment-form.tsx
   ```
</Core_Rules>

<Progressive_Disclosure>
- Load `references/design-deliverables.md` for the complete deliverable and cross-review checklist.
- Load `references/research-integration.md` when discovery hands off research or design needs external option comparison.
- Load `agents/design-team.md` for the 4-phase CTO↔Designer collaboration protocol.
- Load `agents/analyst.md` for codebase analysis tool reference.
</Progressive_Disclosure>

<Team_Collaboration>
When both CTO and Designer are needed (the common case):
- Use TeamCreate(team_name="forge-design") to create a design team
- Add CTO and Designer as team members via Agent tool with team_name parameter
- They collaborate via SendMessage for real-time cross-review
- Reference: agents/design-team.md for the 4-phase collaboration protocol
  Phase 1: Parallel Analysis (CTO: architecture, Designer: UX)
  Phase 2: Cross-Review via SendMessage
  Phase 3: Convergence (resolve conflicts)
  Phase 4: Handoff (unified design artifact)

When only CTO is needed (pure backend/API project):
- Dispatch CTO as individual subagent (no Team needed)

When only Designer is needed (UI-only change):
- Dispatch Designer as individual subagent (no Team needed)
</Team_Collaboration>

<Researcher_Scope>
Researcher is for EXTERNAL investigation only:
- Dispatched when CTO or Designer needs external comparison (libraries, frameworks, vendors)
- NOT for internal codebase analysis — that is the Analyst's job
- Researcher uses context7 + WebSearch; Analyst uses codebase-memory-mcp
- CTO still makes the final architecture call after reviewing Researcher output
</Researcher_Scope>

<Steps>
-1. **Staleness Check (constraint propagation)**
    - Read state.json.staleness — if `spec` is marked stale, BLOCK.
    - Read analysis metadata — if saved codebase analysis is stale or missing for a non-greenfield path, route to `forge:analyze` first.
    - Route to PM to update spec before design proceeds.
    - Only continue when spec staleness is cleared.

-0. **Handoff Interview — Design Intake (BEFORE any design work begins)**
   a. CTO reads spec.md completely, generates technical questions:
      - Missing data flow details, unclear API boundaries
      - Unspecified performance/scalability requirements
      - Ambiguous integration points, unclear state management needs
      Format: "Q: ... | Domain: technical | Blocker: yes/no | Default assumption: ..."

   b. Designer reads spec.md completely, generates UX questions:
      - Missing user flows, unspecified edge-case behaviors
      - Unclear navigation patterns, missing responsive requirements
      - Ambiguous interaction patterns (what happens on error? on empty state?)
      Format: "Q: ... | Domain: design | Blocker: yes/no | Default assumption: ..."

   c. CEO triages all questions:
      - INTERNAL → PM answers from interview knowledge, or CTO/Designer resolves internally
      - CLIENT → only truly customer-owned decisions (max 1-2 questions batched)
      - ASSUMPTION OK → record assumption in spec.md, proceed

   d. After questions resolved, CTO and Designer each write an understanding statement:
      - CTO: "I will build [architecture summary] to support [key requirements]. Key constraints: [list]."
      - Designer: "I will design [UX summary] for [user types]. Key flows: [list]."
      - PM reviews these statements against spec intent. Mismatches → correct immediately.

   e. Understanding confirmed → design work begins.

-0b. **Lessons Check (harness learning)**
    - CTO loads relevant pattern lessons from ~/.claude/forge-lessons/ and state.json.lessons_brief
    - Known bug patterns for the chosen tech stack → add preventive rules to code-rules.md
    - Known QA-failure patterns → add to contracts as explicit constraints
    - Known estimation gaps → flag to CEO for scope calibration

0. Codebase Analysis (skip if greenfield project):
   Dispatch Analyst (forge:analyst) to map existing architecture:
   - Uses codebase-memory-mcp: get_architecture, search_graph, trace_call_path
   - Produces: module map, dependency graph, coupling hotspots, architectural patterns
   - Output saved to .forge/design/codebase-analysis.md
   - CTO uses this as input for architecture decisions
   - Designer uses this to understand existing UI patterns and components

1. Create design team and dispatch agents:
   - Use TeamCreate(team_name="forge-design") to create a persistent design team
   - Add CTO and Designer as team members via Agent tool with team_name parameter
   - Dispatch Researcher in parallel only when discovery handed off an open research brief
     or a design decision depends on outside option comparison
   - Researcher informs the choice; CTO still decides
   - If only CTO or only Designer is needed, dispatch as individual subagent instead

2. CTO produces (informed by Analyst's codebase-analysis.md):
   a. .forge/design/architecture.md
      - Tech stack with version numbers (verified via context7)
      - Directory structure
      - Data flow diagram (text-based)
      - API route inventory
      - State management strategy
   b. .forge/code-rules.md
      - Naming conventions (files, variables, components)
      - Import ordering rules
      - Error handling patterns
      - Each rule with GOOD + BAD examples
   c. .forge/contracts/*.ts
      - TypeScript interfaces for all shared boundaries
      - API request/response types
      - Database model types
      - Component prop types

3. Designer produces (informed by Analyst's codebase-analysis.md):
   a. .forge/design/components.md
      - Component inventory (every UI element)
      - Per-component spec: size, color, spacing, states
      - Interaction patterns (click, hover, drag, swipe)
      - Accessibility requirements (ARIA roles, keyboard nav)
   b. .forge/design/tokens.json
      - Color palette (primary, secondary, neutral, semantic)
      - Typography scale (font family, sizes, weights, line heights)
      - Spacing scale (4px base grid)
      - Border radius values
      - Shadow definitions
      - Breakpoints

4. Cross-Review via Team:
   - CTO sends architecture proposal to Designer: SendMessage(to="designer", ...)
     "Please verify all components can be implemented with this architecture"
   - Designer sends UX proposal to CTO: SendMessage(to="cto", ...)
     "Supporting this interaction flow requires these APIs"
   - They negotiate directly until convergence
   - Conflict resolution: CTO decides technical feasibility, Designer decides UX quality
   - If deadlocked: escalate to CEO (rare)
   - If Researcher was used, CTO folds the brief into the architecture rationale
     and flags any remaining unknowns

5. Internal design-readiness gate:
   - CTO confirms the architecture is implementable at the chosen scale
   - Designer confirms the design covers required flows and states
   - Fact checker confirms technical claims are evidence-backed
   - If the gate fails, revise internally before moving on
   - Escalate to the client only for genuine customer-owned blockers

6. Fact checker validates all technical claims:
   - Every package referenced exists and is at claimed version
   - Every API pattern works as described (verified via context7)
   - Every TypeScript type is syntactically valid
   - Every framework feature is available in the chosen version

7. Optional client check-in only when needed:
   - If a real business-level design blocker remains, present it clearly in customer language
   - Otherwise keep the design decision internal and proceed

8. **Pre-Handoff: Generate Lead Dev questions**
   - CTO anticipates implementation questions Lead Dev will have:
     - Ambiguous module boundaries, unclear dependency ordering
     - Missing contract details, unspecified error propagation paths
     - Performance budget per module, unclear testing requirements
   - CTO resolves what they can; remaining questions are recorded in the handoff brief
   - These become the starting point for Lead Dev's Handoff Interview in Phase 3

9. Internal design readiness passes → update state.json: phase=3, phase_id="develop", phase_name="develop", design_approved=true
   - Update company runtime for implementation:
     `node scripts/forge-lane-runtime.mjs set-company-gate --gate implementation_readiness --gate-owner lead-dev --delivery-state in_progress`
   - Update session handoff toward implementation (include pre-generated questions):
     `node scripts/forge-lane-runtime.mjs set-session-brief --goal "Prepare reviewable implementation lanes" --next-owner lead-dev --handoff "{summary + pre-generated questions}"`

10. Create git tag: forge/v1-design

11. Transition to Phase 3 (forge:develop)
</Steps>

<Scale_Decision>
Project size determines architecture depth:

| Size   | Pages | Architecture Approach                              |
|--------|-------|----------------------------------------------------|
| Small  | 1-3   | Single Next.js app, flat structure, minimal abstraction |
| Medium | 4-10  | Feature-based folders, shared lib, API route layer  |
| Large  | 10+   | Monorepo (Turborepo), shared packages, strict contracts |

CTO determines size from spec.md and applies the matching approach.
Over-engineering a small project is as bad as under-engineering a large one.
</Scale_Decision>

<State_Changes>
- Creates: .forge/design/codebase-analysis.md (Analyst output, skipped for greenfield)
- Creates: .forge/design/architecture.md
- Creates: .forge/design/components.md
- Creates: .forge/design/tokens.json
- Creates: .forge/contracts/*.ts
- Creates: .forge/code-rules.md
- Updates: .forge/state.json (phase=3, design_approved=true)
- Updates: .forge/state.json artifact_versions: bump architecture, contracts, components, code_rules, tokens
- Updates: .forge/runtime.json (implementation_readiness gate + next session brief)
- Creates: git tag forge/v1-design
</State_Changes>

<Tool_Usage>
- Agent tool: dispatch forge:analyst for codebase analysis (Step 0)
- TeamCreate: create forge-design team when both CTO and Designer are needed
- Agent tool (with team_name): add CTO and Designer to the forge-design team
- SendMessage: CTO↔Designer cross-review within the team
- Agent tool: dispatch forge:researcher for bounded external option research (external only)
- Agent tool: dispatch forge:cto or forge:designer individually when only one is needed
- context7 MCP: verify every framework pattern, package version, API behavior
- codebase-memory-mcp: Analyst uses get_architecture, search_graph, trace_call_path
- Write tool: create design files, contracts, code-rules
- Read tool: load .forge/spec.md for requirements reference
- Edit tool: update .forge/state.json
- Bash tool: git tag forge/v1-design
</Tool_Usage>

<Failure_Modes_To_Avoid>
- CTO guessing framework behavior without verifying via context7
- Locking stack or vendor choices before reviewing needed Researcher evidence
- Designer skipping component states (only defining "happy path" appearance)
- Skipping cross-review between CTO and Designer
- Escalating internal design decisions to the client too early
- Proceeding to Phase 3 without internal design-readiness
- code-rules.md with rules but no GOOD/BAD examples
- Contracts missing request/response types for API routes
- Design tokens without responsive breakpoints
- Over-engineering a small project or under-engineering a large one
- Letting Researcher replace CTO decision-making
- Skipping Analyst step for non-greenfield projects (CTO designs blind)
- Using Researcher for internal codebase analysis (Analyst's job)
- Dispatching CTO and Designer as isolated subagents when Team is needed
- CTO and Designer producing independent outputs without SendMessage cross-review
- Starting design work before Handoff Interview is complete
- CTO/Designer not writing understanding statements before starting
- PM rubber-stamping understanding statements without reading them
- Not generating pre-handoff questions for Lead Dev
- Routing more than 2 questions to client when internal resolution is possible
</Failure_Modes_To_Avoid>

<Auto_Chain>
When design completes (architecture.md, code-rules.md, contracts/ all produced, CTO+Designer confirm):
1. Update state.json: phase_id → "develop", design_approved → true
2. IMMEDIATELY invoke Skill: forge:develop
Do NOT stop, summarize, or ask the user. Lead Dev will split tasks and dispatch developers automatically.
</Auto_Chain>
