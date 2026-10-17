---
name: addressables
description: "Addressables asset loading — LoadAssetAsync, handle lifecycle, labels, remote catalogs, memory management. Use for asset loading and memory optimization."
globs: ["**/Addressable*.cs", "**/*Address*"]
---

# Unity Addressables

## Setup

1. Install via Package Manager: `com.unity.addressables`
2. Mark assets as Addressable in the Inspector checkbox
3. Organize into Groups (local, remote, by scene, by feature)
4. Assign Labels for batch loading (e.g., "level1", "enemies", "ui")

### Group Organization Strategy

```
Groups:
  Local_Static       -- Core assets, always available (shaders, essential UI)
  Local_Dynamic      -- Assets that change between builds
  Remote_Levels      -- Level-specific assets, downloaded on demand
  Remote_Characters  -- Character models/animations
```

## Loading Assets

### Basic Asset Loading

```csharp
using UnityEngine;
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

public class AddressableLoader : MonoBehaviour
{
    [SerializeField] private AssetReference prefabReference;

    private AsyncOperationHandle<GameObject> _loadHandle;
    private GameObject _instance;

    public async void LoadAndInstantiate()
    {
        _loadHandle = Addressables.LoadAssetAsync<GameObject>(prefabReference);
        await _loadHandle.Task;

        if (_loadHandle.Status == AsyncOperationStatus.Succeeded)
        {
            _instance = Instantiate(_loadHandle.Result);
        }
        else
        {
            Debug.LogError($"Failed to load addressable: {_loadHandle.OperationException}");
        }
    }

    // CRITICAL: Always release handles to prevent memory leaks
    private void OnDestroy()
    {
        if (_loadHandle.IsValid())
        {
            Addressables.Release(_loadHandle);
        }

        if (_instance != null)
        {
            Destroy(_instance);
        }
    }
}
```

### InstantiateAsync (Load + Instantiate in One Call)

```csharp
public class AddressableInstantiator : MonoBehaviour
{
    [SerializeField] private AssetReference prefabReference;
    private AsyncOperationHandle<GameObject> _instanceHandle;

    public async void SpawnObject(Vector3 position, Quaternion rotation)
    {
        _instanceHandle = Addressables.InstantiateAsync(prefabReference, position, rotation);
        await _instanceHandle.Task;

        if (_instanceHandle.Status != AsyncOperationStatus.Succeeded)
        {
            Debug.LogError("Failed to instantiate addressable");
        }
    }

    private void OnDestroy()
    {
        // ReleaseInstance destroys the object AND releases the handle
        if (_instanceHandle.IsValid())
        {
            Addressables.ReleaseInstance(_instanceHandle);
        }
    }
}
```

## Handle Lifecycle (CRITICAL)

Every `LoadAssetAsync` or `InstantiateAsync` call returns a handle that MUST be released.

### Rules

1. **Every load must have a matching release.** No exceptions.
2. **Track all handles.** Store them in fields or a list.
3. **Release on destroy.** Use OnDestroy or a dedicated cleanup method.
4. **Check IsValid() before releasing.** Prevents double-release errors.

### Handle Tracking Pattern

```csharp
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

public class AddressableManager : MonoBehaviour
{
    private readonly List<AsyncOperationHandle> _handles = new();

    public AsyncOperationHandle<T> LoadAsset<T>(object key)
    {
        var handle = Addressables.LoadAssetAsync<T>(key);
        _handles.Add(handle);
        return handle;
    }

    public AsyncOperationHandle<GameObject> InstantiateAsset(AssetReference reference,
        Vector3 position = default, Quaternion rotation = default)
    {
        var handle = Addressables.InstantiateAsync(reference, position, rotation);
        _handles.Add(handle);
        return handle;
    }

    public void ReleaseAll()
    {
        foreach (var handle in _handles)
        {
            if (handle.IsValid())
            {
                Addressables.Release(handle);
            }
        }
        _handles.Clear();
    }

    private void OnDestroy()
    {
        ReleaseAll();
    }
}
```

## Label-Based Loading

Load multiple assets sharing a label in a single call.

```csharp
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

public class LevelAssetLoader : MonoBehaviour
{
    private AsyncOperationHandle<IList<GameObject>> _levelAssetsHandle;

    public async void LoadLevelAssets(string levelLabel)
    {
        _levelAssetsHandle = Addressables.LoadAssetsAsync<GameObject>(
            levelLabel,
            prefab =>
            {
                // Called for EACH asset as it loads
                Debug.Log($"Loaded: {prefab.name}");
            });

        await _levelAssetsHandle.Task;

        if (_levelAssetsHandle.Status == AsyncOperationStatus.Succeeded)
        {
            Debug.Log($"All {_levelAssetsHandle.Result.Count} assets loaded for {levelLabel}");
        }
    }

    public void UnloadLevelAssets()
    {
        if (_levelAssetsHandle.IsValid())
        {
            Addressables.Release(_levelAssetsHandle);
        }
    }
}
```

## Asset Reference Types

