---
name: orient
description: >-
  Orient a spec-driven jig/servo/shaper repository with a read-only, project-wide
  briefing: start from the `workflow.py orient` headline, then survey open pull
  requests and unmerged work, Proposed ADRs, DEFERRED triggers, refinement items,
  release plans, the inbox, and the bug board; render one readable headline,
  titled sections, one recommendation, and an
  owning-skill handoff. Use when the user invokes `/jig:orient` or explicitly asks
  for a whole-project session pickup, a return-after-time-away briefing, the overall
  project status or big picture, or what to pick up next across the repository. Do
  not use for mid-implementation questions about the current slice such as "what's
  next?" or "what's blocking this test?"; those continue current work rather than
  requesting a project-wide rescan. Also do not use for non-code projects; use
  `studio:project-desk`. Never write files or lifecycle state; scheduled jobs and
  dashboards may capture stdout.
---

> **`$JIG_ROOT`** — jig's runtime root (this plugin's own directory).
> Copilot exposes no plugin-root environment variable, so jig's `SessionStart`
> hook publishes the value into session context. In a fresh shell, resolve it
> with the locator:
> `JIG_ROOT="$(for f in "${COPILOT_HOME:-$HOME/.copilot}"/installed-plugins/*/*/.github/scripts/jig_root.py; do [ -f "$f" ] && python3 "$f" && break; done)"`

# Orient

**One job: tell the user where the project stands and what to do next, in a shape
they can actually read.**

The user runs `/jig:orient` (or asks to be oriented) — the calm manager's question,
*"where do things stand, and what should I pick up?"* Orient answers it by reading
the project's own truth (not guessing), and presenting it in **one fixed, scannable
layout**: a headline that tells the honest state, then a short stack of **titled
sections**, each a list of **titled bullets** — never a wall of inline prose with
items buried mid-sentence.

The substance is grounded; the **format is the point**. If the answer reads like a
paragraph with five things crammed into it, the skill has failed even if every fact is
right.

This is a **project-level rescan**, not a mid-flow nudge. A bare conversational
*"what's next?"* while actively implementing a slice is asking to continue that slice
— not to re-survey the whole project. Orient is for the deliberate "step back and take
stock" moment (an explicit `/jig:orient`, a session pickup, a "where are we overall").

---

## Start from the deterministic headline

Do not re-derive the project's lifecycle state by hand — jig already computes it.
Run the read-only command spec 088 added and use its line as your factual base:

```bash
python3 "$JIG_ROOT/skills/spec-workflow/workflow.py" orient --project-dir . --fetch
# → jig hint: <scaffold state> · active specs: <rollup> · focus: <slice needing attention>
#   …and, only when the checkout is ahead of its default branch:
#   · in flight: <n> commit(s) ahead of <base> on <branch>
#   …and, only when the --fetch check finds a problem:
#   · freshness: <n> commit(s) behind <base>   |   could not reach origin
```

Pass **`--fetch`**. Orient reads *local* boards, ADRs, and slice `STATUS` — all only as
current as your last fetch — so an interactive orientation must refresh against origin
first, or it will confidently narrate a stale picture (work already shipped on trunk
reported as still open). `--fetch` runs one bounded, fail-soft `git fetch` and adds a
`freshness:` segment when the checkout is **behind** origin, or when origin **could not
be reached** (offline: the local view is unverified, not confirmed fresh). This flag is
for the interactive path only — the SessionStart hook never passes it (spec 103's
git-freshness hook already fetches at time-zero), so the hot-path headline is unchanged.

That single `jig hint:` line — scaffold classification, active-spec rollup, and the
slice currently requiring lifecycle attention — is the **deterministic headline**.
Reusing it (rather than re-implementing a second lifecycle-focus algorithm) keeps
Orient's headline from drifting away from jig's own computed state. Orient's job is to
**layer judgment on top**: the ADRs, deferrals, release plans, refinement-todo, inbox,
and standalone bugs that the one-line command does not weigh, then recommend one thing.

**If the headline shows `freshness: … behind …`, treat every local artifact below as
possibly stale** — say so in the headline, and recommend integrating origin (or
re-running after a pull) before trusting the boards. A `could not reach origin` reading
means you could not verify freshness at all; report that honestly rather than implying
the state is current.

---

## The prime directive — formatting

