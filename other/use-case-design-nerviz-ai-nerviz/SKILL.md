---
name: use-case-design
description: >
  Delimits a use case's boundary and emits the parent spec that the layer skills
  detail — trigger, payload, response, side effects, invariants, errors, and canonical
  names. Use when the request involves "new use case", "design before implementing",
  "implementation spec", a new endpoint/event/job, or when a request bundles several
  actions and it's necessary to know whether it's one use case or several. First piece
  of the `/new-feature` pipeline.
argument-hint: "[technical description of the use case]"
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash(find:*), Bash(ls:*), Bash(grep:*), Bash(sort:*), Bash(tail:*)
model: opus
---

## Already-designed use cases

!`find "${CLAUDE_PROJECT_DIR:-.}/docs/use-cases" -mindepth 1 -maxdepth 1 -type d -name 'UC-*' 2>/dev/null | sort | tail -5`

Empty above → none yet, this will be `UC-001`. (`find`, not an `ls` glob: under zsh an unmatched glob
aborts the command before any fallback runs.)

## Target

$ARGUMENTS

---

# Use Case Design

Produces the use case's **parent spec**: the boundary, the flow, and the canonical
names every layer inherits. Writes no code. Weighs no storage technology: the storage family
and the search engine come from the request — stated, or inferred without ambiguity — or from one
factual question with no criteria and no recommendation; weighing them belongs to a planned
solution-design step (`@.claude/decisions/0147-document-storage-and-search-architect.md`). The
audit level is recorded only when the request asks for it, never proposed
(`@.claude/decisions/0149-auditing-variant-of-persistence-architect.md`). The
inbound protocol is the one technology asked with criteria, those of
`@.claude/rules/api-graphql.md` (`0146`).

**Entry rule: one use case, one side effect.** Before any question, apply the
boundary test from `references/scope-boundary.md`. A request with two side effects and
no shared transaction isn't one use case — it's two, and the right answer is to
propose the split, not design the hybrid.

**Vocabulary rule: technical input or nothing.** The request names the concrete
trigger (endpoint, topic, job, schedule) and the concrete destination (table, queue,
service). A request in business language — "when a user is created in the marketing
area" — doesn't get guessed at: stop and ask for a rewrite, listing the expected
vocabulary.

## How it's invoked

Two ways, and both matter: `/use-case-design` by hand, or chained by `/new-feature`
once that orchestrator exists. That's why it does **not** carry
`disable-model-invocation` — that field hides the skill from the model, and a skill the
model can't see is a skill the orchestrator can't call.

It's the first piece in the pipeline: it has no prior partial to require. The guard
against improper firing is the boundary test above — a vague request stops and asks
for a rewrite. Recorded in `@.claude/decisions/0007-pipeline-skills-invocation.md`.

## Why this isn't a subagent

It's a multi-step procedure whose heart is the interview with the user, and a
subagent doesn't see the conversation (axis 6 of the design interview). It writes
files in `docs/use-cases/**` — this repository's default for anything with a side
effect. The subagent lost by failing the counter-test's three questions; the full
record, with all four options and the notes, is in
`@.claude/decisions/0002-skill-use-case-design.md`.

Pinned to `opus`: the partial is what the executor implements verbatim. A pinned model does not make this a subagent — the interview needs the conversation, and the pin holding for the rest of the turn keeps `/new-feature` on the model that designed it (`@.claude/decisions/0081-skill-model-required-per-class.md`).

## Out of scope — and it's someone else's scope, not a lesser scope

