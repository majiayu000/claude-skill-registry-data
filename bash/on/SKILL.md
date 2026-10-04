---
name: wispr:on
description: Start the Wispr Flow voice monitor for this session. Each dictation you speak will arrive as a Monitor notification.
---

If `~/.claude/wispr-config.yml` does not exist, suggest running `/wispr:setup` first, then continue anyway — `monitor.sh` will create a default config.

Read `~/.claude/wispr-config.yml` if it exists. If `wispr_app` is set, pass it as an env var:

```
WISPR_APP=<wispr_app value> bash $CLAUDE_PLUGIN_ROOT/scripts/monitor.sh
```

Otherwise start without it:

```
Monitor(
  command="bash $CLAUDE_PLUGIN_ROOT/scripts/monitor.sh",
  label="Wispr Voice"
)
```

Once the monitor is running:

- Wispr Flow transcriptions prefixed with the trigger word (default: `claude`) arrive as notifications. The trigger word is stripped before the text reaches you.
- Treat each notification as a spoken message from the user. Respond normally.
- To speak a response aloud: `bash $CLAUDE_PLUGIN_ROOT/scripts/speak.sh "your reply"`
