---
name: roblox-datastores
description: >
  Persist player data in Roblox with DataStoreService: GetDataStore, GetAsync/
  SetAsync/UpdateAsync/IncrementAsync wrapped in pcall, load-on-join and
  save-on-leave plus BindToClose, retries, and OrderedDataStore leaderboards. Use
  when saving or loading persistent data in a Roblox experience — when the user
  mentions DataStore, DataStoreService, GetAsync, SetAsync, UpdateAsync, save player
  data, or leaderboards. For general Luau scripting use roblox-luau.
---

# Roblox DataStores

Persist data across sessions in Roblox with `DataStoreService`: loading on join,
saving on leave and shutdown, safe updates, retries, and ordered stores for
leaderboards. Server-side only.

## When to use

- Use to save/load player progress (coins, inventory, levels), build persistent
  leaderboards, or fix data loss, overwrites, and throttling.
- Use when server code calls `DataStoreService`, `GetDataStore`, `GetAsync`,
  `SetAsync`, `UpdateAsync`, or `GetOrderedDataStore`.

**When *not* to use:** general scripting, services, remotes, the client/server
split → `roblox-luau`. High-frequency temporary state (matchmaking, per-round) →
memory stores (a different service). Engine-agnostic persistence theory →
`save-systems`.

## Core workflow

1. **Enable Studio access once.** File → Game Settings → Security → *Enable Studio
   Access to API Services* (use a test place; Studio hits live data). DataStores
   work only from server `Script`s, never `LocalScript`s.
2. **Get a store, then read/write by key.** `DataStoreService:GetDataStore("Name")`;
   key per player is usually `"Player_" .. player.UserId`.
3. **Wrap every call in `pcall`.** `GetAsync`/`SetAsync`/`UpdateAsync` are network
   calls that can fail; an unguarded failure errors the thread and risks data loss.
4. **Load on `PlayerAdded`, save on `PlayerRemoving`, and also `BindToClose`.** A
   leaving player and a shutting-down server both need a final save.
5. **Prefer `UpdateAsync` for read-modify-write** (multi-server safe) over `SetAsync`
   (blind overwrite). On a failed load, do **not** overwrite with defaults — abort
   the save so you don't wipe good data.
6. **Use `OrderedDataStore` for ranked data** (leaderboards) via `GetSortedAsync`.
   Test by joining, changing data, rejoining, and confirming it persisted.

## Patterns

### 1. Load on join (pcall-guarded)

```lua
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")
local store = DataStoreService:GetDataStore("PlayerData")

local DEFAULT = { Coins = 0, Level = 1 }

Players.PlayerAdded:Connect(function(player)
    local key = "Player_" .. player.UserId
    local ok, data = pcall(function()
        return store:GetAsync(key)
    end)

    if not ok then
        -- Load FAILED (network). Do not treat as a new player; flag so we never save
        -- over their real data with defaults.
        warn("Load failed for", player.Name, data)
        player:SetAttribute("DataLoaded", false)
        return
    end

    player:SetAttribute("DataLoaded", true)
    local profile = data or DEFAULT          -- nil == genuinely new player
    applyToLeaderstats(player, profile)
end)
```

### 2. Save with UpdateAsync (multi-server safe)

```lua
-- UpdateAsync reads the latest value, then writes what the callback returns.
-- The callback MUST NOT yield (no task.wait, no further Async calls inside it).
local function savePlayer(player)
    if player:GetAttribute("DataLoaded") == false then return end  -- never overwrite on a bad load
    local key = "Player_" .. player.UserId
    local newData = gatherDataFor(player)    -- a plain table of serializable values

    local ok, err = pcall(function()
        store:UpdateAsync(key, function(old)
            -- merge/decide here; return nil to cancel the write
            return newData
        end)
    end)
    if not ok then warn("Save failed for", player.Name, err) end
end
```

### 3. Save on leave AND on shutdown

```lua
Players.PlayerRemoving:Connect(savePlayer)

-- BindToClose runs when the server shuts down; save everyone still in.
-- It has a limited time budget, so save in parallel and yield until done.
game:BindToClose(function()
    local players = Players:GetPlayers()
    local remaining = #players
    if remaining == 0 then return end
    for _, player in players do
        task.spawn(function()
            savePlayer(player)
            remaining -= 1
        end)
    end
    while remaining > 0 do task.wait() end
end)
```

### 4. Retry with backoff (transient failures)

```lua
local function withRetry(fn, attempts)
    attempts = attempts or 3
    for i = 1, attempts do
        local ok, result = pcall(fn)
        if ok then return true, result end
        if i < attempts then task.wait(2 ^ i) end   -- 2s, 4s, ... backoff
    end
    return false
end

local ok, data = withRetry(function() return store:GetAsync(key) end)
```

### 5. Increment a counter

```lua
-- IncrementAsync is a convenience for integer read-modify-write (still wrap it).
local ok, newTotal = pcall(function()
    return store:IncrementAsync("Visits_" .. player.UserId, 1)
end)
```

### 6. Leaderboard with OrderedDataStore

```lua
local boards = DataStoreService:GetOrderedDataStore("Coins")

-- Write a player's score (call when it changes, not every frame).
pcall(function() boards:SetAsync("Player_" .. player.UserId, coins) end)

-- Read the top 10, descending.
local ok, pages = pcall(function()
    return boards:GetSortedAsync(false, 10)   -- ascending=false → highest first
end)
if ok then
    for rank, entry in ipairs(pages:GetCurrentPage()) do
        print(rank, entry.key, entry.value)   -- entry.value is the number
    end
end
```

## Pitfalls

- **Unhandled failure wipes progress** → always `pcall` Async calls; on a failed
  *load*, mark the session and refuse to *save* so defaults never overwrite real data.
- **`SetAsync` race between servers** → two servers writing the same key can clobber
  each other. Use `UpdateAsync` for read-modify-write so each write sees the latest.
- **Yielding inside the `UpdateAsync` callback** → the callback can't call
  `task.wait` or other Async functions; compute the new value beforehand and return it.
- **No `BindToClose` save** → players in the server at shutdown lose unsaved progress;
  add `game:BindToClose` and wait for saves to finish within its budget.
- **Throttling / "too many requests"** → respect per-key and per-minute limits; don't
  save on every value change. Batch and save on a timer / on leave. `GetAsync` is
  cached briefly, so immediate re-reads may be stale.
- **Storing non-serializable values** → only JSON-serializable data persists: numbers,
  strings, booleans, and tables with string/number keys. `Instance`s, `Vector3`,
  `CFrame`, and functions do not — serialize them to plain tables first.
- **Testing without API access** → DataStores silently can't be used in Studio until
  *Enable Studio Access to API Services* is on (and they don't work from a
  `LocalScript`).
- **`DataStoreKeyInfo` is nil for ordered stores** → `OrderedDataStore` doesn't
  support versioning/metadata; use a regular `DataStore` when you need those.

## References

- For session locking (preventing duplicate data across servers), versioning/
  metadata with `DataStoreSetOptions`, ordered-store pagination
  (`AdvanceToNextPageAsync`), the key error codes and request limits, and
  Right-to-be-Forgotten compliance, read `references/sessions-and-limits.md`.

## Related skills

- `roblox-luau` — services, instances, events, and the server/client model.
- `save-systems` — engine-agnostic serialization, slots, and migration.
