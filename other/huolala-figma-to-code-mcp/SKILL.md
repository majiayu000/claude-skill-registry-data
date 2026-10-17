---
name: huolala-figma-to-code-mcp
description: Convert Figma designs to high-fidelity UI code via MCP service with AI-powered layout processing
triggers:
  - convert figma design to code
  - set up figma mcp service
  - figma to html react vue
  - design to code with high fidelity
  - export figma frame as code
  - configure figma mcp server
  - use huolala figma service
  - convert ui design to implementation
---

# Huolala Figma to Code MCP

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Huolala Figma MCP is an MCP service that automatically converts Figma designs into high-fidelity UI code. It uses an intermediate DSL representation, processes designs through a pipeline (system bar removal, red dot detection, icon recognition, layout calculation), and outputs a ZIP package containing HTML, sliced images, fonts, and other assets ready for LLM conversion to target platforms (React, Vue, Swift, Kotlin, React Native, etc.).

## What It Does

The service:
- Fetches Figma designs via API and converts to intermediate DSL
- Runs an 8-step processing pipeline: DSL tree building, system bar removal, VLM recognition (optional), red dot processing, icon recognition, layer cleaning, layout calculation, asset packaging
- Exports ZIP with `index.html`, sliced images, fonts, `dsl.json`, design screenshot
- Supports high-fidelity conversion: distributed alignment, center alignment, linear/overlapping layout, list detection, automatic text sizing
- Exposes MCP tools for AI clients (Cursor, Cline, etc.)

**Core workflow**: Figma API → DSL → Pipeline (rules engine + optional VLM) → ZIP package

## Installation

### Prerequisites

