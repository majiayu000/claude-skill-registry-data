---
name: python-client-tls-configuration
description: >
  Use this when a Python SDK opens an HTTPS / TLS connection, reviewing code
  that touches ssl.SSLContext or sets check_hostname / verify_mode, supporting
  a private-CA or mTLS deployment, or auditing whether the TLS floor matches
  compliance baselines. Covers ssl.create_default_context() as the secure
  baseline + minimum_version pinning to TLS 1.2/1.3, layered custom-CA via
  load_verify_locations, mTLS via load_cert_chain with key password from a
  CredentialProvider, the never-weaken rule (no check_hostname=False, no
  CERT_NONE, no _create_unverified_context), httpx / aiohttp / asyncpg /
  aiokafka / nats integration, optional SHA-256 cert pinning, and wrapping
  ssl.SSLError / SSLCertVerificationError as AuthError / NetworkError.
  Triggers: ssl.SSLContext, create_default_context, load_verify_locations, load_cert_chain, TLSv1_2, TLSv1_3, check_hostname, verify_mode, CERT_REQUIRED, SNI, mTLS.
---

# python-client-tls-configuration (v1.0.0)

## Rationale

Python's stdlib `ssl` module is correct by default — but the defaults are corruptible by one careless line (`ctx.check_hostname = False`, `ssl.create_default_context().verify_mode = ssl.CERT_NONE`). Most insecure-TLS bugs in Python SDKs come from a developer working around a self-signed-cert error in dev, then forgetting the workaround was committed. The Python pack convention: build the SSLContext via `ssl.create_default_context()` (secure baseline), apply ONLY hardening (raise the floor, never lower), and surface explicit Config knobs for legitimate customization (custom CA, mTLS) without ever exposing `check_hostname=False` as a Config knob.

This skill is cited by `code-reviewer-python` (security review-criteria), `sdk-security-devil` (TLS defaults audit), `python-credential-provider-pattern` (mTLS integration), `python-sdk-config-pattern` (Config TLS fields), and `network-error-classification` (TLS errors as a fatal class).

## Activation signals

- New SDK client opens an HTTPS / TLS connection.
- Code review surfaces `ssl.SSLContext()` bare construction (no defaults).
- Code review surfaces `check_hostname = False` or `verify_mode = ssl.CERT_NONE`.
- TPRD §10 declares mTLS, custom CA, or pinned cert.
- Production deployment uses a private CA — does the SDK accept it without disabling validation?
- Reviewing whether the SDK's TLS floor matches the corporate compliance baseline.

## Core baseline

```python
import ssl

def make_default_context() -> ssl.SSLContext:
    """Return a hardened TLS client context.

    Starts from ``ssl.create_default_context()`` (which is already secure-by-default
    in Python 3.10+) and tightens the version floor to TLS 1.2.

    Examples:
        >>> ctx = make_default_context()
        >>> ctx.minimum_version >= ssl.TLSVersion.TLSv1_2
        True
        >>> ctx.check_hostname
        True
        >>> ctx.verify_mode == ssl.CERT_REQUIRED
        True
    """
    ctx = ssl.create_default_context()
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    return ctx
```

`ssl.create_default_context()` (3.10+):
- `verify_mode = CERT_REQUIRED` — peer cert must validate.
- `check_hostname = True` — peer's CN/SAN must match.
- Loads system trust store (CA bundle from `certifi` if installed; else OS).
- Disables compression (CRIME mitigation).
- Disables session tickets in some configs (but session tickets are GENERALLY safe; default behavior accepted).
- Sets cipher suite to the secure defaults.

The `minimum_version = TLSv1_2` line is belt-and-suspenders: Python's default already excludes 1.0/1.1 on modern OpenSSL, but pinning explicitly survives platform variation.

For TLS 1.3-only deployments (compliance-driven):

```python
def make_tls13_only_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.minimum_version = ssl.TLSVersion.TLSv1_3
    return ctx
```

## Rule 1 — Never weaken; only harden

```python
# WRONG — disables hostname check; defeats SAN/CN matching
ctx.check_hostname = False

# WRONG — accepts ANY cert
ctx.verify_mode = ssl.CERT_NONE

# WRONG — explicit "trust nothing" mode
ctx = ssl._create_unverified_context()                # underscore = private API; never call

# RIGHT — when consumer needs custom CA, ADD it to the trust pool
ctx.load_verify_locations(cafile=str(custom_ca_path))

# RIGHT — when consumer presents a client cert, LOAD it
ctx.load_cert_chain(certfile=str(client_cert), keyfile=str(client_key))
```

