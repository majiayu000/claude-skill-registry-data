---
name: cancel-ralph
description: Stop the Ralph loop of this session. Then the Stop hook lets the session stop.
disable-model-invocation: true
---

# Cancel the Ralph loop

Run this command:

```bash
"${CLAUDE_PLUGIN_ROOT}/plugin/hooks/ralph.py" cancel --session "${CLAUDE_SESSION_ID}"
```

The command removes the state file of this session (`~/.claude/kairos-ralph/<session id>.json`). Then the `Stop` hook lets the session stop.

Give the output of the command to the user. The output names the tasks of the loop and the iteration. If no loop is active, the output says so.

The cancel does not change the items. A task keeps its column and its notes. If a task is in Active and its work is not complete, tell the user its short code.
