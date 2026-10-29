---
name: dotween
description: "DOTween animation library — sequence composition, tween lifecycle, easing, kill strategies. CRITICAL: Always kill tweens in OnDestroy to prevent leaks and errors."
globs: ["**/DOTween*", "**/*Tween*.cs", "**/*Animation*.cs"]
---

# DOTween Animation Library

DOTween (Demigiant) is the standard tweening library for Unity. It provides fluent, chainable methods for animating transforms, UI elements, materials, and arbitrary values with minimal boilerplate.

## Basic Tweens

Every shortcut method follows the pattern `target.DO[Property](endValue, duration)`.

```csharp
// Transform tweens
transform.DOMove(new Vector3(0, 5, 0), 1f);           // World position
transform.DOLocalMove(new Vector3(0, 5, 0), 1f);      // Local position
transform.DOScale(Vector3.one * 1.5f, 0.3f);          // Scale
transform.DORotate(new Vector3(0, 180, 0), 0.5f);     // Euler rotation
transform.DOLocalRotateQuaternion(targetRot, 0.5f);   // Quaternion rotation

// UI tweens (CanvasGroup, Image, etc.)
canvasGroup.DOFade(0f, 0.5f);                         // Alpha fade
image.DOColor(Color.red, 0.2f);                       // Color change
image.DOFillAmount(1f, 1f);                            // Fill bar
rectTransform.DOAnchorPos(Vector2.zero, 0.3f);        // UI position

// Material tweens — NEVER use renderer.material (clones material, breaks batching).
// Use MaterialPropertyBlock for per-instance changes, or tween a shared material if all instances share the tween.
private static readonly int ColorId = Shader.PropertyToID("_Color");
private MaterialPropertyBlock _propBlock;

Color from = Color.black;
DOTween.To(() => from, c =>
{
    from = c;
    _propBlock.SetColor(ColorId, c);
    renderer.SetPropertyBlock(_propBlock);
}, Color.white, 0.1f);

// Arbitrary value tween
float value = 0f;
DOTween.To(() => value, x => value = x, 10f, 1f);
```

## Sequence Composition

Sequences let you chain, overlap, and orchestrate multiple tweens as a single unit.

```csharp
Sequence seq = DOTween.Sequence();

// Append — plays after previous tween finishes
seq.Append(transform.DOMove(targetPos, 0.5f));
seq.Append(transform.DOScale(Vector3.one * 1.2f, 0.3f));

// Join — plays at the same time as the previous tween
seq.Append(transform.DOMove(targetPos, 0.5f));
seq.Join(transform.DORotate(new Vector3(0, 360, 0), 0.5f));

// Insert — plays at a specific time position in the sequence
seq.Insert(0.2f, canvasGroup.DOFade(1f, 0.3f));

// Intervals and callbacks
seq.PrependInterval(0.5f);                             // Delay before sequence starts
seq.AppendInterval(0.2f);                              // Pause between tweens
seq.AppendCallback(() => Debug.Log("Done!"));
seq.InsertCallback(1f, () => PlaySound());

// Sequence settings
seq.SetLoops(3, LoopType.Yoyo);
seq.SetUpdate(true);                                   // Unscaled time
seq.OnComplete(() => Destroy(gameObject));
```

### Nested Sequences

```csharp
Sequence innerSeq = DOTween.Sequence();
innerSeq.Append(transform.DOScale(1.2f, 0.15f));
innerSeq.Append(transform.DOScale(1f, 0.15f));

Sequence outerSeq = DOTween.Sequence();
outerSeq.Append(transform.DOMove(targetPos, 0.5f));
outerSeq.Append(innerSeq);
```

## Easing

Easing controls the interpolation curve. Choose based on the feel you want.

```csharp
transform.DOMove(target, 0.5f).SetEase(Ease.OutBounce);
transform.DOScale(1.2f, 0.2f).SetEase(Ease.OutBack);          // Pop/overshoot
transform.DOMove(target, 1f).SetEase(Ease.InOutQuad);          // Smooth start/stop
canvasGroup.DOFade(0f, 0.3f).SetEase(Ease.InQuad);             // Accelerate out
```

### Common Eases for Game Feel

| Ease | Use Case |
|------|----------|
| `Ease.OutBack` | Button press pop, element appearing with overshoot |
| `Ease.OutBounce` | Landing, dropping items |
| `Ease.InOutQuad` | Smooth camera moves, panel slides |
| `Ease.OutQuad` | Natural deceleration, most general-purpose |
| `Ease.InBack` | Element leaving with anticipation |
| `Ease.OutElastic` | Springy, playful UI elements |
| `Ease.Linear` | Progress bars, constant-speed movement |

