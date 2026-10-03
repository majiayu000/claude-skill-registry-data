---
name: autoplan
description: Automated full review pipeline skill. Use when the user wants to run a complete plan review in one command, automatically chain CEO review then design review then engineering review then DX review, surface only the decisions that need human taste judgment, or compress the full planning workflow into a single structured output.
---

# AutoPlan — Automated Full Review Pipeline

## 1. Purpose & Trigger Conditions

AutoPlan compresses the full planning review gauntlet into a single structured command. Instead of running CEO → Design → Engineering → DX reviews sequentially and answering 15–30 intermediate questions, AutoPlan auto-decides everything resolvable by principle and surfaces only **taste decisions** to the human.

### Activate when the user says any of:
- "autoplan", "auto plan", "auto-plan"
- "run all reviews", "run the full review"
- "review this plan automatically"
- "make the decisions for me"
- "compress the planning workflow"
- "full review pipeline"
- "one-command review"

### Proactively suggest AutoPlan when:
- A plan file (`PLAN.md`, `plan.md`, `spec.md`, `SPEC.md`) is detected in the repo root
- The user has just finished `/spec` or `/office-hours` and has a document ready to review
- The user asks "what next?" after writing a plan

---

## 2. Pre-Flight: Context Ingestion

Before running any sub-review, ingest all available context:

```bash
# Detect plan file
PLAN_FILE=$(ls PLAN.md plan.md SPEC.md spec.md PRD.md prd.md 2>/dev/null | head -1)
echo "PLAN_FILE: ${PLAN_FILE:-none}"

# Detect git context
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
DIRTY=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
echo "BRANCH: $BRANCH | DIRTY_FILES: $DIRTY"

# Detect project type signals
HAS_UI=$(find . -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" 2>/dev/null | head -1)
HAS_API=$(find . -name "routes.ts" -o -name "routes.js" -o -name "router.py" -o -name "*.proto" 2>/dev/null | head -1)
HAS_CLI=$(grep -r "argparse\|click\|cobra\|clap\|commander" . --include="*.py" --include="*.go" --include="*.rs" --include="*.ts" -l 2>/dev/null | head -1)
HAS_ARCH=$(find . -name "*.arxml" -o -name "*.dbc" -o -name "*.ldf" -o -name "system_design*" 2>/dev/null | head -1)
HAS_EMBEDDED=$(find . -name "*.c" -o -name "*.cpp" -o -name "*.h" 2>/dev/null | head -1)

echo "HAS_UI: ${HAS_UI:-none}"
echo "HAS_API: ${HAS_API:-none}"
echo "HAS_CLI: ${HAS_CLI:-none}"
echo "HAS_ARCH: ${HAS_ARCH:-none}"
echo "HAS_EMBEDDED: ${HAS_EMBEDDED:-none}"
```

Read the plan file fully before proceeding. If no plan file is found, ask the user to paste the plan inline or point to a file path.

---

## 3. Review Type Detection

Use the following signals to determine which sub-reviews apply. At minimum, **CEO review and Engineering review always run**. Others are conditional.

| Review         | Trigger Condition                                                                  |
|----------------|------------------------------------------------------------------------------------|
| CEO Review     | Always runs — scope, value, risk, prioritization                                   |
| Design Review  | `HAS_UI` is non-empty, OR plan mentions "UI", "screen", "layout", "component", "design system", "visual" |
| Eng Review     | Always runs — architecture, data model, interfaces, scalability, safety/security   |
| DX Review      | `HAS_API` or `HAS_CLI` is non-empty, OR plan mentions "API", "CLI", "SDK", "developer", "integration", "endpoint" |
| Embedded/Auto  | `HAS_EMBEDDED` or `HAS_ARCH` is non-empty, OR plan mentions "ECU", "AUTOSAR", "CAN", "LIN", "embedded", "RTOS", "ISO 26262", "21434" |

Print which reviews will run before starting:

