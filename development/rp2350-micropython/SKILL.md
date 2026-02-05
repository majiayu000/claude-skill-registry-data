---
name: rp2350-micropython
description: Expert RP2350 development with MicroPython, covering Pimoroni Presto hardware, touchscreen interfaces, RGB lighting control, BLE server implementation, and display rendering. Use when developing for RP2350 boards, implementing touch UI, managing BLE communication, or working with RGB backlights.
---

# RP2350/Pimoroni Presto MicroPython Development

## Overview

This skill provides comprehensive guidance for developing embedded applications on RP2350-based hardware (particularly the Pimoroni Presto) using MicroPython. It covers hardware interfaces, async programming patterns, memory-efficient display rendering, BLE server implementation, MQTT communication, and ADHD-friendly UI design.

## When to Use This Skill

Use this skill when:

- Developing for RP2350 or Pimoroni Presto boards
- Implementing touchscreen interfaces with gesture detection
- Creating BLE GATT servers for peripheral role
- Building MQTT clients for IoT communication
- Controlling RGB backlights with PWM and animations
- Rendering graphics on memory-constrained displays
- Implementing async/concurrent task patterns
- Designing ADHD-friendly visual interfaces
- Managing WiFi connectivity with auto-reconnect
- Optimizing memory usage for framebuffer operations

## Hardware Context

The Pimoroni Presto is an RP2350-based development board featuring:

- **Processor**: Dual ARM Cortex-M33 @ 150MHz with 520KB RAM
- **Display**: 480×480 IPS touchscreen (typically ST7789 controller)
- **Touch**: Capacitive touch (CST816S or FT6236)
- **RGB Backlight**: PWM-controlled 3-channel LED
- **Connectivity**: BLE built-in, WiFi via external module (board-dependent)
- **Memory**: 4MB flash, 520KB SRAM (limited for full framebuffers)

## Core Capabilities

### 1. Touch Input Handling

Use `scripts/touch_handler.py` for debounced touch polling and gesture detection.

**Key Classes:**
- `TouchHandler`: Debounced touch polling with TOUCH_DOWN, TOUCH_UP, TOUCH_DRAG events
- `TouchEvent`: Event objects with coordinates and timestamps
- `GestureDetector`: Swipe and tap gesture recognition

**Usage:**
```python
from touch_handler import TouchHandler, GestureDetector

touch = TouchHandler(touch_device, debounce_ms=50)
gesture = GestureDetector(min_swipe_distance=50)

while True:
    event = touch.poll()
    if event:
        if event.type == TouchHandler.TOUCH_DOWN:
            gesture.start(event.x, event.y)
        elif event.type == TouchHandler.TOUCH_UP:
            detected = gesture.end(event.x, event.y)
            if detected == GestureDetector.SWIPE_LEFT:
                handle_swipe_left()
```

### 2. BLE GATT Server

Use `scripts/ble_gatt_server.py` for peripheral role with custom services.

**Key Classes:**
- `BLETimerServer`: Complete BLE server with timer and battery services
- Pre-defined UUIDs for timer state, control, and battery level
- Connection management and automatic re-advertising

**Usage:**
```python
from ble_gatt_server import BLETimerServer, TIMER_CMD_START, TIMER_CMD_PAUSE

ble = BLETimerServer("Presto-Timer")
ble.start_advertising()

while True:
    # Update clients with current state
    ble.update_timer_state(remaining_seconds=300, is_running=True)

    # Check for commands from clients
    command = ble.get_command()
    if command == TIMER_CMD_START:
        start_timer()
    elif command == TIMER_CMD_PAUSE:
        pause_timer()
```

### 3. MQTT Communication

Use `scripts/mqtt_client.py` for reliable MQTT with auto-reconnect.

**Key Classes:**
- `ReliableMQTTClient`: MQTT client with auto-reconnect and offline queuing
- `WiFiManager`: WiFi connection manager with signal strength monitoring

**Usage:**
```python
from mqtt_client import ReliableMQTTClient, WiFiManager

def message_callback(topic, msg):
    print(f"Received: {topic} -> {msg}")

# Connect WiFi
wifi = WiFiManager("SSID", "password", hostname="presto-001")
wifi.connect()

# Setup MQTT
mqtt = ReliableMQTTClient(
    client_id="presto-001",
    broker="192.168.1.100",
    callback=message_callback
)

mqtt.connect()
mqtt.subscribe("productivity/timer/control/#")

while True:
    mqtt.publish("productivity/status", "online")
    mqtt.check_msg()  # Non-blocking message check
    time.sleep(1)
```

### 4. RGB Backlight Control

Use `scripts/rgb_backlight.py` for PWM-based color control with animations.

**Key Classes:**
- `RGBBacklight`: PWM-based RGB control with color transitions
- `PresetColors`: ADHD-friendly color constants
- Methods for fading, pulsing, rainbow cycling, and urgency gradients

