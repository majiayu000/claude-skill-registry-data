---
name: vcontainer
description: "VContainer dependency injection for Unity — LifetimeScope hierarchy, registration patterns, constructor injection for plain C#, [Inject] for MonoBehaviours. Lightweight alternative to Zenject."
globs: ["**/VContainer*", "**/*LifetimeScope*.cs", "**/*Installer*.cs", "**/Container*.cs"]
---

# VContainer — Dependency Injection for Unity

VContainer is a lightweight, fast DI framework for Unity by hadashiA. It provides constructor injection for plain C# classes, method injection for MonoBehaviours, hierarchical scoping, and lifecycle management without the complexity of Zenject.

## Why Dependency Injection in Unity

- **Decouple systems**: Components depend on interfaces, not concrete types
- **Testability**: Swap real implementations for mocks in tests
- **No singletons**: Avoid static state and its hidden coupling
- **Configurable composition**: Change wiring without changing code
- **Explicit dependencies**: Constructor parameters document what a class needs

## LifetimeScope Hierarchy

VContainer uses `LifetimeScope` MonoBehaviours as composition roots. They form a parent-child hierarchy for dependency resolution.

```
RootLifetimeScope (DontDestroyOnLoad)
  |- AudioService (Singleton)
  |- SaveSystem (Singleton)
  |- AnalyticsService (Singleton)
  +- ISettingsProvider (Singleton)
      |
      |- MainMenuLifetimeScope (MainMenu scene)
      |     |- MainMenuController
      |     +- LeaderboardService
      |
      +- GameLifetimeScope (Game scene)
            |- GameManager
            |- SpawnSystem
            +- ScoreSystem
```

### Root Scope (Project-Wide Services)

```csharp
using VContainer;
using VContainer.Unity;

public class RootLifetimeScope : LifetimeScope
{
    [SerializeField] private AudioSettings _audioSettings;

    protected override void Configure(IContainerBuilder builder)
    {
        // Singletons survive scene loads
        builder.Register<AudioService>(Lifetime.Singleton).As<IAudioService>();
        builder.Register<SaveSystem>(Lifetime.Singleton).As<ISaveSystem>();
        builder.Register<AnalyticsService>(Lifetime.Singleton).As<IAnalyticsService>();

        // ScriptableObject instance
        builder.RegisterInstance(_audioSettings);
    }
}
```

### Scene Scope (Scene-Specific)

```csharp
public class GameLifetimeScope : LifetimeScope
{
    [SerializeField] private LevelConfig _levelConfig;

    protected override void Configure(IContainerBuilder builder)
    {
        // Scene-specific registrations
        builder.Register<ScoreSystem>(Lifetime.Scoped);
        builder.Register<WaveSpawner>(Lifetime.Scoped);

        // Entry point with lifecycle
        builder.RegisterEntryPoint<GameFlowController>();

        // MonoBehaviour already in scene hierarchy
        builder.RegisterComponentInHierarchy<PlayerController>();
        builder.RegisterComponentInHierarchy<HUDManager>();

        // Config data
        builder.RegisterInstance(_levelConfig);
    }
}
```

### Parent-Child Auto-Resolution

Child scopes automatically resolve dependencies from their parent. A `GameLifetimeScope` can inject `IAudioService` registered in `RootLifetimeScope` without explicit wiring.

```csharp
// GameFlowController receives IAudioService from Root + ScoreSystem from Game scope
public class GameFlowController : IStartable, ITickable, IDisposable
{
    private readonly IAudioService _audio;
    private readonly ScoreSystem _score;

    public GameFlowController(IAudioService audio, ScoreSystem score)
    {
        _audio = audio;
        _score = score;
    }
}
```

## Registration Patterns

### Plain C# Classes — Constructor Injection (Preferred)

```csharp
// Registration
builder.Register<ScoreSystem>(Lifetime.Singleton);

// The class — dependencies are constructor parameters
public class ScoreSystem
{
    private readonly IAudioService _audio;
    private readonly ISaveSystem _save;

    public ScoreSystem(IAudioService audio, ISaveSystem save)
    {
        _audio = audio;
        _save = save;
    }

    public void AddScore(int points)
    {
        // Use injected services
        _audio.PlaySfx("score");
        _save.SetInt("score", points);
    }
}
```

