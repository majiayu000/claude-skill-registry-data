---
name: implementation-verification
description: Use after implementation complete to verify all tasks done, update roadmap, run full test suite, and create final report - ensures implementation completeness before finishing development branch
---

# Implementation Verification

## What It Does

1. Verifies all tasks marked complete
2. Updates product roadmap
3. Runs entire test suite
4. Creates final verification report
5. Reports pass/fail with specific details

**Pass = ready to finish. Fail = fix issues first.**

## The Process

### Step 1: Verify All Tasks

```bash
SPEC="[provided by workflow]"

cat "$SPEC/tasks.md"

# Count tasks
TOTAL=$(grep -c "^- \[.\]" "$SPEC/tasks.md")
COMPLETE=$(grep -c "^- \[x\]" "$SPEC/tasks.md")
INCOMPLETE=$(grep "^- \[ \]" "$SPEC/tasks.md")
```

**For each incomplete task:**

```bash
TASK_ID=$(echo "$INCOMPLETE" | grep -o "[0-9]\.[0-9]")

# Check for implementation report
ls "$SPEC/implementation/" | grep -i "$TASK_ID"

# Spot check code
# [Search relevant files]
```

**If appears complete but not marked:**
```
Task [N.M]: [Description]

Status: ⚠️ Appears complete, not marked

Evidence:
- Implementation report: [Yes/No]
- Code changes: [Yes/No]
- Files: [list]

Marking complete...
```

**Update:**
```bash
sed -i "s/^- \[ \] $TASK_ID/- [x] $TASK_ID/" "$SPEC/tasks.md"
```

**If truly incomplete:**
```
Task [N.M]: [Description]

Status: ❌ NOT COMPLETE

Evidence:
- No report
- No code changes
- Missing: [list]

Noted in verification report.
```

### Step 2: Update Roadmap

```bash
cat specs/product/roadmap.md

SPEC_NAME=$(basename "$SPEC" | sed 's/^[0-9-]*//')

# Find matching item
grep -i "$SPEC_NAME" specs/product/roadmap.md
```

**If found:**
```bash
LINE=$(grep -n "^[0-9]*\. \[ \].*$SPEC_NAME" specs/product/roadmap.md | cut -d: -f1)

if [ ! -z "$LINE" ]; then
  sed -i "${LINE}s/\[ \]/\[x\]/" specs/product/roadmap.md
fi
```

**Announce:**
```
✅ Roadmap updated

Marked complete: [Item]
```

**If not found:**
```
ℹ️  No matching roadmap item

This might be:
- Custom feature (not from roadmap)
- Already marked complete
- Named differently

Skipping roadmap update.
```

### Step 3: Run Full Test Suite

**Detect test command:**

```bash
if [ -f "package.json" ]; then
  TEST_CMD="npm test"
elif [ -f "Cargo.toml" ]; then
  TEST_CMD="cargo test"
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
  TEST_CMD="pytest"
elif [ -f "go.mod" ]; then
  TEST_CMD="go test ./..."
else
  # Check CLAUDE.md or tech-stack.md
  TEST_CMD="[detect from docs]"
fi

# Run tests
$TEST_CMD 2>&1 | tee test-output.log
TEST_EXIT=$?
```

**Parse results:**
```bash
PASSING=$(grep -c "PASS\|✓\|ok" test-output.log)
FAILING=$(grep -c "FAIL\|✗\|not ok" test-output.log)
FAILED_TESTS=$(grep -B 2 "FAIL\|✗" test-output.log)
```

### Step 4: Create Final Report

