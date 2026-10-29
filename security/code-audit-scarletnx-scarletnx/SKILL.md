---
name: code-audit
description: "This skill audits uncommitted changes, branches or PRs for bugs, edge cases, SOLID/DRY/SRP, architecture, security, performance and CLAUDE.md violations. Then it automatically fixes ALL the issues and audits again in a loop until the result is clean. Use it for: audit, review, code review, review this PR, check code, look over this, inspect code, or any variation."
---

# Code Audit

**This skill is a LOOP in two phases (see "PHASE SPLIT" below). Phase A audits read-only, pass after pass, until a full pass adds no new findings. Then Phase B fixes ALL the findings (each severity) one time and reads the files again from disk. Then it does confirmation rounds until one round comes back clean. If you stop after one pass, or if you fix code during Phase A, you do not obey the instructions.**

---

## RULE 0: DO NOT YIELD (MANDATORY, read this before all other text)

After the loop starts, **if you end your turn before step 12, that is a violation.** It is not a judgement call and not a courtesy. It is a violation, in the same category as a skipped file.

The loop stops in only one way. You reach step 11, its predicate says stop, and you emit the step 12 Final Report. Until then, you continue the work in the same turn, and you do not check in with the user.

**All of these are violations. Each of them ends your turn:**

| What it looks like | Why it feels justified | What it is |
|---|---|---|
| `"Which would you like: (1) continue, (2) fix first, (3) something else?"` | it offers control | it abandons the loop |
| `"Want me to run Pass 3?"` | it confirms before a cost | the loop already answered this |
| `"Here's what I found so far — let me know how to proceed."` | transparency | a status report that nobody asked for |
| `"Pass 2 is done. Say the word and I'll continue."` | politeness | you wait for a permission that you already have |
| `"Given the yield was thin, I'd expect diminishing returns — your call."` | good judgement | you put your stop rule in place of the rule of the skill |
| You stop because the turn is long, the context is large or much happened | prudence | a cost-shortcut, and the cost is not your decision |

**You already have permission for the full loop.** The skill call IS the authorization for each pass, each fix and each new dispatch, up to the step 11 termination predicate. If you ask again, that is not caution. You do not obey the instruction that the user gave you.

**The one exception is a genuine blocker that makes all progress impossible.** These are blockers:

- a build that you cannot fix from inside the audit
- a credential prompt
- a destructive action outside the audit scope
- a step-5 finding with the explicit mark NEEDS USER INPUT.

These are NOT blockers: `"This is a lot of work,"`, `"I'm unsure whether to continue,"` and `"the user might want to weigh in"`.

**Continuous and one-time instructions.** The loop is a CONTINUOUS instruction. It stays in force until step 12, and it needs no renewal. A user message such as "commit and push" is a ONE-TIME instruction about the current state. It does not become a continuous permission.

Some sessions turned these around: they asked again for the continuous instruction, and they made the one-time instruction general. That is a specific known failure of this skill. Do not do it.

## Usage

```
/code-audit <scope>
```

**Examples:**

- `/code-audit` — audits the uncommitted changes (the default)
- `/code-audit branch` — audits the current branch against main
- `/code-audit staged` — audits only the staged changes
- `/code-audit PR` or `/code-audit PR #123` — audits a pull request
- `/code-audit src/nx/gpu/video/nvdec.c src/nx/hle/services/nvdrv.c` — audits specific files

If the user gives a `<scope>`, use it directly. Do not ask the user to make it clear. If the user gives no scope, use the uncommitted changes as the default.

**The scope does not change.** `/code-audit PR #N` and `/code-audit branch` audit the FULL declared scope. You must NOT make it smaller. Do not limit it to `"changed since last audit,"`, `"recent commits,"`, `"since pass N,"` or `"files I haven't already reviewed."`.

Earlier audit history does NOT decrease the coverage of the current run. This history includes other passes, other commits and review comments that say "reviewed". The skill keeps no state from earlier runs. Each call audits the full declared scope again from the start.

---

## Steps

### 1. Determine Scope

Use the argument of `/code-audit` if the user gives one. If not, find the scope from the context, or use the uncommitted changes as the default:

| Scope                     | Diff source                                     |
| ------------------------- | ----------------------------------------------- |
| **Uncommitted** (default) | `git diff` + `git diff --cached` + `git status` |
| **Staged only**           | `git diff --cached`                             |
| **Branch vs base**        | `git diff main...HEAD`                          |
| **Pull request**          | `gh pr diff <number>` or `gh pr diff`           |
| **Specific files**        | Read the named files directly                   |

Read each file in the scope FULLY. Read a file of more than 800 lines in parts. Use the `offset` and `limit` parameters of the Read tool, and continue until you read 100% of the file. A diff alone is not sufficient. Do not do partial reads (`"changed functions plus context"`). With a partial read, you do not see inconsistencies between files, architectural drift and pattern violations at all.

### 1.5 File Inventory

Before the analysis, list each file in the scope in a numbered checklist:

1. Run the applicable diff command from step 1 to get the file list.
2. Get the line count of each file. For a file that exists, use `wc -l <file>`. A new file in the diff starts at 0, and has its final size after the patch.
3. Write the inventory as a numbered list:

```
File Inventory (N files in scope):
  1. path/file1.ext (NNN lines)
  2. path/file2.ext (NNN lines)
  ...
  N. path/fileN.ext (NNN lines)
Total: N files, M lines.
```

### 1.6 Audit State File (MANDATORY)

Write `.claude/audit-state.json` immediately after the inventory. The path is relative to the repository root (the cwd). Use this exact path, so that the Stop hook can find the file. **Update the file at the end of each pass, before step 9**:

```json
{
  "scope": "PR #822",
  "partitions": 6,
  "pass": 1,
  "phase": "A",
  "inventory_files": 57,
  "complete": false,
  "findings": [
    {"id": "F1", "sev": "HIGH", "file": "src/nx/hle/services/nvdrv.c:42", "status": "open", "raised_pass": 1}
  ]
}
```

**`phase`** (`"A"` or `"B"`, the default is `"A"`). Set it to `"B"` in the same action that ends Phase A (the step 11 decision to remediate). The Stop hook (`.claude/settings.json`) reads it, and tells you the phase whose work you must continue.

