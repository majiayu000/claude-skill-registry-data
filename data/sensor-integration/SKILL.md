---
name: sensor-integration
description: |
  Generate production-quality Python code for sensor integration, sensor fusion, and perception
  systems that run in Pyodide (browser). Creates educational code for teaching IMU sensors,
  LiDAR simulation, depth perception, tactile sensors, and sensor fusion algorithms.
  Focuses on sensor data processing, calibration, noise modeling, and multi-sensor fusion
  for educational purposes.
version: 1.0.0
allowed-tools: [Bash]
---

# Sensor Integration Skill

**Version:** 1.0.0 | **Alignment:** Constitution v6.0.0, Pyodide-Compatible Code | **Purpose:** Generate educational sensor integration code for browser-based learning

---

## Purpose

Generate production-quality Python code for sensor integration that:
- Runs in Pyodide (browser environment)
- Demonstrates sensor data processing and fusion
- Simulates sensor noise and calibration
- Provides educational value for perception systems
- Supports InteractivePython components in Docusaurus

**Key Focus**: Teaching how robots perceive the world through sensors, not just using sensor libraries.

---

## When to Activate

**Activate when:**
- Creating code examples for IMU sensors (accelerometer, gyroscope, magnetometer)
- Demonstrating sensor fusion algorithms (Kalman filtering, complementary filters)
- Teaching depth perception (stereo vision, LiDAR simulation)
- Creating tactile sensor examples
- Building multi-sensor perception systems

**Trigger phrases:**
- "Create sensor fusion code"
- "Generate IMU sensor example"
- "Build Kalman filter for sensors"
- "Create depth perception simulation"
- "Generate sensor calibration code"

---

## Technical Capabilities

### Supported Sensor Types

1. **IMU Sensors**
   - Accelerometer (3-axis acceleration)
   - Gyroscope (angular velocity)
   - Magnetometer (magnetic field)
   - Sensor fusion (attitude estimation)

2. **Depth Sensors**
   - Simulated LiDAR (2D/3D point clouds)
   - Depth camera simulation
   - Stereo vision depth estimation

3. **Tactile Sensors**
   - Force/torque sensors
   - Contact detection
   - Pressure distribution

4. **Sensor Fusion**
   - Kalman filtering
   - Complementary filters
   - Multi-sensor state estimation

### Pyodide-Compatible Libraries

✅ **Supported:**
- NumPy (arrays, linear algebra, signal processing)
- Matplotlib (plotting sensor data, visualizations)
- SciPy (filtering, optimization, signal processing)
- Math (basic math functions)

❌ **NOT Supported:**
- ROS (Robot Operating System)
- Sensor hardware drivers
- Real-time sensor libraries
- File I/O (reading sensor logs)

---

## Code Generation Standards

### Code Structure

```python
"""
[Sensor type] Integration Example

Educational Purpose: [What students will learn about sensors]
Physical AI Context: [How real robots use this sensor]
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional

# Type hints for all functions
# Comprehensive docstrings (Google style)
# Error handling (try-except where appropriate)
# Noise modeling for realistic sensor behavior
# Calibration examples
```

### Example Template: IMU Sensor Fusion

