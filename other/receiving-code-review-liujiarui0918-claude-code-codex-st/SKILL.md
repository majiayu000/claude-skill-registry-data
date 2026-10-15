---
name: receiving-code-review
description: Use when receiving review feedback. Reason about each item — don't performatively agree.
---

# Receiving Code Review

Review feedback is signal, not commands. Treating every comment as a TODO produces compliant code that's still wrong. Treating every comment as an attack produces wars. The middle path: reason about each item.

## Iron Law

**For every comment: understand it, evaluate it, decide on it, then act.** No item gets a reflexive "ok, fixed."

## Red Flags

- Replying "good catch, fixed" to every single comment without thinking.
- Pushing changes within 30 seconds of receiving feedback.
- Making the change without understanding *why* the reviewer flagged it.
- Quietly making changes that go beyond what was asked, hoping no one notices.
- Arguing every point because you're tired and want to ship.

If you're nodding at every comment, you're not reviewing — you're submitting.

## The 4-Step Loop (per comment)

### 1. Understand

- Read the comment fully. Read the code it points at.
- If unclear what they mean, **ask**. Don't guess and "fix" something they didn't ask about.
- Identify the *underlying concern*: correctness? performance? readability? convention? taste?

### 2. Evaluate

- Is the concern valid? Often yes — reviewers spot things you missed.
- Sometimes no — they misread, missed context, or have a preference you disagree with.
- Weigh: severity (bug vs. style), cost (one-line vs. refactor), reviewer's certainty (do they say "must" or "consider"?).

### 3. Decide

Three valid outcomes:

- **Adopt** — they're right, make the change.
- **Push back** — disagree, explain why, keep the code.
- **Discuss** — partial agreement or alternative; propose and align before changing.

"Adopt every time" is not a strategy. It's giving up.

### 4. Act

- If adopting: make the change. Verify it ([[verification-before-completion]]). Reply with what you changed.
- If pushing back: reply with reasoning. Be specific: "this path is hot, allocating here costs N us per call." Not "I think it's fine."
- If discussing: propose options, ask for the reviewer's preference, then act on the agreed path.

## On Pushing Back Well

You can disagree. You should disagree when you're right. But:

- Lead with the reviewer's concern restated, so they know you heard it.
- Bring evidence (benchmark, test, link to convention, prior decision).
- Acknowledge the tradeoff — there is always one.
- If the reviewer maintains the objection after your reply, weight their judgment. They may know context you don't.

Pushing back is not winning. The goal is the best code, not your code.

## On Adopting Well

When you adopt:

- Make the *exact* change requested unless the request is ambiguous. Don't expand scope.
- If adopting reveals a deeper issue ("oh this whole function is wrong"), surface that in a comment — don't silently rewrite.
- Verify after the change. A "small fix" can break things.

## Anti-Patterns

| Pattern | Why it's bad |
|---|---|
| "Done" with no detail | Reviewer can't tell what you did |
| Force-push, no reply | Reviewer has to re-diff from scratch |
| Adopt + silently expand | Scope creep hidden in review thread |
| "I'll address that in a follow-up" (never filed) | The follow-up does not exist |
| Argue to exhaustion to keep your code | Wastes everyone's time, signals bad faith |

## MUST

- MUST reply to every substantive comment (adopted / pushed back / discussed).
- MUST verify after every code change made in response to review.
- MUST NOT make changes outside what was reviewed without flagging them.

## Cross-references

- [[requesting-code-review]] — the self-review you should have done before this.
- [[verification-before-completion]] — every accepted change is a new change, re-verify.
- [[root-cause-tracing]] — if a reviewer's comment exposes a deeper bug, trace it.
