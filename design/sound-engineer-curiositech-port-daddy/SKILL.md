---
license: Apache-2.0
name: sound-engineer
description: Expert in spatial audio, procedural sound design, game audio middleware, and app UX sound design. Specializes in HRTF/Ambisonics, Wwise/FMOD integration, UI sound design, and adaptive music systems. Activate on 'spatial audio', 'HRTF', 'binaural', 'Wwise', 'FMOD', 'procedural sound', 'footstep system', 'adaptive music', 'UI sounds', 'notification audio', 'sonic branding'. NOT for music composition/production (use DAW), audio post-production for film (linear media), voice cloning/TTS (use voice-audio-engineer), podcast editing (use standard audio editors), or hardware design.
allowed-tools: Read,Write,Edit,Bash(python:*,node:*,npm:*,ffmpeg:*),mcp__firecrawl__firecrawl_search,WebFetch,mcp__ElevenLabs__text_to_sound_effects
category: Video & Audio
tags:
  - sound-engineering
  - mixing
  - mastering
  - audio
  - production
pairs-with:
  - skill: voice-audio-engineer
    reason: Voice + spatial audio integration
  - skill: 2000s-visualization-expert
    reason: Audio-reactive visuals
---

# Sound Engineer: Spatial Audio, Procedural Sound & App UX Audio

Expert audio engineer for interactive media: games, VR/AR, and mobile apps. Specializes in spatial audio, procedural sound generation, middleware integration, and UX sound design.

## DECISION POINTS

### 1. Middleware Selection: Wwise vs FMOD
```
IF (budget < $10k AND indie game):
    └─ Use free FMOD (up to $500k revenue)
    
IF (AAA production OR need extensive audio design tools):
    └─ Use Wwise
    └─ IF (team has dedicated audio programmers):
        └─ Full Wwise SDK integration
    └─ ELSE (programmers need simple API):
        └─ Use Wwise Unity/Unreal plugins
        
IF (mobile-only OR web deployment):
    └─ Consider lightweight alternatives
    └─ Check platform restrictions (iOS/WebGL)
```

### 2. Spatial Audio Approach Selection
```
Decision Matrix Based on Context:

Sources > 20 AND VR with head tracking:
    └─ Use Ambisonics (encode once, rotate cheaply)
    
Sources < 10 AND close/important sounds:
    └─ Use full HRTF convolution per source
    
Mobile OR CPU budget tight:
    └─ IF (stereo headphones expected):
        └─ Simple binaural panning
    └─ ELSE:
        └─ Standard stereo panning + distance rolloff
        
Background/ambient sounds:
    └─ Always use simple panning (save CPU for foreground)
```

### 3. Adaptive Music Strategy
```
IF (music needs to match gameplay intensity):
    └─ Horizontal Re-orchestration:
        └─ Layer 1: Basic rhythm/bass
        └─ Layer 2: Add melody
        └─ Layer 3: Add harmony/counterpoint
        └─ Layer 4: Full orchestration
        
IF (different moods needed per area):
    └─ Vertical Stems:
        └─ Peaceful stem (woodwinds, strings)
        └─ Tense stem (brass, percussion)
        └─ Combat stem (full orchestra)
        └─ Crossfade based on game state
        
IF (seamless transitions critical):
    └─ Use musical bars as transition boundaries
    └─ Pre-calculate next transition point
    └─ Never cut mid-phrase
```

### 4. Footstep Implementation Choice
```
Memory budget > 5MB AND < 50 total surfaces:
    └─ Use sample library approach
    
Memory budget tight OR > 100 surface variations:
    └─ Procedural synthesis:
        └─ Impact component (filtered noise burst)
        └─ Surface texture (material-specific)
        └─ Debris scattering (micro-impacts)
        
Performance critical (mobile):
    └─ Pre-generate variations at load time
    └─ Cache 10-20 variants per surface type
```

## FAILURE MODES

### 1. HRTF Overload ("Everything Needs 3D")
**Symptom**: Frame drops when 20+ sounds play simultaneously
**Detection**: CPU profiler shows >50% time in HRTF convolution
**Root Cause**: Applying full HRTF to every sound source
**Fix**: Use HRTF only for 3-5 important sources; simple panning for background
**Prevention**: Set source importance hierarchy at design time

