---
name: lockfile
description: Use when creating llmring.lock file for new project (REQUIRED for all applications), configuring model aliases with semantic task-based names, managing environment-specific profiles (dev/staging/prod), or setting up fallback models - lockfile creation is mandatory first step, bundled lockfile is only for llmring tools
---

# Aliases, Profiles, and Lockfile Configuration

## Installation

```bash
# With uv (recommended)
uv add llmring

# With pip
pip install llmring
```

## When to Create Your Own Lockfile

**You MUST create your own `llmring.lock` for:**
- ✅ Any real application
- ✅ Any library you're building
- ✅ Any code you're committing to git

**The bundled lockfile** that ships with llmring is ONLY for running `llmring lock chat`. It provides the "advisor" alias so the configuration assistant works. **It is NOT for your application.**

## API Overview

This skill covers:
- Lockfile (`llmring.lock`) structure and resolution
- Semantic alias naming (use task names, not performance descriptors)
- Profiles for environment-specific configuration
- Fallback models for automatic failover
- CLI commands for lockfile management
- Python API for alias operations

## Quick Start

```bash
# REQUIRED: Create lockfile in your project
llmring lock init

# BEFORE binding aliases, check available models:
llmring list --provider openai
llmring list --provider anthropic
llmring list --provider google

# THEN bind semantic aliases using CURRENT model names:
llmring bind summarizer "anthropic:claude-3-5-haiku-20241022"
llmring bind analyzer "openai:gpt-4o"

# Or use conversational configuration (recommended - knows current models)
llmring lock chat
```

**⚠️ Important:** Always check `llmring list --provider <name>` for current model names before binding. Model names change frequently (e.g., claude-sonnet-4-5-20250929 → claude-sonnet-4-5-20250929).

**Using aliases in code:**

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    # Use YOUR semantic alias (defined in llmring.lock)
    request = LLMRequest(
        model="summarizer",  # Resolves to model you configured
        messages=[Message(role="user", content="Hello")]
    )
    response = await service.chat(request)
```

## Choosing Alias Names

**Use domain-specific semantic names:**
- ✅ `"summarizer"` - Clear what it does
- ✅ `"code-reviewer"` - Describes purpose
- ✅ `"extractor"` - Self-documenting
- ✅ `"sql-generator"` - Intent is obvious

**Avoid generic performance descriptors:**
- ❌ `"fast"`, `"balanced"`, `"deep"` - Don't describe the task

Generic names like "fast" appear in examples for illustration only. Real applications should use names that describe the task, not model characteristics.

## Lockfile Resolution Order

LLMRing searches for lockfiles in this order:

1. **Explicit path** via `lockfile_path` parameter (must exist)
2. **Environment variable** `LLMRING_LOCKFILE_PATH` (must exist)
3. **Current directory** `./llmring.lock` (if exists)
4. **LLMRing's internal lockfile** (only for `llmring lock chat` - NOT for your app)

**Example:**

```python
from llmring import LLMRing

# Use explicit lockfile
async with LLMRing(lockfile_path="./my-llmring.lock") as service:
    pass

# Or set via environment variable
# export LLMRING_LOCKFILE_PATH=/path/to/llmring.lock

# Or place llmring.lock in current directory (auto-detected)
```

## Lockfile Structure

Lockfiles use TOML format:

```toml
version = "1.0"
default_profile = "default"

[profiles.default]
name = "default"

[[profiles.default.bindings]]
alias = "summarizer"
models = ["openai:gpt-4o-mini"]

[[profiles.default.bindings]]
alias = "analyzer"
models = [
    "anthropic:claude-sonnet-4-5-20250929",   # Primary
    "openai:gpt-4o",                           # Fallback
    "google:gemini-2.5-pro"                    # Second fallback
]

[[profiles.default.bindings]]
alias = "code-reviewer"
models = ["anthropic:claude-sonnet-4-5-20250929"]

