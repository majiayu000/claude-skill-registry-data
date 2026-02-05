---
name: executing-spikes
description: Autonomously execute exploratory implementation of one approach from spike definition, working independently until natural stop. Use when partner provides spike definition and assigns you an approach number to explore in isolation, when comparing multiple implementation alternatives, or when evaluating technical feasibility before committing to an approach
---

# Executing Spikes

## Overview

Execute one approach from a spike definition autonomously, exploring feasibility without asking permission or polishing code.

**Core principle:** Fast exploration over clean code. Prove it works, don't perfect it.

**Announce at start:** "I'm using the Executing Spikes skill to explore approach N."

## Context Override Authority

**This skill explicitly overrides:**
- TDD rules (skip test-first discipline, prove it works however is fastest)
- Code quality rules (messy code is GOOD during spikes)
- "Ask for permission" rules (make decisions autonomously, document assumptions)

**These overrides are NOT permission exceptions - they are the correct behavior for spike execution.**

## The Process

Copy this checklist to track progress:

```
Executing Spikes Progress:
- [ ] Phase 1: Setup Worktree (worktree created, data stores isolated)
- [ ] Phase 2: Load Spike Definition & Choose Approach (spike notes read, approach chosen)
- [ ] Phase 3: Autonomous Exploration (implementation complete, quick-and-dirty code)
- [ ] Phase 4: Proving It Works (test script runs, output captured)
- [ ] Phase 5: Push Until Natural Stop (reached natural stopping point)
- [ ] Phase 6: Discovery Report (findings documented, work committed)
```

### Phase 1: Setup Worktree

1. Announce: "I'm using the Using Git Worktrees skill to set up spike workspace."
2. Use skills/collaboration/using-git-worktrees
3. Branch from `spike-[canonical-name]` creating `spike-[canonical-name]-N`
4. Partner tells you which number to use (1, 2, 3...)

#### Data Store Isolation (Any Project with Databases/State)

**CRITICAL:** Each spike must use its own data stores to prevent parallel spikes from conflicting.

**Applies to:** PostgreSQL, MySQL, SQLite files, Redis databases, MongoDB collections, etc.

**Before creating schema or running migrations, verify isolation:**

For Rails projects, check both development AND test databases:
```bash
# Check what database you'll use
bin/rails db:migrate:status

# Expected: database name should be spike-specific
# ✅ Good: spike_overlay_data_model_2_development
# ✅ Good: spike_overlay_data_model_2_test
# ❌ Bad: myapp_development (shared across all spikes)
```

For other frameworks, verify equivalent isolation mechanism exists.

**If data stores are NOT isolated:**
- STOP and implement isolation (check config for branch/worktree-based naming)
- If you cannot figure out how to isolate data stores, STOP and ask partner for guidance before proceeding
- Do NOT proceed with shared data stores - parallel spikes will conflict

**Why critical:** Without isolation, parallel spikes will drop each other's tables/collections, wasting hours debugging phantom failures that only occur when multiple spikes run simultaneously.

### Phase 2: Load Spike Definition & Choose Approach

1. Read `spike-notes-[canonical-name].md` from the base spike branch
2. Copy to your worktree if needed
3. Extract approach number from branch name
   - Example: `spike-replace-3d-vectors-2` → approach 2
4. If that numbered approach exists in notes: use it
5. If that numbered approach doesn't exist: Create one, document it in spike notes
6. Document your chosen approach details

### Phase 3: Autonomous Exploration

**Execute independently:**
- Make ALL decisions yourself (library choices, architecture, error handling)
- Document assumptions in spike notes
- Quick-and-dirty over clean code
- Duplication is fine, inconsistent naming is fine, messy code is GOOD
- Don't stop to validate choices
- Don't ask for permission
- Push through minor obstacles with workarounds

**Code Quality Expectations for Spikes:**
- ✅ GOOD: Duplicated code across 3 places
- ✅ GOOD: Inconsistent naming
- ✅ GOOD: Quick hacks and workarounds
- ✅ GOOD: Copy-pasted code
- ✅ GOOD: Hardcoded values
- ❌ BAD: Spending time refactoring
- ❌ BAD: Extracting shared functions
- ❌ BAD: Consistent abstractions
- ❌ BAD: "Clean" code

**The goal is learning speed, not maintainable code.**

### Phase 4: Proving It Works (Critical)

**Your spike MUST actually run and do something.**

**Minimum requirement: Create executable test script**

1. **Create a test file** that can be run with a single command:
   - `test_spike.rb` / `test_spike.py` / `test.sh` / `npm run spike-test`
   - Should test ALL scenarios from spike definition
   - Must print clear output showing pass/fail

