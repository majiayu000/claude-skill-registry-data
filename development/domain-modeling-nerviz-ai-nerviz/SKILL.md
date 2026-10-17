---
name: domain-modeling
description: >
  Details the domain and application layer of an already-designed use case — aggregate,
  value objects, invariants, ports, and events — into the `10-domain.md` partial. Use
  when the request involves modeling the domain, defining an aggregate or value object,
  designing a use case's ports, or detailing a spec already created by `use-case-design`.
  Piece of the `/new-feature` pipeline: requires `00-use-case.md` in the given folder
  and stops without it.
argument-hint: "[path of the UC-NNN-<slug> folder]"
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash(find:*), Bash(ls:*), Bash(grep:*), Bash(sort:*)
model: opus
---

## Available specs

!`find "${CLAUDE_PROJECT_DIR:-.}/docs/use-cases" -mindepth 1 -maxdepth 1 -type d -name 'UC-*' 2>/dev/null | sort`

Empty above → none yet, run `/use-case-design` first. (`find`, not an `ls` glob: under zsh an unmatched glob
aborts the command before any fallback runs.)

## Target

$ARGUMENTS

---

# Domain Modeling

Details the **interior** of a use case: what the mother spec named, this skill gives
shape to. Signatures, types, invariants, and where each lives.

**Entry rule: without a mother spec, there's nothing to detail.** This skill reads
`docs/use-cases/UC-NNN-<slug>/00-use-case.md` and treats it as a contract. Without
that file, it stops and tells you to run `/use-case-design` — modeling a domain from a
loose request reinvents the boundary the mother spec exists to fix.

**Exit rule: it doesn't write code.** It emits `10-domain.md`. The Java classes come
from the executor agent, which reads the partial and the `templates/` exemplars.

## How it's invoked

Two paths, and both matter: `/domain-modeling` by hand, or chained by `/new-feature` once
that orchestrator exists. That's why it does **not** carry
`disable-model-invocation` — that field hides the skill from the model, and a skill the
model can't see is a skill the orchestrator can't call.

The guard against out-of-order firing isn't the frontmatter: it's the **entry rule**
above. Without the previous partial, the skill stops and says what needs to run first.
Recorded in `@.claude/decisions/0007-pipeline-skills-invocation.md`.

## Why this isn't a subagent

It's a procedure whose step 3 goes back to the user to ask what the mother spec left
open — the exact type of each value object, which invariant lives in the constructor. A
subagent doesn't see the conversation. Decision recorded in
`@.claude/decisions/0003-skill-domain-modeling.md`.

Pinned to `opus`: the partial is what the executor implements verbatim. A pinned model does not make this a subagent — the interview needs the conversation, and the pin holding for the rest of the turn keeps `/new-feature` on the model that designed it (`@.claude/decisions/0081-skill-model-required-per-class.md`).

## Boundary with neighboring skills

Three pieces touch domain and application. Overlapping would be an ownership bug, so the
division is by **moment**, not by folder:

| Piece | When it acts | What it produces |
|---|---|---|
| `use-case-design` | Before the domain exists | Canonical names and boundary — `00-use-case.md` |
| **this skill** | After the mother spec, before code exists | Signatures and invariants — `10-domain.md` |
| `gof-design-patterns` | Standalone, outside a feature run, on code that already hurts | Refactor of real code (`file:line` that hurts) |

The pattern decision for the case being designed is this skill's, for the domain and
application — step 5b, through that skill's § Design-time use, which this one reads and
never invokes. If the code already exists outside any feature run and the problem is a
growing chain of `if`s, it isn't this skill — it's `/gof-design-patterns`. If there's no
mother spec, it also isn't this skill.

## Procedure

1. **Read the mother spec.** Without `00-use-case.md` in the given folder, stop and
   report. Extract: canonical names, trigger, effects, listed invariants, error table,
   and the component-table rows marked `Detailed by: domain-modeling`.
2. **Read the existing code.** `Glob`/`Grep` the project for the canonical names. The
   aggregate might already exist and the use case be just a new method. Confirm or
   correct the mother spec's NEW/CHANGE/REUSE state — and if you correct it, say so in
   the report: the mother spec is now stale and someone needs to review it.
