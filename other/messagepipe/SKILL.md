---
name: messagepipe
description: "MessagePipe pub/sub for Unity — readonly struct messages, broker registration in the LifetimeScope, IPublisher/ISubscriber injection, disposal discipline, buffered and async variants. The only permitted messaging system in this project."
globs: ["**/*Message.cs", "**/*LifetimeScope*.cs", "**/MessagePipe*"]
---

# MessagePipe — Zero-Allocation Pub/Sub

MessagePipe (Cysharp) is the **only** messaging system permitted here
(`.claude/rules/architecture.md`). No ScriptableObject event channels, no static
EventBus, no C# events for cross-system communication.

It is a DI-first library: publishers and subscribers are resolved from the container,
never constructed. That is what makes a System testable — a stub `IPublisher<T>` is
four lines.

## Messages are readonly structs

```csharp
namespace PoFootball.Systems
{
    /// <summary>
    /// Published when a defender brings the carrier down. Carries the closing speed
    /// that satisfied the threshold so presentation can scale the impact and
    /// telemetry can histogram hit strength.
    /// </summary>
    public readonly struct Systems_TackleMessage
    {
        public readonly int TacklerId;
        public readonly int CarrierId;
        public readonly float ClosingSpeed;

        public Systems_TackleMessage(int tacklerId, int carrierId, float closingSpeed)
        {
            TacklerId = tacklerId;
            CarrierId = carrierId;
            ClosingSpeed = closingSpeed;
        }
    }
}
```

- `readonly struct` — zero allocation on publish, and no subscriber can mutate what
  the next subscriber sees.
- **Carry ids and values, not references.** A message holding a `GameObject` outlives
  the frame in a buffered broker and hands subscribers a destroyed object.
- **Carry what a consumer would otherwise have to recompute.** `ClosingSpeed` is
  already known at the publish site; making a subscriber re-derive it duplicates the
  rule.
- One message type per file, named `*Message`.

## Every broker must be registered

An unregistered message type throws at resolution, not at publish — you get a
container error on scene load, which is the good case. Register in the LifetimeScope
alongside everything else:

```csharp
protected override void Configure(IContainerBuilder builder)
{
    builder.Register<Systems_PlayModel>(Lifetime.Singleton);
    builder.RegisterEntryPoint<Systems_Referee>().AsSelf();

    MessagePipeOptions messagePipeOptions = builder.RegisterMessagePipe();
    builder.RegisterMessageBroker<Systems_PlaySnappedMessage>(messagePipeOptions);
    builder.RegisterMessageBroker<Systems_PlayEndedMessage>(messagePipeOptions);
    builder.RegisterMessageBroker<Systems_TackleMessage>(messagePipeOptions);
    builder.RegisterMessageBroker<Systems_ScoreMessage>(messagePipeOptions);
}
```

`RegisterMessagePipe()` is called **once** per scope and returns the options every
`RegisterMessageBroker<T>` call needs. Requires the
`com.cysharp.messagepipe.vcontainer` package, and the assembly must reference both
`MessagePipe` and `MessagePipe.VContainer`.

## Publishing

Inject `IPublisher<T>` — never a concrete broker.

```csharp
public sealed class Systems_Referee : IFixedTickable
{
    private readonly IPublisher<Systems_TackleMessage> _tacklePublisher;

    public Systems_Referee(IPublisher<Systems_TackleMessage> tacklePublisher)
    {
        _tacklePublisher = tacklePublisher;
    }

    private void EndPlay(int tacklerId, int carrierId, float closingSpeed)
    {
        _tacklePublisher.Publish(new Systems_TackleMessage(tacklerId, carrierId, closingSpeed));
    }
}
```

Publish is **synchronous and re-entrant**: every subscriber runs to completion inside
the `Publish` call, on the caller's stack. Two consequences worth internalizing:

- A subscriber that publishes back into the same broker recurses. Guard with a state
  flag on the model, not with a queue.
- Publishing from `FixedUpdate` means subscribers run in the physics loop. Keep them
  cheap, or hand off with [[unitask]].

## Subscribing

Subscribe once, in `Start` — not in the constructor. A constructor that subscribes
can be reached by a publish before the rest of the object graph is built.

