---
name: transport-security-setup
description: >
  Decides where TLS terminates for a generated or adopted Spring Boot project — at the edge
  (ingress, load balancer, Caddy) or in the embedded Tomcat, with mutual TLS as a recorded
  variant — and writes the matching configuration: forwarded headers and trusted proxies, or an
  SSL bundle with reload and profile-gated TLS; HTTP/2 on; HSTS with exactly one writer; the
  integration test that proves it on a real server; a local Caddy edge through docker-architect.
  Use when the request involves HTTPS, TLS, certificates, HTTP/2, h2c, HSTS, X-Forwarded-Proto,
  "behind a proxy", "configure https", or when project-bootstrap or arch-adopt finds a project
  whose root CLAUDE.md has no Transport line.
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion, Skill, Bash(grep:*), Bash(./mvnw:*), Bash(./gradlew:*)
model: sonnet
effort: low
---

# Transport Security Setup

Decides once, per project, how a request reaches it over TLS, and writes what that decision
needs. One question decides the shape: **where does TLS terminate?** At the edge → the
application holds no key and learns the scheme from the edge's forwarded headers. In the
embedded server → the application loads a mounted certificate through an SSL bundle and serves
8443. Every rule this skill applies is `@.claude/rules/transport-security.md`; every rule about
key material is `@.claude/rules/secrets.md`.

**Entry rule: decide once.** The root `CLAUDE.md` already has a `**Transport:` paragraph →
report "already decided", quote it, and stop. Changing topology is a new decision: the user
deletes the paragraph and runs `/transport-security-setup` again, which then rewrites the
configuration it owns. When the paragraph is missing but `application.yml` already holds
`server.ssl`, `spring.ssl.bundle` or `forward-headers-strategy`, the project decided by hand:
report the lines found, ask which topology they implement, and write only the paragraph — never
rewrite a configuration this skill did not write.

**No key, certificate or password is written, anywhere.** Not in `application.yml`, not under
`src/test/resources`, not "for local use". The production files are mounted at run time and
their paths come from the environment; the test generates its own certificate when it runs.

## Why this is a skill (Form 1) and not Form 2

Form 1: `project-bootstrap` and `arch-adopt` chain it by name, and a skill with
`disable-model-invocation: true` cannot be called through the `Skill` tool — the reason
`sonarqube-setup` stays model-invocable. Axis 2 of the interview — two callers, one of which
runs inside a project where `project-bootstrap` does not exist — made it a skill of its own; the
closest rejected form was a transport block inside `security-architect`, a design skill that
writes docs only and runs per use case, so a project with no protected endpoint would never
decide transport. Record: `@.claude/decisions/0122-transport-security-setup-and-secrets.md`.

Runs on `sonnet` with `effort: low`: one interview with fixed options, then edits per answer
(`@.claude/decisions/0080-procedural-skills-on-sonnet.md`).

## Procedure

**Project directory.** When the caller's one-line context names `project: <absolute path>`,
that directory is the project root, not the session's: read and write every path of this
procedure under it, and run every shell command as `(cd "<path>" && …)`. When this skill chains
`docker-architect`, pass `project: <path>` on in its context.

### 1 · Detect

```bash
grep -n "^\*\*Transport:" CLAUDE.md 2>/dev/null
grep -rnE "server\.ssl|ssl:|bundle:|forward-headers-strategy" --include='application*.yml' --include='application*.properties' . 2>/dev/null | grep -v /target/
grep -nE "spring-boot-starter-(security|jetty)" pom.xml build.gradle */pom.xml */build.gradle 2>/dev/null
```

- `**Transport:` found → entry rule: report and stop.
- `pom.xml` at the root → `maven`; `build.gradle` → `gradle`. The main module is the one with
  `contains_main: true` in the active blueprint; its `src/main/resources/application.yml` is
  the file this skill merges into.
- `spring-boot-starter-security` present → the security filter chain owns HSTS, and step 4 is
  skipped. Absent → step 4 writes the filter.
- `spring-boot-starter-jetty` present → topology B and C are not offered: Jetty does not reload
  a bundle, and the certificate would expire with the application running. Say so in the
  question.

### 2 · Interview — two `AskUserQuestion` calls

