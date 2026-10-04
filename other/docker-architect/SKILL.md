---
name: docker-architect
description: >
  Extends a project's docker-compose.yml and Dockerfile after project-bootstrap's base
  generation — adds the database or messaging service a modeled use case needs, keeps
  the compose-side image tag consistent with the one test-architect pins in
  TestcontainersConfiguration.java, and syncs with 20-persistencia.md / 40-testes.md.
  Also owns the observability backend behind the OTLP collector: Jaeger, or Grafana +
  Tempo + Prometheus. Use when the request involves adding a service to docker-compose,
  containerizing a new dependency, configuring Testcontainers at the compose level,
  "docker-compose is missing the database", or wanting a dashboard, a trace UI, or
  somewhere to actually look at spans and metrics instead of the collector's `debug`
  stdout — or when a use case spec reports a pending service that persistence-architect,
  messaging-architect or test-architect recorded and did not write.
argument-hint: "[path of the UC-NNN-<slug> folder, or empty for a manual service add]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
model: opus
---

## Current compose state

!`R="${CLAUDE_PROJECT_DIR:-.}"; F="$R/docker-compose.yml"; if test ! -d "$R"; then echo "(could not look: project root '$R' is not a readable directory — this is not an answer about docker-compose.yml)"; elif test -f "$F"; then S=$(awk '/^services:[[:space:]]*$/{s=1;next} /^[^[:space:]#]/{s=0} s&&/^  [A-Za-z0-9_.-]+:[[:space:]]*(#.*)?$/{sub(/[[:space:]]*#.*$/,"");print}' "$F"); if test -n "$S"; then echo "$S"; else echo "(docker-compose.yml exists, and the services: block declares nothing)"; fi; else echo "(no docker-compose.yml at project root — run project-bootstrap first)"; fi`

## Target

$ARGUMENTS

---

# Docker Architect

Keeps `docker-compose.yml` and `Dockerfile` in sync with what the project actually
needs, **after** they're born. `project-bootstrap` writes the base pair — one `app`
service, nothing else — at project creation. Every service added afterward (Postgres,
MySQL, a broker) goes through this skill, so there's one owner instead of
`persistence-architect` and `test-architect` each editing the same YAML their own way.

**Entry rule: without `docker-compose.yml` at the project root, there's nothing to
extend.** If it's missing, stop and say to run `project-bootstrap` — this skill never
generates the base pair, only grows it.

The `## Current compose state` block above answers one of three things, and only the
second one arms that rule:

| Output | Meaning | What to do |
|---|---|---|
| A list of service names | The file exists | Proceed |
| `(no docker-compose.yml at project root …)` | The project root was readable and the file is not there | Entry rule applies: stop |
| `(could not look: project root … is not a readable directory …)` | The root itself couldn't be read — **this is not an answer about `docker-compose.yml`** | Don't apply the entry rule. Read the file at the path the user gave, or ask for the project root; run `/arch-doctor`, which reports `CLAUDE_PROJECT_DIR NOT set` |
| `(docker-compose.yml exists but declares no service …)` | The file is there and malformed or empty | Entry rule doesn't apply — the base pair exists. Read the file before editing |

## How it's invoked

Two paths, both real: `/docker-architect` by hand — when the user wants a service added or
checked, and that is how a pending service recorded by a use case spec gets materialized; and
chained by `project-bootstrap` itself, right after it writes the base pair in its own
step 4.10, once per blueprint feature that's already active and needs a container
(`persistence-jpa` → Postgres, `observability` → the OTLP collector) — see
`project-bootstrap/SKILL.md` step 4.10. A third path: chained by `sonarqube-setup` for a
local `sonarqube` service when the project has no server of its own. That's why it carries no
`disable-model-invocation` — a skill the model can't see is a skill a sibling skill can't
call.

**No longer chained mid-design.** `persistence-architect`, `messaging-architect` and
`test-architect` used to invoke this skill the moment their spec named a missing service;
they now record it in the partial and report the `/docker-architect` command instead.
`ArchHook.java guard` enforces it: this skill is class `build`, and a `build`-class call is
refused while a design run is open. Why it changed: a design run hand-wrote a
`schema-registry` service with no template, no tag verification and no healthcheck, inside a
diff everybody reviewed as a spec (`lessons-learned-012.md` §§ 12, 13). Record:
`@.claude/decisions/0058-skill-classes-territory-schema.md`.

The guard against firing on an unborn project isn't the frontmatter: it's the entry rule
above.