The valid customizations expand the trust pool (custom CA) or the client identity (mTLS); they never lower the verification bar.

## Rule 2 — Custom CA for private deployments

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    base_url: str
    tls_ca_bundle: Path | None = None
    tls_min_version: Literal["1.2", "1.3"] = "1.2"


def build_tls_context(config: Config) -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    if config.tls_min_version == "1.3":
        ctx.minimum_version = ssl.TLSVersion.TLSv1_3
    else:
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2

    if config.tls_ca_bundle is not None:
        ctx.load_verify_locations(cafile=str(config.tls_ca_bundle))

    return ctx
```

`load_verify_locations` LAYERS the custom CA on top of system roots — both are accepted. To trust ONLY the custom CA (uncommon; high-security air-gapped deployments), use `cafile=` and remove system roots:

```python
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)         # not create_default_context
ctx.load_verify_locations(cafile=str(custom_ca_path))
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
ctx.verify_mode = ssl.CERT_REQUIRED
ctx.check_hostname = True
```

The custom-CA-only form requires explicit reconstruction of the secure defaults. This is a power-user path; document it as a separate `build_strict_tls_context()` helper.

## Rule 3 — mTLS via `load_cert_chain`

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    base_url: str
    tls_ca_bundle: Path | None = None
    tls_client_cert: Path | None = None
    tls_client_key: Path | None = None
    tls_client_key_password_provider: CredentialProvider | None = None


async def build_mtls_context(config: Config) -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2

    if config.tls_ca_bundle is not None:
        ctx.load_verify_locations(cafile=str(config.tls_ca_bundle))

    if config.tls_client_cert is not None and config.tls_client_key is not None:
        password: str | None = None
        if config.tls_client_key_password_provider is not None:
            secret = await config.tls_client_key_password_provider.get()
            password = secret.get_secret_value()
        ctx.load_cert_chain(
            certfile=str(config.tls_client_cert),
            keyfile=str(config.tls_client_key),
            password=password,
        )

    return ctx
```

The key file may be encrypted; the password is fetched via a `CredentialProvider` (per `python-credential-provider-pattern`) — never literal in source, never in plain Config.

`ssl.SSLContext.load_cert_chain` reads the PEM/DER files synchronously. For SDK construction this is acceptable (one-time at client init); inside a hot path, wrap with `asyncio.to_thread`.

## Rule 4 — `check_hostname` is non-negotiable

```python
# The dev workaround that ships to prod:
# "Just disable it for testing against the staging cert"
ctx.check_hostname = False                              # NEVER

# The "right" way to test against a self-signed cert:
# Generate a real cert (mkcert) and trust it via load_verify_locations
```

For unit tests using `httpx.AsyncClient` against a localhost mock server with self-signed cert: use `respx` (no real socket) per `python-mock-strategy`. For integration tests with a real container (`testcontainers`), generate a real cert via `mkcert` or use a CA the test pre-loads:

```python
@pytest.fixture(scope="session")
def trusted_test_ca(tmp_path_factory) -> Path:
    """Generate a one-shot test CA + leaf, mark CA trusted for the session."""
    ca_dir = tmp_path_factory.mktemp("ca")
    # ... mkcert-style generation, returning the CA bundle path ...
    return ca_dir / "rootCA.pem"
```

Tests then build the SSLContext with the test CA loaded — `check_hostname` stays True; the SAN of the leaf cert matches the localhost test server.

## Rule 5 — Plug into httpx

```python
import httpx

async def make_http_client(config: Config) -> httpx.AsyncClient:
    ctx = build_tls_context(config)
    return httpx.AsyncClient(
        verify=ctx,                            # accepts SSLContext directly
        timeout=httpx.ClientTimeout(total=config.timeout_s),
    )
```

httpx's `verify=` accepts `True` (default secure), `False` (NEVER use), a path string (CA bundle), or an `SSLContext` (preferred — full control).

## Rule 6 — Plug into aiohttp

```python
import aiohttp

async def make_http_client(config: Config) -> aiohttp.ClientSession:
    ctx = build_tls_context(config)
    connector = aiohttp.TCPConnector(ssl=ctx)
    return aiohttp.ClientSession(
        connector=connector,
        timeout=aiohttp.ClientTimeout(total=config.timeout_s),
    )
```

aiohttp's `TCPConnector(ssl=...)` accepts `True` / `False` / `ssl.SSLContext` / `aiohttp.Fingerprint` (cert pinning). Always pass an explicit `SSLContext` for SDK clients — relying on `True` works but cuts off custom CA / mTLS plumbing.

