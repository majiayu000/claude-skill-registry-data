---
name: exercise-patterns
description: Structure for creating hands-on exercises in the Physical AI textbook.
---

## Exercise Template (Strict Format)

```markdown
## Exercise X.Y: [Title]

**Difficulty**: [Beginner | Intermediate | Advanced]
**Time**: [15 min | 30 min | 1 hour | 2 hours]
**Hardware**: [Workstation | Jetson + RealSense | Unitree Robot]

### Objectives
By completing this exercise, you will:
- [Action verb] [specific skill] (e.g., "Create a ROS 2 publisher node")
- [Action verb] [specific skill] (e.g., "Visualize sensor data in RViz2")
- [Action verb] [specific skill] (e.g., "Deploy code to Jetson Orin Nano")

### Prerequisites
- Chapter X completed
- ROS 2 Humble installed
- [Specific hardware setup, e.g., "RealSense D435i connected"]

### Instructions

#### Step 1: [Action]
```bash
# Command to run
ros2 pkg create my_package --build-type ament_python
```

**Expected Output**:
```
Successfully created package 'my_package'
```

#### Step 2: [Action]
[Detailed instructions with code snippets]

#### Step 3: [Verification]
Run this command to verify:
```bash
ros2 topic list
```

**Expected**: You should see `/my_topic` in the list.

### Validation Checklist
- [ ] Code compiles without errors (`colcon build`)
- [ ] Node runs and publishes data (`ros2 topic echo /my_topic`)
- [ ] RViz2 displays data correctly

### Challenge (Optional)
[Extended task for advanced students, e.g., "Modify the node to publish at 100 Hz instead of 10 Hz"]

### Troubleshooting
**Problem**: "Package not found"
**Solution**: Source your workspace (`source install/setup.bash`)

**Problem**: "Topic not visible"
**Solution**: Check if node is running (`ros2 node list`)
```

## Exercise Types

### 1. Thought Experiment (No Code)
**Format**: Conceptual questions to build intuition
**Example**: "List 5 tasks that require physical embodiment that an LLM alone cannot do"

### 2. Simulation Task (Gazebo/Isaac Sim)
**Format**: Code + Launch files + Gazebo world
**Example**: "Spawn a humanoid in Gazebo and make it walk forward 2 meters"

### 3. Hardware Integration (Jetson + Sensors)
**Format**: Deploy ROS 2 node to Jetson, read sensor data
**Example**: "Stream RealSense depth images to your workstation via Wi-Fi"

### 4. Capstone Project (Multi-Week)
**Format**: Complete system with milestones
**Example**: "Build an autonomous room-cleaning robot"

## Progressive Difficulty Curve

**Beginner** (Chapters 1-5):
- Copy-paste code examples
- Run pre-built packages
- Simple parameter changes

**Intermediate** (Chapters 6-15):
- Modify existing code
- Create new nodes
- Integrate multiple sensors

**Advanced** (Chapters 16-28):
- Design complete systems
- Optimize for hardware (Jetson)
- Implement novel algorithms
- Deploy to real robots

## Validation Standards
Every exercise must have:
1. **Clear Success Criteria** - "You should see X" or "The robot should do Y"
2. **Runnable Code** - Copy-paste should work without modification
3. **Hardware Note** - Explicitly state if Jetson/Robot required
4. **Time Estimate** - Realistic completion time for average student
