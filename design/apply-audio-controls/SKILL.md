---
name: apply-audio-controls
description: Use when adding audio or video with sound that plays automatically — to ensure users can pause, stop, or mute it without being unable to hear their screen reader or complete tasks in a noisy environment.
source: W3C WCAG 2.1 SC 1.4.2 Audio Control (Level A); WAI-ARIA media player pattern; W3C Media Accessibility User Requirements (MAUR)
tags: [accessibility, wcag, a11y, audio, autoplay, screen-reader, pause-controls, developer]
related: [apply-timed-content-controls, apply-media-captions, design-accessibility-standards]
---

# Apply Audio Controls

Provide a mechanism to pause, stop, or mute any audio that plays automatically — so screen
reader users can hear their AT output and users in quiet environments can silence the page.

## Why This Is Best Practice

**Adopted by:** WCAG 2.1 SC 1.4.2 (Level A) is required by Section 508 (US), EU EN 301 549,
and UK PSBAR 2018 — Level A means it is the baseline accessibility floor. All major browsers
block audio autoplay by default (Chrome 66+, Firefox 66+, Safari 11+) as a direct response to
this accessibility and user experience problem. The W3C Media Accessibility User Requirements
document identifies audio control as a core screen reader compatibility requirement.
**Impact:** Screen reader users navigate by listening. Auto-playing audio — even at low volume —
overlaps with screen reader speech, making page content inaudible. Users with hearing impairments
who rely on visual feedback cannot tell where audio is coming from. WebAIM's 2024 survey found that
auto-playing audio was rated the #3 most annoying accessibility barrier by screen reader users.
**Why best:** The alternative — `<audio autoplay>` with no controls — has no legitimate use case
that outweighs the accessibility cost. Browser autoplay blocking means most auto-playing audio
fails silently in modern browsers anyway. Starting muted with user-initiated unmute is the correct
pattern for background audio; visible controls are required for any audio that does play.

Sources: W3C WCAG 2.1 SC 1.4.2 (2018); W3C Media Accessibility User Requirements; WebAIM
Screen Reader Survey 2024; Chrome Autoplay Policy (2018)

## Steps

### Step 1: Never autoplay audio — or start muted with visible controls

```html
<!-- Wrong — audio autoplays, conflicts with screen readers -->
<audio autoplay src="background-music.mp3"></audio>
<video autoplay src="promo.mp4"></video>

<!-- Right — audio does not autoplay -->
<audio controls src="background-music.mp3">
  <p>Your browser does not support audio playback.</p>
</audio>

<!-- Right — video autoplays but starts muted; user must unmute -->
<video autoplay muted playsinline controls src="promo.mp4">
  <track kind="captions" src="promo.vtt" srclang="en" label="English">
</video>
```

`muted` + `autoplay` satisfies 1.4.2 because there is no audio output until the user
explicitly unmutes. Native `controls` provides the user mechanism.

### Step 2: If audio must autoplay — put the stop/mute control first in tab order

If autoplay audio is unavoidable (e.g., audio serves as a live alert), place the pause/mute
control as the very first focusable element on the page — before any other content:

```html
<body>
  <!-- First focusable element is the audio control — before navigation, before content -->
  <div id="audio-control-bar">
    <button id="mute-audio" type="button" aria-pressed="false">
      Mute background audio
    </button>
    <audio id="bg-audio" autoplay loop src="ambient.mp3"></audio>
  </div>

  <nav><!-- navigation --></nav>
  <main><!-- content --></main>
</body>
```

```javascript
const muteBtn = document.getElementById('mute-audio');
const audio   = document.getElementById('bg-audio');

muteBtn.addEventListener('click', () => {
  audio.muted = !audio.muted;
  muteBtn.setAttribute('aria-pressed', String(audio.muted));
  muteBtn.textContent = audio.muted ? 'Unmute background audio' : 'Mute background audio';
});
```

"First in tab order" means a screen reader user pressing Tab immediately reaches the
mute control — before they encounter any content obscured by the audio.

### Step 3: Provide independent volume control (alternative to stop/pause)

SC 1.4.2 is satisfied by either: (a) pause/stop, (b) mute, or (c) volume control
independent of system volume. For background audio or ambient sound:

```html
<label for="bg-volume">Background audio volume</label>
<input type="range" id="bg-volume" min="0" max="1" step="0.1" value="0.5"
       aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"
       aria-valuetext="50%">
```

```javascript
const volumeSlider = document.getElementById('bg-volume');
const bgAudio = document.getElementById('bg-audio');

volumeSlider.addEventListener('input', (e) => {
  bgAudio.volume = parseFloat(e.target.value);
  const pct = Math.round(e.target.value * 100);
  volumeSlider.setAttribute('aria-valuenow', pct);
  volumeSlider.setAttribute('aria-valuetext', `${pct}%`);
});
```

### Step 4: Verify browser autoplay policy doesn't silently break your controls

Modern browsers block autoplay with sound. Handle the blocked autoplay case:

```javascript
const audio = document.getElementById('bg-audio');

audio.play().catch((error) => {
  if (error.name === 'NotAllowedError') {
    // Autoplay blocked by browser — show a play button instead
    document.getElementById('play-prompt').removeAttribute('hidden');
  }
});
```

```html
<!-- Fallback for blocked autoplay -->
<div id="play-prompt" hidden>
  <button id="start-audio" type="button">Play background audio</button>
</div>
```

This handles the common case where developers rely on autoplay but browsers silently
block it — resulting in neither audio playing nor controls being visible.

## When NOT to Use

- **Audio shorter than 3 seconds** — SC 1.4.2 only applies to audio that autoplays for
  more than 3 seconds. A brief notification sound (< 3 sec) is exempt.
- **User-initiated audio** — audio the user explicitly started (pressing Play in a media
  player) is not autoplay and doesn't require 1.4.2 controls. Standard pause controls
  from the media player UI are sufficient.

## Common Mistakes

**Background audio with no `controls` attribute and no custom controls.** The audio plays,
no UI element exists to stop it, and keyboard users cannot reach any control. Always add
either native `controls` or a custom mute button.

**Mute button that appears only after audio starts playing.** If the mute control renders
after a JavaScript-controlled delay, keyboard users may hear audio for several seconds before
they can silence it. Render the control before audio starts.

**Volume slider without `aria-valuetext`.** A range input with values 0–1 announces "0.5"
to screen readers. Use `aria-valuenow` (numeric) + `aria-valuetext` ("50%") so the value
is meaningful when announced.