| Doesn't decide | Why | Who decides |
|---|---|---|
| Kafka or SQS | The broker is an architecture choice, fixed earlier: the blueprint's `features` | The user, in `/init-project` |
| **Weighing** relational, document or search for a case — scenarios, trade-offs, pros and cons, a recommendation | A decision interview is a different job from recording a fact. This skill records the storage family and the search engine the request states, or asks one factual question when it does not (step 3, the `Storage` block); it never argues for one | A planned solution-design step, which will write the same `Storage` and `Search index` rows |
| Which design pattern to apply | A pattern shapes the classes of one layer, and this spec fixes no class | Each layer's partial, through `gof-design-patterns` § Design-time use |
| Writing classes, tests, or migrations | The spec describes what to create; creating is a different phase | The layer skills and, eventually, the executor agent |
| Per-layer detail (annotations, columns, exact HTTP status) | Each layer has its own rule and owner | The partial specs — see § Structure |
| **Path, verb, and HTTP status** | Fixing them here creates divergence: `api-rest.md` has URI and status rules this skill doesn't apply, and `30-rest.md` ends up correcting the parent spec's prose. Write the situation (`created`, `conflict with existing state`), not the number | `rest-api-architect`, in `30-rest.md` |
| **Idempotency mechanism** (`Idempotency-Key`, key table) | `api-rest.md` requires it on creation `POST`s; deciding "no" here was overwritten downstream and cost a second persistence pass. Record the business fact — "does repeating the request create a duplicate?" — and mark the technical decision as delegated | `rest-api-architect`, in `30-rest.md` |
| **Exception name and class** | A name fixed here gets demoted by `domain-modeling` (a subclass needs ≥ 2 call sites) and promoted back by a later case. Describe the situation (`email already in use`) and its kind (validation, not found, conflict, business rule) | `domain-modeling`, in `10-domain.md` |
| **Shape of a domain field** — value object, `enum`, or plain primitive | The criterion is `@.claude/rules/value-objects.md`, which this skill does not read: a closed set with no formation rule to validate is an `enum` by criterion 3, and calling it a value object here guarantees a divergence on every such field. Name the component and its role; leave the shape open | `domain-modeling`, in `10-domain.md` |

If the user asks for one of these, say which piece owns it and stop. Don't improvise
the decision.

## Procedure

1. **Validate the vocabulary.** Without a technical trigger and a technical
   destination in the request, stop and ask for a rewrite, with the examples from
   `references/scope-boundary.md`. Don't proceed by guessing.
2. **Count the side effects** using the boundary test. Two or more with no shared
   transaction — or a request naming several operations (create, read, update, delete)
   — is several use cases. **A split becomes backlog, not work:**

   1. Present the list in dependency order (which UC stays synchronous, which reacts to
      which event, which needs the aggregate another one creates) in **one**
      `AskUserQuestion`, asking which one to design now.
   2. Design only the chosen one.
   3. Append the others to `docs/use-cases/BACKLOG.md`, from
      `templates/backlog.md.example`: one line each, with the description ready to pass
      to the next `/new-feature`. **Don't reserve a `UC` number** — that is given when the
      case is designed, so skipping or dropping an entry leaves no gap in the sequence.
      **Do assign a `BL-NN`**, the row's own identifier: highest existing plus one, counting
      both tables of the file, never reused. It is what an impact row cites when the case
      that satisfies a precondition is still in the backlog — without it the `Satisfied by`
      column has nothing to name, and a real run invented `UC-004` twice to fill the sentence.

   **Designing a case that came from the backlog:** its row moves from the table to
   `## Retired`, with the `UC-NNN-<slug>` just assigned and the date. Not deleted — a spec that
   cited that `BL-NN` is immutable once approved, so the citation has to stay resolvable exactly
   when the case stops being backlog.

   Nothing is saved before the answer.
