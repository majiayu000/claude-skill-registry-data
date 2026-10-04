---
name: agency-design
description: Use when designing an AI-native product, feature, or workflow where humans and AI agents share the work, to decide who does what and who holds which decisions. Walks each key step to set its level of autonomy (Level 1 human asks and AI answers, Level 2 human assigns and AI executes, Level 3 human and AI assign to each other), the decision rights, the approval gate, and how human agency is amplified, plus the team roster of who can task the agent and who holds each gate, then produces a one-page Agency Map. Use when the user asks about human-in-the-loop, agent autonomy, approval gates, trust, or the human-AI division of labor, or runs /agency-design.
---

# Agency Design

The Discover-phase skill for the *human* side of AI-native work. `goal-and-constraints` finds the goal and the bottleneck; `agency-design` designs the human-AI relationship: who leads, how far the AI acts on its own, and where the approval gates sit. It keeps humans in the lead as autonomy grows, so **AI amplifies human agency, it does not replace it.**

Run it when you are building anything where humans and agents share work: a chat assistant, a workflow automation, or an autonomous action system. The output is a one-page **Agency Map**.

It walks the four lenses of AI fluency (the **4D** framework: **Delegation, Description, Discernment, Diligence**). Delegation is which level a step sits at; Description is what the human must specify for the AI to execute; Discernment is the verification that earns the level; Diligence is who owns the result and whether AI use is disclosed. The steps below map to these four.

## The three levels of autonomy

Every step sits at one of three levels, defined by **who assigns the work**:

- **Level 1: Human asks, AI answers** (AI chat, copilots). The human drives every turn; the AI advises.
- **Level 2: Human assigns, AI executes** (agentic workflow automation). The human delegates a task or goal; the AI runs the multi-step work; the human reviews.
- **Level 3: Human and AI assign tasks to each other** (autonomous actions). The AI initiates and hands work back to humans or other agents; the human supervises and collaborates.

Two rules govern the levels:

1. **Climb a level only as trust and verifiability are earned.** Level 3 is not a finish line to rush to; it is a right earned per step.
2. **One product mixes levels.** Assign a level per *step*, not one level for the whole product. Judgment stays at Level 1; routine work moves to Level 2; only well-verified, low-stakes actions reach Level 3.

## Roles: who tasks the agent, who holds the gate (team settings)

The levels answer *how far* the AI acts. In a team, also answer *who* it acts with. Most AI-native work is multiplayer: many humans and one or more agents sharing a workspace, not one human and a personal assistant. Name the roster: which humans and which agents are on the team, what each owns, who can task the agent, and who the agent may proactively surface work to. State the roles only a human holds: setting the goal and the north star, and decisions with hard tradeoffs. An agent surfaces a sensitive decision, it does not make it. Keep the shared context legible: agents act on what is written down and accessible, so work in the open and audit it.

## What to do

First, list the key steps or decisions in the workflow (pull them from the Goal & Constraint Brief if you have one). In a team setting, also name the roster (see above): who is on the team, who owns what, who can task the agent, and who it may proactively surface work to. Then interview the user briefly and, for each step, decide:

1. **Level (Delegation).** 1, 2, or 3, and who assigns the work. Confirm the step is within the model's reliable capability (its knowledge, working-memory limits, and steerability); do not raise a step to Level 2 or 3 on optimism. This links back to the feasibility risk in the Brief.
2. **Who leads (AI or Human).** State plainly who is responsible for the step: the AI (it executes), the Human (they lead and the AI assists), or the AI acting with human override.
3. **Description (what the human specifies).** What must the human state for the AI to execute this reliably: the task, the context it needs, and the done criteria. This is the Level 2 handoff contract, made explicit rather than assumed.
4. **Approval gate.** What must a human approve before it happens? High-stakes, irreversible, or customer-facing actions get a gate; low-risk, reversible ones may not.
5. **How human agency is amplified.** What higher-leverage work does raising this step free the human to do? If the honest answer is "nothing, the human is just removed," that is a red flag: autonomy rose without lifting the human.
6. **Trust and verifiability (Discernment).** What evidence justifies this level (evals, audit log, override rate), and what would let it climb higher next cycle? Make the evidence concrete: task-verification checklists, rubrics and style guides, tests, and a doer-verifier pattern where one agent verifies another's work before a human looks. Name the bar: pass@k (can it ever succeed) versus pass^k (does it succeed every time), with pass^k required before a step reaches Level 3 or customer-facing autonomy. The `eval-driven-development` skill produces this evidence. A step earns its climb when it can verify itself before a human does. This step names what earns a climb; `responsible-autonomy` governs how fast the ceiling is allowed to rise across cycles, and holds the downward brake.
7. **Diligence (own the result).** Name the human accountable for this step's output, and whether AI involvement is disclosed where it is customer-facing. Higher autonomy never removes accountability; someone still owns the result.

Then **flag the constraint:** mark the one step where the flow waits on a human (the approval bottleneck), and confirm that gate is intentional, not accidental. Keep it to a single flag; the full constraint analysis is `goal-and-constraints`, not this skill.

Fill `references/agency-map-template.md`, save it as `agency-map.md` in the working project, and show it to the user.

## Self-check before you finish

- Every key step has a level (1/2/3), a clear lead (AI or Human), and an explicit gate (or "none, and why").
- Each raised step is within the model's reliable capability, not raised on optimism.
- No step is at Level 2 or 3 without named trust/verifiability evidence (autonomy is earned, not assumed); customer-facing or Level 3 steps name the pass^k reliability bar.
- Every step names a human owner accountable for the result, and any customer-facing AI output is disclosed (Diligence).
- For each raised step, the human's higher-leverage work is named (agency amplified, not just removed).
- Every high-stakes, irreversible, or customer-facing action has a human-approval gate.
- The constraint is flagged (the step where flow waits on a human) and confirmed intentional.
- In a team setting, the roster is named: who can task the agent, who holds each gate, and the roles only a human holds.
- The map serves the goal and relieves the constraint without breaking trust.

## The two failure modes it prevents

- **Too much AI:** acting where trust is not yet earned breaks adoption. Curated and audited, never spray-and-pray.
- **Too much human:** approving everything makes approval itself the bottleneck. Good design frees human attention for the steps that actually need judgment, and has the agents batch and elevate only the most important decisions rather than interrupting for each one, so the gate stays sustainable.

## The constraint often lives here

For AI-native work the agency boundary is frequently the real constraint (the approval bottleneck), and the make-or-break risk (a capable agent people do not trust gets switched off). Designing agency up front surfaces both, which is why this belongs in Discover.

## Phase state (for the GOAL status-line HUD)

This is a Discover-phase design pass. If the user runs the HUD (`docs/statusline.md`), create or update `.goal/state.json` in the working project with `{ "phase": "Discover", "project": "<the project folder name>" }` at the start of this pass.

## Hand off

The Agency Map feeds the rest of the lifecycle: the levels and gates become requirements in Specify (OpenSpec) and Build (Superpowers). Revisit it each cycle, as trust accrues, steps earn their way to a higher level. The rate of that climb across cycles, and the brake that can lower it, are governed by `responsible-autonomy`, whose Responsible Autonomy Sheet rides alongside this map.

See `references/examples/agentic-triage-agency.md` for a worked Agency Map on an AI-native multi-agent product.
