---
name: testing
description: Choose focused Laravel tests and quality checks that prove behavior without mirroring implementation details.
tags:
  - laravel
  - php
---

# Testing

Tests should prove behavior, not mirror implementation. Prefer the smallest test type that catches the risk.

## Test Selection

Use feature tests for:

- routes and controllers;
- authorization and middleware;
- validation;
- redirects;
- sessions;
- database writes;
- user-facing workflows.

Use unit tests for:

- pure helpers;
- value objects;
- complex Actions/Services without HTTP behavior;
- parsing and normalization rules.

Use browser E2E tests for:

- JavaScript-dependent behavior;
- Livewire/SPA interactions;
- modals, uploads, previews, drag/drop, and browser state;
- critical accessibility-sensitive flows.

Use `ui-agent-browser` while a frontend workflow is still being explored or implemented. Use `e2e-playwright` when that workflow should become repeatable Playwright coverage.

## Framework Fakes

Use Laravel fakes for external or filesystem side effects.

```php
Http::fake([
    'api.example.test/*' => Http::response(['ok' => true]),
]);

$this->post(route('records.send', $record))
    ->assertRedirect()
    ->assertSessionHasNoErrors();

Http::assertSent(fn ($request) => $request->method() === 'POST');
```

Common fakes:

- `Http::fake()`;
- `Storage::fake()`;
- `Mail::fake()`;
- `Notification::fake()`;
- `Queue::fake()` or `Bus::fake()`;
- `Event::fake()`.

## Workflow Tests

For important user-facing workflows, cover the full route behavior.

```php
$this->actingAs($user)
    ->post(route('records.store'), [
        'name' => 'Example',
    ])
    ->assertRedirect(route('records.index'))
    ->assertSessionHasNoErrors();

$this->assertDatabaseHas('records', [
    'name' => 'Example',
]);
```

When rebuilding or porting an app, add feature parity tests for critical happy paths. Parity tests are a regression net, not a replacement for focused tests.

## Render And Document Tests

For pure Blade/report rendering, unsaved Eloquent graphs may be built with `forceFill()` and `setRelation()`.

Use this only when persistence, middleware, authorization, route model binding, database constraints, queries, and events are not part of the behavior.

```php
$owner = (new User)->forceFill(['name' => 'Example User']);
$record = (new Record)->forceFill(['number' => 'DOC-001']);
$record->setRelation('owner', $owner);

$html = view('reports.record', ['record' => $record])->render();

$this->assertStringContainsString('DOC-001', $html);
```

For generated documents, assert both stable source content and artifact validity.

```php
$html = view('reports.record', $viewData)->render();
$output = Pdf::loadView('reports.record', $viewData)->output();

$this->assertStringContainsString('Document Number', $html);
$this->assertStringStartsWith('%PDF-', $output);
```

Avoid broad snapshots unless the project intentionally uses snapshot or visual-regression testing.

## Browser E2E

For Playwright or similar tools:

- prefer role and label locators;
- use web-first assertions;
- avoid fixed sleeps;
- use deterministic auth setup when appropriate;
- keep E2E focused on high-value browser behavior.

For Laravel Playwright details, load `e2e-playwright` instead of re-deriving setup, auth state, locator, trace, and screenshot rules.

## Handoff Verification

Before work is complete, run the relevant checks:

- targeted PHP tests;
- affected browser tests;
- Pint/style check;
- static analysis;
- frontend build/lint;
- route checks;
- queue/job smoke tests.

If a check cannot run, report the command and reason.

## Context Efficiency

Layer: 4 (Verification)

Load this skill only when writing or reviewing tests. Do not load with unrelated skills. Keep tests behavior-focused: smallest test type that catches the risk, no per-function suites unless asked, no frameworks/fixtures for trivial logic.
