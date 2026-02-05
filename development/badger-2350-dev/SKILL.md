---
name: micropython-repl
description: MicroPython REPL usage, package management, module inspection, and interactive debugging for Universe 2025 (Tufty) Badge. Use when installing MicroPython packages, testing code interactively, checking installed modules, or using the REPL for development.
---

# MicroPython REPL and Package Management

Master the MicroPython REPL (Read-Eval-Print Loop) for interactive development, package management, and quick testing on the Universe 2025 (Tufty) Badge.

## Connecting to REPL

### Using screen (macOS/Linux)

```bash
# Find the device
ls /dev/tty.usb*

# Connect (115200 baud)
screen /dev/tty.usbmodem* 115200

# Exit screen: Ctrl+A then K, then Y to confirm
```

### Using mpremote

```bash
# Install mpremote
pip install mpremote

# Connect to REPL
mpremote connect /dev/tty.usbmodem*

# Or auto-detect
mpremote
```

### Using Thonny IDE

1. Open Thonny
2. Tools → Options → Interpreter
3. Select "MicroPython (RP2040)"
4. Choose correct port
5. Shell window shows REPL

## REPL Basics

### Special Commands

```python
# Ctrl+C - Interrupt running program
# Ctrl+D - Soft reboot
# Ctrl+E - Enter paste mode (for multi-line code)
# Ctrl+B - Exit paste mode and execute

# Help system
help()              # General help
help(modules)       # List all modules
help(badgeware)     # Help on specific module

# Quick info
import sys
sys.implementation  # MicroPython version
sys.platform        # Platform info
```

### Interactive Testing

```python
# Test code immediately
>>> from badgeware import screen, display, brushes
>>> screen.brush = brushes.color(255, 255, 255)
>>> screen.text("Test", 10, 10, 2)
>>> display.update()

# Test calculations
>>> temp = 23.5
>>> temp_f = temp * 9/5 + 32
>>> print(f"{temp}C = {temp_f}F")

# Test GPIO
>>> from machine import Pin
>>> led = Pin(25, Pin.OUT)
>>> led.toggle()  # Toggle LED immediately
```

### Paste Mode for Multi-line Code

```bash
# Enter paste mode: Ctrl+E
# Paste your code:
def calculate_distance(x1, y1, x2, y2):
    import math
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx*dx + dy*dy)

print(calculate_distance(0, 0, 3, 4))
# Exit paste mode: Ctrl+D
```

## Package Management

### Using mip (MicroPython Package Installer)

```python
# Install package from micropython-lib
import mip
mip.install("urequests")        # HTTP client
mip.install("logging")           # Logging module
mip.install("umqtt.simple")      # MQTT client

# Install from GitHub
mip.install("github:org/repo/package.py")

# Install to specific location
mip.install("urequests", target="/lib")
```

### Using upip (older method)

```python
# Connect to WiFi first
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SSID', 'password')

# Wait for connection
while not wlan.isconnected():
    pass

# Install package
import upip
upip.install("micropython-logging")
upip.install("picoweb")
```

### Manual Package Installation

```bash
# From your computer, copy files to badge
mpremote cp mymodule.py :/lib/mymodule.py

# Or using ampy
ampy --port /dev/tty.usbmodem* put mymodule.py /lib/mymodule.py

# Then use in REPL
>>> import mymodule
```

## Module Inspection

### List Available Modules

```python
# List all built-in and installed modules
help('modules')

# Check if module exists
import sys
'badgeware' in sys.modules  # False until imported

import badgeware
'badgeware' in sys.modules  # True after import
```

### Inspect Module Contents

```python
# See what's in a module
import badgeware
dir(badgeware)  # List all attributes

# Check specific attributes
hasattr(badgeware, 'screen')  # True
hasattr(badgeware, 'brushes')  # True

# Get function signature
help(badgeware.screen)

# Explore submodules
from badgeware import shapes
dir(shapes)  # See all shape functions

# View source (if available)
import inspect
inspect.getsource(mymodule.myfunction)  # May not work on compiled modules
```

### Check Module Location

