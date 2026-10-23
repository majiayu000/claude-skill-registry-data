---
name: procedure-promote
description: Promote a repeated, verified Yarbrain procedure candidate into a user-owned Agent Skill or propose an update to an existing one. Use after the same procedure succeeds in independent episodes or when the user explicitly requests reusable automation; do not promote facts, policy, or unexplained workarounds.
---

# Promote a Procedure

Turn proven know-how into a reusable procedure without modifying installed
plugin content or activating unreviewed instructions.

## Qualification

Promote a candidate only when the user explicitly requests it or at least two
independent episodes show the same successful procedure. The steps must be
stable, prerequisites identifiable, and success verifiable.

Reject project facts, one-off fixes with unknown causes, behavioral policy that
belongs in agent instructions, and procedures whose safe scope cannot be stated.
Leave an ineligible candidate unchanged and report it as deferred.
An explicit promotion request does not waive these evidence and safety checks.

## Workflow

1. Read the candidate and every supporting episode. Confirm the evidence shows
   success rather than a proposed or partially completed approach.
2. Search the vault's skills/ tree and the user's configured Agent Skill
   directories for the same trigger and outcome.
3. Draft either a new skill or a focused patch to an existing skill under
   inbox/skills/. Do not create a near-duplicate. If the current request does
   not authorize a vault write, show the draft without storing it.
4. Use lowercase kebab-case and frontmatter containing exactly name and
   description. The description must state both what the skill does and when it
   applies.
5. Include prerequisites, ordered steps, verification, meaningful failure
   modes, safety and authority boundaries, and a Provenance section naming the
   source episodes and last successful verification.
6. Show the complete proposal. Promote it to the vault's skills/<name>/SKILL.md
   or another user-approved skill directory only after explicit approval.
7. Validate the promoted skill with the target agent's native validator when
   available. Do not claim it is active until the target agent can discover it.

Do not patch a skill based on name alone. If distinct procedures would use the
same name, choose an unambiguous trigger-based name or stop for the user's
decision; never overwrite the existing skill.

Preserve procedure history through provenance rather than historical commentary
inside the operational steps.