### Interface Binding

```csharp
// Register concrete type, expose as interface
builder.Register<AudioService>(Lifetime.Singleton).As<IAudioService>();

// Multiple interfaces for same implementation
builder.Register<NetworkManager>(Lifetime.Singleton)
    .As<INetworkSender>()
    .As<INetworkReceiver>();

// Self + interface
builder.Register<GameManager>(Lifetime.Singleton)
    .AsSelf()
    .As<IGameStateProvider>();
```

### MonoBehaviour Registration

MonoBehaviours cannot use constructor injection. Use `[Inject]` method injection.

```csharp
// MonoBehaviour already placed in the scene
builder.RegisterComponentInHierarchy<PlayerController>();

// Create MonoBehaviour on a new GameObject
builder.RegisterComponentOnNewGameObject<HUDManager>(
    Lifetime.Scoped,
    "HUDManager"  // Optional GameObject name
);

// Register existing component reference from LifetimeScope's serialized fields
[SerializeField] private PlayerController _player;
// In Configure:
builder.RegisterComponent(_player);
```

```csharp
// MonoBehaviour with [Inject]
public class PlayerController : MonoBehaviour
{
    private IAudioService _audio;
    private IInputService _input;

    [Inject]
    public void Construct(IAudioService audio, IInputService input)
    {
        _audio = audio;
        _input = input;
    }

    private void Update()
    {
        if (_input.JumpPressed)
        {
            Jump();
            _audio.PlaySfx("jump");
        }
    }
}
```

### Entry Points — Lifecycle Without MonoBehaviour

Entry points implement lifecycle interfaces and run without needing a GameObject.

```csharp
builder.RegisterEntryPoint<GameFlowController>();
```

```csharp
public class GameFlowController : IStartable, ITickable, IFixedTickable, IDisposable
{
    private readonly ScoreSystem _score;

    public GameFlowController(ScoreSystem score) => _score = score;

    public void Start()
    {
        // Called once after injection, like MonoBehaviour.Start
        Debug.Log("Game started");
    }

    public void Tick()
    {
        // Called every frame, like MonoBehaviour.Update
    }

    public void FixedTick()
    {
        // Called every FixedUpdate
    }

    public void Dispose()
    {
        // Called when scope is destroyed, like MonoBehaviour.OnDestroy
        Debug.Log("Game ended");
    }
}
```

Available lifecycle interfaces:
- `IStartable` — `Start()` called once after construction
- `ITickable` — `Tick()` called every Update
- `IPostTickable` — `PostTick()` called every LateUpdate
- `IFixedTickable` — `FixedTick()` called every FixedUpdate
- `IDisposable` — `Dispose()` called when scope is destroyed
- `IAsyncStartable` — `async UniTask StartAsync(CancellationToken ct)`

### Factory Registration

For objects that need runtime creation with injected dependencies.

```csharp
// Registration
builder.Register<EnemyFactory>(Lifetime.Scoped);

// Factory class
public class EnemyFactory
{
    private readonly IObjectResolver _container;
    private readonly EnemySettings _settings;

    public EnemyFactory(IObjectResolver container, EnemySettings settings)
    {
        _container = container;
        _settings = settings;
    }

    public Enemy Create(EnemyType type)
    {
        GameObject prefab = _settings.GetPrefab(type);
        GameObject instance = Object.Instantiate(prefab);
        _container.InjectGameObject(instance); // Inject into all [Inject] methods
        return instance.GetComponent<Enemy>();
    }
}
```

### Func Factory (Lightweight)

```csharp
// Register a factory delegate
builder.RegisterFactory<Vector3, Bullet>(container =>
{
    var pool = container.Resolve<BulletPool>();
    return position => pool.Get(position);
}, Lifetime.Scoped);

// Inject the factory
public class Weapon
{
    private readonly Func<Vector3, Bullet> _createBullet;

    public Weapon(Func<Vector3, Bullet> createBullet)
    {
        _createBullet = createBullet;
    }

    public void Fire(Vector3 muzzlePos)
    {
        Bullet b = _createBullet(muzzlePos);
    }
}
```

