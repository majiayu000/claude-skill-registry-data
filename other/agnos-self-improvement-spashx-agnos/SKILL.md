---
name: agnos-self-improvement
description: "AGNOS process self-improvement skill. Runs a recursive self-improvement effort: resolves the improvement target the project declares, measures its line budget with a script, and gives the procedure for each numbered iteration. USE FOR: a session that runs numbered iterations to improve the process; END SESSION step 3, when a friction counter is non-zero."
argument-hint: "(no arguments)"
---

<!-- RQ-RSI-001, RQ-RSI-002, RQ-RSI-003, RQ-RSI-004 / ADR-RSI-001 (DEC-RSI-001, DEC-RSI-002, DEC-RSI-003) -->
# AGNOS Self-Improvement

`<skill-folder>` is the folder holding this file. Run every command from the project's root.

## The target and its budget

The improvement target is the file the project declares in `CLAUDE.md` or `AGENTS.md` with the
sentence `` `<path>` is the improvement target ``, optionally followed by `, at most <N> lines`.
There is no fallback: never pick a target the project does not declare, and never edit a file of an
installed plugin.

Measure the budget with the script matching `session.platform` (read
`agnos-process/_sessionstate/session.yaml` first if not already in context):

| `session.platform` | Command |
|---|---|
| `windows` | `powershell -NoProfile -File <skill-folder>/scripts/budget.ps1` |
| `linux` / `macos` | `bash <skill-folder>/scripts/budget.sh` |

It prints `target=<path> ceiling=<N> lines=<n> left=<n>`. The ceiling is the instructions file's own
"SHALL NOT exceed <N> lines" when it is the target, otherwise the declared `at most <N> lines`,
otherwise 100.

| Exit code | Meaning | Action |
|---|---|---|
| `0` | Within the ceiling | Go on |
| `1` | No declaration, or a target outside the project | STOP, report the message, ask the user to declare a target |
| `2` | Over the ceiling | STOP, report it; the next iteration compresses the target first |

## Procedure

1. **Budget.** Run the script. If the declared target does not exist yet, create it with a
   `# <project> rules` title before the first iteration. <!-- RQ-PLG-018 -->
2. **Size the effort.** Ask the user for the maximum lines to add, at most `left`, and state the
   number of iterations it allows. The budget holds for the whole effort, not per iteration: the
   ceiling applies to the total after the last planned iteration.
3. **One theme at a time.** Propose the next iteration's theme, citing the friction counter(s) of
   `agnos-process/_sessionstate/METRICS_LOG.md` that motivate it, and get it confirmed before
   drafting its artifacts, so each iteration is informed by the previous one's outcome — unless the
   user explicitly asks for the full roadmap upfront.
4. **Draft the rule.** Any rule may be revised or compressed, including rules older than the effort.
   Keep the target's sections, their order and its templates; when a section is renamed, update
   every reference to it (anchors, other skills, entry points).
5. **Conflict check.** Before presenting the candidate rule for DoR approval, re-apply the semantic
   conflict check of START SESSION ACTION step 7 against it, and report any conflict found. It is
   complementary: human review at the theme and DoR gates remains the primary safeguard.
6. **Re-measure.** After the edit, run the script again and copy its output line into the task's
   `Verification` field. Exit code `2` means the iteration is not done.
7. **Commit.** Through the `agnos-git-workflow` skill's `commit-task`, with the `Iteration: <k>/<N>`
   trailer that procedure defines.
