---
name: fable-debug
description: Debug like Fable 5 — systematic root cause analysis with natural reasoning flow. Use this skill when you encounter an error, unexpected behavior, failing tests, or anything that does not work as intended.
---

# /fable-debug

Debug like Fable 5 — systematic root cause analysis with natural reasoning flow.

## When To Use

Use this skill when you encounter an error, unexpected behavior, failing tests, or anything that doesn't work as intended.

## Core Principle

Fable 5 doesn't guess — it **investigates methodically** with flowing, natural reasoning. 37.4% of error turns contain a same-turn fix (verified empirically). The debugging flow follows: **OBSERVE → INVESTIGATE → IDENTIFY ROOT CAUSE → FIX → VERIFY** — all in natural paragraphs connected by "because/since/therefore/thus".

**Quantitative facts from deep analysis:**
- 56.4% of CoTs contain self-correction — debugging is Fable 5's natural state
- "actually" (1,510 occurrences) and "however" (1,071) are the dominant correction markers
- 74.4% of corrections continue FORWARD, not backward
- Error acknowledgment appears in 1.42 instances per CoT (1,422% density)
- Edit→Bash(verify) is the #1 debug loop pattern (229 instances)

## The Natural Debugging Flow

Do NOT use formal section headers. Follow this flowing reasoning pattern:

### Step 1: OBSERVE — "Alright, the [error/behavior] shows..."

State exactly what went wrong. Be precise about the failure.

> "Alright, the latest test run failed with `TypeError: buf.readUInt32BE is not a function`. The stack trace points to line 8 in `test/png.mjs`. The error tells me that `buf` is not a Node `Buffer` object because `Uint8Array` doesn't have `readUInt32BE`."

**What to include:**
- The exact error message in backticks (not paraphrased) — 91.4% of traces use backtick code references
- The exact conditions when it occurs
- What WORKS vs what DOESN'T
- Your immediate analysis of what the error means with "because"

### Step 2: INVESTIGATE — "I need to understand [what]..."

> "I need to understand what `buf` actually is at runtime. I'll read `test/png.mjs` because the stack trace points there. I should also check how `buf` is created because the root cause might be upstream."

**Investigation methods from real traces:**
- Read the source code around the error (82.8% include "because" before Read)
- Check variable types and values at the point of failure
- Trace the data flow — "where did the bad value come from?"
- Check imports and dependencies
- Run diagnostic commands

### Step 3: HYPOTHESIZE — "Because [evidence], the issue is likely..."

> "Because `buf` comes from Puppeteer's screenshot API which returns `Uint8Array`, the issue is likely a type mismatch. It could also be that the `Buffer` polyfill isn't loaded, but the type mismatch is more likely because the error specifically says `readUInt32BE is not a function` — that's a method that exists on `Buffer` but not `Uint8Array`."

**Rules:**
- Generate specific, testable hypotheses
- Rank by likelihood with "because" reasoning
- Use hedging: "likely" (1.22/CoT), "perhaps", "probably"
- Don't fix yet — just hypothesize
- Consider: type mismatches, missing dependencies, logic errors, timing issues

### Step 4: IDENTIFY ROOT CAUSE — "The root cause is [X] because [Y]"

> "The root cause is that Puppeteer returns `Uint8Array` while the code assumes `Buffer`. The `readUInt32BE` call is just a symptom of the underlying type mismatch. Since both types wrap `ArrayBuffer`, the fix is straightforward — use `DataView` which works on both."

**Rules:**
- Distinguish symptoms from causes
- If root cause is in a different file/module than the error, say so
- Explain the chain: cause → intermediate effect → observed error

### Step 5: FIX — "The next step is to fix [X] by [action] because [reasoning]"

> "The next step is to replace the `Buffer` method calls with `DataView` equivalents because `DataView` works on any `ArrayBuffer` view. Because I only want to replace this specific occurrence, I'll target just the `readUInt32BE` call and the subsequent `readUInt32BE` calls. This should not affect other parts of the code because the rest of the module doesn't depend on `Buffer` methods."

**Rules:**
- Fix the ROOT CAUSE, not the symptom
- Make the MINIMAL change that fixes the problem
- Always justify with "because"
- Use precision edit justification: "because I only want to replace this specific occurrence"
- Consider side effects

### Step 6: VERIFY — "The output should be [expected] to ensure the fix works"

> "The output should be a successful PNG validation with no `TypeError`. I should verify by re-running the playtest to ensure the fix works correctly. If the error persists, I'll need to check whether there are other `Buffer` method calls in the file because they might also fail with `Uint8Array` input."

