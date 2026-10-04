---
name: jade-recipe-17-21-threaddeath-removal
description: >-
  Removes the catch of java.lang.ThreadDeath, which JDK 20 deprecated for
  removal after making Thread.stop() throw UnsupportedOperationException.
  Agent-mode recipe: the shard contract names the file; this document defines
  the transform and what must be preserved.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-17-21-threaddeath-removal — the exception can no longer be thrown

The JDK 20 release notes state both halves of this change: *"The ability to
'stop' a thread with the Thread.stop() method has been removed in this release.
The method has been changed to throw UnsupportedOperationException."* and, in
the next sentence, *"As part of this change, java.lang.ThreadDeath has been
deprecated for removal."*

`ThreadDeath` was only ever raised by `Thread.stop()`. From JDK 20 that method
throws instead, so nothing in the runtime can produce a `ThreadDeath` any more.
The catch clause is unreachable.

## Scope of one task

One site, one file: `jade/core/behaviours/ThreadedBehaviourFactory.java:404`.
`blast_class: body-local`.

## The transform

```java
catch (ThreadDeath td) {
    threadState = INTERRUPTED_STATE;
    myLogger.log(Logger.WARNING, "Threaded behaviour "+...+" stopped before termination");
    // ThreadDeath errors should always be propagated so that the top level handler can perform the necessary clean up
    throw td;
}
```

Delete the clause, and the comment that belongs to it.

Check the clause ordering before deleting. This `catch` sits between
`catch (Agent.Interrupted ae)` and `catch (Throwable t)`. Removing it means a
`ThreadDeath` thrown by hand — the only way one can still arise — would be
caught by the `Throwable` clause and set `ERROR_STATE` instead of being
rethrown. That is the only behavioural difference, it applies to a case the JDK
no longer produces, and it must be stated in the shard result rather than passed
over in silence.

## What the agent may not do

- Do not touch the `catch (InterruptedException ie)` or
  `catch (Agent.Interrupted ae)` clauses. They are live and unrelated.
- Do not reorder the remaining clauses.
- Do not delete the `catch (Throwable t)` clause that follows.

## Verification

`ant clean lib` inside `jade-ant:21` with `-Xlint:removal -Xmaxwarns 100000`
reports zero `ThreadDeath in java.lang has been deprecated and marked for
removal` warnings, down from one. The build exits 0 and all four consumers PASS.
`jrba` drives `TickerBehaviour` and `WakerBehaviour`, which run on the threaded
behaviour path this file implements.
