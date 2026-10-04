---
name: superpowers-sage:ai-setup
description: >
  Guided installation of the Roots AI stack (roots/acorn-ai + wordpress/mcp-adapter) in a
  Sage/Bedrock project via Lando. Runs detect-ai-readiness probe, identifies gaps, installs
  missing packages, publishes Acorn AI config, writes API key to .env, generates .mcp.json,
  validates MCP handshake via discover-abilities. Invoke for: ai-setup, install acorn ai,
  mcp adapter, install mcp, setup mcp, ai stack, discover-abilities not working,
  wordpress mcp, acorn-ai setup.
user-invocable: true
---

# /ai-setup — Guided AI Stack Installation

This skill installs and validates the Roots AI stack in your Sage/Bedrock project.

## What it installs

| Package | Purpose |
|---|---|
| `roots/acorn-ai` | Laravel AI SDK bridge for Acorn |
| `wordpress/mcp-adapter` | Exposes WP site via Model Context Protocol (stdio) |

**Prerequisite:** WordPress ≥ 6.9, Lando running.

## Step 1 — Run readiness probe

```bash
node <plugin-scripts-path>/detect-ai-readiness.mjs --path .
```

Read the `missing` array. Proceed through only the steps that apply.

## Step 2 — Install packages (if `missing` includes `acorn-ai` or `mcp-adapter`)

The two packages belong to different layers — install them separately:

```bash
# Laravel AI bridge — goes into the theme
lando theme-composer require roots/acorn-ai

# WordPress MCP plugin — goes into the Bedrock root (installer-paths)
lando composer require wordpress/mcp-adapter

lando wp acorn vendor:publish --tag=acorn-ai
```

`wordpress/mcp-adapter` is a `wordpress-plugin` type package. If installed via the theme Composer it
lands in `theme/vendor/` with no WordPress activation — always use root `composer`.

See [`references/install-steps.md`](references/install-steps.md) for full install details, version conflict resolution, and the Bedrock autoloader stub fix.

## Step 3 — Add API key (if `missing` includes `api-key`)

Ask the user which provider they want to use:
- Anthropic → `ANTHROPIC_API_KEY`
- OpenAI → `OPENAI_API_KEY`

**Do not write the key yourself.** Show the exact line to add to `.env`:

```
ANTHROPIC_API_KEY=<paste-your-key-here>
```

**Warn:** Confirm `.env` is in `.gitignore` before proceeding: `grep .env .gitignore`

## Step 4 — Generate `.mcp.json`

```bash
node <plugin-scripts-path>/generate-project-mcp.mjs --path .
```

This merges the `mcpServers.wordpress` entry non-destructively into the project's `.mcp.json`.

## Step 5 — Validate handshake

```bash
lando wp mcp-adapter list
```

Expected: at least one server listed (e.g. `mcp-adapter-default-server`).

If the command returns "not a registered wp command" with the plugin showing as active, see
[Bedrock + installer-paths stub fix](references/install-steps.md#bedrock--installer-paths-autoloader-silently-broken).

Then in Claude Code, confirm MCP is working:

```
discover-abilities
```

Expected: a list of available WordPress Abilities.

## If something fails

See [`references/rollback.md`](references/rollback.md) for per-step rollback commands.

## Verification

```bash
node <plugin-scripts-path>/detect-ai-readiness.mjs --path .
```

Expected: `"ready": true` with all fields populated.

## Failure modes

### Problem: Composer version conflicts

- **Cause:** `roots/acorn-ai` or `wordpress/mcp-adapter` require a version of Acorn or WordPress that your project doesn't have.
- **Fix:** See [`references/install-steps.md`](references/install-steps.md) for version resolution steps. Usually requires updating Acorn or WordPress first.

### Problem: `wp mcp-adapter list` returns "not a registered wp command" (Bedrock)

- **Cause:** `wordpress/mcp-adapter` looks for `vendor/autoload.php` inside its own plugin directory.
  In Bedrock with `installer-paths` the autoloading lives in the root `vendor/` — the plugin-local
  path never exists, so the plugin silently skips registering all hooks.
- **Fix:** See [`references/install-steps.md`](references/install-steps.md) for the stub solution.

### Problem: MCP server not appearing in `discover-abilities`

- **Cause:** `.mcp.json` was not generated, or the `generate-project-mcp.mjs` script failed.
- **Fix:** Re-run `node <plugin-scripts-path>/generate-project-mcp.mjs --path .` and verify the file exists and contains `"mcpServers": { "wordpress": ... }`.

### Problem: `.env` changes not taking effect

- **Cause:** Lando container cache, or `.env` not sourced by Bedrock.
- **Fix:** Run `lando restart` to refresh containers. Verify `.env` is in the project root and readable.

For complete rollback instructions, see [`references/rollback.md`](references/rollback.md).
