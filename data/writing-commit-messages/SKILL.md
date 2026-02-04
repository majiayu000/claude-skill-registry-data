---
name: writing-commit-messages
description: Use when reviewing commit messages for compliance with the seven rules from cbea.ms/git-commit - checks subject line length, imperative mood, line wrapping, and that the message explains what and why
---

# Commit Message Review

## Overview

**Review commit messages for compliance with the seven rules from cbea.ms/git-commit.**

Commit messages document changes permanently. This skill guides systematic review of commit messages against established conventions: subject line ≤50 chars, imperative mood, body wrapped at 72 chars, explains WHAT and WHY.

**Core principle:** Commit messages are permanent documentation. They must follow conventions or they waste future developers' time.

## The Iron Law

```
AGENTS CANNOT SKIP OR MODIFY THE SEVEN RULES
```

Your job: Report compliance status of the commit message.
NOT your job: Decide if rules don't apply, make exceptions, or accept "close enough."

**Authority boundary:**
- You report: "Subject line is 63 chars, exceeds 50 char limit"
- Supervisor decides: Whether to rewrite message or accept violation
- You never decide: "63 is close enough to 50, I'll approve it"

## When to Use

**Use when:**
- Reviewing commit messages before committing
- Checking `jj describe` or `git commit` messages
- Validating automated commit message generation
- Code review process includes message quality checks
- After a commit is created, before pushing

**Don't use:**
- During active coding (wait until ready to commit)
- For in-progress/draft messages (review when finalized)
- When no message exists yet (this reviews existing messages)

## The Seven Rules

### Rule 1: Separate subject from body with a blank line

**Requirement:** If body exists, line 2 must be blank.

**Check:**
- [ ] Line 1 = subject
- [ ] Line 2 = blank (if line 3+ exist)
- [ ] Line 3+ = body

**Violations:**
- Subject runs directly into body (no blank line)
- Multiple blank lines between subject and body (should be exactly one)

### Rule 2: Limit the subject line to 50 characters

**Requirement:** Subject ≤50 chars ideal, ≤72 chars absolute maximum.

**Check:**
- [ ] Count characters in line 1
- [ ] 1-50 chars = COMPLIANT
- [ ] 51-72 chars = WARNING (exceeds ideal)
- [ ] 73+ chars = VIOLATION (exceeds hard limit)

**Violations:**
- Subject >50 chars (warning level)
- Subject >72 chars (blocking violation)

### Rule 3: Capitalize the subject line

**Requirement:** First word of subject must be capitalized.

**Check:**
- [ ] First character is uppercase letter

**Violations:**
- Subject starts with lowercase letter
- Subject starts with special character (rare, but wrong)

### Rule 4: Do not end the subject line with a period

**Requirement:** Subject line must not end with `.`

**Check:**
- [ ] Last character of line 1 is not `.`

**Violations:**
- Subject ends with period
- Subject ends with other punctuation (`.`, `!`, `?`) - also wrong

### Rule 5: Use the imperative mood in the subject line

**Requirement:** Subject uses imperative mood ("Add feature" not "Added feature").

**Test:** "If applied, this commit will [subject line]" should read correctly.

**Check:**
- [ ] Starts with imperative verb (Add, Fix, Update, Remove, Refactor, etc.)
- [ ] Does NOT use past tense (Added, Fixed, Updated)
- [ ] Does NOT use present continuous (Adding, Fixing, Updating)
- [ ] Does NOT use descriptive form (Addition of, Fixing of)

**Common violations:**
- Past tense: "Added feature", "Fixed bug", "Updated config"
- Present continuous: "Adding feature", "Fixing bug"
- Noun form: "Addition of feature", "Bug fix for X"
- Descriptive: "This commit adds feature"

### Rule 6: Wrap the body at 72 characters

**Requirement:** Every line in body (line 3+) must be ≤72 chars.

**Check:**
- [ ] Line 3 ≤72 chars
- [ ] Line 4 ≤72 chars
- [ ] ...continue for all body lines

