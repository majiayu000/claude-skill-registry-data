---
name: correct
description: "Turn the mistakes agents keep repeating in a repo into checks that make them impossible. Find each mistake class (two occurrences make a class), fix it at the highest level that works (architecture, then types, then a lint or CI check whose error names the fix, then a test, then a hook, prose last), prove each check refuses a real past mistake and allows a nearby legitimate input, and keep a rule-to-enforcer registry. Use when the operator corrects an agent, says 'stop doing X', 'again?', '/correct', 'make this impossible', 'why does this keep happening', or when a rule exists in docs that nothing enforces."
---

# correct

Adapted from Lauren Tan's `/correct` skill in pstack (`cursor/plugins`, MIT,
commit bf0c7cd), extended with what applying it to a governance workspace
taught: every proof needs a control, a crash is not a refusal, and a rule
registry must be replayed, not just written.

The operator keeps correcting agents in this repo for the same mistakes. Change
the repo so the next agent cannot make them.

Assume every contributor is an agent that sees only the files it opened, copies
the nearest example, and takes the shortest path that compiles. The codebase is
its largest input, so a workaround it can see is a workaround it will copy. Design
the repo so a change that looks right from one file is right for the whole repo.

## 1. Find the mistake classes

Read recent commits, reverts and fix-forwards, review comments, agent instruction
files (AGENTS.md, CLAUDE.md, memory), and comments that explain workarounds. Group
the mistakes into classes. **A class counts once it has happened twice.** An
irreversible outward action (publishing, deleting someone else's work) counts at
once: there is no second chance to learn from.

Search the registry first (step 5). If the rule is already written and nothing
enforces it, that is a **repeat**: fix it now, at the highest level, in the same
change.

## 2. Fix each class at the highest level that works

1. **Architecture.** Give each piece of state one owner and each task one
   supported way. Hide internals so the wrong import fails. Replace hand-synced
   lists with one source of truth. Make generated files derived (regenerated and
   verified, never hand-edited or hand-merged). Delete old ways an agent would copy.
2. **Types.** Make the bad state impossible to write.
3. **A lint or CI check whose error names the fix.** Not "blocked": the file,
   type, function or command to use instead. An agent that only hears "no" routes
   around the check; one told what to do goes through it. If the pattern is
   already common, ratchet: fail when a change adds one, and fail when the
   count drops until the baseline is lowered, so it only shrinks.
4. **A test** of the behavior. Fix or delete any test that still passes when the
   behavior breaks, or fails when only internals change.
5. **A hook** that refuses the action when it is taken (an agent command, a
   commit, a file write), for mistakes made outside the code.
6. **Prose last, for judgment calls only.** Nothing fails when an agent skips it.
   Write down why no check can decide it.

## 3. Prove each check

A check never seen failing proves nothing.

- **Proof:** replay the real past mistake (the actual command, diff, file or
  transcript text, with where it came from) against the enforcer only, or against
  a disposable copy of every target, and show the check refuses it.
- **Control:** replay a nearby legitimate input against the enforcer only, or
  against a disposable copy of every target, and show it is allowed. Without
  one, a check that refuses everything passes every proof.
- **Mutation:** break the check in a scratch copy and show its proof fails.
- **A refusal states its reason.** A crashing check also exits non-zero; require
  the refusal's output to name the mistake, and treat other exit codes as errors.
- **An unmeasured condition is "no data", never "clean".**

Run the same command locally and in CI. Exceptions go on the offending line with
a reason, an expiry date and a human's approval.

## 4. Fix the most frequent classes now

One commit per class, each carrying its proof, control and mutation result.

## 5. Keep the registry

Keep one machine-readable table that pairs each rule with what enforces it: the
level, the enforcer's path, how it is reached (hook event, CI job), the dated
occurrences, the proofs and the controls. A runner replays every row against the
real enforcer (invoking only the enforcer or operating on disposable copies in a
scratch directory, never mutating live targets) and fails on any proof allowed
or control refused. A rule with no
enforcer is either a recorded judgment (with the reason) or a gap (with the
ticket that closes it). Drop a rule once its mistake cannot happen, and retire its
prose copy when it reaches a mechanism level.

In the `broomva/workspace` repo this is `.control/rules.yaml`, replayed by `make rules-check`.

## Reply

Each class with its evidence, the level you picked and why a higher level did not
work, the proof and control replayed, the mutation that turned it red, and the
rows added to the registry.

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "I'll add it to AGENTS.md." | That is the lowest level. Nothing fails when the next agent skips it. Try every level above first. |
| "It only happened once." | Then record it and wait for the second. An irreversible action is the exception. |
| "The check passes, so it works." | Show it failing on the real mistake, and passing on a control. |
| "The error says 'blocked'." | Name the fix. A refusal without one teaches the agent to route around it. |
| "The pattern is everywhere, the lint would be red for weeks." | Ratchet it: fail when a change adds one, and fail when the count drops until the baseline is lowered, so it only shrinks. |
