---
name: rails-action-mailer
description: "Use when designing, implementing, reviewing, testing, or operating Rails Action Mailer delivery, templates, attachments, asynchronous delivery, provider configuration, email security, previews, observability, and failure/retry behavior."
license: MIT
---

# Rails Action Mailer Engineering

## Purpose

Treat outbound email as an external side-effect boundary with its own content, delivery, security, observability, and recovery contracts.

This skill composes existing capabilities:

- `rails-active-job` owns durable asynchronous execution, retry/discard, queue, idempotency, and job lifecycle;
- `rails-api-integration` owns external provider boundaries, timeouts, provider adapters, and integration contracts;
- `rails-security` and `rails-security-engineering` own authentication, authorization, tenant isolation, secret, abuse, and trust-boundary controls;
- `rails-observability` owns logging, error reporting, correlation, and instrumentation;
- `rails-test-engineering` owns test-boundary and deterministic test strategy;
- this skill owns Action Mailer-specific content, recipient, delivery, provider, and message lifecycle decisions.

Rails currently documents both immediate `deliver_now` and Active Job-backed `deliver_later`; asynchronous delivery should be treated as a durable side-effect workflow rather than merely a faster controller call.

Core flow:

```text
business event
-> authorization / recipient eligibility
-> mailer contract
-> render HTML/text/attachments
-> delivery mode
-> provider boundary
-> delivery outcome
-> telemetry/retry/recovery
```

## Activate when

- adding or changing an `ActionMailer::Base` / `ApplicationMailer`;
- adding or changing email templates, layouts, multipart content, or attachments;
- deciding between `deliver_now` and `deliver_later`;
- configuring SMTP or another delivery method;
- changing sender, recipient, reply-to, or delivery headers;
- adding email previews or mailer tests;
- diagnosing missing, duplicated, delayed, or failed email;
- changing retry, queue, or provider behavior for email;
- reviewing tenant/user authorization or sensitive-data exposure through email;
- adding delivery observers, interceptors, or email instrumentation.

Do not activate merely because a background job exists. Use `rails-active-job` unless the task actually crosses the Action Mailer message boundary.

## Repository inspection

Inspect before changing mail delivery:

1. Ruby/Rails version and Action Mailer API available in that version;
2. `ApplicationMailer` and existing mailer hierarchy;
3. mailer views, layouts, partials, previews, and helper conventions;
4. default sender/domain and environment-specific delivery settings;
5. SMTP/API/provider gems and credentials;
6. existing queues, `deliver_later`, job retry/discard policy, and enqueue transaction semantics;
7. recipient eligibility and authorization rules;
8. tenant isolation and data classification;
9. attachments and Active Storage integration where applicable;
10. existing email previews, mailer/request/job tests;
11. logging, error reporting, delivery observers/interceptors, and correlation conventions;
12. deployment/runtime configuration and secret management.

Do not introduce a second mailer abstraction or provider adapter when the repository already has an explicit boundary.

## Mailer boundary

A mailer action should describe the message contract:

```text
purpose
recipient eligibility
sender/reply-to
subject
content formats
template/layout
attachments
delivery mode
provider
failure/retry semantics
observability
```

Keep business eligibility and state transitions outside the template.

Prefer a mailer action that receives the minimum durable input required to reconstruct the message.

Do not pass request/controller objects or arbitrary runtime state into mail delivery.

## Recipient and authorization semantics

An email address being syntactically valid does not make the delivery authorized.

Before sending, determine:

- who is entitled to receive the message;
- which tenant/account owns the data;
- whether consent/preferences/unsubscribe rules apply;
- whether the message contains private or sensitive information;
- whether the user can still receive the content when delivery is delayed;
- whether authorization must be rechecked at execution time.

For `deliver_later`, assume recipient state can change between enqueue and execution.

Never treat the mailer itself as the sole authorization boundary for business actions.

Use `rails-security` and `rails-security-engineering` when the message contains sensitive, tenant-scoped, or privileged data.

## Delivery mode

Use `deliver_later` when delivery should not block the caller and the repository's queue/job contract supports durable asynchronous execution. Rails documents `deliver_later` as backed by Active Job.

Use `deliver_now` only when synchronous delivery is explicitly part of the contract and the latency/failure implications are acceptable.

Before selecting a mode, answer:

- is delivery allowed to be delayed?
- what happens if the caller succeeds but the email later fails?
- what retry semantics exist?
- does the message depend on committed database state?
- can duplicate execution resend the message?
- what is the queue and capacity impact?

Do not use synchronous delivery from request paths merely because it is simpler.

## Transaction boundary

