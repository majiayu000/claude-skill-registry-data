---
name: wp-abilities-mcp
description: Use when exposing site features to AI agents in a WordPress + Acorn project - the Abilities API (wp_register_ability, wp_abilities_api_init, /wp-json/wp-abilities/v1), roots/acorn-ai (make:ability), wordpress/mcp-adapter (discover-abilities, execute-ability, meta.mcp.public), the project .mcp.json, ACF 6.8 abilities (allow_ai_access), "ability not showing", connecting an agent to the local site. For generic REST routes use acorn-routes-api; for installing plugins use wp-composer-plugins.
---

# Abilities API and MCP Adapter

WordPress core (6.9+) has the **Abilities API**: a registry of named, schema-described actions with a permission callback. The **MCP Adapter** (`wordpress/mcp-adapter`) projects those abilities to MCP clients over HTTP or STDIO. `roots/acorn-ai` adds an Acorn-friendly base class resolved from the container. Register the domain action once as an ability; REST and MCP exposure are flags on it, not separate code.

Runner placeholders come from the session context: `{{runner.wp}}` (Lando default `lando wp`), `{{runner.acorn}}` (`lando wp acorn`), `{{runner.composer}}` (`lando composer`), `{{runner.cache}}`. Never run `wp` or `composer` on the host.

## When to use

- Adding an ability (read or write) that an agent, the REST API or the MCP Adapter should call.
- Installing or wiring `roots/acorn-ai` and `wordpress/mcp-adapter`, or writing the project `.mcp.json`.
- An ability is missing from `discover-abilities`, `ability:list` or `/wp-abilities/v1/abilities`.
- Deciding which ACF 6.8 abilities to keep, remove or expose.

## Inputs required

- WordPress version (≥ 6.9 for core abilities): `{{runner.wp}} core version`.
- Whether `roots/acorn-ai` and `wordpress/mcp-adapter` are installed, and where (which `composer.json`).
- The action in one sentence, who may run it (capability), and whether it only reads.
- The active profile, namespace and app path from the session context.

## Procedure

1. **Native first.** Check what is already registered before adding anything: `{{runner.wp}} eval 'foreach (wp_get_abilities() as $a) echo $a->get_name(), PHP_EOL;'`. Core registers `core/get-site-info`, `core/get-user-info`, `core/get-environment-info`; ACF 6.8 registers its own when enabled ([references/acf-abilities.md](references/acf-abilities.md)).
2. **Register a category first.** Every ability needs a registered `category`; register yours on `wp_abilities_api_categories_init` (or reuse `site` / `user`).
3. **Register the ability on `wp_abilities_api_init`**, from a service provider `boot()`. Calling `wp_register_ability()` anywhere else is rejected with `_doing_it_wrong`. The registry is created lazily after `init`, so a hook added in `boot()` is always in time.
   - With `roots/acorn-ai`: `{{runner.acorn}} make:ability ListProjects` creates `app/Ai/Abilities/ListProjectsAbility.php`; list the class in `config/ai-wordpress.php` `abilities`. Override `name()`, `category()`, `inputSchema()`, `permission()` and `meta()` (see the traps in [references/acorn-ai.md](references/acorn-ai.md)).
   - Without it: call `wp_register_ability('ns/name', [...])` yourself; keep the callback thin and delegate to a class resolved with `app()`.
4. **Describe it for agents**: `label`, a `description` written like a tool description, an object `input_schema` (always, even with no properties), an `output_schema`, and `meta.annotations` (`readonly`, `destructive`, `idempotent`).
5. **Choose the exposure**:
   - REST `/wp-json/wp-abilities/v1/abilities/<name>/run`: `meta.show_in_rest => true` (in WordPress 7.1, `meta.public => true` seeds it). Read-only abilities answer `GET` with `input` in the query; destructive + idempotent ones `DELETE`; the rest `POST`.
   - MCP default server: `meta.mcp.public => true`. The default server lists three tools (abilities `mcp-adapter/discover-abilities`, `get-ability-info`, `execute-ability`, which MCP clients see as `mcp-adapter-discover-abilities` and so on, `/` becoming `-`); public abilities are reached through them, not as separate tools. For direct tools, create a custom server on `mcp_adapter_init`.
6. **Load the adapter and connect a client** per profile (table below and [references/mcp-adapter.md](references/mcp-adapter.md)). STDIO: `{{runner.wp}} mcp-adapter serve --server=mcp-adapter-default-server --user=<login>`. HTTP: `/wp-json/mcp/mcp-adapter-default-server` with an application password.
7. Clear caches after PHP changes (`{{runner.cache}}`), then verify.

### Profiles

| | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| `roots/acorn-ai` goes in | the Composer project that requires Acorn (theme `composer.json`) | the plugin `composer.json` | root `composer.json` |
| `config/ai-wordpress.php` | theme `config/` | plugin `config/` | project `config/` |
| Provider registration | acorn-ai's provider is package-discovered; your own provider in the theme's `withProviders()` | package discovery or the plugin's provider list in its boot configuration | package discovery; your providers in `composer.json` `extra.acorn.providers` |
| `wordpress/mcp-adapter` | Bedrock root as a `wordpress-plugin` (activate it), or a library in the theme + `McpAdapter::instance()` | library in the plugin `vendor/`; WordPress never loads its plugin file, so the plugin calls `\WP\MCP\Core\McpAdapter::instance()` (early on `init`, gated per environment) | root Composer installs it in the content `plugins/` dir (activate it); define `WP_MCP_AUTOLOAD` as `false` in the Bedrock config because the classes come from the root autoloader |
| ACF abilities | available when ACF ≥ 6.8 and `enable_acf_ai` is on | same | ACF not installed by default: no `acf/*` abilities |