```
🔍 AutoPlan will run: [CEO] [Eng] [Design?] [DX?] [Embedded?]
   Based on detected signals: HAS_UI=<val> HAS_API=<val> HAS_CLI=<val>
   Plan file: <file or inline>
   Starting pipeline...
```

---

## 4. The Six Auto-Decision Principles

AutoPlan makes autonomous decisions using these six principles. Reference them when recording auto-decisions in the output.

1. **Scope Minimization** — When two approaches differ in scope, prefer the smaller one unless the larger is justified by a stated user goal.
2. **Reversibility Preference** — Prefer decisions that are easy to reverse or rollback over irreversible architectural commitments.
3. **Proven Over Novel** — Prefer established patterns, libraries, and protocols over novel/experimental ones unless novelty is the explicit goal.
4. **Explicit Over Implicit** — Prefer explicit contracts (typed APIs, schemas, defined interfaces) over implicit or convention-based ones.
5. **Safety First** — Any decision touching safety-critical or security-sensitive surfaces automatically applies the most conservative option.
6. **User Goal Alignment** — When in doubt, re-read the stated user goal at the top of the plan and choose the option that most directly serves it.

Auto-decided items are tagged: `[AUTO: Principle N]`
Items needing human taste judgment are tagged: `[TASTE GATE]`

---

## 5. Pipeline Execution Order

Execute sub-reviews in this exact sequence. Each review reads the plan, applies its lens, and emits findings into a shared accumulator.

### 5.1 Phase 1 — CEO Review

**Lens:** Strategic value, market timing, prioritization, risk/reward, resource fit.

Auto-decide:
- Whether to defer features marked "nice to have" with no stated deadline → `[AUTO: Principle 1]` defer them
- Whether to accept scope that contradicts the stated user goal → `[AUTO: Principle 6]` flag as out-of-scope
- Standard prioritization of P0 (launch blocker) vs P1 (fast follow) vs P2 (future) features

Surface as `[TASTE GATE]`:
- Trade-offs where business value is genuinely close (e.g., "build vs buy" with similar cost profiles)
- Strategic bets that depend on market timing the AI cannot evaluate
- Any scope item where the user's appetite for risk is the deciding factor

CEO Review Output Format:
```
### CEO Review
**Strategic Fit:** <1-sentence verdict>
**Scope Decision:** <what's in / out and why>
**Risk Rating:** Low / Medium / High — <rationale>
**Auto-Decisions:**
  - [AUTO: P1] <decision>
**Taste Gates:**
  - [TASTE GATE] <question for human>
```

---

### 5.2 Phase 2 — Design Review

**Skip if:** Design signals are absent (see Section 3).

**Lens:** UX coherence, visual hierarchy, accessibility, consistency with design system, component reuse.

Auto-decide:
- Standard accessibility requirements (WCAG 2.1 AA minimum) → `[AUTO: Principle 5]`
- Consistency with existing design system tokens if detectable in codebase
- Responsive breakpoints following industry norms (mobile-first unless plan states otherwise)
- Animation/motion: default to `prefers-reduced-motion` safe → `[AUTO: Principle 5]`

Surface as `[TASTE GATE]`:
- Aesthetic direction when two valid design approaches exist (e.g., minimal vs expressive)
- Brand-specific decisions (colors, typeface, illustration style) not derivable from codebase
- Information architecture choices that depend on user mental models the AI cannot validate
- Any component that could go either "custom build" or "use existing library" with meaningful trade-offs

Design Review Output Format:
```
### Design Review
**UX Verdict:** <coherence assessment>
**Accessibility:** <pass/concern + specifics>
**Design System Fit:** <consistent / gaps found>
**Auto-Decisions:**
  - [AUTO: P3] Use existing component library for <X> — no custom build needed
**Taste Gates:**
  - [TASTE GATE] <aesthetic decision needing human judgment>
```

---

### 5.3 Phase 3 — Engineering Review

**Always runs.**

