---
name: choose-by-consequence
description: 'Use when code must decide what happens on an unusual or failing path. Also use it when the user says "just handle that case", "skip it if it fails", or "is this the best way?". Compares the easy route with each alternative by what it does to the user''s files, data, and output. Picks the option that fails loudly and keeps every count and exit code true. Never writes through a file that the change does not own. Not for checking finished work against the real command output (use `verify-and-review`).'
metadata:
  shadowclone-category: change-control
  shadowclone-section: workflow
  shadowclone-applies-when: when a change adds a skip, block, fallback, default, or retry
---
# Choose by Consequence

## Use when

The code must decide what happens when something is unusual or fails. Examples: a file is a symbolic link, a tool is missing, or a step times out. Each of these is a behavior choice. A choice is risky when it touches owned or shared files, data, security, or public behavior such as output and exit codes.

## Gates

1. For each option, can you say what the user sees and what happens to their files and data? If not, check before you choose.
2. While you plan, did you give each risky choice to the user as an open decision? Put the option that fails loudly first.
3. While you execute, did you pick the option that fails loudly? A skip is loud only when the summary counts it, the final output names it, and the exit code shows it.
4. Do all counts, totals, and statuses in the output still match what happened?
5. Does any write go through a file that the change does not own, such as a symbolic link target? If so, block, and name both paths.
6. Does the handoff list each choice with the real output line that shows it?

## Process

### While you plan

1. List the options. Usual options: do the full job safely, block with an error, skip with a visible line, ask, or fall back.
2. For each option, write its hidden cost: who finds the problem, when, and what the recovery costs.
3. Put each risky choice to the user as one question with 2 to 4 options. Put the option that fails loudly first, and give one reason for it.

### While you execute

1. Do not ask again about a choice that the user made while planning. Follow it.
2. For a new choice, act without asking. Pick the first option that applies:
   - Do the full job safely.
   - Block with a message that names the file, the cause, and the next action.
   - Skip with a counted line at the end of the output, and a nonzero exit code.
3. Never use a silent fallback. A fallback is acceptable only when the output names it and the result is still correct.
4. Write the message that the user reads before you write the code that prints it.
5. Run the real command, and read the summary line, the final lines, and the exit code.
6. Write down each choice and its output line for the handoff.

## Example

**Situation:** A setup command installs guidance for several agents. The instruction file of one agent is a symbolic link to a file that other tools share.
**Easy route:** Skip that agent, print the skip in the middle of the output, and report success.
**Hidden cost:** The summary still said "Installed for 2 agents". The user believed that the setup installed the agent, and nothing told them that the shared file was left alone.
**Best route:** Do not write through the link. Count the agent as not installed. End the output with a line that names the agent and the link target. Exit with a nonzero code.
**Evidence:** The last line is "Not installed for codex: its AGENTS.md is a symbolic link to a shared file". The summary says "Installed for 1 agent", and the exit code is 1.

## Guardrails

- Never write through a symbolic link, a shared file, or a file that another tool owns. Block, and name both paths.
- Do not catch an error only to continue. Catch it to add context, then report it.
- Do not change a default that people rely on without a line in the output and in the handoff.
- Make each error message specific: the path, the cause, and one next action. "Something went wrong" is not a message.
- Keep the decision in one place. A second copy of the same check drifts, and then the two paths disagree.

## Completion

- Each risky choice in one line: the option that you picked and the hidden cost that it avoids.
- The command that you ran and the output line that shows each skip, block, or fallback.
- The exit code of that command.
- The summary or count line, checked against what happened.
- The `file:line` of each new block, skip, or fallback.
