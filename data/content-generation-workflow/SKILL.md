---
name: content-generation-workflow
description: 'Automated workflow for generating AI-powered content using agent_codex.py. Handles prompt setup, batch processing, validation, and output management for InsightfulAffiliate and NextGenCopyAI content.'
---

# Content Generation Workflow

This skill provides a structured workflow for generating AI-powered content at scale using the repository's `agent_codex.py` automation tool. It handles the complete content generation pipeline from prompt creation to validated output.

## When to Use This Skill

Use this skill when you need to:
- Generate multiple content pieces from templates
- Automate copywriting tasks for marketing materials
- Batch process content through AI models
- Transform existing content to match brand voice
- Create product descriptions or landing page copy at scale

## Prerequisites

- Python 3.10 or higher installed
- OpenAI API key set in environment (for production runs)
- Git repository in clean state
- Input content prepared in appropriate directory

## Workflow Overview

```
1. Prepare Input → 2. Create Prompt → 3. Test (Echo) → 4. Run (OpenAI) → 
5. Review Output → 6. Validate → 7. Move to Final → 8. Commit
```

## Quick Start Example

```bash
# Test workflow
./scripts/agent_codex.py \
  --prompt ./prompts/your_prompt.txt \
  --input ./copywriting/source \
  --output ./docs/ai_outputs/test \
  --provider echo \
  --dry-run

# Production run
./scripts/agent_codex.py \
  --prompt ./prompts/your_prompt.txt \
  --input ./copywriting/source \
  --output ./docs/ai_outputs/prod \
  --provider openai \
  --model gpt-4o-mini
```

## Common Use Cases

### Generate Product Descriptions
```bash
./scripts/agent_codex.py \
  --prompt ./prompts/generate_product_descriptions.txt \
  --input ./copywriting/product_specs \
  --output ./docs/ai_outputs/product_descriptions \
  --provider openai
```

### Rewrite to Brand Voice
```bash
./scripts/agent_codex.py \
  --prompt ./prompts/rewrite_to_insightful_voice.txt \
  --input ./copywriting/drafts \
  --output ./docs/ai_outputs/branded \
  --provider openai
```

### Generate Landing Page Components
```bash
./scripts/agent_codex.py \
  --prompt ./prompts/generate_landing_components.txt \
  --input ./copywriting/component_outlines \
  --output ./docs/ai_outputs/components \
  --site ./landing_pages \
  --provider openai \
  --include-ext ".html,.css"
```

## Configuration Reference

### Provider Options
- `openai`: OpenAI API (requires `OPENAI_API_KEY` env var)
- `echo`: Test mode (no API calls)

### Model Options
- `gpt-4o-mini`: Cost-effective (recommended)
- `gpt-4o`: Higher quality
- `gpt-4`: Premium quality

### File Options
```bash
--include-ext ".md,.txt,.html,.css,.json"
--exclude-dirs ".git,node_modules,dist,build,docs/ai_outputs"
```

## Best Practices

1. **Always test first** with `--provider echo --dry-run`
2. **Review outputs** before moving to production locations
3. **Use specific prompts** with clear instructions and constraints
4. **Monitor costs** by tracking API usage
5. **Commit separately** generated vs manually edited content

## Troubleshooting

**No files processed**: Check file extensions and directory paths

**API rate limits**: Reduce batch size or add delays

**Poor quality**: Refine prompt with more examples and constraints

**HTML errors**: Add HTML template to prompt or post-process outputs

## Resources

- Script: `scripts/agent_codex.py`
- Prompts: `prompts/`
- Outputs: `docs/ai_outputs/`
- Help: `./scripts/agent_codex.py --help`
