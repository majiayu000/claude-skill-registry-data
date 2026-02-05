---
name: module-writer
description: Create or update a journal entry module (database, model, actions, views, controllers, API, docs, tests). Use when adding a new journal module or changing an existing module such as mood, health, or obligations.
---

# Module Writer

This Skill helps you create a module used by journal entries. A module is a small, focused set of attributes for one journal entry (example: Mood tracks daily mood).

## When to use this Skill

Use this Skill when:
- Creating a new module
- Updating a module

## Instructions

## Quick start

- Pick a module name and ModuleType category.
- Add migration + model + factory.
- Add actions + tests.
- Add view + web controller + presenter + tests.
- Add API controller + resource + tests.
- Update docs, Bruno, translations.

### Step 1: Write the database migration

1. Verify the migration doesn't exist. Create it via Artisan with `--no-interaction`.

```bash
php artisan make:migration create_module_MODULE_NAME_table --no-interaction
```

1. A module always belongs to a journal entry. Use this pattern:

```
Schema::create('module_health', function (Blueprint $table): void {
    $table->id();
    $table->unsignedBigInteger('journal_entry_id');
    $table->string('category')->default(ModuleType::BODY_HEALTH->value);
    $table->text('health')->nullable();
    $table->timestamps();
});
```

1. A module always has a category from `ModuleType`. Do not add new types. Choose the closest existing category.
1. Never use foreign keys constraints.

### Step 2: Create related model

1. Models live in `App\Models`. Follow existing module models (e.g., `ModuleHealth`). Add a brief header PHPDoc for the model.
1. Add a `module{ModuleName}` method to `JournalEntry`. One module per day, so always `HasOne`.

### Step 3: Create the factory

Create a factory for the model.

### Step 4: Create tests

1. Add a model test for the relationship to `JournalEntry`.
1. Add a test for the new `JournalEntry` relationship method.
1. Never use `for()` on factories. Set `user_id` explicitly.

### Step 5: Add module to ModuleCatalog class

1. All modules are documented within ModuleCatalog so we can reference it later dynamically.

### Step 6: Decide if the module should be added to the default layout for journal action

1. When we create a journal, some modules are added to the layout by default. It's defined in `CreateDefaultLayoutForJournal` action.
1. Enable a module by default only if it is broadly applicable to most users on most days, immediately understandable without explanation, low-effort to use, non-sensitive in nature, and delivers clear value even with incomplete data; otherwise, keep it disabled by default and require explicit user opt-in.

### Step 7: Create the actions to manage the data

1. Create `Log{ModuleName}` (follow existing actions like `LogHealth`).
1. Action flow: validate -> log data -> log user action -> update last activity -> refresh content presence.
1. Add tests for happy path and edge cases.
1. Create `Reset{ModuleName}Data` (see `ResetHealthData`).
1. Add related table to DeleteRelatedJournalData.

### Step 8: Update the CheckPresenceOfContentInJournalEntry job

1. Add the presence of the data of the new module in `app/Jobs/CheckPresenceOfContentInJournalEntry.php`.
1. Update the test to reflect it.

### Step 9: Create a view that will let users interact with the module

1. Views are stored in the `resources/views/app/journal/entry/partials` folder.
1. If the module has Yes/No buttons, use the existing components.
1. If the module uses multiple choices, group the choices together like in the health.blade.php view file.
1. If the module uses multiple choices with multiple accepted values, display them like in the primary_obligation.blade.php view file.
1. Add the view at the right place within the `resources/views/app/journal/entry/show.blade.php` file.

### Step 10: Create the web controller to pilot the view

1. Add a controller to call the right view.
1. Controller names should follow project convention and include the module name (example: `HealthController.php`).
1. Sanitize input with `TextSanitizer` before actions.
1. Validate inline (no Form Requests). Strings must be strings and within max length.
1. Create a presenter for module data.
1. Update the main journal entry presenter to load this data.
1. Test both presenters.
1. Add the appropriate web route.
1. Create controller tests for happy path and edge cases.

### Step 11: Create the api controller

1. Create an API controller that uses the same actions for log/reset.
1. Update `JournalEntryResource` to include the new data.
1. Add API controller tests.

### Step 12: Add marketing documentation

1. Marketing docs live in `resources/views/marketing/docs/api`.
1. Add a new module in the modules folder.
1. Update the resources/views/marketing/docs/api/partials/journal-entry-response.blade.php partial.
1. Update the sidebar to include this new entry.
1. Add a new controller for the documentation of this module.
1. Add a controller test that asserts the content loads.

### Step 13: Add appropriate Bruno API documentation

1. Add Bruno tests for the new API methods in `docs/bruno`.

### Step 14: Update translations

1. Run `composer journalos:locale`.
1. Ensure there are no empty entries in `lang/fr.json`.

### Step 15: Test and lint

1. Run relevant PHPUnit tests for the new module.
1. When tests pass, run `composer test` if needed for coverage.

### Step 16: Add module name to README

1. Add the new module to the README file in the appropriate section: the name and the emoji.

### Step 17: Add module to the /features/modules marketing view

1. Add the module to the list of modules in the marketing site.

Do NOT forget any step. Be extremely thorough in your analysis. DO NOT FORGET ANY STEP.
