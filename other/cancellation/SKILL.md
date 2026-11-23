---
name: cancellation
description: How cancellation tokens flow from the caller through Mediator, handlers and repositories to EF Core, and how tests prove they are passed on. Use when writing any async method, endpoint, handler or repository call.
metadata:
  scope: shared
---

# Cancellation

## The rule

Every async call that can be cancelled is given the token of the request that started it, all the way down to the database. When a caller goes away, the work stops.

| Layer | Where the token comes from |
| --- | --- |
| Presentation | The framework: an endpoint or tool parameter, `HttpContext.RequestAborted`, or (in Lambda) a source built from `context.RemainingTime` |
| Application | `Handle(request, cancellationToken)` |
| Infrastructure | The last parameter of every repository method, passed to every EF Core `...Async` call |

## Steps

1. Add `CancellationToken cancellationToken` as the last parameter of any new async method.
2. Pass it to `sender.Send(request, cancellationToken)`, to every repository call, and to every EF Core method (`ToListAsync`, `CountAsync`, `ExecuteUpdateAsync`, `SaveChangesAsync`).
3. In tests, create a real token and assert it's the one that reached the mock (`unit-tests`):

```csharp
using var tokenSource = new CancellationTokenSource();
var token = tokenSource.Token;

// Act
var result = await handler.Handle(command, token);

// Assert
_ = await reviewsRepository.Received(1).UpdateReview(command.Id, command.Stars, command.Text, token);
```

## Don't

- Use `CancellationToken.None` or `default` outside tests.
- Leave the token out of one call in a chain. Every hop needs it.
- Make the token optional (`= default`) on an interface method.

## Check

``` bash
dotnet build
dotnet test
```
