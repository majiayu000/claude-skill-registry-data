---
name: debug-driven
description: >
  Activates a structured, hypothesis-driven debugging loop.
  Use this skill whenever the user reports a bug, unexpected behavior, or runtime
  error and wants help diagnosing the root cause - especially for bugs that are
  hard to reproduce or where the fix isn't obvious. Trigger on phrases like:
  "debug this", "figure out why X is happening", "something is wrong with Y",
  "I have a bug", "debug-driven", or any request to investigate a runtime issue
  rather than just apply a code fix. Do NOT use for compile errors with obvious
  fixes or simple typos - only when runtime investigation is needed.
compatibility: >
  Requires a coding agent that can read and edit files. Browser-app debugging
  also requires Node.js to run scripts/http-log-ingest.js. Prefer an agent with
  a blocking question tool; if unavailable, fall back to a plain-text prompt.
---

# Debug-Driven

A structured, hypothesis-driven debugging loop. Instead of immediately
guessing a fix, this skill drives a disciplined hypothesis -> instrument ->
reproduce -> analyze -> fix -> verify -> cleanup cycle.

---

## Core Philosophy

**Never guess. Instrument, observe, then fix.**

The best debuggers do not immediately patch code. They:
1. Form multiple hypotheses about what could be wrong
2. Instrument the code to test each hypothesis with real runtime data
3. Let the human reproduce the bug (they are in the loop, not the AI)
4. Analyze the evidence and converge on a root cause
5. Apply a targeted fix and ask for confirmation
6. Clean up all instrumentation

This skill enforces that workflow.

---

## Phase 0: Bug Intake

Before doing anything else, gather what you know. Extract from the user's message:

- **Symptom**: What is actually happening?
- **Expected**: What should happen instead?
- **Reproduction steps**: How to trigger it?
- **Stack / environment**: Language, framework, relevant files?
- **Error output**: Any logs, stack traces, error messages already available?

If reproduction steps are missing or unclear, ask. You cannot proceed without them.

**Reproduction scripting:** If the bug can be triggered by a deterministic sequence (API call, test case, CLI command, browser automation script), write a reproduction script during intake. This script can be re-run by the agent in later cycles without requiring the user to manually reproduce each time. The user should still manually verify the final fix (Phase 6), but intermediate reproduction cycles (Phase 3) can use the script.

---

## Hypothesis Labeling Rules

Hypothesis labels are **session-global and monotonic**:
- Start the first set at `H1`
- Never reuse a label within the same debug session
- After a failed verification, continue from the highest label used so far (`H4`, `H5`, ...) rather than restarting at `H1`
- If an older hypothesis remains relevant, keep its original label instead of renumbering it

Keep track of the **active hypotheses** for the current cycle. An active hypothesis is any hypothesis that is still `INCONCLUSIVE` or newly introduced and not yet ruled out.

**New hypothesis labels may ONLY be introduced in two places:**
1. A Phase 1 cycle (initial or after all hypotheses are ruled out)
2. The "Path Forward" section of the Failed-Verification Recovery Template

In both cases, the full Phase 1 format (label + Mechanism + Confirm + Rule out) is required before the label exists. You cannot introduce a new `Hn` during Phase 4 analysis, Phase 5 fix, or inline in instrumentation code. If analysis reveals a new theory, note it in prose ("this suggests the issue may be in X") and then formally open a Phase 1 cycle to define it.

---

## Phase 1: Hypothesis Generation

### Code reading before hypothesizing

Before generating hypotheses, read enough code to form grounded theories — not just the file mentioned in the bug report:

- **Start at the symptom**: read the code where the bug manifests (the reported file/function)
- **Trace one level out**: follow the call chain — who calls this function? What does it call? Read those callers/callees
- **Check data flow**: if the bug involves wrong values, trace where those values originate (config, DB query, API response, user input)
- **Look for relevant state**: if the component has initialization, lifecycle hooks, or caching, read those paths — bugs often hide in setup code, not in the main logic

Stop when you can articulate at least 3 structurally distinct theories about what could be wrong. You do not need to read the entire codebase — just enough that your hypotheses are grounded in actual code paths, not pure speculation.

### Generating hypotheses

Generate **at least 3 distinct hypotheses** about what could be causing the bug. There is no hard upper limit, but each hypothesis must be structurally distinct — do not pad the list with variations of the same theory.

