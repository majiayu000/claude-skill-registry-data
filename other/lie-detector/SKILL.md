---
name: lie-detector
description: Toph's lie detector for multi-model adversarial review. She feels a heartbeat through the ground and knows when someone is lying, so a change that only claims to work does not fool her. Use for interrogate, /interrogate, adversarial review, multi-model review, "challenge this", "stress test this code", "find blind spots", "tear this apart", or a contested design before it ships. Several reviewers on different models challenge the change independently, and the lead sorts their findings into act on, consider, noted, and dismissed. Never applies changes.
---

# Toph's lie detector

Toph does not need to see a face to catch a lie. She feels the heartbeat jump through the ground. Code lies the same way. It claims to handle the empty case, the retry, the bad input, and the claim does not hold when you push on it. Put several reviewers on the change, each on a different model, and listen for where their heartbeats agree.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

The adversarial signal comes from model diversity, not from assigned personas. The deliverable is a synthesized verdict. Do not apply changes.

## Who dispatches

The top-level session running `avatar-mode` runs this skill. It dispatches one reviewer per entry on the `panel` line of the avatar-setup sheet (`${CLAUDE_CONFIG_DIR:-~/.claude}/team-avatar-models.md` on Claude Code, `${CODEX_HOME:-~/.codex}/team-avatar-models.md` on Codex), then acts as the lead.

When Toph runs this skill herself as a subagent, she cannot dispatch. She runs the reviewer prompt herself once, labels the result as one sequential pass with no model diversity, and still applies the lead judgment. Say in the reply that diversity was lost.

## Step 1. Scope

Find what to review from context.

- If the user points at files or a diff, use that.
- On a feature branch, run `git diff main...HEAD`, or against the right base branch, for the full change.
- If the message refers to recent work, gather the relevant files.

Package the diff or the file contents with any surrounding files a reviewer needs to understand the code.

## Step 2. Intent

Before dispatching, state the intent in one clear paragraph. Draw it from the user's message, the commit messages, the PR description, and the code. If you are unsure of the intent, ask the user before you go on.

## Step 3. Dispatch the reviewers

Dispatch every reviewer in one message, one per entry on the `panel` line, labeled Reviewer A, B, and so on to match the entry count. With no sheet or no `panel` line, use these defaults.

| Reviewer | Default model |
|----------|---------------|
| Reviewer A | `opus` |
| Reviewer B | `fable` |
| Reviewer C | `sonnet` |
| Reviewer D | `haiku` |

Each reviewer is `subagent_type: "team-avatar:toph"`, so it stays read-only, with `run_in_background: true` and `model` set to its entry. Omit `model` for an `inherit` entry, so that reviewer runs on the parent model. An entry that carries an effort, as in `opus @high`, passes that level as the Agent tool's `effort` parameter.

If the Agent tool rejects an entry, run that reviewer on its family's default from the table and say so. Families go by model name, such as Opus, Fable, Sonnet, or Haiku. With no family match, use Reviewer A's default. If it rejects a table default, use the closest valid model from its error message, preferring the same family and tier, and name the substitution in the report. Do not block the review on a model name. Never treat an `inherit` entry as rejected.

Build every reviewer's prompt from [references/reviewer-prompt.md](references/reviewer-prompt.md). Fill the same template for each with the stated intent, the diff or file contents, the rubric from [references/rubric.md](references/rubric.md), and the code quality lens from [references/code-quality-lens.md](references/code-quality-lens.md). Pick each reviewer's effort for the job. Raise it one step for subtle concurrency or security code.

## Step 4. Synthesize

As results come back, build one picture. Parse every reviewer's findings. Merge findings that describe the same issue in different words, and note which models raised each one. A finding that two or more models raised independently is the strongest signal. Read a lone model's finding and weight it accordingly. Note disagreements. When one model flags something and another says the opposite, that is context for the verdict.

## Step 5. Lead judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Read [references/lead-judgment.md](references/lead-judgment.md) for the full framework. Put every finding in one of four buckets, with the models that raised it and a one-line reason.

- **Act on.** Real issues that affect correctness, security, or maintainability given the actual goals. They would block a real PR.
- **Consider.** Legitimate, but you are not sure they outweigh the cost of fixing them now. Worth the user's attention.
- **Noted.** Technically valid but not actionable. Context-dependent, premature optimization, or low impact at this stage.
- **Dismissed.** Wrong, nitpicky, or missing context, with a brief reason.

Before a finding lands in Act on, verify it yourself. Trace the call path or run it. A finding you cannot make concrete moves down a bucket.

## Output format

```
### Intent
> [The intent paragraph from step 2]

### Reviewers
- Reviewer [label]: [model], [N findings]

### Act on
[Each: the issue, which models raised it, why it matters.]

### Consider
[Each: the issue, which models raised it, the tradeoff.]

### Noted
[A brief list.]

### Dismissed
[Each with a brief reason.]

### Agreement map
[Where the models agreed and where they split, and what that pattern says.]
```

Write the prose per `tea-time`.