3. **Interview** with `AskUserQuestion`, eight blocks, one per call when earlier
   answers change the next questions:

   | Block | Fixes |
   |---|---|
   | Trigger, payload, response | Who initiates, what data comes in, what goes out and in what shape. **For an HTTP trigger, also over which protocol** — REST, GraphQL, or both over the same input port — asked with the criteria of `@.claude/rules/api-graphql.md` § Choosing the inbound protocol, REST by default; the answer ends the `Trigger` row in its closed phrase (`inbound REST adapter` · `inbound GraphQL adapter` · `inbound REST and GraphQL adapters`), and a choice already written there by an earlier design step is kept, never re-asked. The protocol is per use case, not per project |
   | Access — **always asked when the trigger is HTTP**, REST or GraphQL | Who may execute it: anyone, any authenticated caller, named roles or groups, only the owner of the resource — and whether someone (a support or admin role) may act on another's resource. The answer is the `Access` row; it is what decides whether `security-architect` runs |
   | Side effects | Writes, external calls, publications — the boundary already counted in step 2, now confirmed |
   | External calls — **always asked when a side effect reaches a system this service does not own** | Per system: what it is and what the case asks of it (read, or a write with an effect over there); its documentation link and whether it publishes an OpenAPI document; **how it authenticates this service** — as this service itself (an authorization server issues it a token), on behalf of the user who made the request, a static key, a username and password, a client certificate, a signature over each request, or none — and the credential's owner; whether it accepts an idempotency key on writes; what the business wants when it is down (fail now, or degrade to a named alternative); and, for a write, what happens when its result is unknown (stop, or reconcile later). The answers are the `External calls` row; a port of kind `external HTTP` in `10-domain.md` is what then decides whether `http-client-architect` runs. Never asked as library, timeout or retry questions |
   | Invariants and errors | Rules the domain guarantees, and the situation each violation produces — described, never named as an exception. **For a message trigger, each situation also gets its business outcome**: a failure someone must look at, or "nothing changes and the message counts as handled" — the second recorded with kind `not an error — no-op, logged and counted`, never as "discarded", since a consumer never drops a message (`@.claude/rules/messaging.md` § Retry and DLQ) |
   | Repetition, transaction, concurrency | Does repeating the request create a duplicate (business fact)? Where does the transaction open and close? What business key could collide? |
   | Storage — **asked only when the request leaves it unclear** | Per aggregate the case writes or reads as its source: `relational` or `document (MongoDB)`; and whether the case searches that data through a search engine. **Recorded, not asked, when the request states it or it is inferred without ambiguity**: the request names the family or the engine ("store orders in MongoDB", "search the catalog in Elasticsearch"); the aggregate already lives in a table or a collection (step 4 reads it); the case extends data already persisted; the request names full-text search over named fields. **Never an inference**: a loose word — "document", "flexible", "fast", "scalable", "schemaless", "JSON". Unclear → one `AskUserQuestion`, a factual question with no criteria and no recommendation: *Will this data be persisted in SQL or NoSQL?* · `SQL (relational)` · `NoSQL (document, MongoDB)`. MongoDB is the only document engine in scope, so no engine question follows — it is recorded. The relational engine (Postgres, MySQL, Oracle) is never asked here: `persistence-architect` asks it. A search engine is asked only when the request names a search but no engine: *Which search engine holds the search index?* · `Elasticsearch` · `OpenSearch`. Whether the case wants a search index at all is never asked. The answers are the `Storage` and `Search index` rows, each with who chose |
   | Audit — **recorded only when the request asks for it** | Per aggregate the case writes: `stamps` (when and by whom it was created and last changed) or `history` (every earlier version readable, with who and when). **Recorded from the request**: it asks who changed the data, when, what it was before, a trail, an audit, a history of changes. A REUSE aggregate keeps the level the code already has (step 4 reads it). **Never asked otherwise, and never proposed**: a case that says nothing about it records `none`. When the request asks for auditing without saying whether earlier values must be readable, one factual question: *Besides who changed it and when, must the earlier values be readable?* · `Who and when only` · `Who, when and the earlier values`. A document aggregate's `history` is recorded as asked — `persistence-architect` stops on it and says why. The answer is the `Audit` row, with who chose |
   | Admission — **recorded only when the request states a limit** | How many requests one caller may make in a window (a quota: "at most 100 per minute per client"), and how many may run at the same time (a cap: "at most 20 at once") — either or both, in the request's own numbers. **Recorded from the request**: it names a rate limit, a quota, a ceiling per client or per partner, a number of requests at the same time. **Never asked otherwise, never proposed, never inferred** from "public", "heavy" or "slow": a case that states no limit records `none`. When the request states a quota without the window or without who counts as one caller, one factual question for the missing half. Only for an HTTP trigger. The answer is the `Admission` row, with who chose |
   | Freshness — **always asked when the case returns data it did not just write** | How old may the answer be when it is served: must every read see the last write, or may it be some seconds or minutes old — in business words ("a balance may be up to 30 seconds old"). The answer is the `Freshness` row, `none` or a duration; a duration is what decides whether `cache-architect` runs. A case that only writes, or returns what it just wrote, records `none` without asking |

   Don't move on with a block unanswered. A missing answer becomes a silent assumption
   in the spec.

   **Checklist before every `AskUserQuestion`.** Read each question and each option:

   | Does it mention… | Then |
   |---|---|
   | an HTTP status code, a verb, or a path | don't ask — `rest-api-architect` decides |
   | idempotency, `Idempotency-Key`, a key table | don't ask — ask the business fact instead |
   | an exception class name | don't ask — `domain-modeling` decides |
   | JWT, OAuth2, an API key, a filter, `@PreAuthorize`, 401 or 403 — for who calls **this** service | don't ask — ask who may execute it; `security-architect` decides the mechanism and the enforcement |
   | discarding, ignoring or dropping a message, a DLQ, a message retry | don't ask — ask the business fact of the `Invariants and errors` block (a failure to look at, or handled with no change); `messaging-architect` maps the first to the DLQ and the second to a committed no-op |
   | a client library (`RestClient`, Feign, `WebClient`), a timeout, a retry count, a circuit breaker | don't ask — ask what the business tolerates when the other system is down or slow; `http-client-architect` decides. **Exception: how the other system authenticates this service is asked here, always** — it is a fact of the integration contract, and the credential's owner is a person to find before the design, not after |
   | the shape of a domain field (value object, `enum`, primitive) | don't ask — ask what values the field admits; `domain-modeling` decides the shape |
   | a cache, Redis, Caffeine, an expiry or TTL, a hit ratio | don't ask — ask how old the answer may be when served; `cache-architect` decides whether a cache exists and its shape |
   | criteria, pros and cons, or a recommendation between SQL, a document store and a search engine — "which fits better", "faster", "more flexible" | don't ask — record what the request states, or ask the bare factual question of the `Storage` block; weighing them belongs to a solution-design step, not to this skill |
   | tables, collections, indexes, a mapping, the relational engine | don't ask — `persistence-architect` and `search-architect` decide |
   | auditing, a history or "who changed it" the request never mentioned; Envers, `_aud` tables, a revision, retention of the history | don't ask — `Audit` is recorded only from the request; the mechanism and the retention are `persistence-architect`'s |
   | a rate limit, a quota, a concurrency limit, 429 or 503 the request never mentioned; Resilience4j, Bucket4j, a bulkhead, a gateway, replicas | don't ask — `Admission` is recorded only from the request; where it is enforced and how are `rest-api-architect`'s and `graphql-api-architect`'s |
   | fewer than 2 real options | don't ask — decide and record it in the spec. The runtime rejects the whole batch over a single one-option question (`@CLAUDE.md` § Known pitfalls) |

   A question whose answer another skill overwrites is worse than no question: it costs
   the user's time and produces a divergence.

   **Negative example** — never ask this:

   > What does the endpoint return after creating? · `201 with body` · `201 without body` · `200 with id`

   The user answered "201 without body"; `rest-api-architect` overwrote it by rule.
   Ask this instead:

   > After creating, does the caller need the created data back, or only a reference to it?
