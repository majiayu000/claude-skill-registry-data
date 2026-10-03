---
name: message-bus-security
description: Secure NATS, RabbitMQ, Kafka, and similar message buses against misconfiguration and cross-tenant leakage. Covers account or vhost isolation, deny-default subject and topic permissions, producer and consumer authentication, replay protection, consumer-side idempotency, and encryption in transit and at rest. Invoke when introducing a bus, adding multi-tenancy, or after a cross-tenant message-leakage incident.
---

# Message Bus Security

Message buses (NATS, RabbitMQ, Kafka, MQTT, AWS SQS/SNS, GCP Pub/Sub) are the connective tissue of distributed systems. They're also the most under-audited part of most architectures — by the time the audit gets to "what's on the bus and who can see it", the team has often been on the system for years without revisiting.

This skill is the per-bus and cross-bus checklist. Pairs with [`distributed-system-audit`](../distributed-system-audit/SKILL.md) (system-level audit), [`agent-client-security`](../agent-client-security/SKILL.md) (when agents are producers/consumers).

## When to invoke

- Introducing a message bus to a new architecture
- Adding multi-tenancy to an existing bus
- After an incident involving cross-tenant leakage, replay, or denial-of-service via the bus
- Auditing a system that uses a bus, especially distributed-agent / IoT / worker-pool architectures
- Periodic review (annually for production buses)

## The model

For each bus, you're checking:

1. **Authentication** — who can connect at all
2. **Authorization** — who can publish where, who can subscribe to what
3. **Tenancy** — can tenant A see tenant B's messages, ever
4. **Confidentiality** — in-transit + at-rest encryption
5. **Integrity / replay** — can a captured message be re-sent or forged
6. **Reliability semantics** — exactly-once / at-least-once / at-most-once, and does the application correctly handle the chosen mode
7. **Audit** — when something happens, can you tell who did it

Each bus implements these differently. Below: the common patterns plus per-bus specifics for the three that dominate small/medium-team setups.

## NATS

### Authentication

NATS has several auth options:

- **NKEYs + signed nonces** (Ed25519 key-pair per client). Standard for production.
- **JWT-based auth** (account hierarchy with signed JWTs). Standard for multi-tenant.
- **Username/password** — for dev only
- **TLS client certs** — supported; rarely needed when NKEYs are in use

Production pattern: **Operator → Accounts → Users**. The Operator signs Account JWTs; each Account signs User JWTs. Each User has an NKEY and presents JWT + signed nonce on connect. Revocation is built into the JWT model.

### Authorization (subject permissions)

Permissions are per-User, per-subject, with allow/deny:

```
# In an Account's User definition
allow:
  publish:   ["events.production.>"]
  subscribe: ["responses.<user-id>.>"]
deny:
  publish:   ["events.admin.>"]
```

Patterns:

- **Per-tenant Account** — each customer / tenant gets its own NATS account. Accounts are completely isolated (no message flows between accounts unless explicitly exported / imported). This is the strongest isolation.
- **Per-agent User** with subject permissions scoped to the agent's role (`agent.<id>.>` for its own messages, `commands.<id>` to receive)
- **Wildcard scoping discipline** — `>` is the multi-level wildcard. `agent.>` means "everything under `agent`." Audit for unintentional `>` grants.
- **Subject hierarchies that match security boundaries** — `tenant.<id>.agent.<id>.>` lets you grant tenant-level or agent-level scope cleanly.

### JetStream

JetStream adds persistence and exactly-once semantics. Security additions:

- **Stream-level access control** — per-account, can be further restricted per-user
- **Consumer auth** — durable consumers have their own identity
- **Encryption at rest** — enable in JetStream config; default is plaintext storage

### Common NATS findings

- One account with one credential used by everything ("we'll add multi-tenancy later")
- Subjects organized by feature, not by tenant — cross-tenant messages flow on shared subjects
- `allow: { publish: [">"] }` for "convenience"
- Heartbeat / health-check subjects unauthenticated (anyone can publish to `health.>`)
- JetStream encryption-at-rest off; sensitive payloads in clear on disk
- Operator keys held by everyone with cluster access; should be air-gapped

## RabbitMQ

### Authentication

- **Username/password** is default. Use TLS to protect credentials in transit.
- **TLS client certificates** as an alternative — strong, more operational overhead
- **LDAP / OAuth** plugins for enterprise SSO
- **Per-vhost users** — every connection authenticates to a specific virtual host

### Vhost isolation

Vhosts are RabbitMQ's tenancy primitive. Exchanges, queues, bindings are vhost-scoped. A user has permissions per-vhost.

- **One vhost per tenant** for multi-tenant SaaS
- **Per-user permission triple**: `configure` (create/delete exchanges/queues), `write` (publish), `read` (subscribe). Each is a regex matched against entity names.
- **Default `guest:guest`** only works on localhost; still: delete it in production

### Permission patterns

```bash
# Per-tenant vhost
rabbitmqctl add_vhost tenant-acme

# Per-app user, scoped to that vhost
rabbitmqctl add_user app-acme '<long-random>'
rabbitmqctl set_permissions -p tenant-acme app-acme \
  '^events\..*'      \  # configure: only event-related exchanges
  '^events\..*'      \  # write
  '^acme\..*'           # read: only own queues
```

Tag-based access control extends permissions for management UI (`management`, `monitoring`, `administrator`).

### Common RabbitMQ findings

