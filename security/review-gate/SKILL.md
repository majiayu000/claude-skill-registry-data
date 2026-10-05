---
description: "Gate skill for managing the PR review → Fix → re-review cycle. Run Code Review + Security Review in parallel, and auto-fix if issues are found"
user-invokable: true
---

# /review-gate

A gate skill that runs code review and security review in parallel for a PR,
and if issues are found, executes an auto-fix → re-review cycle for up to 2 rounds.

## Argument Patterns

- `/review-gate <PR number>` — Run full review cycle on the specified PR
- `/review-gate <PR number> --issue <ISSUE_ID>` — Explicitly specify Issue ID
- `/review-gate` — Run full review cycle on the PR associated with the current branch

---

## Steps

### Phase 1: Collect PR Information

#### 1-1. Identify the PR

If an argument is provided:
- Use `<PR number>`

If no argument is provided:
- Get the PR number for the current branch with `gh pr view --json number -q .number`

#### 1-2. Fetch PR Information

Fetch the following **in parallel**:

```bash
gh pr view <PR number> --json title,body,headRefName,baseRefName,number,url
gh pr diff <PR number> --name-only
```

#### 1-3. Fetch Issue Information

If `--issue` is specified, use that.
Otherwise, extract the Issue ID in `USK-XX` format from the PR body,
and fetch details with `mcp__linear-server__get_issue`.

#### 1-4. Build Context

> **Single source of truth.** Other skills (`/orchestrate`, `/implement`, `/code-review`, `/security-review`) **must** read these blocks from this section instead of redefining their own. Updating the architecture description in this one place propagates everywhere.

**Product context:**
```
yorishiro-proxy is a network proxy (MCP server) for AI agents.
Provides traffic interception, recording, and replay capabilities for vulnerability assessment.
Architecture: TCP Listener → Protocol Detection → Layer Stack (TCP→TLS→HTTP/1|HTTP/2→WS|gRPC|gRPC-Web|SSE|Raw)
              → Pipeline Steps (HostScope→HTTPScope→Safety→PluginPre→Intercept→Transform→PluginPost→Record [→ UpgradeStep])
              → Flow Recording (L7 Message + L4 Envelope.Raw) → MCP Tool

Data path packages (MITM triage targets):
  internal/envelope/, internal/layer/, internal/connector/, internal/pipeline/,
  internal/pluginv2/, internal/proxybuild/, internal/rules/, internal/safety/,
  internal/flow/, internal/session/

Control plane (net/http allowed): internal/mcp/, cmd/, internal/selfupdate/
```

**Security context:**
```
yorishiro-proxy operates as a MITM proxy, therefore:
- It directly processes attacker-controlled traffic
- It holds the CA private key and dynamically issues certificates
- Session recordings may contain credentials (auth tokens, passwords)
- AI agents execute commands via MCP

Threat model:
- Anomalous wire input (malformed headers, smuggling attempts, oversized frames) is in-scope
  by design — the parser must surface anomalies via typed Anomaly fields, not panic
- Plugin Starlark code is sandboxed but plugins are partially trusted (loaded from disk)
- Wire fidelity is a security property: header dedup / Host=URL enforcement / case
  normalization in data path code blocks pentest scenarios — see Phase 3-3 MITM
  Compatibility Triage below
```

---

### Phase 2: Run Reviews in Parallel

#### 2-1. Load Agent Templates

Read `.claude/agents/code-reviewer.md` and `.claude/agents/security-reviewer.md` with the Read tool,
and extract the code block inside each template's `## Prompt Body` section.

#### 2-2. Replace Placeholders

**Code Review Agent:**
- `{{PR_NUMBER}}` → PR number
- `{{PR_TITLE}}` → PR title
- `{{ISSUE_ID}}` → Issue ID
- `{{ISSUE_DESCRIPTION}}` → Issue description
- `{{PRODUCT_CONTEXT}}` → Product context
- `{{CHANGED_FILES}}` → List of changed files

**Security Review Agent:**
- `{{PR_NUMBER}}` → PR number
- `{{PR_TITLE}}` → PR title
- `{{ISSUE_ID}}` → Issue ID
- `{{PRODUCT_CONTEXT}}` → Product context
- `{{SECURITY_CONTEXT}}` → Security context

#### 2-3. Parallel Launch

Launch 2 Task tools **in the same message** in parallel:

```
Task(description="Code review PR #<N>", subagent_type="general-purpose", isolation="worktree", prompt=<Code Review prompt>)
Task(description="Security review PR #<N>", subagent_type="general-purpose", isolation="worktree", prompt=<Security Review prompt>)
```

**Note**: Reviews are read-only, but `isolation: "worktree"` is used because checking out the target branch during parallel execution conflicts with the main worktree state.

---

### Phase 3: Aggregate Verdict

#### 3-1. Parse Results

Extract `VERDICT:` lines from each agent's output and record the verdict.

```
code_review_verdict = APPROVED | CHANGES_REQUESTED
security_review_verdict = APPROVED | CHANGES_REQUESTED
```

