---
name: antilua-testing
description: |
  The Antilua testing workflow: build C++, run C++ unit tests, run client
  integration tests, and lint Lua. Use after any code change.
---

# Antilua Testing Workflow

Run these after every C++ or Lua change to verify nothing is broken.

## Quick reference

| Change type | Build needed? | Test command |
|---|---|---|
| Lua-only (clientmods, builtin) | No | `./util/ci/run_al_tests.sh` |
| C++ only | Yes | Build → unit tests → integration tests |
| Both | Yes | Build → unit tests → integration tests |

## Build

```sh
cmake -B build -DCMAKE_BUILD_TYPE=Release -DRUN_IN_PLACE=TRUE -DBUILD_SERVER=OFF
cmake --build build -j$(nproc)
```

For debug builds:

```sh
cmake -B build -DCMAKE_BUILD_TYPE=Debug -DRUN_IN_PLACE=TRUE -DBUILD_SERVER=OFF
cmake --build build -j$(nproc)
```

- Building takes a long time (>30 minutes on the first run, incremental later).
- Use `-j3` on 4-core machines to keep one core free.
- Out-of-tree builds in `build/` only (in-tree artifacts break CMake).

## C++ unit tests

```sh
./bin/antilua --run-unittests
```

Requires `-DBUILD_UNITTESTS=TRUE` (the default). Reports PASS/FAIL across
~50 modules (~350 individual tests).

## Integration tests (Antilua client-side features)

```sh
./util/ci/run_al_tests.sh
```

Requires `xvfb-run` (from the `xvfb` package) for headless display. The test
mod lives at `clientmods/al_test/` and runs automatically on the devtest game.
Reports `[AL_TEST] PASS/FAIL/SKIP` and a summary line.

Tests that depend on `core.localplayer` (ClientObjectRef, inventory location)
are deferred until the player joins the world, so results appear in two batches.

## Lua lint

```sh
luacheck .
```

Configured by `.luacheckrc` in the repo root. Runs on all Lua files.

## Integration test for the Client Lua Pipe feature

```sh
./util/ci/test_pipe_lua.sh
```

Spawns the game headless with `pipe_lua_enable=true`, writes Lua expressions
to the FIFO, reads responses, and verifies results.

## Interactive testing via Lua Pipe

The Lua pipe lets you send Lua expressions to a running client and read
results — useful for quick smoke tests, inspecting state, or debugging
without restarting.

Enable the pipe in settings (`pipe_lua_enable = true`, path defaults to
`/tmp/antilua_lua`), then:

```sh
echo '{"code":"return core.localplayer:get_pos()", "file":"/tmp/resp"}' > /tmp/antilua_lua
cat /tmp/resp
# ok
# {x=100, y=20, z=-30}
```

Response format: first line is `ok` or `error`, followed by the result.
You can also fire commands (detach, reattach, switch worlds) through the pipe
to test session management in a headless/server context.

## Raw Packet API

Antilua provides client-side Lua APIs for intercepting and sending network
packets. These are exercised by the integration tests at
`clientmods/al_test/test_raw_packet.lua`.

### Sending packets

```lua
core.send_raw_packet(command, payload)
```

- `command`: a number (opcode), a string like `"TOSERVER_INTERACT"`, or a
  constant such as `core.TOSERVER.INTERACT`.
- `payload`: a raw byte string (can contain nulls).
- Blacklisted opcodes: `TOSERVER_INIT`, `TOSERVER_INIT2`, `TOSERVER_FIRST_SRP`,
  `TOSERVER_SRP_BYTES_A`, `TOSERVER_SRP_BYTES_M` — these raise a Lua error.

### Intercepting incoming packets (from server)

```lua
core.register_on_receiving_raw_packet(function(command_id, payload)
    -- return nil/false → let through
    -- return true → silently drop
    -- return "new_payload" → replace payload
end)
```

### Intercepting outgoing packets (to server)

```lua
core.register_on_sending_raw_packet(function(command_id, payload)
    -- same return conventions
end)
```

### Opcode constant tables

| Table | Contents |
|-------|----------|
| `core.TOCLIENT` | `HELLO=0x02`, `HUDCHANGE=0x4B`, `CHAT_MESSAGE=0x2F`, `INVENTORY=0x27` |
| `core.TOSERVER` | `INTERACT=0x39`, `CHAT_MESSAGE=0x32`, `PLAYERPOS=0x23`, `INVENTORY_ACTION=0x31` |

Populated at engine startup from the C++ opcode tables.

## Reference: AGENTS.md

The full API reference for all client-side modding features (Sky API, Clouds
API, Minimap Markers, Camera Nametags, Schematic API, LocalPlayer extras,
Sound API, Camera Roll, Item Override, and more) lives in `AGENTS.md` at
the repo root. The integration test mod at `clientmods/al_test/` exercises
every API and is the canonical source of truth for expected behavior.

## Interactive testing

```sh
./util/start_test.sh
```

Opens the test world with `--go` on workspace 11 (requires i3 and xprintidle).
If idle >10 min, runs headless and reports results instead.
