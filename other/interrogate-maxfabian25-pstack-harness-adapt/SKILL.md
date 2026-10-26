---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Multiple LLM reviewers challenge changes from independent angles."
disable-model-invocation: true
---

# Interrogate

Spawn one reviewer per configured model to adversarially review code changes. The adversarial signal comes from model diversity, not assigned personas. The deliverable is a synthesized verdict. Do NOT auto-apply changes.

## Step 1, Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that.
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) for the full changeset.
- If the user's message references recent work, gather the relevant files.

Package the diff or file contents with any surrounding context files the reviewers need to understand the code.

## Step 2, Intent

Before spawning reviewers, state the intent in one clear paragraph from the user's message, commit messages, the PR description if one exists, and the code. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Launch all reviewers in a single message with the subagent tool, one per entry on the `interrogate reviewers` line in `~/.config/pstack/models.md`, labeled Reviewer A, B, and so on to match the entry count. If the file or that line is missing, use the table defaults for the harness you run in. They match the `interrogate reviewers` row of [harnesses.md](../poteto-mode/references/harnesses.md) (Defaults).

| Subagent | Claude Code default | Codex default |
|----------|---------------------|---------------|
| Reviewer A | `opus@xhigh` | `inherit-parent@xhigh` |
| Reviewer B | `codex:gpt-6.1-sol@xhigh` | `claude:opus@xhigh` |

Each reviewer is a read-only agent per [harnesses.md](../poteto-mode/references/harnesses.md) (Subagents), on its configured entry, or its table default when there is no configured line, applied per [harnesses.md](../poteto-mode/references/harnesses.md) (Models). An `auto` or `inherit-parent` entry runs that reviewer on the parent model. A `codex:` or `claude:` entry runs as a read-only cross-harness seat, launched in the background alongside the subagents.

If a tool rejects a configured entry, run that reviewer on its family's table default and say so. Families are Claude and GPT, read from the model after any `codex:` or `claude:` prefix. Claude models start with `claude-` or are the `opus`, `sonnet`, `haiku`, or `fable` alias. A table `inherit-parent` is the parent's family. With no family match, use Reviewer A's default. If it rejects a table default, resolve and apply per [harnesses.md](../poteto-mode/references/harnesses.md) (Models). Open a separate PR to update this default table and that row of harnesses.md only when the harness's own model list no longer offers that default. A missing CLI, a sign-in failure, or a transient error is not a stale default. Do not block the review on the model issue. Never treat an alias entry as a rejected slug or apply either fallback to it.

Read `references/reviewer-prompt.md` and fill in the same template for every reviewer with the stated intent, the diff or file contents, the rubric from `references/rubric.md`, and the code-quality lens from `references/code-quality-review.md`. Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **poteto-mode** skill.

## Step 4, Synthesize

As results come back, build a unified picture. Parse every reviewer's findings. Merge findings that describe the same issue differently, and note which models raised each one. Findings two or more models raised independently are the highest signal. Read a lone model's finding, but weight it accordingly. Note disagreements. If one model flags something and another explicitly says the opposite, that is context for the verdict.

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
