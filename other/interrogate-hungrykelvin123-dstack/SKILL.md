---
name: interrogate
description: "Challenge risky Roblox code or designs with bounded, independent read-only worker reviews and parent judgment. Use for $interrogate, adversarial review, or finding blind spots."
---

# Interrogate

Interrogate is a bounded adversarial review. It does not implement fixes, does not auto-apply findings, and never uses Roblox Studio MCP playtest controls. Read [`../david-mode/references/agent-runtime.md`](../david-mode/references/agent-runtime.md), [`references/interrogate-panel.md`](references/interrogate-panel.md), and [`../../models.json`](../../models.json) before dispatching reviewers.

Every reviewer uses one worker tier selected by the active client's runtime policy. Use narrow/Haiku for a local, evidence-limited review; use complex/Sonnet-high for cross-module, debugging, or security-sensitive review that is still independently bounded. Codex uses Luna-max for either tier. This is a single-model reviewer panel within the selected tier, not a multi-model panel. The parent checks the actual code and failure paths; agreement among workers is supporting evidence, not a quality guarantee.

## Step 1, Determine scope and risk

Identify the exact diff or files to review:

- a pointed diff or file set from the user's request;
- `git diff <base>...HEAD` for a branch changeset;
- the relevant recent files when the user references work just completed.

Read the smallest surrounding contracts needed to trace behavior: Roblox repository instructions, typed Luau interfaces, remotes, persistence schemas, authored instance rules, and local verification scripts. Do not pull unrelated history or raw logs into every reviewer prompt.

Classify the review using the panel contract and select its budget from `models.json.riskPolicy`. Use fewer reviewers when the diff is smaller than the class suggests. Add a reviewer only when it can see the complete evidence and the parent can wait for it; queue reviewers beyond the runtime concurrency limit.

## Step 2, State the intent

Write one paragraph describing what the change is intended to accomplish. Derive it from the user's request, repository decisions, commit/PR context, and the implementation. Review execution against the intent; do not redesign the product because a reviewer prefers a different goal. Ask the user only if the intent is genuinely unresolved.

## Step 3, Resolve the reviewer route

Use the active client's worker tier and availability checks in the runtime contract for every reviewer. Never silently replace it with another model, lower its effort, or inherit the parent in a new worker. If the selected tier is unavailable, perform a parent-only review and name the missing independent coverage. A client or model configuration file is not proof that a reviewer ran.

Give every reviewer the same intent, complete diff/file set, repository constraints, and rubric. Keep contexts independent and do not show one reviewer's findings to another before collection. Reviewers are leaves and stay read-only in a shared checkout.

Launch ready reviewers within the runtime concurrency cap, retain each handle, and drain queued reviews as slots free. The parent inspects critical paths independently while they work and waits for every launched reviewer before judging.

## Step 4, Fill the reviewer prompt

Read [`references/reviewer-prompt.md`](references/reviewer-prompt.md), [`references/rubric.md`](references/rubric.md), and [`references/code-quality-review.md`](references/code-quality-review.md). Fill one identical prompt for every lane with:

1. the intent paragraph;
2. the diff or complete file contents and only the surrounding evidence needed;
3. the rubric and code-quality lens;
4. the Roblox engineering contract, including server authority, replication, persistence, mobile performance, and the Studio MCP no-playtest boundary.

Require each reviewer to return concrete findings with severity, location, reasoning, and an optional fix. A reviewer that returns no findings is a valid result. Reviewers must not edit files, run destructive commands, call external systems, change model configuration, or launch, start, stop, simulate, or control a Roblox Studio playtest.

## Step 5, Collect receipts and synthesize

For each lane record its label, requested model and effort, route, served identity (observed or unverified), start/end, completion or dropout, finding count, and whether it saw complete evidence. Then:

1. parse every result, including explicit `no findings`;
2. deduplicate concrete issues and list all lanes that raised each one;
3. mark agreement only when at least two independent reviewers raised the same issue, while acknowledging their shared model;
4. keep lone findings visible and evaluate them on their evidence;
5. record explicit disagreements and every coverage gap.

Read [`references/lead-judgment.md`](references/lead-judgment.md). As lead reviewer, categorize each finding as **Act on**, **Consider**, **Noted**, or **Dismissed**, with the lane(s) and one-line rationale. Do not average votes: correctness, security, data integrity, and reachable failure paths outweigh popularity.

## Output format

### Intent
> [The stated intent paragraph]

### Reviewers
- Reviewer [label]: [requested model and effort], served [observed or unverified], [N findings], [complete evidence or gap]

### Act On
[Concrete blockers, with evidence and lanes]

### Consider
[Legitimate tradeoffs, with evidence and lanes]

### Noted
[Valid but low-priority observations]

### Dismissed
[Rejected findings and why]

### Agreement Map
[Agreement, lone findings, disagreements, skipped lanes, and what the coverage means]

### Verification boundary
[Checks performed locally and the exact Roblox Studio checks the user must perform. State that DStack did not use Studio MCP playtest controls.]