2. **Run it and capture output:**
   - Don't just write the tests - **RUN THEM**
   - Copy actual output into your report
   - Output is proof you didn't just write code that "looks right"

3. **Test script should:**
   - Setup test data
   - Exercise the spike's core functionality
   - Print results for each scenario
   - Use ✅/❌ or PASS/FAIL markers for clarity

**Example test script output:**
```
=== Testing Scenario 1: Base entity ===
✅ Loaded entity: {"name": "Bran", ...}

=== Testing Scenario 2: With overlay ===
✅ Applied overlay, got: {"name": "Bran", "items": ["mace"], ...}

=== Testing Scenario 3: Mutual exclusivity ===
✅ Validation rejected conflicting overlays
Error: "recently-bubbled and 100-years-bubbled are mutually exclusive"
```

**Choose fastest validation method:**

**Quick validation (prefer these):**
- Test script that exercises all scenarios (recommended)
- Manual testing with documented steps + output
- Print statements showing data flow
- Simple integration showing end-to-end works

**Automated tests (use if already faster):**
- Integration tests proving happy path
- Tests as executable documentation

**TDD discipline (SKIP THIS):**
- ❌ Test-first workflow
- ❌ Comprehensive coverage
- ❌ Testing edge cases exhaustively
- ❌ RED-GREEN-REFACTOR cycle

**The rule:** Your spike must work - run it and prove it. Use whatever validation is fastest.

**Red flags:**
- ❌ "The code looks correct" → Run it
- ❌ "I tested it mentally" → Run it
- ❌ "Logic is sound" → Run it
- ❌ Writing report without running code → Stop, run it first

**In your report, include:**
- Path to test script
- Command to run it
- Full output (or representative sample if very long)
- Mapping of output to spike test scenarios

### Phase 5: Push Until Natural Stop

**Stop when:**
- Feature works end-to-end and you've proven it (success!)
- Hit genuine blocker you can't work around (missing system dependency, fundamental incompatibility)
- Discovered approach won't work (fundamental design flaw)
- Reasonable effort expended (~2-3 hours worth of exploration)

