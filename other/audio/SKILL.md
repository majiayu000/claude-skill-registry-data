---
name: audio
description: "Unity audio system — AudioMixer groups, snapshots, spatial audio, audio source pooling, compression per platform."
globs: ["**/*.mixer", "**/*Audio*.cs", "**/*Sound*.cs", "**/*Music*.cs"]
---

# Audio System

## AudioMixer Setup

```
Master (exposed: "MasterVolume")
├── Music (exposed: "MusicVolume")
├── SFX (exposed: "SFXVolume")
│   ├── Weapons
│   ├── Environment
│   └── UI
└── Voice (exposed: "VoiceVolume")
```

### Volume Control via Exposed Parameters
```csharp
[SerializeField] private AudioMixer _mixer;

public void SetMasterVolume(float normalizedValue)
{
    // Convert 0-1 slider to decibels (-80 to 0)
    float dB = normalizedValue > 0.001f
        ? Mathf.Log10(normalizedValue) * 20f
        : -80f;
    _mixer.SetFloat("MasterVolume", dB);
}
```

### Snapshots
```csharp
// Transition between snapshots for ambient changes
_underwaterSnapshot.TransitionTo(0.5f);  // Muffle audio underwater
_defaultSnapshot.TransitionTo(1.0f);      // Return to normal
```

## Playing Sounds

```csharp
// One-shot SFX (fire and forget, doesn't interrupt)
_audioSource.PlayOneShot(_explosionClip, 0.8f);

// Music (interruptible, one at a time per source)
_musicSource.clip = _battleMusic;
_musicSource.Play();
```

## Audio Source Pooling

```csharp
public sealed class SFXPool : MonoBehaviour
{
    [SerializeField] private int _poolSize = 16;
    [SerializeField] private AudioMixerGroup _sfxGroup;

    private AudioSource[] _sources;
    private int _nextIndex;

    private void Awake()
    {
        _sources = new AudioSource[_poolSize];
        for (int i = 0; i < _poolSize; i++)
        {
            GameObject obj = new GameObject($"SFX_{i}");
            obj.transform.SetParent(transform);
            AudioSource source = obj.AddComponent<AudioSource>();
            source.outputAudioMixerGroup = _sfxGroup;
            source.playOnAwake = false;
            _sources[i] = source;
        }
    }

    public void PlayAt(AudioClip clip, Vector3 position, float volume = 1f)
    {
        AudioSource source = _sources[_nextIndex];
        _nextIndex = (_nextIndex + 1) % _poolSize;

        source.transform.position = position;
        source.spatialBlend = 1f; // 3D
        source.PlayOneShot(clip, volume);
    }
}
```

## Spatial Audio

- `spatialBlend`: 0 = 2D (UI, music), 1 = 3D (world SFX)
- `minDistance`: full volume radius
- `maxDistance`: silence radius
- `rolloffMode`: Logarithmic (realistic) or Custom (AnimationCurve)
- `spread`: 0 = point source, 360 = omnidirectional

## Compression Per Platform

| Type | Format | Load Type | Use |
|------|--------|-----------|-----|
| Music | Vorbis (quality 40-60%) | Streaming | Background music |
| SFX (short) | ADPCM | Decompress On Load | Gunshots, jumps |
| SFX (long) | Vorbis (quality 70%) | Compressed In Memory | Ambient loops |
| UI | PCM (uncompressed) | Decompress On Load | Button clicks |

## Music System Pattern

```csharp
public sealed class MusicManager : MonoBehaviour
{
    [SerializeField] private AudioSource _sourceA;
    [SerializeField] private AudioSource _sourceB;
    [SerializeField] private float _crossfadeDuration = 2f;

    private AudioSource _activeSource;

    public void CrossfadeTo(AudioClip newClip)
    {
        AudioSource incoming = _activeSource == _sourceA ? _sourceB : _sourceA;
        incoming.clip = newClip;
        incoming.volume = 0f;
        incoming.Play();

        StartCoroutine(Crossfade(_activeSource, incoming));
        _activeSource = incoming;
    }

    private IEnumerator Crossfade(AudioSource outgoing, AudioSource incoming)
    {
        float elapsed = 0f;
        while (elapsed < _crossfadeDuration)
        {
            elapsed += Time.unscaledDeltaTime;
            float t = elapsed / _crossfadeDuration;
            outgoing.volume = 1f - t;
            incoming.volume = t;
            yield return null;
        }
        outgoing.Stop();
    }
}
```

## Key Rules
- One `AudioListener` per scene (usually on the camera)
- Pool AudioSources for one-shot SFX — don't create/destroy
- Use `Time.unscaledDeltaTime` for audio during pause
