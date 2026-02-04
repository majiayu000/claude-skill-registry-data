---
name: python-debug
description: Use when you need to inspect detailed execution flow of a Python program, stepping through functions and inspecting variable contents with pdb. Triggers include requests to debug Python scripts, trace execution, or inspect runtime state using the pdb debugger.
---

# Python Debug

- Run the script under pdb with `python -m pdb [script]`.
- Let the script run until an exception with `-c continue`.
- Run up to a given line X in the debugged file with `-c 'until X'`.