```python
# Find where module is located
import badgeware
badgeware.__file__  # Shows file path

# List files in system directory
import os
os.listdir('/system')
os.listdir('/system/apps')  # MonaOS apps
```

## Interactive Debugging

### Quick Variable Inspection

```python
# Run code and inspect
>>> x = [1, 2, 3, 4, 5]
>>> len(x)
5
>>> type(x)
<class 'list'>
>>> sum(x)
15

# Object inspection
>>> import badgeware
>>> type(badgeware.screen)
<class 'Screen'>
>>> dir(badgeware.screen)  # See all methods
>>> dir(badgeware.brushes)  # See brush functions
>>> dir(badgeware.shapes)  # See shape functions
```

### Print Debugging

```python
# Test function with prints
def process_data(data):
    print(f"Input: {data}")
    result = data * 2
    print(f"Result: {result}")
    return result

>>> process_data(5)
Input: 5
Result: 10
10
```

### Exception Handling

```python
# Test error handling
>>> try:
...     1 / 0
... except ZeroDivisionError as e:
...     print(f"Error: {e}")
Error: division by zero

# Get full traceback
import sys
try:
    buggy_function()
except Exception as e:
    sys.print_exception(e)
```

### Memory Debugging

```python
# Check memory usage
import gc
gc.collect()  # Run garbage collection
gc.mem_free()  # Free memory in bytes
gc.mem_alloc()  # Allocated memory

# Monitor memory during operation
before = gc.mem_free()
# ... do something
after = gc.mem_free()
print(f"Memory used: {before - after} bytes")
```

## Useful REPL Helpers

### Create a helpers.py file

```python
# helpers.py - Load in REPL for common tasks
import gc
import sys
import os
from machine import Pin, freq

def info():
    """Display system information"""
    print(f"Platform: {sys.platform}")
    print(f"Version: {sys.version}")
    print(f"CPU Frequency: {freq()} Hz")
    print(f"Free Memory: {gc.mem_free()} bytes")

def ls(path='/'):
    """List files in directory"""
    try:
        files = os.listdir(path)
        for f in files:
            print(f)
    except:
        print(f"Error listing {path}")

def cat(filename):
    """Display file contents"""
    try:
        with open(filename, 'r') as f:
            print(f.read())
    except Exception as e:
        print(f"Error: {e}")

def rm(filename):
    """Remove file"""
    try:
        os.remove(filename)
        print(f"Removed {filename}")
    except Exception as e:
        print(f"Error: {e}")

def blink(pin=25, times=3):
    """Blink LED for testing"""
    import time
    led = Pin(pin, Pin.OUT)
    for i in range(times):
        led.toggle()
        time.sleep(0.5)
    led.value(0)

# Load in REPL with:
# >>> from helpers import *
# >>> info()
```

### Auto-run at REPL start

Create `boot.py` to run code on startup:

```python
# boot.py - Runs on every boot
import gc
gc.collect()

# Optional: Auto-import common modules
# from badgeware import screen, display, brushes, shapes
# import time

print("Universe 2025 Badge Ready!")
print(f"Free memory: {gc.mem_free()} bytes")
```

## Quick Testing Workflows

### Test Hardware Function

```python
# Test I2C scan
from machine import I2C, Pin
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
devices = i2c.scan()
print(f"Found devices: {[hex(d) for d in devices]}")

# Test display
from badgeware import screen, display, brushes
screen.brush = brushes.color(0, 0, 0)
screen.clear()
screen.brush = brushes.color(255, 255, 255)
screen.text("REPL Test", 10, 10, 2)
display.update()
```

### Test Network Connection

```python
import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("Connecting to WiFi...")
wlan.connect('YOUR_SSID', 'YOUR_PASSWORD')

timeout = 10
while not wlan.isconnected() and timeout > 0:
    print(".", end="")
    time.sleep(1)
    timeout -= 1

if wlan.isconnected():
    print("\nConnected!")
    print(f"IP: {wlan.ifconfig()[0]}")
else:
    print("\nConnection failed")
```

### Test API Call

```python
import urequests
import json

response = urequests.get('https://api.github.com/zen')
print(response.text)
response.close()

# JSON API
response = urequests.get('https://api.example.com/data')
data = response.json()
print(data)
response.close()
```

