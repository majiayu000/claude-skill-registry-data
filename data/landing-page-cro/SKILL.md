---
name: landing-page-cro
description: Audit a landing page and return prioritized conversion fixes across the hero, the proof, the friction, and the CTA, each with the reason and the expected lift direction. Ranks every fix by effort against impact so you ship the cheap wins first. Trigger on "audit my landing page", "why isn't this page converting", "CRO review", "improve my landing page", "review my hero section", or "how do I get more signups from this page".
---

# Landing Page CRO

## What this does
Reads a landing page and returns a ranked list of conversion fixes, grouped by the four things that move a page: the hero, the proof, the friction, and the CTA. Each fix says what to change, why it matters, and which way conversion should move if you make it. It is a worklist you can hand to whoever owns the page, not a vague "make it better."

## What you'll need
You do not need to connect anything to get value today. Paste the URL or the page copy and the skill runs now. Connect the tools and it grounds the audit in how the page actually behaves.

- Works today with: a URL, or the page copy plus a screenshot description and the one action you want visitors to take. Paste it and the skill audits it now.
- More powerful connected to a web-analytics tool: it sees bounce, scroll depth, and where visitors drop, so the fixes target the section that is actually leaking.
- Sharper with a CMS: it can check the page against your other converting pages and reuse what already works.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the page you give it today and gets sharper as you connect tools. It never claims a conversion rate it cannot see. An unknown rate is labeled unknown, not invented, and lift is always a direction, never a promised percentage.

- **Bring your data**: paste the URL or the copy plus the goal action. The skill returns the full four-part audit today. No connection required.
- **Connect your tools**: the same skill pulls bounce, scroll, and drop-off automatically and points the fixes at the section losing the most people.
- **Just exploring**: no page yet? Get the checklist, the exact elements it grades, and a worked example, so you see the shape before you run it.

Every run ends with the one thing that would sharpen the next run, an analytics source to connect or a goal to clarify.

## Customize this for yourself
This was built for a B2B signup or demo page. Set these to your stack:

| Set this | What it is | Example |
|---|---|---|
| GOAL_ACTION | the one thing a visitor should do | start trial, book demo, subscribe |
| AUDIENCE | who the page is for | founders, RevOps, IT buyers |
| PROOF assets | evidence you can show | logos, quotes, numbers, ratings |
| ANALYTICS | your web-analytics connector | a web-analytics tool |
| CMS | where the page is edited | a CMS |
| ABOVE_FOLD | what shows without scrolling | headline, subhead, CTA, one proof |

Audit for one GOAL_ACTION per page. A page asking visitors to do three things converts on none. If the page has two asks, the skill flags it.

## The method

### Hero (the first screen)
Checks the above-the-fold in one glance: does the headline say what this is and who it is for, is the value clear in five seconds, is the CTA visible without scrolling, and is there one proof element early. A hero that makes the visitor work is the most expensive leak on the page.

### Proof
Checks that claims are backed where the visitor doubts them: a specific outcome near the value claim, recognizable logos or quotes near the CTA, and real specifics over adjectives. "Trusted by teams" is not proof. A named result is. Missing proof is a named fix.

### Friction
Finds what makes saying yes harder than it needs to be: too many form fields, an unclear next step, a wall of copy before the point, a CTA that hides, competing links that lead visitors away. Each friction point is named with the fix.

### CTA
Checks the ask itself: is there one primary action, is the button text specific about what happens next ("Start free trial", not "Submit"), does it repeat at natural decision points, and does it match the GOAL_ACTION. Vague or stacked CTAs are flagged.

### Prioritized fix list
Every finding is scored effort against impact and sorted. Cheap high-impact fixes rise to the top, each tagged with the direction conversion should move. You ship the wins first.

## Quality gates
- No claimed conversion rate without a connected analytics source. Unknown stays unknown.
- Lift is always a direction (up, likely up), never a fabricated percentage.
- Every fix names the specific element to change, never "improve the page."
- Illustrative bounce or conversion numbers are marked as examples, never presented as your real data.

## Output (example)
```
LANDING PAGE CRO · page: /trial · goal: start free trial

Est. leak: hero + form (connect analytics to confirm)

Top fixes (effort -> impact, lift direction):
  1. LOW  -> HIGH  ^  Headline says what you do, not who it is for.
                      Add the audience: "for RevOps teams."
  2. LOW  -> HIGH  ^  CTA reads "Submit." Change to "Start free trial."
  3. MED  -> HIGH  ^  Form asks for 7 fields. Cut to email + name.
                      Ask the rest after signup.
  4. LOW  -> MED   ^  No proof above the fold. Move one customer quote up.
  5. LOW  -> MED   ^  3 nav links compete with the CTA. Remove them on
                      this page. One way out.

Next: connect a web-analytics tool to confirm which section leaks most.
```

## Where the inputs come from
The URL or page copy and the GOAL_ACTION come from you. There are no hard thresholds here, CRO is directional, so lift is always expressed as a direction, not a number. Bounce, scroll depth, and drop-off come from a connected web-analytics tool, and cross-page comparisons from a connected CMS. The priorities are yours to reorder.

## Example chat
Here is the skill running on a real page, start to finish.

**You:** Audit my trial signup page. Here's the URL and the copy.

**Claude:** Five fixes, ranked by effort against impact.
```
1. LOW -> HIGH  ^  Headline says what you do, not who it's for.
                    Add the audience: "for RevOps teams."
2. LOW -> HIGH  ^  CTA reads "Submit." Change to "Start free trial."
3. MED -> HIGH  ^  Form asks for 7 fields. Cut to email + name.
```
The catch worth naming: your form is the highest-effort fix on the list but it's sitting at #3, because a headline rewrite and a button-text change are both LOW effort and HIGH impact, and cheap wins ship first. One sharpener: connect a web-analytics tool so I can confirm which section is actually leaking instead of ranking off the page alone.

## Go further
The audit is step one. Here is where an operator takes it once the manual version proves out.

- **Re-audit every time the page changes.** Wire a scheduled Claude task to pull the live page weekly and diff the fix list against what's shipped, so nothing regresses silently.
- **Ground every fix in real drop-off.** Connect Amplitude or a web-analytics tool so the ranked list targets the section actually losing visitors, not just the section that looks weak.
- **Turn the top fix into a ticket automatically.** Push the #1 ranked fix into Linear or your CMS's task queue the moment the audit runs, so it doesn't sit in a doc nobody opens.

You built the worklist once, now it keeps itself current with the page.


## Make it yours
Fork it. Change the four buckets, the way fixes are ranked, the proof you count. The point is not to grade a page against a rubric. It is to ship the change that gets one more visitor to say yes this week. Built by an operator. Customize it, break it, make it better.