### Custom Ease Curves

```csharp
[SerializeField] private AnimationCurve _customEase;
transform.DOMove(target, 1f).SetEase(_customEase);
```

## CRITICAL: Tween Lifecycle and Kill Strategy

**Always kill tweens when the owning object is destroyed.** Tweens that target destroyed objects cause `MissingReferenceException` and memory leaks.

```csharp
public class AnimatedElement : MonoBehaviour
{
    private Tween _activeTween;

    public void PlayAnimation()
    {
        // Kill any existing tween before starting a new one
        _activeTween?.Kill();
        _activeTween = transform.DOScale(1.2f, 0.3f)
            .SetEase(Ease.OutBack);
    }

    private void OnDestroy()
    {
        // CRITICAL: Kill all tweens targeting this transform
        transform.DOKill();

        // If you used SetId(this), also kill by ID:
        // DOTween.Kill(this);

        // Or kill a specific stored tween:
        // _activeTween?.Kill();
    }
}
```

### Kill Methods

```csharp
transform.DOKill();                  // Kill all tweens on this transform
transform.DOKill(true);              // Kill and force completion
DOTween.Kill(this);                  // Kill tweens with this object as ID
DOTween.Kill("myTween");             // Kill tweens with string ID
DOTween.KillAll();                   // Nuclear option — kill everything
tween.Kill();                        // Kill a specific tween reference
```

## Tween IDs

Tag tweens with IDs for targeted operations.

```csharp
transform.DOMove(target, 1f).SetId(this);          // Object ID
transform.DOMove(target, 1f).SetId("uiTransition"); // String ID

// Later: kill, pause, or play by ID
DOTween.Kill("uiTransition");
DOTween.Pause(this);
DOTween.Play(this);
```

## SetAutoKill and Reusable Tweens

By default, tweens auto-destroy on completion. Disable for reusable tweens.

```csharp
private Tween _bounceTween;

private void Awake()
{
    _bounceTween = transform.DOScale(1.2f, 0.15f)
        .SetEase(Ease.OutBack)
        .SetAutoKill(false)
        .SetLoops(2, LoopType.Yoyo)
        .Pause();                    // Create paused, play on demand
}

public void Bounce()
{
    _bounceTween.Restart();         // Replay from beginning
}

private void OnDestroy()
{
    _bounceTween?.Kill();           // Must kill manually since AutoKill is off
}
```

## SetUpdate — Unscaled Time

For animations that should play during pause (Time.timeScale = 0):

```csharp
// Pause menu fade-in plays even when game is paused
canvasGroup.DOFade(1f, 0.3f).SetUpdate(true);

// Also works on sequences
DOTween.Sequence()
    .Append(panel.DOAnchorPos(Vector2.zero, 0.3f))
    .SetUpdate(true);
```

## SetCapacity — Startup Performance

Call once at application startup to pre-allocate tween capacity and avoid runtime resizing.

```csharp
// In a bootstrap MonoBehaviour or RuntimeInitializeOnLoadMethod
[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
private static void InitDOTween()
{
    DOTween.SetTweensCapacity(500, 50); // 500 tweeners, 50 sequences
}
```

## Punch and Shake — Game Juice

Short, impactful animations for feedback.

```csharp
// Punch — snaps back to original value
transform.DOPunchScale(Vector3.one * 0.2f, 0.3f, 6, 0.5f);
transform.DOPunchPosition(new Vector3(0, 30, 0), 0.4f, 8, 0.5f);
transform.DOPunchRotation(new Vector3(0, 0, 15), 0.3f, 8, 0.5f);

// Shake — random oscillation
transform.DOShakePosition(0.5f, strength: 10f, vibrato: 10, randomness: 90);
transform.DOShakeScale(0.3f, 0.5f);
transform.DOShakeRotation(0.5f, new Vector3(0, 0, 30));

// Camera shake
Camera.main.DOShakePosition(0.3f, 0.5f, 14, 90, false, true);
```

## Path Tweens

Move along a series of waypoints.

```csharp
Vector3[] waypoints = new[]
{
    new Vector3(0, 0, 0),
    new Vector3(5, 2, 0),
    new Vector3(10, 0, 0),
    new Vector3(15, 3, 0),
};

transform.DOPath(waypoints, 3f, PathType.CatmullRom)
    .SetEase(Ease.InOutQuad)
    .SetLookAt(0.01f);               // Face movement direction
```

## Common Patterns

### Button Press Feedback

