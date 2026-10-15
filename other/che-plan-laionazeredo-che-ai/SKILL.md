---
name: "che-plan"
description: "Transforms an Approved SPEC into one or more structured tickets (Jira, Linear, ClickUp). Supports single tickets or Epic/Feature structures with sub-tasks, BDD acceptance criteria, and dependency mapping."
---

# Che Plan (Epic & Ticket Generator)

> **SHARED REFERENCES:**
> - Approved SPEC format: `che-spec` skill
> - Engineering contracts (BDD, KISS, DbC): `engineering-contracts` skill
> - Path resolution: `che` CLI (`che compute_paths`, `che ensure_dirs`)

This skill acts as a bridge between technical specification and project management. It ensures that implementation tasks are properly documented, categorized, and linked in external tools.

---

## §0 PRECONDITIONS

1. **Approved SPEC required**: This skill MUST fail if no Approved SPEC is found for the current feature/slug.
2. **MCP Access**: Requires access to `mcp_flockr-linear`, `mcp_laion-clickup`, or a browser-based agent for Jira.
3. **User Input**: Requires Project/Board name and Target Language (default: English).
4. **CANONICAL PRECONDITION TRIO (Vertical + Reversibility + Assertive DbC)**: Parse Approved SPEC YAML frontmatter AND scan §2 SCOPE for literal overrides before any ticket generation.
   4.1 **CANONICAL #0 — Vertical Slice Precondition** (unchanged):
   - **Case A (VERTICAL, default):** `frontmatter.tracer_f0_defined === true` AND §4.5 VERTICAL SLICES table has ≥1 F0 row with Layers Touched ≥ 2 → proceed normally.
   - **Case B (HORIZONTAL OVERRIDE, explicit only):** `frontmatter.vertical_slice_required === false` OR the literal `EXPLICIT_OVERRIDE_HORIZONTAL_PLAN:` + 1-line justification appears verbatim in SPEC §2 SCOPE → proceed, but FIRST append a `[HORIZONTAL_TICKET_PLAN]` entry to decisions.log.jsonl containing the spec_slug, justification verbatim, and count of sub-tasks to be generated.
   - **Case C (INVALID — FAIL HARD):** Neither case above is true. → REJECT with canonical V16/V17 text.
   4.2 **CANONICAL #1 — Reversibility Precondition (TRIGGER per S08 CHE_RULES §X: estimated_files_max >= 5 OR external_deps_count >= 1)**:
   - Parse SPEC for literal `EXPLICIT_OVERRIDE_REVERSIBILITY: <justif>` in §2 SCOPE OR check that header `### §4.6 REVERSIBILITY DECLARATIONS` exists with 3 non-empty sub-tables (V19a Wrapper Boundary, V19b Rollback Flags if applicable, V19c Forking Road).
   - If NEITHER override NOR 3 tables present → REJECT before ticket generation: "CANONICAL #1 Reversibility precondition failed (che-plan §0.4.2). Approved SPEC scope ≥ 5 files or uses ≥ 1 external dep per S08 CHE_RULES, but §4.6 Reversibility Declarations tables (V19a/b/c) are missing AND no EXPLICIT_OVERRIDE_REVERSIBILITY literal in §2. Either (A) re-run che-spec so V19 passes, or (B) get user to add literal `EXPLICIT_OVERRIDE_REVERSIBILITY: <1-line reason ≤120 chars>` to §2 SCOPE, re-approve, then retry."
   4.3 **CANONICAL #3 — Assertive Programming Precondition (TRIGGER per S09 CHE_RULES §X: B_COUNT >= 3)**:
   - If scope `B_COUNT >= 3` (S09): Either SPEC contains valid §4.7 Assertive Programming table (A-1..N rows ≥ ceil(B/3) per S02 CHE_RULES §X), all rows have "CRASH" in last col), OR §2 literal `EXPLICIT_OVERRIDE_DBC_ASSERTIONS: <justif>` exists.
   - Else → REJECT: "CANONICAL #3 DbC Assertive precondition failed per S09 CHE_RULES. B_COUNT=$B >= 3 requires §4.7 Assertive Programming invariants table (V20, density floor per S02) OR explicit override literal. Re-run che-spec to pass V20, or add EXPLICIT_OVERRIDE_DBC_ASSERTIONS to §2."

---

## §1 WORKFLOW

