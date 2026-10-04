---
name: fleet-test
description: How to run and analyze test results for a review
user-invocable: false
---

# Fleet Test Skill

You are running tests for a task under review.

## 1. Identify the Target
- Read parent task for PR URL and branch
- Find the project worktree or clone

## 2. Run Tests
```bash
cd {worktree}
python -m pytest --tb=short -v 2>&1
```

## 3. Analyze Results
For each failure:
- What test failed? (file, function, line)
- Expected vs actual?
- Regression from these changes or pre-existing?
- Environment issue (missing dependency)?

## 4. Report
Complete your review task:
```
fleet_task_complete(summary="X/Y tests pass. Z failures: [list]. Verdict: PASS/FAIL")
```

## 5. If Tests Fail
Create fix task for original author:
```
fleet_task_create(
  title="Fix failing tests: {description}",
  agent_name="{original_author}",
  parent_task="{parent_task_id}",
  task_type="subtask",
  priority="high"
)
```

## 6. If Missing Infrastructure
```
fleet_task_create(
  title="Add {dependency} to project dependencies",
  agent_name="devops",
  task_type="blocker",
  priority="high"
)
```