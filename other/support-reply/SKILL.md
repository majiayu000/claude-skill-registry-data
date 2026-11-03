---
name: support-reply
description: Draft a reply to one support ticket or conversation — classified, checked against the support policy and escalation rules, in the brand's voice — ready for an agent to send. Use when the user pastes or names a customer message and wants an answer they can send. Not for building saved replies for every contact reason; see /support-macros.
metadata:
  argument-hint: "<ticket or file> [project]"
---

# Reply

Draft a reply to the ticket in "$ARGUMENTS". The draft is for an agent to check and send; never send anything yourself.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

The ticket: pasted text, or a file path in `$ARGUMENTS`. When `$ARGUMENTS` or the request names a project, use that name as `<project>` whether or not its folder exists yet in `.singularskills/support/` (create it when you write). With no project named: with exactly one folder there, use it; with several, ask which; with no folder at all, read none of the files below and continue.

Read whichever of these exist; none is required:

- `.singularskills/support/<project>/02-taxonomy.md` for the categories and priorities
- `.singularskills/support/<project>/04-macros.md` for the voice, the `## Policies` section and the macros
- `.singularskills/support/<project>/03-knowledge.md` for articles to link
- `.singularskills/support/<project>/05-escalation.md` for when a ticket must go to someone else
- `.singularskills/branding/<project>/03-verbal.md` for the brand's voice, when `04-macros.md` has none

## Process

1. **Read the ticket** and say in one line what the customer wants and what has gone wrong, if anything.

2. **Check for a security incident first.** If the ticket suggests account takeover, unauthorised access, exposed data or a breach, do not draft a reassuring reply: say "possible security incident", say it must go to the security contact now, and name `/security-incident-response`. Draft only a short holding reply that confirms receipt and promises nothing, for the security contact to approve.

3. **Classify it** with the taxonomy if there is one: category, priority (P1 to P4) and the one-line reason. Without a taxonomy, give your best category and priority and say there is no taxonomy.

4. **Decide whether to escalate** using `05-escalation.md` when it exists: if a trigger matches, say who should take the ticket and what to hand over, and draft the reply the customer gets at the handoff instead of an answer.

5. **Find the policy for what the customer asks.** If the ticket asks for something the team would give (a refund, a credit, an extension, a replacement, a date), find the line in the `## Policies` section of `04-macros.md` that covers it. With no line, ask the user for that policy once. With no answer, the draft promises nothing about it, says who will decide and when the customer will hear back, and you name the missing policy above the draft.

6. **Draft the reply:** start from a matching macro if there is one; answer what was asked, in the brand's voice; link a knowledge-base article where one answers it; and, when something went wrong, pass the checklist in `references/service-recovery.md`. Offer only what a policy line allows. Leave placeholders in angle brackets for anything the agent must fill in or check (`<order date>`).

7. **Protect personal data:** do not repeat the customer's email address, phone number, payment details or account number in the reply, and leave out internal notes and other customers' details.

## Output

In chat, above the draft:
- Category and priority, with the reason
- Escalate or answer, and to whom
- The policy line the reply relies on, or the missing policy
- Anything the agent must check before sending

Then the draft reply, ready to paste. This skill writes no file.
