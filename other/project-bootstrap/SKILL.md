---
name: project-bootstrap
description: >
  Creates the complete initial structure of a Spring Boot project from a declarative
  architecture blueprint. Use when the user asks to create a project from scratch,
  start a new project, set up a project, scaffolding, "new Spring project",
  bootstrap, generate a module structure, create a multi-module Maven or Gradle
  project, build a hexagonal architecture, clean architecture, onion, layered, vertical
  slice or modular monolith, or when the /init-project command is run.
allowed-tools: Read, Write, Edit, Bash, Glob, Skill
model: sonnet
effort: high
---

# Project Bootstrap

Turns an empty directory into a Spring Boot project with declared architectural
boundaries, active hooks, and a green build.

**Does not write business code.** No example, no seed, no demo aggregate. It emits
module structure, packages, POMs, configuration, enforcement, rules, and skills — and
stops there. Classes come from the `/new-feature` pipeline, from a real spec. A `User`
aggregate invented by the bootstrap competes with that spec and diverges from the
layer skills' exemplars, which own the shape. Record:
`@.claude/decisions/0011-bootstrap-without-business-code.md`.

The only Java in the freshly generated project is what the Initializr brings — the
`@SpringBootApplication` class and the context test — plus one `package-info.java` per
role in `packages.map` (step 4.7).

## Dependencies

`java` (JDK 21+) · `git` · `curl`. **Nothing else.** `mvn`/`gradle` on the PATH are not
required — the Initializr's `starter.tgz` already brings the matching wrapper (`mvnw` or
`gradlew`, whichever `build.tool` resolved to).

No Python, no template engines, no bash. The hooks are a single Java file run in
single-file source mode, which makes them identical on Linux, macOS, and Windows — the
same dependency the target audience already has mandatorily.

## When NOT to use

`pom.xml` or `build.gradle` already exists at the root. This skill **does not migrate**
existing projects nor overwrite structure. In that case: stop, report, suggest
`/new-feature` instead.

## Preconditions

```bash
java --version && git --version && curl --version | head -1
ls ${CLAUDE_SKILL_DIR}/templates/*.example
```

Check that the exemplars the procedure cites are there. Some are conditional on the
active blueprint's `build.tool` — **check only the ones the resolved tool needs**, per
the table below:

| Build tool | Exemplars (step 4) |
|---|---|
| `maven` | `pom.parent.xml.example` and `pom.module.xml.example` |
| `gradle` | `settings.gradle.example`, `build.gradle.parent.example`, and `build.gradle.module.example` |

The rest are shared regardless of `build.tool`: `checkstyle.xml.example` and
`checkstyle-test.xml.example` (4.6),
`lombok.config.example` (4.8), `Application.java.example`
and `application.yml.example` (step 3), `features/actuator/application-actuator.yml.example`
and `features/observability/application-observability.yml.example` and
`features/observability/ApplicationTests-tracer.java.example` (4.7),
`docker-compose.yml.example` (4.10) plus **either** `Dockerfile.example` (`maven`) **or**
`Dockerfile-gradle.example` (`gradle`) — never both,
`root.CLAUDE.md.example` and `module.CLAUDE.md.example` (step 6),
`settings.json.example` and `audit-pricing.json.example` (step 6.6, written by the
`export` mode, not by hand), **either**
`ci.yml.example` (`maven`) **or** `ci-gradle.yml.example` (`gradle`) — never both (step
6.5), `README.md.example` and `README.pt-br.md.example` (step 8.5), and
`GENESIS.md.example` (step 8.6) — plus whatever the
active blueprint's `templates:` declares. Don't count files against a fixed number: the
folder grows, the number falls behind, and the precondition starts failing for nothing.
If a cited exemplar is missing, or a tool is missing: **stop and report**, naming what's
missing. Don't improvise a root POM/build.gradle or invent Spring Boot versions from
what you think you know — the version you have in memory is stale by construction.

