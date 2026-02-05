---
name: badger-hardware
description: Hardware integration for Badger 2350 including GPIO, I2C sensors, SPI devices, and electronic components. Use when connecting external hardware, working with sensors, controlling LEDs, reading buttons, or interfacing with I2C/SPI devices on Badger 2350.
---

# Badger 2350 Hardware Integration

Interface with GPIO pins, sensors, and external hardware on the Badger 2350 badge using I2C, SPI, and digital I/O.

## GPIO Basics

### Pin Configuration

```python
from machine import Pin

# Configure pin as output (LED, relay, etc.)
led = Pin(25, Pin.OUT)
led.value(1)  # Turn on (HIGH)
led.value(0)  # Turn off (LOW)
led.toggle()  # Toggle state

# Configure pin as input (button, switch, etc.)
button = Pin(15, Pin.IN, Pin.PULL_UP)
if button.value() == 0:  # Button pressed (pulled to ground)
    print("Button pressed!")

# Configure pin as input with pull-down
sensor = Pin(16, Pin.IN, Pin.PULL_DOWN)
```

### PWM (Pulse Width Modulation)

```python
from machine import Pin, PWM

# Control LED brightness or servo motor
pwm = PWM(Pin(25))
pwm.freq(1000)  # Set frequency to 1kHz

# Set duty cycle (0-65535, where 65535 is 100%)
pwm.duty_u16(32768)  # 50% brightness
pwm.duty_u16(16384)  # 25% brightness
pwm.duty_u16(65535)  # 100% brightness

# Cleanup
pwm.deinit()
```

### Interrupts

```python
from machine import Pin

button = Pin(15, Pin.IN, Pin.PULL_UP)

def button_callback(pin):
    print(f"Button pressed! Pin: {pin}")

# Trigger on falling edge (button press)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_callback)

# Trigger on rising edge (button release)
button.irq(trigger=Pin.IRQ_RISING, handler=button_callback)

# Trigger on both edges
button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_callback)
```

## I2C Communication

### I2C Setup

```python
from machine import I2C, Pin

# Initialize I2C (QWIIC connector uses specific pins)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

# Scan for connected devices
devices = i2c.scan()
print(f"Found {len(devices)} I2C devices:")
for device in devices:
    print(f"  Address: 0x{device:02x}")
```

### Reading from I2C Device

```python
# Read data from I2C device
address = 0x48  # Example: Temperature sensor
data = i2c.readfrom(address, 2)  # Read 2 bytes
print(f"Raw data: {data}")

# Read from specific register
register = 0x00
i2c.writeto(address, bytes([register]))  # Select register
data = i2c.readfrom(address, 2)  # Read data
```

### Writing to I2C Device

```python
# Write single byte
address = 0x48
data = bytes([0x01, 0xA0])
i2c.writeto(address, data)

# Write to specific register
register = 0x01
value = 0xFF
i2c.writeto(address, bytes([register, value]))
```

## Common I2C Sensors

### BME280 (Temperature, Humidity, Pressure)

```python
from machine import I2C, Pin
import time

class BME280:
    def __init__(self, i2c, address=0x76):
        self.i2c = i2c
        self.address = address

    def read_temp(self):
        # Read temperature register
        data = self.i2c.readfrom_mem(self.address, 0xFA, 3)
        temp_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        # Apply calibration (simplified)
        temp_c = temp_raw / 100.0
        return temp_c

    def read_humidity(self):
        # Read humidity register
        data = self.i2c.readfrom_mem(self.address, 0xFD, 2)
        hum_raw = (data[0] << 8) | data[1]
        humidity = hum_raw / 1024.0
        return humidity

# Usage
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
sensor = BME280(i2c)

temp = sensor.read_temp()
humidity = sensor.read_humidity()
print(f"Temp: {temp:.1f}°C, Humidity: {humidity:.1f}%")
```

### APDS9960 (Gesture, Proximity, Color Sensor)

