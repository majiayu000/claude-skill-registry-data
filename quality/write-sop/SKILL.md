---
name: write-sop
description: Writes a standard operating procedure from a process description - purpose, scope, roles, numbered steps, checks and exceptions - with gaps flagged for confirmation. Use to document a repeatable task.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: operations
  source: https://hermes-ide.com/prompts/write-sop
  catalog: 2026.1014.1
---

# Write a standard operating procedure

## Inputs

- [PROCESS] (required): How the task is done today - a walkthrough, notes, a recorded explanation transcript, or an old document. Include who does what, tools used and known problems.
- [AUDIENCE] (optional): Who will follow the SOP and their experience level (for example "new warehouse staff in their first week").
- [FORMAT] (optional; one of: checklist, narrative, table; default: checklist): How to present the procedure steps.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
You write SOPs that people follow under real conditions: a new hire on a busy day, someone covering for a colleague, or an auditor checking compliance. A good SOP has one action per step, says how to know each step worked, and covers what to do when things go wrong. It never pretends to know a threshold, a tool setting or an approval rule that the source did not give.
</context>

<task>
Write an SOP for this process:

<process>
[PROCESS]
</process>

Audience: [AUDIENCE]
Step format: [FORMAT]

1. Identify the start trigger, the end state, and every role involved. If the process description mixes several processes, write the SOP for the main one and list the others under Open questions.
2. Write the procedure:
   - one action per step, starting with a verb ("Scan the delivery note"), in the order it actually happens;
   - name the tool, form or system used in each step, exactly as given;
   - add a check after any step where a mistake is likely or costly ("Confirm the count matches the delivery note");
   - mark decision points clearly with what to do in each case;
   - put warnings before the step they apply to, not after.
3. Present the steps in the requested format: `checklist` as numbered checkbox steps, `narrative` as short numbered paragraphs, `table` with columns Step | Who | Action | Check.
4. Add exceptions: the realistic ways this process goes wrong and what to do, including who to escalate to and when.
5. Match vocabulary to the audience. If the audience is empty, write for a capable new team member with no prior context, and say so.
6. Wherever the source is unclear or silent on something the SOP needs (a limit, an approver, a time), write `[CONFIRM: what is needed]` in place and list it under Open questions.
</task>

<constraints>
- Do not invent thresholds, approval limits, system names, legal or safety requirements. Use `[CONFIRM: …]` instead.
- Keep steps short: about 25 words or fewer each. Split longer ones.
- If the process involves safety, food handling, money or personal data, keep every control step from the source and flag any missing control as an open question rather than adding your own rule as fact.
- No filler introductions. The Purpose section is at most two sentences.
</constraints>

<output_format>
# SOP: <process name>
Version, owner and review date as `[CONFIRM]` placeholders unless given.

## Purpose
## Scope
What it covers and what it does not.
## Roles
Table: Role | Responsibility.
## Before you start
Inputs, access and materials needed.
## Procedure
In the requested format.
## Quality checks
Bullets: what is checked at the end and by whom.
## Exceptions and escalation
Table: Situation | What to do | Escalate to.
## Records
What is recorded, where, and how long it is kept, or `[CONFIRM]`.
## Open questions
Numbered list of every `[CONFIRM]` item.
</output_format>
