---
name: python-credential-provider-pattern
description: >
  Use this when designing a client that authenticates to an external service,
  reviewing an api_key: str field on a Config, spotting a credential in a log
  message or span attribute, or asking whether tokens can rotate without
  restarting the consumer. Covers the async CredentialProvider Protocol, a
  redacting SecretStr wrapper with hmac.compare_digest equality, Static / Env /
  File / CachedFile (mtime-based) / OAuth (refresh-coalesced) provider
  implementations, keyword-only Provider injection on the Client, per-request
  fetch (no instance cache), credential_provider_from_spec helpers, never-log
  rules for span attributes / HTTP debug logs / exception messages, and
  Provider aclose() ownership.
  Triggers: credential, secret, token, api_key, password, SecretStr, mounted-secret, AWS_ACCESS_KEY, refresh, x-api-key, Authorization.
---

# python-credential-provider-pattern (v1.0.0)

## Rationale

A credential is not a Config field. The credential's value changes (rotation, K8s secret reload, IAM token refresh, OAuth refresh) over the SDK's lifetime; the SDK must not bake it into a snapshot at construction. The pattern: a `CredentialProvider` Protocol injected at the same seam as other dependencies (`python-mock-strategy` Rule 1). The provider returns a fresh credential on demand. The SDK NEVER caches the credential beyond a single request, NEVER logs it, NEVER returns it to a caller.

This skill is cited by `code-reviewer-python` (security review-criteria), `python-sdk-config-pattern` (Config takes a Provider, not a token literal), `sdk-security-devil` (credential handling), `python-otel-instrumentation` (no credentials in span attributes), `python-exception-patterns` (`AuthError` carries no token data), and `conventions.yaml` (`credential_log_safety`).

## Activation signals

- Designing a client that authenticates to an external service.
- Code review surfaces an `api_key: str` field on Config (smell — should be Provider).
- Code review surfaces a credential in a log message, span attribute, or repr.
- Production deployment reads creds from K8s mounted secrets — does the SDK reload?
- Reviewing whether a token can be ROTATED without restarting the consumer.

## Core Protocol

```python
# motadatapysdk/credentials.py
from typing import Protocol


class CredentialProvider(Protocol):
    """Async credential source.

    Implementations: StaticProvider, EnvProvider, FileProvider, K8sSecretProvider,
    AWSSignatureProvider, OAuthProvider.

    Every method is allowed to do I/O (file read, network call, IAM exchange);
    callers MUST `await` and treat the value as ephemeral — single-request use only.
    """

    async def get(self) -> "SecretStr":
        """Return the current credential.

        Raises:
            AuthError: If the credential cannot be obtained or has been revoked.
        """
        ...
```

The Protocol method is `async def get()` because some providers do I/O (read a file, refresh an OAuth token, sign an AWS request). Sync providers wrap their value in an `async def` that returns immediately — small overhead, uniform contract.

## Rule 1 — `SecretStr` is the only public credential type

```python
# motadatapysdk/credentials.py
from typing import Final


class SecretStr:
    """Opaque container for a secret string.

    Repr / str / format are all redacted. The raw value is accessed only via
    ``.get_secret_value()`` and only by code that needs to put it on the wire.

    Examples:
        >>> s = SecretStr("super-secret-token")
        >>> str(s)
        '[REDACTED]'
        >>> repr(s)
        "SecretStr('[REDACTED]')"
        >>> s.get_secret_value()
        'super-secret-token'
    """

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        self._value = value

    def __str__(self) -> str:
        return "[REDACTED]"

    def __repr__(self) -> str:
        return "SecretStr('[REDACTED]')"

    def __format__(self, format_spec: str) -> str:
        return "[REDACTED]"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SecretStr):
            return NotImplemented
        # Constant-time compare to avoid timing attacks
        import hmac
        return hmac.compare_digest(self._value, other._value)

    def __hash__(self) -> int:
        # Hash redacted; SecretStr is not safe to use as a dict key in cred-aware code
        return hash("SecretStr-opaque")

    def get_secret_value(self) -> str:
        """Return the underlying secret.

        Use ONLY where the secret must be transmitted on the wire (Authorization
        header, AWS SigV4 signing, NATS auth callback). Never log the result.
        """
        return self._value
```

