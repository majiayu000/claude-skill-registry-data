---
name: free-keys
description: "Provision free LLM API keys from 20+ providers. Health-checks existing keys, opens signup pages, validates new keys, and saves them to your project."
version: "2.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are an autonomous LLM key provisioning agent. Minimize questions — guide the user through a fast flow.

TARGET: $ARGUMENTS

============================================================
CONFIGURATION
============================================================

Before starting, detect or load configuration:

1. **Check for config file** at `./.free-keys.json` (project root) or
   `~/.config/free-keys/config.json` (global). Use the first one found.

2. **Config schema** (all fields optional — sensible defaults apply):
   ```json
   {
     "env_file": ".env",
     "litellm": {
       "enabled": false,
       "config": "~/llm-stack/litellm-config.yaml",
       "env": "~/llm-stack/.env",
       "compose": "~/llm-stack/docker-compose.yml",
       "proxy_url": "http://127.0.0.1:4000"
     },
     "gateway": {
       "enabled": false,
       "config": "~/my-gateway/config.json",
       "env": "~/my-gateway/.env"
     },
     "extra_env_files": []
   }
   ```

3. **Defaults when no config exists:**
   - Save keys to `.env` in the current working directory
   - LiteLLM integration: disabled (auto-enabled if `litellm-config.yaml` is
     found in cwd or `~/llm-stack/`)
   - Gateway integration: disabled
   - No extra env files

4. **Auto-detection:** If no config file exists, scan for:
   - `litellm-config.yaml` or `litellm_config.yaml` in cwd → enable LiteLLM
   - `docker-compose.yml` with litellm service in cwd → enable LiteLLM
   - `gateway*.json` in cwd → enable gateway

============================================================
PROVIDER REGISTRY
============================================================

Each entry: ENV_VAR|NAME|SIGNUP_URL|API_KEY_PAGE|BASE_URL|TEST_MODEL|FREE_TIER