## Lifetime Options

| Lifetime | Behavior | Use For |
|----------|----------|---------|
| `Singleton` | One instance for the entire scope lifetime | Services, managers, shared state |
| `Transient` | New instance every time it is resolved | Stateless utilities, value objects |
| `Scoped` | One instance per scope (child scopes get their own) | Per-scene services, per-context state |

```csharp
builder.Register<AudioService>(Lifetime.Singleton);   // One forever
builder.Register<DamageCalculator>(Lifetime.Transient); // New each time
builder.Register<ScoreTracker>(Lifetime.Scoped);        // One per scene scope
```

## ScriptableObject and Asset Registration

```csharp
public class GameLifetimeScope : LifetimeScope
{
    [SerializeField] private GameConfig _gameConfig;
    [SerializeField] private EnemyDatabase _enemyDatabase;

    protected override void Configure(IContainerBuilder builder)
    {
        // Register as instances (not created by container)
        builder.RegisterInstance(_gameConfig);
        builder.RegisterInstance(_enemyDatabase).As<IEnemyDatabase>();
    }
}
```

## Child Scope Creation at Runtime

```csharp
public class RoomManager
{
    private readonly LifetimeScope _parentScope;

    public RoomManager(LifetimeScope parentScope) => _parentScope = parentScope;

    public LifetimeScope CreateRoomScope(RoomConfig config)
    {
        return _parentScope.CreateChild(builder =>
        {
            builder.RegisterInstance(config);
            builder.Register<RoomController>(Lifetime.Scoped);
            builder.RegisterEntryPoint<RoomLogic>();
        });
    }
}
```

## Common Mistakes

### Circular Dependencies

```csharp
// BAD — A depends on B, B depends on A. Container throws at resolution.
public class A { public A(B b) { } }
public class B { public B(A a) { } }

// FIX — break the cycle with an interface, event, or lazy resolution
public class A { public A(IEventBus bus) { } }
public class B { public B(IEventBus bus) { } }
```

### Registering MonoBehaviours as Transient

```csharp
// BAD — creates a new GameObject every resolve, probably not what you want
builder.RegisterComponentOnNewGameObject<Player>(Lifetime.Transient);

// GOOD — one per scope
builder.RegisterComponentOnNewGameObject<Player>(Lifetime.Scoped);

// GOOD — use existing scene object
builder.RegisterComponentInHierarchy<Player>();
```

### Forgetting to Register Dependencies

```csharp
// If ScoreSystem depends on IAudioService but IAudioService is not registered,
// VContainer throws VContainerException at build time.
// Always verify all dependencies are registered in the scope or a parent scope.
```

### Using [Inject] on Fields (Avoid)

```csharp
// BAD — field injection hides dependencies, untestable
public class BadComponent : MonoBehaviour
{
    [Inject] private IAudioService _audio;
}

// GOOD — method injection is explicit
public class GoodComponent : MonoBehaviour
{
    private IAudioService _audio;

    [Inject]
    public void Construct(IAudioService audio) => _audio = audio;
}
```

## Testing with VContainer

```csharp
[Test]
public void ScoreSystem_AddsScore()
{
    // No container needed — just use constructor
    var mockAudio = new MockAudioService();
    var mockSave = new MockSaveSystem();
    var score = new ScoreSystem(mockAudio, mockSave);

    score.AddScore(100);

    Assert.AreEqual(100, score.CurrentScore);
    Assert.IsTrue(mockAudio.PlayedSfx.Contains("score"));
}
```

## Project Structure Convention

```
Assets/
  Scripts/
    Installers/         (or Scopes/)
      RootLifetimeScope.cs
      GameLifetimeScope.cs
      MainMenuLifetimeScope.cs
    Services/
      IAudioService.cs
      AudioService.cs
    Game/
      GameFlowController.cs
      ScoreSystem.cs
```
