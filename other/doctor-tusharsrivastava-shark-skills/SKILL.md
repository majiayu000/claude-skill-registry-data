---
name: doctor
description: Checks the tools that shark needs in this project (the mcp-debugger server, the debug adapter of each language, the code-health analyzers, rules, rows and baseline, the guard sections), shows one table, and installs the pinned fixes into the shark tool folder after a yes. Use when the user says doctor, check the shark tools, or after a new machine, a new language or a plugin update.
---

# Doctor

Run the check script. It installs and writes nothing:

```bash
node "${CLAUDE_PLUGIN_ROOT:-<directory of this skill>/../..}/skills/init/scripts/doctor.mjs"
```

It prints the tool folder and one row for each item: status (`ok`, `warn`, `missing`, `fail`), area, item, detail
and fix. Exit `0`: nothing is missing. Exit `1`: one or more items are missing or failed.

## The shark tool folder

Opengrep, Lizard and debugpy go in the plugin data folder of shark (`~/.claude/plugins/data/<plugin>-<marketplace>/`),
which plugin updates keep. The analyzers run from it with no PATH setup, and the project's own Python loads debugpy
from it through `PYTHONPATH`. Nothing goes into the system Python or the project environment, so a Python that is
"externally managed" (PEP 668) is not a problem. The only machine need is `python3` 3.9 or later with `venv`.

## Steps

1. Run the script. Show its table, with one row for each item, also each `ok` item.
2. When an item is not `ok`, group the fixes by scope (shark tool folder, npm cache, project, project file,
   machine) and recommend each one. Ask one time.
3. After a yes, run the approved commands one at a time, exactly as the script printed them. Never use `sudo`,
   `--break-system-packages`, or another install command. A `machine` fix is for the user: name it and continue.
   A project or project-file fix (rules, rows, `.gitignore`, the baseline) is a `/shark:init` step: run init for it.
4. Run the script again. Report the final table, each install with its version, and what is still not `ok`. Never
   call a tool ready when the last run did not show it as `ok`.
