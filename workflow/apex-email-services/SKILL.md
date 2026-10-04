---
name: apex-email-services
description: "Use this skill when implementing inbound email processing via Apex: parsing emails sent to a Salesforce-hosted address, creating or updating records from email content, handling attachments, or configuring Email Service routing. Trigger keywords: InboundEmailHandler, email service address, handleInboundEmail, Messaging.InboundEmail, Email-to-Case alternative, process email in Apex. NOT for outbound email — use apex/apex-outbound-email-patterns. NOT for email templates or workflow email alerts — use admin/email-templates-and-alerts."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Reliability
  - Performance
triggers:
  - "how do I process incoming emails with Apex and create records automatically"
  - "my InboundEmailHandler is not receiving emails or silently dropping messages"
  - "how do I parse attachments from an inbound email in Apex code"
  - "what are the daily email limits for Apex Email Services"
  - "email sent to Salesforce address is bouncing or not routing to my handler"
tags:
  - apex-email-services
  - inbound-email
  - InboundEmailHandler
  - email-automation
  - messaging
inputs:
  - "Salesforce org user license count (the daily inbound ceiling scales with it)"
  - "Use case: record creation, parsing, attachment handling, or routing"
  - "Whether the email comes from an external system, customer, or automated process"
  - "Expected email volume per day"
outputs:
  - "Compliant InboundEmailHandler Apex class"
  - "Email Service configuration guidance (Setup > Email Services)"
  - "Attachment parsing strategy for TextAttachment and BinaryAttachment"
  - "Review checklist for production readiness"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-28
---

# Apex Email Services

This skill activates when a practitioner needs to receive, parse, and act on inbound emails using Apex. It covers the full lifecycle: implementing `Messaging.InboundEmailHandler`, configuring the Email Service address in Setup, parsing body and attachment content, handling rejection/bounce behavior, and writing testable handlers. It does NOT cover outbound email (`Messaging.SingleEmailMessage`), email alerts, or the declarative Email-to-Case setup.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the org's **user license count**, not its edition — the inbound processing ceiling scales with licenses. "Email Services: Maximum Number of Email Messages Processed" is *"Number of user licenses multiplied by 1,000; maximum 1,000,000"*, and Salesforce *"limits the total number of messages that all email services combined, including On-Demand Email-to-Case, can process daily."* So it is an **org-wide daily pool**, not a per-service-address allowance: every email service in the org, plus On-Demand Email-to-Case, draws from the same number. Ten licenses means 10,000 messages a day across all of them. Messages over the ceiling are bounced, discarded, or queued for the next day depending on each service's failure-response setting.
- Identify whether you need text parsing, HTML parsing, or binary attachment processing — these require different handler branches.
- The most common wrong assumption: practitioners expect `handleInboundEmail` to run as the sender. It does not — it runs as the Email Service's configured **Context User**, and `email.fromAddress` is unverified header data at every API version. What its database operations enforce is gated by the `apiVersion` in the class's `.cls-meta.xml`, not by the org's release: at **66.0 and below** a handler declared without a sharing keyword runs in system mode, so no user permission enforcement applies unless you explicitly delegate to a helper class declared `with sharing`; at **67.0+** (Summer '26) that inverts and the bare class runs `with sharing` with SOQL/DML defaulting to user mode against the Context User. Read the `.cls-meta.xml` before assuming either. Canonical table: `agents/_shared/AGENT_CONTRACT.md` § *Apex security idiom by API version*.
- Email Services run synchronously per message. Governor limits apply to the full handler execution: 100 SOQL queries, 150 DML statements, and a heap of **50 MB** — email services get their own elevated heap allocation, not the 6 MB synchronous / 12 MB asynchronous figure that applies to ordinary Apex. Size your attachment handling against 50 MB, and note that heap is consumed by *transformations* of a Blob (base64-encoding, `toString()`, string concatenation), each of which allocates a fresh copy, not by holding the original Blob once. The largest payload that can reach the handler is capped upstream: "Email Services: Maximum Size of Email Message (Body and Attachments)" is **25 MB**, measured across body text, HTML, and all attachments together.
- The Email Service address must be **activated** in Setup. An inactive address silently drops all inbound mail.

---

## Core Concepts

### Mode 1: The InboundEmailHandler Interface

`Messaging.InboundEmailHandler` is the contract for all Apex inbound email processing. Your class must implement exactly one method:

```apex
global Messaging.InboundEmailResult handleInboundEmail(
    Messaging.InboundEmail email,
    Messaging.InboundEnvelope envelope
) { ... }
```

The return value matters. If you set `result.success = false`, Salesforce either bounces the message back to the sender or drops it silently — controlled by the **Error Action** setting on the Email Service configuration in Setup. Always return a populated `InboundEmailResult`; a `null` return is treated as failure.

The `InboundEmail` object carries the full message:
- `email.subject` — subject line
- `email.fromAddress` / `email.fromName` — sender identity
- `email.plainTextBody` / `email.htmlBody` — body variants
- `email.toAddresses` / `email.ccAddresses` — recipient arrays
- `email.textAttachments` — list of `InboundEmail.TextAttachment`
- `email.binaryAttachments` — list of `InboundEmail.BinaryAttachment`

