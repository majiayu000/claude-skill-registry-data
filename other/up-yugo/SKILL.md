---
name: up-yugo
description: >-
  Updates the local yugo-stack plugin by pulling
  ~/.cursor/plugins/local/yugo-stack. Use only when the user invokes /up-yugo.
disable-model-invocation: true
---

# up-yugo

Refresh the installed yugo-stack plugin on this machine.

## Do

1. If `~/.cursor/plugins/local/yugo-stack` is missing:

```bash
git clone https://github.com/Spice-Z/yugo-stack.git ~/.cursor/plugins/local/yugo-stack
```

2. Otherwise:

```bash
git -C ~/.cursor/plugins/local/yugo-stack pull
```

3. Refresh the Cloud Agent and Claude Code copies (real files, not symlinks):

```bash
~/.cursor/plugins/local/yugo-stack/setup.sh
```

4. Report the new `HEAD` short hash and which skills changed, if the pull output says so.

## After

Tell the user to reload Cursor (`Developer: Reload Window`) and to start a new Claude Code session if a skill does not show up there. A skill cannot reload the app.

Do not pull or commit the workspace copy of this repo unless the user asked for that too.