### 2. Sample Memory Bloat ("Footstep Explosion")
**Symptom**: 500MB+ audio assets for simple character movement
**Detection**: 50+ footstep samples per character/surface combination
**Root Cause**: Artist creating samples for every possible variation
**Fix**: Implement procedural footstep synthesis with 4-5 base components
**Prevention**: Establish memory budgets early; use procedural for high-variation content

### 3. Mobile Session Chaos ("The Silent Treatment")
**Symptom**: App audio stops working after phone call/notification
**Detection**: Audio stops, never resumes; works fine on first launch
**Root Cause**: No interruption handling for iOS/Android audio sessions
**Fix**: Implement proper session management with interruption observers
**Prevention**: Test with incoming calls, music apps, Siri activation

### 4. UI Sound Assault ("Click Fatigue")
**Symptom**: Users disable sound after 10 minutes of interaction
**Detection**: Every button click at same volume as gameplay audio
**Root Cause**: UI sounds mixed at gameplay levels (-6dB instead of -20dB)
**Fix**: Reduce UI sounds to -18 to -24dB; use subtle, brief tones
**Prevention**: Follow platform audio guidelines; A/B test with real users

### 5. Real-time Processing Overload ("DSP Death Spiral")
**Symptom**: Audio stutters, pops, or cuts out during intense scenes
**Detection**: Audio callback exceeds allocated time budget (>10ms)
**Root Cause**: Too many real-time effects, unoptimized convolution
**Fix**: Use FFT-based convolution; limit concurrent DSP effects
**Prevention**: Profile on lowest-spec target device; set hard limits

## WORKED EXAMPLES

### Example 1: VR Footstep System (Procedural Approach)
**Scenario**: VR game needs infinite footstep variation across 15 surface types, tight memory budget (50MB total audio)

**Expert Decision Process**:
1. **Reject sample approach**: 15 surfaces × 10 variations × 2 feet = 300 samples (150MB)
2. **Choose procedural**: Impact + texture layers, ~2KB of parameters per surface
3. **Surface detection**: Use physics material from VR floor collision
4. **Parameter mapping**: Player velocity → impact force (0.0-1.0 RTPC)

**Implementation**:
```cpp
void OnVRFootstep(Vector3 position, PhysicsMaterial surface, float velocity) {
    // Surface-specific parameters (expert knowledge)
    SurfaceParams params = GetSurfaceParams(surface);
    
    // Procedural synthesis
    float impact_force = Mathf.Clamp01(velocity / 3.0f); // 3m/s = max force
    
    // Wwise integration
    SetRTPCValue("Impact_Force", impact_force, player);
    SetRTPCValue("Surface_Hardness", params.hardness, player);
    SetSwitch("Surface_Type", params.type_name, player);
    
    PostEvent("Play_Footstep_Procedural", player);
}
```

**Novice vs Expert Trade-offs**:
- **Novice**: "Use realistic footstep recordings" → 150MB, repetition after 30 mins
- **Expert**: "Synthesis sounds 90% as good, infinite variation, 50KB total"

### Example 2: Mobile UI Sound Design (Session Handling)
**Scenario**: Meditation app needs subtle notification sounds that respect music apps and phone calls

