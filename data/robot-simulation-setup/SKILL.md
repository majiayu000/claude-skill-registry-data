---
name: robot-simulation-setup
description: |
  Generate production-quality Python code for robot simulations that run in Pyodide (browser).
  Supports simplified physics simulations using NumPy, Matplotlib, and basic physics calculations.
  Creates educational code for teaching robot kinematics, dynamics, and control without requiring
  heavy simulation engines (PyBullet/MuJoCo/Gazebo are not Pyodide-compatible).
  Focuses on 2D/3D visualizations, kinematic chains, and simplified dynamics for educational purposes.
version: 1.0.0
allowed-tools: [Bash]
---

# Robot Simulation Setup Skill

**Version:** 1.0.0 | **Alignment:** Constitution v6.0.0, Pyodide-Compatible Code | **Purpose:** Generate educational robot simulation code for browser-based learning

---

## Purpose

Generate production-quality Python code for robot simulations that:
- Run in Pyodide (browser environment)
- Use NumPy, Matplotlib, and SciPy (Pyodide-compatible)
- Visualize robot kinematics, dynamics, and control
- Provide educational value without heavy simulation engines
- Support InteractivePython components in Docusaurus

**Key Constraint**: PyBullet, MuJoCo, and Gazebo are NOT Pyodide-compatible. This skill creates simplified but educational simulations using pure Python + NumPy.

---

## When to Activate

**Activate when:**
- Creating code examples for robot kinematics (forward/inverse)
- Visualizing robot motion, trajectories, or paths
- Demonstrating control algorithms (PID, MPC, etc.)
- Teaching robot dynamics concepts
- Creating interactive robot simulations for lessons

**Trigger phrases:**
- "Create robot simulation code"
- "Generate kinematics visualization"
- "Build robot arm simulation"
- "Create trajectory planning example"
- "Generate control system simulation"

---

## Technical Capabilities

### Supported Simulation Types

1. **2D Robot Arm Simulations**
   - Forward/inverse kinematics
   - Workspace visualization
   - Trajectory planning
   - Joint angle animations

2. **3D Robot Visualizations**
   - 3D coordinate frames
   - Robot pose visualization
   - End-effector trajectories
   - Multi-link robot chains

3. **Simplified Dynamics**
   - Gravity effects
   - Friction models
   - Inertia calculations
   - Force/torque relationships

4. **Control System Simulations**
   - PID control loops
   - Trajectory tracking
   - Error visualization
   - Response plots

### Pyodide-Compatible Libraries

✅ **Supported:**
- NumPy (arrays, linear algebra, transformations)
- Matplotlib (2D/3D plotting, animations)
- SciPy (optimization, signal processing)
- Math (basic math functions)

❌ **NOT Supported:**
- PyBullet (physics engine)
- MuJoCo (physics engine)
- Gazebo (simulator)
- File I/O (reading URDF/SDF files)
- Subprocess (external processes)
- Threading (parallel execution)

---

## Code Generation Standards

### Code Structure

```python
"""
[Clear description of what this simulation demonstrates]

Educational Purpose: [What students will learn]
Physical AI Context: [How this relates to real robots]
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional

# Type hints for all functions
# Comprehensive docstrings (Google style)
# Error handling (try-except where appropriate)
# Clear variable names
# Comments explaining physics/math
```

### Example Template: 2D Robot Arm

```python
"""
2D Robot Arm Forward Kinematics Simulation

Educational Purpose: Students learn how joint angles map to end-effector position
Physical AI Context: Real robot arms use this same mathematics for positioning
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

def forward_kinematics_2d(
    link1_length: float,
    link2_length: float,
    theta1: float,
    theta2: float
) -> Tuple[float, float]:
    """
    Calculate end-effector position for 2D 2-link robot arm.
    
    Args:
        link1_length: Length of first link (meters)
        link2_length: Length of second link (meters)
        theta1: Joint angle 1 (radians)
        theta2: Joint angle 2 (radians)
    
    Returns:
        (x, y) position of end-effector
    """
    # Joint 1 position
    x1 = link1_length * np.cos(theta1)
    y1 = link1_length * np.sin(theta1)
    
    # End-effector position
    x = x1 + link2_length * np.cos(theta1 + theta2)
    y = y1 + link2_length * np.sin(theta1 + theta2)
    
    return x, y

def visualize_robot_arm(
    link1_length: float = 1.0,
    link2_length: float = 0.8,
    theta1: float = np.pi / 4,
    theta2: float = np.pi / 6
):
    """
    Visualize 2D robot arm configuration.
    
    Args:
        link1_length: Length of first link
        link2_length: Length of second link
        theta1: Joint angle 1 (radians)
        theta2: Joint angle 2 (radians)
    """
    # Calculate positions
    x1 = link1_length * np.cos(theta1)
    y1 = link1_length * np.sin(theta1)
    x_end, y_end = forward_kinematics_2d(
        link1_length, link2_length, theta1, theta2
    )
    
    # Plot
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Draw links
    ax.plot([0, x1], [0, y1], 'b-', linewidth=3, label='Link 1')
    ax.plot([x1, x_end], [y1, y_end], 'r-', linewidth=3, label='Link 2')
    
    # Draw joints
    ax.plot(0, 0, 'ko', markersize=10, label='Base')
    ax.plot(x1, y1, 'ko', markersize=10, label='Joint 1')
    ax.plot(x_end, y_end, 'ro', markersize=10, label='End-effector')
    
    # Formatting
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_title('2D Robot Arm Configuration')
    
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    visualize_robot_arm()
```