The `InboundEnvelope` carries transport-level metadata: `toAddress`, `fromAddress`, which can differ from the `To:` and `From:` headers.

### Mode 2: Email Service Configuration

Each Apex handler class is associated with one or more **Email Service** configurations in Setup > Email Services. Each configuration generates a unique `@[instance].salesforce.com` address. Key settings:

| Setting | Purpose |
|---|---|
| Active | Must be checked or all mail is dropped. |
| Accept Email From | Restrict to specific sender domains or addresses; leave blank to accept all. |
| Error Action | Controls what happens when `success = false` — Bounce, Discard, or Requeue. |
| Apex Class | Points to your `InboundEmailHandler` implementation. |
| Over Email Rate Limit | Action when the daily limit is reached — Bounce, Discard, or Requeue. |

You can create multiple Email Service addresses (each with a different configuration) backed by the same Apex class to support different routing scenarios (e.g., separate addresses per product line, each stamping a different record type on created Cases).

### Mode 3: Attachment Parsing

Two attachment types exist, mapped separately:

- `InboundEmail.TextAttachment`: has `.body` (String), `.fileName`, `.mimeTypeSubType`
- `InboundEmail.BinaryAttachment`: has `.body` (Blob), `.fileName`, `.mimeTypeSubType`

CSV, plain text, and XML files arrive as `TextAttachment` when the MIME type is text-based. Images, PDFs, and binary formats arrive as `BinaryAttachment`. Handlers must check both lists and apply defensive null checks — either list can be null if no attachments of that type exist.

Attachments are processed **synchronously** inside your handler's governor limit budget. The inbound message as a whole — body plus all attachments — is capped at **25 MB**, so that is the ceiling on what can arrive, against the 50 MB email-services heap allocation. Heap is consumed by *transforming* the payload rather than by receiving it: converting a `Blob` to a `String` (e.g., `EncodingUtil.base64Encode`, `Blob.toString()`) allocates a fresh full-size copy each time, and two or three copies of a large attachment will exhaust 50 MB. Use chunked processing, or persist the Blob and defer the heavy work to a `Queueable` called from within the handler — sizing that Queueable's work against the 12 MB asynchronous heap limit rather than the handler's 50 MB.

---

## Common Patterns

### Pattern: Create-or-Update Record from Inbound Email

**When to use:** An external system sends structured emails (e.g., order confirmations, sensor alerts) and you need to upsert Salesforce records based on parsed email content.

**How it works:**
1. Implement `InboundEmailHandler` and parse `email.plainTextBody` or `email.subject` for a record identifier (e.g., an order number in the subject line).
2. Use `SOQL` to find an existing record by the extracted identifier.
3. Upsert or insert accordingly, populating fields from parsed email content.
4. Return `result.success = true` on success, or log errors and return `false` if parsing fails.

```apex
global class OrderEmailHandler implements Messaging.InboundEmailHandler {
    global Messaging.InboundEmailResult handleInboundEmail(
        Messaging.InboundEmail email,
        Messaging.InboundEnvelope envelope
    ) {
        Messaging.InboundEmailResult result = new Messaging.InboundEmailResult();
        try {
            String orderNum = extractOrderNumber(email.subject);
            if (String.isBlank(orderNum)) {
                result.success = false;
                result.message = 'No order number found in subject.';
                return result;
            }
            List<Order__c> orders = [
                SELECT Id FROM Order__c WHERE OrderNumber__c = :orderNum LIMIT 1
            ];
            Order__c order = orders.isEmpty() ? new Order__c(OrderNumber__c = orderNum) : orders[0];
            order.LastEmailBody__c = email.plainTextBody;
            order.LastEmailDate__c = System.now();
            upsert order OrderNumber__c;
            result.success = true;
        } catch (Exception e) {
            result.success = false;
            result.message = e.getMessage();
        }
        return result;
    }

    private String extractOrderNumber(String subject) {
        if (subject == null) return null;
        Pattern p = Pattern.compile('ORD-\\d+');
        Matcher m = p.matcher(subject);
        return m.find() ? m.group() : null;
    }
}
```

**Why not simpler approaches:** A Flow with Email-to-Case only creates Cases. Custom Apex is needed when you need to target arbitrary sObjects, apply complex parsing logic, or conditionally reject mail.

### Pattern: Async Attachment Processing via Queueable

**When to use:** Emails arrive with large or multiple binary attachments that would exceed heap or CPU limits if processed synchronously.

**How it works:**
1. In `handleInboundEmail`, extract only the attachment metadata and Blob data. Store the Blob in a `ContentVersion` record immediately (avoids re-processing the email).
2. Enqueue a `Queueable` job, passing the `ContentVersion` Id.
3. The Queueable performs the expensive parsing (CSV, base64 decode, PDF text extraction stubs, etc.) in a separate transaction with its own governor limits.
4. Return `result.success = true` from the handler immediately — the email is accepted, processing continues asynchronously.