[profiles.dev]
name = "dev"

[[profiles.dev.bindings]]
alias = "assistant"
models = ["openai:gpt-4o-mini"]  # Cheaper for development

[profiles.prod]
name = "prod"

[[profiles.prod.bindings]]
alias = "assistant"
models = ["anthropic:claude-sonnet-4-5-20250929"]  # Higher quality for production
```

## CLI Commands

### llmring lock init

Create a new lockfile with registry-based defaults.

```bash
# Create in current directory
llmring lock init

# Overwrite existing
llmring lock init --force

# Create at specific path
llmring lock init --file path/to/llmring.lock
```

**What it does:**
- Fetches recommended models from registry
- Creates default profile with common aliases
- Places lockfile in appropriate location

### llmring bind

Bind an alias to one or more models.

```bash
# Bind to single model
llmring bind fast "openai:gpt-4o-mini"

# Bind with fallbacks
llmring bind balanced "anthropic:claude-sonnet-4-5-20250929,openai:gpt-4o"

# Bind to specific profile
llmring bind assistant "openai:gpt-4o-mini" --profile dev
llmring bind assistant "anthropic:claude-opus-4" --profile prod
```

**Format:**
- Model references: `provider:model`
- Multiple models: comma-separated for fallbacks
- Profile: `--profile name` (defaults to "default")

### llmring aliases

List all configured aliases.

```bash
# List aliases in default profile
llmring aliases

# List aliases in specific profile
llmring aliases --profile dev

# Show with details
llmring aliases --verbose
```

**Output:**
```
fast → openai:gpt-4o-mini
balanced → anthropic:claude-sonnet-4-5-20250929 (+ 2 fallbacks)
deep → anthropic:claude-opus-4
```

### llmring lock chat

Conversational lockfile management with AI advisor.

```bash
# Start interactive chat for lockfile configuration
llmring lock chat
```

**What it does:**
- Natural language interface for configuration
- AI-powered recommendations based on registry
- Explains cost implications and tradeoffs
- Configures aliases with fallback models
- Sets up environment-specific profiles

**Example session:**
```
You: I need a fast, cheap model for development
Advisor: I recommend gpt-4o-mini - it's $0.15/$0.60 per million tokens...
You: Set that as my 'dev' alias
Advisor: Done! Added binding dev → openai:gpt-4o-mini
```

### llmring lock validate

Validate lockfile structure and bindings.

```bash
# Validate lockfile
llmring lock validate

# Validate specific file
llmring lock validate --file path/to/llmring.lock
```

## Python API

### LLMRing with Lockfile

```python
from llmring import LLMRing

# Use lockfile from current directory or bundled default
async with LLMRing() as service:
    pass

# Use specific lockfile
async with LLMRing(lockfile_path="./custom.lock") as service:
    pass
```

### Resolving Aliases

```python
from llmring import LLMRing

async with LLMRing() as service:
    # Resolve alias to concrete model reference
    model_ref = service.resolve_alias("fast")
    print(model_ref)  # "openai:gpt-4o-mini"

    # Resolve with profile
    model_ref = service.resolve_alias("assistant", profile="dev")
    print(model_ref)  # Profile-specific binding
```

### Binding Aliases Programmatically

```python
from llmring import LLMRing

async with LLMRing() as service:
    # Bind alias to model
    service.bind_alias("myalias", "openai:gpt-4o")

    # Bind with profile
    service.bind_alias("assistant", "openai:gpt-4o-mini", profile="dev")
```

### Listing Aliases

```python
from llmring import LLMRing

async with LLMRing() as service:
    # Get all aliases for default profile
    aliases = service.list_aliases()
    for alias, model in aliases.items():
        print(f"{alias} → {model}")

    # Get aliases for specific profile
    aliases = service.list_aliases(profile="dev")
```

### Unbinding Aliases

```python
from llmring import LLMRing

