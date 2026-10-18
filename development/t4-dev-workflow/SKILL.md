---
name: t4-dev-workflow
description: Use when planning or implementing a feature/change in a T4-team repo (T4 Labs / Slow-Inc) — deciding how to go from idea to shipped code, filing or updating a GitHub issue or PRD, writing a bilingual (Thai + English) issue/PR body, opening a PR, or closing an issue. Covers the grill→PRD→issues→TDD pipeline, the PRD→issues→PR gate, the auto-triggered skill map, triage labels, and the issue lifecycle. Triggers include "let's build X", "file an issue for this", "write the PRD", "open a PR", "what labels", "how do we work here".
---

# T4 Dev Workflow

## Overview

The T4 team's development pipeline, built for an **agent-primary** repo where GitHub issues are the source of truth for *what to do* and *its state* — not a formality. Session-local todos must reconcile back to issues before the session ends. This skill covers how work flows from idea to merge, which skills fire automatically, and the tracker conventions (labels, lifecycle, bilingual bodies).

## The pipeline

When planning or implementing a feature, follow this order:

1. **`/grill-me`** — stress-test the concept interview-style before committing to it.
2. **`/grill-with-docs`** — challenge the plan against existing ADRs in `docs/adr/`; this also lazily produces domain docs (`CONTEXT.md` / ADRs) when a term or decision actually resolves.
3. **Survey the change sites** — enumerate *every* place the change touches **before** writing the plan (below). A PRD written without this plans the change you imagined, not the one the repo needs.
4. **`/to-prd`** — turn the grilled plan into a PRD (one PRD per epic), carrying the survey as its change inventory.
5. **`/to-issues`** — break the PRD into GitHub issues with triage labels (one issue per deliverable).
6. **`/tdd`** — implement test-first (red → green → refactor).

**Four of the six steps above name a skill the agent is mechanically forbidden from invoking.** `/grill-me`, `/grill-with-docs`, `/to-prd` and `/to-issues` all carry `disable-model-invocation: true`, and the `Skill` tool refuses them:

```
Skill triage cannot be used with Skill tool due to disable-model-invocation.
Ask the user to run /triage themselves — it cannot be invoked via the Skill tool.
Do not replicate this skill's workflow by other means.
```

**An agent does not see a blocked call — it sees an absent skill.** A flagged skill is filtered out of the available-skills listing before the agent reads it, so there is nothing to distinguish *"not installed"* from *"installed, reserved for the developer."* On 2026-08-18 an agent bootstrapping a repo concluded the second was the first and wrote the files itself, in good faith, reintroducing the duplication `#96` was filed to remove. That is `#242`.

**So: absence from the listing is not evidence of absence.** When a step names one of these and you cannot see it:

1. **Do not conclude it is missing**, and do not say so to the developer — say it is user-invocation-only and that you cannot call it.
2. **Ask the developer to run it**, naming the exact command and what you will do with the result.
3. **Do not improvise the output.** The error text forbids replicating the workflow by other means, and the whole reason these steps were delegated to another skill is that this family stopped maintaining a second copy of them.
4. **If the developer declines or is unavailable, that is a park**, recorded with what is undone — not a silent substitution.

**This is a property of the other skill, not a defect in this one**, which is why the instruction is a hand-off rather than a fix. The audit of which steps are affected, and what to do about the pipeline being unexecutable from step 1, is tracked separately.

**Hard gate: PRD → issues → PR.** Never open a PR without a referenced issue. A PRD becomes issues before code; code maps to an issue before a PR.

## The hierarchy is a sub-issue tree, not prose

**plan → PRD → issues**, and each edge is a **native GitHub sub-issue**, created through `POST /repos/{owner}/{repo}/issues/{n}/sub_issues` with the child's internal `id` (not its number). `DELETE …/issues/{n}/sub_issue` undoes it, so the structure is safe to build incrementally.

**A plan gets a tracking issue, and keeps its markdown.** The file in `docs/plans/` is the reviewable artifact — it has a diff, a history, and arrives through a PR, none of which an issue body has. The **tracking issue** is the plan's presence on the tracker: a short body linking the file, carrying the tree. Two artifacts, two jobs, a link each way. Record the issue number in `docs/plans/README.md` so the index resolves both directions.

**Why this replaced a heading.** Parenthood used to be `## Parent xeno-skills#176` inside each child. GitHub cannot read that, so nothing could answer *"what did this plan produce, and how much is done"*. Measured 2026-08-17: answering it took exporting 107 open issues, extracting numbers from 54 commit subjects, and a set difference in a shell pipeline — to recover a fact the tracker already held and could not report. **Keep the prose heading if a human reader wants it; it is no longer the mechanism.**

Three things the API will not tell you, each of which misleads if unknown:

- **The rollup counts DIRECT CHILDREN only.** `sub_issues_summary` on a plan reports its PRDs, not its slices — measured on a three-level tree that reported `total: 1` at the top, not 2. **A plan sitting at 0% may have thirty slices done.** Never read a plan's percentage as slice progress.
- **A child has exactly one parent**, enforced by GitHub. Where a slice genuinely serves two, it belongs under the one that *decomposed* it; the other reference stays prose.
- **`## Blocked by` stays prose, always.** A sub-issue expresses **decomposition**, not **ordering**, and GitHub has no native dependency edge. Folding blocked-by into the tree does not move that information — it destroys it.

