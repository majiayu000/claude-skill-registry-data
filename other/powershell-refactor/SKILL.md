---
name: powershell-refactor
description: Refactor existing PowerShell scripts to simplify flow, reduce duplication, standardize naming and structure, and tighten behavior without changing the intended outcome.
version: 1.1.0
---

# PowerShell Refactor Skill

## Intent

Use this skill to improve an existing PowerShell script that already works or mostly works but needs cleanup. The goal is to make the code smaller, clearer, more idiomatic, and easier to maintain without introducing unnecessary abstractions or changing the script's job.

## Use When

- A PowerShell script feels repetitive, bloated, inconsistent, or hard to follow
- Function names, parameter names, or output patterns need to be standardized
- The user wants a script simplified, tightened, cleaned up, or refactored
- The script should be aligned with practical PowerShell conventions for real admin automation

## Do Not Use When

- The main task is to create a brand new script from scratch
- The request is mostly about documentation, README writing, or tutorial content
- The user wants a major architecture redesign instead of a focused refactor
- The script's expected behavior is unclear and changing it would be risky

## Workflow

1. Read the existing script first and identify the real behavior that must stay intact.
2. Find the highest value cleanup targets:
   - duplicated logic
   - dead code
   - inconsistent naming
   - unclear control flow
   - noisy error handling
   - unnecessary wrappers or abstractions
3. Refactor in place with the smallest set of edits that materially improves the script.
4. Prefer native PowerShell patterns:
   - approved verbs
   - clear parameter blocks
   - pipeline-aware logic when it adds value
   - `try` and `catch` only where they improve control and diagnostics
   - `Write-Verbose`, `Write-Warning`, and structured output instead of ad hoc console noise
5. Keep function boundaries practical. Split code only when it improves readability or reuse in a clear way.
6. Recheck for behavior drift, naming consistency, and obvious lint or test issues before finishing.

## Scope Presets

Let the user control how aggressive the pass is. Default to `full cleanup` when no preset is named:

- `naming only`: rename functions to approved verbs, standardize parameter and variable casing, touch nothing else
- `deduplication only`: collapse repeated logic into shared functions or loops, keep all names and structure otherwise
- `full cleanup`: the complete workflow above

When the user names a preset, stay inside it even when other cleanup targets are visible; list the out-of-scope findings at the end instead of fixing them.

## PSScriptAnalyzer Alignment

Run `Invoke-ScriptAnalyzer` on the script before and after when it is available, honoring any `PSScriptAnalyzerSettings.psd1` in the repo. Fix the violations that fall inside the chosen scope preset, and list any remaining ones with a one-line reason they were left, such as a deliberate `Write-Host` for interactive output. The refactor should never introduce new violations.

## Change Summary

End every refactor with a before-and-after summary so the user can review the pass at a glance:

```text
Refactor Summary
- Behavior preserved: [yes / exceptions explicitly listed]
- Lines: [before] -> [after]
- Changes:
  - [each behavior-preserving change in one line, e.g. "merged 3 duplicate retry blocks into Invoke-WithRetry"]
- Analyzer: [violations fixed] fixed, [count] remaining (listed above)
- Out of scope findings: [anything noticed but not touched]
```

## Constraints

- Preserve the script's intended behavior unless the user explicitly asks for a behavior change
- Prefer editing existing files over creating new ones
- Remove obsolete code instead of keeping compatibility shims
- Do not add layers, helper classes, or extra modules unless the current script clearly needs them
- Keep output, parameters, and side effects predictable
- Use comments only where the logic would otherwise be hard to follow
- If a destructive or high risk action is present, preserve or improve safety controls such as `ShouldProcess`, confirmation, or validation

## References

- `shared/skill-standard.md`
- `shared/naming-conventions.md`
- Existing repo patterns in the target script's project

## Help And Examples

Use this skill when the user already has a PowerShell script and wants it cleaned up, simplified, or standardized.

Minimum useful input:

- the `.ps1` or `.psm1` file to refactor
- the behavior that must stay the same
- any style constraints such as approved verbs, no comments, or keeping it single file

Example prompts:

```text
Refactor this PowerShell script to reduce duplication and make the error handling cleaner, but keep the same output and parameters.
```

```text
Tighten this Intune reporting script. Keep it as one file. Rename functions to approved verbs and remove unnecessary abstraction.
```

```text
Clean up this PowerShell module and standardize the parameter blocks without changing how the commands behave.
```

## Validation Checklist

- The refactor preserves the intended behavior of the original script
- Naming, structure, and flow are more consistent than before
- Unnecessary duplication or dead code has been removed
- The result uses practical PowerShell conventions instead of generic abstractions
- Any tests, lint checks, or quick validation steps relevant to the target repo still pass