### Step 1: Spec Analysis
1. Read the SPEC from `$CHE_WORKSPACE_SHARED/specs/<slug>/<timestamp>-spec.md` OR from `$CHE_WORKSPACE_SHARED/spec_<slug>.md` (try both, first existing wins).
2. Extract `B_COUNT`, `AB_COUNT`, `change_class`, AND `tracer_f0_defined` from YAML frontmatter. Parse §4.5 VERTICAL SLICES table into a list of slice dictionaries `[{id:F0, bid:[...], layers:[...], done:...}, {id:F1,...}]`.
3. **Pre-decomposition vertical slice validation (G-VS-2 gate here):**
   - If `EXPLICIT_OVERRIDE_HORIZONTAL_PLAN:` NOT found in §2 SCOPE AND `tracer_f0_defined !== true`: HARD REJECT before structure decision. Msg = identical to §0 Precondition #4 Case C.
   - Parse every sub-slice: compute `distinct_layers = len(set(slice.layers))`. Collect list `single_layer_slices = [s.id for s in slices if distinct_layers < 2 AND s.id[-12:] != 'H-OVERRIDE-1']`. If `len(single_layer_slices) >= 3` AND no override → REJECT: "Vertical slice decomposition has $N slices touching only 1 architectural layer each — this is horizontal planning disguised as vertical. Either add 2nd layer to each slice OR declare EXPLICIT_OVERRIDE_HORIZONTAL_PLAN in §2 SCOPE bullet with ≤120 char justification."
4. **Structure Decision** (thresholds per S10 CHE_RULES §X):
   - **Single Ticket**: If `B_COUNT <= 3` AND `estimated_files_max <= 5` AND `change_class` is not `feature` (S10 Single case). If SPEC has exactly 1 slice (F0 only) → Single Ticket always.
   - **Epic/Feature**: Otherwise (S10 Epic case). Create a parent Epic/Feature and decompose into sub-tasks with 1 SUB-TASK PER SLICE ID. DO NOT create sub-tasks that group multiple slices into one. F0 is ALWAYS the first sub-ticket, critical_path=True.

### Step 2: Content Formatting (MANDATORY TEMPLATE)
Every ticket (single or sub-task) MUST follow this structure to ensure alignment with Specflow Phase 3 and CANONICAL #0 Vertical Slicing:

```markdown
# [ID] [COLLABORATION_TAG] Title (Short & Action-oriented)

> **Tag**: [AI-Assisted] | [Human-Driven] | [Collaborative]
> **Roadmap Phase**: [ID from roadmap.md] (Specflow Phase 2)
> **Strategic Intent**: [Link to intent.md] (Specflow Phase 1)
> **🔴 Vertical Slice Ref (CANONICAL #0)**: [F0 | F1 | F2 | ... FN — EXACT ID from SPEC §4.5 VERTICAL SLICES table. Single ticket = F0 always. Epic Parent = F0..FN range. HORIZONTAL_OVERRIDE ticket = F<N>-H-OVERRIDE-1 if applicable.]
> **Layers Touched (≥2 required, unless override)**: [list 2+ top-level folders from SPEC §4.5 column 4, e.g. pages/ · app/api/ · packages/db/. Single-layer tickets PROHIBITED unless override logged.]
> **🔵 Wrapper Boundaries Touched (CANONICAL #1 Reversibility)**: [List §4.6.1 V19a wrapper globs + external dependency names that this slice modifies. If this task imports ANY SDK outside its wrapper boundary → BLOCK in che-act §0.5. Leave "N/A" if zero external deps.]
> **🟣 Assertion IDs Delivered (CANONICAL #3 DbC)**: [List A-1..N from §4.7 V20 whose invariant enforcement code is added/modified by this ticket. If scope touches ≥3 B-IDs this list must be non-empty. Leave "-" otherwise.]
> **🟤 DRY Rules Touched (V21 DRY Knowledge)**: [List Business Rule rows from §4.8 V21 whose authoritative source is touched. If any rule's single-source module is edited → annotate so downstream consumers are notified in PR review.]

## 📝 Problem Description
[Extract from SPEC §1 WHY]

## 🛠 Functional Requirements
[Extract from SPEC §4.2 Behaviors relevant ONLY to the Vertical Slice Ref listed above — DO NOT include behaviours from other slices. 1 B-ID minimum = F0 ticket.]

## ⚙️ Non-Functional Requirements
[Extract from SPEC §3 Contracts & §7 Hints — relevant to THIS slice only.]

## ⚖️ Mandatory Business Rules
[Extract from SPEC §4.1 Key Rules — rules that apply to B-IDs within THIS vertical slice only.]

## ✅ Acceptance Criteria (BDD Style)
- **Scenario**: [B-ID / AB-ID title — from §4.2 / §4.3 rows covered by this slice per SPEC §4.5 column 3.]
  - **Given** [Given column]
  - **When** [When column]
  - **Then** [Then column]
```

