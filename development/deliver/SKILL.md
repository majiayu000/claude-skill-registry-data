---
name: deliver
description: "Use when Forge delivers the completed product. Tech writer generates docs, CEO compiles delivery report with spec coverage and known issues."
---

<Purpose>
Phase 7 of the Forge pipeline. The final phase where the Tech Writer generates
comprehensive documentation and the CEO compiles a delivery report summarizing
spec coverage, test results, and known issues. The completed product is presented
to the client with full transparency. In Autonomous Company Mode, delivery begins only
after internal readiness gates say the work is truly delivery-ready.
</Purpose>

<Use_When>
- Automatically invoked after Phase 6 (fix) completes or Phase 5 (security) passes clean
- state.json phase=7
</Use_When>

<Steps>
1. Dispatch Tech Writer agent to generate documentation:

   a. README.md:
      - Project overview (from spec.md, non-technical)
      - Getting started (install, configure, run)
      - Environment variables required
      - Available scripts (dev, build, test, lint)
      - Project structure overview
      - Tech stack summary

   b. API Documentation (if API routes exist):
      - For each API route:
        - Method, path, description
        - Request parameters/body (from contracts)
        - Response format (from contracts)
        - Error responses
        - Authentication requirements
      - Save to .forge/delivery-report/api-docs.md

   c. Component Documentation (if UI components exist):
      - For each shared/reusable component:
        - Props interface (from contracts)
        - Usage examples
        - Available variants/states
      - Save to .forge/delivery-report/component-docs.md

   d. Deployment Guide:
      - Environment setup
      - Build commands
      - Deployment steps (Vercel, Docker, etc. based on architecture)
      - Environment variable configuration
      - Post-deployment verification steps
      - Save to .forge/delivery-report/deploy-guide.md

2. CEO compiles Delivery Report (.forge/delivery-report/report.md):

   a. Spec Coverage Analysis:
      - Prefer `.forge/traceability.json` as the source of truth when present
      - Run `node scripts/forge-traceability-report.mjs` to compute coverage and verified coverage
      - Run `node scripts/forge-generate-delivery-report.mjs` to generate a report scaffold from traceability + holes
      - Fall back to manual spec mapping only when traceability artifact is missing
      - List any descoped features with reason and V2 plan

   b. Test Results Summary:
      - Total tests: N (pass: N, fail: N, skip: N)
      - Test coverage percentage (if measurable)
      - QA test case results (from Phase 4)
      - Security audit results (from Phase 5)

   c. Known Issues (minor/cosmetic only — blockers are resolved):
      - List each known issue from .forge/holes/ with severity=minor or cosmetic
      - Impact assessment for each
      - Planned resolution timeline (V1.1 or V2)

   d. Architecture Summary:
      - Tech stack used
      - Key design decisions and rationale
      - Scalability considerations

   e. Handoff Notes:
      - How to extend the codebase
      - Key files and their responsibilities
      - Recommended next steps

2b. **Harness Learning — Project Retrospective**:
    a. CEO reviews the full project lifecycle:
       - Compare spec scope vs delivered scope (estimation lesson)
       - Note phases that took disproportionately long (process lesson)
       - Collect all lessons from .forge/lessons/ created during QA/Fix phases
    b. CEO decides which lessons to promote to global:
       - Pattern lessons matching common project types → copy to ~/.claude/forge-lessons/
       - Process lessons revealing harness bugs → promote AND create fix ticket for harness
       - Estimation lessons → always promote (calibration data is cumulative)
    c. If global lessons exceed 30: curate — merge similar ones, archive outdated ones
    d. Record lesson summary in delivery report

3. Internal delivery readiness gate:
   a. QA confirms blocker count is zero
   b. Security confirms no unresolved delivery-blocking issue remains
   c. CEO confirms the company is ready to present the result externally
   d. If not ready, route internally to the matching team:
      - bug / regression → fix
      - implementation gap → develop
      - design mismatch → design or designer rework
      - quality gap → QA re-check after rework
   e. Reflect the gate in runtime:
      - still blocked:
        `node scripts/forge-lane-runtime.mjs set-company-gate --gate delivery_readiness --gate-owner ceo --delivery-state blocked --internal-blockers "{blocker summaries}"`
      - ready for client:
        `node scripts/forge-lane-runtime.mjs set-company-gate --gate customer_review --gate-owner ceo --delivery-state ready_for_review`

4. Present delivery to client:
   a. Show spec coverage percentage prominently
   b. List completed features with checkmarks
   c. List known issues (minor only) with severity labels
   d. Show test results summary
   e. Provide all generated documentation links
   f. Ask the client to review the completed delivery

5. Client accepts → finalize delivery:
   a. Update state.json: phase=8, phase_id="complete", phase_name="complete", status="delivered"
   b. Create git tag: forge/v1-delivery
   c. Create version tag: forge/v0.1.0
   d. Final dashboard showing complete project summary
   e. Mark runtime delivered:
      `node scripts/forge-lane-runtime.mjs set-company-gate --gate customer_review --gate-owner ceo --delivery-state delivered`

6. Client requests changes → route back to appropriate phase:
   - Feature change → Phase 1 (discovery) for spec amendment
   - Design change → Phase 2 (design)
   - Bug found → Phase 6 (fix)
   - Update runtime with the customer blocker:
     `node scripts/forge-lane-runtime.mjs set-company-gate --gate customer_review --gate-owner pm --delivery-state in_progress --customer-blockers "{customer review feedback summaries}"`
</Steps>

<State_Changes>
- Creates: .forge/delivery-report/report.md
- Creates: .forge/delivery-report/api-docs.md (if applicable)
- Creates: .forge/delivery-report/component-docs.md (if applicable)
- Creates: .forge/delivery-report/deploy-guide.md
- Creates: README.md (project root)
- Updates: .forge/state.json (phase=8, phase_id="complete", phase_name="complete", status="delivered")
- Updates: .forge/runtime.json (delivery/customer_review state + customer feedback routing)
- Promotes: .forge/lessons/*.md → ~/.claude/forge-lessons/ (selected by CEO)
- Creates: git tag forge/v1-delivery
- Creates: git tag forge/v0.1.0
</State_Changes>

<Failure_Modes_To_Avoid>
- Delivering without documentation
- Inflating spec coverage percentage (counting partial implementations as complete)
- Hiding known issues from the client
- Presenting work to the client before internal delivery readiness is met
- Not including deployment instructions
- Generating docs that reference non-existent files or APIs
- Not calculating actual spec coverage (just saying "done")
- Skipping the client review step
- Creating version tag before client accepts delivery
- Forgetting to include environment variable documentation
- Not providing handoff notes for future development
</Failure_Modes_To_Avoid>

<Auto_Chain>
When delivery completes (all docs written, CEO signs off):
1. Update state.json: phase_id → "complete", status → "delivered"
2. Present delivery report to the client
This is the terminal phase — the pipeline ends here. Show the final summary to the user.
</Auto_Chain>
