---
name: oss:documentation-pr
description: Phase 4 of OSS contribution - Document changes and create a comprehensive, reviewable pull request. Writes clear PR description, documents code changes, creates changelog entries, and prepares for review. Use when implementation is complete and ready to submit work.
---

# Phase 4: Documentation & PR Creation

Document changes and create a comprehensive, reviewable pull request.

## Purpose

Create a pull request that:
- Clearly communicates changes
- Justifies the approach
- Makes reviewer's job easy
- Increases merge probability
- Serves as documentation

## When to Use

**Triggers:**
- "PR 작성"
- "pull request 준비"
- "문서화해줘"
- "리뷰 준비"

**Use when:**
- Implementation is complete
- Tests pass locally
- Ready to submit work
- Want to create high-quality PR

## PR Creation Framework

### Step 0: CONTRIBUTING.md Final Verification

**MANDATORY: Final compliance check before PR submission**
- Review CONTRIBUTING.md requirements from Phase 1 one last time
- Verify ALL requirements are met:
  - Code style and formatting standards
  - Commit message format and conventions
  - Branch naming requirements
  - Testing requirements
  - Documentation standards
  - PR submission process
- **PR MUST strictly follow all CONTRIBUTING.md guidelines**

### Step 1: Pre-PR Checklist

Verify everything is ready before creating PR.

```markdown
### Pre-PR Checklist

**CONTRIBUTING.md Compliance:**
- [ ] All contribution guidelines followed
- [ ] Commit messages follow required format
- [ ] Branch named according to conventions
- [ ] Code style matches project standards

**Code quality:**
- [ ] All tests pass locally
- [ ] Linting passes
- [ ] Type checking passes (if applicable)
- [ ] Build succeeds
- [ ] No compiler warnings

**Functionality:**
- [ ] All requirements implemented
- [ ] Edge cases handled
- [ ] Error handling complete
- [ ] Manual testing done

**Tests:**
- [ ] New tests added
- [ ] Existing tests still pass
- [ ] Coverage meets threshold
- [ ] Tests are meaningful

**Documentation:**
- [ ] Code comments added where needed
- [ ] README updated (if needed)
- [ ] CHANGELOG entry added
- [ ] API docs updated (if applicable)

**Git hygiene:**
- [ ] Branch is up to date with main
- [ ] Commits are logical and focused
- [ ] Commit messages are clear
- [ ] No merge commits (rebased if needed)
- [ ] No secrets or sensitive data

**Review readiness:**
- [ ] Self-reviewed all changes
- [ ] Removed debugging code
- [ ] Removed commented-out code
- [ ] No unrelated changes
```

### Step 2: Branch Management

Ensure clean branch state.

**Branch best practices:**

**IMPORTANT: Follow CONTRIBUTING.md branch naming conventions**

```bash
# Create feature branch following project conventions
# Check CONTRIBUTING.md for required format (e.g., feature/, fix/, etc.)
git checkout -b feature/issue-123-description

# Update from main
git fetch origin
git rebase origin/main

# Check status
git status
# Should be clean, ahead of main

# View your commits
git log origin/main..HEAD --oneline
# Should be focused, logical commits

# If commits need cleanup, interactive rebase
git rebase -i origin/main
# Squash, reword, reorder as needed
```

**Commit message quality:**

**IMPORTANT: Follow CONTRIBUTING.md commit message format**
- Check project's required commit message convention
- Some projects use Conventional Commits, others have custom formats
- Verify before writing commit messages

```markdown
### Good Commit Messages

**Format (verify with CONTRIBUTING.md):**
```
type(scope): brief description

Detailed explanation of what and why (not how).
Focus on the motivation and context.

Closes #123
```

**Types:**
- feat: New feature
- fix: Bug fix
- docs: Documentation only
- style: Formatting, no code change
- refactor: Code change without behavior change
- test: Adding tests
- chore: Build process, tooling

**Examples:**

✅ **Good:**
```
fix(auth): handle null user in session validation

Previously, the session validator crashed when user
was null during logout race conditions. Now returns
early with invalid session.

Closes #123
```

❌ **Bad:**
```
fix stuff
```

✅ **Good:**
```
feat(export): add CSV export functionality

Implements CSV export with customizable columns and
optional header row. Uses streaming for large datasets
to avoid memory issues.

- Add exportToCSV function
- Add column selection UI
- Add tests for edge cases

Closes #456
```

❌ **Bad:**
```
added feature
```
```

### Step 3: PR Title

Craft clear, descriptive PR title.

**Title format:**