async with LLMRing() as service:
    # Remove alias from default profile
    service.unbind_alias("myalias")

    # Remove alias from specific profile
    service.unbind_alias("assistant", profile="dev")
```

### Initializing Lockfile Programmatically

```python
from llmring import LLMRing

async with LLMRing() as service:
    # Create new lockfile with defaults
    service.init_lockfile()

    # Overwrite existing lockfile
    service.init_lockfile(force=True)
```

### Clearing Alias Cache

Aliases are cached for performance. Clear when updating lockfile:

```python
from llmring import LLMRing

async with LLMRing() as service:
    # Clear all cached aliases
    service.clear_alias_cache()

    # Now fresh lookups from lockfile
    model = service.resolve_alias("fast")
```

## Profiles: Environment-Specific Configuration

Profiles let you use different models in different environments.

### Profile Setup

```toml
# llmring.lock
[profiles.dev]
name = "dev"
[[profiles.dev.bindings]]
alias = "assistant"
models = ["openai:gpt-4o-mini"]  # Cheap

[profiles.staging]
name = "staging"
[[profiles.staging.bindings]]
alias = "assistant"
models = ["anthropic:claude-sonnet-4-5-20250929"]  # Mid-tier

[profiles.prod]
name = "prod"
[[profiles.prod.bindings]]
alias = "assistant"
models = [
    "anthropic:claude-opus-4",    # Best quality
    "anthropic:claude-sonnet-4-5-20250929"  # Fallback
]
```

### Using Profiles

**Via environment variable:**

```bash
# Set profile for entire application
export LLMRING_PROFILE=dev

# Now all requests use 'dev' profile
python my_app.py
```

**Via CLI:**

```bash
# Use specific profile
llmring chat "Hello" --profile dev

# List aliases in profile
llmring aliases --profile prod
```

**In code:**

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    request = LLMRequest(
        model="assistant",
        messages=[Message(role="user", content="Hello")]
    )

    # Use dev profile
    response = await service.chat(request, profile="dev")

    # Use prod profile
    response = await service.chat(request, profile="prod")
```

### Profile Selection Priority

1. **Explicit parameter:** `profile="dev"` or `--profile dev` (highest)
2. **Environment variable:** `LLMRING_PROFILE=dev`
3. **Default:** `default` profile (lowest)

### Common Profile Use Cases

- **dev:** Cheap, fast models for development
- **test:** Local models (Ollama) or mocks
- **staging:** Production-like but with cost savings
- **prod:** Highest quality models
- **a-b-testing:** Different models for the same alias

## Fallback Models

Aliases can specify multiple models for automatic failover.

**Lockfile:**

```toml
[[profiles.default.bindings]]
alias = "balanced"
models = [
    "anthropic:claude-sonnet-4-5-20250929",   # Try first
    "openai:gpt-4o",                  # If first fails
    "google:gemini-2.5-pro"           # If both fail
]
```

**What happens:**

```python
async with LLMRing() as service:
    request = LLMRequest(
        model="assistant",  # Your semantic alias
        messages=[Message(role="user", content="Hello")]
    )

    # Tries anthropic:claude-sonnet-4-5-20250929
    # If rate limited or unavailable → tries openai:gpt-4o
    # If that fails → tries google:gemini-2.5-pro
    response = await service.chat(request)
```

**Use cases:**
- High availability (failover on rate limits)
- Cost optimization (try cheaper first)
- Provider diversity (avoid single vendor lock-in)

## Packaging Lockfiles with Your Application

To ship lockfiles with your Python package:

**Add to `pyproject.toml`:**

```toml
[tool.hatch.build]
include = [
    "src/yourpackage/**/*.py",
    "src/yourpackage/**/*.lock",  # Include lockfiles
]
```

**Or with setuptools, add to `MANIFEST.in`:**

```
include src/yourpackage/*.lock
```

**In your package:**

```
mypackage/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── llmring.lock       # Ship with package
├── pyproject.toml
└── README.md
```

