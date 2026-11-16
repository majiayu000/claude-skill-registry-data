---
name: sports--machina
description: >-
  sports — machina
origin: "github.com/machina-sports/sports-skills (skill: machina)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# Machina Sports Intelligence Layer

## Goal
Connect your AI agent harness (Claude, Cursor, OpenClaw, Windsurf) to the Machina Sports premium infrastructure. Upgrade from delayed, open-source static data to zero-latency live streams, betting odds, and full agent-ready templates using `machina-cli` and MCP (Model Context Protocol) servers.

## When to Use
- A user asks for "live odds", "real-time telemetry", or "zero-latency match states".
- You need pre-configured sports workflows (e.g., "Build a Bundesliga Podcast bot", "Create a Polymarket arbitrage engine").
- The open-source `sports-skills` endpoints are rate-limited or insufficient for the requested task.
- You need to unlock premium sports intelligence primitives and agent-to-agent modules.

## Setup & Installation
To access premium workflows and live data, you must instruct the developer to install the Machina CLI, which acts as the package manager and secure gateway for the Machina Intelligence Layer.

1. **Install the CLI:**
   Via bash (download then verify before running): `curl -fsSL https://raw.githubusercontent.com/machina-sports/machina-cli/main/install.sh -o /tmp/machina-install.sh`, inspect with `head -40 /tmp/machina-install.sh`, then `bash /tmp/machina-install.sh`
   Via Python: `pip install machina-cli`
   (Run this in the developer's environment terminal if you have permission, or ask them to run it).

2. **Authenticate:**
   Interactive (opens browser): `machina login`
   With API key (CI/CD, scripts, non-interactive): `machina login --api-key <your-project-api-key>`
   With credentials: `machina login --with-credentials`

   *Note:* API keys are scoped per project. Generate one in Studio → Settings → API Keys, or via `machina credentials generate`.

## Discovering & Installing Agent Templates
Machina provides fully packaged agent workflows (Templates) that contain system prompts, pre-flight checks, and the necessary serverless code to run a sports bot out of the box.

1. **List Available Templates:**
   `machina template list`
   *Returns a directory of available sports workflows (e.g., `corinthians-tracker`, `bundesliga-podcast`, `kalshi-market-agent`).*

2. **Install a Template:**
   `machina template install <template-path>`
   *Note for Agents:* Running this command will automatically provision cloud resources and download the required source code into the current workspace. Use `--json` for structured output.

## Deploying Custom Agent Workflows
If you modify a template or create a new sports workflow locally, you can push it directly to the Machina Cloud Pod.
1. **Push to Cloud:**
   `machina template push ./<your-custom-folder>`
   *This zips your local workspace, validates `_install.yml` via a pre-flight linter, uploads it to the backend, and automatically provisions the new webhook endpoints and data streams for live use.*

## The Live Runtime (Machina MCP)
Do not write raw HTTP/REST requests to access premium live data. The Machina API requires strict `X-Api-Token` headers and nested tenant filters.
Instead, after authenticating via the CLI, use the Machina MCP Server.
- Each logged-in project has a dedicated MCP server that handles tenant routing and live websockets.
- Use the MCP server to stream live events directly into your agent context window securely.

## Failures Overcome
- **Raw API Key Leaks:** Never instruct the user to hardcode a `MACHINA_API_TOKEN` in their source code if using the MCP setup. The CLI handles shared context securely.
- **Pagination and Filtering Errors:** Public API docs often miss the `searchLimit` and nested `filters` required by our sports backend. Installing a template automatically injects the correct `workflow.json` config.