```markdown
### PR Title

**Format:** [Type] Brief description of change

**Examples:**

✅ Good titles:
- "Fix: Handle null values in session validation"
- "Feature: Add CSV export with column selection"
- "Refactor: Extract validation logic to separate module"
- "Docs: Add examples for authentication flow"

❌ Bad titles:
- "Fix bug"
- "Update code"
- "Changes"
- "PR for issue #123"

**Guidelines:**
- Start with type: Fix/Feature/Refactor/Docs
- Use imperative mood ("Add" not "Added")
- Be specific but concise
- Mention issue number if applicable
- Max ~60-70 characters
```

### Step 4: PR Description

Write comprehensive PR description.

**Description template:**

```markdown
## PR Description Template

### Summary
[2-3 sentences: What changes, why they're needed, what problem they solve]

### Changes Made
- [Change 1: specific, actionable description]
- [Change 2]
- [Change 3]

### Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test coverage improvement

### Related Issue
Fixes #[issue-number]
<!-- or -->
Relates to #[issue-number]

### How to Test
1. [Step 1: how to set up test scenario]
2. [Step 2: what to do]
3. [Step 3: what to verify]

**Expected behavior:** [what should happen]

### Screenshots (if applicable)
**Before:**
[screenshot or description]

**After:**
[screenshot or description]

### Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

### Additional Notes
[Any context, tradeoffs, alternative approaches considered, future work, or breaking changes]
```

**Customized example:**

```markdown
## Add CSV Export Functionality

### Summary
Implements CSV export feature requested in #456. Users can now export data
tables to CSV format with customizable column selection and optional headers.
Uses streaming approach to handle large datasets without memory issues.

### Changes Made
- Add `exportToCSV` function in `utils/export.js`
- Add column selection checkbox UI in export dialog
- Add "Include Headers" toggle option
- Implement streaming for datasets >10k rows
- Add comprehensive tests for edge cases (empty data, special characters, large datasets)
- Update README with export feature documentation

### Type of Change
- [x] New feature (non-breaking change which adds functionality)

### Related Issue
Fixes #456

### How to Test
1. Navigate to any data table page
2. Click "Export" button in toolbar
3. Select columns to export using checkboxes
4. Toggle "Include Headers" option
5. Click "Download CSV"
6. Verify downloaded file contains expected data

**Expected behavior:** CSV file downloads with selected columns, properly escaped special characters, and headers if enabled.

**Edge cases to test:**
- Empty dataset → Downloads empty file or shows warning
- Large dataset (>10k rows) → Progress indicator shows, no memory issues
- Special characters in data → Properly escaped in CSV

### Screenshots
**Export Dialog:**
[screenshot of new export UI]

**Sample Output:**
```csv
Name,Email,Role
John Doe,john@example.com,Admin
Jane Smith,jane@example.com,User
```

### Checklist
- [x] My code follows the project's style guidelines
- [x] I have performed a self-review of my code
- [x] I have commented my code, particularly in hard-to-understand areas
- [x] I have made corresponding changes to the documentation
- [x] My changes generate no new warnings
- [x] I have added tests that prove my fix is effective or that my feature works
- [x] New and existing unit tests pass locally with my changes
- [x] Any dependent changes have been merged and published

### Additional Notes

**Design decisions:**
- Used streaming for large datasets instead of loading all in memory
- Followed RFC 4180 for CSV format to ensure compatibility
- Made column selection persistent in localStorage

**Future improvements (out of scope for this PR):**
- Add Excel export format
- Add export templates
- Add scheduled exports

**Breaking changes:** None
```

### Step 5: Project-Specific PR Templates

Adapt to project's PR template if exists.

**Check for templates:**
```bash
# Look for PR template
cat .github/PULL_REQUEST_TEMPLATE.md
cat .github/pull_request_template.md
cat docs/pull_request_template.md

# Some projects use issue templates
ls .github/ISSUE_TEMPLATE/
```

**Follow template exactly:**
- Don't skip sections
- Fill in all required fields
- Check all relevant boxes
- Provide requested information

**If no template:**
- Use framework's template above
- Look at recent merged PRs for format
- Follow community conventions

### Step 6: Review Preparation

Make reviewer's job easy.

**Reviewer-friendly practices:**

```markdown
### Making PR Easy to Review

**Size:**
- 🟢 Small: < 200 lines changed
- 🟡 Medium: 200-500 lines
- 🔴 Large: > 500 lines (consider splitting)

**If PR is large:**
- Explain why it can't be split
- Provide roadmap of changes
- Highlight key areas to review
- Offer to review in parts

**Structure:**
- Logical commit history
- Each commit compiles/works
- Related changes grouped
- Unrelated changes separated

**Communication:**
- Clear descriptions
- Inline comments on tricky code
- Link to design docs
- Explain tradeoffs

**Context:**
- Why this approach?
- What alternatives considered?
- Any performance implications?
- Breaking changes?
```

