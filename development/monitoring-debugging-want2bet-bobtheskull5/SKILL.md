---
name: monitoring-debugging
description: Monitor Bob The Skull operation and debug issues. Use when checking system health, diagnosing problems, analyzing logs, monitoring state transitions, or troubleshooting component failures. Covers web monitor, logs, MQTT, state machine, and performance metrics.
allowed-tools: Read, Bash, Grep
---

# Monitoring & Debugging Skill

Comprehensive guide for monitoring Bob's operation and diagnosing issues quickly.

## When to Use This Skill

- **"Bob isn't responding"** - Diagnose unresponsive system
- **"Wake word not detecting"** - Debug audio input issues
- **"Check system health"** - Monitor operation
- **"Why is Bob stuck in [state]?"** - State machine debugging
- **"Analyze logs"** - Log analysis and interpretation
- **"Monitor performance"** - Check latency and metrics

## Quick Reference

### Monitoring Tools

| Tool | Purpose | Access |
|------|---------|--------|
| **Web Monitor** | Real-time dashboard | http://localhost:5001 (PC)<br>http://192.168.1.44:5001 (Pi) |
| **MQTT Monitor** | Event bus viewer | `python mqtt_monitor.py` |
| **Log Files** | Detailed history | `logs/bob.log` |
| **Config Dashboard** | Settings interface | http://localhost:5001/config |

### Quick Diagnostics

```bash
# Is Bob running?
ps aux | grep -i bob

# Current state
curl -s http://localhost:5001/api/state | jq

# Recent errors
tail -50 logs/bob.log | grep -i error

# Recent events
curl -s http://localhost:5001/api/events | jq '.[-10:]'

# Component health
curl -s http://localhost:5001/api/health | jq
```

## Web Monitor Dashboard

### Accessing the Dashboard

**Local (Development PC):**
```
http://localhost:5001
```

**Remote (Raspberry Pi):**
```
http://192.168.1.44:5001
```

### Dashboard Components

**1. Current State Display**
- Shows current state machine state
- Color-coded: Green (active), Yellow (transitioning), Red (error)
- Timestamp of last state change

**2. Recent Events Feed**
- Last 50 events in reverse chronological order
- Event type, timestamp, details
- Filterable by event type

**3. Component Status**
- Wake Word: Active/Inactive
- STT: Ready/Processing
- LLM: Ready/Processing
- TTS: Ready/Speaking
- Vision: FPS, detections
- Eyes: Connected/Disconnected

**4. Performance Metrics**
- Wake word latency
- STT processing time
- LLM response time
- TTS synthesis time
- Vision frame rate
- Total conversation latency

**5. Configuration Links**
- Direct links to all config pages
- Quick access to settings

### Common Dashboard Patterns

**Normal Operation:**
- State cycles: IDLE → WAKE_LISTENING → GREETING → LISTENING → PROCESSING → SPEAKING → WAKE_LISTENING
- Regular WakeWordDetectedEvent
- Consistent frame rate (5-10 FPS)
- Low error count

**Problem Indicators:**
- State stuck for >30 seconds
- Repeated timeout events
- Error events appearing
- Component status showing "Disconnected"
- Missing expected events

## Log Analysis

### Log File Locations

```bash
# Main application log
logs/bob.log

# Component-specific logs (if configured)
logs/wake_word.log
logs/stt.log
logs/llm.log
logs/tts.log
logs/vision.log
```

### Essential Log Patterns

**Show all errors:**
```bash
grep -i error logs/bob.log
# or
tail -f logs/bob.log | grep --color=always -i error
```

**Show state transitions:**
```bash
grep "State transition" logs/bob.log
# Expected: IDLE -> WAKE_LISTENING -> GREETING -> ...
```

**Show event publications:**
```bash
grep "Publishing event" logs/bob.log
```

**Show component initialization:**
```bash
grep "Initializing" logs/bob.log
# Verify all components loaded
```

