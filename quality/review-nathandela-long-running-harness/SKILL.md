---
name: Review
description: Multi-agent review with lesson-calibrated reviewers, runtime verification, and severity classification
---

# Review Skill

## Overview
Perform thorough code review by spawning specialized reviewers in parallel, consolidating findings with severity classification (P0/P1/P2/P3), and gating completion on implementation-reviewer approval. Reviewers are calibrated with past lessons and relevant research before reviewing.

## Methodology
1. Read the epic description (`bd show <epic>`) for EARS requirements -- reviewers verify each requirement is met
2. **Check Acceptance Criteria**: Locate the `## Acceptance Criteria` table in the epic description. For each AC row, verify the implementation satisfies the criterion using the specified verification method.
   - If the AC section is **missing**: flag as **P1 process finding** ("No Acceptance Criteria section found in epic description — plan phase did not generate AC table")
   - If an AC criterion is **not met**: flag as **P1 defect** ("AC-N not satisfied: <details>")
   - If an AC criterion is **met**: annotate the AC row as PASS in the review report
3. **Check Verification Contract**: Locate the `## Verification Contract` section in the epic description.
   - If the contract is **missing**: flag as **P1 process finding** ("No Verification Contract section found in epic description — plan phase did not define required evidence")
   - If the contract exists: verify each item in `Required evidence` explicitly. Missing evidence is a **P1 process or execution defect**, not an optional note.
   - Use `Profile`, `Surfaces`, and `Risks` to decide which verification specialists must run during this review.
4. Run baseline quality gates: `pnpm test` and `pnpm lint`
   - If `Required evidence` includes `build`, also run `pnpm build` before spawning reviewers
5. **Lesson-Calibrated Review (LCR)**:
   a. For each reviewer category (security, test-coverage, simplicity, architecture, etc.), run `ca search "<category> review"` to retrieve relevant past lessons
   b. Filter results by category match and recency (prefer lessons < 30 days old)
   c. Cap at **3-5 lessons per reviewer** -- more dilutes focus
   d. Inject matched lessons into each reviewer's prompt as calibration context
   e. Consult `docs/compound/research/` for methodology references relevant to the review domain (e.g., `docs/compound/research/scenario-testing/` for testing reviews)
   f. **Contradiction detection**: If a reviewer finding contradicts a high-severity lesson (severity >= P1), flag the contradiction for human review via `AskUserQuestion` with both the finding and the lesson content. Do not auto-resolve contradictions.
   > See `review/references/lesson-calibration.md` for detailed calibration guidance
6. Search memory with `ca search` for known patterns and recurring issues (broader search beyond per-reviewer calibration)
7. Select reviewer tier based on diff size:
   - **Small** (<100 lines): 4 core -- security, test-coverage, simplicity, cct-subagent
   - **Medium** (100-500): add architecture, performance, scenario-coverage, pattern-matcher (8 total)
   - **Large** (500+): all reviewers including doc-gardener, drift-detector, runtime-verifier
8. **Runtime Verification (contract-driven)**: Spawn `runtime-verifier` when the Verification Contract requires runtime proof.
   - If `Required evidence` includes `runtime_startup`, `browser_evidence`, or `contract_checks`, spawn `runtime-verifier`
   - **Web UI project**: runtime-verifier validates startup and browser-level behavior
   - **HTTP API project**: runtime-verifier validates startup and representative request/response behavior
   - **CLI/library/service without runtime evidence in the contract**: **SKIP** runtime-verifier and record INFO ("Runtime verification not required by Verification Contract")
   - Role skill: `.claude/skills/compound/agents/runtime-verifier/SKILL.md`
   - Timeout: 5min total suite, 2min per individual test
   > See RV-1 through RV-5 in epic for full requirements
9. **QA Engineer (required when contract asks for browser/UI evidence)**:
   - If `Required evidence` includes `browser_evidence`, `responsive_check`, `edge_states_check`, `console_network_clean`, or `a11y_smoke`, invoke the QA Engineer skill and treat its findings as part of the blocking review result
   - Otherwise, use QA Engineer optionally when reviewers request hands-on verification
   - Skill: `.claude/skills/compound/qa-engineer/SKILL.md`
   - Primary triggers: contract-required browser/UI evidence, visual changes (CSS, HTML, component files), new pages/routes, form modifications, accessibility-related changes
   - The QA Engineer complements runtime-verifier (step 8): runtime-verifier covers automated contract tests, QA Engineer covers exploratory/visual/boundary testing
   - When the Verification Contract requires browser/UI evidence, this step is **not optional**
   - Can also run between review cycles in the infinity loop (see `review-fleet.md`)
10. **Design Craft Review (contract-driven)**: Spawn `design-craft-reviewer` when the Verification Contract requires design quality proof.
   - If `Required evidence` includes `design_craft_check`, spawn `design-craft-reviewer`
   - The reviewer evaluates changed UI code against the `build-great-things` quality checklist: states (loading/empty/error), interaction feedback (hover/active/focus/transitions), visual craft (spacing scale, typography hierarchy, color semantics, shadows, borders), motion, responsiveness, and accessibility
   - **Non-UI projects without `design_craft_check` in the contract**: **SKIP** and record INFO ("Design craft review not required by Verification Contract")
   - Role skill: `.claude/skills/compound/agents/design-craft-reviewer/SKILL.md`
