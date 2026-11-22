---
name: requirements
description: >-
  Requirements. Turns what paying customers asked for into the build list. Captures each ask in their own
  words with the feature it becomes, merges the same feature across customers, and ranks the list by how
  much paid money is behind each line, so you build exactly what was paid for and nothing else. Asks from
  people who haven't paid wait on a separate list. Logs each customer confirming the list, and marks
  features done. Use when the user says "what should I build", "requirements", "build list", "they asked
  for", "what did they want", "scope", "spec", "feature requests", or right after a customer pays.
argument-hint: "[add <deal> | list | build | confirm <deal> | done <feature>]"
---

# requirements

Most products fail because the founder guessed. Here nobody guesses: every line traces back to a company that
paid and said what they need. That list is the product.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/reqs.py" add --deal north-pier --ask "Sync with QuickBooks" --feature "QuickBooks sync"
python3 "${CLAUDE_SKILL_DIR}/reqs.py" list --deal north-pier
python3 "${CLAUDE_SKILL_DIR}/reqs.py" build
python3 "${CLAUDE_SKILL_DIR}/reqs.py" confirm --deal north-pier --said "Yes, that's what we need." --at 2026-11-04
python3 "${CLAUDE_SKILL_DIR}/reqs.py" done --feature "QuickBooks sync" --at 2026-11-20
```

## Steps

1. **Ask right after they pay.** While it's fresh, on a call or by email. Three questions do most of it:
   - "Walk me through what happens today, from the invoice going late to the money coming in."
   - "What would have to be true for you to cancel what you pay for now?"
   - "What else has to work with this?"
2. **Write down their words.** `reqs.py add --ask` is what they said, close to word for word. `--feature` is what it becomes.
   Same feature, same name: that's how asks merge across customers.
3. **Build the list.** `reqs.py build` writes `whale/requirements.md`: features by the paid money behind them, each with who asked
   and how they said it. What someone who hasn't paid asked for goes under Later.
4. **Send it back to them.** Show the user the customer's own list, then "Send this to Renee to confirm? Reply yes or no." Their
   reply goes in with `reqs.py confirm --said "<their words>"`. This is your scope in writing, and it protects you both.
5. **Say no when it's a no.** If an ask can't be built by the promised date, tell the customer now and agree what happens. Move the
   date only with their yes (`/pre-sale new-date`), or refund them. Never quietly drop it.
6. **Build.** Claude can start on the list. `reqs.py done` marks each feature, for everyone who asked. `/launch-planner` tracks the dates.

## Reading the list

- **Top of the list:** several customers asked, or one big one did. Build it first.
- **One customer, small money, big job:** ask if it's a must-have before the ship date, or can come after.
- **Under Later:** a real signal, not a commitment. Ask if they would pay for it.
- **Nobody asked:** it isn't on the list, however good the idea is. Build that after they have what they paid for.

## Example from the reel

North Pier's requirements, ask to feature: "Text the customer first, then email" to Text + email sequence. "Sync with QuickBooks" to
QuickBooks sync. "Escalate after 30 days" to Auto-escalation at 30 days. "Weekly report to the CFO" to Monday CFO report. On the example
board, Saltmarsh and Copperline ask for some of the same, so QuickBooks sync has $42,000 behind it and goes first. (Illustrative: every
company and ask is fictional. QuickBooks is a real product, and using its name here implies no connection to it.)

## What it never does

- Never adds a feature nobody asked for, and never puts words in a customer's mouth.
- Never logs a confirmation they didn't give.
- Never drops a paid-for feature without telling the customer.

## Consent and truth

- Nothing is sent, built or promised without the user's explicit yes for that exact message. Claude drafts, the user says "yes", then
  it goes out from the user's own accounts. One yes per message. Never "yes to all".
- A customer's requirements are private to that customer. Never show one customer's list or name to another without their okay.
- Never invent a number, a result, a client or a deadline.
