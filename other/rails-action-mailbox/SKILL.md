---
name: rails-action-mailbox
description: "Use when designing, implementing, reviewing, testing, or operating Rails Action Mailbox inbound email processing, ingress authentication, mailbox routing, message lifecycle, domain association, failure handling, retention, observability, and security."
license: MIT
---

# Rails Action Mailbox Engineering

## Purpose

Treat inbound email as an untrusted external ingestion boundary, not as a controller shortcut.

This skill owns Action Mailbox-specific decisions around:

- ingress and provider boundary;
- raw RFC822/MIME message handling;
- InboundEmail lifecycle;
- mailbox routing;
- mailbox processing and callbacks;
- sender/recipient and tenant association;
- duplicate and replay semantics;
- bounce, failure, quarantine, and recovery;
- retention/incineration;
- attachment interaction with Active Storage;
- deterministic testing.

It composes existing repository capabilities:

- rails-api-integration for provider/webhook and ingress boundary contracts;
- rails-security and rails-security-engineering for trust, authenticity, authorization, tenant isolation, and abuse controls;
- rails-active-job for asynchronous mailbox execution, retry, queue, idempotency, and transaction semantics;
- rails-active-storage for raw email storage and attachment lifecycle;
- rails-action-mailer for outbound replies and bounce notices;
- rails-observability for correlation, error reporting, metrics, and lifecycle telemetry;
- rails-reliability-engineering and rails-incident-engineering for overload, provider failure, backlog, quarantine, and operational recovery;
- rails-distributed-systems / rails-event-driven-messaging when inbound email becomes a cross-process workflow;
- rails-test-engineering for deterministic ingress/mailbox tests.

Official Rails documentation describes Action Mailbox as the inbound counterpart to Action Mailer. Incoming messages are accepted through a configured ingress, persisted as ActionMailbox::InboundEmail records with raw email in Active Storage, routed to controller-like mailboxes, and processed asynchronously through Active Job.

Core flow:

~~~
provider / MTA
-> authenticated ingress
-> raw RFC822/MIME capture
-> InboundEmail
-> routing
-> mailbox processing
-> domain transaction / side effects
-> delivered | bounced | failed
-> telemetry / recovery
-> retention / incineration
~~~

## Activate when

- adding ActionMailbox::Base or ApplicationMailbox;
- adding a mailbox with process or processing callbacks;
- configuring Mailgun, Mandrill, Postmark, SendGrid, Exim, Postfix, Qmail, or relay ingress;
- changing config.action_mailbox.ingress;
- handling inbound email from customers, replies, support addresses, aliases, or automated systems;
- mapping sender/recipient data to a user, tenant, ticket, project, or domain resource;
- handling email attachments or raw message storage;
- diagnosing duplicate, missing, delayed, bounced, failed, or misrouted inbound mail;
- changing incinerate_after or inbound-email retention;
- adding replay, quarantine, operator tooling, or forensic workflows;
- testing inbound email without live provider dependencies.

Do not activate for outbound email alone; route those tasks to rails-action-mailer.

## Repository inspection

Inspect:

1. resolved Rails, Active Job, and Action Mailbox versions;
2. queue adapter and worker configuration;
3. config.action_mailbox.ingress and credentials;
4. provider webhook/MTA configuration and reverse-proxy limits;
5. app/mailboxes/application_mailbox.rb and existing mailbox routes;
6. action_mailbox_inbound_emails schema and Active Storage configuration;
7. sender/recipient/tenant association and authorization rules;
8. existing idempotency, jobs, events, outbox/inbox, and Action Mailer behavior;
9. logging, error reporting, metrics, alerting, replay, and runbook conventions;
10. ActionMailbox::TestCase, fixtures, factories, and Active Storage test service.

Never invent an ingress contract before inspecting the actual provider/MTA setup.

## Decision rules

1. Classify the change: ingress and mailbox routing, processing lifecycle and failure semantics, authenticity/idempotency/tenant association, attachments/retention/operations, or local development and testing.
2. Load the matching reference below before changing behavior; any new mailbox needs the ingress, processing, and security references.
3. Keep mailbox processing a thin boundary that hands business effects to domain code with durable, idempotent identity.

## Critical invariants

