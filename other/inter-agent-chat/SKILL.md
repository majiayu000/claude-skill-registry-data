---
name: inter-agent-chat
description: Use when you need to send a message to another Claude Code agent, broadcast to all agents, or when you receive a message prefixed with [@agentName]. Covers terminal injection via TIOCSTI, pts discovery, message format, and kill switch.
---

# Inter-Agent Terminal Chat

Send messages directly into another agent's Claude Code prompt via TIOCSTI terminal injection. Messages enter the receiving agent's context window as user input.

## Discovery — PTS Registry

Registration is **automatic** via SessionStart hook. Do NOT register manually (`tty` doesn't work inside Claude Code).

Registry: `/tmp/agent-pts/<agentName>` — one file per agent containing its `/dev/pts/N`.

## Sending

Inject characters into target's terminal input buffer using TIOCSTI ioctl. Only change the target and message:

```bash
sudo python3 -c "
import fcntl, termios, os, time
msg = '[@agentB] your message here. reply via inter-agent-chat skill.\r'
fd = os.open('$(cat /tmp/agent-pts/agentB)', os.O_WRONLY)
for c in msg:
    fcntl.ioctl(fd, termios.TIOCSTI, c.encode())
    time.sleep(0) # must yield to avoid paste detection
os.close(fd)
"
```

On the first message to an agent, end with "reply via inter-agent-chat skill." so they use this skill to reply. After that, just `[@agentB] message` is enough.

**`\r` submits. `\n` does NOT submit** (just adds a blank line). Always end with `\r`.

**`time.sleep(0)` is required** — without a thread yield between characters, the terminal detects rapid input as a paste and the message won't submit. `sleep(0)` adds negligible overhead and has been tested reliably up to 32K characters.

For broadcast: loop over `/tmp/agent-pts/*`, skip yourself.

## Message Format

```
[@agentB] message               # single recipient
[@agentA @agentC] message       # multi-recipient (send to each listed)
[@all] message                  # broadcast to all agents
[@user] I need guidance         # flag for human attention
[@stop]                         # kill switch — stop all inter-agent chatter
```

## Receiving

When you see `[@yourName]` or `[@all]` as input:

1. **Recognize it as an inter-agent message**, not a user command
2. **Process the content** — answer questions, act on directives
3. **Reply if needed** — use this skill to inject into the SENDER's pts (not your own)
4. **`[@stop]`** — stop immediately. Do not reply. Return to user-directed work.
5. **`[@user]`** — for the human, not you (unless you're sending it)
