---
name: unity-game-development
description: Unity game development expertise covering Unity 2D/3D, C# programming, game mechanics, multiplayer networking, and performance optimization. Use when building games with Unity engine, implementing game systems (player controllers, physics, AI, combat), optimizing for 60 FPS, setting up multiplayer with Unity Netcode/Mirror, or working with Unity-specific features (ScriptableObjects, Prefabs, Animation, UI). Applies to PC, mobile, console, and WebGL platforms.
---

# Unity Game Development

Expert guidance for building games with Unity engine. Covers architecture, performance, networking, and Unity-specific patterns.

## Core Principles

**Component-Based Design**: Unity's architecture centers on GameObjects with MonoBehaviour components. Keep components focused and single-purpose.

**Data-Driven Configuration**: Use ScriptableObjects for game data (weapons, characters, levels) to enable designer-friendly tweaking without code changes.

**Performance First**: Target 60 FPS. Avoid GC allocations in Update/FixedUpdate/LateUpdate. Use object pooling for frequently instantiated objects.

**Clean Architecture**: Separate concerns - player input, game logic, presentation, networking. Follow SOLID principles in C#.

## Quick Reference

### Unity Project Structure

```
Assets/
├── _Project/                    # All project-specific code
│   ├── Scripts/
│   │   ├── Player/             # Player-related scripts
│   │   ├── Weapons/            # Weapon systems
│   │   ├── Enemy/              # AI and enemies
│   │   ├── Managers/           # Game managers (singleton pattern)
│   │   ├── UI/                 # UI controllers
│   │   └── Utilities/          # Helper classes
│   ├── Prefabs/                # Reusable GameObjects
│   ├── Scenes/                 # Unity scenes
│   ├── Data/                   # ScriptableObject instances
│   ├── Sprites/                # 2D sprites and textures
│   ├── Audio/                  # Sound effects and music
│   └── Animations/             # Animation clips and controllers
└── Plugins/                    # Third-party packages
```

### Common Patterns

**Player Controller** (2D top-down):
```csharp
public class PlayerController : MonoBehaviour
{
    [SerializeField] private float moveSpeed = 5f;
    private Rigidbody2D rb;
    private Vector2 moveInput;

    void Awake() => rb = GetComponent<Rigidbody2D>();

    void Update() {
        // Read input (runs every frame for responsiveness)
        moveInput.x = Input.GetAxisRaw("Horizontal");
        moveInput.y = Input.GetAxisRaw("Vertical");
        moveInput = moveInput.normalized; // Prevent diagonal speed boost
    }

    void FixedUpdate() {
        // Apply physics (runs at fixed intervals)
        rb.velocity = moveInput * moveSpeed;
    }
}
```

**ScriptableObject for Data**:
```csharp
[CreateAssetMenu(fileName = "WeaponData", menuName = "Game/Weapon")]
public class WeaponData : ScriptableObject
{
    public string weaponName;
    public int damage;
    public float fireRate;
    public Sprite icon;
    public GameObject projectilePrefab;
}
```

**Object Pooling** (avoid GC):
```csharp
public class ObjectPool
{
    private Queue<GameObject> pool = new Queue<GameObject>();
    private GameObject prefab;

    public GameObject Get() {
        if (pool.Count > 0) {
            var obj = pool.Dequeue();
            obj.SetActive(true);
            return obj;
        }
        return Object.Instantiate(prefab);
    }

    public void Return(GameObject obj) {
        obj.SetActive(false);
        pool.Enqueue(obj);
    }
}
```

## Key Areas

- **Architecture**: Design patterns, separation of concerns, FSM, MVC for Unity
- **Performance**: Profiling, draw call reduction, memory management, mobile optimization
- **Networking**: Unity Netcode setup, server-authoritative multiplayer, lag compensation
- **Best Practices**: Naming conventions, folder structure, prefab workflows, serialization

## Development Workflow

**1. Setup**
- Create Unity project (2D or 3D template)
- Install required packages (Input System, Netcode, etc.)
- Set up folder structure (see above)
- Configure project settings (physics layers, tags, input)

**2. Core Mechanics**
- Implement player controller with proper input handling
- Set up camera system (follow cam, bounds clamping)
- Build core gameplay loop (movement, actions, feedback)

**3. Game Systems**
- Add weapons/combat system with data-driven config
- Implement enemy AI with state machines
- Build UI (HUD, menus) with Unity UI (uGUI)

