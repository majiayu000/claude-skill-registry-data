---
name: woz-decision-map
description: "Recover the decisions and open questions from this session's work and post them as review comments on its pull request. TRIGGER on 'decision map', 'what did we decide', or /woz-decision-map."
argument-hint: pull request number (optional)
arguments: pr
---

# Decision map

The CLI owns the sequence and you relay it. Every command prints the next one — run exactly that, never a command you inferred.

Start:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/decision-map.js" prepare $ARGUMENTS
```

If `CLAUDE_PLUGIN_ROOT` is unset in your shell, fall back to `wozcode decisions prepare`.

Add `--pr <number>` if the author names a pull request; otherwise the CLI resolves the one for this branch.

Rules:

- When the output asks you to spawn subagents, spawn one per listed prompt file, each with that single instruction and nothing else, on the model the output names. Do not open the input or output files, and do not answer a stage yourself.
- When a command exits asking for confirmation, show its message to the author and stop. Re-run only with the flag it named, and only after they say so.
- When a stage comes back malformed the CLI says so and asks for the same stage again — re-spawn its subagents and re-run the ingest it prints.
- Show the numbered preview to the author verbatim. They may drop items (`--drop 2,5`) or unhide one (`--enable 7`); pass those through unchanged.
- Nothing is published until the author confirms. Never add, reword, or fill in an item yourself — everything published is theirs.

