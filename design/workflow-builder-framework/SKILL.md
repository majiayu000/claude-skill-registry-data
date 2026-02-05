---
name: workflow-builder-framework
description: Design multi-agent workflows with DAGs, state machines, and event-driven patterns
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Workflow Builder Framework

## Purpose

Build production-grade multi-agent workflows that coordinate complex tasks across distributed systems. Implement orchestration patterns including DAGs (directed acyclic graphs), state machines, event-driven architectures, and saga patterns with robust error handling and full observability.

**Why This Matters**:
- Coordinate multiple agents working on parallel tasks
- Handle failures gracefully with retry and compensation logic
- Scale workflows from simple pipelines to complex orchestrations
- Monitor and debug distributed workflows in production

## Quick Start

### 4-Step Process

1. **Design**: Choose workflow pattern (DAG, state machine, event-driven, saga)
2. **Implement**: Build workflow using pattern templates from PATTERNS.md
3. **Test**: Validate execution paths, error handling, and edge cases
4. **Deploy**: Add observability hooks and deploy with monitoring

### Your First Workflow (60 seconds)

```python
from workflow_builder import DAGWorkflow, Task

# Define tasks
tasks = [
    Task("fetch_data", run=lambda: fetch_api_data()),
    Task("process", run=lambda data: process(data), depends_on=["fetch_data"]),
    Task("save", run=lambda result: save(result), depends_on=["process"])
]

# Build and execute DAG
workflow = DAGWorkflow(tasks)
result = workflow.execute()
```

## Core Patterns Overview

### 1. DAG Workflow
**Use When**: Tasks have clear dependencies, parallelization opportunities
- Directed acyclic graph execution
- Topological sorting for order
- Parallel task execution
- Dependency tracking
- **See**: PATTERNS.md Section 1

### 2. State Machine Workflow
**Use When**: Complex state transitions, approval processes, deployment pipelines
- Finite state machine (FSM)
- State transitions with guards
- Action execution on transitions
- State persistence and recovery
- **See**: PATTERNS.md Section 2

### 3. Event-Driven Workflow
**Use When**: Reactive systems, loosely-coupled components, async processing
- Pub/sub event handling
- Event sourcing patterns
- Event replay capability
- Eventual consistency
- **See**: PATTERNS.md Section 3

### 4. Saga Pattern
**Use When**: Distributed transactions, multi-service coordination, compensation required
- Forward recovery (continue on failure)
- Backward recovery (compensating actions)
- Orchestration vs choreography
- Transaction consistency
- **See**: PATTERNS.md Section 4

### 5. Error Handling & Recovery
**Use When**: All workflows (critical for production)
- Retry strategies (exponential backoff)
- Circuit breakers
- Fallback mechanisms
- Dead letter queues
- **See**: PATTERNS.md Section 5

### 6. Workflow Observability
**Use When**: All workflows (essential for debugging)
- Distributed tracing
- Metrics collection
- Structured logging
- Workflow visualization
- **See**: PATTERNS.md Section 6

### 7. Load Balancing & Scaling
**Use When**: High-throughput workflows, resource constraints
- Task distribution algorithms
- Worker pool management
- Priority queues
- Rate limiting
- **See**: PATTERNS.md Section 7

## Pattern Selection Guide

| Requirement | Recommended Pattern |
|-------------|-------------------|
| Clear task dependencies | DAG Workflow |
| Complex state transitions | State Machine |
| Reactive/async processing | Event-Driven |
| Distributed transactions | Saga Pattern |
| CI/CD pipeline | DAG + State Machine |
| Data processing | DAG + Load Balancing |
| Multi-agent coordination | DAG + Event-Driven |
| Deployment automation | State Machine + Saga |

## Workflow Engines

### Airflow (DAG-focused)
```python
from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG('data_pipeline', schedule='@daily')
fetch = PythonOperator(task_id='fetch', python_callable=fetch_data, dag=dag)
process = PythonOperator(task_id='process', python_callable=process, dag=dag)
fetch >> process  # Dependency
```

### Temporal (Long-running workflows)
```python
from temporalio import workflow

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> str:
        await workflow.execute_activity(
            charge_payment,
            order_id,
            start_to_close_timeout=timedelta(minutes=5)
        )
        await workflow.execute_activity(
            ship_order,
            order_id,
            start_to_close_timeout=timedelta(days=1)
        )
        return "completed"
```

### Prefect (Python-native)
```python
from prefect import flow, task

@task
def fetch():
    return data

@task
def process(data):
    return result

@flow
def pipeline():
    data = fetch()
    return process(data)
```

### Celery (Task queue)
```python
from celery import chain, group

# Sequential
result = chain(task1.s(), task2.s(), task3.s())()

# Parallel
result = group(task1.s(), task2.s(), task3.s())()
```

## Top 3 Gotchas

### 1. Circular Dependencies (DAGs)
**Problem**: Task A depends on B, B depends on A → deadlock

