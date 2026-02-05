---
name: refuel-drills
description: Refuel all burner drills with coal. Use when drills are showing no fuel status or low working count.
allowed-tools: Bash, Read, Write
---

# Refuel All Drills

Use this skill when drills need coal. You must walk to each drill to refuel it!

## Check Which Drills Need Fuel

```bash
pnpm --prefix /Users/golergka/Projects/factorio-agent eval:file /Users/golergka/Projects/factorio-agent/agent-workspace/lua/diagnose-and-fix-drills.lua
```

## Refuel Strategy

**IMPORTANT**: You must be within reach distance (~6 tiles) to insert fuel!

1. Find drills needing fuel
2. Walk to nearest one
3. Insert coal
4. Repeat for each drill

## Example Script

Create and run `lua/refuel-one-drill.lua`:

```lua
dofile("/Users/golergka/Projects/factorio-agent/agent-workspace/lua/safe-interact.lua")

-- Find drills without fuel
local drills = surface.find_entities_filtered{force=force, name='burner-mining-drill'}
local needs_fuel = {}

for _, drill in ipairs(drills) do
    if drill.status == 53 then  -- no fuel status
        table.insert(needs_fuel, drill)
    end
end

if #needs_fuel == 0 then
    rcon.print("All drills have fuel!")
    return
end

-- Find nearest one that needs fuel
local px, py = player.position.x, player.position.y
table.sort(needs_fuel, function(a, b)
    local da = (a.position.x - px)^2 + (a.position.y - py)^2
    local db = (b.position.x - px)^2 + (b.position.y - py)^2
    return da < db
end)

local target = needs_fuel[1]
local dist = math.sqrt((target.position.x - px)^2 + (target.position.y - py)^2)

rcon.print(string.format("%d drills need fuel. Nearest at (%.0f, %.0f), distance: %.1f",
    #needs_fuel, target.position.x, target.position.y, dist))

-- Try to refuel if in range
local result, err = safe_insert(target, {name="coal", count=20})
if result then
    rcon.print("Added " .. result .. " coal to drill!")
else
    rcon.print("Walk to drill first: " .. err)
end
```

## After Refueling

Run factory-status to verify drills are working again.
