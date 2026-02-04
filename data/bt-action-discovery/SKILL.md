---
name: bt-action-discovery
description: Discovers available robot actions by reading action_library.yaml. Returns action catalog with parameters and constraints for BT generation and validation.
---

## Purpose

This skill discovers what actions the robot supports. Currently reads from `action_library/action_library.yaml`. In the future, this will query the robot's advertised ROS services/actions dynamically.

---

## Workflow

1. Read `action_library/action_library.yaml`
2. Parse available primitive and composite actions
3. Return structured action catalog

---

## Output Format

Return the following information:

### Primitives
- Action name
- Package location
- Parameters (name, type, required, default, description)
- Valid ranges
- Example usage

### Composites
- Action name
- Package location
- Parameters
- Example usage

### Constraints
- Workspace bounds (x_range, y_range)
- Color value ranges
- Default spawn position

---

## Example Usage

When invoked, this skill reads the YAML and returns:

```
Available Primitive Actions:
- GoToPose(name, x, y, theta=None, tolerance_pos=0.1, tolerance_angle=0.1)
  - x, y must be in [0, 11]
  - Example: GoToPose(name='Move', x=5.0, y=5.0)

- SetPen(name, r=255, g=255, b=255, width=3, off=0)
  - RGB values in [0, 255]
  - Example: SetPen(name='Red', r=255, g=0, b=0, width=3)

[... continues for all actions ...]

Workspace Constraints:
- x_range: [0, 11]
- y_range: [0, 11]
- Default spawn: (5.544445, 5.544445)
```

---

## Notes

- This skill has **low degree of freedom** - it simply reads and returns the YAML content in a structured format
- Future enhancement: Query live robot instead of static YAML file
- Invoked by: bt-composer (during generation) and bt-validator (during validation)