The redacted forms (`str`, `repr`, `__format__`) catch the most common leaks: f-strings, `print()`, logger format-strings, debug exception messages. `pydantic.SecretStr` is functionally equivalent — if the SDK already depends on pydantic, use it; otherwise the homegrown class above is one file with no transitive cost.

`__eq__` uses `hmac.compare_digest` to defeat timing attacks if the SecretStr is ever compared as part of an authentication path.

## Rule 2 — Provider implementations

### StaticProvider — for tests and static-config paths

```python
class StaticProvider:
    """Credential provider with a fixed value.

    Use for unit tests and for environments where the credential lives in a
    config-management system that already manages rotation (e.g., Hashicorp Vault
    Agent injects the latest value into a known env var).
    """

    def __init__(self, secret: str | SecretStr) -> None:
        self._secret = secret if isinstance(secret, SecretStr) else SecretStr(secret)

    async def get(self) -> SecretStr:
        return self._secret
```

### EnvProvider — read from environment

```python
import os

class EnvProvider:
    """Read the credential from an environment variable on each call.

    Reads on every ``.get()`` so rotation via systemd unit reload (or container
    restart with a new env value) is picked up.
    """

    def __init__(self, *, var_name: str = "MOTADATA_API_KEY") -> None:
        self._var_name = var_name

    async def get(self) -> SecretStr:
        value = os.environ.get(self._var_name)
        if not value:
            raise AuthError(f"environment variable {self._var_name} is unset")
        return SecretStr(value)
```

### FileProvider — for K8s mounted secrets

```python
import asyncio
from pathlib import Path

class FileProvider:
    """Read the credential from a file on each call.

    For K8s ``Secret`` mounted as a file: the kubelet atomically swaps the file
    on rotation, so each ``get()`` picks up the new value within seconds.
    """

    def __init__(self, *, path: Path) -> None:
        self._path = path

    async def get(self) -> SecretStr:
        try:
            value = await asyncio.to_thread(self._path.read_text)
        except FileNotFoundError as e:
            raise AuthError(f"credential file {self._path} not found") from e
        except PermissionError as e:
            raise AuthError(f"credential file {self._path} not readable") from e
        return SecretStr(value.strip())
```

`asyncio.to_thread` because file reads are blocking; running them in the loop's executor preserves async semantics. For a hot path that reads the same file thousands of times per second, add an mtime-based cache:

```python
class CachedFileProvider:
    def __init__(self, *, path: Path, refresh_interval_s: float = 60.0) -> None:
        self._path = path
        self._refresh_interval = refresh_interval_s
        self._cached: SecretStr | None = None
        self._cached_mtime: float = 0.0
        self._lock = asyncio.Lock()

    async def get(self) -> SecretStr:
        async with self._lock:
            mtime = await asyncio.to_thread(lambda: self._path.stat().st_mtime)
            if self._cached is None or mtime > self._cached_mtime:
                value = await asyncio.to_thread(self._path.read_text)
                self._cached = SecretStr(value.strip())
                self._cached_mtime = mtime
            return self._cached
```

K8s atomic-swap rotation works because `kubelet` updates `..data/<key>` symlinks; `stat().st_mtime` reflects the swap.

### OAuthProvider — for token-refresh flows

