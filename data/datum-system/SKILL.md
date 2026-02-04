---
name: datum-system
description: |
  Helps work with the b00t datum system - TOML-based configuration for AI models,
  providers, and services. Datums are stored in ~/.dotfiles/_b00t_/ and specify
  WHICH environment variables are required (not the values). Enables DRY approach
  by centralizing configuration in Rust, exposed to Python via PyO3.
version: 1.0.0
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

## What This Skill Does

The b00t datum system provides declarative TOML-based configuration for AI models, providers, and other services. This skill helps you:

- Create and manage datum files (*.ai.toml, *.ai_model.toml)
- Load datums from Rust via PyO3 bindings (DRY)
- Validate environment variables required by datums
- Discover available models and providers
- Follow b00t pattern: datums specify WHICH env vars, .env contains VALUES

## When It Activates

Activate this skill when you see phrases like:

- "create a datum for [model/provider]"
- "add [model] to the datum system"
- "configure [provider] in b00t"
- "check which environment variables are needed"
- "list available models"
- "validate provider configuration"
- "setup OpenRouter/HuggingFace/Groq/etc in datums"

## Key Concepts

### Datum Types

**Provider Datums** (`~/.dotfiles/_b00t_/*.ai.toml`):
- Define provider metadata (name, type, hint)
- List available models with capabilities and costs
- Specify required environment variables
- Set default configuration values

**Model Datums** (`~/.dotfiles/_b00t_/*.ai_model.toml`):
- Reference a provider
- Specify model-specific parameters
- Define capabilities and access groups
- Set rate limits and context windows

### Environment Pattern

```toml
[env]
# Required: Must be present in .env file
required = ["PROVIDER_API_KEY"]

# Optional: Default values for non-secret configuration
defaults = { PROVIDER_API_BASE = "https://api.provider.com" }
```

**NEVER** store actual API keys in datums - only specify WHICH variables are needed.
Actual values go in `.env` file, loaded via direnv.

## Datum Structure

### Provider Datum Example (`openrouter.ai.toml`)

```toml
[b00t]
name = "openrouter"
type = "ai"
hint = "OpenRouter multi-model gateway - access 200+ models via single API"

[models.qwen-2_5-72b-instruct]
capabilities = "text,chat,code,reasoning,multilingual"
context_length = 32768
cost_per_1k_input_tokens = 0.00035
cost_per_1k_output_tokens = 0.00040
max_tokens = 4096

[models.claude-3-5-sonnet]
capabilities = "text,chat,code,vision,reasoning"
context_length = 200000
cost_per_1k_input_tokens = 0.003
cost_per_1k_output_tokens = 0.015
max_tokens = 8192

[env]
required = ["OPENROUTER_API_KEY"]
defaults = { OPENROUTER_API_BASE = "https://openrouter.ai/api/v1" }
```

### Model Datum Example (`qwen-2.5-72b.ai_model.toml`)

```toml
[b00t]
name = "qwen-2.5-72b"
type = "ai_model"
hint = "Alibaba's Qwen 2.5 72B - strong reasoning and multilingual capabilities"

[ai_model]
provider = "openrouter"
size = "large"
capabilities = ["chat", "code", "reasoning"]
litellm_model = "openrouter/qwen/qwen-2.5-72b-instruct"
api_base = "https://openrouter.ai/api/v1"
api_key_env = "OPENROUTER_API_KEY"
rpm_limit = 60
context_window = 32768
enabled = true
access_groups = ["default"]

[ai_model.parameters]
max_tokens = 4096
temperature = 0.7

[ai_model.metadata]
family = "qwen-2.5"
provider_model_id = "qwen/qwen-2.5-72b-instruct"
cost_per_1k_input = 0.35
cost_per_1k_output = 0.40
```

## Using Datums in Python (DRY Approach)

### Via Pydantic-AI (Recommended)

```python
from b00t_j0b_py import create_pydantic_agent

# Create agent from datum (validates env automatically)
agent = create_pydantic_agent(
    model_datum_name="qwen-2.5-72b",
    system_prompt="You are a helpful assistant"
)

result = await agent.run("What is the capital of France?")
```

### Manual Validation via PyO3