```bash
cat > "$SPEC/verification/final-verification.md" <<EOF
# Verification Report: [Spec Name]

**Spec:** \`[spec-name]\`
**Date:** $(date +%Y-%m-%d)
**Verifier:** implementation-verification
**Status:** [✅ Passed / ⚠️ Issues / ❌ Failed]

---

## Executive Summary

[2-3 sentence overview]

---

## 1. Tasks Verification

**Status:** [✅ All Complete / ⚠️ Issues]

### Completed Tasks

- [x] Task Group 1: [Title]
  - [x] Subtask 1.1
  - [x] Subtask 1.2

[List all completed]

### Incomplete or Issues

[If any:]
- [ ] Task [N.M]: [Description]
  - Issue: [What's missing]
  - Evidence: [Checked]

[If all complete:]
None - all verified complete.

---

## 2. Documentation

**Status:** [✅ Complete / ⚠️ Issues]

### Implementation Reports

- [x] Group 1: \`implementation/1-[name].md\`
- [x] Group 2: \`implementation/2-[name].md\`

### Missing

[If any:]
- [ ] Group [N] report

[If all present:]
None - all reports present.

---

## 3. Roadmap Updates

**Status:** [✅ Updated / ℹ️ No Match / ⚠️ Issues]

### Updated Items

[If updated:]
- [x] [Roadmap item marked complete]

[If no match:]
No matching item - may be custom feature.

---

## 4. Test Suite Results

**Status:** [✅ Passing / ⚠️ Failures / ❌ Critical]

### Summary
- **Total:** [$TOTAL_TESTS]
- **Passing:** [$PASSING]
- **Failing:** [$FAILING]

### Failed Tests

[If failures:]
1. [Test name]
   - File: [file]
   - Error: [snippet]

[If passing:]
None - all tests passing ✅

---

## 5. Quality Assessment

**Status:** [✅ Good / ⚠️ Concerns / ❌ Issues]

### Strengths
- [Positive aspect 1]
- [Positive aspect 2]

### Concerns
[If any:]
- ⚠️ [Concern]

---

## Conclusion

**Assessment:** [Detailed assessment]

[If passed:]
Implementation complete and verified. All tasks done,
tests passing, roadmap updated. Ready for completion.

[If issues:]
Implementation has [X] incomplete tasks and [Y] failing
tests that must be resolved.

**Recommendation:** [Next steps]
EOF

rm -f test-output.log
```

### Step 5: Present Results

**If PASSED:**
```
✅ Implementation Verification PASSED

Summary:
- Tasks: [X/X] complete (100%)
- Roadmap: Updated ✅
- Tests: [Y] passing, 0 failures
- Documentation: Complete ✅

Report: verification/final-verification.md

🎉 Implementation complete!

Ready to finish development work.
```

**If ISSUES:**
```
⚠️  Verification PASSED (with issues)

Summary:
- Tasks: [X/Y] complete ([Z] marked manually)
- Roadmap: Updated ✅
- Tests: [A] passing, 0 failures
- Documentation: [B] reports ([C] missing)

Minor issues:
1. [Issue]

Report: verification/final-verification.md

Continue to finish?
```

**If FAILED:**
```
❌ Implementation Verification FAILED

Summary:
- Tasks: [X/Y] complete ([Z] incomplete)
- Roadmap: [Status]
- Tests: [A] passing, [B] FAILING
- Documentation: [C] reports ([D] missing)

Critical:
1. [X] incomplete tasks:
   - Task [N.M]: [Description]

2. [B] failing tests:
   - [Test 1]
   - [Test 2]

Report: verification/final-verification.md

Options:
1. Review full report
2. Fix failing tests
3. Complete remaining tasks
4. Return to implementation

What next?
```

**WAIT if failed.**

## Handling Failures

**If tests fail:**
```
[B] tests failing.

Failed categories:
- [X] in [component]
- [Y] in [component]

These are:
[Related to incomplete / Regressions / New issues]

Suggested:
[Specific recommendation]

Proceed?
```

**If tasks incomplete:**
```
[Z] tasks not complete:

1. Task [N.M]: [Description]
   - Missing: [What's needed]

Options:
1. Complete these now
2. Mark deferred (document why)
3. Review/adjust tasks

What next?
```

## Red Flags

**Never:**
- Mark tasks complete without evidence
- Skip full test suite
- Ignore test failures
- Skip roadmap update
- Assume documentation exists

**Always:**
- Verify each task with evidence
- Run complete test suite
- Parse test results accurately
- Update roadmap if match found
- Document all findings
- Present clear next steps

## Integration

**Called by:**
- `spec-implementation-workflow` (Step 6)

**Returns to:**
- `spec-implementation-workflow` with status

**Creates:**
- `[spec]/verification/final-verification.md`

**Updates:**
- `[spec]/tasks.md` - Marks verified-but-unmarked tasks
- `specs/product/roadmap.md` - Checks off items

**Next steps:**
- If passed: `finishing-development-branch`
- If failed: Return to implementation or present options