**Exceptions:**
- URLs can exceed 72 chars (can't wrap them)
- Code snippets might exceed (use judgment)
- Everything else must wrap

**Violations:**
- Any body line >72 chars (except URLs/code)
- Body written as one long paragraph (should hard wrap)

### Rule 7: Use the body to explain what and why vs. how

**Requirement:** Body explains WHAT changed and WHY, not HOW.

**Check:**
- [ ] Body describes what changed
- [ ] Body explains why the change was needed
- [ ] Body does NOT describe implementation details (how)
- [ ] Body is present for non-trivial changes

**What = GOOD:**
- "Adds user authentication to API endpoints"
- "Fixes memory leak in worker pool"
- "Updates dependencies to latest stable versions"

**Why = GOOD:**
- "to prevent unauthorized access to user data"
- "to prevent crashes after processing 1000+ jobs"
- "to address security vulnerabilities in crypto library"

**How = BAD:**
- "using bcrypt for password hashing and JWT for tokens"
- "by adding cleanup call to worker.close() method"
- "bumps openssl from 1.1.1 to 3.0.2"

**Violations:**
- Body explains implementation details instead of motivation
- Body missing for non-trivial change
- Body describes how code works instead of what/why changed

## The Review Process

### Step 1: Read the Commit Message

Get the full commit message:
```bash
jj log -r @ -T description
# or
git log -1 --format=%B
```

### Step 2: Check Formatting Rules (1-6)

These are mechanical checks:
1. Blank line after subject? ✓/✗
2. Subject length? (count chars)
3. Subject capitalized? ✓/✗
4. Subject ends with period? ✓/✗
5. Subject uses imperative mood? ✓/✗
6. Body lines ≤72 chars? (check each line)

Report each violation with line numbers.

### Step 3: Check Content (Rule 7)

Read the changes/diff:
```bash
jj show
# or
git show
```

Ask:
- Does the subject accurately describe the primary change?
- Does the body explain WHAT changed?
- Does the body explain WHY it changed?
- Is the body focused on what/why or how?
- Is the change non-trivial? Does it need a body?

### Step 4: Report Findings

**Format:**

```markdown
## Commit Message Review

**Overall Status:** COMPLIANT / PARTIAL / VIOLATION

### Subject Line

**Text:** "[the actual subject line]"
**Length:** X characters

**Rule Compliance:**
- Rule 2 (Length): ✓ COMPLIANT / ⚠️ WARNING (51-72 chars) / ❌ VIOLATION (73+ chars)
- Rule 3 (Capitalized): ✓ COMPLIANT / ❌ VIOLATION
- Rule 4 (No period): ✓ COMPLIANT / ❌ VIOLATION
- Rule 5 (Imperative mood): ✓ COMPLIANT / ❌ VIOLATION

**Violations:**
- ❌ [Specific issue with fix]

### Body

**Rule Compliance:**
- Rule 1 (Blank line): ✓ COMPLIANT / ❌ VIOLATION
- Rule 6 (72 char wrap): ✓ COMPLIANT / ❌ VIOLATION
- Rule 7 (What/Why): ✓ COMPLIANT / ⚠️ NEEDS IMPROVEMENT / ❌ VIOLATION

**Violations:**
- ❌ Line X: [Specific issue]
  - Current: [problematic text]
  - Fix: [corrected text]

### Content Assessment

**Does subject describe the change?** ✓ YES / ⚠️ PARTIAL / ❌ NO
- [Explanation]

**Does body explain WHAT?** ✓ YES / ⚠️ PARTIAL / ❌ NO / N/A (no body)
- [What's explained or missing]

**Does body explain WHY?** ✓ YES / ⚠️ PARTIAL / ❌ NO / N/A (no body)
- [Why's explained or missing]

**Is body required?** YES / NO
- [Justification based on change complexity]

### Suggested Revision

[If violations exist, provide corrected message]
```

## Violation Severity

**BLOCKING:** Cannot commit until fixed
- Subject >72 chars (hard limit)
- Missing blank line between subject and body
- Subject not capitalized
- Subject ends with period
- Subject uses past tense or wrong mood
- Body line >72 chars (except URLs/code)
- No body for non-trivial change
- Body doesn't describe what changed
- Subject doesn't describe the change

**WARNING:** Should fix, but not blocking
- Subject 51-72 chars (exceeds ideal, within limit)
- Body explains "how" instead of "what/why" (minor)
- Body could be clearer about motivation

**NOTE:** Consider for future
- Body could mention additional context
- Alternative wording suggestion

**Never:**
- Downgrade blocking to warning because "it's close"
- Skip violations because "message is good enough"
- Accept past tense because "sounds natural"

## Common Rationalizations (All Wrong)

| Excuse | Reality |
|--------|---------|
| "63 chars is close to 50, good enough" | No. >50 is WARNING. >72 is VIOLATION. Report it. |
| "Past tense is clearer than imperative" | No. Convention is imperative. Report violation. |
| "Body explains how, but it's useful info" | No. Move to code comments. Body is what/why. |
| "Change is obvious, doesn't need body" | Check the rule. Non-trivial changes need body. |
| "Subject describes it well enough" | Subject is summary. Body provides context. Check both. |
| "This is just their style" | Style must follow conventions. Report violation. |
| "No one cares about commit messages" | History is permanent. Future you will care. Report it. |
| "The message communicates the intent" | Intent isn't enough. Must follow format rules too. |

**Seeing yourself in this table? STOP. Report the violation without deciding it's acceptable.**

## Example Review

### Example 1: Multiple Violations

**Message:**
```
I'll create a git commit message following the specified rules for these changes.

Looking at the diff, I can see:
1. Configuration changes
2. Dependency updates
```

**Review:**

```markdown
## Commit Message Review

**Overall Status:** ❌ VIOLATION (Multiple critical issues)

### Subject Line

**Text:** "I'll create a git commit message following the specified rules for these changes."
**Length:** 86 characters

**Rule Compliance:**
- Rule 2 (Length): ❌ VIOLATION (86 chars, exceeds 72 char hard limit)
- Rule 3 (Capitalized): ✓ COMPLIANT (starts with "I")
- Rule 4 (No period): ❌ VIOLATION (ends with period)
- Rule 5 (Imperative mood): ❌ VIOLATION (not imperative, describes intent to create message)

**CRITICAL:** Subject is meta-commentary about creating a message, not describing the actual changes.

### Body

**Rule Compliance:**
- Rule 1 (Blank line): ✓ COMPLIANT
- Rule 6 (72 char wrap): ✓ COMPLIANT
- Rule 7 (What/Why): ❌ VIOLATION (describes message creation process, not code changes)

### Content Assessment

**Does subject describe the change?** ❌ NO
- Subject describes the intent to write a commit message
- Should describe what changed in the code

**Does body explain WHAT?** ❌ NO
- Body lists observations about the diff
- Should explain what actually changed

**Does body explain WHY?** ❌ NO
- No explanation of motivation

**Is body required?** YES (config and dependency changes are non-trivial)

### Suggested Revision

Based on the mentioned changes, the message should be:

```
Update configs and dependencies

Updates configuration files to standardize formatting and
adds new environment variables needed for feature X.

Updates dependency versions to latest stable releases,
bringing in security patches for CVE-2024-XXXXX and
compatibility fixes for Node 20.
```

**Critical:** The current message is the agent's internal thoughts about writing a message, not an actual commit message.
```

### Example 2: Compliant Message

**Message:**
```
Add user authentication to API endpoints

Adds JWT-based authentication to all API endpoints to
prevent unauthorized access to user data. Unauthenticated
requests now receive 401 status codes.

This addresses the security audit findings from Q4 2024
where sensitive endpoints were accessible without auth.
```

**Review:**

```markdown
## Commit Message Review

**Overall Status:** ✓ COMPLIANT

### Subject Line

**Text:** "Add user authentication to API endpoints"
**Length:** 44 characters

**Rule Compliance:**
- Rule 2 (Length): ✓ COMPLIANT (44 chars, under 50)
- Rule 3 (Capitalized): ✓ COMPLIANT
- Rule 4 (No period): ✓ COMPLIANT
- Rule 5 (Imperative mood): ✓ COMPLIANT ("Add")

### Body

**Rule Compliance:**
- Rule 1 (Blank line): ✓ COMPLIANT
- Rule 6 (72 char wrap): ✓ COMPLIANT (longest line: 61 chars)
- Rule 7 (What/Why): ✓ COMPLIANT

### Content Assessment

**Does subject describe the change?** ✓ YES
- Clearly states authentication was added to API

**Does body explain WHAT?** ✓ YES
- JWT authentication added
- Unauthenticated requests get 401

**Does body explain WHY?** ✓ YES
- Prevent unauthorized access
- Address security audit findings

**Is body required?** YES
- Body present and appropriate for this change

**No violations found.** Message follows all seven rules correctly.
```

## Red Flags - You're Rationalizing

**STOP if you catch yourself thinking:**
- "Close enough to 50 characters"
- "Past tense sounds fine"
- "Everyone will understand what it means"
- "The diff shows how, so message doesn't need why"
- "Too minor to need a body"
- "Subject is descriptive enough"
- "No one reads commit messages anyway"
- "This is the developer's style"

**All of these mean:** You're making exceptions to the rules. Stop. Report the violation and let supervisor decide.

## When Message Seems Adequate But Violates Rules

**If message communicates well but violates format:**

```markdown
**Note for supervisor:**

Message effectively communicates the change, but violates Rule X.

Current: [current text]
Required: [what rule requires]

Recommend fixing to comply with conventions even though message is clear.

**For now: Flagging as VIOLATION** until supervisor decides whether to fix or accept.
```

**Critical:** You still flag it as violation. Good communication doesn't override format rules.

## The Bottom Line

**Your job: Report compliance with the seven rules.**

Not your job:
- Decide if rules are too strict
- Determine if violation is "close enough"
- Accept "good communication" over format compliance
- Make exceptions for "good enough" messages

**When in doubt: Flag it and ask supervisor.**

Better to over-report than to approve violations.

The seven rules are conventions. Following them is not optional. You enforce, you don't decide.

## Source

Based on: https://cbea.ms/git-commit/