**Filter by time range:**
```bash
# Last 100 lines
tail -100 logs/bob.log

# Last hour
grep "$(date '+%Y-%m-%d %H')" logs/bob.log

# Specific timestamp
grep "2024-12-09 15:30" logs/bob.log
```

**Event frequency analysis:**
```bash
# Count events by type
grep "Publishing event" logs/bob.log | awk '{print $5}' | sort | uniq -c | sort -rn

# Output:
#   145 WakeWordDetectedEvent
#    98 SpeechRecognizedEvent
#    87 LLMResponseEvent
#    ...
```

### Log Level Interpretation

```
DEBUG: Detailed diagnostic information (verbose)
INFO: General operational messages (normal)
WARNING: Potentially problematic situations (investigate)
ERROR: Error events (requires attention)
CRITICAL: Severe errors (immediate action)
```

## Common Debugging Scenarios

### Scenario 1: Wake Word Not Detecting

**Symptoms:**
- No response to "Hey Bob" or "Wake up Bob"
- No WakeWordDetectedEvent in logs/web monitor

**Diagnosis:**

```bash
# 1. Check if wake word component is running
grep "wake word" logs/bob.log | tail -5

# 2. Check audio input device
python list_audio_devices.py
# Compare to AUDIO_INPUT_DEVICE_INDEX in .env

# 3. Check microphone is receiving input
# On Pi:
arecord -d 3 test.wav && aplay test.wav
# Should hear your recording

# 4. Check sensitivity setting
grep WAKE_WORD_SENSITIVITY .env
# Default: 0.5 (lower = more sensitive, 0.0-1.0)

# 5. Test with audio injection (if configured)
python test_wake_word_inject.py play --file audio/static/testing/wake_up_bob.mp3
```

**Common Causes:**
- ❌ Wrong audio device index
- ❌ Microphone muted or disconnected
- ❌ Sensitivity too high (0.9-1.0)
- ❌ Wake word model not loaded
- ❌ Picovoice API key invalid

**Solutions:**
```bash
# Fix audio device
# 1. List devices: python list_audio_devices.py
# 2. Update .env: BOBTHESKULL_AUDIO_INPUT_DEVICE_INDEX=X
# 3. Restart Bob

# Lower sensitivity
# Edit .env: BOBTHESKULL_WAKE_WORD_SENSITIVITY=0.3
# Restart Bob

# Verify API key
grep PICOVOICE_ACCESS_KEY .env
# Check at console.picovoice.ai
```

### Scenario 2: State Machine Stuck

**Symptoms:**
- Bob unresponsive
- State hasn't changed in minutes
- Timeouts in logs

**Diagnosis:**

```bash
# 1. Check current state
curl -s http://localhost:5001/api/state | jq
# Look at 'current_state' and 'time_in_state'

# 2. Check recent transitions
grep "State transition" logs/bob.log | tail -10

# 3. Check for timeout events
grep -i timeout logs/bob.log | tail -5

# 4. Check what triggered stuck state
grep "Entering state" logs/bob.log | tail -3
```

**Common Stuck States:**

**PROCESSING (stuck):**
- LLM not responding
- Network timeout
- API rate limit

**SPEAKING (stuck):**
- TTS failed to complete
- Audio output issue
- MPV process hung

**LISTENING (stuck):**
- STT waiting for input that never came
- Microphone stopped working
- Timeout not configured

**Solutions:**

```bash
# Graceful recovery (restart Bob)
# Ctrl+C in terminal or:
pkill -f BobTheSkull.py
python BobTheSkull.py

# Check timeouts are configured
grep TIMEOUT .env
# Ensure STATE_MACHINE_*_TIMEOUT values are set

# For specific stuck states:
# - PROCESSING: Check LLM logs, API key, network
# - SPEAKING: Check audio output device
# - LISTENING: Check STT configuration
```

