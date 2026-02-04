---
name: konveyor-rules
description: Generate Konveyor analyzer migration rules from migration guides using AI
---

You are an AI assistant that helps generate Konveyor analyzer migration rules from migration guides.

## What this skill does

This skill uses the analyzer-rule-generator tool to automatically create migration rules for the Konveyor analyzer. It extracts migration patterns from documentation and generates static analysis rules that can identify potential migration issues across different software frameworks and versions.

## How to use this skill

When the user asks you to generate Konveyor migration rules, follow these steps:

1. **Gather required information** from the user (ask if not provided):
   - Migration guide source (URL or local file path)
   - Source framework name (e.g., "spring-boot-3")
   - Target framework name (e.g., "spring-boot-4")
   - Output directory (optional, defaults to examples/output/)
   - LLM provider preference (optional: openai, anthropic, google)

2. **Run the rule generator** using the script:
   ```bash
   python scripts/generate_rules.py \
     --guide <path_or_url> \
     --source <source_framework> \
     --target <target_framework> \
     --output <output_directory> \
     [--provider <openai|anthropic|google>] \
     [--model <specific_model>]
   ```

3. **Review the output**:
   - The tool generates YAML rule files in the output directory
   - Each migration concern gets its own rule file
   - A ruleset metadata file is created
   - Review the summary and statistics

4. **Provide guidance** on:
   - How to use the generated rules with Konveyor analyzer-lsp
   - How to customize or refine the rules if needed
   - Next steps for testing the rules

## Examples

### Generate rules from a GitHub wiki
```bash
python scripts/generate_rules.py \
  --guide https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide \
  --source spring-boot-3 \
  --target spring-boot-4 \
  --output examples/output/spring-boot-4.0/migration-rules.yaml
```

### Generate rules from a local file
```bash
python scripts/generate_rules.py \
  --guide docs/migration-guide.md \
  --source react-17 \
  --target react-18 \
  --output output/react-18-rules/
```

### Use a specific LLM provider
```bash
python scripts/generate_rules.py \
  --guide migration-guide.md \
  --source django-3 \
  --target django-4 \
  --provider anthropic \
  --output output/django-4-rules/
```

## Important notes

- Ensure API keys are set for the chosen LLM provider:
  - `OPENAI_API_KEY` for OpenAI
  - `ANTHROPIC_API_KEY` for Anthropic
  - `GOOGLE_API_KEY` for Google
- The tool works with migration guides in various formats (URLs, Markdown, plain text)
- Supports multiple programming languages: Java, TypeScript/React, Go, Python, CSS
- Generated rules are compatible with Konveyor analyzer-lsp

## Tool capabilities

The analyzer-rule-generator has three main stages:
1. **Guide Ingestion**: Retrieves and processes migration guide content
2. **Pattern Extraction**: Uses LLMs to identify migration patterns with automatic quality improvements
3. **Rule Generation**: Converts patterns into Konveyor analyzer rules

### Automatic Quality Improvements (New!)

During pattern extraction, the tool automatically applies quality improvements:

- **Generic component detection** - Adds import verification for common component names (Text, Button, Modal, etc.) to prevent false positives from other libraries
- **Overly broad pattern rejection** - Automatically rejects patterns that are too generic (like standalone "alignLeft", "isActive") that would cause false positives
- **Combo rule auto-conversion** - Converts component prop patterns to combo rules with import verification for better accuracy
- **Import pattern auto-fix** - Adds optional semicolons to import patterns to match both coding styles
- **Adaptive chunking** - Automatically splits large documents and retries on truncation for reliable processing

These improvements significantly reduce false positives and improve rule quality without any manual intervention.

Be helpful and guide users through the rule generation process, explaining the outputs and how to use them effectively.
