---
name: compound
description: "Primary pipeline knowledge-capture step that closes the compounding loop. Capture a durable lesson in docs/solutions/ onto the open PR before /closeout merges (the default), or post-merge when the lesson only surfaces during/after merge. Use so future /research and /write-a-prd runs improve. Not for trivial edits with no reusable project-level learning, and not for the merge/teardown itself (that's /closeout)."
sources:
  primary:
    - "Living Documentation — Cyrille Martraire"
  secondary:
    - "Thinking in Systems — Donella Meadows"
    - "Software Estimation — Steve McConnell"
    - "Thinking in Bets — Annie Duke"
    - "The Fifth Discipline — Peter Senge"
    - "The Checklist Manifesto — Atul Gawande"
---

# Compound

Document a recently solved problem or shipped feature to compound your project's knowledge. Each documented solution makes future planning and implementation faster — the agent consults `docs/solutions/` during `/research` and `/write-a-prd`, so lessons learned today prevent mistakes tomorrow.

When the work surfaced planning or estimation surprises, capture those too. McConnell-style calibration only happens if actual work feeds back into future shaping.

## Invocation Position

This is a primary pipeline skill that closes the compounding loop. It runs near the tail of the default delivery path, after `/pre-merge` has created the PR.

**Default — capture the lesson in the PR, before merge.** When a durable lesson is already known at PR time, run `/compound` on the open PR branch so the `docs/solutions/` entry rides the same PR as the code that taught it — reviewed before the same merge and merged atomically with it. This places `/compound` between `/pre-merge` and `/closeout`, and returns through `/pre-merge` once:

```
… → /pre-merge → /compound (in-PR, when a lesson exists) → /pre-merge (re-run: the compound commit is the post-stamp delta; re-stamps) → /closeout (merge + teardown) → cleanup
```

The return leg is not decoration. Committing onto the branch moves the head past the stamp `/pre-merge` Phase 4 wrote, and `/pre-merge` is the stamp's only writer — so without the re-run the entry is merged with the code and read by nobody, which is the one thing the in-PR default was chosen to avoid. Phase 5 states the handoff; this is why it exists.

**Fallback — capture post-merge.** Some lessons only surface during or after the merge: integration surprises, QA findings, behavior seen once it ships. For those, run `/compound` after `/closeout` has merged. This is the fallback path, not the default.

Either way, `/compound` never performs the merge or worktree teardown itself — that is `/closeout` — and never writes the review-currency stamp, which is `/pre-merge`'s alone. Capturing in-PR means committing onto the open PR branch and handing back for the review that covers it; it does not mean merging.

Do not use it for trivial edits or for lessons that belong entirely in a higher-fidelity artifact like a test, linter rule, or code comment without any durable project-level learning. Whether in-PR or post-merge, the "When NOT to Use" guard below still applies — most PRs carry no durable lesson, and there is no standing per-PR `docs/solutions/` slot to fill.

## Why This Exists

Without this step, you've done traditional engineering with AI assistance. The first three steps of the workflow (plan, work, review) produce a feature. This fourth step produces a system that builds features better each time.

## When to Use

- When a feature's PR is ready and it taught a durable lesson — capture it onto the PR before merge (the happy path)
- After shipping, when a lesson only became clear during or after the merge (the post-merge fallback)
- After fixing a tricky bug where the root cause was non-obvious
- After a QA cycle revealed issues that could have been caught earlier
- After making an architectural decision with significant tradeoffs
- When you've discovered a pattern that should be reused

## When NOT to Use

- For trivial fixes (typo corrections, simple config changes)
- When the solution is already well-documented in official library docs
- When the lesson is project-specific but you're about to deprecate that code
- When the work was a clean execution of a pre-shaped plan — no surprises, no rework, no non-obvious decisions. The issue body and PR description already carry that record; a `docs/solutions/` entry with no reusable lesson trains future readers to skim
- When in doubt — skipping costs nothing because the issue and PR persist in GitHub. Capturing a low-value lesson costs future planners' attention every time they consult `docs/solutions/`

## Execution Flow

