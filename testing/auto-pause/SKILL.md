---
name: auto-pause
description: Behavior guide for when the auto-pause hook fires or when starting a long-running operation that needs a timeout exception.
---

# Auto-Pause

## When the Hook Fires

The PreToolUse hook will block your next tool call if you've been running for more than 5 minutes since the last user message. When it fires, you'll see a block message. Do this:

1. **Stop immediately** — don't try to work around the block.
2. **Summarize what you've done** since the last user message: what you tried, what worked, what didn't, where you are now.
3. **State clearly what you were about to do next** so the user can say "continue" or redirect.
4. **Wait for user input.**

Example check-in format:
> Auto-paused after ~N minutes. Here's where things stand:
> - Done: [what completed]
> - Current state: [what's true now]
> - Was about to: [next action]
>
> Continue, or should I adjust course?

## Before Starting a Long-Running Operation

If you're about to start something that legitimately takes more than 5 minutes (Playwright test suite, Docker build, Maven package, long-running migration verification), **set an exception before starting**:

```bash
# Grant a 15-minute exception window (adjust as needed)
echo "$(date -u -v+15M +%s)" > /tmp/claude-aligned-long-running-exception.txt
```

Then start the operation. When it completes (success or failure), **clear the exception**:

```bash
rm -f /tmp/claude-aligned-long-running-exception.txt
```

Set the exception duration to match your actual expected runtime — don't just set 60 minutes as a default. If the operation finishes early, clear the file early.

## What Counts as a Long-Running Operation

Set an exception for:
- Playwright / Cypress test runs with `--timeout` flags
- `mvn package`, `mvn verify`, `mvn spring-boot:run` startup wait
- `docker compose build` or multi-service `up`
- Any `Bash` command where you've passed an explicit timeout > 5 minutes to the tool

Don't set an exception just to avoid being paused — the pause exists to catch runaway loops, not legitimate long operations.