**Detection**:
```python
def detect_cycles(tasks):
    visited = set()
    rec_stack = set()

    def dfs(task):
        visited.add(task)
        rec_stack.add(task)
        for dep in task.dependencies:
            if dep not in visited:
                if dfs(dep):
                    return True
            elif dep in rec_stack:
                return True  # Cycle detected
        rec_stack.remove(task)
        return False

    return any(dfs(t) for t in tasks if t not in visited)
```

**Fix**: Use topological sort to validate DAG before execution

### 2. Lost Events (Event-Driven)
**Problem**: Event published before subscriber ready → event lost

**Solution**: Event sourcing with replay
```python
class EventStore:
    def __init__(self):
        self.events = []

    def publish(self, event):
        self.events.append(event)
        self.notify_subscribers(event)

    def replay(self, subscriber, from_position=0):
        for event in self.events[from_position:]:
            subscriber.handle(event)
```

### 3. Saga Compensation Order
**Problem**: Compensating actions execute in wrong order → data corruption

**Solution**: Reverse order of successful steps
```python
class SagaOrchestrator:
    def __init__(self):
        self.executed_steps = []

    async def execute(self, steps):
        try:
            for step in steps:
                await step.forward()
                self.executed_steps.append(step)
        except Exception:
            # Compensate in REVERSE order
            for step in reversed(self.executed_steps):
                await step.compensate()
            raise
```

## Quick Reference Card

### DAG Workflow
```python
# Build DAG
dag = DAGWorkflow()
dag.add_task("A", func=task_a)
dag.add_task("B", func=task_b, depends_on=["A"])
dag.add_task("C", func=task_c, depends_on=["A"])
dag.add_task("D", func=task_d, depends_on=["B", "C"])
result = dag.execute()
```

### State Machine
```python
# Define FSM
fsm = StateMachine(initial="idle")
fsm.add_transition("idle", "running", guard=lambda: can_start())
fsm.add_transition("running", "completed", action=lambda: cleanup())
fsm.add_transition("running", "failed", action=lambda: rollback())
fsm.trigger("start")
```

### Event-Driven
```python
# Setup event bus
bus = EventBus()
bus.subscribe("task.completed", on_task_complete)
bus.subscribe("task.failed", on_task_failed)
bus.publish(Event("task.completed", {"task_id": "123"}))
```

### Saga Pattern
```python
# Define saga
saga = Saga()
saga.add_step(
    forward=lambda: charge_payment(),
    compensate=lambda: refund_payment()
)
saga.add_step(
    forward=lambda: reserve_inventory(),
    compensate=lambda: release_inventory()
)
saga.execute()
```

## Documentation Structure

- **KNOWLEDGE.md**: Theory, workflow engines, academic background
- **PATTERNS.md**: 7 implementation patterns with code
- **EXAMPLES.md**: Complete working examples
- **GOTCHAS.md**: Common problems and solutions
- **REFERENCE.md**: API documentation for workflow engines

## Integration Points

### Agent Orchestrator
```python
# Multi-agent workflow
workflow = DAGWorkflow()
workflow.add_task("analyze", agent="code-analyzer")
workflow.add_task("refactor", agent="refactoring-lead", depends_on=["analyze"])
workflow.add_task("test", agent="test-engineer", depends_on=["refactor"])
workflow.add_task("review", agent="code-reviewer", depends_on=["test"])
```

### Deployment Architect
```python
# Deployment pipeline
pipeline = StateMachine(initial="pending")
pipeline.add_transition("pending", "building")
pipeline.add_transition("building", "testing")
pipeline.add_transition("testing", "staging")
pipeline.add_transition("staging", "production")
pipeline.add_transition("*", "rollback", action=rollback_deployment)
```

## When NOT to Use

- **Simple sequential tasks**: Just use functions
- **One-off scripts**: Overhead not worth it
- **No failure scenarios**: If it always succeeds, simpler patterns work
- **No coordination needed**: Single-agent tasks don't need orchestration

## Next Steps

1. Read KNOWLEDGE.md for workflow theory
2. Study PATTERNS.md for implementation details
3. Try EXAMPLES.md to see complete workflows
4. Reference GOTCHAS.md when debugging
5. Use REFERENCE.md for API details

## Related Skills

- `work-forecasting-parallelization`: Analyze workflow for parallelization opportunities
- `context-engineering-framework`: Manage context in long-running workflows
- `agent-builder-framework`: Build agents that execute workflow tasks

## Quick Wins

Start with these simple patterns:
1. **Basic DAG**: 3 tasks with dependencies (30 min)
2. **Simple State Machine**: 4 states with transitions (45 min)
3. **Event Handler**: 2 events with subscribers (20 min)

Then progress to:
4. **DAG with Error Handling**: Add retry logic (1 hour)
5. **State Machine with Guards**: Add validation (1 hour)
6. **Saga Pattern**: 2-step distributed transaction (2 hours)

---

**Total Lines**: ~450
