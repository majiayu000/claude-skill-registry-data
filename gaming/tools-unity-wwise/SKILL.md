---
name: tools-unity-wwise
description: Wwise audio middleware integration for Unity including events, banks, RTPC, spatial audio, and callback handling.
---

# Wwise Unity Integration

## Overview

Wwise is professional audio middleware providing advanced sound design capabilities. This skill covers Unity integration patterns for events, sound banks, real-time parameters, and spatial audio.

## When to Use

- Playing sound effects and music
- Dynamic audio parameter control
- 3D positional audio
- Audio state management
- Bank loading/unloading

## Core Concepts

### Sound Bank Loading

```csharp
public class AudioBankManager : MonoBehaviour
{
    [SerializeField] private AK.Wwise.Bank _initBank;
    [SerializeField] private AK.Wwise.Bank[] _coreBanks;
    
    private readonly HashSet<uint> _loadedBanks = new();
    
    public async UniTask InitializeAudio()
    {
        // Load Init bank first (required)
        await LoadBankAsync(_initBank);
        
        // Load core banks
        foreach (var bank in _coreBanks)
        {
            await LoadBankAsync(bank);
        }
    }
    
    public async UniTask LoadBankAsync(AK.Wwise.Bank bank)
    {
        if (bank == null || _loadedBanks.Contains(bank.Id))
            return;
        
        var tcs = new UniTaskCompletionSource();
        
        bank.Load(decodeBank: false, saveDecodedBank: false);
        
        // Wait for bank to be ready
        AKRESULT result = AkSoundEngine.LoadBank(
            bank.Name,
            out uint bankId
        );
        
        if (result == AKRESULT.AK_Success)
        {
            _loadedBanks.Add(bankId);
            Debug.Log($"Loaded bank: {bank.Name}");
        }
        else
        {
            Debug.LogError($"Failed to load bank {bank.Name}: {result}");
        }
    }
    
    public void UnloadBank(AK.Wwise.Bank bank)
    {
        if (bank == null) return;
        
        bank.Unload();
        _loadedBanks.Remove(bank.Id);
    }
    
    private void OnDestroy()
    {
        // Unload all banks on shutdown
        foreach (var bank in _coreBanks)
        {
            UnloadBank(bank);
        }
    }
}
```

### Async Bank Loading with Callback

```csharp
public class AsyncBankLoader
{
    public static async UniTask<bool> LoadBankAsync(string bankName)
    {
        var tcs = new UniTaskCompletionSource<bool>();
        
        AkSoundEngine.LoadBank(
            bankName,
            (uint)AkCallbackType.AK_BankLoaded,
            (in_cookie, in_type, in_info) =>
            {
                var loadInfo = (AkBankCallbackInfo)in_info;
                tcs.TrySetResult(loadInfo.loadResult == AKRESULT.AK_Success);
            },
            null,
            out uint bankId
        );
        
        return await tcs.Task;
    }
}
```

## Event Playback

### Basic Event Posting

```csharp
public class AudioEventPlayer : MonoBehaviour
{
    [SerializeField] private AK.Wwise.Event _footstepEvent;
    [SerializeField] private AK.Wwise.Event _attackEvent;
    
    private uint _playingId;
    
    public void PlayFootstep()
    {
        _footstepEvent.Post(gameObject);
    }
    
    public void PlayAttack()
    {
        // Store playing ID for potential stop
        _playingId = _attackEvent.Post(gameObject);
    }
    
    public void StopAttack()
    {
        if (_playingId != 0)
        {
            AkSoundEngine.StopPlayingID(_playingId);
            _playingId = 0;
        }
    }
    
    public void StopAll()
    {
        AkSoundEngine.StopAll(gameObject);
    }
}
```

### Event with Callback

