---
name: new-feature
description: Orchestrates the feature design pipeline — one use case per run, the design skills → an approved UC-NNN-spec.md for the executor; `/new-feature-implement` implements it
disable-model-invocation: true
argument-hint: "<feature description> | UC-NNN-slug of a draft case | empty to list"
model: opus
---

# `/new-feature` — Feature design orchestrator

## Why this is Form 2 (manual skill)

Axis 2 (manual trigger) + axis 5 (procedural) + axis 8 (both). Form 1 rejected — user
requested manual invocation. Subagent rejected — none of the three reasons apply
(context, tools, model). A fixed-order procedure rules out a rule and CLAUDE.md.

**Manual only.** `disable-model-invocation: true` hides this skill from the model: the
`Skill` tool can't call it, and trying is blocked. When a conversation reaches the point
of running it, print the exact command for the user to type — don't attempt the call.

---

Pinned to `opus`: consolidating the partials and settling their divergences is design, and the executor it chains declares its own model (`@.claude/decisions/0081-skill-model-required-per-class.md`).

## Contract

**Class:** orchestrator — the territory is `skill_classes.orchestrator` in
`@.claude/schemas/extensions.json` and `ArchHook.java guard` enforces it. A run writes under
`docs/` only, and `ArchHook.java guard` also refuses a `Skill` call to a `build`-class skill
while this run is open: a design run does not materialize files, it records what is missing.

**Ownership:** Feature zero→spec orchestrator. Owns the sequence, the input table, the
spec lifecycle (`status:`), and the final output (`UC-NNN-spec.md`). Does **not** own the
use case number or slug — `use-case-design` does.

**Reads:**
- `pom.xml`, `.claude/forbidden-imports.txt`, and this project's domain package,
  discovered and never assumed — validates the generated project
- `docs/use-cases/UC-*/` — folder existence and each spec's `status:` line, by command
- `docs/use-cases/UC-NNN-<slug>/*.md` — the partials of the case being run

**Writes (indirectly via layer skills):**
- `docs/use-cases/UC-NNN-<slug>/00-use-case.md` and `docs/use-cases/BACKLOG.md` — via
  `use-case-design`
- `docs/use-cases/UC-NNN-<slug>/10-domain.md` — via `domain-modeling`
- `docs/use-cases/UC-NNN-<slug>/20-persistence.md` — via `persistence-architect`,
  migration SQL included as a code block, never as a file under `src/`
- `docs/use-cases/UC-NNN-<slug>/25-messaging.md` — via `messaging-architect`, only if
  `10-domain.md`'s Events block names external (Kafka) delivery
- `docs/use-cases/UC-NNN-<slug>/35-jobs.md` — via `jobs-architect`, only if
  `25-messaging.md` chose Form B or `00-use-case.md`'s trigger is a schedule
- `docs/use-cases/UC-NNN-<slug>/30-rest.md` — via `rest-api-architect`, unless `00-use-case.md`'s
  `Trigger` names `inbound GraphQL adapter` alone (step 3)
- `docs/use-cases/UC-NNN-<slug>/31-graphql.md` — via `graphql-api-architect`, only if the `Trigger`
  names `inbound GraphQL adapter` or `inbound REST and GraphQL adapters` (step 3g)
- `docs/use-cases/UC-NNN-<slug>/32-security.md` — via `security-architect`, only if
  `00-use-case.md`'s `Access` asks for something the project's filter chain does not
  already give (step 3b)
- `docs/use-cases/UC-NNN-<slug>/28-http-client.md` — via `http-client-architect`, only if
  `10-domain.md` § Ports declares a port of kind `external HTTP` (step 3c)
- `docs/use-cases/UC-NNN-<slug>/29-ai.md` — via `ai-architect`, only if `10-domain.md` § Ports
  declares a port of kind `LLM` or `vector store` (step 3d)
- `docs/use-cases/UC-NNN-<slug>/23-search.md` — via `search-architect`, only if
  `00-use-case.md`'s `Search index` row names a projection (step 3e)
- `docs/use-cases/UC-NNN-<slug>/22-cache.md` — via `cache-architect`, only if
  `00-use-case.md`'s `Freshness` row states a tolerance (step 5b)
- `docs/use-cases/UC-NNN-<slug>/40-tests.md` — via `test-architect`

**Writes outside `docs/`: none.** A run is docs-only, and that is enforced, not promised:
`ArchHook.java guard` refuses a `Skill` call to a `build`-class skill — `docker-architect`
included — while this orchestrator's phase is open, and refuses a write outside
`skill_classes.orchestrator`'s territory. A partial that needs a service the compose file
doesn't declare **asks** whether to add it, and records the answer in its `## Compose services`
(`persistence-architect` step 9, `messaging-architect` step 9); the consolidated spec carries
the list in `## Infrastructure`, and `/new-feature-implement` adds every `materialize` row
after the code is green — never this run. Why: a design run once hand-wrote a `schema-registry` block
into `docker-compose.yml`, with no template, no tag verification and no healthcheck
(`lessons-learned-012.md` §§ 4, 12, 13), and the review was of a spec nobody read that file
through. Record: `@.claude/decisions/0058-skill-classes-territory-schema.md`

**Writes (directly):**
- `docs/use-cases/UC-NNN-<slug>/UC-NNN-spec.md` — implementation plan (executor-ready),
  including its `status:` line (`draft` → `approved`)

**Never writes under `src/`.** Neither does any skill it chains. Every file under `src/`
— migrations included — belongs to `java-spring-boot-developer`, delegated by
`/new-feature-implement`, which also owns the one-time setup pre-flight
(`@.claude/skills/new-feature-implement/SKILL.md`).

**Never runs `git add`, `git commit`, or `git push`.** Neither does any skill it chains.
Git happens only through `git-publish`, behind its two confirmations, at the end steps
below. No end of this flow is left without an explicit git instruction.

**Integrates with (sequence ordered by depends-on):**
1. `use-case-design` — invoked for a new case; skipped on resume when `00-use-case.md` exists
2. `domain-modeling` — invoked if `10-domain.md` is missing (depends on 1)
3. `rest-api-architect` — invoked if `30-rest.md` is missing (depends on 2). Skipped when
   `00-use-case.md`'s `Trigger` names `inbound GraphQL adapter` alone
3g. `graphql-api-architect` — invoked if the `Trigger` names `inbound GraphQL adapter` or
   `inbound REST and GraphQL adapters` and `31-graphql.md` is missing (depends on 1, 2; reads 3 when
   present). Skipped when the case has no GraphQL trigger
3b. `security-architect` — invoked per step 3b's table when `32-security.md` is missing
   (depends on 1, 2, 3). Skipped when `Access` is public in a project with no filter chain, or
   authenticated in one whose chain already denies by default
3c. `http-client-architect` — invoked if `10-domain.md` § Ports declares a port of kind
   `external HTTP` and `28-http-client.md` is missing (depends on 1, 2; reads 3 and 3b when
   present). Skipped when the case calls no other system over HTTP
3d. `ai-architect` — invoked if `10-domain.md` § Ports declares a port of kind `LLM` or
   `vector store` and `29-ai.md` is missing (depends on 1, 2; reads 3, 3b and 3c when present).
   Skipped when the case asks no model and searches no store
