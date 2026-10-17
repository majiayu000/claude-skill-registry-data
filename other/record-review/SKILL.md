---
name: record-review
description: After you implemented a change in this conversation, review it adversarially and record what you fixed, declined and assumed in a committed review-points.md, for /human-review to render. Explicit invocation only — user types /record-review [base].
disable-model-invocation: true
---

# /record-review — review what you just built, write down what you decided

This is the **other end** of `/human-review`. That skill writes up a review that already
happened; this one is what happens. It runs **after** the implementation, in the same
conversation that did it — however that implementation went: a ticket, a pairing session,
a fix that grew. It exists because the most valuable thing a coding agent knows about its
own change is the part that never reaches the diff:

* which review findings it accepted, and which it read and **declined** — and why;
* which reading of an ambiguous ticket it **chose**, which reading it did not take, and
  **how sure it is** that it chose right.

That last number — `confidence:`, in `[0, 1]` — is the cheapest thing on the page and the
one nothing else can supply: a reviewer with an hour and eleven assumptions needs to know
which three were close calls, and only the agent that made them knows. It is honest or it
is noise, which is why `prompt.md` says so in as many words: *0.9 on everything is a lie
the page will show.* The scale is fixed so the numbers mean the same thing across runs —
`1.0` the ticket left no other reading, `0.5` a coin flip, below `0.3` expecting to be
corrected — and it is refused outside that range rather than clamped.

All of it lives in a conversation and dies with it. `review-points.md` is where it is
written down instead, at the repository root, committed with the fixes — so a reviewer
sees the artifact arrive in the PR's own file list rather than taking a generated page's
word for it. The page then renders it; it does not invent it.

**Same conversation, or nobody's decisions.** Run from a fresh conversation, the findings
would still come back, but the accept/decline and the assumptions would be an outsider's
guesses about choices it never made — and they read on the page exactly like the real
ones. If the conversation that wrote the code is gone, resume it (`claude --resume <id>`,
or reopen the chat in VS Code) rather than start a new one.

## Headless runs

`claude -p` / `copilot -p` end when the model ends its turn: nothing backgrounded ever
reports back. The whole flow — prepare, reviewers, `ci`, finish — runs in one turn, every
command in the foreground. A run that stops "waiting for X" has not recorded its review.

## Run it

Read `prompt.md` beside this file and follow it, with `$ARGUMENTS` as the base of the
change set (empty: the merge-base with `origin/main`).

**`record-review.py` does the mechanical half**, so the agent's turns go to judgement. The
first run in VS Code spent 332 tool calls, most of them on things with one right answer:
where the format file lives, what the base is, the diff a hunk at a time, four reviewer
prompts, the trailers, seventeen hand-written PR comments. `prepare` resolves the change
set, writes the diff to one file and one brief per reviewer lens, and runs the repository's
own pre-push checks as a dry-run — the cheapest reviewer there is, and the one four model
reviewers missed when the Spectral hook later refused the push. `finish` fills the
front-matter, carries every `file:line` across the fixes to the tree it commits (and
refuses to commit while one points at a line that is gone or blank — `anchors:
review-commit` then tells the page there is nothing left to remap), checks the file,
commits with the trailers — amending its own commit when re-run before it was pushed, so
a round is one `[auto-fix]` commit — and derives the PR comments
(`push-pr-comments.py --from-review-points`). What is left to the agent: run the reviewers,
decide each finding, write the piles.

From a shell:

```sh
for c in "${CLAUDE_PLUGIN_ROOT:-/nonexistent}/skills/record-review" \
         "${HUMAN_REVIEW_HOME:-/nonexistent}/../record-review" \
         "$(readlink -f .claude/skills/record-review 2>/dev/null)" \
         "$(readlink -f ~/.copilot/skills/record-review 2>/dev/null)" \
         "$HOME/workspace/human-review/skills/record-review"; do
  [ -f "$c/prompt.md" ] && { PROMPT="$c/prompt.md"; break; }
done
```

It works in any harness that loads skills and can start subagents. **Claude Code** runs
its built-in `/code-review high` as the review pass; **VS Code Copilot Chat** (which reads
`.claude/skills/`, `.github/skills/` and `~/.copilot/skills/`) and the Copilot CLI start
four read-only reviewer subagents instead, one lens each. For VS Code, no plugin is
needed — link both skills into the personal skills folder and open a new chat:

```sh
ln -s ~/workspace/human-review/skills/record-review ~/.copilot/skills/record-review
ln -s ~/workspace/human-review/skills/human-review  ~/.copilot/skills/human-review
```

