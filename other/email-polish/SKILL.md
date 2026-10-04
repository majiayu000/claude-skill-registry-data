---
name: email-polish
version: 1.0.0
description: Rewrite a blunt or rough email draft into a warm, friendly-but-professional version - tone and clarity improved, intent, facts, names, dates, and requests preserved exactly.
triggers:
  - polish this email
  - email-polish
  - make this email sound better
  - rewrite my email
  - friendly professional email
capabilities: []
inputs:
  - name: raw_email
    required: true
    description: The owner's draft email text to polish.
  - name: recipient
    required: false
    description: Who the email is going to (name/role) to calibrate formality.
  - name: context
    required: false
    description: Any extra situational context (relationship, prior thread, goal).
---

# Email Polish

## When to use
Use this when you have a rough, blunt, terse, or frustrated email draft and want it to read as friendly but professional - warm, clear, respectful - without changing what it actually says.

**Not for:** writing an email from scratch when there is no draft or intent to work from (you would have to invent the content); translating between languages; or softening a message whose whole point is to be firm and formal, such as a legal notice or final warning - there, over-warming the tone defeats the purpose. Do not use it to add commitments, dates, or promises the owner did not make.

## Method
1. **Read the draft and extract three things:** the core ask, the key facts (names, dates, numbers, links), and the emotional register.
2. **Calibrate formality from the recipient.** *Decision point:* unknown / senior / external -> "Hi Dr. Lee," and no slang; known colleague -> "Hey Sam," relaxed close; recipient unknown -> default to a safe friendly-professional register.
3. **Rewrite paragraph by paragraph,** keeping the original structure unless it is genuinely unclear. Warm opening (one friendly line, not gushing), direct middle, courteous close.
4. **Preserve every fact verbatim.** Names, dates, numbers, links, requests carry over unchanged. *Decision point:* if a needed detail is missing (a meeting time), insert a clear placeholder like `[time]` rather than guessing.
5. **Fix grammar, spelling, and awkward phrasing.** Cut corporate filler ("per my last email", "circling back"). Never let the tone turn passive-aggressive; keep a frustrated draft firm but not sharp.
6. **Ensure a subject line exists;** propose one if absent. Match length to the original - a two-liner stays short.

## Example
**Input (raw):** hey need the report by friday its late again. send it.

**Output:**
```
Subject: Report - Friday deadline

Hi [name],

Hope you're doing well. Quick note - could you get the report over to
me by Friday? It's slipped a couple of times now, so I want to make
sure we stay on track this week.

Thanks a lot,
[Your name]
```

## Pitfalls
- **Scope creep.** Adding a promise, apology, or deadline the owner never wrote turns a polish into a fabrication.
- **Padding.** Inflating a two-line note into five paragraphs of pleasantries wastes the reader's time.
- **Guessing missing facts.** Inventing a time or name instead of leaving a marked placeholder.
- **Buried point.** So much warmth up front that the actual ask disappears; keep the middle direct.

## Output format
```
Subject: <line>

<polished email body: warm open, direct middle, courteous close>

Notes: <only if placeholders were inserted or a judgment call was
made; omit this line entirely otherwise>
```
