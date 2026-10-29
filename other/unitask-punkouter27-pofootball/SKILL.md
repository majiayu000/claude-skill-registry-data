---
name: unitask
description: "UniTask async/await for Unity — zero-alloc async, cancellation tokens, PlayerLoop integration, async LINQ. Use instead of coroutines for cancellation support and cleaner async code."
globs: ["**/UniTask*", "**/*Async*.cs", "**/Cysharp*"]
---

# UniTask — Zero-Allocation Async/Await for Unity

UniTask (Cysharp) provides async/await that integrates natively with Unity's PlayerLoop, produces zero GC allocations, and supports proper cancellation. Prefer UniTask over coroutines and `System.Threading.Tasks.Task` in all Unity projects.

## UniTask vs Coroutines vs System.Threading.Tasks.Task

| Feature | Coroutine | Task | UniTask |
|---------|-----------|------|---------|
| GC allocation | Enumerator + box | Task object + state machine | Zero (struct-based) |
| Cancellation | Manual flag | CancellationToken | CancellationToken |
| Return values | No | Yes | Yes |
| Exception handling | Swallowed silently | try/catch | try/catch |
| Runs on thread pool | No | Yes (dangerous in Unity) | No (PlayerLoop) |
| Awaitable | No | Yes | Yes |

## Basic Usage

### Method Signatures

```csharp
using Cysharp.Threading.Tasks;

// Awaitable, returns nothing
public async UniTask LoadLevelAsync(CancellationToken ct)
{
    await UniTask.Delay(1000, cancellationToken: ct);
}

// Awaitable, returns a value
public async UniTask<int> CalculateScoreAsync(CancellationToken ct)
{
    await UniTask.Yield(ct);
    return 100;
}

// Fire-and-forget (use sparingly, only at call boundaries)
public async UniTaskVoid OnButtonClickedAsync()
{
    await DoSomethingAsync(this.GetCancellationTokenOnDestroy());
}
```

### CRITICAL: Never Use async void

```csharp
// BAD — exceptions silently swallowed, no cancellation, GC allocation
public async void DoSomething() { ... }

// GOOD — proper error propagation, zero alloc
public async UniTask DoSomethingAsync(CancellationToken ct) { ... }

// GOOD — fire-and-forget with error logging
public async UniTaskVoid DoSomethingFireAndForget() { ... }
```

## Waiting and Delays

```csharp
// Time-based delays
await UniTask.Delay(1000, cancellationToken: ct);                    // Milliseconds
await UniTask.Delay(TimeSpan.FromSeconds(1.5f), cancellationToken: ct);

// Frame-based waits
await UniTask.Yield();                                                // Next frame
await UniTask.Yield(PlayerLoopTiming.FixedUpdate);                   // Next FixedUpdate
await UniTask.NextFrame(ct);                                          // Explicit next frame
await UniTask.DelayFrame(5, cancellationToken: ct);                  // Wait N frames

// Condition waits
await UniTask.WaitUntil(() => _isReady, cancellationToken: ct);
await UniTask.WaitWhile(() => _isLoading, cancellationToken: ct);
await UniTask.WaitUntilValueChanged(transform, t => t.position, cancellationToken: ct);

// Unity async operation wrappers
await SceneManager.LoadSceneAsync("GameScene").ToUniTask(cancellationToken: ct);
await Resources.LoadAsync<Texture2D>("myTexture").ToUniTask(cancellationToken: ct);
await UnityWebRequest.Get(url).SendWebRequest().ToUniTask(cancellationToken: ct);
```

## Cancellation Tokens

### CRITICAL: Always Pass Cancellation Tokens

Async operations that outlive their owning object cause `MissingReferenceException` and undefined behavior. Every async method must accept and respect a `CancellationToken`.

### Pattern 1: GetCancellationTokenOnDestroy (Simple)

```csharp
public class SimpleAsync : MonoBehaviour
{
    private async UniTaskVoid Start()
    {
        // Token auto-cancels when this MonoBehaviour is destroyed
        CancellationToken ct = this.GetCancellationTokenOnDestroy();

        await UniTask.Delay(2000, cancellationToken: ct);
        Debug.Log("This won't run if object was destroyed");
    }
}
```

### Pattern 2: Manual CancellationTokenSource (Enable/Disable)

```csharp
public class ManagedAsync : MonoBehaviour
{
    private CancellationTokenSource _cts;

    private void OnEnable()
    {
        _cts = new CancellationTokenSource();
        RunLoopAsync(_cts.Token).Forget();
    }

    private void OnDisable()
    {
        _cts?.Cancel();
        _cts?.Dispose();
        _cts = null;
    }

    private async UniTask RunLoopAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            await UniTask.Delay(1000, cancellationToken: ct);
            DoPeriodicWork();
        }
    }
}
```

### Pattern 3: Linked Tokens (Combine Destroy + Manual Cancel)

