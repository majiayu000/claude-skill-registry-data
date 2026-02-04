---
name: badger-quickstart
description: Complete getting started guide for Universe 2025 (Tufty) Badge from zero to first app. Use when helping absolute beginners, providing step-by-step first-time setup, or when users ask "how do I get started", "where do I begin", or "first steps with the badge".
---

# Universe 2025 (Tufty) Badge Quickstart Guide

Complete step-by-step guide to go from zero to creating your first app for **MonaOS** on the Universe 2025 (Tufty) Badge. Perfect for absolute beginners!

## About the Badge

The Universe 2025 Badge is a custom version of the Pimoroni Tufty 2350, created for GitHub Universe 2025. It comes pre-loaded with **MonaOS**, a MicroPython-based operating system with an app launcher.

### Hardware Specifications
- **RP2350** Dual-core ARM Cortex-M33 @ 200MHz
- **512kB SRAM** and **16MB QSPI XiP flash**
- **320x240 full colour IPS display** (framebuffer pixel doubled from 160x120)
- **2.4GHz WiFi and Bluetooth 5**
- **1000mAh rechargeable battery** (up to 8 hours runtime)
- **IR receiver and transmitter** for beacon hunting
- **Five front-facing buttons** (A, B, C, UP, DOWN)
- **4-zone LED backlight**
- **USB-C** for charging and programming

## About MonaOS

Your badge runs **MonaOS**, which provides:
- An app launcher that auto-discovers apps in `/system/apps/`
- Each app is a directory containing `__init__.py`, `icon.png` (24x24), and optional `assets/`
- Apps implement `update()` function called every frame
- Navigate apps using physical buttons

## What You'll Need

### Hardware
- ✓ Universe 2025 (Tufty) Badge
- ✓ USB-C cable (data capable, not just charging)
- ✓ Computer (macOS, Linux, or Windows)

### Software (we'll install together)
- Python 3.8 or newer
- Development tools (mpremote)
- Text editor or IDE

### Time Required
- First-time setup: 30-45 minutes
- Your first app: 20-30 minutes

## Step-by-Step Setup

### Step 1: Install Python on Your Computer

**Why**: You need Python on your computer to run the tools that communicate with your badge.

**macOS:**
```bash
# Install using Homebrew
brew install python3

# Verify
python3 --version  # Should show 3.8 or higher
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

**Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✓ CHECK "Add Python to PATH"
4. Complete installation
5. Open PowerShell and verify: `python --version`

✅ **Checkpoint**: Run `python3 --version` (or `python --version` on Windows). You should see version 3.8 or higher.

> **Need help?** See the `python-setup` skill for detailed installation guides.

### Step 2: Create Your First Project

**Why**: Keeping projects organized and using virtual environments prevents conflicts.

```bash
# Create a directory for your project
mkdir ~/badger-projects
cd ~/badger-projects
mkdir hello-badge
cd hello-badge

# Create a virtual environment
python3 -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Windows (Command Prompt):
venv\Scripts\activate.bat
```

✅ **Checkpoint**: Your terminal prompt should now show `(venv)` at the beginning.

### Step 3: Install Badge Tools

**Why**: These tools let you communicate with your badge, upload files, and run code.

```bash
# Make sure venv is activated (you should see "(venv)" in prompt)

# Install essential tool
pip install mpremote

# Verify installation
mpremote --version
```

✅ **Checkpoint**: Command should show version number without errors.

### Step 4: Connect Your Badge

**Why**: Let's make sure your computer can talk to your badge.

1. **Connect badge to computer** using USB-C cable
2. **Find the device**:

**macOS/Linux:**
```bash
ls /dev/tty.usb*
# Should see something like: /dev/tty.usbmodem14201
```

**Windows:**
```powershell
# In PowerShell
[System.IO.Ports.SerialPort]::getportnames()
# Should see something like: COM3
```

3. **Test connection**:

**macOS/Linux:**
```bash
mpremote connect /dev/tty.usbmodem* exec "print('Hello from Badge!')"
```

**Windows:**
```powershell
mpremote connect COM3 exec "print('Hello from Badge!')"
```

✅ **Checkpoint**: You should see "Hello from Badge!" printed in your terminal.

> **Troubleshooting**:
> - Badge not found? Try different USB ports
> - Permission denied? See Step 4a below
> - Still stuck? See the `badger-diagnostics` skill

### Step 4a: Fix Permissions (Linux only)

If you get "Permission denied" on Linux:

```bash
# Add yourself to dialout group
sudo usermod -a -G dialout $USER