**Usage:**
```python
from rgb_backlight import RGBBacklight, PresetColors

rgb = RGBBacklight(red_pin=16, green_pin=17, blue_pin=18)

# Instant color change
rgb.set_color(255, 0, 0)  # Red

# Smooth fade
rgb.fade_to(0, 255, 0, duration_ms=1000)  # Fade to green

# Pulse effect
rgb.pulse(PresetColors.FOCUS_BLUE, period_ms=2000, iterations=5)

# Urgency gradient (timer countdown)
r, g, b = rgb.urgency_gradient(remaining_seconds=300, total_seconds=1500)
rgb.fade_to(r, g, b, duration_ms=500)
```

## Development Workflow

### Step 1: Hardware Initialization

Refer to `references/presto_hardware.md` for complete pin configurations and initialization sequences.

**Critical Considerations:**
- Verify GPIO pin assignments for your specific board (check schematic)
- SPI clock speed: Use maximum 62.5MHz for ST7789 displays
- I2C frequency: 400kHz for touch controllers
- PWM frequency: 1000Hz typical for RGB backlight

**Example Initialization:**
```python
from machine import Pin, SPI, I2C, PWM

# Display SPI
spi = SPI(1, baudrate=62_500_000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11))
dc = Pin(8, Pin.OUT)
cs = Pin(9, Pin.OUT)
rst = Pin(12, Pin.OUT)

# Touch I2C
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)

# RGB Backlight PWM
rgb_r = PWM(Pin(16))
rgb_g = PWM(Pin(17))
rgb_b = PWM(Pin(18))

rgb_r.freq(1000)
rgb_g.freq(1000)
rgb_b.freq(1000)
```

### Step 2: Implement Async Architecture

For responsive applications with multiple concurrent tasks, use asyncio patterns from `references/micropython_async.md`.

**Typical Task Structure:**
- **UI Task**: Poll touch input every 10ms, handle gestures
- **Timer Task**: Countdown logic every 1 second
- **BLE Sync Task**: Update BLE clients every 500ms
- **MQTT Task**: Check messages every 100ms, reconnect if needed
- **Display Task**: Update display every 100ms (10 FPS)
- **Backlight Task**: Update RGB based on state every 5 seconds

**Example Async Application:**
```python
import asyncio
from touch_handler import TouchHandler
from ble_gatt_server import BLETimerServer
from mqtt_client import ReliableMQTTClient, WiFiManager
from rgb_backlight import RGBBacklight

async def touch_task(touch, state):
    while True:
        event = touch.poll()
        if event and event.type == TouchHandler.TOUCH_DOWN:
            state.toggle()
        await asyncio.sleep_ms(10)

async def ble_task(ble, state):
    while True:
        ble.update_timer_state(state.remaining, state.running)
        command = ble.get_command()
        if command is not None:
            state.handle_command(command)
        await asyncio.sleep_ms(500)

async def backlight_task(rgb, state):
    while True:
        if state.running:
            r, g, b = rgb.urgency_gradient(state.remaining, state.total)
            rgb.fade_to(r, g, b, duration_ms=500)
        await asyncio.sleep(5)

async def main():
    # Initialize hardware
    touch = TouchHandler(touch_device)
    ble = BLETimerServer("Presto")
    rgb = RGBBacklight(16, 17, 18)
    state = AppState()

    ble.start_advertising()

    # Run all tasks concurrently
    await asyncio.gather(
        touch_task(touch, state),
        ble_task(ble, state),
        backlight_task(rgb, state)
    )

asyncio.run(main())
```

### Step 3: Optimize Display Rendering

**Critical Memory Constraint:**
A full 480×480 RGB565 framebuffer requires ~460KB, nearly exhausting available RAM.

**Solutions (choose based on UI complexity):**

**Option 1: Tile-Based Rendering** (for complex full-screen graphics)
- Render display in 60×60 tiles (~7KB per tile)
- Update one tile at a time
- See `TiledDisplay` class in `references/display_rendering.md`

**Option 2: Partial Updates** (for simple UIs with distinct regions)
- Create small buffers for specific UI elements
- Timer display: 100×100 buffer
- Status bar: 200×30 buffer
- Only update changed regions
- See `PartialUpdateDisplay` in `references/display_rendering.md`

**Option 3: Reduced Color Depth** (for minimal graphics)
- Use 1-bit monochrome for simple timer displays
- Use 8-bit grayscale (10× less memory than RGB565)

Refer to `references/display_rendering.md` for complete implementation details, drawing primitives, and animation techniques.

### Step 4: Implement ADHD-Friendly UI

Follow these principles when designing the interface:

**Visual Hierarchy:**
- Large, simple elements (big touch targets)
- High contrast colors (white on black, vivid colors)
- Minimal clutter (one primary action per screen)

**Color Coding:**
- **Idle**: Gray `(64, 64, 64)` - low intensity
- **Focus**: Blue `(30, 144, 255)` - calm, engaging
- **Break**: Green `(50, 205, 50)` - restful
- **Urgent**: Red `(220, 20, 60)` - attention-grabbing
- **Paused**: Amber `(255, 191, 0)` - intermediate state

Use the `PresetColors` class from `rgb_backlight.py` for consistency.

**Progressive Disclosure:**
- Default view: Large timer digits, minimal information
- Tap to expand: Show progress bar, stats, controls
- Gestures for quick actions: Swipe to pause, double-tap to reset

