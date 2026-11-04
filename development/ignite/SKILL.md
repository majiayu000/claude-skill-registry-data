---
name: ignite
description: "MANDATORY Forge entry point. Use when the user explicitly says \"forge\", \"build a harness\", \"set up Forge\", asks Forge to build a new product, or asks Forge to diagnose/fix/analyze an existing project. If the request is for a phased team workflow, build-vs-repair routing, or harness-based execution, you must start here."
---

<Purpose>
Forge is a Virtual Software Company. Ignite is the universal entry point.
Two modes:
- BUILD mode: idea → spec → design → development → QA → delivery
- REPAIR mode: existing project → diagnosis → fix → QA → delivery

The CEO evaluates the request and routes to the right mode. After kickoff, Forge should
operate like an internal software company: the client gives the request, answers minimum
critical questions, and reviews the delivery at the end. Internal teams own the rest.
</Purpose>

<Use_When>
- User invokes /forge:ignite or says "forge"
- BUILD: "build me a ~~", "I want an app that ~~", "create a ~~"
- REPAIR: "fix this bug", "analyze this error", "why isn't this working?"
- KO: "만들어줘", "고쳐줘", "포지"  JA: "作って", "直して", "フォージ"  ZH: "做一个", "修复", "锻造"
- User wants team-based development or debugging
</Use_When>

<Do_Not_Use_When>
- User is already in a Forge session (use phase-specific skills like forge:continue)
- Trivial one-line change that doesn't need team process
</Do_Not_Use_When>

<Core_Principles>
1. No Evidence, No Code — never write code without evidence
2. No Ambiguity, No Start — if unclear, ask questions instead of implementing
3. No Hole Left Behind — every discovered gap must be tracked
4. Right Architecture, Right Scale — optimal design matched to project scale
5. No Handoff Without Understanding — no handoff without confirmed comprehension
   Each phase transition requires a Handoff Interview: the receiving team reads artifacts,
   generates domain-specific questions, CEO triages (internal vs client), questions are
   resolved, and receiving team confirms understanding before starting work.
   Load `references/handoff-interview.md` for the full protocol.
</Core_Principles>

<Execution_Policy>
- Each Phase MUST complete before the next begins
- The client is NOT the default phase approver; internal readiness gates decide phase progress
- Ask the client only when a blocker is truly customer-owned or critical ambiguity would cause the wrong product to be built
- State is persisted in .forge/ directory
- Cancel with "forge cancel" at any time
- Load `references/phase-map.md` for the compact phase sequence.
- Load `references/handoff-interview.md` for the handoff interview protocol between phases.
- Load `references/constraint-propagation.md` when an artifact changes and downstream impact must be tracked.
- Load `references/context-budget.md` when dispatching agents to determine correct context loading.
- Load `references/harness-learning.md` at project start (intake) to check lessons from past projects, and at delivery to record new lessons.
- Load `references/harness-ab-eval.md` when asked to prove Forge's value against a baseline.
</Execution_Policy>

<Steps>
Phase 0 — INTAKE (CEO):
  1. Read the client's request
  1b. **Lessons Check**: CEO loads global lessons from ~/.claude/forge-lessons/ (if exists)
      - Match project type against lesson `applies_when` conditions
      - Relevant lessons → record in state.json as `lessons_brief`
      - If no global lessons exist → log "No global lessons found, skipping" and set lessons_brief=[]
      - Pattern lessons feed into CTO's code-rules, QA's test plan
      - Estimation lessons calibrate scope assessment
  2. **Internal Deliberation** — CEO does not decide alone; holds internal meeting:
     - CEO asks CTO for technical feasibility assessment + alternative architectures (using context7)
     - If client intent is ambiguous, asks PM for interpretation
     - CEO synthesizes after collecting CTO + PM input
     - Present to client as "Here's how we can do it" (internal deliberation process is not exposed)

  2b. **Express Qualification Check**:
      Before routing to full BUILD or REPAIR pipeline, CEO evaluates if the task qualifies for express mode.

      [Express-qualified tasks] (route to forge:express):
      - Single feature with bounded scope (1-3 files expected)
      - Clear requirements, no ambiguity
      - No architecture decisions needed
      - Bug fix with known location
      - Documentation or config changes
      - User explicitly says "quick", "simple", "express"

      [Full pipeline tasks] (route to forge:discovery or troubleshooter):
      - Multi-system changes
      - Architecture decisions needed
      - Unclear requirements requiring PM interview
      - Security-sensitive changes
      - User explicitly requests full process

      **CEO Decision**: If express-qualified AND user hasn't requested full pipeline:
        → Initialize .forge/ with mode="express", tier="medium"
        → Route directly to forge:express (skips discovery + design)

      **Default**: When unclear, prefer full pipeline. It's better to over-process than under-process.

  3. CEO agent evaluates and ROUTES:

     [BUILD mode] — new product request
      "build me", idea description
      → Can we build this? If not directly, what alternative achieves the same goal?
      → GO: initialize .forge/, Phase 1 (Discovery)

     [REPAIR mode] — existing project fix/analysis
      "fix", "bug", "analyze", "what's wrong"
      → Existing codebase detected?
      → REPAIR Intake: Generate minimal baseline artifacts
        - Read existing codebase structure and create minimal spec.md (scope, constraints, known architecture)
        - Extract existing code conventions into code-rules.md
        - Scan for existing interfaces/types and populate .forge/contracts/ with stubs
      → Dispatch Troubleshooter for diagnosis
      → Diagnosis → Fix → QA → Deliver (skip full Phase 1-3)

  3. If unclear which mode or critical customer intent is missing → ask the client
  4. BUILD: initialize .forge/ directory with state.json (from templates/state.json), hand off to PM
     - state.json MUST include: artifact_versions={}, staleness={}, lessons_brief=[]
     - These fields are required for constraint propagation and harness learning
  5. REPAIR: initialize .forge/ with mode="repair" (same template fields), hand off to Troubleshooter

