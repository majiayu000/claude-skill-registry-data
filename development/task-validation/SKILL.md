---
name: task-validation
description: Validates task completion by checking for real implementation, working code, test results, and compliance with quality standards. Prevents paper solutions and ensures tasks are actually completed before being marked as done.
---

# Task Validation Skill

## Purpose

This skill validates that tasks are truly completed with real working implementation, not just documentation or specifications. It enforces quality standards and prevents "paper solutions."

## Usage

Invoke this skill when you need to:
- Validate task completion before marking as done
- Check if implementation is real or just documentation
- Verify working code and test results
- Ensure compliance with quality standards
- Prevent incomplete work from being marked complete

## Validation Process

### 1. File Verification
```bash
# Check claimed files exist
find .claude -name "filename.py" -type f

# Verify file content
ls -la path/to/file.py
wc -l path/to/file.py
```

### 2. Functionality Testing
```bash
# Test code execution
python script.py --help
python script.py test

# Check for errors
python -m py_compile script.py
```

### 3. Evidence Collection
- File creation proof with paths and sizes
- Working code demonstration with outputs
- Test results showing functionality
- Integration verification

### 4. Standards Compliance
- Follow task execution standards
- Proper Git workflow used
- Comprehensive testing included
- Clear documentation provided

## Validation Criteria

### ✅ PASS Criteria
- All claimed files exist with working code
- Code executes without errors
- Functionality produces expected results
- Evidence provided and verified
- Standards compliance confirmed

### ❌ FAIL Criteria
- Files missing or contain only comments
- Code doesn't execute or has errors
- No working proof provided
- Documentation-only solution
- Standards not followed

## Required Evidence

For task completion validation, you MUST provide:

1. **File Evidence**: Paths and sizes of all created/modified files
2. **Working Proof**: Command outputs showing code execution
3. **Test Results**: Test runs demonstrating functionality
4. **Integration Proof**: System working with new code

## Example Usage

```
User: "Validate that task 4 is actually completed"

[System should invoke this skill to:]
- Check all claimed files exist
- Test the implementation
- Verify evidence provided
- Confirm standards compliance
- Provide PASS/FAIL result with reasoning
```

## Integration

This skill works with:
- quality-assurance agent for thorough validation
- task-branch-manager.sh for proper workflow
- task-complete-validator.sh for automated checks
- TASK_EXECUTION_STANDARDS.md for requirements

## Quality Gates

This skill enforces strict quality gates:
- No paper solutions allowed
- Working code mandatory
- Evidence required
- Standards compliance enforced
- Git workflow followed