**Not available here, so do not plan around them:** *Issue Types* are organisation-only and 404 on a user account; *Projects v2* needs a `read:project` scope this tooling may not hold. Sub-issues work on a personal repo, which is why they are the mechanism.

## Intake — which gaps in a directive you may ask about, and when

**The developer's prompt is the only input to this repo with no contract.** A delegation carries
`BrainstormRequest v1`; an issue body carries the bilingual rule; a PR carries the gate. The directive
that starts the work carries nothing — so a missing element is discovered by **building the wrong
thing**, which is the most expensive place to find it.

**Measured, 2026-08-20.** The directive was *"is it possible to use CRISPE with xeno-skills"*, and the
answer went to the **delegation** layer — the request contract, its validator, the panel. The next
message said the prompt meant was the one between **the developer and the master agent**. One unasked
slot — **which layer** — cost a whole turn, and the question that prevents it is one line long.

**Map the directive onto the five slots, then ask about at most two of them:**

| CRISPE | What it is here | Askable? |
|---|---|---|
| **C — capacity/role** | the stance the work needs: implementer, reviewer, researcher, advisor | **only when the audience decides the artifact's shape** |
| **I — insight** | context and constraints **not in the repo**: why now, who reads it, what was tried elsewhere | **yes** |
| **S — statement** | the deliverable, and the one criterion that must hold | **yes** |
| **P — personality** | already fixed by `CLAUDE.md` — Thai chat, bilingual tracker, English identifiers | **never** |
| **E — experiment** | whether alternatives are worth generating | **never** — it is a cost call you make |

**Finish this sentence before you ask, or do not ask** — the park test from `t4-afk`, pointed at intake:

> *"I cannot start because the directive does not say ___,*
> *and the two readings produce materially different work: ___ versus ___."*

**If you cannot name two concrete readings that end in different artifacts**, take the simpler one and
say which one you took. And a gap the repo already answers is not a gap: `CLAUDE.md`, the tracker, the
ledger, a standing instruction, or one `rg` — **a read is not a question.**

**You pick the moment, and there is one per directive.** Ask **before the first action that commits** —
the first edit, the first issue, the first PR — and in one batch, **not a drip**. After the analysis is
already written under one reading it is too late: the answer then costs a rewrite, which is exactly
what the measurement above is.

**Under AFK there is no ask.** Pick the reading, state the assumption where the work is reported, and
put the alternative in the digest (`t4-afk`) — an unattended run cannot obtain an answer, and a batch
that stalls on a question has stopped being unattended.

**Why this carries a brake and not only a prompt.** `t4-afk` records that the over-asking failure has
**no natural corrective signal**: a guess produces a visible wrong artifact and somebody says so, while
an unnecessary question produces a polite list that reads as diligence. So a rule that says *ask more*
without a ceiling **makes the agent worse** — the two askable slots and the two-readings sentence are
that ceiling. **This is not `/grill-me`**, which stress-tests a concept that already exists; intake runs
before there is one.

## Survey the change sites before writing the plan

Most "surprise cases" aren't surprises — they're **sites the plan never knew about**. They surface mid-implementation, when the cheapest moment to have found them has already passed, and they arrive as scope growth (which under AFK is a 🛑 park). The survey is the step that converts them from surprises into line items.

**Do it after the concept is settled (`/grill-me`) and before `/to-prd`** — surveying a concept that's still moving is wasted, and planning without it is guessing.

**The trigger is an action, not a phase: the first time you are about to write down what you will change.** A plan, a PRD, an issue body, a comment saying "I'll edit X and Y", the first edit of a multi-file change — whichever comes first, that is the cue. Phrase it to yourself as *"I am about to commit to a set of files"*, the same way `/simplify` is tied to *after writing code*.

**Why it needed one.** A step attached to a *phase boundary* fires only when someone happens to notice the boundary — and `using-t4` already warns that boundaries are what get crossed unnoticed (*"a check at task start does not discharge a later trigger"*). **Worked example, one session, minutes apart:** on `#78` the survey was skipped and the consequence arrived inside the same edit — one added clause took the injected dispatcher to 9033 B against a hard 9000 B cap. On `#86` the same agent ran it first and budgeted the addition before writing it. **The difference was not diligence. It was that #86's issue body handed the survey over as a section and #78's did not.**

**A sibling issue's change inventory is survey input.** The warning that would have prevented `#78` was already written down — in `#86`'s body, read in the same session. Before surveying, check the issues adjacent to yours for an inventory someone already built; a survey that ignores one is redoing work that exists.

**What to enumerate — don't stop at the obvious file:**

