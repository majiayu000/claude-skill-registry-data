---
name: jade-recipe-11-17-threadgroup-destroy
description: >-
  Removes the single ThreadGroup.destroy() call in jade.core.Runtime's shutdown
  path. JDK 16 terminally deprecated it and calls the destruction mechanism
  inherently flawed. Agent-mode recipe: the shard contract names the file; this
  document defines the transform and the diagnostic it must not silently drop.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-11-17-threadgroup-destroy — the destruction mechanism is flawed

The JDK 16 release note terminally deprecated `ThreadGroup.stop`, `destroy`,
`isDestroyed`, `setDaemon` and `isDaemon`, stating that "the API and mechanism
for destroying a ThreadGroup is inherently flawed" and that the methods "will be
removed in a future release".

Nothing is broken on JDK 17 — the call still works and JADE shuts down normally.
The rule exists because this is one of only two terminally-deprecated non-wrapper
surfaces in the tree, and it is a single statement.

## Scope of one task

You receive a shard contract. This rule is `blast_class: body-local`
(`parallel_safe: true`), one shard, one flag. Edit only that shard's
`editable_files`; `read_only_context` is read-only.

## The one site

`src/jade/src/jade/core/Runtime.java:297`, inside the shutdown path:

```java
//#MIDP_EXCLUDE_BEGIN
try {
    criticalThreads.destroy();
}
catch(IllegalThreadStateException itse) {
    myLogger.log(Logger.WARNING, "Time-critical threads still active: ");
    criticalThreads.list();
}
finally {
    criticalThreads = null;
}
```

`criticalThreads` is declared `private ThreadGroup` at `Runtime.java:73`. That
declaration is what separates this site from the two `a.destroy()` calls in
`DFAppletCommunicator.java:145` and `:149`, where `a` is a `java.applet.Applet`.
The rule's pattern is receiver-enumerated for exactly this reason: a line-based
regex cannot resolve the receiver's type, and the untyped `\.destroy\(\)` form
scored 0.33 against the 0.7 precision gate. Do not widen it.

## The transform

Remove the `destroy()` call. The `finally` clause performs the only effect that
survives — `criticalThreads = null`, which drops JADE's reference and lets the
group be collected once its threads have exited. Keep that assignment.

## What must not be lost quietly

The `catch` branch is the platform's only warning that time-critical threads are
still running at shutdown, and `criticalThreads.list()` is the only place that
names them. `IllegalThreadStateException` is thrown by `destroy()`, so deleting
the call deletes the diagnostic with it.

Preferred shape: keep an equivalent check that does not use a deprecated method,
for example testing `criticalThreads.activeCount()` and logging the same warning
plus `list()` when it is non-zero, then null the field.

If you cannot preserve the diagnostic without introducing a second deprecated
call, report `NEEDS_REVIEW` and say plainly that the choice is between keeping a
terminally-deprecated call and losing a shutdown warning. Do not delete the
`catch` body and say nothing.

`ThreadGroup.list()` is **not** deprecated and may stay.

## Verification

Recompiling in `jade-ant:17` with `-Xlint:removal` reports no
`[removal] destroy() in ThreadGroup` warning. A JADE container still shuts down
cleanly, the shutdown warning path is either preserved or explicitly reported as
lost, and all consumers PASS.
