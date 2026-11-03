---
name: create-formal-verification-skill
description: "Generate a project-local skill that formally verifies the code where a bug costs the most and tests reach the least, in any language, with whichever verification tool fits. Use for /create-formal-verification-skill, \"model-check this race\", \"prove this invariant\", or when concurrency, retries, state machines, parsers, or unsafe code need more than tests."
---

# Create a formal verification skill

A test checks the cases that someone thought to write. Formal verification checks every case in a stated scope: every order of steps in a model, every input up to a bound, or every input. This skill finds the part of the repo where that matters most, verifies one property of it, and leaves a project-local skill that lets the next agent check a change against that property. Write that skill for an agent who reads it cold, mid-change, and has never seen your work. The user must be able to trust the result and act on it without learning the verification language.

**Platform note.** Keep one shared generated skill tree: `.claude/skills/<name>/` on Claude Code or `.agents/skills/<name>/` on Codex, not both. Resolve host tools through [`codex-tools.md`](../poteto-mode/references/codex-tools.md). The coordinating parent owns every Git mutation; a delegated writer only edits its assigned files and reports checks.

## Choose the target from the code

Answer from the codebase, and ask the user only what you cannot observe. If the user named an area or a bug, start there.

A good target is a promise the code makes, where a break harms users and tests rarely reach the case that breaks it. Choose the strongest such target in the repo, not the one that is easiest to verify.

## Let the question choose the tool

Pick the tool that answers the question at the lowest cost: a model checker, a proof assistant, an SMT-backed verifier, or another tool. Whether events can happen in a bad order usually suits a model checker over a small model of the design, and TLA+ is the default for that in any language. Whether the code itself behaves for every input, as with memory safety, overflow, or a data-structure invariant, usually suits a verifier that runs on the code. If no verifier runs on this language, say so, and test the real code with generated inputs, not a hand model of the function. A property that must hold at every size, where a bound is not enough, can need a proof. Prefer a tool that the repo's developers can install and run, and tell the user why you chose it.

## What makes it good

- **True to the code.** Every part of the model or proof points to code that a reviewer can open. What the verification treats as one indivisible step is one indivisible step in the code. Names come from this repo.
- **Able to fail.** A check that you have never seen fail proves nothing. Show each property failing on a broken variant of the code it guards, such as a removed check or a reordered step. Use disposable copies, never a fault in the working checkout. For a model, show how the code fault changes the model and that the property catches it; an unchanged hand model cannot detect a code edit by itself.
- **Findings stay findings.** When the current code breaks the property, report it with the counterexample in the code's terms. Do not weaken the property or the model until it passes, and do not fix product code in this run. A product fix is separate work.
- **Honest about scope.** Say what is verified, under which bounds and assumptions, and what is left out. A pass covers the model or the bound, not the whole system.
- **Readable without the tool.** State the property and the harm in one plain sentence each. Tell a counterexample as a short sequence of steps in the code's words.
- **Cheap to rerun.** One command, a reproducible tool version, and a run short enough that the next agent will use it on every relevant change.
- **Kept in step with the code.** Record which files and functions each check covers, and the commit at which you last confirmed that the verification describes them. When the covered code changes after that commit, the next agent can see that the verification needs another look.

## Generate the verify skill

Write the project-local skill in the active host's location above. Give `SKILL.md` YAML frontmatter with a `name` matching its directory and a `description` naming the area and when to use it. Without frontmatter, the skill never registers. From the skill alone, the next agent must be able to tell whether a change touches the verified code, run the check, tell a real bug from a modeling error, and update the verification when a change is intended. Put the coverage record and exact full sync commit in the skill, and tell the next agent to move the sync commit forward only after it confirms that the verification describes the code at that commit. Record uncommitted covered changes separately; a commit does not include them. Include the property, harm, source mappings, bounds, assumptions, exclusions, tool version, one rerun command, counterexample interpretation, and cleanup. Any helpers must have their invocation documented and executable permissions set. Use this repo's real commands, paths, and nouns, and leave no placeholders.

If the check is a TLA+ model, tell the next agent to read every result with the registered [`statechart`](../statechart/SKILL.md) skill: `/pstack:statechart` in Claude Code or `$pstack:statechart` in Codex. It shows each invariant violation the checker finds as its shortest path in plain words. When the check passes, it draws a chart of how the system moves between states; a passing check over 500 states writes no chart, and the report still gives each bug path. Refer to `statechart` by its registered name. Its commands, options, and file paths change between releases and machines, so copy none of them into the generated skill or its scripts.

## Prove it before you hand off

Confirm that the active host registers the generated skill by its frontmatter name, then invoke that registered project skill: `/name` in Claude Code, or its skill-picker entry or `$name` in Codex. Capture the actual load and execution; reading the file directly is not registration proof.

Follow its instructions once on the real target. Capture the original result, then use a disposable copy with a fault in the covered code that breaks the property. The check must catch the break. Capture the counterexample in the code's words. If the check misses it or a step does not run, fix the skill or verification, not the fault or property. Keep tool versions, bounds, and assumptions visible; generated-input testing is not a formal proof.

Remove the disposable fault copy and rerun on the original bytes. If any verification file had to change temporarily, restore its captured bytes; never use stash or reset. Confirm the result is back where it started: passing, or failing only on the findings you will report. Clean up failed attempts too, retaining evidence outside disposable copies. A skill without observed native registration and execution is a draft; report those paths as unverified.

## Hand off

Tell the user what you verified, which tool you used and why, the bounds, what the check found in plain words, how to run it, and what it does not cover. Suggest a second target only if you found a close one. Point the user at [`maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.md) for bringing the verification back in line after changes that did not recheck it.
