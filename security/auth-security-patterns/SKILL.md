---
name: auth-security-patterns
description: Authentication, secret management, and security patterns for VoxAgent. Use when handling API keys, implementing authentication, validating user input, managing sessions, or auditing security. Triggers on tasks involving core/keyring_manager.py, core/safety.py, api/middleware, or any security-related code.
---

# Authentication & Security Patterns for VoxAgent

Guidelines for secure secret management, input validation, API authentication, and defense-in-depth across VoxAgent's Python backend and API layer.

## When to Apply

Reference these guidelines when:
- Storing or retrieving API keys (`core/keyring_manager.py`)
- Validating user input or LLM-generated commands (`core/safety.py`)
- Adding authentication to API endpoints
- Implementing session management
- Auditing code for security vulnerabilities
- Reviewing PRs that touch secrets, auth, or user input

## Rule Categories by Priority

| Priority | Category | Impact | Applies to |
|----------|----------|--------|------------|
| 1 | Secret Management | CRITICAL | All modules |
| 2 | Input Validation | CRITICAL | core/, api/ |
| 3 | API Authentication | HIGH | api/ |
| 4 | Session Security | HIGH | api/, core/ |
| 5 | Defense in Depth | MEDIUM | All modules |

## Quick Reference

### 1. Secret Management (CRITICAL)

- `secret-keyring-only` — ALWAYS store API keys in the OS keyring via `keyring` library. Never in config files, env vars in code, or hardcoded strings:
  ```python
  import keyring

  # Good: OS keyring
  def get_api_key(provider: str) -> str:
      key = keyring.get_password("voxagent", f"{provider}_api_key")
      if not key:
          raise ProviderConfigError(f"No API key found for {provider}")
      return key

  # Bad: hardcoded or config file
  API_KEY = "sk-abc123..."  # NEVER
  config = json.load(open("config.json"))["api_key"]  # NEVER
  ```

- `secret-no-log` — NEVER log, print, or include secrets in error messages. Mask them:
  ```python
  # Good: masked
  logger.info("Using provider %s with key %s...", provider, key[:8] + "***")

  # Bad: full key in logs
  logger.info("API key: %s", api_key)
  ```

- `secret-no-serialize` — Never include secrets in JSON responses, Pydantic model exports, or dataclass repr. Use `SecretStr`:
  ```python
  from pydantic import BaseModel, SecretStr

  class ProviderConfig(BaseModel):
      name: str
      api_key: SecretStr  # won't appear in .model_dump() or .json()

      model_config = ConfigDict(json_schema_extra={"properties": {"api_key": {"writeOnly": True}}})
  ```

- `secret-rotation` — Design key access to support rotation. Read from keyring on each use, don't cache indefinitely:
  ```python
  # Good: fresh read
  async def get_headers(self) -> dict[str, str]:
      key = keyring.get_password("voxagent", f"{self.name}_api_key")
      return {"Authorization": f"Bearer {key}"}

  # Bad: cached forever in __init__
  def __init__(self):
      self._key = keyring.get_password(...)  # stale after rotation
  ```

- `secret-scope` — Use separate keyring entries per provider and per environment. Namespace with `voxagent/{provider}/{env}`.

### 2. Input Validation (CRITICAL)

- `input-sanitize-llm` — Always sanitize LLM-generated commands before execution. Use allowlists, not blocklists:
  ```python
  ALLOWED_COMMANDS = frozenset({"open", "search", "play", "pause", "volume"})

  def validate_intent(intent: str) -> bool:
      base_command = intent.split()[0].lower()
      return base_command in ALLOWED_COMMANDS
  ```

- `input-validate-pydantic` — All external input MUST pass through Pydantic validation. Never trust raw dicts or strings:
  ```python
  class SkillRequest(BaseModel):
      skill_name: str = Field(min_length=1, max_length=64, pattern=r"^[a-z_]+$")
      parameters: dict[str, str] = Field(default_factory=dict, max_length=10)

  @router.post("/execute")
  async def execute(request: SkillRequest):
      ...  # request is already validated
  ```

- `input-rate-limit` — Apply rate limiting to all public API endpoints. Use sliding window per client:
  ```python
  from fastapi import Request
  from collections import defaultdict

  REQUEST_LIMIT = 60  # per minute
  _request_counts: dict[str, list[float]] = defaultdict(list)
  ```

