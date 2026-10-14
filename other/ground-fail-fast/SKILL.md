---
name: ground-fail-fast
description: Fail-fast patterns. Reject invalid input at the boundary.
---

# Skill: Fail Fast

> "Reject invalid input at the boundary. Don't let it travel through the system."

## The Standard

- **Boundaries are gates**: HTTP request enters? Validate. Job payload arrives? Validate. Once past the gate, trust the data.
- **Actions trust input**: If you're validating inside an action, validation happened in the wrong place.
- **Fail loudly**: Invalid state should throw, not return false. Silent failures hide bugs.

## The Check

Ask yourself:
- Where does invalid data first enter this flow?
- Is validation happening at that boundary?
- Are downstream components trusting validated input?

## Real-World Examples

See [examples.md](examples.md).