```csharp
public sealed class Systems_Telemetry : IStartable, IDisposable
{
    private readonly ISubscriber<Systems_PlayEndedMessage> _endedSubscriber;
    private IDisposable _subscription;

    public Systems_Telemetry(ISubscriber<Systems_PlayEndedMessage> endedSubscriber)
    {
        _endedSubscriber = endedSubscriber;
    }

    public void Start()
    {
        _subscription = _endedSubscriber.Subscribe(OnPlayEnded);
    }

    private void OnPlayEnded(Systems_PlayEndedMessage message) { /* ... */ }

    public void Dispose()
    {
        _subscription?.Dispose();
    }
}
```

### Disposal is not optional

`Subscribe` returns an `IDisposable`. Dropping it leaks the handler, and the handler
holds the subscriber alive — across scene loads, and across domain reloads in the
Editor. The symptom is a callback firing N times after N play-mode entries.

| Consumer | Pattern |
|---|---|
| System (plain C#) | Implement `IDisposable`, dispose in `Dispose()`. VContainer calls it when the scope dies. |
| View (MonoBehaviour) | `CompositeDisposable`, `.AddTo(_disposables)`, dispose in `OnDestroy`. |
| Many subscriptions | `DisposableBag.CreateBuilder()` → `builder.Build()`. |

```csharp
public sealed class Systems_ScoreView : MonoBehaviour, Systems_IInjectableView
{
    private readonly CompositeDisposable _disposables = new();

    [Inject]
    public void Construct(ISubscriber<Systems_ScoreMessage> scoreSubscriber)
    {
        scoreSubscriber.Subscribe(OnScored).AddTo(_disposables);
    }

    private void OnDestroy() => _disposables.Dispose();
}
```

## Variants

| Interface | Use when |
|---|---|
| `IPublisher<T>` / `ISubscriber<T>` | The default. Keyless, synchronous. |
| `IBufferedPublisher<T>` / `IBufferedSubscriber<T>` | Late subscribers need the last value — a HUD spawned mid-play needs the current score, not the next change. |
| `IAsyncPublisher<T>` / `IAsyncSubscriber<T>` | Handlers do async work. Pair with UniTask and pass a `CancellationToken`. |
| `IPublisher<TKey, TMessage>` | Per-entity routing, e.g. keyed by player id. Prefer one message with an id field until routing cost is measured. |

## Filters

Filters wrap handlers — logging, dedup, rate-limiting — without touching either side:

```csharp
builder.RegisterMessageBroker<Systems_TackleMessage>(messagePipeOptions);
messagePipeOptions.AddGlobalMessageHandlerFilter(typeof(LoggingFilter<>));
```

Use sparingly. A filter that changes whether a message is delivered is game logic
hidden one level below where anyone will look for it.

## Testing

Because Systems depend on `IPublisher<T>`, not a broker, a stub is trivial — no
container, no Unity, EditMode-runnable:

```csharp
private sealed class StubPublisher<T> : IPublisher<T>
{
    public int Count { get; private set; }
    public T Last { get; private set; }

    public void Publish(T message)
    {
        Count++;
        Last = message;
    }
}

[Test]
public void SustainedContact_EndsThePlay()
{
    var ended = new StubPublisher<Systems_PlayEndedMessage>();
    var referee = new Systems_Referee(/* ... */ ended);

    // ...

    Assert.That(ended.Count, Is.EqualTo(1));
    Assert.That(ended.Last.Outcome, Is.EqualTo(Systems_PlayOutcome.Tackle));
}
```

If a System is hard to test this way, it is usually reaching for something it did not
declare — which is the design feedback, not a reason to add a container to the test.

## Rules

- Messages are `readonly struct`, one per file, named `*Message`
- Every message type gets a `RegisterMessageBroker<T>` call — no exceptions
- Inject `IPublisher<T>` / `ISubscriber<T>`; never resolve a broker directly
- Every `Subscribe` result is disposed
- Subscribe in `Start`/`Construct`, not in a constructor
- Systems publish; Views subscribe. A View that publishes is doing logic
- Cross-system communication goes through MessagePipe, never a direct reference

## Related

- [[vcontainer]] — the container that owns broker registration and disposal
- [[unitask]] — for async handlers and for offloading work out of a publish
- [[event-systems]] — why the alternatives (SO channels, static EventBus) are not used
