---
name: cm-readit
description: Turn any website into an audio-enabled experience. Covers TTS reading mode (SpeechSynthesis API), pre-recorded MP3 audio player, and Voice CRO trigger system. Zero dependencies, works on any static or dynamic site. Use when adding read-aloud, audio player, or voice-based conversion features.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# CM ReadIt — Web Audio Experience Skill

> **Philosophy:** Reading is passive. Listening is intimate. Voice builds trust faster than any headline.
> **Core Principle:** Zero dependencies. Progressive enhancement. Respect user's device and preferences.

---

## 🎯 Selective Reading Rule (MANDATORY)

| File | Status | When to Read |
|------|--------|--------------|
| [tts-engine.md](tts-engine.md) | 🔴 **REQUIRED** | Adding TTS / read-aloud to any page |
| [audio-player.md](audio-player.md) | ⚪ Optional | Pre-recorded MP3 playback |
| [voice-cro.md](voice-cro.md) | ⚪ Optional | Trigger-based voice sales / CRO |
| [ui-patterns.md](ui-patterns.md) | ⚪ Optional | Player bar & bottom sheet design |

> 🔴 **tts-engine.md = ALWAYS READ when implementing TTS. Others = only if relevant.**

---

## Quick Decision Tree

```
"I need audio on my website"
│
├─ Read article content aloud (text-to-speech)
│  └─ Use: TTS Engine → tts-engine.md
│     ├─ Blog / article pages → Content Reader pattern
│     ├─ Documentation → Section Reader pattern
│     └─ E-commerce → Product Description Reader pattern
│
├─ Play pre-recorded audio files (MP3/WAV)
│  └─ Use: Audio Player → audio-player.md
│     ├─ Podcasts / interviews → Playlist pattern
│     ├─ Sales pitch / welcome → Triggered playback
│     └─ Background ambient → Loop pattern
│
├─ Voice-based conversion optimization (CRO)
│  └─ Use: Voice CRO → voice-cro.md
│     ├─ Landing pages → Trigger-based bottom sheet
│     ├─ Service pages → Per-page audio scripts
│     └─ Course pages → Social proof audio
│
└─ Combination (TTS + CRO)
   └─ Read tts-engine.md + voice-cro.md
      └─ Ensure no conflict (TTS reader vs CRO player)
```

---

## 🧠 Core Principles (Internalize These)

### 1. The 3 Audio Engines

| Engine | API | Source | Best For |
|--------|-----|--------|----------|
| **TTS Reader** | `SpeechSynthesis` | Page text content | Blogs, articles, docs |
| **Audio Player** | `HTMLAudioElement` | Pre-recorded MP3 | Sales, podcasts, guides |
| **Voice CRO** | `Audio` + triggers | MP3 + behavior detection | Landing pages, sales |

### 2. Progressive Enhancement

```
Feature detection → Graceful degradation → Never break the page

if (!('speechSynthesis' in window)) return;  // TTS
if (!window.Audio) return;                    // Audio
```

**Rule:** Audio features are ENHANCEMENTS. The page must function 100% without them.

### 3. Content Extraction Principle

```
Clone → Strip → Clean → Split → Speak

DON'T read the raw DOM.
DO clone, remove noise, extract clean text.
```

**Strip list (always remove before speaking):**
- CTAs, promotions, ads
- Navigation, footer, sidebar
- Images, videos, iframes, SVGs
- Scripts, styles, hidden elements
- Tags, badges, metadata

### 4. The Chunking Problem

Browsers have a **hard limit** on utterance length (~3000-5000 chars depending on browser/OS). Long text must be split into chunks.

```
Split Strategy:
├─ Split on sentence boundaries (. ! ? \n)
├─ Max chunk: 2500 chars (safe across all browsers)
├─ Preserve sentence integrity (never split mid-sentence)
└─ Chain chunks via onend callback
```

### 5. Voice Selection Priority

```
Language voices:
1. Local service voice (faster, works offline)
2. Network voice (higher quality, needs internet)
3. Any voice matching language prefix
4. null (browser default)
```

### 6. Chrome Keep-Alive Bug

> ⚠️ **CRITICAL:** Chrome silently stops SpeechSynthesis after ~15 seconds of continuous speech. This is the #1 gotcha.

```javascript
// Workaround: pause/resume every 10s
setInterval(() => {
    if (synth.speaking && !synth.paused) {
        synth.pause();
        synth.resume();
    }
}, 10000);
```

### 7. synth.cancel() Triggers onerror

> ⚠️ **GOTCHA:** Calling `synth.cancel()` fires the `onerror` event on any active utterance with error type `'canceled'` or `'interrupted'`.

**Solution:** Use a guard flag or check error type:
```javascript
u.onerror = function(e) {
    if (e.error === 'canceled' || e.error === 'interrupted') return;
    stopReading();
};
```

---

## 🏗️ Architecture Pattern

### Minimal TTS Reader (Copy-Paste Starting Point)