## Why this is a skill and not a subagent

Form 1, motivated by the "Ambos" trigger axis: chained by sibling skills mid-procedure,
and invocable by hand. The closest rejected form was a subagent — it fails the § 5
counter-test in `claude-code-architect-designer`'s decision matrix on all three points:
the service choice is short, its shape fits in `templates/`, and the diff it produces is
a few YAML lines. No context to isolate, no tool to restrict, no model change justified.
Full record: `@.claude/decisions/0029-docker-architect-skill.md`.

Pinned to `opus`, effort inherited: the one procedural skill with an observed design
failure (a broker published to the host and advertised only on the compose network). The
pin lasts for the rest of the turn it fires in
(`@.claude/decisions/0080-procedural-skills-on-sonnet.md`).

## Boundary with neighboring pieces

| Piece | Owns | Doesn't touch |
|---|---|---|
| `project-bootstrap` | Base `Dockerfile` + `docker-compose.yml` (`app` service), once, at generation. Also *decides when* to call this skill for a feature already active in the blueprint (`persistence-jpa`, `observability`) — never writes the service block itself | Any service a use case adds later; the shape of any service block, ever |
| **this skill** | Every service block in `docker-compose.yml`/`Dockerfile` — the ones `project-bootstrap` calls it for at generation, and the ones added later by hand or chained from a UC-driven skill | The engine choice itself — that's `20-persistencia.md`'s call, this skill reads it |
| `persistence-architect` | Engine choice, schema, datasource properties (`20-persistencia.md`) | `docker-compose.yml` directly — invokes this skill instead |
| `messaging-architect` | Broker choice, topic, consumer group (`25-mensageria.md`) | `docker-compose.yml` directly — invokes this skill instead |
| `test-architect` | The pinned image tag inside `TestcontainersConfiguration.java` (one line, Java side) | The compose-side service definition — invokes this skill instead, and both should agree on the same tag |

**The OTLP signal contract has two owners, one per half**, and that is what made
lessons-learned-008 possible. `project-bootstrap`'s
`templates/features/observability/application-observability.yml.example` decides **which
signals the application exports** (`management.otlp.*`); this skill's
`templates/otel-collector-config.yml.example` decides **which signals the collector
accepts** (`service.pipelines`). The OTLP receiver registers no route for a signal that
has no pipeline, so a mismatch is a `404` on every publish cycle, not a startup error.
Adding or removing a signal on either side is a change to both files, in the same commit.
No rule states this — `rules/` is a leaf and cannot name either skill (invariant 1), so
this table is where it lives.

## Procedure

1. **Confirm the base pair exists.** `docker-compose.yml` and `Dockerfile` at the
   project root. Missing either → stop, name what's missing, point to
   `project-bootstrap`.

2. **Find out what's needed.**
   - If the target above names a `UC-NNN-<slug>` folder: read `20-persistencia.md` for the
     engine and version, `25-mensageria.md` for the broker and topic, and `40-testes.md`
     for whether `testcontainers` is active and which image tag `test-architect` already
     pinned in `TestcontainersConfiguration.java`
     (`grep -rn "DockerImageName.parse" src/test`).
   - If called from `project-bootstrap` at generation time: the feature already decided
     it — `persistence-jpa` means Postgres (the engine `application.yml.example`'s
     `datasource.url` already assumes), `observability` means the OTLP collector. No
     engine question to ask, and **no backend question either**: generation stays
     non-interactive, and `project-bootstrap`'s own final report is what tells the user
     the collector exports to `debug` and how to add a UI later. Go straight to step 3.
   - If chained from `sonarqube-setup`: the service is `sonarqube`, already decided by its
     own question (no existing server). No engine question. Go straight to step 3.
   - If invoked manually with no folder: `AskUserQuestion` — engine (Postgres, MySQL,
     Kafka, other), version/tag, port, whether it needs an init script. Don't ask what a
     given spec already answers.

2.5 **Observability backend — ask only when it is actually open.** Conditions, all three:
   invoked manually (not chained), `otel-collector` already in `docker-compose.yml`, and
   no backend service there yet. Otherwise skip this step without mentioning it.

   `AskUserQuestion` with three options, and state what each costs:

   | Answer | What gets merged |
   |---|---|
   | Jaeger | `templates/jaeger-service.yml.example`. One container, traces only, UI on `${JAEGER_UI_PORT:-16686}`. The `metrics` pipeline stays on `debug` |
   | Grafana + Tempo + Prometheus | `templates/grafana-stack-service.yml.example` + its three init scripts. Three containers, both signals, UI on `${GRAFANA_PORT:-3000}` |
   | Keep `debug` | Nothing merged. Say plainly that this means no UI — the collector dumps to its own stdout — and that the question can be re-asked any time by running this skill again |

   Don't recommend by guessing the project's future: Jaeger when only traces are asked
   for, the Grafana stack when the request names metrics or a dashboard. A backend
   already present in `docker-compose.yml` is never replaced by this step — removing one
   is a hand edit the user asks for explicitly.

