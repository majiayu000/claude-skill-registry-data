---
name: code-review
description: "A skill for performing structured code reviews based on git diffs and specialist instructions. Use this skill to analyze code changes, identify required adjustments, and generate detailed review reports that comply with the system's guidelines for surgical changes and security best practices."
argument-hint: "[git_diff_command]: A string command containing the git diff output to be analyzed for code review."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

MANDATORY: Use agents [reviewer-specialist, git-specialist,design-pattern-specialist, security-specialist]

MANDATORY: execute the **{git_diff_command}** argument as a git diff command or any other command that produces a diff-like output or a code file and analyze the output according to the system instructions.

TASK:
Analyze ONLY the provided git diff and identify required adjustments, improvements, or refactorings that strictly comply with the system instructions.

SCOPE & CONSTRAINTS:

- Base your analysis exclusively on the content present in the diff.
- Do NOT infer, assume, or reference code outside the diff.
- Do NOT suggest speculative, stylistic, or unrelated changes.
- Only propose changes that are objectively justified by the system instructions.
- If the diff is already fully compliant, explicitly state that no improvements are required.

PROCESS (internal, do not output):

1. Treat system instructions as authoritative.
2. Analyze the diff line by line.
3. Identify only concrete, observable issues or improvement opportunities.
4. Group findings by independent modification units.
5. Ensure each unit follows the exact same structure.

OUTPUT RULES (MANDATORY):

- Output MUST be a single Markdown file.
- Do NOT include text outside the file content.
- Do NOT explain reasoning outside the defined sections.
- Do NOT include code blocks unless explicitly required inside a section.

FILE PATH RULES:

- Save the file at:
  `docs/agents/reviews/yyyy-mm-dd-<short-description>.md`

FILE CONTENT FORMAT (STRICT):
The file MUST contain exactly the structure below and nothing else:

<description>

## Summary

High-level overview of the analysis result.

## Motivation

Why a review or changes are necessary, strictly based on the diff.

## Proposed Changes

For EACH required modification or improvement, use the following fixed structure:

### Change <N>: <Short Title>

**Type:** Bugfix | Refactor | Compliance | Improvement
**Severity:** Low | Medium | High | Critical

**Problem**
Clear and objective description of the issue, referencing only the diff.

**Evidence**
Specific lines or patterns observed in the diff that justify the change.

**Proposed Adjustment**
Exact description of what must be changed or improved (no speculation).

**Expected Outcome**
What will be improved or corrected after applying this change.

---

(Repeat the structure above for every identified change)

If no changes are required, this section MUST contain exactly:

> No changes required. The diff is fully compliant with the system instructions.

## Alternatives Considered

Briefly list any viable alternatives that were consciously not chosen, or explicitly state:

> No viable alternatives identified within the scope of the diff.

## Risks & Mitigations

Concrete risks introduced by the proposed changes and how to mitigate them, or:

> No significant risks identified.

</description>