These rules are non-negotiable. They are the reason this skill exists.

- **Every distinct item is its own bullet, led by a short bold title.**
  `- **Recents (002-07)** — the last fork of the quick-add split; needs a Home-row mockup first.`
  Never `favourites are done and recipes are done but recents still needs a design and also backup restore is parked and…`
- **Group bullets under `##` / `###` section headers.** The reader should be able to
  jump to "the deferred stuff" or "the one decision" by scanning headers alone.
- **No inline lists.** If you catch yourself writing "X, plus Y, and also Z" where X/Y/Z
  are separate pieces of work, stop and turn them into three bullets.
- **One line per item where possible.** Title — what it is — the blocker or trigger.
  Keep each bullet to roughly one sentence; detail goes in a sub-bullet only if it earns it.
- **Lead with the answer.** The headline and the obvious next step come first, before any
  exhaustive lists.
- **Omit empty sections.** Only render a section if it has real content. A project with no
  pending ADR simply has no "one decision" section — don't print an empty heading.

If you honor nothing else here, honor this section.

---

## What it reads (the survey)

Orient is **read-only reconnaissance**. The deterministic headline (above) already
gives you scaffold state, active-spec rollup, and current focus. Layer the judgment
survey on top.

**First, resolve the docs root — don't hardcode `docs/`.** Read `layout.docs_root` from
`<project>/scaffold.json` (the canonical resolver is `_common/project_layout.py`; the
default is `docs`, and a value of `.` collapses the docs layer so artifacts live at the
repo root). Call the resolved value `<docs_root>` and read everything below relative to
it — with `docs_root="."`, `<docs_root>/specs/` is simply `specs/`. Skipping this makes
Orient report "no spec-driven project" on a perfectly valid track-local repo.

Projects vary, so look for these, use what exists, don't assume they all exist:

- **Open pull requests — check these FIRST, and never skip them.** Run `gh pr list`
  and **read the body** of each open PR (`gh pr view <n>`): unattended workers —
  overnight, cron, servo loops — put their questions-for-the-owner in the PR
  description and nowhere else. For each, note what it asks for, whether it is stale
  against newer local commits, and whether its branch is already an ancestor of local
  work. If `gh` is unavailable, unauthenticated, or the repo has no remote, **say so in
  one line** rather than silently omitting the section — "could not check" and "nothing
  waiting" are different answers.
- **Spec status** — `<docs_root>/specs/<MNN-slug>/` slice files and the spec status board
  `<docs_root>/specs/README.md`. Read each slice's STATUS marker: `DRAFT`,
  `READY_FOR_REVIEW`, `READY_FOR_IMPLEMENTATION`, `IN_PROGRESS`, `REVIEWED`, `RECONCILED`,
  `DONE`, `DEFERRED`, `ABANDONED`. This is the spine of "what's shipped vs. open."
  (`workflow.py orient` already summarizes the active rollup — use it rather than
  recounting from scratch.)
- **Use-case progress** — only when `<docs_root>/product-vision.md` has a `## Use cases`
  section: run the read-only
  `python3 "$JIG_ROOT/skills/spec-workflow/workflow.py" progress --summary --project-dir .`
  and use its output for the briefing's Use-case progress section. It writes nothing,
  and it is a progress view, not a check that the work is on-goal. If it prints a
  one-line `skipped` or `no-op` note (no vision file, no section, or one not elicited
  yet), drop it and
  say nothing about use cases.
- **DEFERRED slices + their triggers** — a DEFERRED slice carries a *resolution trigger*
  ("revisit once X"). Check whether that trigger is now met — a met trigger is often the
  best "obvious next step."
- **Standalone bugs** — the canonical bug status board `<docs_root>/bugs/README.md` (and
  the `<docs_root>/bugs/<NNN-slug>.md` records it links). These are real defects tracked
  outside the spec lifecycle; surface any that are still open. Read this board — don't
  infer bugs from generic source comments.
- **ADRs** — `<docs_root>/decisions/adr-*.md`. Note any with `Status: Proposed` (awaiting
  the user's acceptance) — a pending ADR is usually "the one decision blocking the most."
  Accepted/Superseded ones are context, not action.
- **Refinement / deferred decisions** — servo's `.servo/refinement-todo.md` (or a
  `refinement-todo.md`), and jig's `<docs_root>/inbox.md`. These hold parked
  owner-decisions and polish follow-ups.
