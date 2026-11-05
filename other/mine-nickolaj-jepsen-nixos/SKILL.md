---
name: mine
description: Improve a skill, tool, CLI or hook from how it actually went in your past Claude Code and pi sessions. Findings are routed to /brainstorm, /grill-me or building them.
disable-model-invocation: true
argument-hint: "<target>"
---

This skill finds what to change in a target and why, from how it went in past sessions.

- The argument names a target: a skill, a pi extension or tool, a CLI, or a Claude Code hook or setting.
- With no argument, ask for a target. To review one session across everything it touched, use `/retro`.
- It writes no code unless the user picks findings to build at the end.
- It writes exactly one file, the findings file (see The file), and ends with a chat summary.

## The reader

- `python3 <skill-dir>/scripts/sessions.py` (substitute this skill directory's absolute path) reads Claude Code, its work profile and pi transcripts, read-only.
- `--help` lists its subcommands and flags, run windows and answer classes.
- Each call scans every session, so it takes seconds to a minute.

## Privacy

- Transcripts are private. Never write condensed transcript text to disk.
- Never quote a secret, and quote a phrase rather than a passage.
- Runs marked work profile, and memories under `~/.claude-work/`, are paraphrased, never quoted.
- Every subagent brief repeats these rules.

## The target

Turn the target into matchers for `runs`, using the recipe for its kind. Before judging a specific system, read the docs page the repo's agent instructions point to for it.

- Skill: `--skill <name>`.
  - A run ends at the prompt that invokes another skill, so it often includes work done after the skill's own part. Its error and denial counts are therefore pointers, not verdicts.
  - `via` says whether you asked for the skill or the model reached for it.
  - The `body` path shows which copy ran: the repo's deployed skill, an account-synced copy, or a plugin's.
  - `ver` is the commit that introduced that body text in the repo given by `--repo` (default: the cwd's); `~` marks a near match.
- Question-asking skill: the header splits answers into recommended, other (another option beat the recommendation), no-rec, custom and multi. Read the overall rates first. Per question header, only when headers recur:
  - A header almost always answered with the recommendation is a decision the skill should state rather than ask.
  - One often answered custom is missing an option.
  - One where another option often wins has a wrong recommendation.
- pi extension or tool:
  - Read the extension's source for the tool names it registers, and pass one `--tool` per name.
  - Calls made from inside `codemode` count.
  - The header reports how many pi sessions offered the tool and how many called it. Offered but never called is a description or existence problem.
- CLI: `--cmd <binary>`, plus `--tool` for any harness tool that wraps it (find it in the repo). `--help` calls and an error followed by a retry are discoverability signals.
- Hook or setting: `--text <regex>` on its distinctive output, such as its block message or script name.
  - The header counts denials by kind, for Claude Code only. In pi, read the matched calls' results.
  - A blocked call followed by a rephrased retry of the same intent is likely a false positive.
  - The same denial repeating suggests a missing allow rule.

## The file

- The findings file is `findings/<target>.md` in the agent notes of the project the target belongs to.
- The user's instructions say where agent notes live and what a project is. Without them, the notes are `.agents/notes/` in the repo and the project is the repo; write a `.gitignore` containing `*` there first.
- Apart from that `.gitignore`, the findings file is the only file a run writes. Subagents return their notes in their reply and write no files.
- Never commit it.
- If it exists, this is a rerun. Read it first, pass `--since <its date>` so only newer runs are read, and update the counts of the findings already there.

## Gather

1. `runs <matchers>` gives the signal header and one line per run. Read the header before any run.
2. Run `work --path <target's paths> [--mention <name>]`. It returns your typed turns from the ~10 most recent sessions that edited or discussed the target.
   - These record what was decided and why, and the complaints you stated.
   - They are context, not constraints. A finding may go against one only when that improves the end result, and then it says so with `Reverses:`.
3. Feedback memories that mention the target are corrections someone already wrote down. Look in Claude Code's `projects/*/memory/` and pi's memory store.
4. Read the target's own source and docs.
5. `git log` on the target's paths gives the date of its latest change.

## Read the runs

- Read at most 40 runs: the most recent, keeping at least a few from each version seen. Say how many you left unread.
- With about 8 runs or fewer, read them inline with `runs <matchers> --show all`.
- With more, first print one line naming how many subagents you are about to start. Then hand batches of about 8 to fresh subagents on a cheaper model than yours: `model: "sonnet"` in Claude Code, while pi's subagent roles already lock a cheap one.
- Give each subagent:
  - the target and a few lines on what it is meant to do;
  - its run ids;
  - the reader command to run itself (`runs <matchers> --show <id>,<id>`). `--show` stops at 150 lines per run; `--max-lines` raises it when a run is cut before the target's part ends;
  - the privacy rules above.
- Never paste transcript text into a brief.
- For every run, the subagent returns:
  - First failure: the first point where the run went worse than it should have, in one line, with its turn number (`#n`); or "clean".
  - Next: what the user did once the target's part was done, which is often well before the run's `[ended]` line.
  - Not the target's fault: harness or environment problems the run hit.
- In an interview skill, "yes", "no" and letters are answers, not corrections. A correction is the user redirecting, repeating themselves, rejecting the approach, or interrupting.

## Label with the user

- Group the first failures into named categories.
- Ask one question round, using the harness's question tool when every question is a short pick (pi `ask_user_question`, Claude `AskUserQuestion`). Ask about:
  - the runs whose note you are unsure of, each with its note and a one-line paraphrase of the moment;
  - the category names, and any merges you propose.
- Fold the answers in before writing.

## Findings

For each category:

- Evidence: how many runs it hit out of all of them, the session ids, and a short quote or paraphrase. When every run behind it predates the target's latest change, mark it "possibly fixed".
- Layer: where the fix belongs.
  - the target's own text or scripts;
  - the harness or an extension, through the harness's own extension points rather than patches to its built-ins;
  - agent instructions or memory;
  - the environment.

  A cause shared with other targets is never a fix to this one.

- Fix: what to change, a Size of S, M or L, and a Next: `/brainstorm` when the approach is open, `/grill-me` when it holds decisions, or build.

Two more kinds of finding come from the data, not from failures:

- Desire paths: a follow-up most runs share becomes a step the target offers itself. A tool-call sequence the agent works out again in most runs becomes a bundled script.
- Signal findings: what the header's numbers say on their own, such as the readings under Question-asking skill or a tool that is offered but never called.

A failure seen in one run is an anecdote, not a finding. Rank findings by the runs affected and what each failure cost: corrections, interrupts, abandoned runs.

## Write

Write the findings file. On a rerun, edit it in place.

```markdown
# Findings: <target>

<date> · <N runs (by source), M sessions, date range> · versions seen: <…> · latest change: <sha date>

## Findings

### 1. <category>

<What goes wrong, in 1–3 sentences.>

- Evidence: <k of N runs>; <session ids>; <quote or paraphrase>
- Layer: <layer> · Fix: <the change>
- Size: S · Next: build · Reverses: <decision, date> (only when it does)
- Status: <blank, or picked and where it went>

## Desire paths

- <what follows the runs, or what the agent keeps working out>: <k of N> → <exit or script>

## Anecdotes

- <one-off>: <session id>

## Rejected

- <title>: <one-line reason>
```

Then end with a chat summary holding only:

- the findings file's path;
- the counts ("5 findings from 34 runs");
- one line per finding (`1. <category> · <k/N> · <S|M|L> · <build|/grill-me|/brainstorm>`), with the route last;
- last, the top pick, in a sentence.

## Pick

The user replies by number or in free text.

- Merge, refine or question: answer, and update the findings file when a finding's content changes.
- Build ("do 1, 3"):
  - If a picked finding's Next is `/brainstorm` or `/grill-me`, ask once whether to build it anyway or route it first.
  - Then build them in this session one at a time, run the repo's checks, and mark each one done in the findings file.
- Any other pick: restate the finding as a seed (what, evidence, fix) and name its next command. Mark it picked in the findings file.
