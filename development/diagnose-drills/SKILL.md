---
name: diagnose-drills
description: Diagnose drill problems - fuel shortages, blocked outputs, depleted resources. Use when drills aren't working or showing 0/X working status.
allowed-tools: Bash, Read, Write
---

# Diagnose and Fix Drills

Use this skill when drills are not working properly.

## Quick Diagnostic

Run the diagnostic script:
```bash
pnpm --prefix /Users/golergka/Projects/factorio-agent eval:file /Users/golergka/Projects/factorio-agent/agent-workspace/lua/diagnose-and-fix-drills.lua
```

## What the Diagnostic Checks

- **status=1**: Working normally
- **status=21**: Waiting for target (not on resource)
- **status=34**: No minable resources OR output full
- **status=53**: No fuel - needs coal!
- **status=54**: No power (shouldn't happen with burner drills)

## Common Fixes

1. **No fuel (status 53)**: Walk to drill and add coal using safe_insert
2. **Output full (status 34)**: Clear output inventory with safe_take
3. **No resources**: Drill is depleted, needs to be moved

## Manual Fix Example

```lua
dofile("/Users/golergka/Projects/factorio-agent/agent-workspace/lua/safe-interact.lua")

local drill, msg = find_nearest("burner-mining-drill", 100)
rcon.print(msg)

if drill then
    local result, err = safe_insert(drill, {name="coal", count=10})
    if result then
        rcon.print("Added fuel!")
    else
        rcon.print("Need to walk closer: " .. err)
    end
end
```

Remember: If distance check fails, you must WALK to the drill first!
