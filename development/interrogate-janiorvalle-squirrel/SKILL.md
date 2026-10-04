---
name: interrogate
description: "Use for \"interrogate this\", \"tear this apart\", \"find the blind spots\", or a contested design before it ships. Sends the same diff and rubric to one reviewer per model, merges findings by consensus, then you as lead sort them into act on, consider, noted, dismissed. Never auto-applies. Roast is the required gate. This is the deeper optional pass."
disable-model-invocation: true
---

# Interrogate

One reviewer per model, same prompt, same rubric. The signal comes from model diversity, not from assigned personas, because different models have different blind spots. Two models flagging the same thing independently is strong. One model alone is worth reading, weighted lower.

The deliverable is a verdict. Do not auto-apply anything.

## Step 1. Scope

What to review, from context. Files or a diff the human pointed at. The full changeset against the base branch if you're on a feature branch. Recent work if the human's message refers to it. Package the diff plus whatever surrounding files a reviewer needs to understand it.

## Step 2. State the intent

One paragraph. What is this code trying to do? Take it from the human's message, commit messages, the PR description, the code. Reviewers challenge whether the work achieves the intent well, not whether the intent is right. If you're not sure what the intent is, ask before spawning anyone.

## Step 3. Spawn reviewers

All at once, one per model, read-only. Different model families where you can. Each gets `references/reviewer-prompt.md` filled in with the intent, the diff, and `references/rubric.md`. Same brief to everyone.

## Step 4. Merge

As results come back:

1. Parse all findings.
2. Findings raised by two or more models independently go to the top.
3. Lone findings stay, weighted lower.
4. Deduplicate. Different models describe the same issue differently. Merge and note who raised it.
5. Note disagreements. One model flags X, another says X is fine. That's useful for the verdict.

## Step 5. Lead judgment

You're the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. `references/lead-judgment.md` has the full framework. Reviewers saw a slice and a paragraph. You have the whole conversation, the constraints, what was already tried, what the next PR handles. Use that.

Sort every finding:

- **Act on.** Real. Correctness, security, or maintainability given the actual goals. Would block a real PR.
- **Consider.** Legitimate, but unclear whether it's worth the cost right now. Worth the human's attention.
- **Noted.** Valid but not actionable. Context-dependent, premature, low impact at this stage.
- **Dismissed.** Wrong, nitpicky, or missing context. Say why in a line.

Each finding carries which models raised it, its bucket, and a one-line reason.

## Output

**Intent.** The paragraph from step 2.

**Act on.** Each with location, the finding, who raised it, the reason. More than five means you aren't filtering hard enough.

**Consider.** Same shape.

**Noted.** One line each.

**Dismissed.** One line each with why. This is how the human checks your judgment. Don't hide it.

**Verdict.** Two or three sentences. Ship it, fix the act-on list first, or rethink.

## Where this sits

Roast is the required gate before anything ships. It runs on one engine that didn't write the code, loops until clean, and stays inside a scope fence. Interrogate is the optional deeper pass for a contested design, a change you don't trust, or a sketch from architect before building. Run it when the stakes earn it, not on every PR.