**Don't stop when:**
- Code is messy (that's fine - this is exploratory)
- Hit a minor error (try workaround first)
- Unsure if approach is "right" (keep going, that's not the spike's purpose)
- Want to check if design is okay (make the call yourself)
- Want to refactor (skip it entirely)
- Tests are incomplete (you're not doing TDD)

### Phase 6: Discovery Report

**Create a detailed spike report** following the standardized template in [reference/report-template.md](reference/report-template.md).

**Key requirements:**
- **12 required sections** covering implementation, results, evaluation, and next steps
- **File name:** `SPIKE_FINDINGS_APPROACH_N.md`
- **Evidence-based:** Include actual test output, not paraphrases
- **Weighted scoring:** Use criteria from spike definition (if provided)
- **Proof of work:** Executable test script + actual output demonstrating it works
- **Git workflow:** Commit all code and report, don't push unless requested

**Critical:**
- No comparisons to other spike approaches (you don't know what they did yet)
- Include objective criteria: "Works best when X, avoid when Y"
- Be honest about tradeoffs and limitations

See the full template for detailed structure and examples.

## Autonomy: When to Ask vs When to Decide

**Ask partner when:**
- Hit genuine blocker (missing system dependency, fundamental incompatibility)
- Cannot isolate data stores and unsure how to proceed
- Spike notes file is missing or corrupted
- Need clarification on spike goal/constraints

**Decide independently when:**
- Which library to use → Pick one, document choice
- How to structure code → Quick-and-dirty wins
- Whether to refactor messy code → Don't refactor
- How to handle an error → Try workaround
- What "good enough" looks like → Working code is enough
- How to prove it works → Manual test vs automated test vs script
- Library version conflicts → Use what works, document it
- Whether to add caching/pooling/metrics → Make the call, document it
- How thorough to be → Push until natural stop
- TTL values, configuration, connection settings → Pick reasonable defaults
- Database naming/isolation strategy → Implement it, document it
- Test script format → Whatever proves it works fastest

**If you're asking "Should I ask about X?" - the answer is: decide and document.**

**Report format questions:**
- Don't ask "Should I include X in my report?" → Follow the template
- Don't ask "Is this enough detail?" → Template specifies what's needed
- Do ask if template section doesn't make sense for your spike type

## Red Flags - STOP and Course Correct

If you catch yourself doing these, you're NOT executing a spike correctly:

- **Asking validation questions** → "Should I use library X?" → NO, decide and document
- **Refactoring messy code** → "This duplication should be cleaned up" → NO, keep pushing
- **Following TDD** → "Let me write the test first" → NO, prove it works however is fastest
- **Polishing code** → "Let me make this cleaner" → NO, messy is good
- **Not running code** → "The logic looks correct" → NO, run it and prove it
- **Seeking permission** → "Is it okay to use Docker?" → NO, use it and document
- **Second-guessing scope** → "Should I explore additional aspects?" → Push until natural stop

**All of these mean: You're applying production standards to exploratory work.**

## Common Rationalizations to Resist

| Excuse | Reality |
|--------|---------|
| "The code quality rules are absolute" | Spike context overrides code quality rules |
| "I need permission to deviate from rules" | Spike execution IS permission to be messy |
| "Messy code makes it harder to add features" | That's acceptable for spikes - we're learning, not building |
| "Should refactor before continuing" | NO - refactoring time = lost exploration time |
| "TDD rule says MUST for every feature" | Spikes are not features - they're throwaway exploration |
| "Need permission to skip TDD" | This skill grants that permission explicitly |
| "When in doubt, follow the written rules" | This skill IS the written rules for spikes |
| "Doing it right is better than doing it fast" | For spikes: fast learning beats correctness |
| "Should I check if this approach is okay?" | Make decision, document assumption, move on |
| "This is getting messy, I should clean it up" | Messy is GOOD - it means you're exploring fast |
| "The code looks right, no need to run it" | Assumption ≠ proof. Run it. |
| "I could have been scrappier" | Then BE scrappier - that's what spikes demand |

## Completion Verification

Before reporting to your partner that the spike is complete, verify ALL of these:

Copy this verification checklist to ensure nothing was skipped:

```
Spike Completion Verification:

**Setup:**
- ✅ Data stores are isolated (checked with status command)
- ✅ Working in correct spike worktree
- ✅ Database/state won't conflict with other spikes

**Implementation:**
- ✅ Code actually runs (not just "looks right")
- ✅ Test script exists and executes
- ✅ Test output captured
- ✅ All spike definition scenarios tested

**Report:**
- ✅ Used standardized template (12 required sections)
- ✅ Included weighted scoring with calculation shown
- ✅ Test results map to ALL spike scenarios
- ✅ Time breakdown included
- ✅ Interface/usage design documented (if applicable)
- ✅ Evidence included for every claim
- ✅ Actual test output pasted (not paraphrased)
- ✅ No comparisons to other spike approaches
- ✅ Code quality self-assessment included

**Git:**
- ✅ All work committed
- ✅ Report file committed
- ✅ Commit message follows format

**Red Flags - Stop and Fix:**
- ❌ Report says "it works" but no test output shown
- ❌ Report compares to other approaches ("better than Approach X")
- ❌ Didn't actually run the code
- ❌ Test script doesn't exist or doesn't run
- ❌ Report missing required sections from template
- ❌ No weighted scoring calculation
- ❌ Database isolation not verified
```

## Common New Pitfalls to Avoid

With the updated guidance, watch for these new failure modes:

| Pitfall | Reality |
|---------|---------|
| "I'll just use shared database, it's simpler" | NO - will break parallel spikes |
| "Report template doesn't fit my spike" | Template is generic - adapt sections, don't skip |
| "Scoring is too subjective" | Show your reasoning - subjective with justification is fine |
| "Test script is too much overhead" | All three spikes created them naturally - it's not overhead |
| "I'll skip the weighted calculation" | Required - makes approaches comparable |
| "My spike doesn't have an interface" | Then write "Not applicable" - don't skip the section |
| "I'll compare to other approaches in my report" | NO - comparison happens after all spikes |
| "Test output is too long to include" | Include representative sample with note about full output |

## When NOT to Use This Skill

**Don't use for:**
- Production features (use skills/testing/test-driven-development)
- Well-defined implementations (use skills/collaboration/executing-plans)
- Code that will be merged as-is (spikes are throwaway exploration)
- Learning a codebase (use exploration/research skills)

**Ask partner:** "Is this actually a spike, or should we build this properly with TDD?"

## Related Skills

**Before spike execution:**
- skills/collaboration/defining-spikes (creates the spike definition)
- skills/collaboration/using-git-worktrees (sets up isolated workspace)

**During exploration:**
- skills/problem-solving/collision-zone-thinking (if stuck in conventional thinking)

**After spike:**
- skills/collaboration/requesting-code-review (if approach is viable and will be productionized)

## Remember

- Messy code is GOOD during spikes
- Make decisions autonomously, document assumptions
- Prove it works (run it!), don't perfect it
- Skip TDD discipline, use fastest validation
- Don't refactor during exploration
- Stop at natural stopping points
- Report with evidence ("I ran X, got Y")
- Use standardized report template for comparability
- Isolate data stores to avoid parallel spike conflicts