#### 3-2. Check for Findings

Parse the `FINDINGS:` section from each Claude agent's output and record whether LOW or higher findings exist.
`FINDINGS: None` means no findings.

```
code_review_has_findings = true | false
security_review_has_findings = true | false
has_any_findings = code_review_has_findings or security_review_has_findings
```

#### 3-3. MITM Compatibility Triage

**Before passing findings to the Fixer**, evaluate every finding against the MITM Implementation Principles in `CLAUDE.md`.

yorishiro-proxy is a pentesting MITM proxy. Users intentionally craft anomalous requests
(duplicate headers, Host ≠ URL, mixed-case header names, etc.) for security testing.

**Reject a finding (`REJECTED_MITM`) if it suggests any of the following in data path code**
(see Product context above for the canonical list — `internal/envelope/`, `internal/layer/`,
`internal/connector/`, `internal/pipeline/`, `internal/pluginv2/`, `internal/proxybuild/`,
`internal/rules/`, `internal/safety/`, `internal/flow/`, `internal/session/`):

| Pattern | Example suggestion | Why reject |
|---------|-------------------|------------|
| Deduplicate headers | "Del before Set to ensure single header" | Users intentionally inject duplicate headers (Host header injection, request smuggling) |
| Enforce Host = URL | "Re-derive Host from URL to prevent mismatch" | Host ≠ URL mismatch is a valid pentesting technique |
| Canonicalize header names | "Use CanonicalHeaderKey" or "Lowercase header names" | Wire casing must be preserved (HTTP/1.x is case-insensitive but MITM must not normalize) |
| Reorder headers | "Sort headers alphabetically" | Header order must match wire observation |
| Normalize whitespace | "Trim header value whitespace" | Whitespace in headers may be intentional for testing |
| Use `net/http` types in data path | "Use http.Header instead of RawHeaders" | `net/http` types canonicalize and lose wire fidelity |

**Accept a finding even if it touches data path code when it addresses**:
- Security of the proxy itself (CRLF injection in proxy internals, SSRF scheme validation)
- Code correctness unrelated to wire data (nil checks, resource leaks, race conditions)
- Validation-before-mutation ordering

**Triage output format:**

For each rejected finding, record:
```
REJECTED_MITM:
  - ID: F-2, Source: Code Review, Reason: "Suggests Host=URL enforcement — blocks Host header injection testing"
```

Remove `REJECTED_MITM` findings from the lists passed to the Fixer.
Include the `REJECTED_MITM` list in the Phase 5 report for visibility.

#### 3-4. Aggregate Verdict

| Code Review | Security Review | Aggregate Verdict | Next Action |
|-------------|----------------|-------------------|-------------|
| APPROVED (no findings) | APPROVED (no findings) | **APPROVED** | Phase 5 (Report) |
| APPROVED (with findings) | APPROVED (no/with findings) | **APPROVED_WITH_FINDINGS** | Phase 4 (Fix only, no re-review) |
| Any CHANGES_REQUESTED | Any | **CHANGES_REQUESTED** | Phase 4 (Fix + re-review) |

---

### Phase 4: Fix Cycle (Max 2 Rounds)

> **Note**: For `APPROVED_WITH_FINDINGS`, run Fixer once only and skip re-review.
> The re-review cycle (max 2 rounds) applies only for `CHANGES_REQUESTED`.

#### 4-1. Launch Fixer Agent

Read `.claude/agents/fixer.md` with the Read tool and replace placeholders:

- `{{PR_NUMBER}}` → PR number
- `{{BRANCH_NAME}}` → PR head branch name
- `{{CODE_REVIEW_FINDINGS}}` → Code Review findings (pass all findings if present; "None — Code review passed." if none)
- `{{SECURITY_REVIEW_FINDINGS}}` → Security Review findings (pass all findings if present; "None — Security review passed." if none)
- `{{ORIGINAL_ISSUE_ID}}` → Issue ID
- `{{PRODUCT_CONTEXT}}` → Product context

Launch with Task tool:
- `subagent_type`: `"general-purpose"`
- `isolation`: `"worktree"`
- `description`: `"Fix review findings PR #<N> round <R>"`
- `prompt`: Replaced prompt

#### 4-2. Check Fix Results

Extract the status of each finding from the Fixer Agent output:
- `FIXED`: Fix complete
- `PARTIALLY_FIXED`: Partially fixed
- `UNRESOLVED`: Not resolved

#### 4-3. Re-review

Re-run **only the reviews that were `CHANGES_REQUESTED`**:

- Only Code Review was `CHANGES_REQUESTED` → Re-launch Code Review Agent only
- Only Security Review was `CHANGES_REQUESTED` → Re-launch Security Review Agent only
- Both were `CHANGES_REQUESTED` → Re-launch both in parallel

#### 4-4. Round Management

