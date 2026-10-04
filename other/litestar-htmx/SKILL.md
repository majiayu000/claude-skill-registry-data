---
name: litestar-htmx
description: "Auto-activate for litestar_htmx, HTMXPlugin, HTMXConfig, HTMXRequest, HTMXTemplate, HXLocation, ReplaceUrl, TriggerEvent, HX-* headers, or Litestar partial HTML. Not for client-only HTMX or Litestar Vite JSON."
---

# litestar-htmx

`litestar-htmx` is the standalone Litestar integration for HTMX. Version 0.5.0
ships the `litestar_htmx` import package with request helpers, an optional
application plugin, template responses, and typed HTMX response-header helpers.

## Code Style Rules

- Import the integration from `litestar_htmx`, never the
  `litestar.plugins.htmx` compatibility re-export shim.
- Use `HTMXRequest` when handlers inspect HTMX request headers.
- Return template fragments from HTMX endpoints; keep full-page routes and
  fragment routes distinct.
- Use the response classes for `HX-*` headers; do not assemble those headers
  by hand.
- Keep browser-side HTMX extensions separate from this server package.

## Quick Reference

### Configure the plugin

```python
from litestar import Litestar
from litestar_htmx import HTMXPlugin

app = Litestar(
    route_handlers=[...],
    plugins=[HTMXPlugin()],
)
```

`HTMXPlugin()` is the convenience path: its `on_app_init` hook registers
`HTMXRequest` and all ten HTMX response classes in `app_config.signature_types`.
Its default `HTMXConfig(set_request_class_globally=True)` sets `HTMXRequest`
only when `app_config.request_class is None`.

Preserve an existing custom request class by extending `HTMXRequest`:

```python
from litestar_htmx import HTMXRequest


class ApplicationRequest(HTMXRequest):
    """Application request with HTMX helpers."""
```

If the application only needs response helpers, use
`HTMXConfig(set_request_class_globally=False)`. To inspect `request.htmx`,
configure `HTMXRequest` (or a subclass) as the application request class. The
plugin never replaces a request class already present in `AppConfig`.

The plugin itself is optional. Applications can instead set
`request_class=HTMXRequest` directly and return the response subclasses without
registering `HTMXPlugin`.

### Inspect request headers

`request.htmx` is always an `HTMXDetails` object. Its truth value is `True` only
when `HX-Request` is exactly `"true"`.

```python
from litestar import get
from litestar.response import Template
from litestar_htmx import HTMXRequest


@get("/items")
async def list_items(request: HTMXRequest) -> Template:
    template_name = "partials/item-list.html" if request.htmx else "pages/items.html"
    return Template(template_name=template_name, context={"items": []})
```

Available request helpers:

| Property | Source | Result |
| --- | --- | --- |
| `bool(request.htmx)` | `HX-Request` | Whether this is an HTMX request |
| `request.htmx.boosted` | `HX-Boosted` | `bool` |
| `request.htmx.current_url` | `HX-Current-URL` | `str \| None` |
| `request.htmx.current_url_abs_path` | `HX-Current-URL` | Same-origin path, query, and fragment, or `None` |
| `request.htmx.history_restore_request` | `HX-History-Restore-Request` | `bool` |
| `request.htmx.prompt` | `HX-Prompt` | `str \| None` |
| `request.htmx.target` | `HX-Target` | `str \| None` |
| `request.htmx.trigger` | `HX-Trigger` | `str \| None` |
| `request.htmx.trigger_name` | `HX-Trigger-Name` | `str \| None` |
| `request.htmx.triggering_event` | `Triggering-Event` | Decoded JSON value, or `None` |

`triggering_event` is supplied by HTMX's `event-header` extension and decoded
using the active route handler's `type_decoders`. Malformed JSON resolves to
`None`. Headers accompanied by `<Header>-URI-AutoEncoded: true` are URL-decoded
before use.

### Return template fragments with HTMX headers

`HTMXTemplate` extends Litestar's `Template`. Annotate handlers with
`Template`, then pass normal `Template` arguments plus HTMX-specific options:

```python
from litestar import get
from litestar.response import Template
from litestar_htmx import HTMXTemplate


@get("/items/fragment")
async def item_list() -> Template:
    return HTMXTemplate(
        template_name="partials/item-list.html",
        context={"items": []},
        push_url=False,
        re_swap="outerHTML",
        re_target="#item-list",
        trigger_event="itemsLoaded",
        params={"count": 0},
        after="receive",
    )
```

`trigger_event`, `params`, and `after` form one event declaration. When
`trigger_event` is set, `after` must be `"receive"`, `"settle"`, or `"swap"`
(leaving `after=None` raises `ImproperlyConfiguredException`). `HTMXTemplate`
supports `push_url`, `re_swap`, `re_target`, `trigger_event`, `params`, and
`after`; it does not accept `replace_url`.

### Response helper signatures

All helpers are exported from `litestar_htmx` and
`litestar_htmx.response`.