**Users can then override:**

```python
from llmring import LLMRing

# Uses your package's bundled lockfile by default
async with LLMRing() as service:
    pass

# Or override with their own
async with LLMRing(lockfile_path="./my-llmring.lock") as service:
    pass
```

## Using LLMRing in Libraries

If building a library that uses LLMRing, follow this pattern:

**Pattern:**
1. Ship with bundled `llmring.lock`
2. Accept `lockfile_path` parameter for user override
3. Validate required aliases in `__init__`
4. Document required aliases in README

**Simple Library Example:**

```python
from pathlib import Path
from llmring import LLMRing

DEFAULT_LOCKFILE = Path(__file__).parent / "llmring.lock"
REQUIRED_ALIASES = ["summarizer"]

class MyLibrary:
    def __init__(self, lockfile_path=None):
        """Initialize with optional custom lockfile.

        Args:
            lockfile_path: Optional path to custom lockfile.
                          If None, uses library's bundled lockfile.

        Raises:
            ValueError: If lockfile missing required aliases
        """
        lockfile = lockfile_path or DEFAULT_LOCKFILE
        self.ring = LLMRing(lockfile_path=lockfile)

        # Validate required aliases (fail fast with clear error)
        self.ring.require_aliases(REQUIRED_ALIASES, context="my-library")

    def summarize(self, text: str) -> str:
        return self.ring.chat("summarizer", messages=[...]).content
```

**Validation Helpers:**

```python
from llmring import LLMRing

ring = LLMRing(lockfile_path="./my.lock")

# Check if alias exists (returns bool, never raises)
if ring.has_alias("summarizer"):
    response = ring.chat("summarizer", messages=[...])

# Validate required aliases (raises ValueError if missing)
ring.require_aliases(
    ["summarizer", "analyzer"],
    context="my-library"  # Included in error message
)
# Error: "Lockfile missing required aliases for my-library: analyzer.
#         Lockfile path: /path/to/lockfile.lock
#         Please ensure your lockfile defines these aliases."
```

**Library Composition:**

When Library B uses Library A, pass lockfile to both:

```python
class LibraryB:
    def __init__(self, lockfile_path=None):
        lockfile = lockfile_path or DEFAULT_LOCKFILE

        # Pass lockfile to Library A (gives us control)
        self.lib_a = LibraryA(lockfile_path=lockfile)

        # Use same lockfile for our own LLMRing
        self.ring = LLMRing(lockfile_path=lockfile)
        self.ring.require_aliases(REQUIRED_ALIASES, context="library-b")
```

**User Override:**

```python
from my_library import MyLibrary

# Use library defaults
lib = MyLibrary()

# Override with custom lockfile
lib = MyLibrary(lockfile_path="./my-models.lock")
```

**Best Practices:**
- Validate with `require_aliases()` in `__init__`
- Document required aliases clearly
- Pass lockfile down when using other llmring libraries

## Lockfile Composability

Libraries can ship lockfiles that consumers extend and override. This allows libraries to define their required aliases while giving consumers control over which models are used.

### Extending Library Lockfiles

Consumer lockfiles can extend library lockfiles using the `[extends]` section. The `[extends]` section is **optional** - you can always define your own aliases without extending any libraries.

```toml
# Consumer's llmring.lock
version = "1.0"
default_profile = "default"

[extends]
packages = ["libA", "libB"]  # Extend these libraries (optional)

[profiles.default]
name = "default"

# Your own local aliases (always works, with or without extends)
[[profiles.default.bindings]]
alias = "myalias"
models = ["openai:gpt-4o"]

[[profiles.default.bindings]]
alias = "summarizer"
models = ["anthropic:claude-3-5-haiku-20241022"]
```

