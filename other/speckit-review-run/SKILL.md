---
name: speckit-review-run
description: 'Wraps the review coordinator (/speckit-review-run) to drive the dashboard
  card''s review phase and substeps live: mark review active on entry, flip each substep
  as its pass runs, and mark review done at the end. Composes with other review wrappers
  via the wrap seam.'
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: preset:progress-report
user-invocable: true
disable-model-invocation: false
---

# Speckit Review Run Skill

## Dashboard — enter `review`

```bash
REPORT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.specify/presets/progress-report/scripts/python/progress_report.py"
python3 "$REPORT" enter review
```

As you run each specialized review pass in the core flow, update its substep on the
card — mark it `active` when you start it and `done` when it returns. The substep
keys are exactly `code comments tests errors types simplify` (plus `pr` for a
PR-review pass, if one runs):

```bash
REPORT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.specify/presets/progress-report/scripts/python/progress_report.py"
python3 "$REPORT" substep code=active     # when the code pass starts
python3 "$REPORT" substep code=done       # when it returns
# ...and likewise for comments, tests, errors, types, simplify
```


# Comprehensive PR Review

Run a comprehensive pull request review using multiple specialized agents, each focusing on a different aspect of code quality.

**Review Aspects (optional):** "$ARGUMENTS"

## Review Workflow:

1. **Load Configuration**
   - Read the project config file at `.specify/extensions/review/review-config.yml` (if it exists).
   - If the file does not exist, fall back to the `defaults.agents` section in the extension's `extension.yml`.
   - Extract the `agents` map — each key (`code`, `comments`, `tests`, `errors`, `types`, `simplify`) is a boolean toggle.
   - Agents set to `false` **MUST** be excluded from this run. Do not launch them.

2. **Determine Review Scope**
   - Parse arguments to see if user requested specific review aspects.
   - If specific aspects were requested, run exactly those — config toggles do **not** apply (explicit user request overrides config).
   - Default (no arguments): Run all applicable reviews that are enabled in config.

3. **Available Review Aspects:**

   - **comments** - Analyze code comment accuracy and maintainability
   - **tests** - Review test coverage quality and completeness
   - **errors** - Check error handling for silent failures
   - **types** - Analyze type design and invariants (if new types added)
   - **code** - General code review for project guidelines
   - **simplify** - Simplify code for clarity and maintainability
   - **all** - Run all applicable reviews (default)

4. **Identify Changed Files**

   - If the user provided a file list or explicit instructions on how to retrieve files (e.g., only staged, only unstaged, a specific folder, etc.), follow those instructions directly.
   - Otherwise, you **MUST** execute the `.specify/extensions/review/scripts/bash/detect-changed-files.sh` with `--json` to detect changed files. **Do not** attempt to detect changes by running `git` commands directly, reading git state manually, or using any other method — always delegate to the script.
     - The script automatically picks the best detection mode:
       - **Mode A (feature branch):** diffs the current branch against the default branch (`main`/`master`) from the merge-base, plus any staged and unstaged changes.
       - **Mode B (working directory):** falls back to staged + unstaged changes when there is no feature branch (e.g., working directly on the default branch).
     - JSON output: `{"branch", "default_branch", "mode", "changed_files": [...]}`
   - **Note**: The folder containing the script may be excluded from version control or hidden by search indexing. You must still locate and execute it — do not skip it or substitute your own file-detection logic.
   - **Ignore** the `graphify-out/` directory in all review passes — exclude it from diffs, file reads, and issue reporting. If the changed-files list includes paths under `graphify-out/`, filter them out before dispatching to specialist agents. Generated knowledge-graph artifacts are out of scope for review.

5. **Determine Applicable Reviews**

   Based on changes **and** config toggles (skip any agent where `agents.<name>` is `false`):
   - **Always applicable** (if enabled): `/speckit.review.code` (general quality)
   - **If test files changed** (if enabled): `/speckit.review.tests`
   - **If comments/docs added** (if enabled): `/speckit.review.comments`
   - **If error handling changed** (if enabled): `/speckit.review.errors`
   - **If types added/modified** (if enabled): `/speckit.review.types`
   - **After passing review** (if enabled): `/speckit.review.simplify` (polish and refine)
   - If an agent is disabled by config, note it in the final summary (e.g., "simplify: skipped (disabled in config)").

