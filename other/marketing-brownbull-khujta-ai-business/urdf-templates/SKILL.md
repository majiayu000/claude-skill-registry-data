---
name: urdf-templates
description: URDF structure templates and validation patterns for robotics content. Use when creating robot descriptions, validating URDF files, or teaching URDF concepts.
allowed-tools: Read, Grep
---

# URDF Templates

## Instructions

When working with URDF files:

1. Use the provided templates as starting points
2. Validate against the checklist in validation.md
3. Include safety annotations for joint limits
4. Add comments explaining each section

## Template Selection

| Robot Type | Template | Use Case |
|------------|----------|----------|
| Mobile Robot | mobile-robot.urdf | Wheeled robots, differential drive |
| Humanoid Base | humanoid-base.urdf | Bipedal robots, upper body |

## URDF Structure Overview

```xml
<robot name="robot_name">
  <!-- Links define physical parts -->
  <link name="base_link">
    <visual>...</visual>
    <collision>...</collision>
    <inertial>...</inertial>
  </link>

  <!-- Joints connect links -->
  <joint name="joint_name" type="revolute">
    <parent link="parent_link"/>
    <child link="child_link"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
  </joint>
</robot>
```

## Safety Requirements

1. **Always specify joint limits** - Never leave limits undefined
2. **Include inertial properties** - Required for physics simulation
3. **Add collision geometry** - Required for safe simulation
4. **Document mass values** - Use realistic values

## Reference

See [validation.md](validation.md) for validation rules.
See [templates/](templates/) for complete templates.
