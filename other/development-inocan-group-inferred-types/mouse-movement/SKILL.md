---
name: mouse-movement
description: Human-like mouse movement patterns. Use when automating browser interactions to avoid bot detection.
---

# Mouse Movement Guidelines

## Principles
- Never move in straight lines
- Add random delays between 50-200ms
- Use bezier curves for natural paths
- Vary movement speed (fast start, slow end)

## Implementation Pattern
```python
import random
import pyautogui

def human_move(x, y):
    duration = random.uniform(0.3, 0.8)
    pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeOutQuad)
    time.sleep(random.uniform(0.05, 0.2))
```

## Anti-Detection Tips
- Add micro-jitters during movement
- Randomize click timing
- Simulate scroll behavior between actions
