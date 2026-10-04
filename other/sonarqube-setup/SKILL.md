---
name: sonarqube-setup
description: >
  Configures SonarQube analysis in a generated or adopted Spring Boot project — the
  scanner plugin in the root build file, the project key and server URL, a CI step when
  the server is external, and a local SonarQube container through docker-architect when
  there is no server yet. Use when the request involves SonarQube, SonarCloud, static
  analysis, quality gate, "configure sonar", or when project-bootstrap or arch-adopt
  finds a project without the scanner plugin.
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion, Skill, Bash(curl:*), Bash(grep:*)
model: sonnet
effort: low
---

# SonarQube Setup

Wires a project to a SonarQube server so the code quality the norms describe is measured
by an analyzer, not only reviewed. One question decides the shape: **does a server already
exist?** Yes → the build and CI point at it. No → a local container runs it, and the
build points there.

**Entry rule: configure once.** If the root build file already declares the scanner —
`sonar-maven-plugin` in `pom.xml`, `org.sonarqube` in `build.gradle` — report "already
configured", name the file and line, and stop. Re-running this skill never rewrites a
working setup; changing the server is a hand edit of two properties.

**The token is a secret and is never written.** Not in `pom.xml`, not in `build.gradle`,
not in the workflow, not "temporarily". The scanner reads `SONAR_TOKEN` from the
environment on its own; the build file carries the URL, which is not a secret, and
nothing else about authentication.

## Why this is a skill (Form 1) and not Form 2

Form 1: `project-bootstrap` and `arch-adopt` chain it by name, and a skill with
`disable-model-invocation: true` cannot be called through the `Skill` tool — the same
reason `git-publish` and `docker-architect` stay model-invocable. Axis 2 of the
interview — two callers, one of which runs inside a project where `project-bootstrap`
does not exist — is what made it a skill of its own instead of a step inside the
bootstrap. The closest rejected form was that step: `arch-adopt` would then have to
write `pom.xml` and `docker-compose.yml` itself, widening its territory and giving the
compose file a second owner. Record: `@.claude/decisions/0091-sonarqube-setup-skill.md`.

Runs on `sonnet` with `effort: low`: a fixed procedure behind one question, every
version resolved by `curl` (`@.claude/decisions/0080-procedural-skills-on-sonnet.md`).

## Procedure

### 1 · Detect the build tool and whether Sonar is already there

`pom.xml` at the root → `maven`. `build.gradle` at the root → `gradle`. Neither → stop:
there is no project to configure. Both → stop and say so; this repo never generates both.

Grep the root build file for `sonar-maven-plugin` / `org.sonarqube`. Found → entry rule
above: report and stop.

### 2 · Ask about the server — one `AskUserQuestion`

Two questions in the same call:

1. **Server** — "Is there already a SonarQube server or SonarCloud organization for this
   project?"
   - *Existing SonarQube server* — the user types its URL under "Other" or in a follow-up.
   - *SonarCloud* — the URL is `https://sonarcloud.io`; ask the organization key.
   - *None — run one locally* — a `sonarqube` container is added to
     `docker-compose.yml` (step 4).
2. **Authentication** — "How does the analysis authenticate?"
   - *Token in `SONAR_TOKEN`* (default) — the variable name only; the value lives in the
     developer's shell and in the CI secret of the same name.
   - *Anonymous* — the server allows analysis without a token. Rare outside a local
     container; say so. On a local SonarQube it is **not** the default: three server
     settings have to change first, and the report lists them (§ Report). Without them the
     scan fails only at its end, after a full `verify`, one missing setting per run.

When a caller already passed an answer in its one-line context, don't ask it again.

### 3 · Write the build configuration

Resolve the scanner version on the repository itself — never from memory, same rule
`project-bootstrap/references/build-maven.md` § 4.6 applies to every plugin:

```bash
# maven
curl -sS 'https://repo1.maven.org/maven2/org/sonarsource/scanner/maven/sonar-maven-plugin/maven-metadata.xml' | grep -o '<release>[^<]*</release>'
# gradle — the plugin lives on the Gradle Plugin Portal, not on Maven Central
curl -sS 'https://plugins.gradle.org/m2/org/sonarqube/org.sonarqube.gradle.plugin/maven-metadata.xml' | grep -o '<release>[^<]*</release>'
```

No network → don't write a version: say which one could not be resolved and let the user
supply it.

Then merge — never replace what the root build file already has:

| Tool | Exemplar | Where |
|---|---|---|
| maven | `templates/pom-sonar.xml.example` | properties into the root POM's `<properties>`, the plugin into `<build><pluginManagement><plugins>` |
| gradle | `templates/build-gradle-sonar.example` | the plugin into the root `plugins {}`, the `sonar {}` block at the root level — not inside `subprojects` |