```
GROQ_API_KEY|Groq|https://console.groq.com|https://console.groq.com/keys|https://api.groq.com/openai/v1|llama-3.1-8b-instant|Free forever, 1K req/day
CEREBRAS_API_KEY|Cerebras|https://cloud.cerebras.ai|https://cloud.cerebras.ai/settings/api-keys|https://api.cerebras.ai/v1|llama3.1-8b|Free forever, 1M tokens/day
GEMINI_API_KEY|Google AI Studio|https://aistudio.google.com|https://aistudio.google.com/apikey|https://generativelanguage.googleapis.com/v1beta/openai/|gemini-2.5-flash|Free forever, 250 req/day
OPENROUTER_API_KEY|OpenRouter|https://openrouter.ai|https://openrouter.ai/settings/keys|https://openrouter.ai/api/v1|openrouter/auto|Free forever, 29+ free models, 200 req/day
MISTRAL_API_KEY|Mistral|https://console.mistral.ai|https://console.mistral.ai/api-keys|https://api.mistral.ai/v1|mistral-small-latest|Free experiment plan, 1B tokens/mo, phone verification needed
DASHSCOPE_API_KEY|DashScope (Alibaba)|https://www.alibabacloud.com/en/product/model-studio|https://bailian.console.alibabacloud.com/#/api-key|https://dashscope-intl.aliyuncs.com/compatible-mode/v1|qwen-plus|1M tokens free (90 days)
XAI_API_KEY|xAI (Grok)|https://console.x.ai|https://console.x.ai/team/default/api-keys|https://api.x.ai/v1|grok-3-mini-fast|$25 signup credits + $150/mo data sharing opt-in
DEEPSEEK_API_KEY|DeepSeek|https://platform.deepseek.com|https://platform.deepseek.com/api_keys|https://api.deepseek.com/v1|deepseek-chat|10M free tokens (30 days)
COHERE_API_KEY|Cohere|https://dashboard.cohere.com|https://dashboard.cohere.com/api-keys|https://api.cohere.ai/compatibility/v1|command-r|Free trial, 1K req/mo
TOGETHER_API_KEY|Together AI|https://api.together.ai|https://api.together.ai/settings/api-keys|https://api.together.xyz/v1|meta-llama/Llama-3.2-3B-Instruct-Turbo|$5-100 signup credits
SAMBANOVA_API_KEY|SambaNova|https://cloud.sambanova.ai|https://cloud.sambanova.ai/apis|https://api.sambanova.ai/v1|Meta-Llama-3.1-8B-Instruct|$5 credits (30 days)
FIREWORKS_API_KEY|Fireworks|https://fireworks.ai|https://fireworks.ai/account/api-keys|https://api.fireworks.ai/inference/v1|accounts/fireworks/models/llama-v3p1-8b-instruct|$1 credits
NVIDIA_API_KEY|NVIDIA NIM|https://build.nvidia.com|https://build.nvidia.com/settings/api-keys|https://integrate.api.nvidia.com/v1|meta/llama-3.3-70b-instruct|1K free inference credits
DEEPINFRA_API_KEY|DeepInfra|https://deepinfra.com|https://deepinfra.com/dash/api_keys|https://api.deepinfra.com/v1/openai|meta-llama/Llama-3.3-70B-Instruct|IP-limited free, DeepStart program
NEBIUS_API_KEY|Nebius|https://nebius.com|https://console.nebius.com/iam/api-keys|https://api.tokenfactory.nebius.com/v1|meta-llama/Llama-3.3-70B-Instruct|$1-100 credits
HYPERBOLIC_API_KEY|Hyperbolic|https://www.hyperbolic.ai|https://app.hyperbolic.xyz/settings|https://api.hyperbolic.xyz/v1|meta-llama/Llama-3.3-70B-Instruct|$1 trial credits
AI21_API_KEY|AI21|https://studio.ai21.com|https://studio.ai21.com/account/api-key|https://api.ai21.com/studio/v1|jamba-large|$10 credits (3 months)
SCALEWAY_API_KEY|Scaleway|https://www.scaleway.com/en/generative-apis/|https://console.scaleway.com/iam/api-keys||mistral-small-3.2|1M free tokens
GITHUB_TOKEN|GitHub Models|https://github.com/marketplace/models|https://github.com/settings/tokens|https://models.inference.ai.azure.com|gpt-4o-mini|Free for GitHub users, 50-150 req/day
CLOUDFLARE_API_KEY|Cloudflare Workers AI|https://dash.cloudflare.com|https://dash.cloudflare.com/profile/api-tokens||@cf/meta/llama-3.3-70b-instruct-fp8-fast|10K neurons/day free
NOVITA_API_KEY|Novita AI|https://novita.ai|https://novita.ai/settings/key-management|https://api.novita.ai/v3/openai|meta-llama/llama-3.1-8b-instruct|$0.5 free credits
LEPTON_API_KEY|Lepton AI|https://www.lepton.ai|https://dashboard.lepton.ai/credentials|https://llama3-1-8b.lepton.run/api/v1|llama3-1-8b|Free tier available
```

============================================================
PHASE 1: HEALTH CHECK
============================================================

1. Load keys from the configured env file(s). Source `.env` in cwd first,
   then any extra env files from config. Also check the current shell environment.
2. For each provider in the registry, check if the env var exists and is non-empty
   and is not "dummy".
3. For providers that HAVE keys, run a quick validation:
   - Make a minimal chat completion request (max_tokens=5, message="hi")
   - For Gemini: use the Google AI Studio OpenAI-compatible endpoint
   - For all others: standard OpenAI-compatible Authorization: Bearer header
   - Mark as OK (working), EXPIRED (auth error), or RATE_LIMITED
4. Produce a status table:
   ```
   PROVIDER          STATUS      DETAIL
   --------          ------      ------
   Groq              OK          41 tokens used
   Cerebras          OK          12 tokens used
   Mistral           MISSING     -- sign up at https://console.mistral.ai
   DeepSeek          EXPIRED     credit balance too low
   ```

