---
name: council-codereview
description: Use for code review and quality feedback from both Codex and Gemini. Triggers on "council review code", "council code review", "have council review this", "get council feedback on code".
---

# Council Code Review Skill

Comprehensive code review with both Codex (GPT-5.2) and Gemini for quality, security, and best practices.

## When to Use

- Before committing or creating PRs
- Reviewing new code implementations
- Checking for security vulnerabilities
- Getting quality feedback
- When user asks for code review from the council

## Reasoning Level

**high** (default for code review)

## Execution

1. Identify the code to review:
   - Specific files mentioned by user
   - Staged git changes (`git diff --staged`)
   - Recent modifications

2. Gather the code content and context

3. Formulate a review prompt:
   ```
   Review this code for quality, security, and best practices:

   File: <filename>
   ```
   <code>
   ```

   Please analyze:
   1. Potential bugs or logic errors
   2. Security vulnerabilities
   3. Performance issues
   4. Code style and readability
   5. Suggestions for improvement
   ```

4. Run **BOTH** commands in parallel:

   **Codex:**
   ```bash
   codex exec --sandbox read-only -c model_reasoning_effort="high" "<prompt>"
   ```

   **Gemini:**
   ```bash
   gemini -s -y -o json "<prompt>"
   ```

5. Synthesize review findings

## Response Format

```markdown
## AI Council Code Review

### Codex (GPT-5.2) Review:
**Issues Found:**
- [Severity: High/Medium/Low] [Issue description]

**Security Concerns:**
- [Any security issues]

**Suggestions:**
- [Improvement suggestions]

---

### Gemini Review:
**Issues Found:**
- [Severity: High/Medium/Low] [Issue description]

**Security Concerns:**
- [Any security issues]

**Suggestions:**
- [Improvement suggestions]

---

### Council Synthesis:
**Critical Issues (Both Agree):**
- [Issues identified by both - highest priority]

**Additional Concerns:**
- [Issues only one model caught]

**Agreed Best Practices:**
- [Suggestions both models recommend]

**Final Verdict:** [LGTM / Needs Changes / Blocking Issues]

---
*Session IDs: Codex=[id], Gemini=[id]*
```
