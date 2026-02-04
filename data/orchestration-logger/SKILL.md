---
name: orchestration-logger
description: Unified logging system for AI orchestration workflows with current state metadata and execution logs in a single file
---

# Orchestration Logging Skill
Unified logging for orchestration workflows with automatic state tracking and audit trails. You will create and append orchestration logs to the logfile by directly updating the json file. No code or scripts required.

# Instructions
1. Orchestration logs should be generated under .claude/logs with the filename `.claude/logs/orchestration-{app_name}-{yyyymmdd-HH24MMss}.json` containing:
- **Metadata**: Orchestration progress, completed tasks, current status
- **Execution logs**: Complete logging of all subagent requests and responses
- **Timestamp** should be in SGT

# Usage Patterns
1. Initialize- Start by creating a new logfile with the json structure and metadata
2. Log Request- Log the request under execution_logs with type:request. Update metadata   
3. Log Response- Log the response under execution_logs with type:response. Update metadata

# Example Log
Follow this sample log for guidance 

``` json
{
  "orchestration_id": "{orchestration_id}",
  "log_file": "orchestration-{orchestration_id}.json",
  "metadata": {
    "status": "{running|completed|halted|error}", # halted : if waiting for user input
    "app_name": "hello-world",
    "confirmation_mode": "interactive",
    "started_at": "{timestamp in SGT}",
    "implementation_plan": "plans/us-hello-impl-plan.md",
    "user_story_id": "US-HELLO",
    "current_task": "1.2",
    "current_subagent": "quality-manager",
    "completed_tasks": [1.1],
    "failed_tasks": [],
    "loop_attempts": {},
    "total_tasks": 82,
    "completion_percentage": 1.05,
    "last_completed_subtask_at": null,
    "last_completed_task_id": null,
    "last_updated": "{timestamp in SGT}",
    "final_report": null
  },
  "execution_logs": [
    {
      "task": "1.2",
      "subagent": "python-developer",
      "type":"request",        
      "content":"Implement task 1.2 | Fix the following issues : (a), (b), (c)..",
      "timestamp":"{timestamp in SGT}",
      "implementation_plan": "plans/us-hello-impl-plan.md",
      "user_story": "us-hello-world.md",
    },
    {
      "task": "1.2",
      "subagent": "python-developer",
      "type":"response",        
      "content":"I have implemented task 1.2 with the following changes (a), (b), (c)..",
      "timestamp":"{timestamp in SGT}",
    },
    {
      "task": "1.2",
      "subagent": "quality-manager",
      "type":"request",        
      "content":"Validate the implementation for task 1.2 against the acceptance criteria",
      "timestamp":"{timestamp in SGT}",
      "implementation_plan": "plans/us-hello-impl-plan.md",
      "user_story": "us-hello-world.md",
    },

  ]
}
```
