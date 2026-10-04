---
name: litestar
description: "Auto-activate for Litestar, Controller, Router, @get/@post, FromPath, MsgspecDTO, OpenAPIConfig, Provide, FromDishka, Guard, ASGIMiddleware, HTTPException, ChannelsPlugin, or WebSocket. Not for standalone libs."
---

# Litestar Core Framework & Ecosystem Hub

Use this skill for all core **Litestar** framework subsystems (application composition, routing, controllers, parameters, DTOs, OpenAPI, dependency injection, Dishka integration, authentication/guards, middleware, exception handling, plugin protocols, WebSockets, Channels/SSE, typed settings, and CRUD data services/pagination) and to route to standalone Litestar ecosystem skills.

This guidance targets the released Litestar 2.24.0 contract. Do not copy unreleased `main` APIs into consumer examples.

## Code Style Rules

- Prefer first-party Litestar ecosystem packages (`litestar-granian`, `advanced-alchemy`, `sqlspec`, `msgspec`, `litestar-saq`, `litestar-queues`, `litestar-vite`, `litestar-autowire`, `litestar-security`, `litestar-email`, `litestar-mcp`, `litestar-htmx`) and match the project's existing stack for data access (`advanced-alchemy` vs `sqlspec`), DI (`Provide` vs `Dishka`), settings (`dataclass` vs `pydantic-settings`), background jobs (`litestar-saq` vs `litestar-queues`), and Channels backend (`Memory`, `Redis`, `AsyncPg`/`PsycoPg`, `SQLSpec`).
- Keep `Litestar(...)` app setup and route handlers thin: group domain routes into `Controller` / `Router` hierarchies (`urls.py` + `controllers/` + `services.py` + `schemas.py` + `dependencies.py` + `guards.py`), and centralize multi-domain wiring in `ApplicationCore(InitPluginProtocol, CLIPluginProtocol)` + `create_app() -> Litestar` (`litestar-fullstack` / `litestar-sqlstack` pattern).
- Use Litestar 2.22–2.24 explicit annotations: `FromPath[T]`, `FromQuery[T]`, `FromHeader[T]`, `FromCookie[T]` (or `PathParameter`, `QueryParameter`, `HeaderParameter`, `CookieParameter` when constraints or wire names are needed), `JSONBody[T]`, `MsgPackBody[T]`, `MultipartBody[T]`, `URLEncodedBody[T]`, `NamedDependency[T]`, and `SkipValidation[T]`. Never introduce implicit dependencies or deprecated `litestar.params.Dependency`.
- Define explicit `msgspec.Struct` (camelCase wire format via `rename="camel"`) or `MsgspecDTO` / `SQLAlchemyDTO` / `DataclassDTO` boundary contracts (`dto` and `return_dto`) on routes and controllers; never expose raw ORM models directly without a write-safe DTO.
- Enforce authentication via `AbstractAuthenticationMiddleware` or first-party `JWTAuth` / `JWTCookieAuth` / `SessionAuth`, and enforce authorization in `Guard` functions `(connection: ASGIConnection, route_handler: BaseRouteHandler) -> None | Awaitable[None]` or [`litestar-security`](../litestar-security/SKILL.md) decorators — never inside route handler bodies.
- Prefer built-in middleware configs (`CORSConfig`, `CSRFConfig`, `AllowedHostsConfig`, `CompressionConfig`, `RateLimitConfig`, `ResponseCacheConfig`, `LoggingMiddlewareConfig`) over custom middleware, and subclass `ASGIMiddleware` (`litestar.middleware.ASGIMiddleware`) with `scopes` and `exclude` filters for custom cross-cutting concerns.
- Raise domain-specific `ApplicationError` subclasses in services and map them to HTTP responses (or RFC 9457 Problem Details) in `exception_handlers`; import OpenTelemetry, Prometheus, Structlog, and template plugins from `litestar.plugins.*` (never deprecated `litestar.contrib.*`).
- Use async I/O for all request handlers, WebSocket/SSE streams, service/repository methods, stores, and external clients.

## Quick Reference

### Core Framework Subsystems (This Skill)

