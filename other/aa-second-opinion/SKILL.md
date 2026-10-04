---
name: aa-second-opinion
description: Use when the user wants a second opinion, external code review, or sanity check on recent code changes — even when phrased casually ("another set of eyes", "what would a reviewer say", "review only, don't change anything", "gut check this", "is this any good"). Sends the diff to the Oracle (a second AI) in review mode, then shares your own contrasting assessment. Read-only — does not edit code.
disable-model-invocation: true
---

# Second Opinion

Get an independent code review from the Oracle, then layer your own perspective on top. The point is to give the user _two_ viewpoints they can triangulate from — not a single rubber-stamped answer.

## Workflow

1. **Surface the changes.** Run `git op=status` to see what's in scope. If the user already named specific files, narrow to those; otherwise default to all uncommitted/staged changes.

2. **Publish diff artifacts.** Call `git op=diff artifacts=true` (mode `standard` is fine). This step is load-bearing — `ask_oracle` in review mode reads from these artifacts; without them, the Oracle reviews file _contents_ without seeing what actually changed, which silently produces a useless review. Skipping this is the most common way this skill fails invisibly.

3. **Curate selection if needed.** Use `manage_selection` to add any extra files the Oracle should see for context (callers of changed functions, related tests, the spec being implemented). Skip this if the diff is self-contained.

4. **Request the review.** Call `ask_oracle` with `mode="review"`, instructing the Oracle to review per `references/review-rubric.md` — include the rubric's key rules inline in the message (canonical-path doctrine, Verified vs. Suspected confidence with "Suspected cannot block", and the volume calibration: fewer Verified findings beat exhaustive lists; a clean review with zero manufactured findings is a valid outcome). Pass through any specific concerns the user voiced ("I'm worried about the error handling in X", "does the new caching strategy hold up?") so the Oracle can focus there.

   **Repeat review?** If a prior review of this same change was already triaged (e.g. via `apply-review`), include that triage ledger — each finding with its verdict and one-line reason — and instruct: "Verify the recorded corrections; do not reopen an adjudicated finding without new source evidence." This is what stops the endless re-review spiral of freshly manufactured blockers.

5. **Layer your own take — explicitly contrasting.** After the Oracle responds, share both:
   - A short summary of what the Oracle flagged (don't just dump its full response).
   - **Your own assessment, framed against the Oracle's** — where you agree, where you'd push back, anything you think it missed or overweighted. The user is here for triangulation, not a paraphrase. If you fully agree, say so plainly and briefly.

6. **Do not edit code.** This skill is read-only. Even if the review surfaces clear issues, do not modify anything. Wait for the user to explicitly say "go fix it" (or similar). The reason: the user invoked this skill specifically to _reflect before acting_ — jumping straight to edits collapses two decisions into one and removes their judgment from the loop. Respecting that pause is the whole value proposition.
