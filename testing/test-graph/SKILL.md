---
name: mock-repomaps-fixtures
description: >
  This skill covers patterns for mocking RepoMaps in tests.
  Trigger: Load this skill when working with test_graph fixtures.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: low
  token_estimate: 350
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# Mock RepoMaps Fixtures

This skill covers patterns for mocking RepoMaps in tests.

**Trigger**: Load this skill when working with test_graph fixtures.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Create a small graph fixture | `small_graph` |
| Test adding a node | `TestAddNode` |

## Critical Patterns (Summary)
- **small_graph**: Provides a predefined small graph for testing.
- **TestAddNode**: Tests the functionality of adding a node to the graph.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### small_graph

This pattern provides a predefined small graph for testing purposes, allowing for consistent and repeatable tests.

```python
# Example usage of small_graph
from tests.test_graph import small_graph

def test_small_graph():
    assert len(small_graph.nodes) == expected_node_count
```

### TestAddNode

This pattern tests the functionality of adding a node to the graph, ensuring that the graph updates correctly.

```python
# Example usage of TestAddNode
from tests.test_graph import TestAddNode

def test_add_node():
    test_case = TestAddNode()
    test_case.run()
```

## When to Use

- When you need to create a small graph for unit tests.
- When testing the addition of nodes to a graph structure.

## Commands

```bash
pytest tests/test_graph.py
```

## Anti-Patterns

### Don't: Use real RepoMaps in tests

Using real RepoMaps can lead to flaky tests and inconsistent results.

```python
# BAD
from repo.maps import RepoMap

def test_with_real_repos():
    repo = RepoMap()
    assert repo is not None
```
<!-- L3:END -->