```csharp
public class ButtonFeedback : MonoBehaviour, IPointerDownHandler, IPointerUpHandler
{
    private static readonly Vector3 PressScale = Vector3.one * 0.9f;

    public void OnPointerDown(PointerEventData eventData)
    {
        transform.DOKill();
        transform.DOScale(PressScale, 0.1f).SetEase(Ease.OutQuad);
    }

    public void OnPointerUp(PointerEventData eventData)
    {
        transform.DOKill();
        transform.DOScale(Vector3.one, 0.15f).SetEase(Ease.OutBack);
    }

    private void OnDestroy() => transform.DOKill();
}
```

### Screen Transition

```csharp
public class ScreenTransition : MonoBehaviour
{
    [SerializeField] private CanvasGroup _canvasGroup;
    [SerializeField] private RectTransform _panel;

    public Tween Show()
    {
        _canvasGroup.alpha = 0f;
        _panel.anchoredPosition = new Vector2(0, -50f);

        Sequence seq = DOTween.Sequence();
        seq.Append(_canvasGroup.DOFade(1f, 0.25f));
        seq.Join(_panel.DOAnchorPos(Vector2.zero, 0.3f).SetEase(Ease.OutQuad));
        return seq;
    }

    public Tween Hide()
    {
        Sequence seq = DOTween.Sequence();
        seq.Append(_canvasGroup.DOFade(0f, 0.2f));
        seq.Join(_panel.DOAnchorPos(new Vector2(0, 50f), 0.25f).SetEase(Ease.InQuad));
        return seq;
    }

    private void OnDestroy()
    {
        _canvasGroup.DOKill();
        _panel.DOKill();
    }
}
```

### Damage Flash

```csharp
public void FlashDamage(SpriteRenderer sr)
{
    sr.DOKill();
    Sequence seq = DOTween.Sequence();
    seq.Append(sr.DOColor(Color.red, 0.05f));
    seq.Append(sr.DOColor(Color.white, 0.15f));
    seq.SetId(sr);
}
```

### Collect Animation

```csharp
public void PlayCollectAnimation(Transform item, Vector3 targetUIPos)
{
    Sequence seq = DOTween.Sequence();
    seq.Append(item.DOScale(1.3f, 0.15f).SetEase(Ease.OutBack));
    seq.Append(item.DOMove(targetUIPos, 0.4f).SetEase(Ease.InBack));
    seq.Join(item.DOScale(0f, 0.3f).SetEase(Ease.InQuad));
    seq.OnComplete(() => Destroy(item.gameObject));
}
```

## Anti-Patterns

### DO NOT create tweens in Update

```csharp
// BAD — creates a new tween every frame, massive leak
private void Update()
{
    transform.DOMove(target.position, 0.5f);
}

// GOOD — create once, update target differently
private Tween _moveTween;
public void MoveTo(Vector3 target)
{
    _moveTween?.Kill();
    _moveTween = transform.DOMove(target, 0.5f);
}
```

### DO NOT forget to kill on destroy

```csharp
// BAD — tween continues after object is destroyed
public void Animate()
{
    transform.DOScale(2f, 5f).OnComplete(() => DoSomething());
}

// GOOD — always have a kill strategy
private void OnDestroy() => transform.DOKill();
```

### DO NOT create infinite loops without a kill strategy

```csharp
// BAD — no way to stop this
transform.DORotate(new Vector3(0, 360, 0), 2f, RotateMode.FastBeyond360)
    .SetLoops(-1, LoopType.Restart);

// GOOD — store reference and kill in OnDestroy
private Tween _spinTween;
private void Start()
{
    _spinTween = transform.DORotate(new Vector3(0, 360, 0), 2f, RotateMode.FastBeyond360)
        .SetLoops(-1, LoopType.Restart)
        .SetId(this);
}
private void OnDestroy() => DOTween.Kill(this);
```

## Callbacks

```csharp
transform.DOMove(target, 1f)
    .OnStart(() => Debug.Log("Started"))
    .OnUpdate(() => Debug.Log("Updating"))
    .OnComplete(() => Debug.Log("Done"))
    .OnKill(() => Debug.Log("Killed"))
    .OnStepComplete(() => Debug.Log("Loop step done"));
```

## Tween Control

```csharp
Tween tween = transform.DOMove(target, 1f);

tween.Pause();
tween.Play();
tween.Restart();
tween.Rewind();
tween.Complete();             // Jump to end
tween.Goto(0.5f, true);      // Jump to time, and play
tween.PlayForward();
tween.PlayBackwards();
tween.Flip();                 // Reverse direction
```
