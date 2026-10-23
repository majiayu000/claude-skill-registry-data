---
name: gz-how
persona: main-session
description: Use when the operator asks "how do I …?" or "what can I …?", or when unsure which skill applies or two look alike.
category: agent-operations
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
model: sonnet
metadata:
  skill-version: "1.0.2"
---

# gz-how

The map of how gzkit's skills fit together. Every skill belongs to a **flow**: a
path work travels, with an order, branches, and steps only the operator may take.
Find the flow, then say where the question sits in it.

This skill answers; it never acts and reads no project state. "What should I do
next *here*?" is `gz-status`'s question: it reads the ledger and the campaign.

## How to answer

1. **A question.** Match it in the question index, open the flow file it names
   under `references/`, and answer in this shape:
   - **Flow:** the flow, and where the question sits in it.
   - **Run:** the skill. Name a bare `uv run gz …` command only when no skill
     wraps the task.
   - **Not to be confused with:** the look-alike, when there is one.
   - **Only you can:** the steps reserved to the operator, if any.
   - **Then:** the next step in the flow.
2. **No question.** Answer "what can I do?": one line per flow, then the catalog.
3. **No match.** Say the question is not covered and show the flows. Never
   guess a skill. When an agent consulted this, it then runs the **Run** line
   itself.

## Question index

| How do I … / what can I … | Flow |
|---|---|
| set up gzkit in a repository, write a constitution or PRD | [Project setup](references/project-setup.md) |
| start or resume a session, see where things stand | [Session start](references/session-start.md) |
| turn an idea into an ADR, design something, promote a pool ADR | [Idea to ADR](references/idea-to-adr.md) |
| implement an OBPI, resume a pipeline, attest a brief | [OBPI delivery](references/obpi-delivery.md) |
| close out or validate an ADR | [ADR closeout](references/adr-closeout.md) |
| cut a release | [Release](references/release.md) |
| report, triage or fix a defect; file an issue | [Defects and GHIs](references/defects-and-ghis.md) |
| check, commit, push, sync mirrors | [Commit and sync](references/commit-and-sync.md) |
| change AGENTS.md or another canon surface | [Canon content](references/canon-content.md) |
| handle a complexity crossing | [Complexity](references/complexity.md) |
| run a chore, reduce tech debt, upgrade dependencies | [Codebase upkeep](references/codebase-upkeep.md) |
| validate governance surfaces, audit CLI docs, fix config paths | [Surface integrity](references/surface-integrity.md) |
| find out whether gzkit really works as intended | [Does it work?](references/does-it-work.md) |
| repair governance, undo a completion | [Repair](references/repair.md) |
| learn from outside tools or projects | [Looking outward](references/looking-outward.md) |
| trace what relates to what | [Traceability](references/traceability.md) |
| end a session or a phase | [Session end](references/session-end.md) |
| add, review or retire a skill | [Skill maintenance](references/skill-maintenance.md) |

## What can I do? (catalog)

Every active skill, under its flow. `gz validate --how-coverage` fails when a
skill is missing here, so this list cannot fall behind the catalog.

### Project setup

| Intent | Skill |
|---|---|
| install gzkit's scaffolding in a repository | `gz-init` |
| write or refresh the constitution | `gz-constitute` |
| write product requirements | `gz-prd` |

### Session start and end

| Intent | Skill |
|---|---|
| resume the last session, or write this one's handoff | `gz-session-handoff` |
| see workflow fronts, blockers and next actions | `gz-status` |
| enter or leave a unit of work; ad-hoc reconnaissance | `gz-airlock` |
| step back for the whole-project view (operator-invoked) | `gz-big-picture` |

### Idea to ADR

| Intent | Skill |
|---|---|
| shape an idea through design dialogue | `gz-design` |
| frame an open problem whose outcome is unknown (operator-invoked) | `gz-rnd` |
| book an ADR with its OBPI briefs | `gz-adr-create` |
| scaffold an ADR from the CLI | `gz-plan` |
| score an ADR and its OBPIs | `gz-adr-evaluate` |
| reason through a case before implementing | `gz-justify` |
| promote a pool ADR | `gz-adr-promote` |
| author or finish an OBPI brief | `gz-obpi-specify` |