**This skill generates exactly one build system per project — Maven or Gradle, never
both.** `build.tool` in the blueprint YAML picks it, and it's overridable once at
initialization (step 1's interview); once resolved, every later step branches on that
single value and only ever touches that tool's exemplars. Writing a `pom.xml` and a
`build.gradle` side by side (or vice versa) in the same generated project is a bug in
this procedure, not a harmless extra — Maven and Gradle disagree about which one is
authoritative, `./mvnw` and `./gradlew` both exist and diverge on the first dependency
bump, and every downstream skill that shells out to a build tool (`test-architect`,
`archunit-installer`, CI) has to guess which one is real.

Step 4.10 additionally reads `docker-architect`'s own `templates/postgres-service.yml.example`
and `templates/otel-collector-service.yml.example` (plus its
`templates/otel-collector-config.yml.example`) when `persistence-jpa` or `observability`
is active — see § 4.10. Missing either when the matching feature is active: same
stop-and-report rule.

Naming convention: the `.example` suffix always comes **last**
(`pom.parent.xml.example`, `DomainException.java.example`). An exemplar with the suffix
in the middle escapes the glob above and the precondition turns green without the file
existing.

## Procedure

### 1 · Select the blueprint

List `.claude/blueprints/*/*.yaml` dynamically (never a fixed list in the prompt) —
each architecture lives at `.claude/blueprints/<id>/<id>.yaml`; folders without a
`.yaml` (architecture not yet written) don't appear in the list. If the user hasn't
indicated which one, show `references/blueprint-selection.md` with each one's
`when_to_choose` and `trade_offs`, and ask. **Never assume** the architecture: it's the
most expensive decision to reverse in the whole project.

The blueprint's `build.tool` (`maven` or `gradle`) is a default, not a lock-in — if the
user hasn't said which build tool they want, confirm the blueprint's default with them
here, once, same interview. Don't ask again later: step 2 resolves the final value and
every step from step 3 on assumes it's already settled.

### 2 · Validate the blueprint

Read the YAML and check, one by one:

| # | Rule | If it fails |
|---|---|---|
| 1 | `id`, `name`, `build`, `modules`, `packages`, `dependency_rules`, `features`, `architecture_paths` all exist | Stop and name the missing field |
| 2 | The `depends_on` graph is acyclic | Stop and show the cycle |
| 3 | Exactly **one** module with `contains_main: true` | Stop and list the candidates |
| 4 | Every `feature` referenced by a module exists in `features` | Stop and name the feature |
| 5 | Every `templates.<role>` points to an existing file | Stop and name the path |
| 6 | `architecture_paths` is not an empty list | Stop — without this, step 6.6 has nothing to write |

Don't invent defaults for `dependency_rules` — it's the backbone of the enforcement.

**Resolve the effective build tool now, before step 3.** `build.tool` in the blueprint
is the default; `@.claude/blueprints/_schema.md` documents it as "Overridable at
initialization" — if the user asked for the other tool during step 1's interview, that
override wins. Whatever the final value — `maven` or `gradle` — every step from here on
branches on it once and stays with that choice. Never generate both.

### 3 · Generate the base with Spring Initializr

The Initializr's `type=` parameter is what actually picks the build system — everything
downstream just follows the file shapes it produces:

```bash
# build.tool: maven
curl -sS https://start.spring.io/starter.tgz \
  -d type=maven-project \
  -d language=java \
  -d groupId=<groupId> \
  -d artifactId=<artifactId> \
  -d name=<name> \
  -d packageName=<packageBase> \
  -d javaVersion=21 \
  -d dependencies=<list derived from the features> \
  | tar -xzf - -C .

# build.tool: gradle — same parameters, only `type` changes. Groovy DSL
# (`gradle-project`), not Kotlin DSL (`gradle-project-kotlin`): this skill's own
# exemplars (§ 4) are Groovy, and mixing DSLs between what the Initializr emits and what
# this skill writes on top of it is its own silent divergence.
curl -sS https://start.spring.io/starter.tgz \
  -d type=gradle-project \
  -d language=java \
  -d groupId=<groupId> \
  -d artifactId=<artifactId> \
  -d name=<name> \
  -d packageName=<packageBase> \
  -d javaVersion=21 \
  -d dependencies=<list derived from the features> \
  | tar -xzf - -C .
```

Run **exactly one** of the two, matching the build tool resolved above. Maven's
`starter.tgz` extracts `pom.xml`, `mvnw`, `mvnw.cmd`, and `.mvn/wrapper/`; Gradle's
extracts `build.gradle`, `settings.gradle`, `gradlew`, `gradlew.bat`, and
`gradle/wrapper/`. There's no third case where both sets exist — if a stray `pom.xml` or
`build.gradle` is left over from a previous attempt in this directory, that's the "already
exists" case from § When NOT to use, not something to merge with the tool just generated.

`javaVersion=21` is not a pin from memory — it's this skill's own precondition (JDK
21+, see § Dependencies) made explicit. Without it the Initializr falls back to its own
default, which has been observed to be an older LTS than what this skill requires;
letting that happen means the generated `pom.xml`/`build.gradle` and
`dependency-catalog.md`'s reasoning about the target JDK silently disagree.

The Initializr **is** the version oracle for everything else: it returns the current
Spring Boot GA, with nothing pinned in this repository. Confirm what came back:

```bash
# maven
grep -m1 '<version>' pom.xml && grep -m1 'java.version' pom.xml

# gradle
grep -m1 "id 'org.springframework.boot'" build.gradle && grep -m1 'sourceCompatibility\|JavaVersion' build.gradle
```

If the network isn't available, **stop and ask** the user for the versions. Never write
them from memory. If you pin `bootVersion` explicitly, don't use the `.RELEASE`
suffix — see the note in `references/dependency-catalog.md`.

Feature → Initializr dependency mapping in `references/dependency-catalog.md`.

### 4 · Restructure according to the blueprint

Branch once on the build tool resolved before step 3, and stay on that branch for the
rest of this step — **write only the files of the tool actually chosen.** A `gradle`
project never gets a `pom.xml`, `mvnw`, or `.mvn/`; a `maven` project never gets a
`build.gradle`, `settings.gradle`, or `gradlew`.

**Read `references/build-<tool>.md` § 4 — only the tool just resolved — then
`references/scaffold.md` § 4.** The first holds the tool's file layout (POMs or Gradle
scripts, wrapper); the second what both tools share, including the andaime rule every
later template copy follows. Done when every module of the blueprint exists with its
`depends_on` wired in the build files, and nothing of the other tool is on disk.