When an email represents a committed business event, ensure the mail cannot be enqueued or rendered against state that later rolls back.

Inspect:

- transaction boundary;
- `deliver_later` enqueue timing;
- queue adapter behavior;
- `after_commit` or repository enqueue conventions;
- whether the mail content depends on data changed in the transaction.

Use `rails-active-job` for detailed transaction-aware enqueue semantics.

Do not assume "save then deliver_later" is equivalent to "email always reflects committed state" without checking the actual queue/transaction contract.

## Idempotency and duplicate delivery

Email delivery is normally at-least-once in the presence of retries and operational recovery.

Define what makes a business message unique:

- notification/event ID;
- order/payment/account state transition;
- explicit delivery record;
- provider idempotency support where available.

Separate:

```text
business event uniqueness
from
delivery attempt uniqueness
```

A retryable send failure can produce uncertain provider outcomes. Do not invent local certainty when the provider may have accepted the message before the client observed failure.

For critical notifications, consider a durable delivery record with explicit states such as pending, sending, sent, failed, or unknown.

Use `rails-distributed-systems` when delivery state spans independent systems and exact-once assumptions would be unsafe.

## Message content contract

Keep message templates deterministic from their inputs.

Define:

- subject;
- plain-text body;
- HTML body;
- locale;
- sender/reply-to;
- URL host/protocol;
- attachment set;
- optional headers.

For user-facing HTML email, provide a plain-text counterpart when appropriate. Rails documents multipart generation when matching text and HTML templates are present.

Do not embed business logic, database queries, network calls, or authorization decisions inside views.

Templates should render already-authorized data.

## URLs and host configuration

Email links are generated outside the normal request host context.

Explicitly verify:

- canonical host;
- protocol;
- route helpers;
- environment-specific URL configuration;
- locale/path semantics where applicable.

Do not derive production email URLs from an arbitrary request host or user-controlled input.

## Attachments

Attachments are part of the message contract and can dominate memory, network, and provider limits.

Inspect:

- source storage;
- file size;
- MIME type;
- encoding;
- generation cost;
- sensitivity;
- retention;
- provider limits;
- repeated generation under retries.

Prefer stable identifiers/retrievable data over serializing unnecessary large payloads into jobs.

When using Active Storage, coordinate with the owning Active Storage design and storage/security boundaries.

Never attach secrets or sensitive files merely because they are available to the caller.

## Provider boundary

Treat SMTP or email APIs as external systems.

Define:

- connection/read/open timeouts where the provider/client supports them;
- authentication/configuration source;
- retryable versus permanent failures;
- provider-specific error mapping;
- rate limits;
- sender/domain restrictions;
- fallback provider behavior if supported.

Keep provider-specific configuration out of domain code.

Use `rails-api-integration` when an email provider exposes an HTTP API and provider-specific payloads need an adapter.

Do not retry invalid recipients, authorization failures, malformed requests, or provider rejection codes classified as permanent.

## Configuration and secrets

Action Mailer configuration is environment-sensitive. Rails documents delivery method, delivery toggles, error handling, defaults, SMTP settings, and credentials-based provider configuration.

Verify:

- delivery method;
- sender defaults;
- host/domain;
- credentials;
- TLS settings;
- open/read timeouts;
- development/test behavior;
- staging sandbox/interceptor behavior;
- production delivery enablement.

Never print SMTP credentials, provider tokens, authorization headers, or full secret-bearing configuration.

Use repository secret management rather than hard-coded credentials.

## Previews and development safety

Rails provides Action Mailer previews for visually inspecting rendered messages.

Use previews for content/layout verification without sending real mail.

For staging environments, consider repository-supported interceptors or recipient overrides that make accidental external delivery impossible.

Do not rely on a human remembering whether an environment is safe before running a preview or test.

## Security and privacy

Email is a data-export boundary.

Classify the message contents:

- public;
- internal;
- user-private;
- tenant-private;
- sensitive/high-risk.

Review:

- recipient authorization;
- accidental CC/BCC;
- attachment exposure;
- URL/token leakage;
- unsubscribe/consent semantics;
- tenant boundaries;
- secret exposure;
- logs and error reports containing message contents.

Do not put authentication tokens, password reset secrets, API credentials, or equivalent secrets into logs.

When links contain sensitive one-time capabilities, coordinate token lifetime and revocation with the authentication/security design.

## Observability

Use bounded structured telemetry.

Useful fields include:

- mailer/action name;
- delivery mode;
- queue/job ID when asynchronous;
- correlation/request ID where available;
- notification/business-event ID;
- provider;
- outcome;
- retry count;
- latency;
- failure class.

Avoid logging full bodies, attachments, recipient lists, or sensitive headers by default.

