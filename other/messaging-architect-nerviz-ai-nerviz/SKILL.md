---
name: messaging-architect
description: >
  Designs the Kafka producer/consumer adapter for an already-modeled domain event —
  topic, partition key, serialization, consumer group, delivery semantics, retries and
  DLQ, and the AsyncAPI contract a consumer outside the project reads — into the
  `25-messaging.md` partial. Use when the request involves publishing a
  domain event to Kafka, consuming a Kafka topic, designing a producer or consumer
  adapter, deciding topic/partition/serialization, wiring retry/DLQ for a message
  listener, or documenting the asynchronous contract (AsyncAPI, Springwolf). Piece of the `/new-feature` pipeline: requires `10-domain.md` in the given
  folder with an Events block that names external delivery, and stops without it.
argument-hint: "[path of the UC-NNN-<slug> folder]"
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash(find:*), Bash(ls:*), Bash(grep:*), Bash(sort:*), Bash(awk:*)
model: opus
---

## Available specs

!`find "${CLAUDE_PROJECT_DIR:-.}/docs/use-cases" -mindepth 1 -maxdepth 1 -type d -name 'UC-*' 2>/dev/null | sort`

Empty above → none yet, run `/use-case-design` first. (`find`, not an `ls` glob: under zsh an unmatched glob
aborts the command before any fallback runs.)

## Target

$ARGUMENTS

---

# Messaging Architect

Designs **how a domain event leaves the process and how another one gets consumed**: topic,
key, serialization, delivery semantics, retry and DLQ, and the two adapters that carry it.
What `domain-modeling` already named as an event with a consumer, this skill gives a broker
transport to.

**Entry rule: without `10-domain.md` naming an event for external delivery, there's nothing
to transport.** This skill reads `docs/use-cases/UC-NNN-<slug>/00-use-case.md` and
`10-domain.md` and treats them as a contract. Without the domain partial, it stops and tells
you to run `/domain-modeling`. If the domain partial's Events block is "none," or names only
a sibling use case in the same process, it also stops: an in-process call has no broker to
design — designing Kafka config for it would be scope no one asked for.

**Exit rule: it doesn't write code.** It emits `25-messaging.md`. The Java classes come from
the executor agent, which reads the partial and the `templates/` exemplars.

**Rule rule: the rules don't live here.** Idempotent consumer, `acks=all`, topic naming,
retry/DLQ, and the rest are `@.claude/rules/messaging.md`. This skill applies them and cites
them; it doesn't reproduce them.

## How it's invoked

Two paths, and both matter: `/messaging-architect` by hand, or chained by `/new-feature` once
that orchestrator's pipeline reaches this point. That's why it does **not** carry
`disable-model-invocation` — a skill the model can't see is a skill the orchestrator can't
call.

The guard against out-of-order or unnecessary firing isn't the frontmatter: it's the **entry
rule** above. Recorded in `@.claude/decisions/0007-pipeline-skills-invocation.md`.

## Why this is a skill and not a subagent

Form 1, motivated by axis 2 (chained by `/new-feature`, also invocable by hand) and axis 9
(`domain-modeling` already owns the event; this skill only owns its transport). The closest
rejected form was a fourth option in the same decision — a dedicated "domain events" skill —
which failed invariant 2: `domain-modeling` already asks whether the aggregate emits an event
and already writes the Events block of `10-domain.md`. A subagent was never viable either: it
fails the § 5 counter-test in `claude-code-architect-designer`'s decision matrix on all three
points — the interview over topic/partitioning/DLQ is the heart of the task, the reference
content fits in `templates/`, and the partial it produces is short.

Pinned to `opus`: the partial is what the executor implements verbatim. A pinned model does not make this a subagent — the interview needs the conversation, and the pin holding for the rest of the turn keeps `/new-feature` on the model that designed it (`@.claude/decisions/0081-skill-model-required-per-class.md`).

## Boundary with neighboring skills

The division is by **moment and artifact**, not technology:

| Piece | When it acts | What it produces |
|---|---|---|
| `use-case-design` | Before the domain exists | `00-use-case.md` — boundary and canonical names |
| `domain-modeling` | After the mother spec | `10-domain.md` — aggregate, invariants, ports, **and the event itself** |
| `rest-api-architect` | After the domain partial | `30-rest.md` — transport, no schema, plus the schema requirements it creates |
| **this skill** | After the domain partial, only when an event needs external delivery — and **before** `persistence-architect` | `25-messaging.md`, § 6 included |
| `jobs-architect` | After this skill, when § 2 chose Form B | `35-jobs.md` — the relay's schedule, coordination across instances, the prune job |
| `persistence-architect` | After this skill and `jobs-architect` | `20-persistence.md` + migration — builds what § 6 of both partials asked for |
| `test-architect` | After all of them | `40-tests.md` |

