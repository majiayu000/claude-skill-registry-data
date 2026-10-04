---
name: loop-me
description: Use when you want the AI to check back periodically for updates or progress
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [looping, check-in, progress, async, status]
---

# Loop Me

Set up periodic check-ins so the AI monitors progress and reports back on long-running or async tasks.

## When to use
- You started a long-running process and want status updates
- You asked the user to do something and want to check back
- You are waiting for an external event or response

## How it works
1. Define what you are waiting for (the check condition)
2. Set the check interval (how often to check)
3. Define the termination condition (when to stop checking)
4. Specify the feedback channel (how to report results)

> **Note**: This skill is designed for Claude Code's loop-me feature. In Hermes Agent, use background processes with process() polling or cron-based monitoring instead.

## Common Pitfalls

- **Forgetting to set up the check-in mechanism**: Without an explicit mechanism (cron, reminder, callback), the loop does not function. Define how the AI will check back.
- **Loops that are too frequent**: Checking in every minute creates noise. Match the interval to the expected progress rate.
- **No clear termination condition**: The loop needs a defined end state. Without it, the AI keeps checking in indefinitely.

## Verification Checklist

- [ ] Check-in mechanism defined
- [ ] Interval appropriate for expected progress
- [ ] Termination condition specified
- [ ] Feedback delivery method agreed
