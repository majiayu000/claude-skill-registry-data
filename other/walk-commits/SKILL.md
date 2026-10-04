---
name: walk-commits
description: "Side-route skill for an interactive, commit-by-commit comprehension walkthrough of a finished branch before merge. Use when the person about to merge didn't author the diff — or hasn't internalized it — and needs to understand each commit's intent, riskiest line, deliberate oddities, and what's absent by design, with per-commit sign-off. Not a defect finder (that's /pre-merge), not a behavioral check (that's /verify), not an acceptance-criteria checklist (that's /execute Step 5). Optional and never auto-invoked."
sources:
  primary:
    - "Code Reading: The Open Source Perspective — Diomidis Spinellis"
  secondary:
    - "Best Kept Secrets of Peer Code Review — Jason Cohen"
    - "Peer Review on Open-Source Software Projects — Peter C. Rigby"
  papers:
    - "Peer Review on Open-Source Software Projects — Peter C. Rigby"
---

# Walk Commits

Walk the person about to merge a branch through it commit by commit, so they actually understand what they are shipping. The output is *reviewer comprehension and a sign-off decision*, not a defect list. For each commit you narrate the author's intent (not a restatement of the diff), anchor the single riskiest line, surface the choices that look odd on purpose, name what is absent by design, and flag anything needing the merger's explicit sign-off — then let them step to the next commit.

This skill exists because the highest-leverage finding in Cohen's peer-review dataset is *author preparation*: an annotated change walked through by a prepared narrator correlates with near-zero defect variance. The pipeline produces that annotation nowhere else. `/pre-merge` finds defects across the whole diff; `/verify` runs the app; `/execute` Step 5 checks acceptance criteria. None of them narrate the change commit-by-commit for the human who clicks merge.

## Invocation Position

This is a **side-route skill**. It does not block merge and is never auto-invoked.

It reconnects to the main pipeline at the `/pre-merge` → merge boundary: run it when you want comprehension before approving, then proceed to merge (and `/compound` if a durable lesson emerged). `/pre-merge` Phase 4 *recommends* it (without invoking it) when the person merging did not author the diff or hasn't internalized it; `/execute` Step 5/6 names it as an option before `/pre-merge` from the author side.

Use `/walk-commits` when:

- You are about to merge a branch you did not write, or wrote long enough ago that you no longer hold it in your head.
- A reviewer needs to genuinely understand a change before approving it — not just confirm tests pass.
- You want the comprehension pass to be repeatable and consistent, rather than a prompt you retype every session.

Do not use `/walk-commits`:

- To find defects across the whole diff — that is `/pre-merge`'s adversarial, dimension-based review.
- To confirm the feature behaves correctly at runtime — that is `/verify`.
- To check acceptance criteria — that is `/execute` Step 5's checklist.
- To draft review comments on someone else's open PR — that is `/pre-merge --pr <n>` reviewer-mode.

The line that keeps this distinct from `/pre-merge`: **comprehension and sign-off, not defect-finding.** If you catch yourself enumerating bugs across files, you are running the wrong skill.

## The reading discipline (why this stays small)

Cohen and Rigby both cap effective review at roughly **100–300 LOC and 30–60 minutes** — past that, fatigue degrades comprehension and the walkthrough becomes the rubber-stamp it was meant to prevent. Spinellis supplies the epistemic reason: **minimal comprehension** — read selectively, with a goal, and stop when you understand *enough to sign off*, not when you have read every line. The walkthrough reads selectively per commit toward a goal; it never marches line-by-line through 800 lines.

**If the diff is oversize** (well past ~300 LOC of meaningful change, or many commits), do not power through in one sitting. Recommend chunking the walkthrough across sittings — by logical group of commits, or by subsystem — and say so explicitly before starting. A tired walkthrough is worse than no walkthrough.

## Process

### 1. Establish the range and give the overview first

