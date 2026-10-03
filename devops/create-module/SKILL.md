---
description: Scaffold a new hexagonal module with Facade, ServiceProvider, and registration
argument-hint: "<ModuleName>"
disable-model-invocation: true
allowed-tools: "Read, Write, Edit, Glob, Bash(ls *), Bash(composer *)"
---

# New Module

Scaffold `modules/$ARGUMENTS/`. PascalCase, must not clash with an existing directory — ask if missing.

**First, challenge the need.** A new module requires its own vocabulary, not just its own files. If it wraps one existing concept, it belongs inside an existing module. Layer rules: `.claude/rules/architecture.md`.

## Context

!`ls modules/`

## Steps

1. **Read a small reference module** — `modules/Faq/` or `modules/UtxoTrace/` — and mirror its layout.

2. **Structure**:
   ```
   modules/<Module>/
   ├── Application/<Module>Facade.php
   ├── Domain/<Module>FacadeInterface.php
   ├── Domain/Repository/
   ├── Infrastructure/Http/Controller/
   ├── Infrastructure/Repository/
   └── <Module>ServiceProvider.php
   ```

3. **Domain first** — the Facade interface is the module's public contract. Other modules depend on this and nothing else:
   ```php
   namespace Modules\<Module>\Domain;

   interface <Module>FacadeInterface
   {
       // public API — domain types in, domain types out
   }
   ```

4. **Facade** — thin delegation to Actions, no logic of its own:
   ```php
   namespace Modules\<Module>\Application;

   final readonly class <Module>Facade implements <Module>FacadeInterface
   {
       public function __construct(
           // inject Action interfaces
       ) {
       }
   }
   ```

5. **ServiceProvider**:
   ```php
   namespace Modules\<Module>;

   final class <Module>ServiceProvider extends ServiceProvider
   {
       /** @var array<class-string, class-string> */
       public $singletons = [
           <Module>FacadeInterface::class => <Module>Facade::class,
       ];

       #[Override]
       public function register(): void
       {
           // contextual bindings only
       }
   }
   ```

   Bind the facade interface **now**. Three existing modules skipped this and their facades are dormant — see Known Debt in `CLAUDE.md`.

6. **Register** in `bootstrap/providers.php` — no auto-discovery. `Shared` stays first.

7. **Create** `tests/Unit/<Module>/`.

8. **Update docs** — module table in `docs/architecture.md` and `CLAUDE.md`.

9. ```bash
   composer test
   ```

## Specific to new modules

- Keep `App\Models\*` out of this module's Domain. The model-in-Domain trade is legacy in `Chat`/`OpenAI`/`Payment`/`UtxoTrace`, not a target to replicate
- The Facade never returns an Eloquent model or query builder
- No cycles — check what this module will import before creating it
