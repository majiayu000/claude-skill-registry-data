---
name: language-port
description: >
  Rules for porting a live service to another language behind a parity harness.
  Use when you plan, split, specify or run such a port.
---

# Language port

A language port rewrites a live service in another language.
Traffic switches to the new version when it matches the old version.
A port takes the time of its longest parallel dependency chain plus its serial tail.
The serial tail has these steps:

- catch-up with the old main line;
- scale checks;
- trial and rehearsal;
- switch.

Each rule below keeps work off the serial tail, or keeps a failure out of it.

## Production-scale gate

- From the first stage, measure each candidate against the old version on a sandboxed copy of the production data.
- Measure these values:
  - boot time;
  - peak memory;
  - latency of the read endpoints.
- Run the sandbox with these limits:
  - the server writes only to its own copy of the production data;
  - no network access;
  - its own port;
  - its own process group, apart from the live service.
  The measurement then changes neither the production data nor the live service.
- Gate each stage and the switch on these values and on parity.
  A scale defect then shows in the stage that made it, and the switch does not discover it.
- When the old code caches a read, name that cache in the port spec.
  In the same case, add a test that counts the reads.
  Parity compares results only: a dropped cache keeps parity green and shows only at production scale.

## Libraries

- When a maintained library of the new language does a job, call that library.
- When a client reads an exact old-version format that no library produces, hand-write only the format layer.
  Leave its inner loops, such as scanning, escaping and compression, to a library.
- In each port spec, name the new language's library for each library that the old code calls.

A hand-written replacement passes parity and can run far slower than a tuned library.
These rules keep the speed of the libraries that the old version calls.

## The old main line during the port

- During the parallel phase, merge the old main line into the port branch so the final catch-up stays one small merge.
- When a merge turns a parity row red, give that row to the line that owns its module.
  The back-ports then run in the parallel lines, and the serial tail keeps one small catch-up.
- From the final catch-up to the switch, pause the scheduled jobs that change the main line.
- In the same window, hold behavior changes on the main line.
  The switch then runs on the baseline that the last checks measured.
- Run a step that moves the baseline before the checks that measure that baseline.
  A merge and a catch-up move the baseline.
  A check on a baseline that changes next measures code that the switch does not run.

## Task size and specs

- Size each port task so it lands in one pass, and list the old tests that the task ports.
- In each port spec, list the private interfaces and modules that the ported code calls.
  A small task with a complete list lands in one pass; a missing case or interface costs a second dispatch.
- In a merge spec, state the resolution of each two-sided change.
- Put into the spec each decision that the review can raise.
  A blocked review takes no answer, so an open decision costs a new dispatch.

## Tests and acceptance commands

- Give each time-dependent test an injected clock.
- Give each test and each acceptance command a timeout.
  A test that waits for wall-clock time, or hangs, holds every review that runs it.

Dispatch of ready tasks follows the manager rules in prompts/task_manager.md.
