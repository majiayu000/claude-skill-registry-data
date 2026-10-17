---
name: ai-architect
description: >
  Designs the outbound AI ports of an already-scoped use case — a language model asked for a
  structured answer (classify, extract, moderate) or an embedding model and a vector store asked
  for the nearest items (semantic search, duplicate detection) — into the `29-ai.md` partial: the
  prompt resources, the answer type with closed fields and what an unusable answer becomes, which
  fields go to the provider, the store and who re-indexes it, timeout and the one retrying layer,
  failure families, metrics, configuration and test cases, with Spring AI only in the adapter. Use
  when the request involves Spring AI, ChatClient, an LLM, OpenAI or Anthropic from Java, a prompt,
  structured output, embeddings, pgvector or a vector store. Piece of the `/new-feature` pipeline:
  requires `00-use-case.md` and a `10-domain.md` declaring a port of kind `LLM` or
  `vector store` in the given folder — and stops without them.
argument-hint: "[path of the UC-NNN-<slug> folder]"
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash(find:*), Bash(ls:*), Bash(grep:*), Bash(sort:*), Bash(awk:*), Bash(curl:*)
model: opus
---

## Available specs

!`find "${CLAUDE_PROJECT_DIR:-.}/docs/use-cases" -mindepth 1 -maxdepth 1 -type d -name 'UC-*' 2>/dev/null | sort`

Empty above → none yet, run `/use-case-design` first. (`find`, not an `ls` glob: under zsh an unmatched glob
aborts the command before any fallback runs.)

## Target

$ARGUMENTS

---

# AI Architect

Designs **what a model is asked, with which data, and what its answer is allowed to change**: the
prompt as a versioned resource, the answer as a type whose closed fields the model cannot escape,
the "could not decide" value every unusable answer becomes, the fields that cross to the provider
and the ones that never do, the store a semantic search reads and who keeps it current, and how a
slow, refusing or absent provider reaches the caller. The domain already said what the port means
and which state waits for a person — that is `10-domain.md`. This skill makes the model's side of
that port honest.

**Entry rule: no AI port, no AI design.** This skill reads
`docs/use-cases/UC-NNN-<slug>/10-domain.md` and runs only when § Ports declares an output port of
kind `LLM` or `vector store`. None → stop and say so. `00-use-case.md` is required too: the
trigger and its deadline bound every timeout here.

**Scope rule: structured answers and semantic search, nothing else.** A case whose port needs the
model to call back into the application (tools), a conversation kept across calls (chat memory), an
answer generated over retrieved passages, images, audio or transcription is outside this skill
(`@.claude/rules/ai.md`, the scope paragraph above § Boundary). Stop, name which of them the case needs, and record it — the user
decides between narrowing the case with `use-case-design` and deferring it. Never design it here
half-way.

**Exit rule: it doesn't write code.** It emits `29-ai.md`. The Java classes, prompts and properties
come from the executor agent, which reads the partial and the `templates/` exemplars.

**Rule rule: the rules don't live here.** Boundary, wiring, prompts, output, data sent, semantic
search, failure, observability and tests are `@.claude/rules/ai.md`, which cites
`@.claude/rules/http-client.md` and `@.claude/rules/error-handling.md` for the provider as a remote
system. This skill applies and cites them; it doesn't reproduce them.

## How it's invoked

Two paths: `/ai-architect` by hand, or chained by `/new-feature` after outbound HTTP and before
messaging. That's why it does **not** carry `disable-model-invocation` — a skill the model can't see
is a skill the orchestrator can't call (`@.claude/decisions/0007-pipeline-skills-invocation.md`). The
guard against firing out of order is the entry rule above.

## Why this is a skill and not a subagent

Form 1, motivated by axis 1 of the designer's interview: no piece owned an outbound call to a model,
and the maintainer chose to design it ahead of a run that shows the defect, on the pitfalls the
official documentation and the library's source record (`references/pitfalls.md`) — two of them
reproduced only by running the exemplars. The closest rejected form was a variant of
`http-client-architect`: its interview reaches the engine and the credentials, not the prompt, the
answer type, the data sent or the store. A subagent fails the counter-test on all three points: the
interview is the task, the reference fits in `references/` and `templates/`, and the partial is
short.

Pinned to `opus`: the partial is what the executor implements verbatim, and the pin holding for the
rest of the turn keeps `/new-feature` on the model that designed it
(`@.claude/decisions/0081-skill-model-required-per-class.md`). Design record:
`@.claude/decisions/0145-ai-architect-skill.md` (this repository only).

## Boundary with neighboring skills