The steps from here to 8.6 run **in order, every one of them.** Each heading below names
the reference that holds its body; open it before executing the step — the spine alone is
not the procedure.

### 4.5 · Domain exception family — not here → `references/scaffold.md` § 4.5

Nothing is generated: the exception family belongs to `domain-modeling`. Read the section
for why, so step 4.7 does not reintroduce it.

### 4.6 · Generate the Checkstyle config → `references/build-<tool>.md` § 4.6, then `references/scaffold.md` § 4.6

`config/checkstyle/checkstyle.xml` plus the tool's plugin, bound to `validate`, and
`config/checkstyle/checkstyle-test.xml`, the light rule set for `src/test`. Done when the
build file carries the plugin and both configs exist.

### 4.7 · Materialize the packages and feature configuration → `references/scaffold.md` § 4.7

One `package-info.java` per role in `packages.map`, plus the `application*.yml` of each
active feature. No other `.java`.

### 4.8 · Generate the `lombok.config` → `references/scaffold.md` § 4.8

At the project root.

### 4.9 · Generate the `logback-spring.xml` → `references/scaffold.md` § 4.9

Under `src/main/resources` of the module with `contains_main: true`.

### 4.10 · Generate the base `Dockerfile` and `docker-compose.yml` → `references/scaffold.md` § 4.10

Base pair, plus one service per active feature that needs a container, merged through
`docker-architect`'s templates.

### 5 · Generate the boundary map → `references/project-files.md` § 5

**Read `references/project-files.md` now** — it holds steps 5 to 7.
`.claude/forbidden-imports.txt`, one line per `forbidden_imports` prefix.

### 6 · Generate the root CLAUDE.md and the module ones → `references/project-files.md` § 6

