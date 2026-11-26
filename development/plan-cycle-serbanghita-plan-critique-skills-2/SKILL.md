---
name: plan-cycle
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, LSP, mcp__ide__getDiagnostics, Bash
description: >-
  Draft, critique and merge a plan in one loop, then stop for approval. Use when the user runs /plan-cycle or asks
  to run the full create-and-critique planning loop.
argument-hint: "[plan name]"
disable-model-invocation: true
model: opus
effort: high
license: MIT
---

On Codex, invoke skills with `$skill-name` (for example, `$plan-create`). Use that form when giving Codex
commands; other clients use `/skill-name`.

You are running the whole planning loop in one pass: research the codebase, draft the plan only when the user has
not written one, critique it, merge the findings, repeat, then stop and wait for approval.

This skill never executes the plan. It ends at the approval gate.

Fixed rules:

Read the working agreement at [working-agreement.md](../plan-create/working-agreement.md) before step 1 and follow it
for the whole run. If it cannot be found, tell the user it is missing and apply the rules listed below.

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
9. Stop early only when clean: before any finding is merged across the active convergence chain (since the last
   converged `## Summary` or log start), stop on the first clean iteration; once at least one finding has been
   merged, require two consecutive clean iterations before stopping early. Partition surfaced findings before
   checking cleanliness: any finding matching an earlier `Not merged` entry with unchanged non-`plan.md` evidence
   (or a repeat `split recommendation, left for the user`) is `Previously decided`, is not re-asked, and does not
   reset `cleanPasses`. An iteration is clean when it has `0` new (non-`Previously decided`) `CONFIRMED` or
   `UNVERIFIED` findings; any new finding (merged, asked, or skipped) resets `cleanPasses` to `0`. Respond
   "No new findings." and go to the approval gate.
10. Be brief. No filler, no preamble, no restating the request. No emojis, no em dashes, no bold or italic text.

To do this, follow these steps precisely:

1. Display the following banner before doing anything else:
   ```
   +-------------------------------------------------+
   |  Plan Critique v3.0.1 - Plan cycle              |
   +-------------------------------------------------+
   ```
2. Resolve `plansFolder` from config:
   - Check the active agent's config file first (`.codex/plan-critique-config.json` for Codex,
     `.claude/plan-critique-config.json` for Claude Code,
     `.gemini/plan-critique-config.json` for Agy/Gemini, or `.copilot/plan-critique-config.json` for Copilot CLI),
     falling back to the other agent configs.
   - If no config exists or `plansFolder` is not set or is an empty string:
     - Ask the user: "Where would you like to store your plans? Provide a folder path (default `.planning`):".
       By default, the user should be presented with the option `.planning`.
     - Save `plansFolder` in the active agent's config file.
     - Create the folder if it doesn't exist, and create an `archived/` subfolder inside it.
3. Read the optional `cycleIterations` value from the resolved config file. It is the maximum number of critique
   and merge iterations for this run. Default to `3` when missing, and clamp any value outside the range 1 to 5.
4. Get the active session id:
   - On Copilot CLI (or when `COPILOT_AGENT_SESSION_ID` is set): read `COPILOT_AGENT_SESSION_ID` via
     `echo $COPILOT_AGENT_SESSION_ID` (macOS/Linux) or `$env:COPILOT_AGENT_SESSION_ID` (Windows); if empty, use the
     literal value `default`. Store as `sessionId`.
   - Otherwise (Codex, Claude Code / Agy): run `echo $PPID` and store as `sessionId`.
5. Clean up stale sessions in `[plansFolder]/.sessions/` (non-blocking, never abort because of cleanup):
   - For numeric PID filenames, check `kill -0 [PID] 2>/dev/null` and delete if the process is no longer running.
   - For non-PID session files (e.g. `default` or UUIDs), delete files not modified in the last 7 days.
