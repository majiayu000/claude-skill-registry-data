---
name: motion-planning
description: |
  Generate production-quality Python code for robot motion planning algorithms that run in
  Pyodide (browser). Creates educational code for teaching path planning (A*, RRT), trajectory
  optimization, PID control, model predictive control (MPC), and whole-body control.
  Focuses on algorithm implementation, visualization, and educational clarity.
version: 1.0.0
allowed-tools: [Bash]
---

# Motion Planning Skill

**Version:** 1.0.0 | **Alignment:** Constitution v6.0.0, Pyodide-Compatible Code | **Purpose:** Generate educational motion planning code for browser-based learning

---

## Purpose

Generate production-quality Python code for motion planning that:
- Runs in Pyodide (browser environment)
- Implements path planning algorithms (A*, RRT, etc.)
- Demonstrates trajectory optimization
- Shows control algorithms (PID, MPC)
- Provides educational value for robot motion
- Supports InteractivePython components in Docusaurus

**Key Focus**: Teaching motion planning algorithms and control theory, not just using planning libraries.

---

## When to Activate

**Activate when:**
- Creating code examples for path planning (A*, RRT, Dijkstra)
- Demonstrating trajectory optimization
- Teaching PID control for robots
- Creating model predictive control (MPC) examples
- Building whole-body control systems

**Trigger phrases:**
- "Create path planning code"
- "Generate A* algorithm example"
- "Build PID controller for robot"
- "Create trajectory optimization code"
- "Generate MPC control example"

---

## Technical Capabilities

### Supported Algorithms

1. **Path Planning**
   - A* algorithm
   - RRT (Rapidly-exploring Random Tree)
   - Dijkstra's algorithm
   - Potential fields

2. **Trajectory Optimization**
   - Minimum jerk trajectories
   - Time-optimal trajectories
   - Constrained optimization
   - Smooth path generation

3. **Control Algorithms**
   - PID control
   - Feedforward control
   - Model Predictive Control (MPC)
   - LQR (Linear Quadratic Regulator)

4. **Whole-Body Control**
   - Task-space control
   - Null-space control
   - Prioritized control

### Pyodide-Compatible Libraries

✅ **Supported:**
- NumPy (arrays, linear algebra, optimization)
- Matplotlib (plotting paths, trajectories, control responses)
- SciPy (optimization, signal processing, interpolation)
- Math (basic math functions)

❌ **NOT Supported:**
- OMPL (Open Motion Planning Library)
- ROS navigation stack
- Real-time control libraries
- Hardware-specific controllers

---

## Code Generation Standards

### Code Structure

```python
"""
[Motion Planning Algorithm] Implementation

Educational Purpose: [What students will learn]
Physical AI Context: [How real robots use this algorithm]
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional
from scipy.optimize import minimize

# Type hints for all functions
# Comprehensive docstrings (Google style)
# Error handling (try-except where appropriate)
# Clear algorithm implementation
# Visualization of results
```

### Example Template: A* Path Planning