- **Every occurrence of the thing you're changing**, not the first one. `rg` for the symbol, the string, the config key, the route, the error message. **Duplicates are the classic miss:** the same list, rule, or constant written in two files drifts the moment you update one — this repo's own pipeline is described in both `SKILL.md` and `references/workflow-artifacts.md`, and a change to one alone is a defect.
- **Both sides of every mirror.** Bilingual doc pairs (`*.md` / `*.en.md`), a doc and its diagram, a script and its copy in another delivery path, a template and the test that guards it.
- **Callers, not just the definition.** Who consumes this? What breaks if its shape changes?
- **Tests and fixtures** that assert on what you're changing — including a test whose *string literals* encode the old wording.
- **Docs that state the current behavior.** A README sentence describing what you're about to change is a change site; leaving it is how docs drift.
- **Config, CI, and generated artifacts** that reference the thing by name.

**Output: a change inventory** — a flat list of `path` → *what changes there* → *how you'll verify it*. Put it in the PRD (`references/workflow-artifacts.md` has the block) and in the issue. It becomes the implementation checklist and, later, the reviewer's map.

**Say what the survey couldn't reach.** "I searched `rg '<symbol>'` across `skills/` and `docs/`; anything reached by dynamic name construction wouldn't appear" is an honest boundary and belongs in the plan. An unstated search boundary reads as completeness you didn't verify (`No verdict before evidence`, below).

**Cost check:** the survey is minutes of `rg`; the alternative is finding site #4 after the PR is open, when the fix is a re-plan. It scales down — a one-file change gets a one-line survey — but it doesn't get skipped, and skipping it needs the same proof any other rule does.

*The high-risk refactor protocol's "Inventory first" is this same step applied to behavior rather than files — do both when a refactor is in scope.*

## Derive the set a guard checks; never list it

**A guard written as a list of names cannot see the member added after it — and it passes, so nothing tells you.** The list is correct on the day it is written, which is exactly why nobody revisits it.

**Measured, three times in one repository on one day**, each one correct when written:

| The guard | Listed | Reality by the time it mattered | What went unseen |
|---|---|---|---|
| `.gitattributes` line-ending pins | 4 filenames | 24 hooks | 20 files got the opposite line ending from their own installed copy; two suites red |
| the argv check in `test-skill-log.sh` | 5 variable names | 8 hooks | `record_json` and `op_json` — **it missed two the day it was written to catch them** |
| the `.claude/hooks/` sync loop | 4 filenames | 24 hooks | 19 installed copies byte-compared by nothing |

**The fix is the same each time: compute the set instead of writing it down.** A glob (`hooks/*`), a directory read (`ls`), a scan for the shape that creates a member (`x="$(cat)"`). Then a file added tomorrow is covered the day it lands, or the suite goes red naming it.

**The trigger is writing the second name.** The moment a check contains `a b c`, ask: *what adds the next member, and would this see it?* If the answer is "someone edits this line", derive it.

**Two things this does not say.** A **fixture** may name what it uses — a test that copies three hooks into a temp repo is describing its own setup, not claiming coverage. And a derived set needs its **exclusions stated in the file** (`hooks.json` is the plugin manifest and has no installed counterpart), because a silent exclusion is the same defect wearing a glob.

**Why it belongs beside the change-site survey.** The survey is this rule pointed at a change: *enumerate every site before you plan*. This is the survey pointed at the guard that has to keep noticing sites forever. Both fail the same way — the site nobody looked for — and the guard's version fails silently for longer.

## No verdict before evidence (don't state it as settled until it is)

A confident wrong answer is worse than an uncertain right one, because it ends the investigation. State claims in the register the evidence supports — and never upgrade a claim just because you've repeated it.

**Three registers. Pick the one you've earned:**

| Register | Use when | Say it like |
|---|---|---|
| **Verified** | you produced the evidence *in this session* | "`bun test` → 42 passed" · "read `auth.ts:88`, it returns early on null" |
| **Hypothesis** | it's reasoning, inference, or memory | "**Likely** the cache key collides — unverified, would confirm by ___" |
| **Unknown** | you don't know and haven't checked | "I don't know whether X; checking costs ___" |

**A verdict word requires a named artifact.** *Fixed · works · passes · safe · done · the root cause is · no impact* — each is a claim about the world, so each needs the command you ran, the output you saw, or the `file:line` you read, stated with it. Without that, downgrade the sentence to a hypothesis; don't delete the hedge to sound decisive.

**These are not evidence:**

- *"It should work"* / *"by design"* / *"the types line up"* — reasoning about code is not observing it.
- *"The docs say so"* — for a pinned or non-standard version, read the vendored source.
- *"It worked before"* / *"this pattern always works"* — not about this change.
- *"The test exists"* — existing ≠ run ≠ passing.
- **Another agent said so.** A subagent's or bot's report is a hypothesis until you check it (`clink-subagents` says the same: verify everything a subagent returns).

**The laundering failure mode — the one to actually watch for:** a guess stated in turn 1 gets referenced as established in turn 3, and by turn 6 it's the premise of a design decision no one can trace back to a check. **A claim's register never improves by being repeated or summarized.** When you carry a claim forward, carry its register with it.

**Reporting is part of the rule.** If you didn't run it, say you didn't — "tests not run" is a complete, acceptable sentence. Reporting a suite as green without running it is not optimism; it's a false statement about the repo. Same for partial work: name what's unfinished rather than letting "done" cover it.

