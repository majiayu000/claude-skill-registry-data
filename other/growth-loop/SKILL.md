---
name: growth-loop
description: Weekly GA-driven copy experiment loop for robertritacca.com. Analyze last month's GA data, find one copy problem, implement the fix on a local branch, and write a report for approval. Use when asked to run the growth loop. Never pushes, merges, or deploys.
icon: cycle
displayDescription: "Runs one analytics-driven copy experiment end to end: pulls GA4 data, filters bot noise, forms a falsifiable hypothesis about the words on a page, implements the change on a branch in a temporary worktree, verifies the build, and writes a problem / hypothesis / solution report for approval. Runs itself every Monday, as one of the loops described on the Loops page."
invoke: ["run the growth loop","/growth-loop"]
---

# growth-loop

Weekly GA-driven copy experiment loop for robertritacca.com (this repo's `website/` deploys there via Vercel). Each run: analyze last month's GA data, find ONE copy problem, form a hypothesis, implement the fix on a local branch, and write a clear report for the user to approve. **Never push, merge, or deploy — the user approves every change.**

## When invoked

Run when asked to "run the growth loop" (`/growth-loop`) or by the `growth-loop-weekly` scheduled task.

## Scope guardrails (read first)

- **Copy only.** Headlines, body text, CTA/link labels, button text, page `metadata` titles/descriptions — all inside `website/src`. No CSS, no layout, no component structure, no new components, no dependencies.
- **One focused change per run.** One page, or one copy element (e.g. the same CTA wording) across a few pages. A reviewer should be able to read the diff in under two minutes.
- **Local branch only.** Never `git push`, never merge, never touch the user's checked-out branch or working tree (use a worktree — see step 4).
- Never read into version control or modify `ga-analysis/service-account.json` or `ga-analysis/output/`.

## The loop

### 0. Close the previous loop

Read the newest report in `ga-analysis/loop-reports/` (git-ignored, local-only). If a previous experiment was approved/merged, check whether its metric moved in this run's data and record the verdict (improved / no change / worse / too early to tell) in this run's report. If the previous branch was never merged, note that instead and don't count it as tested. Don't re-run a hypothesis a previous report already tested unless the report says the change was never merged.

### 1. Pull the data

```bash
cd "$(git rev-parse --show-toplevel)/ga-analysis" && ./.venv/bin/python pull_ga.py --days 28
```

Output lands in `ga-analysis/output/all.json`. If the venv is missing: `python3 -m venv .venv && ./.venv/bin/pip install -q -r requirements.txt`. FutureWarnings are harmless.

### 2. Analyze — with the ga-report skill's judgment calls

Apply every gotcha from the `ga-report` skill (`~/.claude/skills/ga-report/SKILL.md` — installed only on Rob's Mac, like the GA venv and credentials; this loop runs there, not on the Windows machine). That skill owns the bot-traffic list, the pagePath-vs-pageTitle rule, and the traffic-mix baselines — read it fresh each run rather than trusting a remembered copy, and subtract the bots it names before drawing conclusions.

Look for **copy-shaped problems**, e.g.: a high-traffic landing page with weak engagement or dwell; strong entry pages that don't lead anywhere (missing/weak CTA copy); case studies with good dwell but low reach (weak titles/descriptions); a mismatch between what a traffic source promises and what the page's headline says.

### 3. Pick ONE problem and write the hypothesis

The hypothesis must be falsifiable and name its metric:
> If we [specific copy change], then [specific metric for a specific page/segment] should [direction] over the next few weeks, because [reasoning grounded in the data].

If the data doesn't support a confident copy hypothesis this week, **say so and stop** — a no-op run with a short "nothing worth changing" report is a valid outcome. Don't invent a change to have something to ship.

### 4. Implement on a branch (via worktree)

Work in a temporary worktree so the user's working tree is untouched:

```bash
REPO=$(git rev-parse --show-toplevel)
WT=$REPO/../.growth-loop-worktree
BRANCH=growth/$(date +%F)-<short-slug>
git -C "$REPO" worktree add "$WT" -b "$BRANCH" main
```

Make the copy edits in `$WT/website/src/...` — new copy follows `content-design.md` (voice, register, banned words) — then verify the build (the repo is an npm workspace — one install at the worktree root wires everything, including the `@robr0/design-system` link back to the worktree's own the site source; it's seconds thanks to the npm cache. Do **not** symlink `node_modules` from the main checkout — Turbopack rejects symlinks that point outside the project root):

```bash
cd "$WT" && npm install --no-fund --no-audit
cd "$WT/website" && npm run build
```

If the build fails because of your edit, fix it. Then commit in the worktree (conventional message, e.g. `experiment(growth): reword /work CTA — hypothesis in loop report 2026-07-20`). Commit scope: the website `prebuild` regenerates tracked files, and they stay out of the commit **unless your edit is what changed them** — with one standing exception that always qualifies: the site chat's corpus (`website/src/data/site-corpus.generated.ts`) is built from page prose, so a copy edit changes it by construction. Commit the regenerated corpus alongside your copy edits every time (a branch without it fails CI's drift guard, and `git worktree remove` refuses a dirty worktree); leave the other regenerated files (everything else the website `prebuild`'s generators write — mostly under `website/src/data/` and `website/public/`, though the chain also touches root surfaces like `README.md` and the design system's token registry) out unless they actually changed. Then clean up:

```bash
rm -rf "$WT/node_modules" "$WT/website/node_modules"
git -C $REPO worktree remove "$WT"
```

The branch survives worktree removal and is ready for the user to review.

### 5. Write the report

Save to `ga-analysis/loop-reports/YYYY-MM-DD.md` **and** repeat it in full in the final message to the user. Plain English — the user is a designer, no analytics jargon. Format:

```markdown
# Growth loop — YYYY-MM-DD

## Last week's experiment
[Verdict on the previous change, or "none / not merged".]

## The problem
[What the data shows, with the actual numbers, after bot filtering.]

## The hypothesis
If we ..., then ... should ..., because ...

## The change (branch: growth/YYYY-MM-DD-slug)
[File(s) touched. Before → after for every copy string changed.]

## How we'll know
[Which metric to look at next run, and roughly what movement would count as a win.]
```

### 6. Hand off for approval

End by telling the user: the branch name, that the build passed, and that nothing is pushed or deployed. To approve they merge the branch (or say `ship` on it); to reject they delete the branch. That's the whole approval step.
