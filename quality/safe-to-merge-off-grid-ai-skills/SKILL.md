---
name: safe-to-merge
description: Take a pull request from "the diff exists" to "ready to merge" and keep it there. Your agent audits its diff, gathers every review signal, answers each comment, fixes behind the checks and re-reviews until nothing blocks. Use when you say "review this PR", "get this PR merge-ready", "/safe-to-merge", "address the review comments", or after pushing to a PR with open comments.
---

# Get PRs merge-ready

A pull request is not done when the code is written. It is done when it is **verified and clean under review**. This skill is the loop that gets it there and keeps it there. It is iterative on purpose: review, triage, fix behind the gates, push, re-review, until the exit criteria hold. Then it feeds what it learned back into the standard.

The rubric for "good" is the **`code-check`** skill. This loop does not re-derive quality; it applies that skill's AUDIT mode to a live PR and manages the round trip with reviewers.

**First, find the repo and the PR.** `gh pr view --json number,headRefName,baseRefName,title,url` (or your git host's CLI). If several PRs are open, confirm which one. Note which repo and stack it is: the gates and tokens differ per repo (`code-check`, Mechanical gates).

**Posting is outward-facing.** Replying to a reviewer, pushing commits and merging are visible to others. Draft first. Post replies and push freely on the PR's own branch (that is the loop), but never merge without an explicit go from the user, and never push to the main branch.

---

## The loop

### Phase 1: Self-audit (before you read anyone else's comments)

Run **`code-check` in AUDIT mode** against `git diff <base>...HEAD`. Produce the per-dimension PASS / FAIL / N/A verdict with evidence (run the mechanical gates, paste the output). Fix your own blocking issues *before* inviting review: a reviewer's time is not your linter. Record the AUDIT verdict; it is half of the exit criteria.

### Phase 2: Gather every review signal

Collect all of them; do not cherry-pick:

- **Automated reviewers:** whatever the repo uses. Common ones: AI review bots (Gemini Code Assist, CodeRabbit, Copilot review; trigger them the way the repo does, for example a `/gemini review` comment), coverage (Codecov, Coveralls: coverage change and patch coverage), static analysis (SonarCloud, CodeQL: new issues, quality gate, security hotspots). CI status: `gh pr checks`.
- **Human comments:** `gh pr view <n> --comments`, and review threads via `gh api repos/{owner}/{repo}/pulls/{n}/comments` (inline) and `.../reviews`.

List every open, unresolved comment in one place. That list is the work.

### Phase 3: Triage each comment (one verdict per comment, no silent skips)

For every comment, choose exactly one, with a one-line reason:

- **ACCEPT, then fix:** valid; fix it in this PR (most CI findings).
- **REJECT, then reply:** not valid or not applicable; reply with the specific reason. A false positive from a bot still gets a polite, concrete answer so the thread resolves.
- **DEFER, as a gap:** real but outside this PR's one concern. Log it in the project's backlog (an issue, or `docs/GAPS_BACKLOG.md` if the repo keeps one) with a link, and reply saying so. One concern per PR; gaps are surfaced, never hidden.

**Reply to each comment on its own thread.** Reviewers and threads resolve one by one, never with one blanket comment. A bot comment you fixed gets a short "fixed in <sha>".

Watch for the trap: a bot flags a symptom, and the real defect is a standard broken underneath (a caller branching on a concrete type, a duplicated constant, a mock asserting itself). Fix the seam (`code-check`: Separation of concerns, SOLID), not the symptom the bot happened to see.

### Phase 4: Fix behind the mechanical gates

Make the accepted fixes on the PR branch. Every fix clears the repo's mechanical gates before it is pushed: formatter, linter, type check, the fix's own tests, coverage against the repo's bar, and a production build if native code, dependencies, config or imports changed. New behaviour ships with a test that proves it (`code-check`: Testing). Never skip hooks (`--no-verify`). Never bundle a repo-wide reformat: format only the lines you touched. A whole-file reformat that trips a size or complexity rule, or bloats the diff, is its own defect: revert it and re-apply minimally.

Commit per concern with a real message, and push. Reply "fixed in <sha>" on each thread you closed.

### Phase 5: Re-review (the loop)

After the push, CI runs again. Go back to **Phase 2**: pull the new signal, triage new and repeated comments, fix, push. Repeat until the exit criteria hold. Each pass should shrink the open list. If it grows, a fix brought a regression: treat it as a Phase 1 miss.

**Exit criteria (all must hold):**
1. `code-check` AUDIT: overall PASS, zero blocking issues.
2. Every review thread resolved (fixed, answered, or deferred with a link). None left open.
3. All CI checks green: no AI reviewer blocker left unaddressed, patch coverage meets the repo's bar, the static analysis gate passes, the build is clean.
4. Evidence attached to the PR: for UI changes, a screenshot per changed surface (read each one and confirm it matches the claim) and a video for any interaction; for every change, the pasted test output and the test that proves the new behaviour; on mobile, the journey run on a device.
5. Honesty check: what is NOT verified is named (not run on a device, not tested with two devices, native linking untested, a bug that could not be reproduced is "candidate, not confirmed"). No inflated "done".

State the exit verdict as one of three gates: **code / wired / verified**. Only "verified" is done. Merging waits for the user's explicit go, and follows the repo's merge style (ask if it is not written down).

### Phase 6: Distill (feed the standard)

The review just taught you something. Before closing out, run **`never-twice`** (`/never-twice`, or ask your agent to use never-twice) on this PR's review comments. The *generic* lessons sharpen `code-check`; the *specific* ones are discarded. A review whose lessons evaporate is re-learned the hard way on the next PR. This phase is not optional: it is how the loop compounds.

---

## Notes

- **Scope discipline.** If review surfaces a real but unrelated problem, it is a gap in the backlog, not scope creep. One concern per PR.
- **The author and the reviewer can be the same agent.** That does not lower the bar. Audit your own diff as a hostile stranger would; the point is to catch the thing you were sure was fine.
- **Green CI with a broken feature is a FAIL.** Checks passing does not mean the feature works; the integration test through the real seam is what proves it.
