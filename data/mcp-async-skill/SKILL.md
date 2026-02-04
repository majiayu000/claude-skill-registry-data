---
name: mcp-async-skill
description: Generate Skills from HTTP MCP servers with async job patterns (submit/status/result). Use when converting MCP specifications (.mcp.json) into reusable Skills using mcp_tool_catalog.yaml, or when calling async MCP tools via JSON-RPC 2.0 with session-based polling.
---

# MCP Async Skill Generator

Generate reusable Skills from HTTP MCP servers that use async job patterns.

## When to Use

- Converting `.mcp.json` into a packaged Skill (tool info is fetched from catalog)
- Calling async MCP tools: submit → poll status → get result → download
- Integrating image/video generation MCPs (fal.ai, Replicate, etc.)

## File Upload (for image/audio/video inputs)

Many MCPs require URL inputs for media files. Use `fal_client` to upload local files:

```bash
# Upload file and get URL (one-liner)
python -c "import fal_client; url=fal_client.upload_file(r'/path/to/file.png'); print(f'URL: {url}')"

# Examples for different platforms:
# Windows
python -c "import fal_client; url=fal_client.upload_file(r'C:\Users\name\image.png'); print(f'URL: {url}')"

# Linux/Mac
python -c "import fal_client; url=fal_client.upload_file('/home/user/image.png'); print(f'URL: {url}')"

# Android (Termux)
python -c "import fal_client; url=fal_client.upload_file('/storage/emulated/0/Download/image.png'); print(f'URL: {url}')"
```

The returned URL (e.g., `https://v3b.fal.media/files/...`) can be used in `image_url`, `image_urls`, `audio_url`, etc. parameters.

**Supported formats:** png, jpg, jpeg, gif, webp, mp3, wav, mp4, webm, etc.

## Quick Start

### Generate Skill from MCP Config (Recommended)

Tool information is automatically fetched from `mcp_tool_catalog.yaml`:

```bash
python scripts/generate_skill.py \
  --mcp-config /path/to/.mcp.json
```

Output: `.claude/skills/<skill-name>/SKILL.md`

The server name in `.mcp.json` is used to look up tools from the catalog.

### Generate Skill with Legacy tools.info

If you have a local `tools.info` file:

```bash
python scripts/generate_skill.py \
  --mcp-config /path/to/.mcp.json \
  --tools-info /path/to/tools.info \
  --name my-mcp-skill
```

### Specify Custom Output Directory

```bash
python scripts/generate_skill.py \
  --mcp-config /path/to/.mcp.json \
  --output /custom/path
```

### Direct Async Tool Call

```bash
python scripts/mcp_async_call.py \
  --endpoint "https://mcp.example.com/sse" \
  --submit-tool "generate_image" \
  --status-tool "check_status" \
  --result-tool "get_result" \
  --args '{"prompt": "a cat"}' \
  --output ./output
```

## Async Pattern Flow

```
1. SUBMIT    → POST JSON-RPC → Get session_id
2. STATUS    → Poll with session_id → Wait for "completed"
3. RESULT    → Get download URL
4. DOWNLOAD  → Save file locally
```

## JSON-RPC 2.0 Format

All MCP calls use this structure:

```json
{
  "jsonrpc": "2.0",
  "id": "unique-id",
  "method": "tools/call",
  "params": {
    "name": "tool_name",
    "arguments": { "key": "value" }
  }
}
```

## Input File Formats

### .mcp.json

The server `name` must match a server `id` in the catalog:

```json
{
  "mcpServers": {
    "t2i-kamui-fal-flux-lora": {
      "type": "http",
      "url": "https://kamui-code.ai/t2i/fal/flux-lora",
      "headers": {
        "KAMUI-CODE-PASS": "your-pass"
      }
    }
  }
}
```

Or direct format:

```json
{
  "name": "t2i-kamui-fal-flux-lora",
  "url": "https://kamui-code.ai/t2i/fal/flux-lora",
  "auth_header": "KAMUI-CODE-PASS",
  "auth_value": "your-pass"
}
```

### mcp_tool_catalog.yaml (Auto-fetched)

Tool information is fetched from:
`https://raw.githubusercontent.com/Yumeno/kamuicode-config-manager/main/mcp_tool_catalog.yaml`

The catalog contains 266+ servers with tool definitions:

```yaml
servers:
  - id: t2i-kamui-fal-flux-lora
    status: online
    tools:
      - name: flux_lora_submit
        description: Submit Flux LoRA image generation request
        inputSchema:
          properties:
            prompt:
              description: Image prompt
              type: string
          required:
            - prompt
          type: object
```

### tools.info (Legacy)

Optional, for backward compatibility:

```json
[
  {
    "name": "generate",
    "description": "Generate content",
    "inputSchema": {
      "type": "object",
      "properties": {
        "prompt": { "type": "string", "description": "Input prompt" }
      },
      "required": ["prompt"]
    }
  }
]
```

## Script Reference

### `scripts/mcp_async_call.py`

Main async MCP caller with full flow automation.

**Options:**
- `--endpoint, -e`: MCP server URL
- `--submit-tool`: Tool name for job submission
- `--status-tool`: Tool name for status checking
- `--result-tool`: Tool name for result retrieval
- `--args, -a`: Submit arguments as JSON string
- `--args-file`: Load arguments from JSON file
- `--output, -o`: Output directory (default: ./output)
- `--poll-interval`: Seconds between polls (default: 2.0)
- `--max-polls`: Maximum poll attempts (default: 300)
- `--header`: Add custom header (format: `Key:Value`)
- `--config, -c`: Load endpoint from .mcp.json

### `scripts/generate_skill.py`

Generate complete Skill from MCP specifications.

**Options:**
- `--mcp-config, -m`: Path to .mcp.json (required)
- `--tools-info, -t`: Path to tools.info (optional, legacy mode)
- `--output, -o`: Output directory
- `--name, -n`: Skill name (auto-detected if omitted)
- `--catalog-url`: Custom catalog URL (default: GitHub raw URL)

**Requirements:**
- `pip install pyyaml requests` (for catalog fetching)

## Generated Skill Structure

Skills are generated to `.claude/skills/<skill-name>/`:

```
.claude/skills/
└── skill-name/
    ├── SKILL.md              # Usage documentation
    ├── scripts/
    │   ├── mcp_async_call.py # Core async caller
    │   └── skill_name.py     # Convenience wrapper
    └── references/
        ├── mcp.json          # Original MCP config
        └── tools.json        # Original tool specs
```

## Common Status Values

| Status | Meaning |
|--------|---------|
| `pending`, `queued` | Job waiting |
| `processing`, `running` | In progress |
| `completed`, `done`, `success` | Finished |
| `failed`, `error` | Failed |

## Programmatic Usage

```python
from scripts.mcp_async_call import run_async_mcp_job

result = run_async_mcp_job(
    endpoint="https://mcp.example.com/sse",
    submit_tool="generate",
    submit_args={"prompt": "sunset over mountains"},
    status_tool="status",
    result_tool="result",
    output_path="./output",
    poll_interval=2.0,
    max_polls=300,
)

print(result["saved_path"])  # Path to downloaded file
```

## Error Handling

The script handles:
- JSON-RPC errors in response
- Job failures (status: failed/error)
- Timeout after max polls
- Download failures

All errors raise exceptions with descriptive messages.