```python
"""
A* Path Planning Algorithm

Educational Purpose: Students learn how A* finds optimal paths
Physical AI Context: Real robots use A* for navigation and motion planning
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
from heapq import heappush, heappop

class Node:
    """Node in A* search graph."""
    
    def __init__(self, x: int, y: int, g: float = 0, h: float = 0, parent=None):
        self.x = x
        self.y = y
        self.g = g  # Cost from start
        self.h = h  # Heuristic to goal
        self.f = g + h  # Total cost
        self.parent = parent
    
    def __lt__(self, other):
        return self.f < other.f

def heuristic(node: Node, goal: Tuple[int, int]) -> float:
    """
    Euclidean distance heuristic for A*.
    
    Args:
        node: Current node
        goal: Goal position (x, y)
    
    Returns:
        Estimated cost to goal
    """
    return np.sqrt((node.x - goal[0])**2 + (node.y - goal[1])**2)

def astar_path_planning(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    obstacles: List[Tuple[int, int]],
    grid_size: Tuple[int, int] = (20, 20)
) -> Optional[List[Tuple[int, int]]]:
    """
    A* path planning algorithm.
    
    Args:
        start: Start position (x, y)
        goal: Goal position (x, y)
        obstacles: List of obstacle positions
        grid_size: Grid dimensions (width, height)
    
    Returns:
        Path as list of (x, y) positions, or None if no path found
    """
    open_set = []
    closed_set = set()
    obstacle_set = set(obstacles)
    
    start_node = Node(start[0], start[1], 0, heuristic(Node(start[0], start[1]), goal))
    heappush(open_set, start_node)
    
    while open_set:
        current = heappop(open_set)
        
        if (current.x, current.y) in closed_set:
            continue
        
        closed_set.add((current.x, current.y))
        
        # Check if goal reached
        if current.x == goal[0] and current.y == goal[1]:
            # Reconstruct path
            path = []
            node = current
            while node:
                path.append((node.x, node.y))
                node = node.parent
            return path[::-1]
        
        # Explore neighbors (8-connected)
        for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            nx, ny = current.x + dx, current.y + dy
            
            # Check bounds
            if nx < 0 or nx >= grid_size[0] or ny < 0 or ny >= grid_size[1]:
                continue
            
            # Check obstacle
            if (nx, ny) in obstacle_set:
                continue
            
            # Check if already explored
            if (nx, ny) in closed_set:
                continue
            
            # Calculate costs
            move_cost = np.sqrt(dx**2 + dy**2)  # Diagonal moves cost more
            g_new = current.g + move_cost
            h_new = heuristic(Node(nx, ny), goal)
            
            neighbor = Node(nx, ny, g_new, h_new, current)
            heappush(open_set, neighbor)
    
    return None  # No path found

def visualize_path(
    start: Tuple[int, int] = (0, 0),
    goal: Tuple[int, int] = (19, 19),
    obstacles: List[Tuple[int, int]] = [(5, 5), (10, 10), (15, 15)]
):
    """Visualize A* path planning."""
    path = astar_path_planning(start, goal, obstacles)
    
    if path is None:
        print("No path found!")
        return
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Draw grid
    grid = np.zeros((20, 20))
    for ox, oy in obstacles:
        grid[oy, ox] = 1
    
    ax.imshow(grid, cmap='gray', origin='lower', alpha=0.3)
    
    # Draw path
    path_x = [p[0] for p in path]
    path_y = [p[1] for p in path]
    ax.plot(path_x, path_y, 'b-', linewidth=2, label='Planned Path')
    ax.scatter(path_x, path_y, c='blue', s=50, zorder=5)
    
    # Draw start and goal
    ax.plot(start[0], start[1], 'go', markersize=15, label='Start', zorder=6)
    ax.plot(goal[0], goal[1], 'ro', markersize=15, label='Goal', zorder=6)
    
    # Draw obstacles
    for ox, oy in obstacles:
        ax.add_patch(plt.Rectangle((ox-0.5, oy-0.5), 1, 1, 
                                   facecolor='black', edgecolor='black'))
    
    ax.set_xlim(-0.5, 19.5)
    ax.set_ylim(-0.5, 19.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('A* Path Planning')
    ax.legend()
    
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    visualize_path()
```

### Example Template: PID Control

