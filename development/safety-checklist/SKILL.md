---
name: safety-checklist
description: Robotics safety validation checklist for reviewing robot code and configurations. Use when reviewing URDF files, ROS 2 nodes, or any robotics content for safety issues.
allowed-tools: Read, Grep
---

# Safety Checklist

## Instructions

When reviewing robotics content for safety:

1. Check against the safety checklist
2. Flag any missing safety measures
3. Verify all limits are defined
4. Ensure warnings are present for dangerous operations

## Quick Safety Check

Before publishing any robotics content, verify:

- [ ] All joint limits are defined
- [ ] Emergency stop considerations mentioned
- [ ] Simulation-only content is marked
- [ ] No dangerous default values
- [ ] Proper units are used (SI units)

## Safety Categories

### Hardware Safety
- Joint limits and torque limits
- Collision avoidance
- Emergency stop handling

### Software Safety
- Error handling in nodes
- Watchdog timers
- State validation

### Educational Safety
- Clear warnings for real hardware
- Simulation vs real robot distinctions
- Supervised operation requirements

## Reference

See [checklist.md](checklist.md) for the complete safety checklist.
