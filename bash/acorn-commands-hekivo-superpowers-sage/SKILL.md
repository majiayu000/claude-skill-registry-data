---
name: superpowers-sage:acorn-commands
description: >
  Acorn CLI commands for WordPress automation — lando acorn make:command,
  artisan-style commands, Command::class, $signature, $description,
  handle() method, command arguments and options, output formatting,
  dependency injection in commands, calling other commands, AppServiceProvider
  registration, wp acorn schedule:run, scheduled commands, data import scripts,
  maintenance commands, theme automation tasks, lando acorn list
user-invocable: false
---

# Custom Acorn CLI Commands

Acorn commands are artisan-style CLI commands running inside WordPress context with full access to the Laravel container (services, Eloquent, config) **and** all WordPress functions (`get_posts()`, `wp_insert_post()`, etc.).

## When to use

- Scheduled data imports or scraping (cron-driven)
- One-off maintenance operations that touch the database and need Laravel services
- Developer tooling: seeding fixtures, resetting caches, recomputing derived data
- Long-running jobs that shouldn't run in a request cycle

## When NOT to use

- Simple WP-CLI operations already covered by `wp post`, `wp user`, `wp option` — use `wp-cli-ops` instead
- Routing / HTTP endpoints — use `acorn-routes` for request-based flows
- Background jobs with retries and failure tracking — use `acorn-queues` (Laravel queues) for durable processing
- Quick ad-hoc queries — `lando wp shell` or `lando wp eval` is faster for exploration

## Prerequisites

- Acorn installed and bootstrapped in the theme
- `ConsoleServiceProvider` registered (default in Acorn skeleton)
- Lando running (`lando start`) — commands execute inside the container

## Creating a Command

```bash
lando acorn make:command ImportProducts
# Generates app/Console/Commands/ImportProducts.php
```

Scripts: [`scripts/create-command.sh`](scripts/create-command.sh)

## Command Anatomy

```php
<?php
namespace App\Console\Commands;
use Illuminate\Console\Command;

class ImportProducts extends Command
{
    protected $signature = 'import:products
        {source : The data source (csv or api)}
        {--dry-run : Preview changes without writing}
        {--limit=100 : Max records to process}
        {--tag=* : Tags to assign (repeatable)}';
    protected $description = 'Import products from CSV or external API';

    public function handle(): int
    {
        $source = $this->argument('source');
        $this->info("Importing from {$source}");
        if ($this->option('dry-run')) { $this->warn('Dry-run mode — no writes.'); }
        return self::SUCCESS; // 0 = success, 1 = failure
    }
}
```

## Arguments and Options

```
{format}         Required       {--with-meta}     Boolean flag
{format=csv}     Default value  {--chunk=500}     Option with default
{format?}        Nullable       {--F|format=csv}  Shortcut
{ids*}           Array
```

## Output and Interaction

```php
$this->info('Done.');  $this->warn('Caution.');  $this->error('Failed!');
$this->table(['ID', 'Title'], $rows);
$this->withProgressBar($items, fn ($item) => process($item));
if (! $this->confirm('Continue?')) { return self::FAILURE; }
```

## Dependency Injection

Inject services into `handle()` — the container resolves them automatically:

```php
public function handle(ProductImporter $importer): int
{
    $results = $importer->run(source: $this->argument('source'), limit: (int) $this->option('limit'));
    $this->info("Imported {$results->created} / skipped {$results->skipped}");
    return self::SUCCESS;
}
```

## Calling Other Commands

```php
$this->call('cache:clear');                                               // With output
$this->callSilent('view:clear');                                          // Silent
$this->call('import:products', ['source' => 'csv', '--dry-run' => true]); // With args
```

## Registration

Commands in `app/Console/Commands/` are auto-discovered. For commands elsewhere, register in a ServiceProvider's `boot()`: `$this->commands([ImportProducts::class])`.

See [`references/scheduling.md`](references/scheduling.md) for scheduling setup and `lando acorn schedule:run`.
See [`references/practical-examples.md`](references/practical-examples.md) for import/maintenance/cache-warmup patterns.
See [`references/troubleshooting.md`](references/troubleshooting.md) for command not found, DI failures, schedule issues.

## Verification

- Run `lando acorn list` and confirm your custom command appears with the correct signature and description.
- Execute the command with `lando acorn <command-name>` and verify it completes without errors, returning exit code 0 (`self::SUCCESS`).
- Test arguments and options by running with `--help` to confirm the signature matches expectations, then run with sample inputs.

## Failure modes

### Problem: Command not discovered (not in `lando acorn list`)
- **Cause:** The command class is not in the `app/Console/Commands/` directory (the auto-discovery path), or the namespace does not match the file location.
- **Fix:** Ensure the command file is at `app/Console/Commands/YourCommand.php` with namespace `App\Console\Commands`. If the command lives elsewhere, register it explicitly in a service provider's `boot()` method: `$this->commands([YourCommand::class])`.

### Problem: Dependency injection resolution fails (target is not instantiable)
- **Cause:** The `handle()` method type-hints a service that is not bound in the container, or the service's own dependencies cannot be resolved.
- **Fix:** Verify the service is registered in a service provider's `register()` method. Check that all constructor parameters of the injected service are also resolvable. Use `lando acorn tinker` and `app()->make(YourService::class)` to test resolution in isolation.

## Escalation

- If DI resolution fails for a complex service tree, consult the service-providers reference in `sage:roots-sage-lando` for correct binding patterns and singleton registration.
- If the command needs to dispatch long-running work, dispatch a queued job instead of running the logic inline -- see `sage:acorn-queues` for job dispatching patterns.
