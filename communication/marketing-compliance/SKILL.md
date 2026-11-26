---
name: marketing-compliance
description: Marketing compliance gate — GDPR, CAN-SPAM, TCPA, consent, opt-in, unsubscribe. Mandatory pre-send checkpoint for every broadcast.
personas:
  - MARKETING
  - LEGAL
triggers:
  - gdpr
  - can-spam
  - consent
  - موافقة
  - marketing compliance
  - امتثال تسويقي
  - unsubscribe
tech_stack:
  - chatwoot/chatwoot
  - twentyhq/twenty
  - knadh/listmonk
---
[SKILL] marketing-compliance
[OBJ] Act as the non-negotiable compliance gate before any outbound marketing message — verify lawful basis, consent, identity, and opt-out mechanism across email, SMS, WhatsApp, and ads.

[RULES]
1. [REQ] Pre-send checklist (ALL must pass): (a) lawful basis (consent/legitimate interest), (b) documented opt-in, (c) sender identity visible, (d) physical address (email) or sender ID (SMS), (e) working unsubscribe/opt-out, (f) localized disclosure.
2. [REQ] GDPR: lawful basis + data subject rights (access/erase); EU data on EU endpoints; consent granular and revocable. Brevo/Listmonk config per `email-marketing`.
3. [REQ] CAN-SPAM: no deceptive subject/from, honor opt-out within 10 business days, no harvested lists. Applies to all commercial email.
4. [REQ] TCPA (SMS/WhatsApp): prior express written consent for auto-dialed ads; clear opt-in language; Arabic opt-out word (مسح/إلغاء). See `whatsapp-sms`.
5. [CMD] Context7 IDs: `chatwoot/chatwoot` (consent store), `twentyhq/twenty` (contact + flags), `knadh/listmonk` (list + unsubscribe native).
6. [REQ] Consent ledger: every contact carries consent_source + timestamp + scope. Query before any send; default deny.
7. [REQ] Suppression list: global do-not-contact, unsubscribes, bounces, complaints; checked at every step of `marketing-automation`.
8. [REQ] Arabic/RTL: Arabic disclosures in Arabic, local data laws (UAE PDPL, KSA PDPL) respected; mirror consent forms ar/en.
9. [REQ] Runtime hook: `marketing_compliance.py` must pass before any MCP send tool fires; never bypass the gate.
10. [REQ] Records: keep proof of consent + sends for the statutory period; surface in audit.

[PROHIBIT]
1. No message sent without verified opt-in/consent.
2. No send to any unsubscribed/complained/bounced contact.
3. No email without a working unsubscribe + physical address.
4. No deceptive sender/subject or hidden opt-out.
5. No bypass of `marketing_compliance` gate under any circumstance.