**Lens:** Architecture, data model, API contracts, scalability, testability, functional safety, cybersecurity, coding standard compliance.

Auto-decide using the six principles:
- Database normalization level (default: 3NF unless plan requires denormalization for performance) → `[AUTO: Principle 3]`
- Error handling strategy (explicit typed errors over generic exceptions) → `[AUTO: Principle 4]`
- Auth mechanism (prefer established OAuth2/OIDC over custom schemes) → `[AUTO: Principle 3]`
- Encryption at rest and in transit (always on for any user data or safety-critical data) → `[AUTO: Principle 5]`
- Interface contracts (typed schemas, Protobuf/OpenAPI over untyped JSON blobs) → `[AUTO: Principle 4]`
- Test coverage floor: minimum 80% unit coverage for business logic → `[AUTO: Principle 5]`
- MISRA/CERT compliance when embedded C/C++ is present → `[AUTO: Principle 5]`
- ISO 26262 ASIL determination when safety-critical automotive context is detected → `[AUTO: Principle 5]`
- Prefer stateless services unless statefulness is explicitly required → `[AUTO: Principle 1]`
- Prefer idempotent APIs → `[AUTO: Principle 2]`

Surface as `[TASTE GATE]`:
- Architecture topology decisions where two valid patterns exist and the trade-off is genuine (e.g., monolith vs microservices at this scale)
- Data model decisions where normalization vs. performance is a real trade-off requiring business context
- Vendor/dependency lock-in trade-offs (e.g., AWS-native vs cloud-agnostic)
- Any decision where the "right" answer depends on team skill set or organizational capability

Automotive/Embedded-specific (when `HAS_EMBEDDED` or `HAS_ARCH`):
- Assign ASIL level from plan context (A/B/C/D); default to ASIL-B if unclear → `[AUTO: Principle 5]`
- Apply MISRA C:2012 rules to all generated C/C++ → `[AUTO: Principle 5]`
- Flag any heap allocation in safety-critical paths → `[AUTO: Principle 5]`
- Apply ISO/SAE 21434 threat analysis hooks if cybersecurity context detected → `[AUTO: Principle 5]`

Engineering Review Output Format:
```
### Engineering Review
**Architecture Verdict:** <sound / concerns>
**Data Model:** <approved / issues>
**Security Posture:** <pass / gaps>
**Safety (if applicable):** ASIL-<X> / <standard applied>
**Auto-Decisions:**
  - [AUTO: P4] Typed API contracts via OpenAPI spec — no untyped JSON
  - [AUTO: P5] TLS 1.3 enforced for all service communication
**Taste Gates:**
  - [TASTE GATE] <architectural trade-off needing human judgment>
**Open Issues (blocking):**
  - <anything that must be resolved before implementation>
```

---

### 5.4 Phase 4 — DX Review

**Skip if:** No API, CLI, or SDK signals detected (see Section 3).

**Lens:** Developer experience, API ergonomics, CLI usability, SDK onboarding, documentation completeness, error message quality.

Auto-decide:
- REST naming conventions (noun-based resource paths, HTTP verbs correct) → `[AUTO: Principle 4]`
- Versioning strategy (URL versioning `/v1/` as default unless plan specifies header versioning) → `[AUTO: Principle 3]`
- Error response shape (RFC 7807 Problem Details as default) → `[AUTO: Principle 3]`
- CLI help text and `--help` flag required for all commands → `[AUTO: Principle 4]`
- Exit codes follow POSIX convention → `[AUTO: Principle 3]`
- SDK typed clients preferred over raw HTTP examples in docs → `[AUTO: Principle 4]`

Surface as `[TASTE GATE]`:
- API style trade-offs (REST vs GraphQL vs gRPC) when the plan hasn't committed
- Pagination strategy (cursor vs offset) when both are valid for the data shape
- CLI command naming that depends on team conventions not visible in codebase

