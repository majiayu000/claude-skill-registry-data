---
name: test-guide-from-code
version: "1.2.0"
user-invocable: true
description: Generate a manual test guide for human testers from code changes (diff, commit, MR/PR). Triggers when user says 「生成测试指南」「测试指南」「人工测试指南」「测试指引」「test guide」「根据代码生成测试」「从 MR 生成测试指南」「从 PR 生成测试指南」 (generate test guide / manual test guide / test guide from code / from MR / from PR), or provides a diff/MR/PR link and asks for a test guide.
dependencies:
  - report-output-discipline
---

# Manual Test Guide Generation

> Automatically generate a structured manual test guide from code changes, enabling testers to precisely verify changed functionality.
>
> **Input formats, output templates, and examples: see [reference.md](reference.md).**

## Prerequisite skill check

On load, verify `report-output-discipline` is available. If missing, abort and print:

`npx skills add FuDesign2008/open-skills -g --skill '*' --yes`

Do not silently fall back.

## Triggers

- 「生成测试指南」「测试指南」「人工测试指南」「测试指引」 (generate test guide / manual test guide)
- 「test guide」
- 「根据代码生成测试」「从代码生成测试指南」 (generate test from code)
- 「从 MR 生成测试指南」「从 PR 生成测试指南」 (test guide from MR / from PR)
- Supports arguments: 「生成测试指南：https://gitlab.example.com/merge_requests/123」

## When to Use

- After an MR/PR is submitted, provide a verification guide for testers
- Before a release, outline manual regression testing scope based on code changes
- For feature delivery acceptance, derive testable user behaviors from code changes

## Execution Flow

### Step 1: Obtain Changes

1. Detect input type (see input format table in [reference.md](reference.md)), choose the appropriate retrieval method
2. If URL: try CLI to get diff; if fails, prompt user to paste
3. If no input: `git diff` (working tree) or `git diff HEAD~1` (latest commit)
4. Confirm a valid diff was obtained

### Step 2: Change Analysis

1. **Changed file inventory**: grouped by functional module
2. **Change type classification**: 🆕 Added / 🔄 Modified / 🐛 Fixed / ⚙️ Config / 🗑️ Removed
3. **User-perceivable behavior changes**: infer impact on user/system behavior
4. **Implicit change identification**: config files, dependency upgrades, database migrations, API contract changes

### Step 3: Generate Test Guide

Each test item includes: test objective, prerequisites, test steps (non-developer friendly), expected results, priority.

**Priority**: P0 core business/data writes/security → P1 auxiliary features/UI/performance → P2 styling/copy/internal refactoring

**Change type → Test strategy**:
- 🆕 → Happy path + boundary/edge cases
- 🔄 → Verify changed points + regression of existing functionality
- 🐛 → Bug scenario verification + regression of related features
- ⚙️ → Config effectiveness + regression of affected features
- 🗑️ → Confirm removal + verify related features are unaffected

### Step 4: Supplement Regression Verification

Derive related modules from changed modules, list functional points requiring regression and verification methods.

### Step 5: Output

Generate the test guide using the template format in [reference.md](reference.md), **saving as a markdown file to the current working directory by default**.

**File naming**: `<feature>_manual_test_guide_<YYYY-MM-DD>.md` (naming rules and examples: see [reference.md](reference.md) "File Naming Rules")

**User override**: User can specify a custom path or filename at trigger time; save as specified.

**Conversation output**: **Do not repeat full content** — only output a brief summary: save path, test item statistics (by P0/P1/P2 distribution), 3–5 core change points, regression scope. Full test items are always written to file only (strategy: see [reference.md](reference.md) "Conversation Output Strategy").

**Derive the HTML page** after the Markdown file is written. Registry row: `人工测试指南` in `report-output-discipline/reference.md` (`human` + `接入`). Derive `<feature>_manual_test_guide_<YYYY-MM-DD>.html` beside the source following `report-output-discipline`, and report both paths.

## Red Flags

- ❌ Skipping implicit change identification, only analyzing business code
- ❌ Test steps using developer jargon ("call API", "returns 200")
- ❌ Missing the original bug scenario for bug fixes
- ❌ Mixing automated tests into the manual test guide
- ❌ Ignoring regression verification scope
- ❌ Generating test items from nothing when no diff was obtained
- ❌ Writing files without confirming the current working directory, causing files to land in the wrong location
- ❌ Filename containing spaces or special filesystem characters (`/` `\` `:` `*` `?` `"` `<` `>` `|`)
- ❌ Not reporting the full save path in the conversation after generating the file
