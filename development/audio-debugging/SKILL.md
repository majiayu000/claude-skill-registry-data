---
name: audio-debugging
description: Automatically helps debug Web Audio API issues, audio playback problems, pitch preservation, and caching issues in the VSSK-shadecn music practice app
---

# Audio Debugging Skill

This skill activates when you encounter audio-related issues in VSSK-shadecn.

## When to Use

This skill automatically activates for:
- Audio playback not working
- Pitch preservation issues
- Speed control problems
- Audio caching failures
- Waveform rendering issues
- Audio buffer errors
- Service worker audio problems

## Debugging Process

### 1. Identify the Issue
- What's the expected behavior?
- What's actually happening?
- When does it occur? (specific conditions)
- Which browsers/devices affected?

### 2. Check Common Problems

**Audio Won't Play**
- [ ] Audio file loaded correctly?
- [ ] Audio context resumed (user gesture required)?
- [ ] Network errors or CORS issues?
- [ ] Browser autoplay policy blocking?

**Pitch Preservation Issues**
- [ ] Using correct Web Audio API methods?
- [ ] playbackRate vs detune?
- [ ] Browser support for pitch shifting?
- [ ] Alternative library needed?

**Caching Problems**
- [ ] Service worker registered?
- [ ] Cache strategy correct for audio?
- [ ] Storage quota exceeded?
- [ ] Cache versioning working?

### 3. Diagnostic Commands

```typescript
// Check audio context state
console.log('AudioContext state:', audioContext.state)

// Test audio loading
fetch('/audio/song.mp3')
  .then(res => console.log('Audio fetch:', res.status))
  .catch(err => console.error('Audio fetch error:', err))

// Check cache
caches.open('audio-v1').then(cache =>
  cache.keys().then(keys => console.log('Cached audio:', keys.length))
)

// Monitor playback
audio.addEventListener('error', (e) => {
  console.error('Audio error:', e)
  console.log('Error code:', audio.error?.code)
  console.log('Error message:', audio.error?.message)
})
```

### 4. Browser-Specific Issues

**iOS Safari**
- Requires user gesture to start audio
- Limited concurrent audio contexts
- No background audio without special handling
- Service worker limitations

**Chrome Android**
- Autoplay policy restrictions
- Battery optimization may pause audio
- Storage quota more restrictive

### 5. Common Fixes

**Audio Context Suspended**
```typescript
// Resume audio context on user interaction
const resumeAudioContext = async () => {
  if (audioContext.state === 'suspended') {
    await audioContext.resume()
  }
}

// Call on user gesture (click, tap)
button.addEventListener('click', resumeAudioContext)
```

**Pitch Preservation**
```typescript
// Use Web Audio API for pitch preservation
const source = audioContext.createBufferSource()
source.playbackRate.value = 0.5 // Half speed
source.detune.value = 0 // Keep original pitch
```

**Cache Issues**
```typescript
// Check storage quota
if ('storage' in navigator && 'estimate' in navigator.storage) {
  const estimate = await navigator.storage.estimate()
  console.log(`Using ${estimate.usage} of ${estimate.quota} bytes`)
}
```

## Output Format

Provide:
1. **Problem Diagnosis**: What's wrong and why
2. **Root Cause**: Technical explanation
3. **Solution**: Step-by-step fix with code
4. **Prevention**: How to avoid this in future
5. **Testing**: How to verify it's fixed
