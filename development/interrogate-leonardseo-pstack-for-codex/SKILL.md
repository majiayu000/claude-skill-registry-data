---
name: interrogate
description: Use for "interrogate", "adversarial review", "independent-run review",
  "challenge this", "stress test this code", "find blind spots", or "tear this apart".
  Multiple LLM reviewers challenge changes from independent angles.
---

Read [Codex runtime contract](../../CODEX-RUNTIME.md) before applying this workflow. It governs tools, delegation, models, authorization and fallbacks.


# Interrogate

Run one reviewer per configured review seat to adversarially review code changes. The signal comes from separately evidenced review runs. Record the actual model used; repeated runs on one model are not model diversity. The deliverable is a synthesized verdict. Do NOT auto-apply changes.

## Step 1, Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that.
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) for the full changeset.
- If the user's message references recent work, gather the relevant files.

Package the diff or file contents with any surrounding context files the reviewers need to understand the code.

## Step 2, Intent

Before spawning reviewers, state the intent in one clear paragraph from the user's message, commit messages, the PR description if one exists, and the code. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Use Review count from explicitly loaded .agents/pstack-config.md, default two. Launch permitted reviewers through actual native tools, or perform separately recorded sequential review passes. Default all roles to inherit-parent; only use explicitly authorized exposed model overrides.

| Subagent | Default model |
|----------|---------------|
| Reviewer A | `inherit-parent` |
| Reviewer B | `inherit-parent` |

For each reviewer, give an explicit read-only scope and the template path.

If a configured model is unsupported, report it and inherit the parent under CODEX-RUNTIME.md. Do not guess a replacement.

Read `references/reviewer-prompt.md` and fill in the same template for every reviewer with the stated intent, the diff or file contents, the rubric from `references/rubric.md`, and the code-quality lens from `references/code-quality-review.md`.

## Step 4, Synthesize

As results come back, build a unified picture. Parse every reviewer's findings. Merge findings that describe the same issue differently, and note which models raised each one. Findings independently reproduced by multiple reviewers deserve attention, but agreement on one model is not independent model-family evidence. Read a lone model's finding, but weight it accordingly. Note disagreements. If one model flags something and another explicitly says the opposite, that is context for the verdict.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Read `references/lead-judgment.md` for the full framework. Put every finding in one of four buckets, with the model(s) that raised it and a one-line rationale.

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. They would block a real PR.
- **Consider**. Legitimate, but you're not sure they outweigh the cost of addressing them now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact at this stage.
- **Dismissed**. Wrong, nitpicky, or missing context, with a brief reason.

## Output Format

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer [label]: [model name], [N findings] (one bullet per reviewer)

### Act On
[Each: description, which models raised it, why it matters.]

### Consider
[Each: description, which models raised it, the tradeoff.]

### Noted
[Brief list.]

### Dismissed
[Each with a brief rationale.]

### Agreement Map
[Where models agreed and diverged, and what that pattern tells us.]
