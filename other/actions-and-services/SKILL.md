---
name: actions-and-services
description: Use Actions and Services as deliberate Laravel application boundaries for use cases, integrations, and reusable workflows.
tags:
  - laravel
  - php
---

# Actions And Services

Actions and Services create application boundaries. Use them based on need, not because every controller method needs another layer.

## When To Use An Action

Use an Action for one named use case:

- `CreateRecord`
- `ApproveRecord`
- `CancelRecord`
- `GenerateRecordDocument`

Actions fit workflows with clear input and output.

```php
final class CreateRecord
{
    public function handle(User $actor, array $data): Record
    {
        return DB::transaction(function () use ($actor, $data) {
            return Record::create([
                'owner_id' => $actor->id,
                'name' => $data['name'],
            ]);
        });
    }
}
```

## When To Use A Service

Use a Service when a component owns a broader capability:

- integration client;
- document generation;
- pricing/calculation policy;
- import/export workflow;
- reusable application workflow.

```php
final class GatewayService
{
    public function createLink(Record $record): string
    {
        $response = Http::baseUrl(config('services.gateway.url'))
            ->timeout(5)
            ->retry(2, 200, throw: false)
            ->post('/links', [
                'reference' => $record->public_reference,
                'amount' => $record->total,
            ]);

        throw_unless($response->successful(), RuntimeException::class);

        return $response->json('url');
    }
}
```

## Integration Boundaries

Keep provider calls in focused services or adapters. The boundary should own:

- request mapping;
- authentication/signing details;
- timeouts and retries;
- response parsing;
- provider error translation;
- sanitized structured logging;
- fake-driven tests.

Do not globalize provider endpoints, payload quirks, status maps, or customer copy.

## Interfaces And Repositories

Do not create an interface for every service.

Add an interface only when:

- multiple implementations exist;
- provider swapping is likely;
- configuration selects implementations;
- the contract is shared across modules;
- the boundary protects domain code from infrastructure.

Do not require Repository Pattern for normal Eloquent CRUD. Add a repository only for real data-access complexity or storage-provider variation.

## Context Efficiency

Layer: 3 (Implementation)

Load this skill only when application boundaries need design. Do not load with unrelated skills. Keep the diff minimal: one Action per use case, one Service per integration or workflow, no interface until a second implementation exists.
