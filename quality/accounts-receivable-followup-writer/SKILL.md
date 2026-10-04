---
name: accounts-receivable-followup-writer
description: "Draft escalating invoice reminder sequences (gentle→neutral→firm→final) from invoice details and client relationship context. Preserves relationships while collecting payment. Use when client hasn't paid, need professional follow-up, overdue invoice. Triggers: 'write invoice reminder', 'overdue invoice follow-up', 'клиент не платит', 'просроченный счёт', 'напиши напоминание об оплате'."
version: 1.0.0
---

# Accounts Receivable Follow-up Writer

This skill generates an escalating sequence of 4 invoice reminder messages — from gentle to final notice — calibrated to the relationship context and days overdue. It operates bilingually (EN/RU) on data provided by the user; no accounting software required.

**Input:**
- Invoice details: amount, currency, due date (or days overdue), client name
- Relationship context: new / long-term / valuable / difficult / other
- Optional: prior contact history, formality preference

**Output:**
- 4 numbered messages (subject line + body + send-date recommendation + tone note)
- Relationship risk flag if applicable
- Human-review reminder footer

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Parse and Validate Input

1. Extract required fields from user input:
   - Invoice amount and currency
   - Due date or days overdue
   - Client name or company
   - Relationship context (new / long-term / valuable / difficult / other)

2. Check for required fields:
   - If invoice amount OR client name is missing: stop and return error message (see Negative Cases)
   - If due date is missing: proceed but flag in output ("Due date not provided — add before sending")

3. Extract optional fields if provided:
   - Prior contact history (e.g., "already sent one email", "called twice, no answer")
   - Formality override (formal / neutral / casual)
   - Single-message request (e.g., "just give me the final notice")

### Step 2: Determine Escalation Starting Level

1. Calculate days overdue (from due date to today, or use user-stated value)
2. Map to starting tone:
   - 1–14 days overdue → start at **Gentle** (Message 1)
   - 15–30 days overdue → start at **Neutral** (Message 2)
   - 31–60 days overdue → start at **Firm** (Message 3)
   - 60+ days overdue → start at **Final** (Message 4); include legal note
3. Note: If prior contact history is provided, advance starting level by one step (e.g., "already sent a reminder" → start at Neutral, not Gentle)

### Step 3: Apply Relationship Context Modifier

1. Read relationship context:
   - **New client / unknown:** Standard escalation; professional but impersonal
   - **Long-term / valued partner:** Warm tone throughout; add explicit relationship-preservation note in Messages 3 and 4
   - **Difficult history:** Formal from Message 1; reference any prior agreements in Message 3
   - **Close / friend-level:** Maximum warmth; avoid implying distrust; recommend direct call after Message 2
2. If context suggests high-stakes relationship: add `⚠️ Relationship risk note` before Message 3 and 4

### Step 4: Generate Message 1 — Gentle Reminder

1. Tone: friendly, assumes the invoice was overlooked; no accusation
2. Structure:
   - Subject line: warm, non-confrontational ("Quick note about Invoice #___")
   - Opening: acknowledge the relationship; reference invoice briefly
   - Body: simple reminder with invoice details; offer to resend if needed
   - Closing: friendly, leaves door open
3. Include send-date: "Send immediately" or "Day 1"
4. Add tone note: 1 sentence explaining why this tone was chosen

### Step 5: Generate Message 2 — Neutral Follow-up

1. Tone: professional, matter-of-fact; no emotional charge
2. Structure:
   - Subject line: direct but not alarming ("Following up: Invoice #___ — [Amount] due")
   - Opening: reference that Message 1 went unanswered (if applicable)
   - Body: restate invoice details; offer payment options or clarification
   - Closing: clear ask with soft deadline ("by end of this week")
3. Include send-date: "5–7 days after Message 1"
4. Add tone note

### Step 6: Generate Message 3 — Firm Notice

1. Tone: direct, professional; references prior outreach; sets firm deadline
2. Structure:
   - Subject line: urgent ("Action Required: Invoice #___ — [Amount] [X days] Overdue")
   - Opening: note that previous reminders went unanswered
   - Body: state invoice details, total owed, exact deadline (specific date); request confirmation of payment or communication
   - Closing: firm but professional; no threats
