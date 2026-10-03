---
name: main-kts
description: Use when creating, writing, or running standalone executable Kotlin scripts with the `.main.kts` extension, including the `kotlin` script runner, shebang execution, `@file:DependsOn`/`@file:Repository`/`@file:Import`/`@file:CompilerOptions`/`@file:OptIn` annotations, script dependencies, command-line `args`, compiled-script caching, and common scripting libraries such as ktor, kotlinx-serialization, kotlinx-coroutines, clikt, and kotlinx-html.
---

# Kotlin Scripts (.main.kts)

Use this skill to generate and run executable Kotlin `.main.kts` scripts: single-file programs that declare their own
dependencies, run directly from the shell, and need no build file.

This is the `kotlin` script runner, not Kotlin Toolchain, Gradle, or Maven. Do not add `module.yaml`, `build.gradle`, or
`pom.xml`. If the task needs a real multi-file project or published artifact, it is not a `.main.kts` task.

## When To Use

- A one-off automation, glue, or CLI utility that should run with `./script.main.kts` or `kotlin script.main.kts`.
- The user wants Kotlin without project scaffolding or a build system.
- Quick API calls, file munging, JSON processing, HTML generation, or shell orchestration.

Prefer a real Kotlin Toolchain or Gradle module when the code grows multiple source files, needs incremental builds, or
ships as a library or application artifact.

## Gather Requirements

Before writing, confirm:

1. What the script should do (purpose and behavior).
2. A name (suggest one from the behavior; the file must end in `.main.kts`).
3. Where to save it (default: current directory).
4. Any inputs it takes (command-line `args`, env vars, stdin).

## Script Structure

`@file:` annotations must come first, before any `import` or code. Order them: `Repository`, `DependsOn`, `Import`,
`CompilerOptions`, `OptIn`.

```kotlin
#!/usr/bin/env kotlin

/**
 * [What the script does.]
 *
 * Usage:
 *   ./script.main.kts <args>
 */

// Custom repositories. If any @file:Repository is present, list every repository needed.
// Maven Central is not kept implicitly once custom repositories are declared.
@file:Repository("https://repo.maven.apache.org/maven2/")
@file:Repository("https://jitpack.io")

// Maven dependencies
@file:DependsOn("group:artifact:version")

// Compose other scripts (optional)
@file:Import("other.main.kts")

// Compiler flags (optional)
@file:CompilerOptions("-jvm-target", "21")

// Opt-ins (optional)
@file:OptIn(ExperimentalStdlibApi::class)

import ...

// Top-level script code runs directly; `args` is available.
```

## Key Mechanics

- **Extension**: use `.main.kts` when the script needs the `main.kts` script definition, especially
  `@file:DependsOn`, `@file:Repository`, `@file:Import`, or compiler options. A plain `.kts` script run with
  `kotlin script.kts arg1` can still read `args`; do not rename solely for CLI arguments.
- **Shebang**: `#!/usr/bin/env kotlin` enables `./script.main.kts`. After writing, suggest `chmod +x script.main.kts`.
- **Run**: `kotlin script.main.kts arg1 arg2` or, once executable, `./script.main.kts arg1 arg2`.
- **Runner rename (Kotlin 2.4.10+)**: starting with Kotlin 2.4.10 the script runner is `kotlinr`, not `kotlin`. On
  those versions run `kotlinr script.main.kts` and use `#!/usr/bin/env kotlinr` in the shebang. Earlier versions keep
  using `kotlin`.
- **Args**: command-line arguments arrive as the `args: Array<String>` variable. Validate and fail fast with `error(...)`
  or `kotlin.system.exitProcess(1)`.
- **Dependencies**: `@file:DependsOn("group:artifact:version")` resolves from Maven Central by default when no
  `@file:Repository` annotations are present. If you add any repository annotation, list every repository the script
  needs, including Maven Central (`https://repo.maven.apache.org/maven2/`) plus custom repositories such as Google or
  JitPack. Version is required; do not rely on ranges.
