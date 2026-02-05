---
name: dev-swarm-use-computer
description: Control the computer by taking screenshots, moving the mouse, clicking, and typing. Use this skill when you need to interact with GUI applications or perform actions that require visual feedback.
---

# Use Computer

This skill enables an agent to interact with the computer's graphical user interface (GUI). It can retrieve screen information, take screenshots of specific regions, and perform mouse and keyboard actions.

## When to Use This Skill

- User needs to interact with GUI applications programmatically
- User asks to automate mouse and keyboard actions
- User wants to take screenshots of specific screen regions
- User needs to test UI flows or perform visual verification
- User requires automated interaction with desktop applications

## Your Roles in This Skill

- **QA Engineer**: Use computer control to perform automated UI testing and verification. Take screenshots to capture UI states and verify visual elements. Execute test scripts that require GUI interaction. Verify application behavior through visual feedback.
- **DevOps Engineer**: Execute Python scripts for computer control operations. Manage system permissions for screen recording and accessibility. Configure screen coordinates and interaction parameters. Troubleshoot PyAutoGUI fail-safe and permission issues.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

All interactions are performed via the `use_computer.py` script. Run it using `uv` from the project root:

```bash
uv run --project dev-swarm/py_scripts python dev-swarm/py_scripts/use_computer.py --json_str '<JSON_COMMAND>'
```

The script returns a JSON response wrapped in `<output></output>` tags.

### 1. Get Screen Information
Use this to understand the monitor setup and primary screen resolution.

**Command:**
```json
{"action": "screen_info"}
```

### 2. Take a Screenshot
Capture a region of the screen with optional scaling and optional pointer marker for coordination correction.

**Command:**
```json
{
  "action": "screenshot",
  "bbox": [x, y, width, height],
  "scale": 1.0,
  "draw_pointer": true,
  "pointer_style": "contrast",
  "pointer_radius": 64
}
```
- `bbox`: (Optional) [left, top, width, height]. If omitted, captures the entire primary screen.
- `scale`: (Optional) Scale factor for the output image (e.g., 0.5 for half size).
- `draw_pointer`: (Optional) Draw a circular marker where the mouse pointer is.
- `pointer_style`: (Optional) Marker style. `contrast` (white border + black dot) or `alert` (red border + yellow dot).
- `pointer_radius`: (Optional) Marker radius in pixels (before scaling).

**Returns:**
Path to the saved image file (usually in the system temp directory), plus `mouse_position` with current cursor coordinates.

**Coordination Correction (Visual Check):**
When `draw_pointer` is enabled, visually verify that the marker in the screenshot matches the returned `mouse_position`. If they do not align (e.g., due to scaling or bbox offsets), adjust your coordinate mapping before issuing the next `input` action.

### 3. Perform Actions
Execute a sequence of mouse and keyboard events.

**Command:**
```json
{
  "action": "input",
  "actions": [
    { "type": "mouse_move", "x": 100, "y": 200, "duration": 0.5 },
    { "type": "click", "button": "left", "clicks": 1, "x": 100, "y": 200 },
    { "type": "type", "text": "Hello, world!", "interval": 0.1 },
    { "type": "key", "keys": ["enter"] },
    { "type": "hotkey", "keys": ["command", "space"] },
    { "type": "wait", "duration": 1.0 }
  ]
}
```

#### Action Types:
- `mouse_move`: Move the cursor to `(x, y)` over `duration` seconds.
- `click`: Click at `(x, y)` (optional) with `button` ('left', 'middle', 'right'), `clicks` count, and `interval` between clicks.
- `type`: Type the specified `text` with `interval` between characters.
- `key`: Press a single key or a list of keys sequentially (e.g., `["enter"]`, `["a", "b", "c"]`).
- `hotkey`: Press a combination of keys simultaneously (e.g., `["command", "v"]`).
- `wait`: Pause execution for `duration` seconds.

## Usage Notes

- **Coordinates**: (0, 0) is the top-left corner of the primary monitor.
- **Fail-safe**: PyAutoGUI has a fail-safe feature. Moving the mouse to any corner of the screen will abort the script.
- **Scaling**: Use a lower `scale` (e.g., 0.5 or 0.25) when taking screenshots for large screens to reduce processing time and token usage if sending to an LLM.
- **Permissions**: Ensure the terminal/IDE has "Screen Recording" and "Accessibility" permissions in System Settings (macOS).