| Subsystem | Key Symbols / Patterns | Reference |
| --- | --- | --- |
| App Composition & Lifecycle | `Litestar(...)`, `AppConfig`, `ApplicationCore`, `lifespan`, `State`, `ImmutableState`, 2.22–2.24 contracts | [app-and-lifecycle.md](references/app-and-lifecycle.md) |
| CLI & Project Config | Autodiscovery, `LITESTAR_*` env vars, `litestar run`/`info`/`routes`/`schema`/`sessions`, `CLIPlugin`, `litestar.toml` | [cli-and-config.md](references/cli-and-config.md) |
| Route Handlers & Controllers | `@get`/`@post`/`@put`/`@patch`/`@delete`, `Controller`, `Router`, layered config inheritance | [handlers.md](references/handlers.md) |
| Parameters & Request Bodies | `FromPath`, `FromQuery`, `FromHeader`, `FromCookie`, `JSONBody`, `MsgPackBody`, `MultipartBody`, `URLEncodedBody`, `UploadFile` | [parameters.md](references/parameters.md) |
| Domain Package Layout | `domains/<name>/` structure, sub-controllers, full-stack domain wiring | [layout.md](references/layout.md) |
| DTOs & Boundary Contracts | `MsgspecDTO`, `SQLAlchemyDTO`, `DataclassDTO`, `DTOConfig`, `DTOData[T]`, `PatchDTO`, `SimpleDTO` | [dtos.md](references/dtos.md) |
| OpenAPI & Schema UI | `OpenAPIConfig`, Scalar/Swagger/Redoc/Stoplight/RapiDoc plugins, `ResponseSpec`, `Operation`, security schemes | [openapi.md](references/openapi.md) |
| Dependency Injection & Dishka | `Provide`, `NamedDependency[T]`, `SkipValidation[T]`, generator cleanup, `FromDishka[T]`, `setup_dishka` | [di-and-dishka.md](references/di-and-dishka.md) |
| Authentication & Guards | `Guard` callables, `ASGIConnection`, `JWTAuth`, `JWTCookieAuth`, `SessionAuth`, OAuth2, RBAC & tenant guards | [auth-and-guards.md](references/auth-and-guards.md) |
| Middleware & HTTP Security | `ASGIMiddleware`, `DefineMiddleware`, `CORSConfig`, `CSRFConfig`, `AllowedHostsConfig`, `CompressionConfig`, `RateLimitConfig` | [middleware.md](references/middleware.md) |
| Exceptions & Problem Details | `HTTPException` hierarchy, `ApplicationError` mapping, `exception_handlers`, `after_exception`, RFC 9457 | [exceptions.md](references/exceptions.md) |
| Plugin Protocols | `InitPlugin`, `CLIPluginProtocol`, `SerializationPluginProtocol`, `OpenAPISchemaPluginProtocol`, `DIPlugin`, `PydanticPlugin` | [plugins.md](references/plugins.md) |
| WebSockets | `@websocket`, `WebSocket` lifecycle, `@websocket_listener`, `@websocket_stream`, WS Dishka DI, WS guards, `stream_pubsub` | [websockets.md](references/websockets.md) |
| Channels & Server-Sent Events | `ChannelsPlugin` (`Memory`, `Redis`, `AsyncPg`, `PsycoPg`, `SQLSpec`), `ServerSentEvent`, `Stream`, `RealtimeEvent`, `RealtimePublisher` | [channels-and-sse.md](references/channels-and-sse.md) |
| Typed Settings & Env Config | `dataclass` + `get_env` vs `pydantic-settings`, `@lru_cache` factories, plugin config builders | [settings.md](references/settings.md) |
| Filters & Pagination | `create_filter_dependencies`, `FilterTypes`, `OffsetPagination`, `ClassicPagination`, cursor pagination, custom search | [filters-and-pagination.md](references/filters-and-pagination.md) |
| Data Services & Repositories | `SQLAlchemyAsyncRepositoryService` (`advanced-alchemy`) and `SQLSpecAsyncService` (`sqlspec`) CRUD services | [services-and-repos.md](references/services-and-repos.md) |
| Logging & Observability | `LoggingConfig`, `StructlogPlugin`, `OpenTelemetryPlugin`, `PrometheusConfig`, `PrometheusController` | [logging-and-observability.md](references/logging-and-observability.md) |
| Stores & Response Caching | `StoreRegistry`, `MemoryStore`, `FileStore`, `RedisStore`, `ValkeyStore`, `ResponseCacheConfig` | [stores-and-caching.md](references/stores-and-caching.md) |

### Standalone Ecosystem Skills

