---
name: flows
description: This skill should be used when designing CrewAI Flows with typed state management, deterministic routing, and event-driven orchestration. Use it for flow architecture, state transitions, control primitives, and production deployment.
version: 3.0.0
tags: [crewai, flows, state-management, routing, orchestration, decorators]
---

# Flows

Comprehensive skill for building CrewAI Flows with structured state management, event-driven control, and production-ready patterns.

## When To Use

- Create flow-based AI orchestration
- Manage state across multi-step workflows
- Implement conditional routing with @router
- Build event-driven systems with @listen
- Add persistence for long-running workflows
- Combine Flows with Crews for production systems
- Design complex control logic (loops, branches, joins)

## Quick Start Workflow

### 1. Scaffold New Flow Project
```bash
python scripts/scaffold_flow.py my_flow
```

### 2. Define State Model
Use structured state with Pydantic for type safety:
```python
from pydantic import BaseModel

class MyState(BaseModel):
    input_data: str = ""
    processed: bool = False
    results: list = []
```

### 3. Implement Flow Logic
```python
from crewai.flow.flow import Flow, listen, start

class MyFlow(Flow[MyState]):
    @start()
    def initialize(self):
        self.state.input_data = "sample"
        return "initialized"
    
    @listen(initialize)
    def process(self, _):
        self.state.processed = True
        return "completed"
```

### 4. Validate and Run
```bash
python scripts/validate_flow.py my_flow/main.py
python my_flow/main.py
```

## Detailed Workflow

### Design Phase
1. **Model State**: Define Pydantic model with all fields needed
2. **Map Flow Topology**: Plan @start, @listen, @router relationships
3. **Identify Control Points**: Where do you need branches or loops?
4. **Plan Persistence**: Which steps need checkpointing?

### Implementation Phase
1. **Create State Model**: Use Pydantic BaseModel
2. **Define Flow Class**: Inherit from Flow[StateType]
3. **Add Decorators**: @start, @listen, @router as needed
4. **Implement Methods**: Each method updates state and returns values
5. **Add Persistence**: Use @persist decorator for critical steps

### Validation Phase
```bash
python scripts/validate_flow.py ./my_flow/main.py
```

Validates:
- Flow class inheritance
- @start decorator presence
- Router labels match listeners
- State model validity
- No circular dependencies

### Execution Phase
```python
flow = MyFlow()
result = flow.kickoff()
```

## State Management

### Structured State (Recommended)
```python
from pydantic import BaseModel

class AppState(BaseModel):
    user_input: str = ""
    processing_result: str = ""
    completed: bool = False

class MyFlow(Flow[AppState]):
    @start()
    def init(self):
        self.state.user_input = "hello"
        return "ok"
```

Benefits:
- Type checking at development time
- IDE autocompletion
- Automatic validation
- Self-documenting

### Unstructured State
```python
class MyFlow(Flow):
    @start()
    def init(self):
        self.state["key"] = "value"  # Dictionary access
        return "ok"
```

Use for:
- Quick prototyping
- Dynamic schemas
- Simple flows

## Decorator Reference

### @start()
Entry point for flow execution.

**Unconditional:**
```python
@start()
def init(self):
    return "started"
```

**Conditional:**
```python
@start("previous_method")
def resume(self):
    return "resumed"
```

### @listen()
Listen to method completion or router labels.

**Single source:**
```python
@listen(init)
def process(self, result):
    return f"Got: {result}"
```

**Multiple sources (AND):**
```python
from crewai.flow.flow import and_

@listen(and_(step_a, step_b))
def merge(self, _):
    return "both completed"
```

**Alternative sources (OR):**
```python
from crewai.flow.flow import or_

@listen(or_(option_a, option_b))
def handle_either(self, _):
    return "one completed"
```

**Label-based:**
```python
@listen("approved")
def publish(self):
    return "published"
```

### @router()
Conditional routing with labels.

```python
@router(evaluate)
def quality_gate(self, _):
    if self.state.score > 80:
        return "approved"
    elif self.state.score > 60:
        return "revision"
    else:
        return "rejected"

@listen("approved")
def handle_approval(self): ...

@listen("revision")
def handle_revision(self): ...
```

### @persist()
Automatic state persistence.

**Class-level:**
```python
from crewai.flow.persistence import persist

@persist()
class MyFlow(Flow[MyState]): ...
```

**Method-level:**
```python
@persist()
@listen(process)
def critical_step(self, _): ...
```

## Common Patterns

### Sequential Pipeline
```
@start() → @listen → @listen → final
```

### Conditional with Retry Loop
```
@start() → @router → "revision" → @listen → back to @router
                     → "approved" → @listen → complete
```

### Parallel Execution with Join
```
          ┌→ branch_a ─┐
@start() ─┤            ├→ @listen(and_(a, b)) → complete
          └→ branch_b ─┘
```

### State Accumulator
```python
@start()
def collect_items(self):
    self.state.items = []
    return "start"

@listen(collect_items)
def add_item(self, _):
    self.state.items.append(new_item)
    if len(self.state.items) < 10:
        return self.add_item("")  # Loop
    return "complete"
```

## Tool Usage

### scaffold_flow.py
Create new flow projects:
```bash
python scripts/scaffold_flow.py my_flow
python scripts/scaffold_flow.py my_flow --path ./projects --with-crew
```

### validate_flow.py
Validate flow structure:
```bash
python scripts/validate_flow.py ./my_flow/main.py
```

### plot_flow.py
Generate visualization:
```bash
python scripts/plot_flow.py ./my_flow/main.py --output flow.html
```

### generate_state.py
Interactive state generator:
```bash
python scripts/generate_state.py --output state.py
```