3. **Check what's already there.** The portrait injected at the top of this file is the
   answer; it lists the keys **inside** the `services:` block and nothing else. When it
   needs to be taken again — the file was edited earlier in the run — take it the same way:

   ```bash
   awk '/^services:[[:space:]]*$/{s=1;next} /^[^[:space:]#]/{s=0} s&&/^  [A-Za-z0-9_.-]+:[[:space:]]*(#.*)?$/{sub(/[[:space:]]*#.*$/,"");print}' docker-compose.yml
   ```

   **Never `grep -A2 "^services:"`.** It reads two lines and stops, so it drops the
   services declared further down and reports the children of `volumes:` as services —
   lessons-learned-012 § 12, where the portrait listed `postgres-data` as a service and
   omitted `kafka` and `otel-collector`. A service already present gets left alone, and
   that decision is only as good as this list: a wrong portrait invites this step to
   recreate what already exists.

4. **Merge the service block.** From the matching `templates/<engine>-service.yml.example`,
   append under `services:` — indentation matched to the file's own, never reformatting
   what's already there. Use the **same image tag** `test-architect` pinned, when one
   exists, so the dev-time container and the integration-test container run identical
   software. If none is pinned yet, use the tag the engine's template ships with and say
   so in the report — `test-architect`'s setup mode is what should pick it up from here,
   not the other way around.

   **A tag that no template ships is verified in the registry, never inferred.** Writing a
   service by hand (§ Service catalog's last paragraph) means choosing a tag, and the same
   discipline invariant 8 applies to a Spring version applies here — a version is not
   written from memory, and "the serializer resolved 8.3.2, so the image is 8.3.2" is
   memory with an extra step:

   ```bash
   docker manifest inspect <repository>:<tag> >/dev/null 2>&1 && echo EXISTS || echo NOT_FOUND
   curl -fsS "https://hub.docker.com/v2/repositories/<repository>/tags/<tag>/" >/dev/null 2>&1 && echo EXISTS || echo NOT_FOUND
   ```

   The first needs a Docker daemon, the second doesn't — run the second when the first
   can't run. `NOT_FOUND` from both, or no network at all → **don't write the tag**: say
   which tag couldn't be confirmed and let the user supply it. A tag that doesn't exist
   fails at `docker compose up`, long after the spec was approved.

   **The healthcheck's binary gets the same treatment.** `curl` or `wget` in a
   healthcheck is an assumption about the image's base. Confirm it, or omit the healthcheck
   and say so in the report — a healthcheck that can never pass marks the service unhealthy
   forever, and every `depends_on: service_healthy` waiting on it hangs.

   **Then give the image a catalog row**, in § Service catalog, before reporting. An image
   used once and never catalogued is an image the next run improvises again, differently.

   Which half leads depends on execution order, and that is why the match isn't only
   promised here: `ArchHook.java compose` compares every `image:` of the compose file with
   every `DockerImageName.parse` under `src/test` and reports a repository whose tags
   disagree. Run it after this step — `java .claude/hooks/ArchHook.java compose` — instead
   of leaving a YAML comment as the only link between the two halves, which is what let a
   tag drift go unnoticed once (`lessons-learned-010.md` § 6).

5. **Wire the app service's environment**, only the variables that change because of
   step 4 (`SPRING_DATASOURCE_URL`/`_USERNAME`/`_PASSWORD` pointing at the new service's
   hostname and port from compose's internal network). For the OTLP collector that is
   **both** endpoint variables, one per signal — `OTLP_ENDPOINT=http://otel-collector:4318/v1/traces`
   and `OTLP_METRICS_ENDPOINT=http://otel-collector:4318/v1/metrics`, matching the two
   placeholders the observability fragment declares. Wiring only the tracing one leaves
   metrics pointed at the app container's own `localhost`, which is silent and wrong.

   **Every pair is host-first by default and container-first in `app`.** The default in
   `application.yml` serves `./mvnw spring-boot:run` on the host, so it names `localhost`
   and a port the service **publishes**. The `app` service's variable names the compose
   hostname and the container port. A service the application reaches with no published
   port leaves the host run with nothing to connect to. The collector shipped like that
   from 0046 until issue #66, and Kafka once shipped with the same mismatch in its
   advertised listeners. `ArchHook.java compose` checks both halves of each pair, reading
   only files.
   Don't invent datasource properties beyond connectivity — sizing and the rest are
   `@.claude/rules/persistence.md`'s and `persistence-architect`'s call, not this
   skill's.

   The backend services from step 2.5 need no variable on the `app` service: the
   application talks only to the collector, and the collector reaches the backend through
   the exporter delta in step 6.

6. **Init script.** Write it under `docker/init/<service>/` and mount it read-only in
   the service's `volumes:`, from the matching `templates/<name>-config.<ext>.example`
   when one exists. For a database service this is conditional on step 2 finding one is
   needed, and skipped entirely when the schema comes from a Flyway migration instead —
   one source of schema truth, not two. For the OTel collector it isn't conditional:
   the collector has no built-in default pipeline and refuses to start without
   `templates/otel-collector-config.yml.example` mounted, so this step always runs for
   that service.

   Same for the backends from step 2.5 — Tempo, Prometheus, and Grafana each refuse to
   start, or start useless, without theirs:

   | Service | Init script | From |
   |---|---|---|
   | `tempo` | `docker/init/tempo/tempo-config.yml` | `templates/tempo-config.yml.example` |
   | `prometheus` | `docker/init/prometheus/prometheus-config.yml` | `templates/prometheus-config.yml.example` |
   | `grafana` | `docker/init/grafana/datasources.yml` | `templates/grafana-datasources.yml.example` |
   | `jaeger` | — none | Jaeger v2 ships a working default |

6.5 **Apply the collector's exporter delta**, and only when step 2.5 merged a backend.
   Edit `docker/init/otel-collector/otel-collector-config.yml` — never a template, never
   a second copy of it — with the `exporters:` entries and the pipeline exporter lists
   written in the header of the backend template just used. Two rules: the `metrics`
   pipeline keeps `debug` when the backend is Jaeger (Jaeger stores no metrics), and an
   exporter is added to `exporters:` rather than replacing what is there. Then note in
   the report that the collector needs `docker compose up -d --force-recreate
   otel-collector` to pick the file up — a mounted config is read once, at start.

7. **Report and stop.** Service added, image tag used (and whether it matches
   `test-architect`'s pin), **how the tag was confirmed** — `docker manifest inspect`, the
   registry's HTTP API, or a template that already shipped it — whether the healthcheck's
   binary was confirmed or the healthcheck omitted, files changed, the catalog row added,
   and — when step 2.5 merged a backend — the UI URL with the variable that moves it
   (`http://localhost:16686`, `JAEGER_UI_PORT`).

   A report that doesn't say how the tag was confirmed is a report that inferred it. Same
   for the healthcheck: a real run wrote both from inference, and neither was mentioned
   (lessons-learned-012 § 13).

   **End the report with the one command that verifies the result** — not optional, and the
   step a real run skipped — and say what it
   catches: `java .claude/hooks/ArchHook.java compose` — every service actually
   `running` rather than `created`, no container from another project holding a host
   port this one publishes, **every published port advertised at an address the host can
   resolve**, and **every `${VAR:default}` the application points at a compose service
   holding on both sides**: the default reaches a port that service publishes, and `app`
   overrides the variable. `docker compose up -d` exits 0 in all four of those failures.

   The third one is the only check in the system that sees it, so say what it means when it
   fires: a service that publishes a port to the host is claiming host reachability, and a
   broker that advertises only its compose-network name breaks that claim on the first
   host-side client — the healthcheck cannot see it (it runs inside the container, where
   `localhost` is the service) and neither can the integration tests (Testcontainers wires
   its own listeners). It reads the file, so run it even with the stack down — that half
   answers without a daemon (lessons-learned-013 § 11).

   Don't start the stack here: nothing has been started yet at this point, and a report about
   containers that do not exist is noise.

   Don't invoke anyone — a sibling skill that chained this one resumes on its own thread.

## Service catalog

| Engine | Template | When **not** |
|---|---|---|
| PostgreSQL | `templates/postgres-service.yml.example` | Engine chosen in `20-persistencia.md` isn't Postgres — or, at bootstrap time, when `persistence-jpa` isn't active in the blueprint |
| MySQL | `templates/mysql-service.yml.example` | Engine chosen in `20-persistencia.md` isn't MySQL |
| Kafka | `templates/kafka-service.yml.example` | Broker chosen in `25-mensageria.md` isn't Kafka, or there is none |
| Schema Registry (Confluent) | `templates/schema-registry-service.yml.example` | `25-mensageria.md` kept the JSON default — which is the rule's default, so this is the common case. Only when the partial recorded the Avro/Protobuf upgrade **and** its trigger. Needs `kafka` in the file, has no volume on purpose (state lives in the `_schemas` topic), and its tag has to match the `kafka-avro-serializer` the POM resolves — verified in the registry, per step 4 |
| OpenTelemetry Collector | `templates/otel-collector-service.yml.example` + init script `templates/otel-collector-config.yml.example` | `observability` isn't active in the blueprint. No engine choice for the collector itself — one vendor-neutral ingest point, always the same shape. Where it *exports* to is a real choice, and it's the next two rows |
| Jaeger | `templates/jaeger-service.yml.example` | No `otel-collector` in the file yet, a backend is already there, or the project wants metrics too — Jaeger stores traces only |
| Grafana + Tempo + Prometheus | `templates/grafana-stack-service.yml.example` + three init scripts (`tempo-config`, `prometheus-config`, `grafana-datasources`) | No `otel-collector` yet, a backend is already there, or three containers is too much for what the project needs — Jaeger is the one-container answer |
| SonarQube (community) | `templates/sonarqube-service.yml.example` | The project already has an external SonarQube server or SonarCloud — `sonarqube-setup` asked, and only its *None* answer chains here. Embedded H2, no database service: local analysis, not a shared server |
| H2 | — no service | In-memory, runs inside the JVM; nothing to containerize |

The collector's default exporter is `debug`, which writes to its own stdout and **is not
a dashboard**. That default is deliberate — this skill doesn't pick an observability
vendor on its own — but it is a starting point, not the end of the road: step 2.5 exists
so the gap gets named out loud instead of waiting for someone to notice that "the traces
work" and "I can see the traces" are different sentences.

Other engines and brokers (Oracle, RabbitMQ, SQS via LocalStack) follow the same shape as
the templates above: image, fixed dev port, named volume for data, healthcheck,
environment for user/password/database (or broker-equivalent). Write the block by hand
from that shape; don't wait for a template to exist before extending a project that needs
one today.

## Contract

**Class:** build — the territory is `skill_classes.build`'s override for this skill in
`@.claude/schemas/extensions.json`: the compose file and the `docker/` tree, nothing else.
`ArchHook.java guard` enforces it, and it also makes this skill **unreachable from inside a
design run** — `/new-feature` and the layer skills record the missing service in the spec,
and the user invokes `/docker-architect` from a prompt of its own afterwards.

**Unfiltered Bash:** verification drives `docker compose` (`up`, `ps`, `logs`), `docker manifest`, `curl` against health endpoints and `java … compose` — the subcommands depend on the services being added, so a fixed list trails the skill. Writes stay under `guard`/`guard bash`, and a force push is blocked by `guard bash` (`guard.force_push`).

**Reads** `docs/use-cases/UC-NNN-<slug>/20-persistencia.md`, `25-mensageria.md`, and
`40-testes.md` when a folder is given; the active blueprint's `features:` (`persistence-jpa`,
`observability`) when called from `project-bootstrap` at generation time; plus
`docker-compose.yml`, `Dockerfile`, `TestcontainersConfiguration.java` (image tag only),
`@.claude/rules/persistence.md`, and `@.claude/rules/messaging.md`.

**Writes** `docker-compose.yml` (every service block, including the ones added at
generation time for an already-active feature), `Dockerfile` (build-stage additions
only, never the base image or base stages `project-bootstrap` wrote), and `docker/init/**`
when an init script is needed. No other skill writes a service block into
`docker-compose.yml` — not even `project-bootstrap`, which only decides *when* to call
this skill — this is the single owner.

**Does not** choose the database engine (`persistence-architect`'s call via
`20-persistencia.md`) or the broker (`messaging-architect`'s call via
`25-mensageria.md`), pin the Testcontainers image tag inside Java (`test-architect`'s one
line in `TestcontainersConfiguration.java`), or write the base
`docker-compose.yml`/`Dockerfile` (`project-bootstrap`, once, at generation). Doesn't
write business code, doesn't touch `.claude/rules/**`.