| Helper | Constructor | Behavior |
| --- | --- | --- |
| `HXStopPolling` | `HXStopPolling()` | Returns status `286` (`HTMX_STOP_POLLING`) |
| `ClientRedirect` | `ClientRedirect(redirect_to)` | Status `200`; sets URL-quoted `HX-Redirect` and deletes `Location` |
| `ClientRefresh` | `ClientRefresh()` | Status `200`; sets `HX-Refresh: true` |
| `PushUrl` | `PushUrl(content, push_url, **response_kwargs)` | Status `200`; sets `HX-Push-Url` |
| `ReplaceUrl` | `ReplaceUrl(content, replace_url, **response_kwargs)` | Status `200`; sets `HX-Replace-Url` |
| `Reswap` | `Reswap(content, method, **response_kwargs)` | Sets `HX-Reswap` |
| `Retarget` | `Retarget(content, target, **response_kwargs)` | Sets `HX-Retarget` |
| `TriggerEvent` | `TriggerEvent(content, name, after, params=None, **response_kwargs)` | Sets `HX-Trigger`, `HX-Trigger-After-Settle`, or `HX-Trigger-After-Swap` |
| `HXLocation` | `HXLocation(redirect_to, source=None, event=None, target=None, select=None, swap=None, hx_headers=None, values=None, **response_kwargs)` | Status `200`; sets JSON in `HX-Location` and deletes `Location` |

Pass a URL `str` to `push_url` or `replace_url` to update history, or `False`
(or `"False"`) to emit `"false"` and prevent the history update. Do not pass
`True`: any `bool` value is serialized as `"false"`.

### Exported types and header enum

`litestar_htmx` (and `litestar_htmx.types`) exports the typing definitions and
header enum used across request and response helpers:

| Export | Kind | Definition / Values |
| --- | --- | --- |
| `HTMXHeaders` | `str, Enum` | Request and response header names (`REQUEST`, `BOOSTED`, `CURRENT_URL`, `HISTORY_RESTORE_REQUEST`, `PROMPT`, `TARGET`, `TRIGGER_ID`, `TRIGGER_NAME`, `TRIGGERING_EVENT`, `REDIRECT`, `REFRESH`, `PUSH_URL`, `REPLACE_URL`, `RE_SWAP`, `RE_TARGET`, `LOCATION`, `TRIGGER_EVENT`, `TRIGGER_AFTER_SETTLE`, `TRIGGER_AFTER_SWAP`) |
| `EventAfterType` | `Literal` | `"receive" \| "settle" \| "swap" \| None` |
| `PushUrlType` | `Union` | `str \| bool` (use URL `str` or `False`) |
| `ReSwapMethod` | `Literal` | `"innerHTML" \| "outerHTML" \| "beforebegin" \| "afterbegin" \| "beforeend" \| "afterend" \| "delete" \| "none" \| None` |
| `LocationType` | `TypedDict` | `path`, `source`, `event`, `target`, `select`, `swap`, `values`, `hx_headers` |
| `TriggerEventType` | `TypedDict` | `name`, `params`, `after` |
| `HtmxHeaderType` | `TypedDict(total=False)` | `location`, `redirect`, `refresh`, `push_url`, `replace_url`, `re_swap`, `re_target`, `trigger_event` |

### Soft navigation with `HXLocation`

Use `HXLocation` for an HTMX navigation request without a full-page reload.
`select` chooses a fragment from the fetched response before it is swapped:

```python
from litestar import post
from litestar_htmx import HXLocation


@post("/items")
async def create_item() -> HXLocation:
    return HXLocation(
        redirect_to="/items",
        source="#create-item",
        event="submit",
        target="#content",
        select="#item-list",
        swap="innerHTML",
        hx_headers={"X-View": "compact"},
        values={"created": "true"},
    )
```

The response uses status `200`, carries `HX-Location`, and removes the ordinary
`Location` header.

### Trigger an event while returning content

`TriggerEvent` requires the response `content`, event `name`, and `after`
phase:

```python
from litestar import post
from litestar_htmx import TriggerEvent


@post("/items")
async def create_item() -> TriggerEvent[str]:
    return TriggerEvent(
        content="<li>Saved</li>",
        name="itemCreated",
        after="swap",
        params={"id": 42},
        media_type="text/html",
    )
```

Prefer `HTMXTemplate` when the content is HTML assembled from application data.

### Litestar Vite is a separate client layer

The standalone package owns Python request parsing and response headers:

```python
from litestar_htmx import HTMXPlugin, HTMXRequest, HTMXTemplate
```

Litestar Vite's `hx-ext="litestar"` JSON templating and CSRF integration come
from the separate `litestar-vite-plugin/helpers` JavaScript export. They are not
installed, registered, or enabled by `HTMXPlugin()`. Use them only when the
project already uses Litestar Vite and needs client-side JSON swaps. See
[Litestar Vite Integration](references/litestar_vite.md).

<workflow>

## Workflow

1. Check the project's installed `litestar-htmx` version and existing request
   class.
2. Register `HTMXPlugin()` or set `request_class=HTMXRequest` directly. Extend
   `HTMXRequest` when the application needs custom request behavior.
