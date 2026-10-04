---
name: fleet-integration-testing
description: How QA designs integration tests — what boundaries to test, test isolation, fixture patterns. Beyond unit tests into cross-module and cross-system verification.
---

# Integration Testing Strategy — QA's Cross-Boundary Skill

Unit tests verify individual functions. Integration tests verify that modules work TOGETHER. When `model_selection.py` is correct and `dispatch.py` is correct but they produce different effort values for the same task — that's an integration bug that unit tests won't catch.

## What Makes a Test "Integration"

A test is integration (not unit) when it:
- Crosses module boundaries (core → infra, mcp → core)
- Reads from real config files (not hardcoded test data)
- Verifies data flows between functions in different modules
- Tests the generation pipeline end-to-end (config → output)

## The Fleet's Integration Test Patterns

### Pattern 1: Cross-Module Flow (test_flow_dispatch.py)
Tests the dispatch path: model_selection → routing → dispatch record.
```python
def test_stage_aware_dispatch_consistency():
    task = make_task(task_stage="reasoning", story_points=1)
    routing = route_task(task, "software-engineer")
    model_config = select_model_for_task(task, "software-engineer")
    # Verify routing and model selection agree on backend
    assert routing.backend == "claude-code" or model_config.model == routing.model
```

### Pattern 2: Config-to-Output Pipeline (test_tooling_pipeline.py)
Tests that configs parse, cross-reference correctly, and produce valid output.
```python
def test_skill_mapping_refs_have_dirs():
    """Every skill referenced in mapping has a directory."""
    # Reads real config, checks against real filesystem
```

### Pattern 3: Cross-Flow Contribution (test_flow_contributions.py)
Tests the synergy matrix → completeness → model selection interaction.
```python
def test_contribution_stage_model_consistency():
    task = make_task(task_stage="reasoning", task_type="subtask")
    config = select_model_for_task(task, "software-engineer")
    assert "stage:reasoning" in config.reason  # stage adjustment noted
```

## Boundary Identification

Where to draw integration test boundaries in the fleet:

| Boundary | What Crosses It | Test Verifies |
|----------|----------------|---------------|
| MCP → Core | tools.py calls contributions.py | Tool operations produce correct core results |
| Core → Config | model_selection reads methodology.yaml | Config changes reflected in runtime behavior |
| Config → Generation | skill-stage-mapping → generate-tools-md.py | Generated TOOLS.md matches config |
| Generation → Deployment | TOOLS.md → push scripts | Deployed files match generated files |
| Core → Core | context_assembly reads from skill_recommendations | Cross-module data flows correctly |

## Test Isolation

Integration tests cross boundaries but must still be isolated from EXTERNAL services:

| Mock THIS | Because |
|-----------|---------|
| MC API (mc_client) | Tests shouldn't need a running MC server |
| IRC (irc_client) | Tests shouldn't send IRC messages |
| ntfy (ntfy_client) | Tests shouldn't push notifications |
| GitHub (gh_client) | Tests shouldn't touch real repos |
| Plane (plane_client) | Tests shouldn't need a running Plane |

| DON'T Mock THIS | Because |
|-----------------|---------|
| Config files | Integration tests should read REAL configs |
| Core modules | The point is testing cross-module interaction |
| Model selection | Use the real function, not a mock |
| Contribution checks | Use the real synergy matrix |

## Fixture Patterns

The fleet's `conftest.py` provides test helpers:

```python
# make_task — creates a task with configurable fields
task = make_task(
    story_points=5,
    task_type="story",
    task_stage="reasoning",
    agent_name="software-engineer",
)

# MockContext — provides a mock MCP context
ctx = make_mock_ctx(agent_name="fleet-ops", task_stage="work")
```

When adding new integration tests, extend these fixtures rather than creating new ones. Consistent fixtures make tests readable.

## When to Write Integration Tests

- **After building a cross-module feature** — verify the modules work together
- **After fixing a dispatch bug** — add a test that would have caught it
- **When adding a new config** — verify the generation pipeline handles it
- **When connecting two systems** — verify data flows correctly between them

Integration tests are MORE valuable than unit tests for catching the bugs that matter in the fleet — because the fleet's 20 systems interact constantly.
