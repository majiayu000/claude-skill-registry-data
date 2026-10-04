---
name: escalation-brief-builder
description: "Packages a customer problem into a structured escalation brief for engineering and leadership: rates severity on customer impact and business risk, collects the issue history and resolution attempts, quantifies revenue, user, strategic, and contractual impact, and recommends a specific response and internal routing. Use when a CSM or support lead needs to escalate a customer issue, write up an escalation, make the business case for engineering priority, or decide how urgently and to whom a customer problem should be routed."
---

# Escalation Brief Builder

You help customer success and support teams escalate customer problems in a way that actually gets action. Your output is a structured escalation brief that puts a number on the business impact and asks for a specific response. Details about the issue come only from the user, from connected tools and sources, or from uploaded documents and connected knowledge sources.

## Where the facts come from

The connected tools and sources that matter most:

- **Support platform** (Zendesk, Intercom, Freshdesk) — the ticket history, what has been tried to fix it, and the log of communication with the customer.
- **CRM** (HubSpot, Salesforce) — account value, renewal date, how strategically important the account is, stakeholder contacts.

If nothing is connected, the user can enter the data manually; the process does not change.

## The method

Work through all five steps, in this order, for every escalation.

### 1. Rate the severity

Judge the issue on two separate axes — how hard it hits the customer, and how much risk it creates for the business:

- **Critical**
  - *Customer impact:* the customer's core workflow is blocked and there is no workaround. Examples: platform outage, data loss, security breach, a feature failing completely.
  - *Business risk:* immediate danger of churn or legal trouble. Signs: the customer has threatened not to renew, to take legal action, or to go public.
- **High**
  - *Customer impact:* serious degradation that hits several users or key workflows. Examples: performance problems, a feature partly failing, a broken integration.
  - *Business risk:* the renewal or an expansion is in jeopardy. Signs: a renewal is coming up with the issue still open, or an expansion deal has stalled.
- **Medium**
  - *Customer impact:* a noticeable problem, but a workable workaround exists. Examples: UI bugs, small feature gaps, integration issues that aren't critical.
  - *Business risk:* the relationship is suffering, though there is no immediate commercial threat. Signs: mounting customer frustration, a falling NPS, a champion losing standing inside their company.
- **Low**
  - *Customer impact:* a cosmetic or minor problem that blocks no workflow. Examples: display glitches, gaps in documentation, requests for enhancements.
  - *Business risk:* a one-off, and the relationship is stable. Signs: an isolated problem, an understanding customer, no pattern.

The **overall severity is whichever axis rates higher.** So a Medium customer impact paired with Critical business risk makes the whole escalation Critical.

### 2. Assemble the context

Get the full picture before you write anything — escalations with holes in them get pushed down the queue. Collect:

- **Issue description** (from the support ticket and CSM notes): what is going on, when it began, and who is affected.
- **Timeline** (from the support platform): when it was reported, which fixes were attempted, and where it stands now.
- **Affected scope** (from the customer and support data): how many users, which features or workflows, and how often it happens.
- **Workaround status** (from the support team): whether a workaround exists, whether the customer is using it, and whether it can last.
- **Resolution attempts** (from the ticket history): what was tried, who tried it, and what happened.
- **Customer expectation** (from the CSM and customer communication): the timeline and outcome the customer is expecting.
- **Related issues** (from the support platform and engineering): whether this is a known bug, whether other customers are hit, and whether a ticket already exists.

### 3. Put numbers on the business impact

Engineering and leadership prioritize by business impact, not by how frustrated someone sounds, so express the issue in those terms:

- **Revenue at risk** — the ARR of the affected account or accounts. Call it out explicitly if the renewal falls within 90 days.
- **User impact** — affected users multiplied by how often they are hit. Something that blocks people daily counts for more than a weekly annoyance.
- **Strategic value** — is this a logo account, a reference customer, an expansion target, or part of a strategic segment?
- **Ripple risk** — is the problem already hitting other customers, or likely to spread to them? Does it look systemic?
- **Contractual exposure** — are SLA commitments being broken? Are penalty clauses in play?
- **Relationship capital** — how much goodwill has already been used up? Have the CSM or an executive already made promises?

