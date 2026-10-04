---
name: ship-auto
description: Auto-ship pipeline — code review, PR, CI, Copilot, merge, deploy — without pausing for human checkpoints. Use in personal repos where the user has already approved the plan and the change isn't D-class (default-branch breaking change, public deploy of breaking change, external send, irreversible delete, force-push). Default ship skill when CLAUDE.md doesn't specify one.
---

# Ship Auto

Run end-to-end: code review → PR → CI → Copilot review → merge → deploy. **Do NOT pause** between phases unless something hits a D-class gate (see below) or a CI/review failure burns through the fix-forward retries. Don't narrate "Want me to commit / PR / merge / deploy?" — that's the friction this skill exists to eliminate.

## Pipeline

### 1. Code Review (parallel background agents)

Dispatch both as background agents simultaneously. **Give each the return contract in its prompt**: findings only — the diff, the review transcript and the tool output stay in the reviewer's context.

**Agent A — Claude review:**
- Review the full diff (`git diff <base-branch>...HEAD`) against the Review Criteria in `workflow-conventions.md`
- Check: goal completeness, simplicity, testing sufficiency, coupling/cohesion
- Return BLOCKING vs ADVISORY findings, each one a `file:line` plus a sentence. No diff hunks, no restatement of the code.

**Agent B — Codex review:**
- Run: `codex review --base <base-branch>`. **No `-c model=` override** — `~/.codex/config.toml` pins the model and carries its own re-check command. A slug pinned here goes stale silently and breaks every ship; `gpt-5.6` is already rejected on a ChatGPT account, and `gpt-5.4` is a generation behind.
- Return the findings in the same shape. Do not paste the codex output back.

**Agent C — Adversarial review (unproven; review after one ship):**
- The author lists the invariants the change claims to hold, one per line.
- Prompt: "For each invariant, find a concrete input, timing, or environment that breaks it. Off-path first: odd paths, backgrounding, a killed peer, stale on-disk state, a second thread. Report only cases traced to a wrong outcome: `file:line`, input, outcome."

Wait for all three. Merge findings. Fix BLOCKING issues. Re-run reviewers only if fixes were >10 lines.

Run this step on every review-fix batch too.

### 2. Definition of Done

If `.claude/definition-of-done.md` exists, verify each item:
- All tests pass
- New code has test coverage for key logic
- Self-reviewed diff — no bugs, security issues, scope creep
- No secrets or personal references in committed code
- Changes match the original request

Any item fails → stop, report what failed. Otherwise continue.

### 3. Create PR

```bash
git push -u origin <branch>
gh pr create --title "<concise title>" --body "$(cat <<'PREOF'
## Summary
- <what changed and why — 2-3 bullets>

## Definition of Done
- [x] All tests pass
- [x] New code has test coverage
- [x] Self-reviewed diff
- [x] No secrets
- [x] Matches request

## Test Plan
- [ ] <how to verify>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
PREOF
)"
```

Capture the PR URL.

### 4. Monitor CI (channel-driven)

If `watch_repo("auto")` hasn't been called for this repo, call it once. Then await `<channel source="github">` events for this PR:
- ✅ CI pass → step 5
- ❌ CI fail → read failure via one `gh pr checks <pr-url>` call, fix, push, await next event. After 3 fix attempts, escalate to the user and stop.

**Timeout fallback:** if no CI event after 30 min, fall back to one `gh pr checks` to confirm state. No checks configured → step 5.

### 5. Monitor Copilot Review (channel-driven)

Await 👀 review-requested events. Approved → step 6. Changes-requested → address comments, push, await one retry max.

**Timeout fallback:** no review event after 5 min → assume no Copilot configured, proceed.

### 6. Merge

`gh pr merge <pr-url> --squash --delete-branch`. Don't ask. Don't narrate. Don't list "auto-merge candidates" vs "require human review" — at this stage you've passed planning, implementation, two reviews, CI, and Copilot; the consent gate is *the next D-class boundary*, not an extra "should I merge?" pause.

### 7. Deploy (if applicable)

If the project has a deploy command (check `CLAUDE.md` or `package.json` scripts for `deploy`, `release`, etc.), trigger it. Channel-watch for the deploy completion event. Done.

## D-class — the only stops

Pause only on:
- Default-branch merge that introduces a **breaking change** (incompatible API, schema migration without backward compat, removal of public surface).
- Public deploy of a breaking change.
- External send (email, Slack, posted comment, social media).
- Irreversible delete (data, branch with unreviewed commits, account, billing resource).
- Force-push to a shared branch.

Everything else is reversible enough that "stop and ask" costs more than "do it and revert if needed".

## Principles

- **Don't ask, don't narrate.** Run the pipeline.
- **Channel events over polling.** GitHub events arrive as `<channel source="github">` notifications. Don't poll `gh pr checks` in a loop.
- **Fix forward.** When CI or Copilot finds issues, fix them. Escalate only after 3 failed attempts.
- **Batch notifications.** Report once when the pipeline completes or hits a real blocker — not "still pending" updates.