```csharp
public class AudioEventWithCallback : MonoBehaviour
{
    [SerializeField] private AK.Wwise.Event _voiceEvent;
    
    public event Action OnVoiceComplete;
    
    public void PlayVoice()
    {
        _voiceEvent.Post(
            gameObject,
            (uint)(AkCallbackType.AK_EndOfEvent | AkCallbackType.AK_Marker),
            OnAudioCallback
        );
    }
    
    private void OnAudioCallback(
        object in_cookie,
        AkCallbackType in_type,
        AkCallbackInfo in_info)
    {
        switch (in_type)
        {
            case AkCallbackType.AK_EndOfEvent:
                OnVoiceComplete?.Invoke();
                break;
                
            case AkCallbackType.AK_Marker:
                var markerInfo = (AkMarkerCallbackInfo)in_info;
                HandleMarker(markerInfo.strLabel);
                break;
        }
    }
    
    private void HandleMarker(string label)
    {
        Debug.Log($"Audio marker: {label}");
        // Sync animation, VFX, etc.
    }
}
```

### Async Event Playback

```csharp
public static class WwiseAsyncExtensions
{
    public static async UniTask PlayAndWaitAsync(
        this AK.Wwise.Event wwiseEvent,
        GameObject gameObject,
        CancellationToken ct = default)
    {
        var tcs = new UniTaskCompletionSource();
        
        uint playingId = wwiseEvent.Post(
            gameObject,
            (uint)AkCallbackType.AK_EndOfEvent,
            (cookie, type, info) => tcs.TrySetResult()
        );
        
        if (playingId == 0)
        {
            Debug.LogWarning($"Failed to post event: {wwiseEvent.Name}");
            return;
        }
        
        // Handle cancellation
        using (ct.Register(() =>
        {
            AkSoundEngine.StopPlayingID(playingId);
            tcs.TrySetCanceled();
        }))
        {
            await tcs.Task;
        }
    }
}

// Usage
await _chargeSound.PlayAndWaitAsync(gameObject, _cts.Token);
```

## RTPC (Real-Time Parameter Control)

### Setting RTPC Values

```csharp
public class AudioParameterController : MonoBehaviour
{
    [SerializeField] private AK.Wwise.RTPC _healthRTPC;
    [SerializeField] private AK.Wwise.RTPC _speedRTPC;
    [SerializeField] private AK.Wwise.RTPC _tensionRTPC;
    
    public void SetHealth(float normalizedHealth)
    {
        // Value 0-100 for health percentage
        _healthRTPC.SetGlobalValue(normalizedHealth * 100f);
    }
    
    public void SetSpeed(float speed)
    {
        // Set on specific game object for 3D sounds
        _speedRTPC.SetValue(gameObject, speed);
    }
    
    public void SetTension(float tension, float interpolationMs = 100f)
    {
        // Smooth interpolation
        AkSoundEngine.SetRTPCValue(
            _tensionRTPC.Id,
            tension,
            gameObject,
            (int)interpolationMs
        );
    }
}
```

### RTPC with Animation

```csharp
public class AudioAnimationSync : MonoBehaviour
{
    [SerializeField] private AK.Wwise.RTPC _animationProgressRTPC;
    
    private Animator _animator;
    
    private void Update()
    {
        var stateInfo = _animator.GetCurrentAnimatorStateInfo(0);
        float progress = stateInfo.normalizedTime % 1f;
        
        _animationProgressRTPC.SetValue(gameObject, progress * 100f);
    }
}
```

## State and Switch Management

### Setting States

```csharp
public class AudioStateManager : MonoBehaviour
{
    [SerializeField] private AK.Wwise.State _combatState;
    [SerializeField] private AK.Wwise.State _explorationState;
    [SerializeField] private AK.Wwise.State _menuState;
    
    public void EnterCombat()
    {
        _combatState.SetValue();
    }
    
    public void ExitCombat()
    {
        _explorationState.SetValue();
    }
    
    public void EnterMenu()
    {
        _menuState.SetValue();
    }
}
```

### Setting Switches

