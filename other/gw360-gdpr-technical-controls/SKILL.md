---
name: gdpr-technical-controls
description: Implement the technical side of GDPR and EU privacy compliance. Covers data inventory, subject-access (SAR) and deletion endpoints, anonymization patterns, log scrubbing, the 72-hour breach notification path, and sub-processor (DPA / AVV) tracking. Invoke when building a product handling EU resident data, responding to a SAR, or preparing for a Datenschutz audit.
---

# GDPR — Technical Controls

GDPR (and its UK / EEA siblings) is a legal framework with a heavy technical surface. This skill stays on the engineering side: what to build, what to log, what to expose, what to delete. For DACH-specific Impressum/AGB/AVV requirements, see [`dach-compliance`](../dach-compliance/SKILL.md). For data-protection legal questions, talk to a DPO.

The terms used here line up with the regulation but are paraphrased. When in doubt, the regulation text is the source of truth.

## When to invoke

- Building or reviewing a product handling EU/EEA/UK resident data
- Responding to a Subject Access Request (SAR) or deletion request
- Preparing for a Datenschutz / DPA audit
- Adding a new third-party processor (analytics, support, email, AI, CDN)
- After a suspected personal-data breach
- A user asked "where is my data?"

## Step 1 — Data inventory

You cannot protect data you cannot enumerate. Build and maintain a record of:

- **What personal data fields** you store (`users.email`, `orders.shipping_address.street`, …)
- **Where** each lives (Postgres table, S3 bucket, log file, third-party processor)
- **Purpose** of each (legal basis: consent / contract / legitimate interest / legal obligation)
- **Retention period** — when it should be deleted
- **Who can access** it (roles, audit log)
- **Third parties (processors)** receiving copies, and the lawful basis for each transfer

A reasonable starting format:

```
Field                    | Location                 | Purpose / basis        | Retention | Processors
-------------------------|--------------------------|------------------------|-----------|-----------
user.email               | postgres.users           | account (contract)     | until-deletion + 30d backup decay | Mailgun (transactional)
user.password_hash       | postgres.users           | auth (contract)        | until-deletion | -
order.shipping_address   | postgres.order_addresses | fulfillment (contract) | 10y (tax)  | DHL (delivery)
user.ip                  | nginx access logs        | abuse (legit interest) | 90d        | -
user.session_cookie      | redis, nginx logs        | session (contract)     | session+30d | -
```

This is the foundation for SARs, deletion requests, breach scoping, and processor-agreement enumeration. Keep it in a private repo or wiki — version-controlled, not in a one-off spreadsheet.

## Step 2 — Subject Access Request (SAR) endpoint

A user can ask for a copy of all their personal data. You have one month to respond (extendable to three with reason).

**Don't build this manually per request**. Build a SAR endpoint or admin tool that produces the export programmatically.

```ts
// Sketch — admin tool that produces a SAR bundle
async function generateSAR(userId: string) {
  const bundle: Record<string, unknown> = {};

  bundle.profile = await db.users.findUnique({ where: { id: userId }, select: safeProfileFields });
  bundle.orders = await db.orders.findMany({ where: { userId }, select: orderFieldsForSAR });
  bundle.addresses = await db.addresses.findMany({ where: { userId }});
  bundle.support_tickets = await db.tickets.findMany({ where: { userEmail: bundle.profile.email }});
  bundle.audit_log = await db.authEvents.findMany({ where: { userId }, take: 1000 });
  bundle.consent_history = await db.consents.findMany({ where: { userId }});

  // Files / media — include URLs to time-limited download links
  bundle.uploads = await listUserUploads(userId);

  return bundle;   // serialize to JSON or ZIP
}
```

Patterns:

- **Authenticate the request rigorously** — the SAR endpoint is itself a takeover vector. Require login + recent re-auth + email-confirm-link before issuing the export.
- **Time-limited download** — the export contains the same PII you protect everywhere else. Serve via a single-use URL, valid for 24h.
- **Document what's NOT in the export** — purely operational metadata (server logs, monitoring data) is generally not required to include but mention it transparently.
- **Right to portability** is a related right — machine-readable format. JSON is fine; offer CSV for tabular fields.

## Step 3 — Deletion endpoint

A user can ask to be deleted (Article 17). You generally have one month.

**Hard problem**: most apps have data scattered across services, with foreign keys, with cached copies in third parties.

```ts
async function deleteUser(userId: string) {
  // 1. Soft-mark for deletion, prevent further logins immediately
  await db.users.update({ where: { id: userId }, data: { deletedAt: new Date(), status: 'deleting' }});
  await invalidateAllSessions(userId);

  // 2. Anonymize records that must be retained for legal reasons (tax invoices etc.)
  await db.invoices.updateMany({
    where: { userId },
    data: { userId: null, customerName: 'DELETED USER', customerEmail: null }
  });

  // 3. Hard-delete records with no retention obligation
  await db.preferences.deleteMany({ where: { userId }});
  await db.sessions.deleteMany({ where: { userId }});
  await db.notifications.deleteMany({ where: { userId }});

  // 4. Files
  await deleteAllUserUploads(userId);

  // 5. Third-party processors — propagate via their APIs
  await mailgunApi.removeContact(user.email);
  await stripeApi.customers.delete(user.stripeCustomerId);
  await intercomApi.users.archive(user.intercomId);

  // 6. Backups — flag for purge on next cycle
  await db.backupPurgeQueue.create({ userId, scheduledFor: nextBackupCycle });

  // 7. Finally, remove the user record itself
  await db.users.delete({ where: { id: userId }});
}
```

Patterns:

- **Retention exceptions exist** — tax law, fraud prevention, ongoing-litigation hold. Anonymize rather than delete in those cases. Document the exception per field.
- **Backups are the awkward part.** Most teams cannot delete from immutable backup archives without restoring everything; the accepted approach is to keep a "delete on restore" pipeline so any restore re-applies the deletion list. Document this in your privacy policy.
- **Propagate to every processor** in your inventory. This is why the inventory exists.
- **Soft-mark first, then delete** — gives you a window to abort if the request was forged.

## Step 4 — Anonymization vs pseudonymization

- **Pseudonymization** — the identifier is replaced with a token, but the mapping exists somewhere (e.g. `user_842` instead of `alice@example.com`). Re-identification is possible if you have the mapping. Still considered personal data under GDPR.
- **Anonymization** — re-identification is not reasonably possible. The data is no longer personal data and outside GDPR scope.

True anonymization is harder than it sounds. Removing names doesn't anonymize if a single record can be uniquely identified (e.g. "person aged 47, working in Eisenstadt, with a Tesla" might be one person).

Use pseudonymization in development / staging / analytics. Reserve true anonymization for data leaving the EU regime entirely.

## Step 5 — Log scrubbing

Logs are often the worst PII leak. The app sanitizes inputs; the logger doesn't know about that.

```ts
// Log middleware — strip known sensitive headers before recording
function safeReqLog(req) {
  return {
    method: req.method,
    path: req.path,
    ip: hashIp(req.ip),                      // hash, not raw
    userAgent: req.headers['user-agent'],
    requestId: req.headers['x-request-id'],
    // Explicitly NOT: authorization, cookie, body
  };
}

// JSON loggers — strip in serializer
const REDACT_KEYS = new Set(['password', 'token', 'cookie', 'authorization', 'email', 'phone']);
function redactingReplacer(key, value) {
  return REDACT_KEYS.has(key.toLowerCase()) ? '[REDACTED]' : value;
}
```

Rules:

- **No bodies in access logs.** Bodies leak passwords on login routes, payment data on checkout, PII on profile updates.
- **Hash or truncate IPs** — full IPv4 is borderline PII per several DPAs. `xxx.xxx.xxx.0` or HMAC-with-rotating-key is safer.
- **Redact known-PII fields** in structured logs by key name.
- **Log retention bounded** — see [`log-strategy`](../log-strategy/SKILL.md). 30 days hot is plenty for most operational needs; longer needs justification.
- **Audit logs** (auth events etc.) get separate, longer retention because they support investigations — but still strip body content.

## Step 6 — Breach notification (72 hours)

Article 33 requires notifying the supervisory authority **within 72 hours** of becoming aware of a personal-data breach. Article 34 requires notifying affected data subjects if the breach is likely to result in "high risk to the rights and freedoms" of individuals.

Engineering preparations:

- **Define "becoming aware"** in your IR runbook — typically confirmation, not first suspicion. See [`incident-response`](../incident-response/SKILL.md).
- **Pre-draft the notification format** — supervisory authorities (Datenschutzbehörde, Bundesbeauftragte) publish templates. Pre-fill the org info; per-incident fields go in at incident time.
- **Inventory lets you scope fast** — "what data was affected" must be answerable in hours, not days. The inventory from step 1 is what makes this possible.
- **Notification can be staged** — first notice in 72h with what you know, follow-ups as you learn more. Better than missing the deadline waiting for full clarity.

## Step 7 — Sub-processors (DPA / AVV)

Every third party that processes personal data on your behalf — analytics, email, CRM, support, AI, CDN, hosting — is a sub-processor and requires a **Data Processing Agreement (DPA, German: AVV)** before going live.

Engineering responsibilities:

- **Maintain the sub-processor list** — public-facing in most jurisdictions. Update before you wire in a new service.
- **Vet new processors** — security posture, GDPR commitments, sub-sub-processors, location, certifications (ISO 27001, SOC 2). Document the review.
- **Implement consent / contractual basis** — analytics typically needs consent (see DACH cookie consent in [`dach-compliance`](../dach-compliance/SKILL.md)); transactional email is usually contract-based and does not.

## Step 8 — Cross-border transfers

EU personal data leaving the EEA needs a transfer mechanism: adequacy decision, Standard Contractual Clauses (SCCs), or a derogation. The post-Schrems-II / Data Privacy Framework landscape changes; check current status before relying on US transfers.

Engineering knobs:

- **EU-region defaults** for cloud services (AWS Frankfurt, GCP europe-, Azure West Europe, Cloudflare EU-data-localization)
- **Data residency** on managed Postgres / Mongo etc. — pick EU region at provisioning, document
- **CDN / edge caches** may replicate globally — consider an EU-only edge for sensitive paths

## Quick checklist

Engineering preparation for a GDPR audit / SAR / breach:

- [ ] Data inventory exists, is version-controlled, is up to date
- [ ] SAR endpoint or admin tool produces an export programmatically
- [ ] Deletion endpoint exists; covers DB, files, third parties, backups (via flag)
- [ ] Logs do not contain bodies or unredacted PII
- [ ] IP addresses in logs are hashed or truncated
- [ ] Sub-processor list is current; DPAs/AVVs in place before integration
- [ ] EU-region defaults for storage / compute
- [ ] Breach notification template pre-drafted, owner assigned
- [ ] Privacy policy mentions retention periods and backup-purge approach
- [ ] Anonymization vs pseudonymization is intentional, documented per use

## What this skill will not do

- Provide legal advice — talk to a DPO / data-protection lawyer for borderline cases
- Help process data without a lawful basis
- Recommend skipping the SAR or deletion endpoints "until we get bigger"