## Asset Templates

### Starter Project
- `assets/starter/main.py` - Complete working flow with persistence
- `assets/starter/README.md` - Project documentation

### Configuration Templates
- `assets/templates/flow-basic.py` - Simple @start/@listen
- `assets/templates/flow-advanced.py` - Router, persistence, and_/or_
- `assets/templates/state-structured.py` - Pydantic state models
- `assets/templates/state-unstructured.py` - Dictionary state

## Reference Documentation

### API Reference
- `references/api/decorators.md` - Complete decorator reference (@start, @listen, @router, @persist, and_, or_)
- `references/api/state-management.md` - State approaches, lifecycle, persistence
- `references/api/flow-attributes.md` - Flow class attributes and methods

### Guides
- `references/guides/state-patterns.md` - Accumulator, Pipeline, Branching, Retry, Progress, Error Recovery, Crew Integration
- `references/guides/control-primitives.md` - Sequential, Conditional Routing, Parallel, Alternative Paths, Human-in-the-Loop, Multi-Start

### External Resources
- `references/external.md` - Official documentation links

## Troubleshooting

### Common Issues

**"No @start decorator found"**
```
Error: Flow must have at least one @start method
```
Solution: Add `@start()` decorator to entry point method

**"Router label has no listener"**
```
Error: Router returns label 'approved' but no @listen('approved') found
```
Solution: Add matching listener for each router label

**"Circular dependency detected"**
```
Error: Circular dependency in decorator chain
```
Solution: Remove circular @listen references

**"State field not found"**
```
Error: 'MyState' object has no attribute 'unknown_field'
```
Solution: Add field to Pydantic model or check field name spelling

**"Invalid state model"**
```
Error: State model must inherit from pydantic.BaseModel
```
Solution: Ensure state class inherits from `BaseModel`

### Debugging Tips

1. **Enable verbose logging:**
```python
import logging
logging.basicConfig(level=logging.INFO)
```

2. **Log state at each step:**
```python
@listen(step)
def next_step(self, _):
    print(f"State: {self.state}")
    ...
```

3. **Visualize the flow:**
```bash
python scripts/plot_flow.py main.py
```

4. **Check state persistence:**
```python
print(f"Flow ID: {flow.state.id}")
```

## Mastery Steps

1. **Start Simple**: Run `assets/templates/flow-basic.py`
2. **Add State**: Define Pydantic model with your fields
3. **Build Chain**: Connect 3-4 steps with @listen
4. **Add Routing**: Implement @router for conditional logic
5. **Try Persistence**: Add @persist decorator
6. **Study Patterns**: Review `references/guides/state-patterns.md`
7. **Master Control**: Study `references/guides/control-primitives.md`
8. **Integrate Crews**: Use core-build skill to create crew, call from Flow

## File Structure

```
flows/
├── SKILL.md                          # This file
├── assets/
│   ├── starter/                      # Complete working flow
│   │   ├── main.py                  # Production-ready example
│   │   └── README.md                # Project documentation
│   └── templates/                    # Progressive examples
│       ├── flow-basic.py            # Simple decorators
│       ├── flow-advanced.py         # Router, persistence
│       ├── state-structured.py      # Pydantic models
│       └── state-unstructured.py    # Dictionary state
├── references/
│   ├── api/                          # API documentation
│   │   ├── decorators.md            # @start, @listen, @router, @persist
│   │   ├── state-management.md      # State approaches & lifecycle
│   │   └── flow-attributes.md       # Flow class reference
│   ├── guides/                       # How-to guides
│   │   ├── state-patterns.md        # Common state patterns
│   │   └── control-primitives.md    # Control flow patterns
│   └── external.md                  # Official docs links
└── scripts/                          # Executable tools
    ├── scaffold_flow.py             # Project scaffolding
    ├── validate_flow.py             # Structure validation
    ├── plot_flow.py                 # Visualization
    └── generate_state.py            # State model generator
```

## Coding-Agent Guidelines

- **Start with state model** before implementing decorators
- **Use structured state** (Pydantic) for all non-trivial flows
- **Keep router labels deterministic** and document them
- **Reserve Flow code for orchestration**, use core-build for crews
- **Make state updates idempotent** where retry is possible
- **Add persistence** for long-running or critical workflows
- **Log flow ID** at key transitions for traceability
- **Use plotting** as a release gate to verify flow topology
- **Document state transitions** in method docstrings
- **Validate before execution** with validate_flow.py

## Production Architecture

### Flow-First Approach
Always start with Flow when building production AI applications:
- Flows provide state management across steps
- Flows enable precise execution control (loops, conditionals)
- Flows offer observability and debugging capabilities

### State Design Principles
- Keep state minimal - only persist what you need
- Use structured data - avoid unstructured dictionaries
- Make fields descriptive and self-documenting

### Crew Integration
- Create crews using core-build skill patterns
- Use Flows to orchestrate crew execution order
- Pass typed payloads between Flow state and crew inputs/outputs

### Persistence Strategy
- Use `@persist()` class-level for full workflow checkpointing
- Use `@persist()` method-level for specific critical steps
- Resume automatically from last checkpoint on restart

### Observability
- Log flow state.id at start and key transitions
- Track router decisions with input evidence
- Monitor branch duration and failure counts

## Next Steps

1. Review `assets/starter/` for a complete working example
2. Study `references/guides/` for patterns and best practices
3. Use `scripts/scaffold_flow.py` to create your first flow
4. Validate with `scripts/validate_flow.py`
5. Visualize with `scripts/plot_flow.py`
6. Deploy with CrewAI Enterprise for production hosting
