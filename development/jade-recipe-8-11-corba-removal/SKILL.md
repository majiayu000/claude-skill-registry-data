---
name: jade-recipe-8-11-corba-removal
description: >-
  Deletes JADE's CORBA dependency instead of retrofitting it: the generated
  FIPA IDL stubs, the IIOP message transport protocol, and their build.xml
  wiring. Agent-mode recipe: the shard contract names the files; this
  document defines what is deleted, what is left alone, and how the leftover
  references are resolved.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-8-11-corba-removal — delete the CORBA dependency

Java SE 11 removed the `java.corba` module (JEP 320). `org.omg.CORBA`,
`org.omg.CosNaming`, `org.omg.PortableServer` and the RMI-IIOP packages are
gone from the runtime image, and JEP 320 states there will be no standalone
CORBA unless a third party takes over maintenance.

There are two ways to answer that. **Retrofit** puts a GlassFish ORB back on
the class path and changes no source; the existing recipe
`jade-recipe-8-11-corba-retrofit` does exactly that and stays in the registry
as the fallback path. **This recipe does the opposite**: it deletes the
dependency, because the sponsor goal is to remove what Java no longer has or
no longer needs, not to re-supply it. The two are alternatives; never run both
against the same workspace.

## Why deletion is safe here (read this before editing)

- `org.omg.*` in this codebase is confined to two places: the generated IDL
  stubs in `src/jade/src/FIPA/` and the single transport
  `src/jade/src/jade/mtp/iiop/MessageTransportProtocol.java`.
- The knowledge graph (`03.5-knowledge-graph.json`, 1015 files) records **zero**
  incoming `imports` / `extends` / `implements` / `calls` / `type_refs` edges
  into that set from the other 972 files. It is a leaf.
- `jade/mtp/iiop/MessageTransportProtocol.java` is the only file in the whole
  workspace that imports the generated `FIPA` package.
- IIOP is one of two MTP implementations (the other is `jade/mtp/http/`), and
  it is not the default: `jade/core/ProfileImpl.java` selects
  `jade.mtp.http.MessageTransportProtocol` when no `-mtps` is given. MTPs are
  loaded by `Class.forName` from a user-supplied class name, so nothing in the
  core names IIOP.

This is a **breaking change for JADE users** — narrow, but real. It belongs in
release notes, not in a silent drop. Exactly three capabilities disappear:
`-mtps jade.mtp.iiop.MessageTransportProtocol`, interop with a foreign FIPA
platform that advertises only `IOR:` addresses, and compiling user code against
`FIPA.*` classes shipped in `jade.jar`. The migration for the first is a
one-string config change to the HTTP MTP; for the second there is none.

## Scope of one task

You receive a shard contract. This rule is `blast_class: signature`, so it is
planned as a **single, sequential shard** (`parallel_safe: false`) — it cannot
be split, because the 43 files are one connected component. Edit or delete
**only** files listed in `editable_files`. `read_only_context` is readable and
must never be written.

Check the shard before you start: `editable_files` must be exactly 43 entries —
the 42 files under `src/jade/src/FIPA/` plus
`src/jade/src/jade/mtp/iiop/MessageTransportProtocol.java` — and
`read_only_context` must be empty. Empty read-only context is not a defect
here; it is the graph-leaf proof rendered as data, and `plan_shards.py` emits an
`empty_read_only_context` warning for it. If the shard contains fewer than 43
files, **stop and report `FAILED` with reason `SHARD_PLAN_INCOMPLETE`, naming
the missing files** — do not delete a partial component and do not edit outside
the shard.

That check exists because it has already failed once. The rule's third pattern,
`^\s*package\s+FIPA\s*;`, is in the manifest for exactly this reason: with only
the `org.omg` patterns, five of the 42 generated files carried no `org.omg`
reference of their own, and `plan_shards.py` (which derives `editable_files`
from flagged files plus their one-hop dependents) left `FIPA/DateTime.java` and
`FIPA/ReceivedObject.java` outside the shard entirely and put
`FIPA/FipaMessage.java` in `read_only_context`. Deleting the 40 in-shard files
would then have left `FipaMessage.java` declaring a `FIPA.Envelope[]` field
whose type no longer existed — a broken build reached by following the shard
contract correctly.

