---
name: litestar-autowire
description: "Auto-activate for litestar_autowire, AutowirePlugin, AutowireConfig, domain_packages, AutowireIntegration, AutowireLoader, or clear_autowire_cache. Not for manual Router composition — use explicit routes."
---

# litestar-autowire

`litestar-autowire` 0.2.0 discovers Litestar controllers and event listeners
from domain packages. It can also load optional integration modules without
turning application setup into a central list of every domain component.

Use Autowire when the project already groups features into stable Python
packages. Keep manual `Router` and plugin composition when the app is small,
route registration is intentionally explicit, or packages do not follow a
consistent convention.

## Code Style Rules

- Configure dotted package roots with `domain_packages`.
- Import public APIs from `litestar_autowire`.
- Keep controllers and listeners in their owning domain package.
- Keep route handlers and listeners async when they perform I/O.
- Configure third-party loaders via `integrations` (`DishkaIntegration()`, `QueuesIntegration()`).
- Configure Dishka and Litestar Queues separately; Autowire only discovers or
  wraps their domain-owned components.
- Call `clear_autowire_cache()` when tests create, replace, or remove modules.

## Quick Reference

### Install

```bash
pip install litestar-autowire==0.2.0
```

Install only the integrations already used by the project:

```bash
pip install "litestar-autowire[dishka]==0.2.0"
pip install "litestar-autowire[queues]==0.2.0"
```

### Domain layout

```text
my_app/
└── domains/
    ├── accounts/
    │   ├── controllers.py
    │   ├── events.py
    │   └── jobs.py
    └── billing/
        └── routes.py
```

Regular packages and PEP 420 namespace packages are supported. Autowire checks
the configured root and each direct child package. Read
[Discovery](references/discovery.md) before changing module conventions or
debugging a missing component.

### App setup

```python
from litestar import Litestar
from litestar_autowire import AutowireConfig, AutowirePlugin

autowire = AutowirePlugin(
    AutowireConfig(domain_packages=["my_app.domains"]),
)

app = Litestar(plugins=[autowire])
```

The default component modules are:

| Component | Module names | Enabled |
| --- | --- | --- |
| Controllers | `controllers`, `routes`, `controller`, `route` | Yes |
| Event listeners | `events`, `listeners` | Yes |
| Litestar Queues tasks | `jobs` | Only with `integrations=["queues"]` |

`AutowireConfig` fields (all constructor arguments are keyword-only):

| Field | Default | Contract |
| --- | --- | --- |
| `domain_packages` | `()` | `str \| Iterable[str]` normalized to `tuple[str, ...]` |
| `integrations` | `()` | Built-in names (`"dishka"`, `"queues"`) or `AutowireIntegration` objects |
| `discover_controllers` | `True` | Register discovered `Controller` subclasses |
| `discover_listeners` | `True` | Register discovered `EventListener` instances |
| `controller_modules` | `("controllers", "routes", "controller", "route")` | `str \| Iterable[str]` normalized to `tuple[str, ...]` |
| `listener_modules` | `("events", "listeners")` | `str \| Iterable[str]` normalized to `tuple[str, ...]` |
| `task_modules` | `("jobs",)` | `str \| Iterable[str]` normalized to `tuple[str, ...]` |
| `router_class` | `None` | Optional router wrapper (`litestar.Router` or compatible type) |
| `before_request` | `None` | Optional hook attached to the wrapper router |
| `after_response` | `None` | Optional hook attached to the wrapper router |
| `force_reload_tasks` | `False` | Passed to `litestar_queues.discover_tasks(force_reload=...)` |
| `log_discovered` | `True` | Defer discovery summary logs to the Litestar startup hook |

Use `config.integration_enabled(name)` to check whether an integration with `name` is configured.

Customize module names without changing the domain layout:

```python
config = AutowireConfig(
    domain_packages=["my_app.domains"],
    controller_modules=["http"],
    listener_modules=["subscribers"],
    discover_listeners=False,
)
```

### Router selection

By default, discovered controller classes are appended directly to
`AppConfig.route_handlers`. Set `router_class=Router` when the project needs a
wrapper for router-level `before_request` or `after_response` hooks:

```python
from litestar import Router
from litestar_autowire import AutowireConfig

config = AutowireConfig(
    domain_packages=["my_app.domains"],
    router_class=Router,
    before_request=set_request_context,
    after_response=record_response,
)
```

