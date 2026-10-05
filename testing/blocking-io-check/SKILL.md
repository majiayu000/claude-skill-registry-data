---
name: ha:blocking-io-check
description: "Detect blocking I/O on the event loop specifically — sync library calls inside async def, imports and file-exists checks as hidden I/O, and unbatched executor jobs. Use when blocking I/O is suspected, NOT for unrelated asyncio questions or wider performance work."
effort: medium
allowed-tools: Read, Grep, Glob, Bash
---

# Blocking-I/O Detection

Identify and fix blocking-I/O anti-patterns in Home Assistant async code.

> Orientation: this is the event-loop analogue of hunting an N+1 query — instead of a query
> per row, the smell is a *blocking call per iteration* (or a hidden sync call) stalling the
> single event loop that runs all of Home Assistant. Companion review agent: `blocking-io-auditor`.

## Iron Laws - Never Violate These

1. **Never call blocking I/O in an async context** (P4) — sync library calls, `open()`,
   `requests.*`, `time.sleep`, `urllib`, `json.load` on a file, `os.path.exists`/`Path.exists`
   inside an `async def` block the whole loop. "don't do blocking I/O in the event loop, even
   in tests" — MartinHjelmare, https://github.com/home-assistant/core/pull/154625#discussion_r2619211602
2. **Do blocking work in the executor, batched into one job** (P4) — wrap sync work in
   `hass.async_add_executor_job`; combine several sync calls into a single job rather than
   scheduling many. Never run executor jobs concurrently as a substitute for an async library.
3. **Imports and file-exists are I/O — move them** (P4) — module imports inside a function and
   filesystem probes cause I/O; import at module top-level or defer to the executor. "we
   should not do imports here as that causes IO" — joostlek,
   https://github.com/home-assistant/core/pull/174058#discussion_r3438274629
4. **A function that never awaits must not be a coroutine** (PS19) — decorate it `@callback`
   instead of `async def`; and don't hop async→sync→async. "Why is this a coroutine function
   if we don't await inside?" — MartinHjelmare,
   https://github.com/home-assistant/core/pull/153268#discussion_r2468783062

## Detection Patterns

### Pattern 1: Loop with a blocking call

```python
# BAD: one blocking sync call per iteration stalls the loop N times
async def async_update(self) -> None:
    for device in self.devices:
        device.state = self.client.read_sync(device.id)  # sync call in async def!

# GOOD: one executor job for the whole batch (P4)
async def async_update(self) -> None:
    states = await self.hass.async_add_executor_job(self._read_all)

def _read_all(self) -> dict[str, State]:
    return {d.id: self.client.read_sync(d.id) for d in self.devices}
```

### Pattern 2: Blocking call directly in `async def`

```python
# BAD: sync file / HTTP / sleep on the event loop
async def async_setup_entry(hass, entry):
    config = json.loads(open(path).read())      # open() + read() block
    resp = requests.get(url)                     # requests blocks
    time.sleep(2)                                # sleep blocks the WHOLE loop

# GOOD: executor for sync file work, async library for HTTP, async sleep
async def async_setup_entry(hass, entry):
    config = await hass.async_add_executor_job(_load_config, path)
    session = async_get_clientsession(hass)
    resp = await session.get(url)
    await asyncio.sleep(2)
```

### Pattern 3: Hidden I/O — imports and filesystem probes

```python
# BAD: import inside the function (I/O on first call) + a filesystem probe on the loop
async def async_get_device(hass):
    import heavy_library                          # import is I/O (joostlek)
    if os.path.exists(cache_path):               # Path.exists() / os.path.exists() is I/O
        ...

# GOOD: import at module top-level; probe the filesystem in the executor
import heavy_library  # top of file

async def async_get_device(hass):
    exists = await hass.async_add_executor_job(cache_path.exists)
    ...
```

## Quick Detection Commands

Use Grep to find known blocking calls inside async code (P4 mechanical check list):

Search integration files for `open(`, `requests.`, `time.sleep`, `urllib`, `json.load`,
`import_module`, `os.path.exists`, `.exists()`, and `socket.` — then read each hit to confirm
it sits inside an `async def` body (or a `@callback`) rather than an executor target.

Use Grep to find `async def` functions and scan their bodies for any `await` — a coroutine
with no `await` should be a `@callback` (PS19).

Use Grep to find `async_add_executor_job` calls inside loops (`for`, `while`,
comprehensions) — several jobs that should be batched into one (P4).

Ruff's `ASYNC` rule family (`flake8-async`) flags many of these mechanically; the HA runtime
also ships a blocking-call detector that raises at runtime when a known blocking call executes
on the loop.

## Analysis Command

For a coordinator or setup module, run:

Use Grep to list every call in the async update / setup path, then verify each one is either
awaited (async library), wrapped in a single `hass.async_add_executor_job`, or a pure
non-I/O computation. Any bare sync I/O call, in-function import, or filesystem probe on the
loop is a P4 violation.

Then confirm sync work is batched — one executor job per logical fetch, not one per device.

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/executor-patterns.md` - Executor batching and offloading
  techniques (one job over many, avoiding concurrent executor jobs, streaming large sync reads)
- `${CLAUDE_SKILL_DIR}/references/async-io-patterns.md` - Async-library and `@callback` patterns:
  wrapping sync libraries, scheduling from the loop, dispatcher/subscription setup, anti-patterns