- `input-size-limit` — Set maximum sizes for all inputs. Reject oversized payloads early:
  ```python
  MAX_TRANSCRIPT_LENGTH = 10_000  # characters
  MAX_FILE_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
  ```

### 3. API Authentication (HIGH)

- `auth-bearer-token` — Use Bearer token authentication for API endpoints. Validate in a FastAPI dependency:
  ```python
  from fastapi import Depends, HTTPException, Security
  from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

  security = HTTPBearer()

  async def verify_token(
      credentials: HTTPAuthorizationCredentials = Security(security),
  ) -> str:
      token = credentials.credentials
      if not await validate_token(token):
          raise HTTPException(status_code=401, detail="Invalid token")
      return token
  ```

- `auth-dependency` — Apply auth as a FastAPI dependency, not inline in each endpoint:
  ```python
  # Good: dependency
  @router.post("/execute", dependencies=[Depends(verify_token)])
  async def execute(request: SkillRequest):
      ...

  # Bad: inline check
  @router.post("/execute")
  async def execute(request: SkillRequest, token: str = Header(...)):
      if not valid(token): raise ...  # repeated in every endpoint
  ```

- `auth-provider-init` — Verify API keys are available at provider initialization, not at first use:
  ```python
  class LLMProvider:
      async def initialize(self) -> None:
          key = keyring.get_password("voxagent", f"{self.name}_api_key")
          if not key:
              raise ProviderConfigError(f"Missing API key for {self.name}")
  ```

- `auth-no-query-params` — Never pass tokens or secrets as URL query parameters. They leak in logs and browser history.

### 4. Session Security (HIGH)

- `session-id-random` — Generate session IDs with `secrets.token_urlsafe(32)`. Never use sequential or predictable IDs.

- `session-expiry` — All sessions MUST have a TTL. Default 30 minutes, configurable:
  ```python
  SESSION_TTL_SECONDS = 1800  # 30 minutes

  @dataclass
  class Session:
      id: str
      created_at: float
      last_active: float

      @property
      def is_expired(self) -> bool:
          return time.time() - self.last_active > SESSION_TTL_SECONDS
  ```

- `session-isolation` — Each voice session is isolated. Never share state (conversation history, context) between sessions.

- `session-cleanup` — Implement periodic cleanup of expired sessions. Use `asyncio.create_task()` with a background loop:
  ```python
  async def cleanup_sessions(store: SessionStore, interval: int = 300) -> None:
      while True:
          await asyncio.sleep(interval)
          expired = [s for s in store.sessions if s.is_expired]
          for session in expired:
              await store.remove(session.id)
  ```

### 5. Defense in Depth (MEDIUM)

- `defense-cors` — Configure CORS strictly. Only allow known origins, not `*`:
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:5173"],  # dashboard only
      allow_methods=["GET", "POST"],
      allow_headers=["Authorization", "Content-Type"],
  )
  ```

- `defense-headers` — Set security headers on all responses:
  ```python
  @app.middleware("http")
  async def security_headers(request: Request, call_next):
      response = await call_next(request)
      response.headers["X-Content-Type-Options"] = "nosniff"
      response.headers["X-Frame-Options"] = "DENY"
      response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
      return response
  ```

- `defense-dependency-audit` — Regularly audit dependencies with `pip-audit` or `safety`. Pin versions in `pyproject.toml`.

- `defense-least-privilege` — Skills declare required permissions in `permissions` field. Reject skills that request more than needed.

## Operational Procedure

### Before coding
1. Check if `core/keyring_manager.py` already handles the secret
2. Identify if the change touches any user input or external data
3. Review the existing security boundary in `core/safety.py`

### During coding
1. Use the OS keyring for ALL secrets — no exceptions
2. Validate all input with Pydantic models
3. Apply auth as FastAPI dependencies, not inline checks
4. Mask secrets in all log output

### After coding
1. Search for hardcoded strings that look like keys or tokens
2. Verify no secrets appear in error messages or API responses
3. Check that all new endpoints have auth dependencies
4. Run `ruff check` for security-related linting rules
