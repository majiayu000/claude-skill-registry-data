---
name: composable-svelte-media
description: Audio, video, and voice components for Composable Svelte. Use when implementing audio players, video embeds, or voice input. Covers AudioPlayer (Web Audio API), VideoEmbed (YouTube/Vimeo/Twitch), and VoiceInput (MediaRecorder) from @composable-svelte/media package.
---

# Composable Svelte Media Package

Audio playback, video embedding, and voice input components.

---

## PACKAGE OVERVIEW

**Package**: `@composable-svelte/media`

**Purpose**: Rich interactive media components for audio, video, and voice.

**Technology Stack**:
- **Web Audio API**: High-performance audio playback
- **MediaRecorder API**: Voice recording and processing
- **Platform Integration**: YouTube, Vimeo, Twitch, Dailymotion, Wistia, etc.

**Core Components**:
- `AudioPlayer` - Full-featured audio player with playlists
- `VideoEmbed` - Platform-agnostic video embedding
- `VoiceInput` - Voice recording with push-to-talk

**State Management**:
All components follow Composable Architecture patterns with dedicated reducers and type-safe actions.

---

## AUDIO PLAYER

**Purpose**: Full-featured audio player with playlist support, shuffle, loop modes, and visualizations.

### Quick Start

```typescript
import { createStore } from '@composable-svelte/core';
import {
  MinimalAudioPlayer,
  FullAudioPlayer,
  audioPlayerReducer,
  createInitialAudioPlayerState
} from '@composable-svelte/media';

// Create player store
const playerStore = createStore({
  initialState: createInitialAudioPlayerState({
    tracks: [
      {
        id: '1',
        title: 'Summer Breeze',
        artist: 'Jazz Ensemble',
        url: '/audio/track1.mp3',
        duration: 245
      },
      {
        id: '2',
        title: 'Midnight Drive',
        artist: 'Synthwave Collective',
        url: '/audio/track2.mp3',
        duration: 312
      }
    ]
  }),
  reducer: audioPlayerReducer,
  dependencies: {}
});

// Render player
<FullAudioPlayer {playerStore} />
```

### Component Variants

**MinimalAudioPlayer**:
- Compact UI (play/pause, track info, progress bar)
- Best for embedded players
- No playlist UI

**FullAudioPlayer**:
- Complete controls (play/pause, skip, shuffle, loop, volume)
- Playlist view
- Audio visualizer
- Best for dedicated music players

**PlaylistView**:
- Standalone playlist component
- Drag-and-drop reordering
- Track search/filter
- Use with either player variant

### Props

**MinimalAudioPlayer**:
- `playerStore: Store<AudioPlayerState, AudioPlayerAction>` - Player store (required)

**FullAudioPlayer**:
- `playerStore: Store<AudioPlayerState, AudioPlayerAction>` - Player store (required)
- `showVisualizer: boolean` - Show audio visualizer (default: true)
- `showPlaylist: boolean` - Show playlist UI (default: true)

### State Interface

```typescript
interface AudioPlayerState {
  // Playback
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  volume: number;              // 0-100
  isMuted: boolean;

  // Playlist
  tracks: AudioTrack[];
  currentTrackIndex: number;
  queue: string[];             // Track IDs

  // Modes
  loopMode: 'none' | 'one' | 'all';
  shuffle: boolean;
  shuffleOrder: number[] | null;

  // UI State
  isLoading: boolean;
  isSeeking: boolean;
  error: string | null;

  // Visualizer
  visualizerData: Uint8Array | null;
}

interface AudioTrack {
  id: string;
  title: string;
  artist: string;
  url: string;
  duration: number;
  albumArt?: string;
  album?: string;
}
```

### Actions

```typescript
type AudioPlayerAction =
  // Playback Control
  | { type: 'play' }
  | { type: 'pause' }
  | { type: 'togglePlayPause' }
  | { type: 'stop' }
  | { type: 'seek'; time: number }

  // Track Navigation
  | { type: 'nextTrack' }
  | { type: 'previousTrack' }
  | { type: 'selectTrack'; trackIndex: number }

  // Volume
  | { type: 'setVolume'; volume: number }
  | { type: 'toggleMute' }

  // Modes
  | { type: 'toggleShuffle' }
  | { type: 'cycleLoopMode' }
  | { type: 'setLoopMode'; mode: 'none' | 'one' | 'all' }

  // Playlist
  | { type: 'addTrack'; track: AudioTrack }
  | { type: 'removeTrack'; trackId: string }
  | { type: 'clearPlaylist' }

  // Internal Events
  | { type: 'timeUpdate'; time: number }
  | { type: 'trackEnded' }
  | { type: 'loadingStarted' }
  | { type: 'loadingCompleted'; duration: number }
  | { type: 'errorOccurred'; error: string };
```

