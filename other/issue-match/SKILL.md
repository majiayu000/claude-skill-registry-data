---
name: issue-match
description: >-
  Measure a target repository's queue and find a live open issue the contribution would close,
  before opening a pull request there. Reports how many PRs are open, how many of the last N
  closed ones were actually merged, and which issue to attach to, because a cold PR into a dead
  queue is a wasted artifact. Triggers: "/issue-match", "is this repo worth a PR", "measure the
  queue".
license: MIT
---

# /issue-match — knock here, or walk past?

> 🧒 End the report to a non-technical owner with an "In plain words" block ([[eli5-always]]).

The owner's rule from 2026-07-25 ([[cold-pr-into-silent-queue]]): **a cold PR into a silent queue is not a contribution, it's noise.** Measuring the queue is the first step, BEFORE writing any code. This skill turns that measurement into a button instead of hand-driving `gh` in every session.

Measured 07-25 on `anthropics/claude-cookbooks`: 220 open PRs, median age 47 days, 51% without a single comment, 67% of merges happened within a day of submission (which means the agreement existed BEFORE the PR). We had 6 open there, 5 cold, **0 merged**. The only one a human reacted to was the one that came in through someone else's open issue.

## How to run it

```bash
python "$USERPROFILE/.claude/scripts/issue_match.py" anthropics/claude-cookbooks --artifact "search agent, adversarial verify"
```

| Command | What it does |
|---|---|
| `<owner/repo>` | measure a single repo |
| `--artifact "kw1, kw2"` | **the main parameter** — the keywords of our artifact, used to find the door |
| `--all` | fan out across every repo in the config (~5s per repo; 14 repos ≈ 70s) |
| `--init` | build the config from OUR PR history (`gh` finds where we submitted) |
| `--live-days N` | an issue counts as live if it was updated within N days (default 30) |
| `--json` | machine-readable output |
| `--no-draft` | skip the entry draft |

Config: `~/.claude/issue_match.json`. Exit codes: `0` measurement done · `2` bad arguments · `4` `gh` unavailable or all fetches failed.

## How to read the output

1. **QUEUE** — open PRs (the exact count, not truncated by a limit), median age (when sampled, this is a **lower bound**, the real one is higher), the share with no comments, the merge pattern. If "merged on the day of submission" is ≥60%, that is not "they merge fast", that is **pre-agreement**; a cold PR will not reproduce that rhythm. Look at **one-time authors**: if none of the merges came from a one-time author, the repo merges only its own people, and a healthy median promises an outsider nothing.
2. **US THERE** — how many of our PRs are sitting and how many got no reaction. Many cold ones = warm those up first instead of spawning new ones.
3. **DOORS** — live third-party issues matching the keywords. Our own issues are counted separately: **your own door is not an invitation**.
4. **VERDICT** — 🟢 enter through an issue · 🟡 open our own issue and wait · 🔴 don't push · ⚪ **not measured** (the issue fetch failed, or the door may have fallen outside the sample) — do not make a decision on that data, run the measurement again. A silent fetch is not an answer.

⚠️ Without `--artifact` a 🟢 verdict is **deliberately withheld**: the match was never checked, and a fresh issue on its own is not yet our door. Broad words ("agent", "memory") produce 🟢 almost everywhere — that is honest noise, not a find; narrow them to the essence of the artifact and read the `← matched:` line.

## Boundaries

- **READ-ONLY.** The skill sends nothing. A comment in someone else's thread and a PR are outbound → a human sends them (or I do under the mandate [[ship-github-no-plus-wait]], but signed and after the quality gate).
- Matching works on words in the title, labels and issue body. That is a crude filter, not comprehension; the final "is this our thread or not" is a human call over the list.
- With >100 open PRs the median age is computed over the newest ones → it is understated. That is flagged in the report.
- **Issue liveness** = human activity (the last comment by a LIVE human, or the issue being opened by a human), not `updatedAt`: that field is bumped by labels and bots, and a "bump" from Dependabot/stale would look like a live door. Bot comments are counted separately and never count as liveness.
- **Where it matched matters.** A match in the title or a label = on-topic; one generic word in the body (`auth`, `fix`, `token`) = more likely a collision, and no 🟢 is granted for it (you need either a title/label hit or ≥2 words in the body). The `← matched` line shows exactly where.
- **The merge median is global** per repo: it mixes all PR types (a typo fix and a new recipe) and does not show the queue for a specific area. A guide, not a verdict — if our artifact is narrow, look by hand at how PRs in exactly that area moved. (Raised by the external reviewer Codex, 07-27; fixing it with a path filter = added complexity, not taken for now.)
- Check the commit/PR signature BEFORE sending ([[signature-is-part-of-the-work]]) — 16 of 20 PRs went out signed by an empty account.

## Further down the pipeline

🟢 → a comment in the thread → the maintainer answers → a PR referencing the issue → `pr_watch.py` watches for a reaction → a scheduled bump.
🔴 → don't push into this repo; the cold PRs already sitting there get **warmed up** (tie each one to the issue it answers) instead of adding a ninth.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