3e. `search-architect` — invoked if `00-use-case.md`'s `Search index` row names a projection and
   `23-search.md` is missing (depends on 1, 2). Skipped when the row reads `none`, or the case
   predates it
4. `messaging-architect` — invoked if `10-domain.md`'s Events block names external
   (Kafka) delivery and `25-messaging.md` is missing (depends on 2). Skipped entirely
   when the event, if any, stays in-process — not every use case needs it
5. `jobs-architect` — invoked if `25-messaging.md` chose Form B, the trigger is a
   schedule, `28-http-client.md` § 10 asks for a reconciliation pass, or `29-ai.md` § 9 asks
   for an ingestion or re-index job, or `23-search.md` § 8 asks for a rebuild job, or the `Audit`
   row names `history` with no history prune job in the project yet, and `35-jobs.md`
   is missing (depends on 1, 3c, 3d, 3e, 4).
   Skipped otherwise
6. `persistence-architect` — invoked if `20-persistence.md` is missing (depends on 2, 3, 3b, 3c, 3d, 3e, 4, 5)
6b. `cache-architect` — invoked if `00-use-case.md`'s `Freshness` row states a tolerance and
   `22-cache.md` is missing (depends on 1, 2, 6; reads 3c, 3e and 5 when present). Skipped when the
   row reads `none` — every case that only writes, and every read that must see the last write
7. `test-architect` — invoked if `40-tests.md` is missing (depends on 2,3,3b,3c,3d,3e,4,5,6,6b)

**Why REST and messaging both run before persistence.** The order follows who generates
requirements for whom. REST generates schema requirements — `Idempotency-Key` on a
creation `POST` needs the shared key table — and persistence generates none for REST.
With persistence first, the table was discovered after the partial was written, and
persistence ran twice.

Messaging is the same shape and was learned the same way: a transactional outbox needs the
shared `outbox_events` table, a consumer needs the shared dedupe table, and neither is
visible from the domain partial alone. With messaging after persistence, `20-persistence.md` was
written without the relay's retry columns and its partial index, and persistence ran twice
again. Messaging depends only on step 2, so running it before persistence costs nothing —
and persistence then reads both requirement lists, `30-rest.md` block 4 and
`25-messaging.md` § 6, in its first pass.

Jobs sits between them for the same reason. The scheduling technology it picks brings tables
(`shedlock`, `QRTZ_*`, `BATCH_*`), the relay's claim depends on how many instances run the
pass, and the prune job needs a bounded delete — three schema facts invisible to persistence
until `35-jobs.md` § 3 and § 6 exist. Jobs itself needs only the use case and messaging's
publication form, so it costs nothing to run first
(`@.claude/decisions/0087-jobs-architect-skill.md`).

GraphQL runs right after REST and before security, the REST step's pair. Both shape the same input
ports, and when the trigger names both adapters the GraphQL partial reads the REST one, so each
operation names its counterpart. It generates requirements for the steps after it: a batch port the
domain did not declare, the batch statement and an index for persistence, and an access row per
root field and per sensitive field for security — none visible before `31-graphql.md` § 9 exists
(`@.claude/decisions/0146-graphql-api-architect-skill.md`).

Security runs right after REST and GraphQL, for the same two reasons in opposite directions. It needs the
endpoints `30-rest.md` fixed — access rules written before them protect a guess — and it can
generate schema requirements: users owned by the application need a credentials store, an
API key needs a key store, both invisible to persistence until `32-security.md` § 7 exists.
Ownership is not one of them: it is an invariant `domain-modeling` already modeled from the
`Access` row (`@.claude/decisions/0112-security-architect-skill.md`).

The HTTP client runs right after security and before messaging, for the same reason in one
direction: it generates requirements for the steps after it. A non-idempotent write to another
system needs its idempotency key persisted with the operation, and an unknown outcome needs a
reconciliation pass — a column persistence cannot see and a job scheduling cannot see until
`28-http-client.md` § 10 exists. It reads the trigger's deadline from `30-rest.md` and whether a
filter chain exists from `32-security.md`, so it waits for both
(`@.claude/decisions/0121-http-client-architect-skill.md`).

The AI ports run right after the HTTP client and before messaging, for the same reason: a vector
store needs its table and extensions created by a migration, and the records it mirrors need a
re-index on every change and a first fill — a schema fact for persistence and a trigger for
messaging or jobs, invisible to all three until `29-ai.md` § 9 exists. It reads the trigger's
deadline from `30-rest.md`, so it waits for REST, and it needs nothing messaging, jobs or
persistence decide (`@.claude/decisions/0145-ai-architect-skill.md`).

The search projection runs right after the AI ports, before messaging, for the same reason: an
index is fed by the source's change events, rebuilt by a job and keyed on the source's version —
a consumer for messaging, a rebuild for jobs, a version field and an outbox event for persistence,
invisible to all three until `23-search.md` § 8 exists. Whether the case has a search index, and on
which engine, is `00-use-case.md`'s row; this orchestrator never decides it
(`@.claude/decisions/0147-document-storage-and-search-architect.md`).

The cache runs after persistence, the one step here that generates no requirement for anyone
before it: a cache adds no table and no column. It wraps an outbound port, so it waits for the
adapters behind it — `20-persistence.md`'s query and `28-http-client.md`'s call — and it
lists every writer of the data it holds, which only the finished partials name. Tests run
after it, because a cached read owes three tests no other layer asks for
(`@.claude/decisions/0144-cache-architect-skill.md`).

**Design order isn't implementation order.** GraphQL is block 4.1, implemented by the conditional
Block G right after Block 3 and before Block S — its resolvers call the same ports as the REST
controllers, and Block S's annotations go on both. Messaging is designed fourth and implemented
sixth: `UC-NNN-spec.md` keeps messaging as block 6, and the executor's conditional Block M
still runs between REST and Tests. Jobs is block 7, implemented by the conditional Block J
right after Block M — a trigger compiles against the inbound port it calls, so it comes last
among the production blocks. Outbound HTTP is block 3.3, implemented by the conditional Block H
right after Block 2 — an adapter compiles against the outbound port and the domain types, and
nothing upstream compiles against it. AI is block 3.7, implemented by the conditional Block A
right after Block H, for the same reason. Security is block 4.5, implemented by the conditional Block S
right after Block 3 — its annotations and the actor resolution go on the controllers Block 3
just wrote. Cache is block 3.4, implemented by the conditional Block C last among the production
blocks, after Block J — a decorator compiles against the port and needs its delegate, and every
writer that must go through it already exists. The pipeline orders by who needs whose requirements;
the spec orders by what compiles against what.
8. `git-publish` — invoked at § Approval, per § End of flow, to commit the approved spec

The executor, `java-spring-boot-developer`, is not a step of this skill: `/new-feature-implement`
delegates to it over an `approved` spec, in a clean session.

`gof-design-patterns` is not a pipeline step, and this orchestrator never invokes it — a
design run cannot reach a `build`-class skill. **Its catalog is still applied at design
time:** each design skill above runs its § Design-time use for its own layer and writes a
`## Design patterns` section into its partial, so the classes a pattern creates are in the
spec the user approves, not chosen by the executor afterwards. The executor implements
those rows, and applies the catalog on its own only for a symptom already on disk
(`@.claude/decisions/0089-design-patterns-decided-at-design-time.md`, superseding the
executor-side trigger of 0077).

---

## Spec lifecycle

`UC-NNN-spec.md` opens with a frontmatter carrying one field:

| `status:` | Written by | When |
|---|---|---|
| `draft` | this skill | at consolidation |
| `approved` | this skill | only after the user's explicit approval, § End of flow |
| `implemented` | `java-spring-boot-developer` | with a green build |
| `implemented-blocked` | `java-spring-boot-developer` | with a green build, when the run left an approved use case unreachable end to end — the code is on disk and verified, and a `Satisfied by` the spec named is not there yet |

A use case folder is **open** when it has no `UC-NNN-spec.md` yet, or its spec is `draft`.
`implemented-blocked` is **not** open: a case whose code is on disk, green and committed is not
work in progress, and its satisfier is usually a backlog row nobody is holding this run for.

**One `/new-feature` produces one use case.** The next one only starts once the previous
is `approved`, `implemented` or `implemented-blocked`.

**An approved spec is immutable.** Later cases read approved specs as a read-only
contract and reuse the aggregate already modeled. A change a new case needs in an
approved one goes into the `## Impact on approved use cases` section of the **new**
spec; the executor applies it in code. Don't edit the old spec — write the line in the
altered case's own `CHANGELOG.md` instead (consolidation step 2).

**A case can be nothing but changes.** Every component `CHANGE`, no new use-case class:
it still gets its own `UC-NNN`, and its slug names the capability added rather than the
trigger, which already belongs to the case being changed
(`@.claude/rules/naming.md` § Use case identifier).

Decide what the current case needs. Don't defer or anticipate a decision "for the future
case" — the future case decides it, in its own impact section.

---

## Entry guardrail

Runs before any skill invocation, any write, and any question. Every check is a command;
the model doesn't interpret the input. **Read `references/entry-guardrail.md` first** — the
survey and classification commands, the error rule, and §§ 2–4 (worktree, project, disk) live
there, shared with `/new-feature-implement`. This section holds only what is this skill's own:
the history check and the input table.

### 1 · Input table — closed

Run the survey of `references/entry-guardrail.md` § 1.

**The disk is not the history.** A folder deleted from the working tree is invisible to
`find` and still in `HEAD`, so the next number looks free when it isn't:

```bash
git ls-tree -d --name-only HEAD docs/use-cases 2>/dev/null
```

A `UC-NNN` that `HEAD` has and the disk doesn't → **stop and report it**, before any
skill call. Two things can be true, and only the user knows which: the number was
recycled (the repository would end up with two different `UC-NNN`, and this run's commit
would delete one while adding the other), or approved work was deleted without being
committed. Name the folder, say which of the two it looks like, and ask. Don't infer the
next free number from the disk alone.

Same comparison for the backlog, and for the same reason — the entry of a deleted case
disappears with its folder, and a run that recreates it from scratch writes different
text nobody compares:

```bash
git diff --stat HEAD -- docs/use-cases/BACKLOG.md 2>/dev/null
```

Non-empty when a `UC-NNN` is missing from the disk → show the diff before
`use-case-design` writes a new entry.

Classify the argument with the commands of `references/entry-guardrail.md` § 1, then
evaluate in order and **stop at the first row that matches**:

| # | Input | Result |
|---|---|---|
| 1 | empty | ✅ list the survey above — each case with its `status` — and stop |
| 2 | `EXACT`, `FOLDER`, status `draft` or `(no spec)` | ✅ resume: skip `use-case-design`, generate only the missing partials, then consolidation |
| 3 | `EXACT`, `FOLDER`, status `approved` | ❌ `<UC-NNN-slug> is approved — implement it in a clean session` — plus the two lines `/clear` and `/new-feature-implement <UC-NNN-slug>`. This skill designs; it cannot forward, since `/new-feature-implement` is manual |
| 4 | `EXACT`, `FOLDER`, status `implemented` or `implemented-blocked` | ❌ `already implemented — describe the change as a new feature` |
| 5 | no `FOLDER`, and the argument's `UC-NNN` resolves to **exactly one** folder on disk | ❌ `<UC-NNN> is <real-slug>, status <status>` — plus the exact command for it: `/new-feature <real-slug>` for an open case, `/new-feature-implement <real-slug>` for an approved one. The case exists; the argument named it wrongly |
| 6 | `EXACT`, no `FOLDER`, number resolving to zero or several folders | ❌ `use case not found; to create one, describe the feature` |
| 7 | `UC_LIKE` but not `EXACT` (slug plus context, malformed slug, two slugs, a path) | ❌ `ambiguous argument` |
| 8 | free text, and the survey shows an open case | ❌ `<UC folder> is open — resume or approve it first` |
| 9 | free text, and no open case | ✅ new: pass the description **as is** to `use-case-design` |
| — | anything else | ❌ `unrecognized argument` |

Row 3 used to implement on the same argument; it is an error row since the implement flow
became its own skill, and it points there instead of guessing
(`@.claude/decisions/0135-new-feature-split-spec-and-implement.md`). A user typing the old
command loses one line, not a run.

Row 5 is the near miss, and it is an **error row, not a success one**: it reports and stops.
`/new-feature UC-003-spec` once answered `use case not found` while
`docs/use-cases/UC-003-initiate-kyc-verification/` sat on disk — literally true, since no folder
carries that name, and practically wrong, since the argument was the basename of the spec file
inside that folder (lessons-learned-014 § 12). The answer names the real slug and the status, so
the next attempt is one line away. It does **not** resolve the argument and carry on: the
argument was wrong, and guessing which case was meant is exactly what the guardrail forbids.

```text
❌ /new-feature: <reason>.
Usage: /new-feature <feature description>   → new use case
       /new-feature UC-NNN-slug              → resume a draft case
       /new-feature                          → list
       /new-feature-implement UC-NNN-slug    → implement an approved case
```

Row 5 keeps that shape and adds the one line that makes it actionable:

```text
❌ /new-feature: UC-003 is UC-003-initiate-kyc-verification, status approved.
Did you mean: /new-feature-implement UC-003-initiate-kyc-verification
Usage: …
```

### 2 · Worktree, project, disk

`references/entry-guardrail.md` §§ 2–4, in that order, before any question or write.
`IGNORED` and the list of pre-existing changes travel to `git-publish` at § Approval.

---

## Procedure — 6 steps + consolidation

**Execution discipline** — the run's cost is turns × context size, not file size:

- **No progress messages** between steps or tools ("moving to step 3", "domain ok"). Each
  one is a turn that re-reads the whole conversation. The only report is § Final report.
- **Independent writes in one turn** — parallel tool calls, not one file per turn.
- **Dependency versions come from the build file.** Read `pom.xml` before resolving any
  version; no web search for a version the project already declares.
- A step's "Output" below is a check the run makes, not a message it prints.

### Step 1: Use case (new case only)

**Invoke** `use-case-design` via the Skill tool, with the user's description as is.

`use-case-design` owns the boundary, the number, and the slug. When the description
holds several use cases, it asks the user which one to design, designs that one, and
writes the rest to `docs/use-cases/BACKLOG.md`. This run continues with the one it
created — never with the others.

**Output:** `docs/use-cases/UC-NNN-<slug>/00-use-case.md` — its folder name is the
`UC-NNN-<slug>` every later step uses.

### Short path — checked right after step 1

A trivial case doesn't need five partials. Check all nine against `00-use-case.md`
and the approved specs:

| Criterion | Unmet when |
|---|---|
| Aggregate reused from an approved spec | the component table has a NEW aggregate or value object |
| No new table, column, or migration | the component table has a NEW or CHANGE migration or entity |
| No new exception | an error situation has no exception already named in an approved spec |
| No question asked to the user | `use-case-design` needed `AskUserQuestion` |
| No freshness tolerance | the `Freshness` row states a duration — a cache to design |
| No model and no semantic search | the case asks a model to classify, extract or moderate, or finds items by meaning — an AI port to design |
| No GraphQL operation | the `Trigger` names a GraphQL adapter — the short template has no GraphQL row |
| No search projection, no new document | the `Search index` row names a projection, or a `document (MongoDB)` aggregate gets a NEW or CHANGE document, collection or index — the short template has no row for either |
| No new audit level | the `Audit` row names `stamps` or `history` for an aggregate whose level is new or changes — stamps, history tables and the actor to design; the short template has no row for them |

All nine met → skip steps 2–6 and write `UC-NNN-spec.md` from
`templates/feature-spec-short.md.example`: every row names its source, an approved spec or
a rule. A row that needs judgment to fill means the case isn't trivial — discard the
short spec and take steps 2–6. One criterion unmet → steps 2–6.

### Step 2: Domain (depends on 1)

If `10-domain.md` is missing: **invoke** `/domain-modeling UC-NNN`.
If it exists: read, validate (four blocks: aggregate, VOs, invariants, ports).

**Output:** "✅ Domain ready" or a list of gaps.

### Step 3: REST (depends on 1,2)

Read the closing phrase of `00-use-case.md`'s `Trigger` row. `inbound GraphQL adapter` alone →
skip this step. Any other phrase, or none (a case written before the phrase existed) → if
`30-rest.md` is missing: **invoke** `/rest-api-architect UC-NNN`.
If it exists: read, validate (eight blocks: resources, DTOs, errors, pagination, idempotency,
personal data, versioning, admission — `none` unless `00-use-case.md` has an `Admission` row).

**Output:** "✅ REST ready", "— skipped (GraphQL only)", or gaps.

### Step 3g: GraphQL (depends on 1, 2, conditional)

If the `Trigger` names `inbound GraphQL adapter` or `inbound REST and GraphQL adapters` and
`31-graphql.md` is missing: **invoke** `/graphql-api-architect UC-NNN`. No GraphQL adapter in the
phrase → skip this step. If `31-graphql.md` exists: read, validate (thirteen blocks: operations,
schema, inputs and payloads, pagination, batch loads, project setup, error map, personal data,
requirements to other partials, contract test cases, declared dependencies, configuration,
deferred).

Every list that grows is a connection with a ceiling, every child field that costs I/O is a batch
load, and the project setup is decided or inherited — a § 6 with neither is a gap. § 9 is what steps
2 (a batch port, through consolidation), 3b and 5 read; § 11 is the only list that entitles the
executor to add the GraphQL starter to `pom.xml`; § 10 is what step 6 turns into tests.

**Output:** "✅ GraphQL ready", "— skipped (no GraphQL trigger)", or gaps.

### Step 3b: Security (depends on 1, 2, 3, 3g, conditional)

Read `00-use-case.md`'s `Access` row, and whether the project already has a filter chain
(`grep -rl "SecurityFilterChain" --include='*.java' src/main`). If `32-security.md` is missing,
**invoke** `/security-architect UC-NNN` when any holds:

| `Access` | Filter chain on disk | Why it runs |
|---|---|---|
| a role, a group, a scope, or the owner | any | this case's rules — and the setup when there is none |
| authenticated | none | first secured case: the project-wide setup |
| public | present | a `permitAll` needs its recorded reason |

Otherwise skip: public in an unsecured project, or authenticated behind a chain that already
denies by default — the spec's security block says which. A GraphQL trigger is not a skip when
`31-graphql.md` § 9 asks for a field-level row: a sensitive field narrower than its operation is
this case's rule whatever the `Access` row says. An `00-use-case.md` with an HTTP
trigger and no `Access` row (written before the row existed) is not a skip: invoke it, it asks.
If `32-security.md` exists: read, validate (eleven blocks: access per endpoint, mechanism,
authorities, project-wide setup, ownership, failure responses, schema requirements, declared
dependencies, configuration, contract test cases, deferred).

§ 7 is what step 5 reads; § 8 is the only list that entitles the executor to add a security
starter to `pom.xml`; § 10 is what step 6 turns into tests.

**Output:** "✅ Security ready", "— skipped (<which row>)", or gaps.

### Step 3c: Outbound HTTP (depends on 1, 2, conditional)

Read `10-domain.md` § Ports. If it declares a port of kind `external HTTP` and
`28-http-client.md` is missing: **invoke** `/http-client-architect UC-NNN`. No such port → skip
this step. An output port with **no kind** is not a skip: stop and ask `domain-modeling` for it —
a kind left out is how an external call reaches the executor with nobody having decided its
timeout. A port of that kind whose `00-use-case.md` has no `External calls` row (written
before the row existed) is not a skip either: invoke it, it asks. If `28-http-client.md` exists:
read, validate (eleven blocks: operations, client, engine and pool, outbound authentication,
retry and resilience, project-wide setup, configuration, declared dependencies, contract test
cases, requirements to other partials, deferred).

§ 10 is what steps 4b and 5 read — the stored idempotency key, a reconciliation pass, the
security impact of the OAuth2 client starter; § 8 is the only list that entitles the executor to
add a client, engine or resilience dependency to `pom.xml`; § 9 is what step 6 turns into tests.

**Output:** "✅ Outbound HTTP ready", "— skipped (no external HTTP port)", or gaps.

### Step 3d: AI (depends on 1, 2, conditional)

Read `10-domain.md` § Ports. If it declares a port of kind `LLM` or `vector store` and
`29-ai.md` is missing: **invoke** `/ai-architect UC-NNN`. No such port → skip this step. A port
of kind `LLM` whose return type has no "could not decide" value, or no review state it leads to,
is not a skip: stop and ask `domain-modeling` for it — the adapter would have nowhere to put an
answer it cannot use. If `29-ai.md` exists: read, validate (twelve blocks: AI ports, provider and
models, prompts and output, data sent, vector store, failure and retry, observability, test
cases, requirements to other partials, declared dependencies, configuration, deferred).

Every timeout in § 6 is below the trigger's deadline, and every field of § 4 sent in clear names
its receiver. § 9 is what steps 4, 4b and 5 read — the store's migration, a re-index trigger, an
ingestion job; § 10 is the only list that entitles the executor to add a Spring AI dependency to
`pom.xml`; § 8 is what step 6 turns into tests.

**Output:** "✅ AI ready", "— skipped (no AI port)", or gaps.

### Step 3e: Search (depends on 1, 2, conditional)

Read `00-use-case.md`'s `Search index` row. If it names a projection and its engine and
`23-search.md` is missing: **invoke** `/search-architect UC-NNN`. `none`, or a spec older than the
row → skip this step. A row that names a projection but no engine is not a skip: stop and send the
case back to `use-case-design`, which asks the one factual question — this orchestrator never picks
an engine. If `23-search.md` exists: read, validate (eleven blocks: projection, index, queries,
writes, rebuild, lag, failure, requirements to other partials, declared dependencies,
configuration, deferred).

