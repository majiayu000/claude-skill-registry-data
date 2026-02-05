---
name: content-writer
description: Write technical content for the Physical AI textbook including chapters, examples, code snippets, and exercises. Use when creating new chapters, writing module content, adding code examples, or creating assessments.
---

# Content Writer Skill

## Instructions

1. **Chapter Structure**
   - Start with learning objectives (3-5 bullet points)
   - Include "Prerequisites" section linking to prior chapters
   - Use h2 for major topics, h3 for subtopics
   - End with "Key Takeaways" and "Next Steps"

2. **Code Examples**
   - Always include working, tested code
   - Add comments explaining key lines
   - Provide both minimal and full examples
   - Include expected output in comments

3. **Technical Accuracy**
   - Verify all commands with Context7 before writing
   - Check version compatibility (ROS 2, Python 3.11+, etc.)
   - Link to official documentation
   - Include troubleshooting tips

4. **Exercises & Assessments**
   - Progressive difficulty (beginner → advanced)
   - Include hints and solutions (collapsible)
   - Tie to real-world robotics scenarios
   - Provide rubrics for self-assessment

5. **RAG-Friendly Formatting**
   - Use descriptive headings (not "Introduction" alone)
   - Include frontmatter: title, description, module, week, tags
   - Avoid excessive nesting (max 3 levels)
   - Keep paragraphs focused (1 idea per paragraph)

## Examples

```mdx
---
title: "ROS 2 Nodes and Topics"
description: "Learn to create ROS 2 nodes that communicate via topics"
module: 1
week: 3
tags: [ros2, nodes, topics, python, rclpy]
---

# ROS 2 Nodes and Topics

## Learning Objectives

By the end of this chapter, you will be able to:
- Create a ROS 2 node using Python and rclpy
- Publish messages to a topic
- Subscribe to topics and process incoming messages
- Understand the ROS 2 communication graph

## Prerequisites

- [Week 1-2: Introduction to Physical AI](/docs/module-1/week-1-2/intro)
- Python 3.10+ installed
- ROS 2 Humble or later

## Creating Your First Node

A ROS 2 node is the fundamental building block...

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        # Timer fires every 0.5 seconds
        self.timer = self.create_timer(0.5, self.timer_callback)
    
    def timer_callback(self):
        msg = String()
        msg.data = 'Hello, Physical AI!'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
```

## Key Takeaways

- Nodes are independent processes in ROS 2
- Topics enable publish-subscribe communication
- `rclpy` is the Python client library for ROS 2

## Next Steps

Continue to [Week 4: ROS 2 Services](/docs/module-1/week-4/services)
```

## Definition of Done

- Chapter follows structure template
- All code examples are tested and working
- Frontmatter complete with proper tags
- Links to prerequisites and next chapters included
- At least one exercise with solution
