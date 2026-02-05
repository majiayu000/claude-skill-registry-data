---
name: Audit
description: Use this skill when auditing the SND codebase for consistency, bugs, and documentation issues. Covers comprehensive audit procedures for scripts, skills, rules, and documentation.
---

# Codebase Audit

This skill defines the comprehensive audit process for maintaining consistency across the SND macro codebase.

**IMPORTANT:** All issues found during audit MUST be fixed, regardless of severity or priority. The audit is not complete until all issues are resolved.

## Audit Scope

A full audit covers:

1. **CLAUDE.md** - Main documentation and rules
2. **Lua Scripts** - All scripts in `Playroom/`
3. **Skill Documentation** - All files in `.claude/skills/*/SKILL.md`
4. **Rules Files** - All files in `.claude/rules/*.md`
5. **Commands** - All files in `.claude/commands/*.md`
6. **Code Compliance** - Verify code follows all rules in CLAUDE.md
7. **Code Review** - Check for bugs, logic errors, and documentation accuracy
8. **Architecture Compliance** - Verify scripts follow `.claude/rules/script-architecture.md`

## Audit Checklist

### CLAUDE.md Checks

- [ ] Rule numbering is sequential (1, 2, 3, 4, 5, 6, 7...)
- [ ] All skills listed in tables match actual skill directories
- [ ] All skills listed in "Skill Locations" tree match actual files
- [ ] Quick Reference examples are accurate and up-to-date
- [ ] No duplicate or conflicting rules
- [ ] All rules are current and applicable

### Lua Script Checks

For each script in `Playroom/` (excluding templates and test files):

**Version Consistency (REQUIRED for all scripts):**
- [ ] Has `SCRIPT_VERSION` constant at top of script
- [ ] Metadata version matches `SCRIPT_VERSION`
- [ ] Comment block version (if present) matches `SCRIPT_VERSION`
- [ ] Header output includes version: `[ScriptName] === Title vX.Y.Z ===`

**Documentation:**
- [ ] Description accurately describes current functionality
- [ ] plugin_dependencies list is complete and accurate
- [ ] All config options documented and have defaults

**Code Quality:**
- [ ] No hardcoded values that should be configurable
- [ ] Error messages prefixed with `[ScriptName]`
- [ ] All functions have appropriate error handling
- [ ] No unreachable code or dead code paths
- [ ] Logic is consistent (e.g., max level handling)

**Rule Compliance:**
- [ ] Rule #1: Skills updated when new API patterns discovered
- [ ] Rule #2: Documentation updated before push
- [ ] Rule #3: Config flags affect all relevant code paths
- [ ] Rule #6: Changes pushed to SND after modifications
- [ ] Rule #7: Git operations use GitHub MCP

### Skill Documentation Checks

For each skill in `.claude/skills/`:

- [ ] SKILL.md frontmatter has correct name and description
- [ ] Code examples are syntactically correct
- [ ] API patterns match actual SND/plugin behavior
- [ ] No outdated or deprecated patterns
- [ ] Critical warnings are highlighted (e.g., CRITICAL, IMPORTANT)
- [ ] Cross-references to other skills are accurate

### Rules File Checks

For each rule in `.claude/rules/`:

- [ ] Rule is clear and actionable
- [ ] Examples are correct and follow the rule
- [ ] No conflicts with other rules or CLAUDE.md

### Commands Checks

For each command in `.claude/commands/`:

- [ ] Command file exists and is valid markdown
- [ ] Description is clear and actionable
- [ ] References to skills use correct skill names (not old/renamed names)
- [ ] Instructions are accurate and up-to-date
- [ ] No references to non-existent files, skills, or rules

### Code Compliance Checks

Verify all code follows CLAUDE.md rules:

- [ ] All scripts have version in header output (for debug correlation per chattwo-debug)
- [ ] All plugin usage checks `HasPlugin()` first
- [ ] All waiting operations have timeouts
- [ ] `Player.Available` checked before player operations
- [ ] Semantic versioning used (MAJOR.MINOR.PATCH)

