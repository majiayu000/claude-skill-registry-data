---
name: logCatalog
description: Find and run any log command over MCP with three tools, the way treg's catalog works (rule 163). logSearch the job in plain words, logGet the id for its inputs and a call that works, logCall it. Use when you need a log command and don't know which tool it is.
---

# logCatalog

Three tools reach every log command: find it by the job, read it, run it.

## 1. Find it: `logSearch`

Say what you want done, in plain words. A platform name narrows it.

```
logSearch { "query": "send a dm on x" }
```

```
query: send a dm on x
verdict: strong
results[8]{id,summary,acts}:
  twitter.dm,"Send one approved direct message on X, …",live
  twitter.dms,"Read an X account's direct messages, …",no
  …
help[1]:
  - logGet {"id":"twitter.dm"}   (its inputs and a call that works)
```

- **verdict:** `strong` means the first result does every word. `closest` means none does all of it, and these do most of it. `none` means nothing fits: the near misses show which words they missed. Say the job differently, or with fewer words.
- **acts:**
  - `no` only reads.
  - `live` has a live run that acts on the platform.
  - `write`, `browser` or `delete` change local data, Twenty or the account's browser.
  - `terminal` is a prompt the owner runs in a terminal, never over MCP.

## 2. Read it: `logGet`

```
logGet { "id": "twitter.dm" }
```

It answers:

- **inputs**, required first, each with its type and a note;
- **call**, a `logCall` line that works, and **live**, the same as a live run, when the command has one;
- **cli**, the same command in a terminal;
- **guide**, the command's guide, to load before first using it;
- **rules**, the AGENTS.md rules the command falls under.

A wrong id gets `didYouMean`.

## 3. Run it: `logCall`

```
logCall { "id": "twitter.dm", "inputs": { "account": "yourAccount", "userId": "12345", "text": "hello" } }
```

- It runs the command through its own tool, so every check still applies: the voice gate, the play, claims, the governor and jobs.
- An unknown input is refused by name, with the inputs it takes. Nothing runs.
- `live: true` runs the live form. It needs `confirmLive: true`, and only when the owner asked for this live run (rule 8).
- `confirmBypass: true` is only for a run outside the account's hours that the owner asked for.
- A long run comes back as a job after `waitMs`. Follow it with `jobStatus`, and watch `tail -f ~/.logCli/mcp/<day>.log` while it runs (rule 26).

## Ids

An id is `<platform>.<command>.<form words>`: `twitter.dm`, `twitter.queue.build`, `facebook.read.members`, `discord.session.check`. A command for any platform has no platform: `localAccount.add`, `search`, `inbox.claim`.

Each command's own tool, such as `twitterDm` or `twitterDmLive`, still works. `logCall` reaches the same tools.
