---
name: stage-map
description: This skill should be used when a founder wants to know which startup stage they're actually in, what the goal and exit criteria of that stage are, what failure modes to watch for, or which tool/module to use next — e.g. "what stage am I at", "what should I focus on now", "am I ready for an MVP", "do I have product-market fit yet", "what's the next step for my startup", "should I be hiring/scaling yet", "الان تو چه مرحله‌ای هستم", "قدم بعدیم چیه", "آماده‌ام برم سراغ MVP؟", "به PMF رسیدم؟", "روی چی تمرکز کنم". Maps the four stages (Idea, MVP, Launch, Scale) from The Founder's Playbook, diagnoses the current stage from evidence, and routes to the right module. Do NOT use to actually run idea validation — that's founder-playbook:idea-stage.
version: 1.0.0
---

# Stage map — where you actually are, and what that stage demands

The lifecycle from *The Founder's Playbook: Building an AI-Native Startup* (Anthropic, 2026). Four stages, each with one goal, one exit condition, and a characteristic set of ways founders get it wrong.

The premise: AI erased the assumption that each new phase requires a bigger team, a different skill set, and a fresh funding round. The founder's job shifts from individual contributor to orchestrator. What didn't change is the sequence — and the most expensive mistake in the AI era is running a stage ahead of the evidence.

## Diagnose before advising

Founders routinely self-report a stage ahead of where their evidence puts them, because building is now so cheap that the *artifacts* of a later stage appear long before its *evidence* does. Diagnose from exit criteria, not from what exists.