**`awaiting_agents`** (optional, the default is false). Set it to `true` in the same action that dispatches the partition reviewers of a pass. Set it back to `false` when their reports arrive. A dispatched subagent reports with a task-notification, and that mechanism needs the turn to end. That is not a yield. When this flag is `true`, the Stop hook lets the turn end.

The flag is NOT a general escape. When the flag is absent or false, the hook still blocks a turn that ends in the middle of the loop. If you set the flag while no agents are in flight, that is the same falsification as an early `complete: true`.

`complete` stays `false` for the full loop. Set it to `true` **only** as the last action of step 12, after you write the Final Report. A **`Stop` hook reads this file, and it does not let your turn end while `complete` is `false`**. If you try to yield in the middle of the loop, the hook gives control back to you with an instruction to continue. Do not set `complete: true` to escape the loop. That is a falsification of the audit.

There are only two legitimate ways out: the step 11 predicate and a genuine blocker (the exception of Rule 0). For a blocker, you must still emit step 12, with a verdict that tells what stopped you.

`status` is one of `open` | `fixed` | `descoped`. A `descoped` finding also needs a `"descope_reason"`, and a `"raised_pass"` that is ≥ 2 passes earlier (see step 5).

This rule exists because your memory of the loop decays as the context fills, and the decay is silent. The file is the authority, not your memory:

- **"Am I done?" is a QUERY, not a judgement.** If a finding has `status: "open"`, the answer is no. At the start of each pass, read the file again. Do not use your memory of the state.
- **With the file, a silent descope is not possible.** If you stop the work on a finding without a word, the finding stays in the file as `open`. It then blocks the CLEAN verdict.
- **The file stays after a context loss.** If the system summarises the conversation in the middle of the loop, this file tells you exactly where you are.

At the start of each pass ≥ 2, read the file again. Before you do other work, echo this line:

```
LOOP STATE: pass N (no cap: until a pass finds nothing new) · P partitions · X findings open · next: step 9 fresh read · DO NOT YIELD (Rule 0)
```

The inventory from step 1.5 is the coverage checklist for steps 9 and 12. You MUST read and analyze each file in it fully. If you skip a file, the skill fails.

### 2. Read Project Rules

Read `CLAUDE.md` and the files that it refers to. If there is no `CLAUDE.md`, skip this step.

### 2.25 Tools: ast-grep + grep

The audit uses two search tools that complete each other. **Prefer ast-grep for code. Use plain grep for text and comments.**

`ast-grep` matches the parse tree. Thus it ignores hits inside strings, comments and tokens that spell the pattern by accident. Use it when the pattern is a code shape (a function call, a declaration, a control-flow construct). `grep` works on text. Use it for comments, docstrings, error messages and exact string literals.

Frequent patterns for an audit in this repository (the C runtime and recompiler, the Python tools):

| Goal | Command |
|---|---|
| Find each caller of a function (to find dead code) | `ast-grep --pattern 'FunctionName($$$)' --lang c src` and `grep -rnw 'FunctionName' src tests tools scripts cmake` |
| Find each use of a struct field | `ast-grep --pattern '$X.field' --lang c src` and `ast-grep --pattern '$X->field' --lang c src` |
| Find each guard that only logs | `grep -rn -A2 'WARN(\|LOG(' src`, and make sure that a `return` or a different exit follows each one |
| Find a guest address squeezed into 32 bits | `ast-grep --pattern '(u32)$X' --lang c src`, then examine if `$X` is a guest address or a pointer |
| Find each syncpoint id that does not come from `syncpt_alloc()` | `grep -rn 'syncpt' src/nx/gpu src/nx/hle/services/nvdrv.c` |
| Find each service command that a file answers | `grep -n '^ *\(@[a-z]* \)*\[[0-9]*\]' src/nx/hle/services/am.swipc` (or the `.swipc` of the service), and the handler `nn_..._Command` in its C file. Each answer must agree with the data that the SDK caller reads (see the `snx-service` skill). |
| Find each TODO/FIXME/HACK marker | `grep -rn 'TODO\|FIXME\|HACK\|XXX' src tests tools scripts cmake` |
| Find a stale claim in a comment (for example, "below 192") | `grep -rn "below 192" src` |
| Find AI-ism punctuation in text that users read | `grep -rn '—' README.md docs/ROADMAP.md <changed user-facing files>`. Then look for a `;` that joins clauses, and for a ` - ` in place of a dash. Do not include code comments and code in backticks. |

Do not memorise the list. The principle is this: **a finding can say that site A uses this pattern, and that you must also check sites B…N. Then you must do a grep or ast-grep step before you complete the finding.** A refactor-completeness finding without a list of all the matches is incomplete.

### 2.5 Parallel Reviewer Decision

Calculate the size of the scope from the inventory:

- **≤10 files AND ≤2000 changed lines**: a single-threaded analysis. You do step 3 directly.
- **>10 files OR >2000 changed lines**: you MUST divide the scope into partitions for domain-specialist reviewer agents. A single-threaded analysis of a large scope is a skill failure. One context window cannot hold a deep analysis of 50+ files.

For partitioned scopes:

1. Group the files by coherent domain. Examples are kernel and services, GPU and shaders, audio and video, platform backends, the recompiler and its ABI, and build and scripts. Usually there are 4-6 partitions. Try to put ≤15 files in each partition.
2. **Reviewer selection.** Look in the available agent types for domain reviewers that the project defines. In this repository, these are the `snx-*-reviewer` agents in `.claude/agents/review/`. The description of each one names the directories or domains that it covers. If such agents exist, the partition boundaries SHOULD follow the domains of the specialists.

   You MUST dispatch each partition to the specialist whose description matches it. A specialist has stack expertise and patterns of past bugs that a generic reviewer does not have. Only for a partition that no specialist covers, or when the project defines no specialists, use `subagent_type=general-purpose`. Dispatch ONE `Agent` call for each partition. Put all the Agent calls in a SINGLE message, so that they run in parallel.
