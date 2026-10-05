---
name: platformer-2d
description: "2D platformer architecture — tight controls (coyote time, input buffer, variable jump), level design patterns, collectibles, checkpoints, hazards, boss patterns."
globs: ["**/Platform*.cs", "**/Player*.cs", "**/Level*.cs"]
---

# 2D Platformer Patterns

## Controller Feel — The Numbers That Matter

```csharp
public sealed class PlatformerController : MonoBehaviour
{
    [Header("Movement")]
    [SerializeField] private float _moveSpeed = 8f;
    [SerializeField] private float _acceleration = 50f;
    [SerializeField] private float _deceleration = 60f;
    [SerializeField] private float _airControlMultiplier = 0.65f;

    [Header("Jump")]
    [SerializeField] private float _jumpForce = 16f;
    [SerializeField] private float _fallMultiplier = 2.5f;
    [SerializeField] private float _lowJumpMultiplier = 2f;
    [SerializeField] private float _coyoteTime = 0.1f;
    [SerializeField] private float _jumpBufferTime = 0.15f;
    [SerializeField] private float _apexHangMultiplier = 0.5f;
    [SerializeField] private float _apexThreshold = 1.5f;

    [Header("Ground Check")]
    [SerializeField] private Transform _groundCheck;
    [SerializeField] private float _groundCheckRadius = 0.15f;
    [SerializeField] private LayerMask _groundLayer;

    private Rigidbody2D _rb;
    private float _coyoteTimer;
    private float _jumpBufferTimer;
    private bool _isGrounded;
    private bool _jumpHeld;

    private void Awake()
    {
        _rb = GetComponent<Rigidbody2D>();
    }

    // Input is forwarded from InputView via these methods — never read Input.* here.
    public void SetMoveInput(float horizontal) => _horizontalInput = horizontal;
    public void OnJumpPressed()
    {
        _jumpBufferTimer = _jumpBufferTime;
        _jumpHeld = true;
    }
    public void OnJumpReleased() => _jumpHeld = false;

    private float _horizontalInput;

    private void Update()
    {
        // Ground check
        _isGrounded = Physics2D.OverlapCircle(_groundCheck.position, _groundCheckRadius, _groundLayer);

        // Coyote time
        if (_isGrounded) _coyoteTimer = _coyoteTime;
        else _coyoteTimer -= Time.deltaTime;

        _jumpBufferTimer -= Time.deltaTime;

        // Trigger jump
        if (_jumpBufferTimer > 0f && _coyoteTimer > 0f)
        {
            _rb.linearVelocity = new Vector2(_rb.linearVelocity.x, _jumpForce);
            _jumpBufferTimer = 0f;
            _coyoteTimer = 0f;
        }
    }

    private void FixedUpdate()
    {
        // Horizontal movement with acceleration
        float targetSpeed = _horizontalInput * _moveSpeed;
        float accel = _isGrounded ? _acceleration : _acceleration * _airControlMultiplier;
        float decel = _isGrounded ? _deceleration : _deceleration * _airControlMultiplier;
        float rate = Mathf.Abs(targetSpeed) > 0.01f ? accel : decel;

        float newSpeedX = Mathf.MoveTowards(_rb.linearVelocity.x, targetSpeed, rate * Time.fixedDeltaTime);
        _rb.linearVelocity = new Vector2(newSpeedX, _rb.linearVelocity.y);

        // Variable jump height + apex hang
        float yVel = _rb.linearVelocity.y;
        if (yVel < 0f)
        {
            // Falling — faster fall
            _rb.linearVelocity += Vector2.up * (Physics2D.gravity.y * (_fallMultiplier - 1f) * Time.fixedDeltaTime);
        }
        else if (yVel > 0f && !_jumpHeld)
        {
            // Released jump early — cut height
            _rb.linearVelocity += Vector2.up * (Physics2D.gravity.y * (_lowJumpMultiplier - 1f) * Time.fixedDeltaTime);
        }

        // Apex hang — slow gravity near jump apex for more control
        if (Mathf.Abs(yVel) < _apexThreshold)
        {
            _rb.linearVelocity += Vector2.up * (Physics2D.gravity.y * (_apexHangMultiplier - 1f) * Time.fixedDeltaTime);
        }
    }
}
```

## Wall Slide / Wall Jump

```csharp
// In Update:
bool isTouchingWall = Physics2D.Raycast(transform.position, facingDirection, 0.5f, _groundLayer);
bool isWallSliding = isTouchingWall && !_isGrounded && _rb.linearVelocity.y < 0f;

if (isWallSliding)
{
    // Apply wall slide friction (cap fall speed)
    _rb.linearVelocity = new Vector2(_rb.linearVelocity.x,
        Mathf.Max(_rb.linearVelocity.y, -_wallSlideSpeed));
}

// Wall jump: jump away from wall
if (_jumpBufferTimer > 0f && isWallSliding)
{
    _rb.linearVelocity = new Vector2(-facingDirection.x * _wallJumpForce.x, _wallJumpForce.y);
    _jumpBufferTimer = 0f;
}
```

## Dash

```csharp
private bool _canDash = true;
private float _dashCooldown = 0.5f;

private IEnumerator Dash(Vector2 direction)
{
    _canDash = false;
    _rb.gravityScale = 0f;
    _rb.linearVelocity = direction.normalized * _dashSpeed;

    // I-frames during dash
    Physics2D.IgnoreLayerCollision(playerLayer, enemyLayer, true);

    yield return _dashDuration; // cached WaitForSeconds

    _rb.gravityScale = _defaultGravity;
    Physics2D.IgnoreLayerCollision(playerLayer, enemyLayer, false);

    yield return new WaitForSeconds(_dashCooldown);
    _canDash = true;
}
```

## One-Way Platforms

Use `PlatformEffector2D` with `surfaceArc = 180` and `useOneWay = true`.

Drop through: temporarily disable collider or set the effector's `rotationalOffset`.

## Level Design Patterns

- **Tilemap-based:** Rule Tiles for auto-tiling, Tile Palette for painting
- **Chunk loading:** divide large levels into chunks, load/unload based on player position
- **Parallax scrolling:** multiple background layers at different speeds

## Checkpoint System

```csharp
public sealed class Checkpoint : MonoBehaviour
{
    [SerializeField] private VoidEventChannel _onCheckpointReached;

    private static Vector3 _lastCheckpointPosition;

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
        {
            _lastCheckpointPosition = transform.position;
            _onCheckpointReached.Raise();
        }
    }

    public static Vector3 GetRespawnPosition() => _lastCheckpointPosition;
}
```

## Boss Patterns

Phase-based state machine:
1. **Phase 1** (100-66% HP): basic attack pattern, vulnerable after combo
2. **Phase 2** (66-33% HP): faster attacks, new moves, environment hazards
3. **Phase 3** (33-0% HP): enraged, all attacks, short vulnerable windows
