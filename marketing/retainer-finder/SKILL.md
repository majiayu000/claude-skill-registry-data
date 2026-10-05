---
name: retainer-finder
description: Analyze a company website and identify recurring service opportunities for agencies. Finds what depreciates without ongoing maintenance, what creates monthly dependency, and what justifies a retainer conversation.
---

# Retainer Finder

Most agencies sell projects. They make money on retainers.

This skill analyzes a company and answers one question: what does this company need every month, and why would they pay for it?

The output is not a proposal - it is a retainer strategy. A map of what to build toward after the first project lands.

## What this does

Three phases:

1. **Depreciation Scan** - Find what is actively losing value without maintenance (rankings, audiences, social presence, email list)
2. **Dependency Map** - Identify what, if implemented, creates ongoing reliance on the agency
3. **Retainer Brief** - Estimated MRR, service stack, renewal risk, and how to transition from project to retainer

## How to use

Pass a URL:

```
/retainer-finder https://empresa.com
```

Or after running `/agency-audit` on the same company - the retainer-finder uses the same signals but asks different questions.

## Phase 1 - Depreciation Scan

**Goal:** Find what is already losing value without someone managing it.

Unlike a project (build once, done), these are things that degrade over time without attention:

| Asset | What happens without maintenance |
|-------|----------------------------------|
| SEO rankings | Competitors publish, you drop. Algorithm updates hit without someone to respond. |
| Ad campaigns | Audiences fatigue, CPMs rise, creative goes stale. Left alone, ROAS drops. |
| Email list | Deliverability degrades without cleaning. Unsent = losing 25% list value per year. |
| Social presence | Algorithm deprioritizes inactive accounts. Followers lose connection. |
| Google Business Profile | Photos age, posts go silent. Reviews go unanswered. |
| Website performance | WordPress plugins update and break things. Security vulnerabilities accumulate. |
| Analytics / tracking | Platform changes break tags. iOS updates kill attribution. |

Check each asset and score it:
- **Active and managed** - someone is maintaining this
- **Active but unmanaged** - running but nobody is watching it
- **Inactive** - abandoned
- **Not present** - does not exist yet

Unmanaged and inactive assets are the retainer opportunity. They are already costing the company - the agency just needs to make that cost visible.

Output:
```
## Depreciation Scan

| Asset | Status | Monthly cost of neglect |
|-------|--------|------------------------|
| SEO | [status] | [what they are losing] |
| Paid ads | [status] | [what they are losing] |
| Email list | [status] | [what they are losing] |
| Social | [status] | [what they are losing] |
| Google Business | [status] | [what they are losing] |
| Website/CMS | [status] | [what they are losing] |
| Analytics | [status] | [what they are losing] |

Top depreciation risks:
1. [asset] - [specific cost of neglect for this company]
2. [asset] - [specific cost]
```

## Phase 2 - Dependency Map

**Goal:** Identify which services, once delivered, require the agency to stay involved.

Not all services create dependency. A logo redesign does not create a retainer. A live ad campaign does.

**High dependency services** (client cannot easily remove agency):

| Service | Why they cannot leave |
|---------|----------------------|
| Paid ads management | Campaign knowledge + audience data lives in the agency's account history. Starting over = losing months of optimization. |
| SEO content | Ongoing content + internal linking strategy. Stopping = rankings drop in 3-6 months. |
| Email marketing automation | Flows built in the tool, segment logic, suppression lists. Complex to hand off. |
| Analytics + reporting | Agency interprets the data. Client cannot read dashboards without context. |
| WordPress maintenance | Updates, backups, security. Client fears touching it themselves. |
| Social media management | Content calendar, brand voice, community - hard to internalize quickly. |
| Google Business management | Review responses, post schedule, local SEO adjustments. |

**Low dependency services** (one-time work, easy to hand off):

- Website redesign (delivered and done)
- Brand identity
- One-time SEO audit
- Analytics setup (once live, client can run it)
- One-time campaign setup without ongoing management

Map which high-dependency services this company needs based on Phase 1 findings.

Output:
```
## Dependency Map

High-dependency opportunities:
1. [service] - dependency reason: [why they cannot leave]
2. [service] - dependency reason: [...]

Low-dependency work to avoid leading with:
- [service] - [why it does not convert to retainer]

Recommended entry: [highest-dependency service that is also lowest friction to start]
```

## Phase 3 - Retainer Brief

**Goal:** Define what the retainer looks like, what it costs, and how to get there.

### Retainer Stack

The retainer stack is the combination of monthly services that makes sense for this company. It should:
- Address active depreciation risks (Phase 1)
- Include at least one high-dependency service (Phase 2)
- Be deliverable by the agency (match to their service list if provided)
- Have a clear ROI story the company can understand

```
## Retainer Brief

### Recommended retainer stack

Core (must-have for ROI to work):
- [service] - [price range/month]
- [service] - [price range/month]

Add-on (increases value and dependency):
- [service] - [price range/month]

Total MRR estimate: [low] - [high]
Contract length recommendation: [3-month / 6-month / 12-month]
Why this length: [one sentence - what takes that long to show results]
```

### Transition Path

How to move from first project to retainer:

1. **Entry project** - the quick win or audit that gets them in the door
2. **Results moment** - the specific milestone that creates the retainer conversation ("we set up your tracking and now you can see X - want us to act on it monthly?")
3. **Retainer pitch** - frame it as "keeping the results" not "more services"

```
Transition path:
Entry: [project] - [price] - [delivery time]
Results moment: [what they will see and when]
Retainer pitch: "[One sentence framing - specific to this company]"
```

### Renewal Risk

Identify what could end the retainer early:

```
Renewal risks:
- [risk 1] - [mitigation]
- [risk 2] - [mitigation]

Strongest retention signal: [what makes this client sticky]
```

## References

- `references/retainer-signals.md` - full signal library by service type and company size

## Output principles

1. Every depreciation risk must be specific to this company - not generic
2. Dependency map must name the actual mechanism ("campaign data lives in our account" not "complex to hand off")
3. MRR estimate must be grounded in service-mapping benchmarks - never inflate
4. Transition path is mandatory - a retainer without an entry path is theory
5. The retainer pitch line is the most important output - it should be usable verbatim in the sales conversation