§ 6's lag is at most the case's `Freshness`; a larger one is a divergence, not a refresh to add.
§ 8 is what steps 4, 4b and 5 read — the indexer's consumer, the rebuild job, the source's version
and change event; § 9 is the only list that entitles the executor to add a search dependency to
`pom.xml`; § 3 and § 4 are what step 6 turns into tests.

**Output:** "✅ Search ready", "— skipped (no search index)", or gaps.

### Step 4: Messaging (depends on 2, conditional)

Read `10-domain.md`'s Events block. If it names external (Kafka) delivery for the
event and `25-messaging.md` is missing: **invoke** `/messaging-architect UC-NNN`. If
the event is absent or stays in-process, skip this step — not every use case needs it.
If `25-messaging.md` exists: read, validate (nine blocks: topic and delivery, producer,
consumer and idempotency, retry/DLQ, configuration, schema requirements, declared
dependencies, personal data, deferred).

A missing § 6 is a gap, not an omission: it's the list step 5 reads. `none` is a valid
value there and means publication Form A with no consumer dedupe table to build. § 7 is
the same shape for build dependencies: it is the only list the executor may act on when it
writes `pom.xml`, so a missing one leaves a needed dependency with no owner
(lessons-learned-013 § 10). **This step is not the only check on it** — a run that reaches
consolidation without taking this step is exactly how two lists went missing and a spec was
approved anyway, so consolidation gates the same thing for every path.

**Output:** "✅ Messaging ready", "— skipped (no external delivery)", or gaps.

### Step 4b: Jobs (depends on 1, 3d, 3e, 4, conditional)

Invoke `/jobs-architect UC-NNN` if `35-jobs.md` is missing and at least one holds:
`25-messaging.md` § 2 chose **Form B**, `00-use-case.md`'s trigger is a schedule, a
recurring run, a batch or a background job, `28-http-client.md` § 10 asks for a reconciliation
pass, `29-ai.md` § 9 asks for an ingestion or re-index job, `23-search.md` § 8 asks for a rebuild job, `00-use-case.md`'s `Audit` row names `history` and the project has no history prune job yet, or a partial's `Deferred` block names a scheduled job. None holds → skip this step. If `35-jobs.md` exists: read, validate (nine blocks: jobs,
technology, coordination, execution guarantees, observability, schema requirements, declared
dependencies, configuration, deferred).

A Form B case with no `35-jobs.md` is a gap, not a skip: the relay would have no schedule and
the outbox no prune — the exact state lessons-learned-014 § 9 found. § 3's replica count and
§ 6's requirements are what step 5 reads; § 7 is the only list that entitles the executor to
add a scheduling dependency to `pom.xml`.

**Output:** "✅ Jobs ready", "— skipped (no scheduled work)", or gaps.

### Step 5: Persistence (depends on 1,2,3,3g,3b,3c,3d,3e,4,4b)

