---
name: cam
description: Computer-aided manufacturing processes
license: MIT
compatibility: opencode
metadata:
  audience: manufacturing engineers, CNC programmers
  category: engineering
---

## What I do

- Generate CNC machine toolpaths from CAD models
- Select appropriate machining strategies and tools
- Optimize cutting parameters for efficiency and quality
- Simulate machining operations to detect collisions
- Post-process toolpaths to machine-specific formats

## When to use me

- When programming CNC machines (mills, lathes, routers)
- When selecting cutting tools and parameters
- When simulating machining operations offline
- When optimizing manufacturing workflows
- When generating G-code for CNC machines

## Key Concepts

### CNC Programming Basics

```python
# G-code fundamentals
class GCodeGenerator:
    # Rapid move (positioning)
    def rapid(self, x=None, y=None, z=None):
        coords = self._format_coords(x, y, z)
        return f"G0 {coords}"
    
    # Linear feed (cutting move)
    def linear_feed(self, x=None, y=None, z=None, feed=100):
        coords = self._format_coords(x, y, z)
        return f"G1 {coords} F{feed}"
    
    # Circular interpolation (clockwise)
    def clockwise_arc(self, x, y, i, j, feed=100):
        return f"G2 X{x} Y{y} I{i} J{j} F{feed}"
    
    # Circular interpolation (counter-clockwise)
    def counterclockwise_arc(self, x, y, i, j, feed=100):
        return f"G3 X{x} Y{y} I{i} J{j} F{feed}"
    
    # Tool change
    def tool_change(self, tool_number):
        return f"M6 T{tool_number}"
    
    # Spindle control
    def spindle_on(self, rpm, clockwise=True):
        direction = "M3" if clockwise else "M4"
        return f"{direction} S{rpm}"
    
    def spindle_off(self):
        return "M5"
```

### Machining Operations

| Operation | Description | Applications |
|-----------|-------------|--------------|
| Facing | Flat surface on top | Stock removal |
| Roughing | Bulk material removal | Near-net shape |
| Finishing | Final surface quality | Precision surfaces |
| Pocket milling | Internal cavities | Molds, pockets |
| Profile milling | Contour following | Complex shapes |
| Drilling | Hole creation | Fasteners, passes |
| Tapping | Thread creation | Threaded holes |
| Turning | Rotational cutting | Cylindrical parts |

### Tool Selection

```python
# Cutting parameters calculation
class CuttingParameters:
    @staticmethod
    def calculate_sfm(diameter, rpm):
        """Surface feet per minute"""
        return 3.14159 * diameter * rpm / 12
    
    @staticmethod
    def calculate_rpm(sfm, diameter):
        """Revolutions per minute"""
        return (sfm * 12) / (3.14159 * diameter)
    
    @staticmethod
    def calculate_feed_rate(rpm, chip_load, num_flutes):
        """IPM = RPM × chip load × number of flutes"""
        return rpm * chip_load * num_flutes
    
    @staticmethod
    def calculate_mrr(depth, width, feed_rate):
        """Material removal rate (cubic inches/min)"""
        return depth * width * feed_rate
```

### Post-Processing

```python
# Post-processor configuration
POST_PROCESSOR_CONFIG = {
    "controller": "Fanuc",
    "output_format": "NC file",
    "settings": {
        "line_numbers": True,
        "decimal_places": 3,
        "modal": True,
        "tool_change": "M6",
        "coolant": {
            "on": "M8",
            "off": "M9"
        }
    }
}
```

### CAM Software

| Software | Specialty |
|----------|-----------|
| MasterCAM | General purpose CNC |
| Fusion 360 | Cloud-based CAM |
| SolidCAM | Integrated with SolidWorks |
| Delcam | Complex geometries |
| GibbsCAM | Multi-axis machining |
| HSMWorks | High-speed machining |