| Task | Skill |
| --- | --- |
| Convention-based domain-package discovery (`AutowirePlugin`, `domain_packages`) | [litestar-autowire](../litestar-autowire/SKILL.md) |
| `msgspec.Struct`, `Meta`, tagged unions, JSON/MsgPack encode/decode hooks | [msgspec](../msgspec/SKILL.md) |
| `SecurityPlugin`, `CurrentUser`, `Principal`, `@requires_role`/`@requires_scope`/`@requires_tenant` | [litestar-security](../litestar-security/SKILL.md) |
| SQLAlchemy ORM models, `SQLAlchemyPlugin`, Alembic migrations, repositories | [advanced-alchemy](../advanced-alchemy/SKILL.md) |
| SQL-first drivers, `SQLFileLoader`, query builders, ADK stores, data dictionary | [sqlspec](../sqlspec/SKILL.md) |
| Vite asset pipeline, HMR, TypeGen, SPA/hybrid modes, and Inertia.js (`InertiaConfig`, `component=`) | [litestar-vite](../litestar-vite/SKILL.md) |
| Server-rendered HTMX requests, partial templates, `HX-*` response helpers | [litestar-htmx](../litestar-htmx/SKILL.md) |
| Redis-backed background workers, queues, cron schedules (`litestar-saq`) | [litestar-saq](../litestar-saq/SKILL.md) |
| SQL/memory task queues, `@task`, `QueueService`, workers (`litestar-queues`) | [litestar-queues](../litestar-queues/SKILL.md) |
| Transactional email (`EmailPlugin`, SMTP/Resend/SendGrid/Mailgun/SES backends) | [litestar-email](../litestar-email/SKILL.md) |
| Model Context Protocol servers (`LitestarMCP`, `@mcp.tool`/`@mcp.resource`/`@mcp.prompt`) | [litestar-mcp](../litestar-mcp/SKILL.md) |
| Google ADK / LLM agent HTTP and SSE serving, tool calls, session services | [litestar-ai](../litestar-ai/SKILL.md) |
| Granian ASGI server plugin, runtime threads, HTTP/2, TLS, static mounts | [litestar-granian](../litestar-granian/SKILL.md) |
| `TestClient`, `AsyncTestClient`, `create_async_test_client`, handler/DI/Guard tests | [litestar-testing](../litestar-testing/SKILL.md) |
| Typed test data factories (`MsgspecFactory`, `ModelFactory`, `DataclassFactory`) | [polyfactory](../polyfactory/SKILL.md) |
| Docker database/service fixtures for integration tests (`pytest-databases`) | [pytest-databases](../pytest-databases/SKILL.md) |
| Wheels, PyApp standalone binaries, GitHub release matrices (`litestar-build`) | [litestar-build](../litestar-build/SKILL.md) |
| Containers, Cloud Run, GKE, Kubernetes, systemd, runtime servers (`litestar-deployment`) | [litestar-deployment](../litestar-deployment/SKILL.md) |
| Python/TypeScript/Litestar code style, linting, typing, and quality gates | [litestar-styleguide](../litestar-styleguide/SKILL.md) |

<workflow>

## Workflow

1. **Detect the project stack first**: inspect `pyproject.toml`, `litestar.toml`, existing domain packages, DI setup (`Provide` vs `Dishka`), data layer (`advanced-alchemy` vs `sqlspec`), settings (`dataclass` vs `pydantic-settings`), and auth (`JWTAuth`/`SessionAuth` vs `litestar-security`).
2. **Open the matching core reference** in `references/*.md` for any Litestar framework concern:
   - Routing, controllers, parameters, or domain layout -> [handlers.md](references/handlers.md), [parameters.md](references/parameters.md), [layout.md](references/layout.md)
   - DTOs, request/response schemas, or OpenAPI docs -> [dtos.md](references/dtos.md), [openapi.md](references/openapi.md)
   - Dependency injection or Dishka providers -> [di-and-dishka.md](references/di-and-dishka.md)
   - Auth backends, guards, middleware, or exception handlers -> [auth-and-guards.md](references/auth-and-guards.md), [middleware.md](references/middleware.md), [exceptions.md](references/exceptions.md)
   - Plugins, WebSockets, Channels/SSE, settings, or CRUD services/filters -> [plugins.md](references/plugins.md), [websockets.md](references/websockets.md), [channels-and-sse.md](references/channels-and-sse.md), [settings.md](references/settings.md), [filters-and-pagination.md](references/filters-and-pagination.md), [services-and-repos.md](references/services-and-repos.md)
   - App composition, CLI, logging/metrics/tracing, or stores/caching -> [app-and-lifecycle.md](references/app-and-lifecycle.md), [cli-and-config.md](references/cli-and-config.md), [logging-and-observability.md](references/logging-and-observability.md), [stores-and-caching.md](references/stores-and-caching.md)
