---
name: ralph
description: Run Kairos tasks one by one in a Ralph loop, through the steps of /kairos:implement.
argument-hint: "<task short code>... [--max-iterations N]"
disable-model-invocation: true
---

# Ralph loop: a list of tasks

The arguments are: `$ARGUMENTS`

## 1. Read each task

Find the task short codes in the arguments (the form is `PREFIX-T-NNNN`). For each code, call `get_item`.

- If `get_item` does not find a code, add `--missing <code>` to the command in step 2. The script then refuses to start and names the code. Tell the user which code is missing. Do not start the loop.
- A task can have a different repository from this checkout, or be in the Blocked column. Then tell the user, and do not start the loop. The user removes the task from the list or makes it workable first.

## 2. Start the loop

Run this command. Give the arguments as they are, and add a `--missing` option for each code that `get_item` did not find:

```bash
"${CLAUDE_PLUGIN_ROOT}/plugin/hooks/ralph.py" start --session "${CLAUDE_SESSION_ID}" $ARGUMENTS
```

If the command fails, show its message to the user and stop. The loop did not start.

The script writes the state of the loop to `~/.claude/kairos-ralph/<session id>.json`, outside the repository. The `Stop` hook of the plugin reads this file. While the file is there, the hook does not let the session stop: it gives you the next step.

## 3. Do the tasks

The output of the script gives the tasks in sequence and the procedure. Do the tasks in that sequence. Each task goes through each step of `/kairos:implement`:

- the repository check;
- Todo, then Active;
- progress notes on the item;
- the completion gate, with evidence for each acceptance criterion;
- the review, the commit, then Completed.

Follow the commit rules of the repository and of the user.

The loop ends in one of three ways:

- **Each task is in Completed.** End your reply with `<promise>ALL TASKS COMPLETE</promise>`.
- **A task stops the loop.** Do not guess. Stop when one of these conditions occurs:
  - a task is in the Blocked column;
  - a task has no acceptance criteria that you can check;
  - the work needs a design decision, a push, a deploy, or a change in a different repository.

  Write the reason on the task and on its parent initiative. Give the reason in your reply. End the reply with `<promise>LOOP STOPPED</promise>`.
- **The loop gets to the iteration limit** (`--max-iterations N`, no limit by default). The hook then lets the session stop. A task can be in an intermediate state.

Write a promise only when it is true. To stop the loop at a different time, the user runs `/kairos:cancel-ralph`.
