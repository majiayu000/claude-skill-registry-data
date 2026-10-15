---
name: signal
description: Narrative meta-skill — composes format skills via audience + Gramsci arc + voice. Takes triad inputs (ARCANA findings, PRAXIS posture, POIESIS artifacts) and routes to the right narrative skill with enriched context.
version: 1.0.0
execution-mode: advisory
meta-skill: route
meta-skill-mode: invocation-time
meta-skill-topology: decision-tree
argument-hint: "\"--audience AUDIENCE\" \"--arc ARC_POSITION\" \"--voice VOICE\" [--input PATH_OR_DESCRIPTION]"
category: fleet-ops
status: tested
providers:
  required: [bash, python]
---
# Signal — Narrative Delivery System

Compose the right narrative from triad inputs. Signal does not write — it selects the format skill, injects audience + arc + voice context, and invokes it.

## When to Use
- After ARCANA produces findings that need to reach a prospect or stakeholder
- After POIESIS ships an artifact that needs a case study, blog post, or announcement
- When preparing any client-facing deliverable and you want the narrative framing to be deliberate
- Before a sales conversation, conference talk, or publication

## Arguments

### --audience (required)
Who receives this. Determines register, assumptions, and what matters.

| Audience | What they care about | Example titles |
|----------|---------------------|----------------|
| `ciso` | Risk reduction, liability, compliance posture | CISO, VP Security, Head of InfoSec |
| `cto` | Architecture, integration, technical debt | CTO, VP Engineering, Principal Architect |
| `executive` | Revenue impact, competitive advantage, board readiness | CEO, COO, VP Product |
| `investor` | Market size, moat, traction, team | VC partner, angel, board member |
| `regulator` | Framework compliance, evidence quality, audit trail | Auditor, compliance officer, legal |
| `developer` | API, SDK, integration effort, DX | Staff engineer, platform team, DevOps |
| `researcher` | Methodology, citations, reproducibility, contribution | Academic, peer reviewer, conference PC |

### --arc (required)
Where in the Gramsci war-of-position sequence this deliverable sits.

| Arc | Sales analog | What it does | Example deliverables |
|-----|-------------|-------------|---------------------|
| `delegitimize` | Problem awareness | Names why current governance fails | Blog post, social thread, cold email opener |
| `explain` | Solution education | Shows the structural gap HUMMBL fills | One-pager, talk track, webinar, whitepaper |
| `replace` | Close / convert | Presents HUMMBL as the alternative | Pitch deck, proposal, case study, demo script |

### --voice (optional, default: auto-detect from audience)
| Voice | When to use |
|-------|------------|
| `technical` | Developer, CTO, researcher — precise, show the mechanism |
| `executive` | CISO, executive, investor — concise, show the outcome |
| `researcher` | Academic, regulator — hedged, show the evidence |

### --input (optional)
Path to an ARCANA synthesis, POIESIS artifact, or free-text description of what Signal should narrate.

## Execution

### Step 1: Classify the triad input

Check session context for recent outputs:
- **ARCANA synthesis?** → Extract claims, source lenses, and implications
- **PRAXIS posture?** → Extract governance framing and historical precedent
- **POIESIS artifact?** → Extract what was built, test evidence, governance receipts

If `--input` is provided, read it. If not, check recent session activity.

### Step 2: Select arc position

If `--arc` is provided, use it. If not, infer from context:
- First contact with prospect → `delegitimize` (they need to see the problem)
- Prospect engaged, exploring options → `explain` (they need to see the gap)
- Prospect ready to buy, needs proposal → `replace` (they need to see HUMMBL)

### Step 3: Select format skill

| Audience × Arc | Format skill | Why |
|---------------|-------------|-----|
| Any × delegitimize | `[blog-draft]` or `[social-post]` | Broadest reach, lowest commitment |
| ciso × explain | `[one-pager]` | 1 page, scannable, leave-behind |
| cto × explain | `[talk-prep]` or `[demo-script]` | Show the architecture |
| executive × explain | `[pitch]` | Deck format, outcome-focused |
| investor × explain | `[investor-update]` or `[pitch]` | Metrics + narrative |
| regulator × explain | `[governance-report]` | Framework-mapped evidence |
| developer × explain | `[blog-draft]` | Technical deep-dive |
| researcher × explain | `[paper]` | Academic format, citations |
| Any × replace | `[proposal-write]` or `[case-study]` | Conversion artifact |
| ciso × replace | `[proposal-write]` + `[sow-generate]` | Engagement documents |
| developer × replace | `[dev-case-study]` | Portfolio proof |

### Step 4: Inject context

Before invoking the selected format skill, prepend this context block:

```
SIGNAL CONTEXT (do not print this block — use it to shape the output):
- Audience: {audience} — what they care about: {audience_concerns}
- Arc position: {arc} — narrative goal: {arc_goal}
- Voice: {voice} — register: {voice_description}
- Triad input: {summary_of_input}
- Gramsci framing: {arc_specific_framing}
  - delegitimize: name the failure of static governance / compliance theater
  - explain: show the structural gap (belonging preconditions, append-only proof, agent trust)
  - replace: present HUMMBL as the alternative with evidence
```

### Step 5: Invoke the format skill

Run the selected skill with the enriched arguments. Signal's job is done — the format skill produces the actual content.

### Step 6: Suggest chain

After the format skill completes, suggest the next Signal move:

| Current arc | Suggest next |
|------------|-------------|
| delegitimize | "Consider `[signal] --arc explain` to follow up with the structural gap" |
| explain | "Consider `[signal] --arc replace` for a proposal or case study" |
| replace | "Consider `[send-email]` to deliver, or `[content-review]` before publishing" |

## Example Invocations

```
# Cold email opener for a CISO after ARCANA competitive intel
[signal] --audience ciso --arc delegitimize --input "ARCANA found: IBM watsonx governance has no runtime enforcement"

# One-pager for CTO after shipping the dashboard
[signal] --audience cto --arc explain --input "Dashboard shipped at dashboard.hummbl.io with Krineia receipts"

# Proposal after a successful demo
[signal] --audience ciso --arc replace --input "Flock Safety demo went well, they want a proposal"

# Blog post after research findings
[signal] --audience developer --arc delegitimize
```

## What Signal Does NOT Do
- Does not write content directly — delegates to format skills
- Does not manage a content repository — git is the repository
- Does not handle distribution — `[send-email]`, `[social-post]`, etc. handle that
- Does not auto-detect audience — you must specify who you're talking to