### 6.5 · Generate CI → `references/project-files.md` § 6.5

Exactly one workflow template — the one of the resolved build tool.

### 6.6 · Write the project's `.claude/` → `references/project-files.md` § 6.6

`ArchHook.java export` writes rules, skills, agents, hook, schema and settings, and
rewrites the rules' `paths`. Nothing in the generated project may depend on this
repository.

### 7 · What the enforcement you just installed does → `references/project-files.md` § 7

Nothing to run — what the final report has to be able to say.

### 8 · Verify → `references/build-<tool>.md` § 8, then `references/verify-and-report.md` § 8


Everything in this step branches on the same build tool resolved before step 3 — run
**only** the column that matches.


**Read `references/verify-and-report.md` now** — it holds steps 8 to 8.6. Done when the
build passes, or when the report says why it failed.

### 8.4 · Configure SonarQube → skill `sonarqube-setup`

Invoke `sonarqube-setup` via the `Skill` tool, with a one-line context: build tool and
coordinates. It owns the one question this step asks — an existing server (URL,
authentication) or a local container — and the scanner in the root build file, the CI
step for an external server, and, for a local one, the `sonarqube` service it hands to
`docker-architect`. After Verify, so the build it touches is already known green; before
the README, so step 8.5's `{{outputContractBlock}}` carries its `SonarQube:` line. The
chained skill joins this phase instead of replacing it — same class, territories summed
(`@.claude/decisions/0092-guard-same-class-chain-sums-territories.md`) — so the steps after
it still write. Don't write any `sonar.*` line here.

### 8.5 · Generate the project README → `references/verify-and-report.md` § 8.5

`README.md` (English) and `README.pt-br.md`, after Verify.

### 8.6 · Write the audit genesis record → `references/verify-and-report.md` § 8.6

`.claude/audit-usage/GENESIS.md`, once.

## Output contract

```
✅ Project <name> created — blueprint <id>

Modules:
  <path> → depends on <list>
  ...

Versions (resolved by the Initializr): Java <x> · Spring Boot <y> · <build tool>
Active features: <list>
Business code: none — by design. <n> package-info.java written
Boundaries: <n> rules in .claude/forbidden-imports.txt — blocking verified ✓
Checkstyle: config/checkstyle/checkstyle.xml — plugin <v> · tool <v>, validate phase · checkstyle-test.xml over src/test
Spotless: check bound to the build (verify / check) — formatting and unused imports, main and test
Lombok: lombok.config at the root — @Data and @Setter stop compilation
ArchUnit: to be installed — `test-architect` skill (see Next steps)
Coverage: JaCoCo generates a report; the 80%/70% gate comes in with `test-architect`
Self-contained: <n> rules + <n> skills + <n> agents + ArchHook.java + extensions.json written by `ArchHook.java export` — no dead paths ✓
Provenance: .claude/.arch-provenance.json — blueprint <id>, ref <ref>, commit <short sha>. `/arch-doctor` reports anything edited since
Audit trail: .claude/audit-usage/ active — one report per skill or agent invocation from now on, by `/command` or by the model. GENESIS.md records this run itself. Fill pricing.json to see cost
Docker: Dockerfile + docker-compose.yml — <list: app, plus one entry per service `docker-architect` merged in step 4.10 for an active feature, e.g. "postgres (persistence-jpa)", "otel-collector (observability)"> — extend with `docker-architect` for anything a future use case adds
Observability UI: <omit this line entirely when `observability` is not active> none — the collector exports to `debug`, which writes spans and metrics to its own stdout and is not a dashboard. Run `/docker-architect` to add one: Jaeger (traces, one container) or Grafana + Tempo + Prometheus (traces and metrics, three)
SonarQube: <the first line of `sonarqube-setup`'s report — existing server <url> | SonarCloud <org> | local container on http://localhost:9000> — scanner <v>, CI step <added | none>
MCP: <none — no server designed for this project yet | <n> server(s) copied to .mcp.json, see MCP-SETUP.md>
Build: <PASSED | FAILED: reason>
Docs: README.md (English, default) + README.pt-br.md — origin, blueprint, stack, skills/agents, this report

Next steps:
  1. /use-case-design <first-use-case-name>
  2. Install the architecture tests (ArchUnit) and wire up the coverage gate with the
     `test-architect` skill as soon as business classes exist. Until then boundaries
     are guaranteed only by the hook (inside Claude Code)<, and by the POMs'
     `depends_on` (in the build) — only if `layout: multi-module`>.
  3. SonarQube — <local: `docker compose up -d sonarqube`, log in at http://localhost:9000
     as admin/admin (a password change is forced), create a token under My Account →
     Security, `export SONAR_TOKEN=…`, then `<./mvnw -B verify sonar:sonar | ./gradlew build sonar>`
     | external: create the `SONAR_TOKEN` repository secret; CI analyses from the next push>
```

