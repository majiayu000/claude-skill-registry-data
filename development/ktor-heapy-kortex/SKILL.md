---
name: ktor
description: Use when building, modifying, debugging, or reviewing Ktor 3.5.x server and client applications, including routing, requests/responses, plugins, serialization, authentication, sessions, WebSockets, SSE, engines, testing, deployment, and Kotlin multiplatform client work.
---

# Ktor

Use this skill for Ktor framework work: Kotlin HTTP servers, HTTP clients, multiplatform clients, REST APIs,
WebSockets, SSE, serialization, authentication, plugins, testing, and deployment.

Do not confuse Ktor with generic Kotlin, Spring Boot, ktorfit, Retrofit, OkHttp-only usage, or Kotlin Toolchain build
configuration. If the task is about `module.yaml` or the `./kotlin` build CLI, load `kotlin-toolchain` too. If the task is
a standalone `.main.kts` script using Ktor, load `main-kts` too.

## Source Snapshot

This skill is generated from the official Ktor documentation:

- Repository: `https://github.com/ktorio/ktor-documentation`
- Ref: `main` at the Ktor `3.5.x` documentation line
- SHA: `d118418a65e03d73ad7c2d33bb68e979cebcb4e5`
- Ktor version variable: `3.5.1`
- Kotlin version variable: `2.3.21`
- Coroutines version variable: `1.11.0`
- Server guide: `references/server.md`
- Client guide: `references/client.md`
- Regeneration log: `generation/generation-steps.md`

Version this skill by the Ktor **minor** line, like `kotlin-toolchain`: this default `SKILL.md` targets Ktor `3.5.x` and
should keep immediate operational guidance here instead of becoming only a version index. If maintaining future docs,
create or update a minor-line snapshot such as Ktor `3.6.x`; do not silently mix breaking or behavior-changing guidance
from a different minor line.

Ktor APIs move between minor releases. When exact syntax matters, inspect the project dependencies/build files first and
prefer the docs for the project's installed Ktor version.

## First Moves

When working in a repository:

1. Inspect build files first: `build.gradle.kts`, `settings.gradle.kts`, `gradle/libs.versions.toml`, `pom.xml`,
   `module.yaml`, or `.main.kts` annotations.
2. Determine Ktor version and whether it is server, client, or both.
3. For server work, load `references/server.md`.
4. For client or multiplatform client work, load `references/client.md`.
5. Preserve the project's build system and existing style. Do not introduce Gradle if the project uses Kotlin Toolchain;
   do not introduce Kotlin Toolchain if the project uses Gradle or Maven.
6. Add only the artifacts required for the plugins/features being installed.
7. After changes, run the project's real tests or at least a compile/build task.

## Core Coordinates and Imports

Ktor artifacts use Maven group `io.ktor`. In Gradle examples, use one version source:

```kotlin
val ktorVersion = "3.5.1"
implementation("io.ktor:ktor-server-core:$ktorVersion")
implementation("io.ktor:ktor-client-core:$ktorVersion")
```

Common server dependencies:

- `ktor-server-core`
- engine: `ktor-server-cio`, `ktor-server-netty`, `ktor-server-jetty-jakarta`, or `ktor-server-tomcat-jakarta`
- serialization: `ktor-server-content-negotiation` + one of `ktor-serialization-kotlinx-json`, `gson`, `jackson`,
  `kotlinx-xml`, `kotlinx-cbor`, `kotlinx-protobuf`
- auth: `ktor-server-auth`, optional `ktor-server-auth-jwt`, `ktor-server-auth-ldap`
- sessions: `ktor-server-sessions`
- testing: `ktor-server-test-host`
- DI: `ktor-server-di`

Common client dependencies:

- `ktor-client-core`
- engine: `ktor-client-cio`, `ktor-client-okhttp`, `ktor-client-apache5`, `ktor-client-java`,
  `ktor-client-jetty-jakarta`, `ktor-client-android`, `ktor-client-darwin`, `ktor-client-curl`, `ktor-client-winhttp`,
  or `ktor-client-js`
- serialization: `ktor-client-content-negotiation` + one of the serialization artifacts above
- auth: `ktor-client-auth`
- logging: `ktor-client-logging`
- testing: `ktor-client-mock`

For `.main.kts`, prefer JVM/platform leaf artifacts where needed, for example `io.ktor:ktor-client-cio-jvm:3.5.1`,
because script dependency resolution can miss Gradle module metadata for multiplatform root artifacts.

## Server Minimal Shape

Load `references/server.md` before non-trivial server edits.

```kotlin
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.application.*
import io.ktor.server.cio.*
import io.ktor.server.engine.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun main() {
    embeddedServer(CIO, port = 8080, host = "0.0.0.0") {
        install(ContentNegotiation) { json() }
        routing {
            get("/health") { call.respondText("OK") }
            get("/") { call.respond(mapOf("status" to "up")) }
        }
    }.start(wait = true)
}
```

Prefer route extension functions once routing grows:

```kotlin
fun Application.module() {
    configureSerialization()
    configureRouting()
}

fun Application.configureRouting() = routing {
    route("/api") { get("/health") { call.respond(HttpStatusCode.OK) } }
}
```

## Client Minimal Shape

Load `references/client.md` before non-trivial client edits.

```kotlin
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.serialization.kotlinx.json.*

suspend fun main() {
    val client = HttpClient(CIO) {
        install(ContentNegotiation) { json() }
    }
    try {
        val body: String = client.get("https://example.com").body()
        println(body)
    } finally {
        client.close()
    }
}
```

Use a singleton/DI-managed `HttpClient` in applications. Do not create and dispose a new client per request.

## Mental Model

Ktor is plugin-oriented:

- A server `Application` installs plugins and registers routes. The current request/response is an `ApplicationCall`.
- A client `HttpClient` installs plugins and makes suspending requests. The current response is an `HttpResponse`.
- Most features require both an artifact and `install(PluginName) { ... }`.
- Serialization is not implicit: install `ContentNegotiation` and choose a serializer.
- Authentication is route-scoped on the server via `authenticate { ... }`; on the client it is request-scoped/provider-
  selected through the `Auth` plugin.
- Engines perform network I/O. Choose an engine compatible with the platform and features needed.

## Frequent Pitfalls

- Missing plugin artifact: `install(ContentNegotiation)` needs `ktor-server-content-negotiation` or
  `ktor-client-content-negotiation` plus serializer artifacts.
- Wrong imports: server packages are under `io.ktor.server.*`; client packages under `io.ktor.client.*`.
- Receiving request bodies twice on server without `DoubleReceive` fails.
- Forgetting `@Serializable` or the Kotlin serialization compiler plugin when using `kotlinx.serialization`.
- Creating an `HttpClient` per request leaks resources and defeats pooling.
- In tests, use Ktor test hosts/mocks instead of binding real ports unless doing E2E.
- For Ktor 3.5 digest auth, prefer RFC 7616 APIs (`DigestAlgorithm`, `DigestQop`, algorithm-aware digest provider) over
  stringly legacy MD5-only examples.

## Verification Checklist

- [ ] Project Ktor version and build system were inspected.
- [ ] Server/client/reference file was loaded as appropriate.
- [ ] Required artifacts match installed plugins/features.
- [ ] Code compiles against the project's Ktor minor version.
- [ ] Tests/build were run, or any blocker is reported explicitly.
