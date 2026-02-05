---
name: behavior-tree-validator
description: Validate py_trees behavior trees across three tiers (critical, important, advisory). Use for debugging existing BTs, diagnosing validation failures, or standalone validation.
---

## Purpose

Validate behavior trees to ensure:
- Syntactic correctness (valid Python, proper structure)
- Action availability (all actions exist in robot's action library)
- Semantic consistency (reasonable parameters, logical ordering)

---

## When to Use This Skill

1. **User reports BT not working** - Diagnose execution failures
2. **Debugging validation failures** - Understand why BT failed validation
3. **Validating manually-written BTs** - Check hand-crafted behavior trees
4. **Called by bt-composer** - Automatically during BT generation

---

## Workflow

### Step 1: Discover Available Actions

Invoke the `bt-action-discovery` skill (user-level skill in ~/.claude/skills/) to get the robot's available actions from the project's action_library.

This is needed to verify all actions in the BT exist in the action library.

---

### Step 2: Run Validation Orchestrator

```bash
python validation/orchestrator.py generated_bts/{filename}.py
```

This runs all three validation tiers and returns JSON results.

---

### Step 3: Parse JSON Output

The validation returns a structured JSON response with:
- `tier1_critical`: Must-pass checks (syntax, structure, imports)
- `tier2_important`: Should-pass checks (parameters, types, ranges)
- `tier3_advisory`: Nice-to-have checks (semantic suggestions)

---

### Step 4: Diagnose Errors

Use `validation-reference.md` (in the same directory as this SKILL.md) for:
- Complete error catalog with fixes
- Detailed tier descriptions
- Troubleshooting guide
- Individual validator usage

---

### Step 5: Provide Fixes to User

Based on tier level:
- **Tier 1 errors**: Critical - BT will not execute
- **Tier 2 warnings**: Important - may cause unexpected behavior
- **Tier 3 suggestions**: Advisory - quality improvements

---

## Validation Tiers Summary

### Tier 1: Critical (Must Pass)
- Valid Python syntax
- `create_root()` function exists and returns Behaviour
- All imports available
- All action nodes exist in action library

**Tools:** `validation/syntax_checker.py`, `validation/ros_checker.py`

---

### Tier 2: Important (Should Pass)
- Parameters within valid ranges
- Required parameters provided
- Parameter types correct

**Tools:** `validation/orchestrator.py` (constraint checking)

---

### Tier 3: Advisory (Nice to Have)
- Reasonable action ordering
- No obvious infinite loops
- No unreachable code paths

**Tools:** Manual review or future LLM-as-judge

---

## Individual Validators

Run specific validators when needed:

```bash
# Syntax and structure only
python validation/syntax_checker.py generated_bts/{filename}.py

# Action existence only
python validation/ros_checker.py generated_bts/{filename}.py

# With live ROS connection
python validation/ros_checker.py generated_bts/{filename}.py --check-live
```

---

## Debugging Workflows

### Problem: BT fails to execute

1. Run full validation orchestrator
2. Check Tier 1 errors (critical)
3. Verify `create_root()` exists
4. Check all imports are valid
5. Ensure all actions exist in action library
6. See `validation-reference.md` for error catalog

---

### Problem: BT executes but behaves unexpectedly

1. Check Tier 2 warnings (parameters)
2. Verify all parameters within valid ranges
3. Check parameter types match expectations
4. Review action ordering
5. See `validation-reference.md` for troubleshooting

---

### Problem: Validation passes but robot doesn't move correctly

1. Check Tier 3 suggestions (semantic)
2. Review action ordering logic
3. Verify pen up/down states
4. Check coordinate calculations
5. Ensure shapes are closed
6. See `validation-reference.md` for best practices

---

## How bt-composer Uses This Skill

During BT generation workflow:

1. Generate BT code
2. Write to file
3. Run validation: `python validation/orchestrator.py {file}`
4. Parse JSON output
5. Decision tree:
   - Tier 1 Fail → MUST regenerate (max 3x)
   - Tier 2 Warnings → Should fix if possible
   - Tier 3 Advisory → Informational only
6. Present to user when validation passes

---

## Detailed Reference

For complete error catalog, troubleshooting guide, and validation examples, see:

**`validation-reference.md`** (in the same directory as this SKILL.md)

This external reference includes:
- Complete validation tier descriptions
- Full error catalog with fixes
- Troubleshooting guide for common problems
- Validation JSON output format
- Individual validator usage details

---

## Notes

- **Degree of freedom: Low** - Run specific validation scripts, parse output
- **Always run full orchestrator** - Don't rely on individual validators alone
- **Fix Tier 1 first** - These prevent execution
- **Max 3 regeneration attempts** - If still failing, simplify task

---

## Related Skills

- `bt-action-discovery` - Discovers available robot actions
- `bt-composer` - Generates BTs and calls this validator
