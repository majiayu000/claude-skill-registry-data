---
name: debug-ffmpeg
description: Debug FFmpeg integration and video/audio processing issues. Use when the user encounters FFmpeg errors, audio extraction problems, codec issues, or video processing failures.
---

# Debug FFmpeg Skill

Troubleshoot FFmpeg-related issues in the video processing pipeline.

## What This Skill Does

This skill helps diagnose and fix FFmpeg integration problems through systematic debugging:

1. **Verify FFmpeg Installation**: Check if FFmpeg is accessible and version
2. **Test FFmpeg Commands**: Run diagnostic commands to validate functionality
3. **Analyze Video Files**: Inspect video file properties, codecs, and streams
4. **Debug Processing Errors**: Identify specific issues in video/audio extraction
5. **Provide Solutions**: Offer concrete fixes for common FFmpeg problems

## Diagnostic Steps

When invoked, this skill follows this troubleshooting workflow:

### 1. Verify FFmpeg Accessibility

```bash
ffmpeg -version
```

Check for:
- FFmpeg version and build date
- Configuration flags and enabled libraries
- Supported codecs and formats

### 2. Inspect Video File Properties

For a given video file:
```bash
ffmpeg -i <video_file>
```

This reveals:
- Container format (MP4, MKV, AVI, etc.)
- Video codec (H.264, H.265, VP9, etc.)
- Audio codec (AAC, MP3, Opus, etc.)
- Duration, bitrate, resolution
- Stream mapping and metadata

### 3. Test Audio Extraction

Verify audio can be extracted properly:
```bash
ffmpeg -i <video_file> -vn -acodec pcm_s16le -ar 16000 -ac 1 test_output.wav
```

Parameters:
- `-vn`: No video (audio only)
- `-acodec pcm_s16le`: 16-bit PCM audio
- `-ar 16000`: 16kHz sample rate (Whisper compatible)
- `-ac 1`: Mono audio

### 4. Test Video Stream Extraction

Check if video streams can be extracted:
```bash
ffmpeg -i <video_file> -an -vcodec copy test_output.mp4
```

### 5. Review Processing Logs

Check application logs for FFmpeg errors:
- Console output from `python cli.py process`
- Log files in the project directory
- Error messages in transcription pipeline

## Common Issues and Solutions

### FFmpeg Not Found
**Symptoms:**
- "FFmpeg command not found"
- "No such file or directory"
- Pipeline fails at audio extraction

**Solutions:**
- Verify FFmpeg is in system PATH: `which ffmpeg` (Linux/Mac) or `where ffmpeg` (Windows)
- Check FFmpeg installation: `ffmpeg -version`
- Install/reinstall FFmpeg if missing
- Use absolute path in configuration

### Audio Extraction Fails
**Symptoms:**
- Empty or corrupt audio files
- "Invalid data found when processing input"
- Zero-byte output files

**Solutions:**
- Check if video has audio stream: `ffmpeg -i <video> 2>&1 | grep Audio`
- Try different audio codec: Use `-acodec libmp3lame` instead of PCM
- Verify video file isn't corrupted: Play in media player
- Check disk space and permissions

### Memory Issues
**Symptoms:**
- Process killed or crashes
- "Out of memory" errors
- System becomes unresponsive

**Solutions:**
- Process shorter video segments
- Reduce audio quality: Use `-ar 8000` instead of 16000
- Close other applications
- Monitor with `top` or Task Manager

### Codec Compatibility
**Symptoms:**
- "Unknown codec" errors
- "Encoder not found"
- Unsupported format messages

**Solutions:**
- Update FFmpeg to latest version
- Check codec support: `ffmpeg -codecs | grep <codec_name>`
- Use compatible codecs: H.264 for video, AAC for audio
- Re-encode video if necessary

### Encoding Errors
**Symptoms:**
- "Conversion failed" messages
- Corrupted output files
- Mismatched audio/video sync

**Solutions:**
- Specify output format explicitly: `-f wav`
- Use safe encoder options: `-strict -2`
- Check input file integrity
- Try copying stream without re-encoding: `-c copy`

## Advanced Debugging

### Get Detailed Stream Information
```bash
ffprobe -v error -show_streams -show_format <video_file>
```

### Test Specific Stream
```bash
ffmpeg -i <video> -map 0:a:0 output.wav  # Extract first audio stream
ffmpeg -i <video> -map 0:v:0 output.mp4  # Extract first video stream
```

### Enable Verbose Logging
```bash
ffmpeg -v verbose -i <input> <output>
```

## MCP Tool Integration

Use `mcp__videochunking-dev__check_pipeline_health` to verify FFmpeg is properly installed and accessible before debugging.

## Output

This skill provides:
- FFmpeg version and capabilities report
- Complete video file analysis (codecs, streams, metadata)
- Specific error messages with technical context
- Step-by-step recommended fixes
- Command examples for manual testing and validation
- Links to FFmpeg documentation for advanced issues