The wrapper is constructed with `path="/"`, the discovered controller classes,
and the configured hooks. Use `integrations=["dishka"]` instead when the
project already uses Dishka and needs `DishkaRouter`. See
[Integrations](references/integrations.md).

<workflow>

## Workflow

1. Inspect the project layout and confirm domains are importable package roots.
2. Choose Autowire only when domain packages follow consistent controller or
   listener module conventions.
3. Register one `AutowirePlugin(AutowireConfig(...))` in the app plugin list.
4. Keep the default module names or configure explicit module-name tuples.
5. Enable only integrations already present in the project stack.
6. Configure Dishka or Litestar Queues through their own application plugins.
7. Test discovery, error propagation, and cache isolation with the patterns in
   [Testing](references/testing.md).

</workflow>

<guardrails>

## Guardrails

- **Do not describe Autowire as recursive domain discovery.** It discovers the
  configured root and direct feature children; component modules may themselves
  contain importable leaf modules.
- **Do not claim arbitrary route-handler discovery.** Autowire registers
  `Controller` subclasses and `EventListener` objects.
- **Do not imply queue tasks are enabled by default.** The `queues` integration
  must be selected and its optional dependency installed.
- **Do not suppress dependency import failures.** Only an absent configured
  package or absent target component module is skipped.
- **Do not use both a custom `router_class` and expect Dishka to replace it.**
  `DishkaIntegration` preserves an already selected router class.
- **Do not give custom integrations the names `dishka` or `queues`.** Built-in
  name collisions fail during configuration.
- **Do not reuse stale discovery state in tests or reload tooling.** Clear the
  process-local caches before rediscovery.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] `domain_packages` contains importable dotted package roots.
- [ ] The configured roots and component module names match the source layout.
- [ ] Controller classes are defined in the discovered module, not merely
  re-exported into it.
- [ ] Queue task discovery is enabled only with the Queues extra and integration.
- [ ] Dishka and Litestar Queues retain their own application configuration.
- [ ] Custom integrations satisfy `AutowireIntegration` and use unique names.
- [ ] Router hooks are paired with a compatible `router_class`.
- [ ] Tests call `clear_autowire_cache()` around dynamic module changes.
- [ ] Missing dependency imports still fail instead of silently dropping a
  domain.

</validation>

<example>

## Example

```python
from litestar import Controller, get


class AccountController(Controller):
    path = "/accounts"

    @get()
    async def list_accounts(self) -> list[dict[str, str]]:
        return [{"name": "primary"}]
```

```python
from litestar import Litestar
from litestar_autowire import AutowireConfig, AutowirePlugin

app = Litestar(
    plugins=[
        AutowirePlugin(
            AutowireConfig(
                domain_packages=["my_app.domains"],
                discover_controllers=True,
                discover_listeners=True,
            )
        )
    ],
)
```

Autowire imports `my_app.domains.accounts.controllers`, registers
`AccountController`, and checks the configured listener module names. It does
not load `jobs.py` until the `queues` integration is selected.

</example>

## References Index

- [Discovery](references/discovery.md) — package traversal, PEP 420 behavior,
  component selection, caches, and import failures
- [Integrations](references/integrations.md) — custom integrations,
  `AutowireLoader`, router selection, Dishka, and Litestar Queues
- [Testing](references/testing.md) — deterministic cache isolation and
  package-discovery tests
- [Litestar Routing](../litestar/references/handlers.md) — controller and manual
  router composition
- [Litestar Plugins](../litestar/references/plugins.md) — application plugin wiring
- [Litestar DI](../litestar/references/di-and-dishka.md) — built-in DI and Dishka selection
- [Litestar Queues](../litestar-queues/SKILL.md) — queue configuration, tasks,
  and workers
- [Litestar Testing](../litestar-testing/SKILL.md) — Litestar test clients and
  dependency overrides

## Official References

- <https://github.com/cofin/litestar-autowire/releases/tag/v0.2.0>
- <https://github.com/cofin/litestar-autowire/tree/v0.2.0/litestar_autowire>
- <https://github.com/cofin/litestar-autowire/blob/v0.2.0/tests/unit/test_autowire_plugin.py>

## Shared Styleguide Baseline

- [General](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
- [Testing](../litestar-styleguide/references/testing.md)