# Log out and log back in for changes to take effect
# Or restart your computer
```

### Step 5: Verify Badge is Ready (CRITICAL)

**Why**: We must verify everything is working before writing code.

```bash
# macOS/Linux:
mpremote connect /dev/tty.usbmodem* exec "
import sys
print('✓ MicroPython:', sys.version)

# Test badgeware module
from badgeware import screen, brushes, shapes
print('✓ badgeware module: loaded')
print('✓ Display size: 160x120')
print('✓ ALL CHECKS PASSED!')
"

# Windows:
mpremote connect COM3 exec "import sys; from badgeware import screen, brushes, shapes; print('✓ MicroPython:', sys.version); print('✓ badgeware loaded'); print('✓ ALL CHECKS PASSED!')"
```

✅ **Checkpoint - ALL must pass**:
- ✓ MicroPython version shown
- ✓ badgeware module loads
- ✓ No error messages

**DO NOT PROCEED until all checks pass.**

### Step 6: Understand MonaOS App Structure

MonaOS apps must follow this structure:

```
my_app/
├── icon.png          # 24x24 PNG icon for launcher
├── __init__.py       # Entry point with update() function
└── assets/          # Optional: app assets (auto-added to path)
    └── ...
```

Your `__init__.py` must implement:
- **`init()`** - Optional, called once when app launches
- **`update()`** - Required, called every frame by MonaOS
- **`on_exit()`** - Optional, called when returning to menu

### Step 7: Create Your First App

Create the app directory structure:

```bash
mkdir hello_app
cd hello_app
```

Create `hello_app/__init__.py`:

```python
# hello_app/__init__.py - Your first MonaOS app!
from badgeware import screen, brushes, shapes, io, PixelFont
import math

# Optional: called once when app launches
def init():
    screen.font = PixelFont.load("nope.ppf")
    print("Hello app initialized!")

# Required: called every frame by MonaOS
def update():
    # Clear the framebuffer
    screen.brush = brushes.color(20, 40, 60)
    screen.clear()

    # Draw animated sine wave
    y = (math.sin(io.ticks / 100) * 20) + 60
    screen.brush = brushes.color(0, 255, 0)
    for x in range(160):
        screen.draw(shapes.rectangle(x, int(y), 1, 1))

    # Draw text
    screen.brush = brushes.color(255, 255, 255)
    screen.text("Hello, Badge!", 10, 10)
    screen.text("Press HOME to exit", 10, 100)

    # Handle button presses
    if io.BUTTON_A in io.pressed:
        print("Button A pressed!")
    if io.BUTTON_HOME in io.pressed:
        # HOME button exits to MonaOS menu automatically
        pass

# Optional: called before returning to menu
def on_exit():
    print("App exiting!")
```

Create `hello_app/icon.png`:
- 24x24 pixel PNG image
- Use any image editor to create a simple icon
- Or download a free icon and resize it

✅ **Checkpoint**: Files created:
- `hello_app/__init__.py`
- `hello_app/icon.png` (24x24 PNG)

### Step 8: Test Your App Locally

```bash
# From your project directory (not inside hello_app/)
cd ~/badger-projects/hello-badge

# Run the app temporarily (doesn't save to badge)
# macOS/Linux:
mpremote connect /dev/tty.usbmodem* run hello_app/__init__.py

