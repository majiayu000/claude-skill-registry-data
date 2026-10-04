---
name: winback-play
description: Re-onboard a churned customer with the same care they got the first time. Reads why they left and whether they left the door open, picks the ones worth winning back, and builds a warm re-onboarding sequence, not a "we miss you" discount blast. Built for any post-sale or growth team, customizable to your product and win-back window. Trigger on "win back churned customers", "re-engage a lost account", "build a win-back sequence", "which churned customers should we chase", "boomerang play", "re-onboard a customer who left", or any win-back question.
---

# Win-Back Play

## What this does
Builds the play to win a churned customer back, and treats the return like an onboarding, not a discount. It reads why each account left, whether the exit left a door open, and whether anything has changed on their side, then picks the ones actually worth chasing and writes a warm re-onboarding sequence for each. The premise: a returning customer should feel the same care they felt the first time, because the reason they come back is rarely the price, it is the feeling that they were wanted. Boomerang customers are real revenue, and this is the motion that earns them.

## What you'll need
You do not need to connect anything to get value today. Paste the churned accounts and why they left, and the skill builds the play now. Connect your tools and it pulls the exit context and the change signals for you.

- Works today with: a churned account, why they left, and when. Paste it, or a short list of them, and go.
- More powerful connected to a CRM: it reads the full history, the champion, the original value, and whether the door was left open.
- Sharper with a product-analytics tool: it sees if they spun up a competitor or if the gap that made them leave still exists.
- Sharper with a signal source: it catches the change that reopens the door, a new leader, a fresh round, a reorg.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on what you paste today and gets sharper as you connect tools. It never invents a reason they would return, and never chases an account that left for a reason that has not changed. A gap is a prompt, not a guess.

- **Bring your data**: paste the churned accounts and their exit reasons. The skill picks the winnable ones and writes the re-onboarding play today.
- **Connect your tools**: the same skill reads the full relationship and the change signals, so the play lands on the accounts whose door actually reopened.
- **Just exploring**: no churned list yet? Get the framework, the winnable-versus-gone test, and a worked example, so you see the shape before you build.

Every run ends with the one thing that would sharpen the next play, a signal to connect or a detail to add.

## Customize this for yourself
This was built to be motion-agnostic. Set these to your win-back:

| Set this | What it is | Default / Example |
|---|---|---|
| WINDOW | how long after churn you reach back | 90 days, retune to your cycle |
| WINNABLE_TEST | what makes an account worth chasing | the reason they left has changed |
| CHANGE_SIGNALS | what reopens a door | new leader, new round, reorg, competitor pain |
| RE_ONBOARD | how you welcome them back | the same care as first time, warm not salesy |
| CHANNELS | where the reach-back runs | the champion's inbox, a human note |
| VOICE | the tone of the return | glad you're back, not "we miss your money" |

The play is yours. The point is to re-onboard a returning customer, not to blast a discount at everyone who ever left.

## The method

### Pick the winnable, drop the gone
Not every churned account is worth chasing. Sort them: winnable means the reason they left has changed or was never really about your product. Gone means the gap that pushed them out still exists. Chasing the gone burns goodwill and your time. Name which is which before you write a word.

### Read why they actually left
The stated reason and the real reason differ. Price is usually a proxy for value not felt. Missing feature is often onboarding that never showed them the feature. Read the real reason, because the win-back has to answer it, not the surface complaint.

### Wait for the door to reopen
A win-back lands when something changed: a new leader with a new mandate, a fresh round and new pressure, a reorg, or the competitor they left for disappointing them. Time the reach-back to the change, not to a calendar. A cold "we miss you" with nothing new is why win-backs get ignored.

### Re-onboard, do not re-sell
The reach-back is a welcome, not a pitch. Lead with what changed on your side that answers why they left, offer to make the return effortless (their config kept warm, their data ready), and bring back the human who knew them. The feeling is glad you are back, not glad to have your money again.