| Piece | Decides | Never decides |
|---|---|---|
| `use-case-design` | What the case does with a classification or a search result, the trigger and its deadline | The model, the prompt |
| `domain-modeling` | The port, its kind, its domain types, the "could not decide" value and the review state it leads to | Anything about the model or the store |
| `http-client-architect` | The integration families' classes, when the project has them first | The AI port's timeout, retry or translation |
| `messaging-architect` / `jobs-architect` | The trigger that re-indexes a store on a record's change, an ingestion or backfill job | The store, the embedding |
| `persistence-architect` | The store's migration — its final name, number and placement | The table's shape the library reads (`29-ai.md` § 9 hands it over) |
| **this skill** | Provider and model per port, prompt resources and variables, answer type, data sent, store and embedding model, timeout and retrying layer per port, failure translation, metrics, AI dependencies and configuration, the `postgres` image row for a store | The port, the review state, the trigger, the tests' code |
| `test-architect` | Which test proves each case of § 8, at what level | — |
| `docker-architect` | The compose block of the database image § Compose services names | — |

## Procedure

1. **Read the specs.** `00-use-case.md` (trigger, Components table), `10-domain.md` (§ Ports
   with their kinds, the domain types, the review state), and — when present — `30-rest.md` (the
   request deadline), `25-messaging.md` and `35-jobs.md` (whether the trigger already retries),
   `32-security.md` (who is asking). Apply the entry rule and the scope rule. List the AI ports,
   each as a port method with its kind.

   **A port of kind `LLM` with no "could not decide" value in its return type, or no review state
   it leads to, is a divergence**, not something to invent here: `10-domain.md` is
   `domain-modeling`'s to change, and the port stays undesigned until it does — an adapter with
   nowhere to put an unusable answer throws it, or worse, guesses.

2. **Survey — every answer the project already gave is inherited, never re-asked.**

   ```bash
   # Boot line — Spring AI 2.x needs Boot 4
   grep -m1 -A1 "<artifactId>spring-boot-starter-parent" pom.xml
   # Spring AI already in the build, and which provider
   grep -nE "spring-ai-bom|spring-ai-starter-(model|vector-store)-" pom.xml
   # AI code already in the project, outside the AI package or inside it
   grep -rlnE "import (org\.springframework\.ai|com\.openai|com\.anthropic)\." --include='*.java' src/main 2>/dev/null
   # Decisions earlier use cases recorded
   find docs/use-cases -name '29-ai.md' 2>/dev/null
   ```

   And the active blueprint's `packages.map` entry ending in `.ai` — the package every AI adapter,
   the wiring and the translation go to. No such entry → stop and say which line is missing from
   the blueprint, instead of choosing a package inside this use case.

   **A Boot 3 project stops here.** Spring AI 2.x runs on Boot 4 only, and the templates are 2.x —
   1.x differs in exactly the APIs they use (`references/pitfalls.md` § Version line). Say so; the
   user upgrades Boot first or designs the port by hand.

   **AI code outside the AI package is not reuse.** Record it in `## Impact on approved use cases`
   and decide with the user between moving it behind the port in this run and deferring that with an
   owner — never a second client for the same provider.

   | Fact | Inherited from | Asked only when |
   |---|---|---|
   | Provider | A starter in `pom.xml`, or an earlier `29-ai.md` § 2 | Neither exists — first AI port of the project |
   | Store and embedding model | An earlier `29-ai.md` § 5 | First store of the project |
   | Project-wide pieces (`AiProperties`, `AiClientConfig`, `AiFailureTranslator`) | Already in the AI package | First AI port |
   | Integration families | The domain exception package (`28-http-client.md` may have created them) | Never asked — created NEW when absent |

3. **Interview — only what steps 1 and 2 did not settle.** `AskUserQuestion`, at most 4 questions
   per call and **never fewer than 2 real options** per question; an axis with one sensible answer
   is decided and recorded, not asked (`@CLAUDE.md` § Known pitfalls). Every option states its cost.

   | Axis | Decides | Skip when |
   |---|---|---|
   | **Provider** — which one the company has a contract and a data-processing agreement with | § 2 | Inherited |
   | **Model per port** — reasoning or not, and the budget per answer | § 2 — and whether temperature is set | An earlier port of the same purpose fixed it |
   | **Each field the prompt could carry** — full, reduced, or not at all; who receives it | § 4, per `@.claude/rules/personal-data.md` § In transit | Never skipped while a prompt carries a record's field |
   | **The threshold of each search** — how it will be measured (a labelled sample of queries) | § 3 | The port is not a search |
   | **Who writes the records a store mirrors** — use cases, jobs, consumers, another service | § 5, one row per writer | The Components tables of every approved case already answer it — list them, then ask only "anything else?" |