```csharp
public class AudioSwitchController : MonoBehaviour
{
    [SerializeField] private AK.Wwise.Switch _surfaceSwitch;
    
    // Different surface types
    [SerializeField] private AK.Wwise.Switch _concreteSurface;
    [SerializeField] private AK.Wwise.Switch _grassSurface;
    [SerializeField] private AK.Wwise.Switch _waterSurface;
    
    public void SetSurface(SurfaceType surface)
    {
        switch (surface)
        {
            case SurfaceType.Concrete:
                _concreteSurface.SetValue(gameObject);
                break;
            case SurfaceType.Grass:
                _grassSurface.SetValue(gameObject);
                break;
            case SurfaceType.Water:
                _waterSurface.SetValue(gameObject);
                break;
        }
    }
}
```

## Spatial Audio

### AkGameObj Setup

```csharp
public class SpatialAudioSetup : MonoBehaviour
{
    private AkGameObj _akGameObj;
    
    private void Awake()
    {
        // Ensure AkGameObj component exists
        _akGameObj = GetComponent<AkGameObj>();
        if (_akGameObj == null)
        {
            _akGameObj = gameObject.AddComponent<AkGameObj>();
        }
        
        // Register with Wwise
        AkSoundEngine.RegisterGameObj(gameObject, gameObject.name);
    }
    
    private void OnDestroy()
    {
        AkSoundEngine.UnregisterGameObj(gameObject);
    }
}
```

### Listener Configuration

```csharp
public class AudioListenerSetup : MonoBehaviour
{
    [SerializeField] private bool _isDefaultListener = true;
    
    private void Awake()
    {
        // Register as game object
        AkSoundEngine.RegisterGameObj(gameObject, "AudioListener");
        
        if (_isDefaultListener)
        {
            // Set as default listener
            ulong[] listeners = { AkSoundEngine.GetAkGameObjectID(gameObject) };
            AkSoundEngine.SetDefaultListeners(listeners, 1);
        }
    }
    
    private void OnDestroy()
    {
        AkSoundEngine.UnregisterGameObj(gameObject);
    }
}
```

### Room and Portal System

```csharp
public class AudioRoom : MonoBehaviour
{
    [SerializeField] private AkRoom _akRoom;
    [SerializeField] private float _reverbLevel = 1f;
    [SerializeField] private float _transmissionLoss = 0.5f;
    
    private void Awake()
    {
        _akRoom = GetComponent<AkRoom>();
        if (_akRoom == null)
        {
            _akRoom = gameObject.AddComponent<AkRoom>();
        }
        
        // Configure room
        _akRoom.reverbLevel = _reverbLevel;
        _akRoom.transmissionLoss = _transmissionLoss;
    }
}
```

## Volume Control

### Volume Settings

```csharp
public class VolumeController : MonoBehaviour
{
    [SerializeField] private AK.Wwise.RTPC _masterVolumeRTPC;
    [SerializeField] private AK.Wwise.RTPC _musicVolumeRTPC;
    [SerializeField] private AK.Wwise.RTPC _sfxVolumeRTPC;
    [SerializeField] private AK.Wwise.RTPC _voiceVolumeRTPC;
    
    public void SetMasterVolume(float volume)
    {
        _masterVolumeRTPC.SetGlobalValue(VolumeToDb(volume));
    }
    
    public void SetMusicVolume(float volume)
    {
        _musicVolumeRTPC.SetGlobalValue(VolumeToDb(volume));
    }
    
    public void SetSFXVolume(float volume)
    {
        _sfxVolumeRTPC.SetGlobalValue(VolumeToDb(volume));
    }
    
    public void SetVoiceVolume(float volume)
    {
        _voiceVolumeRTPC.SetGlobalValue(VolumeToDb(volume));
    }
    
    // Convert linear 0-1 to dB scale
    private float VolumeToDb(float linear)
    {
        if (linear <= 0.0001f) return -96f; // Silence
        return 20f * Mathf.Log10(linear);
    }
    
    public void Mute()
    {
        AkSoundEngine.SetRTPCValue("MasterVolume", -96f);
    }
    
    public void Unmute()
    {
        // Restore to saved value
        SetMasterVolume(PlayerPrefs.GetFloat("MasterVolume", 1f));
    }
}
```

## Animation Event Integration