- Single vhost (`/`) used for all tenants
- `app-user` granted `*.*` permissions (regex matches everything)
- Management UI on public internet without TLS
- Default `guest:guest` still works because the listener was opened to non-localhost
- No `policies` for `queue-mode: lazy` or message TTL — disk fills and bus dies
- Federation / shovel plugins configured but not audited

## Kafka

### Authentication

- **SASL/PLAIN** over TLS for username/password
- **SASL/SCRAM** — better than PLAIN
- **SASL/OAUTHBEARER** — for OIDC-integrated environments
- **mTLS** — strongest, requires PKI

### Authorization (ACLs)

Per-topic, per-operation:

```bash
kafka-acls --bootstrap-server kafka:9092 \
  --add --allow-principal User:app-acme \
  --operation Read --operation Describe \
  --topic events.acme.*
```

Operations: `Read`, `Write`, `Create`, `Delete`, `Alter`, `Describe`, `ClusterAction`, etc.

### Topic / partition design

- **Per-tenant topic prefix** is the common multi-tenant pattern (`tenant-<id>.events`, `tenant-<id>.commands`)
- **No cross-tenant consumer groups** — each tenant's consumer group ID isolated by prefix
- **Compaction tier vs deletion tier** — choose intentionally; compaction-tier topics retain forever
- **Encryption at rest** — disk encryption at the broker is the floor; field-level encryption inside the message for sensitive data

### Common Kafka findings

- Default deny not enforced (`allow.everyone.if.no.acl.found=true` — flip to `false`)
- Single super-user `kafka` credential used by every producer / consumer
- No TLS between clients and brokers (plaintext SASL)
- Schema registry has no auth — anyone can register conflicting schemas
- Mirror / replicator connections without auth
- Connect workers with unrestricted access to all topics

## Generic patterns (applies to every bus)

### Producer / consumer authentication

- **Every connection authenticates**, no anonymous mode in production
- **Identity is per-process / per-instance**, not shared
- **Long-lived static credentials** are a footgun. Prefer rotated tokens or short-lived certs.

### Replay protection

The bus delivers what it's told. If the consumer accepts duplicate messages, replay is trivial.

- **Idempotency keys** in every message (UUID, ULID, or content hash)
- **Consumer dedup table** keyed on idempotency key (see [`backend-architecture`](../backend-architecture/SKILL.md) — same pattern as webhooks)
- **Timestamp + tolerance window** for time-sensitive commands; reject messages outside the window
- **Sequence numbers** per producer for ordering-dependent flows

A "we use TLS so messages can't be replayed" is wrong — TLS protects the channel, not the consumer's state.

### Encryption

- **In transit**: TLS on every listener. Disable plaintext listeners in production.
- **At rest**: bus-specific (JetStream encryption, Kafka disk encryption via dm-crypt / cloud provider, RabbitMQ Mnesia volume encryption)
- **End-to-end (payload-level)**: when sensitive data flows through the bus and bus operators are not trusted with cleartext. Encrypt at the producer, decrypt only at the consumer. Bus sees opaque bytes.

### Cross-cluster / federation

When connecting buses across regions / clusters:

- Each cluster has its own trust root; bridging requires explicit trust
- Federation links / shovels / mirror-makers authenticate just like clients do
- Subject / topic mapping at the bridge — what's allowed to cross, what isn't
- Replay protection still required at the destination cluster

### Audit logging

- **Connection events** (who connected, when, from where)
- **Authentication failures** — repeated failures indicate brute-force or misconfiguration
- **Permission denials** — a publish or subscribe that was denied is a signal (legit reconfig needed, or an attacker probing)
- **Admin actions** (create vhost, change ACL, add user) — these are the security-relevant events

Ship audit logs off-bus; see [`log-strategy`](../log-strategy/SKILL.md).

## When the bus is the entire trust boundary

Some architectures have agents → bus → control plane, with the bus as the only shared infrastructure. The bus's authorization model is then the whole authorization model for the system.

Implications:

- A misconfigured subject/topic permission becomes a system-wide BOLA equivalent
- The bus's audit log is the primary forensic record
- The bus's availability is the system's availability
- Compromise of the bus's admin credentials compromises every tenant

For high-stakes systems with this shape, plan for:

- Per-tenant clusters / namespaces, not just per-tenant subjects within a shared cluster
- Independent backup / DR for the bus (see [`backup-disaster-recovery`](../backup-disaster-recovery/SKILL.md))
- Strict change control on bus configuration

## Checklist

For a message-bus deployment going to production:

- [ ] Every connection authenticated (no anonymous mode)
- [ ] Per-tenant isolation: separate account / vhost / topic-prefix, with enforced permissions
- [ ] Per-producer and per-consumer identity, not shared credentials
- [ ] Permission model is deny-by-default with explicit allows
- [ ] No wildcard `>` / `*` permissions outside of justified admin grants
- [ ] TLS on every listener; no plaintext bind
- [ ] Encryption at rest if the bus persists messages
- [ ] Idempotency keys on every message; consumer dedup table in place
- [ ] Replay protection (nonce, sequence, or timestamp+window)
- [ ] Heartbeat / health subjects authenticated, not free-for-all
- [ ] Cross-cluster federation authenticated and audited
- [ ] Audit logging enabled, shipped off-bus
- [ ] Admin / operator credentials separate from app credentials, restricted use
- [ ] Default credentials (`guest:guest`, etc.) removed
- [ ] Backup / DR strategy for the bus exists

## What this skill will not do

- Help bypass message-bus authentication on systems you do not own
- Recommend wildcard permission grants as a default
- Replace a bus-vendor-specific security guide for highly-regulated deployments