```python
class APDS9960:
    def __init__(self, i2c, address=0x39):
        self.i2c = i2c
        self.address = address
        self._init_sensor()

    def _init_sensor(self):
        # Enable device
        self.i2c.writeto_mem(self.address, 0x80, bytes([0x01]))
        # Enable gesture mode
        self.i2c.writeto_mem(self.address, 0x93, bytes([0x01]))

    def read_gesture(self):
        # Read gesture FIFO
        fifo_level = self.i2c.readfrom_mem(self.address, 0xAE, 1)[0]
        if fifo_level > 0:
            data = self.i2c.readfrom_mem(self.address, 0xFC, 4)
            # Process gesture data
            return self._detect_gesture(data)
        return None

    def _detect_gesture(self, data):
        # Simplified gesture detection
        if data[0] > data[2]:
            return "UP"
        elif data[0] < data[2]:
            return "DOWN"
        elif data[1] > data[3]:
            return "LEFT"
        else:
            return "RIGHT"

# Usage
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
gesture_sensor = APDS9960(i2c)

gesture = gesture_sensor.read_gesture()
if gesture:
    print(f"Gesture detected: {gesture}")
```

### VL53L0X (Time-of-Flight Distance Sensor)

```python
class VL53L0X:
    def __init__(self, i2c, address=0x29):
        self.i2c = i2c
        self.address = address

    def read_distance(self):
        # Start measurement
        self.i2c.writeto_mem(self.address, 0x00, bytes([0x01]))

        # Wait for measurement
        time.sleep(0.05)

        # Read distance (mm)
        data = self.i2c.readfrom_mem(self.address, 0x14, 2)
        distance = (data[0] << 8) | data[1]
        return distance

# Usage
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
tof = VL53L0X(i2c)

distance = tof.read_distance()
print(f"Distance: {distance}mm")
```

## SPI Communication

### SPI Setup

```python
from machine import SPI, Pin

# Initialize SPI
spi = SPI(0, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=Pin(4))

# Chip select pin
cs = Pin(5, Pin.OUT)
cs.value(1)  # Deselect initially

# Read/write data
cs.value(0)  # Select device
spi.write(bytes([0x01, 0x02, 0x03]))  # Write data
data = spi.read(3)  # Read 3 bytes
cs.value(1)  # Deselect device

print(f"Received: {data}")
```

### SD Card Reader (SPI)

```python
from machine import SPI, Pin
import sdcard
import os

# Initialize SPI and SD card
spi = SPI(0, baudrate=1000000, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs = Pin(5, Pin.OUT)

sd = sdcard.SDCard(spi, cs)

# Mount SD card
os.mount(sd, '/sd')

# Write file
with open('/sd/data.txt', 'w') as f:
    f.write('Hello from Badger!')

# Read file
with open('/sd/data.txt', 'r') as f:
    print(f.read())

# Unmount
os.umount('/sd')
```

## Analog Input (ADC)

```python
from machine import ADC, Pin

# Initialize ADC on GPIO pin
adc = ADC(Pin(26))

# Read raw value (0-65535 for 16-bit ADC)
raw_value = adc.read_u16()
print(f"Raw ADC: {raw_value}")

# Convert to voltage (assuming 3.3V reference)
voltage = (raw_value / 65535) * 3.3
print(f"Voltage: {voltage:.2f}V")

# Example: Read potentiometer
while True:
    value = adc.read_u16()
    percentage = (value / 65535) * 100
    print(f"Pot: {percentage:.1f}%")
    time.sleep(0.1)
```

## NeoPixel (WS2812B) LEDs

```python
from machine import Pin
import neopixel
import time

# Initialize NeoPixel strip (8 LEDs on pin 25)
num_leds = 8
np = neopixel.NeoPixel(Pin(25), num_leds)

# Set individual LED color (R, G, B)
np[0] = (255, 0, 0)    # Red
np[1] = (0, 255, 0)    # Green
np[2] = (0, 0, 255)    # Blue
np[3] = (255, 255, 0)  # Yellow
np.write()  # Update LEDs

# Rainbow effect
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_leds):
            pixel_index = (i * 256 // num_leds) + j
            np[i] = wheel(pixel_index & 255)
        np.write()
        time.sleep(wait)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions"""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

rainbow_cycle(0.001)
```

## Servo Motor Control