### Example Template: Trajectory Planning

```python
"""
Robot Trajectory Planning Simulation

Educational Purpose: Students learn how to plan smooth robot motions
Physical AI Context: Real robots use trajectory planning to avoid jerky motions
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

def generate_trajectory(
    start_pos: Tuple[float, float],
    end_pos: Tuple[float, float],
    num_points: int = 100
) -> Tuple[List[float], List[float]]:
    """
    Generate smooth trajectory using cubic interpolation.
    
    Args:
        start_pos: (x, y) starting position
        end_pos: (x, y) ending position
        num_points: Number of trajectory points
    
    Returns:
        (x_trajectory, y_trajectory) lists
    """
    t = np.linspace(0, 1, num_points)
    
    # Cubic interpolation for smooth motion
    x_traj = start_pos[0] + (end_pos[0] - start_pos[0]) * (3*t**2 - 2*t**3)
    y_traj = start_pos[1] + (end_pos[1] - start_pos[1]) * (3*t**2 - 2*t**3)
    
    return x_traj.tolist(), y_traj.tolist()

def visualize_trajectory(
    start_pos: Tuple[float, float] = (0, 0),
    end_pos: Tuple[float, float] = (2, 1.5)
):
    """Visualize planned trajectory."""
    x_traj, y_traj = generate_trajectory(start_pos, end_pos)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.plot(x_traj, y_traj, 'b-', linewidth=2, label='Planned Trajectory')
    ax.plot(start_pos[0], start_pos[1], 'go', markersize=10, label='Start')
    ax.plot(end_pos[0], end_pos[1], 'ro', markersize=10, label='End')
    
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_title('Robot Trajectory Planning')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.show()
```

---

## Best Practices

### 1. Educational Focus
- **Start Simple**: Begin with 2D, single-link examples
- **Build Complexity**: Progress to 3D, multi-link robots
- **Real-World Context**: Connect to actual robot applications
- **Visual Clarity**: Use clear colors, labels, legends

### 2. Code Quality
- **Type Hints**: All functions should have type hints
- **Docstrings**: Google-style docstrings for all functions
- **Error Handling**: Validate inputs, handle edge cases
- **Comments**: Explain physics/math concepts in comments

### 3. Pyodide Compatibility
- **Test in Browser**: Verify code runs in InteractivePython
- **Avoid File I/O**: Don't read URDF/SDF files
- **Use NumPy**: Prefer NumPy arrays over Python lists for performance
- **Limit Complexity**: Keep simulations lightweight for browser

### 4. Interactive Elements
- **Parameter Tuning**: Allow students to modify joint angles, link lengths
- **Real-Time Updates**: Show how changes affect robot configuration
- **Multiple Views**: Provide different visualization perspectives

---

## Common Patterns

### Pattern 1: Forward Kinematics
```python
# Calculate end-effector position from joint angles
def forward_kinematics(joint_angles, link_lengths):
    # Implementation
    pass
```

### Pattern 2: Inverse Kinematics
```python
# Calculate joint angles from desired end-effector position
def inverse_kinematics(target_pos, link_lengths):
    # Implementation (may use optimization)
    pass
```

### Pattern 3: Workspace Visualization
```python
# Show reachable positions of robot
def visualize_workspace(link_lengths):
    # Generate reachable points
    # Plot workspace boundary
    pass
```

### Pattern 4: Trajectory Animation
```python
# Animate robot following a trajectory
def animate_trajectory(trajectory_points):
    # For each point, calculate joint angles
    # Visualize robot configuration
    pass
```

---

## Integration with InteractivePython

### Usage in MDX Files

```mdx
<InteractivePython>
{`
import numpy as np
import matplotlib.pyplot as plt

# [Generated simulation code here]
`}
</InteractivePython>
```

### Student Modifications

Encourage students to:
- Modify joint angles and observe effects
- Change link lengths and see workspace changes
- Adjust trajectory parameters
- Experiment with different control gains

---

## Troubleshooting

### Issue: Code doesn't run in Pyodide
**Solution**: Check for unsupported libraries. Use only NumPy, Matplotlib, SciPy, Math.

### Issue: Animation too slow
**Solution**: Reduce number of points, simplify calculations, use vectorized NumPy operations.

### Issue: Visualization unclear
**Solution**: Add labels, legends, grid, adjust colors, use appropriate aspect ratios.

---

## Output Format

When generating code:
1. **Header Comment**: Clear description and educational purpose
2. **Imports**: Only Pyodide-compatible libraries
3. **Functions**: Type hints, docstrings, error handling
4. **Example Usage**: Working example that demonstrates functionality
5. **Visualization**: Clear, labeled plots with appropriate formatting

---

**Remember**: You're creating educational simulations, not production robot controllers. Focus on clarity, learning, and Pyodide compatibility over realism.