### Scenario 3: LLM Not Responding

**Symptoms:**
- Bob hears speech but doesn't respond
- Stuck in PROCESSING state
- Timeout after 30+ seconds

**Diagnosis:**

```bash
# 1. Check LLM events in logs
grep -E "LLMRequest|LLMResponse|LLMError" logs/bob.log | tail -10

# 2. Verify API key
grep OPENAI_API_KEY .env
# Should start with sk-

# 3. Test API connectivity
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $(grep OPENAI_API_KEY .env | cut -d= -f2)"
# Should return list of models

# 4. Check for rate limit errors
grep "429" logs/bob.log
# 429 = rate limit exceeded

# 5. Check model configuration
grep LLM_MODEL .env
# Default: gpt-4-turbo
```

**Common Causes:**
- ❌ Invalid or expired API key
- ❌ Rate limit exceeded
- ❌ Network connectivity issues
- ❌ Model not available
- ❌ Request timeout

**Solutions:**

```bash
# Test different model
# Edit .env: BOBTHESKULL_LLM_MODEL=gpt-3.5-turbo
# (Faster, cheaper, might work if rate limited)

# Check API usage
# Visit platform.openai.com/usage

# Verify network
ping api.openai.com

# Check firewall
# Ensure port 443 (HTTPS) is open
```

### Scenario 4: Vision Not Working

**Symptoms:**
- No face detection events
- Vision FPS = 0
- Camera errors in logs

**Diagnosis:**

```bash
# 1. Check if vision is enabled
grep VISION_CAN_SEE .env
# Should be: BOBTHESKULL_VISION_CAN_SEE=true

# 2. Check camera is accessible
ls /dev/video*
# Should see: /dev/video0 (or similar)

# 3. Test camera directly
python test_vision_live.py
# Should open window with camera feed

# 4. Check vision logs
grep -i vision logs/bob.log | tail -20

# 5. Check GPU if using acceleration
grep VISION_ENABLE_GPU .env
python test_gpu_status.py
```

**Common Causes:**
- ❌ Camera not connected
- ❌ Camera in use by another process
- ❌ Vision disabled in config
- ❌ GPU issues (if using acceleration)
- ❌ Missing vision dependencies

**Solutions:**

```bash
# Test camera availability
# Kill other processes using camera:
sudo lsof /dev/video0
# Kill PID if found

# Disable GPU acceleration
# Edit .env: BOBTHESKULL_VISION_ENABLE_GPU=false
# Restart Bob

# Check dependencies
pip list | grep -E "opencv|onnx|dlib"
# Should show installed versions
```

### Scenario 5: Audio Output Not Working

**Symptoms:**
- Bob processes but no speech heard
- TTS completes but silent
- Audio file generates but doesn't play

**Diagnosis:**

```bash
# 1. Check audio output device
python list_audio_devices.py
# Verify OUTPUT device index

# 2. Test audio output directly
python test_audio_output.py
# Should hear test tones

# 3. Check MPV is installed
which mpv  # Linux/Mac
where mpv  # Windows
# Should show path to mpv binary

# 4. Check TTS logs
grep -E "TTS|Speaking" logs/bob.log | tail -10

# 5. Test TTS directly
python test_tts_live.py
```

**Common Causes:**
- ❌ Wrong output device index
- ❌ Speaker muted or disconnected
- ❌ MPV not installed or not in PATH
- ❌ Audio file playback failed
- ❌ Volume set to 0

**Solutions:**

```bash
# Fix output device
# 1. List devices: python list_audio_devices.py
# 2. Update .env: BOBTHESKULL_AUDIO_OUTPUT_DEVICE_INDEX=X
# 3. Restart Bob

# Install MPV
# Linux: sudo apt install mpv
# Mac: brew install mpv
# Windows: Download from mpv.io

# Check volume
# Ensure system volume > 0
# Check Bob's volume config
```

