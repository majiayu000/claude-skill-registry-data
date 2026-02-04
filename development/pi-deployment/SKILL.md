---
name: pi-deployment
description: Handles deployment, testing, and debugging of Bob The Skull code on Raspberry Pi. Use when deploying to Pi, testing remote code, troubleshooting Pi issues, or setting up new Pi hardware.
allowed-tools: Read, Edit, Bash, Glob, Grep
---

# Pi Deployment & Remote Testing Skill

Comprehensive workflow for deploying, testing, and debugging Bob The Skull on Raspberry Pi.

## When to Use This Skill

- **"Deploy to the Pi"** - Full deployment workflow
- **"Push updates to Raspberry Pi"** - Code synchronization
- **"Test on the Pi"** - Remote testing procedures
- **"Pi isn't working"** - Troubleshooting remote issues
- **"Setup new Raspberry Pi"** - Initial Pi configuration
- **"Check Pi logs"** - Remote debugging

## Quick Reference

### Pre-Deployment Checklist

```bash
# 1. Check git status - ensure clean or intentional changes
git status

# 2. Verify critical files exist
- .env.bob (API keys configured)
- requirements-body.txt (Pi dependencies)
- setup_raspberry_pi_no_git.sh (setup script)
- BobTheSkull.py or BobSkullOnly.py (main entry point)

# 3. Test locally if possible (optional but recommended)
./venv/Scripts/python test_system_config.py
```

### Deployment Command

```bash
# Windows: Use deploy_to_pi.bat
cmd /c deploy_to_pi.bat

# The script will:
# 1. Copy Python files (*.py)
# 2. Copy config files (.env.bob, requirements*.txt)
# 3. Copy all component directories (wake_word/, stt/, llm/, tts/, etc.)
# 4. Copy setup scripts
```

### Post-Deployment: SSH Connection

```bash
# Connect to Pi
plink -pw peacock7 knarl@192.168.1.44

# Navigate to deployment directory
cd /home/knarl/BobTheSkull5

# Verify files copied
ls -la
```

### Post-Deployment: Setup on Pi

```bash
# Make setup script executable
chmod +x setup_raspberry_pi_no_git.sh

# Run setup (installs dependencies, creates venv)
./setup_raspberry_pi_no_git.sh

# Setup installs:
# - System packages (python3, portaudio, mosquitto-clients, avahi-daemon)
# - Python venv
# - requirements-body.txt dependencies (excludes heavy vision/GPU packages)
```

### Post-Deployment: Configuration

```bash
# Copy environment file
cp .env.bob .env

# Verify API keys are present
grep -E "OPENAI_API_KEY|PICOVOICE_ACCESS_KEY|ELEVEN_LABS_API_KEY" .env

# Check audio device configuration
python list_audio_devices.py

# Update .env if audio device indices changed
nano .env
# BOBTHESKULL_AUDIO_INPUT_DEVICE_INDEX=X
# BOBTHESKULL_AUDIO_OUTPUT_DEVICE_INDEX=Y
```

### Running on Pi

```bash
# Activate virtual environment
source venv/bin/activate

# Run Bob (body mode - no vision)
python BobTheSkull.py

# Or run in background with logging
nohup python BobTheSkull.py > bob.log 2>&1 &

# Monitor logs in real-time
tail -f bob.log

# Or use screen for persistent session
screen -S bob
python BobTheSkull.py
# Detach: Ctrl+A then D
# Reattach: screen -r bob
```

## Deployment Workflow (Step-by-Step)

### Step 1: Pre-Deployment Preparation

**Check what will be deployed:**
```bash
# Review git status
git status

# Check for uncommitted changes to critical files
git diff BobConfig.py
git diff BobTheSkull.py
git diff .env.bob
```

**Verify configuration files:**
```bash
# Ensure .env.bob has valid API keys
cat .env.bob | grep -E "API_KEY|ACCESS_KEY"

# Ensure deployment mode is correct
grep "DEPLOYMENT_MODE" .env.bob
# Should show: BOBTHESKULL_DEPLOYMENT_MODE=bob
```

### Step 2: Deploy Files

**Run deployment script:**
```bash
# Windows
cmd /c deploy_to_pi.bat

# Expected output:
# [1/4] Creating directory on Pi...
# [2/4] Copying Python files...
# [3/4] Copying configuration files...
# [4/4] Copying component directories...
# Deployment Complete!
```