**The register attaches to the claim; nothing attaches it to the question the evidence answers.** That is the gap this rule had, and it is how the rule can be *followed* and still produce a wrong statement: evidence that verifies **X is true** gets spent on **therefore do Y**, where Y needed a read the evidence never touched.

**Three in one session, 2026-08-17, all with real evidence produced in-session and correctly cited:**

| The claim | The evidence held | The read that would have caught it |
|---|---|---|
| *"#175 names no issue"* | `Select-Object -First 14` of the body | the **last** line of the body, which is `Blocked by …` |
| *"`clink` has a `schema` parameter"* | a prior session's handoff note | the live tool schema — one call |
| *"#204 should be closed"* | four checks **on our side**, all correct | the **other repository's** tracker and tests |

The third is the one to remember: the live tool schema, `~/.claude.json`, `server.py:1511` and 15 references in `skills/` were all read and all right. Then the other repo turned out to contain a test whose docstring already held that analysis, a plan issue, and a deliberate exclusion. **The mechanism claim was correct and the recommendation was wrong, and the evidence cited did not reach it.**

**So: when a verdict recommends an ACTION rather than asserting a FACT, the artifact requirement extends to the action's own preconditions.** *Close it · ship it · skip it · file it · this supersedes that* are not facts about the mechanism; each has a precondition set of its own. **For anything cross-repo, the other repository's tracker is one of them** — the survey rule above already treats a sibling issue's change inventory as input, and this is that idea pointed one repo over.

**The cheap tell: name the read you did, then ask what the recommendation assumes that the read did not cover.** In all three cases above the missing read was one command.

**And issuing the action is the same verdict, which is where shell chaining escapes it.** A verdict you
*state* is read by somebody; **a verdict you *run* is read by nothing.** `gh issue close`, `gh pr merge`, a
delete — each asserts its precondition by executing, and the precondition is usually **another
command's output**, in a block that queues the next line before anyone reads the last one.

**Measured, 2026-08-19:** a close fired twice while its PR was unmerged. Both times it sat in the same
block as a merge that had just printed `Pull Request has merge conflicts`, then `not mergeable` — and
both times it was joined with `&&` to a *different* command's success, so it ran anyway.

| The block | What it actually asserts |
|---|---|
| the merge, then `gh issue close <n> --reason completed && echo closed` | nothing — the close runs whatever the merge printed |
| `gh pr view <n> --json state` **read**, then `gh issue close <n>` as a separate step | the precondition, checked |

**So when the precondition of an action is another command's output, read that output as its own step.**
Not the same block, and never chained: `&&` makes the action depend on *a* success rather than *the*
success, and you will not be there to read the failure before the next line runs. This is the same rule
as the action's own preconditions, one layer down — the artifact exists, and the shell scrolls it past.

**Ask what a number measures before you spend it.** A figure can be accurate, correctly cited, and still be **the wrong quantity** for the decision it is carried into — and that failure looks identical to good evidence, because the number really is right.

**Measured, 2026-08-14.** A cost-per-task figure from Artificial Analysis was used **twice** to argue against a model for a reviewer role. That figure measures a **metered API lane**. The lane in question was the developer's **flat subscription**, where it buys nothing and predicts nothing — and the harness's own default evaluator is the same model on the same lane. **The developer had to say so twice.** The number was not wrong; it described something else.

**The check is one question and it is the same shape as the register above:** *what unit, measured on what, and is that the thing I am deciding about?* Cost per task, tokens, latency, an index score and a quota are five different quantities, and only one of them is ever the one you are spending.

**This is the sibling of the action-verdict rule.** That one is evidence answering the wrong **question**; this one is evidence answering in the wrong **unit**. Both are the rule above being *followed* and still producing a wrong statement, which is why neither is a restatement of it.

**Why it lives here and not in a delegation skill.** `clink-subagents` already carries it as a *routing* rule — *"pick the back-end by latency × intelligence × subscription-quota you'll spend, never by its token count"*. The 2026-08-14 failure was about a **native harness feature** with no `clink` in it, so no delegation skill was loaded and the rule was not in the room. **Asking what a number measures is not specific to delegation.**

**Why it's load-bearing here:** the records layer is an index future agents trust without re-checking (`t4-engineering-records` — validated-only, `file:line`, commit SHAs). One unverified verdict written as fact poisons it, and the cost lands on whoever inherits the repo, not on the session that saved a minute.

## Skipping a rule requires proof (the burden is on the skip)

Every rule here has a cost, so there is always a locally-reasonable argument for skipping one. That argument is exactly the failure mode: skipped once with a good story, the rule stops being a rule. So the burden of proof sits on the skip, never on compliance.

**The default is comply.** An exemption is valid only when you can state a **checkable fact about this specific change** that makes the rule inapplicable — one a reviewer can verify *without redoing your reasoning*.