### Complete Example

```typescript
<script lang="ts">
import { createStore } from '@composable-svelte/core';
import {
  FullAudioPlayer,
  PlaylistView,
  audioPlayerReducer,
  createInitialAudioPlayerState,
  type AudioTrack
} from '@composable-svelte/media';

// Sample tracks
const tracks: AudioTrack[] = [
  {
    id: '1',
    title: 'Cosmic Journey',
    artist: 'Space Orchestra',
    url: '/audio/cosmic.mp3',
    duration: 312,
    albumArt: '/images/cosmic.jpg',
    album: 'Stellar Sounds'
  },
  {
    id: '2',
    title: 'Digital Dreams',
    artist: 'Synthwave Collective',
    url: '/audio/digital.mp3',
    duration: 245,
    albumArt: '/images/digital.jpg',
    album: 'Neon Nights'
  }
];

// Create store
const playerStore = createStore({
  initialState: createInitialAudioPlayerState({
    tracks,
    volume: 75,
    loopMode: 'all'
  }),
  reducer: audioPlayerReducer,
  dependencies: {}
});

// Add tracks dynamically
function addTrackToPlaylist(track: AudioTrack) {
  playerStore.dispatch({ type: 'addTrack', track });
}
</script>

<div class="music-app">
  <FullAudioPlayer
    {playerStore}
    showVisualizer={true}
    showPlaylist={true}
  />

  <!-- Status display -->
  {#if $playerStore.error}
    <div class="error-message">{$playerStore.error}</div>
  {/if}
</div>
```

---

## VIDEO EMBED

**Purpose**: Platform-agnostic video embedding for YouTube, Vimeo, Twitch, Dailymotion, and more.

### Quick Start

```typescript
import { VideoEmbed } from '@composable-svelte/media';

<!-- YouTube video -->
<VideoEmbed
  url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  aspectRatio="16:9"
/>

<!-- Vimeo video -->
<VideoEmbed
  url="https://vimeo.com/123456789"
  autoplay={false}
/>

<!-- Auto-detect platform -->
<VideoEmbed url={videoUrl} />
```

### Supported Platforms

- **YouTube** (youtube.com, youtu.be)
- **Vimeo** (vimeo.com)
- **Twitch** (twitch.tv - videos and clips)
- **Dailymotion** (dailymotion.com)
- **Wistia** (wistia.com)
- **Generic video** (mp4, webm, ogg via HTML5 video element)

### Props

- `url: string` - Video URL (required)
- `aspectRatio: '16:9' | '4:3' | '1:1' | '21:9'` - Aspect ratio (default: '16:9')
- `autoplay: boolean` - Auto-play video (default: false)
- `muted: boolean` - Start muted (default: false)
- `controls: boolean` - Show controls (default: true)
- `loop: boolean` - Loop video (default: false)
- `startTime: number` - Start position in seconds (optional)
- `class: string` - Custom CSS class (optional)

### Utility Functions

```typescript
import {
  detectVideo,
  extractVideosFromMarkdown,
  getPlatformConfig,
  getSupportedPlatforms
} from '@composable-svelte/media';

// Detect platform from URL
const platform = detectVideo('https://www.youtube.com/watch?v=abc123');
// Returns: 'youtube'

// Extract all videos from markdown
const videos = extractVideosFromMarkdown(markdownText);
// Returns: [{ url: '...', platform: 'youtube', id: 'abc123' }, ...]

// Get platform configuration
const config = getPlatformConfig('youtube');
// Returns: { name: 'YouTube', embedTemplate: '...', ... }

// List all supported platforms
const platforms = getSupportedPlatforms();
// Returns: ['youtube', 'vimeo', 'twitch', ...]
```

### Examples

```typescript
<!-- Basic YouTube embed -->
<VideoEmbed url="https://www.youtube.com/watch?v=dQw4w9WgXcQ" />

<!-- Vimeo with custom aspect ratio -->
<VideoEmbed
  url="https://vimeo.com/123456789"
  aspectRatio="4:3"
/>

<!-- Twitch clip with autoplay -->
<VideoEmbed
  url="https://clips.twitch.tv/ClipSlugHere"
  autoplay={true}
  muted={true}
/>

<!-- YouTube starting at specific time -->
<VideoEmbed
  url="https://www.youtube.com/watch?v=abc123"
  startTime={90}
/>

<!-- Generic video file -->
<VideoEmbed
  url="/videos/tutorial.mp4"
  controls={true}
  loop={false}
/>
```

### Markdown Integration