```python
import time
from dataclasses import dataclass, field

@dataclass
class _CachedToken:
    secret: SecretStr
    expires_at_unix: float


class OAuthProvider:
    """Fetch + refresh OAuth client_credentials tokens.

    Caches the access token until 60 seconds before its declared expiry; refreshes
    on demand within a ``refresh_lock`` so concurrent ``get()`` calls coalesce.
    """

    def __init__(
        self,
        *,
        token_url: str,
        client_id: str,
        client_secret: SecretStr,
        scope: str | None = None,
        clock_skew_s: float = 60.0,
    ) -> None:
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope
        self._clock_skew_s = clock_skew_s
        self._cached: _CachedToken | None = None
        self._refresh_lock = asyncio.Lock()
        self._http: httpx.AsyncClient | None = None

    async def get(self) -> SecretStr:
        if self._cached is not None and self._cached.expires_at_unix > time.time() + self._clock_skew_s:
            return self._cached.secret

        async with self._refresh_lock:
            # Double-check inside the lock — another task may have refreshed
            if self._cached is not None and self._cached.expires_at_unix > time.time() + self._clock_skew_s:
                return self._cached.secret

            await self._refresh()
            assert self._cached is not None       # mypy
            return self._cached.secret

    async def _refresh(self) -> None:
        if self._http is None:
            self._http = httpx.AsyncClient()
        body = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret.get_secret_value(),
        }
        if self._scope:
            body["scope"] = self._scope
        try:
            resp = await self._http.post(self._token_url, data=body)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise AuthError("OAuth token refresh failed") from e
        data = resp.json()
        self._cached = _CachedToken(
            secret=SecretStr(data["access_token"]),
            expires_at_unix=time.time() + float(data.get("expires_in", 3600)),
        )

    async def aclose(self) -> None:
        if self._http is not None:
            await self._http.aclose()
            self._http = None
```

The refresh-coalescing pattern (`asyncio.Lock` + double-check) is mandatory: without it, N concurrent `get()` calls on cache miss all attempt to refresh, hammering the token endpoint and racing on `_cached`.

`clock_skew_s=60` protects against the token expiring mid-request — refresh 60s before the server's declared expiry.

## Rule 3 — Client takes the Provider, not the credential

```python
# WRONG — credential snapshotted at construction; rotation invisible
@dataclass(frozen=True, kw_only=True)
class Config:
    base_url: str
    api_key: str                      # plain str; no rotation; logs may leak it

class Client:
    def __init__(self, config: Config) -> None:
        self._api_key = config.api_key

# RIGHT — provider injected; rotation works; logs cannot leak the value
@dataclass(frozen=True, kw_only=True)
class Config:
    base_url: str
    timeout_s: float = 5.0
    # No api_key field

class Client:
    def __init__(self, config: Config, *, credentials: CredentialProvider) -> None:
        self._config = config
        self._credentials = credentials

    async def publish(self, topic: str, payload: bytes) -> None:
        token = await self._credentials.get()
        headers = {"Authorization": f"Bearer {token.get_secret_value()}"}
        # token goes out of scope at function exit
        await self._http.post(self._url(topic), data=payload, headers=headers)
```

The `credentials=` parameter is **keyword-only** (per `python-sdk-config-pattern` Rule). The Provider is required; there is no default fallback, because a default fallback would invariably include "read from `MOTADATA_API_KEY` env" which is then surprising for users with a different setup. Make it explicit.

For convenience, ship a top-level helper that picks a Provider by string spec:

```python
def credential_provider_from_spec(spec: str) -> CredentialProvider:
    """Construct a Provider from a URL-like spec.

    Examples:
        >>> p = credential_provider_from_spec("env:MOTADATA_API_KEY")
        >>> isinstance(p, EnvProvider)
        True
        >>> p = credential_provider_from_spec("file:/var/run/secrets/api-key")
        >>> isinstance(p, FileProvider)
        True
    """
    if spec.startswith("env:"):
        return EnvProvider(var_name=spec[len("env:"):])
    if spec.startswith("file:"):
        return FileProvider(path=Path(spec[len("file:"):]))
    if spec.startswith("static:"):
        # SECURITY: only acceptable in tests / dev
        return StaticProvider(spec[len("static:"):])
    raise ValueError(f"unknown credential spec: {spec}")
```

## Rule 4 — Token has the SHORTEST possible lifetime

```python
# WRONG — token cached on the instance
class Client:
    def __init__(self, config: Config, *, credentials: CredentialProvider) -> None:
        self._token: SecretStr | None = None      # leaks across rotation

    async def publish(self, ...):
        if self._token is None:
            self._token = await self._credentials.get()   # cached forever
        ...

# RIGHT — token fresh on every request
async def publish(self, topic: str, payload: bytes) -> None:
    token = await self._credentials.get()        # provider may cache; SDK does not
    headers = {"Authorization": f"Bearer {token.get_secret_value()}"}
    await self._http.post(...)                    # token goes out of scope
```

