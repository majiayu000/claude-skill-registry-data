---
name: topdown
description: "Top-down mobile game architecture — virtual joystick/tap-to-move/twin-stick touch movement, room transitions, fog of war, spawner patterns, wave systems, minimap."
globs: ["**/TopDown*.cs", "**/Room*.cs", "**/Wave*.cs", "**/Spawn*.cs"]
---

# Top-Down Game Patterns

## Movement Types

### Virtual Joystick (Mobile Touch)
```csharp
public sealed class VirtualJoystickController : MonoBehaviour
{
    [SerializeField] private float _moveSpeed = 6f;
    [SerializeField] private float _joystickDeadZone = 0.1f;

    private Rigidbody2D _rb;
    private Vector2 _moveInput;

    private void Awake()
    {
        _rb = GetComponent<Rigidbody2D>();
    }

    /// <summary>
    /// Called by virtual joystick UI component
    /// </summary>
    public void SetMoveInput(Vector2 input)
    {
        _moveInput = input.magnitude > _joystickDeadZone ? input : Vector2.zero;

        // Auto-aim in move direction
        if (_moveInput.sqrMagnitude > 0.01f)
        {
            float angle = Mathf.Atan2(_moveInput.y, _moveInput.x) * Mathf.Rad2Deg - 90f;
            transform.rotation = Quaternion.Euler(0f, 0f, angle);
        }
    }

    private void FixedUpdate()
    {
        _rb.linearVelocity = _moveInput.normalized * _moveSpeed;
    }
}
```

### Twin-Stick Touch (Two Joysticks)
```csharp
// Left joystick: movement
// Right joystick: aim direction (auto-fire when aiming)
// Common in mobile shooters (Archero, Brawl Stars)
```

### Tap-to-Move (NavMeshAgent)
```csharp
private NavMeshAgent _agent;
private Camera _camera;

private void Update()
{
    if (UnityEngine.InputSystem.Touchscreen.current == null) return;

    UnityEngine.InputSystem.Controls.TouchControl touch =
        UnityEngine.InputSystem.Touchscreen.current.primaryTouch;

    if (touch.press.wasPressedThisFrame)
    {
        Vector2 touchPos = touch.position.ReadValue();
        Ray ray = _camera.ScreenPointToRay(touchPos);
        if (Physics.Raycast(ray, out RaycastHit hit, 100f, _groundLayer))
        {
            _agent.SetDestination(hit.point);
        }
    }
}
```

## Camera Setup

- Orthographic camera, fixed Y height
- Cinemachine with Framing Transposer (damping for smooth follow)
- Confiner 2D for room bounds (PolygonCollider2D)

## Room Transitions

```csharp
public sealed class RoomTransition : MonoBehaviour
{
    [SerializeField] private Transform _spawnPoint;
    [SerializeField] private CinemachineConfiner2D _nextRoomConfiner;

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
        {
            other.transform.position = _spawnPoint.position;
            // Switch camera confiner to new room bounds
            CinemachineVirtualCamera vcam = FindFirstObjectByType<CinemachineVirtualCamera>();
            CinemachineConfiner2D confiner = vcam.GetComponent<CinemachineConfiner2D>();
            confiner.m_BoundingShape2D = _nextRoomConfiner.m_BoundingShape2D;
        }
    }
}
```

## Wave System

```csharp
[System.Serializable]
public sealed class EnemyWave
{
    public List<SpawnEntry> Entries;
    public float DelayBeforeWave = 2f;
}

[System.Serializable]
public sealed class SpawnEntry
{
    public GameObject Prefab;
    public int Count;
    public float SpawnDelay = 0.5f;
}

public sealed class WaveManager : MonoBehaviour
{
    [SerializeField] private List<EnemyWave> _waves;
    [SerializeField] private Transform[] _spawnPoints;

    private int _currentWave;
    private int _enemiesAlive;

    public event System.Action<int> OnWaveStarted;
    public event System.Action OnAllWavesComplete;

    public void StartNextWave()
    {
        if (_currentWave >= _waves.Count)
        {
            OnAllWavesComplete?.Invoke();
            return;
        }

        StartCoroutine(SpawnWave(_waves[_currentWave]));
        OnWaveStarted?.Invoke(_currentWave);
        _currentWave++;
    }

    private IEnumerator SpawnWave(EnemyWave wave)
    {
        yield return new WaitForSeconds(wave.DelayBeforeWave);

        for (int i = 0; i < wave.Entries.Count; i++)
        {
            SpawnEntry entry = wave.Entries[i];
            for (int j = 0; j < entry.Count; j++)
            {
                Transform spawnPoint = _spawnPoints[Random.Range(0, _spawnPoints.Length)];
                Instantiate(entry.Prefab, spawnPoint.position, Quaternion.identity);
                _enemiesAlive++;
                yield return new WaitForSeconds(entry.SpawnDelay);
            }
        }
    }

    public void OnEnemyDied()
    {
        _enemiesAlive--;
        if (_enemiesAlive <= 0)
        {
            StartNextWave();
        }
    }
}
```

## Minimap

1. Create a secondary camera (orthographic, top-down, high Y)
2. Set it to render to a RenderTexture
3. Display RenderTexture on a UI RawImage
4. Camera follows player position (X/Z only)
5. Use layers to control what the minimap camera sees

## Projectile Patterns

- **Single:** straight line from muzzle
- **Spread:** 3-5 projectiles in a fan arc
- **Burst:** N projectiles with delay between each
- **Homing:** Lerp direction toward target each frame
- **Circular:** spawn ring of projectiles expanding outward

## Fog of War (Simple)

1. Full-screen quad with black texture
2. Reveal circle around player (shader: distance from player position → alpha)
3. Persistent reveal: write to reveal texture, never erase
4. Performance: use low-res render texture, blur the edges
