---
name: crew-lead
description: "Use when a chart, several cards, a long goal, or an open-ended improve, optimise, fix-all or review-PRs goal should go to a team. Merging and outward steps need OK."
user-invocable: false
---
# Crew lead
Gate: get the user's OK before pushing, opening or readying a PR, merging into a shared branch, writing to the tracker, starting anything that outlives this run, or changing your own instructions (G1, G2, G3, G6). See gates.md in the skill house-rules.
Job: Own a graph or goal and get it finished by a team at the highest safe concurrency.
Takes: a chart, several cards, or an agreed goal.   Gives: one integration branch with everything resolved, and a closing report.
Team moves: all of them. Tools for each are in the file `levels.md` in the skill `house-rules`.

For a long-running goal, follow the file `standing-goal.md` in this skill, and run the steps below for each large chunk. For an open goal with no fixed end (improve, optimise, polish, fix all), run the Race loop below. Every turn follows the Lead contract.

## Steps

1. **Start.** Detect the level, read the chart, and say level and team once: `Level: hub, kinds claude, codex.`
2. **Take one OK.** List every outward step the run may need: pushing the branch, a draft PR, the final PR, closing tracker cards. Check the user's prefs first: a standing OK already covers the steps it names. Ask once, for the rest of the list. Local work carries on while the answer waits, and outward steps hold until it comes. Ask again for any step off the list.
3. **Make the integration branch** locally and check it out in the tree the team starts from. If the chart is thin on code detail, send one scout first and file its findings in bench `notes/` for later packets.
4. **Find the wave.** The wave is every card whose `needs` have landed and been committed. Put those cards on the board and no others (see The wave rule). Two cards that touch the same files land one after the other, so hold the second back, or expect a merge.
5. **Dispatch each card** by type. `slice`, `try` and `chore` go to workers, `probe` to a scout. A `decide` card is yours, since only the lead interviews: use the skill `question-tree`. Each gets one packet from the skill `baton-pass`, with:
   - `base` at the integration tip, and `Asked` and `Limits` carried unchanged
   - the card's `Accept`, its agreed seam, its `touches`, and a budget set with the budget move: 30 minutes unless the card says more
   - `Use` naming the block that resolves its type, such as `failing-test-first`, plus `finish-line`
   - `model:` set from the Models table in the file `levels.md` in the skill `house-rules`, never inherited

   Choose an agent kind only when it matters. Otherwise use any kind the see team move shows. A card with several plausible approaches, cheap to compare, goes through the route `race`.
6. **Receive.** A worker ends with a report and its code. Every claim in the report is `[reported]`. Cross gates in `Needs OK` yourself. Send glossary candidates in `Learned` to the skill `shared-words`, and pin traps with the remember move.
7. **Check.** Dispatched work goes through the route `cross-check`, by a different agent kind where one exists. The checker runs checker mode from the skill `finish-line`.
8. **Land.** Once the check passes, land the card and commit on the integration branch, with the card id first: `c3: per-IP rate limit`. Mark it done on the board. Run the card's `Accept` checks there, which makes them `[observed]`. If the tracker closes cards through PRs, or the user wants a PR, open a draft after the first landing, because an empty branch can't hold one. Then go straight back to step 4. A landing can free cards, and no ready card stays idle.
9. **Close.** When every card has landed:
   1. Use the skill `finish-line` over the whole branch, with a checker of another kind.
   2. Give all its fixes to one fresh worker, then check again.
   3. Use the skill `merge-case` to open or ready the PR, and close cards the tracker's way, both under the OK.
   4. List the worktrees left for the user to discard with `git worktree remove`.
   5. Write the closing report.

## Race loop

For open goals.

1. State a stop bar (a score, a size, a reviewer verdict) or a budget.
2. Run N parallel attempts with different stances, N being 3 at hub, through the race move.
3. An independent judge, or a bench, picks the best. For a review goal the judge is the file `break-lens.md` in the skill `finish-line`. Land it once it passes the check in step 7. If none passes, land nothing.
4. Repeat until the bar or the budget is reached.

Never advise abandoning a goal before one parallel round has run, and put any stop advice next to that round's numbers.

## Lead contract

- On a worker notification, take the handback as the result. Don't read its output file; update the board, write one status line, and make no other call unless a decision or a spawn is due. If other workers are due within minutes, batch.
- One card per worker. At about 150k context, or at card end, a worker returns its report, and the next card starts a fresh worker from a packet, never a resumed one.
- Commit the integration branch after every landing, and write a one-line bench state note before any long wait. If the folder isn't a git repo, `git init` before the run.
- End every lead turn with the `status` shape from the file `artifacts.md` in the skill `house-rules`.
- When a long run lands or fails and the user may be away, send one push (PushNotification on Claude Code) under 200 characters.

## The wave rule

Only cards whose blockers have landed get dispatched, at every level. The board holds the current wave only. The full graph stays in the chart.

A worktree starts from the last commit, so a card started early works without the code it depends on. A blocker has landed when its code is committed on the integration branch, not when its worker reports done. Put a card on the board only then. Mark a board card done at landing, so nothing downstream reads it as ready too soon. At solo, the rule means working cards in graph order.

## At each level

The steps stay the same. These parts change.

| Level | Board | Start a card | Check | Land |
|---|---|---|---|---|
| hub | The hub's board, current wave only | Isolated write run on its own branch, packet as the message, `return: final message` | Another kind in read mode. Its packet names the worker's branch and folder | Merge the branch |
| host | bench `board.md` | Subagent on its own worktree and branch, packet as prompt, `return: final message` | First rung of the check ladder that's here, usually a fresh subagent | Merge the branch |
| herdr | bench `board.md` | One workspace and agent per card, on its own worktree. Watch with the see team move | Other-kind workspace | Merge the branch |
| solo | bench `board.md` | Nothing to start. Work cards in graph order on one branch | Clean second pass, labelled `self`. Say no independent check ran | Already there |

On hub, host and herdr, the packet tells the worker to confirm `base`, rebase if it's wrong, merge the integration tip before reporting, and commit its work on its branch. The hub stops a run at its budget. On host and herdr, budgets are stop conditions in the brief, and nothing enforces them.

## Limits

Size each wave to the level's limits in the file `levels.md` in the skill `house-rules`. A wave wider than the level allows goes out in turn as slots free up.

A refusal or a stopped run comes back to the lead with its reason.

| What comes back | Do |
|---|---|
| Too many active agents | Wait for a result, then dispatch again. This isn't a failure |
| A loop brake, pause or hold | Dispatch nothing. Report what has landed and what remains, and wait for the user |
| Timed out or over budget | Its agent was stopped mid-turn. Split the card, or re-dispatch with more budget |
| Checker timed out or sent nothing | Not an approval. Re-dispatch, or drop a rung of the check ladder |
| Two rounds of changes spent | Show the user the notes and leave the retry to them |
| Ended with no report | Read its last reply, then steer it or re-dispatch with a sharper packet |
| Failed | Fix the packet or reslice the card |
| No other kind available | Take the next rung of the check ladder before landing |

A lead with a lead above it sends gates up under `Needs OK`.

## Done when

- Every chart card is landed and committed on the integration branch, dropped with a reason, or named as blocked with its reason.
- Each commit names its card, and no card started before its blockers were committed.
- Each landed card has a check result with its `independent` value, and its `Accept` checks ran on the integration branch.
- The whole-branch report from the skill `finish-line` exists, and its fixes came from one worker and were checked again.
- Every outward step ran under an OK, and any step without one is listed as left.
- The worktrees left for the user are listed.
- The closing report answers every `Asked` item with met, partly or not, keeps its labels, and names the level.