The PROVIDER decides whether to cache (OAuthProvider does; FileProvider may; StaticProvider trivially does). The CLIENT does not — every request gets a fresh `await provider.get()`. This is the SDK's rotation contract: rotate the underlying source, the next request picks it up.

## Rule 5 — Never log credentials, ever

The `SecretStr` redacted forms catch most leaks. The remaining leak surface:

- **OTel span attributes**: `span.set_attribute("auth.token", token.get_secret_value())` → leaks to backend. Use `auth.scheme = "Bearer"` instead — operators don't need the value.
- **HTTP request logging**: aiohttp / httpx debug logs include headers by default. Configure `Authorization` redaction:
  ```python
  import logging
  class RedactAuthFilter(logging.Filter):
      def filter(self, record: logging.LogRecord) -> bool:
          if hasattr(record, "args") and isinstance(record.args, dict):
              record.args = {k: ("[REDACTED]" if k.lower() == "authorization" else v) for k, v in record.args.items()}
          return True
  logging.getLogger("httpx").addFilter(RedactAuthFilter())
  ```
- **Exception messages**: never `raise AuthError(f"failed for token {token.get_secret_value()}")`. The exception message goes to logs, traces, and possibly the user.
- **`__repr__` leaks via `pdb` / `breakpoint()`**: SecretStr handles this at construction.

`sdk-security-devil` audits each of these. The convention covers them at the source.

## Rule 6 — Never put credentials in source code

```python
# WRONG — committed to git; visible in IDE / GitHub / log of the build agent
client = Client(Config(...), credentials=StaticProvider("ak_prod_xyz123"))

# RIGHT — read from environment / file at runtime
client = Client(
    Config(...),
    credentials=EnvProvider(var_name="MOTADATA_API_KEY"),
)
```

For tests: use `monkeypatch.setenv` / `tmp_path / file.write_text("test-token")` rather than embedding test tokens in source. CI secrets get loaded into the test runtime's env without ever entering source control.

`.env.example` (committed; placeholder) and `.env` (gitignored; real) is the convention from CLAUDE.md rule 27.

## Rule 7 — The Provider is closeable

For Providers that hold resources (OAuthProvider holds an `httpx.AsyncClient`), implement `aclose()`:

```python
class OAuthProvider:
    async def aclose(self) -> None:
        if self._http is not None:
            await self._http.aclose()
            self._http = None
```

The Client takes ownership of closing the Provider only if it constructed it. Default policy: caller constructs the Provider, caller owns its lifetime:

```python
async def main() -> None:
    provider = OAuthProvider(...)
    try:
        async with Client(Config(...), credentials=provider) as c:
            await c.publish("...", b"...")
    finally:
        await provider.aclose()
```

`AsyncExitStack` for multi-resource composition (per `python-asyncio-patterns` discussion).

## Rule 8 — Test the Provider seam

```python
import pytest
from motadatapysdk.credentials import CredentialProvider, SecretStr


class FakeProvider:
    """Test Provider that records every get() call."""

    def __init__(self, *, value: str = "test-token") -> None:
        self._value = value
        self.get_calls: int = 0

    async def get(self) -> SecretStr:
        self.get_calls += 1
        return SecretStr(self._value)


async def test_publish_calls_provider_each_request(client_factory) -> None:
    fake = FakeProvider()
    async with client_factory(credentials=fake) as client:
        await client.publish("t", b"a")
        await client.publish("t", b"b")
    assert fake.get_calls == 2                   # fresh token per request


async def test_provider_failure_surfaces_as_auth_error(client_factory) -> None:
    class BrokenProvider:
        async def get(self) -> SecretStr:
            raise AuthError("token endpoint down")

    async with client_factory(credentials=BrokenProvider()) as client:
        with pytest.raises(AuthError, match="token endpoint down"):
            await client.publish("t", b"a")
```

