---
name: sflow-mcp
description: Configure, diagnose, and record governed Figma or Playwright MCP use without exposing credentials.
disable-model-invocation: true
argument-hint: "status | doctor | probe <server> --network | warm <server> --network | verify-offline <server> | auth status|import|remove playwright | attest <server> | smoke playwright --url <url> | scaffold figma|playwright | record <server> --tool <tool> | design-sources status"
---

# Govern MCP tools

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

- Inspect with `singularity-flow mcp status`; diagnose offline with `singularity-flow mcp doctor`.
- With network consent run `singularity-flow mcp probe <SERVER> --network`.
- Acquire and verify Playwright with `singularity-flow mcp warm playwright --network`; renew its npm-offline local-start proof with `singularity-flow mcp verify-offline playwright`. This does not sandbox the server's own network access.
- Preview private Playwright login state with `singularity-flow mcp auth import playwright --storage-state <FILE> --profile <LOWER-KEBAB>`; repeat with its exact `--confirm <SHA256>`. Inspect with `singularity-flow mcp auth status playwright`; remove with `singularity-flow mcp auth remove playwright --profile <ID> --confirm <ACTIVE-SHA256>`. If corrupt state prevents normal removal, preview and confirm `singularity-flow mcp auth clear playwright`. Only IDs, counts, and digests may be displayed. Windows imports apply and verify a current-user-only ACL and fail closed if that protection is unavailable or unsafe.
- After reviewing, trusting, starting, and authenticating the host server, create a local readiness receipt: `singularity-flow mcp attest <SERVER> --confirm <SERVER>`.
- With browser consent, prove launch, tools, same-origin navigation, snapshot, and close: `singularity-flow mcp smoke playwright --url <AUTHORIZED-URL>`. An origin-bound phase also records navigation evidence.
- Merge an explicit VS Code host entry without replacing unrelated servers: `singularity-flow mcp scaffold playwright` or `singularity-flow mcp scaffold figma` (`--local` selects Figma's desktop endpoint).
- Record output with `singularity-flow mcp record <SERVER> --tool <TOOL> --phase <PHASE> [--output <PATH>] [--note TEXT]`. Only live smoke can record origin-bound navigation; snapshots must report an authorized `Page URL`.
- Record pinned Figma metadata: `singularity-flow mcp record figma --kind design-source --tool get_metadata --phase design-intake --output <XML> --file-key <KEY> --file-version <VERSION> [--node 1:3]`.
- Inspect the exact approved source set downstream prompts will use: `singularity-flow mcp design-sources status`.

The host owns transport, trust, and credentials; Flow owns allowlisting and provenance. `ready` binds host, policy, and authentication-profile digest. A Playwright phase also requires a valid exact-package warm proof; `requireSmoke` needs a receipt under 24 hours old on the Story origin. Never print environment variables, put secrets in `workflow.yml`, silently replace `.vscode/mcp.json`, or overstate a hash receipt.

For Playwright, honor the repository or corporate `.npmrc`; do not override the npm registry in the generated configuration. Keep VS Code/Copilot approval prompts enabled.