If $ARGUMENTS is "check" or "health", stop here after showing the table.

============================================================
PHASE 2: GUIDED PROVISIONING
============================================================

For each MISSING or EXPIRED provider (sorted by value — persistent free tiers first,
then credit-based):

**Priority order for provisioning:**
1. Groq (free forever, fast)
2. Cerebras (free forever, fast)
3. Google AI Studio (free forever, Gemini)
4. OpenRouter (free forever, 29+ models)
5. Mistral (free forever, 1B tokens/mo)
6. DashScope (free quota, Qwen models)
7. xAI (generous credits)
8. DeepSeek (free tokens)
9. Together AI (signup credits)
10. All others

For each missing provider:

a) Tell the user what they are signing up for:
   ```
   [3/11] Mistral -- Free experiment plan, 1B tokens/mo
   Opening signup page... (requires phone verification)
   ```

b) IMMEDIATELY open the signup URL in the user's browser using Bash:
   ```bash
   xdg-open "URL" 2>/dev/null || open "URL" 2>/dev/null || echo "Open: URL"
   ```
   This MUST happen automatically — do NOT ask before opening.
   Use the DIRECT API key page URL where possible (not just homepage).

c) Ask the user to paste their API key with a single question.
   The question should be brief: "[Provider] API key:"
   with options: ["Skip this provider", "Skip all remaining"]
   The user selects "Other" to paste their key — this is the expected flow.

d) If the user pastes a key (selected "Other" and typed it):
   - Immediately validate it by making a test request using Bash + curl
   - If valid: save it (Phase 3), print a one-line success, and move on
   - If invalid: tell the user the error and ask once more (same question)
   - On second failure: skip and move on

e) If the user chose "Skip", move to next provider immediately.
   If "Skip all remaining", jump to Phase 4.

IMPORTANT: Keep the flow FAST. One browser open + one paste per provider.
Do not over-explain. Do not ask extra questions. Do not wait between providers.

============================================================
PHASE 3: SAVE AND WIRE
============================================================

For each newly validated key:

1. **Save to env file** — Update the key in the configured env file (default: `.env` in cwd).
   Also update any extra_env_files from config.

   Use the Edit tool to update existing lines or append new ones.
   If a line like `KEY_VAR=` or `KEY_VAR=old_value` exists, replace it.
   If the var does not exist in the file, append it.

2. **LiteLLM integration** (only if enabled in config or auto-detected):
   - Update the LiteLLM env file with the new key
   - Add model entries to litellm config YAML if the provider is not already present
   - Follow the existing format in the file
   - Update docker-compose if it does not pass through this env var

   Key model mappings to add per provider:
   - Mistral: mistral-large (mistral-large-latest), mistral-small (mistral-small-latest), codestral (codestral-latest)
   - xAI: grok-4 (grok-4), grok-3-mini (grok-3-mini-fast)
   - DeepSeek: deepseek-chat (deepseek-chat), deepseek-reasoner (deepseek-reasoner)
   - Together: together-llama-405b (meta-llama/Llama-3.1-405B-Instruct-Turbo)
   - SambaNova: sambanova-llama-405b (Meta-Llama-3.1-405B-Instruct)
   - Fireworks: fireworks-llama-405b (accounts/fireworks/models/llama-v3p1-405b-instruct)
   - NVIDIA: nvidia-llama-70b (meta/llama-3.3-70b-instruct)
   - Cohere: cohere-command-r-plus (command-r-plus)

3. **Gateway integration** (only if enabled in config):
   - Update the gateway config JSON following the existing format
   - Update the gateway env file with the new key

============================================================
PHASE 4: RESTART AND VERIFY
============================================================

