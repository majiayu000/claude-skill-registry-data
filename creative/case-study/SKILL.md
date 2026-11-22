---
name: case-study
description: >-
  Case Study. Turns the first customer into proof, with their permission. Once the product has shipped, it
  writes a short before-and-after from their real numbers and their real words, and keeps it marked as a
  draft until they have approved that exact text in writing. Change a word and it asks again. Use when the
  user says "case study", "testimonial", "customer story", "get a quote from them", "write up the result",
  "social proof", "can I use their name", or once a customer has seen results.
argument-hint: "[draft <deal> | approve <deal> | check <deal>]"
---

# case-study

Before you have customers, you sell on the demo and the refund. After you have one, you sell on them. One real
story, with a name and a number, is worth more than anything you could write about yourself. But it's a claim
about a real company, so it has to be true and it has to be theirs to give.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/casestudy.py" draft --deal north-pier --before "Paid \$6,400 a month to chase invoices" \
    --after "Cancelled the collections service" --source "North Pier's own numbers, Jan 2027" \
    --quote "We stopped thinking about late invoices." --quote-by "Renee Alvarez, CFO"
python3 "${CLAUDE_SKILL_DIR}/casestudy.py" approve --deal north-pier --said "Approved, go ahead." --at 2027-02-10
python3 "${CLAUDE_SKILL_DIR}/casestudy.py" check --deal north-pier
```

## Steps

1. **Wait for a result.** `draft` refuses until the deal is `delivered` (`/pre-sale deliver`). Give it long enough to have a real number.
2. **Ask first.** "Send this to Renee: would you be open to a short write-up, if you approve every word? Reply yes or no." A no is fine, and it ends here.
3. **Get the real numbers from them.** Before and after, and where they came from. Ask what changed, in their words: "What's different now?"
4. **Draft.** `casestudy.py draft`. It writes `whale/case-studies/<deal>.md` with a DRAFT line at the top. Keep it under 150 words. A quote is what they
   actually said or wrote, word for word, with their name. Don't tidy it into something they wouldn't say.
5. **Send them the exact text.** "Send this to Renee for approval? Reply yes or no."
6. **Log their approval.** `casestudy.py approve --said "<their words>"`. It removes the DRAFT line, for this text only.
7. **Check before every use.** `casestudy.py check`. If the text changed after they approved it, it says to ask again.
8. **Use it.** On the next pitch, in `/offer-builder`, on the launch page. Only then does the "you'd be one of the first" answer in `/objection-handler` change.

## What makes it believable

- **A real name and a real company,** if they agree. If they'd rather not be named, say "a regional freight company" and keep the number.
- **One number.** "Cancelled a $6,400-a-month service" beats a list of adjectives.
- **The bad part.** What was hard before, or what took longer than expected. It's how people know it's true.
- **Typical, or not.** If one customer's result is unusually good, don't suggest everyone gets it. The FTC treats testimonials as claims you must be able to back up.

## Example from the reel's board

After North Pier Logistics has the product: Before, paid $6,400 a month to chase invoices. After, cancelled the collections service. Quote: "We stopped
thinking about late invoices." Renee Alvarez, CFO. It stays a draft until Renee approves it. (Illustrative: this result and this quote are made up to show
the format, and North Pier and Renee are fictional. Your case study uses only what your customer gives you.)

## What it never does

- Never writes a case study before delivery, and never makes up a quote, a number or a logo.
- Never publishes or sends anything without a yes, and never uses a draft their approval doesn't cover.
- Never presents a pre-sale payment as a result. "They paid" is not "it worked".

## Consent and truth

- Nothing is sent or published without the user's explicit yes for that exact message, and the customer's written approval of that exact text. One yes per message. Never "yes to all".
- Stop at the first "no". Not wanting a case study never affects how the customer is treated.
- Never invent a number, a result, a client or a quote. If they withdraw their approval, take it down.