4. **Design each port — § 1 and § 3.** For a port of kind `LLM`: the prompt resources
   (`prompts/<port>-system.st`, `prompts/<port>-user.st`), the named variables and the markers that
   delimit input, the answer type declared in the adapter with every closed field an enum, the value
   meaning "none fits", and every unusable answer mapped to the "could not decide" value — the form is
   `templates/StructuredOutputAdapter.java.example`. For a port of kind `vector store`: the text that
   is embedded, the threshold and its basis, the result ceiling, and the identifiers returned — the
   form is `templates/SemanticSearchAdapter.java.example`, which never returns a record.

5. **Decide the data sent — § 4.** One row per field the record behind the prompt holds, sent or
   not, with the reason. A field that crosses in clear names its receiver and the agreement it
   crosses under — the recorded decision `personal-data.md` requires. Free text a person typed is a
   field too: if it may hold personal data, say so and say what was decided.

6. **Design the store — § 5, vector store only.** pgvector in the project's PostgreSQL is the only
   store this skill's templates carry; a project on another database engine records the store as
   deferred with its reason. Fix the embedding model and its dimension count (≤ 2000 for the HNSW
   index), the distance, the item id (the source record's id, so a write replaces), and **one row per
   writer** of the mirrored records — its path to `ProductEmbeddings`-style `index`/`remove`. A
   writer that cannot call it (another service, a bulk statement) goes to § 9 as a requirement on
   `25-messaging.md` or `35-jobs.md`; a first fill of an existing table is an ingestion job, also § 9.

7. **Failure and retry — § 6.** Per port: the timeout, per attempt, from a measured number and under
   the trigger's deadline; the retrying layer — the provider SDK's `max-retries`, set to `0` when the
   trigger already retries (`@.claude/rules/http-client.md` § Retry); the attempts that follow. Then
   the failure table — the three integration families of `@.claude/rules/error-handling.md`, and what
   each becomes for our caller, read from `00-use-case.md`'s alternative flows. The project-wide
   pieces, NEW or REUSE.

8. **Observability and tests — § 7 and § 8.** The library's metrics and the alarm each exists for,
   plus the review-share counter per port. § 8 lists every case `@.claude/rules/ai.md` § Tests names,
   by level: contract (stub `ChatModel`), provider IT (WireMock), store IT (real pgvector, stub
   `EmbeddingModel`). No case calls a real model.

9. **Requirements to other partials — § 9.** The store's migration to `20-persistence.md` (shape:
   `templates/vector-store-migration.sql.example`); a re-index trigger or an ingestion job to
   `25-messaging.md` or `35-jobs.md`; a missing review state to `10-domain.md`. Each a row, never an
   edit of another partial.

10. **Declare dependencies and configuration — § 10 and § 11.** `spring-ai-bom` imported, with the
    version the Initializr resolves for the project's Boot today, and the starters, version empty —
    managed by the BOM:

    ```bash
    curl -s "https://start.spring.io/dependencies?bootVersion=<boot from step 2>" \
      -H 'Accept: application/vnd.initializr.v2.2+json' | grep -o '"spring-ai":{[^}]*}'
    ```

    Never a version from memory (`@CLAUDE.md` invariant 8); no network → ask. The executor may write
    `pom.xml` for exactly these rows. § 11 lists every property, its value and its owner — shape
    `templates/application-ai.yml.example`; the key is `${…}` with no default
    (`@.claude/rules/secrets.md`).

10b. **Decide the design patterns of this layer.** Run
    `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use over the adapters this case adds.
    The answer goes into `## Design patterns` — `none` is not valid when an adapter is written.

11. **Check the database image — vector store only.** List the keys inside the `services:` block
    and the `postgres` image:

    ```bash
    awk '/^services:[[:space:]]*$/{s=1;next} /^[^[:space:]#]/{s=0} s&&/^  [A-Za-z0-9_.-]+:[[:space:]]*(#.*)?$/{sub(/[[:space:]]*#.*$/,"");print}' docker-compose.yml
    grep -nE "^\s+image:\s*(postgres|pgvector/pgvector)" docker-compose.yml
    ```

    Write the answer as a row of `## Compose services`, shaped and decided by
    `@.claude/skills/docker-architect/references/compose-service-decision.md`: `exists` when the
    `postgres` image is already `pgvector/pgvector`; when `postgres` exists on a plain image, the row
    names the image change and the decision that reference owns — never a second database service; no
    `postgres` at all, the question as usual. A chat model alone → `none`. Do **not** invoke
    `docker-architect` and do not edit `docker-compose.yml`.

12. **Write the partial.** `docs/use-cases/UC-NNN-<slug>/29-ai.md`, from
    `templates/ai-spec.md.example`. Twelve numbered blocks plus `## Compose services` and
    `## Design patterns`, all mandatory, each written as `none` when there is nothing — absence is not
    `none`. § 12 `Deferred` follows the same shape as every other partial's.