3. If valued/long-term relationship: add note "I value our working relationship and want to resolve this directly"
4. Include send-date: "7–10 days after Message 2"
5. Add tone note + relationship risk flag if applicable

### Step 7: Generate Message 4 — Final Notice

1. Tone: formal; references consequences; requests immediate action
2. Structure:
   - Subject line: formal ("Final Notice: Invoice #___ — Payment Required by [Date]")
   - Opening: formal notice; reference all prior outreach
   - Body: final deadline (specific date); state consequences (late fees, collections, legal referral — only include what user has authority over); offer one last opportunity to resolve
   - Closing: formal sign-off; no further reminders implied
3. If 60+ days: add note "Consider consulting a collections specialist or legal counsel before proceeding further"
4. Include send-date: "10–14 days after Message 3"
5. Add tone note

### Step 8: Format and Output

1. Assemble all generated messages in sequence
2. Add sequence header with summary (client name, amount, days overdue, relationship context, escalation starting level)
3. Add relationship risk flag(s) if applicable (before Messages 3 and 4)
4. Add human-review footer
5. If user requested only one specific message: output that message only with a note indicating its escalation stage

---

## Output Format

```
## Invoice Reminder Sequence: [Client Name] — [Amount] [Currency] overdue [X days]

**Relationship context:** [stated context]
**Escalation starting level:** Message [N] ([Tone])
**Prior contact:** [yes/no — summary if yes]

---

### Message 1 — Gentle Reminder
**Subject:** [subject line]
**Send:** Day 1 / immediately
**Tone note:** [1 sentence]

[Message body]

---

### Message 2 — Neutral Follow-up
**Subject:** [subject line]
**Send:** 5–7 days after Message 1
**Tone note:** [1 sentence]

[Message body]

---

⚠️ Relationship risk: [note if applicable]

### Message 3 — Firm Notice
**Subject:** [subject line]
**Send:** 7–10 days after Message 2
**Tone note:** [1 sentence]

[Message body]

---

⚠️ Relationship risk: [note if applicable]

### Message 4 — Final Notice
**Subject:** [subject line]
**Send:** 10–14 days after Message 3
**Tone note:** [1 sentence]

[Message body]

---

⚠️ Review before sending. Add your invoice reference number, company name, and contact details. If the relationship is high-stakes, have a colleague review Messages 3 and 4 before sending.
```

---

## Edge Cases

1. **Missing due date:** Generate sequence; add note "Due date not provided — insert before sending." Use "overdue" framing without a specific number of days.
2. **Very close relationship ("we're friends"):** Apply maximum warmth across all 4; recommend a direct phone call after Message 2; add explicit risk note before Message 4.
3. **60+ days overdue:** Start sequence at Message 3 or 4 (user's choice); always add the legal/collections note to Message 4.
4. **Single message requested:** Output only the requested message with its escalation context; skip the full sequence.
5. **Prior contact stated:** Advance starting tone level by one step; reference prior outreach in the first generated message.
6. **Mixed-language input:** Detect user interface language; output in that language; offer the other-language version on request.

---

## Negative Cases

All error and decline messages must be delivered in the detected language (EN or RU), following the Language Detection rule above.

- **Missing amount or client name:** Stop. Return in the detected language:
  - EN: "Invoice amount and client name are required. Please provide: amount, client name, and ideally the due date."
  - RU: "Необходимо указать сумму счёта и имя клиента. Пожалуйста, предоставьте: сумму, имя клиента и желательно срок оплаты."
- **Aggressive or threatening language requested:** Decline in the detected language. Note that threatening language may create legal liability and damage the relationship. Offer firm Message 4 as the strongest professional alternative.
- **Payment dispute described (not simple non-payment):** Flag in the detected language that this sounds like a payment dispute rather than a simple overdue invoice, and that a reminder sequence may not be appropriate — recommend dispute resolution communication instead.
