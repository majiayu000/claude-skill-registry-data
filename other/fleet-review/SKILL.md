---
name: fleet-review
description: How to review a task as board lead or QA reviewer
user-invocable: false
---

# Fleet Review Skill

You are reviewing a completed task. Follow this checklist:

## 1. Load Context
```
fleet_read_context(task_id="...", project="...")
fleet_agent_status()
```

## 2. Evaluate the Work

### For Code Tasks:
- [ ] PR exists in custom fields?
- [ ] Conventional commit format used?
- [ ] Tests included for new code?
- [ ] Test results in approval rubric — did tests pass?
- [ ] Plan quality score — was a good plan shared?
- [ ] No secrets in diff
- [ ] No hardcoded paths

### For Non-Code Tasks:
- [ ] Output addresses the task requirements?
- [ ] Publication quality markdown?
- [ ] Cross-references with URLs?

## 3. Create QA Subtask (Code Tasks)
```
fleet_task_create(
  title="QA Review: Run tests for {task_title}",
  agent_name="qa-engineer",
  parent_task="{task_id}",
  task_type="subtask",
  priority="high"
)
```

## 4. Decide
- **Approve**: `fleet_approve(approval_id, "approved", "Tests pass. Quality meets standards.")`
- **Reject**: `fleet_approve(approval_id, "rejected", "Specific feedback: what and why")`
- **Escalate**: `fleet_escalate(title="Needs human review", details="...", question="...")`