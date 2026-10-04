---
name: goal-setter
description: Draft, review, or activate a compact /goal when the user wants Codex to keep working until a verifiable result is true. Defines the result, evidence, boundaries, stop conditions, and only useful delegation. Not for ordinary implementation, Q&A, one-off edits, loose brainstorming, or subjective work with no completion test.
---

# Goal Setter

Turn a rough request into a compact `/goal`: the result to achieve, the evidence that proves it, the boundaries that matter, and when Codex should finish or stop. A Goal is a completion contract, not an implementation plan or a second task system.

Prefer the shortest Goal that preserves the user's real outcome. State each rule once. Leave file discovery, implementation order, agent count, models, and tool details to the running Codex task unless the user fixed them.

## Decide whether a Goal fits

Use a Goal when one objective may take many checks or turns and completion can be judged from tests, artifacts, runtime state, screenshots, measurements, sources, or a clear rubric.

Use a normal prompt for a small edit, explanation, or review. If the request is subjective and has no usable completion test, help define the test first instead of pretending the Goal is verifiable.

## Understand before drafting

If tools are needed, first tell the user in one or two sentences what evidence you will inspect. Read the smallest useful set of code, docs, sources, or existing artifacts. Do not begin implementation during Goal intake.

Answer three questions:

1. What result does the user actually need?
2. What observable evidence would prove it?
3. What must be learned before those answers are safe?

For a working system or user-facing artifact, trace the real path from user input to the expected output or state. A mock, screenshot, scaffold, fake service, or isolated component does not satisfy a request for a working result unless the user allowed that substitute.

Ask only when a missing answer could change the result, evidence, scope, safety boundary, or stopping condition. If the user explicitly asks to be interviewed or stress-tested, keep asking material questions under the same rule. Check discoverable facts instead of asking. When one answer determines the next question, ask one at a time; otherwise bundle independent blockers. Stop asking once an honest Goal can be written. Make low-risk reversible assumptions explicit and continue.

For uncertain research, name the decision the work should enable, the leading and competing explanations, evidence that would weaken them, and the point at which further searching is unlikely to change the conclusion.

## Write the Goal

Write plain prose in the user's terms, without labeled fields. Start with the final state and who it serves. Add only clauses whose removal could change the result, evidence, boundary, iteration, or stopping decision.

Cover what matters for this task:

- **Result and evidence.** Name the final state and the concrete place it will be checked. Named requirements need their own evidence; nearby examples or substitutes are supporting evidence only.
- **Real path.** For systems and experiences, require the smallest complete user path through the real runtime, data, service, storage, or generated artifact. Visible primary controls must work, be honestly marked unavailable, or be omitted. Check both the parts and the whole when a list of passing items could hide a broken experience.
- **Read first.** Name at most one or two important anchors, then let Codex discover adjacent files and tests. Do not turn the Goal into a file inventory.
- **Boundaries.** Keep the change to the smallest result that satisfies the request. Update an existing primary document, report, sheet, or tracker instead of creating a duplicate. Name only the few public behaviors, safety rules, permissions, data, billing, or compatibility boundaries that this task could actually break. Do not weaken tests or required behavior to make a check pass.
- **Validation.** Use the most relevant honest check. Reproduce bugs before fixing them; measure performance with a stated method; run the focused tests and integration path for code; use the real browser or equivalent for UI; map material research claims to sources and try once to disprove the leading conclusion. When success, failure, timeout, or another distinct result matters, require evidence that each relevant result actually occurred; a check that could not have failed proves nothing. If full validation is unavailable, require the next honest check and report the gap.
- **Done.** Completion is pass/fail and covers the whole requested result. Codex checks its own diff, output, and evidence before Done. A correctness, safety, or completion finding blocks; other improvements remain the lead's judgment.
- **Long runs.** Only when useful, keep a short `execution-notes.md` with open checks, evidence, pass/fail/blocked state, and material decisions. If Done is false and no stop condition applies, continue with the riskiest or least-certain open check; do not stop at a plan or unverified next steps. Do not keep a verbose activity log or duplicate the active Goal in `GOAL.md`.
- **Stop.** Stop and report the exact blocker after about three genuinely different failed approaches, when required access or approval is unavailable, or when proceeding would change the agreed result, scope, schema, authentication, billing, production state, or destructive boundary.
- **Final report.** Write for someone who saw none of the run. Lead with the outcome and current evidence. Name blocked or unchecked requirements and any material decision the Goal left to Codex.

Use firm words only for real invariants. Do not add generic warnings, exhaustive edge cases, a fixed phase plan, or ordinary command-level parallelism.

## Use subagents only when they help

Subagents are useful when an independent investigation, isolated noisy work, separate implementation area, or independent verification could materially change Done. Low-risk work with decisive automated checks usually needs none.

When delegation is needed, the Goal should directly require the named work to be delegated and require its evidence to be considered before Done. Do not copy runtime tool schemas, model settings, agent names, counts, or scheduling instructions into the Goal.

During execution:

- One lead owns the user's outcome, integration, consequential decisions, final verification, and Done.
- Give each agent one bounded task with its scope, relevant constraints, evidence to return, and stopping condition. Do not pass the whole conversation when a smaller context is sufficient.
- Continue an existing agent when the next task depends on what it already learned. Start a new agent for a genuinely independent line of work or a clean independent review.
- An agent may delegate a smaller independent part when that reduces context or time. Keep ownership clear and avoid delegation chains that add coordination without changing the result.
- The lead continues non-dependent work while agents run. Wait only when their result is needed for the next decision, integration, or completion claim.
- Agents share the working files. Parallel writes require clearly separate owned areas and separate checks. One agent and the smaller tasks it delegates own each area; overlapping or tightly coupled writes stay with one owner.
- Independent verification uses a new read-only agent with the actual artifact and acceptance criteria, not the author's reasoning or a desired verdict. After a material repair, rerun the affected checks and use a new independent review when judgment still controls acceptance.

Keep this adaptive. Do not prescribe a fixed worker count, hierarchy depth, role list, or sequence. The running task chooses the smallest useful shape from current evidence, dependencies, cost, and remaining uncertainty.

`create_thread` is different: it creates a separate user-owned Codex task. Use or mention it only when the user explicitly asks for separate tasks, threads, or worktrees. For several parallel write tasks, require stable non-overlapping ownership, separate validation, understood shared interfaces, a usable Git/worktree base, and time savings that justify integration. Give each task one owned result, its evidence, and its integration rule. Do not use separate tasks merely because work can be divided, and do not create repository structure only to enable them.

Claude Code may realize the same outcome and evidence rules with its own delegation features. Do not force Codex-specific tool details into portable Goal text.

## Length

Start with one sentence or one short paragraph. Complex Goals commonly fit within 800–1,800 characters; 2,500 characters should trigger another compression pass. The runtime hard limit is 4,000 characters.

Run `python3 -B scripts/validate_goal_length.py <file>` once when practical. Passing the length check does not prove that the Goal is good.

## Activate

Use the runtime's native Goal tool when available. In Codex, check `get_goal` first and reuse a matching active Goal instead of creating a duplicate, then use `create_goal` unless the user asked only for a draft. If no native Goal tool exists, return the exact `/goal ...` line. Never claim the Goal was set unless it was.

Before activating, confirm that the result, evidence, important boundaries, stopping condition, and any necessary delegation are clear and proportionate. Remove everything that does not change the run.