3. **Open standalone ecosystem skills** when working on dedicated first-party packages (`advanced-alchemy`, `sqlspec`, `msgspec`, `litestar-vite`, `litestar-htmx`, `litestar-saq`, `litestar-queues`, `litestar-security`, `litestar-autowire`, `litestar-email`, `litestar-mcp`, `litestar-ai`, `litestar-granian`, `litestar-testing`, `polyfactory`, `pytest-databases`, `litestar-build`, `litestar-deployment`).
4. **Keep the stack consistent** across the feature: never mix two persistence layers, two DI containers, or two settings paradigms unless the repository already bridges them intentionally.

</workflow>

<guardrails>

## Guardrails

- Do not infer a new stack from examples — always match the current project's data layer, DI pattern, settings style, and auth mechanism first.
- Do not put authentication, authorization, SQL queries, environment parsing, or heavy background work directly inside route handlers; delegate to `Guard` callables, services/repositories, cached settings factories, and task queues.
- Do not use deprecated `StaticFilesConfig`, `litestar.contrib.*` plugins, `litestar.repository`, `litestar.params.Dependency`, or implicit dependency parameters.
- Do not expose ORM models directly in `dto` / `return_dto` without `exclude` / `include` field rules that prevent mass assignment and hidden relationship lazy-loads.
- Do not call `os.getenv()` inside request handlers or module-level code outside the settings module, and never hardcode secrets in source files.
- Do not call `start_subscription(..., history=N)` on Channels backends that do not implement history (`RedisChannelsPubSubBackend`, `AsyncPgChannelsBackend`, `PsycoPgChannelsBackend`).

</guardrails>

<validation>

## Validation Checkpoint

- [ ] Route handlers use explicit Litestar 2.24 parameter, body, and dependency markers (`FromPath[T]`, `FromQuery[T]`, `JSONBody[T]`, `NamedDependency[T]`, `SkipValidation[T]`).
- [ ] Request and response contracts use `msgspec.Struct` or `MsgspecDTO` / `SQLAlchemyDTO` with explicit field exclusions and `status_code` declarations.
- [ ] Authorization checks live in `Guard` functions (`ASGIConnection`, `BaseRouteHandler`) or `litestar-security` decorators, and domain exceptions map cleanly through `exception_handlers`.
- [ ] Built-in config objects (`CORSConfig`, `CSRFConfig`, `AllowedHostsConfig`, `CompressionConfig`, `LoggingConfig`, `OpenAPIConfig`, `ResponseCacheConfig`) are wired through `Litestar(...)` or `ApplicationCore.on_app_init`.
- [ ] Validation commands use `make` targets when editing skills in this repository.

</validation>

<example>

## Example