DX Review Output Format:
```
### DX Review
**API Ergonomics:** <good / issues>
**CLI Usability:** <good / issues / N/A>
**Documentation Gaps:** <list or "none">
**Auto-Decisions:**
  - [AUTO: P3] RFC 7807 error envelope for all 4xx/5xx responses
**Taste Gates:**
  - [TASTE GATE] <DX trade-off needing human judgment>
```

---

## 6. Conflict Resolution

When sub-reviews produce contradictory findings, resolve conflicts using this hierarchy:

1. **Safety always wins.** If Engineering flags a safety or security concern, it overrides Design or DX convenience.
2. **CEO scope decisions constrain all other reviews.** If CEO cuts a feature, Design and Eng reviews for that feature are voided.
3. **Eng and DX conflicts:** Prefer the more explicit/typed/reversible option per Principles 2 and 4.
4. **Design and DX conflicts:** Prefer the developer-facing contract (DX) over visual presentation when they contradict on data shape; prefer Design when the conflict is purely presentational.
5. **Unresolvable conflicts** become `[TASTE GATE]` items surfaced at the approval gate.

When a conflict is resolved automatically, log it:
```
⚠️  CONFLICT RESOLVED: Design preferred custom date picker; Eng flagged a11y risk.
    Resolution [AUTO: P5]: Use platform-native date input — accessibility takes priority.
```

---

## 7. Output Format — Consolidated Plan

After all sub-reviews complete, emit a single consolidated output in this structure:

```
═══════════════════════════════════════════════════════
  AUTOPLAN REVIEW — <Plan Title or Filename>
  Ran: <which reviews ran>  |  Date: <today>
═══════════════════════════════════════════════════════

## Executive Summary
<2–3 sentence overall verdict: is the plan ready to implement, needs minor fixes, or has blockers?>

## Scope (Final)
**In Scope:**
  - <item>
**Out of Scope (deferred):**
  - <item> [AUTO: P1 — deferred, no stated deadline]
**Blocked (needs resolution before start):**
  - <item>

## Auto-Decisions Log
All decisions made automatically by principle. No human input needed.

| # | Decision | Principle | Rationale |
|---|----------|-----------|-----------|
| 1 | <decision> | P3 | <why> |
| 2 | <decision> | P5 | <why> |
...

## ⚡ Taste Gates — Human Approval Required
These are the ONLY items requiring your judgment. Everything else has been decided.

### TASTE GATE 1: <Topic>
**Context:** <what the trade-off is>
**Option A:** <description> — *Recommended if <condition>*
**Option B:** <description> — *Recommended if <condition>*
**Impact if wrong:** <reversible in a sprint / hard to undo / irreversible>

### TASTE GATE 2: <Topic>
...

## Review Findings (Detail)
<CEO Review block>
<Design Review block (if ran)>
<Engineering Review block>
<DX Review block (if ran)>

## Conflicts Resolved
<list of auto-resolved conflicts, or "None">

## Definition of Done
See Section 10 below — pre-populated with items derived from this plan.
```

---

## 8. Fast Path vs Thorough Path

### Fast Path (`autoplan --fast` or user says "quick review")
- CEO + Eng only, always
- Design and DX skipped even if signals are present
- Auto-decide all taste gates using the **recommended** option
- Output is a single short verdict block (no detailed sub-review sections)
- Use when: the user wants a sanity check before a quick experiment, not a production ship

Fast Path output:
```
⚡ AUTOPLAN FAST
Verdict: <GO / NO-GO / CONDITIONAL>
Key risks: <1–3 bullets>
Auto-decided taste gates: <list of what was assumed>
Next: <one actionable step>
```

### Thorough Path (default)
- All applicable reviews run
- All taste gates surfaced
- Full consolidated output as per Section 7
- Use when: plan is headed toward production, team sign-off needed, or the plan is complex

---

## 9. Integration with Upstream Skills

### From `/spec` or `/office-hours`
If the user just completed a `/spec` or `/office-hours` session, AutoPlan can ingest the output directly:
- Read `SPEC.md` or the last written plan file automatically
- Skip the "paste your plan" prompt
- Reference spec decisions already made to avoid re-litigating them in reviews

