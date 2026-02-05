---
name: ros2-patterns
description: ROS 2 node templates and message types for robotics development. Use when creating ROS 2 nodes, understanding message types, or writing publisher/subscriber patterns.
allowed-tools: Read, Bash
---

# ROS 2 Patterns

## Instructions

When creating ROS 2 code:

1. Use the provided templates as starting points
2. Follow ROS 2 Humble conventions
3. Include proper error handling
4. Add docstrings and comments

## Common Patterns

| Pattern | Template | Use Case |
|---------|----------|----------|
| Publisher | publisher.py | Sending data to topics |
| Subscriber | subscriber.py | Receiving data from topics |
| Service Server | (extend publisher) | Request/response pattern |
| Action Server | (advanced) | Long-running tasks |

## Node Structure

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('node_name')
        # Initialize publishers, subscribers, timers

    def callback(self, msg):
        # Handle incoming messages
        pass

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Reference

See [messages.md](messages.md) for common message types.
See [templates/](templates/) for complete templates.
