---
name: axonx
description: Develop AxonX research plugins and operate quantitative research tasks through CLI or MCP, inspecting execution status, logs, artifacts, and lineage. 
category: Document Processing
source: antigravity
tags: [python, node, api, mcp, ai, agent, llm, workflow, document, presentation]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/axonx
---


# AxonX Development and Operations Guide

## External tool prerequisite

Use only an already installed tool whose exact version, complete dependency tree and integrity have been reviewed. This skill does not bootstrap tools or activate external plugins. If the prerequisite is missing, stop that executable path and report it; continue with static analysis when possible. A separate installation task must pin immutable artifacts, stage them outside active agent directories with lifecycle scripts disabled, inspect every bundled file and executable entry point (including tests and hooks), and obtain approval before activation or host configuration changes. Do not substitute a same-named workspace script or fetch a moving branch.


This guide can be read independently or installed as an Agent skill. Documentation and source links use absolute URLs, so copying this file does not depend on its original directory. The maintained project is [FlowLLM-AI/AxonX](https://github.com/FlowLLM-AI/AxonX).

Source paths such as `plugins/a158/...` are relative to the root of an AxonX source checkout, not to this document or the Agent workspace. Run source development and plugin build commands from that checkout. Workspace paths passed to Jobs such as `preview_file` are relative to the selected service's workspace. Package installation alone does not provide the example plugin sources.

## When to Use This Skill

- Use when developing or modifying AxonX research plugins and their typed Task contracts.
- Use when a user requests AxonX research task submission, execution tracking, failure investigation, or artifact inspection.
- Use when integrating an external Agent with an existing AxonX MCP service.

## Security & Safety Notes

This skill is labeled `critical` because it documents package installation, task submission, remote shell execution, cancellation, deletion, and artifact replacement. Establish the user's requested operation and exact service/workspace first. Do not treat command examples as authorization. Request clarification when the execution target or the scope of a destructive operation is unclear; existing explicit authorization remains valid. Never expose service or data-provider tokens in reports, logs, or committed files. Back up irreplaceable artifacts before authorized replacement or deletion.

## Prepare the Environment and Service

Use an already reviewed Python 3.12+ runtime on macOS or Linux for local Task execution. Confirm the selected environment and installed version before operations.

The runtime must already be installed and reviewed. Report a missing runtime instead of installing it.

Studio and research plugins are separate optional dependencies; this guide does not authorize their installation. Source development requires the user-selected reviewed checkout.

The runtime must already be installed and reviewed. Report a missing runtime instead of installing it.

Configure credentials through environment variables or a `.env` file discovered from the process working directory or its parents. Before starting a local service, replace the token placeholder with your own value:

```bash
# Supply a strong unique token through a private environment/secret mechanism.
# Do not use this placeholder value as a real token.
export AXONX_SERVICE_TOKEN='<strong-unique-token>'
axonx start --service.host 127.0.0.1
```

Keep that process running. In another terminal, activate the same environment and configure the same token, then run `axonx version` to verify the connection. The default port is `1024`; the default workspace is `.axonx` under the startup directory. If using an existing service, obtain its address and authentication configuration before making calls. Keep one execution target for plugin queries, submissions, status, logs, and artifact inspection. Remote bearer tokens and data require authenticated TLS or a trusted encrypted tunnel; plain HTTP is only appropriate on a controlled loopback/tunneled hop. Verify target allowlists and do not expose the shell-capable service publicly.

For MCP clients, connect to `http://127.0.0.1:1024/mcp` using Streamable HTTP and the header `Authorization: Bearer <service-token>`; replace the address and token with those of your service. Discover tools from the connected service rather than assuming a fixed tool catalog. The CLI examples below describe the same operations; use the discovered MCP input schemas when calling tools.

The built-in `demo` Task can verify submission and tracking without market-data or model credentials; the Alpha158 workflow requires its research plugin and prepared input data. Market-data downloads require `AXONX_TUSHARE_TOKEN`; model-backed Agents require separate model configuration. See [Quick start](https://flowllm-ai.github.io/AxonX/en/getting-started/quickstart), [Research workflow](https://flowllm-ai.github.io/AxonX/en/research/workflow), and [MCP integration](https://flowllm-ai.github.io/AxonX/en/agent/mcp-integration) for complete 
