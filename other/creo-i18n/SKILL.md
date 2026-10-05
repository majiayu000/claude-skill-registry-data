---
name: creo-i18n
description: >
  Batch translate JSON locale files to 39+ languages using LM Studio (local LLM).
  Structure-preserving translation with validation. Requires i18n-translator extension.
  Triggers on: /creo i18n, translate, localize, i18n, internationalization.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# i18n Translator Skill

Batch translate JSON locale files using a local LLM via LM Studio. Preserves JSON structure, placeholders, and validates output.

## Commands

| Command | Description |
|---------|-------------|
| `/creo i18n translate <source-lang> <target-langs>` | Translate JSON files from source language to one or more target languages (comma-separated) |
| `/creo i18n validate` | Validate that translated files match source structure |
| `/creo i18n status` | Show translation status: which languages are done, which have issues |

### Examples

```
/creo i18n translate en uk,pl,de
/creo i18n translate en fr
/creo i18n validate
/creo i18n status
```

## Prerequisites

- **Python 3.8+** with `requests` package
- **LM Studio** running locally on port 1234 (default) with a loaded model
- Source JSON locale files in the `input/` directory

## Supported Languages (39+)

| Code | Language | Code | Language | Code | Language |
|------|----------|------|----------|------|----------|
| ar | Arabic | bg | Bulgarian | cs | Czech |
| da | Danish | de | German | el | Greek |
| en | English | es | Spanish | et | Estonian |
| fi | Finnish | fr | French | he | Hebrew |
| hi | Hindi | hr | Croatian | hu | Hungarian |
| id | Indonesian | it | Italian | ja | Japanese |
| ko | Korean | lt | Lithuanian | lv | Latvian |
| ms | Malay | nl | Dutch | no | Norwegian |
| pl | Polish | pt | Portuguese | ro | Romanian |
| ru | Russian | sk | Slovak | sl | Slovenian |
| sr | Serbian | sv | Swedish | th | Thai |
| tr | Turkish | ua | Ukrainian | vi | Vietnamese |
| zh | Chinese (Simplified) | zh-TW | Chinese (Traditional) | fil | Filipino |

You can specify any language code supported by your LLM model.

## How It Works

1. **Source files**: Place JSON locale files in the `input/` directory
2. **Configure**: Edit `config.json` to set source language, target languages, and LM Studio URL
3. **Translate**: The translator walks each JSON file recursively, sending each string value to the LLM with context (the JSON key path)
4. **Validate**: After translation, the validator checks that every translated file has the exact same structure as the source
5. **Output**: Translated files are saved to `output/<lang>/` preserving the original directory structure

## Quality Checks

- **Placeholder preservation**: All `{variable}` placeholders are verified and restored if the LLM renames or removes them
- **Arrow artifact removal**: Common LLM artifacts like `"text -> translation"` are automatically cleaned
- **Multi-line response handling**: If the LLM returns multiple lines, the best one (closest in length to the original) is selected
- **Quote stripping**: Spurious wrapping quotes are removed
- **Structure validation**: Post-translation validation ensures every key exists and types match
- **Incremental translation**: Only changed values are re-translated; existing translations are preserved

## Workflow

### Quick Start

```bash
# 1. Ensure LM Studio is running with a model loaded on port 1234

# 2. Set up your project
mkdir -p input
cp path/to/your/en/*.json input/

# 3. Edit config.json to list target languages
# 4. Run translation
python3 scripts/run_translation.py
```

### Configuration

Edit `config.json`:

```json
{
    "source_language": "en",
    "target_languages": ["uk", "pl", "de", "fr"],
    "lm_studio_url": "http://localhost:1234",
    "model": "local-model",
    "temperature": 0.2,
    "request_delay": 1.0,
    "max_retries": 3
}
```

Create a `config_local.json` to override settings without modifying the shared config.

### Agent Integration

When invoked via `/creo i18n translate`, the agent will:

1. Check that LM Studio is reachable
2. Locate or create the config.json with requested languages
3. Run the translation scripts
4. Validate the output
5. Report results with any issues found

## File Structure

```
extensions/i18n-translator/
  config.json          # Translation configuration
  requirements.txt     # Python dependencies
  scripts/
    translator.py      # Core translation engine
    run_translation.py # Orchestrator (translate + validate)
    validator.py       # Structure validation
  skills/
    creo-i18n/
      SKILL.md         # This file
  agents/
    creo-i18n.md       # Subagent definition
```
