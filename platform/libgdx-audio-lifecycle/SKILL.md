---
name: libgdx-audio-lifecycle
description: Use when writing libGDX Java/Kotlin code involving audio (Sound, Music, Gdx.audio). Use when debugging audio not playing, audio format issues, or platform-specific audio behavior in libGDX.
---

# libGDX Audio

Quick reference for libGDX audio APIs. Covers Sound, Music, platform gotchas, and common audio patterns.

## Audio: Sound vs Music

| | Sound | Music |
|---|---|---|
| **Loading** | Fully into memory | Streamed from disk |
| **Use for** | Short effects (<1MB on Android) | Background tracks, long audio |
| **Concurrent** | Multiple instances via `play()` | One stream per Music object |
| **Auto pause/resume** | No | Yes (libGDX handles automatically) |

**Formats:** WAV, MP3, OGG all supported. **OGG not supported on iOS** — use WAV or MP3.

## Sound API

```java
Sound snd = Gdx.audio.newSound(Gdx.files.internal("click.wav"));

// play() returns instance ID (long).
long id = snd.play();                          // default volume
long id = snd.play(volume);                    // volume: [0, 1]
long id = snd.play(volume, pitch, pan);        // pitch: [0.5, 2.0], pan: [-1, 1]

long id = snd.loop();                          // same overloads as play()
long id = snd.loop(volume, pitch, pan);

// Per-instance control (pass the id from play/loop)
snd.setVolume(id, volume);
snd.setPitch(id, pitch);
snd.setPan(id, pan, volume);                   // NOTE: pan+volume together
snd.setLooping(id, true);
snd.stop(id);
snd.pause(id);
snd.resume(id);

// All-instance control (no id)
snd.stop();
snd.pause();
snd.resume();

snd.dispose();                                 // MUST call when done
```

In non-trivial projects, prefer loading audio via `AssetManager` rather than raw `Gdx.audio.newSound()`. AssetManager handles disposal via `unload()` and supports async loading.

**Gotchas:**
- Pan only works on **mono** sounds (stereo sounds ignore pan).
- Android: uncompressed PCM must be <1MB for Sound. Use Music for larger files.
- `play()` on an already-playing Sound plays it **concurrently** (new instance).
- Behavior when exceeding platform limits is backend-dependent — sounds may silently fail to play. Do not rely on the return value to detect this.
- `play()` called in `create()` can silently fail on Android before the audio system is fully initialized. Defer initial sound playback to the first `render()` frame or use a boolean flag.

## Music API

```java
Music bgm = Gdx.audio.newMusic(Gdx.files.internal("theme.ogg")); // OGG not supported on iOS — use MP3 for cross-platform

bgm.play();
bgm.pause();
bgm.stop();                                    // resets to beginning

bgm.setVolume(volume);                         // [0, 1]
float v = bgm.getVolume();
bgm.setPan(pan, volume);                       // [-1, 1], [0, 1]

bgm.setLooping(true);
boolean playing = bgm.isPlaying();
boolean looping = bgm.isLooping();

bgm.setPosition(seconds);                      // seek (float, in seconds)
float pos = bgm.getPosition();

bgm.setOnCompletionListener(music -> {
    // Called when music finishes playing
});

bgm.dispose();                                 // MUST call when done
```

In non-trivial projects, prefer loading audio via `AssetManager` rather than raw `Gdx.audio.newMusic()`. AssetManager handles disposal via `unload()` and supports async loading.

**Gotchas:**
- **OnCompletionListener does NOT fire when looping is true.** If you need looping + completion callback, set looping=false and restart in the listener.
- libGDX **automatically pauses/resumes Music** on Android pause/resume. You do NOT need to manually pause music in `ApplicationListener.pause()`. Doing so is redundant.
- Only one OnCompletionListener per Music instance (last set wins).
- `setPosition()` is unreliable on some Android devices for MP3 — seeking uses bitrate estimation and can be off by several seconds. OGG seeking is more accurate, but OGG is unsupported on iOS. For cross-platform seeking accuracy, consider WAV (large files) or accept MP3 imprecision.

## Common Patterns

### Shared Music Across Screens

Store Music in the Game class, not in individual Screens. Dispose only in `Game.dispose()`.

```java
public class MyGame extends Game {
    public Music bgm;

    @Override
    public void create() {
        bgm = Gdx.audio.newMusic(Gdx.files.internal("theme.mp3")); // use MP3 for iOS compatibility
        bgm.setLooping(true);
        bgm.play();
        setScreen(new MenuScreen(this));
    }

    @Override
    public void dispose() {
        bgm.dispose();
        getScreen().dispose();
    }
}
```

## Platform Differences

| Behavior | Desktop (LWJGL3) | Android | iOS (RoboVM) |
|---|---|---|---|
| OGG support | Yes | Yes | **No** |
| Music auto-pause | On minimize only | Yes | Yes |
| Sound size limit | None | **<1MB PCM** | None |
| MP3 seeking accuracy | Good | **Unreliable** | Good |

## Common Mistakes

1. **Manually pausing Music in pause()** — libGDX does this automatically. Redundant code confuses readers.
2. **Using Sound for long audio** — Sound loads entirely into memory. Use Music for anything over a few seconds.
3. **Expecting OnCompletionListener with looping** — It won't fire. Use looping=false + manual restart.
4. **Using OGG on iOS** — Will fail silently or crash. Use WAV/MP3.
5. **Playing Sound in create() on Android** — Audio system may not be ready. Defer to first `render()` frame.
6. **Relying on Music.setPosition() accuracy with MP3 on Android** — Seeking can be off by seconds. Use OGG for accuracy (but not on iOS).
7. **Checking Sound.play() return value for failure detection** — Behavior is backend-dependent. Don't rely on it.