3. Each agent prompt MUST include these items:
   - The exact file paths in its partition (explicit paths, not a directory glob).
   - An instruction to read each file FULLY (no partial reads, not only the diff).
   - All the step 3 analysis dimensions, copied word for word. These include refactor-completeness, comment-code synchronization, the defensive-code pair audit and side-effect completeness.
   - The project rules from `CLAUDE.md`. Quote the applicable sections, and do not write "see the file".
   - **Grep scope ≠ read scope.** The *read* scope of the agent is only its partition files. But its *grep / ast-grep* scope is the FULL repository. The agent MUST grep outside its partition for these items:
     - (a) each old-pattern remnant of a refactor that it verifies. For "X should now use Y", list all the X uses that stay.
     - (b) the callers of each public function that its partition touches.
     - (c) the comments that name a count, or a method or class, that it can verify.

     The partition limits where the agent reads files fully. It does not limit where the agent searches.
   - A request for prioritized findings in the format: `file:line — description — suggested fix — severity`.
   - **An explicit delivery instruction.** The plain-text output of a dispatched agent does NOT come back to you. The agent runs as a background teammate, and text that it only prints goes nowhere. Each prompt MUST end with this text: "When you finish, call the `SendMessage` tool with `to: \"main\"` and your full findings as `message`. The system does not deliver your plain-text output. Without that call, the main agent does not get your report."

     That instruction must also tell the agent two more things. It must send its report when the report is empty. It must send a partial report when its budget is short.
4. Wait until all the agents return.
5. Merge their findings into one list without duplicates. Then continue to step 4.

### A silent partition (READ THIS BEFORE YOU DECIDE THAT THE AGENTS ARE BROKEN)

The most frequent failure mode is **an agent that goes idle with no report**. You get an idle notification with `idleReason: "available"` and nothing more. That is NOT a crash, and it is almost never an infrastructure fault. `"available"` means that the agent finished its turn cleanly. The cause is almost always this: the agent did the analysis, wrote the findings as plain text and did not call `SendMessage`. Thus the report disappeared.

When a partition goes silent:

1. **Nudge the agent with the delivery instruction, not with "print your report."** If you tell it to print again, the same failure occurs again. Send it this with `SendMessage`: "The system does not deliver your plain text. Call `SendMessage(to: \"main\", message: <findings>)` now." This gets back the work that the agent already did. Usually, the agent still has its analysis in its context.
2. **Run a controlled test before you declare a systemic failure.** Dispatch ONE trivial task, and see if it returns. If the custom agent types fail and a built-in type (`general-purpose`) succeeds, the problem is the agent definition, not the mechanism. Do this at the SECOND failure, not the fifteenth.
3. **Never decide that "the channel is broken" because of repeated identical silence.** Identical silence across many agents is evidence of a common *contract* bug, which you can fix. It is not evidence of dead infrastructure, which you cannot fix. If you think that the infrastructure is dead, you lose the full partitioned review. Then the audit goes onto a single context that cannot hold it.

Dispatch the partition again only after a nudge with explicit `SendMessage` instructions fails. Use inline analysis only after that. If you use inline analysis, say so clearly in the step 12 verdict. A pass without the full partition count is INVALID per step 8.5, and it cannot support a CLEAN verdict.

A reviewer agent can return generic boilerplate, crash, or cover fewer files than its partition list. Then dispatch that partition again with sharper instructions. If a partition does not respond, nobody audited that part of the scope.

### 3. Analyze

Examine each changed line and the context around it against all the dimensions. Do not write the dimensions that have no findings.

- **Correctness**: Off-by-one, null deref, wrong operator, inverted condition, no break/return where one is necessary, races, deadlocks, resource leaks, swallowed errors, type mismatches
- **Edge Cases**: Empty/null/zero/negative inputs, boundary values, unicode/locale/timezone, concurrency, partial failure
- **SOLID / DRY / SRP**: SRP violations, duplicated logic, modules that depend too much on each other, god objects, feature envy, premature abstraction
- **Architecture**: Does the code agree with the current design, or go against it? Layer violations, necessary abstractions that are absent, encapsulation breaks, names that give a wrong meaning
- **Security**: Injection, auth/authz gaps, secrets in code, unsafe deserialization, SSRF, insufficient input validation
- **Performance**: Hot-path allocations, O(n^2) when O(n) is possible, N+1 queries, a block on async work, unbounded growth
- **Project Rules**: Deviations from the CLAUDE.md conventions. Quote the specific rule that the code violates.
- **Runtime invariants (this repo)**: The code of the game (and the NVIDIA, CRI and Nintendo SDK code in it) is the specification. A service or device answers as the console does, and the disassembly of the SDK caller shows how (`tools/disasm.py`). Syncpoint ids come from `syncpt_alloc()` and stay below 128. Guest addresses are `u64`.

  The code gets to guest memory through `GP()`/`gmem_ptr()`/`gmem_read()`, never through a host pointer that it keeps across a remap. Data that game threads share must have a lock or be atomic, because these threads run truly in parallel on the host. Nothing from a dump goes into git. Quote the rule for each violation.
- **Prose for users (AI-isms)**: Text that a user reads must read as plain prose that a human wrote. This text is `README.md`, `docs/ROADMAP.md` and commit messages. It is also the messages that the runtime prints for players, and the comments that it writes into the `.ini` of the game. Flag these items and write them again:
  - an em-dash (`—`, or its escaped form) that splices clauses or adds an appositive
  - a semicolon that joins two independent clauses
  - a spaced hyphen (` - `) in place of a dash
  - a dramatic "Label: payload" colon for effect
  - a rule-of-three triad, and a "not just X, but Y" flourish.

  Write them again as two sentences or with a plain connector (and / with / where / so / because). Do NOT flag these items:
  - code comments
  - debug log lines (`LOGV`, and `LOG` lines for the developer, not for the player)
  - semicolons inside code in backticks, or in genuine lists that contain commas
  - real colons after a field label (also Keep-a-Changelog `**Term**:` lead-ins)
  - a literal typographic separator between two nouns (for example, `%1 — %2`, or `Settings → X` breadcrumbs).

  The severity is LOW (NIT for a lone separator). If the project CLAUDE.md has a `"Text for users"` / plain-prose rule, a violation is a Project Rules finding. Quote the rule.
