---
name: factory-submit
description: Move the current branch's Linear issue to "In Review"
argument-hint: <issue-id> (optional — auto-detected from branch if omitted)
---

You're handing a ticket off to review. This command moves it to the team's "In Review" state in Linear. It does **not** push code, open a PR, or change git state — those are separate steps the user owns.

**Invocation input:** an optional issue identifier. If omitted, auto-detect it from the current branch name.

## What to do

1. **Read project configuration.** Prefer `.factory-kit/linear.json`; use legacy `.claude/linear.json` only as a migration fallback. If neither exists, stop and direct the user to setup-linear. Pull `teamKey` and `states.inReview` (default `"In Review"`).

2. **Resolve the issue ID.**
   - If invocation input is provided: normalize it (prepend `<teamKey>-` if numeric).
   - Otherwise: get the current branch with `git rev-parse --abbrev-ref HEAD`. Match against `(\d+)` and construct `<teamKey>-<num>` from the first numeric chunk after the team key (case-insensitive). Example: `nishu/non-45-setup-scaffold` → `NON-45`.
   - If no issue ID can be derived, **ask the user** for it. Don't guess.

3. **Confirm before mutating.**
   - Fetch the issue through the connected Linear integration and show: `<KEY-N> — title (current state: <state>)`.
   - Ask the user to confirm the move. If the current state is already `In Review`, say so and stop.

4. **Move the issue.** Use the Linear integration's issue-update capability with `id` and `state` set to the configured `inReview` value. If the integration requires a state UUID, list team statuses and resolve the configured name first.

5. **Post a handoff comment** *(optional but default-on)*. Before flipping state, draft a short comment in the `factory-voice.md` shape so the reviewer knows what they're looking at. Density matters — links into the decision graph (PR, related issues, prior comment threads) are what make the comment useful six months later.

   ```
   **Outcome:** <one sentence — what this branch does>
   **Why:** <the underlying constraint or principle>
   **Tradeoff:** <if any>
   **Refs:** <PR URL, related issue IDs, last commit SHA if no PR>
   ```

   Show the draft, ask for approval, then post it through the Linear integration's comment capability. Skip this step if the invocation input includes `--no-comment` or the issue already has a recent comment from this branch.

6. **Confirm completion.** Print `<KEY-N> moved to In Review.` That's it — no PR side effects.

## Style

Follow `factory-voice.md`. Single confirmation gate per side effect (comment, then state move). Don't narrate intermediate fetches. The handoff comment is the reviewer's entry point — make it parseable at standup speed. If state lookup fails or the team doesn't have an "In Review" state, surface the actual state names and ask which to use.