**Why not synchronous:** The email-services heap ceiling is **50 MB**, not the 6 MB synchronous / 12 MB asynchronous figure for ordinary Apex — a 10–15 MB attachment does not blow heap by arriving. What exhausts it is in-line *transformation*: `EncodingUtil.base64Encode` allocates a second, ~33%-larger copy, `Blob.toString()` a third, and a parse loop one per iteration.

Be precise about what deferring buys you. A `Queueable` runs under the ordinary **12 MB** asynchronous heap limit, so moving work there *lowers* your heap ceiling from 50 MB — "defer it for more heap" is backwards. Defer for a fresh transaction with its own CPU and DML budget and a retry surface, and size the Queueable's work against 12 MB.

### Pattern: Sender-Based Routing with Multiple Service Addresses

**When to use:** Different senders or subject patterns need to create different record types or trigger different workflows, but you want a single Apex class.

**How it works:**
1. Create multiple Email Service configurations in Setup, each pointed at the same Apex class.
2. Pass a routing signal via the email address itself (e.g., `support-billing@...` vs `support-tech@...`) or encode routing in a Custom Setting keyed by `toAddress`.
3. Inside `handleInboundEmail`, read `envelope.toAddress` to determine routing context, then branch logic accordingly.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Customer email should create a Case automatically | Declarative Email-to-Case (Setup > Email-to-Case) | No code needed; native threading and routing built in |
| Email from external system should upsert a custom sObject | Apex Email Service with `InboundEmailHandler` | Email-to-Case only targets Cases; Apex has full DML access |
| Email has large binary attachments requiring custom parsing | Apex handler + Queueable for attachment processing | Avoids synchronous heap/CPU limits |
| Need to reject or bounce specific senders at processing time | Apex handler returning `result.success = false` | Email Services Error Action controls bounce/discard behavior |
| Outbound transactional emails to customers | `Messaging.SingleEmailMessage` or email templates + workflow | This skill covers inbound only |
| Inbound volume approaches the org's daily ceiling (user licenses × 1,000, max 1,000,000) | Platform architecture review — consider middleware or batching | The ceiling is org-wide and shared with On-Demand Email-to-Case, scales with licenses rather than edition, and cannot be raised in code |

---


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org's user license count, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] `InboundEmailHandler` class is `global` and implements the interface correctly
- [ ] `handleInboundEmail` always returns a non-null `InboundEmailResult`
- [ ] Email Service address is **active** in Setup > Email Services
- [ ] `Accept Email From` restriction is configured to prevent spoofing
- [ ] Attachment parsing handles null `textAttachments` and `binaryAttachments` lists defensively
- [ ] Handler has a `try/catch` block and sets `result.success = false` on unexpected exceptions
- [ ] Test class uses `Test.setFixedSearchResults` or constructs `InboundEmail` objects directly
- [ ] Daily volume estimate confirmed against the **org-wide** ceiling (user licenses × 1,000, max 1,000,000), counting every email service **and** On-Demand Email-to-Case against the same pool
- [ ] Large attachment flows enqueue a `Queueable` instead of processing synchronously
- [ ] Error Action on the Email Service config is set intentionally (Bounce vs Discard)

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **The Default Access Mode Is Version-Gated** — at `apiVersion` **66.0 and below**, a handler class with no sharing keyword runs in system mode: no `with sharing` enforcement and no record-level access control unless you explicitly call into a helper class declared `with sharing`, so a handler that creates records with a bare `insert` bypasses all sharing rules silently. At **67.0+** the bare class runs `with sharing` and its SOQL/DML default to user mode against the Email Service's Context User — which moves the risk onto that user's permissions rather than removing it. The gate is the class's `.cls-meta.xml`, not the org's release; see `references/gotchas.md` Gotcha 2.
2. **Inactive Address Drops Mail Silently** — If the Email Service address is set to Inactive in Setup, inbound emails do not bounce and do not generate errors. They are silently discarded. Practitioners regularly deploy a handler, forget to activate the service address, and spend hours debugging a "no traffic" problem.
3. **Both Body Fields Can Be Null** — HTML-only emails leave `plainTextBody` null. Plain-text-only emails leave `htmlBody` null. Production handlers that assume one is always populated throw `NullPointerException`s on real mail. Always test both paths.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| `InboundEmailHandler` Apex class | Global Apex class implementing `Messaging.InboundEmailHandler`, ready to associate with an Email Service configuration |
| Email Service configuration checklist | Verified settings in Setup > Email Services: active flag, accepted senders, error action, rate limit action |
| Attachment parsing strategy | Documented decision on sync vs async processing based on expected attachment size and volume |
| Test class | Apex test constructing `Messaging.InboundEmail` objects directly and asserting on DML outcomes |

---

## Related Skills

- **apex/governor-limits** — Synchronous handler execution consumes the same governor limits as any Apex transaction; consult this skill when attachment or SOQL load is high.
- **apex/apex-rest-services** — Use when the integration partner can push HTTP instead of email; REST is preferable for high-volume structured data exchange.
- **admin/email-templates-and-alerts** — Use for outbound email workflows. NOT a replacement for inbound email processing.
- **integration/rest-api-patterns** — Consider as an alternative integration channel if volume or reliability requirements exceed what Email Services can provide.
