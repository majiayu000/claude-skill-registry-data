---
name: semantik-plugin-development
description: Create semantik plugins (connectors, embeddings, chunkers, rerankers, extractors, agents). Use when developing plugins, creating new integrations, or asking about plugin patterns, protocols, or testing.
metadata:
  short-description: Develop semantik plugins
---

# Semantik Plugin Development

This skill helps you create plugins for Semantik, a self-hosted semantic search engine. Plugins extend Semantik's capabilities for document ingestion, embedding, chunking, reranking, extraction, and AI agents.

## Protocol Version

**Current Version:** 1.0.0

Breaking changes to protocols increment the major version. Your plugins continue to work as long as they satisfy the protocol interface.

## Security Note

Plugins run **in-process** with the main Semantik application (no sandboxing). Only install plugins you trust. See [Security Guide](security-guide.md) for details.

## Quick Start

Create a minimal connector plugin in 5 minutes:

```python
# my_connector.py
from typing import ClassVar, Any, AsyncIterator
import hashlib

class MyConnector:
    PLUGIN_ID: ClassVar[str] = "my-connector"
    PLUGIN_TYPE: ClassVar[str] = "connector"
    PLUGIN_VERSION: ClassVar[str] = "1.0.0"

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    async def authenticate(self) -> bool:
        return True

    async def load_documents(self, source_id: int | None = None) -> AsyncIterator[dict[str, Any]]:
        content = "Document content..."
        yield {
            "content": content,
            "unique_id": "doc-1",
            "source_type": self.PLUGIN_ID,
            "metadata": {},
            "content_hash": hashlib.sha256(content.encode()).hexdigest(),
        }

    @classmethod
    def get_config_fields(cls) -> list[dict[str, Any]]:
        return []

    @classmethod
    def get_secret_fields(cls) -> list[dict[str, Any]]:
        return []

    @classmethod
    def get_manifest(cls) -> dict[str, Any]:
        return {"id": cls.PLUGIN_ID, "type": cls.PLUGIN_TYPE, "version": cls.PLUGIN_VERSION,
                "display_name": "My Connector", "description": "Custom connector"}
```

---

## Plugin Types

| Type | Purpose | Key Method | Template |
|------|---------|------------|----------|
| `connector` | Ingest documents from sources | `load_documents()` | [connector.py](../../../templates/connector.py) |
| `embedding` | Convert text to vectors | `embed_texts()` | [embedding.py](../../../templates/embedding.py) |
| `chunking` | Split documents into chunks | `chunk()` | [chunking.py](../../../templates/chunking.py) |
| `reranker` | Reorder search results | `rerank()` | [reranker.py](../../../templates/reranker.py) |
| `extractor` | Extract entities/metadata | `extract()` | [extractor.py](../../../templates/extractor.py) |
| `agent` | LLM-powered capabilities | `execute()` | [agent.py](../../../templates/agent.py) |

**Type-specific guides:**
- [Connector Guide](connector-guide.md) - Document sources, async iterators
- [Embedding Guide](embedding-guide.md) - Query/document modes, dimensions
- [Chunking Guide](chunking-guide.md) - Text segmentation strategies
- [Reranker Guide](reranker-guide.md) - Cross-encoder reranking
- [Extractor Guide](extractor-guide.md) - Entity and metadata extraction
- [Agent Guide](agent-guide.md) - LLM agents, streaming, context

**Cross-cutting guides:**
- [Testing Guide](testing-guide.md) - Contract tests, mocks, fixtures
- [Security Guide](security-guide.md) - Trust model, best practices
- [Advanced Guide](advanced-guide.md) - Health checks, dependencies, migration

---

## Development Approach

### Protocol-Based (Recommended)

Use plain Python classes with no semantik imports. Plugins are validated by structural typing (duck typing):

```python
class MyPlugin:
    PLUGIN_ID: ClassVar[str] = "my-plugin"
    PLUGIN_TYPE: ClassVar[str] = "connector"  # or embedding, chunking, etc.
    PLUGIN_VERSION: ClassVar[str] = "1.0.0"
    # ... implement required methods
```

**Benefits:**
- Zero dependencies on semantik
- Develop in separate repository
- Distribute via PyPI or git
- No version conflicts