When a caller already passed an answer in its one-line context, don't ask it again.

**First call — the topology**, with one line of what each costs:

| Option | Means |
|---|---|
| *A · Edge (Recommended)* | An ingress, load balancer or reverse proxy terminates TLS and renews the certificate; the application holds no key and trusts `X-Forwarded-*` from the edge's network only |
| *B · Direct* | The embedded Tomcat terminates TLS on 8443 with a certificate mounted at run time and reloaded on renewal; the application owns the key |
| *C · Mutual TLS* | B, and every caller presents a client certificate from a private CA; a missing one fails the handshake, never a 401 |
| *C′ · Service mesh* | The mesh sidecar terminates TLS; the application is configured as in A |

**Second call**, depending on the first:

- A or C′ — **local edge**: "Run a local Caddy edge in docker-compose, so HTTPS, HTTP/2 and HSTS
  behave on the developer's machine as behind the production edge?" — *Yes (Recommended)* /
  *No — local runs plain HTTP*.
- B or C — two questions in the same call:
  1. **Local profile**: "Should the `local` profile skip HTTPS?" — *Yes — local and docker run
     plain HTTP on 8080 (Recommended)* / *No — local needs a certificate too (mkcert)*.
  2. **Reason** for not terminating at the edge, recorded in the paragraph — *No proxy in
     front* / *Compliance requires TLS up to the process* / *Clients reach the process
     directly*. Topology C also records that the client-certificate authentication mechanism is
     designed later, by `security-architect`, when a use case's access rule names a machine
     caller with a certificate.

### 3 · Write the configuration

Merge into the main module's `application.yml` — into its existing roots, never a second
`server:` or `spring:` key in the same document:

| Topology | Exemplar | Adjust |
|---|---|---|
| A, C′ | `templates/application-tls-edge.yml.example` | nothing |
| B | `templates/application-tls-direct.yml.example` | the first block into the existing roots, the `---` document appended at the end. Local profile *No* → the expression becomes `"!docker & (!test | tls)"` |
| C | same as B | also uncomment the bundle's `truststore` and `server.ssl.client-auth: need` |

`server.http2.enabled: true` goes in for every topology.

### 4 · HSTS — only when step 1 found no Spring Security

Write `templates/HstsHeaderFilter.java.example` into the blueprint's configuration package plus
`.web` (`config.web`, `infrastructure.config.web`); in a blueprint with no configuration package
(hexagonal, onion, custom), into a `web` subpackage of the inbound REST adapter. Base package and
package names come from the blueprint's `packages.map`, never from the exemplar.

With Spring Security present, nothing is written: its default header writer already sends the
same value, and the filter would only override it.

### 5 · The test

| Topology | Exemplar | Where |
|---|---|---|
| A, C′ | `templates/ForwardedHeadersIT.java.example` | `src/test/java/<base package>/` of the main module |
| B, C | `templates/TransportSecurityIT.java.example` | same |

For B and C, every `@SpringBootTest` must run with the `test` profile, or its context now starts
with TLS on and fails reading `/etc/tls` (`@.claude/rules/testing.md` § Slices and context
requires it anyway):

```bash
grep -rL '@ActiveProfiles("test")' $(grep -rl "@SpringBootTest" --include='*.java' src/test/ 2>/dev/null) 2>/dev/null
```

Add `@ActiveProfiles("test")` to each file listed. The generator's own `*ApplicationTests` is
usually the only one.

**A datasource in the context.** When the project has a Testcontainers configuration —

```bash
grep -rl "class TestcontainersConfiguration" --include='*.java' src/test/ */src/test/ 2>/dev/null
```

— every `@SpringBootTest` class of the test you write carries
`@Import(TestcontainersConfiguration.class)`. In `ForwardedHeadersIT` that means **each nested
class**: `@NestedTestConfiguration(OVERRIDE)` drops the enclosing class's configuration, an import
included. Without it, a project with JPA or Flyway starts the context against `localhost:5432` —
connection refused on a clean machine, or another project's database where one is running
(lessons-learned-020 § 2). The exemplars don't carry the import: they are compiled in CI against a
project with no datasource, where the class does not exist.

### 6 · Container — through `docker-architect`