- **Release plans** — shaper's `<docs_root>/releases/*.md` and
  `<docs_root>/releases/README.md`. Tells you what's in-scope for the next release vs.
  deferred, and whether a milestone is at risk.
- **Recent work** — the last few commits and any IN_PROGRESS slice, to say honestly
  what just landed (and flag when the board may be stale vs. a very recent commit).
  `workflow.py orient` already reports **unmerged local work** in its `in flight:`
  segment when the checkout is ahead of its default branch; when you see it, name the
  branch. A status board only ever describes the default branch, so finished work
  parked on a branch is invisible to every artifact above.

If tests or a green-count are cheaply visible (a recent run, an oracle summary), cite the
number in the headline as a proof point — but **don't run long suites** just to decorate
the answer.

If there's **no spec-driven project here** (no `<docs_root>/specs/`, no jig/servo/shaper
artifacts), don't invent a status. Say plainly that nothing spec-driven was found, and
point at the right setup skill (`jig:scaffold-init` for a new code workflow), or — if this
looks like a non-code project — hand to **studio:project-desk**.

---

## The output shape (the fixed layout)

Render these sections **in this order**, including only the ones with content. Not every
project has every section — a freshly-shipped MVP may have only a headline, an obvious
next step, deferred bets, and a recommendation.

### 1. Headline — the honest state (always)

One to three sentences, seeded by the `workflow.py orient` line. What's the overall state?
Is there **required** work outstanding, or is "what's next" a **prioritization call**
among optional items? Be honest about both "we're further than you think" and "this is
quietly slipping." Cite a proof point if one is cheap (e.g. "252 tests green").

> *The MVP is fully shipped — slices 002-01 through 002-06 are DONE, plus 002-08 and 002-09
> just landed (252 tests green). There's no required work outstanding; "what's next" is a
> prioritization call among deferred items.*

### 2. The obvious next step (usually)

The single (occasionally two) most natural next thing. A titled bullet with: what it is,
why it follows now, and any dependency/blocker. This is your lead recommendation candidate.

### 3. Waiting on you — open PRs and unmerged work (when any exist)

Anything already finished and parked in front of the user. One titled bullet each: the
PR number and title, what it is asking them for, and whether it is still current. This
sits high in the layout on purpose — a PR awaiting review is work that is *done* and
blocked only on a human, which almost always outranks work not yet started.

Flag these three explicitly when true, because each one misleads differently:

- **Stale** — newer local commits already answer or supersede it ("PR #1 asks 5
  questions; 4 were decided today on `<branch>`, and the PR does not show it").
- **Unmerged branch, no PR** — finished work that no status board reflects, because a
  board only ever describes the default branch.
- **Superseded** — the PR's branch is an ancestor of newer local work, so it can be
  fast-forwarded rather than redone.

> _**PR #1 — night: ground the spec-002 timer drafts** — asks you 5 questions; 4 were
> answered today but the PR still shows them open. Clean fast-forward._

### 4. The one decision blocking the most (when one exists)

If a `Proposed` ADR or a parked owner-decision unblocks more than anything else, surface it
here, prominently, **before** the long lists. Say what it is, that it's awaiting *their*
call, and **what deciding it unblocks**. Only include this section when such a decision
genuinely exists. **Cross-check it against the open PRs first** — a question the user has
already been asked in a PR body is not a fresh decision to re-derive and re-frame, it is
an outstanding one to point at.

### 5. Use-case progress (when the use-case layer is adopted)

Copy the content of `workflow.py progress --summary` as bullets — not recounted, not
re-derived. It carries three things and no more: the done/known totals line; the use cases
with no done slice or no spec (id, goal, which of the two); and the Unanchored count with
its spec names. Keep any `… and N more` line. Add one line naming `workflow.py progress`
for the full per-use-case listing. Never reproduce the full tree and never state a
percentage. This is a progress view, not a verdict that the work is on-goal or drifting.

Omit this section, with no mention of use cases, whenever `--summary` prints a one-line
`skipped` or `no-op` note: no vision file, no `## Use cases` section in it, or one not
yet elicited.

### 6. Larger deferred bets / packs (when they exist)

The bigger parked items that need a **trigger or a decision** before they're actionable.
One titled bullet each: title — one-line what — the trigger or what's blocking it. Group
tightly; this is a menu, not an essay.

### 7. The DRAFT queue / ready to build (when specs are DRAFT)

Specs or slices sitting in DRAFT/READY awaiting a go-ahead. One bullet each with the spec
id and a one-line scope. Note if any is beta/release-blocking, and flag any board row that
looks stale against a very recent commit.

### 8. Polish follow-ups (when they exist)

The small, satisfying parked items — extractions, autocompletes, test-depth, a deferred
AC. Terse bullets; these are the "if you have an hour" pile.

### 9. Standalone fixes — no spec ceremony (when they exist)

Real bugs or contained correctness issues worth doing without a spec. One bullet each:
the symptom, and the contained root-cause/fix if known.

### 10. My recommendation (always)

**One** clear pick, with a two-to-three-sentence why. Name the single dependency or first
decision it needs. Don't re-list the menu — commit to a direction.

### 11. The offer (always)

End with a concrete either/or that hands off to the real work:
> *Want me to draft the 002-07 spec slice, or would you rather tackle backup restore — the
> most user-facing of the deferred bets?*

---

## Orient writes nothing

Orient is **entirely read-only** — it renders its briefing to chat (stdout) and writes
**no file at all**: nothing under `docs/`, no `.jig/` cache, no history log. This keeps the
skill lean and ephemeral and keeps *specs* the only source of project state.

If you want the briefing captured — a scheduled evening run you can read the next morning,
or a dashboard that tracks orientation over time — **capture Orient's output from the job
that runs it** (redirect stdout to a file, or let the dashboard ingest it). A deliberate
machine-readable export / persistence contract is being designed separately; Orient itself
stays zero-write.

## Handoff — Orient points, it doesn't do

Orient is a **map, not the journey**. It never transitions a slice, edits a spec, accepts
an ADR, or writes any file. When the user picks a direction, hand off cleanly to the skill
that owns that work:

- Start / split / transition a spec, or implement a ready slice → **jig:spec-workflow**
  (it coordinates the `implementer` subagent; there is no directly invocable
  `jig:implementer` skill). For unattended runs, servo's loop.
- Accept / write the blocking decision → **jig:adr-workflow**
- Fix a standalone bug → **jig:bug-fix**
- Re-shape release scope → **shaper:shape-release** / **shaper:cutline**

Name the handoff in the offer; let the user green-light it.

---

## Judgment

- **Format over completeness.** A readable briefing of the top ~8 items beats an exhaustive
  unreadable dump. If the list is long, group and cap it — and *say* you capped it ("plus 6
  smaller items in the inbox") rather than silently truncating.
- **Grounded, never guessed.** Every item traces to something you actually read (starting
  from the `workflow.py orient` line). If you're unsure whether a trigger is met or a board
  is stale, say so ("b08a627 just landed 036-05, so this row may be stale") rather than
  asserting.
- **"What's next" means what is *blocked on a human*, not what the repo contains.** The
  filesystem gives you state; the PR queue and unmerged branches give you what is waiting
  on a decision. A survey that reads only local files will confidently report a project as
  unblocked while an open PR sits asking the user five direct questions. Check the
  collaboration layer **every run — including on a re-ask later in the same session**,
  when it is tempting to answer from what you already have in context rather than looking
  again.
- **Honest headline.** Surface slippage and shipped-more-than-expected with equal candor.
  Don't cheerlead; don't doom.
- **One recommendation, not a shrug.** The user came for direction. Pick one, say why, and
  offer to start it — keep the rest available if they ask.
- **Stay read-only.** The moment the user says "do it," hand off. Orient's honesty depends
  on it never being the thing that changes state — it writes nothing at all (not even a
  cache); persisting or exporting what it said is a separate, deliberate concern. Its job is
  to *say* the truth, never to *become* it.
- **Adapt the sections to the project.** The order is fixed; the *presence* of each section
  is not. Show only what's real.

## Gotchas

- Resolve `layout.docs_root` before looking for specs, decisions, bugs, the inbox, or
  releases; `docs_root="."` collapses the docs layer to the repository root.
- Treat a bare mid-flow "what's next?" as a continuation of the current slice, not a
  request to rescan the whole project.
- Keep Orient zero-write. Scheduled jobs and dashboards may capture its stdout, but the
  skill itself never creates a cache, history log, or lifecycle mutation.