```
┌─────────────────────────────────────────┐
│                  IIFE                    │
│                                          │
│  ┌─ Feature Detection ─┐                │
│  │  speechSynthesis?    │                │
│  └──────────┬───────────┘                │
│             ▼                            │
│  ┌─ Content Extraction ─┐               │
│  │  Clone → Strip → Clean│              │
│  └──────────┬────────────┘               │
│             ▼                            │
│  ┌─ Chunking Engine ────┐               │
│  │  Split on sentences   │              │
│  │  Max 2500 chars       │              │
│  └──────────┬────────────┘               │
│             ▼                            │
│  ┌─ Utterance Builder ──┐               │
│  │  Set voice/rate/pitch │              │
│  │  Chain via onend      │              │
│  └──────────┬────────────┘               │
│             ▼                            │
│  ┌─ Player UI ──────────┐               │
│  │  Bar: play/pause/stop │              │
│  │  Progress indicator   │              │
│  │  Trigger button       │              │
│  └──────────┬────────────┘               │
│             ▼                            │
│  ┌─ Keep-Alive Timer ───┐               │
│  │  pause/resume @ 10s  │               │
│  └───────────────────────┘               │
└──────────────────────────────────────────┘
```

### Lifecycle

```
Init → Detect → Inject Trigger Button
         │
   User clicks ▶
         │
   Extract Text → Chunk → Build Utterances
         │
   synth.speak(chunk[0])
         │
   chunk[0].onend → speak(chunk[1]) → ... → speak(chunk[N])
         │                                        │
   Keep-Alive Timer running                   chunk[N].onend
         │                                        │
   User clicks ⏸ → synth.pause()             stopReading()
   User clicks ▶ → synth.resume()            cleanup UI
   User clicks ✕ → synth.cancel()
```

---

## 📐 Implementation Checklist

### For TTS Reader
- [ ] Feature detection (`speechSynthesis` in window)
- [ ] Content container identified (ID or selector)
- [ ] Strip list defined (what to remove before reading)
- [ ] Chunk size set (default 2500)
- [ ] Voice selection logic (language-specific)
- [ ] Player bar UI (play/pause/close + progress)
- [ ] Trigger button injected (topbar or floating)
- [ ] Chrome keep-alive timer (10s interval)
- [ ] `onerror` guard (handle cancel/interrupted)
- [ ] `beforeunload` cleanup
- [ ] `prefers-reduced-motion` respect
- [ ] Mobile safe-area padding

### For Audio Player
- [ ] Audio files hosted and accessible
- [ ] Preload strategy (`none` → load on demand)
- [ ] Play/pause toggle with state management
- [ ] Progress bar with `currentTime/duration`
- [ ] Error handling (network, format, autoplay policy)
- [ ] Session state (dismissed = don't show again)

### For Voice CRO
- [ ] Per-page config object (delay, scroll threshold, audio URLs)
- [ ] Trigger conditions (time + scroll AND/OR interaction)
- [ ] Bottom sheet UI (icon, text, CTA, dismiss)
- [ ] Player bar UI (toggle, progress, CTA button)
- [ ] Session dismissal tracking
- [ ] Stats tracking (shown/listened/dismissed)
- [ ] No conflict with TTS Reader

---

## ⚠️ Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Chrome stops after 15s | Audio cuts mid-sentence | Keep-alive timer (pause/resume) |
| `synth.cancel()` fires onerror | Settings sheet closes immediately | Guard flag or check error type |
| Voices not loaded | No voice available | Listen for `voiceschanged` event |
| Chunk too large | Utterance fails silently | Max 2500 chars per chunk |
| Reading CTA text | TTS reads "Book Now" button text | Strip non-content elements |
| Autoplay blocked | Audio won't start on mobile | Require user interaction first |
| Multiple audio conflicts | TTS + CRO play simultaneously | Mutual exclusion check |
| No cleanup on nav | Audio keeps playing | `beforeunload` → `synth.cancel()` |

---

## 🌐 Multi-Language Support

```
Voice selection by language:
├─ Vietnamese: v.lang === 'vi-VN' || v.lang.startsWith('vi')
├─ English: v.lang === 'en-US' || v.lang.startsWith('en')
├─ Japanese: v.lang === 'ja-JP' || v.lang.startsWith('ja')
├─ Korean: v.lang === 'ko-KR' || v.lang.startsWith('ko')
└─ Any: Pass language code as config parameter
```

Set `utterance.lang` to match the content language for correct pronunciation.

---

## 📚 Reference Files

| File | Content |
|------|---------|
| [tts-engine.md](tts-engine.md) | Complete SpeechSynthesis API reference, chunking strategies, voice selection |
| [audio-player.md](audio-player.md) | HTMLAudioElement patterns, preload strategies, error handling |
| [voice-cro.md](voice-cro.md) | Trigger system, bottom sheet patterns, CRO analytics |
| [ui-patterns.md](ui-patterns.md) | Player bar CSS, bottom sheet CSS, animations, responsive design |

---

## 🔗 Reference Implementations

| File | Description |
|------|-------------|
| [examples/blog-reader.js](examples/blog-reader.js) | Complete TTS reader — Substack-style, 350 LOC |
| [examples/voice-cro.js](examples/voice-cro.js) | Complete Voice CRO trigger system — 390 LOC |

---

> **Remember:** Voice is the most personal interface. A well-placed audio feature can increase engagement 3-5x. But unwanted audio is the fastest way to lose a user. **Always require user initiation. Never autoplay.**
