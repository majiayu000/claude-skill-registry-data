---
name: whatsapp-messaging
description: Use when working on WhatsApp message sending — templates, 24h session window, opt-in, Hebrew tone. Covers `send_whatsapp_message` tool and WhatsApp client.
---

# WhatsApp Messaging skill

## When to invoke

- Touching `src/tools/send-whatsapp-message.ts`
- Touching `src/integrations/whatsapp/`
- Composing customer-facing Hebrew messages
- Designing WhatsApp templates

## Hard rules (from spec)

1. **Outside 24h session window** → only **approved templates** can be sent
2. **Inside 24h session** → free-form text allowed
3. **Always log** every outbound message (CRM + internal log)
4. **Respect opt-in** consent — never send to users who opted out
5. **Never spam** — rate-limit per customer, deduplicate identical messages within short window

## Tone (Hebrew)

- Warm, professional, **not** overly formal ("שלום" + first name, not "אדון/גברת")
- Concise — WhatsApp messages should be short
- No jargon unless the customer used it first
- Sign off with the human advisor's name when appropriate

## Approved use cases (templates)

- Appointment reminders
- Missing document requests
- Process completion notifications
- Parking instructions for office visits
- Follow-up reminders

## Error handling (from spec)

If WhatsApp fails: retry once → fall back to email