The part between `<>` in line 2 only appears if the blueprint is `layout:
multi-module`. In `single-module` there's no per-layer POM and the compiler enforces no
boundary at all: outside Claude Code the project has no enforcement whatsoever until
ArchUnit is installed. Write that, in those words — the generic sentence promises a
build guarantee that doesn't exist.

The ArchUnit and coverage lines aren't optional: without them the user ends up thinking
`code-quality.md`, `architecture-ddd.md`, and `testing.md` already have full automatic
verification. They have part of it — Checkstyle and `lombok.config`. The other two come
in with `test-architect`, and until they do, `verify` checks neither dependency
direction nor coverage.

Neither is the business-code line: a user used to scaffolds expects to find an example
controller. Writing "none — by design" is what keeps them from looking for it and
concluding the generation failed.

## Applicable rules

Every rule in `.claude/rules/` reaches the project through step 6.6 — `ArchHook.java
export` copies them and rewrites their `paths`. **None is read during generation:** the
part of each rule that a bootstrap step turns into a file is already inside the template
that step copies. The table says which, so a rule change knows which template to follow.

| Rule | Embodied by | Step |
|---|---|---|
| `@.claude/rules/architecture-ddd.md` | the blueprint's modules and `depends_on`, `.claude/forbidden-imports.txt`; its `paths` come from `architecture_paths` at export | 4, 5, 6.6 |
| `@.claude/rules/naming.md` | the package names written into `package-info.java` | 4.7 |
| `@.claude/rules/code-quality.md` | `templates/checkstyle.xml.example` — the mechanical half; the ArchUnit half is `test-architect`'s | 4.6 |
| `@.claude/rules/lombok.md` | `templates/lombok.config.example` | 4.8 |
| `@.claude/rules/logging.md` | `templates/logback-spring.xml.example` | 4.9 |
| `@.claude/rules/testing.md` | nothing here — the coverage gate is wired by `test-architect` | — |
| `@.claude/rules/error-handling.md` · `@.claude/rules/api-rest.md` | nothing here — no exception family or handler is generated (4.5) | — |

A rule that changes what a template must say is followed by an edit to that template, not
by a read here. If a step ever needs a rule that doesn't exist in `rules/`, create the rule
file first — don't write it inside this skill.

## Why this is a skill and not an agent

Form 1 (auto-invocable skill): it is a long generation procedure with no interview of its
own, and `/init-project` already isolates the verbose part inside the `project-initializer`
agent. Form 3 was rejected for this file because the three reasons for an agent (preserve
context, restrict tools, change model) are satisfied by that caller, not by this procedure —
two nested agents would only add a second boundary to pass the blueprint across.

Runs on `sonnet` with `effort: high`: generation is template- and YAML-driven, and it runs inside `project-initializer`, also on `sonnet`. A skill's `model` inside a subagent is not documented, so the pin there is a declaration that agrees with the agent's (`@.claude/decisions/0081-skill-model-required-per-class.md`).

## Contract

**Class:** build — the territory is `skill_classes.build`'s override for this skill in
`@.claude/schemas/extensions.json`: the whole tree of the project being generated. It is the
only skill with that reach, and it has it because the tree does not exist yet when it runs.
`ArchHook.java guard` enforces it.

