---
name: ollama-security
description: Review an Ollama deployment for unauthenticated API exposure, model pull from untrusted registries, CORS misconfiguration enabling cross-origin inference abuse, and absence of resource controls on a local inference server.
last_reviewed: 2026-04-29
---

# Ollama Security

## First Principle

**Ollama's default configuration is optimized for a developer's laptop. It has no authentication, open CORS, and pulls model weights from any registry URL you give it. Deploying those defaults in any shared or production context is an unauthenticated inference endpoint with an open model download channel.**

Ollama runs a REST API on port 11434 by default. On macOS it binds to `127.0.0.1`; on Linux it binds to `0.0.0.0`. The Linux default means any host-reachable client can query any loaded model, pull new models, and push arbitrary model names — with no authentication required by default.

## Attack Mental Model

1. **Unauthenticated API abuse** — any process that can reach port 11434 can call `/api/generate`, `/api/chat`, or `/api/pull` without credentials. On a shared host or in a misconfigured container, this is a free inference endpoint for every user on the machine.
2. **Malicious model pull** — `POST /api/pull` accepts any model name. A compromised application that passes user-controlled input to the pull endpoint can cause Ollama to download and run arbitrary model weights.
3. **CORS exfiltration** — Ollama's default CORS policy allows all origins. A malicious web page visited by a developer can make cross-origin requests to `http://localhost:11434` and exfiltrate inference results or trigger model behavior.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Model pull requests reference only an allowlisted set of model names and registry origins. User-controlled input is never interpolated directly into pull requests. |
| **Scope** | The Ollama API is accessible only from authorized clients — either via loopback binding (developer use) or behind an authenticated reverse proxy (shared use). |
| **Isolate** | Ollama runs as a dedicated service account. Model storage, process credentials, and runtime resources are isolated from other services on the host. |
| **Enforce** | CORS is explicitly restricted to the application's own origin. The default wildcard policy is overridden in any non-localhost deployment. |

## OLS.1 API Exposure and Authentication Enforcement

**The core vulnerability:** Ollama has no built-in authentication. The `OLLAMA_HOST` environment variable controls the bind address — but changing it requires restarting the service, and the Linux package defaults to `0.0.0.0:11434`. Teams using Ollama on shared machines or in containers often discover the API is accessible network-wide only after an incident.

### Check

- On Linux, is `OLLAMA_HOST` explicitly set to `127.0.0.1:11434` — or is network exposure intentional and protected by an authenticated proxy?
- Is there an authentication layer (API key, mTLS, or session token) applied to all non-loopback Ollama API access?
- Is access to the `POST /api/pull` and `DELETE /api/delete` endpoints restricted to administrative identities — not available to application service accounts?

### Action

- **Set `OLLAMA_HOST=127.0.0.1:11434` in the systemd unit or container environment.** Do this before deploying to any shared machine:

```ini
# /etc/systemd/system/ollama.service.d/override.conf
[Service]
Environment="OLLAMA_HOST=127.0.0.1:11434"
```

- **For shared or production deployments, place nginx in front of Ollama.** Apply Bearer token authentication at the proxy layer. Only proxy `/api/generate` and `/api/chat` to application clients; restrict `/api/pull`, `/api/delete`, and `/api/push` to admin-only routes.
- **Set `OLLAMA_ORIGINS` to the application's own origin.** Override the wildcard CORS default: `Environment="OLLAMA_ORIGINS=https://myapp.internal"`.

### Failure Modes

- A Docker Compose stack runs Ollama with default settings and maps port 11434 to the host. Any service on the host network — including a compromised container — can query any loaded model.
- A developer visits a malicious web page that makes a cross-origin `fetch("http://localhost:11434/api/generate", ...)` call. The default `*` CORS policy allows the browser to complete the request and return the response to the attacker's origin.

## OLS.2 Model Registry and Pull Authorization

**The core vulnerability:** `POST /api/pull {"model": "<name>"}` is the only input Ollama needs to download and register a model. If an application passes user-supplied or externally-controlled model names to this endpoint, an attacker can cause Ollama to pull an arbitrary model — potentially one containing backdoors or optimized for extracting sensitive context.

### Check

- Is there an allowlist of approved model names that Ollama is permitted to load on each host?
- Is user-controlled input ever interpolated into model pull or generate requests? If so, is it validated against the allowlist before the API call?
- Are model SHA digests verified after pull — confirming the downloaded layers match the registry manifest?

### Action

- **Maintain a model allowlist per environment.** Define the approved model set in a configuration file, not in application code:

```yaml
# ollama-allowlist.yaml
approved_models:
  - "llama3.2:8b-instruct-q4_K_M"
  - "mistral:7b-instruct-v0.3-q5_K_S"
```

- **Validate model names before calling the pull API.** Never pass user input directly as a model name. Validate against the allowlist server-side:

```python
ALLOWED_MODELS = load_allowlist("ollama-allowlist.yaml")

def pull_model(model_name: str):
    if model_name not in ALLOWED_MODELS:
        raise UnauthorizedModelError(model_name)
    requests.post("http://127.0.0.1:11434/api/pull", json={"model": model_name})
```

- **Verify model digests post-pull.** After pulling, call `GET /api/show` to retrieve the model's digest and compare against your registry record. Reject models whose digests do not match.

### Minimum Deliverable Per Review

- [ ] Bind address: `OLLAMA_HOST` value and justification for any non-loopback setting
- [ ] CORS configuration: `OLLAMA_ORIGINS` value and confirmed non-wildcard setting
- [ ] Authentication proxy: configuration for any shared/production deployment
- [ ] Model allowlist: approved model names and digest verification procedure
- [ ] Pull endpoint access control: restricted to admin only, not application service accounts

## Quick Win

**Check `OLLAMA_HOST` right now.** On Linux, run `systemctl show ollama | grep Environment`. If you do not see `OLLAMA_HOST=127.0.0.1:11434`, your Ollama API is listening on all interfaces with no authentication. Set it and restart.

## References

- Local inference alongside llamafile → [llamafile-local-model-security/SKILL.md](../llamafile-local-model-security/SKILL.md)
- LiteLLM proxy as a front-end for Ollama → [litellm-proxy-security/SKILL.md](../litellm-proxy-security/SKILL.md)
- System and runtime security → [system-infrastructure-security/SKILL.md](../system-infrastructure-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
