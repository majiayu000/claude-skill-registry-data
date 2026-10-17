---
name: sonar-lessons
description: >
  Runs this project's SonarQube analysis, extracts the quality gate, bugs,
  vulnerabilities, code smells, duplication and coverage through the SonarQube Web API,
  traces every group of findings to the norm, template or Checkstyle setting in `.claude/`
  that produced it, and writes `docs/lessons-learned/sonar-NNN.md` focused on fixing the
  cause so the next analysis has fewer issues or none. Ends with the `/report-issue` command
  that files it on the Nerviz repository, where the fix belongs.
  Explicit invocation only.
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Grep, Bash(./mvnw:*), Bash(./gradlew:*), Bash(curl:*), Bash(java:*)
model: opus
effort: high
---

# Sonar Lessons

Turns one SonarQube analysis into a lesson the **meta-repository** can act on. A Sonar
issue in a generated project is almost never a one-off: the code came from a template, a
norm allowed it, or nothing in `.claude/` said anything and the model decided alone. Fixing
it here fixes one project; fixing the owner fixes every project generated afterwards. This
skill finds the owner and writes it down; `/report-issue`, typed by the user, hands it to the
repository that owns it.

**Entry rule: this skill runs the analysis, it never sets it up.** No scanner in the root
build file, no server answering, no token — stop and say which one, and what fixes it. It
writes nothing outside `docs/lessons-learned/`: not the build file, not the compose file,
not the token.

**The local file is complete; the issue is not this skill's.** Project paths, lines and
excerpts all belong in `sonar-NNN.md`. What may leave the project — and the privacy rule that
decides it — is owned by `/report-issue`
(`@.claude/decisions/0103-issue-filing-and-skeptical-triage.md`).

## Why this is a skill (Form 2) and not an agent

Form 2 because a full `verify` plus analysis is a side effect the model must not trigger on
its own — axis 2 of the design interview: the user types `/sonar-lessons`, nothing chains
it. Publishing the issue was the second such effect until `0103` moved it to `/report-issue`,
the one door from a generated project to the meta-repository. The symptom behind it (axis 1) was the same
long prompt pasted into every feature round to produce a Sonar lessons-learned by hand. The
closest rejected form was the same skill plus a `sonnet` collector agent holding the build
log and raw JSON; it failed the counter-test of invariant 5, since `facets` and small pages
already keep the extraction short. Record: `@.claude/decisions/0100-sonar-lessons-skill.md`.

Runs on `opus`: step 4 — deciding which norm or template owns a finding, and what the fix
at the owner is — is the judgment the hand-written lessons-learned needed.

## Procedure

Endpoints, parameters and response fields of every call below:
`references/sonar-web-api.md`. Every `curl` authenticates with `-u "$SONAR_TOKEN:"` and
never prints the variable.

### 1 · Preconditions — stop on the first that fails

1. Root build file: `pom.xml` → maven, `build.gradle` → gradle. Neither → stop: nothing to
   analyze (this is also what happens when the skill is typed in the Nerviz
   repository itself).
2. Scanner declared — `sonar-maven-plugin` / `org.sonarqube` in that file. Absent → stop:
   "run `/sonarqube-setup` first".
3. `sonar.host.url` and `sonar.projectKey` read from the build file (`sonar.organization`
   too, for SonarCloud).
4. `curl -sS <host>/api/system/status` answers `"status":"UP"`. Connection refused on
   `localhost` → stop: "`docker compose up -d sonarqube`, wait for `UP`, re-run". Any other
   host → stop, naming the host.
5. `SONAR_TOKEN` set and valid — `curl -sS -u "$SONAR_TOKEN:" <host>/api/authentication/validate`
   answers `"valid":true`. Unset or invalid → stop, naming the variable.
6. Browse permission — one `component_tree` read with `ps=1`, the call step 3's duplication
   read makes (`references/sonar-web-api.md` § Preconditions). `403` → stop with the
   project-analysis-token message below, before step 2 spends minutes on an analysis
   nothing can read. `404` → the project has never been analyzed: go on, and the first
   read of step 3 proves Browse instead, stopping the same way on a `403`.

### 2 · Run the analysis

| Tool | Command |
|---|---|
| maven | `./mvnw -B -q verify sonar:sonar` |
| gradle | `./gradlew -q build sonar` |

`-q` rather than a redirect to a log file: the output stays short, and a redirect is a
write outside this skill's territory. A red build stops here — report the failing module
and the first error line; a lessons-learned about an analysis that never ran is fiction.

The analysis is **asynchronous**. Read `ceTaskId` from `target/sonar/report-task.txt`
(`build/sonar/report-task.txt` for gradle) and poll `/api/ce/task?id=<ceTaskId>` until
`SUCCESS`. Reading measures before that returns the **previous** analysis, silently.
`FAILED` or `CANCELED` → stop with the task's `errorMessage`.

### 3 · Extract

In this order, all read-only:

1. **Quality gate** — status and every condition, with its threshold and actual value.
2. **Measures** — the list in the reference: bugs, vulnerabilities, code smells, hotspots,
   coverage, duplication, ratings, `ncloc`, and the `new_*` metrics the gate reads.
3. **Issues by rule** — one call with `ps=1` and facets on rules, software qualities,
   severities and scopes: the counts, without paging through every issue. Then, for each
   rule, one call with a small `ps` for sample locations, split `MAIN` / `TEST`.
4. **Rule text** — `/api/rules/show` for each rule key: its name and why it matters.
5. **Duplication** — files with duplicated blocks, then the blocks of each.
6. **Coverage** — the files with the most uncovered lines.