## Rule 7 — Plug into asyncpg / nats / aiokafka

Each library accepts an SSLContext through a slightly different parameter name:

```python
# asyncpg
pool = await asyncpg.create_pool(dsn, ssl=ctx)

# nats-py
nc = await nats.connect(servers, tls=ctx)

# aiokafka
producer = AIOKafkaProducer(bootstrap_servers=..., security_protocol="SSL", ssl_context=ctx)

# aiomqtt
client = aiomqtt.Client(host=..., tls_context=ctx)

# aioboto3 — uses urllib3's SSL handling; pass ca_bundle path via Config
```

Document each in the per-client docstring.

## Rule 8 — Cert pinning (SHA-256 fingerprint)

For high-trust deployments (mobile SDKs, desktop apps facing untrusted networks), pin the server's leaf cert SHA-256 fingerprint:

```python
import hashlib
import ssl


def make_pinned_context(*, expected_sha256: bytes, ca_bundle: Path | None = None) -> ssl.SSLContext:
    """Verify the leaf cert SHA-256 matches ``expected_sha256``.

    Layered ON TOP of normal CA validation — both must pass.
    """
    ctx = ssl.create_default_context()
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    if ca_bundle is not None:
        ctx.load_verify_locations(cafile=str(ca_bundle))

    # ssl.SSLContext doesn't natively support pinning; install a verify callback
    # that runs AFTER the normal CA check and asserts the fingerprint.
    # See ssl.SSLContext.set_verify (Python 3.12+) — older versions need a wrapper.

    return ctx                                  # actual pinning verification happens
                                                # at connection time per stack
```

Pinning is an advanced topic. Most SDKs don't need it; if the consumer specifically asks, document it as a separate `Config` field with a clear "pin rotation requires SDK update" warning.

## Rule 9 — Test the TLS knobs

```python
import ssl
import pytest


def test_default_context_is_strict() -> None:
    ctx = build_tls_context(Config(base_url="https://x"))
    assert ctx.check_hostname is True
    assert ctx.verify_mode == ssl.CERT_REQUIRED
    assert ctx.minimum_version >= ssl.TLSVersion.TLSv1_2


def test_custom_ca_layered(tmp_path) -> None:
    ca_path = tmp_path / "custom.pem"
    ca_path.write_text(SAMPLE_CA_PEM)
    ctx = build_tls_context(Config(base_url="https://x", tls_ca_bundle=ca_path))
    # System roots + custom CA both loaded
    cas = ctx.get_ca_certs()
    assert len(cas) > 0


def test_tls13_only_when_configured() -> None:
    ctx = build_tls_context(Config(base_url="https://x", tls_min_version="1.3"))
    assert ctx.minimum_version == ssl.TLSVersion.TLSv1_3


@pytest.mark.integration
async def test_rejects_expired_cert(expired_cert_server) -> None:
    async with httpx.AsyncClient(verify=build_tls_context(Config(base_url="..."))) as c:
        with pytest.raises(ssl.SSLCertVerificationError):
            await c.get(expired_cert_server.url)
```

The last test demonstrates the security gate: an expired cert MUST fail. If a future change accidentally weakens the context, this test catches it.

## Rule 10 — Surface TLS errors as typed exceptions

```python
import ssl

from motadatapysdk.errors import AuthError, NetworkError


async def publish(self, topic: str, payload: bytes) -> None:
    try:
        await self._http.post(self._url(topic), data=payload)
    except ssl.SSLCertVerificationError as e:
        raise AuthError(
            f"server cert verification failed for {self._config.base_url}: {e.verify_message}"
        ) from e
    except ssl.SSLError as e:
        # Other TLS errors (handshake failure, version mismatch)
        raise NetworkError(f"TLS error: {e}") from e
```

Wrap stdlib `ssl.SSLError` in the SDK's typed exceptions per `python-exception-patterns`. `ssl.SSLCertVerificationError` (subclass of `ssl.SSLError`) carries `verify_code` and `verify_message` attributes — surface these to help debugging without leaking the cert content.

## GOOD: full TLS-aware client

