---
name: mediator
description: How source-generated Mediator carries requests from the presentation layer to Application handlers - registration and lifetime, IRequest and IRequestHandler, ValueTask, pipeline behaviours and their order, and why it isn't MediatR. Use when adding or changing a pipeline behaviour, sending a request, or when a handler isn't found.
metadata:
  scope: shared
---

# Mediator

## The rule

Requests travel from the presentation layer to Application through Mediator (`Mediator.Abstractions` in Application, `Mediator.SourceGenerator` in Presentation). It's MIT licensed and generates its dispatch code at build time, so there's no reflection scanning at startup.

| Piece | Where | How |
| --- | --- | --- |
| Request | `src/Application/<Feature>/<Commands or Queries>/<UseCase>/` | A class implementing `IRequest<TResponse>` |
| Handler | Beside the request | `IRequestHandler<TRequest, TResponse>`, returns `ValueTask<TResponse>` |
| Behaviours | `src/Application/Common/Behaviours/` | `IPipelineBehavior<TMessage, TResponse>`, registered as open generics in `src/Application/DependencyInjection.cs` |
| Registration | The presentation layer's startup | `AddMediator` with `ServiceLifetime.Scoped`, so handlers share the request's scoped `DbContext` |
| Sending | Presentation only | `ISender.Send(request, cancellationToken)` |

Every request uses `IRequest<TResponse>`. Mediator also offers `ICommand` and `IQuery` markers; we don't use them, because nothing yet needs a behaviour that applies to only one kind.

Behaviours run in the order they're registered. The first one registered is the outermost, so it runs first on the way in and last on the way out. `LoggingBehaviour` is registered first, so it times and logs everything inside it, validation failures included (`serilog`), and its span wraps the use case (`telemetry`). `ValidationBehaviour` comes next, so invalid requests never reach a handler.

## Steps

1. A new use case needs no registration. The generator finds the request and its handler when the solution builds (`add-a-use-case`).
2. To add a behaviour, create `<Name>Behaviour<TMessage, TResponse>` in `src/Application/Common/Behaviours/`, constrained to `where TMessage : IMessage`, and call `next(message, cancellationToken)` exactly once.
3. Register it in `AddApplication` with `services.AddScoped(typeof(IPipelineBehavior<,>), typeof(<Name>Behaviour<,>))`, in the position that gives the order you want.
4. Test the behaviour on its own with a fake `next` delegate (`unit-tests`), including the case where it stops the request.
5. Send requests only from the presentation layer, always passing the cancellation token (`cancellation`).

## Example

```csharp
// src/Application/DependencyInjection.cs
_ = services.AddValidatorsFromAssembly(Assembly.GetExecutingAssembly(), ServiceLifetime.Transient);

_ = services.AddScoped(typeof(IPipelineBehavior<,>), typeof(LoggingBehaviour<,>));
_ = services.AddScoped(typeof(IPipelineBehavior<,>), typeof(ValidationBehaviour<,>));
```

```csharp
// src/Application/Common/Behaviours/ValidationBehaviour.cs
public class ValidationBehaviour<TMessage, TResponse>(IEnumerable<IValidator<TMessage>> validators) : IPipelineBehavior<TMessage, TResponse>
    where TMessage : IMessage
{
    public async ValueTask<TResponse> Handle(TMessage message, MessageHandlerDelegate<TMessage, TResponse> next, CancellationToken cancellationToken)
    {
        // ... throws ValidationException when any validator fails
        return await next(message, cancellationToken);
    }
}
```

## Don't

- Add MediatR, or any package with a commercial licence. Mediator is the one we use.
- Send a request from inside a handler. Call the repository, or move the shared logic into the Application layer.
- Register `AddMediator` with the default singleton lifetime. Handlers would hold one `DbContext` for the life of the app.
- Return `Task` from a handler. The interface wants `ValueTask`.
- Await a `ValueTask` twice, or keep it to await later.

## Check

``` bash
dotnet build                                   # the generator reports missing or duplicate handlers
dotnet test tests/Application.Tests.Unit
```