`sonar.projectKey` is `<groupId>:<artifactId>` from the root build file. `sonar.host.url`
is the URL from step 2, or `http://localhost:9000` for the local container.
`sonar.organization` only for SonarCloud. Coverage needs no property: the scanner's
default report paths are exactly where the JaCoCo setup `project-bootstrap` writes puts
them (`target/site/jacoco/jacoco.xml`, `build/reports/jacoco/test/jacocoTestReport.xml`).

The `sonar.issue.ignore.multicriteria` entries go in as written, whether or not the files
they name exist yet: each is scoped to one rule and one file, a file absent from the project
matches nothing, and the idempotency templates that produce those files point back at them.
Don't add an entry of your own here — a finding in the project's code is fixed, not muted.

### 4 · Local server — only when step 2 answered *None*

Invoke `docker-architect` through the `Skill` tool with a one-line context:
"service `sonarqube`, chained from `sonarqube-setup` — no engine question". It owns every
service block in `docker-compose.yml`, and its template for this one is
`templates/sonarqube-service.yml.example` there. Don't write the block here, not even
when it looks like a copy: that is the ownership split, not a style choice.

No `docker-compose.yml` at the root → `docker-architect` stops on its own entry rule.
Report that the build points at `http://localhost:9000` and nothing runs there yet.

### 5 · CI — only when the server is external

A local container is unreachable from a CI runner, so this step runs **only** for an
existing server or SonarCloud. Merge `templates/ci-sonar-step.yml.example` into
`.github/workflows/build.yml` (the file `project-bootstrap` step 6.5 writes): job-level
`env`, `fetch-depth: 0` on the checkout, and the analysis step after `verify`. The step
is skipped while the `SONAR_TOKEN` secret is absent — a fork's pull request has none, and
a red build there would say nothing about the code.

No `.github/workflows/build.yml` → skip, and say it in the report.

## Report

```
✅ SonarQube configured — <existing server <url> | SonarCloud <org> | local container>

Build ....... <pom.xml | build.gradle> — scanner <version> (resolved from <repository>)
Project key . <groupId:artifactId>
Server ...... <url> · auth: <SONAR_TOKEN | anonymous>
Compose ..... <sonarqube added by docker-architect, tag <tag> | not touched — external server>
CI .......... <step added, runs when secret SONAR_TOKEN is set | skipped — local server | skipped — no workflow>

Access check (before any scan):
  curl -s <url>/api/authentication/validate      → {"valid":true} when anonymous is allowed
  (or SONAR_TOKEN is exported — the scanner reads it)

First run:  <./mvnw -B verify sonar:sonar | ./gradlew build sonar>
Rerun:      <./mvnw -B sonar:sonar | ./gradlew sonar>   — same build output, no tests again
```

The access check moves an authentication failure from the end of the scan to its start:
`validate` answers in milliseconds, the scan fails only after `verify` has run every test.
The rerun line is for a change on the server side — a setting, a permission, a quality
profile — where the code and `target/` (or `build/`) are unchanged.

For the local container, add three lines the person needs on day one: start it with
`docker compose up -d sonarqube`, the first login is `admin`/`admin` and forces a
password change, and a token is created under *My Account → Security*, then exported as
`SONAR_TOKEN`.

When step 2 answered *Anonymous* for the local container, replace the token line with the
three settings, in this order, and say they are for a local container only — each one
opens the server to anyone who can reach it:

1. *Administration → Configuration → General Settings → Security* — **Force user
   authentication** off. On by default; with it on, `validate` answers `{"valid":false}`.
2. *Administration → Security → Global Permissions*, group **Anyone** — **Execute
   Analysis**. Without it the scanner fails with *"You're not authorized to analyze this
   project or the project doesn't exist on SonarQube and you're not authorized to create
   it."*
3. Same page, same group — **Create Projects**. Needed for the first scan only, while the
   project key does not exist yet. For an external server, the one thing to do by hand: create the
`SONAR_TOKEN` repository secret.

## Contract

**Class:** build — the territory is `skill_classes.build`'s override for this skill in
`@.claude/schemas/extensions.json`: the root build file and `.github/workflows/**`,
nothing else. `ArchHook.java guard` enforces it. `docker-compose.yml` is deliberately
outside it.

**Reads** the root `pom.xml` or `build.gradle` (coordinates, existing plugins), and
`.github/workflows/build.yml` when it exists.

**Writes** the scanner plugin and the `sonar.*` properties into the root build file —
the only change to that file outside a feature round besides `project-bootstrap`'s
generation and the two installers' own setup — and the analysis step into the workflow
when the server is external.

**Never writes** a token, a password, or any credential value, in any file.

**Delegates** the `sonarqube` compose service to `docker-architect`, the single owner of
every service block.

**Chained by** `project-bootstrap` (step 8.4, after Verify) and `arch-adopt` (step 7), and invocable
by hand. **Travels into the generated project** (`export.skills.include`): `arch-adopt`
runs inside the project, where `project-bootstrap` does not exist, and needs this skill
there.