```python
from machine import Pin, PWM
import time

class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)  # 50Hz for servo

    def angle(self, degrees):
        """Set servo angle (0-180 degrees)"""
        # Convert angle to duty cycle
        # 0° = 1ms (3.2% duty)
        # 90° = 1.5ms (7.5% duty)
        # 180° = 2ms (10% duty)
        min_duty = 1638   # 2.5% of 65535
        max_duty = 8192   # 12.5% of 65535
        duty = int(min_duty + (degrees / 180) * (max_duty - min_duty))
        self.pwm.duty_u16(duty)

    def deinit(self):
        self.pwm.deinit()

# Usage
servo = Servo(25)

# Sweep servo
for angle in range(0, 181, 10):
    servo.angle(angle)
    time.sleep(0.1)

servo.deinit()
```

## Relay Control

```python
from machine import Pin
import time

class Relay:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.off()

    def on(self):
        self.pin.value(1)

    def off(self):
        self.pin.value(0)

    def toggle(self):
        self.pin.toggle()

# Usage
relay = Relay(25)

relay.on()
time.sleep(2)
relay.off()

# Pulse relay
for i in range(5):
    relay.toggle()
    time.sleep(0.5)
```

## Integration with Badge Display

### Display Sensor Data

```python
import badger2040
from machine import I2C, Pin
import time

badge = badger2040.Badger2040()
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

def display_sensor_data():
    # Read sensor (example)
    temp = read_temperature()  # Your sensor function
    humidity = read_humidity()

    badge.set_pen(15)
    badge.clear()
    badge.set_pen(0)

    badge.text("Sensor Monitor", 10, 10, scale=2)
    badge.text(f"Temp: {temp:.1f}C", 10, 40, scale=2)
    badge.text(f"Humidity: {humidity:.1f}%", 10, 70, scale=2)

    badge.update()

while True:
    display_sensor_data()
    time.sleep(1)
```

### Interactive Hardware Control

```python
import badger2040
from machine import Pin
import time

badge = badger2040.Badger2040()
led = Pin(25, Pin.OUT)
led_state = False

def draw_ui():
    badge.set_pen(15)
    badge.clear()
    badge.set_pen(0)

    badge.text("LED Control", 10, 10, scale=2)

    status = "ON" if led_state else "OFF"
    badge.text(f"Status: {status}", 10, 50, scale=2)

    badge.text("A: Toggle", 10, 100, scale=1)

    badge.update()

while True:
    draw_ui()

    if badge.pressed(badger2040.BUTTON_A):
        led_state = not led_state
        led.value(1 if led_state else 0)
        time.sleep(0.2)  # Debounce
```

## Power Management for Hardware

```python
from machine import Pin
import machine

# Power control for external hardware
power_pin = Pin(23, Pin.OUT)

def power_on():
    power_pin.value(1)

def power_off():
    power_pin.value(0)

# Use with sleep modes
power_on()
# ... do work with sensor ...
power_off()
machine.lightsleep(5000)  # Sleep 5 seconds
```

## Troubleshooting

**I2C device not detected**: Check wiring, verify device address, ensure pull-up resistors are present

**GPIO not working**: Verify pin is not used by internal badge functions, check if pin is input/output capable

**SPI communication fails**: Check clock polarity and phase, verify baudrate is within device specs

**PWM not smooth**: Increase PWM frequency, ensure duty cycle calculations are correct

**Sensor readings unstable**: Add delays between readings, use averaging, check power supply stability

## Hardware Safety

- **Never exceed 3.3V** on GPIO pins
- Use level shifters for 5V devices
- Add current-limiting resistors for LEDs
- Use flyback diodes with motors and relays
- Keep I2C wires short (< 20cm) or use bus extenders
- Use proper power supply for high-current devices

## Pinout Reference

Common Badger 2350 pins available for external hardware:
- GPIO 0-22: General purpose I/O
- GPIO 26-28: ADC capable (analog input)
- I2C QWIIC: SCL (Pin 5), SDA (Pin 4)
- SPI: SCK, MOSI, MISO (check documentation)

Refer to official Badger 2350 pinout diagram for complete details.
