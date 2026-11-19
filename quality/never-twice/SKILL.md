---
name: never-twice
description: Turn each pull request review into a sharper engineering standard, so the same mistake doesn't come back. Your agent keeps only the general lessons from a review, writes each into code-check with a signal a grep can catch, and logs its source. Use when you say "learn from this review", "/never-twice", "update the standard from these comments", or at the end of safe-to-merge.
---

# Learn from every review

The `code-check` skill is only as good as the mistakes it has learned to catch. Every review is a free lesson. This skill decides which lessons are worth keeping, and folds those, and only those, back into `code-check` so the next PR starts from a higher bar. The discipline is as much about what you REFUSE to add as what you add: a bloated standard is an ignored standard.

**Where the standard lives.** `code-check/SKILL.md` (its PLAN, AUDIT and Standards sections) and its provenance log `code-check/LEDGER.md`, wherever your agent installed the skill (for example `.claude/skills/`, `.agents/skills/`, or the project's own skills folder). If the team keeps its standard elsewhere (a `CONTRIBUTING.md`, an engineering handbook), fold lessons there instead and keep the same ledger beside it.

**Input.** The review comments for a PR: from `safe-to-merge` Phase 2, or `gh pr view <n> --comments` plus `gh api repos/{owner}/{repo}/pulls/{n}/comments`, or a set the user pastes. Include your own AUDIT findings and any bug that slipped past the test suite: a shipped regression is the highest-signal lesson there is ("why did the suite stay green?").

---

## Step 1: For each comment, classify GENERIC or SPECIFIC

Promote a lesson into the standard **only if all five hold**:

1. **Recurs.** It is a *class* of mistake, not this feature's domain bug. The test: *"Would this exact comment be valid on an unrelated PR, in another repo?"* If it only makes sense for this feature, it is SPECIFIC: discard.
2. **Maps to a section.** It sharpens an existing rule, tell or anti-pattern in one Standards section (Separation of concerns, Avoid local state, SOLID, SSOT / DRY, One seam across platforms, Testing, Design, Copy, Branch / PR / honesty, Mechanical gates), or it shows a genuinely missing section. Name the section.
3. **Detectable.** You can state it as a rule with a **tell**: a concrete signal a reviewer or a grep can catch next time (`kind ===`, a hardcoded hex color, `expect(x).toHaveBeenCalled()`, a duplicated constant). "Write better code" is not a tell: discard.
4. **Not already covered.** Search the current skill. If the rule is already there, do NOT duplicate it; at most tighten the existing wording. Most near-misses land here.
5. **Portable.** It belongs in the cross-repo standard. Repo-specific facts (a path, a command, a token name) go to that repo's agent instructions (`CLAUDE.md`, `AGENTS.md`, `.cursor/rules`, or the equivalent), not here. Anything a formatter or linter already enforces is not a lesson: it is a gate config (Mechanical gates).

**Discard (do not touch the skill) when:** it is a one-off domain bug; a style preference the formatter or linter owns; project-specific (it goes to the repo's agent instructions); already covered; or a nit with no general signal. Discarding is the common, correct outcome: most comments are SPECIFIC.

Output a short table: each comment, GENERIC or SPECIFIC, and for a generic one the target section and the tell.

## Step 2: Fold the GENERIC lessons in, minimally

For each GENERIC lesson:

- **Prefer sharpening an existing bullet** over adding a new one. Add the missing *tell* or *anti-pattern* to the rule that already exists. Add a new bullet only when no existing rule covers it. Add a new **section** only when a whole dimension is missing (rare; justify it).
- **Write in the skill's voice:** an imperative rule, the tell, and optionally the anti-pattern. Terse. Match the density of the text around it. No preamble, no hedging.
- **Keep it tight.** The bar for this skill is high signal, no bloat. If your addition makes a section longer without making it sharper, cut it back. One vivid tell beats three paragraphs.
- **One section per lesson.** If a comment spans two sections, split it.

## Step 3: Show the diff, apply, log

- Show the exact before and after edit to `code-check/SKILL.md` for each accepted lesson. Keep edits surgical (a tightened sentence, an added tell); never rewrite a section.
- Apply the edits.
- **Log provenance** in `code-check/LEDGER.md`, one line per accepted lesson:
  `YYYY-MM-DD · <repo> PR #<n> · <section> · <the one-line lesson>`.
  The ledger is the audit trail: it lets anyone see why a rule exists and revert a bad addition. Use absolute dates. Keep only the one-liner in the ledger; the content lives in the skill.
- Report: N comments reviewed, M generic (folded into which sections), N minus M specific (discarded, with why in one phrase). If M is 0, say so plainly. A review with no general lesson is normal and honest; do not invent one to justify an edit.

---

## Guardrails

- **The skill must not only grow.** When you add, look for a rule the new tell makes redundant, and merge them. Net size stays roughly flat; density rises.
- **Never weaken a rule to match a shipped mistake.** Lessons raise the bar, never lower it (as with coverage: raise, never lower).
- **A shipped regression changes the test class, not just the code.** If the lesson is "the suite stayed green while the feature broke", the edit is a sharper Testing tell about the missing corner or seam. Then search the codebase for tests of the same shape.
- **Don't over-fit to one loud reviewer.** One bot's style preference is not a standard. The "would it recur elsewhere?" test must pass on its own merits.
