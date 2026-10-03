---
name: setup-dstack
description: "Configure DStack for Claude Code or Codex, verify the Roblox skill surface and guarded reviewer lanes, and optionally add a bounded startup instruction. Use only for explicit setup, installation checks, client changes, or reviewer configuration; do not use for ordinary Roblox implementation work."
---

# Setup DStack

This is an explicit setup and diagnostics workflow. It configures the agent client, not the user's game. Do not edit Roblox source, project design documents, or repository instructions unless the user separately asks for that work.

Read [`../../references/roblox-engineering.md`](../../references/roblox-engineering.md), [`../../references/roblox-mcp-setup.md`](../../references/roblox-mcp-setup.md), and [`../../models.json`](../../models.json) before changing setup or promising a reviewer lane.

## 1. Identify the parent client

Use the active tool surface to identify Claude Code or Codex. Never ask a child to guess the parent. Keep the two install surfaces separate:

- Claude Code loads `.claude-plugin/plugin.json`, exposes skills as `/dstack:<skill>`, and refreshes an installed plugin with `/reload-plugins`.
- Codex loads `.codex-plugin/plugin.json`, exposes the same skill folders by name, and needs a new task after an install or update so its skill catalog is rebuilt.

Do not reference a versioned cache path. If the plugin is not visible under the `dstack` namespace, stop and give the client-specific install command from the repository README rather than pretending setup succeeded.

## 2. Verify the skill surface

Check the installed plugin's manifest and canonical `skills/` tree. Confirm:

1. `david-mode` is explicit and is the entry point for non-trivial Roblox work.
2. `unslop` is the only implicitly invoked skill.
3. Other skills remain explicit in the catalog. David Mode may route eligible routine batches under its runtime contract; setup does not enable blanket delegation or review.
4. The Claude and Codex manifests point at the same skills and their respective hook files. No bundled worker profile may bypass the shared model policy.

If the installed tree has duplicate copies, use the client's normal uninstall/update flow and reinstall one marketplace entry. Do not edit a cache directory by hand.

## 3. Offer optional startup routing

Do not write global instructions by default. Ask whether the user wants DStack routing added to the parent client's user instructions. If they decline, rely on explicit skill invocation and the plugin hook.

If they approve, snapshot the target file before editing and preserve all unrelated bytes. Add or replace exactly one bounded block:

Claude Code target: `~/.claude/CLAUDE.md`

```text
<!-- dstack:startup:begin -->
For non-trivial Roblox work, use `/dstack:david-mode`. For a narrow request, use the smallest explicit `/dstack:<skill>` instead. Never use Roblox Studio MCP playtest controls; the user playtests.
<!-- dstack:startup:end -->
```

Codex target: `~/.codex/AGENTS.md`

```text
<!-- dstack:startup:begin -->
For non-trivial Roblox work, use `$david-mode`. For a narrow request, use the smallest explicit `$<skill>` instead. Never use Roblox Studio MCP playtest controls; the user playtests.
<!-- dstack:startup:end -->
```

If the markers are duplicated, reversed, or only one marker exists, stop and report inconsistent state instead of guessing a replacement range. User and repository instructions remain higher authority than this optional block.

## 4. Check Roblox Studio MCP without playtesting

Use the connection check only when the active client exposes the Roblox Studio MCP. Distinguish these states:

- configured and connected: use it for necessary non-playtest context;
- configured but closed or disconnected: tell the user once and continue from repository evidence when possible;
- missing or unconfigured: stop and ask whether the user wants setup, following [`roblox-mcp-setup.md`](../../references/roblox-mcp-setup.md). If they say yes, use the official Roblox guide for their client, preserve other servers, and end the turn so they can restart the agent client. If they say no, continue with one concise notice that MCP gives DStack its fullest Roblox context and accuracy.

Never infer that MCP is uninstalled merely because no Studio is connected. Never install a guessed command or overwrite a client configuration. **Do not launch, start, stop, simulate, or control a Roblox Studio playtest.**

## 5. Validate parent and worker routing

Read [`../david-mode/references/agent-runtime.md`](../david-mode/references/agent-runtime.md) before checking delegation. `models.json` is instruction metadata, not executable client configuration or proof of model availability. For an ordinary setup check, inspect advertised capabilities without spending model calls. Probe a worker only when the user explicitly asks to verify worker execution.

Confirm that the user's chosen parent retains planning, difficult implementation, review, and integration. Check the active client's worker policy: Codex requests Luna with `reasoningEffort: max`; Claude Code routes narrow work to native `haiku` and complex work to native `sonnet` with `effort: high`. Claude parents are normally Opus or another user-selected high-capability route such as Fable when the client exposes it. Missing worker controls mean sequential parent execution, including when a native worker tier cannot use its policy. Do not install an unrequested model bridge or change global model settings.

Validate the policy's concurrency, revision, and leaf-worker limits. For an Interrogate panel, read [its panel contract](../interrogate/references/interrogate-panel.md) and use `riskPolicy`; independent contexts share one selected worker tier and do not provide model diversity. Record requested settings separately from observed execution. `interrogate` never auto-applies findings.

## 6. Smoke and report

Run a structural smoke check appropriate to the client. Confirm the plugin namespace, the setup skill, the David Mode skill, the automatic `unslop` rule, the parent/worker policy, and the non-playtest boundary. Do not claim runtime success from a file listing alone.

Report:

- parent client and installed plugin source/version;
- whether the optional startup block was written, unchanged, or declined;
- MCP state and any required restart;
- reviewer lanes attempted, served identity as observed or unverified, and skipped lanes;
- checks run and any remaining user-owned Studio playtesting.
