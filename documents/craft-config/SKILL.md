---
name: craft-config
description: Crafting a config file. The self-documenting contract between package and consumer.
---

# Skill: Craft Config

> "A config file is documentation that happens to be executable. If someone needs the README to understand it, you've failed."

## The Standard

1. **Naming**: The config file matches the package slug. `config/{package-slug}.php`. Registered via `->hasConfigFile()` in the service provider or `$this->mergeConfigFrom()` for raw providers.

2. **Every Key Has a Docblock Comment**: The config file IS the documentation. Multi-line comments explaining purpose, defaults, and trade-offs.

3. **`env()` for Runtime Toggles Only**: Deployment-sensitive values that change between environments. Enabled flags, cache drivers, disk names, queue connections. Never use `env()` for model classes or table names -- those are structural, not environmental.

4. **Class References for Strategy Swapping**: Let users replace implementations via config. Bind the config value to an interface in the service provider. The dominant pattern across all authors.

5. **Zero-Config Defaults**: Everything works out of the box with no changes. Publishing is optional. Every key has a sensible default.

6. **Preset-Based Configuration**: For tools with many granular options, offer semantic presets that replace hundreds of individual settings with a single word. Override individual rules on top of the preset.

7. **Closure-Based Config Values**: Accept closures alongside literal values for dynamic configuration. Filament's pattern: every configuration method accepts a value OR a closure, evaluated at runtime with injected context.

8. **Complexity Matches the Problem Space**: Simple packages get flat configs with 0-12 keys. Complex packages use nested grouping by concern, not by type. Group by concern when you pass 15 keys.

9. **Table and Model Customization**: Always expose table names and model classes. Users will want to extend your models or change table names. Make it easy.

10. **No Closures in Config Files**: Never use closures in config files. `php artisan config:cache` serializes config with `var_export()`, which cannot serialize closures. The app throws "Your configuration files are not serializable." Use class references, invokable classes, or method-based configuration instead. This applies to YOUR config file and any values consumers might set.

11. **Config Validation at Boot**: When a config value references a class (model, strategy, renderer), validate it implements the expected interface at boot time. Fail early with a clear message, not late with a cryptic container error.

## The Anti-Patterns

| Don't                                        | Do                                     | Why                                               |
|----------------------------------------------|----------------------------------------|---------------------------------------------------|
| Use `env()` for model classes or table names | `env()` for runtime toggles only       | Structural config doesn't change per environment  |
| Ship config keys without comments            | Every key gets a docblock              | The config file IS the documentation              |
| Require config publishing to work            | Provide zero-config defaults           | First-touch should be `composer require` and done |
| Leave keys without defaults                  | Every key has a sensible default value | Undefined config keys cause runtime errors        |
| Flat config past 15 keys                     | Nest by concern                        | Flat configs become unreadable at scale           |
| Group config by type                         | Group by concern                       | Developers think in features, not data types      |
| 100+ granular rules with no shortcut         | Offer presets with granular overrides  | One word beats one hundred lines                  |
| Closures in config files                     | Class references or invokable classes  | Breaks `config:cache` -- not serializable         |
| Silently accept invalid class config         | Validate interfaces at boot time       | Fail early with a clear message                   |

## Real-World Examples

See [examples.md](examples.md).