### Step 3: Epic Decomposition (if applicable)
If Epic structure is chosen:
1. **Parent Ticket**: Contains a high-level description, **Goals**, and a **Task Graph** (Mermaid) showing execution order and critical path. Parent MUST explicitly list the vertical slice IDs: `F0 → F1 → F2 → ... → FN` as nodes. **F0 is ALWAYS the first node, marked critical path.**
2. **Sub-tasks**:
   - **PROHIBITED ANTI-PATTERN (HARD FAIL if detected):** NEVER group B-IDs into layer-based logical tasks such as "Data Layer", "API Layer", "UI Layer", "Models only", "Routes only", "Pages only". If keywords `data layer|api layer|ui layer|models|create all|build all endpoints|design all pages` (case-insensitive) appear in ANY sub-task title or description AND no EXPLICIT_OVERRIDE_HORIZONTAL_PLAN logged → HARD REJECT decomposition, log attempt `[HORIZONTAL_TICKET_BLOCKED]` in decisions.log with timestamp + spec_slug + bad_task_title, require user confirmation or override insertion into SPEC §2 before retry.
   - **CANONICAL DECOMPOSITION (MANDATORY):** Group B-IDs EXACTLY ONE SUB-TASK PER VERTICAL SLICE from SPEC §4.5 table. Order = F0 first, then F1, F2, ... FN. Each sub-task title PREFIX = `[<slice_id>] ` (e.g. "[F0] Tracer: Save Event → Dashboard Return"). Each sub-task inherits BDD scenarios ONLY from the B-IDs listed in that slice's "B-IDs / AB-IDs Covered" column of §4.5. NEVER mix B-IDs from 2 different slices into one sub-task unless EXPLICIT_OVERRIDE.
   - Each sub-task gets its own ticket with the Step 2 template above. Vertical Slice Ref field MUST be filled with the EXACT slice ID.
   - **Dependencies**: Establish "blocked by" relations ONLY between consecutive vertical slices: `F0 blocks F1 → F1 blocks F2 → ...`. **NEVER create "API blocks UI" layer-style dependencies.** If a slice legitimately depends on a previous slice's DB migration or route schema — the dependency is slice-to-slice (vertical), not layer-to-layer. Dependencies that cross slices horizontally (e.g. "all DB must be done first") are PROHIBITED unless the parent ticket contains EXPLICIT_OVERRIDE_HORIZONTAL_PLAN justification verbatim AND decision.log entry exists.

### Step 4: External Tool Execution
1. Ask user for:
   - **Target Tool**: Linear (Recommended), ClickUp, or Jira.
   - **Project/Board**: Where the tickets should live.
   - **Language**: English (Default).
2. Call appropriate tool (e.g., `save_issue` for Linear, `clickup_create_task` for ClickUp).
3. If creating an Epic, save the Parent first to get its ID, then set `parentId` for sub-tasks.

---

## §2 RETURN VALUES

Print the results of the creation:
- `PLAN_STRUCTURE=Single|Epic`
- `PARENT_TICKET_ID=<id>`
- `SUBTASKS_COUNT=<count>`
- `TOOL_URL=<link-to-tickets>`

---

