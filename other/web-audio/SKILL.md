---
name: web-audio
description: Use when generating all game or app sound in code with the Web Audio API — synthesised sound effects, a step sequencer for background music, dynamic music that reacts to game state, mixing and ducking, volume settings, speech synthesis for voices, and verifying sound automatically without listening. Also use when a screen is silent, sounds start late, the first sound never plays, or voices sound robotic or are missing.
---

# Web Audio (synthesised sound and music)

Default: one `AudioContext` created or resumed on the first user gesture, a small mixer graph (master → music / effects / voice buses), effects synthesised from oscillators, noise and envelopes, music scheduled ahead on the audio clock, and automated checks that measure signal level.

## Graph

```ts
const ctx = new AudioContext();
const master = new GainNode(ctx, { gain: 0.8 });
const music = new GainNode(ctx), sfx = new GainNode(ctx), voice = new GainNode(ctx);
[music, sfx, voice].forEach(b => b.connect(master));
master.connect(ctx.destination);
```

Expose the bus gains as user settings and persist them.

## Sound effects from code

- Envelope everything (`gain.setValueAtTime(0, t); linearRampToValueAtTime(peak, t + a); exponentialRampToValueAtTime(0.001, t + a + d)`); abrupt starts and stops click.
- Hits: short noise burst through a band-pass filter + a pitched sine drop. Coins: two quick square-wave notes a fourth or fifth apart. UI taps: very short, quiet ticks.
- Give each meaningful action its own sound; keep a table of actions → sound and test that every action has one.

## Music sequencer

- Schedule notes slightly ahead (look-ahead ~100 ms, timer every ~25 ms) using `ctx.currentTime`; `setTimeout` alone drifts.
- Patterns as data (tempo, steps, instrument per track); render the same data offline (`OfflineAudioContext`) to a WAV file for review.
- Dynamic music: open a filter, double a drum pattern or add a layer when tension rises; duck music (lower its bus gain) under important cues.

## State bugs to avoid

- **Before the context exists:** if the game asks for a track before the first gesture, store the request and start it when the context is ready. Recording "current track = X" before it actually plays makes a later "play X" return early, and the screen stays silent.
- Pick the track in one place (the screen router) rather than from many screens.

## Speech synthesis for voices

- `speechSynthesis.getVoices()` is empty until `voiceschanged` fires; wait for it.
- Do not filter out remote voices blindly — on some browsers the good voices are the remote ones.
- Fall back in order: local voice for the language → remote voice → another voice with subtitles → effect sound + subtitles.
- Feed the synthesiser text written for reading (e.g. kana for Japanese titles), separate from the displayed text.
- Keep a reference to each utterance until `onend`, or garbage collection may cut it off.

## Verification without ears

- Connect an `AnalyserNode` to the master and compute RMS; in browser tests assert RMS above a threshold on every screen that should have sound, and below it where silence is expected.
- Render music offline and check duration, peak level (no clipping above 0 dBFS) and that pitch-modulation depth is what you intended — a wrong vibrato formula can swing pitch by hundreds of cents.

## Pitfalls

- **Autoplay policy:** contexts start `suspended`; call `resume()` inside a gesture.
- **Too many nodes:** disconnect finished nodes; reuse noise buffers.
- **Mobile silent switch** on some phones mutes Web Audio; tell users if sound matters.
- **Headless machines** may have no audio device or voices; tests must use analysers and mocks, and real listening remains a human check.