```csharp
using UnityEngine;
using UnityEngine.AddressableAssets;

public class TypedReferences : MonoBehaviour
{
    // Generic reference — loads as UnityEngine.Object
    [SerializeField] private AssetReference genericRef;

    // Typed references — type-safe in Inspector
    [SerializeField] private AssetReferenceGameObject prefabRef;
    [SerializeField] private AssetReferenceTexture2D textureRef;
    [SerializeField] private AssetReferenceSprite spriteRef;
    [SerializeField] private AssetReferenceT<AudioClip> audioRef;
    [SerializeField] private AssetReferenceT<ScriptableObject> dataRef;

    // AssetLabelReference — reference a label for batch loading
    [SerializeField] private AssetLabelReference enemyLabel;

    public async void LoadTypedAssets()
    {
        var prefab = await prefabRef.LoadAssetAsync<GameObject>().Task;
        var texture = await textureRef.LoadAssetAsync<Texture2D>().Task;
        var clip = await audioRef.LoadAssetAsync<AudioClip>().Task;
    }
}
```

## Memory Leak Prevention

### Common Mistakes

```csharp
// BAD: Handle lost, can never release
public void LeakyLoad()
{
    Addressables.LoadAssetAsync<GameObject>("enemy"); // Handle not stored!
}

// BAD: Releasing too early
public async void TooEarlyRelease()
{
    var handle = Addressables.LoadAssetAsync<GameObject>("enemy");
    await handle.Task;
    var instance = Instantiate(handle.Result);
    Addressables.Release(handle); // Releases while instance still uses the asset!
}

// GOOD: Proper lifecycle
private AsyncOperationHandle<GameObject> _handle;
private GameObject _instance;

public async void ProperLoad()
{
    _handle = Addressables.LoadAssetAsync<GameObject>("enemy");
    await _handle.Task;
    _instance = Instantiate(_handle.Result);
}

private void OnDestroy()
{
    if (_instance != null) Destroy(_instance);
    if (_handle.IsValid()) Addressables.Release(_handle);
}
```

## Remote Catalog Updates

```csharp
using UnityEngine;
using UnityEngine.AddressableAssets;
using System.Collections.Generic;

public class CatalogUpdater : MonoBehaviour
{
    public async void CheckForUpdates()
    {
        var checkHandle = Addressables.CheckForCatalogUpdates(false);
        await checkHandle.Task;

        if (checkHandle.Status == AsyncOperationStatus.Succeeded)
        {
            List<string> catalogs = checkHandle.Result as List<string>;
            if (catalogs != null && catalogs.Count > 0)
            {
                Debug.Log($"Found {catalogs.Count} catalog updates");
                var updateHandle = Addressables.UpdateCatalogs(catalogs, false);
                await updateHandle.Task;
                Debug.Log("Catalogs updated successfully");
                Addressables.Release(updateHandle);
            }
        }
        Addressables.Release(checkHandle);
    }
}
```

## Preloading Assets

```csharp
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

public class AssetPreloader : MonoBehaviour
{
    [SerializeField] private List<AssetReference> assetsToPreload;
    private readonly List<AsyncOperationHandle> _preloadHandles = new();

    public async Awaitable PreloadAll()
    {
        var tasks = new List<System.Threading.Tasks.Task>();

        foreach (var assetRef in assetsToPreload)
        {
            var handle = Addressables.LoadAssetAsync<Object>(assetRef);
            _preloadHandles.Add(handle);
            tasks.Add(handle.Task);
        }

        await System.Threading.Tasks.Task.WhenAll(tasks);
        Debug.Log($"Preloaded {_preloadHandles.Count} assets");
    }

    public float GetProgress()
    {
        if (_preloadHandles.Count == 0) return 0f;

        float total = 0f;
        foreach (var handle in _preloadHandles)
        {
            total += handle.PercentComplete;
        }
        return total / _preloadHandles.Count;
    }

    private void OnDestroy()
    {
        foreach (var handle in _preloadHandles)
        {
            if (handle.IsValid()) Addressables.Release(handle);
        }
        _preloadHandles.Clear();
    }
}
```

## Integration with UniTask

UniTask provides zero-allocation async/await. Convert Addressable handles:

```csharp
using Cysharp.Threading.Tasks;
using UnityEngine;
using UnityEngine.AddressableAssets;

public class AddressableUniTaskLoader : MonoBehaviour
{
    public async UniTask<GameObject> LoadPrefab(string address,
        System.Threading.CancellationToken ct = default)
    {
        var handle = Addressables.LoadAssetAsync<GameObject>(address);
        var result = await handle.ToUniTask(cancellationToken: ct);
        return result;
    }

    public async UniTask<T> LoadAsset<T>(AssetReferenceT<T> reference,
        System.Threading.CancellationToken ct = default) where T : Object
    {
        return await reference.LoadAssetAsync<T>().ToUniTask(cancellationToken: ct);
    }
}
```

## Addressables Profiler

Use Window > Asset Management > Addressables > Event Viewer to:
- Track all active handles and their reference counts
- Identify unreleased handles (memory leaks)
- Monitor asset loading and unloading in real time
- Check which groups are loaded

## Build Scripts

| Build Script | Use Case |
|-------------|----------|
| Use Asset Database (fastest) | Editor development, no build needed |
| Simulate Groups (Advanced) | Tests group structure without building |
| Use Existing Build | Production runtime, uses pre-built bundles |
| New Build | Creates new AssetBundles |

Build Addressables before building the player: Addressables Groups window > Build > New Build > Default Build Script.

### Build via Script

```csharp
#if UNITY_EDITOR
using UnityEditor.AddressableAssets.Settings;

public static class AddressableBuildHelper
{
    public static void BuildAddressables()
    {
        AddressableAssetSettings.BuildPlayerContent();
    }
}
#endif
```
