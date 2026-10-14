---
name: sms-pro
description: Use SMS professionally — business texting etiquette, alerts, 2FA-adjacent flows, and compliant organizational messaging.
category: enterprise-communication
---

## Overview

SMS in professional contexts means transactional and operational messaging: alerts, reminders, coordination, and time-sensitive notifications — not marketing blasts (see sms-marketer for that). This skill covers business texting: etiquette, alert design, automation, and the compliance basics for organizational SMS.


Professional SMS — appointment reminders, delivery updates, authentication codes, urgent alerts — reaches people faster than any other channel: 90%+ read within minutes. That speed makes it ideal for time-critical operational messaging and terrible for anything that can wait. The skill is reserving SMS for moments where immediacy genuinely matters.
## When to use

- Setting up operational SMS alerts
- Writing appointment/service reminders
- Coordinating teams via text
- Designing notification SMS (deliveries, incidents, system alerts)
- Establishing business texting policies
- Choosing SMS for internal vs. external comms

- Appointment reminders and confirmations
- Two-factor authentication and security alerts
- Urgent operational notifications (outages, delays)
- Implementing SMS APIs for developers
- Building international SMS coverage
- Choosing SMS providers
## Core concepts

**SMS role in the mix.** SMS is for: time-sensitive alerts, reminders, short coordination, and 2FA/verification codes. It's not for: long discussions (use email/chat), sensitive data (use secure channels), or anything non-urgent (respect the interruption).

**Alert design.** Critical alerts: what happened, impact, what to do, where to go — in 160 characters. Include severity, avoid jargon, link to details. Alert fatigue is real: only truly actionable items via SMS; everything else via less intrusive channels.

**Reminders.** Appointment/service reminders: who, what, when, where, how to confirm/cancel/reschedule. Send at useful intervals (24h + 2h typical). Two-way (reply C to confirm) dramatically reduces no-shows.

**Business texting etiquette.** Identify yourself/organization, keep it brief, respect hours (no non-urgent texts outside business hours), one topic per message, and provide an opt-out path. Professional tone — texts feel personal, so sloppiness stands out.

**Automation.** Triggered SMS from systems: monitoring alerts, scheduling systems, delivery updates, incident notifications. Build in: deduplication (don't send the same alert 50 times), escalation (unacknowledged → next person), and quiet hours with critical-override rules.

**Compliance basics.** Consent for non-transactional messages, opt-out honoring (STOP), sender identification, and data retention policies. Transactional messages (alerts the user signed up for) have lighter requirements than promotional — but document consent either way. Consult legal for your jurisdiction.


**Transactional vs. promotional.** Transactional SMS (order updates, codes, alerts) enjoys high tolerance because it is expected and useful. Promotional SMS faces strict consent requirements and low tolerance. Never blur the line — sending marketing in transactional streams triggers complaints and regulatory risk.

**Sender identity.** Short codes (5–6 digits, high throughput, expensive), long codes / 10DLC (standard numbers, conversational, US carrier-registered), and alphanumeric sender IDs (international, one-way). Choose by use case: 10DLC for conversational business texting, short codes for high-volume alerts, toll-free for support lines.

**Quiet hours and frequency.** Even transactional messages respect local quiet hours (typically 8am–9pm). Frequency expectations: authentication = instant, appointments = 24h + 2h reminders, alerts = only when actionable. Every unnecessary text trains recipients to ignore the necessary ones.

**Provider selection.** Evaluate: delivery rates by country, latency, pricing (per-segment, not per-message — segments matter), API quality, support responsiveness, and compliance features.
Test with real traffic before committing — provider performance varies enormously by destination.
Multi-provider setups hedge outages but add complexity.
**Encoding and segmentation.** GSM-7 (160 chars/segment) vs. Unicode (70 chars/segment) — emojis and non-Latin scripts triple costs.
Concatenate carefully; long messages cost multiples.
Character counters in composing UIs prevent surprise bills.
**Delivery monitoring.** Delivery receipts (DLRs), latency tracking, failure categorization (invalid number, carrier block, content filter), and retry logic.
Monitor by destination — country-level issues hide in global averages.
Alert on delivery drops; they indicate blocks or outages.
## Practical workflow

1. **Define use cases.** List what merits SMS: incident alerts, appointment reminders, delivery notifications, shift coordination, verification codes. Everything else uses other channels.
2. **Design message templates.** Per use case: concise template with variables, severity levels for alerts, and clear CTAs. Test readability — if it needs scrolling, it's too long.
3. **Set policies.** Quiet hours, opt-in/opt-out handling, who can send broadcast texts, tone guidelines, and data retention. Publish the policy.
4. **Build automation.** Integrate with source systems (monitoring, scheduling, ticketing). Implement: dedup, escalation chains, acknowledgment tracking, and delivery logging.
5. **Launch carefully.** Start with transactional use cases (lowest risk, highest value). Monitor: delivery rates, opt-out rates, response times, and complaint feedback.
6. **Review.** Monthly: are alerts actionable? (If routinely ignored, they're noise — fix or remove.) Opt-out trends, after-hours volume, and user feedback.

**Incident alert template:** "[SEV2] Payment API error rate 15% (threshold 5%). Dashboard: [link]. Ack: reply ACK. On-call: [name]."


**Appointment reminder sequence:** T-48h: confirmation request (reply YES to confirm) → T-24h: reminder with details (time, location, preparation) → T-2h: final nudge with check-in link. No-show rates typically drop 30–50% with this sequence. Include reschedule links — friction-free rescheduling beats no-shows.

**2FA SMS best practices:** 6-digit codes (memorable, auto-fillable) → 5–10 minute expiry → clear sender identification → "never share this code" warning → rate-limit requests (prevent SMS bombing) → offer authenticator-app alternatives. Monitor delivery rates by carrier — SMS 2FA fails silently on some networks.

**API integration checklist:** credentials secured → webhook endpoints for DLRs → retry logic with backoff → number validation pre-send → opt-out list syncing → rate limiting → test numbers across carriers → monitoring dashboards.
Load-test before campaigns — provider rate limits surprise the unprepared.
**Cost optimization:** validate numbers (remove landlines, invalid) → use correct encoding → batch where possible → negotiate volume pricing → monitor per-campaign costs.
SMS costs scale linearly — 10% waste reduction is real money at volume.
## Common pitfalls

- **Alert fatigue.** SMS for everything means SMS for nothing. Reserve for actionable and urgent.
- **No dedup.** 47 identical alerts at 3am. Deduplicate and escalate instead.
- **After-hours non-urgent texts.** Respect quiet hours; use scheduled sends for morning delivery.
- **Missing opt-out.** No way to stop messages. Always provide and honor opt-out.
- **Sensitive data via SMS.** Passwords, full account numbers, health details — SMS isn't secure. Use it for pointers, not payloads.
- **No acknowledgment tracking.** Sending critical alerts into the void. Track acks; escalate silence.
- **Inconsistent sender identity.** Messages from random numbers. Use consistent, identified sender IDs.
- **Using SMS for non-urgent content.** Newsletters via text. Reserve SMS for immediacy — everything else belongs in email or push.
- **No opt-out handling.** Failing to process STOP requests immediately. Regulatory penalties are severe and per-message.
- **Ignoring international complexity.** Sender ID rules, character encoding (GSM vs. Unicode segment limits), and pricing vary wildly by country. Test per market.
- **No DLR handling.** Sending blind without delivery confirmation. DLRs are the only truth about delivery — process them.
- **Single provider dependency.** Provider outages halt all messaging. Critical flows deserve failover providers.
