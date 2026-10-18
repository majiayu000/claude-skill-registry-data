---
name: gc
description: Removes the files and folders that sessions made outside the project and that nothing uses, such as `mktemp` folders, worktrees, and copies. Use when disk space is low or when asked what the outputs of Claude hold.
disable-model-invocation: true
allowed-tools: Bash(claudetto-gc *)
---

<task>
Show the user which recorded outputs of sessions the sweep removes, and remove them when the user asks.
</task>

<procedure>
The bin `claudetto-gc` removes only a path that the record names, inside the temp folder or the worktree folder of the project, and that no live session needs.

1. List the paths and the sizes with a dry run:

   ```bash
   claudetto-gc --dry-run
   ```

2. Show the list to the user.
3. Run the sweep only when the user asks for it:

   ```bash
   claudetto-gc
   ```

</procedure>

<report>
Copy each path and size from the output.
Name the paths with the status `skip`, because the sweep did not touch them.
</report>