### Phase 1: Identify What to Capture

On the in-PR default path the work under review is the open PR branch, so the commands below read it directly — a `git log` and a `git diff` of the branch against the base it will merge into, while it is still unmerged. On the post-merge fallback path, run them in a session that can still see the merged feature's history — once `/closeout` has pruned the branch and pulled base, that diff is empty and you must read the PR diff via `gh pr diff <n>` instead. Either way, review the recent work.

Resolve the base first. Do not hardcode `main` — this repo itself uses `prod`, and a *name* is not a *ref*: in a worktree workflow nobody checks the base branch out, so the local branch is frozen at whenever the checkout was made while `origin/<base>` moves on. `/pre-merge`, `/help`, `/walk-commits` and `/visual-recap` carry this same block for the same reason.

```bash
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null | sed 's@^origin/@@')
if [ -z "$BASE_BRANCH" ]; then
  for candidate in main master prod develop trunk; do
    if git rev-parse --verify "$candidate" >/dev/null 2>&1; then BASE_BRANCH=$candidate; break; fi
  done
fi
# A name is not a ref. $BASE_BRANCH names the branch (for `--base`, `git switch`);
# $BASE_REF points at it, and is the only thing safe as a range endpoint.
if git rev-parse --verify "origin/$BASE_BRANCH" >/dev/null 2>&1; then
  BASE_REF="origin/$BASE_BRANCH"
else
  BASE_REF="$BASE_BRANCH"
  echo "note: origin/$BASE_BRANCH does not resolve — measuring against the local branch, which may be stale" >&2
fi
```

**Residual:** `$BASE_REF` is only as fresh as the last `git fetch`, and on a triangular fork (or a remote not named `origin`) `origin/$BASE_BRANCH` may be absent or track your fork rather than upstream — the `else` branch then falls back to the local branch, which is the stale-ref behavior this guard exists to avoid. It says so on stderr rather than falling back silently, because a plausible wrong answer with no signal is what let this defect live for five months. If the counts look wrong, `git fetch` and re-run, or set `BASE_REF` by hand.

Look at:

1. **Git log** — What commits were made? What changed?
   ```bash
   git log --oneline "$BASE_REF..HEAD"
   ```
   Base-relative, not `-20`: a fixed count reads the base's own history as "the work under review" on any branch shorter than it. Two-dot here is correct — these are the commits on this branch and not on the base. (The `git diff` below is three-dot for the mirror reason: it diffs from the merge base rather than subtracting base-side work.) On the post-merge fallback path the branch is gone, so use `gh pr diff <n>` as above.

2. **Issue thread** — What was the original problem? What was discussed?

3. **The diff** — What files changed? What patterns emerged?
   ```bash
   git diff --stat "$BASE_REF...HEAD"
   ```

Ask the user: "What was the most important thing you learned or the trickiest part of this feature?" Their answer often reveals the highest-value lesson to capture.

Before writing, classify the lesson at the right level:

- **Event** — a one-off incident or visible failure
- **Pattern** — something that has happened repeatedly across features, bugs, or handoffs
- **Structure** — a recurring condition in the codebase, workflow, incentives, or decision process that keeps producing the pattern

Prefer capturing the highest level you can support with evidence. If the lesson is structural, name the feedback loop, missing feedback, or delayed effect that made the outcome likely.

**Before proceeding, answer four questions:**

1. **Is this genuinely novel?** Check official library docs and existing `docs/solutions/` files. If the lesson is already well-documented elsewhere, skip it or link to the existing source.
2. **Will this still be accurate in 3 months?** If the lesson is tightly coupled to a dependency version or a temporary workaround, note that — it affects the `volatility` classification below.
3. **Could this be captured closer to the source?** A behavioral invariant is better as a test. A convention is better as a linter rule. A "why" explanation is better as a code comment co-located with the decision — bounded to the *current* why, the reason a reader needs to understand the code as it now stands. The incident that discovered it belongs in the commit message and the PR body, where a reader reconstructing history already looks; `/execute` Step 3 states that routing at the moment the comment is written, and this question is the retrospective check on it. If the lesson can be captured in a higher-fidelity artifact, do that instead of writing prose. This is about *carrying the lesson* — Phase 4's clustering check asks a different question, whether a mechanism should *catch the next instance*, and a recurrence can require one even though the lesson itself needed prose.
4. **Was the process fixed?** (Bug-fix compounds only.) Was the fix a correction (removed the defect) or a workaround (suppressed the failure)? Were structurally similar patterns elsewhere in the codebase found and addressed? What process change would prevent this defect class from entering the codebase again — a stronger test, a linter rule, an assertion, a planning checklist item, or a filed issue in `chrislacey89/skills` (see *Filing against the pack* below)? If the answer is "nothing," the mechanism that produced this defect is still active.