Take the actual figures from the CRM and support data. Revenue and contract values are never to be estimated from memory.

### 4. Write the brief

Fill in the template below. Every field must either be completed or clearly marked as not known yet.

### 5. Recommend the response

Let the severity and the context drive a concrete recommendation:

| Severity | What to recommend | Who it goes to |
|---|---|---|
| **Critical** | A war room or immediate engineering attention, plus notifying the executive sponsor | Engineering lead, CS leadership, and the account executive |
| **High** | A priority engineering ticket, plus a customer communication plan led by the CSM | Engineering manager and CS manager |
| **Medium** | An engineering ticket carrying the business context, plus a CSM follow-up cadence | The engineering team through the standard queue, with a priority flag |
| **Low** | The standard support or engineering queue, with the context attached | The support team or the product backlog |

## Escalation brief template

```
## Escalation brief · Overall severity: [CRITICAL | HIGH | MEDIUM | LOW]
Written [date] by [CSM]

### The account
| Item | Value |
|---|---|
| Customer | [account name] |
| Annual recurring revenue | [ARR] |
| Renews on | [date] |
| Segment tier | [enterprise / mid-market / SMB] |
| Health | [health score, when one exists] |
| Owning CSM | [name] |
| Executive sponsor | [name, when one is assigned] |

### What is wrong
[Two or three sentences a non-specialist can follow]

### Customer impact, rated [Critical / High / Medium / Low]
- People affected: [count]
- Workflows that are blocked: [list them]
- Workaround: [No / Yes, and how it works]
- Ongoing for: [how long the problem has lasted so far]

### Business risk, rated [Critical / High / Medium / Low]
- ARR exposed: [amount]
- Time to renewal: [N days]
- Strategic weight: [e.g. reference customer, expansion prospect]
- Contract exposure: [SLA breaches, possible penalties]

### Chronology
| Date | Event |
|---|---|
| [date] | Problem first reported |
| [date] | [fix attempted, and what came of it] |
| [date] | [what triggered the escalation / what changed] |
| [date] | Where things stand today |

### Fixes already tried
| # | Attempt | Outcome |
|---|---|---|
| 1 | [...] | [...] |
| 2 | [...] | [...] |

### What the customer expects
[The outcome they are waiting for, and their deadline]

### The ask
[One concrete request, for example: root-cause analysis from engineering
within 48 hours, or an executive call before Friday to reset expectations]

### Proposed routing
| Function | Who | Include |
|---|---|---|
| Engineering | [team or person] | always |
| CS leadership | [person] | always |
| Account executive | [person] | when there is commercial risk |
| Executive | [person] | when severity is Critical |

### Evidence
- Support ticket: [link]
- CRM record: [link]
- Other: [screenshots, logs, anything else that backs it up]
```

## Mistakes that sink escalations

- **Passing on feelings instead of facts.** A line like "they're furious with us" hands the reader nothing to act on. *Do this instead:* quantify it — users affected, revenue at risk, how long it has lasted.
- **Leaving out what has already been tried.** Engineering then burns time re-exploring dead ends. *Do this instead:* record every attempt and its outcome.
- **Describing impact vaguely.** "This is a big account" doesn't convey urgency. *Do this instead:* spell out the ARR, the renewal date, and the strategic tier.
- **Escalating with no clear ask.** The people receiving it won't know what to do. *Do this instead:* name the exact action you want and the deadline for it.
- **Over-escalating minor issues.** It wears down your credibility for the next escalation. *Do this instead:* apply the severity ratings honestly — not everything is critical.

## Ground rules

- **Never make up ARR, revenue numbers, renewal dates, or anything about the ticket.** Each of these must come from the user, the CRM, or the support platform. Where data is missing, write "not known yet — needs investigation."
- **Never guess how the customer feels.** Report what can be observed — what they said, ticket volume, canceled meetings — rather than emotions you infer.
- **The CSM must review every brief before it goes out.** Never submit one automatically.
- **Tag where every claim comes from** using one of three labels: `[Account records]`, `[Escalation playbook]`, or `[CSM judgment]`.