## §3 QUALITY GATES
- **BDD Check**: Every sub-task MUST have at least one B-ID or AB-ID mapped to a BDD scenario.
- **Dependency Check**: Epic MUST have at least one dependency link between sub-tasks if `count > 1`.
- **Language Consistency**: Do not mix languages in the same field.
- **Simplicity Bias Check (engineering-contracts §1)**: Prefer the smallest slice that delivers the behaviour; do NOT split or add sub-tasks for completeness. A sub-task MUST NOT carry edge cases the SPEC §1 Non-goals deferred by design.
- **🔴 Gate #4: Vertical Decomposition Compliance (G-VS-2 — CANONICAL #0)**: Run ALL 5 sub-checks below. Any fail → HARD STOP before tool tickets are created; return structured error to user.
  1. **Every sub-task has Vertical Slice Ref filled**: Parse `> **🔴 Vertical Slice Ref (CANONICAL #0)**:` line in every ticket template. If any is empty, `TODO`, or does not match a valid ID from SPEC §4.5 table → FAIL: "Sub-task TITLE missing or invalid Vertical Slice Ref. Must be exactly F0 or F1..FN from the approved SPEC §4.5 VERTICAL SLICES table."
  2. **Sub-task count = SPEC slice count**: If Epic structure: count of sub-tasks generated MUST EQUAL count of non-empty rows in SPEC §4.5 VERTICAL SLICES table. If override case (H-OVERRIDE tickets): slice count may be ≤ 1 per H-OVERRIDE-* tag suffix. Otherwise FAIL: "Number of sub-tasks ($N) ≠ number of slices in §4.5 table ($M). 1 sub-task per vertical slice is the canonical rule. Either add the missing slices to §4.5 table in SPEC or declare override."
  3. **No single-layer sub-tasks without override**: Parse each sub-task Layers Touched line. Split on separator ` · ` or `, `. Count distinct top-level path prefixes. If any sub-task has distinct_layers < 2 AND the sub-task title/description does NOT contain suffix `-H-OVERRIDE-` → FAIL with: "Sub-task [$slice_ref] has only $distinct_layers layer(s) touched — this is horizontal decomposition disguised as slice. Either add at least 1 more architectural layer (UI + API, or API + DB, etc.) OR declare EXPLICIT_OVERRIDE_HORIZONTAL_PLAN in SPEC §2, re-approve SPEC, re-run /che-plan."
  4. **F0 is first, critical path true**: If Epic structure → first generated sub-task is F0 (sorted order), AND Parent ticket Task Graph Mermaid has F0 as entry node, AND F0 dependencies = 0 (blocks all others). FAIL: "F0 (Tracer) MUST be the first sub-task in execution order with no blockers. Any other task depends on F0 being green (vertical plumbing proven)."
  5. **No layer-based keywords without override**: Keyword scan all sub-task titles + descriptions for regex `(Data Layer|API Layer|UI Layer|all models|create all|build all endpoints|all pages first|schema first then)`. If any hit AND SPEC §2 does NOT contain `EXPLICIT_OVERRIDE_HORIZONTAL_PLAN:` literal → FAIL with: "Layer-based anti-pattern keywords detected in sub-task. Use canonical decomposition: 1 sub-task per F0..FN vertical slice from §4.5 SPEC table. Each slice touches ≥2 layers. Override only possible via EXPLICIT_OVERRIDE_HORIZONTAL_PLAN + decision.log."
- **🔴 Gate #5: Canonical Trio Propagation Compliance (Reversibility + DbC + DRY — CANONICAL #1/#3)**: Any sub-task generated for a scope where V19/V20/V21 TRIGGER fired MUST have the 3 new header rows filled (non-empty, not "TODO", not "-" unless genuinely N/A). Enforce:
  1. **Reversibility (CANONICAL #1) gate**: If SPEC has ≥ 1 row in §4.6.1 Wrapper Boundary (V19a), and a sub-task's "Files Affected" list (from §4.5 Layers / Files TOUCHED column, filtered by slice) intersects ANY wrapper glob file → "🔵 Wrapper Boundaries Touched" row MUST list at least 1 wrapper glob + SDK name. If EMPTY → FAIL: "Sub-task [$slice_id] touches files inside wrapper boundary(s) listed in §4.6.1 but header row 🔵 is empty. Must list which wrapper + SDK(s) are affected."
  2. **DbC Assertions (CANONICAL #3) gate**: If B_COUNT ≥ 3 (V20 TRIGGER fired) AND sub-task's B-IDs touch rows in §4.7 whose column 3 ("Where Enforced") paths overlap with this slice's file list → "🟣 Assertion IDs Delivered" row MUST list ≥ 1 A-N assertion ID. If EMPTY → FAIL: "Sub-task touches code paths of assertions from §4.7 but header 🟣 is empty. List A-IDs implemented or refactor so assertion enforcement is delivered in THIS slice (not delayed)."
  3. **DRY Knowledge (V21) gate**: If B_COUNT ≥ 5 (V21 TRIGGER fired) AND sub-task's file list intersects §4.8 col 2 "Authoritative Single-Source Absolute Path" paths for ≥ 1 business rule → "🟤 DRY Rules Touched" row MUST list ≥ 1 rule. If EMPTY → FAIL: "Sub-task edits the Authoritative Single-Source for a DRY business rule listed in §4.8 but header 🟤 is empty. List it so downstream consumers are alerted in PR review."