10b. **Visual Verification (contract-driven)**: When the Verification Contract includes `browser_evidence`, `design_craft_check`, or `responsive_check`, take Playwright screenshots as evidence.
   - Auto-detect: Use the QA Engineer detection priority (see `.claude/skills/compound/qa-engineer/SKILL.md` Phase 1) to check for a runnable UI. If no UI framework detected, **SKIP** and record INFO.
   - **If UI detected**: Start the dev server in the background, wait for HTTP readiness (poll every 1s, timeout 30s), then take headless Playwright screenshots at 4 viewports: 375px (mobile), 768px (tablet), 1024px (small desktop), 1440px (desktop). Navigate key routes (up to 10) and screenshot each.
   - **Evidence**: Save screenshots alongside review artifacts. Reference them in the Verification Contract evidence table as proof for `browser_evidence` or `responsive_check`.
   - **Visual critique**: Include layout, spacing, contrast, hierarchy, and responsive observations in the review findings with screenshot references.
   - **Graceful degradation**: If Playwright is unavailable, record a **P3/INFO** finding ("Playwright not available for visual verification") and proceed with code-only review. Tag visual concerns with [NEEDS_QA] for the QA Engineer.
   - **Cleanup**: Stop the dev server after screenshot capture.
11. Spawn reviewers in an **AgentTeam** (TeamCreate + Task with `team_name`):
   - Role skills: `.claude/skills/compound/agents/{security-reviewer,architecture-reviewer,performance-reviewer,test-coverage-reviewer,simplicity-reviewer,scenario-coverage-reviewer}/SKILL.md`
   - Security specialist skills (on-demand, spawned by security-reviewer): `.claude/skills/compound/agents/{security-injection,security-secrets,security-auth,security-data,security-deps}/SKILL.md`
   - Runtime verifier (conditional, see step 8): `.claude/skills/compound/agents/runtime-verifier/SKILL.md`
   - Design craft reviewer (conditional, see step 10): `.claude/skills/compound/agents/design-craft-reviewer/SKILL.md`
   - For large diffs (500+), deploy MULTIPLE instances; split files across instances, coordinate via SendMessage
12. Reviewers communicate findings to each other via `SendMessage`
13. Collect, consolidate, and deduplicate all findings (including QA Engineer findings from step 9 and design craft findings from step 10)
14. Classify by severity: P0 (blocks merge), P1 (critical/blocking), P2 (important), P3 (minor)
15. Use `AskUserQuestion` when severity is ambiguous or fix has multiple valid options
16. Create beads issues for P1 findings: `bd create --title="P1: ..."`
17. Verify spec alignment: flag unmet EARS requirements as P1, flag requirements met but missing from acceptance criteria as gaps
18. Fix all P1 findings before proceeding
19. Run `/implementation-reviewer` as mandatory gate
20. Capture novel findings with `ca learn`; pattern-matcher auto-reinforces recurring issues

## Acceptance Criteria Review Protocol
When checking AC, produce a summary table in the review report:

| AC ID | Criterion | Status | Evidence |
|-------|-----------|--------|----------|
| AC-1  | When X... | PASS/FAIL | test file, line N / manual check |

All AC rows must be PASS for the review to proceed to `/implementation-reviewer`.

## Verification Contract Review Protocol
When checking the Verification Contract, produce a second summary table in the review report:

| Evidence | Status | Proof | Notes |
|----------|--------|-------|-------|
| build | PASS/FAIL | command output / artifact | optional detail |

Rules:
- Every item in `Required evidence` must be marked PASS, FAIL, or ESCALATED
- `ESCALATED` means review strengthened the contract because the planned evidence was too weak for the actual risk
- Missing runtime/browser/UI evidence is a blocking review outcome, not a polish suggestion
- If the contract is absent, record a P1 process finding and review against the legacy floor (`test`, `lint`) plus obvious risk-based evidence

## Lesson-Calibrated Review Protocol
Reviewers are pre-loaded with relevant lessons before they begin reviewing:

### Per-Reviewer Calibration
Each reviewer receives lessons filtered by their domain:
- **security-reviewer**: `ca search "security vulnerability injection XSS"`
- **test-coverage-reviewer**: `ca search "testing coverage TDD mock"`
- **simplicity-reviewer**: `ca search "complexity refactor simplify"`
- **architecture-reviewer**: `ca search "architecture module boundary coupling"`
- **performance-reviewer**: `ca search "performance optimization latency"`
- **design-craft-reviewer**: `ca search "design craft visual hierarchy spacing motion states"`
- **pattern-matcher**: `ca search "pattern recurring mistake"`

### Calibration Rules
- **Cap**: 3-5 lessons per reviewer (prevents context dilution)
- **Recency bias**: Prefer lessons from the last 30 days; older lessons included only if severity >= P1
- **Category filter**: Match lesson tags to reviewer domain; discard unrelated results
- **Research supplement**: Each reviewer may also receive relevant research excerpts from `docs/research/`