### ABC-Based (Advanced)

Inherit from semantik base classes when you need access to internal utilities:

```python
from shared.connectors.base import BaseConnector

class MyConnector(BaseConnector):
    # ... inherit helper methods
```

**Use when:**
- Building embedding plugins with GPU management
- Need access to shared utilities
- Developing internal/builtin plugins

---

## Required Class Variables

Every plugin must define:

```python
from typing import ClassVar, Any

class MyPlugin:
    PLUGIN_ID: ClassVar[str] = "my-plugin"      # Unique ID (lowercase, hyphens)
    PLUGIN_TYPE: ClassVar[str] = "connector"    # One of 6 types
    PLUGIN_VERSION: ClassVar[str] = "1.0.0"     # Semantic version
```

Some plugin types require additional class variables:

| Type | Additional Variables |
|------|---------------------|
| `connector` | `METADATA` (dict with name, description, icon) |
| `embedding` | `INTERNAL_NAME`, `API_ID`, `PROVIDER_TYPE`, `METADATA` |
| `chunking` | (none) |
| `reranker` | (none) |
| `extractor` | (none) |
| `agent` | (none) |

---

## Manifest Method

All plugins must implement `get_manifest()`:

```python
@classmethod
def get_manifest(cls) -> dict[str, Any]:
    return {
        "id": cls.PLUGIN_ID,
        "type": cls.PLUGIN_TYPE,
        "version": cls.PLUGIN_VERSION,
        "display_name": "My Plugin",
        "description": "What the plugin does",
        # Optional fields:
        "author": "Your Name",
        "license": "MIT",
        "homepage": "https://github.com/...",
        "requires": ["other-plugin"],  # Dependencies
        "capabilities": {},  # Plugin-specific capabilities
    }
```

---

## Configuration

### Config Fields (UI)

Define configuration fields for the Semantik UI:

```python
@classmethod
def get_config_fields(cls) -> list[dict[str, Any]]:
    return [
        {
            "name": "base_url",
            "type": "text",        # text, password, number, boolean, select
            "label": "Base URL",
            "description": "API endpoint",
            "required": True,
            "placeholder": "https://api.example.com",
        },
        {
            "name": "model",
            "type": "select",
            "label": "Model",
            "options": ["model-a", "model-b"],
            "default": "model-a",
        },
    ]
```

### Secret Fields

Mark fields that contain secrets (encrypted at rest):

```python
@classmethod
def get_secret_fields(cls) -> list[dict[str, Any]]:
    return [
        {"name": "api_key", "label": "API Key", "required": True},
    ]
```

### Environment Variables

Use the `_env` suffix pattern for secrets:

```python
# In config schema - user enters env var name
"api_key_env": "OPENAI_API_KEY"

# At runtime, semantik resolves it
config = {"api_key": "sk-actual-key-value"}  # Resolved
```

---

## Testing

### Manual Verification

```bash
pip install -e .
python -c "
from my_plugin import MyConnector
print(f'ID: {MyConnector.PLUGIN_ID}')
print(f'Type: {MyConnector.PLUGIN_TYPE}')
print(f'Manifest: {MyConnector.get_manifest()}')
"
```

### Protocol Validation

```python
import pytest

class TestMyPlugin:
    def test_has_required_attributes(self):
        assert hasattr(MyPlugin, "PLUGIN_ID")
        assert hasattr(MyPlugin, "PLUGIN_TYPE")
        assert hasattr(MyPlugin, "PLUGIN_VERSION")
        assert MyPlugin.PLUGIN_TYPE == "connector"

    def test_manifest_format(self):
        manifest = MyPlugin.get_manifest()
        assert "id" in manifest
        assert "type" in manifest
        assert "display_name" in manifest

    @pytest.mark.asyncio
    async def test_core_functionality(self):
        plugin = MyPlugin(config={})
        # Test plugin-specific methods
```

### With Semantik Test Mixins

If semantik is installed:

```python
from shared.plugins.testing.contracts import ConnectorProtocolTestMixin

class TestMyConnector(ConnectorProtocolTestMixin):
    plugin_class = MyConnector
```

---

## Packaging

### pyproject.toml