```python
"""
IMU Sensor Fusion using Complementary Filter

Educational Purpose: Students learn how to combine accelerometer and gyroscope data
Physical AI Context: Real robots use sensor fusion for accurate attitude estimation
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List

class IMUSensor:
    """Simulated IMU sensor with noise."""
    
    def __init__(self, noise_level: float = 0.1):
        """
        Initialize IMU sensor.
        
        Args:
            noise_level: Standard deviation of sensor noise
        """
        self.noise_level = noise_level
    
    def read_accelerometer(self, true_accel: np.ndarray) -> np.ndarray:
        """
        Read accelerometer with noise.
        
        Args:
            true_accel: True acceleration [ax, ay, az]
        
        Returns:
            Noisy acceleration measurement
        """
        noise = np.random.normal(0, self.noise_level, 3)
        return true_accel + noise
    
    def read_gyroscope(self, true_angular_vel: np.ndarray) -> np.ndarray:
        """
        Read gyroscope with noise.
        
        Args:
            true_angular_vel: True angular velocity [wx, wy, wz]
        
        Returns:
            Noisy angular velocity measurement
        """
        noise = np.random.normal(0, self.noise_level, 3)
        return true_angular_vel + noise

def complementary_filter(
    accel_data: np.ndarray,
    gyro_data: np.ndarray,
    dt: float,
    alpha: float = 0.98
) -> float:
    """
    Complementary filter for attitude estimation.
    
    Combines accelerometer (low-frequency) and gyroscope (high-frequency) data.
    
    Args:
        accel_data: Accelerometer reading [ax, ay, az]
        gyro_data: Gyroscope reading [wx, wy, wz]
        dt: Time step (seconds)
        alpha: Filter coefficient (0-1), higher = trust gyro more
    
    Returns:
        Estimated pitch angle (radians)
    """
    # Calculate pitch from accelerometer
    pitch_accel = np.arctan2(accel_data[0], np.sqrt(accel_data[1]**2 + accel_data[2]**2))
    
    # Integrate gyroscope
    pitch_gyro = pitch_gyro + gyro_data[1] * dt
    
    # Complementary filter: blend accel (low-freq) and gyro (high-freq)
    pitch = alpha * pitch_gyro + (1 - alpha) * pitch_accel
    
    return pitch

def simulate_imu_fusion(
    duration: float = 10.0,
    dt: float = 0.01,
    noise_level: float = 0.1
):
    """
    Simulate IMU sensor fusion.
    
    Args:
        duration: Simulation duration (seconds)
        dt: Time step (seconds)
        noise_level: Sensor noise level
    """
    imu = IMUSensor(noise_level=noise_level)
    
    time = np.arange(0, duration, dt)
    true_pitch = 0.5 * np.sin(0.5 * time)  # True pitch motion
    estimated_pitch = []
    
    pitch_gyro = 0.0  # Initialize
    
    for t in time:
        # True sensor values (simplified)
        true_accel = np.array([np.sin(true_pitch[int(t/dt)]), 0, np.cos(true_pitch[int(t/dt)])])
        true_gyro = np.array([0, 0.5 * 0.5 * np.cos(0.5 * t), 0])  # Derivative of pitch
        
        # Read sensors
        accel = imu.read_accelerometer(true_accel)
        gyro = imu.read_gyroscope(true_gyro)
        
        # Sensor fusion
        pitch = complementary_filter(accel, gyro, dt)
        estimated_pitch.append(pitch)
        pitch_gyro = pitch
    
    # Visualize
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(time, np.degrees(true_pitch), 'b-', label='True Pitch', linewidth=2)
    ax.plot(time, np.degrees(estimated_pitch), 'r--', label='Estimated Pitch', linewidth=2)
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Pitch Angle (degrees)')
    ax.set_title('IMU Sensor Fusion: Complementary Filter')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    simulate_imu_fusion()
```

### Example Template: LiDAR Simulation