**Smooth Transitions:**
- Always fade between colors (300-500ms duration)
- Use easing functions for animations
- Avoid jarring changes that break hyperfocus

## Common Patterns

### Pattern: Timer Countdown with Visual Feedback

Combine timer logic, BLE sync, and RGB backlight:

```python
class TimerState:
    def __init__(self, duration_seconds):
        self.total = duration_seconds
        self.remaining = duration_seconds
        self.running = False

async def timer_countdown(state):
    while True:
        if state.running and state.remaining > 0:
            state.remaining -= 1
        await asyncio.sleep(1)

async def visual_feedback(state, rgb):
    while True:
        if state.running:
            r, g, b = rgb.urgency_gradient(state.remaining, state.total)
            rgb.fade_to(r, g, b, duration_ms=500)
        await asyncio.sleep(5)

async def ble_sync(state, ble):
    while True:
        ble.update_timer_state(state.remaining, state.running)
        await asyncio.sleep_ms(500)
```

### Pattern: Touch-Based Timer Control

Start/pause timer with tap, reset with long press:

```python
async def touch_control(touch, gesture, state):
    touch_start_time = 0

    while True:
        event = touch.poll()

        if event:
            if event.type == TouchHandler.TOUCH_DOWN:
                gesture.start(event.x, event.y)
                touch_start_time = time.ticks_ms()

            elif event.type == TouchHandler.TOUCH_UP:
                duration = time.ticks_diff(time.ticks_ms(), touch_start_time)

                if duration > 1000:
                    # Long press: reset timer
                    state.remaining = state.total
                    state.running = False
                else:
                    # Tap: toggle running
                    detected = gesture.end(event.x, event.y)
                    if detected == GestureDetector.TAP:
                        state.running = not state.running

        await asyncio.sleep_ms(10)
```

### Pattern: MQTT Command Handling

Subscribe to control topics and update state:

```python
def mqtt_callback(topic, msg):
    """Handle incoming MQTT messages."""
    global app_state

    topic_str = topic.decode()
    msg_str = msg.decode()

    if topic_str == "productivity/timer/control/start":
        app_state.running = True
    elif topic_str == "productivity/timer/control/pause":
        app_state.running = False
    elif topic_str == "productivity/timer/control/reset":
        app_state.remaining = app_state.total

mqtt = ReliableMQTTClient(
    client_id="presto-001",
    broker="192.168.1.100",
    callback=mqtt_callback
)

mqtt.subscribe("productivity/timer/control/#")
```

## Performance Optimization

### Memory Management

**Critical Rules:**
1. Force garbage collection before allocating large buffers
2. Delete large objects immediately after use
3. Reuse buffers instead of creating new ones
4. Monitor memory with `gc.mem_free()` during development

**Example:**
```python
import gc

# Before allocating framebuffer
gc.collect()
print(f"Free before: {gc.mem_free()}")

# Use buffer
buffer = bytearray(100 * 100 * 2)
# ... use buffer ...
del buffer

# Clean up
gc.collect()
print(f"Free after: {gc.mem_free()}")
```

### Task Scheduling

Balance responsiveness vs CPU usage with appropriate sleep times:

- **Touch input**: 10ms (100 checks/second) - high responsiveness
- **Display updates**: 100ms (10 FPS) - smooth enough for UI
- **BLE sync**: 500ms - adequate for state updates
- **MQTT check**: 100ms - responsive to commands
- **Backlight updates**: 5000ms - slow changes prevent distraction

## Troubleshooting

### Touch Not Responding

1. Verify I2C connection: `i2c.scan()` should show touch controller address
2. Check touch controller I2C address (typically 0x15 for CST816S)
3. Verify GPIO pins match schematic
4. Add pull-up resistors to SDA/SCL if needed (typically 4.7kΩ)

### BLE Connection Drops

1. Reduce BLE notification frequency (increase sleep time in sync task)
2. Check for WiFi/BLE interference (shared radio on some modules)
3. Verify keepalive interval matches client expectations
4. Monitor connection events in `_irq_handler`

### Display Artifacts or Tearing

1. Reduce SPI clock speed if using long cables
2. Implement double buffering for small regions
3. Use partial updates instead of full screen redraws
4. Ensure display CS line is properly controlled

### Memory Exhaustion

1. Check `gc.mem_free()` at critical points
2. Reduce framebuffer size (use tiles or partial updates)
3. Call `gc.collect()` before large allocations
4. Monitor for memory leaks (allocations without deletion)

## Resources

This skill includes:

### scripts/
Executable Python modules for core functionality:
- `touch_handler.py`: Touch input and gesture detection
- `ble_gatt_server.py`: BLE GATT server implementation
- `mqtt_client.py`: Reliable MQTT client with auto-reconnect
- `rgb_backlight.py`: RGB LED control with animations

### references/
Detailed documentation for hardware and software:
- `presto_hardware.md`: Complete hardware reference, pinout, initialization
- `micropython_async.md`: Asyncio patterns and concurrent task management
- `display_rendering.md`: Memory-efficient rendering techniques and UI design

All scripts are production-ready and can be used directly or customized for specific applications.