Ask (batch these, don't interrogate):
1. Have you talked to people with this problem who aren't friends or investors? How many?
2. Is anything shipped, and does anyone outside your circle use it?
3. Do users come back unprompted — without you nudging them?
4. Is anyone paying? Do you know your CAC, LTV, and payback period?
5. What are you personally doing every day right now?

Then place them by **the last exit condition genuinely met**, and say so plainly when that's earlier than they assumed. Having a working product does not make someone MVP-stage; having *evidence* does.

## The four stages

### Idea — "Is this worth building?"

- **Goal:** research-oriented validation — solid evidence that a real problem exists and that the proposed solution addresses it, *before* committing resources to building.
- **Exit:** problem–solution fit. Yes to all three: (1) the problem is real and specific — you can name who has it, how often, how severely, what they do today; (2) the solution addresses the problem validation *revealed*, not the one assumed; (3) enough signal that committing to an MVP is a reasoned decision rather than an act of faith.
- **Failure modes:** mistaking building for validating (a prototype is a conversation prop, not evidence — 42% of startups failed building something nobody wanted, *before* AI made building free) · premature scaling (agentic tools will refactor a flawed premise with the same enthusiasm as a good one) · loss of objectivity (confirmation bias now comes with a research engine).
- **Run it:** `/founder-playbook:idea-stage`

### MVP — "What exactly should we build first?"

- **Goal:** translate a validated problem into the smallest focused product real users will actually use. Two co-equal goals: move fast, and don't accrue compounding technical debt. Plus a third that founders skip: **persistent context from day one** — specs, architectural decisions, `CLAUDE.md` — or every session re-derives foundations and AI-generated changes drift.
- **Exit:** genuine evidence of product-market fit — a specific, identifiable group returns to it (retention), pays for it (revenue), or tells others (referral).
- **Failure modes:** agentic technical debt (unlike ordinary debt, it *compounds* — without written specs and constraints each session re-derives decisions and they drift, producing a codebase with no coherent mental model) · false product-market fit (launch energy from friends, investor portfolios, and a Hacker News spike predicts nothing about week six) · zero-friction scope creep (every addition is individually defensible; the antidote is a written scope doc naming what the product deliberately does *not* do, and what user evidence would justify adding anything) · insecure by inexperience (AI generates code that works, not code that's secure; vulnerabilities are invisible until exploited, so there's no natural feedback loop).
- **Litmus tests:** the Sean Ellis test (>40% of active users "very disappointed" if they lost it) · the effort test (pre-PMF, retention requires constant founder intervention; post-PMF the product starts pulling instead of you pushing).
- **Do first:** define architecture *before* building and save it as `CLAUDE.md` · write the scope doc · set retention/activation benchmarks and Day-7/Day-30 targets *before* launch, plus an explicit definition of what a false positive looks like (signups without activation, revenue without retention) · security review before any real user touches it.
- **Related modules:** `/venture:pmf` · `/venture:customers`

### Launch — "Does this business deserve to grow?"

- **Goal:** turn early traction into a repeatable growth engine, harden the infrastructure, and build an actual company around the product. Not to remove the founder, but to free their attention for the decisions only they can make.
- **Exit:** all three — (1) growth is repeatable and channel-driven with CAC, LTV, and payback you can defend; (2) the product handles production workloads with security and compliance in order; (3) operations run without founder bottlenecks.
- **Failure modes:** technical debt comes due (MVP shortcuts start accruing interest) · the founder becomes the bottleneck (signs: hour-long decisions take a week, support piles up because only you know the answer, tasks happen only when you remember them) · security and compliance no longer deferrable · expansion before you're ready (a new market adds variables that destroy your ability to read your own data, while the original base gets neglected).
- **Do first:** architectural audit → triaged remediation sequence · an audit of everything landing on your desk, sorted into automate / delegate / genuinely founder · security review against the frameworks your buyers require · a lightweight PM operating system (sprint cadence, minimum spec template, bug triage tree, weekly metrics brief).
- **Related modules:** `/venture:gtm` · `/venture:model`

### Scale — "Is this a business rather than a bet?"

- **Goal:** systematic growth sustained by mature operations; a defensible moat from accumulated depth — domain expertise built into the product, integration depth, and proprietary data and workflows.
- **Exit:** a threshold rather than a milestone — the company is sustainable while the founder is increasingly not running day-to-day. In practice: sustainable profitability without external capital, IPO-readiness, or acquisition. All three require systematic auditable growth, a moat that survives scrutiny, and operational maturity. The test: *if a well-funded incumbent copied your product today, would your users stay?*
- **Failure modes:** delegating the operational layer (hand off too fast and decisions lose founder context; too slow and you're the bottleneck — the real work is codifying knowledge that lives only in your head) · scaling technical operations (buyers now evaluate the *organization*: documentation, SLAs, support, observability) · scaling organizational functions (hiring, payroll, accounting, legal, compliance monitoring) · building a GTM function (organic growth has a ceiling; signs of hitting it are flattening curves, rising CAC, and a pipeline that only moves when you're personally in it).
- **Moat mechanics:** turn domain expertise into AI context and reusable skills · compound accumulated user data into a feedback loop a copycat can't recreate · create workflow lock-in through integrations, APIs, and SDKs that let customers *build on* the product.
- **Related modules:** `/venture:gtm` · `/venture:review`

## Choosing the Claude surface

| If the task is… | Reach for | Why |
|---|---|---|
| A question, a rewrite, a quick brainstorm | **Chat** | Fast, conversational, no setup |
| Research, analysis, or a finished document built from your files and systems | **Claude Cowork** | Folder access, connectors, skills, scheduled runs |
| Writing, testing, or shipping software | **Claude Code** | Codebase access, diffs, git, dev environments |

Same model underneath; what changes is the workspace around it.

## How to answer

1. **Diagnose the stage from evidence**, and name it plainly — including when it's earlier than the founder believes.
2. **State that stage's goal and exit condition** in one line each.
3. **Name the one or two failure modes** they're closest to right now, with the specific signal you noticed.
4. **Route:** the single next action, and the module or surface for it.
5. Note anything from the *next* stage that must be started early (measurement frameworks and `CLAUDE.md` are the two most commonly started too late).

Load `references/lifecycle.md` for the full stage-by-stage exercise list from the book.
