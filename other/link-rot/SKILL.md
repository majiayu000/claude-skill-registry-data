---
name: link-rot
description: "Monthly loop that checks every external link the built site renders still resolves. Build the site, probe the external hrefs with scripts/check-external-links.mjs, verify every failure by hand, and fix genuinely dead links on a local branch for approval. Use when asked to run the link rot loop or check the external links. Never pushes, merges, or deploys."
icon: link_off
displayDescription: "Collects every external link the built site renders, from case-study references to footer profiles, and checks each one still resolves. The build already proves internal links can never break; the outside world offers no such guarantee. Failures are verified by hand before anything is called dead, because bot-blockers fake them, and real rot is fixed on a branch for approval. One of the loops described on the Loops page."
invoke: ["run the link rot loop","/link-rot","check the external links"]
---

# link-rot

Monthly loop over the one class of link the build cannot guard: external ones. `scripts/validate-internal-links.mjs` makes a broken internal href impossible; a moved profile, a deleted article, or a dead product page outside the site rots silently. Each run probes every external href in the prerendered HTML, verifies the failures by hand, and fixes real rot on a local branch. **Never push, merge, or deploy — the user approves every change.**

## When invoked

Run when asked to "run the link rot loop" (`/link-rot`), or by a scheduled task once one is created.

## Scope guardrails (read first)

- **A probe failure is a lead, not a verdict.** Plenty of hosts answer scripts with 403/429/999 while serving browsers fine. Never flag, fix, or remove a link the loop hasn't confirmed dead in a real browser.
- **Link surgery only.** Swap an href for its new home, or remove a dead anchor with the minimal wording change that removal forces. Rewrites beyond that, and any dead link whose replacement needs a judgment call (which article now says this? does the paragraph still hold without it?), go in the report as proposals.
- **Local branch only.** Never push or touch the user's working tree — the temporary-worktree recipe in `.claude/skills/growth-loop/SKILL.md` (step 4), branch name `links/YYYY-MM-DD`. Skip the worktree entirely on a clean pass.

## The loop

### 1. Build and probe

```bash
npm --prefix website run build
node scripts/check-external-links.mjs
```

The script owns extraction and probing — which HTML it reads, timeouts, the HEAD-then-GET fallback, and the `KNOWN_BLOCKERS` list of hosts that reject scripts on principle (its doc block also owns why it is deliberately not part of `verify`). A same-day build's output can be reused if it is fresh.

### 2. Verify every failure by hand

For each reported failure: retry with `curl` and a browser user agent, then load it in the Browser pane. Three outcomes:

- **Alive in a browser** → a bot-blocker, not rot. Add the host to `KNOWN_BLOCKERS` in `scripts/check-external-links.mjs` with a written reason, so future runs list it for manual checking instead of re-flagging it.
- **Redirects permanently to a real new home** → fixable; point the href at the destination.
- **Actually dead** → fixable or proposable per the scope guardrails.

Also spot-check the links the script listed under known blockers — they are probed by nobody, so this manual pass is their only coverage.

### 3. Fix on a branch

Worktree recipe from the growth-loop skill, branch `links/YYYY-MM-DD`. Verify the website build in the worktree; if anchor text changed, the regenerated corpus rides along per the commit-scope rule in that recipe.

### 4. Report and hand off

Repeat the full report in the final message (the in-repo `KNOWN_BLOCKERS` reasons are the durable record; no report file). Group findings as **fixed on the branch** (old href → new href, with the pages that rendered it), **proposed** (dead, but the replacement is a judgment call), and **false alarms recorded** (hosts added to the blocker list). **"Every link resolves" is a valid outcome** — say so briefly and stop. End with the branch name if one exists, confirmation the build passed, and the approval step: merging the branch (or saying `ship`) approves it; deleting it rejects it.