### Wwise Animation Event Callback

```csharp
public class WwiseAnimationEventHandler : MonoBehaviour
{
    [SerializeField] private AK.Wwise.Event _footstepEvent;
    [SerializeField] private AK.Wwise.Event _whooshEvent;
    [SerializeField] private AK.Wwise.Event _impactEvent;
    
    // Called from animation event
    public void PlayFootstep()
    {
        _footstepEvent.Post(gameObject);
    }
    
    // Called from animation event with string parameter
    public void PlaySoundByName(string eventName)
    {
        AkSoundEngine.PostEvent(eventName, gameObject);
    }
    
    // Called from animation event
    public void PlayWhoosh()
    {
        _whooshEvent.Post(gameObject);
    }
    
    // Called from animation event
    public void PlayImpact()
    {
        _impactEvent.Post(gameObject);
    }
}
```

## Performance Patterns

### Pooled Audio Sources

```csharp
public class PooledAudioEmitter : MonoBehaviour, IPoolable
{
    private uint _currentPlayingId;
    
    public void OnSpawn()
    {
        AkSoundEngine.RegisterGameObj(gameObject);
    }
    
    public void OnDespawn()
    {
        if (_currentPlayingId != 0)
        {
            AkSoundEngine.StopPlayingID(_currentPlayingId);
            _currentPlayingId = 0;
        }
        AkSoundEngine.UnregisterGameObj(gameObject);
    }
    
    public void PlayEvent(AK.Wwise.Event wwiseEvent)
    {
        _currentPlayingId = wwiseEvent.Post(gameObject);
    }
}
```

### Batch Event Posting

```csharp
public class AudioBatcher
{
    private readonly List<(AK.Wwise.Event evt, GameObject go)> _pendingEvents = new();
    private const int MaxEventsPerFrame = 10;
    
    public void QueueEvent(AK.Wwise.Event evt, GameObject go)
    {
        _pendingEvents.Add((evt, go));
    }
    
    public void ProcessBatch()
    {
        int processed = 0;
        
        while (_pendingEvents.Count > 0 && processed < MaxEventsPerFrame)
        {
            var (evt, go) = _pendingEvents[0];
            _pendingEvents.RemoveAt(0);
            
            if (go != null)
            {
                evt.Post(go);
            }
            
            processed++;
        }
    }
}
```

## Error Handling

### Safe Event Posting

```csharp
public static class WwiseSafeExtensions
{
    public static uint PostSafe(this AK.Wwise.Event evt, GameObject go)
    {
        if (evt == null || !evt.IsValid())
        {
            Debug.LogWarning("Attempted to post invalid Wwise event");
            return 0;
        }
        
        if (go == null)
        {
            Debug.LogWarning($"Attempted to post event {evt.Name} on null GameObject");
            return 0;
        }
        
        return evt.Post(go);
    }
    
    public static void SetValueSafe(this AK.Wwise.RTPC rtpc, GameObject go, float value)
    {
        if (rtpc == null || !rtpc.IsValid())
        {
            Debug.LogWarning("Attempted to set invalid RTPC");
            return;
        }
        
        rtpc.SetValue(go, value);
    }
}
```

## Best Practices

1. **Load Init bank first** - Required for Wwise to function
2. **Register game objects** - Before posting events
3. **Unregister on destroy** - Prevent memory leaks
4. **Use callbacks for sync** - Animation markers, end events
5. **Pool audio emitters** - Reduce registration overhead
6. **Batch event posts** - Limit per-frame calls
7. **Use RTPC interpolation** - Smooth parameter changes
8. **Manage bank memory** - Load/unload per scene
9. **Set switches before events** - Order matters
10. **Profile audio CPU** - Wwise has profiler tools

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No sound | Check bank loaded, game object registered |
| Event not found | Verify bank contains event, bank is loaded |
| RTPC not working | Check RTPC name matches Wwise project |
| 3D audio wrong | Verify listener setup, position updates |
| Memory issues | Unload unused banks |
| Clicks/pops | Use fade times, check sample rates |