```toml
[project]
name = "semantik-plugin-myconnector"
version = "1.0.0"
requires-python = ">=3.10"
dependencies = []  # Your dependencies only

[project.entry-points."semantik.plugins"]
my-connector = "my_plugin.connector:MyConnector"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

See [templates/pyproject.toml](../../../templates/pyproject.toml) for a complete template.

### Entry Point Format

```
plugin-id = "module.path:ClassName"
```

- `plugin-id`: Should match `PLUGIN_ID`
- `module.path`: Python import path
- `ClassName`: Your plugin class

### Installation

```bash
# Development
pip install -e .

# From git
pip install git+https://github.com/you/semantik-plugin-myconnector.git

# Via Semantik API
POST /api/v2/plugins/install
{"install_command": "git+https://github.com/..."}
```

---

## Common Issues

### Plugin Not Loading

1. Check entry point is registered:
   ```bash
   pip show semantik-plugin-myconnector
   ```

2. Verify PLUGIN_TYPE is valid:
   ```python
   assert PLUGIN_TYPE in ["connector", "embedding", "chunking", "reranker", "extractor", "agent"]
   ```

3. Check for import errors:
   ```python
   try:
       from my_plugin import MyConnector
   except ImportError as e:
       print(f"Error: {e}")
   ```

### Validation Errors

| Error | Fix |
|-------|-----|
| `missing required keys: {'content'}` | Add all required fields to returned dict |
| `Invalid role: 'xyz'` | Use valid string from MESSAGE_ROLES |
| `content_hash must be 64 characters` | Use `hashlib.sha256(text.encode()).hexdigest()` |

### Async Issues

All I/O methods must be async:

```python
# Wrong
def load_documents(self):
    yield {"content": "..."}

# Right
async def load_documents(self) -> AsyncIterator[dict]:
    yield {"content": "..."}
```

---

## Templates

Ready-to-use templates in `templates/`:

| File | Description |
|------|-------------|
| `connector.py` | Document source connector |
| `embedding.py` | Embedding model provider |
| `chunking.py` | Text chunking strategy |
| `reranker.py` | Search result reranker |
| `extractor.py` | Entity/metadata extractor |
| `agent.py` | LLM-powered agent |
| `pyproject.toml` | Package configuration |

Copy a template and modify:

```bash
cp templates/connector.py my_connector.py
# Edit PLUGIN_ID, PLUGIN_VERSION, and implement methods
```

---

## Data Format Reference

### Connector Documents (IngestedDocumentDict)

```python
{
    "content": str,              # Full text (required)
    "unique_id": str,            # Unique identifier (required)
    "source_type": str,          # Your PLUGIN_ID (required)
    "metadata": dict,            # Source metadata (required)
    "content_hash": str,         # SHA-256, 64 hex chars (required)
    "file_path": str | None,     # Local path (optional)
}
```

### Chunk Format (ChunkDict)

```python
{
    "content": str,              # Chunk text (required)
    "metadata": {                # Chunk metadata (required)
        "chunk_index": int,
        "start_offset": int,
        "end_offset": int,
    },
    "chunk_id": str | None,      # Unique ID (optional)
    "embedding": list[float] | None,  # Pre-computed (optional)
}
```

### Rerank Result (RerankResultDict)

```python
{
    "index": int,                # Original document index (required)
    "score": float,              # Relevance score (required)
    "text": str | None,          # Document text (optional)
    "metadata": dict | None,     # Metadata (optional)
}
```

### Agent Message (AgentMessageDict)

```python
{
    "id": str,                   # Unique ID (required)
    "role": str,                 # user, assistant, system, tool_call, tool_result, error
    "type": str,                 # text, thinking, tool_use, tool_output, partial, final, error
    "content": str,              # Message content (required)
    "timestamp": str,            # ISO 8601 (required)
    "is_partial": bool,          # Streaming partial (optional)
    "sequence_number": int,      # Message order (optional)
}
```

---

## Getting Help

- **Semantik docs**: See `semantik/docs/external-plugins.md` for protocol details
- **Protocol reference**: See `semantik/docs/plugin-protocols.md` for full specifications
- **Examples**: Check `semantik/packages/shared/plugins/builtins/` for built-in plugins
