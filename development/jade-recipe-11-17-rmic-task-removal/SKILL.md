---
name: jade-recipe-11-17-rmic-task-removal
description: >-
  Removes the two Ant <rmic> pregeneration steps from build.xml. The rmic tool
  they drive was removed in JDK 15, and Ant refuses the task on JDK 15+, which
  is the only thing stopping the JADE build on JDK 17. Agent-mode recipe: the
  shard contract names the file; this document defines the transform and the
  one condition under which the agent must stop instead.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-11-17-rmic-task-removal — the static stub compiler is gone

`rmic` was deprecated for removal in JDK 13 and removed in JDK 15. Ant does not
fall back; it fails the task outright:

```
build.xml:154: rmic does not exist under Java 15 and higher, use rmic of an
older JDK and explicitly set the executable attribute
```

This is the only compile-or-build breakage in the 11-to-17 window. javac itself
is clean: a probe of the untouched baseline on `jade-ant:17` compiled all 972
sources with zero errors at source/target 11 and again at 17.

## Scope of one task

You receive a shard contract. This rule is `blast_class: body-local`
(`parallel_safe: true`). Edit only that shard's `editable_files`;
`read_only_context` is read-only.

`src/jade/build.xml` is absent from the knowledge graph — the graph is built
from `.java` sources — so the shard planner emitted an isolated shard and said
so with `flagged_file_not_in_graph`. That warning is expected here and is not a
signal that something is missing.

## The two sites

| file | line | construct |
|---|---|---|
| `src/jade/build.xml` | 154 | `<rmic classname="jade.imtp.rmi.ServiceManagerRMIImpl" base="${build}"/>` |
| `src/jade/build.xml` | 155 | `<rmic classname="jade.imtp.rmi.NodeRMIImpl" base="${build}"/>` |

Both sit at the end of the `jade` target, after `<javac>` and the resource
`<copy>`. Delete the two elements, and the `<!-- JADE-FLAG: -->` comment the
scanner injected after the enclosing tag. Change nothing else: no `excludes`,
no `classpath`, no target dependency list.

## Why deleting them is safe

Static stubs have been obsolete since Java 5. Both named classes extend
`java.rmi.server.UnicastRemoteObject`:

- `src/jade/src/jade/imtp/rmi/ServiceManagerRMIImpl.java:46`
- `src/jade/src/jade/imtp/rmi/NodeRMIImpl.java:38`

`UnicastRemoteObject.exportObject` generates a dynamic proxy stub at export
time, and the JDK 13 release note that deprecated `rmic` says so directly:
dynamically generated stubs "are functionally equivalent to statically generated
stubs". Removing the pregeneration step removes a build dependency, not a
runtime capability. Note also that `jade.core.ProfileImpl:540` defaults the IMTP
to LEAP, so the RMI IMTP is an opt-in transport in the first place.

## What the agent may not do

- Do **not** set `executable=` on the `<rmic>` task to point at an older JDK's
  rmic. That pins the build to a second JDK installation to keep a step that
  produces nothing the runtime needs.
- Do **not** add an `excludes` pattern to hide `jade/imtp/rmi/**` from javac.
  The sources compile fine; only the pregeneration step is dead. Hiding live
  source from the compiler to make a build pass is forbidden by AGENTS.md #11.
- Do **not** delete the `jade.imtp.rmi` package. The rule is about the build
  step, not the transport.

## Stop condition

If anything in the workspace or in `consumer-playground/` loads a
`*_Stub` class by name, or otherwise depends on a pregenerated stub file rather
than on `UnicastRemoteObject` export, dynamic stubs do not cover it. Report
`NEEDS_REVIEW` naming the site instead of deleting.

## Verification

`ant clean lib` in `jade-ant:17` prints `BUILD SUCCESSFUL`, exits 0, and
produces `lib/jade.jar`. No build file in the workspace still contains `<rmic`.