```python
import b00t_py

# Load datum from Rust (DRY - no Python duplication)
datum = b00t_py.load_ai_model_datum("qwen-2.5-72b", "~/.dotfiles/_b00t_")

# Validate environment
validation = b00t_py.check_provider_env("openrouter", "~/.dotfiles/_b00t_")
if not validation["available"]:
    print(f"Missing: {validation['missing_env_vars']}")

# List available providers and models
providers = b00t_py.list_ai_providers("~/.dotfiles/_b00t_")
models = b00t_py.list_ai_models("~/.dotfiles/_b00t_")
```

## Workflow

### Adding a New Provider

1. **Create provider datum** in `~/.dotfiles/_b00t_/provider.ai.toml`
2. **Add models** with capabilities and costs
3. **Specify env requirements** (WHICH keys needed)
4. **Update .env.example** in b00t-j0b-py with commented key
5. **Test validation** via PyO3 bindings

### Adding a New Model

1. **Create model datum** in `~/.dotfiles/_b00t_/model-name.ai_model.toml`
2. **Reference provider** and specify litellm_model string
3. **Set capabilities** and access groups
4. **Define parameters** (temperature, max_tokens, etc.)
5. **Add metadata** (costs, family, etc.)

### Validating Configuration

```bash
# Via Python
python3 -c "import b00t_py; print(b00t_py.list_ai_providers('~/.dotfiles/_b00t_'))"

# Check specific provider
python3 -c "import b00t_py; print(b00t_py.check_provider_env('openrouter', '~/.dotfiles/_b00t_'))"
```

## DRY Philosophy

**ALWAYS:**
- ✅ Use PyO3 bindings to access Rust datum parsing
- ✅ Store configuration in TOML datums
- ✅ Specify WHICH env vars are required in datums
- ✅ Store actual API key VALUES in .env (loaded via direnv)

**NEVER:**
- ❌ Duplicate datum parsing logic in Python
- ❌ Store API keys or secrets in datum files
- ❌ Hard-code model configurations in Python
- ❌ Create provider-specific Python classes (use datums instead)

## File Locations

- **Datums**: `~/.dotfiles/_b00t_/*.ai.toml` and `~/.dotfiles/_b00t_/*.ai_model.toml`
- **PyO3 bindings**: `b00t-py/src/lib.rs` (Rust functions exposed to Python)
- **Python integration**: `b00t-j0b-py/src/b00t_j0b_py/pydantic_ai_integration.py`
- **Environment values**: `.env` (gitignored, loaded via direnv)
- **Environment template**: `b00t-j0b-py/.env.example`

## Examples

### Create OpenRouter Provider Datum

```toml
[b00t]
name = "openrouter"
type = "ai"
hint = "OpenRouter multi-model gateway"

[models.qwen-2_5-72b-instruct]
capabilities = "text,chat,code"
cost_per_1k_input_tokens = 0.00035

[env]
required = ["OPENROUTER_API_KEY"]
defaults = { OPENROUTER_API_BASE = "https://openrouter.ai/api/v1" }
```

### Create Model Datum

```toml
[b00t]
name = "my-model"
type = "ai_model"

[ai_model]
provider = "openrouter"
litellm_model = "openrouter/qwen/qwen-2.5-72b-instruct"
api_key_env = "OPENROUTER_API_KEY"
```

## Troubleshooting

**"Missing environment variable"**
- Check `.env` file has the key
- Run `direnv allow` to load environment
- Verify datum specifies correct key name in `env.required`

**"Provider not found"**
- Ensure `~/.dotfiles/_b00t_/provider.ai.toml` exists
- Check file has correct `[b00t]` section with `type = "ai"`

**"Model not found"**
- Verify `~/.dotfiles/_b00t_/model.ai_model.toml` exists
- Check `[ai_model]` section has `provider` field matching existing provider datum

## Related Skills

- **direnv-pattern**: Setting up .env and .envrc files
- **dry-philosophy**: Avoiding code duplication via PyO3
- **justfile-usage**: Adding datum commands to justfile

## References

- `docs/ENVIRONMENT_SETUP.md` - Environment variable pattern
- `docs/PYDANTIC_AI_ANALYSIS.md` - Pydantic-AI integration
- `b00t-c0re-lib/src/datum_ai_model.rs` - Rust datum implementation
- `b00t-py/src/lib.rs` - PyO3 bindings
