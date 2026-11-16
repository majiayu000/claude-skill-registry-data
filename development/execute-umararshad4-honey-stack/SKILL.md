---
name: execute
description: "Use when the user says \"continue\", \"next\", \"do the TODOs\", \"run the plan\", or \"implement these tickets\", or a plan, ticket set or TODO.md is ready to build."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "obra/superpowers 7.0.0 skills/subagent-driven-development (+ task-reviewer-prompt.md), executing-plans, dispatching-parallel-agents; mattpocock/skills implement, to-tickets (frontier); cursor/plugins pstack 0.15.25 poteto-mode playbooks/autonomous-run, playbooks/feature (throughput checkpoint), swarm; MCT (local) skills/todo-orchestrator"
---

# Execute

Drain the queue to done in one continuous run. The user asked for the work, so do all of it: no "should I continue?", no progress check-ins between items. The checkboxes, the rulings and the final report are the record.

## 1. Load the queue

Take the first source that exists: what the user named, then unchecked plan tasks (`docs/plans/`), then the ticket frontier (open tickets whose blockers are done), then unchecked items in root `TODO.md`. The user's prompt wins when it conflicts with the queue.

For tracker work, read the latest `triage` brief, acceptance criteria and source discussion. If a reported bug lacks a reproduction or an existing PR already addresses it, read [the triage procedure](../triage/SKILL.md) as reference guidance before authoring a competing fix; do not implicitly invoke its standalone command. Use a project-local verification harness for the relevant journeys when available.

**Resume, don't redo.** Ticked items are done. After a compaction or in a new session, trust the checkboxes, ruling lines, `git log` and `git diff` over memory. Read the plan's global constraints and its design or spec once; the spec settles conflicts inside the plan.

**Classify each item:**
- **independent**: no shared files or interfaces with pending items
- **dependent**: needs another item's output; runs after it
- **blocked**: needs something outside the repo (an answer, access, a service)
- **risky**: destructive, auth, payments, migrations, shared config; runs sequentially with its own check

Split an item that hides two deliverables before starting it.

Done when: you have an ordered queue with each item's class and the check that proves it.

## 2. Pick the lanes

**Sequential by default.** Run items in parallel subagents only when they're independent and their files and checks are disjoint; a plan's parallel-lanes table, when present, already says which. Merging conflicting worker output costs more than parallelism saves.

Each worker brief stands alone: the item text with its exact values, the files it may touch, interfaces from earlier items, the verify command, and the report contract (`DONE`, `DONE_WITH_CONCERNS` or `BLOCKED`; files changed; the check's output). Workers do their own work and don't spawn reviewers. Batch several small same-shape edits (the same fix across ten files) into one brief.

Without a subagent tool, run every item inline in the same order.

## 3. Work each item

Keep the user's scope across turns. `continue` does not authorize new resources or destructive actions. For non-trivial work, use `honey task set` to name the operation, targets and required checks; `honey task status --json` shows the current evidence and diagnostic metrics. A new task starts without old proof. An inspection request stays read-only until the user asks for execution. These records never override host permissions.

1. Implement the smallest change that satisfies the item. For code changes, use the `tdd` skill where a clean seam exists. For system tasks, check the resulting state; keep inspection tasks read-only.
2. Run the `verify` skill with the item's check.
3. **Pass**: tick it (`- [ ]` → `- [x]`) in the plan or `TODO.md`. For GitHub tickets, leave the issue open and list it in the report; closing is the `ship` skill's job.
4. **Fail**: run the `debug` skill. Spend at most two fix rounds on one item, then write a blocker under it and move to the next item that doesn't depend on it:
   ```markdown
   - [ ] Import CSV with quoted fields
     - blocked: `npm test -- csv.test.ts` fails "unterminated quote" at row 3 after 2 fixes; needs a decision on RFC 4180 vs. the legacy export format
   ```

Done when (per item): its check passed this turn and the box is ticked, or a blocker line names the evidence and what would unblock it.

## 4. Rule, don't stall

Ambiguity, a plan defect, two instructions that disagree, a cap you'd have asked to exceed: decide and keep going. The spec outranks the plan, and your judgment settles what neither answers. Record each decision under its item, or at the end of the plan for cross-cutting ones:

```
Ruling: kept the legacy date format in exports — the spec only covers imports — cost if wrong: one formatter swap in export.ts
```

Four things stop the run, and only these:
- a destructive or irreversible action
- a product-defining choice that changes what gets built
- something needing credentials, accounts or paid services
- a contradiction where every path forward is a guess

Before stopping, finish every item that doesn't depend on the answer. Then send one decision brief covering just that stop.

## 5. Review every diff

The main thread reads every subagent diff (`git diff` over the worker's files); a worker's summary is a claim. Check that the diff stays inside its file boundary, does what the item says and nothing extra, and that the check output in the report is real.

- That read is the per-item review; run the `review` skill once on the whole queue's diff at the end.
- When the user requests an independent review, dispatch a fresh reviewer subagent with the item text, the diff, and the global constraints. It reports **spec compliance** first (missing, extra, misunderstood), then **quality** (Critical, Important, Minor, each with `file:line`). Critical and Important findings enter the fix rounds; Minor ones go to the report. The reviewer gets the diff, not your opinion of it.

After the last item, run once the broad checks the combined change warrants (full suite, typecheck, lint), rather than after every item.

Done when: every diff was read in the main thread and the broad checks ran.

## 6. Report

In order: items done, items blocked (with their evidence), every `Ruling:` line from this run (all of them, so the user can undo any), Minor findings, then the receipt. If the user asked for commits, make one per verified item.
