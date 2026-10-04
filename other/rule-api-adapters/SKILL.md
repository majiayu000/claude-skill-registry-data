---
name: rule-api-adapters
description: MANDATORY when editing files matching ["api/src/adapters/**/*.py"]. When working on external service adapters in api/src/adapters/
---

# API Adapters Rules

## Config Pattern

ALWAYS define adapter configuration as a class inheriting from `PydanticBaseEnvConfig`. ALWAYS use an env prefix to namespace environment variables (e.g., `S3_`, `OPENSEARCH_`). NEVER read environment variables directly with `os.getenv()` in adapter code.

Example from codebase:
```python
# From api/src/adapters/search/opensearch_config.py
from src.util.env_config import PydanticBaseEnvConfig

class OpensearchConfig(PydanticBaseEnvConfig):
    model_config = SettingsConfigDict(env_prefix="OPENSEARCH_")

    host: str = "localhost"
    port: int = 9200
    use_ssl: bool = True
    namespace: str = ""
```

## Retry Logic

ALWAYS use `tenacity` for retry logic on external service calls. ALWAYS use `@retry` with `stop=stop_after_attempt(N)` and `wait=wait_random_exponential()`. NEVER implement custom retry loops. NEVER retry on non-transient errors (4xx client errors).

Example from codebase:
```python
from tenacity import retry, stop_after_attempt, wait_random_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(multiplier=1, max=10),
)
def fetch_from_external_service(self, request_data: dict) -> dict:
    response = self.client.post(self.endpoint, json=request_data)
    response.raise_for_status()
    return response.json()
```

## Factory Pattern

ALWAYS use factory functions or classes for adapter instantiation when the adapter has multiple implementations (e.g., real client vs mock client). NEVER instantiate adapters with complex configuration inline.

Example from codebase:
```python
# From api/src/adapters/sam_gov/factory.py pattern
def get_sam_gov_client(config: SamGovConfig) -> BaseSamGovClient:
    if config.use_mock:
        return MockSamGovClient(config)
    return SamGovClient(config)
```

## Mock Clients

ALWAYS provide dedicated mock client classes for testing (e.g., `MockLoginGovOAuthClient`). NEVER mock at the method level when a full mock client class exists. ALWAYS place mock clients adjacent to their real counterparts.

Example from codebase:
```python
# From api/src/adapters/oauth/login_gov/mock_login_gov_oauth_client.py
class MockLoginGovOAuthClient(BaseLoginGovOAuthClient):
    def get_login_url(self, state: str, nonce: str) -> str:
        return f"http://localhost:5001/authorize?state={state}&nonce={nonce}"

    def get_token(self, auth_code: str) -> dict:
        return {"access_token": "mock-token", "id_token": "mock-id-token"}
```

## Client Class Structure

ALWAYS encapsulate external API communication in a client class. ALWAYS accept a config object in the constructor. NEVER expose raw HTTP clients (requests, httpx) to calling code. ALWAYS return typed response objects, not raw dicts.

Example from codebase:
```python
# From api/src/adapters/s3_adapter.py pattern
class S3Adapter:
    def __init__(self, config: S3Config):
        self.config = config
        self.client = boto3.client("s3", **config.boto_kwargs())

    def upload_file(self, key: str, body: bytes) -> str:
        self.client.put_object(Bucket=self.config.bucket, Key=key, Body=body)
        return key
```

## Session Management

ALWAYS pass database session objects explicitly through adapter methods when database access is needed. NEVER create database sessions inside adapters. NEVER store sessions as instance variables.

## Error Mapping

ALWAYS map external service errors to internal exception types. NEVER let raw boto3, requests, or third-party exceptions propagate to service layer code. ALWAYS log the original error before re-raising.

Example from codebase:
```python
from botocore.exceptions import ClientError

def get_object(self, key: str) -> bytes:
    try:
        response = self.client.get_object(Bucket=self.config.bucket, Key=key)
        return response["Body"].read()
    except ClientError as e:
        logger.error(
            "S3 get_object failed",
            extra={"key": key, "error_code": e.response["Error"]["Code"]},
        )
        raise StorageError(f"Failed to retrieve {key}") from e
```

## Adapter Boundaries

NEVER call external services directly from the service layer — ALWAYS go through an adapter. NEVER import adapter implementation details into route or service code — only import the adapter interface/base class.

## Type Decorators

ALWAYS place custom SQLAlchemy type decorators in `api/src/adapters/db/type_decorators/`. NEVER define type decorators inline in model files.

## Logging

ALWAYS begin every adapter module with `logger = logging.getLogger(__name__)`. ALWAYS use static log message strings with `extra={}` for dynamic values. NEVER log credentials, tokens, or PII. ALWAYS log external service call outcomes (success/failure) with relevant identifiers.

---

## Context Enrichment

When generating significant adapter code (new adapter, new external integration, retry logic), enrich your context:
- Call `get_architecture_section("api")` from the `simpler-grants-context` MCP server to understand adapter layer principles
- Call `get_rule_detail("api-services")` for how services consume adapters
- Call `get_rule_detail("api-error-handling")` for error mapping patterns
- Call `get_rule_detail("cross-domain")` for structured logging conventions
- Consult **Compound Knowledge** for indexed documentation on adapter patterns

## Related Rules

When working on adapters, also consult these related rules:
- **`api-services.mdc`** — service functions that consume adapters
- **`api-tasks.mdc`** — background tasks that use adapters (S3, SQS, Pinpoint)
- **`api-search.mdc`** — OpenSearch adapter and query patterns
- **`api-error-handling.mdc`** — error mapping and logging
- **`cross-domain.mdc`** — structured logging, no PII in logs

## Specialist Validation

When generating or significantly modifying adapter code:

**For simple changes (< 20 lines, config update, minor method change):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new adapter method, retry logic modification):**
Invoke `codebase-conventions-reviewer` to validate against project conventions.

**For complex changes (new external integration, new adapter class, authentication flow):**
Invoke the following specialists (run in parallel where possible):
- `security-sentinel` — validate credential handling, secret management, auth flows
- `architecture-strategist` — validate adapter boundaries and interface design
- `kieran-python-reviewer` — Python-specific quality review
