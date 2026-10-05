---
name: object-pooling
description: "Object pooling patterns — Unity ObjectPool<T>, custom ComponentPool, warm-up strategies, return-to-pool lifecycle. Eliminates runtime Instantiate/Destroy overhead."
alwaysApply: true
---

# Object Pooling

Every `Instantiate()` allocates memory. Every `Destroy()` triggers GC. Pool objects you create and destroy frequently: projectiles, particles, enemies, pickups, audio sources.

## Unity Built-In ObjectPool<T> (2021+)

```csharp
using UnityEngine.Pool;

public sealed class ProjectilePool : MonoBehaviour
{
    [SerializeField] private Projectile _prefab;
    [SerializeField] private int _defaultCapacity = 20;
    [SerializeField] private int _maxSize = 100;

    private ObjectPool<Projectile> _pool;

    private void Awake()
    {
        _pool = new ObjectPool<Projectile>(
            createFunc: CreateProjectile,
            actionOnGet: OnGetProjectile,
            actionOnRelease: OnReleaseProjectile,
            actionOnDestroy: OnDestroyProjectile,
            collectionCheck: false,
            defaultCapacity: _defaultCapacity,
            maxSize: _maxSize
        );
    }

    public Projectile Get() => _pool.Get();

    public void Release(Projectile projectile) => _pool.Release(projectile);

    private Projectile CreateProjectile()
    {
        Projectile projectile = Instantiate(_prefab);
        projectile.SetPool(this);
        return projectile;
    }

    private void OnGetProjectile(Projectile projectile)
    {
        projectile.gameObject.SetActive(true);
    }

    private void OnReleaseProjectile(Projectile projectile)
    {
        projectile.gameObject.SetActive(false);
    }

    private void OnDestroyProjectile(Projectile projectile)
    {
        Destroy(projectile.gameObject);
    }
}

// Projectile returns itself to pool
public sealed class Projectile : MonoBehaviour
{
    private ProjectilePool _pool;

    public void SetPool(ProjectilePool pool) => _pool = pool;

    public void ReturnToPool()
    {
        _pool.Release(this);
    }
}
```

## Warm-Up (Pre-Spawn)

Pre-instantiate objects during loading to avoid runtime hitches:

```csharp
private void Start()
{
    // Pre-warm the pool
    List<Projectile> temp = new List<Projectile>();
    for (int i = 0; i < _defaultCapacity; i++)
    {
        temp.Add(_pool.Get());
    }
    for (int i = 0; i < temp.Count; i++)
    {
        _pool.Release(temp[i]);
    }
    temp.Clear();
}
```

## Return-to-Pool Lifecycle

The key contract: **objects must reset their state when returned to pool.**

```csharp
private void OnReleaseProjectile(Projectile projectile)
{
    // Reset state
    projectile.transform.position = Vector3.zero;
    projectile.transform.rotation = Quaternion.identity;
    projectile.ResetState(); // Clear velocity, damage flags, timers

    // Deactivate
    projectile.gameObject.SetActive(false);
}
```

## When to Pool

**Pool these:**
- Projectiles (bullets, arrows, spells)
- Particle effects
- Audio sources (one-shot sounds)
- Enemies in wave-based games
- Pickup items
- Damage numbers / floating text
- Trail renderers

**Don't pool these:**
- One-time objects (boss, unique NPCs)
- Tiny objects created once (data containers)
- Objects that live the entire scene

## Pool Sizing

- **Start small** — 10-20 instances for most pools
- **Monitor** — if you see `Instantiate` in Profiler during gameplay, increase pool size
- **Max cap** — set `maxSize` to prevent unbounded growth (e.g., 100-200)
- **Per-level tuning** — different levels may need different pool sizes

## Generic Pool Manager

```csharp
public sealed class PoolManager : MonoBehaviour
{
    private readonly Dictionary<GameObject, ObjectPool<GameObject>> _pools = new();

    public GameObject Get(GameObject prefab, Vector3 position, Quaternion rotation)
    {
        if (!_pools.ContainsKey(prefab))
        {
            _pools[prefab] = new ObjectPool<GameObject>(
                () => Instantiate(prefab),
                obj => obj.SetActive(true),
                obj => obj.SetActive(false),
                obj => Destroy(obj),
                false, 10, 100
            );
        }

        GameObject obj = _pools[prefab].Get();
        obj.transform.SetPositionAndRotation(position, rotation);
        return obj;
    }

    public void Release(GameObject prefab, GameObject instance)
    {
        _pools[prefab].Release(instance);
    }
}
```

## Cached WaitForSeconds

Don't forget to pool `WaitForSeconds`:

```csharp
// BAD — allocates every time
yield return new WaitForSeconds(0.5f);

// GOOD — cache and reuse
private readonly WaitForSeconds _halfSecond = new WaitForSeconds(0.5f);
yield return _halfSecond;
```
