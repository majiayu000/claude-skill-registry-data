---
name: node-config-state
description: Config layering and durable state for a Node Web Only server - defaults deep-merged with config.json, the ephemeral session secret, and atomic state.json writes. Use when loading config, adding a config key, deciding what may be persisted, or writing a state file. Triggers on config.json, config.example.json, deepMerge, loadConfig, state.json, randomBytes session secrets, mode 0600, and write-then-rename.
user-invocable: false
---

# Node Config and State

**Built-in defaults are the source of truth, a user's `config.json` is merged over them, and only durable facts are ever written back to disk.**

## Config

Resolution runs in three layers, lowest first:

1. A built-in default object, which defines both the shape and the fallback for every key.
2. A user `config.json` deep-merged over the defaults, its path passed with `--config`.
3. Environment variables and flags overriding individual values on top.

Defaults sit lowest so an omitted key still has a value, which is what lets a user's config file name only what they want to change.

The file ships as `config.example.json` rather than as `config.json`, so a user copying it never has their edits overwritten by an update, and a missing file falls back to defaults instead of erroring.

```js
import { readFile } from 'node:fs/promises';

const DEFAULTS = {
  host: '127.0.0.1',
  port: 8080,
  usersFile: 'users.json',
  stateFile: 'state.json',
  auth: { enabled: false },
};

const isObj = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);

function deepMerge(base, override) {
  const out = structuredClone(base);
  for (const [key, value] of Object.entries(override)) {
    out[key] = isObj(value) && isObj(out[key]) ? deepMerge(out[key], value) : value;
  }
  return out;
}

export async function loadConfig(path) {
  let user = {};
  if (path) {
    try {
      user = JSON.parse(await readFile(path, 'utf8'));
    } catch (err) {
      if (err.code !== 'ENOENT') throw err;
    }
  }
  const merged = deepMerge(DEFAULTS, user);
  if (process.env.PORT) merged.port = Number(process.env.PORT);
  return merged;
}
```

Only `ENOENT` is swallowed. A malformed JSON file or a permissions error propagates, because starting on the defaults after silently ignoring the config a user wrote is worse than refusing to start.

Config is loaded once at boot and the resulting object is passed into `start`. Nothing re-reads the file or reaches for `process.env` further down, so a function's behavior is a function of its arguments.

## Secrets Are Not Config

The session secret is regenerated on every boot with `randomBytes` and held in memory only. It never appears in the config file, in `state.json`, or in any other artifact.

A restart therefore invalidates every outstanding session. That is the intended trade-off for a single-process app with no session store: the alternative is a secret on disk that outlives the process and has to be rotated by hand.

```js
import { randomBytes } from 'node:crypto';

export function newSessionSecret() {
  return randomBytes(32);
}
```

Derived runtime values follow the same rule. Anything the process can recompute at boot is recomputed rather than persisted, since a stale cached value is harder to notice than a missing one.

## Durable State

`state.json` holds the only server-written durable state: small, non-secret facts such as a mode flag or a counter.

It is created at mode `0600`, matching every other file these projects write into a user's directory, because it sits next to the app's data and often reflects that environment.

Writes go to a temporary file and then `rename` over the target. `rename` is atomic on POSIX, so a crash mid-write leaves either the complete old file or the complete new one, never a truncated JSON document that fails to parse on the next boot.

```js
import { readFile, writeFile, rename } from 'node:fs/promises';

export async function readState(path, fallback) {
    try {
        return JSON.parse(await readFile(path, 'utf8'));
    } catch (err) {
        if (err.code === 'ENOENT') return fallback;
        throw err;
    }
}

export async function writeState(path, state) {
    const tmp = `${path}.${process.pid}.tmp`;
    await writeFile(tmp, JSON.stringify(state, null, 2), { mode: 0o600 });
    await rename(tmp, path);
}
```

The temporary name carries the process ID so two instances writing at once cannot corrupt each other's intermediate file.

`readState` takes an explicit fallback rather than returning `undefined`, which keeps the first-run case out of every caller.

## What Goes Where

| Value | Where it lives |
|---|---|
| Port, host, file paths, feature flags | `DEFAULTS`, overridable by `config.json` and env |
| Session secret | memory only, regenerated each boot |
| A mode flag the operator toggled at run time | `state.json` at `0600` |
| Credentials | `users.json`, read on each login, never written by the server |
| Anything recomputable at boot | nowhere, recompute it |