### Scenario 6: High Latency / Slow Response

**Symptoms:**
- Delay between speech and response
- Vision FPS very low
- State transitions taking >10 seconds

**Diagnosis:**

```bash
# 1. Check performance metrics in web monitor
# http://localhost:5001
# Look at component latencies

# 2. Check system resources
top
# Look for high CPU/memory usage

# 3. Check component timings in logs
grep -E "took|duration|latency" logs/bob.log | tail -20

# 4. Check GPU usage (if using vision with GPU)
nvidia-smi  # If NVIDIA GPU
# or
python test_gpu_status.py

# 5. Check network latency
ping api.openai.com
ping api.elevenlabs.io
```

**Common Causes:**
- ❌ Slow network connection
- ❌ GPU not being used (CPU fallback)
- ❌ Resource-heavy operations
- ❌ LLM model too large
- ❌ Multiple heavy components running

**Performance Targets:**
- Wake word: < 500ms
- STT: < 3s
- LLM: < 3s
- TTS: < 2s
- Vision: 5-10 FPS
- Total: < 10s end-to-end

**Solutions:**

```bash
# Use faster LLM model
# Edit .env: BOBTHESKULL_LLM_MODEL=gpt-3.5-turbo

# Enable GPU for vision (if available)
# Edit .env: BOBTHESKULL_VISION_ENABLE_GPU=true

# Reduce vision frame rate
# Edit .env: BOBTHESKULL_VISION_MAX_FRAMES_PER_SECOND=5

# Check network
# Test on local network if possible
# Verify good WiFi signal (Pi)
```

## MQTT Event Bus Monitoring

### Using mqtt_monitor.py

```bash
# Start MQTT monitor
python mqtt_monitor.py

# Output shows real-time events:
# 2024-12-09 15:30:45 | WakeWordDetectedEvent | phrase=wake up bob
# 2024-12-09 15:30:46 | StateTransitionEvent | from=IDLE to=WAKE_LISTENING
# 2024-12-09 15:30:47 | GreetingEvent | greeting=Yes wizard?
# ...
```

### Event Flow Analysis

**Normal conversation flow:**
```
1. WakeWordDetectedEvent (phrase=wake up bob)
2. StateTransitionEvent (IDLE -> WAKE_LISTENING)
3. GreetingEvent (greeting=Yes wizard?)
4. StateTransitionEvent (WAKE_LISTENING -> GREETING)
5. SpeechRecognizedEvent (transcript=What time is it?)
6. StateTransitionEvent (GREETING -> PROCESSING)
7. LLMRequestEvent (input=What time is it?)
8. LLMResponseEvent (response=It's 3:30 PM)
9. StateTransitionEvent (PROCESSING -> SPEAKING)
10. TTSEvent (text=It's 3:30 PM)
11. SpeakingCompleteEvent
12. StateTransitionEvent (SPEAKING -> WAKE_LISTENING)
```

**Problem patterns:**

**Missing events:**
```
WakeWordDetectedEvent
(no StateTransitionEvent) ← Problem: State machine not responding
```

**Repeated events:**
```
WakeWordDetectedEvent
WakeWordDetectedEvent  ← Problem: Audio feedback loop
WakeWordDetectedEvent
```

**Timeout sequence:**
```
StateTransitionEvent (-> LISTENING)
TimeoutEvent (state=LISTENING)  ← Problem: No speech detected
StateTransitionEvent (LISTENING -> ERROR)
```

## State Machine Monitoring

### Valid State Transitions

```
IDLE ──wake_word──> WAKE_LISTENING ──greeting_complete──> GREETING
GREETING ──speech_detected──> LISTENING
LISTENING ──speech_recognized──> PROCESSING
PROCESSING ──llm_response──> SPEAKING
SPEAKING ──speaking_complete──> WAKE_LISTENING
[any] ──error──> ERROR
ERROR ──timeout──> IDLE
```

