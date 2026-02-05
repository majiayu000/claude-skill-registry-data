---
name: transcription-debugger
description: Diagnoses and fixes VoiceLite transcription issues including silent failures, event handling problems, and whisper errors. Activates when transcription isn't working, text doesn't appear, or whisper-related errors occur.
---

# Transcription Debugger

This skill diagnoses the transcription issues that have caused silent failures in v1.0.87-94.

## When This Skill Activates

- "Transcription not working", "no text appears", "whisper not responding"
- "AudioFileReady not firing", "event handler issues"
- Whisper process errors or timeouts
- Users reporting recording works but no text output

## Diagnostic Flow

### Step 1: Check Build Configuration

**Debug vs Release Mode**
```csharp
// Check: ErrorLogger.cs
#if DEBUG
    Console.WriteLine("DEBUG MODE - Full logging enabled");
#else
    // PROBLEM: v1.0.94 bug - logging was suppressed here!
#endif
```

**Critical**: Ensure logging works in Release builds!

### Step 2: Verify Event Chain

**Expected Flow**:
```
User Press Hotkey
    ↓
AudioRecorder.StartRecording()
    ↓
AudioRecorder.StopRecording()
    ↓
AudioFileReady event fires ← COMMON FAILURE POINT
    ↓
PersistentWhisperService.TranscribeAsync()
    ↓
TranscriptionCompleted event fires
    ↓
TextInjector.InjectText()
```

**Check Event Subscription**:
```csharp
// MainWindow.xaml.cs - Verify this exists:
_audioRecorder.AudioFileReady += OnAudioFileReady;

// Common issue: Event not subscribed or handler missing
private async void OnAudioFileReady(object sender, AudioFileReadyEventArgs e)
{
    // v1.0.87 bug: This wasn't being called
    ErrorLogger.Log($"AudioFileReady fired: {e.FilePath}");
}
```

### Step 3: Test Whisper Directly

**Manual Whisper Test**:
```bash
# Create test audio file
echo "Test audio" > test.txt

# Run whisper directly
./VoiceLite/whisper/whisper.exe \
  -m VoiceLite/whisper/ggml-tiny.bin \
  -f test_audio.wav \
  --no-timestamps \
  --language en \
  --temperature 0.2 \
  --beam-size 1

# Expected: Text output within 2 seconds
```

### Step 4: Check Process Lifecycle

**Whisper Process Issues**:
```csharp
// PersistentWhisperService.cs
// Check timeout calculation
var timeout = (int)(audioLength * 3000); // Should be 2-3x audio length

// Verify process disposal
finally
{
    process?.Dispose(); // Must dispose to prevent zombies
}

// Check for hanging processes
tasklist | findstr whisper.exe
```

### Step 5: Verify Model & Files

**Required Files**:
```bash
# Model file exists and correct size
test -f "VoiceLite/whisper/ggml-tiny.bin" || echo "Model missing!"
stat -c%s "VoiceLite/whisper/ggml-tiny.bin" # Should be 44048314 bytes

# Whisper executable present
test -f "VoiceLite/whisper/whisper.exe" || echo "Whisper missing!"

# Check permissions
ls -la VoiceLite/whisper/
```

## Common Issues & Fixes

### Issue 1: Silent Failure (No Error, No Text)
**v1.0.87-90 Bug**: AudioFileReady event not firing

**Fix**:
```csharp
// Ensure event is raised after file write
_audioRecorder.AudioFileReady += OnAudioFileReady; // Subscribe
await File.WriteAllBytesAsync(path, audioData);
AudioFileReady?.Invoke(this, new AudioFileReadyEventArgs(path)); // Raise
```

### Issue 2: Logging Suppressed in Release
**v1.0.94 Bug**: `#if !DEBUG` blocks around logging

**Fix**:
```csharp
// Remove conditional compilation from logging
- #if DEBUG
    ErrorLogger.Log("Important diagnostic info");
- #endif
+ ErrorLogger.Log("Important diagnostic info"); // Always log
```

### Issue 3: Whisper Process Hangs
**Symptom**: Transcription never completes

**Diagnostics**:
```bash
# Check for zombie processes
tasklist | findstr whisper.exe

# Kill if needed
taskkill /F /IM whisper.exe
```

**Fix**:
```csharp
// Add proper timeout handling
if (!process.WaitForExit(timeout))
{
    ErrorLogger.Log($"Whisper timeout after {timeout}ms");
    process.Kill();
    throw new TimeoutException();
}
```

### Issue 4: Wrong Audio Format
**Symptom**: Garbled or empty transcription

**Check**:
```csharp
// AudioRecorder.cs - Must be 16kHz, 16-bit, mono
_waveIn = new WaveInEvent
{
    WaveFormat = new WaveFormat(16000, 16, 1), // Critical!
};
```

## Testing Checklist

1. [ ] Record 5-second test audio
2. [ ] Verify WAV file created in temp directory
3. [ ] Check AudioFileReady event fires
4. [ ] Confirm whisper.exe launches
5. [ ] Verify transcription completes < 3 seconds
6. [ ] Check text appears in target application

## Historical Context

**v1.0.87-90**: AudioFileReady event wasn't firing due to missing event raise
**v1.0.94**: Logging was disabled in Release builds with `#if !DEBUG`
**v1.0.95-96**: Model file missing from installer (different issue)

## Critical Log Patterns

Search VoiceLite logs for diagnostic info:

```bash
# Log location
$log_file = "$env:LOCALAPPDATA\VoiceLite\logs\voicelite.log"

# Check if AudioFileReady is firing
grep "AudioFileReady fired" $log_file

# Check whisper process launch
grep "Starting whisper process" $log_file | tail -5

# Check for timeout errors
grep "Whisper timeout" $log_file

# Check for event subscription
grep "Event subscribed: AudioFileReady" $log_file

# Check transcription completion
grep "Transcription completed" $log_file | tail -5
```

## Test Audio Phrases

Use these phrases to test accuracy (expect 95%+ correct):

**Technical Terms**:
- "npm install react useState useEffect"
- "git commit minus m add new feature"
- "dotnet build configuration release"

**Common Dictation**:
- "Hello world this is a test recording"
- "The quick brown fox jumps over the lazy dog"

**Expected**: All technical terms captured correctly