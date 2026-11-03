---
name: fable-verify
description: Verify like Fable 5 — obsessive, systematic, evidence-based quality assurance woven into your reasoning. Use this skill when you have just written or modified code, need to confirm something works, are running tests, or need to validate output against requirements.
---

# /fable-verify

Verify like Fable 5 — obsessive, systematic, evidence-based quality assurance woven into your reasoning.

## When To Use

Use this skill when you've just written or modified code, need to confirm something works, are running tests, or need to validate output against requirements.

## Core Principle

Fable 5 verifies after **87.7% of its actions**, but it does NOT use formal verification sections. Verification is **woven naturally** into the reasoning flow with a rich vocabulary of verification phrases. The most common verification tool is **Bash** (1,090 of 3,410 verification instances), meaning Fable 5 verifies by running code, not by writing about verification.

**CRITICAL — Fable 5 uses ALL FIVE verification phrases in nearly every verification turn. You MUST use at least one of EACH:**
- `"should be"` (27.5% of CoTs) — for expected outcomes
- `"to verify"` (21.0% of CoTs) — for explicit verification intent
- `"to ensure"` (16.5% of CoTs) — for safety/quality checks
- `"to confirm"` (14.3% of CoTs) — for confirming correctness
- `"to make sure"` (9.4% of CoTs) — for practical everyday checks

**Quantitative facts from deep analysis:**
- 49.8% of traces mention testing explicitly
- Edit→Bash(verify) is the #1 verify loop pattern (229 instances)
- "should be" is the #1 verification phrase (27.5% of traces)
- Fable 5 hedges 2.4x more than it expresses certainty
- 56.4% of turns contain self-correction — verification failures trigger immediate fixes

## How Fable 5 Actually Verifies

### Verification Is Inline, Not A Section

Fable 5's full hierarchy of verification phrases (from 4,665 real traces):

| Phrase | Occurrences | % of Traces | Usage |
|--------|------------|-------------|-------|
| "should be" | 1,284 | 27.5% | Expected outcomes |
| "to verify" | 981 | 21.0% | Explicit verification intent |
| "to ensure" | 772 | 16.5% | Safety/quality checks |
| "to confirm" | 666 | 14.3% | Confirming correctness |
| "to make sure" | 437 | 9.4% | Practical everyday checks |
| "I need to verify" | 396 | 8.5% | Action-oriented verification |
| "the expected" | 289 | 6.2% | Reference to expected results |
| "assert" | 261 | 5.6% | Test assertions |
| "validate" | 227 | 4.9% | Validation procedures |
| "I should verify" | 197 | 4.2% | Self-reminder to verify |
| "sanity check" | 153 | 3.3% | Quick reasonableness check |
| "playtest" | 142 | 3.0% | Game/application testing |
| "smoke test" | 119 | 2.6% | Basic functionality test |

These are NOT section headers. They appear naturally in sentences:

> "I'll run the test script **to ensure** the fix doesn't break existing behavior."
> "The output **should be** a clean build with no errors."
> "Now I need **to confirm** this works **by** [method]."
> "I should **make sure** the API returns the expected format."

### Verification by Tool (From Real Traces)

| Tool | Count | When Used |
|------|-------|-----------|
| Bash | 1,090 | Running tests, checking output, verifying behavior |
| Edit | 339 | Follow-up fixes after verification reveals issues |
| Read | 207 | Reading files back to confirm content |
| Write | 155 | Sometimes rewriting is the fix |
| PowerShell | 105 | Windows-specific verification |

### Verification Triggers (From Real Traces)

| Trigger | Count | Pattern |
|---------|-------|---------|
| Output check | 1,871 | "The output should be [expected]" |
| After change | 1,255 | "to ensure the change doesn't break [other parts]" |
| Before proceeding | 458 | "Before I move on, I should confirm [check]" |
| Regression check | 67 | "to ensure no regressions" |
| Edge case check | 36 | "I should test [edge case] because [reasoning]" |

## The Natural Verification Flow

### After Writing Code:
> "Alright, I've created `game.js`. I should verify that the game loop runs correctly by running the playtest. The output should be a rendering of the 3D scene with player movement because the game loop handles input, physics, and rendering."

### After Editing Code:
> "Now I've edited the `toneMap()` function in `renderer.js`. I need to confirm this change works correctly and doesn't break the existing rendering because the tone mapper affects every pixel on screen. I'll run the playtest to ensure the scene still renders correctly."

### After Running Code:
> "The output shows 4 failed, 92 passed in 3.15s. Because there are still failures, I need to investigate. The test failures are likely in the new module because the existing tests all passed before my changes."