```typescript
<script lang="ts">
import { VideoEmbed, extractVideosFromMarkdown } from '@composable-svelte/media';

const markdown = `
# My Post

Check out this video:
https://www.youtube.com/watch?v=dQw4w9WgXcQ

And this Vimeo:
https://vimeo.com/123456789
`;

const videos = extractVideosFromMarkdown(markdown);
</script>

<!-- Render all detected videos -->
{#each videos as video}
  <VideoEmbed url={video.url} />
{/each}
```

---

## VOICE INPUT

**Purpose**: Voice recording with push-to-talk and conversation modes, real-time transcription support.

### Quick Start

```typescript
import { createStore } from '@composable-svelte/core';
import {
  VoiceInput,
  voiceInputReducer,
  createInitialVoiceInputState
} from '@composable-svelte/media';

// Create voice input store
const voiceStore = createStore({
  initialState: createInitialVoiceInputState({
    mode: 'push-to-talk'
  }),
  reducer: voiceInputReducer,
  dependencies: {
    onAudioData: async (audioBlob) => {
      // Send to transcription service
      const formData = new FormData();
      formData.append('audio', audioBlob);
      const response = await fetch('/api/transcribe', {
        method: 'POST',
        body: formData
      });
      const { text } = await response.json();
      return text;
    }
  }
});

<VoiceInput {voiceStore} />
```

### Recording Modes

**Push-to-Talk**:
- Hold button to record
- Release to stop
- Best for short messages
- Lower latency

**Conversation**:
- Toggle recording on/off
- Best for long-form speech
- Automatic silence detection (optional)

### Props

- `voiceStore: Store<VoiceInputState, VoiceInputAction>` - Voice input store (required)
- `showWaveform: boolean` - Show audio waveform (default: true)
- `showTimer: boolean` - Show recording timer (default: true)
- `class: string` - Custom CSS class (optional)

### State Interface

```typescript
interface VoiceInputState {
  // Recording
  isRecording: boolean;
  isPaused: boolean;
  mode: 'push-to-talk' | 'conversation';

  // Audio
  audioBlob: Blob | null;
  audioUrl: string | null;
  duration: number;              // Recording duration in seconds

  // Transcription
  isTranscribing: boolean;
  transcript: string | null;
  transcriptError: string | null;

  // Visualization
  waveformData: Uint8Array | null;
  volumeLevel: number;           // 0-100

  // Error handling
  error: string | null;
  permissionDenied: boolean;
}
```

### Actions

```typescript
type VoiceInputAction =
  // Recording
  | { type: 'startRecording' }
  | { type: 'stopRecording' }
  | { type: 'pauseRecording' }
  | { type: 'resumeRecording' }
  | { type: 'cancelRecording' }

  // Mode
  | { type: 'setMode'; mode: 'push-to-talk' | 'conversation' }

  // Transcription
  | { type: 'transcriptionStarted' }
  | { type: 'transcriptionCompleted'; transcript: string }
  | { type: 'transcriptionFailed'; error: string }

  // Internal Events
  | { type: 'recordingStarted' }
  | { type: 'recordingStopped'; audioBlob: Blob; duration: number }
  | { type: 'audioDataAvailable'; data: Uint8Array }
  | { type: 'volumeChanged'; level: number }
  | { type: 'errorOccurred'; error: string }
  | { type: 'permissionDenied' };
```

### Dependencies

```typescript
interface VoiceInputDependencies {
  // Transcription handler (optional)
  onAudioData?: (audioBlob: Blob) => Promise<string>;

  // Audio processing (optional)
  onAudioProcessed?: (audioBlob: Blob) => Promise<Blob>;
}
```

### Complete Example

```typescript
<script lang="ts">
import { createStore, Effect } from '@composable-svelte/core';
import {
  VoiceInput,
  voiceInputReducer,
  createInitialVoiceInputState
} from '@composable-svelte/media';

// Create voice input store with transcription
const voiceStore = createStore({
  initialState: createInitialVoiceInputState({
    mode: 'push-to-talk'
  }),
  reducer: voiceInputReducer,
  dependencies: {
    // Send audio to Whisper API for transcription
    onAudioData: async (audioBlob: Blob) => {
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.webm');
      formData.append('model', 'whisper-1');

      const response = await fetch('https://api.openai.com/v1/audio/transcriptions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${OPENAI_API_KEY}`
        },
        body: formData
      });

      const { text } = await response.json();
      return text;
    }
  }
});

// Toggle recording mode
function toggleMode() {
  const newMode = $voiceStore.mode === 'push-to-talk' ? 'conversation' : 'push-to-talk';
  voiceStore.dispatch({ type: 'setMode', mode: newMode });
}
</script>

