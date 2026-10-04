---
name: resume-bod
description: "Resume the BOD/Agency Council kickoff workflow in a new chat session — restores context from memory, summarizes prior state, and reassembles the full 12-person council in two waves. Trigger when the user invokes /resume-bod, /bod-resume, 'resume the board', 'continue council workflow', or 'pick up where BOD left off'. Also for: checking whether a prior team still exists before creating a new one (reuses existing if intact), assembling a focused sub-council (engineering, GTM, or marketing only) when a full board isn't needed, and confirming project identity from ~/.claude/memory/medium-term.md before proceeding. The two-wave spawn policy (6 leaders max per wave) prevents team config corruption. After context is restored, offers explicit next actions: assemble full council, assemble focused team, or skip and continue solo."
---

# Resume BOD — Continue Council Workflow in New Session

Use this skill to restore context and continue The Agency council workflow without re-deriving state manually.

---

## When Invoked

Trigger on:
- `/resume-bod`
- `/bod-resume`
- "resume the board"
- "continue council workflow"
- "pick up where BOD left off"

---

## Step 1: Load Session Context

1. Read `~/.claude/memory/medium-term.md`
2. Identify the active project and confirm whether `agency-agents` is the target
3. Read the target project's `PROJECT.md`
4. Read latest session log at `{project}/memory/sessions/YYYY-MM-DD.md` (most recent)

If project is ambiguous, ask the user to choose from active projects before proceeding.

---

## Step 2: Summarize Prior BOD State

Summarize in 5 bullets max:
- Last completed phase / milestone
- Current status and blockers
- Last known council/team state
- Key constraints (Tier rules, approvals)
- Next recommended action

Do not re-explore the codebase unless PROJECT.md is stale or missing critical state.

---

## Step 3: Offer Council Assembly

After context summary, offer explicit next actions:

- **Assemble full council now** (`BOD`, `assemble`, `the board`, `the council`)
- **Assemble focused team** (engineering / gtm / marketing / custom)
- **Skip assembly** and continue solo planning

If user confirms assembly, proceed immediately.

---

## Step 4: Assemble via TeamCreate + Two-Wave Spawn

For full council:

1. Create team `agency-council` via `TeamCreate`
2. Spawn leaders in TWO WAVES (max 6 each):

Wave 1:
- engineering-lead
- design-lead
- game-development-lead
- marketing-lead
- sales-lead
- paid-media-lead

Wave 2:
- product-lead
- pm-lead
- testing-lead
- operations-lead
- specialized-lead
- spatial-lead

3. Wait for wave 1 join acknowledgements before wave 2
4. Send council kickoff brief after all 12 are online

Never spawn all 12 in a single parallel burst — it can corrupt team config writes.

---

## Step 5: Kickoff Brief Template

Use this message format:

```
TYPE: council-assembly
PURPOSE: project-resume
PROJECT: [project name]
SCOPE: [brief]
DEPARTMENTS_NEEDED: [list]
TIMELINE: [urgency]
PROJECT_LEAD: [team-lead]
---
[What was completed previously]
[What remains]
[Decisions needed now]
```

Then request each leader's dept perspective (deliverables, dependencies, risks).

---

## Step 6: Resume Execution Loop

After leader replies:
1. Synthesize shared plan
2. Assign work packages
3. Enforce tiers:
   - Tier 1 = leader approves
   - Tier 2 = escalate to parent AI
   - Tier 3 = escalate to human
4. Report concise checkpoint summary to user

---

## Key Rules

- Read memory first, spawn second
- Treat PROJECT.md as source of truth unless user says otherwise
- Use 2-wave spawn policy every time
- Keep kickoff summaries concise and decision-focused
- If prior team still exists, reuse it instead of creating duplicate team
- If team config looks corrupted, shutdown, clean up, then recreate
