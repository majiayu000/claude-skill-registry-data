---
name: cold-call-opener
description: Turn a cold dial into a conversation. A permission-based opener plus ready objection turns for "not interested," "no time," "just send me info," and "we already use X," tuned to one persona. Built for B2B SDRs and full-cycle reps, customizable to your persona, offer, and dialer. Trigger on "write a cold call opener", "give me objection responses", "handle 'not interested'", "cold call script for this persona", or any live-dial prep.
---

# Cold-Call Opener

## What this does
Writes a short, permission-based opener that respects the fact you interrupted someone, plus the four turns you actually hit on the phone: the reflex brush-off, the no-time push, the "send me something," and the incumbent wall. Each turn keeps the call alive without fighting the prospect.

## What you'll need
You do not need to connect anything to get value today. Tell the skill who you are calling and what you do, and it runs now. Connect the tools below and it grounds the opener in the real account.

- Works today with: a persona, your one-line offer, and the objection you keep losing on. Paste it and go.
- More powerful connected to a CRM: it reads the account and any prior touches so the opener references a real reason to call.
- Sharper with an enrichment tool: pulls the role and current stack so the "we already use X" turn names the right incumbent.
- Sharper with a dialer or call tool: lets you save the openers and turns as snippets for the persona you dial most.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on what you tell it today and gets sharper as you connect tools. It never invents a detail about the account it cannot see. A missing fact is a question, not a guess.

- **Bring your data**: name the persona and the offer. The skill writes the opener and the four turns now, grounded only in what you gave it.
- **Connect your tools**: the same skill reads the account and stack so the opener has a real hook and the incumbent turn names the actual tool.
- **Just exploring**: no target yet? Get the opener structure, the objection map, and a worked example on a sample persona, so you see the shape before you dial.

Every run ends with the one thing that would make the next call sharper, a fact to add or a tool to connect.

## Customize this for yourself
This was built for B2B phone outbound into a named persona. Set these to your motion:

| Set this | What it is | Default / Example |
|---|---|---|
| PERSONA | who picks up | AE, RevOps lead, Support manager |
| OFFER | the one problem you solve | stated in the prospect's words |
| PERMISSION_LINE | how you ask for 30 seconds | "did I catch you at an okay time?" |
| INCUMBENT | the tool they likely already use | a category tool, named if known |
| TONE | how direct you run | plain and calm, never pushy |
| CRM | your CRM connector | a CRM you already run |
| DIALER | where you save snippets | a dialer or call tool you run |

Dial any persona you like. The skill builds the turns around your offer and the objection you actually lose on, not a generic gauntlet.

## The method

### Permission-based opener
Open by naming that you are a cold call, then ask for a small, honest slice of time. "I know I am interrupting, can I take 30 seconds and you tell me if it is worth more?" Candor lowers the reflex to hang up. No fake familiarity, no "how are you today."

### The pattern-interrupt, not the pitch
The opener earns the next 30 seconds by being specific and short, not by pitching. One reason you called this person, in one sentence, ending in a question that hands them control.

### Objection turns (the four you actually hit)
- **Not interested**: agree first, then ask one honest question. "Totally fair, most people say that before they have a reason to care. Can I give you the one reason I called and you decide?"
- **No time**: shrink the ask, offer the exit. "I believe you. Ten seconds now, or a better time to call back?"
- **Just send me info**: trade the send for one question, so the info is relevant. "Happy to. So I do not spam you, what is the one thing worth me including?"
- **We already use X**: validate the incumbent, find the gap. "Most people I call do. I am not calling to rip it out. Usually the gap is [angle], is that true for you too?"

### The graceful exit
Every turn has a version that ends the call cleanly if the answer is a real no. A fast, respectful exit protects the number and your reputation. No badgering.

## Quality gates
- The opener asks permission and admits it is a cold call. No fake rapport.
- Every objection turn agrees before it redirects. Never argue the prospect down.
- The "we already use X" turn names a gap, not a knock on the incumbent.
- Every turn has a clean exit. No third attempt after a real no.

## Output (example)
```
COLD CALL · RevOps lead · offer: cut manual pipeline hygiene

Opener:
"Hi [name], you don't know me, this is a cold call. Can I take
30 seconds to tell you why I called, then you tell me if it is
worth more? ... I called because RevOps teams your size usually
lose a day a week to manual CRM cleanup before forecast. Is that
a real thing for you, or have you solved it?"

Objection turns:
- Not interested -> "Fair. Most people say that first. One reason
  I called, then you decide?"
- No time       -> "Believe you. Ten seconds now, or better to
  call back Thursday?"
- Send me info   -> "Happy to. What is the one thing worth including
  so it is not noise?"
- Already use X  -> "Most people do. Not calling to replace it. The
  gap is usually [angle]. True for you?"
```

## Where the inputs come from
PERSONA, OFFER, and INCUMBENT are yours to set; the 30-second permission ask and the four-objection map are defaults that suited high-volume phone outbound, not laws. A slower, exec-only motion can lengthen the opener. The structure holds. The inputs are yours.

## Example chat
Here is the skill running on a real persona ahead of a dial session.

**You:** Write me a cold call opener for a RevOps lead. We cut manual pipeline hygiene work.

**Claude:** Here's the opener and the turn you'll need most on this persona.
```
Opener: "Hi [name], you don't know me, this is a cold call.
Can I take 30 seconds to tell you why I called, then you tell
me if it's worth more? ... RevOps teams your size usually lose
a day a week to manual CRM cleanup before forecast. Real thing
for you, or already solved?"
```
The permission ask matters more than the pitch here. Naming that it's a cold call up front lowers the reflex hang-up, which is the actual failure point on this persona, not the offer itself. One sharpener: tell me who they likely already use for pipeline hygiene, right now the "we already use X" turn is generic instead of naming the real incumbent.

**You:** They usually use a spreadsheet, not a tool. Adjust the objection turn.

**Claude:** Updated the incumbent turn to match.
```
"Already use X" turn -> "Most teams I call run this off a
spreadsheet, not a dedicated tool. Not calling to replace your
process, usually the gap is forecast accuracy slipping as the
team grows. True for you?"
```
Naming the spreadsheet instead of a competitor tool changes the whole turn, it validates what they actually have instead of guessing at a tool they don't use. One sharpener: connect your CRM so the opener can reference a real prior touch on this account instead of a cold, contextless open.

## Go further
The read is step one. Here's where an operator takes it once the manual version proves out.

- **Load it straight into the dialer.** Save the opener and the four objection turns as snippets in your dialer so reps pull them mid-call instead of paging through a doc.
- **Sharpen the incumbent turn automatically.** Connect an enrichment tool so the "already use X" turn names the real tool on record for that account, not a guess.
- **Turn call outcomes into the next version.** Feed Gong call recordings back through weekly so the objection turns update based on what's actually landing, not what sounded good on paper.

You built the read once; now it runs itself.


## Make it yours
Fork it. Change the persona, the permission line, the objections you map, the tone. The point is not to read someone else's script. It is to run yours, calmer and sharper. Built by an operator. Customize it, break it, make it better.
