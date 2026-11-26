---
name: flow
description: Turn a `log inspect` recording into a flow (rule 31) - a definition built from the recording, its documentation, an XState machine, the `log flow run` command and an MCP tool of its own - and run it on any account. Use after recording a procedure with inspect, when the owner says "make it a state machine", "run it on another account", "register it as an MCP", or to run a saved flow.
---

# flow

Record once, then run anywhere: recording → definition → docs → machine →
command → MCP tool.

## Hard boundaries

1. **Built from a recording, never by hand** (rules 25, 29). Each step's
   element is the role and accessible name the recorded snapshot gave it;
   each step's confirming request is the mutation the recorded step sent.
   A confirming request only proves the call happened. **What it answered
   decides the step** (rule 73): a step's `answers` name the call and what its
   answer must say (a value, what we sent, present, the account's home city,
   country or id), with the error code it raises, written from the request's
   doc ("What it sent and what came back"). Every step with a confirming
   request checks the field its request doc says it answers, and a test
   refuses a flow step that waits on a call without checking its answer. A
   streamed answer is read from its first part. The flow's doc shows every
   check, and recording the flow again keeps them.
2. **Dry run unless `--live`** (rule 8); over MCP, live is its own tool (the
   flow's tool name ending in `Live`), with confirmLive.
3. **Every gate** (rules 19, 35): a run is one launch through
   the inspect session, so every step is recorded again (snapshot,
   screenshot, HAR, rea) and mapped.
4. **No credential in a step or param**: sign-in is `signIn`/`code`,
   which read the private login.json; typed values are redacted in snapshots.
5. Run it live (rule 26): Monitor; every machine state prints.

## The routine

The example is a Facebook flow, `profileSetup`:

```bash
# 1. record (skills/inspect)
log inspect start --account <a> --url <url> --bypass --now
log inspect do click <ref> --live ...   # one step at a time
log inspect do stop

# 2. recording → definition + docs (params renamed from text1/file1)
log flow fromInspect ~/.logCli/runs/inspect/<run> --name profileSetup \
  --rename text1=firstName --rename text2=lastName --rename file1=profilePhoto --rename file2=coverPhoto

# 3. run it on another account (dry run first: lists the filled steps, opens nothing)
log flow run profileSetup --account <a> --set firstName=<first> --set lastName=<last> \
  --set profilePhoto=<path|url> --set coverPhoto=<path|url>
log flow run profileSetup --account <a> ... --live --bypass --now
```

Over MCP the same run is the flow's own tool with `account` and the params
by name, and its live twin with `confirmLive: true`. The CLI words
(`log flow run <name>`) are the same on every platform.

A failed step ends the run (`failedAt`): read that step's folder in the new
recording (rule 25), re-record the changed part with inspect, rebuild the flow.

## Deterministic steps (rule 79)

A step never guesses which control to press: `python/browser/controlMatch.py`
scores every visible control by role, then name, inside the step's dialog
(`within`). The exact requirements (and their error codes) are in
[docs/specs/flows.md](../../docs/specs/flows.md). A Dismiss button with no
accessible name is found by its text.

`fromInspect` writes what keeps a step deterministic:

- `within`: the dialog around the control in the snapshot before the step.
- `expect`: the call the step must cause, a mutation first, else a plain
  endpoint, else a `…DialogQuery`. The session waits for it, and the step
  fails without it.
- `answers`: what that call must say (rule 73), added from the recording's
  exchanges before the flow ships; `answers.test.ts` refuses a step with
  `expect` and no `answers`.

Before a flow's first click, fill, upload or location, `clearOverlays` reads the page
and presses Escape for each known overlay over it (`OVERLAY_CLEARS`,
`src/browser/flow/helpers/overlays.ts`), then reads the page again. One
still there after its Escape, or a clear call that answers otherwise, stops
the flow at that step with `overlayNotCleared`. An overlay no known state
names stays unknown, for SubQ to read (rule 73). A new overlay is added there
with its page state, fixture and answer.

When a platform changes a page, add its snapshot excerpt to
`python/fixtures/controls/` (no names, no page copy) and a case to
`src/browser/flow/controlMatch.test.ts`, so the next change fails a test, not
a live run.

Rebuild the platform's request docs after a run.

Facebook's flows, their tools, checks and overlays: `skills/facebookFlows/SKILL.md` (the facebookFlows guide).