**What gets copied:**
- **Python files**: All `*.py` in root
- **Config files**: `.env.bob`, `requirements*.txt`, setup scripts
- **Component directories**: `events/`, `wake_word/`, `stt/`, `llm/`, `tts/`, `state_machine/`, `vision/`, `hardware/`, `web/`

**What does NOT get copied:**
- `venv/` - Virtual environment (recreated on Pi)
- `.git/` - Git repository
- `__pycache__/` - Python cache
- `logs/` - Old log files
- `EmbeddingsDB/`, `LongTermDB/` - Databases

### Step 3: Connect to Pi

**SSH Connection:**
```bash
# Connect via plink (PuTTY)
plink -pw peacock7 knarl@192.168.1.44

# Or use WSL/Git Bash
ssh knarl@192.168.1.44
# Password: peacock7
```

**Network Info:**
- Pi IP: 192.168.1.44
- User: knarl
- Password: peacock7
- Hostname: bob-pi.local (mDNS)

### Step 4: Setup Environment on Pi

**First-time setup (or after major changes):**
```bash
cd /home/knarl/BobTheSkull5

# Make setup script executable
chmod +x setup_raspberry_pi_no_git.sh

# Run setup (5-10 minutes)
./setup_raspberry_pi_no_git.sh
```

**What setup does:**
1. Updates system packages (`apt update && apt upgrade`)
2. Installs system dependencies (Python, PortAudio, MQTT, mDNS)
3. Creates Python virtual environment
4. Installs Python packages from `requirements-body.txt`
5. Enables Avahi daemon for mDNS discovery

**Setup complete when you see:**
```
=========================================
Setup Complete!
=========================================

Next steps:
1. Copy .env.body to .env and update with your PC's IP address
2. Add your Picovoice API key to .env
3. Run: source venv/bin/activate
4. Run: python BobSkullOnly.py --broker <YOUR_PC_IP>
```

### Step 5: Configure Audio Devices

**List available audio devices:**
```bash
python list_audio_devices.py
```

**Example output:**
```
Input Devices:
  [0] Built-in Microphone
  [4] PS3 Eye Camera (USB Mic)

Output Devices:
  [2] Built-in Speaker
  [3] USB Audio Device
```

**Update .env with correct indices:**
```bash
nano .env

# Set to your device indices
BOBTHESKULL_AUDIO_INPUT_DEVICE_INDEX=4
BOBTHESKULL_AUDIO_OUTPUT_DEVICE_INDEX=3
```

### Step 6: Test Components

**Test audio output:**
```bash
# Test speaker/audio output
python test_audio_output.py
# Should hear test tones
```

**Test wake word detection:**
```bash
# Test microphone and wake word
python test_wake_word_live.py
# Say "Wake up Bob" or "Hey Bob"
# Should see detection events
```

**Test MQTT connection (if using distributed mode):**
```bash
# Test MQTT broker connection
python test_mqtt.py
# Should connect to localhost:1883
```

### Step 7: Run Bob

**Standard run:**
```bash
source venv/bin/activate
python BobTheSkull.py
```

**Background run with logging:**
```bash
nohup python BobTheSkull.py > bob.log 2>&1 &

# Monitor logs
tail -f bob.log

# Stop background process
pkill -f BobTheSkull.py
```

**Using screen (recommended for long-term):**
```bash
# Start screen session
screen -S bob
python BobTheSkull.py

# Detach from screen: Ctrl+A then D
# Reattach to screen: screen -r bob
# Kill screen: Ctrl+C then exit
```

## Testing Strategies

### Component-by-Component Testing

**Test in this order to isolate issues:**

1. **Audio Output**
   ```bash
   python test_audio_output.py
   ```
   Verifies: Speaker/audio device working

2. **Audio Input**
   ```bash
   python test_wake_word_live.py
   ```
   Verifies: Microphone working, wake word detection

3. **MQTT/EventBus**
   ```bash
   python test_mqtt.py
   ```
   Verifies: Event bus communication

4. **Web Monitor**
   ```bash
   python test_web_monitor.py
   # Open browser: http://192.168.1.44:5001
   ```
   Verifies: Web interface accessible

5. **Full System**
   ```bash
   python BobTheSkull.py
   ```
   Verifies: Complete integration

### Remote Debugging via Web Monitor

**Access from Windows PC:**
```
http://192.168.1.44:5001
```

**Monitor dashboard shows:**
- Current state machine state
- Recent events
- Component status
- System metrics
- Real-time logs