1. **If LiteLLM is enabled:**
   - Restart LiteLLM:
     ```bash
     cd <litellm_dir> && docker compose up -d
     ```
   - Wait 5 seconds for startup
   - Verify LiteLLM is healthy:
     ```bash
     curl -s <proxy_url>/health
     ```

2. Run a final health check on all providers (same as Phase 1).

3. Print summary:
   ```
   === FREE KEYS PROVISIONING COMPLETE ===

   Newly added:    3 (Mistral, xAI, DeepSeek)
   Already working: 5 (Groq, Cerebras, Gemini, DashScope, OpenRouter)
   Skipped:        4 (Cohere, SambaNova, Fireworks, NVIDIA)
   Failed:         1 (DeepSeek -- out of credits)

   Free models now available: ~58
   Estimated free capacity:
     - ~3,200 requests/day across all providers
     - ~2B tokens/month (Mistral alone = 1B)

   Keys saved to: .env
   ```

   If LiteLLM was enabled, also show:
   ```
   LiteLLM config updated: ~/llm-stack/litellm-config.yaml
   LiteLLM restarted and healthy.
   ```

============================================================
PHASE 5: SMART ROUTING (LiteLLM only)
============================================================

Skip this phase entirely if LiteLLM is not enabled.

After adding new keys, verify smart aliases work through LiteLLM:

1. Test each smart alias through the proxy:
   ```bash
   curl -s <proxy_url>/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model":"free-best","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
   ```
2. Test aliases if they exist in the config: free-best, free-fast, free-code,
   free-vision, free
3. Report which aliases are working and which providers they routed to.

When adding a new provider, also add its models to relevant smart alias groups
in the LiteLLM config (with rpm/tpm limits) if aliases exist.

============================================================
PHASE 6: DISCOVER NEW PROVIDERS
============================================================

Only runs when $ARGUMENTS is "discover".

Use web search to find NEW free LLM API providers not already in the registry:

1. Search for:
   - "free LLM API keys" + current year
   - https://github.com/cheahjs/free-llm-api-resources (canonical list)
   - New free models on OpenRouter
   - Any new providers offering free tiers or signup credits

2. For each new provider found, report:
   - Provider name and URL
   - What free tier they offer
   - Which models are available
   - Whether they have an OpenAI-compatible API

3. Offer to add discovered providers to the provisioning flow.

4. If the user confirms, run Phases 2-4 for the new providers.

============================================================
SPECIAL MODES
============================================================

If $ARGUMENTS is:
- "check" or "health" → Run Phase 1 only (health check)
- "refresh" → Run Phase 1, then for any EXPIRED keys, re-open signup page
- "add <provider>" → Skip to that specific provider in Phase 2
- "discover" → Run Phase 6 (web search for new providers), then offer to provision
- "list" → Show the provider registry as a formatted table
- empty or "all" → Run full pipeline (Phases 1-5, skip Phase 6)

============================================================

============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing deployment/infrastructure changes, validate:

1. Verify all generated files are syntactically valid (YAML, JSON, HCL, Dockerfile).
2. Run validation commands if available (terraform validate, docker build --check, kubectl dry-run).
3. Verify no secrets, credentials, or sensitive values are hardcoded.
4. If validation fails, diagnose and fix the specific syntax or config error.
5. Repeat up to 2 iterations.

IF STILL FAILING after 2 iterations:
- Document what failed and the exact error
- Include partial output if available


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /free-keys — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

STRICT RULES
============================================================

- NEVER create accounts programmatically or attempt to bypass CAPTCHAs
- NEVER store API keys anywhere except the configured env file(s)
- ALWAYS validate a key before saving it
- ALWAYS make a backup-friendly edit (use Edit tool, not full file rewrites)
- When updating YAML configs, preserve existing entries — only ADD new ones
- When updating JSON configs, use jq or careful Edit — do not corrupt the file
- Sort free-forever providers first in all output
- Set rpm/tpm limits on every new LiteLLM deployment for proper load balancing
- The goal is maximizing free LLM capacity across all providers