3. **Ask only what's missing.** `AskUserQuestion` for what the mother spec didn't fix,
   **at most 4 questions per call and never fewer than 2 real options per question**. One
   option isn't a question: decide that item and record the decision in the partial. The
   runtime rejects the **whole batch** over a single one-option question
   (`InputValidationError ... "too_small"`), which is a full round trip lost —
   `@CLAUDE.md` § Known pitfalls. This step is where it happened
   (`lessons-learned-010.md` § 8).

   | Typical gap | Why it matters |
   |---|---|
   | Type of each field — `String` or value object | `email: String` spreads validation everywhere; `Email` concentrates it in one place. The criterion isn't opinion: `@.claude/rules/value-objects.md` |
   | Invariant in the constructor or in a method | Constructor = always true. Method = only for that transition |
   | Does the aggregate emit an event? | Decides whether there's a sibling UC to consume it, and whether `messaging-architect` comes in |
   | …and can that event be lost without anyone noticing? | The `Durability` column of § 4 · Events. A property of the event — whether its absence is later detectable and recoverable — not of its transport. `messaging-architect` turns the answer into a publication form; deciding the form here is opining outside this skill's territory |
   | Aggregate boundary — what's inside and what's a reference by id | An aggregate that's too big is an unnecessary lock |
   | Command with a single field | Sometimes the record is ceremony; sometimes it's cheap extensibility |

   Don't ask what the mother spec already answered. Repeating an already-answered
   question is the sign you didn't read step 1.
