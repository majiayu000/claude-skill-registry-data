---
name: nim
description: >
  Invoke various LLMs (GLM-5, Kimi-k2.5, Llama 3.1, etc.) via NVIDIA NIM API 
  to save main agent tokens and leverage specialized model capabilities.
---

# NVIDIA NIM Skill for OpenClaw

This skill allows OpenClaw to delegate tasks to external models hosted on the NVIDIA NIM platform.

## Setup

1. **Get API Key**: Register at [build.nvidia.com](https://build.nvidia.com) and get your `nvapi-...` key.
2. **Set Environment Variable**:
   ```bash
   export NVIDIA_API_KEY="your_api_key_here"
   ```

## Usage

### Direct Command
```bash
python3 scripts/nim_call.py <model_alias> "<prompt>"
```

### Supported Aliases
- `glm5`: Zhipu AI GLM-5
- `kimi`: Moonshot Kimi-k2.5
- `r1`: DeepSeek R1 (Llama-8B Distill)
- `llama`: Llama 3.1 405B
- `phi`: Microsoft Phi-4

## Integration with CLAUDE.md
Add this to your project's `CLAUDE.md`:
```markdown
- /nim <model> <prompt>: Call NVIDIA NIM models.
```
