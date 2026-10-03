---
name: issue-sanity-check
layer: method
description: A pessimistic go/no-go the moment you pick up a GitHub issue — read it skeptically and hunt for reasons NOT to do it (already done? obsolete? duplicate? premise wrong? cheaper way? net-negative?), returning proceed / reshape / drop with one-line evidence. The pickup-time half of the dedup gate (the create-time half is /issue-dedup). Use as step 1 of the Task Execution Workflow, or run /issue-sanity-check #NN.
allowed-tools: mcp__github__issue_read, mcp__github__search_issues, mcp__github__list_issues, mcp__github__add_issue_comment, Read, Grep, Glob, Bash
---

# Issue Sanity-Check — should this even be done? (pickup gate)

Claiming an issue and starting to build is a reflex. This skill inserts a **deliberately
skeptical pause** first: a stale, obsolete, duplicated, or wrong-premise issue is cheapest to
catch *before* a build is sunk into it. It's the **pickup-time** half of the dedup gate;
**`/issue-dedup`** is the create-time half. Both are sub-issues of epic #297.

This is a **skeptic's checklist, not a rubber stamp.** Your job here is to find a reason *not*
to do the work. If you can't find one, that's the proceed signal.

## When this fires

Step 1 of the Task Execution Workflow — the moment you claim an issue, before doing the
work. Also on demand: `/issue-sanity-check #NN`.

## The checklist (hunt for a reason to STOP)

Read the issue, then ask each — answer with one line of evidence (a link, a path, a date):

1. **Already done?** — search closed issues/PRs and the code for the change. Did a later
   commit/PR already ship this? (`git log --oneline -S'<symbol>'`, `search_issues state:closed`.)
2. **Obsolete / overtaken?** — has the architecture moved past it? (e.g. it targets Pages but
   we're on Workers; it patches a file that's been deleted/rewritten.)
3. **Duplicate / colliding?** — is there an open issue or epic for the same thing? (Reuse the
   `/issue-dedup` search. If yes, this is a merge, not two builds.)
3b. **Already being worked — right now?** — the one an issue search misses, because the
   collision isn't another *issue*, it's another *runner*. Check all three:
   - the issue is **closed** (someone finished while you were reading it),
   - an **open or merged PR** references it (`search_pull_requests "<N> in:body"`, then confirm a
     `Closes #N`-style keyword — `Follow-up to #N` is not a claim),
   - **`status:in-progress`** is on it and was stamped recently (check the label's event
     timestamp, not just its presence — a crashed run leaves a stale one).
   > Any of those → **🛑 Drop** (or 🔁 into "review/finish the existing PR"). This cost three
   > duplicate builds on 2026-08-05 alone: #1478 started 8 min *after* #1473 closed its issue,
   > and #1889 opened while #1888 was already open. The pipeline half of this gate is the
   > `claim-guard` in `scripts/pipeline-loop-guard.mjs` (#1890) — it cannot see interactive
   > sessions, which is exactly how #1622 and #1889 happened. **You are that half.**
4. **Premise still true?** — does the "we think that…" hypothesis still hold, or did reality
   change? A wrong premise makes a perfectly-built feature worthless.
5. **Cheaper alternative?** — is there a smaller change, an existing composable/skill, or a
   config flip that gets 90% of the value? (KISS — CLAUDE.md core principle.)
6. **Net-negative?** — does it add surface/complexity we'll regret, contradict a current
   pattern, or block something more valuable? Sometimes the right move is to close it.
7. **Target reachable?** — do the files the issue *names* actually render or execute? Run
   `node scripts/check-issue-targets.mjs <issue-number>`. An issue can name dead code, and
   building exactly to spec then ships something nobody can reach **while satisfying every
   acceptance criterion** — #1657 specified an Import button in `ProductsTab.vue`, a component
   mounted in no template.
   > ⚠️ **Flag, never drop.** Zero references is a *hypothesis* (the #1149 deletion protocol,
   > in reverse): this repo mounts things dynamically — directory scanners, the
   > `croutonBlocks`/`croutonLayoutBlocks` registries, `@nuxt/kit` resolver paths. The probe
   > already excuses file-routed paths (`server/api/**`, `app/pages/**`, auto-imported
   > `utils`/`composables`) and registry entries, but verify before acting. The right verdict
   > is **🔁 Reshape** — "build it, somewhere reachable; confirm where" — not 🛑.

## The verdict (REQUIRED output)

End with exactly one of:

- **✅ Proceed** — no blocker found. One line on why it still makes sense, then go.
- **🔁 Reshape** — the goal is valid but the framing/scope is wrong. State the smaller/changed
  scope, update the issue body, then proceed on the reshaped version.
- **🛑 Drop** — there's a real reason not to do it. Name it with evidence, and (interactive)
  recommend closing `not_planned` / merging into the duplicate — **ask the owner before
  closing**, don't unilaterally bin their issue.

Keep it tight — seven one-line checks and a verdict, not an essay. The value is the *pause*, not
a long report.

## Recording it

- **Interactive** → state the verdict in chat. For 🔁/🛑, ask the owner before reshaping or
  closing (use `AskUserQuestion`). For a 🛑 you act on, post a comment with the evidence so the
  close is explained (lead with the 🤖 provenance header — see CLAUDE.md).
- **Autonomous / pipeline** → post the verdict as a comment on the issue (provenance header)
  so the chain is auditable, and for 🛑 set `status:blocked` + @mention rather than closing
  silently.

## What this is not

- Not the create gate — that's `/issue-dedup` (don't mint a duplicate).
- Not bug-archaeology — that's the "how/when was this introduced" gate for *bugs* (#424).
- Not a license to skip work you simply don't feel like doing — the verdict needs *evidence*,
  not vibes.