**Add code comments in PR:**

Use GitHub's review comment feature to explain:
- Why specific approach taken
- Known limitations
- Areas you want feedback on
- Anything non-obvious

**Example:**
```javascript
// (Add PR comment: "This uses binary search instead of linear scan
// because dataset can be large. Benchmarked 100x faster on 10k items.")
const index = binarySearch(array, target)
```

### Step 7: CI/CD Preparation

Ensure automated checks will pass.

```markdown
### CI/CD Checklist

**Before pushing:**
- [ ] All tests pass locally
- [ ] Linting passes
- [ ] Type checking passes
- [ ] Build succeeds
- [ ] Coverage meets threshold

**After pushing:**
- [ ] Monitor CI/CD pipeline
- [ ] All checks pass
- [ ] No flaky test failures
- [ ] Build artifacts generated (if applicable)

**If CI fails:**
- Fix immediately
- Don't wait for reviewer
- Force push if fixing commits
- Comment explaining fixes
```

**Common CI failures:**

```markdown
### Troubleshooting CI

**Tests fail in CI but pass locally:**
- [ ] Check for timezone assumptions
- [ ] Check for file path assumptions (Windows vs Unix)
- [ ] Check for race conditions
- [ ] Check for missing test data
- [ ] Check for environment differences

**Linting fails:**
```bash
# Run same linter locally
npm run lint
# Auto-fix if possible
npm run lint:fix
```

**Build fails:**
```bash
# Clean build locally
rm -rf node_modules dist
npm install
npm run build
```

**Coverage below threshold:**
```bash
# Check coverage locally
npm run test:coverage
# Add missing tests
```
```

### Step 8: PR Submission

Submit PR and engage with feedback.

**Submission process:**

```bash
# Push branch to remote
git push -u origin feature/issue-123-description

# Create PR via CLI (if using gh)
gh pr create --title "Fix: Handle null user in session" \
             --body-file pr-description.md \
             --label bug \
             --assignee @me

# Or via GitHub web interface
# 1. Go to repository
# 2. Click "Pull requests" tab
# 3. Click "New pull request"
# 4. Select your branch
# 5. Fill in title and description
# 6. Click "Create pull request"
```

**After submission:**

```markdown
### Post-Submission Actions

**Immediately:**
- [ ] Comment on original issue linking to PR
  "Submitted PR #789 to address this issue"
- [ ] Add appropriate labels (if permissions allow)
- [ ] Request review from maintainers (if process requires)
- [ ] Link any related issues/PRs

**Monitor:**
- [ ] CI/CD status - fix if failing
- [ ] Review comments - respond promptly
- [ ] Merge conflicts - resolve quickly
- [ ] Feedback - address constructively

**Be responsive:**
- Respond to comments within 24-48 hours
- Thank reviewers for feedback
- Explain reasoning if disagreeing
- Make requested changes promptly
- Keep discussion respectful and professional
```

### Step 9: Handling Feedback

Respond to review comments effectively.

**Review response best practices:**

```markdown
### Responding to Reviews

**Good practices:**

✅ **Acknowledge feedback:**
"Good catch! I'll fix this."
"That's a great point. Let me refactor this."

✅ **Explain reasoning:**
"I used approach X because Y. However, I see your point about Z. Let me try W instead."

✅ **Ask clarifying questions:**
"I'm not sure I understand the concern here. Could you elaborate on the edge case you're thinking of?"

✅ **Suggest alternatives:**
"Would you prefer approach A or B? I think A is simpler but B is more extensible."

✅ **Mark resolved:**
After addressing comment, reply "Done" or "Fixed in [commit]" and resolve thread

❌ **Avoid:**
- Defensive responses
- Ignoring feedback
- Taking criticism personally
- Arguing unnecessarily
- Making excuses

**Types of feedback:**

**1. Bugs/Issues (Must fix):**
- Fix immediately
- Add test to prevent regression
- Thank reviewer

**2. Style/Convention (Must fix):**
- Follow project standards
- Even if you disagree
- Consistency matters

**3. Suggestions (Evaluate):**
- Consider merit
- Discuss tradeoffs
- Implement if better
- Explain if not

**4. Questions (Answer):**
- Clarify approach
- Add comments if unclear
- May indicate code needs simplification

**5. Nitpicks (Optional):**
- Fix if easy
- Push back if not valuable
- "Will fix in follow-up" if time-consuming
```

**Making changes:**

```bash
# Make requested changes
[edit files]

# Commit changes
git add [files]
git commit -m "Address review feedback: improve error handling"

# Push to PR
git push

# Comment on review
"Changes made in [commit-hash]"
```

