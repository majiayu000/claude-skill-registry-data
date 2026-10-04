---
name: assistant-telos
description: "Create or update Telos purpose, mission, goals, challenges, and strategies. Use for explicit purpose or Telos work."
---

# Telos — Deep Context Framework

## Contracts

| Contract | File | Purpose |
|---|---|---|
| **Input** | `contracts/input.yaml` | Action (create/update/review), entity type, focus sections |
| **Output** | `contracts/output.yaml` | TCF file, sections completed, review findings |

**Rules:**
- Create action must produce a TCF with at minimum: problems, mission, goals
- Review action must assess every section's completeness
- Existing TCF must be located before update/review proceeds

Based on [Daniel Miessler's Telos](https://github.com/danielmiessler/Telos) — an open-source framework for creating Deep Context about things that matter to humans.

**Core idea:** Help entities of any size — individuals, teams, organizations — articulate what they are about and how they're pursuing their purpose. The output is a Telos Context File (TCF) that gives AI agents strategic context about *why* you do what you do.

## Goal

Create, update, or review Telos Context Files that connect problems, mission, goals, strategies, projects, and lived progress.

## Success Criteria

- Create actions produce at least Problems, Mission, and Goals.
- Updates preserve existing sections and change only the requested focus areas.
- Reviews identify missing, weak, stale, or disconnected sections.
- Projects and strategies trace backward to mission and problems.

## Constraints

- Do not invent personal values, goals, history, or organizational facts.
- Ask when a missing answer would change the user's mission, goals, or strategic framing.
- Keep sensitive personal content out of durable files unless the user explicitly provides and approves it.

## The Explainability Chain

```
Problem  →  Mission  →  Narrative  →  Goal  →  Challenge  →  Strategy  →  Project  →  Journal
  (why)      (what)      (story)     (target)   (blocker)     (how)       (doing)     (living)
```

Every item traces backward. If a project can't connect to a problem, question why it exists.

## Two TCF Types

Telos supports both personal and organizational context files. Both use the same core chain but differ in scope.

### Personal TCF

Full sections (in order):

| Section | Prefix | Purpose |
|---|---|---|
| **Document Purpose** | — | What this file is and how sections connect |
| **History** | — | Background that shapes your perspective |
| **Problems** | P1, P2... | Issues in the world that genuinely move you |
| **Mission** | M1, M2... | What you're building/doing to address the problems |
| **Narratives** | N1, N2... | How you explain yourself: "I believe [P] matters, so I'm [M]" |
| **Goals** | G1, G2... | Specific, time-bound targets (mix personal + professional) |
| **Challenges** | C1, C2... | Concrete obstacles blocking progress |
| **Ideas** | I1, I2... | Current beliefs, principles, and convictions |
| **Predictions** | — | Forecasts with confidence percentages |
| **Wisdom** | — | Distilled life lessons and principles |
| **Metrics** | K1, K2... | Measurable indicators of progress on goals |
| **Projects** | — | Active work, each linked to a strategy/goal |
| **Journal/Log** | — | Dated entries tracking the lived experience |

Optional personal sections: Things I've Been Wrong About, Best Books, Best Movies, Traumas.

### Corporate/Team TCF

Adds organizational structure on top of the core chain:

| Section | Purpose |
|---|---|
| **Company History** | Origin story and market context |
| **Company Mission** | Organizational purpose |
| **Company Goals** | G1, G2... ranked by importance (each half as important as previous) |
| **Company KPIs** | K1, K2... measurable metrics tied to goals |
| **Team Mission** | Team-specific purpose within the organization |
| **Team Goals** | SG1, SG2... team objectives with deadlines |
| **Team KPIs** | SK1, SK2... team metrics (e.g., time-to-detect, remediation speed) |
| **Risk Register** | R1, R2... key organizational vulnerabilities |
| **Strategies** | Approaches addressing challenges and risks |
| **Infrastructure Notes** | Technology stack and platform details |
| **Team** | Members, skills, assignments (table format) |
| **Projects** | Active work with priority, timeline, status, cost (table format) |
| **Current State** | Timestamped activity log tracking KPI changes over time |

## Storage

Telos Context File lives at `~/{agent_state_dir}/telos.md` — global, cross-project, loaded at every session start.

For team/corporate context in a specific repo, use `{agent_state_dir}/telos.md` at the project root.

## Commands

### Create (`telos create` / first time)

Ask: "Personal or team/project context?" Then walk through the relevant sections.

**Personal TCF creation — walk through one section at a time:**

**Step 1 — History**
> "Tell me about your background — what shaped how you see the world?"

Brief biographical context. Keep it to what's relevant.

**Step 2 — Problems**
> "What problems in the world genuinely bother you? Not theoretical — things you feel emotionally compelled to address."

Capture as P1, P2, etc. Each should be specific enough to act on.

**Step 3 — Mission**
> "What are you building or working toward to address those problems?"

Capture as M1, M2, etc. Each mission should connect to a problem.

**Step 4 — Narratives**
> "How would you explain this to someone? Format: 'I believe [problem] is important, which is why I'm [mission].'"

Capture as N1, N2, etc. These are the sentences you'd actually say.

**Step 5 — Goals**
> "What does success look like? Be specific — include deadlines where possible."

Capture as G1, G2, etc. Mix personal and professional.

**Step 6 — Challenges**
> "What's actually blocking you right now? Be concrete."

Capture as C1, C2, etc. Not "lack of time" but "spending 60% of time on ops instead of product."

**Step 7 — Optional sections**

Ask if they want to capture any of: Ideas (current beliefs), Predictions (with confidence %), Metrics (measurable KPIs), Wisdom (life principles).

Don't push — these are valuable but not required for a useful TCF.

**Step 8 — Projects**
> "What are you actively working on? Each should connect back to a goal or mission."

List with connections to the chain.

After each step, confirm with the user before moving on. When complete, write `~/{agent_state_dir}/telos.md`.

**Corporate/Team TCF creation** follows the same pattern but with organizational scope — company goals, team structure, KPIs, risk register, project tables.

### Update (`telos update` / `update telos`)

Read the existing `~/{agent_state_dir}/telos.md`, present it, and ask what changed. Common updates:
- New project → verify it connects to the chain
- Goal achieved → celebrate, remove or mark done, add next one
- Challenge resolved → update strategies
- Mission evolved → cascade changes down the chain
- Add a journal entry → dated log of what's happening
- Update predictions → adjust confidence percentages

### Review (`telos review` / `review telos`)

Read `~/{agent_state_dir}/telos.md` and check the explainability chain:
- Does every project trace back to a problem?
- Are there orphan projects (no chain connection)?
- Are there goals with no active projects (stalled)?
- Are there challenges with no strategies (unaddressed)?
- Are predictions aging? (check dates vs. confidence)
- Are metrics being tracked? (any stale KPIs)

Present findings as a health check, not a lecture.

### Apply (`telos apply` / when starting work)

When beginning a task, optionally check it against telos:
- Which problem does this serve?
- Which goal does this advance?
- Is this the highest-leverage thing to work on right now?

This is a gentle filter, not a gate. The user decides.

## Stop Rules

- Stop and ask before creating or rewriting mission-critical sections from assumptions.
- Stop and report gaps when no existing TCF can be found for update/review.
- Do not persist sensitive personal context unless the user explicitly asks to include it.

## TCF File Format (Personal)

Use Daniel Miessler's prefixed identifier system:

```markdown
# Telos Context File
*Last updated: YYYY-MM-DD*

## Document Purpose
This is my personal TCF. It captures what I'm about and how I'm pursuing my purpose.
Path: Problems → Mission → Narratives → Goals → Challenges → Strategies → Projects → Journal.

## History
- [biographical context]

## Problems
- P1: [problem]
- P2: [problem]

## Mission
- M1: [mission addressing P1]
- M2: [mission addressing P2]

## Narratives
- N1: I believe [P1] matters, which is why I'm [M1].

## Goals
- G1: [specific goal with deadline]
- G2: [specific goal with deadline]

## Challenges
- C1: [concrete obstacle]
- C2: [concrete obstacle]

## Ideas
- I1: [current belief or conviction]

## Predictions
- [prediction statement] ([confidence]%)

## Metrics
- K1: [measurable indicator tied to a goal]

## Projects
- [project name] — [description] → G1, M1

## Journal
- [DD/MM/YYYY]: [entry]
```

## How Agents Use Telos

When `~/{agent_state_dir}/telos.md` is loaded at session start:
- **Ideation**: Score ideas partly on telos alignment — does this serve the mission?
- **Planning**: When multiple approaches exist, prefer the one aligned with stated goals
- **Prioritization**: If the user asks "what should I work on?" — consult telos
- **Reflection**: At task completion, note if the work advanced a goal
- **Context**: Understand *why* the user cares about this project, not just *what* to build

Telos is context, not constraint. It informs decisions but never blocks work the user explicitly requests.

## Output

Return:
- **Action taken** - created, updated, reviewed, applied, or no changes needed.
- **TCF location** - path to the Telos Context File read or changed.
- **Sections** - sections completed, updated, reviewed, or still missing.
- **Findings** - chain health, orphaned items, stale entries, or strategic alignment notes.
- **Open questions** - decisions or missing context needed before the next Telos update.
- **Status** - created, updated, reviewed, applied, or blocked by missing TCF/context.

## Rules

- **Conversational, not ceremonial** — this should feel like useful reflection, not a form
- **User's words, not yours** — capture their language, don't rephrase into corporate-speak
- **Prefixed identifiers** — use P1/M1/G1/C1/K1 format for cross-referencing
- **Living document** — encourage regular updates; stale context is worse than no context
- **No judgment** — if a project doesn't connect to the chain, point it out gently
- **Privacy first** — TCF may contain personal aspirations and history; never share or log externally
- **Right-sized** — personal TCF should stay under 80 lines; include only sections that add value