# Windows:
mpremote connect COM3 run hello_app/__init__.py
```

✅ **Checkpoint**: Your badge display should show "Hello, Badge!" with an animated wave. Press HOME to exit.

### Step 9: Install Your App to MonaOS

**Why**: Install it permanently so it appears in the MonaOS launcher menu!

**⚠️ IMPORTANT**: The `/system/apps/` directory is READ-ONLY via mpremote. You MUST use USB Mass Storage Mode.

#### Enter USB Mass Storage Mode

1. **Connect badge** via USB-C (if not already connected)
2. **Press RESET button TWICE** quickly (double-click the RESET button on the back)
3. **Wait 2-3 seconds** - Badge will appear as **"BADGER"** drive
4. **Verify**: Drive should appear in Finder (macOS), File Explorer (Windows), or file manager (Linux)

#### Install Your App

**macOS/Linux:**
```bash
# Copy your entire app directory to the badge
cp -r hello_app /Volumes/BADGER/apps/

# OR manually via Finder:
# 1. Open BADGER drive in Finder
# 2. Navigate to apps/ folder
# 3. Drag hello_app folder into apps/
```

**Windows:**
```powershell
# Copy your entire app directory
# (Replace D: with your actual BADGER drive letter)
xcopy hello_app D:\apps\hello_app\ /E /I

# OR manually via File Explorer:
# 1. Open BADGER drive
# 2. Navigate to apps\ folder
# 3. Drag hello_app folder into apps\
```

#### Exit Mass Storage Mode

**macOS:**
```bash
# Eject the drive
diskutil eject /Volumes/BADGER

# Or right-click BADGER in Finder → Eject
```

**Windows:**
- Right-click BADGER drive → "Eject"
- Or use "Safely Remove Hardware" in system tray

**Linux:**
```bash
# Eject the drive
sudo umount /media/$USER/BADGER
```

**All Platforms:**
- Press **RESET button once** on the badge
- Badge reboots into MonaOS with your app installed!

✅ **Checkpoint**:
- BADGER drive was successfully ejected
- Badge reboots normally (you see MonaOS menu)

### Step 10: Launch Your App from the Badge

1. **On your badge**: Press HOME if needed to return to MonaOS launcher
2. **Navigate**: Use UP/DOWN buttons to find your app
3. **Launch**: Press the select button to run your app!

**Note**: The default MonaOS menu shows 6 apps. You may need to expand pagination (see https://badger.github.io/hack/menu-pagination/)

🎉 **Congratulations!** Your first MonaOS app is installed and running!

## 🎉 Congratulations!

You just:
- ✓ Set up your Python development environment
- ✓ Installed badge communication tools
- ✓ Connected to your badge
- ✓ Created your first MonaOS app with proper structure
- ✓ Installed your app into MonaOS launcher
- ✓ Launched your custom app from the badge!

## Quick Reference Card

Save these commands - you'll use them a lot:

```bash
# Activate your virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\Activate.ps1 # Windows

# Test app temporarily (doesn't save)
mpremote run my_app/__init__.py

# Install app to MonaOS launcher (USB Mass Storage Mode REQUIRED)
# 1. Press RESET button twice on badge (enters Mass Storage Mode)
# 2. Copy app to badge:
cp -r my_app /Volumes/BADGER/apps/           # macOS/Linux
xcopy my_app D:\apps\my_app\ /E /I          # Windows
# 3. Eject BADGER drive safely
# 4. Press RESET once to reboot

# List files (read-only view)
mpremote ls /system/apps

# Connect to REPL (interactive mode)
mpremote
# (Ctrl+C to interrupt, Ctrl+D to soft reset, Ctrl+X to exit)
```

**⚠️ Remember**: You CANNOT use `mpremote` to install apps to `/system/apps/` - it's read-only! Always use USB Mass Storage Mode.

## Your First Improvements

### 1. Add Button Interactions

```python
def update():
    screen.brush = brushes.color(20, 40, 60)
    screen.clear()

    screen.brush = brushes.color(255, 255, 255)

    if io.BUTTON_A in io.held:
        screen.text("Button A held!", 10, 50)
    elif io.BUTTON_B in io.pressed:
        screen.text("Button B pressed!", 10, 50)
    elif io.BUTTON_C in io.released:
        screen.text("Button C released!", 10, 50)
