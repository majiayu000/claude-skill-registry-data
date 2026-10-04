---
name: critical-review
description: Use when you want structured feedback on a plan or document before implementation.
risk: safe
risk-note: "writes to ~/.claude/plans/ only, with user consent"
argument-hint: "[plan-file]"
---

# Critical Review

This skill must only be invoked from the main session, never from a subagent.

1. **Identify the target document:**
   a. If the user specified a file path or plan name, use that.
   b. Else determine the project name: check `origin` git remote (parse last path component, strip `.git`) → git root basename → working directory basename. If ambiguous, ask the user.
   c. List files in `~/.claude/plans/<project-name>/`, sorted by modification time (most recent first). If the directory does not exist or contains no `.md` files, tell the user: "No plan files found in `~/.claude/plans/<project-name>/`. Please specify a file path to review." and stop.
   d. Confirm with the user: "I'll review `<filename>`. Correct?"

2. **Round 1 — Spawn 4 parallel subagents** (all four on the **latest, most capable model** — omit the `model` override so each inherits the session model rather than pinning a version-specific name; plan adjudication is precision work where a weaker model's false positives cost more verification time than the savings, so don't downgrade to a cheaper tier; `CLAUDE_CODE_SUBAGENT_MODEL` overrides if set):
   - **Agent 1 — Correctness & Logic**: Logic errors, wrong assumptions, API misuse, spec violations, contradictions within the plan.
   - **Agent 2 — Edge Cases & Robustness**: Boundary conditions, empty/malformed inputs, error handling gaps, crash scenarios, encoding/Unicode issues.
   - **Agent 3 — Feasibility & Performance**: Over-engineering, unrealistic scope, dependency risks, library limitations, performance concerns, scaling issues.
   - **Agent 4 — Testing & Completeness**: Coverage gaps, untested paths, missing integration tests, weak assertions, unaddressed requirements.

   **Each subagent's prompt MUST include these instructions verbatim:**
   > Read the target plan document. Read at most 5 source files directly relevant to your review — prefer files explicitly named in the plan. Do NOT read the entire codebase.
   >
   > Return findings as a numbered list, max 10 items, highest severity first. Each item must have exactly these fields:
   > - **Severity**: critical | major | minor
   > - **Location**: file path and section/function name
   > - **Issue**: one-sentence description
   > - **Fix**: one-sentence suggested fix
   >
   > Return NO other text, except: if you encounter tool errors or cannot read required files, report that as your first finding with severity "critical" and location "tooling".

3. After all subagents complete, **synthesize** in the main session:
   - Deduplicate overlapping findings
   - Prioritize by severity
   - If a subagent returned zero findings, note that to the user
   - Present a consolidated list to the user

4. If the user approves incorporating feedback: **the main session** (not a subagent) updates the plan document with a new revision and notes what changed.

5. **Decision logging** (runs after every user response — approval, rejection, or deferral):
   Append each decision to `~/.claude/plans/<project-name>/decision-log.md`. Create the file if it doesn't exist. Append-only — never overwrite existing entries. Format per entry:
   ```
   ## YYYY-MM-DD — [Plan filename]
   - **Finding:** [1-sentence summary]
   - **Decision:** accepted / rejected / deferred
   - **Rationale:** [why — from the user's response or the discussion]
   - **Alternatives considered:** [if any were discussed]
   ```

6. **Iterate until clean.** After applying fixes, automatically start the next round:
   - Spawn **2 parallel subagents** that review ONLY the sections changed in the latest revision, **both on the latest, most capable model** (omit the `model` override so they inherit the session model; fix verification is high-stakes — don't downgrade to a cheaper tier; `CLAUDE_CODE_SUBAGENT_MODEL` overrides if set):
     - **Agent A — Correctness, Logic & Edge Cases**
     - **Agent B — Feasibility, Testing & Completeness**
   - Each subagent's prompt MUST include the same verbatim format template from step 2, modified to say: "Review ONLY the following changed sections: [list sections]. Read at most 3 source files relevant to the changes. Max 5 items."
   - Synthesize, present to user, apply approved fixes, increment revision.
   - **Stop condition**: a round produces **0 critical and 0 major** findings. Minor-only findings do not block — note them and declare the plan ready.
   - **Safety valve**: max 7 total rounds (1 initial + 6 follow-ups). If critical/major issues persist after 7 rounds, STOP — report what keeps recurring and flag to the user that the plan may need structural rework rather than incremental fixes.

7. When the stop condition is met, inform the user the review is complete and the plan is ready for implementation. Do not begin implementation unless the user explicitly requests it.

8. If the user does not approve changes at any point, present the findings as a reference, log the rejections (step 5), and end. Do not modify any files.

## Output Contract

The final synthesized report MUST include all of the following:

- **Document reviewed**: path to the plan or document
- **Findings table**: each finding with severity, location, issue, and fix
- **Aggregate counts**: total findings broken down by severity (critical/major/minor)
- **Verdict**: one of `clean` (0 critical, 0 major) or `needs-revision` (1+ critical or major)
- **Change summary** *(conditional)*: include only when revisions were applied; omit when user declines changes
