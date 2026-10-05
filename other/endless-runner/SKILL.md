---
name: endless-runner
description: "Endless runner architecture — procedural chunk spawning, lane-based or free movement, obstacle patterns, speed ramping, coin/collectible systems, distance scoring."
globs: ["**/Runner*.cs", "**/Endless*.cs", "**/Chunk*.cs", "**/Obstacle*.cs", "**/Lane*.cs"]
---

# Endless Runner Patterns

## Chunk-Based Level Generation

```csharp
public sealed class ChunkSpawner : MonoBehaviour
{
    [SerializeField] private GameObject[] _chunkPrefabs;
    [SerializeField] private float _chunkLength = 20f;
    [SerializeField] private int _activeChunkCount = 5;
    [SerializeField] private Transform _player;

    private readonly Queue<GameObject> _activeChunks = new();
    private float _spawnZ;
    private ObjectPool<GameObject>[] _chunkPools;

    private void Awake()
    {
        _spawnZ = 0f;
        // Initialize pools for each chunk type
    }

    private void Update()
    {
        float playerZ = _player.position.z;
        float despawnZ = playerZ - _chunkLength;

        // Recycle chunks behind player
        while (_activeChunks.Count > 0)
        {
            GameObject oldest = _activeChunks.Peek();
            if (oldest.transform.position.z < despawnZ)
            {
                _activeChunks.Dequeue();
                oldest.SetActive(false); // return to pool
            }
            else break;
        }

        // Spawn chunks ahead
        float spawnThreshold = playerZ + _chunkLength * _activeChunkCount;
        while (_spawnZ < spawnThreshold)
        {
            SpawnChunk();
        }
    }

    private void SpawnChunk()
    {
        int index = Random.Range(0, _chunkPrefabs.Length);
        GameObject chunk = GetFromPool(index);
        chunk.transform.position = new Vector3(0f, 0f, _spawnZ);
        chunk.SetActive(true);
        _activeChunks.Enqueue(chunk);
        _spawnZ += _chunkLength;
    }

    private GameObject GetFromPool(int index)
    {
        // Use ObjectPool<T> or custom pool
        return Instantiate(_chunkPrefabs[index]); // placeholder — use pool
    }
}
```

## Lane-Based Movement (3-Lane)

```csharp
public sealed class LaneRunner : MonoBehaviour
{
    [Header("Lanes")]
    [SerializeField] private float _laneWidth = 2.5f;
    [SerializeField] private float _laneSwitchSpeed = 15f;

    [Header("Jump")]
    [SerializeField] private float _jumpForce = 10f;
    [SerializeField] private float _gravity = -30f;

    [Header("Slide")]
    [SerializeField] private float _slideDuration = 0.5f;

    private int _currentLane; // -1, 0, 1
    private float _targetX;
    private float _verticalVelocity;
    private bool _isGrounded = true;
    private bool _isSliding;
    private CharacterController _controller;

    private void Awake()
    {
        _controller = GetComponent<CharacterController>();
        _currentLane = 0;
    }

    public void SwitchLane(int direction) // -1 left, +1 right
    {
        _currentLane = Mathf.Clamp(_currentLane + direction, -1, 1);
        _targetX = _currentLane * _laneWidth;
    }

    public void Jump()
    {
        if (!_isGrounded) return;
        _verticalVelocity = _jumpForce;
        _isGrounded = false;
    }

    public void Slide()
    {
        if (_isSliding) return;
        StartCoroutine(SlideCoroutine());
    }

    private IEnumerator SlideCoroutine()
    {
        _isSliding = true;
        _controller.height = 0.5f;
        _controller.center = new Vector3(0f, 0.25f, 0f);

        yield return new WaitForSeconds(_slideDuration);

        _controller.height = 2f;
        _controller.center = new Vector3(0f, 1f, 0f);
        _isSliding = false;
    }

    private void Update()
    {
        // Lateral movement
        float currentX = transform.position.x;
        float newX = Mathf.MoveTowards(currentX, _targetX, _laneSwitchSpeed * Time.deltaTime);

        // Vertical
        if (_isGrounded && _verticalVelocity < 0f)
        {
            _verticalVelocity = -1f;
        }
        _verticalVelocity += _gravity * Time.deltaTime;

        Vector3 move = new Vector3(newX - currentX, _verticalVelocity * Time.deltaTime, 0f);
        _controller.Move(move);

        _isGrounded = _controller.isGrounded;
    }
}
```

## Touch Input Mapping

```csharp
public sealed class RunnerInput : MonoBehaviour
{
    [SerializeField] private LaneRunner _runner;
    [SerializeField] private float _swipeThreshold = 50f;

    private Vector2 _touchStart;

    private void Update()
    {
        if (UnityEngine.InputSystem.Touchscreen.current == null) return;

        UnityEngine.InputSystem.Controls.TouchControl touch =
            UnityEngine.InputSystem.Touchscreen.current.primaryTouch;

        if (touch.press.wasPressedThisFrame)
        {
            _touchStart = touch.position.ReadValue();
        }

        if (touch.press.wasReleasedThisFrame)
        {
            Vector2 delta = touch.position.ReadValue() - _touchStart;

            if (delta.magnitude > _swipeThreshold)
            {
                if (Mathf.Abs(delta.x) > Mathf.Abs(delta.y))
                {
                    _runner.SwitchLane(delta.x > 0f ? 1 : -1);
                }
                else if (delta.y > 0f)
                {
                    _runner.Jump();
                }
                else
                {
                    _runner.Slide();
                }
            }
        }
    }
}
```

## Speed Ramping

```csharp
public sealed class SpeedManager : MonoBehaviour
{
    [SerializeField] private float _startSpeed = 8f;
    [SerializeField] private float _maxSpeed = 25f;
    [SerializeField] private float _accelerationPerSecond = 0.1f;

    private float _currentSpeed;
    private float _playTime;

    public float CurrentSpeed => _currentSpeed;

    private void Update()
    {
        _playTime += Time.deltaTime;
        _currentSpeed = Mathf.Min(_startSpeed + _accelerationPerSecond * _playTime, _maxSpeed);
    }

    public void ResetSpeed()
    {
        _playTime = 0f;
        _currentSpeed = _startSpeed;
    }
}
```

## Scoring

- **Distance score:** increases with time × speed
- **Coin multiplier:** collected coins multiply final score
- **Combo bonus:** consecutive collectibles without missing

## Obstacle Design Patterns

- **Low barrier:** jump over
- **High barrier:** slide under
- **Side barrier:** switch lanes
- **Combined:** low + side forces specific lane + jump
- **Moving obstacle:** timing-based avoidance

## Performance

- Pool ALL chunks, obstacles, collectibles, and effects
- Only 3-5 chunks active at any time
- Disable renderers/colliders when chunks are pooled
- Use LOD or disable distant chunk details
- Move world toward player (or keep player stationary and move world) to avoid floating-point precision issues at large Z values