### Step 10: Merge Preparation

Final steps before merge.

```markdown
### Pre-Merge Checklist

**Code review:**
- [ ] All reviewer comments addressed
- [ ] Requested changes made
- [ ] Approvals received (per project policy)
- [ ] No unresolved threads

**CI/CD:**
- [ ] All checks passing
- [ ] No merge conflicts
- [ ] Branch up to date with main

**Final review:**
- [ ] Re-review your changes
- [ ] Check for any last-minute issues
- [ ] Verify all commits are squashed (if project requires)
- [ ] Verify commit message is clean

**Documentation:**
- [ ] CHANGELOG updated
- [ ] README current
- [ ] Migration guide (if breaking)
- [ ] Release notes drafted (if applicable)

**Ready to merge:**
- [ ] Maintainer approval received
- [ ] All checks passed
- [ ] No outstanding concerns
- [ ] Follow-up issues created (if any)
```

## PR Quality Checklist

Use this to ensure high-quality PRs:

```markdown
### PR Quality Checklist

**Clarity:**
- [ ] Title is clear and descriptive
- [ ] Description explains what and why
- [ ] Changes are well-organized
- [ ] Context is provided

**Completeness:**
- [ ] All requirements addressed
- [ ] Tests included
- [ ] Documentation updated
- [ ] Edge cases handled

**Reviewability:**
- [ ] PR is focused (single concern)
- [ ] Size is reasonable
- [ ] Commits are logical
- [ ] Code is self-explanatory

**Technical:**
- [ ] Follows conventions
- [ ] No obvious issues
- [ ] Tests pass
- [ ] CI passes

**Communication:**
- [ ] Original issue linked
- [ ] How to test explained
- [ ] Tradeoffs documented
- [ ] Breaking changes highlighted
```

## Common Pitfalls

**Avoid:**

❌ **Vague descriptions** - "Fixed bug" tells nothing
❌ **Huge PRs** - Hard to review, less likely to merge
❌ **Mixing concerns** - Multiple unrelated changes
❌ **No tests** - Reviewers will ask for them
❌ **Ignoring CI failures** - Shows lack of diligence
❌ **Poor commit messages** - Makes history useless
❌ **Defensive attitude** - Makes collaboration difficult
❌ **Rushing** - Quality beats speed

## Output Format

Provide PR creation guide:

```markdown
# 📤 Pull Request Ready: [Issue Title]

**Issue:** #[number]
**Branch:** [branch-name]
**Status:** Ready to submit

---

## PR Information

**Title:**
```
[Type]: [Clear description]
```

**Description:**
```
[Full PR description using template]
```

**Labels:** [suggested labels]

---

## Pre-Submission Checklist

**Code:**
- ✅ Tests pass
- ✅ Linting passes
- ✅ Build succeeds
- ✅ Self-reviewed

**Documentation:**
- ✅ Comments added
- ✅ README updated
- ✅ CHANGELOG entry
- ✅ API docs updated

**Git:**
- ✅ Branch up to date
- ✅ Commits clean
- ✅ No secrets
- ✅ No merge commits

---

## Submission Command

```bash
# Push branch
git push -u origin [branch-name]

# Create PR (via gh CLI)
gh pr create --title "[title]" --body "[description]"

# Or use GitHub web interface
# https://github.com/[owner]/[repo]/compare/[branch]
```

---

## Post-Submission

**Next steps:**
1. Monitor CI/CD pipeline
2. Respond to review comments promptly
3. Address feedback constructively
4. Keep PR updated with main branch

**Timeline:**
- Review typically within: [project-specific]
- Address feedback within: 24-48 hours
- Merge after: approvals + CI pass

---

## 🎉 Contribution Complete!

Thank you for contributing to open source!

**After merge:**
- [ ] Close related issues
- [ ] Update local main branch
- [ ] Delete feature branch
- [ ] Celebrate! 🎉

**Future contributions:**
- Consider more complex issues
- Help review others' PRs
- Improve documentation
- Engage with community
```

## Integration with Main Framework

When invoked from main framework:

1. **Receive context:** Implemented changes from Phase 3, test results, branch state
2. **Guide documentation:** PR title, description, checklist
3. **Verify readiness:** All quality checks met
4. **Return PR content:** Ready to copy/paste or submit
5. **Update tracker:** Mark Phase 4 complete - contribution done!

This completes the full OSS contribution workflow.

## Learning from Reviews

**Track feedback patterns:**
- What do reviewers commonly ask for?
- What mistakes do you repeat?
- What can you catch in self-review?
- How to improve next PR?

**Build reputation:**
- High-quality PRs
- Responsive to feedback
- Respectful communication
- Consistent contributions

**Each PR is practice for the next one!**
