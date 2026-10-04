---
name: pr-split
description: Check if a pull request is too large and guide splitting it into focused PRs.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: all
  audience: developers
  workflow: analysis
  since: "2026-02-24"
---

## What I do

I help you assess whether a PR is too large and guide you through splitting it if needed:

1. **Size Assessment** — Evaluate the PR by lines changed and number of distinct logical concerns
2. **Threshold Check** — Evaluate size and cohesion together: >1 concern is always too large; >400 lines is a review-risk signal that requires an atomicity check
3. **If OK**: Confirm the PR is appropriately sized
4. **If Too Large**: Identify distinct concerns, propose a logical split, and guide branch strategy
5. **If Unsplittable**: Help you document and annotate the PR for easier review despite size

Oversized PRs slow review, increase risk of missed issues, and frustrate reviewers. This skill prevents that.

## When to use me

Use when you want to:
- Check if your PR exceeds recommended size limits
- Get guidance on splitting an oversized PR
- Identify logical groupings for a large changeset
- Document why a large PR cannot be split
- Plan a sequence of dependent PRs

## PR lifecycle focus

Stage: **Scope sizing and split planning** (usually before requesting review).

## Use Instead [if available]

- Use `pr-self-review` for a full author checklist beyond PR size/scope.
- Use `pr-create` to draft and open the PR once scope is settled.
- Use `pr-review` for reviewer-side feedback on an already-open PR.

## Example usage

"Is this PR too big?"
"Help me split this PR into smaller ones"
"Check my PR size and suggest a split strategy"

---

## Workflow

Here's how I guide you through PR size assessment and splitting:

### Step 1: Size Assessment
I'll ask for your PR stats if not provided in context:
- How many files changed?
- How many lines added?
- How many lines deleted?
- Rough breakdown by area (auth, API, UI, database, etc.)

Alternatively, you can paste the PR diff or provide a link to an open PR.

### Step 2: Threshold Check
I'll evaluate against the standard threshold:
- **Too big if**: changes span >1 distinct logical concern (regardless of line count)
- **Needs atomicity check if**: >400 lines but still one concern
  - If the change is cleanly splittable: treat as too large and split
  - If the change is truly atomic/unsplittable: keep as one PR and use Step 3c review guidance
- **Clearly OK if**: <=400 lines and focused on one concern

Examples:
- ✅ 300 lines adding auth validation → Within threshold (single concern)
- ❌ 250 lines of auth + 200 lines of payment changes → Over threshold (2 separate concerns)
- ⚠️ 500 lines adding a complete new API endpoint with routes, handlers, and tests → Single concern; run atomicity check (split if possible, otherwise Step 3c)
- ⚠️ 600 lines refactoring one module → Single concern; run atomicity check (split if possible, otherwise Step 3c)
- ❌ 600 lines refactoring + 100 lines new feature → Over threshold (2 concerns: refactor + feature)

### Step 3a: If Within Threshold
**✅ Your PR is appropriately sized!**
- Proceed to request review
- No split needed
- Use your regular review process

### Step 3b: If Above Threshold
**⚠️ Your PR is too large.**

I'll help you split it:

1. **Identify distinct concerns**: Read the diff and group changes by concern
   - "Concern A: Add authentication"
   - "Concern B: Refactor payment logic"
   - "Concern C: Update documentation"

2. **Order by dependency**: Determine the sequence for splitting
   - Core functionality first (what other concerns depend on?)
   - Dependent changes later (what depends on the core?)
   - Standalone refactors last (no dependencies)

   Example order:
   ```
   PR-1: Add auth validation (core)
   PR-2: Update payment to use auth (depends on PR-1)
   PR-3: Documentation and cleanup (independent)
   ```

3. **Guide branch strategy**: Create a plan for splitting
   - Create a feature branch for each concern
   - Base each branch on `main` or previous PR branch (if dependent)
   - Keep commits organized: one PR per concern

4. **Walk through execution**: Help you execute the split
   - Which files go in which PR?
   - What order to open them?
   - How to test each one independently?

### Step 3c: If Unsplittable
**🔒 Large but can't be split**

Some changes are genuinely atomic and can't be split (e.g., auto-generated files, schema migrations, large renames). I'll help you handle this:

1. **Document in PR description**:
   ```
   NOTES: This PR is larger than our standard threshold because:
   [Explain why it cannot be split]
   ```

2. **Guide review strategy**:
   - Use "file-by-file review" mode with the reviewer
   - Schedule a walkthrough to discuss the change
   - Highlight the most critical files for review focus

3. **Suggest alternatives**:
   - Can any preparatory work be split into a separate PR?
   - Can any cleanup be deferred to a follow-up PR?
   - Can the change be phased over multiple PRs in a different way?

---

## Size Threshold Details

**Why 400 lines?**
- Industry research (Google, SmartBear): 400 lines is where review effectiveness drops significantly
- Beyond this, reviewers miss 50% more defects
- Aligns with "fits in one review session" (30–45 minutes)

**Why "concern-based" splitting?**
- Lines changed can be misleading (auto-generated files, large renames)
- What matters is logical cohesion: one concern per PR
- Concern-based PRs are easier to review, test, and revert if needed

## Tips for Success

- **Split early**: Before requesting review, check the size
- **Be specific about concerns**: "auth + refactor" is clearer than "various changes"
- **Test each PR independently**: After splitting, verify each PR works in isolation
- **Order carefully**: Base dependent PRs on each other, not all on main
- **Communicate**: If you can't split, explain why in the PR description
- **Ask for help**: If unsure about splitting strategy, run this skill first