`domain-modeling` decides **whether** an event exists and **who consumes it**. This skill
never redefines the event or its payload's business meaning — it only decides how it travels.
If the consuming use case is a sibling in the same process, there is no broker to design and
this skill doesn't run at all (see Entry rule).

**Out of scope, on purpose: in-process dispatch.** Spring's own `ApplicationEventPublisher`/
`@EventListener` is a same-JVM transport for the same kind of domain event this skill handles
for Kafka. No use case in this repo has needed it yet, so it isn't built — anti-pattern 9
(anticipation) in `claude-code-architect-designer`'s decision matrix. If one does, it's one
more transport option inside this skill (another `templates/` pair and a section in
`@.claude/rules/messaging.md`), not a new skill: the boundary above already put event
*definition* in `domain-modeling` and event *transport* here, and in-process dispatch is
still transport.

## Procedure

1. **Read the specs.** `00-use-case.md` and `10-domain.md` from the folder in
   the target above. Without the second, stop. Extract: the event's name, payload fields, the
   consuming use case, and whether that consumer is external (another service, another
   deployable) — that's what makes this skill apply at all.

   When the consuming case is a search projection's indexer — its `23-search.md` exists — read its
   **§ 8** too: the consumer it requires is fixed there, by guarantee — one partition key per
   aggregate, at-least-once, a stale write acknowledged and never retried, a bounded retry and a
   dead letter. The search document and its write rules are `search-architect`'s; this skill
   designs the consumer around them.

2. **Survey what already exists.** A topic or consumer group already wired gets reused, not
   duplicated. **The bounded context comes from here too — read it, never ask.** The topic
   name's first segment (`@.claude/rules/messaging.md` § Topics and serialization) is a
   project fact with the same standing as the base package: it is declared once, in the
   project's root `CLAUDE.md`, and every topic of every use case shares it.

   ```bash
   grep -i "bounded context" CLAUDE.md
   grep -rhoE "^ *(topic|topics?\.[a-z-]+): *[a-z0-9.-]+" src/main/resources/ 2>/dev/null
   ```

   Not declared **and** no topic exists yet → stop and say which line is missing from the
   root `CLAUDE.md`, rather than choosing a prefix inside this use case. A prefix decided
   per use case is how one system ends up with two namespaces: the next case, designed in
   another session, has no reason to pick the same one (lessons-learned-012 § 5).

   ```bash
   grep -rln "@KafkaListener\|KafkaTemplate" --include='*.java' src/ 2>/dev/null
   grep -rn "group-id\|bootstrap-servers" src/main/resources/ 2>/dev/null
   grep -rl "processed_events\|ProcessedEventStore" --include='*.java' src/ 2>/dev/null
   ```