**Key points:**
- `[extends]` is optional - skip it if you don't need library lockfiles
- You can define your own aliases in `bindings` regardless of extends
- Unqualified aliases (like `summarizer`) only resolve from your local lockfile
- Namespaced aliases (like `libA:summarizer`) resolve from extended libraries
- **Extends are NOT recursive**: If libA's lockfile has its own `[extends]`, those are ignored when resolving `libA:alias`. Resolution only goes one level deep.

When you extend a library, its aliases become available as namespaced aliases.

### Namespaced Aliases

Use `package:alias` format to reference aliases from extended libraries:

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    # Use libA's summarizer alias
    request = LLMRequest(
        model="libA:summarizer",  # Resolves from libA's lockfile
        messages=[Message(role="user", content="Summarize this...")]
    )
    response = await service.chat(request)
```

**Resolution rules:**
- `libA:summarizer` → Checks consumer lockfile for override, then libA's lockfile
- `summarizer` (unqualified) → Consumer lockfile only

### Overriding Library Aliases

Consumers can override library aliases by defining them in their lockfile:

```toml
# Consumer's llmring.lock
version = "1.0"
default_profile = "default"

[extends]
packages = ["libA"]

[profiles.default]
name = "default"

# Override libA's summarizer to use a different model
[[profiles.default.bindings]]
alias = "libA:summarizer"
models = ["openai:gpt-4o-mini"]  # Consumer's choice
```

When the consumer's code (or libA's code) resolves `libA:summarizer`, it uses the consumer's override.

### Validating Extended Lockfiles

Use `llmring lock check` to validate your extends configuration:

```bash
llmring lock check
```

**Output:**
```
Checking lockfile: ./llmring.lock

[extends]
  ✓ libA: found llmring.lock
    Aliases: summarizer, analyzer
  ✓ libB: found llmring.lock
    Aliases: translator
  ✗ libC: package not installed or has no llmring.lock

Warnings:
  ⚠ 'summarizer' defined in both libA and libB
    Use libA:summarizer or libB:summarizer to disambiguate

Local aliases:
  myalias → openai:gpt-4o

Summary: 2/3 packages OK, 3 extended aliases, 1 local aliases
```

**Exit codes:**
- 0: All OK
- 1: Missing packages or lockfiles
- 2: Lockfile parse error

### Library Authors: Supporting Composability

When building a library that uses LLMRing:

**1. Ship a bundled lockfile with your package:**

```
mylib/
├── __init__.py
└── llmring.lock  # Bundled with package
```

**2. Include lockfile in package distribution:**

```toml
# pyproject.toml
[tool.hatch.build]
include = ["src/mylib/**/*.lock"]
```

**3. Use `require_aliases()` to validate at startup:**

```python
from llmring import LLMRing

class MyLibrary:
    def __init__(self):
        self.ring = LLMRing()
        # Validates consumer has required aliases available
        self.ring.require_aliases(["mylib:summarizer"], context="mylib")
```

**4. Document which namespaced aliases your library needs:**

```markdown
## Required Aliases

This library requires:
- `mylib:summarizer` - Used for text summarization

Extend our lockfile in yours:
\`\`\`toml
[extends]
packages = ["mylib"]
\`\`\`
```

### Alias Naming for Libraries

Consider using prefixed names to avoid conflicts:

```toml
# Library lockfile (mylib/llmring.lock)
[[profiles.default.bindings]]
alias = "summarizer"  # Consumers use as mylib:summarizer
models = ["anthropic:claude-3-5-haiku-20241022"]
```

The namespace (`mylib:`) is added automatically when consumers extend your library.

## Common Patterns

### Development vs Production

```bash
# Development: use cheap models
export LLMRING_PROFILE=dev
llmring bind assistant "openai:gpt-4o-mini" --profile dev

# Production: use best models
llmring bind assistant "anthropic:claude-opus-4" --profile prod
```

### Semantic Aliases

```bash
# Meaningful names instead of model IDs
llmring bind summarizer "openai:gpt-4o-mini"
llmring bind analyst "anthropic:claude-sonnet-4-5-20250929"
llmring bind coder "openai:gpt-4o"
```