| Not a proof (judgment dressed up) | A proof (checkable fact) |
|---|---|
| "Small change, tests can't be affected" | "`git diff --name-only` is `README.md` only — no code path is reachable from it" |
| "This is unrelated to the failing suite" | "The suite imports `src/a.ts`; the diff touches `src/b.ts`, which nothing in `a` imports — checked with the import graph" |
| "Obviously safe" / "I'm confident" | "The function is unreferenced: `rg 'fooBar\(' -g '!*.test.*'` returns only its definition" |
| "Running it is slow" | *Never* a proof. Cost is not evidence. |
| "The user is in a hurry" | *Never* a proof. Urgency changes priority, not truth. |

**If you cannot state the proof, follow the skill.** Uncertainty resolves toward compliance — always, and without asking. "I'm not sure whether this needs a test" means it needs a test.

**Offering the developer a choice to skip a gate is itself a skip.** The rules above bind *your* reasoning — urgency is not a proof, uncertainty resolves toward compliance. The move that routes around both is to hand the choice over: *"merge now, or run the review first — about six minutes?"* The developer's "yes" is **not a checkable fact about this change**, so **the burden of proof does not transfer by asking**. It only looks like authorisation, and the skip proceeds looking approved.

**Why "but they can waive it" is the wrong objection.** They can. The rule is about **who raises it**. A developer who says *"skip the review"* has decided with the cost in front of them; an agent that offers *"fast, or thorough?"* while reporting a time estimate has framed the choice so the fast answer looks free, and has moved a gate into the developer's queue. **The allowed form is: report the cost, then comply.** A **developer-initiated waiver** remains valid; an agent-offered one does not.

**This is not "never ask anything".** You may still say a gate is expensive, and you may still ask when a gate is **genuinely ambiguous in scope** — *which* files a security review should cover is a real question. What you may not do is present skipping as an option you are neutral about. It is the mirror image of the over-asking failure in `t4-afk`: that one asks permission to do more, this one **asks permission to do less**.
**And state every judgment gate, whether or not you have an exemption to write.** The exemption rule above covers a rule you *argue* your way out of. It does not cover one you simply never reach — and the judgment gates (`/simplify`, `/code-review`, `/scrutinize`, `/security-review`, `/verify`) have no hook, so skipping one used to leave no trace at all. Put the answer on the branch as a commit trailer:

```
T4-Gates: simplify=ran code-review=ran scrutinize=not-run security-review=n-a verify=ran
```

**`not-run` is a legal answer** and `check-gate-ledger` accepts it. The guard raises the cost of skipping a judgment gate from zero; it does not pretend to verify the reasoning, which it cannot. What it refuses is a gate you say nothing about, because an unrun gate is otherwise indistinguishable from a passed one in the only report anybody reads.

**And passing the guard does not discharge this rule — they set different bars, deliberately.** `check-gate-ledger` demands *state it*. This section demands *state it **and** justify it with a checkable fact, or do not skip*. A commit can satisfy the first while violating the second, and **nothing anywhere notices**.

Measured: `pal-mcp-server` PR #86 carries `T4-Gates: simplify=not-run code-review=not-run scrutinize=not-run security-review=not-run verify=ran`. **Against the guard it passes cleanly** — every gate stated, every value legal. **Against this section it is four violations**, because not one carries the checkable fact. Its author believed the ledger had discharged the obligation.

**That belief is the predictable one, and that is why this paragraph exists.** The guard is what speaks at commit time; the section is a document. An agent optimising against the mechanism that talks back lands on a bare `not-run`, which is exactly what the proof requirement was written to prevent. **A permissive guard beside a strict rule relaxes the strict rule in practice** unless the difference is stated where the rule is.

**Neither side is going to grow into the other.** The guard cannot check whether a reason is *true*, and this file already says so — *"hooks can raise the cost of skipping a judgment skill but can't verify the reasoning."* So the bar the guard enforces is a floor, and the bar here is the actual requirement. **Read a green `check-gate-ledger` as "nothing was silent", never as "the skips were justified."**

**Say it where the work is reported.** An exemption that lives only in your head is a violation, not an exemption: write it in the PR body / the message reporting the work, in the form *rule → the checkable fact → how to verify it*. This is what makes it reviewable, and what makes a wrong exemption catchable later.

**Never exemptable by argument:**

- **Hook-enforced rules** — a PR needs a referenced issue, `verify` must pass, dangerous git. The gate does not read prose; arguing with it means disabling it, which is the anti-pattern itself.
- **Safety and trust boundaries** — `/security-review` on anything touching auth/secrets/input trust, and the destructive-command rules. The blast radius is asymmetric: being right saves minutes, being wrong is unrecoverable.
- **Anything the user has just told you to do.** A direct instruction is not a rule you get to prove your way out of.

**Consequence for a stated exemption that turns out wrong:** it becomes a record, not a shrug — the rule that was skipped goes back on, and the wrong proof is worth a line in the post-mortem (`t4-engineering-records`), because a bad exemption pattern will otherwise repeat.

*This meta-rule governs every "narrow exception" clause in these skills, including the one below.*

## A red must fail for the reason the test names

**A non-zero exit is not a red.** Read the failure output and check it is the failure the assertion describes — a red you have not read is a green you have not earned.

