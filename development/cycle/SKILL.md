---
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, LSP, mcp__ide__getDiagnostics, Bash
description: Draft, critique and merge a plan in one loop, then stop for approval
argument-hint: plan name
disable-model-invocation: true
model: opus
effort: high
---

You are running the whole planning loop in one pass: research the codebase, draft the plan only when the user has
not written one, critique it, merge the findings, repeat, then stop and wait for approval.

This skill never executes the plan. It ends at the approval gate.

Fixed rules:

Read the working agreement at [working-agreement.md](../../working-agreement.md) before step 1 and follow it for
the whole run. If that path does not resolve, look for `working-agreement.md` in the project root, then in
`.claude/`. If it cannot be found anywhere, tell the user it is missing and apply the rules listed below.

These rules bind this phase and override any step below that conflicts with them:

1. Never execute the plan, and never write, edit or refactor project code during this run. This phase produces a
   plan folder, a `plan.md`, a `critique.md` and a `cycle-log.md` and nothing else. The user approves before
   anything is built.
2. The user owns the plan. Draft `plan.md` only when it is empty or still the unedited template. When it holds
   text the user wrote, never overwrite it, and never drop the user's requirements, wording or constraints while
   merging.
3. Never assume, ask. Change `plan.md` on your own only when the change a finding asks for is obvious. Stop and
   ask the user whenever it is not: the finding is ambiguous, it touches a requirement or a constraint the user
   wrote, it changes the scope or the intent of a chapter, it rewrites more than the finding covers, or two
   findings pull in different directions. Show the finding, the exact edit you propose and the alternatives, then
   apply the answer. A doubt is a question, never a guess.
4. Be adversarial in every iteration. Try to refute each finding before you write it down, and report only what
   survives the attempt.
5. Grade confidence per finding. Report a finding as CONFIRMED only when you verified it against the codebase.
   Label everything else UNVERIFIED and state what you could not check and why. Prove every finding with a
   `file:line` reference, a command output, or a failing test.
6. Re-read `plan.md` from disk at the start of every iteration and cite line numbers only from that copy. Merging
   shifts every line below the merge point, so numbers carried over from an earlier iteration are wrong.
7. Verify what you merge, not only what you find. A suggested solution is a claim like any other: run the command
   before you write it into a verification section, and check every line reference in it against the file it
   names. An unverified fix is not merged, it is asked about. A merge that ships a broken command costs the next
   iteration. Run only commands that read: this phase verifies, it never builds, installs, migrates, commits or
   writes anywhere outside the plan folder.
8. Merging is automatic for the obvious changes only, and never silent. Record every merged finding, every finding
   you asked about with the answer you got, and every skipped finding with its reason, in `cycle-log.md`, and
   print the same summary after each iteration.
9. Stop early when an iteration surfaces no new findings. Respond "No new findings." and go to the approval gate.
10. Be brief. No filler, no preamble, no restating the request. No emojis, no em dashes, no bold or italic text.

To do this, follow these steps precisely:

1. Display the following banner before doing anything else:
   ```
   +-------------------------------------------------+
   |  Plan Critique v2.6.1 - Plan cycle              |
   +-------------------------------------------------+
   ```
2. Read `.claude/plan-critique-config.json` and get `plansFolder` path from settings.
   If the file doesn't exist or `plansFolder` is not set or is an empty string:
   - Ask the user: "Where would you like to store your plans? Provide a folder path (default `.planning`):".
     By default, the user should be presented with the option `.planning`.
   - Save the path as `plansFolder` in `.claude/plan-critique-config.json`
   - Create the folder if it doesn't exist
   - Create an `archived/` subfolder inside it
3. Read the optional `cycleIterations` value from the same config file. It is the maximum number of critique and
   merge iterations for this run. Default to `3` when it is missing, and clamp any value outside the range 1 to 5.
4. Get the Claude Code process ID by running: `echo $PPID`. Store this as `sessionPID`.
5. Clean up stale sessions: Scan `[plansFolder]/.sessions/` for files. For each file named with a PID, check if that
   process is still running via `kill -0 [PID] 2>/dev/null`. If the command fails (process not running), delete that
   session file. This is non-blocking cleanup.
6. Read the current session's plan from `[plansFolder]/.sessions/[sessionPID]` if it exists. Store as `sessionPlan`.
7. Scan `[plansFolder]/` for subdirectories (each subdirectory is a plan). Exclude `archived/` and `.sessions/`
   folders and any files, only list plan directories.
8. Select the plan for this cycle:
   - If `$ARGUMENTS` is a slug that matches an existing plan folder, select that plan.
   - Else if `$ARGUMENTS` is not empty, treat it as the name of a new plan and create it by following the plan
     naming and folder creation steps of [../create/SKILL.md](../create/SKILL.md): the slug rules, the name
     collision check, the folder creation and the `plan.md` template from
     [plan-template.md](../create/plan-template.md). Do not display the create banner.
   - Else if `sessionPlan` exists and matches a plan folder, auto-select it and inform the user:
     "Using current session plan: [sessionPlan]"
   - Else if exactly one plan exists, auto-select it and inform the user.
   - Else if plans exist, ask the user to select one from the list, and offer creating a new plan as the last
     option.
   - Else ask the user for a name for the new plan and create it as described above.