- Treat inbound email as hostile input.
- Do not trust From, Reply-To, Return-Path, or arbitrary headers as authentication merely because they parse successfully.
- Do not assume one InboundEmail row means the business effect has happened exactly once.
- Never log full raw email bodies by default.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change configures ingress, ingress authentication, or ApplicationMailbox routing | [references/ingress-and-routing.md](references/ingress-and-routing.md) | Ingress boundary; Mailbox routing | `action-mailbox-ingress-boundary`, `action-mailbox-routing-contract` |
| a change alters mailbox processing, processing states, bounce/failure handling, or transactional and asynchronous work | [references/processing-lifecycle.md](references/processing-lifecycle.md) | Mailbox processing boundary; Lifecycle and processing states; Callbacks and failure semantics; Transactions and asynchronous work | `action-mailbox-processing-lifecycle`, `action-mailbox-failure-quarantine` |
| a change trusts sender identity, deduplicates deliveries, or associates email with tenants or resources | [references/security-and-idempotency.md](references/security-and-idempotency.md) | Authenticity and security; Idempotency and duplicate delivery; Tenant and resource association | `action-mailbox-authenticity-security`, `action-mailbox-idempotency`, `action-mailbox-tenant-association` |
| a change stores attachments, alters retention or incineration, or affects operations, capacity, or provider/MTA behavior | [references/attachments-retention-operations.md](references/attachments-retention-operations.md) | Attachments and Active Storage; Retention, privacy, and incineration; Observability and operations; Capacity and performance; Provider and MTA compatibility | none |
| exercising mailboxes locally or choosing and writing Action Mailbox tests | [references/testing.md](references/testing.md) | Local development and testing | `action-mailbox-testing` |

## Reference example

A mailbox that authenticates the sender before processing, creates its record, and hands attachments to Active Storage.

```ruby
class SupportMailbox < ApplicationMailbox
  routing /^support\+/i => :support

  before_processing :ensure_known_sender

  def process
    ticket = current_account.tickets.create!(
      subject: mail.subject,
      from_address: mail.from.address
    )

    mail.attachments.each do |attachment|
      ticket.attachments.attach(
        io: attachment.body.to_io,
        filename: attachment.filename,
        content_type: attachment.mime_type
      )
    end
  end

  private

  def ensure_known_sender
    bounce_with Mailer.unrecognized_sender(mail) unless mail.from.address.end_with?("@example.com")
  end
end
```

## Agent review checklist

- [ ] Rails/Action Mailbox version resolved
- [ ] ingress/provider/MTA boundary inspected
- [ ] ingress authentication mechanism explicit
- [ ] raw RFC822 requirement explicit
- [ ] request/body size limits reviewed
- [ ] ApplicationMailbox routing order reviewed
- [ ] catch-all/unmatched recipient behavior explicit
- [ ] mailbox owns orchestration rather than unrelated domain policy
- [ ] sender identity proof separated from ingress authentication
- [ ] recipient and tenant authorization explicit
- [ ] duplicate/replay semantics explicit
- [ ] domain idempotency owner explicit
- [ ] transaction/commit boundary explicit
- [ ] downstream job/event semantics explicit
- [ ] attachments reviewed through Active Storage
- [ ] content/file limits explicit
- [ ] failure/bounce/quarantine behavior explicit
- [ ] status transitions treated as lifecycle evidence
- [ ] retention/incineration policy reviewed
- [ ] logs redact raw message and credentials
- [ ] lifecycle telemetry and correlation reviewed
- [ ] deterministic mailbox tests exist
- [ ] cross-tenant and duplicate negative tests exist

## Anti-patterns / failure modes

- trusting the From header as authentication;
- treating ingress authentication as domain authorization;
- using recipient strings as tenant authorization;
- routing broad patterns before specific mailbox routes;
- silently dropping unmatched recipients;
- performing non-idempotent side effects before duplicate detection;
- assuming Action Mailbox guarantees exactly-once business effects;
- rescuing all exceptions and marking mail delivered;
- doing unbounded work from email attachments;
- logging raw RFC822 content;
- exposing internal InboundEmail records as a public API;
- putting provider-specific payload parsing in mailbox classes;
- extending raw-email retention without a privacy requirement;
- assuming incineration removes derived domain data;
- performing slow network calls inside database transactions;
- enqueueing follow-up jobs before required state is committed;
- relying on Message-ID alone when provider behavior does not guarantee stability;
- using replay tooling that bypasses authorization;
- treating HTML or attachment MIME metadata as trusted;
- claiming inbound email is secure because the provider signed the webhook.