## Common Errors & Troubleshooting

### Error: "pscp not found"

**Problem**: PuTTY not installed or not in PATH

**Solution**:
```bash
# Option 1: Install PuTTY
# Download from: https://www.putty.org/

# Option 2: Use WSL/Git Bash instead
scp -r *.py knarl@192.168.1.44:/home/knarl/BobTheSkull5/
```

### Error: "Connection refused" when deploying

**Problem**: Pi is offline or IP address changed

**Solution**:
```bash
# Ping to verify Pi is online
ping 192.168.1.44

# Try mDNS hostname
ping bob-pi.local

# If IP changed, update deploy_to_pi.bat:
# set PI_HOST=<NEW_IP>
```

### Error: "PortAudio not found" on Pi

**Problem**: System dependencies not installed

**Solution**:
```bash
# SSH to Pi
plink -pw peacock7 knarl@192.168.1.44

# Install PortAudio manually
sudo apt update
sudo apt install -y portaudio19-dev python3-pyaudio

# Recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-body.txt
```

### Error: "No module named 'pvporcupine'"

**Problem**: Wrong requirements file used or venv not activated

**Solution**:
```bash
# Ensure using requirements-body.txt (not requirements.txt)
source venv/bin/activate
pip install -r requirements-body.txt

# Verify pvporcupine installed
pip list | grep pvporcupine
```

### Error: Audio device index invalid

**Problem**: Device indices changed or incorrect

**Solution**:
```bash
# List current audio devices
python list_audio_devices.py

# Update .env with correct indices
nano .env
# Change BOBTHESKULL_AUDIO_INPUT_DEVICE_INDEX
# Change BOBTHESKULL_AUDIO_OUTPUT_DEVICE_INDEX

# Test audio
python test_audio_output.py
```

### Error: "Permission denied" for serial port

**Problem**: User not in dialout group

**Solution**:
```bash
# Add user to dialout group
sudo usermod -a -G dialout knarl

# Logout and login again (or reboot)
sudo reboot
```

### Error: Wake word not detecting

**Problem**: Microphone not working or sensitivity too low

**Solution**:
```bash
# 1. Verify microphone
python list_audio_devices.py
# Ensure correct input device index

# 2. Test microphone recording
arecord -d 5 -f cd test.wav
aplay test.wav
# Should hear your recording

# 3. Adjust wake word sensitivity
nano .env
# BOBTHESKULL_WAKE_WORD_SENSITIVITY=0.3  # Lower = more sensitive (0.0-1.0)

# 4. Test wake word
python test_wake_word_live.py
```

### Error: MQTT connection failed

**Problem**: MQTT broker not running or wrong config

**Solution**:
```bash
# Check if mosquitto is running
sudo systemctl status mosquitto

# Start mosquitto if not running
sudo systemctl start mosquitto
sudo systemctl enable mosquitto

# Verify MQTT config in .env
grep MQTT .env
# Should show:
# BOBTHESKULL_MQTT_BROKER_HOST=localhost
# BOBTHESKULL_MQTT_BROKER_PORT=1883
```

### Error: Eyes controller not found

**Problem**: Eyes controller offline or discovery failed

**Solution**:
```bash
# Test mDNS discovery
python test_mdns_discovery.py

# Try serial discovery
ls /dev/ttyUSB*
# If serial device exists: /dev/ttyUSB0

# Update .env to force serial mode
nano .env
# BOBTHESKULL_EYES_DISCOVERY_MODE=serial
# BOBTHESKULL_EYES_SERIAL_PORT=/dev/ttyUSB0
```

### Slow performance on Pi

**Problem**: Pi CPU limited or wrong Python version

**Solution**:
```bash
# Check CPU usage
top
# Look for high CPU processes

# Verify Python version (should be 3.9-3.11)
python3 --version

# Ensure using body requirements (no vision overhead)
pip list | grep -E "opencv|onnx|dlib"
# Should NOT be installed in body mode

# Consider disabling wake word processing on Pi
# Use distributed architecture with vision PC doing wake word
```

## Remote Log Monitoring

### View logs from Windows

**Option 1: SSH and tail**
```bash
plink -pw peacock7 knarl@192.168.1.44 "tail -f /home/knarl/BobTheSkull5/bob.log"
```

**Option 2: Web Monitor**
```
http://192.168.1.44:5001/logs
```

### Log file locations on Pi