6. **Launch Review Agents**

   **Sequential approach** (one at a time):
   - Easier to understand and act on
   - Each report is complete before next
   - Good for interactive review

   **Parallel approach** (user can request):
   - Launch all agents simultaneously
   - Faster for comprehensive review
   - Results come back together

7. **Aggregate Results**

   After agents complete, summarize using the four-bucket severity scheme. Always render the section headers with these emoji icons — do not substitute or drop them:
   - 🚨 **Critical** — must fix before merge (bugs, security vulnerabilities, broken contracts)
   - ⚠️ **Important** — strongly recommended (significant quality or correctness concerns)
   - 💡 **Suggestions** — worth addressing (code quality, missing tests, refactors)
   - ✨ **Optional Polish** — nice-to-have style/naming/cosmetic improvements
   - ✅ **Strengths** — what's well-done (be genuine, not perfunctory)
   - 🛠 **Recommended Action** — numbered next-steps list

8. **Provide Action Plan**

   Organize findings:
   ```markdown
   # PR Review Summary

   ## Overview
   [2–3 sentences: what this PR does and why it matters]

   ## 🚨 Critical Issues (must fix before merge)
   - [agent-name]: Issue description [file:line]

   ## ⚠️ Important Issues
   - [agent-name]: Issue description [file:line]

   ## 💡 Suggestions
   - [agent-name]: Suggestion [file:line]

   ## ✨ Optional Polish
   - [agent-name]: Polish item [file:line]

   ## ✅ Strengths
   - [What's well-done — be genuine, not perfunctory]

   ## 🛠 Recommended Action
   1. [Numbered next-steps list]

   ## Recommendation
   **[Approve | Approve with conditions | Request changes]**
   [One paragraph explaining the reasoning]
   ```

   Omit any severity bucket that has nothing to report.

## Usage Examples:

**Full review (default):**
```
/speckit-review-run
```

**Specific aspects:**
```
/speckit-review-run tests errors
# Reviews only test coverage and error handling

/speckit-review-run comments
# Reviews only code comments

/speckit-review-run simplify
# Simplifies code after passing review
```

**Parallel review:**
```
/speckit-review-run all parallel
# Launches all agents in parallel
```

## Agent Descriptions:

**comment**:
- Verifies comment accuracy vs code
- Identifies comment rot
- Checks documentation completeness

**tests**:
- Reviews behavioral test coverage
- Identifies critical gaps
- Evaluates test quality

**errors**:
- Finds silent failures
- Reviews catch blocks
- Checks error logging

**types**:
- Analyzes type encapsulation
- Reviews invariant expression
- Rates type design quality

**code**:
- Checks project-specific guidelines (`.specify/memory/constitution.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, or equivalent) compliance
- Detects bugs and issues
- Reviews general code quality

**simplify**:
- Simplifies complex code
- Improves clarity and readability
- Applies project standards
- Preserves functionality

## Tips:

- **Run early**: Before creating PR, not after
- **Focus on changes**: Agents analyze diff by default
- **Address critical first**: Fix high-priority issues before lower priority
- **Re-run after fixes**: Verify issues are resolved
- **Use specific reviews**: Target specific aspects when you know the concern

## Notes:

- Agents run autonomously and return detailed reports
- Each agent focuses on its specialty for deep analysis
- Results are actionable with specific file:line references
- Agents use appropriate models for their complexity

## Dashboard — `review` done

When every pass has run, mark the review phase done. If a pass surfaced findings you
fixed, say so in the summary; if it surfaced a blocker you can't resolve, mark the
phase blocked instead.

```bash
REPORT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.specify/presets/progress-report/scripts/python/progress_report.py"
python3 "$REPORT" substep code=done comments=done tests=done errors=done types=done simplify=done
python3 "$REPORT" done review --summary "<pass/fail + what was fixed>"
# blocked instead:  python3 "$REPORT" block review --reason "<what's blocking>"
```

The `pr` substep tracks a PR-review pass; if the PR is opened/reviewed by a later
step (e.g. autopilot's draft-PR step or `/speckit-git-pr`), mark it there with
`python3 "$REPORT" substep pr=done`. When all five phases read `done`, the dashboard
auto-renders the card as complete.