<div class="voice-container">
  <VoiceInput
    {voiceStore}
    showWaveform={true}
    showTimer={true}
  />

  <!-- Mode toggle -->
  <button onclick={toggleMode}>
    Mode: {$voiceStore.mode}
  </button>

  <!-- Display transcript -->
  {#if $voiceStore.transcript}
    <div class="transcript">
      <strong>Transcript:</strong>
      <p>{$voiceStore.transcript}</p>
    </div>
  {/if}

  <!-- Error display -->
  {#if $voiceStore.error}
    <div class="error">{$voiceStore.error}</div>
  {/if}

  {#if $voiceStore.permissionDenied}
    <div class="warning">Microphone access denied</div>
  {/if}
</div>
```

### Browser Permissions

Voice input requires microphone permissions. Handle permission flow:

```typescript
// Check permission before recording
if ($voiceStore.permissionDenied) {
  // Show permission request UI
  alert('Please grant microphone access to use voice input');
}
```

---

## AUDIO MANAGER

**Purpose**: Low-level audio management for custom implementations.

### API

```typescript
import {
  AudioManager,
  createAudioManager,
  getAudioManager,
  deleteAudioManager
} from '@composable-svelte/media';

// Create manager
const manager = createAudioManager({
  id: 'my-player',
  onTimeUpdate: (time) => console.log('Time:', time),
  onEnded: () => console.log('Ended'),
  onError: (error) => console.error('Error:', error)
});

// Load and play
await manager.load('/audio/track.mp3');
manager.play();

// Get existing manager
const existing = getAudioManager('my-player');

// Cleanup
deleteAudioManager('my-player');
```

---

## COMPONENT SELECTION GUIDE

**When to use each component**:

**AudioPlayer**:
- Music streaming apps
- Podcast players
- Audio courses
- Meditation apps
- Need playlist management

**VideoEmbed**:
- Blog posts with videos
- Video galleries
- Educational content
- Marketing pages
- Platform-agnostic video

**VoiceInput**:
- Voice commands
- Audio messages
- Voice notes
- Transcription apps
- Accessibility features

---

## CROSS-REFERENCES

**Related Skills**:
- **composable-svelte-core**: Store, reducer, Effect system
- **composable-svelte-chat**: StreamingChat (can integrate with VoiceInput)
- **composable-svelte-code**: CodeEditor, syntax highlighting
- **composable-svelte-components**: UI components (Button, Input, etc.)

**When to Use Each Package**:
- **media**: Audio players, video embeds, voice input
- **chat**: Real-time chat, streaming responses
- **code**: Code editors, syntax highlighting, visual programming
- **graphics**: 3D scenes, WebGPU/WebGL rendering
- **charts**: 2D data visualization

---

## TESTING PATTERNS

### AudioPlayer Testing

```typescript
import { TestStore } from '@composable-svelte/core';
import { audioPlayerReducer, createInitialAudioPlayerState } from '@composable-svelte/media';

const store = new TestStore({
  initialState: createInitialAudioPlayerState({
    tracks: [
      { id: '1', title: 'Track 1', url: '/audio/1.mp3', duration: 180 }
    ]
  }),
  reducer: audioPlayerReducer,
  dependencies: {}
});

// Test play
await store.send({ type: 'play' }, (state) => {
  expect(state.isPlaying).toBe(true);
});

// Test track change
await store.send({ type: 'nextTrack' }, (state) => {
  expect(state.currentTrackIndex).toBe(1);
});
```

### VoiceInput Testing

```typescript
import { TestStore } from '@composable-svelte/core';
import { voiceInputReducer, createInitialVoiceInputState } from '@composable-svelte/media';

const store = new TestStore({
  initialState: createInitialVoiceInputState(),
  reducer: voiceInputReducer,
  dependencies: {
    onAudioData: vi.fn((blob) => Promise.resolve('Test transcript'))
  }
});

// Test recording start
await store.send({ type: 'startRecording' });
await store.receive({ type: 'recordingStarted' }, (state) => {
  expect(state.isRecording).toBe(true);
});
```

---

## TROUBLESHOOTING

**AudioPlayer not playing**:
- Check audio URL is accessible
- Verify browser autoplay policy (may require user interaction)
- Ensure audio format is supported (mp3, wav, ogg recommended)

**VideoEmbed not loading**:
- Verify URL format matches platform requirements
- Check platform embed permissions (some require API keys)
- Ensure platform allows embedding (some videos are restricted)

**VoiceInput permission denied**:
- User must grant microphone access
- HTTPS required (except localhost)
- Check browser compatibility (MediaRecorder API)