### Contradiction Handling (LCR-3)
When a reviewer produces a finding that directly contradicts a calibration lesson:
1. Flag the contradiction with both the finding and the lesson text
2. Escalate via `AskUserQuestion` -- do NOT auto-resolve
3. Record resolution via `ca learn` to prevent future contradictions

## Memory Integration
- Run `ca search` before review for known recurring issues
- **LCR**: Per-reviewer calibration queries (see Lesson-Calibrated Review Protocol above)
- **pattern-matcher** auto-reinforces: recurring findings get severity increased via `ca learn`
- **cct-subagent** reads CCT patterns for known Claude failure patterns
- Capture the review report via `ca learn` with `type=solution`

## Runtime Verification Integration
When the runtime-verifier is triggered by the Verification Contract:
- Verifier generates ephemeral Playwright tests against a running application instance
- Findings are reported in standard P0-P3 format and merged with other reviewer findings
- If the app cannot be started: report as **P1/INFRA** with diagnostics (not silent skip)
- If no runtime target exists for the required evidence: report as **P1/INFRA** or **P3/INFO SKIPPED** with justification
- Verifier uses Playwright/Puppeteer **library APIs** (code generation), NOT browser MCP tools

## Docs Integration
- **doc-gardener** checks code/docs alignment and ADR compliance
- Flags undocumented public APIs and ADR violations

## Literature
- Consult `docs/compound/research/scenario-testing/` for runtime verification methodology and testing best practices
- Consult `docs/compound/research/code-review/` for systematic review methodology, severity taxonomies, and evidence-based review practices
- Run `ca knowledge "code review methodology"` for indexed knowledge on review techniques
- Run `ca search "review"` for lessons from past review cycles

## Common Pitfalls
- Ignoring reviewer feedback because "it works"
- Not running all 12 reviewer perspectives (skipping dimensions)
- Treating all findings as equal priority (classify P1/P2/P3 first)
- Not creating beads issues for deferred fixes
- Skipping quality gates before review
- Bypassing the implementation-reviewer gate
- Not checking CCT patterns for known Claude mistakes
- Not checking acceptance criteria from the epic description
- Not checking the Verification Contract from the epic description
- Not calibrating reviewers with past lessons (LCR skip)
- Running runtime-verifier when the Verification Contract does not require runtime proof
- Skipping runtime-verifier when the Verification Contract does require runtime proof
- Silently skipping runtime-verifier when build fails (must report P1/INFRA)
- Not invoking QA Engineer when the Verification Contract requires browser/UI evidence
- Not spawning design-craft-reviewer when the Verification Contract includes `design_craft_check`
- Skipping design-craft-reviewer for non-UI projects that don't have `design_craft_check` in the contract (correct behavior — not a pitfall)
- Not taking visual screenshots when the Verification Contract requires `browser_evidence` or `responsive_check` (reviewers should see what users see)
- Taking screenshots on non-UI projects (waste of time — auto-detect first)

## Quality Criteria
- Baseline quality gates pass (`pnpm test`, `pnpm lint`)
- `pnpm build` passed when the Verification Contract required build evidence
- All 12 reviewer perspectives were applied in parallel
- Findings are classified P0/P1/P2/P3 and deduplicated
- **Verification Contract checked and all required evidence verified**
- **Reviewers were calibrated with 3-5 relevant lessons each (LCR)**
- **Research references were consulted for applicable review domains**
- **Lesson contradictions were flagged for human review (LCR-3)**
- pattern-matcher checked memory and reinforced recurring issues
- cct-subagent checked against known Claude failure patterns
- doc-gardener confirmed docs/ADR alignment
- security-reviewer P0 findings: none (blocks merge)
- security-reviewer P1 findings: all acknowledged or resolved
- **Runtime verifier ran when required by the Verification Contract or reported why it was not required**
- **Design craft reviewer ran when `design_craft_check` was in the Verification Contract or reported why it was not required**
- **QA Engineer invoked when contract-required browser/UI evidence was in scope**
- **Visual screenshots taken at 4 viewports when contract requires browser/UI evidence, or INFO recorded explaining why skipped**
- All P1 findings fixed before `/implementation-reviewer` approval
- All spec requirements verified against implementation
- **All acceptance criteria checked and verified (PASS/FAIL)**
- **All Verification Contract evidence checked and verified (PASS/FAIL/ESCALATED)**
- scenario-coverage-reviewer verified scenario table coverage (medium+ diffs)
- `/implementation-reviewer` approved as mandatory gate

## PHASE GATE 4 -- MANDATORY
Before starting Compound, verify review is complete:
- `/implementation-reviewer` must have returned APPROVED
- All P1 findings must be resolved
- **All acceptance criteria must be PASS**
- **All Verification Contract evidence must be PASS or explicitly escalated and resolved**

**CRITICAL**: Use `ca learn` for ALL lesson storage -- NOT MEMORY.md.
