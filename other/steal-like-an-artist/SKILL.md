---
name: steal-like-an-artist
description: "Use when starting any non-trivial build, design, feature, redesign, integration, prompt, pipeline or research task, right after a context compaction, or when Nour says steal like an artist, learn from the best, reverse engineer it, whats the best setup out there, or theres gotta be a good setup. Always-on stance: before writing from scratch, find the two to four best existing implementations (this repo, open source, products), take their mechanisms, build the smallest version that carries them, and leave a Benchmarked against line. Not for: a status read, a merge, a CI or deploy question, a one-line fix, a copy edit, a question about an existing file, debugging a broken feature (systematic-debugging), or a schema or migration change (nickstire-tidb-ddl, statenour-migration). In-repo prior art alone is prior-art-grep, a shipped binary or capture is reverse-engineer-anything, a skill or tool search is find-skill."
triggers: steal like an artist, learn from the best, best setup out there, what kind of setup, gotta be a good setup, how would a pro do it, reverse engineer it, benchmark the best, how do the pros do it, best in class, upgrade the basic stuff, lets build, redesign, new feature, new pipeline
---

# steal-like-an-artist

Always on. Before you build anything non-trivial, find who already solved it best and take the mechanism.
A blank page is the last option, not the first. This skill does not do the search itself: it says which tool to reach
for, in what order, and what receipt to leave.

House-authored for Nour on 2026-10-26 (job 2026-10-26-steal-like-an-artist), not vendored. SKILL.md is byte-identical
in the repo copy (`.claude/skills/`) and the machine copy (`~/.claude/skills/`); change both or neither. `evals/` lives
in the repo only.
His words, 2026-10-26: "steal like an artist instead of trying to start on our own", "always max creative truth seeking
n hard working for me ... max resourceful creative proactive". And 2026-10-22: "always learn from the best".

## The rule

1. **Name the task in one line.** Anything on the "When NOT to use" list: skip silently, no line. Write
   `steal-like-an-artist: nothing to benchmark for <task>` only when a task looked non-trivial and you chose not to
   benchmark it. The cost test: a Perplexity research run takes 5 to 12 minutes, so benchmark anything that is more than
   about an hour of build, and skip below that unless Nour asked for it.
2. **Find two to four of the best existing implementations,** cheapest source first:
   - This repo and its sibling app: `prior-art-grep`. The other app often already has it. Grep `docs/UPSTREAMS.md`
     for the candidate (about 170 KB, never read whole): it holds adoption verdicts already made.
   - Open source and products: Perplexity in Chrome (Nour's standing directive). Never fan out research subagents and
     never burn session tokens on broad web reading; read only the one or two best cited sources yourself.
     A main session whose Chrome cannot reach Perplexity reads the primary pages directly and says so in one line.
     A lane or session that cannot drive Chrome does not web-read at all: it lists the exact Perplexity query under
     CROSS-LANE NEEDS in its return, for the manager to run.
   - Other products' PUBLIC pages and flows (a competitor's tire finder, a booking flow): ordinary public web reading,
     observation only. No accounts, no orders, no forms submitted, no terms broken.
   - A skill, MCP, plugin or tool that already does the job: `find-skill`.
   - A shipped binary, package, capture or device of OUR OWN: `reverse-engineer-anything` (static first, own accounts
     only). A complete source repo is ordinary reading, not REA.
   - A pasted plan or audit: `plan-gate` first; most of it is usually built already.
   - `prior-art-grep`, `plan-gate`, `source-to-skill` and `find-skill` are REPO skills. In a session with only the
     machine copy loaded, use `find-skills` (the machine twin of `find-skill`) and plain `git grep`, and say so in the
     skip or receipt line.
3. **Extract mechanisms, not trivia.** For each one: the data flow, the trick that makes it fast or good, the UI pattern,
   and the failure it avoids. A feature list or a star count is not a mechanism.
4. **Decide each one: adopt, adapt or reject,** with its cost and a kill criterion (the result that would make us drop
   it). Mechanisms are free; code has a licence. Never copy GPL or AGPL code in, never go behind a login, never break a
   site's terms (memory `feedback-learn-from-the-best`).
5. **Write the receipt, then build.** One line in the plan, the lane brief and the PR body:
   `Benchmarked against: <name> (<url>) · adopted: <mechanism> · rejected: <mechanism> because <reason>`
   Then build the smallest version that carries the adopted mechanisms. `ponytail` and `karpathy-guidelines` still
   apply: steal the mechanism, not the size.

## The stance, as behaviors you can check

Truth-seeking, hard work, resourcefulness and creativity are already checkable traits in `.agents/core/IDENTITY.md`
(voice in `.agents/core/SOUL.md`). This skill adds the steal-first order and two behaviors those files do not spell out:

| What Nour asked for | What it looks like in a turn |
|---|---|
| Proactive | Name the adjacent rot and the next step without being asked. Propose it; do not drift into it. |
| Fulfils what he wants | His words are the spec. A wider reading of them is a ruling: write it down in one line so he can overrule it. |

## Where it sits with the other skills

| Skill | Its job | This skill's part |
|---|---|---|
| `find-skill` | Per-turn gate: would an outside search change the answer? | Says yes for every non-trivial build, and says where to search. |
| `prior-art-grep` | In-repo duplicates: tables, queues, tools, flags | Step 2, first stop. |
| `reverse-engineer-anything` | Shipped artifacts we own | Step 2, only for binaries, packages and captures. |
| `brainstorming` | Shape the design | Runs after the benchmark, with the adopted mechanisms as input. |
| `source-to-skill` | Turn a found source into a cited skill | When the best source is worth keeping as a skill. |

## When NOT to use

- A status read, "check whats going on", a merge, a CI or deploy check.
- A one-line fix, a typo, a copy edit, a rename.
- A question about how an existing file works, or a bug in a feature that exists (that is `systematic-debugging`).
- A schema or migration change (that is `nickstire-tidb-ddl` or `statenour-migration`).
- Anything under about an hour of build that Nour did not ask to benchmark.

## The receipt

A turn that applied it has a `Benchmarked against:` line in the plan, the brief or the PR body. A non-trivial task that
skipped it says why in one line. "I know how this is usually done" is not a benchmark.

## Red flags

- "Nothing out there fits us" said before any search.
- A list of product names with no mechanism under any of them.
- Copying all of the best product instead of the one mechanism that matters.
- A research fan-out in session tokens instead of Perplexity in Chrome.
- The benchmark is in the reply but not in the plan or the PR body, so the next session cannot see it.