## Classification: delete whole file vs edit in place

Use this test on every file, in this order. Do not improvise a fourth case.

**1. Delete the whole file** when the file exists *only* to serve CORBA:

- Anything under `src/jade/src/FIPA/` — all 42 `.java` files. Every one of them
  carries the generator banner `From: FIPA.IDL` / `By: idltojava`; they are
  `idlj` output for `fipa.idl`, not hand-written code. This includes the 5 files
  that carry no `org.omg.` reference themselves (`AgentID.java`,
  `DateTime.java`, `Envelope.java`, `FipaMessage.java`, `ReceivedObject.java`):
  they are IDL value structs whose only consumers are the Helper/Holder classes
  being deleted, and two of them (`FipaMessage` -> `FIPA.Envelope[]`,
  `ReceivedObject` -> `FIPA.DateTime`) would not even compile once their
  siblings are gone. Leaving any of them behind produces dead code or a broken
  build, never a working API. Do not confuse `FIPA.Envelope` (an IDL struct,
  deleted) with `jade.domain.FIPAAgentManagement.Envelope` (core JADE, kept).
- `src/jade/src/jade/mtp/iiop/MessageTransportProtocol.java`, and the now-empty
  `jade/mtp/iiop/` directory with it.
- `src/jade/src/fipa.idl` — the IDL source the deleted stubs were generated
  from. Keeping it invites someone to regenerate them.

**2. Edit in place** when the file survives but names a deleted artifact. In
this codebase that is exactly one file, `src/jade/build.xml`:

- delete the `idlj` target (the `<exec executable="idlj.exe">` block) and drop
  `idlj` from the `depends` list of the `jade` target;
- delete the `check_execIdlj` target and the `EXECidlj.is.set` `<condition>` in
  `init`;
- remove `jade.mtp.iiop` from the `packagenames` attribute of the `javadoc`
  task (note the surrounding entries are space-separated, not comma-separated —
  do not break `jade.mtp.http`);
- remove `<include name="src/FIPA/**"/>` from `dist_src`, and `src/*.idl` if no
  other `.idl` file remains;
- fix the stale header comment that promises `iiop.jar` (line 6); the `lib`
  target never produced a separate `iiop.jar` anyway.

`build.xml` is not a `.java` file, so it is **not** in `editable_files` and not
in the flag index. Edit it anyway — it is part of the same shard's work — and
list it explicitly in the result envelope's `files[]` so the change is
auditable. Do not touch any other build file.

**3. Leave alone.** Not every string with "iiop" or "FIPA" in it is CORBA:

- `jade/domain/FIPANames.java:186` — `public static final String IIOP =
  "fipa.mts.mtp.iiop.std"`. Keep it. It is a protocol *name*, not an
  implementation, and the same file already keeps `WAP` (line 191), a name with
  no implementation in the tree. Deleting a public constant would break client
  code that merely reads it; deleting the implementation does not.
- `jade.domain.FIPAAgentManagement.*`, `jade.lang.acl.*`, and every other
  `FIPA`-flavoured package in `jade/` — these are JADE's own ontology classes
  and have nothing to do with the IDL stubs.
- `jade/mtp/http/**` and `jade/mtp/MTP.java` — the surviving MTP and its
  interface.
- `jade/imtp/**` — IMTP (intra-platform) is a different mechanism from MTP
  (inter-platform). CORBA never touched it.
- Anything under `consumer-playground/` — outside the workspace, and no
  consumer references IIOP, `org.omg`, `-mtps` or `-nomtp`.

## References to deleted classes in files that stay

After the deletions, run this and read every hit before you accept the shard:

```
grep -rn -E "\borg\.omg\.|^\s*package\s+FIPA\s*;|\bFIPA\.[A-Z]|jade\.mtp\.iiop|jade/mtp/iiop|fipa\.idl|idlj" <workspace>
```

Resolve each surviving hit into exactly one of these outcomes:

