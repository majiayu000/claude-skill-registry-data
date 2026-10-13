---
name: deep-review
description: Multi-pass code review with security, quality, structural analysis, and validation
---

<Purpose>
Deep Review structures code review as 4 specialized passes: Security (pass 1), Quality (pass 2), Structural (pass 3), and Validation (pass 4). Passes 1-3 run in parallel for independent analysis. Pass 4 validates findings from all prior passes, confirming real issues and dismissing false positives. The result is a consolidated, severity-rated review with validated findings.
</Purpose>

<Use_When>
- User wants thorough multi-perspective code review: `/deep-review`, `--deep`
- PR or changeset is large (10+ files) and benefits from specialized analysis
- Changes touch security-sensitive code (auth, payments, API endpoints)
- User wants false-positive filtering on review findings
</Use_When>

<Do_Not_Use_When>
- Quick review of a small change (1-3 files) — use code-reviewer agent directly
- User only wants security-specific review — use security-reviewer agent directly
- User wants a style-only review — use code-reviewer with model=haiku
</Do_Not_Use_When>

<Why_This_Exists>
Single-pass code reviews often miss issues or produce false positives because one reviewer tries to cover all concerns (security, quality, architecture) simultaneously. Deep Review separates concerns into specialized passes where each reviewer focuses on their domain, then adds a validation pass that filters false positives — producing higher-quality, actionable findings.
</Why_This_Exists>

<Execution_Policy>
- Passes 1-3 MUST run in parallel (independent concerns)
- Pass 4 runs sequentially after passes 1-3 complete (depends on their output)
- Each pass uses the appropriate specialist agent
- Findings include validationStatus after pass 4
- Output is a consolidated markdown report
</Execution_Policy>

<Steps>
1. **Identify the scope**: Determine what to review:
   - If a PR number or branch is specified, get the diff
   - If files are specified, review those files
   - If no scope specified, review recent uncommitted changes (`git diff`)

2. **Pass 1 - Security** (parallel): Spawn security-reviewer agent
   ```
   Task(subagent_type="oh-my-copilot:security-reviewer", model="sonnet", name="security-pass", prompt="
   SECURITY REVIEW PASS for deep-review.
   Review the following changes for security vulnerabilities:
   - OWASP Top 10 categories
   - Hardcoded secrets
   - Injection vulnerabilities (SQL, XSS, command injection)
   - Authentication/authorization issues
   - Input validation gaps

   Output each finding as:
   FINDING:
   - severity: CRITICAL|HIGH|MEDIUM|LOW
   - category: security
   - subcategory: [OWASP category]
   - file: [file:line]
   - title: [brief title]
   - description: [detailed description]
   - suggestedFix: [how to fix]
   END_FINDING

   Scope: [insert scope/diff here]
   ")
   ```

3. **Pass 2 - Quality** (parallel): Spawn code-reviewer agent
   ```
   Task(subagent_type="oh-my-copilot:code-reviewer", model="sonnet", name="quality-pass", prompt="
   QUALITY REVIEW PASS for deep-review.
   Review the following changes for code quality:
   - Logic defects (off-by-one, null handling, unreachable branches)
   - Error handling completeness
   - Performance issues (N+1 queries, O(n²) algorithms)
   - Anti-patterns and SOLID violations
   - Code duplication

   Output each finding as:
   FINDING:
   - severity: CRITICAL|HIGH|MEDIUM|LOW
   - category: quality
   - subcategory: [logic|error-handling|performance|anti-pattern|duplication]
   - file: [file:line]
   - title: [brief title]
   - description: [detailed description]
   - suggestedFix: [how to fix]
   END_FINDING

   Scope: [insert scope/diff here]
   ")
   ```

4. **Pass 3 - Structural** (parallel): Spawn architect agent
   ```
   Task(subagent_type="oh-my-copilot:architect", model="sonnet", name="structural-pass", prompt="
   STRUCTURAL REVIEW PASS for deep-review.
   Review the following changes for architectural concerns:
   - API contract changes (breaking changes, versioning)
   - Backward compatibility
   - Coupling and cohesion issues
   - Abstraction leaks
   - Module boundary violations
   - Dependency direction violations

   Output each finding as:
   FINDING:
   - severity: CRITICAL|HIGH|MEDIUM|LOW
   - category: structural
   - subcategory: [api-contract|compatibility|coupling|abstraction|boundary|dependency]
   - file: [file:line]
   - title: [brief title]
   - description: [detailed description]
   - suggestedFix: [how to fix]
   END_FINDING

   Scope: [insert scope/diff here]
   ")
   ```

