---
name: self-validate
description: After any batch of changes (edits, skill updates, cross-references, docs), runs systematic validation to catch inconsistencies, missing references, broken links, and syntax errors before declaring done. Prevents the need for follow-up corrections.
---

# Self-Validate Skill

## Problem it solves

Changes are declared complete without verifying they actually took effect. Cross-references are added to some files but not others. Links point to nowhere. Batch operations silently fail on some items. The user catches it and the fix gets re-done.

## Protocol

### 1. After every batch operation

Run a validation scan before declaring done. Use the appropriate checks:

### 2. Cross-reference validation

When adding cross-references across multiple files:

```powershell
$base = "<skills-path>"
$missing = @()
Get-ChildItem $base -Directory | ForEach-Object {
    $path = Join-Path $_.FullName "SKILL.md"
    if (Test-Path $path) {
        $content = Get-Content $path -Raw
        if ($content -notmatch "## Cross-references") {
            $missing += $_.Name
        }
    }
}
if ($missing.Count -gt 0) {
    Write-Warning "Missing cross-references in: $($missing -join ', ')"
}
```

### 3. File content integrity

After bulk edits (find/replace, append, regex transforms):

- Verify the total file count matches expectations
- Spot-check 2-3 files for correct content
- Check for artifacts of failed operations (e.g., `System.Collections.Hashtable[...]`, unescaped template variables)
- Ensure no files lost their original content

### 4. Link validation

When adding URLs or file references:

- Verify each URL with a web fetch or known-to-exist check
- Verify each file path reference actually points to an existing file
- Do not link to GitHub org pages when a specific repo exists
- Do not link to npm packages without checking the package exists

### 5. Cross-file consistency

When the same change touches multiple files (e.g., bat + README):

- Verify menu numbers match between implementations
- Verify descriptions say the same thing
- Verify command names are identical across all references
- Verify help sections list the same set of commands

### 6. Syntax validation

After code changes:

- For batch files: check label format, matching `goto` targets, parenthesis balance
- For PowerShell: check cmdlet names, parameter syntax
- For Python: run `py_compile` or syntax check
- For YAML/JSON: verify parseable

### 7. Re-verify after fixes

If validation finds issues, fix them and re-run the relevant validation checks. Do not assume the fix worked.

## Detection triggers

Activate automatically after:
- Bulk cross-reference additions
- Batch find/replace operations  
- Multiple simultaneous file edits
- Adding new commands, menu items, or doc sections
- Creating or modifying skill files
- Any operation where "did it actually work?" is a reasonable question

## When NOT to use
- Single-file, single-edit operations with immediate visible confirmation
- User explicitly says "don't bother validating"

## Cross-references

- **anti-premature-termination** — Both enforce verification before declaring done. self-validate focuses on technical correctness after batch operations; anti-premature-termination focuses on completion criteria for tasks.
- **project-backup-status** — Run validation before and after making changes to ensure backup integrity and change correctness.
- **follow-existing-patterns** — Validation checks that new code actually matches the existing patterns it was supposed to follow.
- **verify-and-cite** — Both require verification. self-validate checks file integrity and cross-references; verify-and-cite checks factual claims and sources.
- **universal-format-lint** — Syntax validation overlaps with linting and formatting checks.

- **audit-project** — Both run systematic checks. audit-project is broader (deps, disk, git); self-validate focuses on change integrity in the current session.
- **toolchain-fallback** — Run validation after toolchain install to confirm the fallback works.
- **project-scripts** — After generating or modifying scripts via project-scripts, validate they execute correctly and are properly cataloged.
- **release-changelog** — Validate release artifacts after cutting: version bump in the right file, changelog date/format correct, tag exists on remote, CI triggered.
- **skill-loader** — After loading a skill and its cross-references, validate the combined instruction set is consistent.
- **writing-quality-anti-slop** — After writing, self-validate against the kill-list before presenting to the user.

## Bundled validation script

A bundled script is at `scripts/validate.ps1` (PowerShell). It automates cross-reference validation, frontmatter checks, and path resolution:

```powershell
.\scripts\validate.ps1 -SkillsDir "."
.\scripts\validate.ps1 -SkillsDir "." -Fix
```

The script exits with a non-zero code if issues are found, suitable for CI/gate checks.

To use as a project-local tool:

```powershell
cp <skill-path>/self-validate/scripts/validate.ps1 .ai_scripts/
.ai_scripts\validate.ps1 -SkillsDir "."
```