4. **Read the code before proposing.** `Glob`/`Grep` to know what already exists:
   aggregate, ports, repository, controller. Every spec component carries a **NEW**,
   **CHANGE**, or **REUSE** state. Proposing to create what already exists is this
   skill's most expensive failure mode.

   Read the approved specs too — every `UC-NNN-spec.md` whose `status:` is `approved`,
   `implemented` or `implemented-blocked`. They are a **read-only contract**: reuse the
   aggregate they already modeled, and never edit their files. A change this case needs in an approved case
   goes into this spec's `## Impact on approved use cases` section — which case, what
   changes, why. Decide what this case needs; don't defer or anticipate a decision for a
   future case.

   **An impact row that adds a precondition names which use case satisfies it.** This is the
   one row shape that can break a case that was working: "reject when `status != ACTIVE`" is
   correct, applies cleanly, compiles, passes — and leaves the earlier case reachable only
   through a state nothing in the system produces. That happened: a use case became 422 on
   every real call, the build stayed green, and the only trace was a comment in a test
   fixture. So each such row carries a fourth column, **Satisfied by**, with one of:

   - **an approved, implemented or implemented-blocked `UC-NNN`** — name it, and the
     precondition is reachable today;
   - **this very case** — it both adds the precondition and provides the transition;
   - **a backlog row, by its `BL-NN`** — `docs/use-cases/BACKLOG.md` gives every row an
     identifier for exactly this, and a `UC` number is **not** one of the answers here: a
     backlog case has no `UC` number until it is designed, and writing one invents it. Name the
     `BL-NN`, then this spec's `## Out of scope` repeats it and the consequence is stated
     outright: from this change until that case ships, the earlier use case is unreachable end
     to end. A reviewer may accept that; nobody can accept it without being told.

   No fourth answer. "The tests construct the state" is not a satisfier — a fixture that
   fabricates a state no production path can reach is the signature of this defect, not the
   solution to it.
