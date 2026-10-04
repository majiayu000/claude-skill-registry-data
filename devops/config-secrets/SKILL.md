---
name: config-secrets
description: Manage AICP's runtime secrets — env vars in `.env` (gitignored) consumed by `aicp/config/loader.py`, cloud-backend tokens (Anthropic, OpenRouter, ntfy), HuggingFace tokens for model downloads. Add new secrets, rotate existing ones, audit `.env.example` placeholders, set up CI/CD secret injection. Distinct from infra-security (audits posture) — this skill is the operational lifecycle. Loads when the operator says "add a secret" / "rotate token X" / "configure secret Y" / "what env vars does AICP need".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# config-secrets

The operational lifecycle of AICP's runtime secrets. AICP reads secrets from
`.env` via `aicp/config/loader.py`. Examples include cloud-backend tokens
(`ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`), HuggingFace token for model
downloads (`HF_TOKEN`), notification webhook URLs (`NTFY_TOPIC`). This skill
ADDS new secrets, ROTATES existing ones, and ensures `.env.example` stays
honest. Different from `infra-security` (which AUDITS the posture of secrets
end-to-end) — this skill is the day-to-day add/rotate/configure cycle.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "add a secret", "rotate token X", "configure secret Y", "what env vars does AICP need", "the API key needs updating", "set up HF_TOKEN"
- **New backend integration**: a new cloud backend or external service is being added; it needs a secret
- **Token rotation cycle**: scheduled rotation (every 90 days for prod tokens, immediate after a security incident)
- **Onboarding a new contributor**: the operator wants to give them the secrets they need to run AICP locally — this skill produces the `.env.example` walk-through
- **CI/CD pipeline setup**: GitHub Actions / GitLab CI needs secrets injected; this skill captures which ones
- **From infra-security audit**: a security audit flagged a missing or weak secret pattern; this skill fixes it

Do NOT load when:

- The concern is auditing the posture (load `infra-security` for end-to-end audit)
- The concern is which env vars exist generally (load `config-env`)
- The concern is feature flags (load `config-feature-flags`)
- A secret has leaked and you need incident response (load `ops-incident` first; rotate via this skill afterward)

## Operations

This skill has 4 named operations.

### Operation 1: Inventory the secret

**Trigger**: skill loaded; operator described a secret to add/rotate.

**Process**:

1. Frame the secret concretely: NAME (env var), PURPOSE (what AICP uses it for), SCOPE (read by which module), LIFETIME (rotation cadence), BLAST RADIUS (what fails if it's wrong/missing).
2. Check if the secret already exists:

   ```bash
   grep -rn "<SECRET_NAME>" aicp/ tools/ tests/ docker-compose.yaml Makefile 2>/dev/null | grep -v ".pyc"
   ```

   - If found in code: existing secret, this is a rotation or scope change
   - If not found: new secret, needs to be wired into the consumer

3. Check `.env.example`:

   ```bash
   grep "<SECRET_NAME>" .env.example 2>&1
   ```

   `.env.example` should ALREADY list every secret with a placeholder. If missing, that's a documentation gap to fix.

4. Identify the consumer file in `aicp/config/loader.py` (or equivalent) that READS the secret. New secrets need a consumer; without one, the secret is orphaned (per [feature-implement Gotcha 1](../feature-implement/SKILL.md)).

**Quality bar (Operation 1 done when)**:

- [ ] Secret has explicit NAME + PURPOSE + SCOPE + LIFETIME + BLAST RADIUS recorded
- [ ] Existing-vs-new classification confirmed
- [ ] `.env.example` checked
- [ ] Consumer file identified (for new secrets)

### Operation 2: Author the change

**Trigger**: Operation 1 inventory complete; operator approved the scope.

**Process**:

For **NEW secrets**:

1. Add to `.env.example` with a placeholder value and a comment:

   ```bash
   # OpenRouter API key — used by aicp/backends/openrouter.py for the openrouter tier
   # Get one at: https://openrouter.ai/keys
   # Format: sk-or-v1-... (64+ chars)
   OPENROUTER_API_KEY=<replace-with-your-openrouter-key>
   ```

2. Add to `aicp/config/loader.py` the read + validation:

   ```python
   def load_openrouter_key() -> str | None:
       value = os.getenv("OPENROUTER_API_KEY")
       if value and not value.startswith("sk-or-"):
           logger.warning("OPENROUTER_API_KEY format unexpected; verify the value")
       return value
   ```

3. Wire the consumer file (the backend / handler that uses the secret) to call the loader.
4. **Never log or echo the secret value**. The loader returns the value but logs ONLY format warnings, never the value itself.
5. Update CI/CD config (`.github/workflows/*.yaml` if present) to inject the secret as an env var.

For **ROTATIONS** (token replacement):

1. Generate the new token from the provider (out-of-band — the operator does this in the provider's UI).
2. Update local `.env` with the new value (NOT committed; `.env` is gitignored).
3. Update CI/CD secret store with the new value.
4. Test the new token: run a small request that exercises the secret (e.g., `aicp --route "test" -b openrouter` if rotating OpenRouter).
5. After confirming the new token works EVERYWHERE, REVOKE the old token in the provider's UI. Don't leave dual-active tokens — that defeats rotation.

For **PLACEHOLDER UPDATES** (`.env.example` drift):

1. Audit `.env.example` against actual env vars referenced in code:

   ```bash
   grep -rn 'os.getenv\|os.environ\[' aicp/ tools/ --include='*.py' \
     | grep -oE '"[A-Z_]+"' | sort -u
   ```

2. For each env var found in code but missing from `.env.example`: add a placeholder + comment.
3. For each placeholder in `.env.example` not found in code: investigate — either remove the placeholder (deprecated secret) or add the missing consumer (orphan).

**Quality bar (Operation 2 done when)**:

- [ ] For new: `.env.example` updated, loader updated, consumer wired, CI updated
- [ ] For rotation: new token tested end-to-end, old token revoked
- [ ] For drift: `.env.example` matches actual env var usage in code
- [ ] No secret value committed (verify `git diff` shows only placeholders / `<...>`)

### Operation 3: Verify

**Trigger**: Operation 2 changes applied.

**Process**:

1. Run the test suite — `pytest tests/ -x --tb=short`. If a test references the new secret, it must pass; if no test exists for the secret-using path, file a follow-up task.
2. Verify the secret is reachable in the runtime where it's needed:
   - Local dev: `python -m aicp.cli --check` should report all required env vars OK
   - Docker: `docker compose exec aicp env | grep <SECRET_NAME>` (without revealing the value — pipe through `head -c 10` or check existence only)
   - CI: trigger a test run; confirm secret-dependent tests pass
3. Verify `.env` is still gitignored:

   ```bash
   git check-ignore .env || echo "WARNING: .env not gitignored"
   ```

4. Run wiki lint on any docs you updated (`docs/runbooks/secrets.md`, `wiki/decisions/...` etc.).

**Quality bar (Operation 3 done when)**:

- [ ] Tests pass
- [ ] Secret reachable in all required runtimes (local + docker + CI as applicable)
- [ ] `.env` confirmed still gitignored
- [ ] Wiki lint passes for any docs touched

### Operation 4: Document + close out

**Trigger**: Operation 3 verifications passed.

**Process**:

1. Update or create the secrets runbook at `docs/runbooks/secrets.md`. For each AICP secret, document:
   - NAME / PURPOSE / consumer file path / where to obtain / format / rotation cadence
2. If the secret has a non-default rotation cadence (e.g., quarterly), add a backlog task with `target_date` for the next rotation: `wiki/backlog/tasks/T<n>-rotate-<secret>-<quarter>.md`.
3. If a SYSTEMIC pattern emerged (e.g., "every cloud backend secret should also have a rate-limit env var"), contribute back as a lesson: `gateway contribute --type lesson`.
4. Commit per conventional format:
   - New: `feat(config): add <SECRET_NAME> for <consumer>`
   - Rotation: `chore(secrets): rotate <SECRET_NAME>` (NEVER include the value)
   - Drift fix: `docs(env): align .env.example with code usage`
5. Inform the operator: change live, runbook updated, next rotation task scheduled (if applicable).

**Quality bar (Operation 4 done when)**:

- [ ] `docs/runbooks/secrets.md` updated
- [ ] Rotation backlog task created if non-default cadence
- [ ] Lesson contributed if systemic
- [ ] Conventional commit (no value committed)

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Committing the actual value (the worst possible mistake)

The temptation: pasting the new token into `.env.example` "just to test" or "for clarity." NO — once committed, it's in git history forever and must be ROTATED (not just deleted from the file).

**Detection**: did `git diff` for any commit show a real-looking token (long random string starting with `sk-`, `gho_`, `ghp_`, `hf_`, etc.)?

**The rule**: every commit that touches `.env.example` shows ONLY placeholders (`<replace-with-...>`, `<your-...>`). Run `git diff --staged | grep -E 'sk-|gho_|ghp_|hf_'` BEFORE committing — if any match, abort the commit and rotate the leaked value.

### Gotcha 2: Skipping `.env.example` (documentation drift)

The temptation: add a new secret to `.env`, wire the consumer, ship it. Skip updating `.env.example` because "it works on my machine." Next contributor clones the repo, runs `make setup`, gets a cryptic error because they don't know they need a new env var.

**Detection**: `grep -rn 'os.getenv\|os.environ' aicp/ --include='*.py' | grep -oE '"[A-Z_]+"' | sort -u` returns env vars not in `.env.example`.

**The rule**: every code reference to an env var has a matching entry in `.env.example`. The example IS the contract for what AICP needs to run.

### Gotcha 3: Logging the secret accidentally (silent leak)

The temptation: `logger.debug(f"using API key {api_key}")` for "debugging." Logs go to disk, get shipped to log aggregators, get scraped by SREs — all of which is a leak vector.

**Detection**: `grep -rn 'logger\.' aicp/ --include='*.py' | grep -iE 'api_key|token|secret|password'`

**The rule**: secrets NEVER appear in log lines. The variable name can appear (`logger.debug("using OPENROUTER_API_KEY")`) but never the value. If you need to debug whether the value is present, log only its length or first/last 4 chars.

### Gotcha 4: Rotation that leaves dual-active tokens (compromised window)

The temptation: generate the new token, deploy it, "we'll revoke the old one later." Both tokens are now valid. If the old token leaked at any point, the leak has been extended.

**Detection**: did Operation 2 explicitly REVOKE the old token after confirming the new one works?

**The rule**: rotation is atomic — old token revoked within minutes of new token confirmed working. Never leave dual-active tokens overnight unless there's a deployment window requirement.

### Gotcha 5: Secrets in profile YAML (wrong layer)

The temptation: `config/profiles/reliable.yaml` has `notify.ntfy_url: "https://ntfy.sh/secret-topic-foo"`. The URL contains an authentication token. This commits the secret to the repo.

**Detection**: `grep -rEn 'token|key|password|secret|sk-|gho_|ghp_|hf_' config/profiles/ 2>/dev/null`.

**The rule**: profiles reference env vars, never values. Use `${NTFY_TOPIC}` in the profile YAML; let the loader resolve it from `.env`. If the profile loader doesn't support env var interpolation, that's a tooling gap to fix in `aicp/core/profiles.py` — file a task.

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifacts:

- **Real secrets loader**: see [aicp/config/loader.py](../../../aicp/config/loader.py) for the env var read pattern AICP uses
- **Real `.env.example`**: see [.env.example](../../../.env.example) for the placeholder + comment pattern
- **Real runbook structure**: see `docs/runbooks/` (create if missing) — markdown with NAME / PURPOSE / consumer / source / format / rotation cadence per secret

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml). AICP-specific concerns: `.env` lives at repo root, gitignored. Profiles reference env vars (no inline values). Docker compose injects env vars via `env_file: .env`. CI/CD secret store (GitHub Actions secrets) provides values for non-local runtimes.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| infra-security | end-to-end security audit | Audit posture across secrets + guardrails + exposure + supply chain; this skill is per-secret operational |
| config-env | general env var management | Includes secrets but also non-secret config; this skill is secrets-specific |
| config-feature-flags | feature toggles | Different config dimension (behavior vs identity) |
| config-deploy | deployment configuration | Deploy includes injecting secrets to target runtime; this skill manages the secrets themselves |
| ops-incident | leak response | Reactive (a secret leaked); this skill rotates as part of incident response |
| foundation-config | initial config setup | Greenfield; this skill is per-secret lifecycle |
