---
name: pstack
description: >
  Engineering principles for rigorous agent work, condensed from poteto's pstack Cursor
  plugin (github.com/cursor/plugins/tree/main/pstack). Data shape first, smallest diff,
  design red flags for agent-written repos, reproduce then fix root causes, prove it on
  the real artifact, explain every measured number, confidence tiers, and fixing repeated
  mistakes with structure instead of text. ALWAYS load before non-trivial code changes,
  architecture decisions, debugging, refactors, migrations, perf work, code review, or
  long autonomous runs. Read procedures.md for subagent briefs, verdict words,
  benchmarks, and overnight runs.
---

# pstack

Write less code, but code you can prove works. Proof is what makes parallel agents safe:
if every agent hands back evidence, nobody has to re-check every diff.

Concrete procedures (subagent briefs, verdict words, benchmark steps, overnight runs) live in `procedures.md` next to this file. Read it when the task
needs one of them.

## Gist

1. **Data shape first.** Name the structure before you write logic.
2. **Smallest diff. Delete before you add.**
3. **Reproduce, then fix the root cause.** Ship only what evidence supports.
4. **Prove it on the real artifact.** "It compiles" is not proof.
5. **Build the lever.** A script that does or proves the work beats hand edits.
6. **Do not ask what you can observe.** Run something and let the result decide.
7. **Encode repeated lessons as structure,** not as more text.

In the final reply, name each principle that changed a decision and say which decision.
A principle cited without a decision is name-dropping.

## 1. Before code

**Caller's usage first.** For anything other code will call, write the usage (README
snippet plus two or three real call sites) before the types. Derive the types from the
usage. When they disagree, fix the types, not the usage.

**Model the domain.** Encode the domain in a structure instead of scattered conditionals:
a state machine instead of booleans, a discriminated union instead of optional-field bags,
a table or registry instead of if/else spread across files, a reducer instead of ad hoc
mutation. Signs you skipped this: a feature that grows an if/else chain by one branch, or
a second boolean that must stay in sync with the first. Do not force an abstraction when
the code is already clear, local and unlikely to grow.

**Redesign, do not bolt on.** For a new requirement ask: "if we wrote this from scratch
with this requirement, what would we build?" Propagate through types, docs and examples.

**Subtract first.** Delete dead code, one-caller wrappers, redundant validators and stub
references before building on top.

**Design red flags.** Assume the next contributor is an agent that sees only the files it
opened, copies the nearest example, and takes the shortest path that compiles. Prefer the
design where a change that looks right from one file is right for the whole repo. Reject
or revise a design that has:

| Flag | Fix |
|---|---|
| Split ownership: two modules write the same state | One owner per piece of state, others read or ask |
| Two ways to do one task | Keep one, migrate callers, delete the rest in the same change |
| Importable internals | Make them unreachable so an outside import fails the build |
| Hand-synced lists | One list, derive the others, or fail the build when they differ |
| Pass-through layer with the same shape | Inline it unless it adds policy or a real abstraction |
| Shallow module: big interface, little hidden | Pull complexity behind a smaller interface |
| Temporal decomposition: load/validate/save modules | Group by domain knowledge, not execution order |
| Information leakage: wire or storage types in the API | Parse into domain types behind the interface |

**Design twice, only for one-way doors.** For decisions that are expensive to reverse,
sketch two structurally different shapes (not two flavors of one shape) and pick the one
that hides more behind a smaller interface. For contested designs ask the oracle agent
for a second opinion. Agreement between models is high signal.

**Prototype empirical forks.** If the answer is a fact you could observe (layout, timing,
output, perf), it is not the user's question. Build a throwaway in a scratch folder, put
variants behind one switch, observe, decide. Never review an abstract plan with no code
behind it: reviewers invent risks that never happen.

## 2. While coding

**Smallest diff.** Put each decision behind one source of truth. Fewer lines beat elegant
boilerplate.

**Code judo.** Before accepting working code, look for a reframing that keeps behavior and
makes whole branches, modes, helpers or layers disappear. An ad hoc `if` added to an
unrelated flow is a design problem, not a style nit. Move it into a state machine, helper
or module. Pushing a file past ~1000 lines needs a strong reason.

**Minimize reader load.** Count layers between question and answer, and hidden mutable
state the reader must hold. Test: can a new reader answer "where does X come from?" and
"what can change X?" in under 30 seconds? If not, cut layers or cut state.

**Build the lever.** For non-trivial work, write the codemod, generator, script or check
that does or proves it. Do the first unit by hand, then build the tool and rerun it on that
unit to diff against your hand version. If you cite this principle and the diff has no
script, you did not apply it. A deterministic script beats fanning out subagents to apply
edits by hand.

**Idempotent operations.** For every state change ask: what if this runs twice, and what
if the last run crashed at any point? Derive each step from the current state, not from
what the last run meant to do. Leftovers (locks, temp files, claimed jobs) must be
recognizable as stale. Write to a temp path, then rename.

**Separate before serializing.** If concurrent actors might write the same file, key,
branch or object, first give each actor its own target and merge at read time. Treat "we
need a lock" as a design smell. Conventions are not concurrency control.

**Migrate callers, then delete the old API, in one wave.** No parallel old and new paths.

