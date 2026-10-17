---
name: init-project
description: >
  Initializes a Spring Boot project from scratch with a selectable architecture. Manual
  ritual — interview, validate the blueprint, generate the structure, install the hooks
  and verify the build. Explicit invocation only.
argument-hint: "[--blueprint <id>] [--build maven|gradle] [--groupId <groupId>] [--name <artifactId>] [--bounded-context <name>]"
disable-model-invocation: true
allowed-tools: Agent, Read, Write, Glob, AskUserQuestion, Bash(find:*), Bash(sort:*), Bash(ls:*), Bash(head:*), Bash(java .claude/hooks/ArchHook.java audit genesis:*)
model: sonnet
effort: low
---

## Available blueprints

!`find "${CLAUDE_PROJECT_DIR:-.}/.claude/blueprints" -mindepth 2 -maxdepth 2 -name '*.yaml' 2>/dev/null | sort`

## Next to this repository

!`ls -a "${CLAUDE_PROJECT_DIR:-.}/.." | head -30`

## Session

${CLAUDE_SESSION_ID}

## Arguments

$ARGUMENTS

---

## Procedure

1. The project is generated next to this repository, at `../<artifactId>`
   (`project-bootstrap` § Where the project is born). If `--name` is given and the listing above
   shows that name, check it with `ls -a` on that directory. If it holds `pom.xml` or
   `build.gradle`, **do not initialize**: report what you found and suggest `/new-feature` from
   a session opened in that directory. Stop here.
2. **Interview — every question of the run, here, before delegating.** The agent runs in the
   background, where `AskUserQuestion` does not exist; a question it needs mid-run is a hand-back,
   a resume over its whole context, and a user who cannot leave the terminal
   (`@.claude/lessons-learned/lessons-learned-020.md` § 6). Read every blueprint listed above in
   one response, in parallel.

   The questions, in this order — skip any the arguments already answer:

   1. *Architecture* — every blueprint by `id`, each with its `when_to_choose` and a `trade_off`
      from the YAML itself, written in the question text; up to four of them as options, the
      rest typed by `id` under Other. Never a list written by hand.
   2. *Build* — Maven or Gradle.
   3. *Features* — multi-select, and **only** over the features the chosen blueprint sets
      `false`, among REST, JPA + Flyway, Kafka, SQS, OpenAPI, Testcontainers, Actuator. Every
      feature it sets `true` is already confirmed and never asked. None `false` → no question.
      An active feature is a dependency and its configuration, never business code
      (`@.claude/decisions/0011-bootstrap-without-business-code.md`); ArchUnit and coverage are
      not asked, `test-architect` installs them later.
   4. *artifactId*.
   5. *groupId*.
   6. *Project name* — default: the artifactId.
   7. *Bounded context* — default: the artifactId; the first segment of every topic name, and
      nothing else in the project declares it.
   8. *Transport topology* — the first question of `transport-security-setup` § 2, read from
      that file, with its options.
   9. *SonarQube* — the two questions of `sonarqube-setup` § 2, read from that file, with their
      options. Those skills own their questions; this step asks them earlier and never rewrites
      them.
   10. *Follow-ups*, only when an answer needs one — the second question set of
       `transport-security-setup` § 2 for the chosen topology; a server URL or SonarCloud
       organization when the Sonar answer named an existing server.

   Send them in that order, **at most four questions per `AskUserQuestion` call and two to four
   options per question** — the tool rejects the whole call otherwise
   (`@docs/pt-br/11-pitfalls.md` § `AskUserQuestion`). A question whose options or default
   depend on an answer not yet given — *Features* on the blueprint, a default on the artifactId,
   a follow-up on its parent — goes to the next call. A free-text field offers its default and
   one variant derived from an answer already given; the value itself is typed under Other.

   A free-text answer that comes back incomplete — `groupId` without `artifactId` — is asked
   again, alone, before delegating.
3. Delegate to the `project-initializer` agent, passing the arguments and **every** answer of
   step 2, by name: blueprint, coordinates, project name, bounded context, build tool, features
   (every one the blueprint sets `true`, plus the ones checked), transport topology and its
   follow-up, Sonar server and authentication. The agent asks
   nothing; a missing answer makes it stop with `blocked: missing <field>`, and then the field
   is asked here and the agent is resumed once. The agent exists for two of the three legitimate
   reasons: generation produces verbose output that shouldn't fill this conversation, and it
   runs with a restricted set of tools.
4. Return the agent's report without rewriting it — the format is fixed in the
   § Output contract of `.claude/skills/project-bootstrap/SKILL.md`.
5. **Fill the genesis record**, once the report says the project was created:

   ```bash
   java .claude/hooks/ArchHook.java audit genesis "<absolute path of the generated project>" <session id above>
   ```

   It replaces Started, Finished and tokens in the project's
   `.claude/audit-usage/GENESIS.md` from this session's transcripts — this conversation since the
   `/init-project` message, typed or reached through the Skill tool, and every agent run. Show
   its three lines. A non-zero exit says why; report that line, and never write the values
   yourself. Before step 6, so the first commit carries the filled record.
6. Chain `git-publish` once the report says the project was created, and only then, with
   `project: <absolute path of the generated project>` in its context. This skill is its only
   caller after a generation: the agent no longer chains it.
7. End by telling the user to open a new session in the generated project
   (`cd ../<artifactId> && claude`). That session loads the project's own `settings.json` and
   hooks; this one keeps this repository's.

## Why this is a manually-invoked skill

Form 2: creating a project is a ritual a person starts (axis 2 — `/init-project`), and the
interview it leads to cannot be triggered by inference from a sentence. Form 1 was rejected
for exactly that: a skill that can scaffold a whole tree on the model's own judgment is a
directory rewritten by accident. Form 3 was rejected here and used one level down instead —
the isolation belongs to the generation, which is why `project-initializer` exists, and the
interview belongs here, in the main session, the only place `AskUserQuestion` is guaranteed
(`@.claude/decisions/0123-lessons-learned-020-init-project-run.md`).

Runs on `sonnet` with `effort: low`: the interview reads its questions from the blueprints and from the two chained skills, and the generation is delegated to `project-initializer`, which declares its own model (`@.claude/decisions/0081-skill-model-required-per-class.md`).

## Contract

**Class:** orchestrator — the territory is `skill_classes.orchestrator`'s override for this
skill in `@.claude/schemas/extensions.json`, and it is **empty**: this skill writes no file
itself. Everything is written by `project-initializer`, which the guard bypasses as an
executor agent, and by `project-bootstrap` under it. `ArchHook.java guard` enforces it. The one
write it causes is `audit genesis` replacing four placeholders in the generated project's
`GENESIS.md`, outside this repository — done by the hook's code, never by a `Write`.

**Reads** the blueprint listing and the listing of this repository's parent directory injected
above, every blueprint YAML for the interview, the § 2 questions of `transport-security-setup`
and `sonarqube-setup`, and the arguments.

**Owns** the interview of a project's first generation. The questions about transport and Sonar
stay owned by their skills; this one only asks them before the agent starts.

**Delegates** to `project-initializer` — never generates a file inline, not even a single
`pom.xml`. A partial generation from this thread is the failure mode the agent exists to
prevent: the report would describe a tree nobody wrote in full.
