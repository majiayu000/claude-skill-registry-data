---
name: hyper-casual
description: "Hyper-casual mobile game architecture — one-tap/swipe controls, instant onboarding, short sessions, ad monetization, minimalist visuals, level progression, score systems."
globs: ["**/HyperCasual*.cs", "**/Level*.cs", "**/GameManager*.cs"]
---

# Hyper-Casual Mobile Patterns

## Core Design Principles

- **One mechanic, perfected** — the entire game is one interaction
- **Instant onboarding** — player understands in 3 seconds, no tutorial screen
- **Short sessions** — 30-60 second rounds
- **Satisfying feedback** — haptics, screen shake, particle bursts, sound on every action
- **Endless or level-based** — simple progression keeps players coming back

## One-Tap Controller

```csharp
public sealed class TapController : MonoBehaviour
{
    [Header("Input")]
    [SerializeField] private float _tapForce = 10f;
    [SerializeField] private float _holdForceMultiplier = 0.5f;

    private Rigidbody _rb;
    private bool _isTouching;

    private void Awake()
    {
        _rb = GetComponent<Rigidbody>();
    }

    private void Update()
    {
        if (UnityEngine.InputSystem.Touchscreen.current == null) return;

        UnityEngine.InputSystem.Controls.TouchControl touch =
            UnityEngine.InputSystem.Touchscreen.current.primaryTouch;

        if (touch.press.wasPressedThisFrame)
        {
            OnTap();
        }

        _isTouching = touch.press.isPressed;
    }

    private void FixedUpdate()
    {
        if (_isTouching)
        {
            _rb.AddForce(Vector3.up * _holdForceMultiplier, ForceMode.Acceleration);
        }
    }

    private void OnTap()
    {
        _rb.linearVelocity = Vector3.zero;
        _rb.AddForce(Vector3.up * _tapForce, ForceMode.Impulse);
    }
}
```

## Swipe Controller

```csharp
public sealed class SwipeController : MonoBehaviour
{
    [SerializeField] private float _swipeThreshold = 50f;
    [SerializeField] private float _moveSpeed = 10f;
    [SerializeField] private float _laneSwitchDuration = 0.15f;

    private Vector2 _touchStartPos;
    private bool _isSwiping;

    private void Update()
    {
        if (UnityEngine.InputSystem.Touchscreen.current == null) return;

        UnityEngine.InputSystem.Controls.TouchControl touch =
            UnityEngine.InputSystem.Touchscreen.current.primaryTouch;

        if (touch.press.wasPressedThisFrame)
        {
            _touchStartPos = touch.position.ReadValue();
            _isSwiping = true;
        }

        if (touch.press.wasReleasedThisFrame && _isSwiping)
        {
            Vector2 delta = touch.position.ReadValue() - _touchStartPos;
            _isSwiping = false;

            if (delta.magnitude > _swipeThreshold)
            {
                if (Mathf.Abs(delta.x) > Mathf.Abs(delta.y))
                {
                    OnSwipeHorizontal(delta.x > 0f ? 1 : -1);
                }
                else
                {
                    OnSwipeVertical(delta.y > 0f ? 1 : -1);
                }
            }
            else
            {
                OnTap();
            }
        }
    }

    private void OnSwipeHorizontal(int direction) { /* lane switch or steer */ }
    private void OnSwipeVertical(int direction) { /* jump or duck */ }
    private void OnTap() { /* primary action */ }
}
```

## Level Progression System

```csharp
[CreateAssetMenu(menuName = "HyperCasual/Level Config")]
public sealed class LevelConfig : ScriptableObject
{
    [SerializeField] private int _levelNumber;
    [SerializeField] private float _speed = 5f;
    [SerializeField] private float _obstacleFrequency = 0.5f;
    [SerializeField] private Color _themeColor = Color.white;
    [SerializeField] private int _targetScore;

    public int LevelNumber => _levelNumber;
    public float Speed => _speed;
    public float ObstacleFrequency => _obstacleFrequency;
    public Color ThemeColor => _themeColor;
    public int TargetScore => _targetScore;
}

public sealed class LevelManager : MonoBehaviour
{
    [SerializeField] private LevelConfig[] _levels;

    private int _currentLevelIndex;
    private const string LEVEL_KEY = "CurrentLevel";

    private void Awake()
    {
        _currentLevelIndex = PlayerPrefs.GetInt(LEVEL_KEY, 0);
    }

    public LevelConfig GetCurrentLevel()
    {
        int index = _currentLevelIndex % _levels.Length;
        return _levels[index];
    }

    public void CompleteLevel()
    {
        _currentLevelIndex++;
        PlayerPrefs.SetInt(LEVEL_KEY, _currentLevelIndex);
        PlayerPrefs.Save();
    }
}
```

## Game Loop (Hyper-Casual)

```
Splash → Menu (one big PLAY button)
    → Playing (auto-forward, player reacts)
        → Game Over (score, best, retry/home)
            → Rewarded Ad (continue?) → resume or Menu
```

- **No loading screens** — instant transitions
- **No settings menus** — sound toggle only
- **Retry = instant** — no delays, no confirmation

## Monetization Hooks

- **Interstitial:** show after every 3rd game over (not on first play)
- **Rewarded:** offer continue/2x score at game over
- **Banner:** bottom of menu screen only (never during gameplay)

```csharp
public interface IAdService
{
    void ShowInterstitial(System.Action onComplete);
    void ShowRewarded(System.Action<bool> onResult);
    void ShowBanner();
    void HideBanner();
}
```

## Visual Style

- Solid colors, no textures (smallest build size)
- Primitives: cubes, spheres, cylinders
- Color palette: 3-4 colors max per level
- Camera: fixed angle or auto-follow, never player-controlled

## Performance Budget

- **< 30 draw calls** — hyper-casual games should be trivially simple to render
- **< 50MB build size** — critical for ad network installs
- **30fps** — saves battery, users don't notice for casual games
- **Zero allocations** in gameplay loop