- Python 3.11+
- Figma Personal Access Token ([Settings → Security](https://www.figma.com/settings))

### Setup

```bash
# Clone repository
git clone https://github.com/HuolalaTech/huolala-figma-mcp.git
cd huolala-figma-mcp

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env and set:
# MDAP_FIGMA_TOKEN=your_figma_token_here
```

### Start MCP Service

```bash
python -m mdap_u2c --port=10001
```

Service will be available at `http://localhost:10001/mcp`

### Configure MCP Client

Add to your MCP client configuration (e.g., Cursor, Claude Desktop):

```json
{
  "mcpServers": {
    "ui2code-local": {
      "url": "http://localhost:10001/mcp",
      "transport": "http"
    }
  }
}
```

## Key MCP Tool

### `figma_to_code_package`

Converts a Figma design URL to a downloadable ZIP package.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `figma_url` | string | Full Figma URL with `/file/{key}/` or `/design/{key}/` and `?node-id=` |
| `image_scale` | array | Image scale factors (1-4), e.g., `[3, 2]` for 3x and 2x |
| `target_platform` | string | Target platform: `h5`, `vue`, `react`, `react native`, `ios`, `android` |

**Example call from AI agent:**

```
Use the figma_to_code_package tool with:
- figma_url: https://www.figma.com/design/abc123/MyDesign?node-id=1-2
- image_scale: [3, 2]
- target_platform: react
```

**Response:**

```json
{
  "zip_url": "http://localhost:10001/download/abc123.zip",
  "metadata": {
    "node_id": "1-2",
    "file_key": "abc123",
    "platform": "react"
  },
  "message": "zip_url 可直接下载"
}
```

**ZIP Contents:**

```
extracted_package/
├── index.html          # Rule-based HTML for LLM conversion
├── images/             # Sliced assets, icons
│   ├── icon_001.png
│   └── background_002.png
├── fonts/              # Font files
│   └── CustomFont.ttf
├── dsl.json            # Intermediate DSL structure
├── design.png          # Original design screenshot
└── vlm_result.json     # VLM output (if enabled)
```

## Configuration

### Environment Variables

```bash
# Required
MDAP_FIGMA_TOKEN=figd_...              # Figma Personal Access Token

# Optional VLM (multimodal) support
MDAP_VLM_PROVIDER=openai               # Provider: openai, anthropic, etc.
MDAP_VLM_API_KEY=sk-...                # API key for VLM
MDAP_VLM_MODEL=gpt-4o                  # Model name
MDAP_VLM_BASE_URL=https://api.openai.com/v1  # API base URL

# Service configuration
MDAP_PORT=10001                        # Service port (default: 10001)
```

### Pipeline Processors

The DSL processing pipeline has configurable processors in `src/mdap_u2c/dsl_processors/`:

1. **DslToTreeProcessor** - Build node tree with overlap/containment tracking
2. **SystemBarProcessor** - Remove status bar and home bar
3. **VlmProcessor** - Multimodal LLM for list detection (optional, disabled by default)
4. **RedDotProcessor** - Detect and adjust red dot badges
5. **IconProcessor** - Recognize and merge icon components
6. **CleanProcessor** - Remove invisible/transparent redundant layers
7. **LayoutProcessor** - Calculate projection splits, list layouts, auto-sizing
8. **ExportProcessor** - Package assets, deduplicate images, export HTML

Processors are auto-registered and run in priority order.

## Using Prompt Templates

Templates in `assets/prompts/` standardize MCP tool calls and transcoding workflows.

### Available Templates

| Template | MCP Prompt Name | Purpose |
|----------|-----------------|---------|
| `get_figma_property.md` | `get_figma_property` | Extract Figma properties (text, styles) for partial UI updates |
| `ui2code_with_skills.md` | `ui2code_with_skills` | Full UI-to-code: fetch ZIP, adjust components, load Skills, generate code |

### Using in Cursor/IDEs with MCP Prompts

```
/ui2code_with_skills
```

Then provide:
- Figma URL
- Target platform (react, vue, ios, etc.)
- Additional requirements

### Using in IDEs Without MCP Prompts

Copy template content from `assets/prompts/*.md` into your IDE's Skills/Rules directory.

## Code Examples

### Python: Direct Service Usage

```python
from mdap_u2c.services.ui2code_service import UI2CodeService
from mdap_u2c.config import config
import asyncio

async def convert_figma():
    service = UI2CodeService()
    
    result = await service.figma_to_code_package(
        figma_url="https://www.figma.com/design/abc123/MyApp?node-id=1-2",
        image_scale=[3, 2],
        target_platform="react"
    )
    
    print(f"Download ZIP: {result['zip_url']}")
    print(f"Metadata: {result['metadata']}")

asyncio.run(convert_figma())
```

### Python: Custom DSL Processor

```python
from mdap_u2c.dsl_processors.base import BaseDslProcessor, register_processor
from mdap_u2c.dsl.models import DslComponent

@register_processor
class CustomLayoutProcessor(BaseDslProcessor):
    priority = 650  # Run after LayoutProcessor (600)
    
    async def process(self, dsl_component: DslComponent) -> DslComponent:
        # Custom layout logic
        if dsl_component.type == "container":
            # Adjust container properties
            dsl_component.layout = "custom-grid"
        
        return dsl_component
```

### Python: Accessing Figma Data Directly

```python
from mdap_u2c.figma.client import FigmaClient
from mdap_u2c.config import config

async def get_figma_nodes():
    client = FigmaClient(config.figma_token)
    
    # Get file nodes
    file_data = await client.get_file(
        file_key="abc123",
        node_ids=["1:2", "1:3"]
    )
    
    # Get images
    images = await client.get_images(
        file_key="abc123",
        node_ids=["1:2"],
        scale=3.0
    )
    
    return file_data, images
```

### JavaScript/TypeScript: MCP Client Integration

```typescript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const client = new Client({
  name: 'figma-converter',
  version: '1.0.0'
});

await client.connect(
  new StdioClientTransport({
    command: 'python',
    args: ['-m', 'mdap_u2c', '--port=10001']
  })
);

const result = await client.callTool({
  name: 'figma_to_code_package',
  arguments: {
    figma_url: 'https://www.figma.com/design/abc123/App?node-id=1-2',
    image_scale: [3, 2],
    target_platform: 'react'
  }
});

console.log(result.zip_url);
```

## Common Workflows

### Convert Figma to React

1. Start MCP service: `python -m mdap_u2c --port=10001`
2. In AI agent (Cursor): `/ui2code_with_skills`
3. Provide Figma URL and select `react` as target
4. Agent calls `figma_to_code_package` → receives ZIP
5. Agent extracts `index.html` and converts to React components using project Skills
6. Agent generates component code with proper imports, props, styling

### Convert Figma to Vue

Same workflow, specify `vue` as target platform. Agent uses Vue-specific Skills from `assets/prompts/`.

### Extract Figma Properties Only

1. In AI agent: `/get_figma_property`
2. Provide Figma URL
3. Agent retrieves text content, colors, spacing, typography without full conversion
4. Useful for updating existing UI rather than full regeneration

### Enable VLM for Complex UI

```bash
# Configure VLM in .env
export MDAP_VLM_PROVIDER=openai
export MDAP_VLM_API_KEY=sk-...
export MDAP_VLM_MODEL=gpt-4o
export MDAP_VLM_BASE_URL=https://api.openai.com/v1

# Restart service
python -m mdap_u2c --port=10001
```

VLM processor will now detect lists, repeating components, and complex layouts automatically.

## Testing

### Automated Comparison Testing

Batch-test multiple Figma URLs and generate HTML similarity reports:

```bash
# Install test dependencies
pip install ".[ui2code-test]"
playwright install chromium

# Configure test URLs in tests/test_url_list.txt
# Each line: figma_url|node_id|platform

# Run tests
python tests/ui2code_auto_test.py
```

Test output includes visual comparison screenshots and similarity scores.

### Manual Testing

```bash
# Start service
python -m mdap_u2c --port=10001

# In another terminal, test MCP endpoint
curl http://localhost:10001/health
# Should return: {"status": "healthy"}

# Test tool via HTTP (if HTTP transport enabled)
curl -X POST http://localhost:10001/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "figma_to_code_package",
      "arguments": {
        "figma_url": "https://www.figma.com/design/abc/test?node-id=1-2",
        "image_scale": [2],
        "target_platform": "h5"
      }
    }
  }'
```

## Troubleshooting

### Service Won't Start

**Problem**: `ModuleNotFoundError` or import errors

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall in editable mode
pip install -e .
```

### Figma Token Invalid

**Problem**: `401 Unauthorized` errors

**Solution**:
- Verify token in `.env` matches your Figma Personal Access Token
- Generate new token at [Figma Settings → Security](https://www.figma.com/settings)
- Ensure token has file access permissions

### MCP Client Can't Connect

**Problem**: Client shows "Connection refused"

**Solution**:
```bash
# Check service is running
curl http://localhost:10001/health

# Verify port in client config matches service port
# Default is 10001, change with:
python -m mdap_u2c --port=8080
```

### ZIP Download Fails

**Problem**: `zip_url` returns 404

**Solution**:
- ZIP files are temporary; download immediately after generation
- Check service logs for export errors
- Verify disk space for temporary ZIP storage

### Low Fidelity Output

**Problem**: Generated HTML doesn't match design

**Solution**:
- Enable VLM for complex layouts (see VLM configuration above)
- Check `dsl.json` in ZIP to verify DSL structure
- Increase `image_scale` to `[3, 2]` for higher resolution assets
- Review `design.png` vs output to identify specific issues

### VLM Not Working

**Problem**: VLM processor skipped or errors

**Solution**:
```bash
# Verify all VLM env vars are set
echo $MDAP_VLM_PROVIDER
echo $MDAP_VLM_API_KEY
echo $MDAP_VLM_MODEL

# Test VLM API separately
curl $MDAP_VLM_BASE_URL/chat/completions \
  -H "Authorization: Bearer $MDAP_VLM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o", "messages": [{"role": "user", "content": "test"}]}'
```

### Memory Issues with Large Designs

**Problem**: Service crashes or slows on large Figma files

**Solution**:
- Convert smaller frames/sections instead of entire pages
- Increase system memory allocation
- Disable VLM if not needed (reduces memory footprint)

### Font Files Missing

**Problem**: ZIP contains no fonts or fonts don't render

**Solution**:
- Ensure Figma design uses fonts available in `assets/fonts/`
- Add custom fonts to `assets/fonts/` directory
- Check font licensing for redistribution

## Project Structure

```
huolala-figma-mcp/
├── src/mdap_u2c/
│   ├── figma/              # Figma API client, node parsing
│   ├── dsl_processors/     # Pipeline processors (8 steps)
│   ├── services/           # FigmaService, UI2CodeService, ExportService
│   ├── server/             # FastMCP server, MCP tools/prompts
│   ├── dsl/                # DSL models and utilities
│   └── config/             # Configuration management
├── assets/
│   ├── fonts/              # Font files
│   ├── prompts/            # MCP prompt templates
│   └── cv_templates/       # Computer vision templates
├── tests/
│   ├── ui2code_auto_test.py  # Automated comparison testing
│   └── test_url_list.txt     # Test Figma URLs
└── pyproject.toml          # Dependencies and metadata
```

## Advanced Usage

### Custom Skills for Target Platforms

Create platform-specific conversion skills in `assets/prompts/skills/`:

```markdown
# assets/prompts/skills/react_native_skill.md

## React Native Conversion Rules

When converting to React Native:
- Use `View` instead of `div`
- Use `Text` for all text content
- Use `StyleSheet.create()` for styles
- Convert `px` to responsive units
- Use `Image` with `source` prop for assets
```

Reference in main prompt template to load conditionally.

### Extending the DSL Pipeline

Add custom processors by subclassing `BaseDslProcessor`:

```python
from mdap_u2c.dsl_processors.base import BaseDslProcessor, register_processor

@register_processor
class AccessibilityProcessor(BaseDslProcessor):
    priority = 700  # After layout, before export
    
    async def process(self, dsl_component):
        # Add accessibility labels
        if dsl_component.type == "image":
            dsl_component.properties["aria-label"] = "Generated image"
        
        return dsl_component
```

Processor runs automatically when registered.

---

**Additional Resources:**
- [FastMCP Documentation](https://gofastmcp.com/)
- [Figma REST API](https://www.figma.com/developers/api)
- [GitHub Repository](https://github.com/HuolalaTech/huolala-figma-mcp)