## Verification

- `{{runner.acorn}} ability:list` (acorn-ai) or the `wp eval` loop from step 1 shows the name.
- `{{runner.wp}} mcp-adapter list` shows `mcp-adapter-default-server` (and custom servers).
- STDIO smoke test: `echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"mcp-adapter-discover-abilities","arguments":{}}}' | {{runner.wp}} mcp-adapter serve --server=mcp-adapter-default-server --user=<login>` lists your ability.
- REST: `GET /wp-json/wp-abilities/v1/abilities/<name>` as an authenticated user returns it when `show_in_rest` is true.
- The MCP client (after restarting it) lists the server from `.mcp.json`.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `_doing_it_wrong`: "must be registered on wp_abilities_api_init" | `wp_register_ability()` called in `boot()` directly or on `init` | Wrap it in `add_action('wp_abilities_api_init', …)` |
| acorn-ai ability silently missing | `Ability::category()` returns `null` by default and core requires a registered category | Override `category()` and register the category on `wp_abilities_api_categories_init` |
| "Ability category … is not registered" | Category registered on the wrong hook or after the ability | Use `wp_abilities_api_categories_init` |
| Execute returns `ability_callback_exception` (argument count) on an acorn-ai ability | Without an `input_schema`, core calls the callback with no argument, but the acorn-ai wrapper expects `array $input` | Always return an object schema from `inputSchema()` |
| Ability missing from `discover-abilities` | No `meta.mcp.public => true` (a top-level `meta.public` is not read by adapter 0.5.0) | Add `'mcp' => ['public' => true]` to `meta()` |
| REST run returns 404 `rest_ability_not_found` | `meta.show_in_rest` false (default) | Set `show_in_rest` (or `public` on 7.1) |
| REST run rejects the method | Method must follow annotations (`readonly` → GET) | Call with the method the annotations imply |
| `mcp-adapter` is "not a registered wp command" while the plugin is active | Its autoloader looked for a plugin-local `vendor/autoload.php` and stopped | Define `WP_MCP_AUTOLOAD` false (classes from the root autoloader), or install it where its own `vendor/` exists |
| MCP client gets garbage before the JSON-RPC stream | `serve` without `--server` prints "Using server: …" to stdout; PHP notices printed to stdout | Always pass `--server=`; keep `WP_DEBUG_DISPLAY` off for the serve command |
| `execute-ability` denied | `permission_callback` false for the `--user` (or no user: logged out) | Pass `--user=` with the needed capability; review the callback |
| `{{runner.acorn}} ability:list` crashes reading properties | Older acorn-ai reads `WP_Ability` properties instead of getters | Use the `wp eval` loop from step 1, or update/patch the package |

## Escalation

- Ability design at depth (grouping, shared services, error codes, input schema gotchas): the third-party `wp-abilities-api` skill.
- Capability design for `permission_callback`: wp-security-escaping. Plain REST routes or Acorn routes: acorn-routes-api.
- Installing the packages: wp-composer-plugins. Exposing a write ability (create, update, delete) to agents on a shared or production site: ask the user first and propose gating by environment.

<!-- verified:
wp/wp-includes/abilities-api.php:290-305 — wp_register_ability requires doing_action('wp_abilities_api_init'); abilities-api/class-wp-abilities-registry.php:283-313 — lazy registry after init fires wp_abilities_api_init;
class-wp-abilities-registry.php:141-157 — category must be registered; class-wp-ability.php:295 — category required; :346-371 — meta.public (since 7.1.0) seeds show_in_rest;
class-wp-ability.php:585-590 — callback gets $input only when input_schema is non-empty; :519-533 — input without schema rejected;
wp-includes/abilities.php:17-35,90-300 — core categories site/user and core/* abilities; rest-api/endpoints/class-wp-rest-abilities-v1-run-controller.php:45,110-145 — run route, method from annotations, show_in_rest;
vendor/roots/acorn-ai (0.1.2) src/AcornAiServiceProvider.php:72-94 — registers config('ai-wordpress.abilities') on wp_abilities_api_init with fn(array $input); src/Abilities/Ability.php:62-64 — category() null, name() "<ns>/<kebab>"; MakeAbilityCommand — \Ai\Abilities; README — publish tags ai-wordpress-config / ai-config;
vendor/wordpress/mcp-adapter (0.5.0) includes/Autoloader.php:30-41 — WP_MCP_AUTOLOAD bypass; Core/McpAdapter.php:54-66,114-120,140 — init on init@20 (CLI) / rest_api_init@15, default server, 'mcp-adapter' command;
Servers/DefaultServerFactory.php:44-57 — server id/route, three tools; Abilities/McpAbilityHelperTrait.php:39,64 — meta['mcp']['public']; Cli/McpCommand.php:53-90 — --server/--user; :78 prints "Using server" when omitted; Transport/HttpTransport.php:111-120 — default capability 'read';
advanced-custom-fields-pro src/AI/Abilities/*.php — ability names and categories (see references/acf-abilities.md).
-->
