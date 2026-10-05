---
name: lead-research
description: Use when researching prospects or accounts before outreach. Covers qualification, finding the trigger event, identifying the right contact, and producing a brief that makes outreach specific rather than generic.
metadata:
  category: business
  version: 1.0.0
  tags: [sales, prospecting, research, qualification, outreach]
---

# Lead Research

## Purpose

Research an account well enough that the outreach is obviously not a template. The entire value of lead research is producing one specific, true, relevant observation that could not have been written about any other company.

## When to Use

- Researching an account before outreach.
- Qualifying inbound leads.
- Building a target list.
- Preparing for a sales call.

## Capabilities

- Qualification against a defined profile.
- Trigger-event identification.
- Finding the right contact and the actual decision maker.
- Producing a brief that makes outreach specific.

## Inputs

- The ideal customer profile, defined in observable terms.
- The account.
- What you are actually selling, and to what problem.

## Outputs

- A qualification verdict with the reasoning.
- The trigger, if there is one.
- One specific observation that makes the outreach non-generic.

## Workflow

1. **Qualify before researching** — Does this account match the profile at all? Deep research on an unqualified account is wasted time, and it is the most common way prospecting time disappears.
2. **Find the trigger** — What changed recently? A funding round, a new executive, a job posting, a product launch, a public complaint. Outreach without a trigger is an interruption; outreach with one is a response.
3. **Read what they publish** — Their engineering blog, their job postings, their changelog. Job postings in particular are extraordinarily informative: they say exactly what a company is building and what it lacks.
4. **Find the person with the problem** — Not the most senior person. The person who owns the pain is the one who will reply.
5. **Find one specific, true observation** — Something that could not be written about any other company. This is the entire output; everything else is preparation for it.
6. **Stop when you have it** — More research does not improve outreach past this point.

## Best Practices

- Job postings are the most under-used signal in prospecting. A company hiring three platform engineers and a site reliability engineer is a company with a reliability problem, and they have just told you so in public.
- One specific observation beats five generic ones. "I saw you're hiring three platform engineers" is worth more than any amount of "I noticed your impressive growth".
- The trigger is what makes outreach timely. Without one, you are asking someone to change their priorities for a stranger.
- Do not personalize with something trivially scraped. "I see you're based in Austin" is not personalization; it is proof of automation.
- Qualify ruthlessly. Time spent researching an account that will never buy is the most expensive thing in prospecting.
- If you cannot find one specific, true, relevant observation, the account is not ready. Move on.

## Examples

**A brief that makes the outreach write itself:**

```markdown
## Acme Logistics — qualification: STRONG

**Profile match**
- 340 employees (target: 100-1,000)
- Series C, $60M, 8 months ago
- Self-reported "50+ microservices" (engineering blog, March)
- No dedicated platform team (inferred: see hiring, below)

**Trigger — this is the reason to reach out now**
Posted 4 roles in the last 3 weeks: 2x Platform Engineer, 1x SRE, 1x
"Developer Experience Engineer" (a newly created role — the posting says so).

The SRE posting says, verbatim: *"Our deploy pipeline takes 45 minutes and
teams have started deploying less often as a result. You'll own fixing that."*

They have publicly described the exact problem we solve, in a job posting,
and stated that it is changing their engineers' behavior.

**The person**
Not the VP Engineering. The hiring manager on the DevEx posting is Priya S.,
Director of Engineering — she owns this problem, she is being asked to fix it,
and she has just been given headcount to do it. She is the one who will reply.

**The observation for the outreach**
"Your SRE posting says deploys take 45 minutes and teams have started deploying
less often. That second part is the expensive one — and it's usually the test
suite, not the build."

That sentence could not have been written about any other company. It quotes
their own words back at them, and it demonstrates that we understand the
problem rather than the keyword.

**Disqualifiers checked**
- Not already a customer
- No existing vendor in this category (no relevant job-posting requirements,
  no mentions in their blog)
- Budget: they just raised, and they have opened four requisitions.
```

## Notes

- The job posting is the highest-signal public artifact most companies produce. It states what they lack, what they are willing to pay to fix, and who owns it — all in public, all for free.
- Quoting a company's own words back to them is the most effective form of personalization, because it is unfakeable at scale.
- The discipline of "if you cannot find one specific true observation, move on" is what makes prospecting time productive. Most of it is spent on accounts where no such observation exists.
