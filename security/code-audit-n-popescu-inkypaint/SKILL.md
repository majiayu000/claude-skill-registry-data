---
name: code-audit
description: "Audits uncommitted changes, branches, or PRs for bugs, edge cases, SOLID/DRY/SRP, architecture, security, performance, and CLAUDE.md violations — then automatically fixes ALL issues and re-audits in a loop until clean. Use when: audit, review, code review, review this PR, check code, look over this, inspect code, or any variation."
---

# Code Audit

**This skill is a LOOP in two phases (see "PHASE SPLIT" below). Phase A audits read-only, pass after pass, until a full pass adds no new findings. Phase B then fixes ALL findings (every severity) once, re-reads from disk, and runs confirmation rounds until one comes back clean. Stopping after one pass, or fixing during Phase A, is a failure to follow instructions.**

---

## RULE 0: DO NOT YIELD (BINDING, read this before anything else)

Once the loop starts, **ending your turn before step 12 is a violation.** Not a judgement call, not a courtesy — a violation, in the same category as skipping a file.

The loop terminates in exactly one way: you reach step 11, its predicate says stop, and you emit the step 12 Final Report. Until that happens you keep working, in the same turn, without checking in.

**These are all violations. Every one of them ends your turn:**

| What it looks like | Why it feels justified | What it is |
|---|---|---|
| "Which would you like: (1) continue, (2) fix first, (3) something else?" | offering control | abandoning the loop |
| "Want me to run Pass 3?" | confirming before cost | the loop already answered this |
| "Here's what I found so far — let me know how to proceed." | transparency | a status report nobody asked for |
| "Pass 2 is done. Say the word and I'll continue." | politeness | waiting for permission you have |
| "Given the yield was thin, I'd expect diminishing returns — your call." | good judgement | substituting your stopping rule for the skill's |
| Stopping because the turn is long / context is large / a lot happened | prudence | a cost-shortcut, and cost is not your call |

**You already have permission for the whole loop.** Invoking the skill IS the authorization for every pass, every fix, every re-dispatch, up to the step 11 termination predicate. Asking again is not caution; it is failing to follow the instruction you were given.

**The one exception:** a genuine blocker that makes forward progress impossible — a build that cannot be fixed from inside the audit, a credential prompt, a destructive action outside audit scope, or a step-5 finding explicitly marked NEEDS USER INPUT. "This is a lot of work," "I'm unsure whether to continue," and "the user might want to weigh in" are NOT blockers.

**Standing vs one-time instructions.** The loop is a STANDING instruction: it stays in force until step 12 without renewal. A user message like "commit and push" is a ONE-TIME instruction about the current state; it does not become standing permission. Treating these backwards — re-asking for the standing one, generalising the one-time one — is a specific known failure of this skill. Do not.

## Usage

```
/code-audit <scope>
```

**Examples:**

- `/code-audit` — audit uncommitted changes (default)
- `/code-audit branch` — audit current branch vs main
- `/code-audit staged` — audit staged changes only
- `/code-audit PR` or `/code-audit PR #123` — audit a pull request
- `/code-audit src/nx/gpu/video/nvdec.c src/nx/hle/services/nvdrv.c` — audit specific files

If `<scope>` is provided, use it directly — do not ask the user to clarify. If omitted, default to uncommitted changes.

**Scope is immutable.** `/code-audit PR #N` and `/code-audit branch` audit the FULL declared scope. You may NOT narrow to "changed since last audit," "recent commits," "since pass N," or "files I haven't already reviewed." Prior audit history (other passes, other commits, review comments saying "reviewed") does NOT reduce coverage on the current run. The skill is stateless with respect to previous runs — every invocation re-audits the entire declared scope from scratch.

---

## Steps

### 1. Determine Scope

Use the argument passed to `/code-audit` if provided. Otherwise infer from context or default to uncommitted:

| Scope                     | Diff source                                     |
| ------------------------- | ----------------------------------------------- |
| **Uncommitted** (default) | `git diff` + `git diff --cached` + `git status` |
| **Staged only**           | `git diff --cached`                             |
| **Branch vs base**        | `git diff main...HEAD`                          |
| **Pull request**          | `gh pr diff <number>` or `gh pr diff`           |
| **Specific files**        | Read named files directly                       |

For each file in scope, read it FULLY. Files >800 lines must be read in chunks (using Read tool offset/limit parameters) until 100% of the file has been covered. Diffs alone are insufficient. Partial reads ("changed functions plus context") are forbidden — they cause cross-file inconsistencies, architectural drift, and pattern violations to be missed entirely.

### 1.5 File Inventory

Before analysis, enumerate every file in scope and produce a numbered checklist:

1. Run the appropriate diff command from step 1 to extract the file list.
2. For each file, get its line count (`wc -l <file>` for existing files; new files in the diff start at 0 and have their final size after the patch).
3. Output the inventory as a numbered list:

```
File Inventory (N files in scope):
  1. path/file1.ext (NNN lines)
  2. path/file2.ext (NNN lines)
  ...
  N. path/fileN.ext (NNN lines)
Total: N files, M lines.
```

### 1.6 Audit State File (BINDING)

Write `.claude/audit-state.json` (relative to the repo root / cwd — this exact path, so the Stop hook can find it) immediately after the inventory, and **update it at the end of every pass, before step 9**:

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