**Expert Decision Process**:
1. **Audio session category**: `.ambient` with `.mixWithOthers` (don't interrupt Spotify)
2. **Volume levels**: -20dB for notifications, -24dB for UI feedback
3. **Interruption handling**: Pause during calls, resume after
4. **Haptic coordination**: Match audio transients to taptic feedback

**Implementation**:
```swift
class AppAudioManager {
    func setupAudioSession() {
        let session = AVAudioSession.sharedInstance()
        try? session.setCategory(.ambient, mode: .default, options: [.mixWithOthers])
        
        // Handle interruptions (phone calls, Siri)
        NotificationCenter.default.addObserver(
            self, selector: #selector(handleInterruption),
            name: AVAudioSession.interruptionNotification, object: nil
        )
    }
    
    @objc func handleInterruption(notification: Notification) {
        guard let info = notification.userInfo,
              let typeValue = info[AVAudioSessionInterruptionTypeKey] as? UInt,
              let type = AVAudioSession.InterruptionType(rawValue: typeValue) else { return }
        
        switch type {
        case .began:
            pauseAllAudio()  // Phone call started
        case .ended:
            if let optionsValue = info[AVAudioSessionInterruptionOptionKey] as? UInt {
                let options = AVAudioSession.InterruptionOptions(rawValue: optionsValue)
                if options.contains(.shouldResume) {
                    resumeAudio()  // Safe to resume
                }
            }
        }
    }
}
```

**What Novice Misses**: Assumes audio "just works"; ignores platform session requirements
**Expert Insight**: Mobile audio requires explicit session management; test with real interruptions

### Example 3: Adaptive Music System (RTPC Setup)
**Scenario**: Action RPG needs music that scales with combat intensity (0 = exploration, 1 = boss fight)

**Expert Decision Process**:
1. **Choose horizontal orchestration** over vertical stems (smoother intensity scaling)
2. **RTPC mapping**: Combat_Intensity (0.0-1.0) drives 4 instrument layers
3. **Transition timing**: Use musical bars, never cut mid-phrase
4. **Fallback logic**: If RTPC fails, default to medium intensity

**Wwise Implementation**:
```
Combat_Music_Container/
├── Layer_1_Rhythm (RTPC: Combat_Intensity > 0.0)
├── Layer_2_Melody (RTPC: Combat_Intensity > 0.3)  
├── Layer_3_Harmony (RTPC: Combat_Intensity > 0.6)
└── Layer_4_Full_Orch (RTPC: Combat_Intensity > 0.8)
```

**Code Integration**:
```cpp
void UpdateCombatMusic() {
    float intensity = CalculateCombatIntensity(); // 0.0 = safe, 1.0 = boss fight
    
    // Smooth the transitions (avoid jarring jumps)
    float smoothed = Mathf.Lerp(current_intensity, intensity, Time.deltaTime * 2.0f);
    current_intensity = smoothed;
    
    // Only update on musical boundaries
    if (IsOnMusicalBeat() && Mathf.Abs(smoothed - last_sent_intensity) > 0.1f) {
        SetRTPCValue("Combat_Intensity", smoothed, music_player);
        last_sent_intensity = smoothed;
    }
}
```

**Expert vs Novice**:
- **Novice**: Hard cuts between "calm" and "combat" tracks
- **Expert**: Continuous intensity scaling with musical timing awareness

## QUALITY GATES

Audio implementation is complete when ALL conditions are verified:

- [ ] **Spatial Audio Performance**: HRTF processing uses <2ms per source; total audio CPU <10% of frame time
- [ ] **Procedural Sound Variation**: No audible repetition in 5+ minutes of continuous footsteps/environmental audio
- [ ] **Mobile Session Handling**: Audio correctly pauses/resumes during phone calls, route changes, and interruptions
- [ ] **Distance Rolloff Accuracy**: 3D positioned sounds follow inverse-square law with proper reference distance
- [ ] **RTPC Parameter Validation**: All real-time parameters (0.0-1.0) respond smoothly without pops or clicks
- [ ] **Memory Budget Compliance**: Total audio assets <50MB mobile, <200MB desktop; streaming works for large content
- [ ] **UI Sound Levels**: Interface audio at -18 to -24dB; never conflicts with gameplay audio
- [ ] **Platform Audio Guidelines**: iOS/Android audio session categories correct; respects system volume controls
- [ ] **Middleware Integration**: All audio events fire correctly; no missing dependencies or broken references
- [ ] **Haptic-Audio Sync**: Tactile feedback matches audio transients within 10ms on supported devices

## NOT-FOR Boundaries

**This skill should NOT be used for:**

- **Music composition/production** → Use DAW-specific skills (Logic, Ableton, Pro Tools)
- **Voice synthesis/cloning** → Use `voice-audio-engineer` skill instead
- **Linear audio post-production** → Film/TV workflows require different expertise
- **Podcast/broadcast editing** → Use standard audio editor workflows
- **Hardware microphone setup** → Audio engineering hardware expertise
- **Real-time voice chat implementation** → Use WebRTC/networking specialists
- **Audio compression/streaming protocols** → Use backend/networking skills
- **Machine learning audio models** → Use ML/AI specialists for model training

**Delegation Rules:**
- For voice AI: "Use **voice-audio-engineer** for TTS, voice cloning, speech recognition"
- For music creation: "Use DAW specialists for composition, arrangement, mixing"
- For video audio: "Use video editor skills for linear media synchronization"
## Imported bundle navigation

These preserved source files add depth when their stated topic is needed.

- [references/implementations.md](references/implementations.md) — Sound Engineering Implementation Reference.