```python
import click
import msgspec
from litestar import Controller, Litestar, MediaType, Request, Response, get, post
from litestar.config.app import AppConfig
from litestar.config.cors import CORSConfig
from litestar.config.response_cache import ResponseCacheConfig
from litestar.connection import ASGIConnection
from litestar.datastructures import State
from litestar.di import NamedDependency, Provide
from litestar.dto import DTOConfig, MsgspecDTO
from litestar.exceptions import LitestarException, NotFoundException, PermissionDeniedException
from litestar.handlers.base import BaseRouteHandler
from litestar.logging import LoggingConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.params import FromPath, FromQuery, JSONBody
from litestar.plugins import CLIPluginProtocol, InitPluginProtocol
from litestar.status_codes import HTTP_201_CREATED, HTTP_409_CONFLICT
from litestar.stores.memory import MemoryStore
from litestar.stores.registry import StoreRegistry


class DuplicateSkuError(LitestarException):
    """Raised when an item SKU already exists."""

    def __init__(self, sku: str) -> None:
        self.sku = sku
        self.message = f"SKU '{sku}' already exists"
        super().__init__(self.message)


def duplicate_sku_exception_handler(
    request: Request[object, object, State],
    exc: DuplicateSkuError,
) -> Response[dict[str, object]]:
    """Map DuplicateSkuError to an HTTP 409 response."""
    return Response(
        media_type=MediaType.JSON,
        status_code=HTTP_409_CONFLICT,
        content={"detail": exc.message, "sku": exc.sku, "path": request.url.path},
    )


async def require_catalog_editor(
    connection: ASGIConnection[BaseRouteHandler, dict[str, object], object, State],
    _: BaseRouteHandler,
) -> None:
    """Verify the authenticated user has catalog write permission."""
    user = connection.scope.get("user")
    if not isinstance(user, dict) or "catalog:write" not in user.get("scopes", ()):
        raise PermissionDeniedException("Missing catalog:write scope")


class CatalogItem(msgspec.Struct, rename="camel"):
    """Serialized catalog item contract."""

    id: int
    sku: str
    name: str
    locale: str = "en"


class CreateCatalogItem(msgspec.Struct, rename="camel"):
    """Payload for creating a catalog item."""

    sku: str
    name: str


class CatalogItemReadDTO(MsgspecDTO[CatalogItem]):
    """Read DTO for CatalogItem responses."""

    config = DTOConfig(rename_strategy="camel")


class CatalogService:
    """Domain service managing catalog items."""

    async def fetch_item(self, item_id: int, locale: str) -> CatalogItem:
        if item_id <= 0:
            raise NotFoundException(f"Item {item_id} not found")
        return CatalogItem(id=item_id, sku=f"SKU-{item_id}", name="Widget", locale=locale)

    async def create_item(self, data: CreateCatalogItem) -> CatalogItem:
        if data.sku == "DUPLICATE":
            raise DuplicateSkuError(data.sku)
        return CatalogItem(id=1, sku=data.sku, name=data.name)


async def provide_catalog_service() -> CatalogService:
    """Provide request-scoped CatalogService."""
    return CatalogService()


class CatalogController(Controller):
    """HTTP controller for catalog operations."""

    path = "/catalog"
    tags = ["Catalog"]
    dependencies = {"catalog_service": Provide(provide_catalog_service)}
    return_dto = CatalogItemReadDTO

    @get("/{item_id:int}", cache=60)
    async def get_item(
        self,
        item_id: FromPath[int],
        catalog_service: NamedDependency[CatalogService],
        locale: FromQuery[str] = "en",
    ) -> CatalogItem:
        """Resolve path/query parameters and service dependency explicitly."""
        return await catalog_service.fetch_item(item_id=item_id, locale=locale)

    @post("/", guards=[require_catalog_editor], status_code=HTTP_201_CREATED)
    async def create_item(
        self,
        data: JSONBody[CreateCatalogItem],
        catalog_service: NamedDependency[CatalogService],
    ) -> CatalogItem:
        """Validate JSON payload, enforce guard, and delegate creation to service."""
        return await catalog_service.create_item(data)


class ApplicationCore(InitPluginProtocol, CLIPluginProtocol):
    """Reference architecture core plugin (litestar-fullstack / litestar-sqlstack)."""

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.route_handlers.append(CatalogController)
        app_config.exception_handlers[DuplicateSkuError] = duplicate_sku_exception_handler
        app_config.cors_config = CORSConfig(allow_origins=["https://app.example.com"])
        app_config.openapi_config = OpenAPIConfig(
            title="Catalog API",
            version="1.0.0",
            render_plugins=[ScalarRenderPlugin()],
        )
        app_config.stores = StoreRegistry(stores={"response_cache": MemoryStore()})
        app_config.response_cache_config = ResponseCacheConfig(default_expiration=60)
        app_config.logging_config = LoggingConfig(
            log_exceptions="always",
            disable_stack_trace={404, NotFoundException},
        )
        app_config.state = State({"service_name": "catalog-api"})
        return app_config

    def on_cli_init(self, cli: click.Group) -> None:
        _ = cli


def create_app() -> Litestar:
    """Compose the Litestar 2.24 application via ApplicationCore."""
    return Litestar(plugins=[ApplicationCore()])
```

</example>

## References Index

- [app-and-lifecycle.md](references/app-and-lifecycle.md)
- [auth-and-guards.md](references/auth-and-guards.md)
- [channels-and-sse.md](references/channels-and-sse.md)
- [cli-and-config.md](references/cli-and-config.md)
- [di-and-dishka.md](references/di-and-dishka.md)
- [dtos.md](references/dtos.md)
- [exceptions.md](references/exceptions.md)
- [filters-and-pagination.md](references/filters-and-pagination.md)
- [handlers.md](references/handlers.md)
- [layout.md](references/layout.md)
- [logging-and-observability.md](references/logging-and-observability.md)
- [middleware.md](references/middleware.md)
- [openapi.md](references/openapi.md)
- [parameters.md](references/parameters.md)
- [plugins.md](references/plugins.md)
- [services-and-repos.md](references/services-and-repos.md)
- [settings.md](references/settings.md)
- [stores-and-caching.md](references/stores-and-caching.md)
- [websockets.md](references/websockets.md)

## Official References

- <https://docs.litestar.dev/> - Litestar documentation
- <https://docs.litestar.dev/latest/reference/> - Litestar API reference
- <https://docs.litestar.dev/latest/release-notes/changelog.html> - Litestar 2.x changelog
- <https://github.com/litestar-org/litestar/tree/v2.24.0> - Audited Litestar 2.24.0 source
- <https://dishka.readthedocs.io/en/stable/integrations/litestar.html> - Dishka Litestar integration

## Shared Styleguide Baseline

- [General](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
