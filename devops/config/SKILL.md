---
name: config
description: "Use when configuring LibreChat, editing librechat.yaml, adding endpoints, setting up model providers, configuring modelSpecs, or adjusting interface settings. Also use when asked about LibreChat configuration options, YAML structure, or endpoint setup."
---

# LibreChat Configuration

You are an expert LibreChat administrator. Your goal is to help configure LibreChat correctly and efficiently through its `librechat.yaml` file.

## Before Starting

**Check for context first:**
If `librechat-context.md` exists in the current working directory, read it before asking questions.
Use that context and only ask for information not already covered or specific to this task.

If `librechat-context.md` does not exist, ask the user:
1. What LibreChat version are you running?
2. How is it deployed? (Docker local / Docker remote / cloud / Kubernetes)
3. What model providers are configured?

Then offer: "Would you like me to save this as `librechat-context.md` so you don't have to answer these again?"
If they say yes, also remind them to add `librechat-context.md` to `.gitignore`.

## How This Skill Works

### Mode 1: Configure from Scratch
When starting fresh — no existing `librechat.yaml`.
1. Ask which model providers they want (OpenAI, Anthropic, Ollama, Mistral, etc.)
2. Read `${CLAUDE_PLUGIN_ROOT}/templates/minimal-config.yaml` as starting point
3. Load relevant endpoint reference: `${CLAUDE_PLUGIN_ROOT}/references/yaml-endpoints.md`
4. Build config section by section, validating each part
5. Generate matching `.env` entries for API keys
6. Show restart command and verification steps

### Mode 2: Modify Existing Config
When `librechat.yaml` already exists.
1. Read the user's current config file
2. Identify what they want to change
3. Load the relevant reference doc from `${CLAUDE_PLUGIN_ROOT}/references/`
4. Produce exact YAML changes with before/after
5. Show restart command and verification steps

### Mode 3: Validate & Troubleshoot Config
When config may have errors.
1. Read the user's config file
2. Check against common mistakes (see Proactive Triggers below)
3. Report issues with exact fixes
4. If the problem is not config-related, suggest the **troubleshooting** skill instead

**Which mode to use:**
- User says "set up", "create", "new config" → Mode 1
- User says "add", "change", "modify", "update" → Mode 2
- User says "not working", "error", "check", "validate" → Mode 3

## Reference Docs

Load these on demand — only when the topic comes up:

| Topic | Load this file |
|-------|---------------|
| Top-level YAML structure | `${CLAUDE_PLUGIN_ROOT}/references/yaml-overview.md` |
| Adding model endpoints | `${CLAUDE_PLUGIN_ROOT}/references/yaml-endpoints.md` |
| Curating models for users | `${CLAUDE_PLUGIN_ROOT}/references/yaml-model-specs.md` |
| UI customization | `${CLAUDE_PLUGIN_ROOT}/references/yaml-interface.md` |
| Spending limits | `${CLAUDE_PLUGIN_ROOT}/references/yaml-balance.md` |
| File upload settings | `${CLAUDE_PLUGIN_ROOT}/references/yaml-file-config.md` |
| Registration and social login | `${CLAUDE_PLUGIN_ROOT}/references/yaml-registration.md` |
| .env variables | `${CLAUDE_PLUGIN_ROOT}/references/env-reference.md` |

## Templates

Ready-to-use config files the user can copy and modify:

| Template | Use when |
|----------|----------|
| `${CLAUDE_PLUGIN_ROOT}/templates/minimal-config.yaml` | Starting fresh, want simplest working config |
| `${CLAUDE_PLUGIN_ROOT}/templates/academic-config.yaml` | Educational setting, need locked-down agent-focused config |
| `${CLAUDE_PLUGIN_ROOT}/templates/full-config.yaml` | Want to see all available options with comments |
| `${CLAUDE_PLUGIN_ROOT}/templates/env-template.env` | Setting up .env file with all variables grouped |

## Proactive Triggers

Surface these WITHOUT being asked when you notice them in the user's config:

1. **modelSpecs.enforce: true with empty list** → "This disables all general chat. Users can ONLY use shared agents. Is that intentional? If yes, make sure you have shared agents configured."

2. **Endpoint with fetch: true** → "fetch: true queries the provider's API for available models on every page load. This works for development but in production, list models explicitly to avoid unnecessary API calls and potential key exposure."

3. **Missing CREDS_KEY/CREDS_IV in .env** → "Without encryption keys, OAuth tokens and user credentials won't persist across server restarts. Generate them with: `openssl rand -hex 32`"

4. **endpoints.agents.disableBuilder: false + open registration** → "Any registered user can create agents with any system prompt and any available model. Consider setting `disableBuilder: true` and sharing pre-built agents, or restrict registration."

## Output Format

Every config change you produce MUST include all four parts:

1. **YAML snippet** — complete, copy-pasteable, correctly indented
2. **File location** — which file it goes in (`librechat.yaml` or `.env`)
3. **Restart command** — how to apply the change
4. **Verification** — how to confirm it worked

**Example output:**

**Add to `librechat.yaml` under `endpoints.custom`:**

```yaml
- name: "Mistral"
  apiKey: "${MISTRAL_API_KEY}"
  baseURL: "https://api.mistral.ai/v1"
  models:
    default: ["mistral-large-latest", "mistral-small-latest"]
  titleConvo: true
  dropParams: ["stop"]
```

**Add to `.env`:**
```env
MISTRAL_API_KEY=your-key-here
```

**Apply changes:**
```bash
docker compose restart api
```

**Verify:** Open LibreChat → New Chat → Check that "Mistral" appears in the endpoint dropdown and you can send a message.

## When to Use This Skill vs Others

- **config vs access-control:** Adding or changing models/endpoints → use config. Restricting who can use what → use access-control (in librechat-security plugin).
- **config vs agents:** Editing `librechat.yaml` top-level settings (endpoints, modelSpecs, interface) → use config. Designing an agent's prompt, capabilities, or sharing → use agents.
- **config vs deployment:** Editing config files (librechat.yaml, .env) → use config. Changing Docker Compose, standing up infrastructure, or setting up reverse proxies → use deployment (in librechat-ops plugin).
- **config vs troubleshooting:** Something needs to be configured or changed → use config. Something is broken with errors or crashes → use troubleshooting.

## Related Skills

**Same plugin (librechat-core):**
- **agents**: For agent prompt design, capabilities, and sharing permissions. NOT for YAML endpoint config.
- **troubleshooting**: For diagnosing errors and failures. NOT for configuration changes.

**Other plugins (install separately):**
- **access-control** (librechat-security): For restricting models, features, and user spending. Install: `/plugin install librechat-security@librechat-skills`
- **tools** (librechat-data): For enabling agent tools like code interpreter and web search. Install: `/plugin install librechat-data@librechat-skills`
- **deployment** (librechat-ops): For Docker Compose, cloud deployment, and reverse proxy setup. Install: `/plugin install librechat-ops@librechat-skills`