### State Duration Expectations

| State | Normal Duration | Max Timeout |
|-------|----------------|-------------|
| IDLE | Indefinite | None |
| WAKE_LISTENING | < 1s (greeting) | 5s |
| GREETING | 1-2s (play greeting) | 10s |
| LISTENING | < 5s (speech) | 30s |
| PROCESSING | 2-5s (LLM) | 30s |
| SPEAKING | 2-10s (TTS+playback) | 60s |
| ERROR | < 5s (recovery) | 10s |

### Monitoring State Health

```bash
# Check current state and duration
curl -s http://localhost:5001/api/state | jq '{state: .current_state, duration: .time_in_state}'

# If duration > expected max timeout → investigate

# Check recent transitions
curl -s http://localhost:5001/api/events | jq '.[] | select(.type == "StateTransitionEvent") | {from: .from_state, to: .to_state, time: .timestamp}'

# Verify transitions are valid
# Compare to state machine diagram
```

## Remote Pi Monitoring

### SSH Access

```bash
# Connect to Pi
ssh knarl@192.168.1.44
# Password: peacock7

# Or use plink (Windows)
plink -pw peacock7 knarl@192.168.1.44
```

### Remote Commands

```bash
# Check if Bob is running
ssh knarl@192.168.1.44 "ps aux | grep BobTheSkull"

# View recent logs
ssh knarl@192.168.1.44 "tail -50 /home/knarl/BobTheSkull5/logs/bob.log"

# Check errors
ssh knarl@192.168.1.44 "grep -i error /home/knarl/BobTheSkull5/logs/bob.log | tail -10"

# Restart Bob
ssh knarl@192.168.1.44 "pkill -f BobTheSkull && cd /home/knarl/BobTheSkull5 && nohup python BobTheSkull.py > bob.log 2>&1 &"
```

### Web Monitor from PC

```
http://192.168.1.44:5001
```

**Verify Pi web monitor is accessible:**
```bash
# From PC
curl -s http://192.168.1.44:5001/api/health
```

## Performance Metrics

### Key Metrics to Track

**1. Component Latencies**
- Wake word detection: < 500ms
- STT processing: < 3s
- LLM response: < 3s
- TTS synthesis: < 2s

**2. Vision Performance**
- Frame rate: 5-10 FPS
- Detection rate: Varies by scene
- GPU utilization: 20-40% (if enabled)

**3. Event Bus**
- Event publish rate: ~5-20 events/second
- Event processing latency: < 100ms
- Queue depth: < 10 events

**4. State Machine**
- Transition latency: < 100ms
- State duration: Within expected ranges
- Timeout frequency: < 1% of transitions

### Collecting Metrics

**Via web monitor:**
```
http://localhost:5001
# Shows real-time metrics in dashboard
```

**Via logs:**
```bash
# Extract latency measurements
grep "took" logs/bob.log | awk '{print $NF}' | sort -n

# Count events per minute
grep "Publishing event" logs/bob.log | cut -d' ' -f1-2 | uniq -c

# Average FPS
grep "FPS:" logs/bob.log | awk '{sum+=$NF; count++} END {print sum/count}'
```

## Health Check Procedures

### Startup Health Check

**After starting Bob, verify:**

```bash
# 1. All components initialized
grep "Initializing" logs/bob.log
# Should see: Wake Word, STT, LLM, TTS, Vision (if enabled), Eyes

# 2. No initialization errors
grep -i "initialization.*error" logs/bob.log
# Should be empty

# 3. State machine started
grep "State machine started" logs/bob.log

# 4. Current state is IDLE
curl -s http://localhost:5001/api/state | jq .current_state
# Should show: "IDLE"

# 5. Web monitor accessible
curl -s http://localhost:5001/api/health
# Should return: {"status": "ok"}
```

### Periodic Health Check

**Run every few hours during development:**

