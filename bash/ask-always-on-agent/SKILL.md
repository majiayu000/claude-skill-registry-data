---
name: ask-always-on-agent
description: Reach Frank on his phone through an always-on paseo agent (coding-agent or personal-agent). Use when a question to the user has had no answer for 15 minutes, or when the user says to send a message, ask, or hand off work to the coding-agent, the personal-agent, or "the always-on agent".
---

# ask-always-on-agent

A coding CLI session lives in a terminal; Frank cannot see it from his phone. The always-on paseo
agents can be seen there: paseo's app runs on mobile, and a question an agent asks shows up in it.
So when Frank is away from the terminal, a CLI session reaches him by sending its question to an
always-on agent, which re-asks it in paseo. The always-on agent is a relay: it shows, it does not
judge or answer.

## When to use it

- **Unanswered question.** Your question tool returned with no answer (timeout, cancel, headless
  run), or the question has waited 15 minutes. This is the only time you message an always-on
  agent on your own. In a herdr pane you need not count: the `ask-watchdog` LaunchAgent
  (`~/coding-agent/devops/ask-watchdog/README.md`) relays a pane blocked on any dialog for 15
  minutes and types the answer back.
- **Explicit hand-off.** The user says to ask, tell, message or hand work to one of the agents.

## Which agent

| Agent | Topic | Runs on |
|---|---|---|
| `coding-agent` | engineering, coding, the fleet, products | mac-mini-m2, mac-mini-m6, dev-server-frank-lume, archs-mac-mini |
| `personal-agent` | Frank's personal life | mac-mini-m2 only |

For an **unanswered question**, pick by folder: a session under `~/personal-agent` sends to
`personal-agent`; any other folder sends to `coding-agent`. For an **explicit hand-off**, pick by
topic; when the topic is unclear or mixed, ask the user which agent before sending.

The script finds the agent by its label `keepalive=<name>` on this host's paseo daemon, and
follows the name to its home host (`ssh://mac-mini-m2` or `ssh://mac-mini-m6`) when it is not
here. It prints one stderr line when it does. Pass `--host <endpoint>` to choose the daemon
yourself; then it never falls back.

## The script

```bash
~/.agents/skills/ask-always-on-agent/scripts/ask-always-on-agent [--host <endpoint>] <name> [paseo send options] [prompt]
```

Everything after `<name>` goes to `paseo send` unchanged. The script waits until the agent is idle
again, through any question the agent asks in paseo, then prints the agent's tagged reply.
There is no timeout. `--prompt-file <path>` sends a long message; `--image <path>` attaches a
screenshot; `--behavior interrupt` cuts into a busy agent (default `steer` queues behind its
current turn); `--no-wait` returns at once, then `paseo logs -f <id>` shows the reply.

## Escalate an unanswered question

1. Write the message from this template, with the question and its options verbatim:

   ```
   Show Frank this question with your AskUserQuestion tool, verbatim with these options.
   Do not answer it yourself. Reply with only his answer.

   Context: <what this session is doing, in one or two sentences>. Folder: <cwd>.
   My recommended option: <label>.

   Question: <the question>
   Options:
   - <label>: <description>
   - <label>: <description>
   ```

2. Send it, with `--prompt-file` for a long one:

   ```bash
   ~/.agents/skills/ask-always-on-agent/scripts/ask-always-on-agent coding-agent --prompt-file /tmp/question.md
   ```

   The command returns when Frank answers in paseo; that can take hours. Wait.

3. Take the reply as Frank's answer and continue. Your next message to the user says, in full:
   the question waited 15 minutes, so it was relayed through `<agent>` on `<host>`; Frank
   answered it through paseo (mobile); and this is the answer you are acting on.

4. If the command fails or the reply is empty, stop and keep waiting for the user. Do not take
   your own recommended option.

Every message gets a reply tag at its end, and the script prints only the reply that begins with
that tag. The always-on agent is a shared inbox, so an untagged reply is someone else's turn.

## Hand off a task

Send the task as a plain message, no relay wording. The agent runs in `bypassPermissions` and
acts on it. Relay its reply to the user as written, with one line naming the agent and host.
End the message with the address the agent can reach you at later:

```
Reply-to: herdr <hostname -s> <$HERDR_PANE_ID>     # when HERDR_ENV=1
Reply-to: tmux <hostname -s> <$TMUX_PANE>          # otherwise
```

## Reverse channel

`paseo send` goes one way. Every coding CLI session runs in herdr or tmux, so the always-on
agent reaches a session by typing into its pane, at the `Reply-to` address from the hand-off.
Both commands work from the paseo agent, which runs in no pane: herdr and tmux find their
sockets by default path for the same user.

- **herdr**: `herdr agent prompt <pane> '<text>'`. When in doubt that the pane still hosts the
  agent, `herdr agent get <pane>` first; a closed pane errors `agent_not_found`, and pane ids are
  never reused.
- **tmux**: `tmux send-keys -t <pane> -l '<text>'; sleep 0.3; tmux send-keys -t <pane> Enter`.
  The pause stops a TUI from swallowing the Enter.
- **Another host**: prefix either command with `ssh <host>`, using the `~/.ssh/config` alias.

The text lands as typed input and queues behind a busy agent's current turn. Keep it to one
line, or write a file and send its path with one line saying what to do with it.

As the always-on agent: answer a hand-off at its `Reply-to` address this way. A hand-off with no
`Reply-to` gets only the reply to its own message.

## If it fails

- `no agent labelled keepalive=<name>`: the keepalive job is not loaded on that host
  (`launchctl list | grep keepalive`), or the daemon is down (`paseo daemon status`). See
  `~/coding-agent/devops/paseo-keepalive/README.md`.
- `more than one agent labelled`: the job made a duplicate; archive one by hand, same README.
- `Cannot connect to daemon` with `--host`: the endpoint must be `host:port`, `ssh://host`, or
  a pairing URL.