Format each hypothesis using **exactly** this structure. Do NOT use numbered lists, paragraphs, headings, or any other layout. Use `*` bullet prefix and indented sub-fields:

```text
* H1: [Short label — max ~10 words, e.g. "Off-by-one in pagination cursor"]
  - Mechanism: [1-2 sentences: how this fault causes the observed symptom]
  - Confirm: [What specific log values or behavior would prove this fault exists]
  - Rule out: [What specific log values or behavior would prove this fault does NOT exist]
```

Example:

```text
* H1: Discount rate read from stale cache entry
  - Mechanism: The pricing service caches discount rates for 5 minutes. If the rate
    was updated after the cache was populated, the old rate is applied to new orders.
  - Confirm: Log shows discount_rate=0.0 at cart.js:44 despite DB having rate=0.1
  - Rule out: Log shows discount_rate matches the current DB value
```

**Writing precise Confirm / Rule-out criteria:**
Criteria must name **specific expected values or value ranges**, not ambiguous states. The agent doing the verdict check will compare log output literally against your criteria — if the criteria say "is false" but the log shows `undefined`, that is not a match. Write criteria that account for every value the code can actually produce.

- **Good:** `initialDataFetched is falsy (false, undefined, or null)` — covers all cases
- **Good:** `discount_rate === 0.0` — exact value
- **Bad:** `initialDataFetched is false` — what if it's `undefined`? The verdict becomes ambiguous
- **Bad:** `the value is wrong` — not specific enough to check mechanically

If you are unsure which exact value to expect, use a range or disjunction (`X is one of [a, b, c]`) rather than guessing a single value.

**Rules:**
- Order by plausibility (most likely first)
- Cover structurally distinct failure modes - do not list variations of the same root cause
- At least one hypothesis should be in the reported area, and at least one should cover an upstream or downstream assumption you are NOT sure about
- Do not propose a fix yet - this is purely diagnostic
- Every hypothesis must describe a **specific fault** — something wrong that causes the symptom. "The recount triggers correctly" or "trace the execution flow" are not hypotheses. If it cannot be phrased as "the bug is caused by [specific fault]", rewrite it or drop it.
- Do NOT offer to skip instrumentation. No matter how confident you are from reading the code, you must instrument and observe runtime evidence before proposing a fix. Code reading produces hypotheses, not conclusions.
- Do NOT shortcut the logging method. Use the correct method for the project type (file-append for non-browser, fetch-to-ingest-server for browser). Do not substitute `console.log` to "move faster" or because you are confident - follow the documented flow.

Present the hypotheses to the user as context for what you are about to instrument, then **immediately proceed to Phase 2 in the same response**. Do not pause, do not ask for feedback, do not ask "what should we do next?", do not offer alternative courses of action. The user will have a chance to intervene during Phase 3 (reproduction) if any hypothesis is wrong.

---

## Phase 2: Instrumentation

Design and inject logging statements that will generate evidence for or against each hypothesis.

### Log output method

All debug instrumentation **logs to a file** (`./debug-output.log` by default) rather than to stdout or console. This lets the agent read the log file directly after reproduction.

- **Non-browser apps** -> file-append using the language's native API. See [log-output-recipes.md](references/log-output-recipes.md) for one-liners and full examples per language.
- **Browser apps** -> `fetch()` to the HTTP log ingest server bundled with this skill. See [log-output-recipes.md](references/log-output-recipes.md) for server launch procedure and fetch pattern.

**You MUST use the method above for the project type.** Do NOT substitute `console.log` because it seems easier. The only valid reason to use `console.log` for browser apps is if the user explicitly refused to run the ingest server.

### Log format

Every log line MUST start with the hypothesis label, followed by location, data label, and value:

```
<Hn> | <file>:<line> | <label> | <value>
```

The `Hn` prefix is not optional — it is what makes hypothesis-driven analysis possible. Without it, log lines cannot be filtered by hypothesis, and the Phase 4 mechanical verdict check cannot work. Every `_dbg()` call or `fetch()` body must embed the `Hn` label as the **first field in the log string itself**, not as a separate argument.

**Correct** — hypothesis label is part of the string:
```js
_dbg('H1 | auth.js:42 | token_received | ' + JSON.stringify(token));
```

```js
fetch('http://localhost:' + port + '/log', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'H2 | cart.js:88 | discount_rate | ' + rate })
});
```

