---
name: understand-networked-events
description: Figure out how events are being used in the project. You can't answer questions about them without this skill.
---

# Understand networked events

In Highrise Studio, networked events allow clients and servers to communicate with each other. It can be challenging for developers to understand how these events are used, especially when they are used in multiple scripts. This skill will help you understand how specific networked events flow between clients and servers so you can understand what they do.

## Instructions

Add the following steps to your todo list:
1. Ask the user for any additional information that is needed to solve the request.
2. Find and read any scripts that refer to the specified events.
    - Look especially for calls to `Connect()`, `Fire*()` (where `*` might be `Client`, `Server`, etc.), and `.Changed` (which returns the on-changed event for a networked value).
3. Check `.claude/events` in the project for an existing response for this scenario. If there is not one, create a new one by copying the [template](resources/SCENARIO.md).
4. Edit or fill out the scenario file with the information you found in step 2, and search for any other relevant information needed.
5. Read the contents of the scenario file and return the result to the user.