Large answers are the only real cost of this skill: always request the facet first and
page only what step 4 needs.

### 4 · Trace each finding group to its owner

Group by Sonar rule (a duplicated block is its own group). For each group, find the piece
of **this project's `.claude/`** that produced it, in this order, and stop at the first hit:

| Origin | How to find it |
|---|---|
| **Template copied verbatim** | `Grep` the flagged construct in `.claude/skills/*/templates/*.example`. A hit means every project gets the issue |
| **Norm that allows or requires it** | `.claude/rules/00-index.md` → the norm for that layer; a norm that prescribes the flagged shape, or explicitly permits it |
| **Checkstyle / build configuration** | `config/checkstyle/*.xml` and the root build file — a check that is missing, or disabled, where Sonar has the equivalent rule |
| **Test template teaches the pattern** | Same as the first row, restricted to `test-architect` and `new-feature` test templates |
| **Code the bootstrap generated** | No template in the project — `project-bootstrap` does not travel. Name it `project-bootstrap` plus the role of the file (entry point, exception handler, config class) |
| **Nothing — the model decided alone** | No norm and no template covers the construct. The fix is a norm, or a line in the one that owns that layer |

Then decide the **fix at the owner**: which file in `.claude/`, what change, and whether it
also needs enforcement (a Checkstyle check, an ArchUnit rule) so the issue cannot come back.
Say it concretely — a file path, a line, the shape of the change — never "improve the
template".

Check whether an owner file was edited locally since the export:
`java .claude/hooks/ArchHook.java doctor` names the edited `.claude/` files. When the file at
fault is one of them, the lesson says so: the meta-repository's version may not have the defect.

### 5 · Write `docs/lessons-learned/sonar-NNN.md`

`NNN` is the highest existing `sonar-*.md` plus one, `001` when the directory is empty.
Fill `templates/lessons-learned.md.example`: snapshot, issues by origin, one section per
group, and the structural lesson — what in `.claude/` would have caught the whole class of
issue before the analysis did. Complete here: project paths, lines, excerpts all belong in
this file.

**Progress against the previous run.** When `sonar-<NNN-1>.md` exists, read its snapshot
and fill the snapshot's *Previous* and *Δ* columns, and mark each finding group *new*,
*recurring* (same rule key in the previous file) or — in a closing list — *gone*. The goal
is fewer issues each round; this is the only place that says whether it is happening. A
recurring group whose previous file already named the fix at the owner says so: the fix was
proposed and has not reached this project (not merged upstream, or not pulled with
`/arch-adopt`).

Report the path and the snapshot line, then go on to step 6.

### 6 · Hand it to `/report-issue` — print the command, invoke nothing

Write `not filed yet — /report-issue docs/lessons-learned/sonar-NNN.md` in the `## Issue`
line at the end of `sonar-NNN.md`, and end the report with that command. `/report-issue` is
manual-only: it picks the `sonar-lessons` form, strips the project from the body, searches
duplicates, asks, and overwrites the `## Issue` line with the outcome. The user types it, or
the lesson stays local — the line says which, for a later reader and for the next run's
step 5.

## Failure modes

**No scanner in the build file:**
```
❌ pom.xml declares no sonar-maven-plugin. Run /sonarqube-setup, then /sonar-lessons.
Nothing written.
```

**Server down:**
```
❌ http://localhost:9000 refused the connection.
Run `docker compose up -d sonarqube`, wait for /api/system/status to answer UP, re-run.
```

**Token missing, invalid, or unable to read:**
```
❌ SONAR_TOKEN is not set — export a user token (My Account → Security) and re-run.
❌ <call> answered 403 — SONAR_TOKEN can analyze but not browse this project.
   A project analysis token cannot read the Web API; use a user token with Browse.
```

**Build red:**
```
❌ verify failed in <module> — <first error line>. No analysis ran; nothing written.
```

**Compute engine task failed:**
```
❌ Analysis task <id> ended FAILED: <errorMessage>. The previous analysis is still on the
server; nothing was read from it.
```

## Report

```
✅ Sonar lessons — <quality gate status> · <N> issues (<main> main / <test> test) · coverage <x> % · duplication <y> %

Lessons ..... docs/lessons-learned/sonar-NNN.md — <G> groups: <t> template, <r> norm, <c> checkstyle, <b> bootstrap, <m> model alone
Top owners .. <.claude path> (<n> issues) · <.claude path> (<n>) · …
Dashboard ... <host>/dashboard?id=<projectKey>
File it ..... /report-issue docs/lessons-learned/sonar-NNN.md
```

## Contract

**Class:** report — the territory is `skill_classes.report` in
`@.claude/schemas/extensions.json`: `docs/lessons-learned/**`, nothing else. `ArchHook.java
guard` enforces it; `target/` and `build/`, which the analysis writes, are ignored by git
and outside what `guard sweep` sees.

**Reads** the root build file, `target/sonar/report-task.txt` (or `build/sonar/`),
`.claude/rules/**`, `.claude/skills/*/templates/**`, `config/checkstyle/**`,
`.claude/.arch-provenance.json` (the version line of the file), and the SonarQube Web API.

**Writes** `docs/lessons-learned/sonar-NNN.md`.

**Publishes** nothing. The issue is `/report-issue`'s, typed by the user with the path step 6
prints; the body file `sonar-NNN.issue.md` is written there.

**Never writes** the build file, `docker-compose.yml`, a token, or anything under `src/`. A
finding is fixed at its owner in the meta-repository, or by `/new-feature` in this
project — not by this skill.

**Not chained** by any skill. Travels into the generated project
(`export.skills.include`); in the Nerviz repository itself it stops at
step 1, which has no build file.