**Wrong** — no hypothesis label, no file:line, freeform arguments:
```js
_dbg('tokenReceived', token);          // missing Hn, missing file:line
_dbg('discount', { rate, subtotal });  // missing Hn, missing file:line
```

If a log line does not match `<Hn> | <file>:<line> | <label> | <value>`, it is malformed. Fix it before proceeding.

### Log placement strategy

- Log at entry or exit of suspicious functions (capture inputs and outputs)
- Log before or after state mutations (capture before and after values)
- Log inside conditional branches (which path is actually taken?)
- Log loop boundaries if loops are involved (how many iterations? what values?)

### Wrapping instrumentation in region blocks

**All debug instrumentation MUST be wrapped in `#region DEBUG` / `#endregion DEBUG` blocks.** This makes cleanup reliable - entire regions can be found and deleted as units.

Use the appropriate region markers for the language:

| Language | Start marker | End marker |
|---|---|---|
| JavaScript / TypeScript | `// #region DEBUG` | `// #endregion DEBUG` |
| Python | `# region DEBUG` | `# endregion DEBUG` |
| C# | `#region DEBUG` | `#endregion DEBUG` |
| Java / Kotlin | `// region DEBUG` | `// endregion DEBUG` |
| Go / Rust | `// region DEBUG` | `// endregion DEBUG` |
| Ruby | `# region DEBUG` | `# endregion DEBUG` |

**Rules:**
- Every piece of debug code (log statements, debug-only imports, temporary variables) goes inside a region block
- Multiple region blocks per file are fine - group by hypothesis
- Never put non-debug production code inside a region block
- The region comment is the outer wrapper; log lines and helpers go inside

### Scoping instrumentation

- Add only what is needed to test your hypotheses - do not spam logs everywhere
- If you have 4 hypotheses, group logs by which hypothesis they test
- Each group should be in its own region block

**Guardrails:**
- Only add instrumentation that is explicitly tied to one or more active hypothesis labels
- Do not add freeform or "just in case" logging with no hypothesis mapping
- If a hypothesis is no longer active, stop adding logs for it unless you explicitly reactivate it with a stated reason
- **Every `Hn` label used in instrumentation must reference a hypothesis that was formally defined in Phase 1 format** (short label + mechanism + evidence criteria). You may NOT invent a new `Hn` tag in instrumentation code and define the hypothesis later or not at all — that is not a hypothesis, it is freeform logging with a label painted on it.
- **Instrumentation tests hypotheses, not fixes.** If you want to know whether a fix worked, that is Phase 6 (user reproduction). Do not add logging "to see if the fix executes" — that conflates diagnosis with verification and leads to drift.
- **Instrumentation is read-only.** Debug code observes and logs — it does NOT change application behavior. Do not add `setTimeout` triggers, force-call methods, bypass guards, set flags, inject test data, or modify control flow "to see what happens." If you want to test whether changing behavior X fixes the bug, that is a Phase 5 fix, not Phase 2 instrumentation. Instrumentation that alters the system under observation invalidates the evidence it collects.

After adding instrumentation, tell the user exactly what was added and where.