4. **Fix the signatures.** Names from `@.claude/rules/naming.md` § Architecture vocabulary
   — they already come from the mother spec, don't change them. Exception names are
   this skill's: the mother spec only describes the situation and its kind. Zero framework types in signatures
   (`@.claude/rules/architecture-ddd.md`). Zero `null` crossing a boundary; `Optional`
   only on query return (`@.claude/rules/code-quality.md`). Every primitive field goes
   through the `@.claude/rules/value-objects.md` criterion before staying a primitive —
   a field with a formation rule that stays `String` is a decision to justify in the
   partial, not a default.

   **Derive which fields are sensitive — don't decide it.**
   `@.claude/rules/logging.md` § Masking candidates is the derivation, and it is
   mechanical: a field matches by **type** (the catalog's personal-data value objects) or
   by **name** (the list in that section, on the whole name or part of it). Walk every
   field of the aggregate and of every command and response shape through both halves, and
   list each match in the aggregate block.

   Two consequences, both from the same real failure — a `String securityNumber` holding a
   CPF that no partial ever flagged, and that shipped:

   - **A field that matches and is not masked needs a written reason** in the partial. The
     default is masked; not masking is the decision that has to say why.
   - **The list is a floor, not a ceiling.** A field carrying personal data whose name is
     not on the list is still a candidate, and the name goes into the rule — that is the
     only way the next project inherits it.

   This block is what `rest-api-architect` applies and what the architecture test checks;
   an empty block on an aggregate with a person in it is the bug, not the absence of one.
4b. **A status with more than one value owes a transition, or a named future case.** Whenever
   the aggregate carries a state field whose type admits more than one value — an enum, a
   status value object, a lifecycle flag — every value some use case will eventually need has
   to be **reachable through the aggregate's own API**. For each one, the partial's aggregate
   block says which of these holds:

   - **a method on the aggregate** (`activate()`, `reject(reason)`), designed here, when a use
     case in this project performs the transition — now or in the case being designed;
   - **a named backlog `UC-NNN`** that will introduce it, stated as such, when nothing does
     yet.

   What is never an answer: the reidratation path. A factory that exists to rebuild persisted
   state (`rehydrate`, a package-private constructor the mapper calls) is not a transition, and
   using it to produce a state no behaviour produces is how a state becomes reachable in tests
   and unreachable in production. That shipped: `Customer.register()` always produced
   `KYC_IN_PROGRESS`, the aggregate had no transition, a later case added a precondition on
   `ACTIVE`, and the fixtures reached it through `rehydrate()` while every real request failed
   (lessons-learned-013 §§ 5, 8.7).

   Design only the transitions a use case needs — a method for a value nobody moves to yet is
   dead code, and the named backlog case is the correct answer in that situation. What this step
   forbids is the third option: a value with no method and no named case, where the gap is
   discovered later by whoever adds a precondition on it.

   When the state is an enum, a question the aggregate asks about it — final or not, which
   value a verdict leads to — is a method of the enum, and the partial names it; where a branch
   over the state goes is `@.claude/rules/code-quality.md` § Branching on a closed set. Form
   exemplar: `templates/Enum.java.example`.
4c. **`Access` = the owner makes ownership an invariant of this case.** When
   `00-use-case.md`'s `Access` row says only the owner may execute it, the check is a
   business rule, never a request rule (`@.claude/rules/authorization.md` § Boundary), and this
   partial carries its three pieces:

   - **the owner field** on the aggregate, typed as the identity value object of whoever owns
     it (`CustomerId`, `UserId`) — REUSE when it exists;
   - **the actor in the command** — a value object (`Actor`) holding that identity, plus the
     override flag or role when `Access` grants one (a support agent acting on any order).
     Never a framework type: the controller resolves it from the authenticated principal, and
     `security-architect` names where;
   - **the invariant** "the actor owns the aggregate, or holds the override", raising the
     **same not-found exception** the use case raises for an absent aggregate — the response
     must not reveal that someone else's resource exists. A distinct 403 needs a typed
     exception `@.claude/rules/error-handling.md` does not have; propose it as a divergence,
     never invent it.

   A query use case filtered by owner ("my orders") carries the actor the same way, and the
   outbound port takes it as a parameter — the filter is in the query, not applied after
   loading everyone's rows.

4d. **An external call becomes a port of kind `external HTTP`.** When `00-use-case.md`'s
   `External calls` row names a system this case calls over HTTP, the partial carries:

   - **the outbound port**, kind `external HTTP`, in domain types only — named for the
     capability (`PaymentGatewayPort`, `AddressLookupPort`), never for the client or the vendor's
     product. Every output port in § 3 names its kind; the orchestrator reads it;
   - **the domain outcome of each business answer** the row describes — a refusal is a
     `BusinessRuleViolationException`, an absent remote resource an empty `Optional`, a duplicate a
     `ConflictException`. A failure of the system itself (down, slow, unreadable) is not modeled
     here: it is an integration family (`@.claude/rules/error-handling.md` § Integration
     families), and the port's Javadoc names the ones it may throw;
   - **the idempotency key** on the aggregate, when the row says the call is a write and the
     system accepts a key: a value object created with the operation and persisted with it,
     never generated at call time — REUSE when it exists;
   - **a state for an unknown result**, when the row says a write's unknown result is
     reconciled later (`CAPTURE_UNKNOWN`), with the transition out of it — the reconciliation
     pass that drives it is a requirement for `jobs-architect`, recorded by
     `http-client-architect`.

   Client, timeouts and retries are not this partial's: `http-client-architect` reads this port.

4e. **A model or a semantic search becomes a port of kind `LLM` or `vector store`.** When the case
   asks a language model for a decision-shaped answer — classify, extract, moderate — the port is
   kind `LLM`; when it asks for the items nearest in meaning to a text, kind `vector store`
   (embedding is not a kind of its own: a similarity search needs the vectors stored). The partial
   carries:

   - **the outbound port**, in domain types only, named for the capability (`TicketClassifier`,
     `ProductSemanticSearch`), never for the model or the vendor;
   - **for an `LLM` port, a return type with a "could not decide" value** — a sealed
     `Suggested | Undecided`, never a bare enum — **and the review state it leads to**
     (`AWAITING_TRIAGE`, `PENDING_REVIEW`) with the transition out of it. The model suggests; the
     aggregate decides, and a value the domain keeps for itself (a `CRITICAL` priority) is set by a
     domain rule, never accepted from the suggestion (`@.claude/rules/ai.md` § Boundary);
   - **for a `vector store` port, identifiers as the result**, never the aggregate, and the write
     side (`index`, `remove`) as a port of the same kind when this case changes what the store
     mirrors.

   Model, prompt, store and timeouts are not this partial's: `ai-architect` reads this port.

4f. **A search over words, filters or facets becomes a port of kind `search index`.** Only when
   `00-use-case.md`'s `Search index` row names a projection — never inferred here. The partial
   carries:

   - **for the read case, the outbound port** named for the capability (`OrderSearch`), taking the
     query in domain terms and a cursor, returning a **read projection** — a record of what the
     result shows — and never the aggregate, which a caller that acts on it loads from its own
     repository;
   - **for the indexer case, the write side** (`upsert`, `remove`, each with the source's version)
     as a port of the same kind, and the outcome "the index already holds a newer copy" as a value
     of its result, not an exception;
   - **the change event the projection is fed by** — the snapshot it carries and the source
     aggregate's version — in the Events block, for every case that changes the source.

   A search by meaning stays `vector store` (4e). The mapping, the engine and the indexer's rules
   are not this partial's: `search-architect` reads this port
   (`@.claude/rules/search.md` § Boundary).

4g. **Reading an aggregate's history is a port of kind `persistence`.** Only when the case shows
   earlier versions and `00-use-case.md`'s `Audit` row says `history` for that aggregate —
   never inferred here, and nothing in this partial for a case that only writes an audited
   aggregate: the stamps and the history are written by the adapter, with no port. The partial
   carries the outbound port named for the capability (`LoadOrderHistoryPort`), taking the
   aggregate's id and a page, returning a **read projection** per change — revision, instant,
   actor, whether it created, updated or deleted, and only the fields the case shows — never the
   aggregate rehydrated: an old version may break an invariant the current code holds. A delete
   carries no state, so the projection is a sealed pair (written · deleted), never one record
   with empty fields. The stamps a business rule reads ("only its creator may cancel") are a
   field of the aggregate, loaded like any other; the aggregate never writes them. Mapping and
   tables are `persistence-architect`'s (`@.claude/rules/persistence.md` § Auditing).
5. **Map each invariant to its exception.** Typed family from
   `@.claude/rules/error-handling.md` and `errorCode` in `UPPER_SNAKE_CASE`. An invariant
   without a named exception is an invariant nobody will implement.

   **The exception family belongs to this skill, and this is where it enters the
   project.** `project-bootstrap` doesn't write it — it has no invariant to tie it to
   (`@.claude/decisions/0011-bootstrap-without-business-code.md`). So: search for
   `DomainException` in the project with `Grep`. If it doesn't exist, the partial's
   invariants block opens with the line **"Exception family: NEW — six classes in the
   `domain.exception` package"**, and names the six. If it already exists, write
   **REUSE** and name only the missing ones. Once per project, not once per use case —
   the second spec finds them and reuses them.

   The form exemplars are `templates/DomainException.java.example`, the four typed
   ones, and `templates/ConcurrentUpdateException.java.example` — the one named subclass
   the rule fixes, since the persistence adapter throws it on the first optimistic-lock
   failure and a message listener's retry tells it apart by type. Don't invent categories
   beyond the four: the taxonomy belongs to the rule, not this skill.

   Default every invariant to the plain typed family + a string `errorCode`. Promote to
   a named subclass (`OrderAlreadyPaidException extends ConflictException`, no new
   state) only when the entry bar in `@.claude/rules/error-handling.md` § Shape of the
   base classes is met: the `errorCode` already repeats across ≥ 2 call sites, or a
   caller needs to `catch` it specifically rather than branch on `errorCode()`. A first
   occurrence never gets its own class — the same discipline `gof-design-patterns` applies to
   when a symptom earns a design pattern.

   **A second call site found in a later use case** promotes the exception here, in this
   case's `10-domain.md`, under `## Impact on approved use cases` — never by editing the
   earlier case's partial or spec, which are approved and immutable.
5b. **Decide the design patterns of the domain and application.** Run
   `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use over what this case adds —
   aggregate, value objects, ports, application services — against the mother spec's forces
   (a rule enumerated per type, construction with invariants, a predicate the query also
   needs) and the code step 2 surveyed. The answer goes into `## Design patterns`, and every
   class it creates into § 5 Components to create — `none` when nothing matches, and absence
   is not `none`.
6. **Generate** from `templates/domain-spec.md.example` to
   `docs/use-cases/UC-NNN-<slug>/10-domain.md`. The diagrams of block 1 — the `classDiagram`, and the
   `stateDiagram-v2` whenever *State reachability* is not `none` — are drawn last, from the
   tables already written, per `@.claude/rules/spec-diagrams.md`. Syntax and the renderer's
   traps: `references/mermaid-class-and-state.md`; a shape the base template does not show (a
   child entity with a multiplicity, a sealed type, final states):
   `templates/domain-diagram-variants.md.example`.
7. **Report and stop.** File path, divergences found against the mother spec, and what's
   missing for the folder to be complete (`20-persistence.md`, `30-rest.md`,
   `40-tests.md`). Don't invoke anyone.

## What the partial contains

Five blocks, all mandatory. An empty block is written as "none" — deleting it hides a
question nobody asked.

| Block | Details | Form exemplar |
|---|---|---|
| Aggregate and value objects | Root, fields, types, which VOs exist and why, which fields are sensitive (masking candidates), and — for every state field with more than one value — which method reaches each value or which named backlog case will; a class diagram of the root and its value objects, and a state diagram when a state field has more than one value | `Aggregate.java.example` · `ValueObject.java.example` · `ValueObjectCatalog.java.example` · `Enum.java.example` |
| Invariants | Each rule, where it's enforced, which exception it raises; and the state of the exception family (NEW or REUSE) | `DomainGuards.java.example` · `DomainException.java.example`, the four typed ones and `ConcurrentUpdateException.java.example` · `@.claude/rules/error-handling.md` |
| Ports | Input (`<Verb><Noun>UseCase`), command, output — complete signatures, each output port with its kind (`persistence` · `messaging` · `external HTTP` · `LLM` · `vector store` · `search index`) | `UseCasePort.java.example` · `Command.java.example` |
| Events | Which event, which payload, which UC consumes it | `DomainEvent.java.example` |
| Design patterns | Each pattern the domain or application adopts: the spec line or `file:line` that forces it, the classes it creates, the "When not" checked — step 5b | `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use |

The exemplars in `templates/` are **reference for form**, not files to copy: they show a
record with a compact constructor, a static `of` factory, and total absence of
framework. It's the executor that reads them when generating code.

Thirteen exemplars, and the six of the exception family (`DomainException`, `NotFound`,
`Validation`, `BusinessRuleViolation`, `Conflict`, `ConcurrentUpdate`) — the first five
arrived here when `project-bootstrap` stopped emitting business code. This skill owns the shape of the domain, and the
exception is domain: transport-agnostic, no framework, with a stable `errorCode`.
Record: `@.claude/decisions/0011-bootstrap-without-business-code.md`.

## Contract

**Class:** design — the territory is `skill_classes.design` in
`@.claude/schemas/extensions.json` and `ArchHook.java guard` enforces it. Writes inside the
use case folder and nothing else; a write anywhere outside is refused with exit 2.

**Reads** `docs/use-cases/UC-NNN-<slug>/00-use-case.md` (mandatory — stops without
it), `@.claude/rules/architecture-ddd.md` (Domain and Application sections),
`@.claude/rules/value-objects.md` (criterion for which field becomes a value object),
`@.claude/rules/naming.md`, `@.claude/rules/error-handling.md`,
`@.claude/rules/code-quality.md`, `@.claude/rules/logging.md` (which fields to flag as
masking candidates), `@.claude/rules/spec-diagrams.md` (the diagrams of block 1) with
`references/mermaid-class-and-state.md`, `@.claude/rules/authorization.md` § Boundary (only when `Access` is the
owner — step 4c), and the active blueprint's `packages.map`.

**Writes** `docs/use-cases/UC-NNN-<slug>/10-domain.md`. Only that file.

**Does not write Java code.** The classes in `domain/**` and `application/**` come from
the executor agent — the exception family included: this skill owns the **shape** (the
`templates/` exemplars) and the **state** (NEW or REUSE, in the partial), not the
writing. Does not touch `00-use-case.md` (`use-case-design`), the other partials, or
`.claude/rules/**`.

**Does not collide with `gof-design-patterns`.** That skill owns the catalog and, invoked
standalone, refactors code that already hurts; this one decides which catalog row shapes the
domain of the case being designed, and writes the decision into the partial — step 5b.
Different artifacts, one owner of each.

**Does not** decide persistence, mapping, or transport technology —
`20-persistence.md` and `30-rest.md` have their own owners.