```bash
# Main application log
~/BobTheSkull5/bob.log

# System logs (if running as service)
/var/log/syslog | grep bob

# MQTT logs
/var/log/mosquitto/mosquitto.log
```

### Useful log filtering

```bash
# Show errors only
tail -f bob.log | grep -i error

# Show state transitions
tail -f bob.log | grep "State transition"

# Show event publications
tail -f bob.log | grep "Publishing event"

# Show LLM interactions
tail -f bob.log | grep "LLM"
```

## Deployment Modes

### Body Mode (Raspberry Pi)

**Configuration** (`.env.bob`):
```bash
BOBTHESKULL_DEPLOYMENT_MODE=bob
BOBTHESKULL_VISION_CAN_SEE=false
BOBTHESKULL_WAKE_WORD_ENABLED=true
BOBTHESKULL_MQTT_BROKER_HOST=localhost
```

**Components enabled**:
- ✅ Wake Word Detection
- ✅ Speech-to-Text (STT)
- ✅ Language Processing (LLM)
- ✅ Text-to-Speech (TTS)
- ✅ State Machine
- ✅ Eyes Controller
- ✅ Web Monitor
- ❌ Vision System (disabled)

**Use when**: Running standalone Bob on Pi without vision PC

### Distributed Mode (Future)

**Vision PC runs:**
- Vision system
- MQTT broker

**Raspberry Pi runs:**
- Wake word, STT, LLM, TTS, Eyes
- Connects to vision PC's MQTT broker

**Configuration** (`.env` on Pi):
```bash
BOBTHESKULL_MQTT_BROKER_HOST=192.168.1.XXX  # Vision PC IP
```

## Pro Tips

1. **Use screen for persistence** - Prevents SSH disconnects from stopping Bob
   ```bash
   screen -S bob
   python BobTheSkull.py
   # Ctrl+A D to detach
   ```

2. **Create deployment aliases** - Add to `~/.bashrc` on Pi:
   ```bash
   alias bob-run='cd ~/BobTheSkull5 && source venv/bin/activate && python BobTheSkull.py'
   alias bob-log='tail -f ~/BobTheSkull5/bob.log'
   alias bob-stop='pkill -f BobTheSkull.py'
   ```

3. **Monitor from Windows** - Keep web monitor open during deployment:
   ```
   http://192.168.1.44:5001
   ```

4. **Test incrementally** - Don't deploy everything at once:
   - Deploy → Test audio → Deploy → Test wake word → Deploy → Test full system

5. **Keep backup .env** - Copy working `.env` before changing:
   ```bash
   cp .env .env.backup
   ```

6. **Use version tags** - Tag working versions in git:
   ```bash
   git tag -a pi-working-2024-12-09 -m "Working Pi deployment"
   ```

7. **Automated health checks** - Run periodic tests:
   ```bash
   # On Pi, add to crontab
   */5 * * * * /home/knarl/BobTheSkull5/health_check.sh
   ```

8. **Remote file editing** - Use nano on Pi, VS Code Remote SSH, or WinSCP

9. **Quick config changes** - Use web interface instead of editing files:
   ```
   http://192.168.1.44:5001/config
   ```

10. **Network discovery** - Use mDNS instead of IP addresses:
    ```bash
    ping bob-pi.local
    ssh knarl@bob-pi.local
    ```

## Common Workflows

### Workflow: Quick Bug Fix Deployment

```bash
# 1. Fix bug locally on Windows
# 2. Test locally (if possible)
./venv/Scripts/python test_system_config.py

# 3. Deploy single file (faster than full deploy)
pscp -pw peacock7 BobConfig.py knarl@192.168.1.44:/home/knarl/BobTheSkull5/

# 4. Restart Bob on Pi
plink -pw peacock7 knarl@192.168.1.44 "pkill -f BobTheSkull.py"
plink -pw peacock7 knarl@192.168.1.44 "cd ~/BobTheSkull5 && nohup python BobTheSkull.py > bob.log 2>&1 &"

# 5. Monitor logs
plink -pw peacock7 knarl@192.168.1.44 "tail -f ~/BobTheSkull5/bob.log"
```

### Workflow: Configuration Change