```python
"""
PID Control for Robot Motion

Educational Purpose: Students learn how PID controllers work for robot control
Physical AI Context: Real robots use PID control for position, velocity, and force control
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

class PIDController:
    """PID controller implementation."""
    
    def __init__(self, kp: float, ki: float, kd: float, dt: float = 0.01):
        """
        Initialize PID controller.
        
        Args:
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
            dt: Time step (seconds)
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.integral = 0.0
        self.prev_error = 0.0
    
    def compute(self, setpoint: float, current_value: float) -> float:
        """
        Compute PID control output.
        
        Args:
            setpoint: Desired value
            current_value: Current value
        
        Returns:
            Control output
        """
        error = setpoint - current_value
        
        # Proportional term
        p_term = self.kp * error
        
        # Integral term
        self.integral += error * self.dt
        i_term = self.ki * self.integral
        
        # Derivative term
        derivative = (error - self.prev_error) / self.dt
        d_term = self.kd * derivative
        
        # Update for next iteration
        self.prev_error = error
        
        # Total output
        output = p_term + i_term + d_term
        
        return output
    
    def reset(self):
        """Reset controller state."""
        self.integral = 0.0
        self.prev_error = 0.0

def simulate_pid_control(
    kp: float = 1.0,
    ki: float = 0.1,
    kd: float = 0.5,
    duration: float = 10.0,
    dt: float = 0.01
):
    """
    Simulate PID control system.
    
    Args:
        kp: Proportional gain
        ki: Integral gain
        kd: Derivative gain
        duration: Simulation duration (seconds)
        dt: Time step (seconds)
    """
    pid = PIDController(kp, ki, kd, dt)
    
    time = np.arange(0, duration, dt)
    setpoint = np.ones_like(time) * 1.0  # Step input
    position = np.zeros_like(time)
    velocity = np.zeros_like(time)
    
    # Simple dynamics: mass-spring-damper
    mass = 1.0
    damping = 0.1
    
    for i in range(1, len(time)):
        # Compute control
        control = pid.compute(setpoint[i], position[i-1])
        
        # Update dynamics
        acceleration = (control - damping * velocity[i-1]) / mass
        velocity[i] = velocity[i-1] + acceleration * dt
        position[i] = position[i-1] + velocity[i] * dt
    
    # Visualize
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.plot(time, setpoint, 'r--', label='Setpoint', linewidth=2)
    ax1.plot(time, position, 'b-', label='Position', linewidth=2)
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Position')
    ax1.set_title('PID Control: Position Response')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    error = setpoint - position
    ax2.plot(time, error, 'g-', label='Error', linewidth=2)
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Error')
    ax2.set_title('Control Error')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    simulate_pid_control()
```

---

## Best Practices

### 1. Algorithm Clarity
- **Step-by-step**: Show algorithm execution step-by-step
- **Visualization**: Plot paths, trajectories, control responses
- **Comments**: Explain algorithm logic in comments
- **Pseudocode**: Include algorithm structure in docstrings

### 2. Educational Focus
- **Start Simple**: Begin with 2D, single-robot examples
- **Build Complexity**: Progress to 3D, multi-robot scenarios
- **Compare Algorithms**: Show different planning/control approaches
- **Real-World Context**: Connect to actual robot applications

### 3. Code Quality
- **Type Hints**: All functions should have type hints
- **Docstrings**: Google-style docstrings explaining algorithms
- **Error Handling**: Validate inputs, handle edge cases
- **Modularity**: Separate algorithm from visualization

### 4. Performance
- **Efficient Implementation**: Use vectorized NumPy operations
- **Reasonable Complexity**: Keep algorithms simple enough for browser
- **Optimization**: Use SciPy optimization where appropriate

---

## Common Patterns

### Pattern 1: Path Planning
```python
def plan_path(start, goal, obstacles):
    # Initialize search
    # Explore graph
    # Find optimal path
    # Return path
    pass
```

### Pattern 2: Trajectory Generation
```python
def generate_trajectory(waypoints, constraints):
    # Interpolate between waypoints
    # Optimize for smoothness/time
    # Return trajectory
    pass
```

### Pattern 3: Control Loop
```python
def control_loop(setpoint, current_state, controller):
    # Compute error
    # Compute control output
    # Apply to system
    # Return new state
    pass
```

### Pattern 4: Optimization-Based Planning
```python
def optimize_trajectory(objective, constraints):
    # Define optimization problem
    # Solve using scipy.optimize
    # Return optimal trajectory
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

# [Generated motion planning code here]
`}
</InteractivePython>
```

### Student Modifications

Encourage students to:
- Modify algorithm parameters (gains, weights, etc.)
- Change start/goal positions
- Add/remove obstacles
- Experiment with different algorithms
- Tune control parameters

---

## Troubleshooting

### Issue: Path planning too slow
**Solution**: Reduce grid resolution, limit search space, use simpler heuristics.

### Issue: Control unstable
**Solution**: Check gains, ensure proper initialization, validate system dynamics.

### Issue: Visualization unclear
**Solution**: Add labels, legends, use appropriate colors, show multiple views.

---

## Output Format

When generating code:
1. **Header Comment**: Clear description and educational purpose
2. **Algorithm Class/Function**: Clear implementation with comments
3. **Visualization**: Clear plots showing paths, trajectories, or control responses
4. **Example Usage**: Working example demonstrating functionality
5. **Parameter Tuning**: Show how parameters affect results

---

**Remember**: You're teaching motion planning and control algorithms. Focus on understanding how algorithms work, not just using planning libraries.