6. Read the current session's plan from `[plansFolder]/.sessions/[sessionId]` if it exists. Store as `sessionPlan`.
7. Scan `[plansFolder]/` for subdirectories (each subdirectory is a plan). Exclude `archived/` and `.sessions/`
   folders and any files, only list plan directories.
8. Select the plan for this cycle:
   - If `$ARGUMENTS` or the invoking prompt text is a slug that matches an existing plan folder, select that plan.
   - Else if `$ARGUMENTS` or the invoking prompt text is not empty, treat it as the name of a new plan and create it
     by following the plan naming and folder creation steps of [../plan-create/SKILL.md](../plan-create/SKILL.md):
     the slug rules, the name collision check, the folder creation and the `plan.md` template from
     [plan-template.md](../plan-create/plan-template.md). Do not display the create banner.
   - Else if `sessionPlan` exists and matches a plan folder, auto-select it and inform the user:
     "Using current session plan: [sessionPlan]"
   - Else if exactly one plan exists, auto-select it and inform the user.
   - Else if plans exist, ask the user to select one from the list, and offer creating a new plan as the last
     option.
   - Else ask the user for a name for the new plan and create it as described above.
9. Update the session file `[plansFolder]/.sessions/[sessionId]` with the selected plan slug (create if needed).
10. Read `[plansFolder]/[selected-plan]/plan.md` and classify it:
    - Empty, or still the unedited template from [plan-template.md](../plan-create/plan-template.md), which is
      recognised by the placeholder chapter heading and the bracketed placeholder lines: the plan needs a draft.
    - Anything else: the user wrote it. Inform the user "Using the existing plan.md, no draft written." and go to
      step 13.
11. Prepare the draft. Tell the user "plan.md is still the template. Drafting a first pass." and get the goal:
    - Use `$ARGUMENTS` or the invoking prompt text as the goal when it describes what to build.
    - Otherwise ask the user: "Describe what this plan must achieve:". Do not guess the goal.
12. Research the codebase, then write the draft:
    - Resolve project instructions from `AGENTS.md` for Codex, `GEMINI.md` for Agy,
      `.github/copilot-instructions.md` for Copilot, or `CLAUDE.md` for Claude Code. Fall back to `AGENTS.md` then
      `CLAUDE.md`, and read the result alongside `README.md` and the files the goal touches.
    - List every file that the plan will create, modify or delete, and verify each path exists with Glob before
      writing it down. Show this list to the user before writing the plan.
    - Ask the user whenever the research leaves a real choice open, such as which module owns the change or which
      of two approaches the plan should take. Do not pick one and write it down as if it were settled.
    - Write `[plansFolder]/[selected-plan]/plan.md` using [plan-template.md](../plan-create/plan-template.md): one
      numbered chapter per unit of work, in dependency order, each with its own `Affected files` and
      `Verification` sections. Every chapter names the test to write or the command to run.
    - Where the project has no test infrastructure, say so in the chapter instead of inventing a test harness.
13. Check prerequisites once, before the loop:
    - If `plan.md` is empty after step 12: respond with "Plan file is empty. Edit
      `[plansFolder]/[selected-plan]/plan.md`" and stop.
    - If no project instructions file exists (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or
      `.github/copilot-instructions.md`): respond with "Create a project instructions file in the root of your
      project." and stop.
    - Detect the project languages and probe code intelligence as described in step 10 of
      [../plan-critique/SKILL.md](../plan-critique/SKILL.md). Record whether LSP / a language server is available,
      and reuse that answer for every iteration instead of probing again.
