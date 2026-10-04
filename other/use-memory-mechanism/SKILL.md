---
name: use-memory-mechanism
description: Use to start or resume work referencing the memory mechanism — find or create a work chunk for this repo, read prior handoff annotations, log decisions/gotchas during work, and leave a handoff annotation before finishing. Trigger when the user says "start work", "resume work", "log a task", "handoff", "what was I doing", or before beginning a fresh implementation session.
---

# UseMemoryMechanism — conventions for persisting important instructions

Using a mechanism to persist certain textual data between sessions is key for
agentic coding. This skill assumes there is an environment variable `AGENT_TECHNIQUES_MEMORY_MECHANSIM`
which will determine which of the guides in `guides/*.md` file is relevant for understanding
how to use the mechanism. Use the full guide to understand the exact way to invoke or use the
memory mechansim when starting, continuing, handing off, or exploring what specific work chunks
need to be understood. When in doubt you can read the full narrative guide, but the high level
feature sets listed below can give a way to search for the target you need within the guide.

## Find or start work

Look for the starting work or claiming work items within the guide to see how to surface what
are the currently slated things to work on. For example, the taskwarrior memory mechanism uses
the invocation below to list the already created work chunks related to the project.

```bash
task project:<repo> list
```

No task yet? Create one before writing code using the memory mechanisms create functionality.
For task warrior that looks like.

```bash
task add "<title>" project:<repo> +feature
task <id> start
```

## Read prior handoffs

When starting work, look to see if there are hand off messages persisted on
the work chunk in the memory mechansim or parent chunks. This involves
reading the annotations or metadata on the task or work chunk. These are the last
agent's (or your own past session's) notes. For taskwarrior this is

```bash
task <id> information
```

## Log as you go

As work progresses for a particular task or chunk, create annotations about
what happens like the following for taskwarrior.

```bash
task <id> annotate "decision: <choice> because <reason>"
task <id> annotate "gotcha: <non-obvious constraint>"
```

## Handoff before finishing

Always leave one of these before context closes, even mid-task:

```bash
task <id> annotate "handoff: done=<...>, next=<...>, traps=<...>"
task <id> stop
```

Task fully done:

```bash
task <id> done
```

## Reference design/plan docs in handoffs

If this task's work went through the superpowers `brainstorming`/`writing-plans`
skills, they'll have written a design and/or plan doc under
`docs/superpowers/specs/` or `docs/superpowers/plans/`. Point to those paths in the
handoff so a resuming agent doesn't have to rediscover them:

```bash
task <id> annotate "handoff: done=<...>, next=<...>, traps=<...>, docs=docs/superpowers/plans/<file>.md"
```

## Convention

Prefix annotations with `handoff:`, `decision:`, or `gotcha:` — nothing
else. This lets future agents `grep` the task's annotations for the kind of
context they need instead of reading everything.
