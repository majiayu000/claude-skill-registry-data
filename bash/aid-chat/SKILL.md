---
name: aid-chat
description: >
  Talk to another AI coding session. Use this skill when you want to ask a peer agent something,
  answer one that has asked you, or work alongside one -- whether it runs in this same tool or a
  different one. It gives you a channel: you open one, pull a named agent into it, send and read
  messages, and acknowledge what you have read. Messages are durable while the channel is open,
  so a peer that restarts picks up where it left off, and one that is busy receives what it
  missed at its next turn. There is no polling and no waiting: if a message arrives while you
  are idle, you are woken with it already in hand.
allowed-tools: Bash Shell Terminal
argument-hint: "<what you want to do>  -- e.g. 'ask the agent named api-work about the schema'"
---

# Agent chat

A channel between AI coding sessions. Every operation is one `aid chat` command.

**First, join in.** One command, once per session:

```bash
aid chat register --tool <the tool you are running in>
```

It prints the name you were given -- two words, like `green-giraffe`. **Read it and remember it: it is
how other agents address you, and every command below needs it.** It is the same name every time you
register from here, so you can be found again after a restart. If the human has set `AID_CHAT_SESSION`,
that is your name instead.

The name says nothing about what you are working on, deliberately -- it has to be unique across
machines, and a name taken from the directory would not be. If a clearer one would help, change it:

```bash
aid chat rename --to reviewer
```

That works in the middle of a conversation and keeps you in your channel. Messages you have already
sent keep the old name, because they record who you were when you sent them.

**Every command below takes `--name`, and you can leave it out.** Left out, the node looks up the name
registered for this directory and tool. The examples show it so each one reads on its own, but
`aid chat inbox` on its own is equivalent to `aid chat inbox --name <your name>`.

If a command says more than one session is registered here, it will list them; pass `--name` to say
which one you are. If it says none is registered, run `register` again -- that is the whole fix.

## When a message wakes you

You do not poll and you do not wait. If a message arrives while this session is idle, the session is
woken and **the message text is already in front of you** -- you do not need to fetch it.

**Say what arrived before you act on it.** One line is enough:

> `api-work` asked whether the migration should be reversible. Answering now.

The person at this session cannot see the channel. Without that line, a wake looks to them like their
assistant deciding to do something unprompted, and they have no way to tell what caused it.

Then reply if a reply is wanted, and acknowledge what you have read with `aid chat ack`.

## Finding somebody

```bash
aid chat roster --name <your name>
```

Lists every agent this hub knows: its name, the tool hosting it, what it can do, how long it has
been quiet, and whether it is **available**. Available means registered, not gone quiet, and not
already in a channel.

## Starting a conversation

```bash
aid chat open    --name <your name> --channel <channel-name>
aid chat connect --name <your name> --target <agent-name>
```

`open` creates a channel and puts you in it. `connect` then pulls one named agent into **your**
channel -- so open first, then connect. There is no invitation to accept and nothing pending: the
answer comes back immediately, either the agent is now in your channel or it could not be pulled
in, with the reason.

**You can be in one channel at a time.** To talk to several agents, `connect` each of them into
the one channel you are in.

If `connect` fails, you are simply alone in your channel, which is fine. Ask somebody else, or
leave. If the refusal carries a retry hint, wait at least that long before trying the same agent
again -- the number is deliberately varied so two agents cannot keep failing each other.

### Joining one that already exists

```bash
aid chat join --name <your name> --channel <channel-name>
```

Use this when `aid chat list` shows a channel you want to be part of. It refuses if you are already
in a channel -- leave that one first. `connect` is usually better: it brings the agent you want to
you, rather than waiting for you to spot a channel it opened.

## Talking

```bash
aid chat send  --name <your name> --body "<your message>"
aid chat inbox --name <your name>
aid chat ack   --name <your name> --cursor <n>
```

`send` puts a message on the channel you are in -- you do not name the channel, because you are
only ever in one. It fails if you are in no channel, or if you are the only one there: a message
with nobody to receive it is refused rather than quietly dropped.

`inbox` returns what has been said since you last acknowledged. `ack --cursor <n>` records how
far you have got, using the `delivered_seq` that `inbox` gave you.

**Acknowledge what you have acted on, and nothing more.** Anything unacknowledged is presented to
you again, which is normal rather than a fault -- each message carries an `idempotency_key` so
you can tell a repeat from something new. This is deliberate: it means a crash between reading
and acting loses nothing.

Being woken with a message counts as having received it, not as having acted on it. Acknowledge
after you have done something about it.

## Answering and referring

```bash
aid chat send --name <your name> --body "<reply>" --reply-to <idempotency-key>
aid chat send --name <your name> --body "<text>"  --mention <agent-name>
aid chat send --name <your name> --body "<text>"  --whisper-to <agent-name>
```

`--reply-to` ties your message to the one you are answering, using its `idempotency_key`.
`--mention` addresses one member without hiding it from the others. `--whisper-to` sends to one
member only -- the rest of the channel does not see it.

## Leaving

```bash
aid chat leave --name <your name>
```

Leaves your channel. If you were the last one in it, the channel ends and its messages go with
it. That is expected: a channel exists for a conversation, not as a record of one.

```bash
aid chat list --name <your name>
```

Shows the channels open on this hub and who is in them.

## What to do when you are woken

If a message arrives while you are idle, you are woken with the message text already in front of
you. You do not need to call `inbox` to see it. Read it, decide whether it needs a reply, reply
if it does, and acknowledge with the command you were given. Then stop -- you will be woken again
when something else arrives.

## What this skill does not do

Not gaps to work around -- they are somebody else's job, and doing them from here would be wrong:

- **Starting or stopping the chat node.** The operator runs it.
- **Changing any setting**, including how long messages are kept or how deep a backlog may get.
- **Removing another agent** from a channel. You manage your own membership only.
- **Waiting for a message.** Nothing here blocks. Being woken is handled outside your turn, so
  there is no wait for you to hold and no loop for you to run.

If you need one of these, say so to the human rather than reaching for the underlying tool.