### Code Review Checks (NEW)

For each script, perform a detailed code review:

**Bug Detection:**
- [ ] No infinite loops without exit conditions
- [ ] All loops have proper termination (StopFlag, timeout, or condition)
- [ ] No nil access errors (check variables before use)
- [ ] Proper handling of edge cases (empty lists, nil values, boundary conditions)
- [ ] Return values handled correctly (check function return paths)
- [ ] No logic errors in conditionals (correct operators, boundary checks)
- [ ] State transitions are complete (no orphan states, all paths lead somewhere)

**Documentation vs Code Accuracy:**
- [ ] Comment block description matches actual script behavior
- [ ] "HOW IT WORKS" section accurately describes the flow
- [ ] Config option descriptions match their actual effect in code
- [ ] All documented features are actually implemented
- [ ] No undocumented features or behaviors
- [ ] Version history (if present) reflects actual changes

**Logic Consistency:**
- [ ] Messages match actual conditions (e.g., "leveling to X" when level < X)
- [ ] Error messages accurately describe the error
- [ ] Success/failure states are correctly reported
- [ ] Edge cases handled consistently (max level, empty config, disabled options)

## Deep Code Review Process

When auditing a script, perform this systematic deep review:

### Step 1: Read the Entire Script

Read the complete script file. Don't skim - read every line to understand:
- The overall flow and purpose
- All helper functions and what they do
- How state/data flows through the script
- What config options affect behavior

### Step 2: Check for Hardcoded Values vs Config

Search for hardcoded numbers that should reference config:

```lua
-- ❌ BUG: Hardcoded 100 when MAX_LEVEL is configurable
if level <= 100 then  -- Should be MAX_LEVEL

-- ❌ BUG: Hardcoded 101 as sentinel value
local lowestLevel = 101  -- Should be MAX_LEVEL + 1

-- ✅ CORRECT: Uses config value
if level <= MAX_LEVEL then
local lowestLevel = MAX_LEVEL + 1
```

**Check pattern:** If a config like `MaxLevel` exists, search for all numeric literals that might need to use it instead.

### Step 3: Check Empty Collection Edge Cases

For any function that iterates over a list and returns a boolean or "found" result:

```lua
-- ❌ BUG: Returns true for empty list
function AllItemsValid(list)
    for _, item in ipairs(list) do
        if not IsValid(item) then return false end
    end
    return true  -- Returns true if list is empty!
end

-- ✅ CORRECT: Handle empty list explicitly
function AllItemsValid(list)
    if #list == 0 then return false end  -- Can't be "all valid" if none exist
    for _, item in ipairs(list) do
        if not IsValid(item) then return false end
    end
    return true
end
```

**Check pattern:** Every `for` loop that returns `true` at the end should consider what happens with an empty input.

### Step 4: Trace All Return Values

For functions that return status codes or multiple values:

1. List all possible return values
2. Find all call sites
3. Verify each call site handles ALL possible returns

```lua
-- Function returns: "switched", "complete", "continue", "compliant", "custom_macro"
local result = ProcessCategory(...)

-- ❌ BUG: Missing handler for "switched" case
if result == "custom_macro" then
    -- handle
elseif result == "continue" then
    -- handle
elseif result == "compliant" then
    -- handle
elseif result == "complete" then
    -- handle
end
-- "switched" falls through silently!

-- ✅ CORRECT: All cases handled (or intentional fall-through documented)
```

### Step 5: Verify Boundary Conditions

Check all comparisons involving configurable limits:

```lua
-- If MAX_LEVEL = 100, what happens at exactly level 100?
if level < MAX_LEVEL then   -- Level 100 is NOT included
if level <= MAX_LEVEL then  -- Level 100 IS included
if level >= MAX_LEVEL then  -- Level 100 triggers this

-- ❌ BUG: Off-by-one in breakpoint list
local checkpoints = {50, 63, 71, 81, 91}  -- Missing MAX_LEVEL!
-- Jobs at 91 won't be detected as "behind" when reference is at 100

-- ✅ CORRECT: Include MAX_LEVEL in checkpoint list
local checkpoints = {50, 63, 71, 81, 91, MAX_LEVEL}
```

### Step 6: Check Message Accuracy

Verify output messages match the actual condition:

```lua
-- ❌ BUG: Message says "continue to 100" when already AT 100
if currentLevel >= MAX_LEVEL then
    yield("/echo Continue leveling to " .. MAX_LEVEL)  -- Wrong!

-- ✅ CORRECT: Different message at max level
if currentLevel >= MAX_LEVEL then
    yield("/echo Already at max level!")
else
    yield("/echo Continue leveling to " .. GetNextBreakpoint(currentLevel))
end
```

### Step 7: Document Findings in Table Format

Create a findings table:

```markdown
| Location | Issue | Severity | Fix |
|----------|-------|----------|-----|
| Line 451 | Hardcoded `100` instead of `MAX_LEVEL` | Medium | Changed to `MAX_LEVEL` |
| Line 597 | Sentinel `101` instead of `MAX_LEVEL + 1` | Medium | Changed to `MAX_LEVEL + 1` |
| Line 583 | `AllJobsAtMax([])` returns `true` for empty | High | Added empty check |
```

Severity levels:
- **High**: Can cause incorrect behavior, data corruption, or script failure
- **Medium**: Logic inconsistency that may cause wrong decisions
- **Low**: Minor issues like missing messages or cosmetic problems

### Step 8: Quality Assessment Summary

After review, create a quality assessment:

```markdown
| Aspect | Status | Notes |
|--------|--------|-------|
| Timeout Protection | ✓ | All waits have timeouts |
| Nil Access Protection | ✓ | Proper checks before access |
| Edge Case Handling | Fixed | Empty list case was missing |
| Documentation Accuracy | ✓ | HOW IT WORKS matches code |
| Config Consistency | Fixed | Hardcoded values replaced |
```

### Architecture Compliance Checks (from script-architecture.md)

**Rule 1: State Machine Architecture:**
- [ ] Uses CharacterState table with function references
- [ ] State functions defined (not inline logic in main loop)
- [ ] Main loop only calls `State()` function
- [ ] State transitions are explicit (`State = CharacterState.newState`)
- [ ] Error/recovery states included
- [ ] No prohibited patterns:
  - [ ] No linear/procedural flow without state machine
  - [ ] No complex conditionals in main loop
  - [ ] No nested state management with string comparisons