Rails supports delivery lifecycle observers/interceptors for email processing and observation.

Use observers/interceptors for genuinely cross-cutting delivery concerns rather than embedding business workflows there.

## Testing

Test the message contract at focused boundaries:

- mailer action returns the expected message;
- recipients and headers are correct;
- HTML/text content is correct;
- attachments are correct;
- authorization/tenant isolation is preserved;
- `deliver_later` enqueues the expected job;
- queue and delivery mode are correct;
- transaction/enqueue behavior is safe;
- retry/failure classification is correct;
- previews render;
- provider boundary is isolated.

Do not make tests depend on a live SMTP provider.

Prefer deterministic mailer tests plus Active Job assertions and focused provider-boundary tests.

## Reference example

A mailer that keeps rendering deterministic, the subject translated, and delivery asynchronous.

```ruby
class InvoiceMailer < ApplicationMailer
  def issued(invoice)
    @invoice = invoice
    attach_pdf(invoice)

    mail(
      to: invoice.customer_email,
      reply_to: "support@example.com",
      subject: t(".subject", ref: invoice.reference)
    )
  end

  private

  def attach_pdf(invoice)
    pdf = InvoicePdf.render(invoice) # rendering delegated to a tested PORO, not the mailer
    attachments["invoice-#{invoice.reference}.pdf"] = {
      mime_type: "application/pdf",
      content: pdf
    }
  end
end

# Always enqueue, never render synchronously in a request:
# InvoiceMailer.with(invoice: invoice).issued.deliver_later
```

## Agent review checklist

- [ ] ApplicationMailer hierarchy inspected
- [ ] recipient eligibility/authorization identified
- [ ] tenant/privacy boundary identified
- [ ] deliver_now vs deliver_later explicitly justified
- [ ] transaction/commit semantics checked
- [ ] duplicate/uncertain delivery semantics addressed
- [ ] content contract defined
- [ ] HTML/text/attachment behavior checked
- [ ] production URL/host configuration verified
- [ ] provider boundary isolated
- [ ] credentials protected
- [ ] previews/staging safeguards considered
- [ ] observability is structured and payload-minimized
- [ ] mailer/job/provider tests exist at appropriate boundaries

## Anti-patterns

- sending email synchronously from every request by default;
- embedding authorization or database workflows inside templates;
- enqueuing mail against uncommitted state;
- Do not assume a failed SMTP/API call means the provider definitely did not send.
- relying on email address format as authorization;
- putting secrets or full message bodies into logs;
- hard-coding production SMTP credentials;
- using live email providers in deterministic tests;
- rebuilding large attachments repeatedly during retries;
- adding a new mailer abstraction without repository justification;
- using observers/interceptors for business workflows;
- assuming retry automatically gives exactly-once email delivery.

## Verification

Verify at the smallest owning boundary:

```text
mailer contract
-> focused mailer tests
-> enqueue/delivery semantics
-> provider boundary tests
-> security/privacy checks
-> application regression tests
```

For production delivery changes additionally verify environment configuration, secret presence without value disclosure, queue/runtime configuration, provider connectivity, and delivery observability.

Never claim successful real-world email delivery without observing provider/runtime evidence.

## Source foundation

Primary Rails guidance:
- https://guides.rubyonrails.org/action_mailer_basics.html
- https://guides.rubyonrails.org/testing.html
- https://guides.rubyonrails.org/active_job_basics.html
- https://guides.rubyonrails.org/security.html

Repository composition:
- `rails-active-job` skill
- `rails-api-integration` skill
- `rails-observability` skill
- `rails-security` skill
- `rails-security-engineering` skill
- `rails-test-engineering` skill

## Rails Action Mailer changes

For email and Action Mailer changes:
- inspect ApplicationMailer, mailer views/layouts, delivery configuration, provider dependencies, queue behavior, recipient rules, security controls, and mailer tests before implementing;
- define the recipient/authorization contract separately from message rendering;
- justify deliver_now versus deliver_later from latency, transaction, retry, and duplicate-delivery semantics;
- ensure asynchronous mail observes committed state when the message depends on transactional data;
- classify provider outcomes as retryable, permanent, or uncertain rather than assuming a failed network call means no email was sent;
- isolate provider-specific behavior and credentials from domain code;
- protect tenant/private data, security tokens, attachments, and email logs;
- use deterministic mailer/Active Job/provider tests rather than live SMTP/API calls;
- preserve delivery correlation without logging full message bodies or sensitive headers;
- use previews/interceptors/observers only for their intended rendering or cross-cutting lifecycle responsibilities;
- do not claim real-world delivery without provider/runtime evidence.