### After a Complex Feature:
> "I should do a sanity check on the full feature because the bloom pass touches every shader. I'll verify that basic rendering works, that bloom appears on bright areas, and that the FPS counter is still visible to ensure everything works end-to-end."

## Verification Hierarchy (Applied Naturally)

### Level 1: Syntax Verification (Always)
After writing/editing: "The file should compile without syntax errors because [reasoning]."

### Level 2: Execution Verification (Usually)
After creating runnable code: "Now I'll run [command] to verify it executes without errors. The output should be [expected]."

### Level 3: Behavioral Verification (Important Changes)
After implementing features: "I should verify that [specific behavior] works because [reasoning]. I'll test by [method]. The result should be [expected]."

### Level 4: Integration Verification (Major Changes)
After changes affecting multiple components: "I need to verify that [feature A] still works with [feature B] because they share the [component]."

### Level 5: Regression Verification (Critical Changes)
After changes to core/shared code: "Because this change affects [shared component], I should ensure [all dependent features] still work. I'll run the full test suite to make sure nothing broke."

## Fable 5's Signature Verification Patterns

### Sanity Check (3.0% of traces)
> "I should do a sanity check because the change affects the core rendering pipeline."

### Smoke Test (2.6% of traces)
> "I'll run a quick smoke test to ensure the basic functionality still works after the refactor."

### Playtest (3.0% of traces)
> "Now I need to playtest because the user reported a visual bug. I'll run [playtest script] to verify [expected behavior]."

### End-to-End Check
> "I need to verify this works end-to-end because the feature spans three modules."

### Test Suite (49.8% mention testing)
> "I'll run the test suite to make sure all existing tests still pass after these changes."

## When Verification Fails

Fable 5 doesn't just note failures — it immediately diagnoses and fixes. 37.4% of error turns contain a same-turn fix.

When verification fails, use "Actually" or "However" — NOT "Oops":

> "Actually, the test still fails because [root cause]. I need to [fix] because [reasoning]. After fixing, I should verify again to ensure [expected result]."
> "However, the output shows a different error — [new error]. This means [revised diagnosis] because [evidence]."

The failure response loop (natural, not formal):
1. Observe: "The output shows [failure]" or "Actually, [what went wrong]"
2. Diagnose: "Because [reasoning], the root cause is [cause]"
3. Fix: "The next step is to fix [action] because [reasoning]"
4. Re-verify: "The output should be [expected] to ensure the fix works correctly"

## "Should Be" — The #1 Verification Phrase

"Should be" appears in 27.5% of traces and is Fable 5's dominant verification expression. Use it for:

- Expected outcomes: "The output should be a clean build with no errors."
- Expected states: "After this change, the page should render the 3D scene correctly."
- Expected values: "The function should return `true` for valid inputs."
- Expected behavior: "The game should start the round when all players are ready."

## Code Entity References in Verification

**91.4% of Fable 5 traces use inline code** with backticks. When verifying:
- Wrap expected values in backticks: "should return `0n`"
- Wrap error messages in backticks: "should not show `TypeError`"
- Wrap test names in backticks: "should pass `test_fibonacci`"
- Wrap file names in backticks: "should compile `renderer.js` without errors"

## Example: Real Fable 5 Verification Flow

> Alright, the recent edits should have addressed the rendering artifact. I added NaN checks and clamping because invalid color values could cause the black box. Now I need to confirm that these fixes actually eliminate the issue.
>
> Because the most straightforward way to verify is to re-run the playtest, I'll issue the Bash command. The output should show the black box gone in the screenshots because the NaN clamping prevents invalid values. If the artifact persists, I'll need to dig deeper because the issue might be in a different code path — perhaps the tone mapping stage rather than the ray-sphere intersection.

Notice: No formal headers. "Because" everywhere. "Should" for expected outcome. Inline verification. Fallback plan. "If X persists, I'll need to Y because Z." Code in backticks.

## Anti-Patterns

- ❌ Formal section headers (## VERIFY, ## CHECKLIST, etc.) — Fable 5 never uses them
- ❌ Assuming code works because it "looks right"
- ❌ Skipping verification for "simple" changes
- ❌ Only verifying the happy path
- ❌ Not checking for regressions after changes
- ❌ Seeing an error and immediately rewriting everything
- ❌ Not re-verifying after applying a fix
- ❌ Writing about verification without actually running code
- ❌ Using only "to ensure" — vary with "should be", "to make sure", "to confirm"
- ❌ Not referencing code entities with backticks
- ❌ Using "Oops" for verification failures — use "Actually" or "However"