Phase 1 — DISCOVERY (PM):
  1. Invoke forge:discovery skill
  2. PM interviews the client with understanding verification loops
     - After each major topic, PM summarizes understanding back to client
     - Client confirms or corrects before moving to next topic
  3. Generate spec.md from template
  4. Internal assumptions and validation targets are recorded
  5. **Pre-handoff: PM pre-generates questions CTO/Designer will likely have**
     - PM anticipates technical/design ambiguities in the spec
     - CEO reviews and resolves what can be answered internally
  6. CEO reviews spec readiness → internal GO to Phase 2

Phase 2 — DESIGN (CTO + Designer):
  1. **Handoff Interview: CTO + Designer read spec.md and generate domain questions**
     - CTO: technical feasibility questions, missing constraints, integration gaps
     - Designer: UX flow gaps, missing states, interaction ambiguities
     - CEO triages: internal (PM/CEO answers) vs client-owned (ask client)
     - Questions resolved before design work begins
  2. Invoke forge:design skill
  3. CTO: architecture + code-rules.md + interface contracts
  4. Designer: UI/UX spec + component definitions
  5. Cross-review between CTO and Designer
  6. Fact checker validates all technical claims via context7
  7. **Pre-handoff: CTO generates implementation questions Lead Dev will need**
  8. CTO + Designer + fact-checker confirm design readiness → Phase 3

Phase 3 — DEVELOPMENT (Lead + Devs + Publisher):
  1. **Handoff Interview: Lead reads architecture, contracts, code-rules, components**
     - Lead generates implementation questions (ambiguous boundaries, unclear contracts)
     - CEO triages: CTO answers technical, Designer answers UX, client if business-owned
     - Lead confirms understanding before splitting tasks
  2. Invoke forge:develop skill
  3. Lead splits work into tasks, creates git worktrees
  4. Each developer/publisher works in isolated worktree
  5. PR-based merge with 3-tier review (auto → lead → CTO)
  6. Code rules enforced — inconsistent code is REJECTED
  7. All required lanes merged and internally verified → Phase 4

Phase 4 — QA (QA Engineer):
  1. Invoke forge:qa skill
  2. Functional, visual, contract, regression, edge-case testing
  3. Issues go to bug tracker (.forge/holes/)
  4. Blockers → Phase 6, No blockers → Phase 5

Phase 5 — SECURITY (Security Reviewer):
  1. Invoke forge:security skill
  2. OWASP Top 10, secrets scan, auth/authz review
  3. Security issues = blockers → Phase 6

Phase 6 — FIX LOOP (Fact Checker + Devs + Troubleshooter):
  1. Invoke forge:fix skill
  2. Simple issues: fact-check → dev fix → QA re-verify
  3. Complex issues: troubleshooter RCA → dev fix → QA re-verify
  4. Max 3 iterations on the same blocker before CEO escalates to the client with alternatives
  5. All blockers resolved → Phase 7

Phase 7 — DELIVERY (CEO + Tech Writer):
  1. Invoke forge:deliver skill
  2. Tech writer generates docs (README, API docs, deploy guide)
  3. QA + Security + CEO confirm delivery readiness
  4. CEO compiles delivery report and presents it to the client for final review
</Steps>

<State_Management>
On first invocation, create .forge/ directory:

.forge/
├── state.json      ← current phase, progress, active agents, artifact_versions, staleness
├── spec.md         ← client-approved spec (Phase 1 output)
├── code-rules.md   ← CTO-defined code rules (Phase 2 output)
├── design/         ← architecture + UI design (Phase 2 output)
├── contracts/      ← interface contracts (Phase 2 output)
├── evidence/       ← fact-checker verification results
├── holes/          ← discovered issues
├── tasks/          ← work unit definitions
├── worktrees/      ← git worktree directories
├── knowledge/      ← project knowledge base
├── lessons/        ← harness learning: lessons from QA, fixes, and delivery
└── delivery-report/← final delivery docs

state.json includes `artifact_versions` and `staleness` fields for constraint propagation.
See `references/constraint-propagation.md` for the full protocol.
</State_Management>

<Dashboard>
After each major transition, show progress to the client in customer language. Internal
status may be richer than what is shown externally:

Forge Progress:
┌─────────────────────────────────┐
│ Phase: N/{max} ({phase_name})   │
│ ████████░░░░ XX%               │
│                                │
│ ✅ Completed                    │
│ 🔄 In Progress                  │
│ ⏳ Pending                      │
│                                │
│ Known Issues: N                │
│ Needs Client Input: N          │
└─────────────────────────────────┘
</Dashboard>

<Rollback>
Each Phase completion creates a git tag:
  forge/v{N}-{phase_name}

Client can request rollback:
  "The earlier design was better" → rollback to forge/v1-design → continue from Phase 2
</Rollback>

<Tool_Usage>
- Use Agent tool to dispatch team members (CEO, PM, CTO, etc.)
- Use Write for .forge/tasks/ and .forge/state.json tracking
- Use Bash for git operations (worktree, branch, tag, merge)
- Use Write for .forge/ state files
- Use Read for loading specs, contracts, code-rules
- Do NOT use tools without evidence (PreToolUse guard may deny code writes when harness prerequisites are missing)
- Treat the customer as the client, not the internal project manager
</Tool_Usage>