9. Update the session file `[plansFolder]/.sessions/[sessionPID]` with the selected plan slug (create if needed).
10. Read `[plansFolder]/[selected-plan]/plan.md` and classify it:
    - Empty, or still the unedited template from [plan-template.md](../create/plan-template.md), which is
      recognised by the placeholder chapter heading and the bracketed placeholder lines: the plan needs a draft.
    - Anything else: the user wrote it. Inform the user "Using the existing plan.md, no draft written." and go to
      step 13.
11. Prepare the draft. Tell the user "plan.md is still the template. Drafting a first pass." and get the goal:
    - Use `$ARGUMENTS` as the goal when it describes what to build.
    - Otherwise ask the user: "Describe what this plan must achieve:". Do not guess the goal.
12. Research the codebase, then write the draft:
    - Read `CLAUDE.md` and `README.md`, and the existing files the goal touches.
    - List every file that the plan will create, modify or delete, and verify each path exists with Glob before
      writing it down. Show this list to the user before writing the plan.
    - Ask the user whenever the research leaves a real choice open, such as which module owns the change or which
      of two approaches the plan should take. Do not pick one and write it down as if it were settled.
    - Write `[plansFolder]/[selected-plan]/plan.md` using [plan-template.md](../create/plan-template.md): one
      numbered chapter per unit of work, in dependency order, each with its own `Affected files` and
      `Verification` sections. Every chapter names the test to write or the command to run.
    - Where the project has no test infrastructure, say so in the chapter instead of inventing a test harness.
13. Check prerequisites once, before the loop:
    - If `plan.md` is empty after step 12: respond with "Plan file is empty. Edit
      `[plansFolder]/[selected-plan]/plan.md`" and stop.
    - If `CLAUDE.md` does not exist in the project root: respond with "Create a `CLAUDE.md` file in the root of
      your project." and stop.
    - Detect the project languages and probe LSP as described in the LSP availability step of
      [../critique/SKILL.md](../critique/SKILL.md). Record whether LSP is available, and reuse that answer for
      every iteration instead of probing again.
14. Run the cycle. Repeat the following until you have run `cycleIterations` iterations or an iteration surfaces
    no new findings:
    - Re-read `plan.md` from disk.
    - Critique it by following the fixed rules and the analysis steps of
      [../critique/SKILL.md](../critique/SKILL.md), including the split evaluation. Skip its config, session and plan
      selection steps, which this run already did. Its rule against editing `plan.md` binds the critique step
      only, because merging is a separate step below.
    - Write the critique to `[plansFolder]/[selected-plan]/critique.md` using
      [critique-format.md](../critique/critique-format.md), with the iteration number incremented from the previous
      critique.
    - If the critique found nothing, respond with "No new findings." and leave the loop.
    - Merge the findings into `plan.md`:
      - Apply a CONFIRMED finding to the chapter it belongs to when the edit it asks for is obvious.
      - Ask the user before making any change that is not obvious, and apply the answer. This covers an
        ambiguous finding, a finding that touches a requirement or a constraint the user wrote, a finding that
        changes the scope or the intent of a chapter, and two findings that pull in different directions. Show
        the finding, the exact edit you propose and the alternatives. Ask once per change, and group the
        questions of one iteration together so the loop stops as little as possible.
      - Apply an UNVERIFIED finding only when it clarifies the plan and cannot lose information. Ask about it
        otherwise.
      - Skip any finding whose evidence is missing.
      - Verify each edit before you write it. Run any command the finding puts into a `Verification` section and
        confirm it passes on the current tree and can fail, and check every path and line number the edit
        introduces. Do not carry a line range or an index from the critique into the plan when the chapter will
        change the lines it points at: anchor to a heading, a fence or a symbol instead. When the edit does not
        survive this check, ask the user rather than merging it.
      - Keep the `Affected files` and `Verification` sections in every chapter.
      - When the critique recommends splitting the plan, do not split it. Record the recommendation as an open
        item for the approval gate.
    - Append an entry to `[plansFolder]/[selected-plan]/cycle-log.md` using [cycle-log-format.md](cycle-log-format.md),
      and print the same merged and skipped summary to the user.
15. Print the final `plan.md` in full, followed by the open items: every skipped finding and every split
    recommendation.
16. Stop at the approval gate and respond:
    ```
    Cycle complete after [N] iteration(s): [plansFolder]/[selected-plan]/plan.md
    Merged: [X] findings. Asked about: [Z]. Not merged: [Y], listed in cycle-log.md.
    Nothing has been executed and no project code was changed.
    Review the plan. When you approve it, run `/plan:execute`.
    ```

Notes:

- Never execute the plan from this skill, not even when the user approves it in the same session. Point the user
  at `/plan:execute`, which carries its own rules, its own confirmation and its own execution log.
- Each iteration is a full adversarial pass over the plan and the codebase, so a three iteration run on a large
  plan is expensive. Set `cycleIterations` to 1 or 2 in `.claude/plan-critique-config.json` for small plans.
- The cycle is resumable. Run it again on the same plan and it continues from the current `plan.md` and from the
  iteration number recorded in `critique.md`.
- `critique.md` holds the latest iteration only, because each critique overwrites it. `cycle-log.md` holds the
  history of what was merged and what was skipped.
- The plan folder, the session file and the config file are the same ones used by `/plan:create`,
  `/plan:critique`, `/plan:execute` and `/plan:archive`. The cycle is a shortcut through the first two, not a
  separate workflow.
