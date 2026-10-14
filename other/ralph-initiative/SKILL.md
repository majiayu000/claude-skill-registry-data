---
name: ralph-initiative
description: Run the open tasks of a Kairos initiative in a Ralph loop, in the sequence of their blocks edges.
argument-hint: "<initiative short code> [--max-iterations N]"
disable-model-invocation: true
---

# Ralph loop: the tasks of an initiative

The arguments are: `$ARGUMENTS`

## 1. Read the initiative and its tasks

1. Call `get_item` with the initiative short code (the form is `PREFIX-I-NNNN`). If `get_item` does not find it, tell the user, and do not start the loop.
2. The result gives the children of the initiative. Call `get_item` for each child task. Ignore a task in a done column. For each other task, record:
   - its short code;
   - its column;
   - each item that blocks it, and if that blocker is done (`get_item` marks a done blocker `[done]`).
3. A task can have a different repository from this checkout. Tell the user, and do not give that task to the script.

## 2. Start the loop

Give the tasks to the script as JSON on stdin, sorted by short code. The script puts each blocker before the task that it blocks. It skips these tasks:

- a task in the Blocked column;
- a task with a blocker that is not done and not in the list;
- a task in a cycle of `blocks` edges, or a task after a skipped blocker.

```bash
"${CLAUDE_PLUGIN_ROOT}/plugin/hooks/ralph.py" start-initiative --session "${CLAUDE_SESSION_ID}" $ARGUMENTS <<'JSON'
{"tasks": [
  {"code": "PREFIX-T-0001", "column": "Todo", "blockers": []},
  {"code": "PREFIX-T-0002", "column": "Todo", "blockers": [{"code": "PREFIX-T-0001", "done": false}]}
]}
JSON
```

The fields are `code`, `column` and `blockers` (each with `code` and `done`). The script refuses each other field. If the command fails, show its message to the user and stop. The loop did not start.

The script writes the state of the loop to `~/.claude/kairos-ralph/<session id>.json`, outside the repository. The `Stop` hook of the plugin reads this file and gives you the next step at each stop.

## 3. Do the tasks

The output of the script gives the tasks in sequence and the procedure. It also gives the skipped tasks and the reasons. Write the skipped tasks and their reasons on the initiative with `edit_item`.

Do the tasks in that sequence. Each task goes through each step of `/kairos:implement`:

- the repository check;
- Todo, then Active;
- progress notes on the item;
- the completion gate, with evidence for each acceptance criterion;
- the review, the commit, then Completed.

Follow the commit rules of the repository and of the user. Every few tasks, write a short progress note on the initiative with `append_note`.

The loop ends in one of three ways:

- **Each task in the sequence is in Completed.** End your reply with `<promise>ALL TASKS COMPLETE</promise>`. Do not move the initiative: the user reviews it.
- **A task stops the loop.** Do not guess. Stop when one of these conditions occurs:
  - a task is in the Blocked column;
  - a task has no acceptance criteria that you can check;
  - the work needs a design decision, a push, a deploy, or a change in a different repository.

  Write the reason on the task and on the initiative. Give the reason in your reply. End the reply with `<promise>LOOP STOPPED</promise>`.
- **The loop gets to the iteration limit** (`--max-iterations N`, no limit by default). The hook then lets the session stop.

Write a promise only when it is true. To stop the loop at a different time, the user runs `/kairos:cancel-ralph`.
