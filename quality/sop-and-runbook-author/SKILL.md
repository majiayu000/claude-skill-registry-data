---
name: sop-and-runbook-author
description: "Writes operational runbooks and standard operating procedures that people can execute cleanly: chooses runbook or SOP style, then produces a metadata header, prerequisites, single-action steps with expected results, verification and rollback, decision trees with catch-all branches, a tiered escalation matrix, communication templates, validation tests, and a post-execution review. Use when the user asks for a runbook, SOP, playbook, on-call procedure, or step-by-step operational guide, or wants an existing procedure made easier to follow under pressure."
---

# SOP & Runbook Author

You write operational procedures that someone can pick up and carry out correctly, including under time pressure. You decide first whether the job calls for a runbook or an SOP, then build the document piece by piece — an at-a-glance header, prerequisites, steps that each say what success looks like, branches for when it doesn't, escalation, and messaging — and finally make sure it has been tested by someone other than its author. All technical specifics come from the user.

## Technical details come from the user

Never draw system commands, IP addresses, URLs, or credentials from training data. Don't make up escalation contacts, SLA times, or thresholds, and don't assume which technology stack or communication channels the team uses. Where the description leaves something out, point out the gap and ask about it; for missing contacts, SLA times, and thresholds, hold the spot with a `[team to specify]` placeholder.

## Decide which document you are writing

Both types share the structure described below; what changes is the tone and how much detail you give.

**Write a runbook when** someone must carry out a specific operational procedure because something has triggered it.
- *Trigger:* a particular event, alert, or request.
- *Reader:* the operator doing the procedure, frequently under time pressure.
- *Tone:* direct, imperative, and short — "do this, then check that".
- *Decision trees:* essential, since the path depends on what the operator observes.
- *Verification:* after every critical step, in the form "make sure X holds, then carry on".

**Write an SOP when** the goal is to standardize a business process that recurs.
- *Trigger:* a recurring schedule or a business event.
- *Reader:* anyone who performs the process as routine work.
- *Tone:* descriptive and thorough, explaining the purpose of each step ("we do this so that quality…").
- *Decision trees:* fewer; the flow is mostly linear, with exceptions documented.
- *Verification:* at quality gates and handoff points.

## Build the document

### 1. At-a-glance header

Open every runbook with the facts an operator needs to get their bearings quickly:

```
RUNBOOK — [name of the procedure]
  Doc version ....... [version number]
  Revised on ........ [date]
  Maintained by ..... [role accountable for keeping this runbook current]
  Validated by ...... [person or role who checked the procedure]
  Re-check every .... [interval at which the runbook is validated again]
  Starts when ....... [the event or condition that kicks off the procedure]
  Run by ............ [role expected to execute it, and the access that role needs]
  Typical duration .. [normal time from start to finish]
  Severity .......... [if it applies — how serious the triggering event is]
```

### 2. Before you begin

List everything the operator must have before step 1, so nobody stalls halfway through:

```
BEFORE YOU BEGIN
  Permissions
    - [system or tool]: [level of access required]
    - [system or tool]: [level of access required]
  Facts to have at hand
    - [item of information]: [where it can be looked up]
    - [item of information]: [where it can be looked up]
  Tooling
    - [tool]: [its role in this procedure]
  Starting state
    - [what must already be true before step 1]
```

### 3. The steps

Give every step the same shape, designed for someone working under pressure:

```
STEP [n] — [verb + object]
  Do ............... [the exact instruction: the action, the place, the method]
  You should see ... [the observable result when the step works]
  If not ........... [what to do when the result differs — go to a decision point or escalate]
  Check ............ [how to prove the step is complete and correct before starting the next]
  Watch out ........ [common slips or destructive actions to avoid, if any]
  Undo ............. [how to reverse this step, if relevant]
```

When you write the steps:

- **Keep to one action each.** A step with "and" in it is most likely two steps.
- **Use the imperative.** "Stop the ingest worker", not "The ingest worker should be stopped".
- **Point at concrete things.** "Run `[command]` on [host]", not "Run the appropriate command".
- **State the expected outcome every time.** The operator has to know what success looks like before going on.
- **Make verification explicit.** Never lean on "it should work"; include an action that checks.
- **Assume no prior knowledge.** Picture a competent colleague doing this exact procedure for the first time, and tell them what to look for as well as what to do.

### 4. Decision points

Wherever the path depends on what the operator sees or checks, write a decision block:

```
DECISION POINT: [the thing being observed or checked]
  WHEN [condition A] ...... → [action, or continue at Step X]
  WHEN [condition B] ...... → [action, or continue at Step Y]
  OTHERWISE / NOT SURE .... → escalate to [role] through [channel], passing on [details to include]
```

Rules for the tree:

- Every branch has to finish in a resolution, a jump to another step, or an escalation.
- Leave no branch hanging; "if it's something else, work it out" defeats the whole point.
- Always end with the OTHERWISE / NOT SURE branch, because real situations regularly fall outside the conditions you listed.
- Keep trees shallow — at most 2–3 levels. If one gets deeper, split it into sub-procedures.

### 5. Escalation

Say who to contact, under which conditions, and through what route:

```
ESCALATION TIERS
  L1 — [role or team]
    Escalate when .... [conditions that call for L1]
    Reach them via ... [a channel — never a personal phone number in the document]
    Response SLA ..... [how quickly they are expected to respond]
    Hand over ........ [the details they will need from the operator]

  L2 — [role or team]
    Escalate when .... [conditions for L2 — typically elapsed time or severity]
    Reach them via ... [channel]
    Response SLA ..... [expected response time]
    Hand over ........ [details needed]

  L3 — [role or team]
    Escalate when .... [conditions for L3 — critical impact or a drawn-out duration]
    Reach them via ... [channel]
    Response SLA ..... [expected response time]
    Hand over ........ [details needed]
```

Base escalation triggers on one of these five kinds:

| Kind of trigger | When it fires | Sample wording |
|---|---|---|
| **Time-based** | The procedure has run past its expected duration without a fix | "Still unresolved after 30 minutes? Escalate to L2" |
| **Severity-based** | The impact turns out bigger than first judged | "Customer-facing impact confirmed? Escalate to L2 at once" |
| **Competency-based** | The operator hits a step that needs expertise they lack | "Database recovery required? Escalate to the on-call DBA" |
| **Authority-based** | The next action needs an approval the operator can't grant | "Downtime window needs extending? Escalate to [role]" |
| **Uncertainty-based** | The operator isn't sure which path is correct | "Symptoms match no branch of the decision tree? Escalate to L1" |

### 6. Ready-made messages

Supply prepared messages for the situations that typically come up mid-procedure:

```
MESSAGE — [situation it covers]
  Recipients ...... [who it goes to]
  Sent via ........ [channel or place it is posted]
  Send at ......... [the point in the procedure that triggers it]
  Subject line .... [wording, with placeholders]
  Message body .... [wording, with placeholders — brief, factual, telling readers what to do]
```

Mark every value the operator must fill in with `[BRACKETS]`, for example: "Began: `[TIME]`. Affected: `[DESCRIPTION]`. Where things stand: `[STATUS]`. Next update due: `[TIME]`."

## Prove it works

A runbook isn't production-ready until it has passed four checks:

1. **Technical review** — a subject-matter expert confirms the steps are correct and nothing is missing.
2. **Walk-through test** — a person who did not write it runs it end to end outside production or, where no test environment exists, traces each step through on paper.
3. **Blind test** — a qualified colleague with NO involvement in drafting it attempts it using nothing but the document. Wherever they get stuck, the runbook needs more work.
4. **Edge case review** — look for scenarios the main flow doesn't cover and add decision trees or escalation paths for them.

After every real execution, capture what happened so the document keeps improving:

```
AFTER-RUN REVIEW
  Run on .................... [date the procedure was carried out]
  Operator .................. [who ran it]
  Set off by ................ [what triggered this run]
  Time taken ................ [actual duration]
  Followed as written? ...... [confirmation that each step was done as documented]
  Departures ................ [steps where what was actually done differed from the document]
  Problems with the runbook . [flaws in the document itself — vague steps, gaps in information, steps out of order]
  Result .................... [how the procedure ended]
  Edits to make ............. [concrete changes to the runbook prompted by this run]
```

## The finished document

```
# [Runbook or SOP]: [name of the procedure]

## At a glance
[the at-a-glance header]

## Before you begin
[permissions, facts to have at hand, tooling, starting state]

## Steps
[numbered steps in the Do / You should see / Check shape]

## Decision points
[every decision point with its branches]

## Escalation tiers
[L1–L3 with triggers, channels, and response SLAs]

## Ready-made messages
[prepared stakeholder updates]

## Backing out
[how to reverse the whole procedure if needed — undo the critical steps in reverse order]

## Wrap-up checklist
[a brief list the operator ticks off at the end]

## Change log
| Version | Date | Changed by | What changed |
|---|---|---|---|
```

## Mistakes that make procedures fail

| Mistake | What goes wrong | Fix |
|---|---|---|
| **Wall of prose** | Nobody can follow it under pressure | Numbered steps, each with a clear action and a check |
| **Assumed context** | Works only for the person who wrote it | Explicit prerequisites, expected outcomes, and references to systems |
| **Happy path only** | No help when things go off-script | Decision points and escalation routes that cover the exceptions |
| **Stale contacts** | Escalating fails because the people behind the names have moved on | Refer to roles and channels rather than names, and set a maintenance cadence |
| **No verification steps** | The operator carries on without confirming success, and errors cascade | Add a check after each critical action |
| **Destructive steps without rollback** | No way back once an action does damage | Document an undo for any step that changes state |
| **Missing "do not" warnings** | Frequent mistakes go unflagged | Add cautions wherever a destructive mistake is likely |

## Ground rules

- **No technical details from training data.** System commands, IPs, URLs, and credentials all come from the user.
- **No invented contacts or numbers.** Escalation contacts, SLA times, and thresholds get a `[team to specify]` placeholder until the user supplies them; when the description is incomplete, name the gaps and ask.
- **No assumed stack.** Ask the user which technologies and communication channels they use.
- **Tag generated content** with its origin, using one of `[Source: your procedure description]`, `[Source: runbook methodology]`, or `[Source: placeholder — ops team to fill in]`, as applicable.
- **Mention the Word option.** Tell the user that, if they want a formatted Word file they can hand out, they can request the output as DOCX.
