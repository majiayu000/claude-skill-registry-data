---
name: qyrus-setup
description: Set up or update QyrusAI Assure end to end, including missing Python, uv, Qyrion, and qyrusai dependencies and one private env-file path for MCP and web/mobile sessions. Use for plain setup/onboarding requests, accepted CLI updates, missing or obsolete tools, shared X-API-Key, application URL or team selection, key rotation, and MCP connection/authentication failures.
---

# Configure Qyrus once

<!-- Distilled from: README.md, plugin.json, .claude-plugin/marketplace.json, shared/prerequisites.md, shared/credentials.md, shared/update-checks.md, shared/local-state.md, scripts/qyrus_env.py, scripts/qyrus_mcp.py, scripts/qyrus_antigravity.py, scripts/qyrus_updates.py, apps/qyrion/src/qyrion/client/auth.py. -->

“Set up QyrusAI Assure” is sufficient: own dependency preparation, shared
credentials, connection checks, and continuation of the user's task. In Claude
Code, first follow `references/claude-installation.md` for registration,
symlink handling, existing installations, and activation status. In Antigravity,
follow `references/antigravity-installation.md` for native plugin placement and
the credential-free MCP registration helper; preserve other connectors. Read
`references/prerequisites.md` for detection and installation; perform missing
user-local installs within the setup request instead of handing back a checklist.
For a missing Qyrion CLI, use the newest published public release, including
betas; setup downloads only the platform binary without checksum-file checks.
Use `references/credentials.md` for the bundled configure helper and path
precedence. Reuse a supplied/saved/default private file; ask for a new file/path
only when missing, never its contents. The helper installs the pinned SDK and
writes the derived MCP URL. Do not open secrets in model-visible tools.

For an existing installation, follow `references/update-checks.md`: check at
most once every four hours during plugin use, stay quiet when unchanged, and
install an available update only when the user accepts or explicitly requests
it. Keep source/editable/pinned installations and explicit overrides intact.
After an accepted install, verify the running version and capabilities before
recording completion. A plugin refresh and a CLI binary update are separate.
See `references/local-state.md` for private result records and host-memory
pointers. Do not read all references or repeat setup during every task.

After local setup, check only the surfaces needed for the current request:

| Surface | Read-only verification |
|---|---|
| Qyrus Aegis MCP | Reconnect and confirm the host lists six tools (the three core tools plus `qyrus_tools`, `qyrus_tool_schema`, `qyrus_tool_call`; every tool when the file sets `QYRUS_MCP_TOOLS=all`), call `qyrus_guide_get`, then `qyrus_teams_get_by_api_key` with `{}` |
| Qyrion | Helper-wrapped `capabilities --json`; select the MCP-discovered team per `references/credentials.md`, then verify with `sessions list --json` |
| qyrusai | Setup prepares the pinned package; the helper's `sdk` action ensures it remains installed before each SDK script |

Do not run paid sessions, create tests, or submit generation requests merely
to check installation. Continue the user's original task after setup succeeds.
Installing the plugin makes this setup workflow available; dependency
installation is performed when setup or a dependent task invokes it. Connecting
a separate work-management account still requires that connector's flow.
Keep guide-first MCP team discovery for plugin setup. Updated Qyrion
`auth teams` uses TestHub; older binaries call usermgmt directly and can
reject a key that works for MCP. Preserve returned team UUIDs; never select
an org ID.

Report registration, dependency/connection checks, and host activation
separately. When setup checks have succeeded and only a reload/new session
remains, give that single next step; do not ask the user to say "set up" again.
Preserve a working editable Qyrion installation; a source version different
from the public CLI release is not by itself a failed capability check.