**4. Multiplayer** (if needed)
- Install Unity Netcode for GameObjects
- Set up NetworkManager and spawn management
- Implement server-authoritative logic
- Add client-side prediction for responsiveness

**5. Polish**
- Add animations, VFX, SFX
- Implement juice (screen shake, particle effects, audio feedback)
- Optimize performance (profiling, object pooling, batching)

**6. Build**
- Configure build settings for target platform
- Test on target hardware
- Profile and optimize further if needed

## Unity-Specific APIs

**Update Loops**:
- `Update()` - Every frame, use for input and non-physics logic
- `FixedUpdate()` - Fixed intervals (default 50Hz), use for physics
- `LateUpdate()` - After all Updates, use for camera following

**Finding Objects**:
- Avoid `FindObjectOfType()` in Update (slow)
- Cache references in `Awake()` or via serialized fields
- Use `GetComponent<T>()` in Awake, not Update

**Instantiate/Destroy**:
- Use Object Pooling instead of Instantiate/Destroy in gameplay
- `Instantiate()` and `Destroy()` cause GC allocations

**Input**:
- Prefer new Input System over legacy `Input.GetKey()`
- Read input in Update, apply in FixedUpdate for physics

## Performance Checklist

- [ ] Zero GC allocations in hot paths (Update, FixedUpdate)
- [ ] Object pooling for bullets, enemies, VFX
- [ ] Sprite batching enabled (same texture, same material)
- [ ] Physics layers configured (only check collisions between relevant layers)
- [ ] Camera culling optimized (don't render off-screen objects)
- [ ] Draw calls < 100 for mobile, < 200 for PC
- [ ] Target 60 FPS on mid-range hardware
- [ ] Profiler shows no CPU/GPU spikes

## Common Pitfalls

**❌ Allocating in Update**:
```csharp
void Update() {
    var enemies = FindObjectsOfType<Enemy>(); // GC allocation every frame!
}
```

**✅ Cache references**:
```csharp
private Enemy[] enemies;
void Start() => enemies = FindObjectsOfType<Enemy>();
```

**❌ String concatenation**:
```csharp
scoreText.text = "Score: " + score; // GC allocation!
```

**✅ Use StringBuilder or format**:
```csharp
scoreText.SetText("Score: {0}", score); // No allocation with TextMeshPro
```

**❌ Using Update for timers**:
```csharp
void Update() {
    timer += Time.deltaTime; // Fine, but...
}
```

**✅ Use Coroutines for delays**:
```csharp
IEnumerator Cooldown() {
    yield return new WaitForSeconds(1f);
}
```

## Testing

**Play Mode Tests**: Test game logic in Unity Editor
```csharp
[UnityTest]
public IEnumerator Player_TakesDamage_HealthDecreases() {
    var player = new GameObject().AddComponent<Player>();
    player.health = 100;
    player.TakeDamage(10);
    Assert.AreEqual(90, player.health);
    yield return null;
}
```

**Unit Tests**: Test pure C# logic without Unity
```csharp
[Test]
public void WeaponData_DPS_CalculatesCorrectly() {
    var weapon = ScriptableObject.CreateInstance<WeaponData>();
    weapon.damage = 10;
    weapon.fireRate = 2f; // shots per second
    Assert.AreEqual(20f, weapon.DPS);
}
```

## Asset Templates

See `assets/` for:
- `2d-project-structure/` - Example folder hierarchy for 2D games
- `scriptableobject-template.cs` - Boilerplate ScriptableObject template
- `monobehaviour-template.cs` - Clean MonoBehaviour template with regions

## Platform-Specific Notes

**Mobile** (Android/iOS):
- Target 30 FPS minimum, 60 FPS ideal
- Use sprite atlases to reduce draw calls
- Disable unused quality settings
- Test on low-end devices early

**WebGL**:
- Avoid System.IO, threading, sockets
- Keep build size < 50MB
- Use Addressables for large assets
- Test on target browsers (Chrome, Firefox, Safari)

**PC** (Windows/Mac/Linux):
- IL2CPP for better performance
- Support windowed/fullscreen modes
- Provide graphics quality settings
- Test input (keyboard, mouse, gamepad)

---

**For detailed architecture patterns, performance tuning, or multiplayer setup, refer to the key areas above.**
