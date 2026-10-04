---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-reviewer review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Four Claude reviewers challenge changes from independent angles."
disable-model-invocation: true
---

# Interrogate

Spawn four Claude reviewers to adversarially review code changes. Each reviewer gets the same prompt and rubric. The adversarial signal comes from independent review attempts, not assigned personas. Agreement across reviewers is high-confidence signal; lone-reviewer findings are worth reading but lower confidence.

The deliverable is a synthesized verdict. Do NOT auto-apply changes.

## Step 1, Determine Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) to get the full changeset
- If the user's message references recent work, gather the relevant files
- Design / plan / ADR docs (markdown) are in scope when the user explicitly names them as the target. State in Step 2's intent that this is a design review, not a code review, so reviewers calibrate the rubric accordingly.

Collect the material into a clear package: the diff (or file contents), and any surrounding context files the reviewers will need to understand the code.

## Step 2, State the Intent

Before spawning reviewers, state the intent explicitly. What is this code trying to accomplish? Derive this from:

- The user's message
- Commit messages
- PR description if one exists
- The code itself

Write one clear paragraph. This is critical: reviewers challenge whether the work achieves the intent well, not whether the intent itself is correct. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Launch all four in a single message using the Agent tool. All four use Claude-family models and get the same prompt built from the template in `references/reviewer-prompt.md`. The adversarial signal comes from independent attempts; the two-tier split (opus / sonnet) adds capability diversity on top.

| Subagent | Model |
|----------|-------|
| Reviewer A | `opus` |
| Reviewer B | `opus` |
| Reviewer C | `sonnet` |
| Reviewer D | `sonnet` |

For each reviewer:
- `subagent_type`: `general-purpose`
- `model`: the value from the table above
- `run_in_background`: `false`

Set `run_in_background: false` on all four. The Agent tool backgrounds agents by default, and synthesis needs every reviewer's findings before it can start. Launching them as four independent calls in one message still runs them in parallel; `false` only means their findings land in the tool results instead of arriving later as notifications.

If any reviewer does end up running in the background, do not begin Step 4 until all four have reported. A verdict built on a partial set of reviewers is worse than no verdict: the consensus signal in Step 4 depends on how many reviewers independently raised a finding, and that count is meaningless while reviewers are still outstanding. Never predict or fabricate a pending reviewer's findings.

The Agent tool's `model` parameter accepts the short tier name (`sonnet | opus | haiku | fable`); specific dated slugs and per-call reasoning-effort knobs are not accepted on direct Agent calls. If a value in the table is rejected as unresolvable, check the current list of valid values in the Agent tool's error message, pick the closest equivalent, spawn with the valid value, and open a separate PR to update this table. Do not block the review on the slug issue.

The reviewers must not modify files. Enforce this in the prompt itself ("Do not edit, write, or otherwise modify any files. Output your findings only.") — the Agent tool has no `readonly` flag, so this is a prompt-level discipline.

Read `references/reviewer-prompt.md` and fill in the template with:
1. The stated intent
2. The diff or file contents
3. The review rubric from `references/rubric.md`

Each reviewer produces structured findings as described in the prompt template.

## Step 4, Synthesize

Once all four reviewers have reported, build a unified picture:

1. **Parse all findings** from the four reviewers
2. **Identify consensus**. Findings raised by 2+ reviewers independently are highest signal.
3. **Identify lone-reviewer findings**. Still worth reading, but weight accordingly.
4. **Deduplicate**. Different reviewers may describe the same issue differently. Merge these and note which reviewers raised it.
5. **Note disagreements**. If one reviewer flags something and another explicitly says the opposite, that's useful context for the verdict.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator.

Read `references/lead-judgment.md` for the full framework. Core principle: reviewers only see a slice of the codebase. You have the full context: the goal, the constraints, the timeline, and which tradeoffs were already considered. Use that context aggressively.

Categorize every finding into one of four buckets:

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. These would block a real PR.
- **Consider**. Legitimate points, but you're not sure they outweigh the cost of addressing them right now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact given the current stage.
- **Dismissed**. Wrong, nitpicky, or missing context. Brief explanation why.

For each finding, include:
- Which reviewer(s) raised it
- The category (act on / consider / noted / dismissed)
- A one-line rationale for the categorization

## Output Format

Present the verdict in this structure:

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer A: [model name], [N findings]
- Reviewer B: [model name], [N findings]
- Reviewer C: [model name], [N findings]
- Reviewer D: [model name], [N findings]

### Act On
[Findings that should be addressed. For each: description, which reviewers raised it, why it matters.]

### Consider
[Findings worth thinking about. For each: description, which reviewers raised it, tradeoff involved.]

### Noted
[Valid but low-priority. Brief list.]

### Dismissed
[Rejected findings with brief rationale. This section matters because it shows the user what was filtered out and why, so they can override your judgment if they disagree.]

### Agreement Map
[Where did reviewers agree? Where did they diverge? What does the pattern of agreement/disagreement tell us?]
