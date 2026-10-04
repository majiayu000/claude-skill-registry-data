---
name: doc-catalog-query
description: Answer cross-service architecture questions by reading all service catalogs from the registry (default ~/.claude/service-catalog/, override with $CLAUDE_DOC_HOME). Catalogs are written by /sdd:doc-catalog. Ask things like "who consumes the LeadCreated SNS event?", "what services call /api/v1/consent?", "which services does marketing-service depend on?"
argument-hint: "free-text architecture question"
allowed-tools: Read, Bash(ls:*), Bash(find:*)
---

# Service Catalog Query


---

## Registry Path

All registry reads resolve through a single environment variable:

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/service-catalog"
```

- **Default** (no env var set): `~/.claude/service-catalog/` — identical to the original behavior.
- **Override**: `export CLAUDE_DOC_HOME=/path/to/registry-root` — e.g., a cloned GitLab repo for team-shared catalogs.

The same variable controls `/sdd:doc-catalog`, `/sdd:doc-adr`, `/sdd:doc-adr-query`, `/sdd:doc-spec`, and `/sdd:doc-spec-query`, so all doc registries move together.

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Lists all catalogs in `~/.claude/service-catalog/` |
| 2 | Reads every catalog file |
| 2.5 | Builds a topic/queue index (resolved wire name → every publisher + every consumer) |
| 3 | Answers `$ARGUMENTS` using the combined knowledge |
| 4 | Cites which service(s) the answer comes from |

---

## Step 1 — Check Registry

```bash
ls "${CLAUDE_DOC_HOME:-$HOME/.claude}/service-catalog"/*.md 2>/dev/null
```

If empty, abort:

```
No service catalogs found in ~/.claude/service-catalog/.

Run /sdd:doc-catalog in each service project — it generates the catalog and stores it
in this registry in one step.
```

List available catalogs before answering:

```
Reading 4 service catalogs:
  leads-service.md
  marketing-service.md
  consent-service.md
  creditbureau-service.md
```

---

## Step 2 — Read All Catalogs

Read every `.md` file in `~/.claude/service-catalog/`. Build a combined
knowledge base of:

- REST endpoints (method, path, request/response DTOs)
- SNS topics published (topic name, message schema)
- SQS queues consumed (queue name, message schema)
- Feign clients (target service, methods called)
- External integrations (third-party APIs, SDKs)
- Scheduled jobs
- Key configuration

---

## Step 2.5 — Build the Topic/Queue Index

Before answering, build a normalized index mapping every **resolved wire topic/queue
name** to every service that publishes or consumes it. Skip this only for questions
that aren't event-flow related (endpoint discovery, dependency mapping, data
ownership, etc.).

This step exists because the same event can be labeled differently across services'
catalogs — one service's docs may describe it by a feature/ticket name (e.g.
`CollateralCreationEvent`, `collateral-creation-event-arn`) while another describes the
*same* topic by its literal wire name (`collateral-event`). Answering by grepping
catalogs for the phrase used in the question — instead of the resolved topic/queue
name — silently drops publishers or consumers that happen to use a different label for
the same topic. This has already caused a real miss: `storefront-api` also publishes to
`collateral-event`, but a query for "collateral-creation" only surfaced `leads-service`
and `collateral-service`, because those two catalogs happened to contain that literal
phrase and `storefront-api.md` did not.

For each catalog:
- Read the `## Publishes (SNS)` table — take the `Topic` cell together with the
  resolved property/ARN key (from that table or from `Key Configuration`), not the
  event-type name.
- Read the `## Consumes (SQS)` table — take the `Queue` cell and its `Source topic`
  column when present, resolved the same way.
- Normalize each reference to the literal string bound to the SNS topic ARN or SQS
  queue name — the wire value, not the prose heading or event-type class name used
  in the table.

Build an in-memory table, one row per resolved topic/queue:

```
Topic/queue (resolved wire name)   Published by                          Consumed by
collateral-event                   leads-service, storefront-api             collateral-service, consumer-portal-service, communication-service
lead-events                        leads-service                         marketing-service, consent-service
```

When two or more services resolve to the same wire name under different prose
descriptions, list every one of them — never assume the label used in the question is
the only alias for that topic. Step 3's event-flow queries look up against *this
index*, not against a literal grep of the question's phrase.

---

## Step 3 — Answer the Question

Use the combined catalog knowledge (including the Step 2.5 index) to answer
`$ARGUMENTS`.

### Query types and how to answer them

**Event flow** — "who publishes/consumes X?"
- Resolve X to its wire topic/queue name using the Step 2.5 index first — do not
  search catalogs for the literal phrase in the question, since a service may
  describe the same topic with different wording
- Look up that wire name in the index to get every publisher and every consumer
- Show the full chain: publisher(s) → topic/queue → consumer(s), listing **all**
  publishers/consumers the index found, not just the first match

**Endpoint discovery** — "what services expose X endpoint?"
- Search all `Endpoints` sections for the path or method

**Dependency mapping** — "what does X service depend on?"
- Read X's Feign clients + external integrations
- List target services + third-party APIs

**Impact analysis** — "what breaks if leads-service goes down?"
- Find all services with a Feign client pointing to leads-service
- Find all services consuming queues/topics that leads-service publishes to

**Data ownership** — "who owns the consent_flag field?"
- Search DTOs and request/response schemas across all catalogs

---

## Step 4 — Format the Answer

Always cite the source catalog for every claim:

```
Question: Who consumes the LeadCreated SNS event?

LeadCreated is published by:
  leads-service  →  SNS topic: lead-events  (schema: LeadCreatedEvent)

Consumed by:
  marketing-service  →  SQS queue: marketing-lead-events-queue
  consent-service    →  SQS queue: consent-lead-events-queue

Sources: leads-service.md, marketing-service.md, consent-service.md
```

When the Step 2.5 index finds more than one publisher for the same wire topic, surface
all of them — this is exactly the case a literal-phrase search misses:

```
Question: Where is the collateral-event published from?

collateral-event is published by:
  leads-service  →  CollateralCreationEvent<VehicleDetailDto> — detailed lead
                     processed w/ valid VIN/mileage/state, gated by
                     feature-flag.send-collateral-event
  storefront-api    →  CollateralSNSPublisher.publishEvent() — fired on collateral
                     changes to an application, gated by
                     aws.sns-enabled.collateral-event (independent flag)

Consumed by:
  collateral-service  →  SQS queue: collateral-event-collateral-service

Sources: leads-service.md, storefront-api.md, collateral-service.md
```

If the answer cannot be determined from the available catalogs:

```
Could not find this information in the current registry.
The catalog for <service> may be missing or outdated — run /sdd:doc-catalog in that project.
```

---

## Related Skills

- `doc-catalog` — generates a single service's catalog and stores it in the registry
- `doc-adr-query` — same pattern for architecture decisions