```bash
# Check error count
error_count=$(grep -i error logs/bob.log | wc -l)
echo "Errors: $error_count"
# Goal: < 10 errors per hour

# Check state machine is cycling
tail -100 logs/bob.log | grep "State transition" | wc -l
# Should be > 0 if actively used

# Check component status
curl -s http://localhost:5001/api/health | jq
```

## Common Error Messages

### Error: "Device not found"

**Full error:** `PyAudio error: Device X not found`

**Cause:** Audio device index invalid or device disconnected

**Fix:**
```bash
python list_audio_devices.py
# Update .env with correct device index
```

### Error: "API key invalid"

**Full error:** `OpenAI API Error: Invalid API key`

**Cause:** API key expired, revoked, or incorrect

**Fix:**
```bash
# Verify API key format
grep OPENAI_API_KEY .env
# Should start with sk-

# Test key at platform.openai.com
# Generate new key if needed
```

### Error: "Camera not accessible"

**Full error:** `Cannot open camera /dev/video0`

**Cause:** Camera in use, disconnected, or permissions issue

**Fix:**
```bash
# Check camera exists
ls -l /dev/video*

# Check permissions
sudo chmod 666 /dev/video0

# Kill processes using camera
sudo lsof /dev/video0
sudo kill <PID>
```

### Error: "MQTT connection refused"

**Full error:** `MQTT broker connection refused on localhost:1883`

**Cause:** MQTT broker not running

**Fix:**
```bash
# Check if mosquitto is running
systemctl status mosquitto

# Start mosquitto
sudo systemctl start mosquitto

# Or use embedded broker (if configured)
```

## Pro Tips

1. **Keep web monitor open** - Always have http://localhost:5001 open in browser during development

2. **Use screen on Pi** - Run Bob in screen session to prevent SSH disconnects from killing it

3. **Tail logs in separate terminal** - Keep `tail -f logs/bob.log` running in another terminal

4. **Grep with color** - Use `grep --color=always` to highlight matches

5. **Create monitoring aliases** - Add to ~/.bashrc:
   ```bash
   alias bob-log='tail -f logs/bob.log'
   alias bob-errors='grep -i error logs/bob.log | tail -20'
   alias bob-state='curl -s http://localhost:5001/api/state | jq'
   ```

6. **Use jq for JSON** - Install `jq` for pretty-printing API responses

7. **Monitor network** - Use `nethogs` or `iftop` to see network usage

8. **Check timestamps** - Always check event timestamps to understand sequence

9. **Compare working vs broken** - Keep logs from working state to compare

10. **Test incrementally** - Don't change multiple things at once

## Integration with Other Skills

**Works well with:**
- **pi-deployment** - Monitor after deployment to verify success
- **audio-injection-testing** - Monitor events during automated testing
- **config-pattern** - Verify config changes have desired effect

## Time Savings

**Without skill:**
- 15-20 minutes figuring out where to look
- 10-15 minutes trial-and-error debugging
- Missed correlations between components

**With skill:**
- 3-5 minutes following documented scenario
- Quick diagnosis with known patterns
- Clear troubleshooting checklists

**Estimated time savings: 3-4x faster issue resolution**

## References

**Monitoring Tools:**
- [web/monitor_server.py](../../web/monitor_server.py) - Web dashboard
- [mqtt_monitor.py](../../mqtt_monitor.py) - MQTT event viewer
- [test_web_monitor.py](../../test_web_monitor.py) - Monitor testing

**Log Files:**
- `logs/bob.log` - Main application log
- Check `.env` for LOG_LEVEL setting

**API Endpoints:**
- `GET /api/state` - Current state
- `GET /api/events` - Recent events
- `GET /api/health` - Component health

**Related Documentation:**
- [requirements/LoggingandMonitoringRequirements.md](../../requirements/LoggingandMonitoringRequirements.md)
- [CLAUDE.md](../../CLAUDE.md) - Project overview