13. **Report and stop.** Path of the file written; each port with its model and timeout next to the
    trigger's deadline; every field of § 4 sent in clear, with its receiver; for a store, every writer
    of § 5 and how it re-indexes; the `## Compose services` row; each § 9 requirement. A port with no
    "could not decide" value, a writer nobody could name, or a timeout above the deadline is a finding.
    Don't invoke anyone else: the next pipeline step reads § 9.

## What the partial contains

| Block | Fixes |
|---|---|
| 1 · AI ports | One row per port: kind, what it asks, what it returns, the "could not decide" value, the review state |
| 2 · Provider and models | Provider, model and options per port, and whether inherited |
| 3 · Prompts and output | Per `LLM` port: resources, variables, answer type, closed fields, every unusable answer. Per search: threshold and its basis, result ceiling |
| 4 · Data sent | Per field: sent or not, in which form, why; the receiver and its agreement |
| 5 · Vector store | Store, embedding model, dimensions, distance, item id, every writer and its re-index path — `none` without a store |
| 6 · Failure and retry | Per port: timeout, retrying layer, attempts; the failure table; project-wide pieces NEW or REUSE |
| 7 · Observability | Metric names and the alarm each exists for; content logging off |
| 8 · Test cases | Every case, by level |
| 9 · Requirements to other partials | Migration, re-index trigger, ingestion job, review state |
| 10 · Declared dependencies | BOM and starters |
| 11 · Configuration | Every property, its value, its owner |
| 12 · Deferred | Same shape as every partial. `none` when nothing was deferred |
| Compose services | The `postgres` image row for a store, or `none` |
| Design patterns | The adapter over each port, with its classes — step 10b |

Plus `## Impact on approved use cases` and `## Implementation order`, as in every partial.

The exemplars in `templates/` are **reference for form**, not files to copy. Each was compiled and
run against the classpath the Initializr resolved on the day it was written:

| Exemplar | Shape of |
|---|---|
| `templates/StructuredOutputAdapter.java.example` | A port of kind `LLM`: domain types, answer type, adapter, every unusable answer to "could not decide" |
| `templates/SemanticSearchAdapter.java.example` | A port of kind `vector store`: search returning ids, the write side that re-indexes and removes |
| `templates/AiClientConfig.java.example` | `AiProperties`, one `ChatClient` per port from the auto-configured builder, per-port options with the timeout, `AiFailureTranslator` |
| `templates/application-ai.yml.example` | Key placeholder, base URL, the SDK's retries, content logging off, the store's settings, `app.ai.*` per port |
| `templates/ticket-classifier-system.st.example`, `ticket-classifier-user.st.example` | A system prompt naming the input as data, a user prompt holding only the delimited variable |
| `templates/vector-store-migration.sql.example` | The store's schema as a migration — handed to `20-persistence.md` |
| `templates/ai-spec.md.example` | The partial |

## Contract

**Class:** design — the territory is `skill_classes.design` in
`@.claude/schemas/extensions.json`, and `ArchHook.java guard` enforces it. Writes inside the use
case folder and nothing else.

**Reads** `docs/use-cases/UC-NNN-<slug>/00-use-case.md` (mandatory), `10-domain.md`
(mandatory), `30-rest.md`, `25-messaging.md`, `35-jobs.md`, `32-security.md` (when present), the
Components tables and `29-ai.md` of earlier cases, `pom.xml`, `docker-compose.yml`, the active
blueprint's `packages.map`, the Initializr's metadata, `@.claude/rules/ai.md`,
`@.claude/rules/http-client.md`, `@.claude/rules/error-handling.md`,
`@.claude/rules/personal-data.md`, `@.claude/rules/secrets.md`, `@.claude/rules/observability.md`,
`@.claude/rules/architecture-ddd.md`,
`@.claude/skills/docker-architect/references/compose-service-decision.md`, and this skill's
`references/`.

**Writes** `docs/use-cases/UC-NNN-<slug>/29-ai.md`. Nothing else.

**Owns** the provider and the model and options of each AI port, the prompt resources and their
variables, the answer type and what each unusable answer becomes, the fields sent to the provider,
the store, its embedding model and the list of writers that must re-index, the timeout and the
retrying layer of each AI port, the translation of provider failures, AI metrics, AI dependencies
and configuration, and the `postgres` image row a store needs.

**Does not decide** the port, its domain types or the review state (`10-domain.md`), the trigger
and its deadline (`00-use-case.md`, `30-rest.md`), a re-index trigger or an ingestion job
(`25-messaging.md`, `35-jobs.md`), the migration's final form (`20-persistence.md`), or the tests
(`40-tests.md`). Does not write Java, prompts, `pom.xml`, `application.yml` or
`docker-compose.yml` — the executor and `docker-architect` do, from this partial. Doesn't touch
`.claude/rules/**`.