> For complete per-language examples (Node, Python, Go, Java, C#, Ruby, browser fetch), see [log-output-recipes.md](references/log-output-recipes.md).

---

## Phase 3: Reproduction Request (Interactive Loop)

After adding instrumentation, present an interactive reproduction menu. **You MUST use a tool call that blocks execution and waits for the user to select an answer** - do NOT just print the choices as text in your response. Use whichever tool your platform provides for asking the user a question with predefined selectable answers (for example, `ask`, `askQuestion`, `ask_user`, or equivalent).

**If an automated reproduction script exists** (written during Phase 0 or a prior cycle), run it instead of asking the user. Skip the interactive menu and proceed directly to Phase 4. Only use the interactive menu when no reproduction script exists, or for the final verification (Phase 6) which always requires user confirmation.

**Question text:**
> I've added instrumentation to test [H1, H2, H3].
>
> Please reproduce the bug using these steps:
> 1. [reproduction step 1 from Phase 0]
> 2. [reproduction step 2 from Phase 0]
> 3. ...
>
> Debug output will be written to `./debug-output.log`. I will read it after you reproduce.
> Log handling for this run: [clearing or appending] `./debug-output.log` because [brief reason].
> If the app needs a restart or rebuild, do that first.
>
> After testing, select an option below.

**Answer choices:**
1. `Issue reproduced -- proceed with analysis`
2. `Mark as fixed`

The second option covers the rare case where the bug resolves during instrumentation (e.g., the agent touched a file that triggered a rebuild that fixed a stale cache). In the normal flow, choose option 1.

If your platform does **not** provide a blocking question tool with selectable answers, present the same prompt and the same two choices as plain text, then wait for the user's reply before continuing.

**Behavior:**
- **"Issue reproduced"** -> proceed to Phase 4 (Log Analysis). The agent reads `./debug-output.log` directly.
- **"Mark as fixed"** -> skip directly to Phase 7 (Cleanup).

---

## Phase 4: Log Analysis

**Phase 4 is analysis only — no code changes, no instrumentation edits.** If you need more data, the outcome is INCONCLUSIVE and you return to Phase 2. Do not edit source files during Phase 4.

Read `./debug-output.log` (or whatever log file path was used). Then:

1. Parse the log lines using the `<Hn> | <file>:<line> | <label> | <value>` format — filter by hypothesis label to group related lines
2. For each active hypothesis, check whether the logs confirm, refute, or leave it inconclusive
3. Identify the specific line or value that reveals the root cause
4. If the root cause is still unclear, go back to Phase 2 and add more targeted instrumentation

**After every analysis round, you MUST present a verdict for every active hypothesis.** Every active hypothesis must get exactly one of: **CONFIRMED**, **RULED OUT**, or **INCONCLUSIVE**. No other verdicts are valid. In particular, "CONFIRMED WORKING" is not a verdict — hypotheses describe faults, and a fault is either present (CONFIRMED) or absent (RULED OUT).

**How to produce each verdict — mechanical check, not a judgment call:**
1. Re-read the hypothesis's **Confirm** field. Does a specific log line match it? If yes -> CONFIRMED candidate.
2. Re-read the hypothesis's **Rule out** field. Does a specific log line match it? If yes -> RULED OUT, even if the behavior "looks related."
3. If a log line matches the Rule-out criteria, the verdict **cannot** be CONFIRMED — full stop. The Rule-out condition is met.
4. If neither Confirm nor Rule-out criteria are clearly matched -> INCONCLUSIVE.

**Use this exact format for every verdict** — one block per hypothesis, with the criteria and matching log line quoted side by side. Do NOT use a one-line summary without the evidence structure:

```text
- H1 (Off-by-one in cursor): RULED OUT
  Rule-out criteria: "Log shows cursor value matches expected page boundary"
  Matching log line: "H1 | handler.go:67 | page_cursor | 42" (42 matches expected)

- H2 (Discount not applied to subtotal): CONFIRMED
  Confirm criteria: "Log shows discount_rate=0.0 at cart.js:44 despite DB having rate=0.1"
  Matching log line: "H2 | cart.js:44 | discount_rate | 0.0"

- H3 (Wrong product ID in lookup): INCONCLUSIVE
  Neither criteria matched — log shows product_id=undefined (not anticipated by Confirm or Rule-out)
```

If you cannot produce a matching log line for the Confirm or Rule-out field, the verdict is INCONCLUSIVE — even if you believe the hypothesis is correct from reading the code. If the log value doesn't match the Confirm criteria exactly (e.g., criteria says "is false" but log shows "undefined"), note the discrepancy and mark INCONCLUSIVE or revise the criteria before confirming.

**Verdict persistence:** Once a hypothesis receives CONFIRMED or RULED OUT based on specific log evidence, that verdict holds for the rest of the session unless new log evidence from a later cycle directly contradicts the original log lines. You may not flip a verdict based on reasoning about the code or because a fix didn't work — only new runtime evidence can change a verdict. If you find yourself wanting to reverse a verdict, state which new log lines contradict the original evidence.

**If log evidence does not match any Confirm or Rule-out criteria** and the logs reveal something unexpected that none of your criteria anticipated, the problem is not just insufficient data — your evidence criteria may be wrong. In this case, mark the hypothesis INCONCLUSIVE and note what the criteria missed. When you return to Phase 2, revise the Confirm/Rule-out fields to account for the unexpected observation before adding more instrumentation.

### Phase 4 outcomes

- If one or more active hypotheses are `CONFIRMED` -> proceed to Phase 5
- If any are `INCONCLUSIVE` and the remaining hypotheses still plausibly cover the bug -> go back to Phase 2 with more targeted instrumentation for those specific hypotheses
- **If evidence reveals the problem is in an area that no active hypothesis covers** (e.g., the function is never called, the data comes from an unexpected source) -> open a new Phase 1 cycle to generate hypotheses for the newly revealed area. Carry forward any still-relevant INCONCLUSIVE hypotheses by their original labels. New hypotheses start at the next unused label.
- If all active hypotheses are `RULED OUT` -> generate new hypotheses using the next available session-global labels (return to Phase 1)

### Log file management between iterations

Before each new reproduction cycle, decide whether to **clear** or **append** to the log file:

- **Clear** when: the fix changed behavior and old log lines would be misleading, when starting a new debug cycle after failed verification, or when you are narrowing to fewer hypotheses and want to reduce noise.
  **To clear, delete the file** (`rm`, `Remove-Item`, `del`, or equivalent). Do NOT use `echo "" > file` or shell redirection to "empty" it — on Windows, PowerShell redirection writes UTF-16LE with a BOM, which corrupts subsequent UTF-8 appends and produces garbled log output.
- **Append** when: you want to compare values across iterations within the same active hypothesis cycle, or multiple active hypotheses are still open and prior data is still useful

State your choice and reasoning briefly when presenting the reproduction menu. The reproduction prompt must explicitly say whether the log file is being **cleared** or **appended**, and why.

---

## Phase 5: Fix

**Prerequisite:** You may only reach this phase after log evidence from Phase 4 has **confirmed** a hypothesis. Confidence from code reading alone is not sufficient - you must have observed the actual runtime values that prove the root cause. If you have not run through Phases 2-4, go back.

Once the root cause is confirmed by log evidence, propose a **targeted fix**:

**Phase 5 contains NO instrumentation.** If you realize during Phase 5 that you need more runtime data before you can write a fix, STOP — do not add logging. State what is missing and return to Phase 2. Phase 5 produces exactly one artifact: a code change that fixes the confirmed fault.

- Fix only what the evidence points to - do not refactor unrelated things
- Show a diff-style before or after if the change is non-trivial
- Briefly explain *why* the fix addresses the confirmed root cause
- If the fix has side effects or risks, call them out

After applying the fix, proceed to Phase 6 for user verification.

---

## Phase 6: Verification (Interactive Loop)

After the fix is applied, use a **blocking question tool** (not a text message - a tool call with selectable answers). Note: the answer choices here differ from Phase 3.

**Question text:**
> Fix applied: [brief description of what was changed].
>
> Please reproduce the bug using the original steps to verify the fix.
> After testing, select an option below.

**Answer choices:**
1. `Issue still present -- fix did not work`
2. `Mark as fixed`

If your platform does **not** provide a blocking question tool with selectable answers, present the same prompt and the same two choices as plain text, then wait for the user's reply before continuing.

**Behavior:**
- **"Issue still present"** -> **Phase 6 ends immediately.** Do not keep looping inside verification. Follow the **Failed-Verification Recovery Protocol** (its own section below). The very next agent action must be the mandatory recovery template — not another fix, not more verification, and not freeform instrumentation. **This applies every time the user selects "Issue still present" — not just the first time.** The 2nd, 3rd, and Nth failure each require the full recovery protocol with the same rigor as the 1st. Skipping the protocol on subsequent failures is the most common form of agent drift.
- **"Mark as fixed"** -> proceed to Phase 7 (Cleanup).

**Abandoning the debug session:**
At any point, if the user says they want to stop debugging (for example, "abandon", "stop", "give up", "cancel"), proceed directly to Phase 7 (Cleanup). **Always clean up, even when abandoning.**

This loop continues — cycling through structured debug cycles ending in Phases 5-6 — until the user selects "Mark as fixed" or explicitly abandons the session.

---

## Failed-Verification Recovery Protocol

**This is the single most important section for preventing agent drift.** When the user selects `Issue still present -- fix did not work`, treat that as a **hard boundary** between debug cycles. Everything below is mandatory.

### Mandatory Recovery Template

Your **very first action** after `Issue still present` must be to **read `./debug-output.log`** to obtain post-fix evidence. Then produce the template below. Do not add instrumentation, do not edit code, do not do anything else until you have read the log file and produced this complete template.

```text
## Phase 6 Failed — New Debug Cycle

**Next available hypothesis labels:** H<n>+

### Fix Disposition

The failed fix in [file(s)] will be: **reverted** / **kept**.
- **Log evidence comparison:** [Quote specific log lines from BEFORE the fix vs AFTER
  the fix that show whether behavior changed. If you have no post-fix logs, you
  cannot claim the fix "addresses a valid issue" — revert it.]
- **Decision reasoning:** [Based on the log comparison above, explain why keeping
  or reverting is the right call.]

### Active Hypothesis Verdicts (from post-fix logs)

- H1 (short label): CONFIRMED / RULED OUT / INCONCLUSIVE — [evidence summary]
- H2 (short label): CONFIRMED / RULED OUT / INCONCLUSIVE — [evidence summary]
- ...one bullet per hypothesis that was active in the previous cycle...

### Why the Previous Fix Was Insufficient

[State whether the confirmed root cause was wrong, partial, or merely symptomatic.
Do not claim the root cause is "identified" unless a currently active hypothesis
is CONFIRMED by runtime evidence from the latest reproduction.]

### Path Forward

**Continuing existing hypotheses** / **Generating new hypotheses starting at H<n>**

[If generating new hypotheses, execute Phase 1 now — the same rules and format
apply. Minimum 3 new hypotheses, each with label + Mechanism + Confirm + Rule out.
Do not proceed to Phase 2 until every new hypothesis is written below.]

* H<n>: [Short label describing a specific fault]
  - Mechanism: [How this fault would cause the observed symptom]
  - Confirm: [What log evidence would prove this hypothesis]
  - Rule out: [What log evidence would disprove this hypothesis]
* H<n+1>: ...
* H<n+2>: ...
  [minimum 3 new hypotheses]
```

**Every field is required.** If you skip a field, you are drifting. If the "Path Forward" section says "Generating new hypotheses" but contains fewer than 3 hypotheses or no hypothesis list at all, you are drifting.

### Fix Disposition Rules

After a failed verification you MUST explicitly decide what to do with the failed fix. **The decision must be grounded in log evidence, not reasoning about the code.**

- **Revert** when: you have no post-fix logs to compare against, or the post-fix logs show no meaningful behavior change, or the fix was based on a hypothesis that is no longer CONFIRMED, or the fix could mask or interfere with further diagnosis.
- **Keep** when: post-fix logs show a concrete, observable behavior change in the right direction (quote the specific log lines), AND the bug persists due to an additional issue downstream of the fixed code path. A common case: the fix corrects a prerequisite (e.g., a value that was wrong is now correct) but the symptom persists because a second fault exists downstream. If the post-fix logs prove the prerequisite is now correct, **keep the fix** — reverting it would re-introduce the first fault and force you to fix it again later.
- **Default to revert.** "The fix addresses a valid issue" or "the logic seems correct" is not sufficient justification to keep a fix that didn't work. If you cannot point to specific log lines showing changed behavior, revert. But note: "default to revert" means revert **when you have no log evidence either way**. If you read the post-fix logs and they show a real change, that is evidence — use it.
- Do not silently leave a failed fix in place and pile more changes on top.
- **Stating a disposition is not the same as executing it.** After writing the recovery template:
  - If **reverted**: show the revert (undo edit, git checkout, or equivalent) before adding any new instrumentation. The next code change the agent makes must be the revert itself.
  - If **kept**: no action needed, but the log evidence comparison must include quoted post-fix log lines (not reasoning about the code).

### Continuing Existing Hypotheses

Choose this only if the existing hypothesis list already contains one or more unresolved `INCONCLUSIVE` items that still meaningfully explain the issue.

Requirements:
- Restate every still-active carried-forward hypothesis using its original label
- Update each carried-forward hypothesis with its new verdict
- Add only targeted instrumentation tied to those active labels
- Return to Phase 3 for reproduction after instrumentation

### Generating New Hypotheses

Choose this when the prior active hypotheses are no longer sufficient or all were ruled out by the latest evidence. **This is a full Phase 1 cycle** — the same rules, format, and rigor from Phase 1 apply. Refer to Phase 1 for the complete requirements.

**After defining new hypotheses in the Path Forward section, proceed to Phase 2 for instrumentation.** Do NOT skip to Phase 5. New hypotheses must be tested with instrumentation and observed with runtime evidence before any fix is attempted. The sequence is always: define hypotheses (here) -> instrument (Phase 2) -> reproduce (Phase 3) -> analyze (Phase 4) -> fix only if CONFIRMED (Phase 5).

### What Counts as a Valid Hypothesis

A hypothesis must describe a **specific fault mechanism** — something that is wrong in the code or environment that causes the observed symptom. It must be possible for the hypothesis to be wrong.

**Valid hypotheses:**
- `H7: autoFetch guard skips data sources with undefined initialDataFetched` — describes a specific code path that could be faulty
- `H8: count API rejects requests when no filter context is provided` — describes a specific server-side failure mode

**Invalid "hypotheses" (these are observations, not fault descriptions):**
- `H7: the recount is being triggered correctly` — this describes correct behavior, not a fault. A hypothesis that "things work" cannot explain a bug.
- `H7: verify the fix executes` — this is testing a code change, not diagnosing a fault. Use Phase 6 for that.
- `H7: trace the full execution flow` — this is an instrumentation strategy, not a hypothesis. You need to say what you think is *wrong*, not what you want to *observe*.
- `H7: count service should bypass initialDataFetched check` — this describes a code change (fix), not a fault. The fault version is: `H7: initialDataFetched guard blocks counting for data sources that never auto-fetch`. Hypotheses describe what IS wrong, not what SHOULD be changed.

If a proposed hypothesis cannot be phrased as "the bug is caused by [specific fault]", it is not a hypothesis.

### Hard Guardrails After Failed Verification

You MUST NOT:
- Apply another production fix immediately after failed verification
- Stay in Phase 6 for multiple rounds — one `Issue still present` ends Phase 6
- Add instrumentation unless each new log is tied to an active hypothesis label **that has a full definition** (label + mechanism + evidence criteria)
- Create ad-hoc `Hn` labels in instrumentation code without first defining the hypothesis in Phase 1 format
- Claim the root cause is "identified" unless a currently active hypothesis is `CONFIRMED` by runtime evidence from the latest cycle
- Restart numbering at `H1`
- Add instrumentation "to test a fix" — instrumentation tests *hypotheses about what is wrong*, not whether a fix works. Phase 6 (reproduction by the user) tests fixes
- Give a hypothesis a verdict of "CONFIRMED WORKING" — that is not a valid verdict. The three valid verdicts are CONFIRMED (this fault is the cause), RULED OUT (this fault is not the cause), and INCONCLUSIVE (insufficient evidence). "Working" is not a fault state.
- Declare "root cause identified" in prose outside of the Phase 4 verdict format — root cause identification happens through a CONFIRMED verdict on a specific hypothesis, not through narrative claims during analysis

Only return to Phase 5 after at least one **currently active** hypothesis is newly `CONFIRMED` by evidence from the post-fix run or later runs in the new cycle.

---

## Escalation Criteria

The debug loop can cycle indefinitely. Recognize when it is no longer productive.

**After 3 full cycles** (Phase 1 through Phase 6) without a CONFIRMED hypothesis, pause and present the user with options:

- The bug may be in a dependency, framework, or runtime — application-level instrumentation cannot reach it. Suggest checking dependency versions, known issues, or upstream changelogs.
- A different diagnostic approach may be more effective: `git bisect`, profiling, or consulting someone with domain knowledge of the affected subsystem.
- The reproduction may be unreliable — if log output is inconsistent across runs, the bug may be timing-dependent and needs the async/concurrent debugging approach (see Edge Cases).

**Do not abandon the structured approach silently.** If you believe escalation is warranted before 3 cycles, state your reasoning explicitly. The user decides whether to continue, escalate, or abandon.

---

## Phase 7: Cleanup

Once the issue is marked as fixed (or the session is abandoned), perform **ALL** of the following cleanup steps. This is critical - no debug artifacts should survive.

### 1. Stop the log ingest server (if running)

If the log ingest server was started during this session, read the PID from `./debug-ingest.pid` and kill that process. Then delete both `./debug-ingest.pid` and `./debug-ingest.port`. The server attempts to clean these up on graceful shutdown, but verify they are gone.

### 2. Delete the log file

Delete the log file that was passed as `--logFile` (for example, `./debug-output.log`).

### 3. Remove all `#region DEBUG` blocks

Search the codebase for files containing `region DEBUG`. For each file, remove the entire block from the start marker through the end marker, inclusive of all content between. Verify that no debug regions remain.

> See [cleanup-patterns.md](references/cleanup-patterns.md) for per-language regex patterns.

### 4. Remove debug-only imports

Check for any imports that were added solely for debug logging (for example, `import json` in Python). These should have been inside region blocks, but verify independently.

### 5. Final artifact scan

Search the codebase for any remaining occurrences of:
- `region DEBUG`
- `debug-output.log` (or whatever log file path was used)
- `debug-ingest.pid` and `debug-ingest.port` (delete these files if they still exist)
- `localhost:<port>/log` (if the ingest server was used)
- `_dbg` helper functions added for debug logging

If any artifacts remain, remove them.

### 6. Confirm cleanup

Tell the user: *"Cleanup complete. All debug instrumentation, region blocks, log files, and the ingest server have been removed."*

---

## Edge Cases & Special Situations

### Bug is hard to reproduce

If the user cannot easily reproduce the bug, help them write a minimal test or script that reliably triggers it before proceeding to instrumentation.

### Async or concurrent bugs

For race conditions or async timing issues:
- Include timestamps in log lines: `_dbg('H1 | ' + Date.now() + ' | label | ' + value)`
- Log event loop or promise chain entry and resolution points
- Consider adding artificial delays to expose timing-dependent behavior

### Production-only bugs

If the bug only appears in production:
- Propose the minimum safe instrumentation that can be deployed to prod
- Prefer structured log fields over `console.log` for production use
- Agree with the user on whether to deploy debug instrumentation or reproduce locally with prod data

### Bug reappears after fix

Reopen structured hypothesis work. The original root cause may have been a symptom of a deeper issue. Treat this as a new debug cycle using the failed-verification recovery protocol, and continue hypothesis labels monotonically from the highest `Hn` already used in the session.

---

## Quick Reference Card

```text
Phase 0  -> Intake: symptom, expected, repro steps, env, reproduction script if possible
Phase 1  -> Hypotheses: at least 3, ordered by plausibility, no fixes yet
Phase 2  -> Instrumentation: targeted logs in #region DEBUG blocks
Phase 3  -> INTERACTIVE MENU: ask human to reproduce (or run repro script), choose outcome
Phase 4  -> Analysis: confirm/refute each active hypothesis from log evidence
         -> If evidence reveals new area: open Phase 1 for that area
Phase 5  -> Fix: targeted, evidence-based, NO instrumentation
Phase 6  -> INTERACTIVE MENU: human verifies fix, choose outcome
RECOVERY -> MANDATORY TEMPLATE: fix disposition, verdicts, path forward
         -> No code changes until template is complete
         -> New Hn labels require Phase 1 definitions first
ESCALATE -> After 3 cycles without CONFIRMED: suggest alternative approaches
Phase 7  -> Cleanup: remove regions, log file, ingest server, all artifacts
         -> Loop through new structured cycles until "Mark as fixed" or abandoned
```

---

## Agent Compatibility Notes

This skill is designed to work with AI coding agents that can read or write files and interact with the user. It works best when the agent also has a blocking question tool, but it can fall back to plain-text prompts when that tool is unavailable.

**Interactive menu:** You MUST use a tool call that presents selectable answer choices and blocks until the user responds (for example, `ask`, `askQuestion`, `ask_user`, or equivalent). Do NOT just print the choices as text - that does not block execution and the agent will continue without waiting. Only fall back to printing choices as text if your platform genuinely has no such tool.

**Log ingest server:** The ingest script is bundled at [`scripts/http-log-ingest.js`](scripts/http-log-ingest.js) inside this skill's directory - do NOT create your own. Follow the **Server launch procedure** in [log-output-recipes.md](references/log-output-recipes.md): try once, if blocked ask the user, if that fails fall back to `console.log`. Do NOT try creative workarounds (REPL, PowerShell jobs, child process hacks) - they waste tokens and always fail.

**Cleanup:** The `#region DEBUG` blocks and isolated log file make instrumentation easy to search for and remove programmatically. Always use them consistently.

> See [cleanup-patterns.md](references/cleanup-patterns.md) for regex patterns, [framework-recipes.md](references/framework-recipes.md) for framework-specific instrumentation examples, and [log-output-recipes.md](references/log-output-recipes.md) for per-language logging patterns.