### Build the sequence
Write the actual touches: the warm opener tied to the change, the make-it-easy offer, the human re-onboarding. Short, specific, and human. If the sequence could be sent to anyone who ever churned, it is a discount blast, not a win-back. Rewrite until the account's real reason is load-bearing.

## Quality gates
- Every account is sorted winnable or gone, with the reason. No blanket chase of the whole churn list.
- The real reason they left is named, not just the stated one.
- The reach-back is timed to a change signal, never a generic "we miss you."
- The sequence re-onboards, it does not re-sell. No desperation discount as the opener.
- The message fails if it could be sent to any churned account. Rewrite until the reason is load-bearing.

## Output (example)
```
WIN-BACK PLAY · Northwind (illustrative) · churned 7 months ago

Winnable?   YES. Left for a competitor over a missing integration.
            That integration shipped in Q1. The reason is gone.
Real reason Not price. They were never fully onboarded onto the
            workflow that would have made the integration matter.
Door open?  Yes. New VP started 6 weeks ago (change signal).
            Original champion still there.

RE-ONBOARDING SEQUENCE:
  Touch 1 (to the champion): "The integration you needed shipped.
    Thought of you. No pitch, just wanted you to know."
  Touch 2 (to the new VP): a warm intro via the champion, framed as
    "worth another look given what changed."
  Touch 3 (the return): "We kept your config warm. If you want back
    in, it's a 10-minute restart, not a rebuild."

Not sent: any "we miss you, here's 30% off." That answers nothing.
```

## Example chat
Here is the skill turning a churned account into a real return.

**You:** We lost Northwind 7 months ago. They said we were too expensive and went with a cheaper tool. Should we chase them?

**Claude:** Depends whether the real reason changed, and price is almost never the real reason. Let me read it: if they left purely on cost and nothing has changed, they are gone, do not burn the goodwill. But "too expensive" usually means "I did not feel enough value to justify it," which is an onboarding problem wearing a pricing costume. Was Northwind ever fully onboarded onto your core workflow?

**You:** Honestly no. They set up the basics and never got to the automation piece.

**Claude:** Then this is winnable, and the win-back is not a discount, it is the onboarding they never got. Here is the play:
```
Touch 1: warm note from their old CSM, not sales. "Been thinking
  about your team. When you were with us, you never got to the
  automation piece, which is the part that would've paid for the
  whole thing. Can I show you in 15 minutes, no strings?"
Touch 2: if they bite, re-onboard for real, start at the value
  they missed, not at setup.
Touch 3: make the return effortless, keep their old config warm.
```
The reason is load-bearing: this message only makes sense for an account that churned under-onboarded. One sharpener: connect a signal source and I will time the reach-back to a real change on their side, a new leader or a fresh round, so you knock when the door is actually open.

## Go further
The play is step one. Here is where an operator takes it once it works.

- **Run the boomerang list on a schedule.** Have a Claude task sweep churned accounts monthly, sort winnable versus gone, and surface only the ones whose door just reopened to the CSM in Slack.
- **Wire change signals to the reach-back.** Connect a signal source so a new leader or a fresh round at a churned account triggers the win-back play automatically, timed to the change instead of a calendar.
- **Close the loop to onboarding.** Feed every win-back reason back into the onboarding audit, because the same gap that lost them is the one costing you the next cohort.

You stop treating churn as final and start treating it as a list.

## Where the inputs come from
The window, the winnable test, and the change signals are yours to set. The examples here suited a 90-day-plus win-back on a subscription product. A longer enterprise cycle waits for a bigger change; a self-serve motion moves faster. The logic, pick winnable over gone, answer the real reason, time to a change, re-onboard don't re-sell, does not change.

## Make it yours
Fork it. Change the window, the winnable test, the sequence, the voice. The point is not to blast a discount at everyone who left. It is to welcome back the ones worth having, with the care that makes them stay this time. Built by an operator. Customize it, break it, make it better.