### OBPI delivery

| Intent | Skill |
|---|---|
| audit the plan against the brief before coding | `gz-plan-audit` |
| run an OBPI from plan to attested completion | `gz-obpi-pipeline` |
| claim or release an OBPI lock | `gz-obpi-lock` |
| check a brief against the project tree | `gz-obpi-brief-drift` |
| review an OBPI's code for reuse and quality | `gz-obpi-simplify` |
| wrap QA commands in receipts for attestation | `gz-arb` |
| run Gate 2 for one ADR | `gz-implement` |
| reconcile briefs and the ADR table from the ledger | `gz-obpi-sync` |

### ADR closeout and release

| Intent | Skill |
|---|---|
| reconcile an ADR's evidence and ledger state | `gz-adr-sync` |
| witness and attest ADR completion | `gz-adr-closeout-ceremony` |
| audit a completed ADR to Validated | `gz-adr-audit` |
| record an ADR receipt event | `gz-adr-emit-receipt` |
| show ADR lifecycle and OBPI detail | `gz-adr-status` |
| cut a GHI-driven patch release | `gz-patch-release` |

### Defects and GHIs

| Intent | Skill |
|---|---|
| file an issue from inside gzkit | `ghi-author` |
| file an issue against gzkit from an adopter repo | `gz-issue-file` |
| rank the open issue queue | `ghi-triage` |
| do an issue's work and close it | `ghi-close` |
| record a course-correction, defect or discovery | `gz-insights-remember` |

### Commit and sync

| Intent | Skill |
|---|---|
| run the per-change quality gate | `gz-check` |
| commit and push through the guarded ritual (operator-invoked) | `git-sync` |
| regenerate mirrors after a skill or canon edit | `gz-agent-sync` |

### Canon content

| Intent | Skill |
|---|---|
| capture an entry into a surface's corpus | `gz-content-remember` |
| stage a candidate rendition | `gz-content-compose` |
| judge a candidate rendition before attestation | `gz-advisor-qc` |
| trim per-turn instruction load | `gz-context-diet` |

### Complexity

| Intent | Skill |
|---|---|
| preview complexity hints while writing | `gz-complexity-guide` |
| read the advisor's diagnosis of a crossing | `gz-complexity-advisor` |
| refresh the distilled complexity doctrine | `gz-complexity-distill` |

### Codebase upkeep

| Intent | Skill |
|---|---|
| run a maintenance chore | `gz-chore-runner` |
| survey technical debt | `gz-tech-debt-review` |
| find Java-flavoured shapes to make Pythonic | `gz-pythonic-pattern-detect` |
| record the evidence for an applied rewrite | `gz-pythonic-pattern-apply` |
| upgrade uv, Python and dependencies | `gz-deps-upgrade` |
| rank the foundation backlog | `gz-foundation-triage` |
| report maintenance findings | `gz-tidy` |

### Surface integrity

| Intent | Skill |
|---|---|
| run governance validators | `gz-validate` |
| audit CLI manpage and index coverage | `gz-cli-audit` |
| check configured and manifest paths | `gz-check-config-paths` |
| record bare-to-slug ID renames | `gz-migrate-semver` |

### Does it work?

| Intent | Skill |
|---|---|
| run the four-axis health audit (operator-invoked) | `gz-health-audit` |
| trace declared intent to shipped surface | `gz-intent-trace` |
| prove a workflow end to end on a target repo | `gz-flighttest` |

### Repair

| Intent | Skill |
|---|---|
| enter or leave the maintenance hangar | `gz-mx` |

### Looking outward

| Intent | Skill |
|---|---|
| scan competitor tools for moves (gzkit repo only) | `gz-competitor-radar` |
| scan AirlineOps governance parity (gzkit repo only) | `airlineops-parity-scan` |

### Traceability

