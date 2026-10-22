---
name: generate-uat-tests
description: Generate a structured set of human-executable UAT test cases from SPEAKMAN.AI Phase 1/2 outputs and the implemented codebase, traced back to use cases and business requirements. Use when the user wants UAT test cases, QA test scripts, or user-acceptance test documentation.
---

# generate-uat-tests — Human UAT Test Case Generator

You generate a structured set of human-executable UAT test cases from Phase 1/2 SPEAKMAN.AI
outputs and the implemented codebase. The output is a Markdown document a QA tester works
through manually in a browser — not automated tests.

Every test case maps to a UC-ID from the Phase 2 use case catalog, which maps back to a
business requirement from Phase 1. This closes the traceability chain:

```
Business outcome → Requirement → Use Case → UAT test → Pass/Fail → Functionality Score
```

The completed test results feed directly into `/promote-environment 3` (QA→PROD gate), which
reads this file to compute the functionality score.

---

## Step 0 — Collect Inputs

Ask the user:

> "Provide the following:
> 1. Phase 1 SAD output directory (contains raw/business_context_clarifier.txt and raw/business_analyst.txt) — or press Enter to skip
> 2. Phase 2 requirements output directory (contains raw/use_case_catalog.txt, raw/api_schema.txt, etc.) — required
> 3. Project root (the implemented codebase) — press Enter to skip if not available
> 4. Output path for the UAT document (e.g. D:\git\my-project\uat) — will be created if absent
> 5. Application base URL for test steps (e.g. http://localhost:5174) — default: http://localhost:5174"

Store:
- **PHASE1_DIR**: path or null
- **PHASE2_DIR**: path (required — stop if absent)
- **PROJECT_ROOT**: path or null
- **OUTPUT_DIR**: absolute path
- **APP_URL**: base URL testers will use (default `http://localhost:5174`)

---

## Step 1 — Load Contracts

Read everything before generating any test cases. Do not guess at content.

### 1a — Phase 1 (if PHASE1_DIR provided)

Read from `{PHASE1_DIR}/raw/` — skip any file that is absent:

| File | Variable | Contains |
|---|---|---|
| `business_context_clarifier.txt` | P1_CONTEXT | Business goals, intended outcomes, KPIs, success criteria, in-scope/out-of-scope |
| `business_analyst.txt` | P1_REQUIREMENTS | Requirement IDs (FR-XX, NFR-XX) with descriptions and acceptance criteria |

If PHASE1_DIR is null, set P1_CONTEXT = null and P1_REQUIREMENTS = null. Note that requirement
traceability will be limited to UC-IDs only — the Scope Creep detection and business outcome
sections will be omitted.

### 1b — Phase 2 (required)

Read from `{PHASE2_DIR}/raw/`:

| File | Variable | Contains | Required? |
|---|---|---|---|
| `use_case_catalog.txt` | USE_CASES | UC-IDs, actors, Gherkin Given/When/Then, req_refs | Required — stop if absent |
| `api_schema.txt` | API_SCHEMA | All endpoints, request/response shapes, field types | Required |
| `business_analyst.txt` | P2_REQUIREMENTS | Requirement IDs and descriptions (Phase 2 may have refined them) | Optional |
| `field_definitions.txt` | FIELD_DEFS | Field constraints — valid formats, max lengths, allowed values | Optional |

Use P2_REQUIREMENTS if present, otherwise P1_REQUIREMENTS. If both are present, P2_REQUIREMENTS
takes precedence (it is the reviewed version).

### 1c — Codebase scan (if PROJECT_ROOT provided)

Read source files to determine:
- Which routes are implemented (compare against API_SCHEMA for gap detection)
- What features exist beyond the use case catalog (scope creep candidates)
- Confirm the application base URL / port

If PROJECT_ROOT is null, set SCOPE_DELTA = null. Note the omission in the document.

---

## Step 2 — Build the Requirements Index

From the requirements source (P2_REQUIREMENTS or P1_REQUIREMENTS), extract **REQ_INDEX**:
```
[
  { "id": "FR-01", "description": "Users can log in with username and password" },
  { "id": "NFR-03", "description": "All endpoints require authentication except /health" },
  ...
]
```

If no requirements source is available, derive a minimal index from the `req_refs` fields in
USE_CASES — treat the UC title as a stand-in description.

---

## Step 3 — Generate Test Cases

For each UC-ID in USE_CASES, generate one or more test cases. Work through the entire use case
catalog — do not skip any UC-ID.

**One UC → one or more test cases:**
- Always generate a **happy-path** test case (the main success scenario)
- If the UC contains explicit unhappy-path Gherkin scenarios (error cases, rejected inputs,
  access-denied flows), generate one additional test case per scenario
- Mark each test case `type: Happy path` or `type: Negative`

**Test case ID sequence:** TC-001, TC-002, ... across all test cases regardless of UC grouping.

**For each test case, populate all fields:**

| Field | Source / Rule |
|---|---|
| `test_id` | TC-{n:03d} — sequential across the whole document |
| `uc_id` | UC-ID from use case catalog |
| `req_ref` | req_refs from the UC entry (comma-separated); cross-reference REQ_INDEX for descriptions |
| `actor` | actor from the UC |
| `feature` | Short name of the use case (2–5 words, title case) |
| `scenario` | Gherkin scenario title, or "Happy path" / "Negative — {reason}" if no title |
| `type` | Happy path / Negative |
| `preconditions` | Derived from Given clauses + any required system state |
| `steps` | Numbered, human-executable actions (see rules below) |
| `expected_result` | Observable outcome (see rules below) |
| `actual_result` | _(blank — tester fills in)_ |
| `status` | _(blank — tester marks PASS / FAIL / BLOCKED)_ |
| `tester` | _(blank — tester initials or name)_ |
| `date` | _(blank)_ |
| `notes` | _(blank — for deviations, screenshots, observations)_ |

### Step writing rules

Steps must be executable by a non-developer with no access to the database or server logs.

- Write steps as imperative actions: "Click", "Enter", "Navigate to", "Select", "Wait for"
- Name UI elements as they appear in the application (button labels, form field labels, tab names)
- Include all setup: log in, navigate, create prerequisite records
- State data values verbatim: `Name: "Test Client A"`, `IP Ranges: "192.168.1.1/32"`
- For API-only interactions with no UI control, write a curl command the tester can paste into a terminal
- Separate setup, action, and observation into distinct numbered steps — do not combine them
- If a later test case depends on data created by an earlier one, say so explicitly in Pre-conditions

### Expected result rules

- Must be observable and unambiguous: "A green success banner appears with the text 'Scope saved'" — not "scope is saved"
- For list views: "A new row appears in the table with name 'Test Client A' and status 'PENDING'"
- For error cases: state the exact error message visible on screen, or the HTTP status code and body if testing via curl
- Reference field names and labels as they appear in the UI, not JSON field names
- Do not say "it works" or "the action succeeds" — describe what the tester sees

---

## Step 4 — Scope Delta Analysis

Compare the API_SCHEMA routes against the UC-IDs to detect mismatches.

**Untraced features** (in codebase/API schema but not mapped to any UC-ID):
- Identify API endpoints or UI controls that cannot be traced to a UC-ID
- These are scope creep candidates — they were built but not in the requirements

**Unimplemented use cases** (UC-IDs in catalog but no corresponding route):
- Identify UC-IDs where no API endpoint implements the described scenario
- These are potential gaps in the implementation

Build **SCOPE_DELTA**:
```json
{
  "untraced_features": [
    { "endpoint": "POST /api/engagements/{id}/pipeline/gate4/complete",
      "note": "No UC-ID in catalog — possible undocumented gate completion flow" }
  ],
  "unimplemented_uc_ids": [
    { "uc_id": "UC-12", "title": "Export report as PDF", "note": "No route found in codebase" }
  ]
}
```

If PROJECT_ROOT was null, set SCOPE_DELTA = null and note codebase was not scanned.

---

## Step 5 — Write UAT Document

Create `{OUTPUT_DIR}/uat_test_cases.md`. Write the full document using the Write tool — do not
produce a partial stub.

Document structure:

```markdown
# UAT Test Cases

| | |
|---|---|
| Generated | {today ISO date} |
| Phase 2 source | {PHASE2_DIR} |
| Phase 1 source | {PHASE1_DIR or "not provided"} |
| Application URL | {APP_URL} |
| Total test cases | {count} |
| UC-IDs covered | {covered} / {total} |
| Happy path | {count} |
| Negative | {count} |

---

## Business Outcomes (Traceability Anchor)

{Only include this section if P1_CONTEXT is available.}

The following business outcomes were stated in the Phase 1 brief. Each is linked to the use
cases (and therefore test cases) that provide evidence it was achieved.

| Outcome | UC-IDs | Test Cases |
|---|---|---|
| {outcome from P1_CONTEXT} | UC-01, UC-03 | TC-001, TC-004 |
| ... | | |

---

## Scope Delta

### Features not traced to a use case
{List from SCOPE_DELTA.untraced_features, or "None identified" or "Codebase not scanned — provide PROJECT_ROOT to enable this check"}

### Use cases with no implementation found
{List from SCOPE_DELTA.unimplemented_uc_ids, or "None identified" or "Codebase not scanned"}

---

## Test Execution Tracker

| Total | Not Run | Pass | Fail | Blocked |
|---|---|---|---|---|
| {total} | {total} | — | — | — |

_Update this table as tests are executed._

---

## Test Cases

{For each UC-ID, one ### heading. All test cases for that UC appear under it.}

### {Feature Name} — {UC-ID}

**Requirement:** {req_ref} — {requirement description from REQ_INDEX}
**Actor:** {actor}

---

#### TC-001 · Happy path — {scenario title}

**Type:** Happy path

**Pre-conditions**
- {pre-condition 1}
- {pre-condition 2}

**Steps**

| # | Action | Expected Result |
|---|---|---|
| 1 | Navigate to {APP_URL} | Login page is displayed |
| 2 | Enter Username: `lead_analyst`, Password: `ChangeMe123!`, click **Log In** | Redirected to the Engagements list page |
| 3 | {action} | {expected observable result} |

**Execution Record**

| Actual Result | Status | Tester | Date | Notes |
|---|---|---|---|---|
| | | | | |

---

#### TC-002 · Negative — {scenario title}

{same structure}

---

{next UC-ID heading}
```

---

## Step 6 — Report

```
UAT Test Cases — {PHASE2_DIR basename}
────────────────────────────────────────
Output            : {OUTPUT_DIR}/uat_test_cases.md
Test cases        : {total}
UC-IDs covered    : {covered} / {total} ({pct}%)
Happy path        : {count}
Negative          : {count}
Untraced features : {count} (scope creep candidates)
Unimplemented UCs : {count}
```

Then say:

> "Open `uat_test_cases.md` and work through each test case in the application at {APP_URL}.
> For each test, fill in the **Actual Result**, **Status** (PASS / FAIL / BLOCKED), your
> initials in **Tester**, and today's date. Update the **Test Execution Tracker** table at the
> top as you go.
>
> When all tests are executed, run `/promote-environment 3` — the gate will read this file
> to compute the functionality score before deciding whether to allow PROD promotion."

---

## Rules

- **Never invent use cases.** Every test case maps to a UC-ID from the Phase 2 catalog.
  Features observed in the codebase that have no UC-ID go to SCOPE_DELTA, not to test cases.
- **Steps must be human-executable.** No Python, no database queries, no internal calls a UI
  tester cannot make. If the only path is via API, write a curl command.
- **Expected results must be observable.** What the tester sees, reads, or can copy. Not what
  the server does internally.
- **Cover every UC-ID.** A use case with no test case is a gap. If a UC cannot be tested
  because it has no UI and no documented API endpoint, note it as BLOCKED in SCOPE_DELTA.
- **One happy path per UC minimum.** Negative tests add depth; they do not substitute for the
  happy path.
- **Do not modify Phase 2 contracts.** Read only. The UAT document is derived from contracts,
  not a revision of them.
- **Write the complete document.** Do not produce a stub or a subset. Every UC-ID gets its
  test cases in the output file.