- **Refactor completeness**: A finding can have the shape "X should now use Y". Examples are a new accessor, a renamed API or an extracted helper. For such a finding, grep the FULL repository (not only the partition) for each use of the old pattern that stays. List each site that you find. Fix it, or mark it out-of-scope with a reason. A refactor finding that does not list each old-pattern site is incomplete.

  Use `ast-grep` for code patterns. For example, use `ast-grep --pattern 'g_ch_syncpt_next' --lang c` after the syncpoints moved to `syncpt_alloc()`. Use plain `grep` for substrings. The AST search does not match in unrelated tokens or comments.
- **Comment-code synchronization**: A comment can name a quantity (`192 syncpoints`, `stage slots: 0 VertexA, 1 VertexB`), a function (`see shader_merge_dual`) or a list (`4 Initialize, 6 SetAndWait, 7 Get`). Verify each such claim against the current code. For a numeric count, count the items that the comment describes, one by one. For a named function, make sure that the name exists with `grep -rnw 'FunctionName' src` or `ast-grep --pattern 'FunctionName($$$)' --lang c`. Stale counts and method references to names that do not exist are real LOW findings. They collect silently and give wrong information to future readers.
- **Defensive-code pair audit**:
  - A runtime guard that only LOGS (`LOG`, `WARN`, `fprintf(stderr, ...)`) must also `return`, or stop the downstream code in a different way. The downstream code must not run with the bad state. A guard that only logs is a guard that does not guard.
  - A service answer that reports a failure (a nonzero result) must leave the out-parameters as the console does. The SDK often reads them all the same. Check the caller.
  - A path that takes a lock (`pm_lock`) must release it at each exit of that path. This includes early returns inside `switch` cases.
- **Side-effect completeness**: Code can change state that a different stage uses. Then verify that the hand-off occurs. These are the hand-offs:
  - A syncpoint increment gets to its waiters through `syncpt_incr`/`syncpt_add`, which wake `syncpt_wait` and the nvhost events.
  - A holder of `vk_lock` uses `syncpt_add_quiet`. The outermost `vk_unlock` of the thread signals its events after the lock goes (`vk_release_events`, `syncpt_events`). A signal under `vk_lock` takes the lock of the kernel. That deadlocks against a thread that stops on a trap on GPU-owned memory. Thus do not change a quiet increment back into `syncpt_add`.
  - A kernel event goes through `kevent_signal`.
  - GPU writes to guest memory go through the write-back paths of the Vulkan renderer (render targets in `gpu/vk/surface.c`, compute results in `gpu/vk/compute.c`, DMA copies).
  - Released audio buffers go through the release event that the game waits on.

  A change that gets to a buffer but never gets to its consumer is invisible, until a different event flushes it by chance. That is a real correctness bug.

### 4. Report Findings

**Keep this short. Do NOT write the full changelog table in the intermediate passes. Keep the detailed changelog for the final report (step 12).** In each pass, write only a short numbered list of findings, as in this example:

```
Pass N findings:
1. [CRITICAL] `file.ext:NN` — brief description (AUTO)
2. [HIGH] `file.ext:NN` — brief description (AUTO)
3. [MEDIUM] `file.ext:NN` — brief description (AUTO)
4. [LOW] `file.ext:NN` — brief description (AUTO)
5. [NIT] `file.ext:NN` — brief description (AUTO)
```

Severity levels:

- **CRITICAL**: Data loss, security breach, or production crash.
- **HIGH**: A probable bug or a significant design flaw.
- **MEDIUM**: Code smell, maintainability concern, or moderate risk.
- **LOW**: A minor issue of style, names or conventions.
- **NIT**: Purely stylistic.

### 5. Fix ALL Findings

> **This step is PHASE B.** See "PHASE SPLIT: AUDIT, THEN REMEDIATE" below. Audit passes are read-only. Nothing in this step runs before two conditions are true: Phase A closed, and the tree is still byte-identical to the recorded `baseline`. If you are in the middle of the audit, do not start to fix.

**Fix each finding at each severity level. Do not ask permission. Do not skip LOW or NIT.**

**You must not descope a finding from THIS pass.** You can descope only a carry-over: a finding from an earlier pass that a reviewer flags again. Even then, obey the rules of step 11, and write the reason into `audit-state.json`. Some agents decide that a fresh finding is `"out of scope,"`, `"pre-existing,"`, `"shared with other code,"`, `"riskier than it's worth,"` or `"better as a follow-up"`. That is not a descope. It is a skipped finding, and then the CLEAN verdict is false.

Refuse these two specific dodges:

- **`"Pre-existing, not introduced by this PR."`** This is not relevant. The skill audits the files in the scope, not the diff. If a bug is live in a file that you audit, it is a finding.
- **"The correct fix is too structural / touches too much."** The rule "Architecturally correct, always" is for this case. Sometimes the correct fix is genuinely larger than the audit can land. That is one of the rare NEEDS USER INPUT cases. Raise it as one, and continue the loop. It is not a silent drop.

A finding can give two legitimate remedies (the finding says "either X or document Y"). Then to pick one IS to fix the finding. Say which one you picked, and why.

**Fix in priority order:** CRITICAL first, then HIGH, MEDIUM, LOW, NIT. A fix of a higher severity can make a finding of a lower severity obsolete. It can also change the correct fix for that finding.

- **AUTO**: The correct fix is clear. Apply it.
- **NEEDS USER INPUT**: It needs a design decision. Ask the user, wait, then apply the fix.

**Before you change a function signature, a return type or a public API:** use Grep to find ALL the call sites, consumers and references. Update each of them. Do not trust the build to find callers that you missed. Some can be in dynamic code, templates or test files that compile with stale signatures.

#### VERIFY BEFORE WRITE (MANDATORY)

**Never write a call to an API if you did not read its declaration in this session.** Do not trust your memory, and do not think `"it's obviously named that"`. Read the declaration.

An edit can call a function, method, constant, enumerator, log category or CMake function that you did not open in this session. Before such an edit, Grep or Read its declaration. One command is sufficient:

```
grep -rnw 'syncpt_alloc' src                        # does this function exist?
grep -nE '^[A-Za-z_].*\(' src/nx/hle/kernel/ipc.h   # a module's API surface is its header
```

