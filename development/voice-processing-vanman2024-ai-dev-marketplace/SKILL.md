---
name: voice-processing
description: Voice cloning workflows, voice library management, audio format conversion, and voice settings. Use when cloning voices, managing voice libraries, processing audio for voice creation, configuring voice settings, or when user mentions voice cloning, instant cloning, professional cloning, voice library, audio processing, voice settings, or ElevenLabs voices.
allowed-tools: Bash, Read, Write, Edit
---

# Voice Processing Skill

This skill provides comprehensive voice processing capabilities for ElevenLabs including voice cloning (instant and professional), voice library management, audio format conversion, and voice settings configuration.

## Voice Cloning Overview

ElevenLabs offers two voice cloning approaches:

### Instant Voice Cloning (IVC)
- Requires only brief audio samples (1-5 minutes)
- Fast processing and quick turnaround
- Suitable for rapid prototyping and testing
- Cannot be shared in Voice Library
- Requires Creator plan or higher

### Professional Voice Cloning (PVC)
- Requires extended training audio (30+ minutes recommended)
- Hyper-realistic, high-quality output
- Suitable for production applications
- Can be shared in Voice Library for earnings
- Requires Creator plan or higher

## Available Scripts

### 1. clone-voice.sh
Clone a voice using instant or professional method.

**Usage:**
```bash
bash scripts/clone-voice.sh --name "Voice Name" --method instant --files "audio1.mp3,audio2.mp3"
bash scripts/clone-voice.sh --name "Voice Name" --method professional --files "audio1.mp3,audio2.mp3" --description "Voice description"
```

**Features:**
- Supports both instant and professional cloning
- Multiple audio file inputs
- Automatic file validation
- Voice captcha verification
- Returns voice ID for use in TTS

### 2. list-voices.sh
Fetch and list available voices with filtering options.

**Usage:**
```bash
bash scripts/list-voices.sh --category all
bash scripts/list-voices.sh --category cloned
bash scripts/list-voices.sh --category library --search "Australian narration"
```

**Features:**
- List all voices (owned, cloned, library)
- Filter by category (cloned, library, default, voice-design)
- Search by tags and descriptions
- Display voice details (name, ID, category, description)
- JSON or table output formats

### 3. process-audio.py
Process audio files for voice cloning preparation.

**Usage:**
```bash
python scripts/process-audio.py --input audio.mp3 --output processed.mp3 --sample-rate 22050
python scripts/process-audio.py --input audio.mp3 --output processed.mp3 --remove-noise --normalize
```

**Features:**
- Audio format conversion (MP3, WAV, FLAC, OGG)
- Sample rate conversion
- Noise reduction
- Audio normalization
- Silence trimming
- Quality validation

### 4. manage-voice-library.sh
Manage voice library operations.

**Usage:**
```bash
bash scripts/manage-voice-library.sh --action add --voice-id "abc123" --collection "My Voices"
bash scripts/manage-voice-library.sh --action share --voice-id "abc123" --enable-rewards
bash scripts/manage-voice-library.sh --action remove --voice-id "abc123"
```

**Features:**
- Add voices to library
- Share professional clones for rewards
- Remove voices from library
- Add descriptions and tags
- Manage voice collections

### 5. configure-voice-settings.sh
Configure and update voice settings.

**Usage:**
```bash
bash scripts/configure-voice-settings.sh --voice-id "abc123" --stability 0.75 --similarity 0.85
bash scripts/configure-voice-settings.sh --voice-id "abc123" --get-defaults
```

**Features:**
- Get default voice settings
- Get voice-specific settings
- Update stability parameter (0.0-1.0)
- Update similarity boost (0.0-1.0)
- Update style parameter (0.0-1.0)
- Validate settings before applying

## Templates

### 1. voice-clone-config.json.template
Configuration template for voice cloning operations.

**Variables:**
- `${VOICE_NAME}` - Name for the cloned voice
- `${VOICE_DESCRIPTION}` - Description of the voice
- `${CLONING_METHOD}` - "instant" or "professional"
- `${AUDIO_FILES}` - Array of audio file paths
- `${LABELS}` - Custom tags/labels for organization

### 2. voice-settings.json.template
Voice settings configuration template.

**Variables:**
- `${VOICE_ID}` - Voice identifier
- `${STABILITY}` - Stability parameter (0.0-1.0)
- `${SIMILARITY_BOOST}` - Similarity boost (0.0-1.0)
- `${STYLE}` - Style parameter (0.0-1.0)
- `${USE_SPEAKER_BOOST}` - Enable speaker boost (true/false)

### 3. voice-library-entry.json.template
Voice library entry configuration template.

**Variables:**
- `${VOICE_ID}` - Voice identifier
- `${DISPLAY_NAME}` - Public display name
- `${DESCRIPTION}` - Voice description
- `${TAGS}` - Array of searchable tags
- `${CATEGORY}` - Voice category
- `${ENABLE_REWARDS}` - Enable cash rewards (true/false)

### 4. audio-processing-config.json.template
Audio processing pipeline configuration.

**Variables:**
- `${INPUT_FORMAT}` - Input audio format
- `${OUTPUT_FORMAT}` - Output audio format
- `${SAMPLE_RATE}` - Target sample rate (Hz)
- `${BITRATE}` - Audio bitrate (kbps)
- `${REMOVE_NOISE}` - Enable noise reduction (true/false)
- `${NORMALIZE}` - Enable normalization (true/false)

### 5. voice-verification.json.template
Voice verification captcha configuration.