| what you find | what to do |
|---|---|
| a compile-time reference (`import`, type, `extends`, `new`) to a deleted class from a surviving file | **Stop.** The premise of the shard is broken — the component was not a leaf after all. Report `FAILED` with the file and line; do not invent a replacement type. |
| a build-file reference to a deleted path or target | edit it out, per case 2 above |
| a javadoc/comment reference (`@see jade.mtp.iiop...`, prose about IIOP) | rewrite the sentence to state that the IIOP MTP was removed in this version and HTTP is the transport; never leave a dangling `@see`/`@link` to a deleted type, it breaks the javadoc target |
| a string constant naming the protocol, not the class (`"fipa.mts.mtp.iiop.std"`) | keep it — case 3 above |
| a `// JADE-FLAG:CORBA_REMOVAL` comment in a file you deleted | nothing; it went with the file |
| a `// JADE-FLAG:CORBA_REMOVAL` comment in a file you kept | it must not exist. If it does, the file was misclassified — re-run the classification test on it. |

## Verification

The per-shard verifier does not apply to this shard, and you must know why
before you reach that step. `verify_shard.py` compiles every path in
`editable_files` with `javac` and exits **2 (`SHARD_FILE_MISSING`)** the moment
one of them is not on disk. A deletion shard removes all of them, so the exit
code reports the intended end state, not a defect. Treat that exit as
inapplicable **only** when it names a file this shard deliberately deleted and
the deletion is listed in the result envelope; any other `SHARD_FILE_MISSING`
is a real failure and the shard is rolled back.

Substitute evidence — stronger than per-shard `javac`, and required before
accepting:

1. Full build, in Docker, on JDK 11: `ant clean jade` in the `jade-ant:11`
   image must print `BUILD SUCCESSFUL` and exit 0. Before the removal it prints
   exactly 100 errors, all of them `package org.omg.CORBA does not exist` (53)
   or `package org.omg.CORBA.portable does not exist` (47); after the removal it
   must print none. Nothing else is accepted as proof of a
   build. Capture it to `07-build.log`.
2. `jade.jar` must contain no `FIPA/*.class` and no `jade/mtp/iiop/*.class`.
3. `runtime_verify.py` must report all four consumers PASS, unchanged, with no
   edit on the consumer side.
4. The `grep` above returns only hits resolved as "keep" by the table.

`gate_signatures.py` still applies: build the after-graph and check that no
signature change leaked outside the shard's editable set.

At accept time, `shard_checkpoint.py --accept` exits **1** with
`"<file> no longer exists on disk at accept time"` for each deleted file. That
warning is expected here and the shard is still marked `ACCEPTED`; the exit
code 1 is not a failure. `--rollback` restores every deleted file from its
checkpoint blob, so the deletion stays reversible until accept.

## Invariants

- No edit or deletion outside `editable_files`, with the single documented
  exception of `src/jade/build.xml`, which must be named in the envelope.
- `read_only_context` is never written.
- No file is excluded from compilation while being left in the tree. Removing a
  source file is legal; adding an `excludes` pattern to `build.xml` to hide a
  file that still exists is a pipeline integrity violation (AGENTS.md #11) and
  is forbidden even if it makes the build pass.
- No new dependency is added. If the fix needs a jar, it is the wrong fix — that
  is the retrofit recipe, not this one.
- No public API of the JADE core changes. The only removed public surface is
  the `FIPA.*` package and `jade.mtp.iiop.MessageTransportProtocol`.

## Status to report

| status | when |
|---|---|
| `FIXED` | every file in the delete list is gone, `build.xml` is cleaned, `ant clean jade` on JDK 11 gives BUILD SUCCESSFUL and exit 0, and 4/4 consumers PASS |
| `NEEDS_REVIEW` | the deletions are done and the build is green, but a surviving prose/javadoc reference could not be rewritten with certainty |
| `SKIPPED` | the shard is already CORBA-free (nothing matched) |
| `FAILED` | a surviving file has a compile-time reference to a deleted class, the build does not reach BUILD SUCCESSFUL, or any consumer stops passing |

Never report `FIXED` with an empty `files[]`. Never report a status you did not
observe: `BUILD SUCCESSFUL` and exit 0 from Docker are the only accepted proof
of a build, and consumer PASS is the only accepted proof of behavior.