5. **Consolidate findings**: Collect all findings from passes 1-3. Deduplicate by file:line + category (if two passes flag the same location for the same concern, merge them).

6. **Pass 4 - Validation**: Spawn code-reviewer agent (opus) with ALL findings
   ```
   Task(subagent_type="oh-my-copilot:code-reviewer", model="opus", name="validation-pass", prompt="
   VALIDATION PASS for deep-review.

   You are validating findings from 3 specialist review passes. For EACH finding below,
   read the actual code at the referenced file:line and determine:

   - confirmed_valid: The finding is a real issue that should be fixed
   - dismissed_false_positive: The finding is incorrect or not actually an issue (explain why)
   - needs_human_review: Cannot determine automatically, needs human judgment

   [Insert consolidated findings here]

   For each finding, output:
   VALIDATION:
   - findingId: [N]
   - validationStatus: confirmed_valid|dismissed_false_positive|needs_human_review
   - validationNote: [brief explanation of validation decision]
   END_VALIDATION
   ")
   ```

7. **Generate consolidated report**: Produce the final review report:
   - Group findings by severity (CRITICAL > HIGH > MEDIUM > LOW)
   - Include validationStatus for each finding
   - Mark dismissed findings clearly
   - Provide overall verdict: APPROVE (no confirmed CRITICAL/HIGH), REQUEST CHANGES (confirmed CRITICAL/HIGH exists), or COMMENT (only MEDIUM/LOW confirmed)
   - Save report if requested

</Steps>

<Tool_Usage>
- Use `Task(subagent_type="oh-my-copilot:security-reviewer", ...)` for Pass 1
- Use `Task(subagent_type="oh-my-copilot:code-reviewer", ...)` for Pass 2 and Pass 4
- Use `Task(subagent_type="oh-my-copilot:architect", ...)` for Pass 3
- Fire passes 1-3 simultaneously (independent concerns)
- Wait for all 3 to complete before starting Pass 4
</Tool_Usage>

<Examples>
<Good>
Three review passes fired simultaneously:
```
Task(subagent_type="oh-my-copilot:security-reviewer", model="sonnet", name="security-pass", prompt="...")
Task(subagent_type="oh-my-copilot:code-reviewer", model="sonnet", name="quality-pass", prompt="...")
Task(subagent_type="oh-my-copilot:architect", model="sonnet", name="structural-pass", prompt="...")
```
Then after all complete, validation pass:
```
Task(subagent_type="oh-my-copilot:code-reviewer", model="opus", name="validation-pass", prompt="[all findings]")
```
Why good: Parallel specialist passes, sequential validation, proper model routing.
</Good>

<Bad>
Running all 4 passes sequentially:
```
security = Task(security-reviewer, ...) # wait...
quality = Task(code-reviewer, ...) # wait...
structural = Task(architect, ...) # wait...
validation = Task(code-reviewer, ...) # wait...
```
Why bad: Passes 1-3 are independent and should run in parallel.
</Bad>
</Examples>

<Output_Format>
# Deep Review Report

**Scope:** [files/PR reviewed]
**Passes Completed:** 4/4
**Verdict:** APPROVE | REQUEST CHANGES | COMMENT

## Summary
- Confirmed Issues: X (Y critical, Z high)
- Dismissed False Positives: N
- Needs Human Review: M

## Confirmed Issues

### CRITICAL
[CRITICAL] [title] — [category]
File: [file:line]
Status: ✅ confirmed_valid
Description: [description]
Fix: [suggestedFix]
Validation: [validationNote]

### HIGH
...

### MEDIUM
...

### LOW
...

## Dismissed False Positives
[Finding] — dismissed because: [validationNote]

## Needs Human Review
[Finding] — reason: [validationNote]
</Output_Format>

<Final_Checklist>
- [ ] Passes 1-3 ran in parallel (3 simultaneous agent spawns)
- [ ] Pass 4 validated all findings from passes 1-3
- [ ] Each finding has a validationStatus
- [ ] Findings are deduplicated across passes
- [ ] Report grouped by severity
- [ ] Clear verdict issued (APPROVE/REQUEST CHANGES/COMMENT)
</Final_Checklist>