## Verification

For an Action Mailbox feature:

~~~
Rails/version evidence
-> ingress boundary
-> authentication
-> routing
-> sender/recipient/tenant authorization
-> idempotency
-> domain transaction
-> async follow-up
-> failure/bounce/quarantine
-> attachment/security review
-> retention
-> observability
-> deterministic tests
-> regression verification
~~~

Never claim that inbound email is exactly-once, authenticated as a business user, or durable beyond configured retention without evidence from the actual ingress, domain, queue, and storage contracts.

## Source foundation

Primary Rails sources:

- https://guides.rubyonrails.org/action_mailbox_basics.html
- https://api.rubyonrails.org/classes/ActionMailbox/Base.html
- https://api.rubyonrails.org/classes/ActionMailbox/Router.html
- https://api.rubyonrails.org/classes/ActionMailbox/InboundEmail.html
- https://api.rubyonrails.org/classes/ActionMailbox/TestHelper.html

These sources document Action Mailbox ingress configuration, asynchronous mailbox routing, InboundEmail persistence/status tracking, mailbox callbacks/bounce behavior, testing helpers, and automatic incineration.

Composed repository skills:

- `rails-action-mailer` skill
- `rails-active-job` skill
- `rails-active-storage` skill
- `rails-api-integration` skill
- `rails-security` skill
- `rails-security-engineering` skill
- `rails-database-engineering` skill
- `rails-event-driven-messaging` skill
- `rails-distributed-systems` skill
- `rails-observability` skill
- `rails-reliability-engineering` skill
- `rails-incident-engineering` skill
- `rails-test-engineering` skill
- `rails-test-engineering` skill

## Rails Action Mailbox changes

For inbound email and Action Mailbox changes:
- inspect the configured ingress, provider/MTA setup, ApplicationMailbox routes, mailbox classes, Active Job queue behavior, InboundEmail schema/storage, authorization rules, Active Storage behavior, retention configuration, observability, and mailbox tests before implementing;
- classify the boundary as external ingress, mailbox routing, mailbox processing, or downstream asynchronous work;
- keep ingress authentication separate from sender identity, recipient authorization, and tenant/resource authorization;
- treat the From header, Reply-To, Return-Path, custom headers, HTML, links, and attachment metadata as untrusted input until the owning boundary verifies them;
- define provider/MTA retry, duplicate, raw-message, body-size, timeout, and credential-rotation contracts at the ingress boundary;
- keep provider-specific payload handling out of mailbox/domain code;
- order mailbox routes from specific to general, define unmatched-message behavior, and test route collisions;
- keep mailbox classes focused on orchestration and delegate complex domain rules to the owning service/model/policy boundary;
- use before_processing for cheap deterministic prerequisites and keep framework status truthful; do not convert programmer defects into successful delivery;
- separate business-invalid messages, transient dependencies, poison messages, and programmer failures so retry/bounce/quarantine behavior is bounded and explicit;
- do not assume Action Mailbox provides exactly-once business effects; define durable domain idempotency for non-idempotent mutations and preserve message identity during replay;
- persist tenant/resource ownership through authoritative application state and propagate tenant context to downstream jobs/events;
- coordinate business mutations and follow-up jobs/events through the actual transaction/commit contract;
- use rails-active-storage for attachment/storage lifecycle and enforce server-side size/type/content limits;
- treat raw inbound mail as privacy-sensitive data; never log full raw messages or credentials by default;
- review config.action_mailbox.incinerate_after as a raw-message retention policy and distinguish it from lifecycle of derived domain data;
- use deterministic ActionMailbox test helpers and local/test storage/provider doubles; do not rely on live email providers for ordinary CI;
- add negative tests for spoofed senders, cross-tenant targets, duplicate delivery, unmatched routing, poison messages, and sensitive log output;
- never claim inbound email is authenticated as a business user merely because the ingress is authenticated, and never claim exactly-once processing without evidence from the domain idempotency contract.