```csharp
public class LinkedTokenExample : MonoBehaviour
{
    private CancellationTokenSource _actionCts;

    public async UniTask PerformActionAsync()
    {
        // Cancel previous action if still running
        _actionCts?.Cancel();
        _actionCts?.Dispose();
        _actionCts = new CancellationTokenSource();

        // Link with destroy token so it cancels on either condition
        CancellationToken destroyCt = this.GetCancellationTokenOnDestroy();
        CancellationTokenSource linked = CancellationTokenSource.CreateLinkedTokenSource(
            _actionCts.Token, destroyCt);

        try
        {
            await DoWorkAsync(linked.Token);
        }
        catch (OperationCanceledException)
        {
            // Expected on cancellation — do nothing
        }
        finally
        {
            linked.Dispose();
        }
    }
}
```

### Handling OperationCanceledException

```csharp
public async UniTask LoadDataAsync(CancellationToken ct)
{
    try
    {
        await SomeAsyncOperation(ct);
    }
    catch (OperationCanceledException)
    {
        // Normal cancellation — cleanup silently
        return;
    }
    catch (Exception ex)
    {
        // Actual error — log and handle
        Debug.LogException(ex);
    }
}
```

## PlayerLoop Integration

UniTask hooks into Unity's PlayerLoop for precise timing control.

```csharp
// Available timing points
await UniTask.Yield(PlayerLoopTiming.Initialization);
await UniTask.Yield(PlayerLoopTiming.EarlyUpdate);
await UniTask.Yield(PlayerLoopTiming.FixedUpdate);
await UniTask.Yield(PlayerLoopTiming.PreUpdate);
await UniTask.Yield(PlayerLoopTiming.Update);
await UniTask.Yield(PlayerLoopTiming.PreLateUpdate);
await UniTask.Yield(PlayerLoopTiming.PostLateUpdate);
await UniTask.Yield(PlayerLoopTiming.LastPostLateUpdate);

// Wait for specific timing in FixedUpdate
await UniTask.WaitForFixedUpdate(ct);

// Wait for end of frame (replacement for WaitForEndOfFrame coroutine)
await UniTask.Yield(PlayerLoopTiming.LastPostLateUpdate, ct);
```

## WhenAll / WhenAny — Parallel Execution

```csharp
// Wait for all tasks to complete (parallel)
(int score, string name) = await UniTask.WhenAll(
    LoadScoreAsync(ct),
    LoadNameAsync(ct)
);

// Wait for first task to complete
int winnerIndex = await UniTask.WhenAny(
    WaitForInputAsync(ct),
    WaitForTimeoutAsync(5f, ct)
);

// Typed WhenAny with result
(bool hasResult, int result) = await UniTask.WhenAny(
    FetchFromCacheAsync(ct),
    FetchFromNetworkAsync(ct)
);

// Load multiple assets in parallel
var textures = await UniTask.WhenAll(
    paths.Select(p => LoadTextureAsync(p, ct))
);
```

## Forget and Fire-and-Forget

```csharp
// Fire and forget — logs exceptions to Debug.LogException
DoSomethingAsync(ct).Forget();

// Suppress specific cancellation exceptions
DoSomethingAsync(ct).SuppressCancellationThrow().Forget();
```

## UniTaskCompletionSource — Manual Completion

For wrapping callback-based APIs or creating custom awaitable operations.

```csharp
public class DialogSystem : MonoBehaviour
{
    private UniTaskCompletionSource<DialogResult> _dialogTcs;

    public async UniTask<DialogResult> ShowDialogAsync(string message, CancellationToken ct)
    {
        _dialogTcs = new UniTaskCompletionSource<DialogResult>();

        // Register cancellation
        ct.Register(() => _dialogTcs.TrySetCanceled());

        ShowDialogUI(message);
        return await _dialogTcs.Task;
    }

    // Called by UI buttons
    public void OnConfirmClicked() => _dialogTcs.TrySetResult(DialogResult.Confirm);
    public void OnCancelClicked() => _dialogTcs.TrySetResult(DialogResult.Cancel);
}
```

## Async LINQ

UniTask provides async LINQ operators for event streams.

```csharp
using Cysharp.Threading.Tasks.Linq;

// Async event stream from button clicks
button.OnClickAsAsyncEnumerable()
    .ForEachAsync(_ =>
    {
        Debug.Log("Clicked");
    }, ct);

// Throttled input
button.OnClickAsAsyncEnumerable()
    .ThrottleFirst(TimeSpan.FromSeconds(1))
    .ForEachAsync(_ => ProcessClick(), ct);

// Channel-based producer/consumer
var channel = Channel.CreateSingleConsumerUnbounded<int>();
channel.Writer.TryWrite(42);
await channel.Reader.ReadAllAsync(ct).ForEachAsync(item => Process(item));
```

## Integration with DOTween

Await DOTween animations using the DOTween-UniTask bridge.

