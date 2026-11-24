---
name: ideas
description: "Turns one question on any subject into a short list of novel, useful and well-reasoned ideas by running a fixed ideation playbook as fresh helpers. Use when the user says 'give me ideas', 'what are my options' or 'how could I approach' a problem. Not for design options for a code change (exo:spec) or sourced research (exo:search)."
disable-model-invocation: true
argument-hint: "<question>"
metadata:
  author: exo
  tags: [ideas, brainstorm, ideation]
---

# Ideas

## Purpose

Turn one question into a ranked top 3 of ideas with a score, a prior-art verdict, a reason each could fail and a first test, written to report.md in a run folder.

## Prerequisites

The Agent tool, with the models opus and fable available (a rejected fable agent reruns on opus). A run starts about 14 helpers, about 9 more on a second round, and uses a noticeable part of the subscription limit. The helpers write under `~/.ideas/`, outside the project, so a permission rule `Edit(~/.ideas/**)` lets them save the prompts. The prompts the helpers read are the eight files in `references/`, named in the steps below.

## Instructions

Run the steps below in order for the question in `$ARGUMENTS`, else the question in the user's request in this conversation. When neither holds a question, ask the user for it once, then ask nothing more during the run. Answer in the language of the question.

### Setup

1. Make the run folder `$HOME/.ideas/<YYYY-MM-DD>-<slug>/`, where the slug is the question in ASCII, lowercase, words joined by `-`, at most 40 characters; when the folder exists add `-2` (then `-3`). Call its absolute path `RUN`.
2. Every step below is one fresh `general-purpose` agent with the model and effort given for it. Its prompt is: `Read <prompt file> and follow it exactly. Fill the placeholders {run} = RUN, {question} = <the question, verbatim>`, plus `{batch}` and `{n}` where the step gives them. Start agents of the same step in one message, and start the next step only after every file of the current step exists. When an Agent call with model fable is rejected, start it again with model opus and the same effort, and note this in report.md.
3. An agent writes its file and replies with the path. Run files are append-only: never edit a file an agent wrote, and write only the files marked "main session". When an expected file is missing, rerun that agent once. When a batch file is still missing, go on with the batch short and record that in report.md. When frame.md, diverge-avoid-obvious.md or revised.md is still missing, stop the run and tell the user which step failed.

### Round 1

1. Frame: `${CLAUDE_SKILL_DIR}/references/frame.md`, model opus, effort medium. Writes frame.md.
2. Diverge: three agents in one message, model fable, effort high, one per prompt: `${CLAUDE_SKILL_DIR}/references/diverge-overgenerate.md`, `${CLAUDE_SKILL_DIR}/references/diverge-avoid-obvious.md`, `${CLAUDE_SKILL_DIR}/references/diverge-unrelated-domain.md`. Each writes `diverge-<arm>.md` with 5 ideas under `## Ideas`.
3. Revise: `${CLAUDE_SKILL_DIR}/references/revise.md`, model opus, effort high. Writes revised.md with 5 ideas.
4. Pool (main session): read only the `## Ideas` section of each diverge-*.md file (not `## Scaffold`) and of revised.md. Write pool.md with all ideas left after merging duplicates into one idea, one `### I01 <title>` heading each (`I01` onward, no gaps) followed by its description. Order the ideas round-robin across the four sources, so that each batch of 5 in order holds at most two ideas from one source. Write which source made each idea only to methods.md, never to pool.md.
5. Prior art: split the pool IDs in order into batches of up to 5. Start one agent per batch in one message with `${CLAUDE_SKILL_DIR}/references/prior-art.md`, model sonnet, effort medium, `{batch}` = the IDs of the batch, `{n}` = 1, 2, 3 and so on, one per batch. Writes `prior-art-<n>.md`.
6. Score: start one fresh agent per batch in one message with `${CLAUDE_SKILL_DIR}/references/score.md`, model opus, effort high, the same `{batch}` and `{n}`. After the prompt add an empty line and `Read these files together in one message, with parallel calls: <prompt file>, RUN/frame.md, RUN/pool.md, RUN/prior-art-<n>.md.`, with full paths. Writes `score-<n>.md`.

### Pivot

Read the `Total:` lines. When round 1 is over and no idea has 14 or more out of 20, run one more round, and no more than that:

1. Write avoid.md (main session): the titles and descriptions of the 10 lowest-scored ideas.
2. Run the three diverge agents again. Add to each prompt: `Write your file as {run}/diverge-<arm>-r2.md instead, and also read {run}/avoid.md: none of your ideas may follow the directions of the ideas listed there.`
3. Merge each round-2 idea that duplicates a round-1 idea or another round-2 idea into one (drop it, keeping the existing idea). Append the `## Ideas` sections of the three `-r2` files to pool.md with the remaining ideas, numbered after the last round-1 ID and ordered round-robin across the three arms, and add their sources to methods.md.
4. Run prior art and score only for the new ideas, in batches of up to 5 with `{n}` = `1-r2`, `2-r2` and so on. The step 5 and 6 rules apply.

### Plan and report

1. Rank all scored ideas (both rounds) by `Total:`. Break ties on the `Novelty:` score, then the `Survival:` score. An idea whose prior-art verdict is `exists` ranks only on its total and shows its verdict.
2. Plan: one agent with `${CLAUDE_SKILL_DIR}/references/plan.md`, model opus, effort high, `{batch}` = the IDs of the top 3 in rank order. Writes plan.md.
3. Write report.md (main session) in the language of the question, but keep the labels below in English; only the text after a label may be in the question's language. Parts:
   - For each of the top 3, a section `## <rank>. <title>` with the lines `Score: <n>/20`, `Prior art: <exists|partly|new>`, `Why it could fail:` (the idea's `Breaks where:` line from its score file) and `First test:` (from plan.md, with its pass and fail rule), and the idea's description.
   - Then a table of all scored ideas: rank, ID, title, total, prior-art verdict, method from methods.md.
   - A line for each agent that stayed missing after its rerun.
4. Reply in the language of the question with the top 3 (title, score, one line each) and the path to report.md.

## Examples

Request: "ideas for getting more people to read our newsletter". The skill makes `~/.ideas/<YYYY-MM-DD>-ideas-for-getting-more-people-to-read-ou/`, runs the playbook, and replies:

```
1. <title>, 16/20: <one line>
2. <title>, 15/20: <one line>
3. <title>, 14/20: <one line>
Report: ~/.ideas/<YYYY-MM-DD>-<slug>/report.md
```

## Limitations

- The run is fully automatic: it asks nothing after the question.
- Ideas rest on the helpers' knowledge and a prior-art check, not on a sourced search; use /exo:search for sources.
- Run files are append-only, and a run folder is never reused: a second run of the same question gets `-2`.

## Troubleshooting

| Error | Cause | Solution |
| --- | --- | --- |
| An Agent call with model fable is rejected | The model is not available | Rerun it with model opus and the same effort, and note it in report.md. |
| An expected file is missing | An agent failed to write it | Rerun that agent once; a batch file still missing goes on short and is recorded in report.md. |
| frame.md, diverge-avoid-obvious.md or revised.md is missing after the rerun | A core step failed | Stop the run and tell the user which step failed. |
