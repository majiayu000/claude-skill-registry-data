---
name: jade-recipe-17-21-finalize-removal
description: >-
  Removes Object.finalize() overrides in favour of the close or shutdown method
  each of them already delegates to. JEP 421 (JDK 18) deprecated finalization
  for removal. Agent-mode recipe: the shard contract names the files; this
  document defines the transform and the condition that forces NEEDS_REVIEW.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-17-21-finalize-removal — the finalizers are on the way out

JEP 421 terminally deprecated finalization in JDK 18: *"We will terminally
deprecate these methods in the java.base and java.desktop modules, by
annotating them with @Deprecated(forRemoval=true)."* The JEP's own advice is
the transform this rule performs — *"Maintainers of libraries and applications
that rely upon finalization should consider migrating to other resource
management techniques such as the try-with-resources statement and cleaners."*

Under `-Xlint:removal` on JDK 21 these are the tree's only escalations: four
sites that were plain `[deprecation]` on 17 and are `[removal]` on 21.

## Scope of one task

You receive a shard contract. This rule is `blast_class: body-local`
(`parallel_safe: true`). Edit only that shard's `editable_files`.

## The transform

Every finalizer in this tree is a wrapper around a cleanup method that already
exists. Delete the override and make sure the cleanup method is reachable on
the normal path.

`jade/core/management/JarClassLoader.java:207` — the body is `close();` followed
by `super.finalize();`. `close()` is public and already called by the owning
code. Delete the override outright; `super.finalize()` goes with it.

`jade/tools/SocketProxyAgent/Connection.java:239` — the body is
`if (!closed) { close(); }`. `close()` is package-private and is called on the
normal path. Delete the override.

`jade/tools/SocketProxyAgent/Server.java:143` — this one is different and must
be read before it is touched. The finalizer body is **live cleanup code on the
normal path**: `Server.java:119` calls `finalize()` explicitly from a `finally`
block. Do not delete the body. Rename the method to an ordinary name — `cleanup`
— keep the body verbatim, and change the `finally` block at :119 to call it.
An explicit call to `finalize()` is itself a site this rule closes.

## The condition that forces NEEDS_REVIEW

Deleting a finalizer removes a garbage-collection-time safety net. That is the
point of JEP 421, and it is still a behaviour change.

Before deleting any override, confirm that the resource it releases is also
released on the normal path — a `close()`, `shutdown()` or `closeDown()` that
the owning code actually calls. If you cannot find that call, **do not delete
the finalizer**. Record the site as `NEEDS_REVIEW` naming the resource and why
the normal path looks incomplete. A leaked socket is worse than a deprecation
warning.

Do not replace a finalizer with a `java.lang.ref.Cleaner` in this run. A Cleaner
needs a registration site and a state object that holds no reference back to the
owner, which is a design change, not a mechanical one.

## Verification

`ant clean lib` inside `jade-ant:21` with `-Xlint:removal -Xmaxwarns 100000`
reports zero `finalize() in Object has been deprecated and marked for removal`
warnings, down from four. The build exits 0 with `BUILD SUCCESSFUL` and all four
consumers PASS. `restaurant-recommendation` and `hw-jade` both exercise
container shutdown, which is the path `JarClassLoader.close()` sits on.
