---
name: tidy
description: The cleanup stage. When a build hits a milestone (pre-launch, end of a sprint, "let's tidy this up"), scan a repo — or 100+ repos at once — for rot, see the extent at a glance, then clean it with confirmation. Report-first, never silently edits. Works on any git repo, Hamzaish-built or not.
---

# /tidy — the cleanup stage

Rot accumulates in every repo: links that point at moved/gitignored files, a key that
slipped into a commit, an asset nothing references, a dependency that 404s on install.
None of it is visible day-to-day — it surfaces at the worst time (a reader's 404, a
failing CI, a leaked key). **`/tidy` is the stage where you find and clear it on purpose.**

This is a *stage*, not a gate. The fast guards (`check-changelog`, `check-assets`) block
on every push; `/tidy` is the broad, report-first sweep you run when it's time to clean.

## How to run it

```bash
bun run tidy                      # the current repo → summary + recommended next steps
bun run tidy <path>               # a specific repo
bun run tidy --all ~/Claude       # every git repo under a folder → one aggregate table
bun run tidy --links              # drill into one category (--secrets --files --deps)
```

It scans four kinds of rot and **shows the extent first** (a count per category) so you
never get a wall of output:

| | what it catches |
|---|---|
| 🔗 **Links** | markdown/HTML links to missing files, or that resolve only to a **gitignored** target (works on the author's disk, 404s for everyone else) |
| 🔑 **Secrets** | high-confidence committed-key patterns (AWS, Stripe, GitHub, Google, Slack, private-key blocks) — flagged for **review**, not auto-judged |
| 🗑 **Dead files** | committed images/assets that **nothing references** — safe to prune |
| 📦 **Deps** | `package.json` dependencies that **don't resolve on npm** (the dead-`@inngest/sdk` class) |

## The flow (report → recommend → ask → fix)

1. **Run it.** Present the summary table — extent per category, per repo.
2. **Recommend.** Call out which categories matter and why (a broken link is a reader's
   404; a flagged secret needs rotating; an unresolvable dep breaks every install).
3. **Ask.** Let the operator pick what to clean. Never assume.
4. **Fix with confirmation — plan, then apply.** `bun run tidy --fix <repo>` prints the
   exact change plan (which broken links get de-linked) **without writing anything**;
   re-run with `--apply` to make those edits. So you always *see each change first*.
   Auto-fix is narrow on purpose: it only **de-links** broken/gitignored text links
   (`[text](bad)` → `text`). Secrets, deps, images/HTML links, and file deletions are
   **never** auto-applied — they're listed as manual with guidance (rotate a key, pick the
   right package), because their fix is judgement, not a line-edit. Survey many with
   `--all`, then `--fix` one repo at a time.

## Discipline

- **Report-first, always.** The value is *seeing* the rot before touching anything.
- **Don't gate on it.** `/tidy` is slow (network dep checks) and broad — keep it a stage, not a push-blocker. The narrow guards stay the gate.
- **Secrets are review-grade.** A pattern match is a *prompt to look*, not a verdict — and if real, the fix is rotate-the-key, not just delete-the-line.
- **Frozen dirs are skipped** (`_archive/`, `node_modules/`) — they're not yours to tidy.
- **The engine is portable.** `scripts/tidy.ts` runs against any repo path — that's what makes the 100+-repo sweep one command.
