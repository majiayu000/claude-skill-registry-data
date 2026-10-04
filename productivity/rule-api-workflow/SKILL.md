---
name: rule-api-workflow
description: MANDATORY when editing files matching ["api/src/workflow/**/*.py"]. When working on workflow orchestration in api/src/workflow/
---

# API Workflow Rules

## State Machine Base Class

ALWAYS use the `python-statemachine` library's `StateChart` base class for state machines. ALWAYS set `atomic_configuration_update = True` for single-state transitions. ALWAYS set `catch_errors_as_events = False` to let exceptions propagate.

Example from codebase:
```python
# From api/src/workflow/state_machine/opportunity_publish_state_machine.py
from statemachine import StateChart, State

class OpportunityPublishStateMachine(StateChart):
    atomic_configuration_update = True
    catch_errors_as_events = False

    # States
    draft = State(initial=True)
    under_review = State()
    published = State()
    closed = State()

    # Transitions
    submit_for_review = draft.to(under_review)
    approve = under_review.to(published)
    reject = under_review.to(draft)
    close = published.to(closed)
```

## Metrics Pattern

ALWAYS define a `Metrics` class as a `StrEnum` inside workflow classes, following the same pattern as Task metrics. ALWAYS use `increment()` for tracking workflow events.

Example from codebase:
```python
class Metrics(StrEnum):
    TRANSITIONS_PROCESSED = "transitions_processed"
    APPROVALS_GRANTED = "approvals_granted"
    REJECTIONS_ISSUED = "rejections_issued"
```

## Event Model

ALWAYS use typed event models (`StateMachineEvent`, `SQSMessageContainer`) for workflow events. NEVER pass raw dicts as workflow events. ALWAYS include event metadata (timestamp, actor, source).

Example from codebase:
```python
# From api/src/workflow/handler/event_handler.py pattern
class StateMachineEvent:
    event_type: str
    entity_id: uuid.UUID
    actor_id: uuid.UUID
    timestamp: datetime
    metadata: dict
```

## State Persistence

ALWAYS use database-backed persistence via `BaseStatePersistenceModel` subclasses. NEVER store workflow state in memory or cache. ALWAYS persist state transitions atomically with business data changes.

Example from codebase:
```python
# From api/src/workflow/state_persistence/opportunity_persistence_model.py
class OpportunityStatePersistence(BaseStatePersistenceModel):
    __tablename__ = "opportunity_workflow_state"

    opportunity_id = mapped_column(UUID, ForeignKey("opportunity.opportunity_id"))
    current_state = mapped_column(String, nullable=False)
    previous_state = mapped_column(String, nullable=True)
```

## Listener/Observer Pattern

ALWAYS use the listener pattern for side effects on state transitions (audit logging, email notifications). NEVER embed side-effect logic directly in state machine transition handlers. ALWAYS register listeners via the workflow registry.

Example from codebase:
```python
# From api/src/workflow/listener/workflow_audit_listener.py
class WorkflowAuditListener:
    def on_transition(self, event: StateMachineEvent, from_state: str, to_state: str):
        logger.info(
            "Workflow state transition",
            extra={
                "entity_id": str(event.entity_id),
                "from_state": from_state,
                "to_state": to_state,
                "actor_id": str(event.actor_id),
            },
        )
```

## Registry Pattern

ALWAYS use `WorkflowRegistry` and `WorkflowClientRegistry` for workflow and client registration. NEVER instantiate workflow services directly — always look them up via the registry.

## Approval Processing

ALWAYS use the `ApprovalProcessor` for approval-based workflows. ALWAYS validate actor permissions before processing approvals. ALWAYS record approval decisions in the audit trail.

## Background Task Execution

ALWAYS use the `workflow_background_task` decorator for workflow tasks that run as ECS containers. This decorator handles NewRelic custom transaction setup and workflow-specific monitoring.

## Logging

ALWAYS begin every workflow module with `logger = logging.getLogger(__name__)`. ALWAYS log state transitions with `from_state`, `to_state`, and `entity_id` in `extra={}`. NEVER log PII. ALWAYS use static log message strings.

Example from codebase:
```python
import logging
logger = logging.getLogger(__name__)

logger.info(
    "Opportunity state transition completed",
    extra={
        "opportunity_id": str(opportunity_id),
        "from_state": previous_state,
        "to_state": new_state,
    },
)
```

## Error Handling

ALWAYS let state machine exceptions propagate — the Task framework handles status tracking. NEVER catch and swallow state transition errors. ALWAYS validate preconditions before triggering transitions.

---

## Context Enrichment

When generating significant workflow code (new state machine, new listener, new event type), enrich your context:
- Call `get_architecture_section("api")` from the `simpler-grants-context` MCP server to understand workflow architecture
- Call `get_rule_detail("api-tasks")` for background task patterns that workflows use
- Call `get_rule_detail("api-services")` for service layer patterns that workflows call
- Call `get_rule_detail("api-database")` for state persistence and transaction patterns
- Consult **Compound Knowledge** for indexed documentation on workflow patterns

## Related Rules

When working on workflows, also consult these related rules:
- **`api-tasks.mdc`** — task framework that workflows execute within
- **`api-services.mdc`** — service functions that workflows orchestrate
- **`api-database.mdc`** — state persistence models and transaction management
- **`api-adapters.mdc`** — external service adapters used by workflow listeners (email, SQS)
- **`api-error-handling.mdc`** — error handling patterns
- **`cross-domain.mdc`** — structured logging, factory patterns

## Specialist Validation

When generating or significantly modifying workflow code:

**For simple changes (< 20 lines, adding a metric, updating a log message):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new state transition, new listener):**
Invoke `codebase-conventions-reviewer` to validate against project conventions.

**For complex changes (new state machine, new workflow type, cross-workflow orchestration):**
Invoke the following specialists (run in parallel where possible):
- `architecture-strategist` — validate state machine boundaries and workflow design
- `data-integrity-guardian` — validate state persistence and transition atomicity
- `kieran-python-reviewer` — Python-specific quality review