```

### 2. Draw Shapes

```python
def update():
    screen.brush = brushes.color(20, 40, 60)
    screen.clear()

    # Draw a circle
    screen.brush = brushes.color(255, 0, 0)
    screen.draw(shapes.circle(80, 60, 30))

    # Draw a rectangle
    screen.brush = brushes.color(0, 255, 0)
    screen.draw(shapes.rectangle(10, 10, 50, 30))

    # Draw a line
    screen.brush = brushes.color(255, 255, 255)
    screen.draw(shapes.line(0, 0, 160, 120))
```

### 3. Create a Counter

```python
# Add at top level
counter = 0

def update():
    global counter

    screen.brush = brushes.color(0, 0, 0)
    screen.clear()

    screen.brush = brushes.color(255, 255, 255)
    screen.text(f"Count: {counter}", 30, 50)

    if io.BUTTON_A in io.pressed:
        counter += 1
    if io.BUTTON_B in io.pressed:
        counter = 0
```

## Common Beginner Questions

### Q: Do I need to activate venv every time?

**Yes**, activate it each time you open a new terminal.

### Q: What if I make a mistake in my code?

Edit locally, test with mpremote, then reinstall via Mass Storage Mode:
```bash
# 1. Edit your code locally
# 2. Test it temporarily
mpremote run my_app/__init__.py

# 3. Reinstall via Mass Storage Mode
# - Press RESET twice (enters Mass Storage Mode)
# - Replace files in /Volumes/BADGER/apps/my_app/
# - Eject and press RESET once
```

### Q: Can I edit code directly on the badge?

Yes! Enter USB Mass Storage Mode (press RESET twice). Badge appears as "BADGER" disk. Edit files in `/Volumes/BADGER/apps/` using any text editor.

### Q: What if my badge freezes?

Press the RESET button on the back of the badge.

### Q: How do I see errors?

Connect to REPL:
```bash
mpremote
```
Then test importing: `import my_app`. Errors will show in terminal.

### Q: How do I remove an app?

```bash
mpremote rm -rf :/system/apps/my_app
```

### Q: My app doesn't appear in the menu?

The default menu shows 6 apps. Expand pagination: https://badger.github.io/hack/menu-pagination/

## Troubleshooting Common Issues

### Badge not detected

1. Check USB cable (must be data cable, not just charging)
2. Try different USB port
3. Restart badge (press RESET)
4. Check connection:
   - **macOS/Linux**: `ls /dev/tty.usb*`
   - **Windows**: Check Device Manager

### "Permission denied" error

**Linux**: Add yourself to dialout group (see Step 4a)
**Windows**: Run PowerShell as Administrator

### "Module not found" error

Activate your virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\Activate.ps1 # Windows
```

### App doesn't appear in MonaOS menu

1. Verify upload: `mpremote ls /system/apps/my_app`
2. Check files exist: `__init__.py` and `icon.png`
3. Icon must be 24x24 PNG
4. May need to expand menu pagination

## Next Steps

### Learn More About App Development
→ See `badger-app-creator` skill
- Advanced button handling
- Working with sprites and images
- WiFi integration
- State management and persistence

### Connect Hardware
→ See `badger-hardware` skill
- GPIO pins and sensors
- I2C/SPI devices
- IR transmitter/receiver
- LED backlight control

### Use the REPL
→ See `micropython-repl` skill
- Interactive development
- Quick testing
- Install packages

### Improve Your Workflow
→ See `badger-deploy` skill
- Automated deployment scripts
- Project organization
- Multi-file apps

## Official Resources

- **Getting Started**: https://badger.github.io/get-started/
- **Hacks & Tutorials**: https://badger.github.io/hacks/
- **Official Apps**: https://badger.github.io/apps/
- **Source Code**: https://github.com/badger/home/tree/main/badgerware
- **API Docs**: https://github.com/badger/home/blob/main/badgerware/

## You're Ready!

You now have everything you need to create amazing projects with your Universe 2025 Badge. Happy coding! 🦡