If `20-persistence.md` is missing: **invoke** `/persistence-architect UC-NNN`. It reads
every schema requirement list in the same pass — `30-rest.md` block 4 (the idempotency
table among them) when step 3 ran, when step 3g ran `31-graphql.md` § 9 (one statement per batch
port, bounded by § 6's max batch, and the index each connection's order needs), when step 3b ran `32-security.md` § 7 (a credentials or API-key store),
when step 3c ran `28-http-client.md` § 10 (a stored idempotency key, an unknown-outcome state),
when step 3d ran `29-ai.md` § 9 (a vector store's table, its extensions and its index),
when step 3e ran `23-search.md` § 8 (the source's version and its change event in the outbox),
when step 4 ran `25-messaging.md` § 6 (the shared outbox table, the
dedupe table), and when step 4b ran `35-jobs.md` § 3 and § 6 (the replica count its claim
strategy must meet, the scheduling tables, the prune's bounded delete). If it exists: read, validate (seven blocks: schema, mapping, adapter and
ports, migrations, configuration, declared dependencies, deferred). § 6 is the persistence twin
of `25-messaging.md` § 7,
and the same rule holds: it is the only list that entitles the executor to touch `pom.xml` —
and consolidation checks it again, for the paths that never take this step.

**Output:** "✅ Persistence ready" or gaps.

### Step 5b: Cache (depends on 1, 2, 5, conditional)

Invoke `/cache-architect UC-NNN` if `22-cache.md` is missing and `00-use-case.md`'s
`Freshness` row states a tolerance — a duration an answer may be old. The row reads `none`, or
the case predates the row → skip this step: no tolerance, no cache
(`@.claude/rules/caching.md` § Boundary). If `22-cache.md` exists: read, validate (ten blocks:
cached reads, provider, expiry and size, invalidation, failure and load, serialization,
observability, declared dependencies, configuration, deferred).

Every expiry in § 3 is at most the tolerance it serves — minus `23-search.md` § 6's lag when the
cached read is a search projection — and every writer of the cached data
has a § 4 row — a writer named in another approved case's Components table and missing from
§ 4 is a gap. § 8 is the only list that entitles the executor to add a cache dependency to
`pom.xml`; § 1 and § 4 are what step 6 turns into tests.

**Output:** "✅ Cache ready", "— skipped (no freshness tolerance)", or gaps.

### Step 6: Tests (depends on 1,2,3,3g,3b,3c,3d,3e,4,5,5b)

If `40-tests.md` is missing: **invoke** `/test-architect UC-NNN` (design mode).
If it exists: read, validate (five blocks: pyramid, cases, fixtures, coverage, test dependencies).
When step 3b ran, every case of `32-security.md` § 10 has a test row — a missing one is a gap.
When step 3g ran, every case of `31-graphql.md` § 10 has a test row at the level it names, and the
schema snapshot test exists — a missing one is a gap, and so is an access case placed in the
GraphQL slice, where no filter chain runs.
When step 3c ran, every case of `28-http-client.md` § 9 has a test row — a missing one is a gap.
When step 3d ran, every case of `29-ai.md` § 8 has a test row at the level it names — a missing
one is a gap, and so is any row that calls a real model.
When step 5b ran, every cached read of `22-cache.md` § 1 has three test rows — a second read
not reaching the source, an eviction by every writer of § 4 that goes through the port, and
two callers never sharing an entry when the key names the caller (`@.claude/rules/caching.md`
§ Tests). A missing one is a gap.

**Output:** "✅ Tests ready" or gaps.

### Consolidation (after 1,2,5,6 ✅, and 3 or 3g — steps 3, 3g, 3b, 3c, 3d, 3e, 4, 4b and 5b conditional)

If all specs that apply exist and validate (REST only when step 3 wasn't skipped, GraphQL only when
step 3g wasn't, security only when step 3b wasn't skipped,
outbound HTTP only when step 3c wasn't, AI only when step 3d wasn't, search only when step 3e wasn't, messaging only when step 4 wasn't, jobs only when step
4b wasn't, cache only when step 5b wasn't):

1. **Resolve divergences before consolidating.** The partials are written by different
   skills, and downstream corrects upstream: `30-rest.md` fixes the path and status
   that `00-use-case.md` had sketched, `20-persistence.md` fixes the key that the
   domain described in prose. Stacking both versions and explaining in a note which one
   wins pushes the work onto the reader — and the note ends up two hundred lines away
   from where it matters.

   Walk through every partial in the folder and, for each fact that appears in more than one with
   different values, apply this precedence:

   | Fact | Who wins |
   |---|---|
   | HTTP path, verb, status, body shape | `30-rest.md` — except the 401 and 403 rows, below |
   | GraphQL root fields and the port each calls, types, fields and nullability, inputs, payloads and `userErrors`, connections and their ceilings, batch loads, the GraphQL error map, the project's GraphQL limits | `31-graphql.md` — except who may read each field, below. A batch port it asked for becomes `10-domain.md`'s port by consolidation, with `31-graphql.md` as who asked; the batch statement and its index are `20-persistence.md`'s |
   | Who may call each endpoint, GraphQL root field and sensitive field, the authentication mechanism, the claims-to-authorities mapping, the `permitAll` list and its reasons, the 401 and 403 rows, CORS, OpenAPI and Actuator exposure, where the controller reads the actor from | `32-security.md`. The actor field, the owner field and the ownership invariant stay `10-domain.md`'s; an owner-only `Access` whose domain partial has no actor is not settled by precedence: **stop and ask** |
   | Table, column, key, index, migration | `20-persistence.md` — including every table or column another partial *asked for*: the requirement is born in `30-rest.md` block 4 or `25-messaging.md` § 6, the final form (name, type, nullability, index, migration) is always this one's |
   | Topic, serialization, delivery guarantee, consumer retry and DLQ | `25-messaging.md` |
   | Outbox table, its columns, the claim query, and the values the columns encode (batch size, backoff, attempt ceiling, retention window, the prune's statement) | `20-persistence.md` — the whole table is its territory. `25-messaging.md` declares the **guarantee** those values have to deliver, never the columns; a § 6 row naming columns is reported as a divergence and the guarantee is what carries over |
   | Client, engine and pool, timeouts, the retrying layer and its policy, breaker and bulkhead, outbound authentication, the failure table of each remote operation | `28-http-client.md`. The outbound port, its domain types, the idempotency key field and the unknown-outcome state stay `10-domain.md`'s; the column and the reconciliation schedule are persistence's and jobs's, as for every requirement |
   | Scheduling technology, a job's trigger and cadence (the relay's poll interval included), coordination across instances and the replica count, overlap and missed-run policy, on/off property, job metrics, the prune job | `35-jobs.md`. A claim strategy in `20-persistence.md` that does not meet `35-jobs.md` § 3's replica count is not settled by precedence — it is a guarantee dropped by a shape decision: **stop and ask** |
   | Provider and model of each AI port, its prompt resources and answer type, what each unusable answer becomes, the fields sent to the provider, the store and its embedding model, the timeout and retrying layer of each AI port | `29-ai.md`. The port, its "could not decide" value and the review state stay `10-domain.md`'s; a timeout above the trigger's deadline, or a personal-data field sent in clear without a named receiver, is not settled by precedence: **stop and ask** |
   | The search document and its mapping, the index version and alias, the query and its cursor, the indexer's write rules, the rebuild's alias swap, the lag the projection consumes, the search dependency | `23-search.md`. Whether the case has a search index, its engine and the freshness tolerance stay `00-use-case.md`'s; a lag larger than the tolerance is not settled by precedence: **stop and ask** |
   | Storage family of each aggregate | `00-use-case.md` — never a design partial, and never this orchestrator. An aggregate the code already stores in the other family is not settled by precedence: **stop and ask** |
   | Audit level of each aggregate | `00-use-case.md` — never a design partial. An aggregate the code already audits at a higher level than the row asks is not settled by precedence (a history cannot be switched off without losing it): **stop and ask** |
   | Which reads are cached, each cache key, the cache provider, expiry and size per cache, the writers that must evict, cache serialization and metrics | `22-cache.md`. The freshness tolerance stays `00-use-case.md`'s; an expiry longer than it is not settled by precedence — it serves answers older than the business allowed: **stop and ask** |
   | Aggregate name, value object, port, event | `10-domain.md` |
   | Exception class and `errorCode` | `10-domain.md` |
   | Use case boundary, invariants, error situations | `00-use-case.md` |
   | Name and level of each test | `40-tests.md` |
   | A design pattern and the classes it creates | The partial of the layer those classes live in. Two partials adopting different patterns for the same class is not settled by precedence: **stop and ask** |

   `UC-NNN-spec.md` carries **a single value per fact** — the winner — across all
   blocks, including those that had inherited the old value. The discarded versions go
   into a `## Resolved divergences` section at the end, one line each: fact, discarded
   value, adopted value, partial that decided. The executor reads one truth; the audit
   trail is still there.

   A divergence the table doesn't resolve — two facts from the same owner, or a
   business-rule contradiction — **stops the pipeline** and asks. Don't invent it or
   stack it.

   **A downstream partial never edits an upstream one's fact — it asks for it.** A requirement
   born downstream and landing upstream — `20-persistence.md` bounding the producer's send
   time so the outbox lease outlives any send, a value `25-messaging.md` owns — travels as a
   named requirement in the downstream partial, and this step resolves it like any other
   divergence: the owner's block in `UC-NNN-spec.md` carries the new value, and
   `## Resolved divergences` records who asked. Carried silently into the owner's block, it is
   a fact with two authors and no record of the second.

   **And one shape the table resolves only in appearance:** a column decision that changes
   behaviour. `20-persistence.md` wins on the column, always — but when dropping a column
   also drops a guarantee `25-messaging.md` declared (no `next_attempt_at`, so per-row
   exponential backoff becomes a fixed repoll), the winner is not the answer. That is a
   divergence the table doesn't resolve: **stop and ask**, and record which guarantee the
   chosen shape delivers. A precedence rule written for table shape must never be what
   settles a behaviour.

2. Consolidate into a single file: `UC-NNN-spec.md`, with `status: draft`, **by reference**
   - Each block holds only the final decisions — one value per fact — and the path of the
     partial that details it. Never copy a partial's tables, SQL, or code: a copied
     consolidation doubled the output of a real run and added nothing the partial lacked
   - Structure: 5 blocks (use case, domain, persistence, REST, tests) — `## 4 REST` reads
     `none — GraphQL only` when step 3 was skipped — plus `## 4.1 GraphQL` only when step 3g ran,
     `none` otherwise, plus a 6th
     (messaging) only when step 4 wasn't skipped, a 7th (jobs) only when step 4b wasn't, and
     the security block (`## 4.5 Security`) only when step 3b wasn't — when it was, that block
     reads `none` with the skip row of step 3b, so "covered by deny-by-default" is a recorded
     fact and not a missing block
   - The outbound HTTP block (`## 3.3 Outbound HTTP`) only when step 3c ran; `none` otherwise
   - The cache block (`## 3.4 Cache`) only when step 5b ran; `none` otherwise
   - The AI block (`## 3.7 AI`) only when step 3d ran; `none` otherwise
   - The search block (`## 3.8 Search`) only when step 3e ran; `none` otherwise
   - `## Impact on approved use cases`: every row from the same section of each partial —
     "none" when all are empty
   - `## Design patterns`: every row from the same section of each partial, with the partial
     that decided it — "none" when all are empty. **A partial that applies must carry the
     section, or consolidation stops**: absence is not `none`, the same test as the
     declared-dependency lists below. A row whose force is neither a spec line nor a
     `file:line` is not consolidated — the pipeline stops and asks
   - **A row that adds a precondition must name its satisfier, or consolidation stops.** Any
     row making an earlier case require a state it did not require before — a status, a flag, a
     related record — carries the `Satisfied by` column `00-use-case.md` already asks for:
     an approved `UC-NNN`, this case, or a backlog row **by its `BL-NN`**. Missing or vague, the
     pipeline stops and asks; it is not filled in by inference. A `UC` number is not a valid
     answer for a backlog case — it has none until it is designed, and two reports of a real run
     invented `UC-004` because the sentence needed a name and `BACKLOG.md` had none to give
     (lessons-learned-014 § 7). Where the satisfier is a backlog row, the consolidated spec says
     outright that the earlier case is unreachable end to end until that one ships, and the final
     report repeats it, citing the same `BL-NN` — a use case that answers 422
     on every real call is not a detail the reader should have to find in a test fixture
     (lessons-learned-013 § 5)
   - **A partial that applies must carry its declared-dependency section, or consolidation
     stops.** `20-persistence.md` § 6 always; `31-graphql.md` § 11 whenever step 3g ran; `32-security.md` § 8 whenever step 3b ran;
     `28-http-client.md` § 8 whenever step 3c ran; `29-ai.md` § 10 whenever step 3d ran; `23-search.md` § 9 whenever step 3e ran;
     `25-messaging.md` § 7 whenever step 4 ran; `35-jobs.md` § 7 whenever step 4b ran; `22-cache.md` § 8 whenever step 5b ran; `40-tests.md` § 5 always. The
     value `none` is legitimate and common — most cases need no new dependency — but **absence
     is not `none`**: one says the design skill decided nothing was needed, the other says
     nobody looked, and the executor cannot tell them apart. Steps 4 and 5 validate the same
     thing; they are conditional, and a spec once reached `approved` with both lists missing
     because its partials had been written in earlier runs (lessons-learned-014 § 6). The
     executor then added a dependency to `pom.xml` by inference — a defensible one, and
     precisely the decision this list reserves for the design skill. Consolidation is the block
     every run passes, which is why the check belongs here as well, exactly like `Satisfied by`
     above
   - **A partial that needs a container must carry `## Compose services`, or consolidation
     stops.** `20-persistence.md` always; `25-messaging.md` whenever step 4 ran; `22-cache.md` whenever step 5b ran; `29-ai.md` whenever step 3d ran; `23-search.md` whenever step 3e ran. `none` is
     valid (H2, no broker) and absence is not. Every row goes into the spec's
     `## Infrastructure` with the partial that decided it, shaped by
     `@.claude/skills/docker-architect/references/compose-service-decision.md`. Without it the implement run, in a session that never saw
     this one's report, has nothing to add and nothing to name — the broker of issue #119
   - **A personal-data field crossing the process boundary in clear carries a recorded
     decision, or consolidation stops.** `25-messaging.md` § 8, `30-rest.md` § 6, `31-graphql.md` § 8 and `29-ai.md` § 4 each list
     the fields of the payload, the response body and the GraphQL output types that match
     `@.claude/rules/logging.md` § Masking candidates, with the form chosen. A `full value` row
     without a named receiver and a reason is not consolidated: the pipeline stops and asks, and
     it is not filled in by inference. `none` is a valid value and absence is not one. Until now
     this was a line in the **final report** — detection after the spec is approved, after the
     code is written and after the commit, and in the observed run it appeared there only because
     the executor volunteered it, for a CPF already published in clear on a topic
     (lessons-learned-014 § 8, `@.claude/rules/personal-data.md` § In transit)
   - **A deferred row leaves the run with an owner, or consolidation stops.** Each partial's
     `Deferred` block carries what it decided not to do, the norm that requires it, and an
     intended owner. `checklist` → add the item to this spec's checklist; the run implements it.
     `backlog` → **consolidation appends the row to `docs/use-cases/BACKLOG.md` and assigns its
     `BL-NN`**, then writes that id into this spec's `## Out of scope` with the consequence
     spelled out: what the project does not guarantee until that row ships. Consolidation is the
     only writer of a backlog row inside a feature run — two partials each computing "highest
     plus one" would issue the same `BL-NN`. An item whose norm makes it mandatory and whose
     owner is missing or vague stops the pipeline and is not inferred: a real run decided a
     7-day retention for `outbox_events`, left a commented `DELETE` in the migration, kept
     `app.outbox.prune-after` out of `application.yml` on purpose, and handed the job to nobody,
     over a table whose payload carries personal data (lessons-learned-014 § 9,
     `@.claude/rules/personal-data.md` § At rest)
   - **Every case named in that section gets a line in its own `CHANGELOG.md`**, at
     `docs/use-cases/UC-XXX-<slug>/CHANGELOG.md` — created on the first change, appended
     afterwards. One line: date, the `UC-NNN` making the change, and what changed
     (`2026-09-27 · UC-003 · RegisterCustomerUseCase now emits CustomerRegistered`). The
     approved spec stays untouched, which is exactly why the log is a separate file
     (`@.claude/rules/naming.md` § Use case identifier). Without it, nobody reading the
     altered case ever learns it changed — immutability keeps the text and loses the
     history
   - Order: implementation order (depends-on)
   - **Every `permitAll` carries its reason, or consolidation stops.** `32-security.md` § 1
     lists the public paths of the project after this case, each with a reason; a public row
     with none, or a first secured case whose `## Impact on approved use cases` does not say
     what happens to the endpoints earlier cases published without a chain, is not consolidated
     — deny by default turns them into 401 on the next deploy, and nobody chose that
     (`@.claude/rules/authorization.md` § Default access)
   - Recipient: `java-spring-boot-developer` agent — a spec with § 4.1 runs the executor's
     conditional Block G (steps G1-G3, right after Block 3 and before Block S), which generates the
     schema file, the GraphQL controllers and records, and — the first time — the GraphQL setup from
     `31-graphql.md`; a spec with § 4.5 runs the executor's
     conditional Block S (steps S1-S3, right after REST), which generates the filter chain, the
     mechanism wiring, the method-security annotations and the actor resolution from
     `32-security.md`; a spec with § 3.3 runs the executor's conditional Block H (steps H1-H3,
     right after Block 2), which generates the outbound adapters, the shared translator and the
     engine configuration from `28-http-client.md`; a spec with § 6 runs the executor's
     conditional Block M (steps M1-M4, between REST and Tests), which generates the Kafka
     producer/consumer adapters from `25-messaging.md`; a spec with § 7 runs Block J (steps
     J1-J3, right after Block M), which generates the scheduling wiring and triggers from
     `35-jobs.md`; a spec with § 3.4 runs Block C (steps C1-C3, right after Block J), which
     generates the cache wiring and the port decorators from `22-cache.md`. None touches the fixed
     19-item checklist

3. **Check whether the architecture tests can now be turned on.** The bootstrap doesn't
   install ArchUnit or the coverage gate by design: a `check` over an empty set proves
   nothing. After the first feature that condition no longer holds, and nothing in the
   pipeline was watching for it.

   ```bash
   grep -rl "ArchRule\|ArchTest" --include='*.java' src/test/ 2>/dev/null | head -1
   find src/main/java -name '*.java' ! -name 'package-info.java' | head -1
   ```

   Second command with a result and the first without: the project now has business
   classes and still has no boundary enforcement outside the editor. In `single-module`
   the compiler doesn't enforce anything either, so there's no verification at all.
   **Propose running `test-architect` in setup mode** — propose, don't run it: detection
   is mechanical, authorization is the user's.

---

## End of flow

Every branch below ends in an explicit instruction. None of them runs git outside
`git-publish`.

**Design and implementation never share a session.** This skill designs; a run that
consolidated a spec ends at § Approval. An `approved` spec is implemented only by
`/new-feature-implement UC-NNN-<slug>`, typed after `/clear`. The executor never inherits the
conversation, but the orchestrator's thread does: every hand-back it receives, every group it
launches and the `git-publish` after them would otherwise run at the 250–370k context the
design phase leaves behind
(`@.claude/decisions/0130-executor-split-by-block-group-implement-in-clean-session.md`). The
second half of the pipeline lives in its own skill, so an implement run never loads this body
(`@.claude/decisions/0135-new-feature-split-spec-and-implement.md`).

### Approval — asked on every run that consolidated a spec

`AskUserQuestion`: **Approve `UC-NNN-spec.md`** / **Keep as draft**.

- **Keep as draft** → report the spec path and the resume command
  (`/new-feature UC-NNN-<slug>`), and stop. No git: a draft isn't a deliverable.
- **Approve** → change the spec's line to `status: approved`, then **invoke** `git-publish`
  via the `Skill` tool, with context `docs(UC-NNN-<slug>): approved spec` and
  `docs/use-cases/UC-NNN-<slug>/` plus `docs/use-cases/BACKLOG.md` as the paths to stage.
  Nothing else: a design-only run writes nothing outside `docs/`, and the guard is what makes
  that true rather than intended. Then the final report, which ends with the two lines to
  type next:

  ```
  /clear
  /new-feature-implement UC-NNN-<slug>
  ```

  What used to be staged here — `docker-compose.yml` and `docker/init/**`, when the pipeline
  chained `docker-architect` — is no longer written during the run at all. Every
  `## Infrastructure` row goes into the final report: a `materialize` row is added by
  `/new-feature-implement`, and a `pending` row carries the `/docker-architect` invocation the
  user runs. An unmentioned service is how a `kafka` service went orphan once
  (`lessons-learned-010.md` § 7), and the fix is naming it, not writing the file mid-design.

### Final report

Last message of the run, and the only report: the spec path and status, the backlog
entries left for later (if any), **every `## Infrastructure` row of the spec** — each
compose service with its decision: `materialize` (the implement run adds it), `pending` (with
the `/docker-architect` command that adds it), `external` (with its address), or "none" —
**every approved use case this run left unreachable end to end**, with the backlog row that
restores it named by its `BL-NN` (or "none") — never a `UC` number, which a backlog row does not
have — **every item a partial deferred, with the owner it left it to** (a checklist item, or a
`BL-NN`, or "none"), **every guarantee delegated to a consumer outside this project whose
idempotency is assumed or unknown** (or "none"), and **every personal-data field that crosses
a boundary in clear, with its receiver** (or "none") — now a repeat of what § 8 and § 6 of the
partials already recorded, not the first time anyone asks — three findings a reader must not have to
reconstruct from a fixture comment or a Javadoc sentence — what `git-publish`
did, and the next commands. After § Approval those are `/clear` and
`/new-feature-implement UC-NNN-<slug>`; after **Keep as draft**, `/new-feature UC-NNN-<slug>`.

---

## Template: UC-NNN-spec.md

Lives at `.claude/skills/new-feature/templates/feature-spec.md.example`; the short path
uses `templates/feature-spec-short.md.example`.

Structure (5 blocks, implementation order — plus outbound HTTP, cache, GraphQL, security, messaging and jobs when they apply):
- Frontmatter: `status:`
- Block 1: Use case
- Block 2: Domain model (aggregate, VOs, invariants, ports, events)
- Block 3: Persistence (JPA mapping, migrations, transactions)
- Block 3.3 (conditional): Outbound HTTP (client and engine per dependency, timeouts, retrying
  layer, authentication, project-wide setup NEW/REUSE) — present when step 3c ran; "none"
  otherwise. Implemented by the executor's Block H, right after Block 2
- Block 3.4 (conditional): Cache (cached reads and keys, provider, expiry per cache, writers that
  evict) — present only when step 5b ran; "none" otherwise. Implemented by the executor's
  Block C, last among the production blocks
- Block 3.5 (conditional): Messaging (producer/consumer, delivery semantics, retry/DLQ)
  — present only when `10-domain.md` named external delivery for the event; "none"
  otherwise. See the known gap above — the executor doesn't consume this block yet
- Block 3.6 (conditional): Jobs (technology, triggers, coordination, replica count) —
  present only when step 4b ran; "none" otherwise. Implemented by the executor's Block J
- Block 4: REST API (resources, DTOs, errors, pagination, idempotency) — `none — GraphQL only`
  when step 3 was skipped
- Block 4.1 (conditional): GraphQL (root fields and ports, connections, batch loads, errors as data,
  project setup NEW/inherited) — present when step 3g ran; "none" otherwise. Implemented by the
  executor's Block G, right after Block 3
- Block 4.5 (conditional): Security (mechanism, access per endpoint, `permitAll` list,
  ownership, setup NEW/REUSE) — present when step 3b ran; otherwise `none` with the skip row.
  Implemented by the executor's Block S, right after Block 3
- Block 5: Tests (pyramid, critical cases, coverage, checklist)
- Impact on approved use cases ("none" when empty)
- Final section: Resolved divergences (empty when there were none)

See `templates/feature-spec.md.example` for the full shape.

---

## References

- **D14** — ordered pipeline: use-case → domain → persistence → REST → tests → executor. Order
  of REST and persistence swapped by `0037`.
- **D17** — pipeline skills without `disable-model-invocation` (so `/new-feature` can call them).
- **D20** — `/new-feature` deferred; `java-spring-boot-developer` executor; scope: both.
- **D22** — `/new-feature` design (this record).
- **`@.claude/decisions/0032-messaging-architect-skill.md`** — `messaging-architect`
  chained as a conditional step, same pattern as `persistence-architect`/`rest-api-architect`.
- **`@.claude/decisions/0144-cache-architect-skill.md`** — `cache-architect` chained as step 5b,
  after persistence, only when the use case states a freshness tolerance.
- **`@.claude/decisions/0146-graphql-api-architect-skill.md`** — `graphql-api-architect` chained as
  step 3g, the REST step's pair, when the `Trigger` names a GraphQL adapter; step 3 skipped when it
  names GraphQL alone.
- **`@.claude/decisions/0130-executor-split-by-block-group-implement-in-clean-session.md`** and
  **`@.claude/decisions/0135-new-feature-split-spec-and-implement.md`** — design and implement
  never share a session; the implement flow is `/new-feature-implement`, a skill of its own.
- **`@.claude/decisions/0037-lessons-learned-005-remediation.md`** — closed input table,
  one use case per run, spec lifecycle, no `src/` and no git outside `git-publish`.
- **Invariant 2** (`@CLAUDE.md`) — single owner. The orchestrator owns `UC-NNN-spec.md`;
  `use-case-design` owns number and slug.
- **Invariant 8** (`@CLAUDE.md`) — specs via skills; code via executor.

---

## Entry into generated projects

Step 6.6 writes the skills into the project. `/new-feature` travels the same way — the user runs
`/new-feature <feature description>` to design a new feature.

No adaptation needed — skills already use relative paths.