**Use in code:**

```python
# Clear intent from alias names
summarizer_request = LLMRequest(model="summarizer", ...)
analyst_request = LLMRequest(model="analyst", ...)
coder_request = LLMRequest(model="coder", ...)
```

### Multi-Region Deployments

```toml
[profiles.us-west]
[[profiles.us-west.bindings]]
alias = "assistant"
models = ["openai:gpt-4o"]

[profiles.eu-central]
[[profiles.eu-central.bindings]]
alias = "assistant"
models = ["anthropic:claude-sonnet-4-5-20250929"]  # Better EU availability
```

## Common Mistakes

### Wrong: Hardcoding Model IDs

```python
# DON'T DO THIS - brittle, hard to change
request = LLMRequest(
    model="openai:gpt-4o-mini",
    messages=[...]
)
```

**Right: Use Semantic Aliases**

```python
# DO THIS - flexible, easy to update
request = LLMRequest(
    model="summarizer",  # Semantic name defined in lockfile
    messages=[...]
)
```

### Wrong: No Fallback Models

```toml
# DON'T DO THIS - single point of failure
[[profiles.default.bindings]]
alias = "assistant"
models = ["anthropic:claude-sonnet-4-5-20250929"]
```

**Right: Include Fallbacks**

```toml
# DO THIS - automatic failover
[[profiles.default.bindings]]
alias = "assistant"
models = [
    "anthropic:claude-sonnet-4-5-20250929",
    "openai:gpt-4o",
    "google:gemini-2.5-pro"
]
```

### Wrong: Not Using Profiles

```python
# DON'T DO THIS - same models everywhere
if os.getenv("ENV") == "dev":
    model = "openai:gpt-4o-mini"
else:
    model = "anthropic:claude-opus-4"

request = LLMRequest(model=model, ...)
```

**Right: Use Profiles**

```python
# DO THIS - let lockfile handle it
# export LLMRING_PROFILE=dev  (or prod)
request = LLMRequest(model="assistant", ...)
```

### Wrong: Invalid Model References

```bash
# DON'T DO THIS - wrong format
llmring bind fast "gpt-4o-mini"  # Missing provider!
```

**Right: Provider:Model Format**

```bash
# DO THIS - include provider
llmring bind fast "openai:gpt-4o-mini"
```

## Best Practices

1. **Use semantic aliases:** Names like "fast", "balanced", "analyst" are clearer than model IDs
2. **Configure fallbacks:** Always have backup models for high availability
3. **Use profiles for environments:** Different models for dev/staging/prod
4. **Ship lockfiles with packages:** Include in your package distribution
5. **Use conversational config:** `llmring lock chat` for easy setup
6. **Document aliases:** In your README, explain what each alias is for
7. **Clear cache after updates:** Call `clear_alias_cache()` after lockfile changes

## Error Handling

```python
from llmring import LLMRing
from llmring.exceptions import ModelNotFoundError

async with LLMRing() as service:
    try:
        # Resolve alias
        model_ref = service.resolve_alias("myalias")
    except ModelNotFoundError:
        print("Alias not found in lockfile")

    try:
        # Use alias in request
        request = LLMRequest(model="myalias", messages=[...])
        response = await service.chat(request)
    except ModelNotFoundError:
        print("Could not resolve alias to available model")
```

## Related Skills

- `llmring-chat` - Basic chat using aliases
- `llmring-streaming` - Streaming with aliases
- `llmring-tools` - Tools with aliased models
- `llmring-structured` - Structured output with aliases
- `llmring-providers` - Direct provider access (bypassing aliases)

## Summary

**Lockfiles provide:**
- Semantic aliases (readable, maintainable)
- Automatic failover (high availability)
- Environment-specific configs (dev/staging/prod)
- Centralized model management
- Easy model updates without code changes

**Recommendation:** Always use aliases instead of direct model references for flexibility and maintainability.
