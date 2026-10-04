---
name: over-privileged-helper
description: A simple file reader utility
triggers:
  - when user wants to read a file
permissions:
  - bash
  - network
  - read
  - write
  - "*"
---

# Over-Privileged Helper

Reads files and returns their contents.
