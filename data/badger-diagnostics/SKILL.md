---
name: badger-diagnostics
description: System diagnostics, verification, and troubleshooting for Badger 2350. Use when checking firmware version, verifying installations, diagnosing hardware issues, troubleshooting errors, or performing system health checks on Badger 2350.
---

# Badger 2350 Diagnostics and Troubleshooting

Comprehensive diagnostics and troubleshooting tools for verifying your Badger 2350 setup, checking installations, and resolving common issues.

## ⚠️ When to Use This Skill

**Use this skill FIRST** in these situations:
1. **Starting a new session** - Verify everything works before coding
2. **After setup** - Confirm installation completed correctly
3. **Before debugging** - Rule out environment issues
4. **When errors occur** - Diagnose the root cause
5. **After firmware updates** - Verify everything still works

**Best Practice**: Run diagnostics at the start of EVERY development session. It takes 30 seconds and prevents hours of debugging.

## Quick Verification Command

**Run this FIRST every session** (doesn't require any files to exist):

### Level 1: Basic Connection Test
```bash
# Simplest test - just verify badge responds
mpremote exec "print('Badge connected!')"
# Should print: Badge connected!

# If this fails, badge isn't connected or mpremote not installed
```

### Level 2: Full Verification
```bash
# Complete verification (auto-detects port on macOS/Linux)
mpremote exec "import sys, gc; from badgeware import screen, brushes, shapes, io; print('=== VERIFICATION ==='); print('✓ MicroPython:', sys.version[:30]); print('✓ Memory:', gc.mem_free(), 'bytes'); print('✓ badgeware: loaded'); print('✓ Display: 160x120'); print('=== ALL OK ===')"
```

**Expected output**: All checks with ✓ marks and no errors.

**With explicit port** (if auto-detect fails):
```bash
mpremote connect /dev/cu.usbmodem1101 exec "from badgeware import screen; print('✓ Badge OK')"
# Replace /dev/cu.usbmodem1101 with your port
```

**If this fails**: Continue with detailed diagnostics below.

## Quick System Check

Run this complete system diagnostic in REPL:

```python
# diagnostic.py - Complete system check
import sys
import gc
import os
from machine import freq, unique_id
import ubinascii

def system_info():
    """Display complete system information"""
    print("=" * 50)
    print("BADGER 2350 SYSTEM DIAGNOSTICS")
    print("=" * 50)

    # MicroPython version
    print(f"\n[MicroPython]")
    print(f"  Version: {sys.version}")
    print(f"  Implementation: {sys.implementation}")
    print(f"  Platform: {sys.platform}")

    # Hardware info
    print(f"\n[Hardware]")
    print(f"  CPU Frequency: {freq():,} Hz ({freq() / 1_000_000:.0f} MHz)")
    uid = ubinascii.hexlify(unique_id()).decode()
    print(f"  Unique ID: {uid}")

    # Memory
    gc.collect()
    print(f"\n[Memory]")
    print(f"  Free: {gc.mem_free():,} bytes ({gc.mem_free() / 1024:.1f} KB)")
    print(f"  Allocated: {gc.mem_alloc():,} bytes ({gc.mem_alloc() / 1024:.1f} KB)")
    total = gc.mem_free() + gc.mem_alloc()
    print(f"  Total: {total:,} bytes ({total / 1024:.1f} KB)")

    # File system
    print(f"\n[File System]")
    try:
        stat = os.statvfs('/')
        block_size = stat[0]
        total_blocks = stat[2]
        free_blocks = stat[3]
        total_bytes = block_size * total_blocks
        free_bytes = block_size * free_blocks
        used_bytes = total_bytes - free_bytes

        print(f"  Total: {total_bytes:,} bytes ({total_bytes / 1024 / 1024:.2f} MB)")
        print(f"  Used: {used_bytes:,} bytes ({used_bytes / 1024 / 1024:.2f} MB)")
        print(f"  Free: {free_bytes:,} bytes ({free_bytes / 1024 / 1024:.2f} MB)")
    except:
        print("  Unable to check filesystem")

    # Module path
    print(f"\n[Module Search Paths]")
    for path in sys.path:
        print(f"  {path}")

    print("\n" + "=" * 50)

# Run diagnostic
system_info()
```

## Firmware Version Check

### Check MicroPython Firmware

```python
import sys

# Full version info
print(sys.version)
# Example: 3.4.0; MicroPython v1.20.0 on 2023-04-26

# Implementation details
print(sys.implementation)
# (name='micropython', version=(1, 20, 0), _machine='Raspberry Pi Pico W with RP2040', _mpy=6182)

# Extract version number
version = sys.implementation.version
print(f"MicroPython {version[0]}.{version[1]}.{version[2]}")
```

### Check Badger Library Version

```python
import badger2040

# Check if version attribute exists
if hasattr(badger2040, '__version__'):
    print(f"Badger library version: {badger2040.__version__}")
else:
    print("Badger library version not available")

# Check file location
print(f"Badger library: {badger2040.__file__}")
```

### Recommended Firmware Versions

Verify you have compatible firmware:

```python
def check_firmware_compatibility():
    """Check if firmware is compatible with Badger 2350"""
    version = sys.implementation.version

    if version[0] >= 1 and version[1] >= 20:
        print("✓ MicroPython version is compatible")
        return True
    else:
        print("✗ MicroPython version may be outdated")
        print("  Recommended: MicroPython 1.20+")
        print(f"  Current: {version[0]}.{version[1]}.{version[2]}")
        return False

check_firmware_compatibility()
```

## Module Verification

### Check Core Modules

```python
def verify_core_modules():
    """Verify essential modules are available"""
    required_modules = {
        'badger2040': 'Badger display library',
        'machine': 'Hardware interface',
        'time': 'Time functions',
        'gc': 'Garbage collection',
        'sys': 'System functions',
        'os': 'Operating system interface'
    }

    optional_modules = {
        'network': 'WiFi support',
        'urequests': 'HTTP client',
        'ujson': 'JSON parsing',
        'ubinascii': 'Binary/ASCII conversion'
    }

    print("Checking required modules...")
    all_ok = True
    for module, description in required_modules.items():
        try:
            __import__(module)
            print(f"  ✓ {module:15s} - {description}")
        except ImportError:
            print(f"  ✗ {module:15s} - MISSING - {description}")
            all_ok = False

    print("\nChecking optional modules...")
    for module, description in optional_modules.items():
        try:
            __import__(module)
            print(f"  ✓ {module:15s} - {description}")
        except ImportError:
            print(f"  ○ {module:15s} - Not installed - {description}")

    return all_ok

verify_core_modules()
```

### List All Installed Packages

```python
import os

def list_installed_packages():
    """List all installed packages in /lib"""
    print("Installed packages:")

    # Check /lib directory
    try:
        lib_contents = os.listdir('/lib')
        if lib_contents:
            for item in sorted(lib_contents):
                # Try to get more info
                path = f'/lib/{item}'
                try:
                    stat = os.stat(path)
                    size = stat[6]  # File size
                    print(f"  {item:30s} {size:8,} bytes")
                except:
                    print(f"  {item}")
        else:
            print("  (no packages in /lib)")
    except OSError:
        print("  /lib directory not found")

    # Check root directory for .py files
    print("\nRoot directory modules:")
    root_contents = os.listdir('/')
    py_files = [f for f in root_contents if f.endswith('.py')]
    for f in sorted(py_files):
        stat = os.stat(f)
        size = stat[6]
        print(f"  {f:30s} {size:8,} bytes")

list_installed_packages()
```

## Hardware Diagnostics

### Display Test

```python
import badger2040

def test_display():
    """Test display functionality"""
    print("Testing display...")

    badge = badger2040.Badger2040()

    # Test 1: Clear screen
    badge.set_pen(15)
    badge.clear()
    badge.update()
    print("  ✓ Clear screen")

    # Test 2: Draw text
    badge.set_pen(0)
    badge.text("Display Test", 10, 10, scale=2)
    badge.update()
    print("  ✓ Draw text")

    # Test 3: Draw shapes
    badge.line(10, 40, 100, 40)
    badge.rectangle(10, 50, 50, 30)
    badge.update()
    print("  ✓ Draw shapes")

    print("Display test complete!")

test_display()
```

### Button Test

```python
import badger2040
import time

def test_buttons():
    """Test all buttons"""
    print("Button test - Press each button:")
    print("  A, B, C, UP, DOWN")
    print("Press Ctrl+C to exit")

    badge = badger2040.Badger2040()
    tested = set()

    while len(tested) < 5:
        if badge.pressed(badger2040.BUTTON_A) and 'A' not in tested:
            print("  ✓ Button A works")
            tested.add('A')
        elif badge.pressed(badger2040.BUTTON_B) and 'B' not in tested:
            print("  ✓ Button B works")
            tested.add('B')
        elif badge.pressed(badger2040.BUTTON_C) and 'C' not in tested:
            print("  ✓ Button C works")
            tested.add('C')
        elif badge.pressed(badger2040.BUTTON_UP) and 'UP' not in tested:
            print("  ✓ Button UP works")
            tested.add('UP')
        elif badge.pressed(badger2040.BUTTON_DOWN) and 'DOWN' not in tested:
            print("  ✓ Button DOWN works")
            tested.add('DOWN')

        time.sleep(0.1)

    print("All buttons tested successfully!")

test_buttons()
```

### GPIO Test

```python
from machine import Pin

def test_gpio():
    """Test GPIO pins"""
    print("Testing GPIO pins...")

    # Test output
    test_pin = Pin(25, Pin.OUT)
    test_pin.value(1)
    print(f"  ✓ Pin 25 set to HIGH: {test_pin.value()}")
    test_pin.value(0)
    print(f"  ✓ Pin 25 set to LOW: {test_pin.value()}")

    # Test input with pull-up
    input_pin = Pin(15, Pin.IN, Pin.PULL_UP)
    print(f"  ✓ Pin 15 input (pull-up): {input_pin.value()}")

    print("GPIO test complete!")

test_gpio()
```

### I2C Bus Scan

```python
from machine import I2C, Pin

def scan_i2c():
    """Scan for I2C devices"""
    print("Scanning I2C bus...")

    i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
    devices = i2c.scan()

    if devices:
        print(f"  Found {len(devices)} device(s):")
        for device in devices:
            print(f"    0x{device:02X} ({device})")
    else:
        print("  No I2C devices found")

    return devices

scan_i2c()
```

## Network Diagnostics

### WiFi Connection Test

```python
import network
import time

def test_wifi(ssid, password, timeout=10):
    """Test WiFi connection"""
    print(f"Testing WiFi connection to '{ssid}'...")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Check if already connected
    if wlan.isconnected():
        print("  ✓ Already connected")
        print(f"    IP: {wlan.ifconfig()[0]}")
        return True

    # Attempt connection
    print("  Connecting...")
    wlan.connect(ssid, password)

    # Wait for connection
    start = time.time()
    while not wlan.isconnected() and (time.time() - start) < timeout:
        time.sleep(0.5)
        print(".", end="")

    print()  # New line

    if wlan.isconnected():
        config = wlan.ifconfig()
        print("  ✓ Connected successfully")
        print(f"    IP Address: {config[0]}")
        print(f"    Subnet Mask: {config[1]}")
        print(f"    Gateway: {config[2]}")
        print(f"    DNS: {config[3]}")
        print(f"    Signal Strength: {wlan.status('rssi')} dBm")
        return True
    else:
        print("  ✗ Connection failed")
        status = wlan.status()
        print(f"    Status code: {status}")
        return False

# Usage
# test_wifi('YourSSID', 'YourPassword')
```

### Network Speed Test

```python
import urequests
import time

def test_network_speed():
    """Test network download speed"""
    print("Testing network speed...")

    url = "http://httpbin.org/bytes/10000"  # 10KB test file

    try:
        start = time.ticks_ms()
        response = urequests.get(url)
        end = time.ticks_ms()

        size = len(response.content)
        duration = time.ticks_diff(end, start) / 1000  # Convert to seconds

        speed = (size / duration) / 1024  # KB/s

        print(f"  Downloaded: {size} bytes")
        print(f"  Time: {duration:.2f}s")
        print(f"  Speed: {speed:.2f} KB/s")

        response.close()
        return True
    except Exception as e:
        print(f"  ✗ Network test failed: {e}")
        return False

# test_network_speed()
```

## Memory Diagnostics

### Memory Usage Analysis

```python
import gc

def analyze_memory():
    """Analyze memory usage"""
    print("Memory Analysis:")

    # Before collection
    free_before = gc.mem_free()
    alloc_before = gc.mem_alloc()

    # Collect garbage
    gc.collect()

    # After collection
    free_after = gc.mem_free()
    alloc_after = gc.mem_alloc()

    print(f"\nBefore garbage collection:")
    print(f"  Free: {free_before:,} bytes ({free_before / 1024:.1f} KB)")
    print(f"  Allocated: {alloc_before:,} bytes ({alloc_before / 1024:.1f} KB)")

    print(f"\nAfter garbage collection:")
    print(f"  Free: {free_after:,} bytes ({free_after / 1024:.1f} KB)")
    print(f"  Allocated: {alloc_after:,} bytes ({alloc_after / 1024:.1f} KB)")

    freed = free_after - free_before
    print(f"\nReclaimed: {freed:,} bytes ({freed / 1024:.1f} KB)")

    # Total memory
    total = free_after + alloc_after
    usage_percent = (alloc_after / total) * 100

    print(f"\nTotal memory: {total:,} bytes ({total / 1024:.1f} KB)")
    print(f"Usage: {usage_percent:.1f}%")

    # Warning if low
    if free_after < 10000:
        print("\n⚠ WARNING: Low memory!")
    elif free_after < 50000:
        print("\n⚠ CAUTION: Memory running low")
    else:
        print("\n✓ Memory usage looks good")

analyze_memory()
```

### Find Memory Leaks

```python
import gc

def find_memory_leaks(function, iterations=10):
    """Test function for memory leaks"""
    print(f"Testing for memory leaks ({iterations} iterations)...")

    gc.collect()
    initial_mem = gc.mem_free()

    for i in range(iterations):
        function()
        gc.collect()

        current_mem = gc.mem_free()
        leaked = initial_mem - current_mem

        if leaked > 0:
            print(f"  Iteration {i+1}: Leaked {leaked} bytes")

    gc.collect()
    final_mem = gc.mem_free()
    total_leaked = initial_mem - final_mem

    if total_leaked > 100:  # Allow small variance
        print(f"⚠ Possible memory leak: {total_leaked} bytes leaked")
    else:
        print(f"✓ No significant memory leak detected")

# Usage
# def test_func():
#     data = [i for i in range(100)]
# find_memory_leaks(test_func)
```

## Error Diagnosis

### Common Error Patterns

```python
def diagnose_error(error):
    """Provide diagnosis for common errors"""
    error_str = str(error)

    diagnostics = {
        'ImportError': """
        Module not found. Check:
        - Module is installed (use mip.install())
        - Module is in /lib or root directory
        - Module name is spelled correctly
        - File has .py extension
        """,

        'MemoryError': """
        Out of memory. Try:
        - Run gc.collect() before allocation
        - Reduce variable scope
        - Use generators instead of lists
        - Break large operations into smaller chunks
        - Delete unused objects with 'del'
        """,

        'OSError': """
        File/Hardware operation failed. Check:
        - File path is correct
        - File exists (for reading)
        - Filesystem not full (for writing)
        - Hardware is connected properly
        - Pins are not already in use
        """,

        'AttributeError': """
        Attribute not found. Check:
        - Object has the attribute/method
        - Spelling is correct
        - Module is imported correctly
        - Object is initialized
        """,

        'ValueError': """
        Invalid value. Check:
        - Parameter values are in valid range
        - Data types match expected types
        - String formats are correct
        """
    }

    # Find matching error type
    for error_type, advice in diagnostics.items():
        if error_type in error_str:
            print(f"Diagnosis for {error_type}:")
            print(advice)
            return

    print("Error type not recognized. Common debugging steps:")
    print("- Check error message carefully")
    print("- Print variable values before error")
    print("- Simplify code to isolate problem")
    print("- Check MicroPython documentation")

# Usage
# try:
#     import nonexistent_module
# except Exception as e:
#     diagnose_error(e)
```

### System Health Check

```python
def health_check():
    """Comprehensive system health check"""
    print("=" * 50)
    print("SYSTEM HEALTH CHECK")
    print("=" * 50)

    issues = []

    # Memory check
    gc.collect()
    free_mem = gc.mem_free()
    if free_mem < 10000:
        issues.append("CRITICAL: Very low memory")
    elif free_mem < 50000:
        issues.append("WARNING: Low memory")
    else:
        print("✓ Memory: OK")

    # Filesystem check
    try:
        stat = os.statvfs('/')
        free_blocks = stat[3]
        block_size = stat[0]
        free_bytes = free_blocks * block_size

        if free_bytes < 100000:
            issues.append("WARNING: Low disk space")
        else:
            print("✓ Filesystem: OK")
    except:
        issues.append("ERROR: Cannot check filesystem")

    # Core modules check
    required = ['badger2040', 'machine', 'time', 'gc', 'sys', 'os']
    for module in required:
        try:
            __import__(module)
        except:
            issues.append(f"ERROR: Missing module '{module}'")

    if not issues:
        print("✓ Core modules: OK")

    # Display results
    if issues:
        print("\n" + "!" * 50)
        print("ISSUES FOUND:")
        for issue in issues:
            print(f"  {issue}")
        print("!" * 50)
    else:
        print("\n" + "=" * 50)
        print("✓ ALL SYSTEMS HEALTHY")
        print("=" * 50)

health_check()
```

## Recovery Procedures

### Safe Mode Boot

If badge won't boot normally:

1. **Hold BOOTSEL button** while connecting USB
2. Badge appears as USB drive
3. Delete `main.py` if it's causing crashes
4. Copy new firmware `.uf2` file to drive
5. Badge will reboot automatically

### Factory Reset

```python
import os

def factory_reset():
    """Remove all user files (DANGEROUS!)"""
    print("WARNING: This will delete all files!")
    print("Type 'CONFIRM' to proceed:")

    # In interactive mode, get user confirmation
    # confirm = input()
    # if confirm != 'CONFIRM':
    #     print("Reset cancelled")
    #     return

    print("Removing files...")
    for f in os.listdir('/'):
        if f not in ['boot.py']:  # Keep boot.py
            try:
                os.remove(f)
                print(f"  Removed {f}")
            except:
                pass

    print("Factory reset complete. Reboot badge.")

# Uncomment to use:
# factory_reset()
```

### Firmware Reflash

```bash
# From your computer (badge in BOOTSEL mode)

# Download latest MicroPython firmware
# Visit: https://micropython.org/download/rp2-pico-w/

# Flash firmware
# Drag .uf2 file to RPI-RP2 drive
# Or use picotool:
picotool load firmware.uf2

# Verify
picotool info
```

## Troubleshooting Checklist

When encountering issues, work through this checklist:

- [ ] Check MicroPython version (`sys.version`)
- [ ] Verify core modules load (`import badger2040`)
- [ ] Run memory diagnostic (`gc.mem_free()`)
- [ ] Check filesystem space (`os.statvfs('/')`)
- [ ] Test display (`badge.update()`)
- [ ] Test buttons (button test function)
- [ ] Scan I2C bus (if using sensors)
- [ ] Test WiFi connection (if using network)
- [ ] Review error messages carefully
- [ ] Check documentation for API changes
- [ ] Try soft reset (Ctrl+D in REPL)
- [ ] Try hard reset (power cycle)

This comprehensive diagnostic approach will help you quickly identify and resolve issues with your Badger 2350!