| Intent | Skill |
|---|---|
| query the artifact graph and readiness | `gz-state` |
| map an ADR to the artifacts it produced | `gz-adr-map` |
| image the governance shape and a node's blast radius | `gz-ontology` |

### Skill maintenance

| Intent | Skill |
|---|---|
| review a skill against the code it wields | `gz-skill-review` |

### Namespace routers

Each picks a skill by intent; this guide explains the flow the skill sits in.
All are operator-invoked.

| Intent | Skill |
|---|---|
| design through release | `gz-workflow` |
| ADR, OBPI and ledger governance | `gz-governance` |
| quality and complexity | `gz-quality` |
| project lifecycle | `gz-project` |
| context preservation and orientation | `gz-context` |
| repository and release management | `gz-manage` |
| maintenance chores | `gz-chores` |

### Not in the catalog

- `gz-how` — this guide.

## Look-alikes

| You want | Use | Not |
|---|---|---|
| where things stand and what to do next | `gz-status` | this guide (what is possible) or `gz-state` (the artifact graph) |
| relationships, what is unattested, what is ready | `gz-state` | `gz-status` (fronts and next actions) |
| whether one OBPI is complete | `uv run gz obpi status`, a command | `gz-state` (its completion is Layer 2; read the ledger) |
| one ADR's lifecycle | `gz-adr-status` | `gz-state` |
| the per-change gate | `gz-check` | `gz-implement` (Gate 2 for one ADR, writes the ledger) or `gz-validate` (one validator) |
| a brief checked against the code tree | `gz-obpi-brief-drift` | `gz-obpi-sync` (brief against ledger evidence) or `gz-adr-sync` (a whole ADR, every layer) |
| an issue filed from inside gzkit | `ghi-author` | `gz-issue-file` (from an adopter repository) |
| a correction, defect or discovery recorded | `gz-insights-remember` | `gz-content-remember` (changes canon) |
| an idea you can state, shaped | `gz-design` | `gz-rnd` (open problem, outcome unknown) or `gz-plan` (an ADR already decided) |
| one issue's work done | `ghi-close` | `ghi-triage` (ranks the whole queue) |
| code reviewed | `gz-obpi-simplify` | `gz-tech-debt-review` (a debt survey) |
| attestation evidence | `gz-arb` | `gz-check` (a bare run produces no receipt) |
| complexity help while writing | `gz-complexity-guide` | `gz-complexity-advisor` (a crossing at commit) or `gz-complexity-distill` (the doctrine) |
| to know whether it really works | `gz-intent-trace` | `gz-health-audit` (it feels wobbly), `gz-flighttest` (prove a flow), `gz-big-picture` (the wide view) |
| Gate 5 on an ADR | `gz-adr-closeout-ceremony` | `gz-adr-audit` (verification after attestation) |
| governance repaired | `gz-mx` | `gz-airlock` (reconnaissance with light repair at most) |
| session memory | `gz-session-handoff` | `gz-airlock` (transit) or `gz-obpi-lock` (occupancy) |
| a skill picked by intent | a namespace router | this guide (the flow around it) |

## Phase boundaries

Decide at a boundary between phases, never mid-phase; mid-phase, continue or
hand a bounded track to a subagent.

- **Continue** when the next phase needs this one verbatim: design into booking
  the ADR, plan into the pipeline.
- **Subagent** for a bounded, independent track, dispatched with its Why
  (`AGENTS.md` § Behavior Rules).
- **Compact** when the context still matters and the session continues;
  `CLAUDE.md` § Compact Instructions says what must survive.
- **Clear** when nothing here matters next; the ledger and the handoff chain
  carry the state.
- **Handoff** (`gz-session-handoff`) at the end of every session, and as a
  `CHECKPOINT` to bookmark mid-flight. In gzkit a handoff is session memory and
  carries the operator's rulings forward, not only a way to move work elsewhere.
- **Airlock** (`gz-airlock`) when entering or leaving a unit of work. Transit,
  exchange and handoff are three subjects; the ruling that separates them is
  carried verbatim in `gz-session-handoff` § Three subjects.

See [Session end](references/session-end.md).