**Variables:**
- `${VOICE_ID}` - Voice to verify
- `${CAPTCHA_TYPE}` - Verification type
- `${VERIFICATION_TEXT}` - Text to speak for verification

### 6. batch-clone-config.json.template
Batch voice cloning configuration for multiple voices.

**Variables:**
- `${VOICES}` - Array of voice configurations
- `${COMMON_SETTINGS}` - Shared settings across all clones
- `${OUTPUT_DIRECTORY}` - Directory for voice IDs output

## Examples

### instant-cloning/
Complete example of instant voice cloning workflow.

**Contents:**
- `README.md` - Step-by-step guide for instant cloning
- `sample-audio/` - Example audio files
- `clone-workflow.sh` - Complete workflow script
- `verify-clone.sh` - Clone verification script

### professional-cloning/
Complete example of professional voice cloning workflow.

**Contents:**
- `README.md` - Step-by-step guide for professional cloning
- `sample-audio/` - Example training audio files (30+ minutes)
- `clone-workflow.sh` - Complete workflow script
- `training-guide.md` - Best practices for training audio

### voice-library/
Voice library browsing and management examples.

**Contents:**
- `README.md` - Voice library guide
- `search-voices.sh` - Search and filter examples
- `add-to-collection.sh` - Collection management
- `share-voice.sh` - Voice sharing workflow

### audio-processing/
Audio processing pipeline examples.

**Contents:**
- `README.md` - Audio processing guide
- `convert-formats.sh` - Format conversion examples
- `prepare-for-cloning.sh` - Audio preparation workflow
- `batch-process.sh` - Batch processing script

### voice-settings-optimization/
Voice settings optimization examples.

**Contents:**
- `README.md` - Settings optimization guide
- `optimize-stability.sh` - Stability tuning
- `optimize-similarity.sh` - Similarity tuning
- `test-settings.sh` - Settings testing workflow

## Voice Cloning Best Practices

### Audio Quality Requirements
1. **Sample Rate**: 22,050 Hz or higher recommended
2. **Format**: MP3, WAV, FLAC, or OGG
3. **Quality**: Clear audio with minimal background noise
4. **Duration**:
   - Instant: 1-5 minutes minimum
   - Professional: 30+ minutes recommended
5. **Content**: Natural speech, avoid music/effects

### Multiple Files
- More files improve clone quality
- Each file should be 30 seconds to 5 minutes
- Vary intonation and emotion across files
- Consistent recording environment

### Voice Settings Parameters

**Stability (0.0-1.0)**
- Lower values: More expressive, variable
- Higher values: More consistent, stable
- Default: 0.75
- Use case: Narration (high), Dialogue (medium), Emotional (low)

**Similarity Boost (0.0-1.0)**
- Lower values: More creative, varied
- Higher values: Closer to original voice
- Default: 0.75
- Use case: Clone fidelity vs. versatility trade-off

**Style (0.0-1.0)**
- Lower values: More neutral
- Higher values: More expressive
- Default: 0.0
- Use case: Character voices (high), Neutral narration (low)

## Voice Library Features

### Discovery
- Browse 5,000+ community voices
- Search by tags, descriptions, categories
- Preview voices before adding
- Filter by language, accent, characteristics

### Sharing
- Share Professional Voice Clones only
- Earn cash rewards when others use your voice
- Add descriptions and tags for discoverability
- Control sharing permissions

### Collections
- Organize voices into custom collections
- Add/remove voices from collections
- Share collections with team members
- Export collection metadata

## API Integration

All scripts use the ElevenLabs API with the following authentication:

```bash
export ELEVEN_API_KEY="your_api_key_here"
```

API endpoints used:
- `POST /v1/voices/add` - Clone voice (instant/professional)
- `GET /v1/voices` - List all voices
- `GET /v1/voices/{voice_id}` - Get voice details
- `POST /v1/voices/{voice_id}/edit` - Update voice
- `DELETE /v1/voices/{voice_id}` - Delete voice
- `GET /v1/voices/{voice_id}/settings` - Get voice settings
- `POST /v1/voices/{voice_id}/settings/edit` - Update settings

## Troubleshooting

### Common Issues

**Voice clone quality is poor**
- Increase audio sample duration
- Ensure clear, noise-free recordings
- Use multiple audio files
- Consider upgrading to professional cloning

**API authentication fails**
- Verify ELEVEN_API_KEY is set correctly
- Check API key has necessary permissions
- Ensure account has Creator plan or higher

**Audio processing errors**
- Verify audio file format is supported
- Check file is not corrupted
- Ensure ffmpeg is installed for conversions
- Validate sample rate and bitrate

**Voice not appearing in library**
- Only Professional Voice Clones can be shared
- Verify voice verification (captcha) is complete
- Check voice meets library quality standards
- Allow time for processing and review

## Dependencies

### Required
- `curl` - API requests
- `jq` - JSON parsing
- `python3` - Audio processing scripts
- ElevenLabs API key (Creator plan or higher)

### Optional
- `ffmpeg` - Advanced audio processing
- `pydub` - Python audio manipulation
- `librosa` - Audio analysis
- `numpy` - Audio array operations

## References

- [ElevenLabs Voice Capabilities](https://elevenlabs.io/docs/capabilities/voices)
- [Instant Voice Cloning Guide](https://elevenlabs.io/docs/cookbooks/voices/instant-voice-cloning)
- [Voice API Reference](https://elevenlabs.io/docs/api-reference/voices)
- Voice Library: https://elevenlabs.io/voice-library

---

**Generated for**: ElevenLabs Plugin
**Version**: 1.0.0