**Two generators, both measured in this repo, and both produce a red against code that does not exist:**

- **The harness reports the failure, not the code.** Building `check-issue-ref` test-first on 2026-08-11, the red passed against a **missing file**: `sh` exits non-zero when it cannot open a script. Every assertion downstream of "it exited non-zero" was satisfied by the absence of the thing under test.
- **The path leaks into the assertion.** The second assertion in that same test — *"the message names what's missing"* — matched on the word `issue`, which appears in the interpreter's own error because the script is called `check-issue-ref`. The test was reading its own filename.

**The correction is one rule: assert on something only the implementation can emit.** A returned value, a real flag, a measured number, a file the code writes. Never a word that also appears in a path, an error message, or the test's own text.

**And the same trap runs the other way — an assertion that cannot fail.** On 2026-08-19 a fixture built with `json.dump` was written to prove a control byte is stripped before display; `json.dump` cannot emit a raw ESC, so the fixture could not carry the attack and the assertion passed against a file that never contained it. **A green that was never capable of red is the same defect seen from the other side**, and it is why every rule suite here carries positive controls.

**Make the detector dirty on purpose.** A red nobody has seen go green for the stated reason, and a green nobody has seen go red, are both claims rather than evidence. The probe costs a minute; the alternative is a suite that passes both before and after a defect — which happened here on 2026-08-19, twice, with 94 assertions watching.

**For a delegated red, this is necessary and not sufficient** — a worker can return a red that reproduces perfectly and is still anchored on a sentence it invented. That case, and what to demand instead, is in `clink-masteragent`; it is not restated here.

**No enforcement is added.** Nothing can read an assertion and decide what it is *about*.

## Root cause before fix (applies to bugs *and* review findings)

**Do not propose a fix, and do not edit, until you can name the root cause with evidence.** The output of diagnosis is a sentence of the shape: *"X fails because `path/file.ts:42` does Y when Z, which I reproduced by ___."* Until you can write that sentence, any fix is a guess dressed as a solution.

The order — no step skipped because the answer "looks obvious":

1. **Reproduce.** A failing test, a command, or an exact sequence. If you can't reproduce it, say so explicitly and treat everything after as a hypothesis, not a diagnosis.
2. **Trace the actual path.** Read the real code from entry point to failure — not the diff, not the file you assume is at fault. Cite `file:line`.
3. **Falsify.** State the hypothesis so it can be wrong, then try to break it. If two causes both explain the symptom, you haven't finished.
4. **Then** propose the fix — and say which part of the trace it addresses.

`/debug-mantra` (9arm) is the discipline for this; invoke it on any bug, error, stack trace, or failing test rather than working from the symptom.

**Why it's a rule here:** a symptom-level fix in an agent-primary repo is expensive twice — it lands, looks green, and the real cause resurfaces later with the misleading fix now in the way. It also poisons the records layer: a post-mortem written from an untraced fix is a *wrong* index entry, worse than none (`t4-engineering-records`).

