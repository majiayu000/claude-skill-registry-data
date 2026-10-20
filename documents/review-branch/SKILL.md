---
name: review-branch
description: Reviews a branch for code and security issues, verifies findings, and reports high and medium severity issues in a fenced markdown block.
---

# Review Branch

/code-review and /security-review the mentioned branch. Verify all findings before presenting them.

## Output

Put all medium and high findings, high first, in a single fenced markdown code block so the raw markdown can be copied. Inside the block, each finding is exactly one line in this format, separated by a blank line, with nothing else in the block (no headings, no notes):

**<n>. [<High|Medium>] <finding>:** `<file:line>` <description>

- Ensure the description is less than 400 characters
- If there are no medium or high findings, say so instead of printing an empty block.

After the block, list low findings as one short bullet each, then one line with the security review result.

## Example

```markdown
**1. [Medium] Skip cutoff is dated from the wrong event:** `docs/plan.md:180` The cutoff uses the first `true` in prod, but ...
```
