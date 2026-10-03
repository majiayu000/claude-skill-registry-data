---
name: ls-mcp-builder
description: "Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (MCPServer) or Node/TypeScript (MCP SDK)."
metadata:
  version: "1.2"
compatibility: "Python 3.12+. Scripts in scripts/ (evaluation.py, connections.py, llm_providers/) follow framework tooling standard. MCP connection: mcp. Claude: anthropic. OpenAI-compatible: openai. Emulation: no extra deps; uses JSON script to simulate LLM."
license: Complete terms in LICENSE.txt
---

# MCP Server Development Guide

Use this skill when designing, implementing, or evaluating an MCP server for an
external API or service. Keep the main workflow short, then load the detailed
reference that matches the implementation language or evaluation task.

## Load First

- MCP protocol: fetch `https://modelcontextprotocol.io/llms-full.txt`
- [MCP best practices](./references/mcp_best_practices.md)
- Python SDK docs: fetch `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- TypeScript SDK docs: fetch `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`

## Workflow

### 1. Research and Plan

- Read the target service API docs: auth, rate limits, pagination, errors,
  endpoints, schemas, and destructive operations.
- Design workflow-level tools instead of thin endpoint wrappers.
- Prefer high-signal outputs, stable human-readable IDs, and explicit
  `concise` or `detailed` response modes.
- Plan shared request helpers, pagination, formatting, input validation,
  authentication, and actionable error messages before writing tools.
- Mark read-only, destructive, idempotent, and open-world behavior with MCP tool
  annotations where supported.

### 2. Implement

For Python, load [Python implementation guide](./references/python_mcp_server.md).
Use the MCP Python SDK, Pydantic models, type hints, async I/O for external
calls, shared helpers, and clear module-level constants.

For Node/TypeScript, load
[TypeScript implementation guide](./references/node_mcp_server.md). Use the MCP
TypeScript SDK, strict TypeScript, Zod schemas, explicit return types, and a
working build script.

For every tool:

- Use schema validation with useful constraints and examples.
- Write descriptions that explain when to use the tool, expected inputs,
  output shape, and recovery steps for common errors.
- Keep tool outputs bounded and predictable; paginate or summarize large data.
- Return errors as actionable tool results when the agent can recover.

### 3. Review and Test

- Check for duplicated code, inconsistent output formats, weak validation, and
  generic exceptions.
- Do not run long-lived stdio MCP servers directly in the main terminal without
  a timeout or harness.
- Python smoke checks: `python -m py_compile server.py`, then run the evaluation
  harness or a short timeout test.
- TypeScript smoke checks: `npm run build`, confirm `dist/` output, then run the
  evaluation harness or a short timeout test.
- Use the quality checklist in the language guide before handing off.

### 4. Evaluate

Load [evaluation guide](./references/evaluation.md) to create read-only,
verifiable questions and run the bundled harness.

Run the harness with its dependencies from the skill directory:

```bash
uv run --with 'mcp>=2,<3' --with 'anthropic>=0.39.0' --with 'openai>=1.0.0' -- python scripts/evaluation.py --help
```

Provider examples:

```bash
# Claude provider
ANTHROPIC_API_KEY=... uv run --with 'mcp>=2,<3' --with 'anthropic>=0.39.0' --with 'openai>=1.0.0' -- python scripts/evaluation.py \
  -t stdio -c python -a my_server.py evaluation.xml

# OpenAI-compatible provider
OPENAI_API_KEY=... uv run --with 'mcp>=2,<3' --with 'anthropic>=0.39.0' --with 'openai>=1.0.0' -- python scripts/evaluation.py --provider openai \
  -t stdio -c python -a my_server.py evaluation.xml

# Emulation provider, no LLM key
uv run --with 'mcp>=2,<3' -- python scripts/evaluation.py --provider emulation \
  --emulation-script assets/smoke_emulation.json \
  -t stdio -c python -a my_server.py assets/smoke_eval.xml
```

The evaluation XML format is:

```xml
<evaluation>
  <qa_pair>
    <question>Question that requires read-only tool use.</question>
    <answer>Stable expected answer.</answer>
  </qa_pair>
</evaluation>
```

## Reference Library

- [MCP best practices](./references/mcp_best_practices.md): universal design,
  naming, response, pagination, security, and error-handling guidance.
- [Python implementation guide](./references/python_mcp_server.md): MCPServer
  examples, Pydantic patterns, resources, prompts, and quality checklist.
- [TypeScript implementation guide](./references/node_mcp_server.md): SDK server
  structure, Zod patterns, tool registration, build setup, and checklist.
- [Evaluation guide](./references/evaluation.md): question design, XML format,
  harness setup, providers, reporting, and troubleshooting.