**`phase`** (`"A"` or `"B"`, default `"A"`). Set it to `"B"` in the same action that ends Phase A (step 11's decision to remediate). The Stop hook (`.claude/settings.json`) reads it to tell you which phase's work to resume.

**`awaiting_agents`** (optional, default false). Set it `true` in the same action that dispatches a pass's partition reviewers, and back to `false` the moment their reports land. Dispatched subagents report by task-notification, which mechanically requires the turn to end — that is not a yield, and the Stop hook lets it through when this flag is set. It is NOT a general escape: with the flag absent or false, a turn ending mid-loop is still blocked. Setting it while no agents are actually in flight is the same falsification as setting `complete: true` early.

`complete` stays `false` for the whole loop. Set it to `true` **only** as the last action of step 12, after the Final Report is written. A **`Stop` hook reads this file and refuses to let your turn end while `complete` is `false`** — so if you try to yield mid-loop, you will be handed back control with an instruction to continue. Do not set `complete: true` to escape the loop; that is falsifying the audit. The only legitimate ways out are the step 11 predicate and a genuine blocker (Rule 0's exception), and a blocker still requires emitting step 12 with the verdict explaining what stopped you.

`status` is one of `open` | `fixed` | `descoped`. `descoped` additionally requires `"descope_reason"` and `"raised_pass"` ≥ 2 passes earlier (see step 5).

This exists because your memory of the loop decays as context fills, and the decay is silent. The file is the authority, not your recollection:

- **"Am I done?" is a QUERY, not a judgement.** Any finding with `status: "open"` means the answer is no. Re-read the file at the start of every pass rather than recalling state.
- **It makes silent descoping impossible.** A finding you quietly stopped working on sits in the file as `open` and blocks the CLEAN verdict.
- **It survives context loss.** If the conversation is summarised mid-loop, this file tells you exactly where you are.

At the start of every pass ≥ 2, re-read it and echo one line before doing anything else:

```
LOOP STATE: pass N (no cap: until a pass finds nothing new) · P partitions · X findings open · next: step 9 fresh read · DO NOT YIELD (Rule 0)
```

This list is the coverage checklist for steps 9 and 12. Every file here MUST be read fully and analyzed. Skipping any file is a skill failure.

### 2. Read Project Rules

Read `CLAUDE.md` and any files it references. Skip if none exists.

### 2.25 Tooling: ast-grep + grep

The audit uses two complementary search tools. **Prefer ast-grep for code; use plain grep for text and comments.**

`ast-grep` matches the parse tree, so it ignores hits inside strings, comments, and tokens that happen to spell the pattern. Use it whenever the pattern is a code shape (function call, declaration, control-flow construct). `grep` works on text — use it for comments, docstrings, error messages, and exact string literals.

Common audit-time patterns in this repo (C runtime and recompiler, Python tools):

| Goal | Command |
|---|---|
| Find every caller of a function (catch dead code) | `ast-grep --pattern 'FunctionName($$$)' --lang c src` and `grep -rnw 'FunctionName' src tests tools scripts cmake` |
| Find every use of a struct field | `ast-grep --pattern '$X.field' --lang c src` and `ast-grep --pattern '$X->field' --lang c src` |
| Find every guard that only logs | `grep -rn -A2 'WARN(\|LOG(' src` and check each is followed by a `return` or other exit |
| Find a guest address squeezed into 32 bits | `ast-grep --pattern '(u32)$X' --lang c src`, then check whether `$X` is a guest address or pointer |
| Find every syncpoint id not from `syncpt_alloc()` | `grep -rn 'syncpt' src/nx/gpu src/nx/hle/services/nvdrv.c` |
| Find every service command a file answers | `grep -n '^ *\(@[a-z]* \)*\[[0-9]*\]' src/nx/hle/services/am.swipc` (or the service's `.swipc`), and the handler `nn_..._Command` in its C file (each answer must match what the SDK caller reads, see the `snx-service` skill) |
| Find every TODO/FIXME/HACK marker | `grep -rn 'TODO\|FIXME\|HACK\|XXX' src tests tools scripts cmake` |
| Find a stale comment claim (e.g. "below 192") | `grep -rn "below 192" src` |
| Find AI-ism punctuation in user-facing text | `grep -rn '—' README.md docs/ROADMAP.md <changed user-facing files>`; then check for clause-joining `;` and stand-in ` - ` (exclude code comments and backticked code) |

Don't memorise the list — the principle is: **if a finding is "this pattern is used at site A, but should also be checked at sites B…N", you have a grep/ast-grep step to take before you finish the finding.** Reporting a refactor-completeness finding without having enumerated the matches is incomplete.

### 2.5 Parallel Reviewer Decision

Compute scope size from the inventory:

- **≤10 files AND ≤2000 lines changed**: single-threaded analysis — you do step 3 directly.
- **>10 files OR >2000 lines changed**: MUST partition into domain-specialist reviewer agents. Single-threaded analysis on a large scope is a skill failure — no single context window can hold deep analysis of 50+ files.

For partitioned scopes:

1. Group files by coherent domain (kernel and services, GPU and shaders, audio and video, platform backends, the recompiler and its ABI, build and scripts). 4-6 partitions is typical; aim for ≤15 files per partition.
2. **Reviewer selection.** Check the available agent types for project-defined domain reviewers (in this repo, the `snx-*-reviewer` agents in `.claude/agents/review/`; each one's description names the directories/domains it covers). If any exist, partition boundaries SHOULD follow the specialists' domains, and each partition MUST be dispatched to the specialist whose description matches it — a specialist encodes stack expertise and past-bug patterns a generic reviewer lacks. Only for a partition no specialist covers (or when a project defines none) fall back to `subagent_type=general-purpose`. Dispatch ONE `Agent` call per partition; all Agent calls go in a SINGLE message so they run in parallel.
3. Each agent prompt MUST include:
   - The exact file paths in its partition (explicit paths, not a directory glob).
   - Instructions to read every file FULLY (no partial reads, no diff-only).
   - The full step 3 analysis dimensions, listed verbatim — including refactor-completeness, comment-code synchronization, defensive-code pair audit, and side-effect completeness.
   - The project rules from `CLAUDE.md` (quoted relevant sections, not "see the file").
   - **Grep scope ≠ read scope.** The agent's *read* scope is limited to its partition files, but its *grep / ast-grep* scope is the WHOLE repo. Specifically the agent MUST grep beyond its partition for: (a) any old-pattern remnant of a refactor it's verifying ("X should now use Y" → enumerate all remaining X uses), (b) callers of any public function its partition touches, (c) comments naming a count or method/class it can verify. The partition limits where the agent reads files fully, not where it searches.
   - A request for prioritized findings in the format: `file:line — description — suggested fix — severity`.
   - **An explicit delivery instruction.** A dispatched agent's plain-text output is NOT returned to you — it runs as a background teammate, and text it merely prints goes nowhere. Every prompt MUST end with: "When done, call the `SendMessage` tool with `to: \"main\"` and your full findings as `message`. Your plain-text output is not delivered; without that call your report is lost." Send-even-if-empty and send-partial-if-short-on-budget belong in that instruction too.
4. Wait for all agents to return.
5. Aggregate their findings into a single deduplicated list, then continue to step 4.

### Diagnosing a silent partition (READ THIS BEFORE CONCLUDING THE AGENTS ARE BROKEN)

The dominant failure mode is **an agent going idle with no report** — you receive an idle notification with `idleReason: "available"` and nothing else. That is NOT a crash, and it is almost never an infrastructure fault. `"available"` means the agent finished its turn cleanly. The overwhelmingly likely cause is that it did the analysis, wrote the findings as plain text, and never called `SendMessage` — so the report evaporated.

When a partition goes silent:

1. **Nudge with the delivery instruction, not "print your report."** Telling it to print again reproduces the failure. `SendMessage` it: "Your plain text is not delivered. Call `SendMessage(to: \"main\", message: <findings>)` now." This recovers the work already done — the agent usually still has its analysis in context.
2. **Run a controlled test before declaring systemic failure.** Dispatch ONE trivial task and see if it returns. If custom agent types fail and a built-in (`general-purpose`) succeeds, the problem is the agent definition, not the mechanism. Do this on the SECOND failure, not the fifteenth.
3. **Never conclude "the channel is broken" from repeated identical silence.** Identical silence across many agents is evidence of a common *contract* bug, which is fixable, not of dead infrastructure, which is not. Assuming the latter costs the entire partitioned review and pushes the audit onto a single context that cannot hold it.

Only after a nudge with explicit `SendMessage` instructions fails should you re-dispatch, and only after that should you fall back to inline analysis. If you do fall back, say so plainly in the step 12 verdict: passes without the full partition count are INVALID per step 8.5 and cannot support a CLEAN verdict.

If a reviewer agent returns generic boilerplate, crashes, or covers fewer files than its partition listed, re-dispatch that partition with sharper instructions. A non-responsive partition means that part of the scope wasn't audited.

### 3. Analyze

Examine every changed line and surrounding context against all dimensions. Omit dimensions with no findings.

- **Correctness**: Off-by-one, null deref, wrong operator, inverted condition, missing break/return, races, deadlocks, resource leaks, swallowed errors, type mismatches
- **Edge Cases**: Empty/null/zero/negative inputs, boundary values, unicode/locale/timezone, concurrency, partial failure
- **SOLID / DRY / SRP**: SRP violations, duplicated logic, tight coupling, god objects, feature envy, premature abstraction
- **Architecture**: Fits or fights existing design, layering violations, missing abstractions, encapsulation breaks, misleading names
- **Security**: Injection, auth/authz gaps, secrets in code, unsafe deserialization, SSRF, insufficient input validation
- **Performance**: Hot-path allocations, O(n^2) when O(n) possible, N+1 queries, blocking on async, unbounded growth
- **Project Rules**: Deviations from CLAUDE.md conventions — quote the specific rule violated
- **Runtime invariants (this repo)**: The game's own code (and the NVIDIA, CRI and Nintendo SDK code inside it) is the specification: a service or device answers the way the console does, which the SDK caller's disassembly shows (`tools/disasm.py`). Syncpoint ids come from `syncpt_alloc()` and stay below 128. Guest addresses are `u64`, and guest memory is reached through `GP()`/`gmem_ptr()`/`gmem_read()`, never a host pointer kept across a remap. Anything shared between game threads (which run truly parallel on the host) is locked or atomic. Nothing from a dump goes into git. Quote the rule for each violation.
- **User-facing prose (AI-isms)**: Text a user reads — `README.md`, `docs/ROADMAP.md`, commit messages, messages the runtime prints for players, and the comments it writes into the game's `.ini` — must read as plain, human-written prose. Flag and rewrite: em-dash (`—`, or its escaped form) used to splice clauses or tack on an appositive; semicolons joining two independent clauses; a spaced hyphen (` - `) standing in for a dash; dramatic "Label: payload" colons used for effect; rule-of-three triads and "not just X, but Y" flourishes. Rewrite as two sentences or a plain connector (and / with / where / so / because). Do NOT flag: code comments, debug log lines (`LOGV`, and `LOG` lines meant for the developer rather than the player), semicolons inside backticked code or genuine comma-bearing lists, real field-label colons (incl. Keep-a-Changelog `**Term**:` lead-ins), or a literal typographic separator between two nouns (e.g. `%1 — %2`, `Settings → X` breadcrumbs). Severity LOW (NIT for a lone separator). If the project CLAUDE.md has a "user-facing text" / plain-prose rule, treat a violation as a Project Rules finding and quote it.
- **Refactor completeness**: For any finding of the shape "X should now use Y" (an accessor was introduced, an API was renamed, a helper was extracted), grep the WHOLE repo (not just the partition) for every remaining use of the old pattern. List every site found and either fix it or mark it out-of-scope with a reason. A refactor finding that doesn't enumerate every old-pattern site is incomplete. Use `ast-grep` for code patterns (e.g. `ast-grep --pattern 'g_ch_syncpt_next' --lang c` after syncpoints moved to `syncpt_alloc()`) and plain `grep` for substrings — the AST search avoids matching in unrelated tokens or comments.
- **Comment-code synchronization**: For every comment that names a quantity ("192 syncpoints", "stage slots: 0 VertexA, 1 VertexB"), a function (`see shader_merge_dual`), or a list ("4 Initialize, 6 SetAndWait, 7 Get"), verify the claim against current code. Numeric counts: literally count the items the comment describes. Named functions: `grep -rnw 'FunctionName' src` or `ast-grep --pattern 'FunctionName($$$)' --lang c` to confirm the name exists. Stale counts and dangling method references are real LOW findings — they accumulate silently and mislead future readers.
- **Defensive-code pair audit**:
  - Every runtime guard that only LOGS (`LOG`, `WARN`, `fprintf(stderr, ...)`) must also `return` or otherwise stop the downstream code from running with the bad state. A guard that only logs is a guard that doesn't guard.
  - A service answer that reports failure (a nonzero result) must leave the out-parameters the way the console does: the SDK often reads them anyway. Check the caller.
  - Every lock taken on a path (`pm_lock`) is released on every exit of that path, including early returns inside `switch` cases.
- **Side-effect completeness**: When code changes state that another stage consumes, verify the hand-off happens. A syncpoint increment reaches waiters through `syncpt_incr`/`syncpt_add` (which wake `syncpt_wait` and the nvhost events), or, from a holder of `vk_lock`, through `syncpt_add_quiet`, whose events the thread's outermost `vk_unlock` signals after the lock goes (`vk_release_events`, `syncpt_events`): signaling under `vk_lock` takes the kernel's lock, which deadlocks against a thread trapped on GPU-owned memory, so do not turn a quiet increment back into `syncpt_add`, a kernel event through `kevent_signal`, GPU writes to guest memory through the Vulkan renderer's write-back paths (render targets in `gpu/vk/surface.c`, compute results in `gpu/vk/compute.c`, DMA copies), and released audio buffers through the release event the game waits on. A change that lands in a buffer but never reaches its consumer is invisible until something else happens to flush it — a real correctness bug.

### 4. Report Findings

**Keep this brief — do NOT output the full changelog table during intermediate passes. Save the detailed changelog for the final report (step 12).** During each pass, just output a short numbered list of findings like:

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
- **HIGH**: Likely bug or significant design flaw.
- **MEDIUM**: Code smell, maintainability concern, or moderate risk.
- **LOW**: Minor style/naming/convention issue.
- **NIT**: Purely stylistic.

### 5. Fix ALL Findings

> **This step is PHASE B.** See "PHASE SPLIT: AUDIT, THEN REMEDIATE" below. Audit passes are read-only; nothing in this step runs until Phase A has closed and the tree is still byte-identical to the recorded `baseline`. If you are mid-audit, do not start fixing.

**Fix every finding at every severity level. Do not ask permission. Do not skip LOW or NIT.**

**A finding raised in THIS pass may not be descoped.** Descoping is available only for a carry-over — a finding raised in an earlier pass and re-flagged — and only per step 11's rules, with the reason written into `audit-state.json`. Deciding a fresh finding is "out of scope," "pre-existing," "shared with other code," "riskier than it's worth," or "better as a follow-up" is not a descope; it is skipping a finding, and the CLEAN verdict is then false.

Two specific dodges to refuse:

- **"Pre-existing, not introduced by this PR."** Irrelevant. The skill audits the files in scope, not the diff. If a bug is live in a file you are auditing, it is a finding.
- **"The correct fix is too structural / touches too much."** That is what "Architecturally correct, always" is for. If the proper fix is genuinely larger than the audit can land, that is one of the rare NEEDS USER INPUT cases — raise it as such and keep looping. It is not a silent drop.

When a finding offers two legitimate remedies (the finding itself says "either X or document Y"), picking one IS fixing it. Say which you picked and why.

**Fix in priority order:** CRITICAL first, then HIGH, MEDIUM, LOW, NIT. A higher-severity fix may make a lower-severity finding obsolete or change what the correct fix is.

- **AUTO**: Correct fix is unambiguous — apply it.
- **NEEDS USER INPUT**: Requires a design decision — ask the user, wait, then apply.

**Before changing any function signature, return type, or public API:** use Grep to find ALL call sites, consumers, and references. Update every one of them. Do not rely on the build to catch missed callers — some may be in dynamic code, templates, or test files that survive compilation with stale signatures.

#### VERIFY BEFORE WRITE (BINDING)

**Never write a call to an API you have not read the declaration of in this session.** Not "recall", not "it's obviously named that" — read it.

Before an edit that calls a function, method, constant, enumerator, logging category, or CMake function you have not already opened here, Grep or Read its declaration first. One command:

```
grep -rnw 'syncpt_alloc' src                        # does this function exist?
grep -nE '^[A-Za-z_].*\(' src/nx/hle/kernel/ipc.h   # a module's API surface is its header
```

Then check the SEMANTICS, not just the spelling: in a `.swipc` file, buffer attribute 5 and 0x21 both declare an input buffer, but 0x21 (AutoSelect) also takes the pointer (X) buffer the SDK uses for small inputs. Picking the wrong one compiles, and every request then fails with InvalidCmifRequest (`[bad request]` in the log), since the dispatcher counts an AutoSelect buffer in both of its lists.

This exists because it is the single most common way this skill produces broken code: a name that looks right but does not exist costs a full rebuild cycle to discover. A full rebuild here takes minutes, and the grep takes two seconds.

**Compile-gate in small batches.** Build after roughly every 5 edits, not every 15. A failure in a 15-edit batch cannot be attributed without bisecting, and a long rebuild tempts you to stack more edits while it runs — which is how "green" claims drift ahead of reality.

#### VERIFY THE MECHANISM, NOT THE STORY (BINDING)

VERIFY BEFORE WRITE stops you calling an API that does not exist. This rule stops you calling one that exists and does something *other than what the finding assumed*. That is the failure mode that produces fixes strictly worse than the bug, and it passes both the compiler and the test suite.

**A finding's causal story is a HYPOTHESIS until you have read the mechanism yourself.** This applies with full force to findings from your own reviewer agents: a specialist writing "the root cause is X, fix it by calling Y" has given you a lead, not a verified diagnosis. Reviewers read; they do not run. Confidence in their prose is not evidence.

Before an edit whose correctness depends on what a callee *does*, three obligations:

1. **Read the callee's body, not just its signature**, whenever the fix relies on how it touches shared state — order of writes, what it copies vs. moves, what it clears, what it leaves behind. A name that sounds like the operation you want is not a contract.
2. **Trace one full real-world cycle**, not one invocation. If the operation is driven by the frame loop, a game thread's loop, a GPU submit, an audio buffer cycle, or a retry, follow it through the *repeat*: second call, retry N, next frame, next tick. Fixes that are correct exactly once are a recurring shape here.
3. **Ask what the next actor does with the state you just set.** A flag you set on this tick is read by something on the next one. Find that reader before you change the writer.

**Your tests are not independent evidence when you wrote them from the same model as the fix.** If the fix assumes one invocation, a single-invocation test confirms the assumption, not the behaviour. When a fix depends on a repeat, the test must drive the repeat; when it depends on an edge (a second movie, a scene change, a save written by an earlier run), the test must cross that edge. A green suite built on the fix's own premises tells you nothing about the premise.

Real examples from this repo:

- host1x channels were moved from syncpoint 200 to 150 because the first VIC job crashed at 200 and 150 played the movie. The table NvRmStream indexes was 128 entries, so 150 wrote past it into the game's heap on every video frame, which only showed up later as unrelated-looking crashes. Reading `NvRmStreamInit` showed the size.
- An intermittent crash looked fixed after seven clean runs. The next session it crashed in four of six. One clean run, or a handful, is not evidence for a race.

If you cannot afford to read the mechanism, you cannot afford to make the edit. Downgrade the finding to NEEDS USER INPUT rather than guessing.

List each fix: `file:line` — what changed.

### 6. Build Verification

Build, run the tests (`ctest --test-dir build`: the generator, the services' and the filesystem's fixtures, the recompiler's differential tests and more), and run the game through the scenes the changes affect (`snx-build` and `snx-run` skills). If any fails, treat each error as CRITICAL, fix, rebuild. Do not proceed until all are green.

```bash
cmake --preset default -B build && cmake --build build
ctest --test-dir build
tools/run_game.py <id> --runs 3 --dump work/<Game>
```

- The runtime builds with Clang's default warnings, and only `missing-prototypes` and `missing-variable-declarations` fail the build (the tests build with `-Wall -Wextra -Werror`), so a clean-looking runtime build says little. Build a changed file once with more warnings on (its line from `build/compile_commands.json`, with `-Wall -Wextra -fsyntax-only`) and check none come from the change.
- A fix for a crash or a race is run until the evidence is statistical: the crash rate before and after, with the run counts, goes in the commit message.
- Memory-safety fixes also get an AddressSanitizer build and a run. The runtime links as C++ (VMA), so the flag goes on the C, C++ and link lines, and the build stays out of `games/`: `cmake --preset default -B build/asan -DSNX_DEPLOY=OFF -DCMAKE_C_FLAGS=-fsanitize=address -DCMAKE_CXX_FLAGS=-fsanitize=address -DCMAKE_EXE_LINKER_FLAGS=-fsanitize=address && cmake --build build/asan`, then from `games/<id>/`: `../../build/asan/scarletnx --game=<id> --seconds=60`.
- The game module only needs recompiling (`build/scarletnx -r work/<Game>`) when `src/common/cpu/recompiler/` (codegen and the LLVM backend), `src/common/cpu/aarch64/` (the decoder and the ABI), `src/nx/loader/`, or the module's flags in `src/nx/runtime/driver/toolchain.c` changed.

### 7. Diff Review Before Commit

Run `git diff` and review the full diff of everything about to be committed. Check for:

- Unintended changes (accidental whitespace, stray edits outside the audit scope)
- Debug lines or temporary code that should not be committed
- Edits that drifted from the intended fix
- Changes to files outside the audit scope

If anything looks wrong, fix it before proceeding.

### 8. Commit & Push (PR/branch scopes only)

For PR or branch scope: stage, commit with a subject that says what the pass fixed, in the repo's form (CLAUDE.md: a bracketed area prefix, `[hle]`, then an imperative sentence), and push. Never force-push a pushed branch.
For uncommitted local scope: skip — leave fixes uncommitted.

#### VERIFY THE MESSAGE AGAINST THE DIFF (BINDING)

**Every claim in the commit message must be grepped against the staged diff before committing.** A commit message is a factual assertion about what the commit contains. Writing one from your intent rather than from the diff produces a false record in permanent history, and it is worse than any bug the audit fixes — a bug is visible in the code, a false message actively misleads the next reader.

For each substantive claim, confirm it:

```
git diff --cached -- <file> | grep -F '<the changed line>'   # is the change actually staged?
git diff --cached --stat                                     # do the touched files match the story?
```

Any claim you cannot find in the diff must be deleted from the message or fixed in the code before committing. Both are fine; shipping the claim is not.

This exists because a message written from intent describes the fix you meant, and the diff is the fix you made.

**Commit at the end of Phase B's remediation and of each confirmation round, as soon as the build and the runs are green.** Phase A commits nothing (it edits nothing). Do not roll into the next confirmation round with work uncommitted: two rounds of uncommitted work with no fallback is a real failure mode, not a hypothetical one.

---

## PHASE SPLIT: AUDIT, THEN REMEDIATE (BINDING)

**Audit passes are READ-ONLY. All fixing happens afterwards, once, against a frozen ledger.** Do not interleave them.

The audit runs in two phases with a hard boundary:

### Phase A — AUDIT (read-only, N passes)

1. Record the baseline commit: `git rev-parse HEAD` → write it into `audit-state.json` as `baseline`.
2. Run the partition reviewers per step 8.5. **Make no edits of any kind** — not code, not comments, not tests, not CMake. Reviewers are read/grep/ast-grep only (plus, at most, a single-file compiled probe against one header, which is legitimately how subtle guard bugs get found).
3. Merge each pass's reports into ONE ranked ledger in `audit-state.json`, deduplicated, ordered CRITICAL → NIT.
4. Additional Phase A passes are for COVERAGE, not for re-checking your own work: a second pass exists to find what the first missed, and because the tree has not changed, anything it reports is a genuine miss rather than fresh damage.

**Phase A ends only when a full pass adds no new findings.** There is no pass cap: a pass that finds anything new, at any severity, is followed by another pass. The tree is byte-identical to `baseline` throughout — verify with `git diff --quiet` before leaving Phase A, and say so.

### Phase B — REMEDIATE (fix once, verify once)

5. Fix the ledger in severity order, applying VERIFY BEFORE WRITE and compile-gating in small batches.
6. Build green, `ctest` green, and the game run through the scenes the fixes affect (`snx-run`): the tests cover what they cover, the game runs the rest.
7. A confirmation pass over the files you actually changed — not the whole inventory — to catch damage the remediation itself introduced. Fix what it finds, rebuild, run again.
8. **Confirmation repeats until a round is clean.** If a confirmation round found anything at HIGH or above, the fixes for it are themselves unverified remediation and get their own round, scoped to that delta. Stop only when a round returns nothing at all. There is no round cap.
9. Commit, verifying the message against the diff, and push.

### Why this is binding

The interleaved design has a specific pathology: **each pass's findings are dominated by the previous pass's fixes, so the loop measures its own churn rather than converging.** In one real run, pass 6's most serious findings were all pass-5 regressions — a symlink escape introduced while fixing a different symlink escape, a permanently-latching cache introduced while fixing a redundant one, and a test made *fully* vacuous by an assertion added to make it less vacuous. None of those defects existed in the code being audited. They were manufactured by the audit.

A frozen baseline removes the feedback loop at the source. You cannot damage what you are not editing, and a reviewer reading an unchanging tree reports real defects instead of your last hour's mistakes.

**Consequence for step 11's decision:** "no new findings" in Phase A means the audit is complete, not that the code is fixed. Do not emit a CLEAN verdict until Phase B's confirmation rounds are also green.

**The confirmation pass is where remediation damage is caught, so treat its yield as a measurement of the remediation, not as noise.** In one real run the first confirmation round returned six regressions the remediation had introduced — including a "root cause" fix that made the guard it shipped alongside structurally unable to fire — and the round that fixed those introduced two more. A confirmation round that comes back heavy is telling you the fixes were written from stories rather than mechanisms; the answer is another round plus VERIFY THE MECHANISM, not a verdict.

---

## LOOP: Repeat Until Clean (no pass cap)

**Within Phase A, after every audit pass, you MUST re-read and re-analyze. Do not skip this.** (Under the phase split there are no "fix passes" to re-analyze after — remediation is a single Phase B step with its own confirmation pass.)

### 8.5 Pass Definition (BINDING)

A "pass" is **every partition reviewer agent from step 2.5 re-dispatched in parallel**, on every file in the original inventory, full file reads. No exceptions.

**NOT a pass:**
- A single "verifier" or "spot-check" agent
- A subset of partitions (even if "Pass N−1 was clean for them" or "no Pass N−1 changes landed in those files")
- A grep-only verification without agent dispatch
- Inlining the analysis yourself instead of using agents

If the original scope used 6 partitions, every pass ≥2 dispatches EXACTLY 6 agents. Skipping any partition because "it was clean last time," "Pass N−1 didn't touch those files," or "I'm pretty sure nothing changed there" is **forbidden**. The skill is stateless between passes by design — a clean partition can be broken by a fix in another partition that changes a shared header, modifies an interface contract, or shifts call-site behaviour. You cannot rule that out without re-reading.

**If you dispatch fewer than the established partition count from step 2.5, the pass is INVALID.** The result is not a pass, cannot contribute to a CLEAN verdict, and the loop MUST re-dispatch the missing partitions before proceeding. State the violation explicitly ("Pass N was partial: dispatched A of P partitions — re-dispatching the missing P−A now") and continue the work.

**Anti-rationalization watch.** If you find yourself reasoning along any of these lines while planning a pass, you are about to downgrade the audit, NOT optimize it:
- "Pass N−1 was clean for partition X, skip it"
- "No Pass N−1 changes touched those files"
- "A focused verifier covers the concern"
- "This should be enough"
- "Re-running on unchanged files won't catch anything new"
- "I'll dispatch fewer agents to save tokens / time / context"

Each of those is a cost-shortcut, not a value judgement. Token budgeting is the **user's** job (via `+500k`-style directives), not yours. Run the full work.

**Anti-yield watch (Rule 0).** The list above is about downgrading a pass. This one is about ending the loop, which is the more common failure. If you catch yourself thinking any of these, you are about to violate Rule 0:
- "I should check in before starting another pass"
- "The user would probably want to weigh in here"
- "I'll report what I have and let them decide"
- "This is a natural stopping point"
- "The turn is getting long / a lot has happened"
- "I'll ask whether to keep going, to be safe"
- "I'll note this as out of scope and mention it in the summary"

**On "the last pass mostly found problems my own fixes caused":** under the phase split above this should no longer happen, because Phase A does not edit. If you are seeing it, you have interleaved fixing into an audit pass — stop, note the violation, and finish Phase A read-only.

It is still never a reason to yield. Damage you caused is damage that ships, so it must be fixed before the verdict either way. The difference is that the answer is now "go back to a frozen baseline", not "run another interleaved pass and hope it converges."

None of these is caution. Each is you replacing the skill's termination predicate with your own comfort. Keep going.

### 9. Fresh Read (NO EXCEPTIONS)

Use the Read tool to re-read **ALL files in the original audit scope** — not just the ones you edited. A fix in file A can invalidate assumptions in file B (callers, shared state, interface contracts). Your context is stale for every file, not just edited ones. Call Read on each file and look at actual disk contents. Do NOT rely on memory, context, or edit diffs.

**Mandatory checklist output.** Every pass ≥2 must begin with an explicit re-read confirmation matching the inventory from step 1.5:

```
Re-read confirmation (Pass N):
  1. path/file1.ext ✓
  2. path/file2.ext ✓
  ...
  M. path/fileM.ext ✓
  Re-read: M/M files
```

If the count does not match the inventory total, the pass is invalid — return to step 9 and read the missing files. For partitioned scopes (step 2.5), re-dispatch the partitioned reviewer agents with their respective file lists for the re-analysis; do not collapse a partitioned scope into single-threaded re-reads.

### 10. Re-Analyze (Full Scope, Not Just Edits)

Using ONLY fresh file contents from step 9, run the full step 3 analysis against **every file in the audit scope** — not just files you touched. Specifically check:

- Did any fix introduce a new issue in the edited file?
- Did any fix break a caller, consumer, or sibling file that wasn't edited?
- Did any fix regress another dimension?
- Are there issues in unedited files that I missed on the first pass?
- Did I miss anything earlier that I can now see with fresh eyes?

### 10.5 Dead-Code Scan

For every public function newly introduced or non-trivially modified in this audit's scope, grep for callers across the entire repo:

```bash
# Functions: find all call sites
ast-grep --pattern 'FunctionName($$$)' --lang c src
grep -rnw 'FunctionName' src tests tools scripts cmake
```

- **Zero callers** → either remove the function, or document the call path preserving it (e.g., reached through a dispatch table like `svc_register`, the `Renderer` table in `gpu/renderer.h`, or the generated code's calls into `src/common/cpu/aarch64/cpu_helpers.c`). A service's handler has no caller in the sources: its caller is the dispatcher generated into `build/src/nx/snx_hle-swipc/` from the `.swipc`, so check the command is declared there instead. A function that this audit is the first to grep for callers is a function nobody else verified is used.
- **Only self-callers (tests + the definition site)** → flag for likely-dead status; verify the test isn't the sole reason the function exists.

This step is mandatory on every pass — dead code accumulates between passes when fixes remove the last caller of a helper without removing the helper.

### 11. Decision

Evaluate in order. This predicate is the ONLY thing that may end the loop — not your read of the yield, the effort spent, or how the last pass went.

1. **Phase A, new findings exist** (not raised in an earlier pass) → record them in `audit-state.json` and run another full pass (step 8.5). Open findings are expected in Phase A: they are fixed in Phase B, never during an audit pass.
2. **Phase A, a full pass added nothing new** → Phase A is over. Go to Phase B: fix the ledger (step 5), build and run (step 6), then the confirmation rounds.
2b. **Phase B, any finding in `audit-state.json` with `status: "open"`** → back to step 5. Not optional.
3. **Only carry-over findings persist** (same finding re-flagged from a prior pass) → resolve them now: fix, or descope to a tracked artifact (issue link, PR description note, removal from scope) with the reason written into the state file. The skill is NOT allowed to re-flag the same finding for 3+ passes without action. File-size violations, missing test coverage, lossy collapses — these accumulate forever when "stay in scope" is used as a dodge. Once every carry-over is `fixed` or `descoped`, go to step 11.5.
4. **Zero findings** → go to step 11.5, then step 12.
5. **There is no pass cap.** A pass that found anything new is always followed by another full pass. The loop ends only through branches 3 or 4.

**Every branch ends at step 12.** There is no path out of this loop that skips the Final Report. If you are about to end your turn and have not emitted step 12, you are in violation of Rule 0 — go back and finish.

**Diminishing returns is not a termination condition.** "The last pass found little," "the remaining findings are minor," and "another pass probably won't find much" do not appear in the predicate above. Only the numbered conditions do. If you want to argue a pass is not worth running, that argument belongs in the step 12 verdict AFTER the predicate says stop — never as a reason to stop early.

### 11.5 Pre-Final-Report Self-Audit

Before writing the final report, answer each question explicitly:

0a. **Rule 0 audit.** Did I end a turn anywhere between step 4 and here — to ask permission, present options, report progress, or confirm the next pass? If yes, that was a violation. Note it plainly in the final report's Summary rather than hiding it; the user needs to know the loop ran discontinuously and why.

0b. **State-file audit.** Does `audit-state.json` contain any finding with `status: "open"`? If yes, I am not at step 11.5 — return to step 5 (Phase B fixes it). Does every `descoped` entry carry a `descope_reason` AND a `raised_pass` at least two passes old? A fresh finding marked `descoped` is a skipped finding, and the verdict cannot be CLEAN.

0. **Pass-count audit.** For every pass N ≥ 2, count the agent dispatches. Did I dispatch the SAME number of partition reviewers that step 2.5 established for Pass 1? If any pass was partial (fewer agents, a focused verifier, a single re-check, a grep-only walk in place of agent dispatch) — that pass is INVALID per step 8.5. Re-run the missing partitions and continue the loop before writing the final report. Do NOT classify a partial pass as "clean" — partial passes have no verdict at all.

1. Did I read every file in the inventory FULLY? (Compare step 1.5 inventory to actual Read calls.)
2. Did I analyze every file against every step-3 dimension — not just the dimensions where I expected findings? Including refactor-completeness, comment-code synchronization, defensive-code pair audit, side-effect completeness?
3. For partitioned scopes: did every reviewer agent return concrete findings (or explicitly "none")? If any agent crashed, returned generic boilerplate, or covered fewer files than its partition listed, that partition was not audited.
4. Did I assume prior pass coverage instead of re-reading? (Anti-trust rule from step 1.)
5. Are the file counts in step 12's `Files in Scope` and `Files Fully Read` going to match? If not, I have not finished.
6. For every refactor-shape finding I raised (introduced an accessor, renamed an API, extracted a helper), did I `ast-grep` / `grep` the WHOLE repo for the old pattern and either fix or descope every match — not just the matches inside my partition?
7. For every numeric or named claim in any comment I edited or left in place this pass ("WHY ONLY THESE FOUR", "the other nine", "see ::engineFor"), did I verify the claim against current code? Stale comment counts and dangling method references in the diff are findings I'm supposed to catch.
8. For every runtime guard, lock, or service failure path I touched, did I verify its pair? Asymmetric guard coverage = real LOW (sometimes MEDIUM) finding I should have raised.
9. For every change to state another stage consumes (syncpoints, kernel events, guest memory written by the GPU, audio buffers), did I trace forward to the hand-off? "It works because the next frame happens to flush it" is not a verification.
10. For every new or non-trivially modified public function in this PR, did I `ast-grep` / `grep` for callers? Dead helpers introduced by a fix are real findings.

If any answer is "no," "skipped," "I assumed," or "partially," return to step 9 and complete the missing work. Only proceed to step 12 when every answer is "yes."

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

- **Architecturally correct, always.** Never apply a quick hack, shortcut, or workaround. Every fix must be the proper solution — the change a senior engineer would make if they owned this code long-term. If the correct fix is harder or touches more files, that's the fix.
- **No TODOs, no follow-ups.** Never leave `TODO`, `FIXME`, `HACK`, `XXX`, "revisit later", or any comment implying future work. Never suggest a follow-up task. The code after audit must have zero outstanding action items.
- **Solve the root cause.** If a finding is a symptom, fix the underlying problem. Don't patch symptoms.

## Guidelines

- **Be direct.** No praise sandwiches.
- **Be concrete.** Every finding must cite a file and line.
- **Be proportional.** Scale depth to the size and risk of the change.
- **Don't invent problems.** If the code is solid, say so.
- **Respect project style.** Flag CLAUDE.md deviations, not personal preferences.
- **Read before judging.** A "bug" in the diff may be correct in context.
- **Fix confidently.** Don't ask permission for obvious corrections.
- **Minimize disruption.** Surgical fixes only — don't refactor surrounding code unless necessary to resolve a finding.
- **Stay in scope, but not as a dodge.** Analyze the changed code and its immediate context (callers, callees, shared state). Do not expand the audit to the entire codebase. BUT: if a finding has been raised in 2+ prior passes and continues to be deferred under "out of scope," that pattern is itself a finding — either fix it this pass or descope it to a tracked artifact (issue link, PR description note) so it stops re-appearing. "Carry-over scope" is not a permanent exemption. **This guideline bounds where you LOOK, never whether you fix what you found** — read it with step 5, which forbids descoping a finding raised in the current pass. Using "stay in scope" to drop a fresh finding inverts this line's intent.
- **Read scope ≠ grep scope.** Reading is bounded by the audit scope. Grepping / ast-grepping is repo-wide whenever a finding requires enumerating call sites, old-pattern remnants, or stale comment references.