#### Filing against the pack — the fifth mechanism

**This subsection is not gated to bug fixes.** Q4 above is (its heading says so), but both Q4 and Phase 4's promote-to-mechanism rule cite the rules below, and Phase 4 is not bug-fix-gated. The incident this mechanism exists for was a *feature* compound. A procedure reachable only from the path its own incident did not take is the defect being fixed, one level down — so the rules are declared here, once, and both phases point at them.

**The fifth name is scoped by ownership, not by difficulty.** The first four are artifacts of *this* codebase; the fifth exists because some preventing changes are not — they are changes to a skill's prose, gate, handoff, or contract test in `chrislacey89/skills`, which no downstream artifact can carry at all. That, and only that, is when the fifth name qualifies. It does **not** qualify because the first four are hard, expensive, or unclear here: that is the compliance exit #257 deliberately left closed, and "I could not build one" still resolves the way it always did — by naming in the entry which of the four came closest and what blocked it.

##### Filing-owner gate (DO-CONFIRM — check before writing anything outbound)

**Filing moves words out of the repo you are standing in, into a public one.** That is a different act from every other mechanism in the list — a test, a linter rule, an assertion, and a checklist item all stay put. So before composing a body, confirm the current repo's owner is one you are permitted to file *from*:

```bash
git remote get-url origin | sed -E 's#(git@[^:]+:|https://[^/]+/)([^/]+)/.*#\2#'
```

Compare it against the allowlist below. **The allowlist is the whole gate — an owner that is not on it is not permitted, including an owner you do not recognize.** Do not invert this into "block the owners I know are work": a client org that was onboarded last week is on nobody's list yet, so a denylist admits exactly the repo with the least-known confidentiality posture. Fail closed on unknown.

<!-- filing-allowlist:start -->
```text
chrislacey89
```
<!-- filing-allowlist:end -->

The markers around that fence are load-bearing: this subsection contains several fenced blocks, so "the list is the code block below" is ambiguous to anything reading mechanically — a reader that guesses wrong extracts prose and every owner then fails the check. Match the markers, not the position.

Add an owner to that list only as a deliberate, reviewed edit — one line, offline, greppable. A public repo you contribute to qualifies once you name it; it does **not** qualify merely for being public. Visibility is a mutable remote property, a public fork can front a private parent, and — the reason that matters here — *what gets filed is a narrative about the work, not the repo's code*. Public source and a confidential engagement around it is an ordinary combination, and "we hit this while building X for Y" leaks the relationship even when every line is world-readable.

**When the owner is not on the allowlist, the fifth name is unavailable.** Fall back to the behavior that predates this mechanism: record the prescription in the entry's Prevention → Process-level slot, recommend `/improve-pipeline`, and let a human carry it across. The lesson is not lost; it just does not travel automatically.

##### Composing and filing

When both the ownership guard and the filing-owner gate pass, **filing is the mechanism, and `/compound` files it** — the prescription reaching this repo is the artifact, not a sentence recommending that someone carry it there. First check for overlap and comment on the existing issue rather than filing a new one; a new outbound channel into a backlog is only worth having if it does not fill with restatements.

```bash
gh issue list -R chrislacey89/skills --state all --search "<pipeline area> <failure-mode keywords>"
gh issue create -R chrislacey89/skills --title "[improve-pipeline] <pipeline area> — <prescription>" --body-file <file>
```