Invoke `docker-architect` through the `Skill` tool with a one-line context, and only in these two
cases. It owns every service block and the `Dockerfile`; don't write either here, not even when
it looks like a copy.

- A or C′ with a local edge → "service `edge` (Caddy) and `docker/caddy/Caddyfile`, chained from
  `transport-security-setup` — no engine question".
- B or C → "`Dockerfile`: the image also listens on 8443 (`EXPOSE 8080 8443`), chained from
  `transport-security-setup` — no service to add".

No `docker-compose.yml` or `Dockerfile` at the root → `docker-architect` stops on its own entry
rule; say so in the report.

### 7 · Record the decision

Write the matching paragraph of `templates/CLAUDE-transport.md.example` into the root
`CLAUDE.md`, placeholders filled, right below the `**Bounded context:` paragraph (or below the
first heading when there is none). That template owns the wording.

### 8 · Verify

When chained by `project-bootstrap`, skip: its own Verify runs next and covers the test this
skill wrote. Otherwise run the project's full build — `./mvnw -B verify` or `./gradlew build`.
A red test is reported with its first failing assertion, never "fixed" by loosening the
configuration.

## Report

```
✅ Transport decided — topology <A edge | B direct | C mutual TLS | C′ mesh>

Configuration . <application.yml path> — <forwarded headers + trusted proxies | SSL bundle `webserver`, reload, 8443, TLS on except <profiles>> · HTTP/2 on
HSTS .......... <Spring Security's default writer | HstsHeaderFilter in <package>>
Test .......... <ForwardedHeadersIT | TransportSecurityIT> — <green in the build | runs in project-bootstrap's Verify> · @ActiveProfiles("test") added to <n files | none needed>
Container ..... <edge (Caddy) added by docker-architect | Dockerfile EXPOSE 8443 by docker-architect | not touched — <reason>>
CLAUDE.md ..... Transport paragraph written
```

Then the lines the person needs on day one, by topology:

- **A / C′** — in each environment, set `TRUSTED_PROXIES` to the edge's addresses (CIDR list);
  the default trusts every private range. With the local edge: `docker compose up -d edge`, then
  `docker compose exec edge caddy trust` once, and open `https://localhost:8443`.
- **B / C** — mount the certificate and key (PEM, PKCS#8) as files and set `TLS_CERTIFICATE` and
  `TLS_PRIVATE_KEY` to their `file:` paths; renew them with an ACME client or the platform, never
  by hand. A Kubernetes secret is mounted as a directory, never with `subPath`. Probes read
  `/actuator/health/readiness` and `/liveness`. Local profile *No* → generate a local pair with
  `mkcert localhost` outside the repository and point the two variables at it.
- **C** — the bundle's truststore holds only the private CA that issues client certificates, from
  `TLS_CLIENT_CA`.

## Contract

**Class:** build — the territory is `skill_classes.build`'s override for this skill in
`@.claude/schemas/extensions.json`: the main module's `application*.yml`, the
`HstsHeaderFilter.java` file, `src/test/**` (the IT, and the test profile on existing
`@SpringBootTest` classes), and the root `CLAUDE.md`. `ArchHook.java guard` enforces it.
`docker-compose.yml`, `docker/**` and the `Dockerfile` are deliberately outside it.

**Reads** the root `CLAUDE.md`, the build file, the active blueprint's `packages.map`, and the
main module's `application*.yml`.

**Writes** the transport configuration, the HSTS filter when no security chain exists, one
transport IT, and the `**Transport:` paragraph — the project fact `security-architect`,
`http-client-architect` and `docker-architect` read.

**Never writes** a certificate, a key, a keystore or a password, in any file.

**Delegates** the `edge` service, the Caddyfile and the `Dockerfile` port to `docker-architect`,
the single owner of both files. Outbound TLS — a client certificate or a private CA for a call
this service makes — is `http-client-architect`'s, never this skill's. The client-certificate
authentication mechanism of topology C is `security-architect`'s, designed with the first use
case that needs it.

**Chained by** `project-bootstrap` (step 7.5, before Verify) and `arch-adopt` (step 7.5), and
invocable by hand. **Travels into the generated project** (`export.skills.include`): `arch-adopt`
runs inside the project, where `project-bootstrap` does not exist, and needs this skill there.
