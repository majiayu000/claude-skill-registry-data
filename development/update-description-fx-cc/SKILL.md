---
name: update-description
description: Updates GitHub Release notes with human-readable summaries AFTER release-please creates a release. Use when user says "update release description", "improve release notes", or after merging a release-please PR. NEVER modifies the release PR body (breaks parsing).
---

# Update Release-Please Description

This skill creates human-readable summaries for release-please GitHub Releases.

## ⚠️ CRITICAL: Never Modify the Release PR Body

**DO NOT edit the release-please PR body.** Release-please parses specific patterns from the PR body to extract version information. Modifying the PR body (especially wrapping content in `<details>` tags or changing headers) will break version parsing and result in:

- `⚠ Failed to find version in release notes`
- `⚠ Failed to parse releases`
- Empty GitHub Release body

Reference: [release-please PR body parsing](https://github.com/googleapis/release-please/blob/main/src/util/pull-request-body.ts) expects `<summary>` tags to contain version patterns like `1.1.0` or `component: 1.1.0`.

## Correct Workflow

1. **Let release-please create the PR** - don't touch it
2. **Merge the PR** - release-please creates the GitHub Release
3. **Run this skill** - update the GitHub Release notes with a human-readable summary

## EXECUTION CHECKLIST

**You MUST complete each step in order. Mark each complete before proceeding.**

### [ ] STEP 1: Find the Release to Update

```bash
# List recent releases
gh release list --limit 5
```

Look for releases with empty or minimal descriptions. Check a specific release:

```bash
gh release view <TAG> --json body,tagName,name
```

**Checkpoint:** State the release tag (e.g., "Updating Release myapp-v1.1.0")

If the release body already has good content, confirm with user before overwriting.

---

### [ ] STEP 2: Get Changelog & Extract PR Numbers

Get the version's changelog section from CHANGELOG.md:

```bash
# Read CHANGELOG.md and find the version section
cat CHANGELOG.md
```

Extract ALL `(#N)` references from the version section:

```bash
# Example: extract PR numbers from changelog content
echo '<CHANGELOG_SECTION>' | grep -oE '\(#[0-9]+\)' | grep -oE '[0-9]+' | sort -u -n
```

**Checkpoint:** Report "Found N PRs: #X, #Y, #Z..."

---

### [ ] STEP 3: Fetch ALL Referenced PR Bodies

⚠️ **CRITICAL: Fetch the actual PR descriptions, not just titles!**

For EACH PR number from Step 2, fetch full details:

```bash
gh pr view <NUMBER> --json number,title,body
```

Run in parallel for efficiency.

**Checkpoint:** List each PR with its title AND a snippet of its body:
```
Fetched N PR descriptions:
- #84 "Add row numbers column": "## Summary\nAdded row numbers to help users track position..."
- #87 "Add pagination": "## Changes\n- New Pagination component\n- Supports page size selection..."
```

**VIOLATION CHECK:**
- ❌ If you only have commit messages from the changelog → GO BACK
- ❌ If you only have PR titles without bodies → GO BACK
- ✅ You should have fetched `gh pr view` for EACH `#N` reference

---

### [ ] STEP 3b: Self-Check Before Proceeding

**STOP. Answer these questions before continuing:**

1. How many PRs did Step 2 identify? ___
2. How many `gh pr view` calls did you make in Step 3? ___
3. Do these numbers match? ___

**If the numbers don't match, you skipped PRs. Go back to Step 3.**

---

### [ ] STEP 4: Categorize Changes

Using PR BODIES, categorize:

**User-facing (include):**
- New capabilities
- Noticeable improvements
- UX bug fixes
- Perceptible performance gains

**Internal-only (exclude):**
- Refactors
- Test/CI changes
- Docs changes

**Checkpoint:** List what's included vs excluded.

---

### [ ] STEP 5: Write Summary

**Audience:** Users, PMs, executives — NOT developers.

**Forbidden:** component, SSR, tRPC, virtualization, CLS, refactor, robust, seamless, enhanced

**Format:**
```markdown
### What's New
- [2-4 bullets, plain language, what users can DO]

### What's Changed
- [2-4 bullets, improvements/fixes users notice]
```

**Translations:**
| PR Body Says | You Write |
|--------------|-----------|
| "Virtualized grid for 1000+ items" | "Large lists load faster" |
| "Eliminated CLS with SSR skeletons" | "Pages no longer jump during load" |
| "Refactored Button variants" | (OMIT) |

**Checkpoint:** Draft complete.

---

### [ ] STEP 6: Update GitHub Release

Update the GitHub Release notes directly using `gh release edit`:

```bash
gh release edit <TAG> --notes '### What'\''s New

- First bullet
- Second bullet

### What'\''s Changed

- First bullet
- Second bullet

---

<details>
<summary>Full Changelog</summary>

## [X.Y.Z](compare-link) (date)

### Features
- feature 1
- feature 2

### Bug Fixes
- fix 1
- fix 2

</details>'
```

**Important:** The full changelog from CHANGELOG.md goes inside the `<details>` block.

---

### [ ] STEP 7: Verify

```bash
gh release view <TAG> --json body -q '.body' | head -30
```

**Checkpoint:** Summary at top, full changelog in collapsible section.

---

## ANTI-PATTERNS (VIOLATIONS)

These indicate you skipped steps or did something wrong:

| If you did this... | You violated... |
|--------------------|-----------------|
| Modified the release PR body | CRITICAL - breaks release-please parsing |
| Used `git log` for commit info | Step 3 - must fetch PR bodies |
| Wrote summary from PR titles | Step 3 - titles are insufficient |
| Didn't list fetched bodies | Step 3 checkpoint |
| Jumped to writing summary | Steps 2-4 |
| Used forbidden words | Step 5 rules |
