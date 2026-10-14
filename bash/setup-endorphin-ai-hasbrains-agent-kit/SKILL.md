---
name: setup
description: Turn on the statusline-kit status line. Use when the user asks to set up, enable, switch on or fix the status line from the statusline-kit plugin, or to show or hide its git information.
---

# Turn on the status line

The plugin's hooks already record every run. The status line itself is the one thing a plugin
cannot switch on: Claude Code reads `statusLine` only from the user's own settings. This skill
adds that entry.

## Steps

1. Check `jq` is installed (`command -v jq`). The status line and the hooks need it. If it is
   missing, tell the user how to install it (`brew install jq`, `apt install jq`) and stop.
2. Check the script exists: `${CLAUDE_PLUGIN_DATA}/statusline.sh`. The plugin copies it there at
   the start of every session, so it survives plugin updates. If it is missing, copy it now:
   `mkdir -p "${CLAUDE_PLUGIN_DATA}" && cp "${CLAUDE_PLUGIN_ROOT}/statusline.sh" "${CLAUDE_PLUGIN_DATA}/statusline.sh"`.
3. Read `~/.claude/settings.json`. If it already has a `statusLine` entry that is not this one,
   show it to the user and ask before replacing it.
4. Ask whether to show git information: nothing, everything (`--git`), or a comma list of
   `repo`, `branch`, `worktree` (`--git repo,branch`).
5. Set the entry, keeping everything else in the file as it is:

   ```json
   "statusLine": {
     "type": "command",
     "command": "bash \"${CLAUDE_PLUGIN_DATA}/statusline.sh\"",
     "refreshInterval": 2
   }
   ```

   Append the git option inside the command when the user chose one, for example
   `bash \"${CLAUDE_PLUGIN_DATA}/statusline.sh\" --git branch`.
6. Tell the user the status line appears after the next message, and that `/statusline-kit:setup`
   can be run again to change the git option.

## Do not

- Do not also run the kit's `install.sh`: it installs the same hooks into `~/.claude`, and every
  run would then be recorded twice. If `~/.claude/hooks/subagent-stop.sh` exists, tell the user
  that both are installed and that one of them has to go.
- Do not write anywhere except `~/.claude/settings.json`.