```python
"""
2D LiDAR Simulation

Educational Purpose: Students learn how LiDAR sensors work and process point clouds
Physical AI Context: Real robots use LiDAR for mapping and obstacle detection
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

def simulate_lidar_2d(
    robot_pos: Tuple[float, float],
    robot_angle: float,
    obstacles: List[Tuple[float, float, float]],  # (x, y, radius)
    max_range: float = 5.0,
    num_beams: int = 360
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simulate 2D LiDAR scan.
    
    Args:
        robot_pos: Robot position (x, y)
        robot_angle: Robot orientation (radians)
        obstacles: List of circular obstacles (x, y, radius)
        max_range: Maximum LiDAR range (meters)
        num_beams: Number of LiDAR beams
    
    Returns:
        (angles, ranges) - LiDAR scan data
    """
    angles = np.linspace(0, 2*np.pi, num_beams)
    ranges = np.full(num_beams, max_range)
    
    for i, angle in enumerate(angles):
        beam_angle = robot_angle + angle
        
        # Ray casting
        for obstacle in obstacles:
            # Calculate intersection with circular obstacle
            # (simplified ray-circle intersection)
            dx = np.cos(beam_angle)
            dy = np.sin(beam_angle)
            
            # Ray from robot
            ox, oy = robot_pos
            cx, cy, r = obstacle
            
            # Vector from robot to obstacle center
            to_center = np.array([cx - ox, cy - oy])
            to_center_dist = np.linalg.norm(to_center)
            
            # Project onto ray
            proj = np.dot(to_center, [dx, dy])
            
            if proj > 0:  # Obstacle in front
                perp_dist = np.sqrt(to_center_dist**2 - proj**2)
                if perp_dist < r:  # Ray intersects obstacle
                    # Calculate intersection distance
                    intersection_dist = proj - np.sqrt(r**2 - perp_dist**2)
                    if 0 < intersection_dist < ranges[i]:
                        ranges[i] = intersection_dist
    
    return angles, ranges

def visualize_lidar_scan(
    robot_pos: Tuple[float, float] = (0, 0),
    robot_angle: float = 0,
    obstacles: List[Tuple[float, float, float]] = [(2, 1, 0.5), (-1, 2, 0.3)]
):
    """Visualize 2D LiDAR scan."""
    angles, ranges = simulate_lidar_2d(robot_pos, robot_angle, obstacles)
    
    # Convert to Cartesian
    x_points = robot_pos[0] + ranges * np.cos(robot_angle + angles)
    y_points = robot_pos[1] + ranges * np.sin(robot_angle + angles)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Draw obstacles
    for ox, oy, r in obstacles:
        circle = plt.Circle((ox, oy), r, color='gray', alpha=0.5)
        ax.add_patch(circle)
    
    # Draw LiDAR scan
    ax.scatter(x_points, y_points, c=ranges, cmap='viridis', s=10)
    
    # Draw robot
    ax.plot(robot_pos[0], robot_pos[1], 'ro', markersize=15, label='Robot')
    ax.arrow(robot_pos[0], robot_pos[1], 
             0.5*np.cos(robot_angle), 0.5*np.sin(robot_angle),
             head_width=0.1, head_length=0.1, fc='red', ec='red')
    
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_title('2D LiDAR Scan Simulation')
    ax.legend()
    
    plt.tight_layout()
    plt.show()
```

---

## Best Practices

### 1. Realistic Noise Modeling
- Add Gaussian noise to sensor readings
- Model sensor drift (gyroscope bias)
- Include quantization effects
- Show how noise affects fusion algorithms

### 2. Calibration Examples
- Sensor offset calibration
- Scale factor calibration
- Coordinate frame alignment
- Temperature compensation (conceptual)

### 3. Educational Clarity
- Show raw sensor data vs. processed data
- Visualize sensor fusion process step-by-step
- Compare different fusion algorithms
- Demonstrate sensor limitations

### 4. Code Quality
- Type hints for all functions
- Comprehensive docstrings
- Error handling for invalid inputs
- Clear variable names

---

## Common Patterns

### Pattern 1: Sensor Reading with Noise
```python
def read_sensor(true_value, noise_std):
    noise = np.random.normal(0, noise_std)
    return true_value + noise
```

### Pattern 2: Kalman Filter
```python
def kalman_filter(measurement, state_estimate, uncertainty):
    # Prediction step
    # Update step
    # Return new estimate
    pass
```

### Pattern 3: Sensor Calibration
```python
def calibrate_sensor(raw_readings, known_values):
    # Calculate offset and scale
    # Return calibration parameters
    pass
```

### Pattern 4: Multi-Sensor Fusion
```python
def fuse_sensors(imu_data, camera_data, lidar_data):
    # Combine data from multiple sensors
    # Weight by sensor reliability
    # Return fused estimate
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

# [Generated sensor code here]
`}
</InteractivePython>
```

### Student Modifications

Encourage students to:
- Adjust noise levels and observe effects
- Modify filter parameters
- Change sensor configurations
- Experiment with different fusion algorithms

---

## Troubleshooting

### Issue: Sensor fusion unstable
**Solution**: Check filter parameters, ensure proper initialization, validate sensor data ranges.

### Issue: Visualization unclear
**Solution**: Add labels, legends, use appropriate color maps, show multiple views.

### Issue: Code too slow
**Solution**: Use vectorized NumPy operations, reduce number of sensor readings, optimize algorithms.

---

## Output Format

When generating code:
1. **Header Comment**: Clear description and educational purpose
2. **Sensor Class/Function**: Simulated sensor with noise
3. **Processing Functions**: Fusion, filtering, calibration
4. **Visualization**: Clear plots showing sensor data and processing results
5. **Example Usage**: Working example demonstrating functionality

---

**Remember**: You're teaching how robots perceive the world. Focus on understanding sensor principles, noise, and fusion algorithms, not just using sensor libraries.