`FakeProvider` is the test pattern from `python-mock-strategy` (Protocol-typed Fake). `mypy --strict` accepts it as a `CredentialProvider` because Protocols are structurally typed.

## GOOD: full client method

```python
import logging

from motadatapysdk.credentials import CredentialProvider, SecretStr
from motadatapysdk.errors import AuthError, MotadataError, NetworkError

logger = logging.getLogger(__name__)


class Client:
    """Async client for the motadata API.

    Examples:
        >>> async def demo() -> None:
        ...     async with Client(
        ...         Config(base_url="https://x"),
        ...         credentials=EnvProvider(var_name="MOTADATA_API_KEY"),
        ...     ) as client:
        ...         await client.publish("topic", b"x")
        >>> asyncio.run(demo())  # doctest: +SKIP
    """

    def __init__(self, config: Config, *, credentials: CredentialProvider) -> None:
        self._config = config
        self._credentials = credentials

    async def publish(self, topic: str, payload: bytes) -> None:
        try:
            token = await self._credentials.get()
        except AuthError:
            logger.warning("credential refresh failed for publish to %s", topic)
            raise

        headers = {"Authorization": f"Bearer {token.get_secret_value()}"}
        # token leaves scope after the post completes
        try:
            response = await self._http.post(
                self._url(topic), data=payload, headers=headers,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (401, 403):
                raise AuthError(
                    f"server rejected credentials for {topic}",
                    status_code=e.response.status_code,
                ) from e
            raise

    def _url(self, topic: str) -> str:
        return f"{self._config.base_url.rstrip('/')}/topics/{topic}"
```

Demonstrates: Provider injected (Rule 3), token fetched per request (Rule 4), `get_secret_value()` used at the wire boundary only, no token in log message (Rule 5), AuthError on 401/403, exception chaining via `from e`.

## BAD anti-patterns

```python
# 1. Credential in Config
@dataclass
class Config:
    api_key: str                      # snapshotted; rotation breaks; logs leak repr

# 2. Token cached on the client instance
self._token: str | None = None
async def publish(...):
    if self._token is None:
        self._token = await self._credentials.get()   # rotation invisible

# 3. Logging the token
logger.debug("publishing with token %s", token.get_secret_value())   # leak

# 4. Token in span attribute
span.set_attribute("auth.token", token.get_secret_value())          # leak to OTel backend

# 5. Token in exception message
raise AuthError(f"server rejected token {token.get_secret_value()}")  # leak in traces

# 6. Plain str instead of SecretStr
def get_token(self) -> str:        # caller might log it
    ...

# 7. Hardcoded credential
StaticProvider("ak_prod_xyz")      # committed to git

# 8. No refresh lock on OAuth refresh
async def _refresh(self):
    if self._token is None:
        self._token = await ...     # N concurrent calls all hit the token endpoint

# 9. Never closing the Provider's resources
provider = OAuthProvider(...)
async with Client(..., credentials=provider) as c:
    ...                             # provider's httpx.AsyncClient leaks

# 10. Comparing SecretStr with ==
if user_token == sdk_token:        # if both are SecretStr, OK (constant-time);
                                    # if either is str, it's still str-compare and may time-attack
# Use hmac.compare_digest on the raw values when authenticating.
```

## Cross-references

- `python-sdk-config-pattern` — Config has no credential field; Provider is a separate constructor parameter.
- `python-mock-strategy` — Provider is a Protocol; tests use FakeProvider.
- `python-exception-patterns` — `AuthError` from `python-exception-patterns`; carries `status_code` only.
- `python-asyncio-patterns` Rule 4 — Provider's `get()` is cancellation-safe.
- `python-otel-instrumentation` — span attributes use `auth.scheme`, never the value.
- `python-client-shutdown-lifecycle` — Provider's `aclose()` is part of caller's cleanup.
- `network-error-classification` (shared) — 401/403 → `AuthError`.
- `idempotent-retry-safety` (shared) — `AuthError` is NOT retriable without re-resolving the credential.
- `conventions.yaml` `credential_log_safety` — design-rule enforcement.
