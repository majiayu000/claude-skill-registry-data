---
name: koe-setup
description: Guide users through Koe's initial setup and ongoing configuration, including installation, ASR/LLM credential setup, personalized dictionary generation, system prompt customization, and hotkey configuration.
---

# Koe Setup & Configuration

Guide the user through Koe's initial setup and ongoing configuration. This skill helps with installation, credential setup, personalized dictionary generation, system prompt customization, and hotkey configuration.

## Configuration Files

All config files live in `~/.koe/` and are auto-generated on first launch:

```
~/.koe/
├── config.yaml          # Main configuration (ASR, LLM, feedback, hotkey)
├── dictionary.txt       # User dictionary (hotwords + LLM correction terms)
├── system_prompt.txt    # LLM system prompt (correction rules)
└── user_prompt.txt      # LLM user prompt template (usually no need to change)
```

## Workflow

### Step 1: Check Installation Status

Check if Koe is installed and if `~/.koe/` exists:

```bash
# Check if config directory exists
ls -la ~/.koe/

# Check if Koe.app is installed
ls /Applications/Koe.app 2>/dev/null || mdfind "kGMDItemDisplayName == 'Koe'" -onlyin /Applications -onlyin ~/Applications
```

If not installed, guide the user:

```bash
# Option A: Homebrew (recommended)
brew install koe --cask

# Option B: Download from GitHub Releases
# https://github.com/missuo/koe/releases/latest
```

After installation, launch Koe once to generate default config files, then grant three permissions in System Settings > Privacy & Security:
1. **Microphone** — for audio capture
2. **Accessibility** — for auto-paste (Cmd+V simulation)
3. **Input Monitoring** — for global hotkey detection

### Step 2: Configure ASR Credentials

Koe uses Doubao (豆包) ASR by ByteDance. The user needs Volcengine (火山引擎) credentials.

Ask the user: "Do you already have Volcengine (火山引擎) ASR credentials? If not, I can guide you through getting them."

Guide to get credentials:
1. Go to https://console.volcengine.com/speech/app
2. Create an app, then copy **App ID** (app_key) and **Access Token** (access_key)

Then update `~/.koe/config.yaml`:
```yaml
asr:
  app_key: "<their App ID>"
  access_key: "<their Access Token>"
```

### Step 3: Configure LLM

Koe supports any OpenAI-compatible API for text correction. Ask the user which LLM provider they use.

Common configurations:

```yaml
# OpenAI
llm:
  base_url: "https://api.openai.com/v1"
  api_key: "sk-..."  # or "${OPENAI_API_KEY}"
  model: "gpt-4o-mini"

# Any OpenAI-compatible endpoint
llm:
  base_url: "https://your-provider.com/v1"
  api_key: "..."
  model: "your-model"
```

Recommend fast, cheap models since latency matters for voice input (gpt-4o-mini, deepseek-chat, etc.).

**Important:** The `api_key` field supports environment variable substitution with `${VAR_NAME}` syntax. If the user prefers not to put API keys in plain text config files, suggest using environment variables.

### Step 4: Personalized Dictionary

This is the most impactful customization. Ask the user about their profession and domain:

> "What's your primary work domain? For example: frontend development, backend/DevOps, data science, iOS development, product management, academic research, etc. I'll generate a tailored dictionary for you."

Based on their answer, generate a comprehensive dictionary file at `~/.koe/dictionary.txt`. The dictionary serves two purposes:
1. **ASR hotwords** — improves speech recognition accuracy for these terms
2. **LLM correction context** — the LLM prioritizes these spellings

Guidelines for dictionary generation:
- One term per line, lines starting with `#` are comments
- Include proper capitalization (e.g., `PostgreSQL` not `postgresql`)
- Include brand names, tools, frameworks, libraries relevant to their domain
- Include common abbreviations and acronyms they'd use verbally
- Include team/product-specific terms if the user mentions them
- Group terms by category with comment headers for readability
- Aim for 100-300 terms for a good starting dictionary

Example structure:
```
# Programming Languages
TypeScript
JavaScript
Python
Rust

# Frameworks & Libraries
React
Next.js
Tailwind CSS

# Cloud & Infrastructure
Cloudflare
AWS
Kubernetes
Docker

# Tools
VS Code
GitHub Actions
Terraform

# Domain-Specific Terms
# (add terms specific to user's work)
```

After generating, remind the user they can always add more terms later — it's just a text file.

### Step 5: System Prompt Customization

The default system prompt is tuned for software developers working in mixed Chinese-English. Based on the user's profession, consider adjusting:

Read the current system prompt:
```bash
cat ~/.koe/system_prompt.txt
```

Possible customizations based on profession:
- **Non-technical users**: Remove or simplify the technical term rules, add rules for their domain terminology
- **English-only users**: Remove Chinese-specific rules (spacing, punctuation), focus on English conventions
- **Academic/research**: Add rules for citation terms, paper-specific jargon, LaTeX terms
- **Medical/legal**: Add domain-specific formatting rules

Only modify the system prompt if the user's needs clearly differ from the defaults. The default prompt works well for most developer use cases.

**Important:** The `user_prompt.txt` template usually does not need changes. Only modify it if the user has specific needs for the prompt structure.

### Step 6: Hotkey Configuration

By default, Koe uses the **Fn** key. If the user wants a different trigger key, explain the available options:

```yaml
hotkey:
  # Options: fn | left_option | right_option | left_command | right_command
  trigger_key: "fn"
```

| Option | Key | Notes |
|--------|-----|-------|
| `fn` | Fn/Globe key | Default. Works on all Mac keyboards |
| `left_option` | Left Option | Good alternative if Fn is remapped |
| `right_option` | Right Option | Least likely to conflict with shortcuts |
| `left_command` | Left Command | May conflict with system shortcuts |
| `right_command` | Right Command | Less conflict-prone than left Command |

Changes take effect automatically within ~3 seconds (no restart needed).

### Step 7: Feedback Sounds

If the user wants to disable sound effects:
```yaml
feedback:
  start_sound: false   # Silence on recording start
  stop_sound: false     # Silence on recording stop
  error_sound: true     # Keep error sounds (recommended)
```

## Verification

After setup, guide the user to test:

1. Launch Koe (or it may already be running in the menu bar)
2. Open any text input (Notes, browser, terminal)
3. Press and hold the trigger key, speak a sentence, release
4. Or tap the trigger key once to start, speak, tap again to stop
5. The corrected text should be pasted automatically

If something doesn't work, check:
- Menu bar icon should show Koe is running
- All three permissions are granted in System Settings
- ASR credentials are correct (check `app_key` and `access_key`)
- LLM endpoint is reachable and API key is valid