### Handing off downstream
After AutoPlan completes:
- If taste gates are approved → suggest next action: "Ready to implement. Run `/ship` when code is done or start with `<first task>`."
- If taste gates are rejected/modified → update the consolidated plan inline with the user's choices and re-emit the Definition of Done
- If blockers exist → do not suggest implementation; surface the blockers as the only next step

---

## 10. Definition of Done Checklist

AutoPlan generates a pre-populated DoD from the plan and review findings. Template:

```markdown
## Definition of Done — <Plan Title>
Generated by AutoPlan on <date>

### Scope
- [ ] All In-Scope items from the plan are implemented
- [ ] All Out-of-Scope items are documented as deferred (not built)

### Engineering
- [ ] All [AUTO] architectural decisions are implemented as specified
- [ ] Taste Gate decisions are reflected in the implementation
- [ ] Unit test coverage ≥ 80% on business logic
- [ ] Integration tests cover all critical user paths
- [ ] No MISRA/CERT violations (if embedded) — static analysis clean
- [ ] ASIL-<X> requirements met and documented (if automotive)
- [ ] Security: TLS enforced, auth validated, secrets not hardcoded
- [ ] All API contracts match the OpenAPI/schema spec

### Design (if applicable)
- [ ] WCAG 2.1 AA passes (run axe or Lighthouse)
- [ ] Responsive layout validated at mobile / tablet / desktop breakpoints
- [ ] Reduced-motion mode verified
- [ ] Design system tokens used (no hardcoded colors/spacing)

### DX (if applicable)
- [ ] API versioning implemented (`/v1/` prefix or agreed scheme)
- [ ] Error responses follow RFC 7807 shape
- [ ] All CLI commands have `--help` text and correct exit codes
- [ ] SDK/client examples updated to reflect final API shape

### Taste Gate Resolutions
- [ ] Taste Gate 1: <topic> — resolved as <option chosen>
- [ ] Taste Gate 2: <topic> — resolved as <option chosen>

### Review & Sign-off
- [ ] AutoPlan consolidated output reviewed by team lead
- [ ] No blocking issues remain open
- [ ] Plan file updated with all Auto-Decisions and Taste Gate resolutions
- [ ] Change committed: `git add <plan file> && git commit -m "docs: finalize autoplan review outputs"`
```

---

## 11. Spawned / Headless Mode

When running inside a CI pipeline, orchestrator, or spawned sub-agent session (`SESSION_KIND=spawned` or `GSTACK_HEADLESS=true`):

- **Do not** use `AskUserQuestion` or any interactive prompt
- Auto-decide ALL taste gates using the **recommended** option (Option A by convention)
- Log every auto-decided taste gate clearly: `[TASTE GATE AUTO-DECIDED: <topic> → Option A: <description>]`
- Emit the full consolidated output as prose
- End with a machine-parseable completion block:

```
AUTOPLAN_RESULT: COMPLETE
BLOCKING_ISSUES: <count>
TASTE_GATES_SURFACED: <count>
TASTE_GATES_AUTO_DECIDED: <count>
REVIEWS_RAN: CEO,ENG[,DESIGN][,DX][,EMBEDDED]
NEXT_ACTION: <one string>
```

---

## 12. Edge Cases & Recovery

### No plan file found
Ask once:
> I couldn't find a plan file (PLAN.md, SPEC.md, etc.). Please paste your plan inline or tell me the file path.

If the user pastes inline, treat the paste as the plan and proceed normally.

### Plan is too vague to review
If the plan is fewer than 5 substantive lines or contains only placeholders:
- Do not run the full pipeline
- Return: "This plan is too early-stage for a full review. Run `/office-hours` first to shape it, then come back."

### Mid-pipeline failure
If a sub-review cannot complete (e.g., missing context, ambiguous plan section):
- Mark that review as `[SKIPPED — insufficient context]`
- Continue with remaining reviews
- Note the skip in the Executive Summary