Resolve the commit range to walk — the commits on this branch not yet on the base branch:

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
git log --oneline --no-merges "$BASE_REF..HEAD"
git diff --stat "$BASE_REF...HEAD"
```

Do not hardcode `main` — detect the base (this repo itself uses `prod`). If the range is empty or the base can't be resolved, ask the user which range to walk. The `git diff` is three-dot (diff from the merge base) while the `git log` stays two-dot (commits reachable from HEAD but not the base) — these are different operators for different questions, and swapping the diff to two-dot reports deletions for base-side work this branch never touched.

**Residual:** `$BASE_REF` is only as fresh as the last `git fetch`, and on a triangular fork (or a remote not named `origin`) `origin/$BASE_BRANCH` may be absent or track your fork rather than upstream — the `else` branch then falls back to the local branch, which is the stale-ref behavior this guard exists to avoid. It says so on stderr rather than falling back silently, because a plausible wrong answer with no signal is what let this defect live for five months. If the counts look wrong, `git fetch` and re-run, or set `BASE_REF` by hand.

Then present an **overview before the first commit** (Spinellis: *overview first*). It is short and does two jobs:

- **State the scale and apply the budget.** Total commits, total changed LOC, files touched. If it exceeds the 100–300 LOC / 30–60 min budget, recommend chunking now (see "The reading discipline" above).
- **Declare the reading mode** (Spinellis: *reading mode determines strategy*). Most branches are one of:
  - **Evolution** — adding or changing behavior. Strategy: find the exemplar commit, read backward from the call sites the diff touches, scope comprehension to interface contracts.
  - **Maintenance** — fixing a defect. Strategy: anchor on the symptom, trace manifestation → source, ignore unrelated paths.

  Naming the mode picks how each commit gets read. State which one this branch is and why.

### 2. Walk each commit

Loop over the commits **in order**. For the current commit, read it with `git show <hash>` and produce the per-commit card below. Keep it tight — no padding, no diff restatement.

Derive **intent** with Spinellis's *five-strategy function understanding*, cheapest-first — stop at the first source that suffices:

1. commit subject → 2. symbol name → 3. **the call sites the diff touches** → 4. the body → 5. tests / docs.

Read the body only when the name and call sites fail to explain the change. This makes "intent" a disciplined derivation, not a paraphrase of the hunk.

Pick the **single riskiest line** with Spinellis's *surface-signal scan* — a catalog for where to point:

- canonical-`for` deviation (`<=`, non-zero start) → likely off-by-one
- `[lower, upper)` half-open-range misread
- push/pop or **mutex acquire/release asymmetry on error paths**
- empty `catch` with no comment
- missing `static` / over-broad visibility
- `FALLTHROUGH` omission in a switch
- an unclassifiable pointer or `any`
- a high-churn file (many recent touches → fragile)
- a symbol **removed in one hunk and re-added — same name or renamed — elsewhere with a changed signature, return type, or lifecycle**: a function replaced by a structurally-evolved successor. The unified diff splits one evolving thing into a delete hunk and an add hunk and hides that callers now depend on a new contract; read the new shape against the old, not as two unrelated edits.

Anchor it as `file:line` so the user can click straight to it. **Detecting the replaced-symbol case:** when a commit shows a large deletion of a symbol and a large addition elsewhere, check whether they are the same logical unit (rename detection, `git log --follow`, or matching call sites) before treating them as independent edits — then carry the finding through the existing Riskiest-line / Looks-odd-on-purpose / Absent-by-design card lines (no new card line needed).

Surface **intentional-looking-odd choices** with Spinellis's *deviation = signal*: any departure from a canonical form demands an explicit "why." Either the author intended it (and the walkthrough states the reason) or it is a bug. The deleted `enabled=true` filter that turns out to be the *point* of the change lives here — it looks like an omission but is the intent.

Name **things absent by design** by classifying each apparent omission (Spinellis): **justified** (deliberate, explained), **careless** (a real gap), or **malicious** (hidden). Forcing the classification stops the merger from glossing over a missing test, a skipped error path, or an unhandled state.

Decide **sign-off items** against the *documentation trust hierarchy* (Spinellis): tests and assertions outrank revision logs, which outrank comments, which outrank prose. Verify stated intent against the **added test** — the most executable evidence — not the commit message. A commit whose claimed behavior has no test backing it is a 🟡 at best.

Mark each commit 🟢 / 🟡 / 🔴:

- 🟢 understood, intent verified against executable evidence, sign-off clear
- 🟡 understood but carries an open question, a thin test, or a deliberate oddity worth confirming
- 🔴 not yet understood, or the diff contradicts the stated intent — do not sign off

**The prose bar for the card.** Every field below is authored prose — the one layer the shared rendering core leaves to you. Hold it to **`references/writing-for-humans.md`**: the revision bar (strip clutter, cut the warm-up, Bar/Beach Test, active verbs, concrete nouns, short-not-shallow) and the *what counts vs. what doesn't* test. **Intent** in particular must carry the mental model the diff cannot show; a narrativized restatement of the hunk fails the test even when every word is accurate. Write for someone who has worked in this project for a couple of weeks: they know the language and the repo's shape, and they do not know this commit — so gloss a domain term the commit introduces on first use. The doc's *shape* is written for issue and PR bodies; what carries over is the bar and the mental-model test.

#### Per-commit card

```
### <short-hash> — <commit subject>   🟢|🟡|🔴
**Files:** <the files this commit touches>
**Intent:** <why this change exists, derived cheapest-first — not a diff restatement>
**Riskiest line:** `path/to/file.ts:NN` — <what to watch and why it is the riskiest>
**Looks odd on purpose:** <deliberate deviations and the reason — or "none">
**Absent by design:** <omissions, each classified justified / careless / malicious — or "none">
**Sign-off:** <what the merger must confirm; cite the test that backs the intent, or note its absence>
```

Omit a line when it genuinely has nothing (e.g. "Looks odd on purpose:" on a boring commit) — empty scaffolding is padding.

#### Optional: render the commit as a line-anchored callout

The card above is chat text by default, and for most commits that is the right altitude. But when a commit's riskiest line or deliberate oddity is hard to grasp *out of context* — a subtle change inside a long hunk, a multi-file commit whose pieces only make sense together — render that single commit as a focused, line-anchored callout using the shared **`references/visual-rendering-core.md`** rendering core (the same core `/visual-recap` authors against). The card's fields map straight onto the core's blocks: the **riskiest line** and **looks-odd-on-purpose** entries become `callout`s anchored to the real after-side lines of `git show <hash>`, and the **sign-off** becomes a `signoff-<short-hash>` unit.

When a *commit sweeps one root cause across four or more near-identical sites*, the block is the **per-unit series** (`references/visual-recap-design.md` §12): one real `<section>` per site rather than three-to-eight sampled ones, opened by the required all-units matrix. For a sweep the population is the finding — sample it and a deliberately exempt site reads exactly like an oversight — so the 3–8 budget bounds depth within a unit, never the number of units.

When a *choice* is what needs rendering rather than a change — three or more mutually exclusive options, each carrying three or more attributes, not orderable on one axis — the block is the **options-comparison** (`references/visual-recap-design.md` §11), and its threshold and its relationship to the `AskUserQuestion` menu live in `references/next-step-menu.md`. That block is forward-looking, so its grounding rule differs: each cell is cited with its source or visibly marked asserted (`references/visual-rendering-core.md` §1, *Forward-looking blocks*).

This is an enhancement, not a new default — keep it optional and keep the stepper:

- **Reach for it** only when the line genuinely reads better shown in its hunk than described in prose. A boring commit does not earn an HTML file (Norman, *featuritis*).
- **Grounding holds.** The callout's line numbers and hunk text are copied from `git show`, never retyped; you write only the note. Visual emphasis must not exceed the real change (the core's Lie Factor ≤ 1 rule).
- **Canonical token core, not the reviewed app's aesthetic (forcing function).** Confirm the rendered callout's `:root`/`[data-theme]` block is the canonical `references/visual-recap-design.md` §1 set — canonical variable names and values — not a palette, font stack, or chrome re-derived from the app under review. A review instrument stays visually independent of its subject (core §6).
- **Route answers through the copy-text button.** When a commit is rendered this way, the merger's sign-off and any per-callout response are captured by the core's **Copy feedback** button into the `recap-feedback v1` block (keyed by the stable `signoff-<short-hash>` / `c-<file-slug>-L<line>` ids) and pasted back — instead of, or alongside, the `AskUserQuestion` answer. Promote anything durable to a GitHub PR review comment.
- **Transient artifact.** The HTML is written to a gitignored `.context/` or `mktemp` path and deleted when the walkthrough ends — per the core's transient-artifact rule. What persists is the 🟢/🟡/🔴 sign-off, not the file.

The `AskUserQuestion` stepper below remains the spine of the walkthrough; the callout is a per-commit zoom you opt into, not a replacement for it.

### 3. Step the loop with AskUserQuestion

After each commit's card, advance the walkthrough with a single `AskUserQuestion` (one question per turn — never a menu of separate questions). Offer:

- **Next commit** — proceed to the following commit.
- **2–3 commit-specific deep-dives** — concrete, drawn from *this* commit (e.g. "Show the test that backs commit 3's claim," "Read the call sites of the renamed export," "Confirm the `"use server"` boundary with a `next build`").

When a commit is opaque, do **not** deep-recurse line by line. Take Spinellis's *breadth-first escape* and use **execution as a reading tool**: read the test as the spec, try another call site, or escalate to a `next build` / `/verify`. PR-level example: a migrated `"use server"` action with a new injectable `db` param was confirmed by a build, not by staring at the diff. Naming this as a legitimate reading move keeps comprehension moving instead of stalling.

### 4. Wrap up after the last commit

After the final commit, offer a wrap-up via `AskUserQuestion`:

- A one-screen summary: per-commit 🟢/🟡/🔴 roll-up and the open 🟡/🔴 items the merger still needs to resolve before merging.
- Whether to proceed to merge, or to pause on the unresolved items.

If any commit is still 🔴, say plainly that the branch is not yet understood well enough to sign off, and name what is unresolved. The skill's job is honest comprehension, not a green light.

## What This Skill is NOT

- **Not a defect review.** It does not sweep the whole diff for bugs across dimensions — `/pre-merge` does that and emits advisory findings.
- **Not a behavioral check.** It does not run the app — `/verify` does that.
- **Not an acceptance-criteria checklist.** That is `/execute` Step 5.
- **Not a mandatory stage.** It is optional, invoked only when wanted, and never auto-runs. If a future sample of PRs shows it is rarely invoked or only fires on diffs `/pre-merge` already covered, fold it back into `/pre-merge` as an optional phase.
- **Not a rubber stamp.** Clicking "Next commit" without absorbing each card defeats the point. The 🟢/🟡/🔴 sign-off and the test-backed intent check are the structural guards against that.

## Handoff

- **Expected input:** a finished branch ready to merge, plus the base branch to diff against. No upstream artifact is required, though a linked PRD or slice issue helps frame intent.
- **Produces:** reviewer comprehension and a per-commit sign-off (🟢/🟡/🔴) with the open items the merger must resolve — a decision, not a durable file. It does not create issues, post comments, or edit code.
- **Reconnects at:** the `/pre-merge` → merge boundary. Run it before approving; proceed to merge once commits are understood, then `/compound` if a durable lesson emerged.
- **What comes next:** the user merges (or pauses on unresolved 🔴/🟡 items). `/walk-commits` does not invoke anything.