**Make illegal states unrepresentable.** Strengthen a type only where partiality appears:
a `!`, a cast, or a "should never happen" throw marks a type that is too weak. Then stop.
The `typescript` skill has the syntax.

## 3. Debugging

1. **Reproduce first, on the same surface as the bug.** If it will not reproduce,
   synthesize the trigger, tighten conditions or instrument until it fires. Ask the user
   only after driving the surface as far as it goes.
2. **Binary-search the cause.** List hypotheses, pick the check that cuts the most
   remaining space, get runtime evidence, eliminate. Instrument instead of guessing.
3. **Ask if the bad state is legitimate.** If the system may be in that state, the code
   that broke on it is the root cause: handle it there. If the state should never exist,
   a guard where it broke hides the bug: find what produced it. Guards, retries, swallowed
   errors and clamped values are the usual ways to hide a bug.
4. **Attack the premise.** After two failed fixes that share one belief, write the belief
   down in one sentence and test it directly before a third fix.
5. **Ship only what evidence supports.** "Belt-and-suspenders that might help is a
   hypothesis, not a fix." Revert everything a disproved hypothesis motivated.
6. **Fix the pattern, not the instance.** Find every place with the same fault.
7. **Leave a signal.** If the deciding fact took a deep dig, add the cheap always-on log or
   check that would have shown it at first look.

If it fails only after a restart, suspect persisted state first: config, caches, lock
files. A workaround that needs a paragraph-long comment means the code is wrong.

## 4. Proving it

**Check the real artifact.** Run the feature, read the stored value, drive the UI. Not a
proxy, not a subagent's self-report, not a build log. When a check fails or passes too
easily, suspect the observation method before the system. Prefer a rerunnable script over
a one-time eyeball.

**Proof ladder.** For each fact a change's safety depends on, say how far you got:

1. You said so (worthless alone)
2. You pointed at the line
3. You walked the failure and showed it cannot happen
4. You ran a script that calls the real code and fails loudly if you are wrong
5. You reproduced it in the running app

**Explain the number.** Before you report or act on a measured number:
- Ask "why not double?" and name the limiter (a core, a lock, disk, network, the load
  generator) from a profile, not from reading code.
- Rule out errors, skipped or cached work, code that never ran, an untuned side, noise.
- Keep run count, spread and limiter next to the number.
- Removing a piece that takes 10% of the run makes it at most ~11% faster. A result past
  a physical limit measured something else.

**Perf mantras, cheapest first.** Stop at the first that meets the target: don't do it,
do it once, do less, do it later, do it when nobody looks, do it concurrently, do it
cheaper.

**One change, one measurement, keep or revert.** Never stack untested changes. Never claim
a win from code inspection.

**Test behavior with two imagined edits.** Break the behavior: the test must fail. Change
only internals: the test must pass. Derive expected values from the requirement, not from
a run of the code.

**Sequence verifiable units.** Each step ends in a check before the next starts. In git
the failing repro lands before the fix.

**Migrations match exactly, bugs included.** Fix old bugs in separate commits so old and
new output stay comparable.

## 5. Judgment and candor

**Label every claim** with its evidence in the same sentence: measured, inferred or guess.
Never hand the user a check you could run. Never invent a link or citation.

**Confidence tiers** for "why" questions and diagnoses:

| Tier | Meaning | Phrasing |
|---|---|---|
| Direct | Someone wrote down why (PR, commit, comment) | "This exists because X [cite]" |
| Supported | Several indirect sources agree | "The evidence points to X: A, B" |
| Inferred | Your reading of the context | "Given A and B, X seems likely" |
| Speculative | Plausible, thin evidence | "One possibility is X, no direct evidence" |
| Unknown | You looked and found nothing | "Searched A, B, C, found no rationale" |

"Because", "fixes" and "was designed to" need a citation next to them. Code is not
evidence of its own intent.

**Sycophancy trap.** When the user embeds a guess ("I assume it's for performance?"),
treat it as one hypothesis and check it independently.

**No is an acceptable answer.** Decline, push back, or say "this doesn't earn its place"
when true. A recommendation is a judgment, not a validation.

**Judge review findings, do not aggregate them.** A hypothetical ("what if this is null")
counts only if you trace a real call site to it. "I would have done it differently" is not
a finding unless it shows a concrete problem. Reviewers inflate nits when they find nothing
big; all-nit reviews mean the code is fine. Findings two models raise independently are
the highest signal. Take security and correctness findings seriously even from one model.

**Decide reversible work yourself.** Pause only for irreversible actions (force-push to
shared branches, deploys, data deletion, external messages) or product calls no experiment
can settle.

## 6. Lessons

When the same mistake happens twice, fix it at the highest level that works:

1. **Architecture.** One owner per state, one supported way, hide internals, delete the
   old way an agent would copy.
2. **Types.** Make the bad state unwritable.
3. **Lint or CI check** whose error names the file or function to use instead. If the
   pattern is already common, fail only when a change adds more.
4. **Test** the behavior.
5. **Docs or agent rules,** last. Nothing fails when an agent skips them.

Prove each new check fails on a real past mistake. If the fix is structural, use only the
structural fix: the instruction is the symptom. A broken skill gets fixed in its own
change; do not block on it and do not silently work around it.