Then check the SEMANTICS, not only how you spell the name. For example, in a `.swipc` file, buffer attribute 5 and 0x21 both declare an input buffer. But 0x21 (AutoSelect) also takes the pointer (X) buffer that the SDK uses for small inputs. If you pick the wrong one, the code compiles, but each request then fails with InvalidCmifRequest (`[bad request]` in the log). The cause is that the dispatcher counts an AutoSelect buffer in both of its lists.

This rule exists because this is the most frequent way that this skill makes broken code. A name can look correct but not exist, and you find this only after a full rebuild cycle. A full rebuild here takes minutes, and the grep takes two seconds.

**Compile-gate in small batches.** Build after approximately every 5 edits, not every 15. If a 15-edit batch fails, you cannot find the edit that caused the failure without a bisection. Also, a long rebuild tempts you to add more edits while it runs. That is how "green" claims drift ahead of reality.

#### VERIFY THE MECHANISM, NOT THE STORY (MANDATORY)

VERIFY BEFORE WRITE prevents a call to an API that does not exist. This rule prevents a call to an API that exists but does something *different from what the finding assumed*. That failure mode makes fixes that are strictly worse than the bug. Such fixes pass both the compiler and the test suite.

**The causal story of a finding is a HYPOTHESIS until you read the mechanism yourself.** This applies with full force to findings from your own reviewer agents. A specialist can write `"the root cause is X, fix it by calling Y"`. That gives you a lead, not a verified diagnosis. Reviewers read, but they do not run code. Confidence in their prose is not evidence.

An edit can be correct only if a callee *does* a specific thing. Before such an edit, you have three obligations:

1. **Read the body of the callee, not only its signature**, when the fix relies on how it touches shared state. Examples are the order of writes, what it copies and what it moves, what it clears and what it leaves behind. A name that sounds like the operation that you want is not a contract.
2. **Trace one full real-world cycle**, not one call. The frame loop, the loop of a game thread, a GPU submit, an audio buffer cycle or a retry can drive the operation. Then follow it through the *repeat*: the second call, retry N, the next frame, the next tick. Fixes that are correct for exactly one call are a frequent shape here.
3. **Ask what the next actor does with the state that you set.** If you set a flag on this tick, something reads it on the next tick. Find that reader before you change the writer.

**Your tests are not independent evidence if you wrote them from the same model as the fix.** If the fix assumes one call, a test with one call confirms the assumption, not the behaviour. When a fix depends on a repeat, the test must drive the repeat. When it depends on an edge, the test must cross that edge. Examples of edges are a second movie, a scene change and a save that an earlier run wrote. A green suite on the premises of the fix tells you nothing about the premise.

Real examples from this repository:

- A change moved the host1x channels from syncpoint 200 to 150. The first VIC job crashed at 200, and with 150 the movie played. But the table that NvRmStream indexes had 128 entries. Thus 150 wrote past the table into the heap of the game on each video frame. This showed only later, as crashes that looked unrelated. A read of `NvRmStreamInit` showed the size.
- An intermittent crash looked fixed after seven clean runs. In the next session, it crashed in four of six runs. One clean run, or a small number of clean runs, is not evidence for a race.

If you cannot afford to read the mechanism, you cannot afford to make the edit. Downgrade the finding to NEEDS USER INPUT. Do not guess.

List each fix: `file:line` — what changed.

### 6. Build Verification

Build, and run the tests with `ctest --test-dir build`. The tests include the generator, the fixtures of the services and of the filesystem, the differential tests of the recompiler, and more. Run the game through the scenes that the changes affect (the `snx-build` and `snx-run` skills). If one of these fails, each error has CRITICAL severity. Fix it and build again. Do not continue until all of them are green.

```bash
cmake --preset default -B build && cmake --build build
ctest --test-dir build
tools/run_game.py <id> --runs 3 --dump work/<Game>
```

- The runtime builds with the default warnings of Clang. Only `missing-prototypes` and `missing-variable-declarations` make the build fail (the tests build with `-Wall -Wextra -Werror`). Thus a runtime build that looks clean tells you little. Build each changed file one time with more warnings (its line from `build/compile_commands.json`, with `-Wall -Wextra -fsyntax-only`). Make sure that none of the warnings comes from the change.
- Run a fix for a crash or a race until the evidence is statistical. Put the crash rate before and after the fix, with the run counts, in the commit message.
- A memory-safety fix also gets an AddressSanitizer build and a run. The runtime links as C++ (VMA). Thus the flag goes on the C, C++ and link lines. The build stays out of `games/`: `cmake --preset default -B build/asan -DSNX_DEPLOY=OFF -DCMAKE_C_FLAGS=-fsanitize=address -DCMAKE_CXX_FLAGS=-fsanitize=address -DCMAKE_EXE_LINKER_FLAGS=-fsanitize=address && cmake --build build/asan`. Then, from `games/<id>/`, run `../../build/asan/scarletnx --game=<id> --seconds=60`.
- Recompile the game module (`build/scarletnx -r work/<Game>`) only when one of these items changed:
  - `src/common/cpu/recompiler/` (codegen and the LLVM backend)
  - `src/common/cpu/aarch64/` (the decoder and the ABI)
  - `src/nx/loader/`
  - the flags of the module in `src/nx/runtime/driver/toolchain.c`.

### 7. Diff Review Before Commit

Run `git diff`, and review the full diff of all the changes that you will commit. Look for these problems:

- Unintended changes (accidental whitespace, stray edits outside the audit scope)
- Debug lines or temporary code that must not go into the commit
- Edits that drifted from the intended fix
- Changes to files outside the audit scope

If something looks wrong, fix it before you continue.

### 8. Commit & Push (PR/branch scopes only)

For a PR or branch scope, stage the changes and commit them. The subject says what the pass fixed, in the form of the repository. This form (CLAUDE.md) is a bracketed area prefix, `[hle]`, then an imperative sentence. Then push. Never force-push a pushed branch.
For an uncommitted local scope, skip this step, and leave the fixes uncommitted.

#### VERIFY THE MESSAGE AGAINST THE DIFF (MANDATORY)

**Before you commit, grep the staged diff for each claim in the commit message.** A commit message is a factual statement about the contents of the commit. If you write it from your intent, and not from the diff, you put a false record in permanent history. That is worse than any bug that the audit fixes. A bug is visible in the code, but a false message actively misleads the next reader.

Confirm each substantive claim:

```
git diff --cached -- <file> | grep -F '<the changed line>'   # is the change actually staged?
git diff --cached --stat                                     # do the touched files match the story?
```

If you cannot find a claim in the diff, delete it from the message, or fix the code, before you commit. Both are correct. Do not ship the claim.

This rule exists because a message from your intent describes the fix that you meant. The diff is the fix that you made.

**Commit at the end of the Phase B remediation and at the end of each confirmation round.** Do it as soon as the build and the runs are green. Phase A commits nothing, because it edits nothing. Do not start the next confirmation round with uncommitted work. Two rounds of uncommitted work with no fallback is a real failure mode, not a hypothetical one.

---

## PHASE SPLIT: AUDIT, THEN REMEDIATE (MANDATORY)

**Audit passes are READ-ONLY. All the fixes come after them, one time, against a frozen ledger.** Do not interleave the passes and the fixes.

The audit runs in two phases with a hard boundary:

### Phase A — AUDIT (read-only, N passes)

1. Record the baseline commit with `git rev-parse HEAD`. Write it into `audit-state.json` as `baseline`.
2. Run the partition reviewers per step 8.5. **Make no edits of any type**: no code, no comments, no tests, no CMake. Reviewers only read, grep and ast-grep. At most, they can also compile a single-file probe against one header. That is a legitimate way to find subtle guard bugs.
3. Merge the reports of each pass into ONE ranked ledger in `audit-state.json`, without duplicates, in the order CRITICAL → NIT.
4. Additional Phase A passes are for COVERAGE, not to check your own work again. A second pass exists to find what the first pass missed. The tree did not change, thus each item that it reports is a genuine miss and not fresh damage.

**Phase A ends only when a full pass adds no new findings.** There is no pass cap. If a pass finds something new, at any severity, another pass comes after it. The tree stays byte-identical to `baseline` all the time. Before you leave Phase A, verify this with `git diff --quiet`, and say so.

### Phase B — REMEDIATE (fix once, verify once)

5. Fix the ledger in severity order. Apply VERIFY BEFORE WRITE, and compile-gate in small batches.
6. Get a green build and a green `ctest`, and run the game through the scenes that the fixes affect (`snx-run`). The tests cover what they cover, and the game runs cover the rest.
7. Do a confirmation pass over the files that you changed, not the full inventory. It finds damage that the remediation itself caused. Fix what it finds, build again and run again.
8. **Confirmation rounds repeat until a round is clean.** A confirmation round can find something at HIGH or above. Then its fixes are also remediation that nobody verified, and they get their own round, with a scope of that delta. Stop only when a round returns nothing at all. There is no round cap.
9. Commit and push. Before the commit, verify the message against the diff.

### Why this is mandatory

The interleaved design has a specific pathology. **The fixes of the previous pass cause most of the findings of each pass. Thus the loop measures its own churn, and it does not converge.** In one real run, the most serious findings of pass 6 were all pass-5 regressions:

- a symlink escape that a fix of a different symlink escape caused
- a cache that latched permanently, which a fix of a redundant cache caused
- a test that became *fully* vacuous because of an assertion that the audit added to make it less vacuous.

None of those defects existed in the audited code. The audit made them.

A frozen baseline removes the feedback loop at the source. You cannot damage code that you do not edit. A reviewer that reads a tree that does not change reports real defects, not the mistakes of your last hour.

**The result for the step 11 decision:** "no new findings" in Phase A means that the audit is complete. It does not mean that you fixed the code. Do not emit a CLEAN verdict until the Phase B confirmation rounds are also green.

**The confirmation pass finds the remediation damage. Thus its yield is a measurement of the remediation, not noise.** In one real run, the first confirmation round returned six regressions that the remediation caused. One of them was a "root cause" fix that made the guard that shipped with it structurally unable to fire. The round that fixed those six caused two more.

If a confirmation round comes back heavy, the fixes came from stories, not from mechanisms. The answer is another round plus VERIFY THE MECHANISM, not a verdict.

---

## LOOP: Repeat Until Clean (no pass cap)

**In Phase A, after each audit pass, you MUST re-read and re-analyze. Do not skip this.** (With the phase split, there are no "fix passes" after which to re-analyze. The remediation is a single Phase B step with its own confirmation pass.)

### 8.5 Pass Definition (MANDATORY)

A "pass" is **a new dispatch of all the partition reviewer agents from step 2.5, in parallel**. They read each file in the original inventory fully. There are no exceptions.

**These are NOT a pass:**
- A single "verifier" or "spot-check" agent
- A subset of partitions (even if "Pass N−1 was clean for them" or "no Pass N−1 changes landed in those files")
- A grep-only verification without agent dispatch
- Analysis that you do inline yourself, and not with agents

If the original scope used 6 partitions, each pass ≥2 dispatches EXACTLY 6 agents. **Do not skip a partition** because `"it was clean last time,"`, `"Pass N−1 didn't touch those files,"` or `"I'm pretty sure nothing changed there"`. The skill keeps no state between passes, by design. A fix in a different partition can break a clean partition. That fix can change a shared header, modify an interface contract or shift call-site behaviour. You cannot exclude that if you do not read the files again.

**If you dispatch fewer agents than the established partition count from step 2.5, the pass is INVALID.** The result is not a pass, and it cannot contribute to a CLEAN verdict. Before the loop continues, it MUST dispatch the partitions that it did not dispatch. State the violation explicitly (`"Pass N was partial: dispatched A of P partitions — re-dispatching the missing P−A now"`), and continue the work.

**Anti-rationalization watch.** When you plan a pass, you can think along one of these lines. If you do, you are about to downgrade the audit, NOT optimize it:
- `"Pass N−1 was clean for partition X, skip it"`
- `"No Pass N−1 changes touched those files"`
- `"A focused verifier covers the concern"`
- `"This should be enough"`
- `"Re-running on unchanged files won't catch anything new"`
- `"I'll dispatch fewer agents to save tokens / time / context"`

Each of those is a cost-shortcut, not a value judgement. The token budget is the job of the **user** (with `+500k`-style directives), not your job. Do the full work.