3. **Interview — only what the specs don't fix.** `AskUserQuestion`, at most 4 questions per
   call and **never fewer than 2 real options per question**: one option isn't a question —
   decide it and record the decision in the partial, since the runtime rejects the whole
   batch over a single one (`@CLAUDE.md` § Known pitfalls). Don't re-ask what
   `00-use-case.md` or `10-domain.md` already answered.

   | Axis | Decides |
   |---|---|
   | **Publication timing** — must the event survive a broker outage between the commit and the publish? | Form A (publish after commit) or Form B (transactional outbox + relay), per `@.claude/rules/messaging.md` § Publication timing. Read the `Durability` column of `10-domain.md` § Events **first**: when it already answers, record the form and don't ask again |
   | Partition key candidate (which field must stay ordered) | Whether the aggregate id is enough, or a composite key is needed |
   | Consumer group id, new or existing | Reuse vs. a fresh subscription with its own offset |
   | `auto-offset-reset` tolerance (losing vs. reprocessing on redeploy) | `earliest` or `latest` |
   | Ordering requirement across different aggregates | Whether one topic is enough or the event needs to fan out differently |
   | Existing `processed_events`-style dedupe table in this project | Reuse vs. ask `persistence-architect` to model one |
   | **Serialization** — do both sides need a contract they can validate at build time, and is there a second team on the other end asking for it? | JSON (the rule's default) or a schema registry. **Ask only with the cost in the question**, see below |
   | **Personal data in the payload** — does the event carry a field that identifies a natural person, and if so, what is the minimum the receiver needs? | The payload's field list: full value, reduced form (id, hash, last digits), or a reference the receiver resolves. `@.claude/rules/personal-data.md` § In transit. **Always asked when a candidate field exists**, see below |
   | **Who guarantees dedupe**, when the consumer is not in this project | Whether at-least-once is actually absorbed anywhere. `@.claude/rules/messaging.md` § Delivery semantics |
| **Who owns the contract** — does a document already exist that this service must implement, or does a team outside negotiate it before any code? | Code-first (the rule's default, generated by Springwolf from the annotations) or spec-first (ZenWave SDK). **Ask only with the cost in the question**, see below |

   Every axis but the first is consumer-side. A use case that only **produces** still has the
   publication timing to settle, so "no axis applies, no `AskUserQuestion` this pass" is never
   the right conclusion for a producing use case: either the domain partial's `Durability`
   column already fixed the form and the partial records which, or this step asks.

   **The serialization axis, and the shape its question must have.**
   `@.claude/rules/messaging.md` § Topics and serialization fixes JSON as the default and
   makes a schema registry a deliberate upgrade — "not assumed until a use case actually
   needs it". So:

   - **No trigger written in `00-use-case.md` or `10-domain.md` → don't ask.** Record
     `JSON` in the partial together with the rule's condition, in one line, and move on. A
     rule default is not a question, and "the consumer is another team" is not by itself the
     trigger — the trigger is that both sides need the contract validated **at build time**.
   - **Trigger written → ask, with the cost inside the question, not after it.** The upgrade
     is not one line of configuration; the option text names every place it lands:

     | The upgrade buys | The upgrade costs |
     |---|---|
     | A contract both sides validate at build time, and compatibility checked by the registry | A `schema-registry` service in `docker-compose.yml` · three dependencies (`org.apache.avro:avro`, `io.confluent:kafka-avro-serializer`, `avro-maven-plugin`) · the `confluent` repository, because the serializer is **not on Maven Central** · a new source directory (`src/main/avro/*.avsc`) and generated code · a JaCoCo exclusion for that generated code · `mock://` in the tests, with subject compatibility not really tested |

   A user who picks the upgrade after reading that row picked it knowingly. One who is
   offered "JSON (recommended)" versus "Avro + schema registry" with no cost attached is
   picking a name, and that is how the six items above entered a project in one answer.

   **The personal-data axis, and why it is asked and not inferred.** Run the candidate test of
   `@.claude/rules/personal-data.md` § What counts as personal data over the payload's fields —
   against the types of `@.claude/rules/value-objects.md` § Catalog, never against field names
   alone: the field that leaked a national identifier in a real run was called
   `securityNumber`, and masking it in the logs (which `@.claude/rules/logging.md` did require,
   and which was applied) changed nothing about the copy serialized into the outbox column and
   the copy published on the topic.

   - **Candidate field present → ask, with the three legitimate answers as the options:** the
     full value, a reduced form, or a reference the receiver resolves under its own
     authorization. "The receiver's whole purpose is that value" is a correct answer — an
     identity-verification service does need the identifier it verifies — and it is the answer
     that most needs recording, because it is the one nobody revisits when the receiver
     changes.
   - **No candidate field → one line in the partial saying so**, not silence. `none` is an
     answer; an unasked question is what shipped a CPF in clear across a team boundary and into
     a `jsonb` column retained for seven days.
   - Whatever the answer, it lands in § 2 of the partial next to the payload's field list, with
     the receiver named. A decision recorded elsewhere is a decision the next run re-decides.

   **The dedupe-owner axis.** At-least-once delivery is only safe because something absorbs
   the duplicate, and `@.claude/rules/messaging.md` § Delivery semantics puts that on the
   consumer. When the consumer is **in this project**, step 5a is what makes it true. When it
   is **not** — another team, another company — the guarantee is being delegated across an
   organizational boundary, and this skill's job is to say so out loud rather than let a
   Javadoc sentence imply it is handled:

   - name the receiver, and state whether its idempotency is **contracted** (written down
     somewhere both sides can point at), **assumed**, or **unknown**;
   - when the answer is "assumed" or "unknown", that is a **finding for the final report**, not
     a line buried in § 3 — the run ends naming it, so the person who asked for the feature
     decides whether to accept it;
   - the event's own identity is what makes dedupe possible at all, so the payload carries it
     regardless of who dedupes: the same `event_id` the outbox row is keyed on.

   **The contract-owner axis, and why it is rarely asked.** `@.claude/rules/messaging.md` § Contract
   documentation makes the AsyncAPI document a product of the code and spec-first an alternative with
   written criteria. So:

   - **No trigger written in `00-use-case.md` or `10-domain.md` → don't ask.** Record `code-first` in
     § 1 with the rule's condition in one line. "Another team consumes the topic" is not a trigger —
     that team reads the generated document. The trigger is that a document **exists before this
     service** and this service must conform to it.
   - **Trigger written → ask, with the cost inside the question:**

     | Spec-first buys | Spec-first costs |
     |---|---|
     | The document is the source and the code conforms to it | A generator that writes **Spring Cloud Stream** adapters — not the `KafkaTemplate` and `@KafkaListener` ones of this skill's exemplars — so the String wire contract, the outbox writer and the flow layout are replaced · a build plugin and two generator artifacts outside the Boot BOM · generated sources under `target/` · operation ids written as Java identifiers (`templates/zenwave-sdk-maven.xml.example`) |

   - Whatever the answer, it is written in § 1 next to the channel row. Spec-first also writes
     `spring-cloud-stream` as the transport there, and the Form A/B publication axis does not apply
     to it: the generator knows no outbox, and this skill reports that instead of designing around it.

4. **Design the producer adapter.** Implements the outbound port `domain-modeling` already
   declared — never a new interface. Payload is the minimum the consumer needs, mapped
   explicitly from the domain event; the event itself never serializes directly. The
   publication form from step 3 decides the shape, and only the shape — the port's signature
   is the same either way:

   | Form | What implements the port | Extra pieces | Exemplar |
   |---|---|---|---|
   | A — publish after commit (default) | The adapter sends to the broker directly | none | `templates/KafkaProducerAdapter.java.example` |
   | B — transactional outbox + relay | The adapter writes an outbox row inside the caller's transaction | the relay pass (`RelayOutboxEvents` + `OutboxEventSender`, whose Kafka implementation is the only `KafkaTemplate` importer), `OutboxRelayGateway` port, shared `outbox_events` table. The pass's **schedule** and the **prune job** are `jobs-architect`'s | `templates/OutboxRelayPublisher.java.example` |

   **4a. Form B's outbox, when step 2 found none. Declare the need, never the columns.**
   The outbox belongs to `persistence-architect` — the table, its columns, its indexes, its
   migration, the claim query, and the pacing those columns encode. This skill's § 6 row
   says three things and stops:

   1. that the case needs the project's shared `outbox_events` (one for the whole project,
      never one per event or per aggregate — same nature as `idempotency_keys`);
   2. the **delivery guarantee** the relay has to honour: at-least-once, how many attempts
      before giving up, and the DLQ destination once it does;
   3. the addressee — that skill's **step 4b**, which models it from
      `persistence-architect/templates/OutboxEventTable.sql.example`.

   **And the schedule is not this partial's either.** When a pass runs, how often, on how many
   instances, the switch that keeps it out of the integration tests, and the job that prunes
   published rows are `jobs-architect`'s — it runs right after this skill whenever § 2 chose
   Form B, and reads § 2 and § 6 to design them into `35-jobs.md`
   (`@.claude/decisions/0087-jobs-architect-skill.md`). This partial names the relay's pass and
   the guarantee it owes; it never names a cron, an interval, or a lock.

   **Never list column names here.** Inventing `next_attempt_at`, `failure_reason`,
   `created_at` as "requirements" produced three guaranteed divergences in a real run, and
   one of them silently changed behaviour: the exemplar has no `next_attempt_at`, so
   per-row exponential backoff became a fixed 2s repoll, decided by a precedence rule
   written for table shape. The column set has one owner and one canonical source, and
   neither is this file.

   The guarantee has a second half, and it is the one a real run left unstated: **at-least-once
   only holds if something absorbs the duplicate.** § 6's row names the attempts and the DLQ;
   § 3 names who dedupes (step 3's axis). The claim query itself — locked, leased, or explicitly
   single-instance — is `persistence-architect`'s decision and belongs in `20-persistence.md`;
   what this skill must not do is accept a method *named* like a claim as proof that a claim
   happens. A gateway method called `claimPending` implemented as an unlocked `SELECT` is the
   shape that shipped, and two relay instances then publish the whole batch twice, every pass.

   What this skill keeps is the guarantee, and it keeps it as a **requirement**, not a
   suggestion: a shape that cannot satisfy the declared backoff and attempt count is a
   divergence that stops the pipeline (`/new-feature`'s consolidation, § Precedence), not
   something either skill resolves alone. The port stays declared here too — the pair in
   step 4b implements `OutboxRelayGateway`, it doesn't re-declare it.

   The receiving end models the table once from
   `persistence-architect/templates/OutboxEventTable.sql.example` and
   `templates/OutboxEventStore.java.example` (for an aggregate of the document family,
   `MongoSharedCollections.java.example`, the outbox written inside the MongoDB transaction) — the mirror of its own step 4a for
   `idempotency_keys`. Name the step in the partial, so the requirement has an addressee
   instead of a hope.

5. **Design the consumer adapter.** Translates the inbound payload into a call on the target
   use case's inbound port. Dedupe on the event's own identity before calling it; no
   `Acknowledgment` and no retry in the listener — the container commits after it returns and
   owns every retry. `@LogExecution` on the listener method is not decided here: the commons
   package may be installed by the implement run's pre-flight, after this design, so the
   executor adds it then, only when that package carries it.
   Shape: `templates/KafkaConsumerAdapter.java.example`. When the use case it calls writes an
   audited aggregate — an `Audit` row other than `none` — the call runs under
   `SystemActor.run("<consumer-name>", …)`: a listener thread has no caller, and an audited write
   with no authentication fails (`@.claude/rules/persistence.md` § Auditing ·
   `persistence-architect/templates/SystemActor.java.example`). The name is the consumer's.

   **5a. Dedupe table, when step 2 found none yet.** Not per-consumer: one table
   (`processed_events` or equivalent), shared by every listener in the project, modeled once.
   If missing, add it as a second row of **§ 6 · Schema requirements** and flag that
   `persistence-architect` needs to model it — this skill doesn't design tables,
   `20-persistence.md` does.

6. **Fix retry and DLQ.** Per `@.claude/rules/messaging.md` § Retry and DLQ, into § 4 of the
   partial. Asks nothing: every value below is derived from what is already written.

   - **Retry mode — derived, never asked.** `blocking` when `00-use-case.md`'s `Concurrency`
     or `Repetition` row makes per-key order decide the outcome (a state machine, first-wins, a
     later record superseding an earlier), or when the backoff takes seconds. `non-blocking`
     only when neither holds and the wait is long. The row cited is the `Why`.
     Shapes: `templates/KafkaListenerErrorHandler.java.example` (blocking) ·
     `templates/KafkaRetryableTopicListener.java.example` (non-blocking).
   - **Classification — project-wide, never per case.** Search the project for
     `ListenerFailureClassification`: absent → NEW, this case writes the shared error handling;
     present → REUSE. List every exception the consumed use case can raise (its error table, its
     `10-domain.md` ports) and the handling the rule's table gives it. A case that needs a type
     retried differently from the table is a rule question, not a row: stop and report it.
   - **`ConcurrentUpdateException`** — a consumed use case that writes a versioned aggregate
     raises it; its row is "retried", never "straight to the DLQ".
   - **Discard is no handling.** A record `00-use-case.md` calls "discarded" or "ignored" is a
     no-op the use case returns normally, with its log line and metric — written as such in the
     table, and a divergence to `10-domain.md` when the domain models it as an exception.

7. **Fix the configuration.** Bootstrap servers, producer `acks`/idempotence, consumer group
   and offset reset, ack mode — from `templates/application-kafka.yml.example`. Mandatory
   values are the rule; what this skill decides is the per-use-case sizing (group id, offset
   reset tolerance) from step 3. **Ack mode is derived:** not set (Boot's `BATCH`) unless the
   consumed use case has a port of kind `external HTTP` or `LLM` in `10-domain.md`, then
   `record`; already `record` in the project → stays `record` (`@.claude/rules/messaging.md`
   § Configuration).

   **JSON means JSON text on the wire, converted once per side** —
   `@.claude/rules/messaging.md` § Topics and serialization. The yml's `StringSerializer` /
   `StringDeserializer` pair is not a default to tune per case: it is what lets the Form A
   publisher and the Form B relay put the same bytes on one topic, and the partial names
   where each conversion happens (the publisher or the `OutboxAppender`; the converter bean
   in front of the listeners). A JSON value serializer in the yml next to a Form B relay
   publishes every payload double-encoded — the contradiction the exemplars carried until
   issue #58.

   **This skill owns the `bootstrap-servers` default, and it is host-first.** The application
   started with `./mvnw spring-boot:run` runs on the host, so the default has to be an address
   the host resolves — `${KAFKA_BOOTSTRAP_SERVERS:localhost:<external port>}`, the port
   `docker-architect`'s service block publishes for its EXTERNAL listener. The compose `app`
   service overrides the variable with the internal address. Defaulting to the internal one
   instead is `UnknownHostException: kafka` on the first host-side publish, with no path to
   recovery and no check that sees it — lessons-learned-013 § 11.

   **Declare the dependencies this transport needs, in § 7 of the partial.** A `KafkaTemplate`
   needs `org.springframework.boot:spring-boot-starter-kafka`: Spring Boot 4 moved Kafka
   autoconfiguration out of `spring-boot-autoconfigure`, so a plain `spring-kafka` library
   dependency wires nothing at all and every property above stays inert. Version column empty
   whenever the Boot parent manages it — never a version from memory (`@CLAUDE.md`
   invariant 8). The executor may write `pom.xml` for exactly the dependencies this block
   names; a requirement missing here is a run that stops at a missing type with nobody
   entitled to add it.

7b. **Decide the design patterns of this layer.** Run
   `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use over the producers and
   listeners this case adds, against the specs and what step 2 surveyed. The common symptom
   is listeners repeating one skeleton — deserialize, dedupe, call the port, acknowledge —
   with one step different; the catalog prefers an injected handler over a `protected
   abstract` hook when a single step varies. Reshaping the listeners that already exist is
   an `## Impact on approved use cases` row. The answer goes into `## Design patterns` —
   `none` when nothing matches, and absence is not `none`.

7c. **Fix the contract rows (§ 1), derived — never asked.** From what steps 1–7 already fixed:

   - **Channel and message name** — the topic, and the event's own name, identical on both sides.
   - **Headers** — `none` unless a header a consumer must rely on exists in the specs; each one is named,
     typed and described. The default wire carries only key and value.
   - **Producer operation** — derived id `<topic>_send_<port method>` from § 2's signature, and a
     description a consumer can act on: what the event means, when it is emitted, and **the partition
     key** (the key binding is not rendered into the document — `references/springwolf-reference.md`).
     `none` for a consumer-only case.
   - **Consumer operation** — derived id `<topic>_receive_<listener method>` and a description of what
     the listener does with the event, redelivery included. `none` for a producer-only case.

   The ids are derived, so the port method of `10-domain.md` and the listener's method name are part of
   the contract: rename either later and the snapshot test reports a changed operation. The first Kafka
   case of the project also declares `springwolf-kafka` in § 7 — the version is resolved from Maven
   Central, never written here — and the `springwolf` block of `templates/application-kafka.yml.example`
   in § 5. Under spec-first these rows are the generator's inputs, not annotations.

8. **Write the partial.** `docs/use-cases/UC-NNN-<slug>/25-messaging.md`, from
   `templates/messaging-spec.md.example`. Nine numbered blocks plus `## Compose services` and `## Design patterns`, all mandatory — § 6 through § 9
   included, each written as `none` when there is nothing to ask for.

   **§ 8 is `Personal data`, and it is written before the payload is called done.** Run
   `@.claude/rules/personal-data.md` § How to verify grep 1 against the payload record this partial
   just designed, and read every hit against the derivation in
   `@.claude/rules/logging.md` § Masking candidates — the type catalog plus the name list, one
   owner, not re-derived here. For each field that matches, § 8 states which of the three
   legitimate answers applies: the **full value** (the receiver's whole purpose needs it), a
   **reduced form** (an id, a hash, the last digits), or a **reference** the receiver resolves
   under its own authorization. A full value carries the receiver's name and the reason, which
   is the `Recorded decision` `@.claude/rules/personal-data.md` § In transit requires — *the exception
   is the record, not the absence of one*.

   A CPF crossed a team boundary in clear on a Kafka topic because no step ever asked: the
   pipeline's only mention of personal data was in the final report, which is detection after
   the spec is approved, after the code is written and after the commit, and it surfaced there
   only because the executor volunteered it (lessons-learned-014 § 8). The field was named
   `securityNumber`, which is why the name list and not intuition is what the grep is read
   against.

   **§ 9 is `Deferred`:** one row per item this partial decided not to do in this run — what was
   decided, what is missing, the norm that requires it (by path), and the intended owner,
   `checklist` (this run does it) or `backlog` (a later one does). Absence is not `none`: one
   says nothing was deferred, the other says nobody looked. Consolidation resolves each row to a
   real owner and is what writes the `BACKLOG.md` line and assigns its `BL-NN`. A deferral that
   leaves no owner is how a decided retention window ended up enforced by nothing
   (lessons-learned-014 § 9).

9. **Check Kafka has a container.** List the keys inside the `services:` block and look
   for `kafka` — never `grep -A2 "^services:"`, which reads two lines and then reports the
   children of `volumes:` as services (lessons-learned-012 § 12):

   ```bash
   awk '/^services:[[:space:]]*$/{s=1;next} /^[^[:space:]#]/{s=0} s&&/^  [A-Za-z0-9_.-]+:[[:space:]]*(#.*)?$/{sub(/[[:space:]]*#.*$/,"");print}' docker-compose.yml
   ```

   Write the answer as a row of the partial's `## Compose services`, shaped and decided by
   `@.claude/skills/docker-architect/references/compose-service-decision.md` — `exists` when `kafka` is listed, otherwise the question
   that reference owns (*add it*, *it runs elsewhere*, *I'll add it*). An `external` answer
   makes that address the host default of `spring.kafka.bootstrap-servers` in § 5, in place
   of `localhost:${KAFKA_EXTERNAL_PORT:29092}`. Do **not** invoke `docker-architect` and do
   not edit `docker-compose.yml`: that skill is the file's single owner, it is class `build`,
   and `ArchHook.java guard` refuses the call while a design run is open. A `materialize` row
   is added by `/new-feature-implement`, after the code is green.

10. **Report and stop.** Path of the file written, **the content of § 6** (each schema
    requirement handed to `persistence-architect`, or "none"), **the content of § 7** (each
    declared dependency the executor has to add, or "none"), the `## Compose services` row
    step 9 wrote,
    **the personal-data answer** (which fields cross, in what form, to which receiver — or
    "none"), **and, when the consumer is not in this project, whether its idempotency is
    contracted, assumed or unknown** — the last two are findings the person who asked for the
    feature has to see, not partial content to be read later,
    and what's missing for the folder to be complete (`20-persistence.md`,
    `40-tests.md`, and `35-jobs.md` under Form B). Don't invoke anyone else — under Form B
    `jobs-architect` runs next and reads § 2 and § 6; then `persistence-architect` reads § 6 in
    its first pass.

## What the partial contains

Ten blocks. An empty block is written as "none" — deleting it hides a question nobody
asked.

| Block | Fixes | Form exemplar |
|---|---|---|
| Topic and delivery | Topic name, partition key, serialization, delivery semantics, **and the AsyncAPI contract rows** — channel and message name, headers, the producer and consumer operations with their derived ids and descriptions, code-first or spec-first | `@.claude/rules/messaging.md` § Topics and serialization · § Contract documentation |
| Producer adapter | The port from `10-domain.md`, **the publication form (A or B) and why**, the adapter, the payload shape, and — Form B only — that the case needs the shared outbox plus the delivery guarantee its relay must honour | `KafkaProducerAdapter.java.example` (A) · `OutboxRelayPublisher.java.example` (B) |
| Consumer adapter and idempotency | The consuming use case, the listener, the dedupe key and table | `KafkaConsumerAdapter.java.example` |
| Retry and DLQ | Retry mode (derived, with the row that decided it), attempts and backoff, DLQ topic and its monitoring, NEW or REUSE of the shared error handling, and every exception the consumed use case raises with the handling the project-wide table gives it | `@.claude/rules/messaging.md` § Retry and DLQ |
| Configuration | Group id, offset reset, ack mode (derived — `BATCH` unless a consumed use case reaches another system), with the decided value and why | `application-kafka.yml.example` |
| Schema requirements | Every table this transport needs that the domain didn't model — the shared `outbox_events` under Form B (step 4a), the shared dedupe table (step 5a) — one row each, stating **which table and which guarantee**, never a column name and never DDL. The outbox's columns and pacing belong to `20-persistence.md`; a column named here becomes a divergence there. `none` when there are none | `@.claude/rules/messaging.md` § Publication timing · § Retry and DLQ |
| Declared dependencies | Build dependencies this transport needs and the project does not declare — the only list entitling the executor to touch `pom.xml`. The first Kafka case also lists `springwolf-kafka`, with no version: not managed by the Boot BOM, resolved at write time (`references/springwolf-reference.md`). `none` when there are none, and absence is not `none` | — |
| Personal data | Every payload field matching `@.claude/rules/logging.md` § Masking candidates, with the form chosen — full value, reduced, or a reference — and, for a full value, the receiver and the reason. That is the `Recorded decision` `@.claude/rules/personal-data.md` § In transit requires. `none` when the payload carries none, and absence is not `none` | `@.claude/rules/personal-data.md` § How to verify, grep 1 |
| Deferred | One row per item this partial decided **not** to do in this run: what was decided, what is missing, the norm that requires it (by path), and the intended owner — `checklist` or `backlog`. `none` when nothing was deferred, absence is not `none`. Consolidation resolves the owner and is what writes the `BACKLOG.md` line | — |
| Design patterns | Each pattern the producers or listeners adopt, with its force, its classes and the "When not" checked — step 7b. `none` when none | `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use |

The exemplars in `templates/` are **reference for form**, not files to copy. It's the
executor agent that reads them when generating code.

The mapper comes in two exemplars — the payload's `from` inside `KafkaProducerAdapter.java.example`, and `MessagingMapStructMapper.java.example` beside it — because the mechanism is the project's, not this partial's: the partial says what maps to what, and the executor writes it in the mechanism the root `CLAUDE.md`'s `**Mappers:` paragraph names (`@.claude/rules/mapping.md`).

## Contract

**Class:** design — the territory is `skill_classes.design` in
`@.claude/schemas/extensions.json` and `ArchHook.java guard` enforces it. Writes inside the
use case folder and nothing else: the broker service belongs to `docker-architect`, and a
write to the compose file is refused with exit 2.

**Reads** `docs/use-cases/UC-NNN-<slug>/00-use-case.md` and `10-domain.md` (mandatory —
stops without the second, or without its Events block naming external delivery),
`@.claude/rules/messaging.md`, `@.claude/rules/architecture-ddd.md` (Adapters section),
`@.claude/rules/naming.md`, `@.claude/rules/error-handling.md`, `@.claude/rules/lombok.md`,
the active blueprint's `packages.map`, and this skill's `references/springwolf-reference.md`.

**Writes** `docs/use-cases/UC-NNN-<slug>/25-messaging.md`. Nothing else.

**Does not write Java code.** The publisher, listener, and payload classes come from the
executor agent — the AsyncAPI annotations on them included; this skill only fixes the rows of § 1 they
are written from. It never writes or edits the committed snapshot: that file is the executor's, from
the document the project serves.

**Does not edit `docker-compose.yml`, and does not invoke `docker-architect` either.** When
step 9 finds no `kafka` service, it records the user's answer in the partial's
`## Compose services` (`@.claude/skills/docker-architect/references/compose-service-decision.md`),
and `/new-feature-implement` adds a `materialize` row after the code is green. The guard enforces both halves: the file is
outside this class's territory, and a `build`-class skill is unreachable from inside a design
run.

**Does not model the dedupe table, nor the outbox table.** When step 5a or step 4a finds
none, it names the need as a row of § 6 for `persistence-architect` to pick up — this skill
doesn't design schema. That block is the contract between the two: this skill runs **before**
`persistence-architect` in `/new-feature`, so § 6 is input to that skill's first pass, not a
correction to a partial already written. Form B's relay reads that state through the application-layer
`OutboxRelayGateway`, never through the persistence adapter's entity or repository
(`@.claude/rules/architecture-ddd.md` § Adapters).

**Owns the publication form** (after-commit vs. outbox + relay), from step 3's first axis.
`domain-modeling` records whether the event tolerates being lost — the `Durability` column of
`10-domain.md` § Events; this skill turns that property into a transport decision. A form
chosen upstream of the `Durability` column is a divergence to report, not to adopt silently.

**Does not decide** the use case boundary (`00-use-case.md`), whether an event exists or
its payload's business meaning (`10-domain.md`, `domain-modeling`'s call), the transport for
synchronous HTTP (`30-rest.md`), or the tests (`40-tests.md`). Doesn't touch
`.claude/rules/**`.

**Does not cover in-process Spring events** (`ApplicationEventPublisher`/`@EventListener`) —
see § Boundary with neighboring skills. No symptom for it yet in this repo.

**Does not collide with `domain-modeling`**: that one declares the event and the outbound
port, this one says how the port is served over Kafka. The event's payload meaning belongs to
the other; if it needs to change, report the divergence instead of rewriting it.