**Unfiltered Bash:** generation runs `curl` against the Initializr, `tar`, `./mvnw`, `java … export`, `grep` and moves over a tree that does not exist yet — a scoped list would run to ~15 prefixes, and one command missing from it aborts the run halfway through. Writes stay under `guard`/`guard bash`, and a force push is blocked by `guard bash` (`guard.force_push`).

**Reads before generating:**

- `.claude/blueprints/<id>/<id>.yaml` — the blueprint chosen in step 1
- `references/blueprint-selection.md` and `references/dependency-catalog.md` — steps 1 to 3
- `references/build-<tool>.md` — step 4, **only** the resolved tool's
- `references/scaffold.md` — step 4
- `references/project-files.md` — step 5
- `references/verify-and-report.md` — step 8

No rule file is read: § Applicable rules says where each one already lives in a template,
and step 6.6's copy is `export`'s, not a transcription.

**Writes** (paths relative to the **generated project**, not this repository) — no
other skill touches these files:

- Exactly one of: `pom.xml` and `*/pom.xml` (`build.tool: maven`), or `settings.gradle`,
  `build.gradle`, and `*/build.gradle` (`build.tool: gradle`) — never both in the same
  project, see step 4
- `CLAUDE.md` and `*/CLAUDE.md`
- `.claude/forbidden-imports.txt`
- `.claude/rules/*.md` — every rule of this repo, `paths` derived, see step 6.6
- `.claude/skills/**` and `.claude/agents/**` — whatever `export`'s `include` lists, see
  step 6.6. The list is data in `@.claude/schemas/extensions.json`, not prose here
- `Dockerfile` and `docker-compose.yml` — base pair, step 4.10, plus (via
  `docker-architect`'s own templates and merge procedure, called from the same step)
  one service per blueprint feature that's already active and needs a container
  (`persistence-jpa`, `observability` today). Every service a **use case** adds
  afterward is `docker-architect`'s alone, invoked on its own thread, not this skill's
- `.claude/hooks/ArchHook.java` — copy, see step 6.6
- `.claude/schemas/extensions.json` — copy without its own `export` block, see step 6.6
- `.claude/settings.json` — written whole, see step 6.6
- `.claude/audit-usage/pricing.json` and the `.claude/audit-usage/` directory itself —
  step 6.6. The reports and `history.jsonl` inside it are written afterwards by
  `ArchHook.java audit`, never by this skill
- `.claude/audit-usage/GENESIS.md` — step 8.6, once, the only report in that directory
  this skill ever writes itself. Everything else in that directory after it is
  `ArchHook.java audit`'s alone
- `.mcp.json` and `MCP-SETUP.md` — **only if** `templates/mcp.json.example` exists, step
  6.6 as an optional copy. Absent in most bootstraps, on purpose
- `config/checkstyle/checkstyle.xml` and `config/checkstyle/checkstyle-test.xml`
- `lombok.config`
- `src/main/resources/application*.yml`
- `src/main/java/**/package-info.java` — one per role in `packages.map`, step 4.7. **No
  other `.java`**: business classes come from the `/new-feature` pipeline
- `.github/workflows/*`
- `README.md` and `README.pt-br.md` — step 8.5, after Verify. English is the default,
  Portuguese the linked option

`.gitignore` is deliberately left out — it comes from the Initializr (step 6.5).

**Chains** `sonarqube-setup` in step 8.4 — the `sonar.*` lines of the root build file,
the workflow's analysis step and the `sonarqube` compose service are that skill's (and,
for the service, `docker-architect`'s), even though they land in files this skill wrote.

**Hands off to** `use-case-design`, `domain-modeling`, `persistence-architect`,
`rest-api-architect`, and `test-architect`, which design the first feature. The
architecture tests and the coverage gate belong to `test-architect`'s setup mode —
this bootstrap deliberately doesn't generate them.

**Does not write business code, and this is the § of the contract that says so.** No
`.java` beyond the `package-info.java` files, no `.sql`, no file in `src/test/**`. If a
future step needs to emit a class, the right question is which layer skill owns that
shape — not how to add one more exemplar here.