**Anti-yield watch (Rule 0).** The list above is about a downgrade of a pass. This list is about the end of the loop, which is the more frequent failure. If you think one of these, you are about to violate Rule 0:
- `"I should check in before starting another pass"`
- `"The user would probably want to weigh in here"`
- `"I'll report what I have and let them decide"`
- `"This is a natural stopping point"`
- `"The turn is getting long / a lot has happened"`
- `"I'll ask whether to keep going, to be safe"`
- `"I'll note this as out of scope and mention it in the summary"`

**About "the last pass mostly found problems my own fixes caused":** with the phase split above, this cannot occur now. Phase A does not edit. If you see it, you put fixes into an audit pass. Stop, record the violation, and complete Phase A read-only.

It is still never a reason to yield. Damage that you caused is damage that ships. Thus you must fix it before the verdict in all cases. The difference is that the answer is now "go back to a frozen baseline", not "run another interleaved pass and hope it converges."

None of these is caution. In each of them, you put your own comfort in place of the termination predicate of the skill. Continue.

### 9. Fresh Read (NO EXCEPTIONS)

Use the Read tool to read **ALL the files in the original audit scope** again. Do not read only the files that you edited. A fix in file A can make assumptions in file B incorrect (callers, shared state, interface contracts). Your context is stale for each file, not only for the edited files. Call Read on each file, and look at the real contents on the disk. Do NOT rely on memory, context or edit diffs.

**Mandatory checklist output.** Each pass ≥2 must start with an explicit re-read confirmation that matches the inventory from step 1.5:

```
Re-read confirmation (Pass N):
  1. path/file1.ext ✓
  2. path/file2.ext ✓
  ...
  M. path/fileM.ext ✓
  Re-read: M/M files
```

If the count does not agree with the inventory total, the pass is invalid. Go back to step 9, and read the files that you did not read. For partitioned scopes (step 2.5), dispatch the partitioned reviewer agents again, each with its file list, for the re-analysis. Do not change a partitioned scope into single-threaded re-reads.

### 10. Re-Analyze (Full Scope, Not Just Edits)

Use ONLY the fresh file contents from step 9. Run the full step 3 analysis against **each file in the audit scope**, not only the files that you touched. Ask these questions:

- Did a fix cause a new issue in the edited file?
- Did a fix break a caller, a consumer or a sibling file that nobody edited?
- Did a fix cause a regression in a different dimension?
- Are there issues in unedited files that I missed in the first pass?
- Did I miss something earlier that I can now see with fresh eyes?

### 10.5 Dead-Code Scan

Find each public function that is new, or that has a non-trivial change, in the scope of this audit. Grep the full repository for its callers:

```bash
# Functions: find all call sites
ast-grep --pattern 'FunctionName($$$)' --lang c src
grep -rnw 'FunctionName' src tests tools scripts cmake
```

- **Zero callers** → remove the function, or document the call path that keeps it. Examples of such a path are a dispatch table such as `svc_register` and the `Renderer` table in `gpu/renderer.h`. A different example is the calls of the generated code into `src/common/cpu/aarch64/cpu_helpers.c`. A service handler has no caller in the sources. Its caller is the dispatcher that the build generates into `build/src/nx/snx_hle-swipc/` from the `.swipc`, so make sure that the command is in that dispatcher. If this audit is the first to grep for the callers of a function, nobody else verified that something uses it.
- **Only self-callers (tests + the definition site)** → flag the function as probably dead. Make sure that the test is not the only reason for the function.

This step is mandatory in each pass. Dead code collects between passes when a fix removes the last caller of a helper but not the helper.

### 11. Decision

Evaluate these items in order. This predicate is the ONLY thing that can end the loop. Your opinion of the yield, the effort that you spent and the result of the last pass cannot end it.

1. **Phase A, new findings exist** (findings that no earlier pass raised) → record them in `audit-state.json`, and run another full pass (step 8.5). In Phase A, open findings are normal. You fix them in Phase B, never during an audit pass.
2. **Phase A, a full pass added nothing new** → Phase A is over. Go to Phase B: fix the ledger (step 5), build and run (step 6), then the confirmation rounds.
2b. **Phase B, any finding in `audit-state.json` with `status: "open"`** → go back to step 5. This is not optional.
3. **Only carry-over findings persist** (the same finding, flagged again from an earlier pass) → resolve them now. Fix each one, or descope it to a tracked artifact. Examples are an issue link, a note in the PR description and a removal from the scope. Write the reason into the state file.

   The skill must NOT flag the same finding again for 3+ passes without action. File-size violations, absent test coverage and lossy collapses collect forever when an agent uses "stay in scope" as a dodge. When each carry-over is `fixed` or `descoped`, go to step 11.5.
4. **Zero findings** → go to step 11.5, then step 12.
5. **There is no pass cap.** After a pass that found something new, another full pass always comes. The loop ends only through branches 3 or 4.

**Each branch ends at step 12.** No path out of this loop skips the Final Report. If you are about to end your turn and you did not emit step 12, you violate Rule 0. Go back and finish.

**A decrease in returns is not a termination condition.** `"The last pass found little,"`, `"the remaining findings are minor,"` and `"another pass probably won't find much"` are not in the predicate above. Only the numbered conditions are in it. You can think that a pass is not worth a run. Put that argument in the step 12 verdict, AFTER the predicate says stop. Never use it as a reason to stop early.

### 11.5 Pre-Final-Report Self-Audit

Before you write the final report, answer each question explicitly:

0a. **Rule 0 audit.** Did I end a turn between step 4 and here, to ask permission, to give options, to report progress or to confirm the next pass? If yes, that was a violation. Write it clearly in the Summary of the final report, and do not hide it. The user must know that the loop did not run continuously, and why.

0b. **State-file audit.** Does `audit-state.json` contain a finding with `status: "open"`? If yes, I am not at step 11.5, and I must go back to step 5 (Phase B fixes it). Does each `descoped` entry have a `descope_reason` AND a `raised_pass` at least two passes old? A fresh finding with the mark `descoped` is a skipped finding, and the verdict cannot be CLEAN.

0. **Pass-count audit.** Count the agent dispatches for each pass N ≥ 2. Did I dispatch the SAME number of partition reviewers that step 2.5 established for Pass 1? A partial pass (fewer agents, a focused verifier, a single re-check, a grep-only walk without agents) is INVALID per step 8.5. Run the partitions that did not run, and continue the loop before you write the final report. Do NOT classify a partial pass as "clean", because a partial pass has no verdict at all.