14. Run the cycle:
    - Before iteration 1, initialize `hasMerged = false` and `cleanPasses = 0` from
      `[plansFolder]/[selected-plan]/cycle-log.md`:
      - If `cycle-log.md` does not exist, or its last `## Summary` follows the final iteration entry and stopped
        with `no new findings` or `two consecutive clean passes`: keep `hasMerged = false` and `cleanPasses = 0`.
      - If the last `## Summary` stopped with `iteration limit reached`, or if trailing iteration entries have no
        following `## Summary` (an interrupted run): scan back to the last converged `## Summary` (`no new findings`
        or `two consecutive clean passes`) or log start. Set `hasMerged = true` if any iteration in that segment
        modified `plan.md` (`Merged > 0` or an `Asked` entry whose `Answer:` starts with `Applied:`), and set
        `cleanPasses` to the trailing consecutive clean iteration count (`0` or `1`).
    - Open a `## Run [n]` block in `[plansFolder]/[selected-plan]/cycle-log.md` with `Started: [YYYY-MM-DD HH:MM:SS]`
      before iteration 1 of this run (creating `# Plan Cycle Log: [Plan Title]` and `Plan drafted by:` on Run 1,
      and incrementing `[n]` from the last `## Run` on resumed runs).
    - Repeat the following until you have run `cycleIterations` iterations or the stop condition below triggers:
      - Re-read `plan.md` from disk.
      - Critique it by following the fixed rules and the analysis steps of
        [../plan-critique/SKILL.md](../plan-critique/SKILL.md), including the split evaluation. Skip its config,
        session and plan selection steps, which this run already did. Its rule against editing `plan.md` binds
        the critique step only, because merging is a separate step below.
      - Write the critique to `[plansFolder]/[selected-plan]/critique.md` using
        [critique-format.md](../plan-critique/critique-format.md), with the iteration number incremented from the
        previous critique.
      - Partition surfaced findings before the clean check:
        - Compare each surfaced finding against earlier `Not merged` entries in `cycle-log.md` using chapter title
          plus finding target/summary as the match key (ignoring shifting `plan.md` line numbers when checking
          whether non-`plan.md` evidence is unchanged). Also match any repeat `split recommendation, left for the
          user` already logged under `Not merged`.
        - Classify matched unchanged repeats as `Previously decided`: do not re-ask them, do not re-count them in
          `Not merged` or `Open items`, and log them under `Previously decided` instead.
      - Evaluate the remaining new findings (`CONFIRMED` and `UNVERIFIED`):
        - If clean (`0` new `CONFIRMED` and `0` new `UNVERIFIED` findings):
          - If `hasMerged` is `true`, increment `cleanPasses` by 1.
          - Skip the merge step below.
        - If not clean (one or more new `CONFIRMED` or `UNVERIFIED` findings, whether merged, asked, or skipped):
          - Reset `cleanPasses = 0` and merge the new findings into `plan.md`:
            - Oscillation check (before merging any finding): inspect `[plansFolder]/[selected-plan]/cycle-log.md`
              for all changes recorded as merged anywhere in the selected plan's log across all runs (both
              `Merged` entries and `Asked` entries whose `Answer:` starts with `Applied:`), not only in the
              immediately preceding iteration. When an `Asked` entry with `Answer: Applied:` explicitly approved
              reversing an earlier merge, that decision supersedes the earlier entry so subsequent checks compare
              against the latest decision rather than re-flagging the old merge. If applying a finding would
              undo, revert, or contradict an active earlier decision, do not auto-merge it. Surface it to the
              user instead per fixed rule 3, showing the earlier change, the new finding, and the options. Record
              the surfaced finding under `Asked`, and if declined or left unapplied also record it under
              `Not merged` with `Reason: reverses an earlier merge, asked`.
            - Apply a CONFIRMED finding to the chapter it belongs to when it passes the oscillation check and the
              edit it asks for is obvious.
            - Ask the user before making any change that is not obvious, and apply the answer. This covers an
              ambiguous finding, a finding that touches a requirement or a constraint the user wrote, a finding that
              changes the scope or the intent of a chapter, two findings that pull in different directions, and any
              finding flagged by the oscillation check. Show the finding, the exact edit you propose and the
              alternatives. Ask once per change, and group the questions of one iteration together so the loop
              stops as little as possible.
            - Apply an UNVERIFIED finding only when it passes the oscillation check, clarifies the plan and cannot
              lose information. Ask about it otherwise.
            - Skip any finding whose evidence is missing.
            - Record `Answer:` in `Asked` entries starting with `Applied:` or `Declined:`, and include `Evidence:`
              on every `Not merged` entry (`file:line`, command output, or `"missing"`).
            - Verify each edit before you write it. Run any command the finding puts into a `Verification` section
              and confirm it passes on the current tree and can fail, and check every path and line number the edit
              introduces. Do not carry a line range or an index from the critique into the plan when the chapter
              will change the lines it points at: anchor to a heading, a fence or a symbol instead. When the edit
              does not survive this check, ask the user rather than merging it.
            - Keep the `Affected files` and `Verification` sections in every chapter.
            - When the critique recommends splitting the plan, do not split it. Record the recommendation under
              `Not merged` with `Reason: split recommendation, left for the user` as an open item for the approval
              gate.
            - If at least one edit was written to `plan.md` in this iteration (auto-merged or applied from the
              user's answer), set `hasMerged = true`.
      - Append an entry to `[plansFolder]/[selected-plan]/cycle-log.md` using
        [cycle-log-format.md](cycle-log-format.md), and print the same merged and skipped summary to the user.
      - Check the stop condition:
        - If the iteration was clean and (`hasMerged` is `false` or `cleanPasses >= 2`): record exit reason
          (`no new findings` when `hasMerged` is `false`, or `two consecutive clean passes` when
          `cleanPasses >= 2`, taking precedence over `iteration limit reached` if on the final iteration), respond
          with "No new findings." and leave the loop.
        - If the iteration was clean and `hasMerged` is `true` and `cleanPasses` is 1: inform the user that one
          clean pass is complete and one more consecutive clean pass is needed, then continue if `cycleIterations`
          allows (otherwise record `iteration limit reached`).
    - Write `## Summary` at the end of the current `## Run [n]` block on loop exit, using `Stopped because`
      (`no new findings`, `two consecutive clean passes`, or `iteration limit reached`), current-run `Iterations run`
      and `Questions asked`, and `Open items` counting deduplicated `Not merged` entries across all unfinished or
      active runs.
15. Print the final `plan.md` in full, followed by the open items: every deduplicated skipped finding and split
    recommendation recorded under `Not merged` across all unfinished or active runs.
16. Stop at the approval gate and respond (with `[N]`, `Merged`, `Asked about`, and `Not merged` scoped to the
    current run):
    ```
    Cycle complete after [N] iteration(s): [plansFolder]/[selected-plan]/plan.md
    Merged: [X] findings. Asked about: [Z]. Not merged: [Y], listed in cycle-log.md.
    Nothing has been executed and no project code was changed.
    Review the plan. When you approve it, run `/plan-execute`.
    ```

Notes:

- Never execute the plan from this skill, not even when the user approves it in the same session. Point the user
  at `/plan-execute`, which carries its own rules, its own confirmation and its own execution log.
- Each iteration is a full adversarial pass over the plan and the codebase, so a three iteration run on a large
  plan is expensive. After a merge in a run, two consecutive clean iterations are needed, so a run merging in
  iteration 1 stops at iteration 3 at the earliest (`cycleIterations` of 1 or 2 hits the iteration limit unless a
  prior run left `cleanPasses = 1`, and 4 or 5 is needed to stop before the cap). Set `cycleIterations` to 1 or 2
  in your config file for small plans.
- If the active agent ignores `model` frontmatter, select a high-capability model with `/model`.
- The cycle is resumable. Run it again on the same plan and it continues from the current `plan.md` and from the
  iteration number recorded in `critique.md`.
- `critique.md` holds the latest iteration only, because each critique overwrites it. `cycle-log.md` holds the
  history of what was merged and what was skipped.
- The plan folder, the session file and the config file are the same ones used by `/plan-create`,
  `/plan-critique`, `/plan-execute` and `/plan-archive`. The cycle is a shortcut through the first two, not a
  separate workflow.