`--title` and `--body*` are required, not stylistic: `gh issue create` with neither errors out under any non-interactive runner, which is every AFK path this mechanism is meant to survive.

**Write the body anonymized, and treat that as part of the contract rather than good manners.** The gate above decides *whether* you may file; this decides *what crosses*. Describe the incident's shape, not its subject:

- **Name** the pack file the change targets, the pipeline step that missed it, and what it should have done instead.
- **Do not name** the downstream repo, its owner, its client, its paths, its identifiers, or its issue and PR numbers. Characterize it — *"a downstream TypeScript web/page-analysis repo"* — the way #266 did, which is the worked example: it opens `Triggering repo: anonymized` and records that the source was *deliberately stripped of identifiers*.
- **Do not cite this entry's path as the evidence.** A `docs/solutions/…` path is a filename from a repo the reader may have no access to, so it proves nothing to them and identifies the work to everyone else. Carry the reasoning across instead; the entry stays home.

The pack file and the failure shape are what make a proposal actionable here. Everything the anonymization rule strips is detail that was only ever legible in the repo it came from.

Keep it short. This is a proposal stub, not a worked proposal — `/improve-pipeline` is what develops one, and the `/improve-pipeline` recommendation later in this phase still stands: recommend it, do not invoke it. **Cite the issue number in the entry.** An uncited filing is prose again: the entry names `#N`, or the fifth name was not used.

**Rabbit Hole review.** If a PRD issue exists for this feature, read its Rabbit Holes section. For each one, check: did the pre-decided resolution hold, or did it need to be revised during implementation? Rabbit Holes that bit — required a different resolution than planned, or surfaced late despite being named — are high-value compound targets. Capture the risk pattern and the *actual* resolution in `docs/solutions/` so future `/write-a-prd` sessions surface them during the completeness scan. Rabbit Holes that held as planned are less valuable to document unless the risk pattern is likely to recur in unrelated features.

**Scope accuracy check.** Also check: did this feature reveal a *scope* lesson worth capturing?

- Were significant activities omitted from the original decomposition that had to be discovered during implementation?
- Did a specific type of work (auth integration, data migration, UI state management) consistently appear as unplanned scope additions?

If a scope pattern emerges (e.g., "auth changes in this codebase consistently require updating three additional systems"), capture it in the appropriate existing `docs/solutions/` category — `integration-issues/`, `patterns/`, etc. The lesson compounds: `/write-a-prd`'s omitted activities scan and `/prd-to-issues`'s scope completeness check both consult `docs/solutions/`, so a documented pattern directly improves the next feature's planning.

If the main lesson is not about the downstream project but about Skill Kit itself — for example unclear skill boundaries, missing handoff guidance, or weak process guardrails in `chrislacey89/skills` — recommend `/improve-pipeline` if that skill is present. Do not invoke it. `/compound` still captures project knowledge; `/improve-pipeline` is for improving Skill Kit.

**Calibration check.** Also ask:

- Which unknowns actually drove variance between the shaped work and the implemented work?
- Did the team confuse a target, estimate, or commitment at any point?
- Did the first tracer bullet materially tighten confidence or reveal hidden work?
- Are there concrete actuals from this feature that should become a baseline for similar future work?

You do not need formal project accounting. A few truthful lines about what actually widened or narrowed the work are enough to improve future planning.

### Phase 2: Classify the Problem

Determine the category for filing. Use the most specific category that fits:

