---
name: llamafile-local-model-security
description: Review a llamafile local inference deployment for unsafe model artifact handling, exposed HTTP server attack surface, local filesystem and process access risks, and absence of access controls on a single-binary inference endpoint.
last_reviewed: 2026-04-29
---

# Llamafile Local Model Security

## First Principle

**llamafile makes running a model locally trivially easy. That ease is also an unadvertised attack surface — a default HTTP server, bound to localhost with no authentication, running with the privileges of whoever launched it.**

Llamafile bundles a model and a GGML inference runtime into a single executable. Run it, and you have an OpenAI-compatible HTTP API on port 8080. That convenience defaults to no authentication, no rate limiting, and the process permissions of the launching user. On a shared development machine or in a container with open networking, that is an unguarded inference endpoint accessible to anything that can reach the port.

## Attack Mental Model

1. **Unauthenticated API access** — any process or user on the same host (or network-reachable host) can query the inference endpoint, inject prompts, and receive outputs — with no credential requirement.
2. **Malicious model artifact** — a GGML/GGUF file downloaded from an untrusted source can contain weight modifications equivalent to a backdoor. The model file is the trust root; a tampered model behaves incorrectly in attacker-controlled scenarios.
3. **Process privilege abuse** — llamafile inherits the launching user's permissions. If that user has write access to application code, credentials, or sensitive files, a prompt-injected model output that triggers tool use or code execution runs with those permissions.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Model artifacts are verified by SHA-256 against a known-good registry before the llamafile is executed. Unverified model files are not run. |
| **Scope** | The llamafile HTTP server binds to `127.0.0.1` only and is launched by a dedicated low-privilege service account. Its port is not reachable from outside the host without explicit, justified network exposure. |
| **Isolate** | llamafile runs in a container or VM with no access to production credentials, secrets, or network endpoints beyond its defined inference scope. |
| **Enforce** | Any application layer consuming the llamafile API applies authentication, rate limiting, and output validation — the llamafile binary itself is treated as an unauthenticated internal service. |

## LLF.1 Model Artifact Integrity and Provenance

**The core vulnerability:** GGUF model files are downloaded from Hugging Face or other public hosts, often by following links in documentation or READMEs. Without checksum verification, there is no guarantee that the downloaded file matches what the model author published — or that the model author's published file is itself trustworthy.

### Check

- Is every GGUF model file verified by SHA-256 against a value from the model author's official release page (not from the download host's auto-generated metadata)?
- Is there an approved model list for local inference — limiting which models can be run on which machines?
- Are GGUF files stored in a location with restricted write access — preventing post-download tampering?

### Action

- **Verify checksums at download time and before each run.** Maintain a local registry of approved GGUF files with their expected SHA-256 values. Before launching llamafile, recompute the checksum:

```bash
#!/bin/bash
EXPECTED_SHA="abc123..."
ACTUAL_SHA=$(sha256sum "$MODEL_PATH" | awk '{print $1}')
if [ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]; then
  echo "Model checksum mismatch — refusing to launch" >&2
  exit 1
fi
exec ./llamafile --model "$MODEL_PATH" --host 127.0.0.1 "$@"
```

- **Store GGUF files with restricted permissions.** The model file directory should be owned by the service account and not world-writable. Mode `640` is appropriate.
- **Log model artifact versions.** For every llamafile launch, emit a structured log entry: `{model_path, sha256, launched_by, timestamp}`.

### Failure Modes

- A developer downloads a GGUF from a community hub link in a forum post. The link points to a slightly modified file. The model behaves correctly on standard prompts and incorrectly on a specific trigger sequence.
- A post-download tampering attack modifies a GGUF file in a shared NFS mount. All machines using that mount run the tampered model.

## LLF.2 HTTP Server Exposure and Access Control

**The core vulnerability:** llamafile's built-in server defaults to all interfaces (`0.0.0.0`) in some versions and has no authentication. In a shared machine, CI environment, or container with host networking, this means the inference endpoint is accessible to any process or user without credentials.

### Check

- Is llamafile started with `--host 127.0.0.1` — never `0.0.0.0` — unless network exposure is explicitly required and justified?
- Is an application-layer authentication proxy (nginx, Caddy, or similar) placed in front of the llamafile port for any network-exposed deployment?
- Is rate limiting applied to prevent DoS via inference exhaustion — especially on shared machines where GPU/CPU resources are finite?
- Is the llamafile process run as a dedicated low-privilege service account rather than a developer's interactive user account?

### Action

- **Bind to loopback only.** Always start with `--host 127.0.0.1`. If network access is required, terminate TLS and authentication at a reverse proxy — never expose the raw llamafile port.
- **Run as a dedicated service account.** Create a `llamafile-svc` account with no login shell and no access to developer credentials or application secrets. Launch llamafile under this account via systemd or a container entrypoint.
- **Apply rate limiting at the proxy layer.** Limit requests per minute per client IP. Inference requests are expensive; a single client sending 100 concurrent requests can exhaust GPU resources.
- **Disable the built-in web UI in production.** The llamafile web UI at `/` is a browser-accessible chat interface. Disable it with `--nobrowser` and restrict static asset serving when deploying as a backend service.

### Minimum Deliverable Per Review

- [ ] Model artifact registry: GGUF path, SHA-256, approved-by, last verified date
- [ ] Launch script: checksum verification step before exec
- [ ] Network binding: confirmed `--host 127.0.0.1` or documented justification for broader exposure
- [ ] Service account: dedicated low-privilege account name and permissions audit
- [ ] Rate limiting configuration at the proxy layer
- [ ] Web UI status: disabled in non-interactive deployments

## Quick Win

**Add one line to your launch script: `--host 127.0.0.1`.** If llamafile is currently binding to all interfaces, this single flag closes the unauthenticated network exposure. Then add the SHA-256 check. Both changes take under ten minutes and eliminate the two most common llamafile deployment vulnerabilities.

## References

- Model artifact integrity for full model pipelines → [model-supply-chain-security/SKILL.md](../model-supply-chain-security/SKILL.md)
- Local inference alongside Ollama → [ollama-security/SKILL.md](../ollama-security/SKILL.md)
- System and runtime security → [system-infrastructure-security/SKILL.md](../system-infrastructure-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
