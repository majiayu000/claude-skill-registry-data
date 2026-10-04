---
name: task-completion-web-dm-duo
description: >
  Task lifecycle protocol for web-research subagents in DM/Duo mode
  (no BBS). Extends the base task-completion protocol with a mandatory
  self-assessment checklist for source verification and coverage. Results
  are shared through `complete_task` summaries and targeted `send_message`
  DMs — there is no Bulletin Board System.
---

# Task Completion Skill (Web Research — DM/Duo)

## Task Lifecycle

Tasks are automatically assigned to you by the framework — you do not
need to claim them manually.

1. **Execute the task** — follow your domain skill's workflow to
   complete the work.
2. **Complete the task** — call `complete_task` with a thorough summary.
   Your summary is the ONLY way the orchestrator (DM mode) or the main
   worker (Duo mode) sees your findings. Include: the answer with exact
   numbers/names, the tools or method you used, the source URLs you
   relied on, and any caveats or uncertainties.
3. **Optional peer DM** — if your conclusion rests on a non-obvious
   assumption, hinges on a single primary source, or contradicts an
   earlier finding by a peer, follow `complete_task` with a targeted
   `send_message` to the relevant peer that calls out the assumption,
   source, or conflict. Skip this when the task is fully self-contained.

## Rules

- There is no `post_to_bbs` tool and no BBS channels (`#discoveries`,
  `#key-findings`, `#consensus`) in this run. Do NOT attempt to call them
  or reference them in your output.
- Focus on YOUR assigned task — don't try to do everything.
- You CANNOT create tasks for other agents. Only execute tasks assigned
  by the orchestrator.
- If a task fails or you cannot complete it, still call `complete_task`
  with an explanation of what went wrong.
- **Ordering rule**: call `complete_task` FIRST, then any follow-up
  `send_message`. The orchestrator trusts the task board, not your
  prose — a peer DM that mentions completion before the task is actually
  marked completed will be labelled `status=running` and ignored.

## Completion Self-Assessment (MANDATORY)

Before calling `complete_task`, run through this checklist:

1. **Coverage**: Did I address every dimension of the assigned task?
2. **Verification**: Did I cross-verify key facts from 2+ independent sources?
3. **Precision**: Am I using exact values, names, and terms from sources
   (not paraphrased or approximated)?
4. **Conflicts**: Did I identify and flag any conflicting information?
5. **Sources**: Did I include URLs for every factual claim in the
   `complete_task` summary itself — not just in some external store?

**If any item fails, do more work before completing.** Do not call
`complete_task` until you have genuinely exhausted your ability to
improve the answer. Default to doing MORE work, not less.