**Applies equally to:** review findings (`/scrutinize`, `/code-review` — verify the finding against the code before acting on it, including one an agent or a bot reported), CI failures (read the log; don't re-run hoping), and performance work (measure first; a guessed bottleneck is the same error wearing a stopwatch).

**The exceptions are narrow, and you say them out loud:** a trivially-reversible one-liner where reproduction costs more than the change, or an emergency mitigation to stop the bleeding — in which case the mitigation is *not* the fix, and the root cause stays open work (ledger row + issue).

## Auto-triggered skills (fire without waiting for the user)

| Trigger | Skill | Condition |
|---|---|---|
| **A new directive from the developer** — the first message of a task, or one that changes its shape | **intake** (above) | Before the first committing action. At most two slots, one batch; under AFK, assume and report |
| **About to write down what you will change** — a plan, a PRD, an issue body, or the first edit of a multi-file change | **change-site survey** (above) | Every time. Check adjacent issues for an inventory that already exists |
| Bug / error / stack trace | `/debug-mantra` | Start a debug session every time |
| Complex debug / perf regression | `/diagnose` | reproduce → minimise → hypothesise → fix |
| After fixing a bug | `/post-mortem` (see t4-engineering-records) | Record root cause + fix + validation |
| After writing or changing code | `/simplify` | Before committing — check over-engineering |
| Editing UI / frontend | `/impeccable` | Every time a component or CSS is touched |
| Before merge / ship | `/code-review` + `/scrutinize` | Correctness + outsider perspective |
| Touching auth / token / secret / any security boundary | `/security-review` | Every boundary crossing |
| After implementation | `/verify` | Confirm the feature works in the app |
| New UI needs a design brief | `/impeccable` (shape) | Plan the UX before implementing a component |
| UI ready to ship | `/impeccable` (audit + harden) | a11y / perf / responsive + edge cases before merge |
| Codebase complexity growing | `/improve-codebase-architecture` (or equivalent) | On a cadence (e.g. every few days) or after a major feature |
| Exploring unfamiliar code | `/zoom-out` | High-level context before editing |
| User asks "is there a skill for X?" | `/find-skills` | Search before hand-writing code |

## Capability router (optional)

Route by the *capability* a task needs, not a hardcoded tool name — the capability is stable; the tool/command is repo/runtime config that `t4-project-bootstrap` populates from the installed MCP/PAL tools.

| Capability | Tool (repo-configured — examples) |
|---|---|
| Code review | `mcp__pal__codereview` |
| Debug / diagnose | `mcp__pal__debug` |
| Architecture review | `mcp__pal__analyze` |
| Security audit | `mcp__pal__secaudit` |
| Test / QA planning | `mcp__pal__testgen` |
| Deep reasoning / second opinion | `mcp__pal__thinkdeep` / `consensus` |

If nothing is configured for a capability, use the general skills directly.

## What's mechanically enforced (vs. agent discipline)

In a repo with the T4 hooks installed (`t4-project-bootstrap` → `references/hooks-layer.md`), part of this pipeline is a **hard gate**, not just discipline the agent is trusted to keep:

- **PRD → issues → PR** — the `PreToolUse` gate **denies** `gh pr create` with no referenced issue.
- **Ship gate (`/verify`)** — before `gh pr merge` (merge is the ship point; not the iterative `create`), the gate **runs the repo's `verify` command itself** (`.claude/t4.json` `"verify"` — keep it fast; e2e belongs in CI) and denies on failure. The server-side CI required-check + branch protection is the real guarantee (it also covers a human merging on the web).
- **Before merge** — `gh pr merge` **asks** you to confirm `/code-review` + `/scrutinize` ran — unless `.claude/t4.json` sets `"autoMerge"`/`"afk"` (an unattended run under standing authorization), which skips the ask; the `verify` deny still holds.
- **Dangerous git** (`reset --hard`, force-push, `clean -f`, `branch -D`) is **denied**.
- **The GitHub MCP surface is gated too** (#83) — `mcp__github__create_pull_request` meets the same issue-reference rule as `gh pr create`, and `mcp__github__merge_pull_request` meets the same verify-and-review ship gate as `gh pr merge`. Read-only GitHub tools pass; anything else under `mcp__github__` **asks**, so a capability the server gains tomorrow does not fail open. This was a real hole, not a hypothetical one: six PRs were merged straight through the MCP tool with no verify and no review, and none of them looked like a bypass at the time.
- **Agent-agnostic guards** — the `PreToolUse` gate only sees tool calls *Claude* makes, so a repo running Codex/Gemini (or a human) pushes past it. A git **pre-push** hook re-checks the issue reference and blocks a large dirty tree or committed build artifacts, binding every agent on the clone (`t4-project-bootstrap` → `references/guards-layer.md`). Opt-in per clone and `--no-verify`-able, so the same scripts run in CI where they aren't.
- **CI required checks** — the layer above the hooks (`t4-project-bootstrap` → `references/ci-cd-layer.md`): `lint`/`typecheck`/`test`/`build` are separate **required status checks** on `main` and direct pushes are blocked, so a red PR can't be merged by anyone — agent or human on the web. Where a ruleset isn't available, `.claude/t4.json` `"requireGreenCI": true` makes the gate check `gh pr checks` before merge instead (weaker: it only binds agent-run commands). E2E lives in CI, not in the local `verify`.

Everything else — TDD discipline, `/simplify`, the *depth* of a review — stays agent discipline, reinforced by the session-start dispatcher (the injected `using-t4` map). Hooks can raise the cost of skipping a judgment skill but can't verify the reasoning; only checkable actions are hard-enforced.

## High-risk / core refactor protocol

Ordinary TDD covers most changes. A refactor of a **large or load-bearing module** — a "god object", a critical seam, a monolith you're decomposing — needs more, because the risk is *silent behavior change during relocation*. When you're moving/extracting code in such a module, follow this (distilled from the MangaDock characterization ADRs):

1. **Inventory first.** List the behavioral variants and landmines the module actually has (known divergences, edge cases) before moving anything — you only preserve what you've named. (This is the *behavioral* half of the change-site survey above; a refactor needs both.)
2. **Characterize before you move.** Add characterization tests that pin the *current* output (quirks included) at the seam **first**. Refactor only behind green characterization — it's the net that catches a relocation that changed behavior.
3. **One seam per commit.** Extract one boundary at a time, each commit output-equivalent (ideally byte-identical). A reviewer or a diff can verify one seam; a ten-seam commit hides a regression.
4. **Never mix relocation with a behavior fix.** Move in one commit, fix in another — otherwise "did the move change anything?" is unanswerable.
5. **Preserve known divergences.** A deliberate quirk stays (with its characterization test); don't "clean it up" mid-move.
6. **Attach new features at the new seam, not the monolith** you're retiring.

Under AFK this is doubly load-bearing: seam/architecture decisions are a 🛑 **park** (see `t4-afk`), so an unattended run does the *mechanical* extraction behind characterization tests and parks the judgment calls.

## Bilingual tracker rule (GitHub only)

Issue bodies, PRD bodies, and PR descriptions must be **bilingual — English + a full Thai mirror**:

- **Title:** English, conventional-commit style (e.g. `fix(<scope>): ...`).
- **Body:** each section in English, then a mirrored Thai version — either a `## สรุปภาษาไทย` section covering the whole body, or `EN / TH` paired paragraphs per section for long docs.
- **The Thai must mirror the English exactly** — same detail, sentence count, bullets, tables. "สรุป" is not a summary; never shorten or omit.
- Code identifiers, filenames, log excerpts, and acceptance-criteria checkboxes stay English; the Thai explains them, never translates identifiers.
- **Review-reply comments may be English-only.** Anything a teammate reads to *decide* gets both languages.
- **Scope: the GitHub tracker.** This rule governs issue / PRD / PR bodies. Governed **agent docs** (`CONTEXT.md`, `DESIGN.md`, `PRODUCT.md`, `docs/agents/*`) have their *own* bilingual convention — `<!-- lang:en/th -->` markers, full mirror (see `t4-project-bootstrap` → governance-docs). Chat, reports, and status updates are single-language (the developer's — Thai); code, commit messages, and inline comments stay English.

## Retarget a stacked PR before merging its parent

**`gh pr merge <parent> --delete-branch` closes every PR whose base is that branch, and the close is not reversible.** Measured on 2026-08-11: three PRs open, `#41` based on `#35`'s branch. Merging `#35` deleted `feat/root-cause-first`, GitHub closed `#41`, and recovery failed twice —

```
gh pr reopen 41       -> Could not open the pull request
gh pr edit 41 --base main -> Cannot change the base branch of a closed pull request
```

**Both failures are the same wall.** A closed PR's base is immutable, so you cannot retarget it, and you cannot reopen it because its base branch no longer exists. The review history, the comments and the CI record are stranded there.

**So the order is fixed, and it is the only part that matters:**

1. **Retarget every child to `main` first** — `gh pr edit <child> --base main`, while the child is still open.
2. **Then merge the parent.** `--delete-branch` is now safe: nothing points at the branch.
3. **Then merge the children**, whose diffs now read against `main`.

**If it has already happened:** rebase the child's branch onto `main`, open a **replacement** PR, and reference the closed one in its body. The old PR stays closed — that is not a workaround, it is the only path, and the reference is what keeps its review history findable.

**No hook enforces this.** The gate sees one prospective tool call and cannot know another PR is stacked on the branch this one deletes; discovering that costs a network call the gate has no budget for. It is ordering discipline, and it is written here because the failure is silent, immediate and permanent.

## Issue lifecycle (Definition-of-Done gate)

- Every code change maps to **one issue you're allowed to work** — authored by us, or labeled `ready-for-agent`.
- Keep the issue **body** current (not just comments) as scope/state changes, bilingual.
- **Close with a stated reason** — completed-with-evidence / cancelled / duplicate / wontfix / stale. Never close silently; never leave finished work open.
- New work discovered mid-session gets a ledger row and (if non-trivial) an issue, so it doesn't vanish into MD (see t4-agent-memory).

## Triage labels

Five canonical triage roles: `needs-triage` · `needs-info` · `ready-for-agent` · `ready-for-human` · `wontfix`. Optional groups as the tracker grows: **Component** (one per issue), **Type** (`Bug`/`tech-debt`/`security`/`Feature`/…), **Severity** (`critical`/`Major`/`Minor` — a `security` issue must be `critical` or `Major`). Full definitions + the `docs/agents/triage-labels.md` skeleton are in the reference.

## Delegation guardrail

Delegate only mechanical, low-blast-radius work to a cheap subagent (bulk renames, boilerplate, log summarizing, grep-and-report). Never delegate security-boundary code, architecture/seam decisions, bilingual issue/PR authoring, or judgment-gated skills (`/scrutinize`, `/code-review`, `/security-review`, `/debug-mantra`). A delegated change is not exempt from the verify/E2E mandate. See **`references/delegation.md`** for the discipline: sizing (chunk by independently-governed unit), the Option A/B skill-handoff economics (a handed-off skill costs context budget, not free), landmine injection into the child prompt, and component-aware verification.

## Skeletons

See `references/workflow-artifacts.md` for: `docs/agents/{workflow,issue-tracker,triage-labels}.md`, and the PRD / design-spec / implementation-plan templates.

## Cross-skill

- Recording the *outcome* of the work (post-mortem / ADR / impact entry) → **t4-engineering-records**.
- Reconciling issues ↔ the open-work ledger, and session-start reads → **t4-agent-memory**.
- Scaffolding these files into a new repo → **t4-project-bootstrap**.

## Common mistakes

- **Opening a PR with no issue.** Breaks the gate; the work has no tracked state.
- **A Thai body that summarizes instead of mirrors.** The rule is same-depth mirror, not a digest.
- **Closing an issue silently.** Always state the reason + evidence.
- **Fixing the symptom you saw first.** Name the root cause with evidence before proposing or applying a fix — see above.
- **Planning from the first file you opened.** Survey every change site before the PRD; the sites you didn't look for become mid-implementation "surprises".
- **Translating code identifiers into Thai.** Identifiers stay English; the Thai explains around them.