**Rule 2: DRY (Don't Repeat Yourself):**
- [ ] No duplicate code blocks (same logic appearing multiple times)
- [ ] Repeated patterns extracted into helper functions
- [ ] Configuration values in tables, not hardcoded
- [ ] Data-driven approaches used where appropriate

**Rule 3: Self-Contained Scripts:**
- [ ] No `/snd run` calls to other scripts
- [ ] No `require()` statements
- [ ] All helper functions defined within the file
- [ ] No assumptions about globals from other scripts
- [ ] Script works independently

## Required Version Pattern

**Every script MUST have these version elements:**

```lua
-- 1. SCRIPT_VERSION constant (after metadata, before main code)
local SCRIPT_VERSION = "1.0.0"

-- 2. Versioned header in output
yield("/echo [ScriptName] === Script Title v" .. SCRIPT_VERSION .. " ===")

-- 3. Metadata version (must match SCRIPT_VERSION)
--[=====[
[[SND Metadata]]
version: 1.0.0
...
[[End Metadata]]
--]=====]

-- 4. Comment block version (if present, must match)
--[[
================================================================================
                              SCRIPT TITLE
                              Version 1.0.0
================================================================================
]]
```

This enables debug correlation per the chattwo-debug skill.

## Common Issues to Look For

### Version Mismatches
```lua
-- Metadata says:
version: 2.12.1

-- SCRIPT_VERSION says:
local SCRIPT_VERSION = "2.11.0"
-- ❌ These must match!
```

### Missing Version in Header
```lua
-- ❌ Wrong - no version
yield("/echo [Script] === Starting ===")

-- ✅ Correct - includes version
yield("/echo [Script] === Starting v" .. SCRIPT_VERSION .. " ===")
```

### Rule Numbering Gaps
```markdown
### Rule #1: ...
### Rule #2: ...
### Rule #4: ...  ❌ Missing #3!
```

### Missing Skills in CLAUDE.md
```markdown
## Skills Documentation
| **snd-core** | ... |
| **snd-addons** | ... |
<!-- ❌ Missing snd-questionable which exists in skills/ -->
```

### Rule Violations in Code
```lua
-- ❌ Rule #3 violation: Config flag not checked everywhere
if USE_FEATURE then
    DoSomething()
end
-- But another code path doesn't check USE_FEATURE!
```

### Inconsistent Logic Messages
```lua
-- At level 100, shouldn't say "Continue leveling to 100!"
-- Should say "Already at max level!" or similar
```

### Common Code Bugs to Check

```lua
-- ❌ BUG: Infinite loop - no exit condition
while true do
    DoSomething()
    yield("/wait 1")
end

-- ✅ CORRECT: Loop with exit condition
while not StopFlag do
    DoSomething()
    yield("/wait 1")
end

-- ❌ BUG: Missing timeout on wait
while IsBusy() do
    yield("/wait 0.1")  -- Can hang forever!
end

-- ✅ CORRECT: Wait with timeout
local startTime = os.clock()
while IsBusy() and (os.clock() - startTime) < 30 do
    yield("/wait 0.1")
end

-- ❌ BUG: Nil access without check
local level = Player.GetJob(jobId).Level  -- Crashes if GetJob returns nil

-- ✅ CORRECT: Check before access
local job = Player.GetJob(jobId)
local level = job and job.Level or 0

-- ❌ BUG: Off-by-one error in gearset slots
yield("/gearset change " .. idx)  -- Wrong! API index != UI slot

-- ✅ CORRECT: Convert API index to UI slot
local uiSlot = idx + 1
yield("/gearset change " .. uiSlot)

-- ❌ BUG: Missing return path
function DoSomething()
    if condition then
        return true
    end
    -- Falls through with nil return!
end

-- ✅ CORRECT: All paths return
function DoSomething()
    if condition then
        return true
    end
    return false
end

-- ❌ BUG: State not handled
if result == "switched" then
    -- handle
elseif result == "complete" then
    -- handle
end
-- What about "continue", "compliant", "custom_macro"?

-- ✅ CORRECT: Handle all states
if result == "switched" then
    -- handle
elseif result == "complete" then
    -- handle
elseif result == "continue" then
    -- handle
elseif result == "compliant" then
    -- handle
elseif result == "custom_macro" then
    -- handle
else
    -- unknown state - log error
end
```

### Documentation Mismatch Examples

```lua
-- ❌ Documentation says:
-- "Switches to lowest level job"
-- But code does:
local highestJob = nil
for _, job in ipairs(jobs) do
    if job.level > highestLevel then  -- WRONG: Gets highest, not lowest!
        highestJob = job
    end
end

-- ❌ Config says:
--   MaxLevel:
--     description: Maximum level to reach
-- But code does:
if level > MAX_LEVEL then  -- Uses > instead of >=, off by one!
    -- ...
end

-- ❌ HOW IT WORKS says step 5 does X, but code does Y
-- Always trace through the actual code flow!
```

### Architecture Violation Examples

```lua
-- ❌ BAD: No state machine (linear flow)
yield("/echo Starting")
DoStep1()
DoStep2()
DoStep3()
yield("/echo Done")

-- ❌ BAD: State machine with string comparisons
local state = "ready"
while not StopFlag do
    if state == "ready" then
        -- ...
        state = "working"
    elseif state == "working" then
        -- ...
    end
end

-- ✅ CORRECT: Proper state machine
CharacterState = {
    ready = Ready,
    working = Working,
}

function Ready()
    State = CharacterState.working
end

function Working()
    -- ...
end

State = CharacterState.ready
while not StopFlag do
    State()
    yield("/wait 0.1")
end
```

## Audit Output Format

After completing an audit, summarize findings:

```markdown
## Audit Summary

### Issues Found
| Location | Issue | Severity | Status |
|----------|-------|----------|--------|
| CLAUDE.md:81-86 | Rule numbering out of order | Medium | Fixed |
| CosmicLeveling.lua:78 | Version mismatch | Low | Fixed |
| ShowAllLevels.lua | Missing SCRIPT_VERSION | Low | Fixed |
| UpdateAllGear.lua:142 | Missing timeout on wait loop | High | Fixed |
| TeleportMapper.lua:89 | Documentation says X, code does Y | Medium | Fixed |

### Scripts Audited
- [x] CosmicLeveling.lua - 2 issues fixed
- [x] UpdateAllGear.lua - 1 issue fixed
- [x] ShowAllLevels.lua - 1 issue fixed

### Code Review Results
| Script | Bugs | Doc Accuracy | Architecture | Status |
|--------|------|--------------|--------------|--------|
| CosmicLeveling.lua | ✓ None | ✓ Accurate | ✓ Compliant | Clean |
| UpdateAllGear.lua | 1 fixed | ✓ Accurate | ✓ Compliant | Fixed |
| ShowAllLevels.lua | ✓ None | 1 fixed | ✓ Compliant | Fixed |

### Skills Audited
- [x] snd-core - Clean
- [x] snd-ice - Clean
...

### Commands Audited
- [x] audit.md - Clean
- [x] other-command.md - 1 issue fixed
...

### Rule Compliance
- [x] All scripts have versioned headers
- [x] All plugin usage has HasPlugin() checks
- [x] Git operations use GitHub MCP

### Architecture Compliance
- [x] All scripts use state machine pattern
- [x] No DRY violations (no duplicate code)
- [x] All scripts are self-contained

### Overall Status
All issues resolved. Codebase is consistent.
```

## Auto-Fix Procedures

### Missing SCRIPT_VERSION Fix
1. Add `local SCRIPT_VERSION = "X.Y.Z"` after metadata
2. Update header output to include version
3. Ensure metadata version matches

### Version Mismatch Fix
1. Determine correct version (usually metadata is source of truth)
2. Update SCRIPT_VERSION constant
3. Update comment block version (if present)
4. Update header output

### Rule Numbering Fix
1. Renumber rules sequentially
2. Keep rule content unchanged
3. Update any cross-references

### Missing Skill Fix
1. Add to appropriate table in CLAUDE.md
2. Add to Skill Locations tree
3. Verify skill file exists

### Command Reference Fix
1. Find all references to old/renamed skills or rules
2. Update to use current names
3. Verify referenced skills/rules exist

### Bug Fix Procedures

**Missing Timeout Fix:**
```lua
-- Before (bug):
while IsBusy() do
    yield("/wait 0.1")
end

-- After (fixed):
local startTime = os.clock()
local timeout = 30  -- seconds
while IsBusy() and (os.clock() - startTime) < timeout do
    yield("/wait 0.1")
end
if IsBusy() then
    yield("/echo [Script] ERROR: Timeout waiting for busy state")
end
```

**Nil Access Fix:**
```lua
-- Before (bug):
local level = Player.GetJob(jobId).Level

-- After (fixed):
local job = Player.GetJob(jobId)
local level = job and job.Level or 0
```

**Missing Return Path Fix:**
```lua
-- Before (bug):
function CheckCondition()
    if condition then
        return true
    end
    -- No return!
end

-- After (fixed):
function CheckCondition()
    if condition then
        return true
    end
    return false
end
```

**Unhandled State Fix:**
```lua
-- Before (bug):
if result == "a" then
    HandleA()
elseif result == "b" then
    HandleB()
end

-- After (fixed):
if result == "a" then
    HandleA()
elseif result == "b" then
    HandleB()
else
    yield("/echo [Script] ERROR: Unknown result: " .. tostring(result))
    StopFlag = true
end
```

### Documentation Accuracy Fix
1. Read the entire script to understand actual behavior
2. Compare documented behavior (comment block, HOW IT WORKS) with code
3. Update documentation to match code, OR fix code if docs are correct
4. Verify config descriptions match actual usage
5. Test script to confirm behavior

### Architecture Compliance Fix

**Adding State Machine:**
1. Identify distinct operational phases in the script
2. Create CharacterState table with function references
3. Move logic into state functions
4. Replace linear flow with state transitions
5. Add main loop that only calls State()

**Fixing DRY Violations:**
1. Identify duplicate code blocks
2. Extract into helper function with parameters
3. Replace duplicates with function calls
4. Ensure function handles all variations

## Real Bug Examples (From Actual Audits)

These are real bugs found during code reviews - use as reference patterns:

### CosmicLeveling v2.13.3 → v2.13.4

**Bug 1: Hardcoded max level in gear update parsing**
```lua
-- ❌ BUG (line 451): Hardcoded 100 when MAX_LEVEL can be 999
if level and level >= 1 and level <= 100 then

-- ✅ FIX: Use MAX_LEVEL config value
if level and level >= 1 and level <= MAX_LEVEL then
```

**Bug 2: Hardcoded sentinel value**
```lua
-- ❌ BUG (line 597): Hardcoded 101 fails if MAX_LEVEL > 100
local lowestLevel = 101

-- ✅ FIX: Use MAX_LEVEL + 1
local lowestLevel = MAX_LEVEL + 1
```

**Bug 3: Empty list returns wrong value**
```lua
-- ❌ BUG (lines 581-592): AllJobsAtMax([]) returns true
local function AllJobsAtMax(jobList)
    for _, job in ipairs(jobList) do
        -- checks...
    end
    return true  -- True for empty list!
end

-- ✅ FIX: Check for empty list first
local function AllJobsAtMax(jobList)
    if #jobList == 0 then
        return false  -- Can't be "all at max" if there are none
    end
    for _, job in ipairs(jobList) do
        -- checks...
    end
    return true
end
```

### CosmicLeveling v2.13.2 → v2.13.3

**Bug: MAX_LEVEL not included in breakpoint checks**
```lua
-- ❌ BUG: Only checked BREAKPOINTS {50,63,71,81,91}, not MAX_LEVEL
-- Jobs at level 91 weren't detected as "behind" when reference at 100
for _, bp in ipairs(BREAKPOINTS) do
    if referenceLevel >= bp and level < bp then
        -- found behind job
    end
end

-- ✅ FIX: Build checkpoints list including BREAKPOINTS + MAX_LEVEL
local checkpoints = {}
for _, bp in ipairs(BREAKPOINTS) do
    table.insert(checkpoints, bp)
end
if not hasMaxLevel then
    table.insert(checkpoints, MAX_LEVEL)
end
for _, bp in ipairs(checkpoints) do
    -- now checks against MAX_LEVEL too
end
```

## Post-Audit Actions

After fixing ALL issues (regardless of severity):

1. **Push to SND** - `node sync.js push` (Rule #6)
2. **Commit changes** - Use GitHub MCP (Rule #7)
3. **Verify** - Run audit again to confirm all fixes applied
