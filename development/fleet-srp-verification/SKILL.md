---
name: fleet-srp-verification
description: How the architect verifies single responsibility — is each module/class/function doing one thing? The concrete checks that prevent god classes and mixed concerns.
---

# SRP Verification — Architect's Structural Check

Single Responsibility Principle: every module, class, and function should have one reason to change. When a module does config loading AND API calls AND data transformation AND error handling, it has 4 reasons to change — and changing any one risks breaking the others.

## Concrete SRP Checks

### Module Level (files)

**Check:** Can you describe what this module does in ONE sentence without "and"?

| Module | Description | SRP? |
|--------|------------|------|
| fleet/core/model_selection.py | "Selects model and effort for a task" | YES — one concern |
| fleet/core/contributions.py | "Checks contribution completeness" | YES — one concern |
| fleet/mcp/tools.py | "Implements all 30 MCP tools" | BORDERLINE — many tools but one concern (MCP interface) |
| hypothetical bad.py | "Reads config AND calls API AND transforms data AND writes files" | NO — 4 concerns |

**Metric:** If a module has >10 public functions across different domains, it likely violates SRP.
**Metric:** If a module is >500 lines, investigate whether it should be split.

### Function Level

**Check:** Does this function do one thing, or does it have steps that should be separate functions?

```python
# BAD — does 3 things
def process_task(task):
    config = load_config()           # 1. Config loading
    result = call_api(config, task)  # 2. API call
    formatted = format_output(result) # 3. Formatting
    return formatted

# GOOD — each function does one thing
def load_config(): ...
def call_api(config, task): ...
def format_output(result): ...
def process_task(task):
    return format_output(call_api(load_config(), task))
```

**Metric:** If a function has more than 3 distinct logical blocks separated by blank lines, it likely does too much.

### Class Level (if applicable)

**Check:** Does this class have methods that serve different purposes?

```python
# BAD — mixed concerns
class TaskManager:
    def create_task(self, ...): ...      # Task CRUD
    def dispatch_task(self, ...): ...    # Dispatch logic
    def check_budget(self, ...): ...     # Budget logic
    def send_notification(self, ...): ... # Notification logic

# GOOD — separated concerns
class TaskStore:         # CRUD only
class Dispatcher:        # Dispatch logic only
class BudgetMonitor:     # Budget logic only
class NotificationRouter: # Notification only
```

## How to Verify During Design Contribution

When producing `design_input`, check the target area for SRP:

1. **List the responsibilities** of each module you're touching
2. **If >1 responsibility**: suggest split in your design_input
3. **If creating new modules**: define their single responsibility explicitly
4. **Reference existing patterns**: "Like mc_client.py, this should ONLY handle API communication"

### In Your design_input Contribution

```
Target: fleet/core/new_module.py
Responsibility: Check phase standards against delivery phase config (ONE thing)
Does NOT: load config (caller provides), call APIs (uses passed mc client),
          format output (returns data, caller formats)
Pattern: Same as contributions.py — receives dependencies, returns result
```

## The Fleet's SRP Patterns

The fleet codebase follows SRP well in most areas:

| Pattern | How SRP is Applied |
|---------|-------------------|
| core/ modules | Each module = one domain concept (contributions, phases, velocity, etc.) |
| infra/ clients | Each client = one external service (mc_client, irc_client, gh_client, etc.) |
| mcp/roles/*.py | Each file = one role's group calls |
| Event chains | Builder functions create chains. ChainRunner executes them. Separation. |
| Context system | context_assembly aggregates. preembed formats. Different concerns. |

When you spot a violation, flag it in your architecture health report or design contribution.

## Integration With Architecture Health CRON

Your weekly health check should include SRP verification:
1. Scan for modules >500 lines
2. Check for modules with >10 public functions across different domains
3. Flag modules where the description requires "and"
4. Track: is SRP compliance improving or declining over time?
