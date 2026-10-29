---
name: mcporter-skillifier
description: Generate Codex skills that call MCP servers through MCPorter, including stdio or HTTP connections and keep-alive support for multi-turn `continuation_id` flows.
---

# Mcporter Skillifier

Use this skill to generate a Codex skill that calls an MCP server through the `mcporter` CLI. The generated skill contains a shell wrapper and a skill-local `mcporter.json`; it does not register MCP tools with Codex. The wrapper invokes `bash scripts/mcp` through `exec_command`.

The wrapper uses `npx -y mcporter@${MCPORTER_VERSION}` by default, with the generated script pin as its default version. Set `MCPORTER_BIN=mcporter` to use a local binary instead. MCPorter provides the keep-alive daemon used by servers that retain state between calls.

## Generate the skill

Run `scripts/generate_skill.py` from this skill's directory. Choose exactly one connection method: `--stdio` for a local process or `--http-url` for an HTTP MCP endpoint.

For a stdio server that keeps an in-memory continuation, enable `--keep-alive`:

```bash
python3 scripts/generate_skill.py \
  --skill-name my-mcp-skill \
  --stdio 'uvx --from ${PAL_MCP_FROM} pal-mcp-server' \
  --keep-alive \
  --with-fixture-tests
```

The generator normalizes the skill and server names to hyphen-case. By default it writes beside this skill's directory; set `--out-dir` to choose another parent directory. The output directory name is the normalized skill name. Use `--force` only when you intend to replace an existing output directory.

Set server environment values with repeatable `--env KEY=VALUE` arguments. Optional `--server-name` and `--server-description` configure the entry in `mcporter.json`. For keep-alive servers, `--idle-timeout-ms` sets the daemon idle timeout.

`--with-fixture-tests` adds a deterministic fixture MCP server and offline tests for multi-turn behavior. Generation does not run the generated self-test unless `--verify` is supplied. Verification requires `npx` and may require authentication or network access; `--no-verify` explicitly keeps generation offline.

MCPorter interpolates `${VAR}` in configuration commands, but does not support Bash defaults such as `${VAR:-fallback}`. Set variables before running the generated skill when a value needs a default. Avoid `${local_var}` in shell snippets embedded in `mcporter.json`; MCPorter may treat it as a required configuration placeholder.

## Call the generated skill

From the generated skill directory, list the configured server's tools and call one:

```bash
bash scripts/mcp list
bash scripts/mcp call <tool> --output json --args '{"key":"value"}'
```

The wrapper also accepts fully qualified `server.tool` selectors and HTTP URLs after `call`. It uses the skill's `mcporter.json` by default; set `MCP_SKILL_CONFIG` to use another config file. With no command or a help argument, `scripts/mcp` prints its usage and the MCPorter selection options.

For in-memory `continuation_id` flows, generate with `--keep-alive` so separate wrapper invocations reuse the server process. The fixture tests exercise this behavior without API keys:

```bash
python3 -m unittest -q tests/test_offline.py
```

The `codex-skill-scoped-mcp` experiment also contains integration checks for continuity across CLI invocations, isolation between skill configs, parallel calls, and parallel invocations:

- `experiments/codex-skill-scoped-mcp/scripts/test_mcporter_skillifier_fixture_multiturn.sh`
- `experiments/codex-skill-scoped-mcp/scripts/test_mcporter_skillifier_parallel_calls_same_daemon.sh`
- `experiments/codex-skill-scoped-mcp/scripts/test_mcporter_skillifier_parallel_invocations_isolated_daemons.sh`