## File System Operations

### List and Navigate Files

```python
import os

# Current directory
os.getcwd()

# List files
os.listdir()
os.listdir('/lib')

# File info
os.stat('main.py')  # Returns (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)

# Check if file exists
try:
    os.stat('main.py')
    print("File exists")
except:
    print("File not found")
```

### Read/Write Files

```python
# Write file
with open('test.txt', 'w') as f:
    f.write('Hello from REPL!\n')

# Read file
with open('test.txt', 'r') as f:
    content = f.read()
    print(content)

# Append to file
with open('log.txt', 'a') as f:
    f.write(f'Log entry: {time.time()}\n')
```

### Remove Files

```python
import os

# Remove file
os.remove('test.txt')

# Remove directory (must be empty)
os.rmdir('mydir')
```

## Checking Installed Packages

### Verify Package Installation

```python
# Method 1: Try to import
try:
    import urequests
    print("urequests is installed")
    print(f"Location: {urequests.__file__}")
except ImportError:
    print("urequests not installed")

# Method 2: Check file system
import os
lib_files = os.listdir('/lib')
print("Installed in /lib:")
for f in lib_files:
    print(f"  {f}")

# Method 3: Check sys.path
import sys
print("Module search paths:")
for path in sys.path:
    print(f"  {path}")
```

### Package Version Info

```python
# Some packages have __version__
import urequests
if hasattr(urequests, '__version__'):
    print(f"urequests version: {urequests.__version__}")

# Check MicroPython version
import sys
print(sys.version)
print(sys.implementation)
```

## REPL Tips and Tricks

### History Navigation

- **Up/Down arrows**: Navigate command history
- **Tab**: Auto-completion (limited support)

### Copy Output from REPL

```python
# Run command and capture output
>>> result = []
>>> for i in range(10):
...     result.append(i * 2)
>>> print(result)
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Copy from terminal window
```

### Run Script from REPL

```python
# Import and run
import myapp
myapp.main()

# Or reload after changes
import sys
if 'myapp' in sys.modules:
    del sys.modules['myapp']
import myapp
```

### Timing Code

```python
import time

start = time.ticks_ms()
# ... your code here
for i in range(1000):
    x = i * 2
end = time.ticks_ms()

print(f"Execution time: {time.ticks_diff(end, start)}ms")
```

## Common REPL Issues

**REPL not responding**: Press Ctrl+C to interrupt, or Ctrl+D to soft reset

**Can't import module**: Check `sys.path`, verify file is in `/lib` or root directory

**Out of memory**: Run `gc.collect()`, reduce variable usage, delete large objects

**Module changes not reflected**: Delete from `sys.modules` and re-import

**Connection lost**: Reconnect with screen or mpremote, check USB cable

## Using mpremote for Quick Operations

```bash
# Execute Python code remotely
mpremote exec "import machine; print(machine.freq())"

# Run local script on device
mpremote run test.py

# Copy file to device
mpremote cp test.py :main.py

# Copy file from device
mpremote cp :main.py local.py

# Mount local directory on device
mpremote mount .

# Filesystem operations
mpremote ls
mpremote mkdir /data
mpremote rm test.txt

# Chain commands
mpremote connect /dev/tty.usbmodem* cp main.py :main.py exec "import main"
```

## REPL Best Practices

1. **Save work frequently** - REPL state is lost on reboot
2. **Use paste mode** for multi-line code
3. **Run `gc.collect()`** before memory-intensive operations
4. **Test incrementally** - Build up complex code piece by piece
5. **Create helper functions** in a dedicated module
6. **Use `print()` liberally** for debugging
7. **Soft reset (Ctrl+D)** to clear state between tests
8. **Keep REPL sessions short** - Move working code to files

## Integration with Development Workflow

1. **Prototype in REPL** - Test ideas interactively
2. **Save to file** - Once code works, save to .py file
3. **Test from file** - Import and run from REPL
4. **Iterate** - Make changes, reload, test
5. **Deploy** - Upload final version to badge

The REPL is your best friend for rapid experimentation and debugging on the Badger 2350!
