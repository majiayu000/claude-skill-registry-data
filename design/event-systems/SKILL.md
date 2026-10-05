---
name: event-systems
description: "Event system patterns — C# events, UnityEvent, SO event channels, static EventBus. When to use each, zero-allocation patterns, memory leak prevention."
alwaysApply: true
---

# Event Systems

Events decouple systems. The publisher doesn't know who's listening. The subscriber doesn't know who's publishing.

## When to Use Each Type

| Type | Coupling | Config | Allocation | Best For |
|------|----------|--------|------------|----------|
| C# events / Action | Code-only | None | Zero with struct | Internal class communication |
| UnityEvent | Inspector-wired | Designer | Some | Button clicks, animation events, designer-configurable |
| SO Event Channel | Asset-based | Designer | Minimal | Cross-system communication |
| Static EventBus | Global | None | Depends | Truly global events (rare) |

## C# Events (Preferred for Code)

```csharp
public sealed class HealthSystem : MonoBehaviour
{
    // Declare event
    public event System.Action<float, float> OnHealthChanged; // current, max
    public event System.Action OnDied;

    [SerializeField] private float _maxHealth = 100f;
    private float _currentHealth;

    public void TakeDamage(float amount)
    {
        _currentHealth = Mathf.Max(0f, _currentHealth - amount);
        OnHealthChanged?.Invoke(_currentHealth, _maxHealth);

        if (_currentHealth <= 0f)
        {
            OnDied?.Invoke();
        }
    }
}

// Subscriber
public sealed class HealthBar : MonoBehaviour
{
    [SerializeField] private HealthSystem _health;

    private void OnEnable()
    {
        _health.OnHealthChanged += UpdateBar;
        _health.OnDied += HandleDeath;
    }

    private void OnDisable()
    {
        _health.OnHealthChanged -= UpdateBar;
        _health.OnDied -= HandleDeath;
    }

    private void UpdateBar(float current, float max)
    {
        // Update UI
    }

    private void HandleDeath()
    {
        // Show death screen
    }
}
```

## CRITICAL: Always Unsubscribe

**Subscribe in `OnEnable`, unsubscribe in `OnDisable`.** This handles:
- Object deactivated (`SetActive(false)` → `OnDisable`)
- Object destroyed (`OnDisable` → `OnDestroy`)
- Scene unloaded

```csharp
// GOOD — symmetric subscribe/unsubscribe
private void OnEnable() => _source.OnEvent += HandleEvent;
private void OnDisable() => _source.OnEvent -= HandleEvent;

// BAD — memory leak if object is destroyed or deactivated
private void Start() => _source.OnEvent += HandleEvent;
// No unsubscribe → delegate holds reference → object can't be GC'd
```

## SO Event Channels (Cross-System)

See the `scriptable-objects` skill for the full pattern. Quick reference:

```csharp
// Create event asset: Assets/Events/OnPlayerDied.asset
// Wire same asset to publisher AND subscriber via [SerializeField]

// Publisher
[SerializeField] private VoidEventChannel _onPlayerDied;
_onPlayerDied.Raise();

// Subscriber (completely decoupled — doesn't know about publisher)
[SerializeField] private VoidEventChannel _onPlayerDied;
private void OnEnable() => _onPlayerDied.Subscribe(HandlePlayerDied);
private void OnDisable() => _onPlayerDied.Unsubscribe(HandlePlayerDied);
```

## UnityEvent (Designer-Configurable)

```csharp
public sealed class InteractableObject : MonoBehaviour
{
    [SerializeField] private UnityEvent _onInteract;

    public void Interact()
    {
        _onInteract?.Invoke(); // Designers wire responses in Inspector
    }
}
```

Use when designers need to configure responses without code:
- Button clicks
- Animation events
- Trigger zones
- Cutscene triggers

**Caution:** UnityEvents are slower than C# events and harder to debug. Use C# events for code-to-code communication.

## Static EventBus (Global, Use Sparingly)

```csharp
public static class GameEvents
{
    public static event System.Action OnGamePaused;
    public static event System.Action OnGameResumed;
    public static event System.Action<int> OnScoreChanged;

    public static void RaisePaused() => OnGamePaused?.Invoke();
    public static void RaiseResumed() => OnGameResumed?.Invoke();
    public static void RaiseScoreChanged(int score) => OnScoreChanged?.Invoke(score);
}
```

**Warning:** Static events are never garbage collected. Subscribers MUST unsubscribe. Use only for truly global events that every system needs.

## Zero-Allocation Pattern (Hot Path)

For events fired every frame (rare but exists):

```csharp
// Use ref struct to avoid heap allocation
public readonly ref struct DamageEvent
{
    public readonly float Amount;
    public readonly Vector3 Position;
    public readonly GameObject Source;

    public DamageEvent(float amount, Vector3 position, GameObject source)
    {
        Amount = amount;
        Position = position;
        Source = source;
    }
}

// Note: ref structs can't be stored in Action<T> delegates
// Use a custom delegate or direct method call for zero-alloc
```

## Common Mistakes

1. **Subscribing without unsubscribing** → memory leak, events fire on destroyed objects
2. **Subscribing in Awake, unsubscribing in OnDestroy** → events fire when object is disabled
3. **Using events for synchronous, same-frame logic** → direct method call is simpler
4. **Too many event channels** → if publisher and subscriber always exist together, use direct reference