- **Composition**: `@file:Import("other.main.kts")` inlines another script so it can share top-level declarations.
- **Caching**: compiled scripts are cached and recompiled only when the source or its `@file:` annotations change. The
  cache lives at `$KOTLIN_MAIN_KTS_COMPILED_SCRIPTS_CACHE_DIR`, or `~/Library/Caches/main.kts.compiled.cache` on macOS by
  default. Disable by setting that variable to an empty value if you need a clean compile.
- **The cache key ignores command-line compiler flags.** It hashes the source and its `@file:` annotations only — *not*
  `-Xplugin` or other flags passed to the runner. So toggling `-Xplugin` on an unchanged file does not force a recompile:
  a run *with* the serialization plugin caches serializer-bearing bytecode that a later run *without* the plugin silently
  reuses (and vice versa). When testing whether a compiler plugin actually applies, clear the cache first — otherwise a
  stale entry masks the real result. This is a genuine debugging trap: an `@Serializable` script can appear to work with
  no plugin simply because an earlier plugged-in run populated the cache.
- **First run is slow**: dependency resolution and compilation happen on the first run; later runs hit the cache.

## Running: `kotlin` vs `kotlinc -script`

Both compile and execute a `.main.kts` — since Kotlin 1.3.70 the runner handles scripts "the same way as
`kotlinc -script`". They differ in the interface, how script arguments are passed, and how you supply compiler options:

|                 | `kotlin script.main.kts args...`                                           | `kotlinc -script script.main.kts -- args...`             |
|-----------------|----------------------------------------------------------------------------|----------------------------------------------------------|
| What it is      | Runner wrapper - detects the script, compiles, runs. Best for CLI/shebang. | Compiler CLI - you state explicitly that it is a script. |
| Script `args`   | Everything after the file name becomes `args`.                             | Use `--` to split script args from compiler options.     |
| Compiler plugin | `kotlin -Xplugin=... script.main.kts`                                      | `kotlinc -script -Xplugin=... script.main.kts`           |

Both apply `-Xplugin` at the script's compile phase — this is how `@Serializable` is made to work (see Serialization
formats). For debugging compiler-plugin problems, prefer `kotlinc -script`: you work with the compiler and its options
directly, without the runner's own command-line parsing in between.

## Common Dependencies

| Library            | Coordinate                                                 | Use case                       |
|--------------------|------------------------------------------------------------|--------------------------------|
| ktor-client        | `io.ktor:ktor-client-cio-jvm:3.5.1`                        | HTTP client (async; see below) |
| kotlinx-coroutines | `org.jetbrains.kotlinx:kotlinx-coroutines-core-jvm:1.11.0` | async / concurrency            |
| clikt              | `com.github.ajalt.clikt:clikt-jvm:5.1.0`                   | CLI argument parsing           |
| kotlinx-html       | `org.jetbrains.kotlinx:kotlinx-html-jvm:0.12.0`            | HTML generation                |

