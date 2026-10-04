---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Four LLM reviewers challenge changes from independent angles."
disable-model-invocation: true
---

# Interrogate

Spawn four reviewers on four different models to adversarially review code changes. Each model gets the same prompt and rubric. The adversarial signal comes from model diversity, not assigned personas. Different models have different blind spots, priors, and reasoning patterns. Agreement across models is high-confidence signal; lone-model findings are worth reading but lower confidence.

The deliverable is a synthesized verdict. Do NOT auto-apply changes.

## Step 1, Determine Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) to get the full changeset
- If the user's message references recent work, gather the relevant files

Collect the material into a clear package: the diff (or file contents), and any surrounding context files the reviewers will need to understand the code.

## Step 2, State the Intent

Before spawning reviewers, state the intent explicitly. What is this code trying to accomplish? Derive this from:

- The user's message
- Commit messages
- PR description if one exists
- The code itself

Write one clear paragraph. This is critical: reviewers challenge whether the work achieves the intent well, not whether the intent itself is correct. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Launch all four in one parallel `subagent` call, each using the `reviewer` agent with a different model. All four get the same prompt built from the template in `references/reviewer-prompt.md`.

| Subagent | Model |
|----------|-------|
| Reviewer A | `litellm/bedrock-claude-opus-4-8` |
| Reviewer B | `litellm/bedrock-claude-opus-5` |
| Reviewer C | `litellm/qwen3.8-27b-fp8` |
| Reviewer D | `litellm/bedrock-mantle-gpt-5-6-sol` |

Use this shape:

```text
subagent({
  tasks: [
    { agent: "reviewer", model: "litellm/bedrock-claude-opus-4-8", task: REVIEW_PROMPT, output: false, progress: false },
    { agent: "reviewer", model: "litellm/bedrock-claude-opus-5", task: REVIEW_PROMPT, output: false, progress: false },
    { agent: "reviewer", model: "litellm/qwen3.8-27b-fp8", task: REVIEW_PROMPT, output: false, progress: false },
    { agent: "reviewer", model: "litellm/bedrock-mantle-gpt-5-6-sol", task: REVIEW_PROMPT, output: false, progress: false }
  ],
  concurrency: 4,
  context: "fresh"
})
```

`REVIEW_PROMPT` must explicitly say: `Review only. Do not edit files.`

If a model slug is rejected as unresolvable, run `pi --list-models`, choose the closest available model from the same family, complete the review, then update this table. Do not block the review on a slug issue.

Read `references/reviewer-prompt.md` and fill in the template with:
1. The stated intent
2. The diff or file contents
3. The review rubric from `references/rubric.md`

Each reviewer produces structured findings as described in the prompt template.

## Step 4, Synthesize

As reviewer results come back, build a unified picture:

1. **Parse all findings** from the four reviewers
2. **Identify consensus**. Findings raised by 2+ models independently are highest signal.
3. **Identify lone-model findings**. Still worth reading, but weight accordingly.
4. **Deduplicate**. Different models may describe the same issue differently. Merge these and note which models raised it.
5. **Note disagreements**. If one model flags something and another explicitly says the opposite, that's useful context for the verdict.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator.

Read `references/lead-judgment.md` for the full framework. Core principle: reviewers only see a slice of the codebase. You have the full context: the goal, the constraints, the timeline, and which tradeoffs were already considered. Use that context aggressively.

Categorize every finding into one of four buckets:

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. These would block a real PR.
- **Consider**. Legitimate points, but you're not sure they outweigh the cost of addressing them right now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact given the current stage.
- **Dismissed**. Wrong, nitpicky, or missing context. Brief explanation why.

For each finding, include:
- Which model(s) raised it
- The category (act on / consider / noted / dismissed)
- A one-line rationale for the categorization

## Output Format

Present the verdict in this structure:

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Model A: [model name], [N findings]
- Model B: [model name], [N findings]
- Model C: [model name], [N findings]
- Model D: [model name], [N findings]

### Act On
[Findings that should be addressed. For each: description, which models raised it, why it matters.]

### Consider
[Findings worth thinking about. For each: description, which models raised it, tradeoff involved.]

### Noted
[Valid but low-priority. Brief list.]

### Dismissed
[Rejected findings with brief rationale. This section matters because it shows the user what was filtered out and why, so they can override your judgment if they disagree.]

### Agreement Map
[Where did models agree? Where did they diverge? What does the pattern of agreement/disagreement tell us?]