5. **Derive the real paths** from the active blueprint's `packages.map` — the same YAML in
   a generated project, which carries its own copy. Never write a generic path when the
   real one is knowable.
6. **Fix the canonical names** per `@.claude/rules/naming.md`: the use case and its
   ports in the active blueprint's vocabulary (§ Architecture vocabulary — in this
   repository, the naming comment in the blueprint's YAML), aggregate as a noun. Never
   `<Verb><Noun>Service` by default: in a clean-architecture blueprint the use case is a
   concrete `<Verb><Noun>UseCase` with no interface. No exception names — see § Out of
   scope. These names are the inherited contract — the partial specs detail them, never
   reinvent them.
7. **Fix the number and the slug.** This skill is their only owner — no caller passes
   them in. `NNN` is the highest existing `UC-NNN` plus one, read from the injection at
   the top (`UC-001` when there's none); the slug is kebab-case, from the trigger's verb
   and noun.
8. **Generate** from `templates/use-case-spec.md.example` into
   `docs/use-cases/UC-NNN-<slug>/00-use-case.md`. Create the folder; don't create the
   empty partials.

   **The template is the only source of the file's shape.** An existing
   `00-use-case.md` is read in step 4 as a contract — aggregate, names — never as a
   format exemplar: a spec written by an older version keeps lines the template has since
   dropped, and copying one revives them.

   The two diagrams are drawn last, from the text already written, per
   `@.claude/rules/spec-diagrams.md`: the `sequenceDiagram` under `## Flow` from the numbered
   list, and the `flowchart TD` under the **Out** table from the checks of the flow and the
   table's situations. A name or an outcome a diagram needs and the text lacks goes into the
   text first. Syntax and the renderer's traps: `references/mermaid-use-case-diagrams.md`; a
   trigger, port or outcome the base template does not show (an event, a schedule, an
   `external HTTP` port and its failures): `templates/use-case-diagram-variants.md.example`.
9. **Report and stop.** File path, the boundary applied, the backlog entries the split
   produced (if any), and the table of who details each partial. **Don't invoke any
   skill** — see § Handoff.

## Spec structure

One folder per use case. One file per owner — nobody edits another's file.

```
docs/use-cases/UC-001-create-user/
├── 00-use-case.md        ← this skill. Boundary, flow, canonical names
├── 10-domain.md          ← domain-modeling
├── 20-persistence.md     ← persistence-architect
├── 30-rest.md            ← rest-api-architect
├── 40-tests.md           ← test-architect
└── UC-001-spec.md        ← /new-feature: consolidated spec, carries `status:`
```

`docs/use-cases/BACKLOG.md` sits beside the folders: the use cases a split left for later.

While the partials don't exist yet, `00-use-case.md` stands on its own: the
component table already names every file to create and who details it. It's an
incomplete spec, not an invalid one. Which partials exist is read from the folder, never
written into this file: a status line here goes stale the moment the next partial lands.

## Handoff — declarative, never executable

This skill ends at the file. It doesn't call `rest-api-architect`, `gof-design-patterns`, or
`test-architect`, for two reasons: each one exclusively owns its own paths, and
merging design with execution makes "writes no code" impossible to verify.

The link lives in three passive places: the `Detailed by` column of the component
table, this section, and the final report — which prints the command the user runs
next, with the spec's path as the argument.

## Contract

**Class:** design — the territory is `skill_classes.design` in
`@.claude/schemas/extensions.json` and `ArchHook.java guard` enforces it. Writes inside the
use case folder and the backlog, nothing else; a write anywhere outside is refused with exit
2, not reported.

**Reads** `@.claude/rules/architecture-ddd.md` (Application section — where the
transaction opens, what doesn't go in the signatures), `@.claude/rules/naming.md`,
`@.claude/rules/error-handling.md` (the four kinds only — names belong to `domain-modeling`),
`@.claude/rules/api-graphql.md` (§ Choosing the inbound protocol only, for an HTTP trigger),
`@.claude/rules/spec-diagrams.md` (the sequence diagram and the flowchart) with
`references/mermaid-use-case-diagrams.md`,
the active blueprint's `packages.map` and naming convention, and this
skill's `references/scope-boundary.md` before counting effects.

**Writes** `docs/use-cases/UC-NNN-<slug>/00-use-case.md` and appends to
`docs/use-cases/BACKLOG.md`. Only those. The `10-` through `40-` partials belong to the
layer skills; the consolidated `UC-NNN-spec.md` belongs to the `/new-feature`
orchestrator.

**Owns** the use case number and slug. No other piece assigns them.

**Shares one sequence, with one other named writer.** `BL-NN` is assigned here when a split
appends a backlog row, and by `/new-feature`'s consolidation when a partial defers something to
the backlog. Those two, never a third: a design skill that appended its own row would compute
"highest plus one" against the same file in the same run and issue a duplicate.

**Does not** edit an approved spec (`status: approved`, `implemented` or
`implemented-blocked`) — reads it as a contract, and records the needed change in its own
impact section.

**Does not** write code, tests, migrations, or OpenAPI, and never writes under `src/`. Doesn't touch the inbound REST
adapter — the package the blueprint's `packages.map` gives that role
(`rest-api-architect`) —, the domain or application (`gof-design-patterns`,
`domain-modeling`), nor `.claude/rules/**`. Doesn't weigh a storage technology: records the
storage family and the search engine the request states or the user answers.

**Does not** reproduce rules. Cites by path; what the rule already says isn't repeated
in the spec.

**Also carries** `examples/` — twelve complete `00-use-case.md` fixtures for testing
`/new-feature` and `java-spring-boot-developer`, indexed in `examples/README.md`. Meta-repo
documentation, not this skill's runtime output: the `export` manifest keeps only
`SKILL.md`, `templates/` and `references/`, so this directory does not travel.