```csharp
// Await a single tween
await transform.DOMove(targetPos, 1f)
    .SetEase(Ease.OutQuad)
    .ToUniTask(cancellationToken: ct);

// Await a sequence
Sequence seq = DOTween.Sequence();
seq.Append(transform.DOScale(1.2f, 0.2f));
seq.Append(transform.DOScale(1f, 0.2f));
await seq.ToUniTask(cancellationToken: ct);

// Sequential animation chain
await transform.DOMove(pointA, 0.5f).ToUniTask(cancellationToken: ct);
await transform.DOMove(pointB, 0.5f).ToUniTask(cancellationToken: ct);
await transform.DOMove(pointC, 0.5f).ToUniTask(cancellationToken: ct);
```

## Integration with Addressables

```csharp
// Load asset
GameObject prefab = await Addressables.LoadAssetAsync<GameObject>("EnemyPrefab")
    .ToUniTask(cancellationToken: ct);

// Instantiate
GameObject instance = await Addressables.InstantiateAsync("EnemyPrefab", position, rotation)
    .ToUniTask(cancellationToken: ct);

// Load scene
await Addressables.LoadSceneAsync("GameScene", LoadSceneMode.Additive)
    .ToUniTask(cancellationToken: ct);
```

## Common Patterns

### Async Initialization Chain

```csharp
public class GameBootstrap : MonoBehaviour
{
    private async UniTaskVoid Start()
    {
        CancellationToken ct = this.GetCancellationTokenOnDestroy();

        try
        {
            await InitializeServicesAsync(ct);
            await LoadPlayerDataAsync(ct);
            await PreloadAssetsAsync(ct);
            await LoadGameSceneAsync(ct);
        }
        catch (OperationCanceledException)
        {
            Debug.Log("Bootstrap cancelled");
        }
        catch (Exception ex)
        {
            Debug.LogException(ex);
        }
    }
}
```

### Async State Machine

```csharp
public class EnemyAI : MonoBehaviour
{
    private CancellationTokenSource _cts;

    private void OnEnable()
    {
        _cts = new CancellationTokenSource();
        RunAIAsync(_cts.Token).Forget();
    }

    private void OnDisable()
    {
        _cts?.Cancel();
        _cts?.Dispose();
    }

    private async UniTask RunAIAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            await PatrolAsync(ct);
            await ChaseAsync(ct);
            await AttackAsync(ct);
            await UniTask.Yield(ct);
        }
    }

    private async UniTask PatrolAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested && !CanSeePlayer())
        {
            MoveToNextWaypoint();
            await UniTask.Delay(100, cancellationToken: ct);
        }
    }
}
```

### Timeout Wrapper

```csharp
public static async UniTask<T> WithTimeout<T>(
    UniTask<T> task,
    float timeoutSeconds,
    CancellationToken ct)
{
    int winnerIndex = await UniTask.WhenAny(
        task,
        UniTask.Delay(TimeSpan.FromSeconds(timeoutSeconds), cancellationToken: ct)
            .ContinueWith(() => default(T))
    );

    if (winnerIndex == 1)
        throw new TimeoutException($"Operation timed out after {timeoutSeconds}s");

    return await task;
}
```

### Debounced Input

```csharp
private async UniTask ProcessSearchInputAsync(TMP_InputField input, CancellationToken ct)
{
    string previousText = string.Empty;

    while (!ct.IsCancellationRequested)
    {
        await UniTask.WaitUntilValueChanged(input, i => i.text, cancellationToken: ct);

        // Debounce: wait 300ms after last change
        await UniTask.Delay(300, cancellationToken: ct);

        string currentText = input.text;
        if (currentText != previousText)
        {
            previousText = currentText;
            await PerformSearchAsync(currentText, ct);
        }
    }
}
```

## Anti-Patterns

### Do not use async void anywhere

```csharp
// BAD — exception vanishes, no cancellation
public async void OnButtonClicked() { ... }

// GOOD
public async UniTaskVoid OnButtonClickedAsync()
{
    CancellationToken ct = this.GetCancellationTokenOnDestroy();
    await HandleClickAsync(ct);
}
```

### Do not forget cancellation tokens

```csharp
// BAD — runs forever even after object is destroyed
public async UniTask BadMethod()
{
    await UniTask.Delay(5000);
    transform.position = Vector3.zero; // MissingReferenceException if destroyed
}

// GOOD
public async UniTask GoodMethod(CancellationToken ct)
{
    await UniTask.Delay(5000, cancellationToken: ct);
    transform.position = Vector3.zero;
}
```

### Do not use Task.Run or Task.Delay in Unity

```csharp
// BAD — runs on thread pool, not main thread
await Task.Run(() => transform.position = Vector3.zero);

// BAD — System.Threading timer, not Unity time-aware
await Task.Delay(1000);

// GOOD
await UniTask.SwitchToMainThread();
await UniTask.Delay(1000);
```
