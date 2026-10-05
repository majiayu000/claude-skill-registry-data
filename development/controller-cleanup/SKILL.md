---
name: controller-cleanup
description: Keep Laravel controllers focused on HTTP orchestration by moving validation, authorization, and business workflows outward.
tags:
  - laravel
  - php
---

# Controller Cleanup

Use this skill when controllers become difficult to understand, test, or maintain.

When a Laravel app has several menus/pages, also use `module-per-menu`: avoid one broad controller for the whole app, and split by menu, page group, or resource boundary.

Controllers should stay thin and focused on HTTP orchestration. They should not contain long business workflows, provider payload construction, repeated query logic, or file-processing loops.

## Responsibilities

A controller may:

- receive route-bound models and requests;
- call `$this->authorize()` or rely on middleware/Form Request authorization;
- call a Form Request's `validated()` data;
- invoke an Action or Service;
- return redirects, views, JSON resources, streams, or downloads;
- attach session flash messages.

A controller should not:

- build external provider payloads inline;
- contain multi-step write workflows without a transaction boundary;
- duplicate validation rules;
- hide authorization inside unrelated branches;
- contain heavy report/query logic that is reused elsewhere.

## Route Boundaries

Keep coarse access requirements visible in routes or route groups.

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::resource('records', RecordController::class)
        ->middlewareFor('index', 'can:viewAny,' . Record::class)
        ->middlewareFor(['create', 'store'], 'can:create,' . Record::class)
        ->middlewareFor(['edit', 'update'], 'can:update,record')
        ->middlewareFor('destroy', 'can:delete,record');
});
```

Use Policies for model-state rules and Form Request `authorize()` for request-input-dependent authorization.

## Route Order And Cache Safety

Use controller actions for committed production endpoints that need middleware, sessions, tests, cache headers, or deployment route caching.

Route closures are acceptable for static views, simple redirects, prototypes, and temporary debugging.

Place static or specific routes before broad resource routes when URI patterns could collide.

```php
Route::get('records/export', ExportRecordsController::class)
    ->name('records.export');

Route::resource('records', RecordController::class);
```

Verify collision-prone route changes with `php artisan route:list` or a feature test.

## Generic Store Pattern

```php
final class RecordController
{
    public function store(StoreRecordRequest $request, CreateRecord $create): RedirectResponse
    {
        $record = $create->handle($request->user(), $request->validated());

        return redirect()
            ->route('records.show', $record)
            ->with('status', 'Record created.');
    }
}
```

## Guardrails

- Do not extract one-line code merely to create more layers.
- Do not require Repository Pattern by default.
- Keep framework-specific HTTP concerns in controllers.
- Keep reusable business operations outside controllers.

## Context Efficiency

Layer: 3 (Implementation)

Load this skill only when controllers need cleanup. Do not load with unrelated skills. Keep the diff minimal: inline validation only when rules are tiny, otherwise Form Request; one Action per use case; no repository by default.
