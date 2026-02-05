---
name: validation-phase
description: Quality validation after execution. Runs confidence-check skill (if complexity ≥15), spawns code-quality-validator for build verification, and reviewer agent for quality assessment. Scales checks based on change size.
---

# Validation Phase Skill

> **ROOT AGENT ONLY** - Spawns agents, runs only from root Claude Code agent.

**Purpose:** Validate implementation quality before reporting
**Trigger:** After execution-phase completes
**Input:** `workerResults`, `complexity` (int), `prdPath`, `scope`
**Output:** `{status, confidenceScore?, buildChecks, reviewFindings}`

---

## Workflow

**1. Run confidence-check (if complexity ≥15)**

- 5-point weighted assessment: duplicates, patterns, architecture, examples, requirements
- Score ≥90% → Proceed
- Score 70-89% → Flag concerns
- Score <70% → Escalate

**2. Verify Acceptance Criteria (AC) completion**

- Scan story files in PRD for AC checkbox format: `- [x]` (completed) or `- [ ]` (incomplete)
- If any AC marked incomplete (`- [ ]`):
  - Report list of stories with incomplete AC
  - CRITICAL block - must complete AC before proceeding
- If all AC checked (`- [x]`):
  - Continue to quality checks

**3. Run code-quality-validator agent**

- Scales checks by change size (Small/Medium/Large)
- Small (1-3 files): `pnpm build`
- Medium (4-10 files): `pnpm build && lint && prettier`
- Large (11+ files): `pnpm build && lint && prettier && test`

**4. Run reviewer agent**

- Code patterns, SOLID principles, security
- Error handling, naming consistency, PRD compliance
- Return quality assessment + recommendations

---

## Validation Strategy

| Change Size | Files | Checks Run                      |
| ----------- | ----- | ------------------------------- |
| Small       | 1-3   | Build only                      |
| Medium      | 4-10  | Build + Lint + Prettier         |
| Large       | 11+   | Build + Lint + Prettier + Tests |

---

## Failure Handling

| Failure Type           | Action                                         |
| ---------------------- | ---------------------------------------------- |
| Incomplete AC          | CRITICAL - must complete before proceeding     |
| Build failure          | CRITICAL - must fix before proceeding          |
| Lint/Prettier warnings | Non-blocking, provide recommendations          |
| Test failures          | Ask user: fix, continue with warnings, or skip |

---

## Output Example

```json
{
  "status": "pass",
  "confidenceScore": 92,
  "acVerification": {
    "status": "pass",
    "checked": 8,
    "incompleteStories": []
  },
  "buildChecks": {
    "build": { "status": "pass" },
    "lint": { "status": "pass" },
    "prettier": { "status": "pass" },
    "tests": { "status": "pass" }
  },
  "reviewFindings": [
    {
      "severity": "info",
      "file": "src/auth.service.ts",
      "message": "Add JSDoc comments"
    }
  ],
  "recommendations": ["Add integration tests for edge cases"]
}
```

**AC Failure Example:**

```json
{
  "status": "blocked",
  "acVerification": {
    "status": "incomplete",
    "checked": 8,
    "incompleteStories": [
      "prj-epc-002: User login - AC 2, 4 incomplete",
      "prj-epc-005: Password reset - AC 1 incomplete"
    ]
  },
  "message": "Cannot proceed: 2 stories have incomplete acceptance criteria"
}
```

---

## Integration

**Called by:**

- `/audit` command (after execution-phase)
- `/build` command (after execution-phase)
- `/ms` command (for complexity ≥15)

**Calls:**

- `confidence-check` skill (if complexity ≥15)
- `code-quality-validator` agent
- `reviewer` agent
- `AskUserQuestion` tool (on test failures)

**Next step:** report-phase (final report + sign-off)
