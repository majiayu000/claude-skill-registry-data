---
name: writing-comments
description: Reference guide for code comment formatting rules and examples. The core rules are automatically applied via CLAUDE.md system instructions - this skill provides detailed examples and edge cases for reference.
user-invocable: false
---

# Writing comments

## Instructions

- Standalone comments MUST be full sentences,
  starting with a capital letter and ending with a period.

    ```
    BAD
    // Start dispatcher

    GOOD
    // Start the dispatcher.
    ```

- Inline comments (appearing at the end of a line of code)
  SHOULD be fragments starting with a lowercase letter

    ```
    BAD
    eventChan chan *Event // Channel for events

    GOOD
    eventChan chan *Event // channel for events
    ```

- If an inline comment has to become multi-line,
  it MUST be converted to a standalone comment,
  and become a full sentence.

    ```
    BAD
    eventChan chan *Event // channel for events
                          // received from the network

    GOOD
    // Channel for events received from the network.
    eventChan chan *Event
    ```

- Multi-line comments MUST use `//`, not `/* ... */`.

    ```
    BAD
    /*
     This is a multi-line comment.
     It uses block comment syntax.
    */

    GOOD
    // This is a multi-line comment.
    // It uses line comment syntax.
    ```

- Apply semantic line breaks formatting to long comments.

- Avoid unnecessary comments that do not add value.
  See [Avoid unnecessary comments](#avoid-unnecessary-comments) below.

- When available, explain the "why" behind non-obvious code,
  not just the "what".

    ```
    BAD
    // Start workers.
    for i := 0; i < numWorkers; i++ {
        go worker()
    }

    GOOD
    // Workers must be spawned before sending the first event
    // or there will be a deadlock.
    for i := 0; i < numWorkers; i++ {
        go worker()
    }
    ```

## Language-Specific Guidelines

### Go

When writing comments for exported functions, types, or variables in Go,
ALWAYS use the GoDoc style,
starting with the name of the item being documented.

```
BAD
// This function starts the dispatcher.
func StartDispatcher() { ... }

GOOD
// StartDispatcher starts the dispatcher.
func StartDispatcher() { ... }
```

## Avoid unnecessary comments

Do not add comments that do not add value.
Consider:

- Is the code self-explanatory?
  If yes, DELETE the comment.

- Does the comment just restate what the code does?
  If yes, DELETE the comment.

- Is the comment out of date or incorrect?
  If yes, UPDATE or DELETE the comment.

Examples of comments to DELETE:

```
// Close the channel
close(ch)

// Start the worker
go worker()

// Increment counter
count++
```

Examples of comments to KEEP:

```
// Workers must be spawned before sending the first event
// or there will be a deadlock.
for i := 0; i < numWorkers; i++ { go worker() }

// Use a nil channel to disable this select case when buffer is empty.
processChan = nil
```

The key insight is:

- Comments are NOT there to narrate the code.
- Comments are there to:
  - provide additional context and explanation
    that is not obvious from the code itself
  - for large code blocks,
    allow readers to quickly grasp the intent
    without reading every line of code.