| Category | When to Use |
|----------|-------------|
| `integration-issues` | External API, third-party service, library integration |
| `architecture-decisions` | Structural choices with significant tradeoffs |
| `performance-issues` | Optimization, N+1 queries, caching strategies |
| `runtime-errors` | Bugs that were hard to diagnose |
| `logic-errors` | Business logic that was subtly wrong |
| `testing-patterns` | Testing approaches that worked well (or didn't) |
| `ui-patterns` | Frontend patterns, component architecture |
| `devops` | Build, deploy, CI/CD, environment issues |
| `security-issues` | Auth, permissions, data handling |
| `patterns` | Reusable patterns that emerged from implementation |

### Phase 3: Write the Solution Document

Create the document in `docs/solutions/<category>/`. Use the template below.

**Before writing the Root Cause section**, apply two tests. First: was the outcome a predictable consequence of the decision, or did it depend on conditions that weren't available to reason about at decision time? If unpredictable from the decision, the lesson belongs in Context (what you now know about the environment), not Prevention (what to do differently next time). Second: under what conditions would this lesson mislead a future agent? If you can't name a condition that would make the lesson wrong, tighten it until it's falsifiable or drop it. For Pattern and Structure lessons, record the answer in the Rule Scope section of the template so future `/research` consumers can pattern-match their own work's shape against the preconditions without re-deriving them from prose.

**Ensure the directory exists:**
```bash
mkdir -p docs/solutions/<category>
```

**Filename convention:** `<kebab-case-problem-slug>-<YYYY-MM-DD>.md`

Example: `docs/solutions/integration-issues/ably-presence-channel-auth-2026-03-28.md`

```markdown
---
date: YYYY-MM-DD
category: <category>
problem_type: <specific type within category>
components: [list, of, affected, components]
technologies: [list, of, relevant, technologies]
severity: low | medium | high | critical
volatility: evergreen | stable | volatile
---

# [Problem Title]

## Problem

[1-2 sentence description of the issue. Be specific enough that someone searching for this problem would find it.]

## Context

[What were you building when this came up? What was the expected behavior vs actual behavior?]

## Symptoms

[Observable symptoms that would help someone recognize they're hitting the same issue.]

- [Symptom 1 — error message, behavior, timing]
- [Symptom 2]

## Root Cause

[Why this happened. Be precise — not "the API was wrong" but "Ably's presence channel requires explicit auth via a server-side token request endpoint, not client-side API key auth."]

## Learning Level

- **Level:** Event / Pattern / Structure
- **Feedback loop or delay:** [If applicable, what reinforcing loop, balancing loop, missing feedback, or delayed effect made this likely?]

## Rule Scope

*Required for Pattern and Structure lessons. Optional for Event lessons — include only when the event's Solution embeds a transferable rule.*

[State the structural conditions under which the Solution's recommendation is correct, so a future `/research` consumer can pattern-match against their own work's shape without re-deriving the preconditions from prose. Be specific about shape, not just keywords — a 2-step agent loop with a terminal forced tool is a different shape from a 3-step loop where the same tool is non-terminal, even though both mention the same tool name. Note where the rule inverts if the conditions differ, and cross-reference sibling docs that cover the inverted or adjacent shape.]

- **Applies when:** [Structural preconditions — e.g., "the forced tool is terminal in the agent loop", "the callback replaces rather than merges the collection", "the component is a client component rendered inside an RSC boundary"]
- **Inverts or does not apply when:** [The shapes where following this recommendation would produce the opposite of the intended outcome, or simply not help — e.g., "for N+1-step loops where the tool is non-terminal, the `stopWhen` list must exclude it; see `<sibling-doc>`"]
- **Sibling docs:** [Links to `docs/solutions/` entries covering adjacent or inverted shapes, if any exist]

[Diagram suggestion: if Rule Scope describes conditional applicability with ≥3 distinguishable branches (multiple Applies-when shapes, or several Inverts-or-does-not-apply shapes that diverge in different directions), consider invoking `/mermaid` for a decision diagram showing which conditions route to which recommendation. Skip when the rule is binary (one Applies-when, one Inverts-when) — prose is already the cleanest rendering at that size.]

## Solution

[The actual fix. Include before/after code when it helps.]

**Before:**
```typescript
// What didn't work and why
```

**After:**
```typescript
// What works and why
```

## Prevention

[How to avoid this in the future. Separate code-level and process-level strategies.]

**Code-level:** [Tests, assertions, checks, linter rules that would catch this defect or its siblings.]

**Process-level:** [Pipeline step changes — e.g., "add auth token refresh to /write-a-prd's omitted activities scan" or "this defect class is a specification error; invest more in /shape for this domain."]

## Planning / Calibration Notes

[Include when the lesson should change future shaping, decomposition, or commitment language.]

- **What widened the work:** [Unknowns, omitted activities, or integration surprises]
- **What tightened the work:** [Tracer bullet, research answer, reused pattern, or existing baseline]
- **Future planning adjustment:** [What `/research`, `/write-a-prd`, or `/prd-to-issues` should do differently next time]

## Actuals Worth Reusing

[Include when this feature produced a reusable baseline for future work. Keep it lightweight and qualitative if hard numbers are unavailable.]

- **Comparable future work:** [What kind of feature this should inform]
- **Reusable baseline:** [Size, effort shape, scope pattern, or dependency pattern to remember]

## Defect Classification (bug-fix compounds only)

**Origin phase:** Specification error / Design error / Coding error
**Fix type:** Correction (addresses root cause) / Workaround (suppresses symptom — note what the real fix would require)

## Key Decision

[If an architectural or library choice was made, document it here.]

**Decision:** [What was chosen]
**Rationale:** [Why]
**Alternatives considered:** [What else was evaluated]
**Revisable:** [Yes/No — and under what conditions]

## Related

- [Link to GitHub issue or PR if applicable]
- [Link to related docs/solutions/ files if they exist]
- [Link to the research spike issue when one exists for this feature — `Refs #<spike-issue-number>`. This preserves the causal chain from research → PRD → slices → PR → compound, citable from any machine. If the project uses archive-mode research instead, omit this link — archive paths are openable only by the originating user, so they add no value to a `docs/solutions/` entry that may be read by others.]

## Shelf Life

[What change would make this solution unnecessary? E.g., "When Ably SDK v3 ships built-in auth" or "When we refactor the auth module per RFC #42". If this is an enduring principle, write "Evergreen — no expiration condition."]
```

**Adjust the template to fit the content.** Not every solution needs every section. A simple bug fix might just need Problem, Root Cause, Solution, and Prevention. An architectural decision might skip Symptoms and emphasize Key Decision. Don't pad sections that have nothing to say.

### Phase 4: Check for Overlaps

Before committing, search for existing solutions that might overlap:

```bash
grep -rl "relevant-keyword" docs/solutions/ 2>/dev/null
```

If a related solution already exists:
- **If it's the same problem solved again:** Update the existing file instead of creating a duplicate. Add new context, note if the solution changed.
- **If it's a related but distinct problem:** Create the new file and add cross-references in both documents.
- **If the existing solution is now outdated:** Update or supersede it. Never silently let stale solutions persist.

**Defect clustering check (DO-CONFIRM — verify before committing the entry).** Search for not just overlapping solutions but overlapping defect patterns. If `docs/solutions/` already holds an entry in the same `category` whose `problem_type` names the same underlying pattern, this one is the *second* recording of that pattern — prose was the deliverable the first time and the pattern recurred anyway. Match on both fields: `category` is one of the ten enumerated values in Phase 2's table, so it is the anchor you can actually grep; `problem_type` is free text a reader must judge, and matching on it alone finds nothing. For a worked pair, this repo's own `staleness-gate-intermediate-writers` (`problem_type: staleness gate invalidated by an unenumerated intermediate writer`) and `by-construction-claims-need-a-mechanism` (`problem_type: a claim asserted as holding "by construction" is maintained by hand in N files, with nothing constructing it`) share not one word. The second entry names them as the same pattern anyway — *"a limitation, a source gap, a stamped interval, or a verification that constrains nothing downstream is a footnote, not a mechanism"* — which is the judgment this check is asking you to make, and which no string match would ever reach.

This entry ships with a mechanism that would catch the next instance — one of the five Q4 names: a test, a linter rule, an assertion, a planning checklist item, or a filed issue in `chrislacey89/skills`. The fifth is available only under the ownership guard in Phase 1's *Filing against the pack* subsection — the preventing change belongs to the pipeline rather than to this codebase — and is not an exit for the first four being hard. That subsection carries the filing procedure too, and it is not bug-fix-gated; the enumeration is likewise borrowed from Q4 independently of Q4's own bug-fix flag, since this check is not gated to bug fixes. If none of the five can be built here, the entry states in one line which came closest and what blocked it. A third prose-only entry on the same pattern is not a valid outcome.

Record the judgment either way. Deciding that an existing entry names a *different* pattern is also an exit from this check, and it is the cheaper one — so it leaves a line too: name the nearest entry and say why it is not the same pattern. An escape that has to be written down is one a reader can argue with; an escape taken silently is the shape this whole check exists to close.

Name the pattern in the entry as well (e.g., "both auth integration bugs were specification errors — the PRD never addresses token refresh"). This feeds back into `/write-a-prd`'s omitted activities scan and `/shape`'s probing.

### Phase 5: Commit

**In-PR (the default):** commit the solution document onto the open PR branch and push, so the entry joins the PR. Committing does not review it — the hand-back below is what makes it reviewed and merged with the code that taught it:

```bash
git add docs/solutions/<category>/<filename>.md
git add <path/to/mechanism>   # Phase 4's mechanism — omit when Phase 4 did not fire, or recorded that none could be built
git commit -m "docs: compound — <brief description of what was learned>"
git push        # in-PR path: push so the entry joins the open PR for review
```

An entry claiming a mechanism, committed while that mechanism sits unstaged, is the unenforced-claim shape Phase 4 exists to close.

**Pack-level filing check (DO-CONFIRM — verify before committing the entry).** The fifth Q4 name has nothing to stage — it lives in another repo. Its equivalent of staging is that the issue is **already filed** and its number is cited in the entry before this commit. Committing an entry that says a pack-level issue will be filed is the same unenforced claim with a longer fuse, so confirm the issue exists rather than asserting it:

```bash
gh issue view -R chrislacey89/skills <n> --json number,title,state
```

A non-zero exit means the entry cites an issue that is not there — do not commit it. This is weaker than a contract test and deliberately so: the citation lives in a downstream repo's `docs/solutions/` file, which this repo's CI cannot read, so there is nothing for a `scripts/test-*.sh` to assert against. What the suite *can* pin is that this command is still here, and `scripts/test-q4-mechanism-names.sh` does — the check runs where the claim is made, and the pin stops the check itself from being quietly dropped.

**Then hand to a `/pre-merge` re-run — that push just moved the head past the review stamp.** `/pre-merge` Phase 4 recorded the SHA its review actually covered, and the commit above lands after it. `/compound` cannot fix that itself: `/pre-merge` is the stamp's only writer — pinned by `scripts/test-review-currency-marker.sh` — and a skill that stamped its own commit would certify as reviewed the one commit nothing independent read. So the in-PR path's terminal step is a review, not a merge.

Hand to `/pre-merge` in author-mode. It reads the stamp off the PR, takes the post-stamp delta — this commit — as its subject, and re-stamps at the new head (its Phase 1 step 4). `/closeout` follows from `/pre-merge`'s own next-step menu; **the in-PR path never hands to `/closeout` directly.**

**Why this is not ceremony on the docs-only case.** The in-PR default exists so the entry is "reviewed and merged with the code that taught it" — Phase 5's own words. Skipping the re-run makes the second half of that true and the first half false, which is worse than the post-merge fallback, because the fallback at least does not claim the review. And the case is not reliably docs-only: this commit stages Phase 4's mechanism alongside the entry, and in the measurement behind #336 — four `docs: compound` commits across seventeen stamped merges — two carried code (a contract test rewritten to derive its coverage from the schema, and a new test file), both under a subject beginning `docs: compound`. The subject line is not evidence of what the commit contains, and the mechanism file is exactly the kind of guard `/compound` Phase 4 found vacuous when self-authored.

**The re-run terminates here; it does not bounce back.** Its subject is the entry that captured the lesson, so no *uncaptured* lesson can emerge from reading it — `/pre-merge` Phase 4's closing recommendation is conditioned on that and does not re-offer `/compound`. There is one re-run per in-PR capture, and its exit is `/closeout`.

**Post-merge (fallback):** the same commit lands on the base branch. If the repo requires review for the base branch, open a small PR for the doc rather than pushing it unreviewed — the whole point of the in-PR default is to keep `docs/solutions/` entries reviewed, so don't bypass that on the fallback path.

### Phase 6: Report

Tell the user what was captured, then print the closing block that matches the path you took.

**In-PR path (default)** — the lesson now rides the open PR, one commit past the stamp `/pre-merge` Phase 4 wrote. Hand off to the re-run that reviews it and moves the stamp; `/closeout` merges after that, from `/pre-merge`'s menu:

```
Compounded onto PR #<n>: docs/solutions/<category>/<filename>.md
Mechanism: <path/to/mechanism>   [or: chrislacey89/skills#<n> — pack-level, filed] [or: none possible — <the one-line reason from the entry>] [or: n/a — Phase 4 did not fire]

Key lesson: [One sentence summary of the most important takeaway]

This rides the PR and will be consulted automatically during future /research and /write-a-prd sessions. It is not yet reviewed: it landed after the stamp, so the re-run below is what makes "reviewed and merged with the code that taught it" true rather than asserted.

**Next session:** /pre-merge
**Input:** PR #<n> — the post-stamp delta is this compound commit; review it and re-stamp, then /closeout
```

**Post-merge path (fallback)** — the work already shipped; this is the end of the loop:

```
Compounded: docs/solutions/<category>/<filename>.md
Mechanism: <path/to/mechanism>   [or: chrislacey89/skills#<n> — pack-level, filed] [or: none possible — <the one-line reason from the entry>] [or: n/a — Phase 4 did not fire]

Key lesson: [One sentence summary of the most important takeaway]

This will be consulted automatically during future /research and /write-a-prd sessions.

**Loop closed.** Next: /help when you return to this repo.
```

On the in-PR path two steps still follow — `/pre-merge` re-reads the delta and re-stamps, then `/closeout` performs the merge — so `/compound` hands to the first of them with a `**Next session:**` line. On the post-merge path `/compound` is the end of the loop, so it prints the loop-closed line instead. `/help` is only a suggested re-entry point; the user may also re-enter via `/shape`, `/qa`, or any other appropriate skill.

## Maintenance

The `docs/solutions/` directory needs periodic maintenance. Solutions go stale when:

- The library/service updates with breaking changes
- You refactor away from the documented approach
- The codebase evolves past the documented pattern
- The context that made the solution correct changes, so the old advice would now mislead future work

When you notice a stale solution during research or planning, either update it or delete it. Stale solutions are worse than no solutions — they actively mislead the agent.

Use the `volatility` field to drive review cadence instead of a blanket schedule:

- **`volatile`** (dependency/API-specific) — review when those dependencies change, or at most every 90 days
- **`stable`** (architectural patterns) — review quarterly
- **`evergreen`** (fundamental principles) — review annually

During review, check each document's **Shelf Life** section. If the expiration condition has been met, delete the document. If the document describes a workaround for a design problem that has since been fixed, delete it — stale workarounds are worse than no documentation.

## Handoff

- **Expected input:** a durable lesson worth reusing — known at PR time (the in-PR default) or surfacing during/after merge (the post-merge fallback), plus solved bugs or meaningful lessons from implementation, QA, or review
- **Produces:** durable `docs/solutions/` knowledge that feeds future `/research` and `/write-a-prd` sessions — riding the PR on the in-PR path, committed to base (or a small doc PR) on the post-merge path
- **Comes after:** `/pre-merge` on the in-PR default path (capture onto the PR branch, hand back for a re-run that reviews the new commit and re-stamps, then `/closeout` merges code + lesson together); `/closeout` on the post-merge fallback path. `/compound` captures the lesson — it never merges, and it never writes the review-currency stamp
- **Closes the loop on:** `/pre-merge`, `/closeout`, and shipped implementation work
- **What comes next:** in-PR, a `/pre-merge` re-run in author-mode reviews the compound commit as the post-stamp delta and re-stamps, then `/closeout` merges the PR carrying the lesson; post-merge, the loop is closed. Either way, future features consult the compounded knowledge during discovery, research, and shaping