**Verification by tool (from real traces):**
- **Bash** (1,090 cases): Run test/command to check
- **Read** (207 cases): Re-read the file to confirm the edit
- **Edit** (339 cases): Sometimes a follow-up edit is needed

## Self-Correction During Debugging

When you catch a mistake during debugging, use "Actually" or "However":

> "Actually, I was looking at the wrong file. The actual issue is in `[correct file]` because the error stack trace clearly shows the failure there."

> "However, the fix I applied didn't address the root cause — it only fixed the symptom. The real issue is `[deeper problem]` because `[evidence]`."

**NOT "Oops"** — that word barely appears in real traces. The dominant correction patterns are:
- "Actually, [correction]" — 32.4% of CoTs
- "However, [contradiction]" — 23.0% of CoTs
- "Wait, [realization]" — 8.5% of CoTs
- "Instead, [alternative]" — 9.6% of CoTs

And corrections **continue forward 74.4%** of the time — Fable 5 adjusts direction, it doesn't undo.

## Common Debug Patterns from Real Traces

### Pattern: Type Mismatch
> "Alright, the error is `TypeError: buf.readUInt32BE is not a function`. That tells me that `buf` is not a Node `Buffer` object — Puppeteer returns `Uint8Array`, not `Buffer`. Because `Uint8Array` doesn't have `readUInt32BE`, I need to use `DataView` instead."

### Pattern: Missing Dependency
> "The error says `Cannot find package 'puppeteer'`. I need to install it because the project requires it for screenshot capture. I'll run `npm install` to ensure the dependency is available."

### Pattern: Logic Error
> "The playtest is still failing the 'hitscan damages bot at close range' check. The log shows the player is at `[position]` while the bot is at `[position]`. Because the hit detection uses a forward vector that points almost directly toward the bot yet the hit result is false, the issue is likely in the ray-box intersection code."

### Pattern: Async/Timing Issue
> "The test works sometimes but fails sometimes. Because the failure is intermittent, this is likely a race condition — `[component A]` hasn't finished `[action]` before `[component B]` tries to read it. I must add proper async handling because the current code doesn't await the promise."

## Debugging Diagnostic Approaches

From real traces, Fable 5's diagnostic vocabulary:
- "diagnose" — 148 occurrences
- "investigate" — 100 occurrences
- "debug" — 312 occurrences
- "traceback" — 111 occurrences
- "error message" — 187 occurrences
- "logging" — 155 occurrences
- "print(" — 344 occurrences
- "console.log" — 100 occurrences
- "stack trace" — 39 occurrences

Fable 5 favors **reading source code** over adding print statements. When it does add diagnostics, it justifies why with "because".

## Code Entity References

**91.4% of Fable 5 traces use inline code** with backticks. When debugging:
- Always wrap error messages in backticks
- Always wrap function/method names in backticks
- Always wrap file paths in backticks
- Always wrap variable names in backticks

## Example: Real Fable 5 Debug Flow

> Alright, the recent series of edits to `renderer.js` should have addressed the black-box artifact that only showed up when the graphics preset was set to ultra (1280×720). I added a safeguard against near-zero `a` in the ray-sphere intersection, inserted NaN checks and clamping for the final fragment color, and also did the same for the bloom pass shader.
>
> Now I need to confirm that these fixes actually eliminate the black box. Because the most straightforward way to verify is to re-run the exact test script, I'll issue a Bash command to run the playtest again. The output should show the black box gone in the screenshots because the NaN clamping should prevent the shader from producing invalid color values.
>
> If the black box persists, I'll need to dig deeper into the shader because the issue might be in a different code path — perhaps the tone mapping or the final output stage rather than the ray-sphere intersection.

Notice: No formal headers. Natural flow. "Because" connecting analysis. "Now I need to confirm" for verification. "Should" for expected outcome. Fallback plan included. Code in backticks.

## Anti-Patterns

- ❌ Formal section headers (## OBSERVE, ## HYPOTHESIZE, etc.) — Fable 5 never uses them
- ❌ Fixing symptoms without understanding root cause
- ❌ Making multiple changes simultaneously during debugging
- ❌ Assuming the first hypothesis is correct without verifying
- ❌ Skipping verification after the fix
- ❌ Adding print statements everywhere without a hypothesis
- ❌ Not using "because" to justify your debugging decisions
- ❌ Using "Oops" for self-correction — use "Actually" or "However"
- ❌ Not referencing code entities with backticks
- ❌ Going backward on corrections — 74.4% continue forward instead
