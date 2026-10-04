---
name: self-review
description: "Self-review rule compliance for the current session"
allowed-tools: Read, Grep, Glob
disable-model-invocation: true
---

Review whether rules were followed in this session.

## Instructions

1. Read all rule sources fresh from disk (do not rely on memory). Walk both the shared tier and the current tool's tier:

   ```
   ~/.config/ai/PERSONAL.md
   ~/.config/ai/guardrails.md
   ~/.config/ai/rules/*.md
   ~/.config/{{TOOL_NAME_LC}}/DEVGUARD.md      (if exists — Claude carries a thin tool-specific addendum)
   ~/.config/{{TOOL_NAME_LC}}/rules/*.md       (e.g. claude-subagent-trust.md)
   ~/.config/ai/memory/*.md                    (feedback entries only)
   ~/.config/{{TOOL_NAME_LC}}/memory/*.md      (feedback entries only — claude-* / codex-* prefix)
   ~/.config/ai/memory/private/*.md            (feedback entries only)
   ```

2. Derive the rows from what you read: one row per top-level rule (each `##` section, or each top-level bullet in a file without sections) and one row per memory feedback entry, named by its `name` field. Do not carry a fixed list — a rule that was added, removed, or renamed on disk must show up that way in the review.

3. Evaluate each row against the conversation history:
   - **✓** followed (cite evidence)
   - **✗** violated (cite the specific action/message)
   - **—** not triggered (explain why) OR `— (n/a — rule not present in this tool)` if the rule lives in a tier that does not apply to the current tool.

4. Output in this exact format: one `###` section per rule source in the walk order above, each a three-column table. Example for guardrails.md:

   ````
   ## Self-Review: Rule Compliance

   ### guardrails.md (shared)

   | Rule | Result | Evidence |
   |------|--------|----------|
   | Verification Before Completion (evidence in the same message) | ✓/✗ | ... |
   | Absence Proofs (scope match + command and output) | ✓/✗/— | ... |
   | Scope Resolution | ✓/✗/— | ... |
   | Restored Context Authority (summary-only shorthand) | ✓/✗/— | ... |
   | Pre-Implementation Gate (leanness) | ✓/✗/— | ... |
   ````

5. Close with the tally and, only when at least one row is ✗, the actionability table:

   ````
   ### Actionability

   **Followed**: N / **Violated**: N / **Not triggered**: N

   | Violation | Fix | Feasibility |
   |-----------|-----|-------------|
   | ... | hook / rule change / code change | 즉시 가능 / 규모별 분기 / 불가 (구조적 한계 — reason) |
   ````

Be brutally honest. Do not soften or omit violations.
