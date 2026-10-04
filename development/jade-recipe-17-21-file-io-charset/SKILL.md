---
name: jade-recipe-17-21-file-io-charset
description: >-
  Pins an explicit UTF-8 charset on the file reader, writer and print stream
  constructors that JADE uses to write files it later reads back itself.
  JEP 400 (JDK 18) changed those constructors from the platform default charset
  to UTF-8. Agent-mode recipe: the shard contract names the files; this document
  defines the transform and the sites it must refuse to touch.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-17-21-file-io-charset — make the file encoding say what it means

JEP 400 changed `Charset.defaultCharset()` to return UTF-8 from JDK 18 onward,
and with it every API that encodes or decodes text without an explicit charset.
The JEP names the affected `java.io` constructors directly: *"In the java.io
package, InputStreamReader, FileReader, OutputStreamWriter, FileWriter, and
PrintStream define constructors to create readers, writers, and print streams
that encode or decode using the default charset."*

Nothing breaks and nothing warns. The code compiles identically on 17 and on 21.
Only the bytes change, and only on a host whose platform default was not already
UTF-8.

The JEP also states the failure mode this rule exists to remove: a file written
by one JVM and read by another with a different default charset is *"silently
corrupted or incomplete, since the FileReader cannot tell that it decoded the
text using the wrong charset relative to the FileWriter."*

## Scope of one task

You receive a shard contract. This rule is `blast_class: body-local`
(`parallel_safe: true`). Edit only that shard's `editable_files`;
`read_only_context` is read-only.

## The transform

```
new FileReader(f)             ->  new FileReader(f, StandardCharsets.UTF_8)
new FileWriter(f)             ->  new FileWriter(f, StandardCharsets.UTF_8)
new FileWriter(f, append)     ->  new FileWriter(f, StandardCharsets.UTF_8, append)
new PrintStream(f)            ->  new PrintStream(f, StandardCharsets.UTF_8)
```

Add `import java.nio.charset.StandardCharsets;` when the file does not already
have it. Insert it in the existing import block, in the position the surrounding
imports imply; do not reorder the block.

Note the argument order on `FileWriter`: the charset goes **before** the append
flag, not after. `new FileWriter(f, true)` becomes
`new FileWriter(f, StandardCharsets.UTF_8, true)`.

## Why UTF-8 and not something else

These are files JADE writes and JADE reads back — persisted messages, fault
recovery state, log and CSV output. On JDK 21 they are UTF-8 already, because
that is what JEP 400 made the default. Pinning UTF-8 changes nothing on 21 and
makes a jar built here behave the same way on 17, which removes the
version-dependence rather than adding one.

## The sites this rule must NOT touch

**Anything that crosses a process or a node boundary.** Those sites carry the
same question as the ACL and JICP wire codecs, which are a deliberate
maintainer decision and are not part of this run. If the stream comes from a
socket rather than a file, skip it, keep the `// JADE-FLAG:` marker, and name it
in the shard result:

```java
new PrintStream(socket.getOutputStream())        // SKIP - wire format
new PrintStream(client.getOutputStream(), true)  // SKIP - wire format
```

Three such sites exist: `jade/tools/SocketProxyAgent/JadeBridge.java:171`,
`jade/tools/SocketProxyAgent/Connection.java:75` and
`jade/tools/applet/DFAppletCommunicator.java:96`.

**Anything already carrying a charset.** A constructor with an explicit
`Charset` or charset-name argument is done; leave it and drop its marker.

**Anything reading a file this process did not write** — an operator-supplied
policy or configuration file whose encoding is fixed by whoever wrote it.
Record it as `NEEDS_REVIEW` with the file's role, rather than guessing.

## What the agent may not do

- Do not edit a site inside a comment or a string literal. Check with
  `java_source.is_live_code()` before every edit.
- Do not touch `#PJAVA_INCLUDE`, `#DOTNET_INCLUDE` or `#MIDP_EXCLUDE` blocks.
  They are comment text, not code.
- Do not convert the surrounding code to try-with-resources. That is a separate
  rule with its own deferral marker already in these files.
- Do not change `System.in`, `System.out` or `System.err` wrappers. JEP 400
  explicitly leaves those to `Console.charset()`.

## Verification

`ant clean lib` inside `jade-ant:21` exits 0 with `BUILD SUCCESSFUL`, the four
consumers still PASS, and every site left behind is named in the shard result
with its reason.