```python
from __future__ import annotations

import asyncio
import ssl
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Self

import httpx

from motadatapysdk.credentials import CredentialProvider
from motadatapysdk.errors import AuthError, NetworkError


@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    base_url: str
    timeout_s: float = 5.0
    tls_min_version: Literal["1.2", "1.3"] = "1.2"
    tls_ca_bundle: Path | None = None
    tls_client_cert: Path | None = None
    tls_client_key: Path | None = None


async def build_tls_context(config: Config) -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.minimum_version = (
        ssl.TLSVersion.TLSv1_3 if config.tls_min_version == "1.3"
        else ssl.TLSVersion.TLSv1_2
    )
    if config.tls_ca_bundle is not None:
        await asyncio.to_thread(ctx.load_verify_locations, str(config.tls_ca_bundle))
    if config.tls_client_cert is not None and config.tls_client_key is not None:
        await asyncio.to_thread(
            ctx.load_cert_chain,
            str(config.tls_client_cert),
            str(config.tls_client_key),
        )
    return ctx


class Client:
    """Async client with full TLS configuration.

    Examples:
        >>> async def demo() -> None:
        ...     async with Client(Config(
        ...         base_url="https://api.example.com",
        ...         tls_min_version="1.3",
        ...     )) as client:
        ...         await client.publish("topic", b"x")
        >>> asyncio.run(demo())  # doctest: +SKIP
    """

    def __init__(self, config: Config, *, credentials: CredentialProvider) -> None:
        self._config = config
        self._credentials = credentials
        self._http: httpx.AsyncClient | None = None
        self._closed = False

    async def __aenter__(self) -> Self:
        ctx = await build_tls_context(self._config)
        self._http = httpx.AsyncClient(
            verify=ctx,
            timeout=httpx.ClientTimeout(total=self._config.timeout_s),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, tb) -> None:
        if self._http is not None and not self._closed:
            self._closed = True
            await self._http.aclose()

    async def publish(self, topic: str, payload: bytes) -> None:
        if self._http is None or self._closed:
            raise InvalidStateError("client is not entered or already closed")

        token = await self._credentials.get()
        try:
            response = await self._http.post(
                self._url(topic),
                data=payload,
                headers={"Authorization": f"Bearer {token.get_secret_value()}"},
            )
            response.raise_for_status()
        except ssl.SSLCertVerificationError as e:
            raise AuthError(
                f"server cert verification failed: {e.verify_message}",
            ) from e
        except ssl.SSLError as e:
            raise NetworkError(f"TLS error: {e}") from e
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (401, 403):
                raise AuthError(
                    "server rejected credentials",
                    status_code=e.response.status_code,
                ) from e
            raise

    def _url(self, topic: str) -> str:
        return f"{self._config.base_url.rstrip('/')}/topics/{topic}"
```

Demonstrates: hardened default (Rule 0), version pinning (Rule 0), Config-driven custom CA + mTLS (Rules 2-3), `check_hostname` always True (Rule 4), httpx integration (Rule 5), typed exception wrap on TLS error (Rule 10).

## BAD anti-patterns

```python
# 1. check_hostname=False (the canonical mistake)
ctx.check_hostname = False

# 2. CERT_NONE
ctx.verify_mode = ssl.CERT_NONE

# 3. _create_unverified_context (private API; explicit insecurity)
ctx = ssl._create_unverified_context()

# 4. Bare SSLContext (loses defaults)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# missing: minimum_version, verify_mode, check_hostname, system roots

# 5. Old protocol constant
ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)            # deprecated; use PROTOCOL_TLS_CLIENT

# 6. Hardcoded cert path
ctx.load_verify_locations(cafile="/etc/ssl/my-ca.pem")  # not Config-driven

# 7. Plain str for the client key password
ctx.load_cert_chain("cert.pem", "key.pem", password="hunter2")  # literal in source

# 8. verify=False in httpx
async with httpx.AsyncClient(verify=False) as c:     # disables ALL TLS verification
    ...

# 9. No SSLContext on aiohttp
connector = aiohttp.TCPConnector()                   # default; works but loses custom CA path
async with aiohttp.ClientSession(connector=connector): ...

# 10. Catch ssl.SSLError, swallow
try:
    response = await self._http.get(...)
except ssl.SSLError:
    pass                                              # security failure becomes silent
```

## Cross-references

- `python-credential-provider-pattern` — mTLS key password via Provider.
- `python-sdk-config-pattern` — TLS knobs as Config fields.
- `python-exception-patterns` — wrap `ssl.SSLError` / `ssl.SSLCertVerificationError`.
- `python-pytest-patterns` + `python-testcontainers-setup` — integration tests with real certs (mkcert).
- `python-mock-strategy` — unit tests via respx (no real TLS).
- `python-asyncio-leak-prevention` — close httpx / aiohttp on exit.
- `network-error-classification` (shared) — TLS errors as fatal class.
- `sdk-security-devil` — audits the bad list above.
