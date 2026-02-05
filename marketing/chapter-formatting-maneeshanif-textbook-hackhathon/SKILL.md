---
name: chapter-formatting
description: Enforce consistent chapter formatting, numbering conventions, and structural alignment across the entire textbook. Use when creating new chapters, reviewing existing content for consistency, or establishing formatting standards.
---

# Chapter Formatting Skill

## Instructions

### 1. Numbering Convention

All chapters follow a hierarchical numbering system:

```
Module X.Y.Z — Title
│
├── X = Module number (1-4)
├── Y = Week number within module
└── Z = Section number within week (optional)

Examples:
- Module 1.1 — Introduction to Physical AI
- Module 1.2.1 — ROS 2 Node Basics
- Module 2.3 — Unity Visualization Setup
```

### 2. File Naming Convention

```
docs/
├── module-1/
│   ├── _category_.json          # Module metadata
│   ├── index.mdx                # Module overview (1.0)
│   ├── week-1-2/
│   │   ├── _category_.json
│   │   ├── index.mdx            # Week overview (1.1)
│   │   ├── 01-embodied-ai.mdx   # Section 1.1.1
│   │   ├── 02-humanoid-overview.mdx  # Section 1.1.2
│   │   └── 03-sensors.mdx       # Section 1.1.3
│   └── week-3-5/
│       ├── index.mdx            # Week overview (1.2)
│       ├── 01-nodes.mdx
│       ├── 02-topics.mdx
│       └── 03-services.mdx
```

### 3. Frontmatter Standard

Every MDX file MUST have:

```yaml
---
title: "1.2.1 — ROS 2 Node Basics"
sidebar_label: "1.2.1 Node Basics"
sidebar_position: 1
description: "Learn the fundamentals of ROS 2 nodes and how to create them with Python"
module: 1
week: 3
section: 1
tags: [ros2, nodes, python, rclpy, beginner]
difficulty: beginner  # beginner | intermediate | advanced
estimated_time: "30 minutes"
---
```

### 4. Section Ordering

Every chapter follows this exact order:

```markdown
# [Number] — [Title]

> **Summary**: One-sentence description of what you'll learn.

## 🎯 Learning Objectives
- Objective 1
- Objective 2
- Objective 3

## 📋 Prerequisites
- [Link to required prior chapter]
- Required software/tools

## 📖 Content
### Topic 1
...
### Topic 2
...

## 💻 Hands-On Exercise
### Exercise 1: [Name]
**Difficulty**: ⭐ Beginner
...

## 🔑 Key Takeaways
- Takeaway 1
- Takeaway 2

## 📚 Further Reading
- [External resource 1]
- [External resource 2]

## ➡️ Next Steps
Continue to [Next Chapter Title](/path/to/next)
```

### 5. Sidebar Category Files

Each folder needs `_category_.json`:

```json
{
  "label": "Module 1: ROS 2 Fundamentals",
  "position": 1,
  "collapsible": true,
  "collapsed": false,
  "link": {
    "type": "doc",
    "id": "module-1/index"
  }
}
```

### 6. Cross-Reference Format

Always use consistent link format:

```markdown
✅ Correct:
See [1.2.1 — Node Basics](/docs/module-1/week-3-5/01-nodes) for details.

❌ Wrong:
See the nodes chapter for details.
See [here](/docs/module-1/week-3-5/01-nodes) for details.
```

### 7. Difficulty Indicators

Use consistent emoji markers:

| Level | Emoji | Badge |
|-------|-------|-------|
| Beginner | ⭐ | `difficulty: beginner` |
| Intermediate | ⭐⭐ | `difficulty: intermediate` |
| Advanced | ⭐⭐⭐ | `difficulty: advanced` |

## Examples

### Module Index Page

```mdx
---
title: "Module 1 — The Robotic Nervous System"
sidebar_label: "Module 1: ROS 2"
sidebar_position: 1
description: "Master ROS 2 middleware for robot control"
module: 1
tags: [ros2, middleware, robotics]
---

# Module 1 — The Robotic Nervous System (ROS 2)

> **Focus**: Middleware for robot control

## 🎯 Module Overview

In this module, you will learn...

## 📅 Weekly Schedule

| Week | Topics | Difficulty |
|------|--------|------------|
| 1-2 | [Intro to Physical AI](/docs/module-1/week-1-2/) | ⭐ |
| 3-5 | [ROS 2 Fundamentals](/docs/module-1/week-3-5/) | ⭐⭐ |

## 🏆 Module Outcomes

By completing this module, you will be able to:
- Create ROS 2 nodes using Python
- Implement publish-subscribe patterns
- Understand URDF for humanoid robots
```

## Validation Checklist

- [ ] All files have correct numbering in title
- [ ] `sidebar_position` matches intended order
- [ ] Frontmatter includes all required fields
- [ ] Cross-references use full chapter numbers
- [ ] Difficulty levels are marked
- [ ] `_category_.json` exists in each folder

## Definition of Done

- Every chapter follows the numbering convention (X.Y.Z)
- All frontmatter fields present and consistent
- Sidebar renders in correct order
- Cross-references use chapter numbers
- No orphan pages (all linked in sidebar)