3. Separate full-page endpoints from fragment endpoints. Branch on
   `request.htmx` only when one URL intentionally supports both.
4. Render fragments with `Template` or `HTMXTemplate`.
5. Select the narrow response helper matching the required HTMX header.
6. Configure CSRF protection for every state-changing HTMX request.
7. Test the response body, status, and exact `HX-*` header.
8. Add Litestar Vite's client extension only for bundled assets, CSRF header
   injection, or JSON templating.

</workflow>

<guardrails>

## Guardrails

- **Use `litestar_htmx`, never `litestar.plugins.htmx`.** The 0.5.0 package is a
  standalone distribution; `litestar.plugins.htmx` is only a compatibility
  re-export shim.
- **Pass every required response-helper argument.** `TriggerEvent` requires
  `content`, `name`, and a non-null `after` (`"receive"`, `"settle"`, or
  `"swap"`); `PushUrl`, `ReplaceUrl`, `Reswap`, and `Retarget` also require
  `content`.
- **Pass a URL `str` or `False` for `push_url` and `replace_url`.** Any boolean
  value (including `True`) is serialized as `"false"`.
- **Use `select=` on `HXLocation` to choose returned content.** Do not confuse
  it with `target=`, which chooses the receiving element.
- **Do not assume `HTMXPlugin` overrides an existing request class.** It
  preserves a non-null `AppConfig.request_class`.
- **Do not treat `request.htmx` as an optional object.** Test its truth value to
  identify HTMX requests.
- **Do not send a normal redirect for `HXLocation` or `ClientRedirect`.** These
  helpers return `200` with HTMX response headers and delete `Location`.
- **Do not attribute `hx-ext="litestar"` to `litestar-htmx`.** That browser
  extension ships with Litestar Vite's npm package.
- **Do not return unsanitized, concatenated HTML.** Render templates so escaping
  and template caching remain intact.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] Imports use `litestar_htmx`, not `litestar.plugins.htmx`
- [ ] `HTMXPlugin()` or `request_class=HTMXRequest` wires request helpers
- [ ] A custom global request class extends `HTMXRequest`
- [ ] Full pages and HTMX fragments have explicit boundaries
- [ ] `TriggerEvent` and `HTMXTemplate(trigger_event=...)` set `after` to `"receive"`, `"settle"`, or `"swap"`
- [ ] `PushUrl`, `ReplaceUrl`, and `HTMXTemplate(push_url=...)` pass a URL `str` or `False` (never `True`)
- [ ] `HXLocation.select` and `HXLocation.target` serve distinct purposes
- [ ] State-changing HTMX requests include the application's CSRF token
- [ ] Tests assert the exact status, body, and `HX-*` response header
- [ ] Litestar Vite client-extension guidance is identified as a separate layer

</validation>

<example>

## Example

Return a fragment, retarget the swap, prevent a history update, and verify the
HTMX response:

```python
from litestar import Controller, get
from litestar.response import Template
from litestar_htmx import HTMXRequest, HTMXTemplate


class ItemController(Controller):
    path = "/items"

    @get("/")
    async def index(self, request: HTMXRequest) -> Template:
        items = [{"id": 1, "name": "Widget"}]
        if request.htmx:
            return HTMXTemplate(
                template_name="partials/item-list.html",
                context={"items": items},
                re_target="#item-list",
                re_swap="outerHTML",
                push_url=False,
            )
        return Template(template_name="pages/items.html", context={"items": items})
```

```python
async def test_htmx_item_list(client) -> None:
    response = await client.get(
        "/items/",
        headers={"HX-Request": "true", "HX-Target": "item-list"},
    )

    assert response.status_code == 200
    assert response.headers["HX-Retarget"] == "#item-list"
    assert response.headers["HX-Reswap"] == "outerHTML"
    assert response.headers["HX-Push-Url"] == "false"
    assert "<html" not in response.text
```

</example>

## References Index

- **[Litestar Vite Integration](references/litestar_vite.md)** — Keep the
  standalone Python package distinct from Litestar Vite's browser extension.
- **[Litestar](../litestar/SKILL.md)** — Application setup, templates, and
  lifecycle fundamentals.
- **[Litestar Vite](../litestar-vite/SKILL.md)** — Asset bundling, template
  mode, HMR, and the client helper package.
- **[Litestar Testing](../litestar-testing/SKILL.md)** — Async clients and
  application fixtures.

## Official References

- <https://pypi.org/project/litestar-htmx/0.5.0/>
- <https://github.com/litestar-org/litestar-htmx/tree/v0.5.0/litestar_htmx>
- <https://github.com/litestar-org/litestar-htmx/blob/v0.5.0/litestar_htmx/request.py>
- <https://github.com/litestar-org/litestar-htmx/blob/v0.5.0/litestar_htmx/response.py>
- <https://github.com/litestar-org/litestar-htmx/tree/v0.5.0/tests>
- <https://htmx.org/reference/>

## Shared Styleguide Baseline

- [General Principles](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
- [Testing](../litestar-styleguide/references/testing.md)