Versions move; confirm the latest stable coordinate on [central.sonatype.com](https://central.sonatype.com) before
pinning if the script must stay current.

**Use the `-jvm` artifact for Kotlin Multiplatform libraries.** `@file:DependsOn` resolves through a Maven resolver that
reads `.pom` files and ignores Gradle Module Metadata (the `.module` files). Most KMP libraries here (Ktor, clikt, and the
format libraries below) publish their bare coordinate as an empty umbrella jar with **no JVM classes** — the bytecode
lives in the `-jvm` platform artifact — so the bare coordinate resolves but yields `unresolved reference` at compile
time. Depend on `io.ktor:ktor-client-cio-jvm`, not `io.ktor:ktor-client-cio`. The `-jvm` leaf always works, so it is the
one uniform rule; a library already pinned to a `-jvm` (or plain-JVM) leaf — like `kotlinx-html-jvm` — needs no change.

The exception proves the mechanism: `kotlinx-serialization` and `kotlinx-coroutines` publish their root as a *POM* that
declares a compile dependency on their own `-jvm` artifact, which the resolver follows — so `kotlinx-serialization-json`
(no `-jvm`) also resolves. It is not that these libraries are special to the runner; it is that they redirect via POM
where the umbrella libraries do not. Verified on Kotlin 2.4.0 by inspecting each root POM and jar; `-jvm` is still the
safe uniform choice.

### Serialization formats

These build on kotlinx.serialization — in a real module you annotate a data class with `@Serializable` once and swap the
format backend (JSON, YAML, TOML, XML, CSV) over the same model.

> **`@Serializable` needs the serialization compiler plugin, passed on the command line.** A bare `kotlin script.main.kts`
> does not apply it, and `@file:CompilerOptions("-Xplugin=…")` does not enable it either — so encode/decode throws
> `Serializer for class … is not found` at runtime. It *does* work when you pass the plugin as a `-Xplugin` flag to the
> runner or compiler (verified on Kotlin 2.4.0):
> `kotlin -Xplugin="$KOTLIN_HOME/lib/kotlinx-serialization-compiler-plugin.jar" script.main.kts`. To keep
> `./script.main.kts` self-contained via a shebang, bake that flag in with a shebang form below (`env -S` or a shell
> polyglot); or skip codegen and walk the parsed tree (JSON shown below). When toggling the plugin on and off to check
> whether it applied, clear the compiled-script cache between runs — it is not keyed by `-Xplugin`, so a stale entry will
> mask the result (see Caching).

| Format | Coordinate (`-jvm` leaf, see the KMP note above)              |
|--------|---------------------------------------------------------------|
| JSON   | `org.jetbrains.kotlinx:kotlinx-serialization-json-jvm:1.11.0` |
| YAML   | `io.heapy.kotaml:kotaml-jvm:0.110.0`                          |
| TOML   | `com.akuleshov7:ktoml-core-jvm:0.7.1`                         |
| XML    | `io.github.pdvrieze.xmlutil:serialization-jvm:1.0.0`          |
| CSV    | `app.softwork:kotlinx-serialization-csv-jvm:0.0.23`           |

**JSON in a script** works without the plugin if you skip `@Serializable` and walk the parsed tree instead:

```kotlin
@file:DependsOn("org.jetbrains.kotlinx:kotlinx-serialization-json-jvm:1.11.0")

import kotlinx.serialization.json.*

val root = Json.parseToJsonElement(jsonText)          // no @Serializable, no compiler plugin
val name = root.jsonObject["name"]!!.jsonPrimitive.content
```

**Self-contained shebang version.** Passing `-Xplugin` on the command line works, but then `./script.main.kts` no longer
runs standalone. To bake the plugin into the file so it executes directly, use one of two shebang forms. Both need
`KOTLIN_HOME` to point at the compiler, and both must be run as `./script.main.kts`, **not** `kotlin script.main.kts` —
go through the runner and the shebang is never read, so `-Xplugin` is skipped and `@Serializable` fails at runtime again.

*Option A — `env -S` (needs GNU coreutils 8.30+/2018 or BSD `env`).* `env -S` splits the shebang string and hands the
runner `kotlin -Xplugin=… script.main.kts args…` — exactly the argv documented above. But `${VAR}` expansion *inside a
real shebang* is platform-split, and the difference decides whether the file runs at all:

```kotlin
#!/usr/bin/env -S kotlin -Xplugin=${KOTLIN_HOME}/lib/kotlinx-serialization-compiler-plugin.jar
@file:DependsOn("org.jetbrains.kotlinx:kotlinx-serialization-json:1.11.0")

import kotlinx.serialization.*
import kotlinx.serialization.json.*

@Serializable data class Data(val a: Int, val b: String)
println(Json.encodeToString(Data(42, "str")))         // prints {"a":42,"b":"str"}
```

- **On Linux `${KOTLIN_HOME}` expands; on macOS it does not** — the kernel decides, not `env`. Linux hands `env` the whole
  shebang tail as one argument, so `env -S` splits *and* expands it. macOS/XNU splits the `#!` line on whitespace *before*
  `env` runs, so `env -S` only sees the first token as its `-S` operand; `${KOTLIN_HOME}` arrives as a separate,
  already-split argv element that `env` passes through verbatim. The literal string reaches the compiler, which dies with
  `plugin classpath entry points to a non-existent location: ${KOTLIN_HOME}/…`. Tested on macOS + Kotlin 2.4.0 (fails);
  `env -S` expands the variable only when called from a shell, not from a shebang. The Linux path is inferred from its
  single-arg shebang contract, not run in this session.
- **Where expansion does happen, braces are mandatory.** `${KOTLIN_HOME}` expands; `$KOTLIN_HOME` fails with
  `only ${VARNAME} expansion is supported` — `-S`'s own parser, not the shell.
- **On macOS, hardcode the absolute jar path** (`-Xplugin=/…/lib/kotlinx-serialization-compiler-plugin.jar`) — that form
  is verified working. The cost is length: the kernel measures the shebang against `BINPRM_BUF_SIZE` (128 bytes before
  Linux 5.1, 256 after), and a full jar path runs ~126 bytes even from a short prefix — brushing the old cap. The variable
  was what kept the line short, and that is exactly what macOS won't expand, so there is no headroom to gain here.
- On Kotlin 2.4.10+ the runner is `kotlinr`, so the shebang becomes `#!/usr/bin/env -S kotlinr -Xplugin=…`.

*Option B — shell/Kotlin polyglot (portable; bare POSIX `sh`).* Uglier, but needs no `env -S`, so it runs on any POSIX
shell:

```sh
#!/bin/sh
//usr/bin/env kotlinc -script -Xplugin="$KOTLIN_HOME/lib/kotlinx-serialization-compiler-plugin.jar" -- "$0" "$@"; exit $?
@file:DependsOn("org.jetbrains.kotlinx:kotlinx-serialization-json:1.11.0")

import kotlinx.serialization.*
import kotlinx.serialization.json.*

@Serializable data class Data(val a: Int, val b: String)
println(Json.encodeToString(Data(42, "str")))         // prints {"a":42,"b":"str"}
```

Run it as `./script.main.kts` (or `sh script.main.kts`). Line 2 is the pivot: the shell reads `//usr/bin/env…` as the
path `/usr/bin/env` and execs the compiler, while Kotlin reads the same line as a `//` comment. Keep that exec on a single
`//` line — a `/*` written *after* `//` stays inside the line comment and never opens a block comment, so the shell lines
leak into Kotlin and fail to compile (the common trap).

Both examples use the plain `kotlinx-serialization-json` coordinate because its root POM redirects to `-jvm` (see the KMP
note); an umbrella-only library would still need its `-jvm` leaf here. Because Option B expands `$KOTLIN_HOME` in a real
shell line, it keeps a variable path working everywhere, macOS included — so it is the portable choice for a single file
that must run on both. Use Option A's variable form on Linux; on macOS use Option B or hardcode the jar path. Even so, a
real Gradle/Kotlin module is the clean
answer; use either shebang only for a genuinely single-file need.

### Ktor client modules

Each engine pulls in `ktor-client-core-jvm` transitively, so depend on one engine alone — pick it:

| Engine                                  | Notes                                                      |
|-----------------------------------------|------------------------------------------------------------|
| `io.ktor:ktor-client-cio-jvm:3.5.1`     | Pure-Kotlin coroutine engine, no extra deps. Good default. |
| `io.ktor:ktor-client-java-jvm:3.5.1`    | JDK 11+ `java.net.http`; HTTP/2, no third-party deps.      |
| `io.ktor:ktor-client-okhttp-jvm:3.5.1`  | OkHttp-backed; HTTP/2, connection pooling.                 |
| `io.ktor:ktor-client-apache5-jvm:3.5.1` | Apache HttpClient 5.                                       |

Plugins are separate artifacts; add them alongside the engine as needed:

| Plugin                                              | Purpose                                            |
|-----------------------------------------------------|----------------------------------------------------|
| `io.ktor:ktor-client-content-negotiation-jvm:3.5.1` | (De)serialize bodies by `Content-Type`.            |
| `io.ktor:ktor-client-logging-jvm:3.5.1`             | Request/response logging.                          |
| `io.ktor:ktor-client-auth-jvm:3.5.1`                | Basic / Bearer (with token refresh) / Digest auth. |
| `io.ktor:ktor-client-encoding-jvm:3.5.1`            | gzip/deflate compression handling.                 |
| `io.ktor:ktor-client-websockets-jvm:3.5.1`          | WebSocket support.                                 |

Content negotiation also needs a converter — `io.ktor:ktor-serialization-kotlinx-json-jvm:3.5.1` (note the
`ktor-serialization-*` prefix, not `ktor-client-*`). It relies on `@Serializable`, so the codegen caveat above applies
in a plain script.

### Shelling out

Use the JDK's `ProcessBuilder` — it is enough for scripts and needs no dependency.

## After Generation

1. Write the file with the `.main.kts` extension.
2. Tell the user to run `chmod +x <name>.main.kts` if they want `./<name>.main.kts` execution.
3. Show the exact run command and what output to expect.
4. Note the first run compiles and downloads dependencies, so it is slower than later runs.

## Example: Fetch A URL With Ktor

```kotlin
#!/usr/bin/env kotlin

/**
 * Fetches a URL and prints the response body.
 *
 * Usage:
 *   ./fetch.main.kts https://api.example.com/data
 */

@file:DependsOn("io.ktor:ktor-client-cio-jvm:3.5.1")

import io.ktor.client.HttpClient
import io.ktor.client.engine.cio.CIO
import io.ktor.client.request.get
import io.ktor.client.statement.bodyAsText
import io.ktor.http.isSuccess
import kotlinx.coroutines.runBlocking
import kotlin.system.exitProcess

val url = args.firstOrNull() ?: run {
    System.err.println("Usage: fetch.main.kts <url>")
    exitProcess(1)
}

runBlocking {
    HttpClient(CIO).use { client ->
        val response = client.get(url)
        if (!response.status.isSuccess()) {
            System.err.println("HTTP ${response.status}")
            exitProcess(1)
        }
        println(response.bodyAsText())
    }
}
```

## Pitfalls

- A `.kts` file that is not `.main.kts` can still see `args`, but it will not resolve `main.kts` annotations such as
  `@file:DependsOn`; rename only when those script-definition features are needed.
- `@file:` annotations after the first `import` or statement are ignored or fail — keep them at the top.
- Missing versions in `@file:DependsOn` break resolution; always pin `group:artifact:version`.
- Editing a script invalidates its cache and forces a recompile; do not expect instant runs after every change.
- For dependencies on JitPack, Google, or private repos, add `@file:Repository(...)` before `@file:DependsOn(...)` and
  include Maven Central explicitly too if any dependency still comes from Central.
- Kotlin Multiplatform deps resolve to an empty umbrella unless you use the `-jvm` artifact — `unresolved reference`
  despite a correct `@file:DependsOn` usually means a missing `-jvm` suffix (see Common Dependencies).
- `@Serializable` codegen is off by default in `.main.kts` (the plugin is not applied), so it fails at runtime, not
  compile time. Enable it by passing `-Xplugin=…serialization…` to the runner/compiler, parse JSON via `JsonElement`, or
  move the logic to a real module.
- `const val` is rejected at the top level of a script — use a plain `val` (top-level script declarations are not inside
  an object).
- Long-lived or multi-file logic belongs in a real module, not a script.
