---
name: litellm-proxy-security
description: Review a LiteLLM proxy deployment for API key leakage through the proxy layer, model routing abuse, budget enforcement bypass, insecure master key configuration, and database credential exposure in the proxy config file.
last_reviewed: 2026-04-29
---

# LiteLLM Proxy Security

## First Principle

**The LiteLLM proxy is a key aggregator. Every upstream API key you configure in it is available to every client authorized to use the proxy — unless you explicitly scope virtual keys. A single compromised virtual key can exhaust your upstream budget across every configured provider.**

LiteLLM centralizes access to multiple LLM providers behind a single proxy endpoint. That centralization is its value proposition and its risk concentration point. The proxy config YAML contains plaintext API keys for every upstream provider. The proxy's virtual key system is the only thing preventing a client with one key from spending across all configured models. Budget limits are enforced in the proxy's database — and that database must be protected from direct access.

## Attack Mental Model

1. **Config file key leakage** — the `config.yaml` or environment variables containing upstream provider API keys are exposed via misconfigured container mounts, Git commits, or verbose error responses.
2. **Virtual key scope abuse** — a LiteLLM virtual key grants access to whichever models the key owner is permitted to use. If model allowlists are not enforced per key, a key issued for one model can be used to route requests to any configured model.
3. **Budget database tampering** — LiteLLM stores budget and spend data in PostgreSQL or SQLite. Direct database access allows an attacker to reset spend counters, increase budget limits, or forge audit logs.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Virtual keys are issued with explicit model allowlists, budget ceilings, and expiry times. Keys without these constraints are not valid. |
| **Scope** | Upstream provider keys are read from environment variables or a secrets manager at runtime — never committed to `config.yaml` in version control. |
| **Isolate** | The proxy database is accessible only from the proxy process — not from application services or developer workstations directly. |
| **Enforce** | Budget limits and model restrictions are enforced in the proxy, not in application code. Application code cannot override proxy-layer controls by manipulating request parameters. |

## LPS.1 API Key Management and Config Hardening

**The core vulnerability:** LiteLLM's `config.yaml` supports inline `api_key` fields for each model entry. Teams new to the proxy copy examples from documentation that include placeholder keys — then fill in real keys without noticing the file is going into Git or a container image layer.

### Check

- Does `config.yaml` contain any `api_key` fields with literal key values — or do all keys reference environment variables (`os.environ/PROVIDER_API_KEY`)?
- Is `config.yaml` listed in `.gitignore` — and does `git log --all -p -- config.yaml` show no historical commit that included a real key?
- Is the LiteLLM master key (`LITELLM_MASTER_KEY`) a strong random secret — not the default `sk-1234` or any value from documentation?
- Are upstream provider keys rotated on a schedule, and is rotation tested against the proxy before old keys are retired?

### Action

- **Use environment variable references for all upstream keys.** Never put literal key values in `config.yaml`:

```yaml
# config.yaml — correct
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY  # resolved at runtime
```

- **Store secrets in a secrets manager.** In Kubernetes, use a `Secret` object projected as environment variables into the proxy pod. In bare-metal deployments, use Vault or AWS Secrets Manager with a sidecar injector.
- **Set a strong master key.** `LITELLM_MASTER_KEY` must be a randomly generated 32+ byte secret. Rotate it on a defined schedule. Invalidate all virtual keys when the master key rotates.
- **Verify no keys in Git history.** Run `git log --all --full-history -p | grep -i "api_key\|sk-"` to check for historical leakage. If found, rotate affected keys immediately and rewrite history or archive the repository.

### Failure Modes

- A developer adds `api_key: sk-real-openai-key` to `config.yaml` and commits it to a public GitHub repo. The key is scraped within minutes.
- The proxy container image is built with `config.yaml` COPY'd in. Anyone who can pull the image (`docker history`, layer inspection) can extract the keys.
- `LITELLM_MASTER_KEY=sk-1234` is left from the quickstart docs. Any client that guesses the master key has admin access to the proxy.

## LPS.2 Virtual Key Scoping and Budget Enforcement

**The core vulnerability:** LiteLLM virtual keys are powerful: they control which models a client can access, what budget they can spend, and when they expire. If keys are issued without model restrictions, any client can route to any configured upstream — including expensive models or providers not intended for that client.

### Check

- Are all virtual keys issued with an explicit `models` field limiting them to authorized model names?
- Are per-key budget limits (`max_budget`) set — and is there a global fallback budget that prevents any single key from exhausting the full upstream allowance?
- Do virtual key responses include an expiry time (`expires`) — or are keys issued with indefinite validity?
- Is the `/key/generate` admin endpoint protected so only authorized administrators can issue new keys?

### Action

- **Issue all virtual keys with model restrictions and budget ceilings:**

```python
import requests

response = requests.post(
    "http://litellm-proxy:4000/key/generate",
    headers={"Authorization": f"Bearer {LITELLM_MASTER_KEY}"},
    json={
        "models": ["gpt-4o-mini", "claude-haiku-4-5"],  # explicit allowlist
        "max_budget": 5.00,          # USD ceiling
        "budget_duration": "30d",    # resets monthly
        "expires": "2026-05-29",     # hard expiry
        "metadata": {"issued_to": "service-x", "purpose": "summarization"},
    }
)
```

- **Restrict the `/key/generate` and `/key/delete` endpoints.** Only the master key should be able to call these endpoints. Verify this with a test: attempt to call `/key/generate` with a regular virtual key and confirm it returns `403`.
- **Enable spend tracking and alerting.** Configure `LITELLM_LOG=DEBUG` in non-production and set spend alert thresholds. Route spend events to your observability stack.

### Minimum Deliverable Per Review

- [ ] Config key audit: zero literal key values in `config.yaml`, all using `os.environ/` references
- [ ] Git history check: no upstream keys in any commit on any branch
- [ ] Master key strength: length, randomness, and rotation schedule
- [ ] Virtual key policy: model restriction, budget ceiling, and expiry required for all issued keys
- [ ] Admin endpoint protection: `/key/generate` and `/key/delete` require master key
- [ ] Database access control: proxy DB not reachable from application services directly

## Quick Win

**Scan `config.yaml` for literal `api_key` values right now:** `grep -n "api_key:" config.yaml | grep -v "os.environ"`. Any line that prints has a key that needs to move to an environment variable before your next deployment.

## References

- Local model backends behind LiteLLM → [ollama-security/SKILL.md](../ollama-security/SKILL.md)
- Secrets management in AI infrastructure → [secrets-in-prompts-detection/SKILL.md](../secrets-in-prompts-detection/SKILL.md)
- System and runtime security → [system-infrastructure-security/SKILL.md](../system-infrastructure-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