### Conflicting user instructions
If the user says "skip design review" but design signals are strong (e.g., plan has 8 UI sections):
- Respect the user instruction, skip Design review
- Add a one-line note: `Design review skipped by user request. Note: plan has significant UI scope.`

---

## 13. Automotive & Safety-Critical Addendum

When automotive/embedded context is detected, AutoPlan applies additional review logic:

### AUTOSAR Compliance Check
- Verify that software component (SWC) interfaces are defined before implementation
- Flag any plan item that bypasses RTE abstraction as a blocker
- Auto-apply: BSW module reuse over custom implementations `[AUTO: P3]`

### Functional Safety (ISO 26262)
- Derive ASIL from the plan's stated system function and failure mode impact
- Default ASIL-B if unclear; flag as `[TASTE GATE]` if the user must confirm
- Check: FMEA/FMEDA mentioned? If not, flag as a gap
- Check: Safety mechanisms (redundancy, watchdog, plausibility checks) present in the design?

### Cybersecurity (ISO/SAE 21434)
- Check: TARA (Threat Analysis and Risk Assessment) referenced?
- Auto-apply: Secure boot, signed firmware, encrypted OTA as non-negotiable if OTA is in scope `[AUTO: P5]`
- Flag: Any plan item that stores keys in plaintext or skips certificate pinning

### Network Protocol Validation
- Verify CAN/CAN-FD message IDs don't collide with standard diagnostic IDs (0x7DF, 0x7E0–0x7EF)
- Flag LIN schedule table completeness if LIN frames are defined in the plan
- Check Ethernet configuration for VLAN segmentation if mixed-criticality traffic is present

---

## 14. Example Run (Illustrative)

**User:** "autoplan"

**AutoPlan response:**

```
🔍 AutoPlan starting...
   Plan file: PLAN.md (247 lines)
   Reviews: [CEO] [ENG] [DESIGN] — DX skipped (no API/CLI signals)
   Ingesting plan...

═══════════════════════════════════════════════════════
  AUTOPLAN REVIEW — "Zone Controller Refactor"
  Ran: CEO, Engineering, Design  |  Date: 2026-07-22
═══════════════════════════════════════════════════════

## Executive Summary
The plan is implementable with two minor scope clarifications and one architectural
decision pending human input. No blocking issues. Recommend proceeding after the
single taste gate below is resolved.

## Auto-Decisions Log
| # | Decision | Principle | Rationale |
|---|----------|-----------|-----------|
| 1 | Defer "multi-zone sync v2" to P2 | P1 | No deadline stated, adds 3 sprints |
| 2 | Use AUTOSAR BSW module for NVM | P3 | Existing BSW available; custom NVM risky |
| 3 | ASIL-B assigned to zone controller | P5 | Body control function; injury risk low-medium |
| 4 | Typed ARXML interface before code | P4 | Interface-first prevents integration rework |

## ⚡ Taste Gates — Human Approval Required

### TASTE GATE 1: State machine implementation approach
**Context:** Zone controller state machine could be implemented in Stateflow (MBD path)
or hand-coded C with a state table (traditional path). Both are ASIL-B compliant.
**Option A:** Stateflow / MBD — auto-generates MISRA-compliant C, easier to review visually
**Option B:** Hand-coded state table in C — more portable, no toolchain dependency
**Impact if wrong:** Hard to change mid-sprint; choose now.

## Definition of Done
[pre-populated checklist — see Section 10]
```

---

## 15. Skill Completion Signal

After emitting all output, always end with:

```
✅ AutoPlan complete.
   Auto-decisions: <N> | Taste gates: <N> | Blockers: <N>
   Next: <resolve taste gates above, then proceed to implementation>
```

If there are zero taste gates, say:
```
✅ AutoPlan complete — no taste decisions required. Plan is fully decided. Ready to implement.
```