```bash
# Option 1: Use web interface (fastest)
# Open: http://192.168.1.44:5001/config
# Make changes via UI
# Click Save

# Option 2: Edit .env remotely
plink -pw peacock7 knarl@192.168.1.44
nano /home/knarl/BobTheSkull5/.env
# Make changes
# Ctrl+X, Y, Enter
exit

# Restart Bob
plink -pw peacock7 knarl@192.168.1.44 "pkill -f BobTheSkull.py && cd ~/BobTheSkull5 && nohup python BobTheSkull.py > bob.log 2>&1 &"
```

### Workflow: Fresh Pi Setup

```bash
# 1. Deploy files from Windows
cmd /c deploy_to_pi.bat

# 2. SSH to Pi
plink -pw peacock7 knarl@192.168.1.44

# 3. Run full setup
cd /home/knarl/BobTheSkull5
chmod +x setup_raspberry_pi_no_git.sh
./setup_raspberry_pi_no_git.sh

# 4. Configure environment
cp .env.bob .env
nano .env
# Update audio device indices

# 5. Test audio
python list_audio_devices.py
python test_audio_output.py

# 6. Run Bob
screen -S bob
python BobTheSkull.py
# Ctrl+A D to detach
```

### Workflow: Debugging Remote Issues

```bash
# 1. Check if Bob is running
plink -pw peacock7 knarl@192.168.1.44 "ps aux | grep BobTheSkull"

# 2. Check recent logs
plink -pw peacock7 knarl@192.168.1.44 "tail -100 ~/BobTheSkull5/bob.log"

# 3. Check for errors
plink -pw peacock7 knarl@192.168.1.44 "grep -i error ~/BobTheSkull5/bob.log | tail -20"

# 4. Open web monitor in browser
# http://192.168.1.44:5001

# 5. If needed, run tests remotely
plink -pw peacock7 knarl@192.168.1.44 "cd ~/BobTheSkull5 && source venv/bin/activate && python test_mqtt.py"
```

## Time Savings

**Without this skill:**
- 30-45 minutes per deploy (forgotten steps, troubleshooting, trial-and-error)
- 15-20 minutes debugging common errors
- Frequent deployment failures requiring rework

**With this skill:**
- 10-15 minutes per deploy (documented workflow)
- 5 minutes resolving common errors (troubleshooting guide)
- Higher success rate on first attempt

**Estimated time savings: 2-3x faster deployments**

## Integration with Other Skills

**Works well with:**
- **cross-repo-sync** - When deploying files from BobFast5 (audio files)
- **config-pattern** - Testing new config parameters on Pi
- **event-flow** - Verifying event handling in distributed MQTT architecture

## Common Mistakes to Avoid

1. ❌ **Deploying without testing locally first**
   - Always test locally when possible before deploying

2. ❌ **Forgetting to update .env on Pi**
   - Always verify `.env` after deployment

3. ❌ **Using wrong requirements file**
   - Pi should use `requirements-body.txt`, not `requirements.txt`

4. ❌ **Not checking audio device indices**
   - Indices can change, always verify with `list_audio_devices.py`

5. ❌ **Deploying with hardcoded paths**
   - Use relative paths or environment variables

6. ❌ **Not monitoring logs during first run**
   - Always tail logs during initial deployment

7. ❌ **Forgetting to enable avahi-daemon**
   - mDNS discovery requires avahi running

8. ❌ **Running full requirements.txt on Pi**
   - Installs unnecessary vision/GPU packages (slower, more disk space)

9. ❌ **Not using screen/nohup for background runs**
   - SSH disconnect will kill Bob

10. ❌ **Skipping component-by-component testing**
    - Test audio → wake word → full system incrementally

## References

**Deployment Scripts:**
- [deploy_to_pi.bat](../../deploy_to_pi.bat) - Windows deployment script
- [setup_raspberry_pi_no_git.sh](../../setup_raspberry_pi_no_git.sh) - Pi setup script
- [.env.bob](../../.env.bob) - Body mode configuration template

**Test Scripts:**
- `test_audio_output.py` - Test speaker
- `test_wake_word_live.py` - Test microphone and wake word
- `test_mqtt.py` - Test MQTT connection
- `test_web_monitor.py` - Test web interface
- `list_audio_devices.py` - List audio devices

**Configuration Files:**
- [BobConfig.py](../../BobConfig.py) - Default configuration
- `.env` - Environment-specific overrides (on Pi)
- `config.yaml` - Optional YAML configuration

**Related Documentation:**
- [CLAUDE.md](../../CLAUDE.md) - Project overview
- [requirements/DeploymentRequirements.md](../../requirements/DeploymentRequirements.md) - Deployment specs