```
# For APPROVED_WITH_FINDINGS: Fix only, no re-review
if aggregate_verdict == APPROVED_WITH_FINDINGS:
    Launch Fixer Agent (pass all findings including LOW)
    → Phase 5

# For CHANGES_REQUESTED: Fix + re-review cycle (max 2 rounds)
current_round = 1

while current_round <= 2:
    if aggregate_verdict == APPROVED or aggregate_verdict == APPROVED_WITH_FINDINGS:
        break  → Phase 5

    Launch Fixer Agent (pass all findings including LOW)
    Run re-review (only the side that was CHANGES_REQUESTED)
    Aggregate verdict

    current_round += 1

if current_round > 2 and aggregate_verdict == CHANGES_REQUESTED:
    → ESCALATE
```

---

### Phase 5: Report Results

#### 5-1. Final Status

| Result | Meaning |
|--------|---------|
| **APPROVED** | Both reviews passed (initial or after Fix) |
| **ESCALATED** | Review not passed after 2 rounds of fixes. Manual intervention required |

#### 5-2. Report to User

```markdown
## Review Gate Results: PR #<N>

**Final Verdict**: APPROVED / ESCALATED
**PR**: <PR URL>
**Fix Rounds**: 0 / 1 / 2

### Review Results

| Review | Initial | Round 1 | Round 2 | Final |
|--------|---------|---------|---------|-------|
| Code Review | APPROVED/CHANGES_REQUESTED | — | — | APPROVED |
| Security Review | CHANGES_REQUESTED | APPROVED | — | APPROVED |

### Findings Summary

| ID | Severity | Category | Status |
|----|----------|----------|--------|
| F-1 | HIGH | Correctness | FIXED (Round 1) |
| S-1 | MEDIUM | InputValidation | FIXED (Round 1) |

### MITM-Rejected Findings (if any)

The following findings were rejected because they conflict with MITM proxy design principles:

| ID | Source | Reason |
|----|--------|--------|
| F-2 | Code Review | Suggests Host=URL enforcement — blocks Host header injection testing |

### Escalation (ESCALATED only)

The following findings could not be resolved in 2 rounds of fixes. Manual intervention requested:

| ID | Severity | File | Description |
|----|----------|------|-------------|
| ... | ... | ... | ... |
```

#### 5-3. Update Linear Status (if Issue ID exists)

| Event | Linear Comment |
|-------|---------------|
| Review passed | "PR #N: Code Review APPROVED, Security Review APPROVED" |
| Fix cycle starts | "PR #N: Review found issues. Fix round 1 starting." |
| Passes after Fix | "PR #N: All findings resolved after N fix round(s)." |
| Escalation | "PR #N: ESCALATION - N unresolved findings after 2 fix rounds. Manual intervention needed." |

Post comments to Issues using `mcp__linear-server__create_comment`.

### Phase 6: Worktree Cleanup

After the review cycle completes, delete **only the worktrees of sub-agents you launched**.

**Important**: To prevent accidentally destroying worktrees actively in use by other sessions,
do not bulk-delete.

**Steps:**

1. Record agent IDs from each Task call in Phases 2 through 4
2. Run the following for each recorded agent ID:

Write those IDs one per line to a file and run the canonical cleanup snippet against it.

> Use the canonical cleanup snippet in `CLAUDE.md` → **Agent Isolation Strategy → Worktree
> Cleanup**. Do not construct `.claude/worktrees/agent-<id>` from an ID (a nested sub-agent's
> worktree lives inside its parent's, so the path does not exist and the remove silently
> no-ops), use `--force --force` (a single `--force` fails on a locked worktree), and never
> select paths with `grep -F -f` (this machine's `grep` is ugrep: an empty pattern file matches
> every line).

3. When this skill runs as a **delegated agent** (from `/orchestrate` 2.5 or `/autopilot` Phase 5),
   clean up your own reviewers and fixers here, before returning, and still report every ID in
   `agent_ids`. The caller treats that list as a fallback, not as your cleanup.

Note: When called from `/orchestrate`, bulk deletion happens in Phase 3-3, so there may be duplication,
but it is idempotent so no problem. This effectively functions only when `/review-gate` is run standalone.

---

## Concurrency Strategy

| Scenario | Strategy | Concurrent Agents |
|----------|----------|------------------|
| Initial review | Code + Security in parallel | 2 |
| Re-review (one side only) | Single execution | 1 |
| Re-review (both sides) | Code + Security in parallel | 2 |
| Fix | Fixer 1 agent only | 1 |

## Maximum Agent Calls Per PR (Worst Case)

Initial review 2 + Fix 1 + Re-review 2 + Fix 1 + Re-review 2 = **8 calls**
For APPROVED_WITH_FINDINGS: Initial review 2 + Fix 1 = **3 calls**

---

## Notes

- Review agents are **read-only** — they make no code changes whatsoever
- Fixer Agent operates in a **worktree** — directly modifies the PR branch
- **LOW and above** findings are all fix targets (NIT only is excluded)
- Even if APPROVED, launch Fixer if LOW findings exist (no re-review needed)
- On escalation, do not attempt fixes; defer to the user's judgment