**Headless Copilot CLI (`copilot -p`) cannot invoke this skill by name.** It is
`disable-model-invocation: true`, and in `-p` mode there is no user to type the slash
command, so `/record-review` as the prompt answers `Skill not found`. Hand it the files
instead — `Read <skill dir>/SKILL.md and <skill dir>/prompt.md, then follow them` — with
the skill dir found as above. And pass `--harness copilot-cli` to `prepare` and `finish`:
a `copilot -p` started from a Claude Code session inherits `CLAUDE_CODE_SESSION_ID`, and
without the flag the review is recorded as that Claude session's.

Either way the reviewers only
*find*; the conversation that wrote the code *decides*.

## What the flow downstream depends on

Three things, and a fourth for the pull request. Each is read by a script, so getting one
wrong is a silent loss of exactly one row on the page:

| what | read by | if it is missing |
| --- | --- | --- |
| `review-points.md` at the repo root | `scripts/review-points.py` | the Review tab has no Fixed / Ignored / Assumptions piles, and says so rather than rendering "nothing outstanding" |
| `.human-review/review-points.json`, the structured report (not committed — regenerated from the file above) | `hrbuild/tabs/review.py`, after checking it against `reference/review-points.schema.json` | the build stops and names what does not match. The Review tab is rendered from this report only, under titles and labels the builder owns |
| `Review-Points:` + `Implements:` trailers | `scripts/review-commits.py` | which commit is the implementation and which is the review is guessed from the file's history, or not at all. `Implements:` names the feature's own commit (`--implements <sha>` when HEAD is housekeeping after it), and `Audited: <base>..<head>` the range the reviewers actually read |
| `Claude-Session:` on both commits | `scripts/session-cost.py` | the phase costs fall back to `.human-review/.session`, which is gitignored and dies with the directory. Outside Claude Code the line is left out; a Copilot CLI review gets `Copilot-Session:` instead, the session `finish` found in `~/.copilot/session-store.db` |
| `review-cost.json` beside the record, committed with it | `review-cost.py --ledger` → the `$` tab's first three rows | the rows are *derived* from the session stores after the fact, and say so. `finish` writes it: implementation (every harness that edited the change set before `prepare` — Claude transcripts, the Copilot CLI store, VS Code chat logs), review (`prepare` → the reviewers' end, which the first `ci` stamps), auto-fixes (→ this `finish`; each CI round's `finish` runs it on). Schema: `reference/review-cost.schema.json` |
| `.human-review/pr-comments.json` (not committed) | `scripts/push-pr-comments.py`, behind the Review tab's *Push to GitHub PR* button | the button has nothing to send; `--from-review-points` can derive a blunter one from the record |

**The trailers are written by `record-review.py finish`, and the harness may write after
them** — or ask `finish` to: `--commit-trailer "Co-authored-by: Copilot <…>"` (repeatable)
appends a line of its own, so no harness has to patch the script to sign the commit.
Claude Code appends `Co-Authored-By: Claude …` as a paragraph of its own, which puts the
three keys in the *penultimate* paragraph — and git's `%(trailers:key=…)` only parses the
last one, so it returns empty for all three. The first real run of this flow produced two
correctly trailered commits that the page reported as "not recorded" for exactly that
reason. `review-commits.py` therefore reads the keys off any line of `%B`, with
`%(trailers)` as the first pass only. Nothing is asked of the agent beyond one key per
line: a paragraph landing after them is expected and harmless.

**Two commits at least: the implementation, then the review.** The implementation may
already be several commits by the time this runs — they are left as they are, and
`Implements:` names the last of them. The review is one commit: the accepted fixes plus
`review-points.md`, its subject starting with **`[auto-fix]`** — as does any later commit
applying a reviewer's finding — so `git log --grep='\[auto-fix\]'` finds everything the
agent changed on the review's say-so, and `review-commits.py` lists those commits (and
falls back to the last one when a squash lost the trailers). That split is what makes
"what did reviewing cost, against writing it" a measurement instead of an estimate — the
commits are the only timestamps in the whole flow that a rebase cannot move without also
moving the work.

## Which review pass

In Claude Code, the **harness built-in** `/code-review` (effort levels `low`…`ultra`,
`--fix`, `--comment`) — not the `code-review:code-review` plugin, which needs a real
GitHub PR and ends by posting a `gh pr comment`.

`--fix` is refused deliberately, and so is a reviewer subagent with write access. Either
applies the findings to the working tree, which destroys the accept/decline information
this whole flow is built to capture: afterwards there is a diff, and no record of which of
its lines the agent would have argued with.

Never re-run a pass to "confirm" a finding. Two runs over the same diff word and rank
their findings differently, so a second invocation does not confirm the first — it produces
a different review at full price, and whichever ran last wins.

## The demo PR is this flow plus hand retouches

`petclinic`'s `test-pr` branch ran this flow, then has a handful of deliberate retouches
on top — one per review-page tab, so the demo has something to show everywhere.
`demo/DEMO-PR-RECIPE.md` lists them, with the commit each one landed in and how to redo it.