1. Did I read each file in the inventory FULLY? (Compare the step 1.5 inventory to the real Read calls.)
2. Did I analyze each file against each step-3 dimension, and not only the dimensions where I expected findings? Did I include refactor-completeness, comment-code synchronization, the defensive-code pair audit and side-effect completeness?
3. For partitioned scopes: did each reviewer agent return concrete findings (or explicitly "none")? If an agent crashed, returned generic boilerplate or covered fewer files than its partition list, nobody audited that partition.
4. Did I assume coverage from an earlier pass, and not read the files again? (This is the anti-trust rule from step 1.)
5. Will the file counts in `Files in Scope` and `Files Fully Read` of step 12 agree? If not, I did not finish.
6. Think of each refactor-shape finding that I raised (a new accessor, a renamed API, an extracted helper). Did I `ast-grep` / `grep` the FULL repository for the old pattern? Did I fix or descope each match, and not only the matches inside my partition?
7. Think of each numeric or named claim in the comments that I edited or kept in this pass. Examples are "WHY ONLY THESE FOUR", "the other nine" and "see ::engineFor". Did I verify the claim against the current code? Stale comment counts and method references to names that do not exist in the diff are findings that I must find.
8. For each runtime guard, lock or service failure path that I touched, did I verify its pair? Asymmetric guard coverage is a real LOW (sometimes MEDIUM) finding that I must raise.
9. Think of each change to state that a different stage uses (syncpoints, kernel events, guest memory that the GPU writes, audio buffers). Did I trace forward to the hand-off? "It works because the next frame happens to flush it" is not a verification.
10. For each new public function, or each public function with a non-trivial change in this PR, did I `ast-grep` / `grep` for callers? A dead helper that a fix added is a real finding.

If an answer is "no," "skipped," "I assumed," or "partially," go back to step 9 and complete the work that remains. Go to step 12 only when each answer is "yes."

---

### 12. Final Report

```
## Code Audit — Final (Pass N)

### Summary
<2-3 sentences: what was found, what was fixed, overall quality>

### Changelog

#### Pass 1
| # | Severity | File | Finding | Fix Applied |
|---|----------|------|---------|-------------|
| 1 | CRITICAL | `path/file.ext:NN` | <what was wrong> | <what was changed — be specific: old value → new value, added/removed call, restructured logic, etc.> |
| 2 | HIGH | `path/file.ext:NN` | <what was wrong> | <specific change> |
| 3 | MEDIUM | `path/file.ext:NN` | <what was wrong> | <specific change> |
| 4 | LOW | `path/file.ext:NN` | <what was wrong> | <specific change> |
| 5 | NIT | `path/file.ext:NN` | <what was wrong> | <specific change> |

#### Pass 2 (if applicable)
| # | Severity | File | Finding | Fix Applied |
|---|----------|------|---------|-------------|
| 6 | LOW | `path/file.ext:NN` | <what was wrong> | <specific change> |

...

### Audit Summary

**IMPORTANT: These totals are CUMULATIVE across ALL passes, not just the last pass. Count every finding from every pass.**

| Metric | Value |
|---|---|
| Passes | N |
| Files in Scope | N |
| Files Fully Read | N |
| Coverage | N% |
| Files Modified | N |
| Total Findings (all passes) | N |
| CRITICAL (all passes) | N found → N fixed |
| HIGH (all passes) | N found → N fixed |
| MEDIUM (all passes) | N found → N fixed |
| LOW (all passes) | N found → N fixed |
| NIT (all passes) | N found → N fixed |
| Build | PASS |
| Verdict | CLEAN |

**Coverage rule.** Coverage = `Files Fully Read / Files in Scope × 100`. The skill cannot declare CLEAN with Coverage <100%. If Coverage <100%, the verdict header is `INCOMPLETE` (not `CLEAN`), and the verdict body must list which inventory files were skipped and explain why. Do not paper over an incomplete audit by relabeling skipped files as "out of scope" — they were already declared in scope at step 1.5.

To compute findings: go through the Changelog tables above, count every row at each severity level across all passes. The "found" and "fixed" numbers must match the total rows in the Changelog.

### Verdict
CLEAN — <one sentence rationale>
```

---

## Fix Philosophy

- **Architecturally correct, always.** Never apply a quick hack, shortcut or workaround. Each fix must be the correct solution: the change that a senior engineer makes if the code is theirs for a long time. If the correct fix is harder or touches more files, that is the fix.
- **No TODOs, no follow-ups.** Never leave `TODO`, `FIXME`, `HACK`, `XXX`, "revisit later", or a different comment that tells of future work. Never suggest a follow-up task. After the audit, the code must have zero open action items.
- **Solve the root cause.** If a finding is a symptom, fix the problem that causes it. Do not patch symptoms.

## Guidelines

- **Be direct.** No praise sandwiches.
- **Be concrete.** Each finding must cite a file and a line.
- **Be proportional.** Scale the depth to the size and risk of the change.
- **Do not invent problems.** If the code is solid, say so.
- **Respect project style.** Flag CLAUDE.md deviations, not personal preferences.
- **Read before you judge.** A "bug" in the diff can be correct in its context.
- **Fix confidently.** Do not ask permission for obvious corrections.
- **Minimize disruption.** Make only surgical fixes. Do not refactor the code around a fix unless that is necessary to resolve a finding.
- **Stay in scope, but not as a dodge.** Analyze the changed code and its immediate context (callers, callees, shared state). Do not expand the audit to the full codebase. BUT: a finding can come up in 2+ earlier passes, and each time the agent postpones it as "out of scope".

  That pattern is itself a finding. Fix it in this pass, or descope it to a tracked artifact (an issue link or a PR description note). Then it does not appear again. "Carry-over scope" is not a permanent exemption.

  **This guideline limits where you LOOK, never if you fix what you found.** Read it with step 5, which forbids a descope of a finding from the current pass. If you use "stay in scope" to drop a fresh finding, you go against the intent of this line.
- **Read scope ≠ grep scope.** The audit scope limits your reads. Your grep and ast-grep searches cover the full repository when a finding needs a list of call sites, old-pattern remnants or stale comment references.
