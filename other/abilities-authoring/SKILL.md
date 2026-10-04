---
name: superpowers-sage:abilities-authoring
description: >
  Creates custom WordPress Abilities for the WP MCP Adapter (WP 6.9+). An Ability is a PHP
  class extending Roots\AcornAi\Abilities\Ability that exposes a JSON schema and execute()
  method — auto-discovered by the MCP Adapter and callable via Claude's execute-ability tool.
  Covers: lando wp acorn make:ability, AbilitiesServiceProvider registration, JSON schema
  definition, discover-abilities validation. Invoke for: abilities, make ability,
  custom mcp endpoint, discover-abilities, execute-ability, acorn ability,
  abilities-authoring, mcp endpoint, wp ability, make:ability.
---

# abilities-authoring — WordPress MCP Abilities

An Ability exposes a callable MCP endpoint via the WordPress MCP Adapter. Claude calls it via `execute-ability` after `discover-abilities` lists it.

## Anatomy of an Ability

```php
class ListProjectsAbility extends Ability
{
    public string $name = 'projects/list';
    public string $description = 'Return all published Project CPT posts.';
    public array $schema = [ /* JSON Schema for input */ ];

    public function execute(array $args): array
    {
        // returns array — serialized as JSON by the adapter
    }
}
```

## Creating an Ability

```bash
lando wp acorn make:ability <Name>
# Example: lando wp acorn make:ability ListProjects
# Creates: app/Abilities/ListProjectsAbility.php
```

Use templates in `assets/ability-*.php.tpl` for query, CRUD, and search patterns.

## Registration

In `app/Providers/AbilitiesServiceProvider.php`:

```php
use App\Abilities\ListProjectsAbility;

public function boot(): void
{
    $this->app->make(AbilityRegistry::class)->register([
        new ListProjectsAbility(),
    ]);
}
```

See [`references/registration.md`](references/registration.md) for full ServiceProvider setup.

## JSON Schema

The `$schema` array follows JSON Schema Draft-07. See [`references/schema.md`](references/schema.md).

## MCP exposure

For an Ability to appear in `discover-abilities`, the MCP Adapter must be running. See [`references/mcp-exposure.md`](references/mcp-exposure.md).

## Common patterns

See [`references/patterns.md`](references/patterns.md) for query, CRUD, search, ACF field groups, and Livewire components patterns.

## Verification

```bash
bash scripts/list-abilities.sh
```

Then in your Claude Code session: call `discover-abilities` — the Ability should appear.

## Failure modes

### Problem: Ability not appearing in `discover-abilities`
- **Cause:** The Ability is not registered in `AbilitiesServiceProvider`, or the service provider is not in `config/app.php` providers array.
- **Fix:** Verify the Ability class is added to `AbilityRegistry::register()` in the service provider. Check that the provider is listed in `config/app.php` and is actually being booted. Claude Code caches `discover-abilities` — restart the editor after registration changes.

### Problem: `execute()` fails with "schema validation error"
- **Cause:** Input does not match the `$schema` definition. The MCP Adapter validates before calling your method.
- **Fix:** Review the schema properties, required fields, and type constraints. Ensure the input JSON matches enum values, integer ranges, and required field names exactly.

### Problem: Ability returns invalid response (not JSON-serializable)
- **Cause:** The `execute()` method returns an object, resource, or value that cannot be JSON-serialized (e.g., a `WP_Post` object).
- **Fix:** Return plain arrays only. Extract post data with `array_map()` and map each `WP_Post` to an associative array.

## Escalation

- For complex schema validation, consult the JSON Schema Draft-07 reference in `references/schema.md`.
- For ACF integration, see the ACF field groups pattern in `references/patterns.md`.
- If the Ability needs to expose Livewire components or act on multiple post types, see the Livewire pattern in `references/patterns.md`.
