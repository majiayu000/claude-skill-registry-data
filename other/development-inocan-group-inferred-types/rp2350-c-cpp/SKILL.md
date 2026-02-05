---
name: rp2350-c-cpp
description: Expert RP2350 C/C++ development with Pico SDK, covering CMake configuration, peripheral drivers (GPIO, SPI, I2C, PWM, UART), hardware optimization, FreeRTOS integration, and bare-metal programming. Use when developing C/C++ firmware for RP2350/RP2040 boards, implementing hardware drivers, optimizing performance, or building real-time embedded applications.
---

# RP2350 C/C++ Development with Pico SDK

## Overview

This skill provides comprehensive guidance for developing high-performance embedded applications on RP2350 and RP2040 hardware using C/C++ and the official Raspberry Pi Pico SDK. It covers project setup, CMake configuration, peripheral programming, memory optimization, multicore development, and FreeRTOS integration.

## When to Use This Skill

Use this skill when:

- Developing C/C++ firmware for RP2350 or RP2040 boards
- Setting up Pico SDK projects with CMake
- Implementing hardware drivers (GPIO, SPI, I2C, PWM, UART, ADC)
- Writing interrupt service routines and DMA transfers
- Building multicore applications utilizing both ARM cores
- Integrating FreeRTOS for real-time task management
- Optimizing memory usage and execution speed
- Implementing USB device or host functionality
- Working with PIO (Programmable I/O) for custom protocols
- Debugging with picoprobe or SWD interfaces
- Porting applications from RP2040 to RP2350

## Hardware Context

### RP2350 Features

- **Processor**: Dual ARM Cortex-M33 @ 150MHz (or dual RISC-V Hazard3 @ 150MHz)
- **Memory**: 520KB SRAM, up to 16MB external flash
- **Security**: ARM TrustZone-M, secure boot, signed firmware
- **Peripherals**:
  - 30 multifunction GPIO pins
  - 2× UART, 2× SPI, 2× I2C
  - 12-bit ADC with up to 5 channels
  - 24× PWM channels
  - 12× PIO state machines
  - USB 1.1 host/device
  - DMA controller with 12 channels
- **Power**: 1.8-3.6V operation, sleep modes down to 180µA

### RP2040 Features (for comparison)

- **Processor**: Dual ARM Cortex-M0+ @ 133MHz
- **Memory**: 264KB SRAM, up to 16MB external flash
- **Peripherals**: Similar to RP2350 but without TrustZone and with lower performance

## Core Capabilities

### 1. Project Setup with CMake

Use `assets/project_template/` for a complete CMake-based project structure.

**Key Components:**
- `CMakeLists.txt` - Main build configuration
- `pico_sdk_import.cmake` - SDK integration
- `.vscode/` - VSCode configuration for debugging
- `src/` - Source code directory

**Quick Start:**
```bash
# Copy template
cp -r assets/project_template/ my_project
cd my_project

# Configure environment
export PICO_SDK_PATH=/path/to/pico-sdk

# Build
mkdir build && cd build
cmake ..
make -j4
```

**CMakeLists.txt Structure:**
```cmake
cmake_minimum_required(VERSION 3.13)

# Include SDK
include(pico_sdk_import.cmake)

project(my_project C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize SDK
pico_sdk_init()

# Add executable
add_executable(my_project
    src/main.c
    src/peripheral_init.c
)

# Link libraries
target_link_libraries(my_project
    pico_stdlib
    hardware_spi
    hardware_i2c
    hardware_pwm
    hardware_adc
)

# Enable USB output, disable UART
pico_enable_stdio_usb(my_project 1)
pico_enable_stdio_uart(my_project 0)

# Create map/bin/hex/uf2 files
pico_add_extra_outputs(my_project)
```

Refer to `references/cmake_configuration.md` for advanced CMake patterns including multicore builds, FreeRTOS integration, and custom linker scripts.

### 2. GPIO and Basic I/O

**Initialization:**
```c
#include "pico/stdlib.h"

// Configure GPIO as output
const uint LED_PIN = 25;
gpio_init(LED_PIN);
gpio_set_dir(LED_PIN, GPIO_OUT);

// Configure GPIO as input with pull-up
const uint BUTTON_PIN = 15;
gpio_init(BUTTON_PIN);
gpio_set_dir(BUTTON_PIN, GPIO_IN);
gpio_pull_up(BUTTON_PIN);
```

**Interrupt Handling:**
```c
void gpio_callback(uint gpio, uint32_t events) {
    if (gpio == BUTTON_PIN && (events & GPIO_IRQ_EDGE_FALL)) {
        // Button pressed
        gpio_put(LED_PIN, !gpio_get(LED_PIN));
    }
}

int main() {
    stdio_init_all();

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    gpio_init(BUTTON_PIN);
    gpio_set_dir(BUTTON_PIN, GPIO_IN);
    gpio_pull_up(BUTTON_PIN);

    // Enable interrupt
    gpio_set_irq_enabled_with_callback(
        BUTTON_PIN,
        GPIO_IRQ_EDGE_FALL,
        true,
        &gpio_callback
    );

    while (1) {
        tight_loop_contents();
    }
}
```

### 3. SPI Communication

**Standard SPI Setup:**
```c
#include "hardware/spi.h"

#define SPI_PORT spi0
#define PIN_MISO 16
#define PIN_CS   17
#define PIN_SCK  18
#define PIN_MOSI 19

void spi_init_device() {
    // Initialize SPI at 10 MHz
    spi_init(SPI_PORT, 10 * 1000 * 1000);

    // Configure GPIO for SPI
    gpio_set_function(PIN_MISO, GPIO_FUNC_SPI);
    gpio_set_function(PIN_SCK,  GPIO_FUNC_SPI);
    gpio_set_function(PIN_MOSI, GPIO_FUNC_SPI);

    // Initialize CS pin as GPIO output
    gpio_init(PIN_CS);
    gpio_set_dir(PIN_CS, GPIO_OUT);
    gpio_put(PIN_CS, 1);  // CS high (inactive)
}

uint8_t spi_read_register(uint8_t reg) {
    uint8_t data;
    gpio_put(PIN_CS, 0);  // CS low
    spi_write_blocking(SPI_PORT, &reg, 1);
    spi_read_blocking(SPI_PORT, 0, &data, 1);
    gpio_put(PIN_CS, 1);  // CS high
    return data;
}

void spi_write_register(uint8_t reg, uint8_t value) {
    uint8_t buf[2] = {reg, value};
    gpio_put(PIN_CS, 0);
    spi_write_blocking(SPI_PORT, buf, 2);
    gpio_put(PIN_CS, 1);
}
```

**DMA-Based SPI Transfer:**
```c
#include "hardware/dma.h"

void spi_dma_transfer(uint8_t *tx_buf, uint8_t *rx_buf, size_t len) {
    int dma_tx = dma_claim_unused_channel(true);
    int dma_rx = dma_claim_unused_channel(true);

    // Configure TX DMA
    dma_channel_config c_tx = dma_channel_get_default_config(dma_tx);
    channel_config_set_transfer_data_size(&c_tx, DMA_SIZE_8);
    channel_config_set_dreq(&c_tx, spi_get_dreq(SPI_PORT, true));

    dma_channel_configure(
        dma_tx, &c_tx,
        &spi_get_hw(SPI_PORT)->dr,  // dst
        tx_buf,                      // src
        len,                         // transfer count
        false                        // don't start yet
    );

    // Configure RX DMA
    dma_channel_config c_rx = dma_channel_get_default_config(dma_rx);
    channel_config_set_transfer_data_size(&c_rx, DMA_SIZE_8);
    channel_config_set_dreq(&c_rx, spi_get_dreq(SPI_PORT, false));
    channel_config_set_read_increment(&c_rx, false);
    channel_config_set_write_increment(&c_rx, true);

    dma_channel_configure(
        dma_rx, &c_rx,
        rx_buf,                      // dst
        &spi_get_hw(SPI_PORT)->dr,  // src
        len,                         // transfer count
        false                        // don't start yet
    );

    // Start both channels
    gpio_put(PIN_CS, 0);
    dma_start_channel_mask((1u << dma_tx) | (1u << dma_rx));

    // Wait for completion
    dma_channel_wait_for_finish_blocking(dma_rx);
    gpio_put(PIN_CS, 1);

    // Release channels
    dma_channel_unclaim(dma_tx);
    dma_channel_unclaim(dma_rx);
}
```

### 4. I2C Communication

**I2C Setup and Operations:**
```c
#include "hardware/i2c.h"

#define I2C_PORT i2c0
#define I2C_SDA 4
#define I2C_SCL 5
#define I2C_FREQ 400000  // 400 kHz

void i2c_init_device() {
    // Initialize I2C at 400 kHz
    i2c_init(I2C_PORT, I2C_FREQ);

    // Configure GPIO for I2C
    gpio_set_function(I2C_SDA, GPIO_FUNC_I2C);
    gpio_set_function(I2C_SCL, GPIO_FUNC_I2C);
    gpio_pull_up(I2C_SDA);
    gpio_pull_up(I2C_SCL);
}

// Read single byte
uint8_t i2c_read_byte(uint8_t addr, uint8_t reg) {
    uint8_t data;
    i2c_write_blocking(I2C_PORT, addr, &reg, 1, true);
    i2c_read_blocking(I2C_PORT, addr, &data, 1, false);
    return data;
}

// Write single byte
void i2c_write_byte(uint8_t addr, uint8_t reg, uint8_t value) {
    uint8_t buf[2] = {reg, value};
    i2c_write_blocking(I2C_PORT, addr, buf, 2, false);
}

// Read multiple bytes
int i2c_read_bytes(uint8_t addr, uint8_t reg, uint8_t *buf, size_t len) {
    i2c_write_blocking(I2C_PORT, addr, &reg, 1, true);
    return i2c_read_blocking(I2C_PORT, addr, buf, len, false);
}

// I2C scanner
void i2c_scan() {
    printf("\nI2C Bus Scan\n");
    printf("   0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F\n");

    for (int addr = 0; addr < (1 << 7); ++addr) {
        if (addr % 16 == 0) {
            printf("%02x ", addr);
        }

        int ret;
        uint8_t rxdata;
        ret = i2c_read_blocking(I2C_PORT, addr, &rxdata, 1, false);

        printf(ret < 0 ? "." : "@");
        printf(addr % 16 == 15 ? "\n" : "  ");
    }
}
```

### 5. PWM for LED/Motor Control

**PWM Configuration:**
```c
#include "hardware/pwm.h"

void pwm_init_pin(uint gpio, uint freq_hz, float duty_cycle) {
    // Configure GPIO for PWM
    gpio_set_function(gpio, GPIO_FUNC_PWM);

    // Find PWM slice
    uint slice_num = pwm_gpio_to_slice_num(gpio);

    // Calculate divider and wrap for desired frequency
    uint32_t clock_freq = 125000000;  // 125 MHz
    uint32_t divider = clock_freq / (freq_hz * 65536);
    if (divider < 1) divider = 1;

    uint32_t wrap = (clock_freq / (freq_hz * divider)) - 1;

    // Configure PWM
    pwm_set_clkdiv(slice_num, divider);
    pwm_set_wrap(slice_num, wrap);

    // Set duty cycle
    uint16_t level = (uint16_t)(wrap * duty_cycle);
    pwm_set_gpio_level(gpio, level);

    // Enable PWM
    pwm_set_enabled(slice_num, true);
}

// Example: RGB LED control
void rgb_led_init(uint pin_r, uint pin_g, uint pin_b) {
    pwm_init_pin(pin_r, 1000, 0.0);  // 1 kHz, 0% duty
    pwm_init_pin(pin_g, 1000, 0.0);
    pwm_init_pin(pin_b, 1000, 0.0);
}

void rgb_led_set_color(uint pin_r, uint pin_g, uint pin_b,
                       float r, float g, float b) {
    uint slice_r = pwm_gpio_to_slice_num(pin_r);
    uint slice_g = pwm_gpio_to_slice_num(pin_g);
    uint slice_b = pwm_gpio_to_slice_num(pin_b);

    uint16_t wrap = pwm_get_wrap(slice_r);

    pwm_set_gpio_level(pin_r, (uint16_t)(wrap * r));
    pwm_set_gpio_level(pin_g, (uint16_t)(wrap * g));
    pwm_set_gpio_level(pin_b, (uint16_t)(wrap * b));
}
```

### 6. ADC (Analog-to-Digital Converter)

**ADC Reading:**
```c
#include "hardware/adc.h"

void adc_init_all() {
    adc_init();

    // Make sure GPIO is high-impedance, no pullups etc
    adc_gpio_init(26);  // ADC0
    adc_gpio_init(27);  // ADC1
    adc_gpio_init(28);  // ADC2
}

uint16_t adc_read_channel(uint channel) {
    adc_select_input(channel);
    return adc_read();
}

float adc_read_voltage(uint channel) {
    adc_select_input(channel);
    uint16_t raw = adc_read();
    // Convert to voltage (3.3V reference, 12-bit ADC)
    return raw * 3.3f / 4096.0f;
}

// Read internal temperature sensor
float read_onboard_temperature() {
    adc_select_input(4);  // Temperature sensor on ADC4
    uint16_t raw = adc_read();

    // Convert to temperature (from RP2040 datasheet)
    const float conversion = 3.3f / 4096.0f;
    float voltage = raw * conversion;
    float temp_c = 27.0f - (voltage - 0.706f) / 0.001721f;

    return temp_c;
}
```

### 7. Multicore Programming

**Core1 Launch:**
```c
#include "pico/multicore.h"

void core1_entry() {
    while (1) {
        // Core 1 work here
        printf("Running on core 1\n");
        sleep_ms(1000);
    }
}

int main() {
    stdio_init_all();

    printf("Starting core 1\n");
    multicore_launch_core1(core1_entry);

    while (1) {
        // Core 0 work here
        printf("Running on core 0\n");
        sleep_ms(1000);
    }
}
```

**Intercore Communication:**
```c
#include "pico/multicore.h"

// Core 0 to Core 1 FIFO
void core0_send_to_core1(uint32_t data) {
    multicore_fifo_push_blocking(data);
}

// Core 1 receives from Core 0
uint32_t core1_receive_from_core0() {
    return multicore_fifo_pop_blocking();
}

// Example: Core 1 worker
void core1_worker() {
    while (1) {
        uint32_t cmd = multicore_fifo_pop_blocking();

        switch (cmd) {
            case 1:
                // Process command 1
                break;
            case 2:
                // Process command 2
                break;
        }

        // Send result back to Core 0
        multicore_fifo_push_blocking(42);
    }
}
```

### 8. USB Device Implementation

**USB Serial (CDC):**
Already enabled with `pico_enable_stdio_usb()` in CMakeLists.txt.

**Custom USB Device:**
```c
#include "tusb.h"

// USB HID Keyboard example
void send_key_press(uint8_t keycode) {
    if (tud_hid_ready()) {
        uint8_t report[8] = {0};
        report[2] = keycode;  // Keycode
        tud_hid_keyboard_report(0, 0, report);

        // Release key
        sleep_ms(10);
        tud_hid_keyboard_report(0, 0, NULL);
    }
}
```

Refer to `references/pico_sdk_reference.md` for comprehensive USB API documentation including HID, MSC, and CDC examples.

## Development Workflow

### Step 1: Environment Setup

**Install Dependencies:**
```bash
# Linux/Raspberry Pi
sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi \
                 build-essential libstdc++-arm-none-eabi-newlib

# macOS
brew install cmake
brew install --cask gcc-arm-embedded
```

**Clone Pico SDK:**
```bash
cd ~
git clone https://github.com/raspberrypi/pico-sdk.git
cd pico-sdk
git submodule update --init
export PICO_SDK_PATH=$(pwd)
```

### Step 2: Create Project from Template

Use the provided project template:
```bash
cp -r assets/project_template/ my_project
cd my_project
```

Edit `CMakeLists.txt` to configure your project name and dependencies.

### Step 3: Build

```bash
mkdir build
cd build
cmake ..
make -j4
```

Output files:
- `my_project.elf` - ELF executable
- `my_project.bin` - Binary image
- `my_project.uf2` - USB bootloader format
- `my_project.hex` - Intel HEX format

### Step 4: Flash Firmware

**Method 1: USB Bootloader (BOOTSEL mode)**
```bash
# 1. Hold BOOTSEL button while plugging in USB
# 2. Copy UF2 file to mounted drive
cp my_project.uf2 /media/$USER/RPI-RP2/
```

**Method 2: Using Picoprobe/SWD**
```bash
# Using OpenOCD with picoprobe
openocd -f interface/cmsis-dap.cfg \
        -f target/rp2040.cfg \
        -c "program my_project.elf verify reset exit"
```

**Method 3: Using Flash Script**
Use `scripts/flash.sh` for automated flashing:
```bash
./scripts/flash.sh build/my_project.uf2
```

### Step 5: Debug

**Serial Debug Output:**
```c
#include "pico/stdlib.h"

int main() {
    stdio_init_all();

    while (!tud_cdc_connected()) {
        sleep_ms(100);
    }

    printf("Debug: System initialized\n");
    // Your code here
}
```

**GDB Debugging with Picoprobe:**
```bash
# Terminal 1: Start OpenOCD
openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg

# Terminal 2: Start GDB
gdb-multiarch my_project.elf
(gdb) target remote localhost:3333
(gdb) load
(gdb) break main
(gdb) continue
```

Refer to `.vscode/launch.json` in the project template for VSCode debugging configuration.

## Common Patterns

### Pattern: Non-Blocking Timer

```c
#include "pico/time.h"

typedef struct {
    absolute_time_t last_trigger;
    uint32_t interval_ms;
} timer_t;

void timer_init(timer_t *timer, uint32_t interval_ms) {
    timer->interval_ms = interval_ms;
    timer->last_trigger = get_absolute_time();
}

bool timer_expired(timer_t *timer) {
    absolute_time_t now = get_absolute_time();
    int64_t elapsed = absolute_time_diff_us(timer->last_trigger, now);

    if (elapsed >= timer->interval_ms * 1000) {
        timer->last_trigger = now;
        return true;
    }
    return false;
}

// Usage
int main() {
    timer_t blink_timer;
    timer_init(&blink_timer, 500);  // 500ms interval

    while (1) {
        if (timer_expired(&blink_timer)) {
            gpio_xor_mask(1 << LED_PIN);
        }

        // Other non-blocking work
        tight_loop_contents();
    }
}
```

### Pattern: State Machine

```c
typedef enum {
    STATE_IDLE,
    STATE_RUNNING,
    STATE_PAUSED,
    STATE_COMPLETED
} app_state_t;

typedef struct {
    app_state_t state;
    uint32_t counter;
    bool button_pressed;
} app_context_t;

void state_machine_update(app_context_t *ctx) {
    switch (ctx->state) {
        case STATE_IDLE:
            if (ctx->button_pressed) {
                ctx->state = STATE_RUNNING;
                ctx->counter = 0;
            }
            break;

        case STATE_RUNNING:
            ctx->counter++;
            if (ctx->button_pressed) {
                ctx->state = STATE_PAUSED;
            }
            if (ctx->counter >= 1000) {
                ctx->state = STATE_COMPLETED;
            }
            break;

        case STATE_PAUSED:
            if (ctx->button_pressed) {
                ctx->state = STATE_RUNNING;
            }
            break;

        case STATE_COMPLETED:
            // Reset on button press
            if (ctx->button_pressed) {
                ctx->state = STATE_IDLE;
            }
            break;
    }

    ctx->button_pressed = false;
}
```

### Pattern: Circular Buffer (Ring Buffer)

```c
typedef struct {
    uint8_t *buffer;
    size_t size;
    size_t head;
    size_t tail;
    size_t count;
} ring_buffer_t;

void ring_buffer_init(ring_buffer_t *rb, uint8_t *buffer, size_t size) {
    rb->buffer = buffer;
    rb->size = size;
    rb->head = 0;
    rb->tail = 0;
    rb->count = 0;
}

bool ring_buffer_push(ring_buffer_t *rb, uint8_t data) {
    if (rb->count >= rb->size) {
        return false;  // Buffer full
    }

    rb->buffer[rb->head] = data;
    rb->head = (rb->head + 1) % rb->size;
    rb->count++;
    return true;
}

bool ring_buffer_pop(ring_buffer_t *rb, uint8_t *data) {
    if (rb->count == 0) {
        return false;  // Buffer empty
    }

    *data = rb->buffer[rb->tail];
    rb->tail = (rb->tail + 1) % rb->size;
    rb->count--;
    return true;
}
```

## Performance Optimization

### Memory Management

**Stack Size Configuration:**
In `CMakeLists.txt`:
```cmake
# Increase stack size if needed
target_compile_definitions(my_project PRIVATE
    PICO_STACK_SIZE=0x2000  # 8KB stack
    PICO_CORE1_STACK_SIZE=0x2000
)
```

**Static vs Dynamic Allocation:**
```c
// Prefer static allocation on embedded systems
static uint8_t buffer[1024];

// Avoid malloc/free if possible
// If needed, consider custom allocator
```

**Memory-Mapped I/O:**
```c
#include "hardware/regs/addressmap.h"

// Direct register access (faster than SDK functions)
#define GPIO_OUT_REG ((volatile uint32_t*)(SIO_BASE + 0x10))
#define GPIO_OUT_SET ((volatile uint32_t*)(SIO_BASE + 0x14))
#define GPIO_OUT_CLR ((volatile uint32_t*)(SIO_BASE + 0x18))
#define GPIO_OUT_XOR ((volatile uint32_t*)(SIO_BASE + 0x1C))

// Fast GPIO toggle
*GPIO_OUT_XOR = (1 << LED_PIN);
```

### Code Optimization

**Compiler Flags in CMakeLists.txt:**
```cmake
# Optimization level
target_compile_options(my_project PRIVATE
    -O3                    # Maximum optimization
    -flto                  # Link-time optimization
    -ffunction-sections    # Each function in own section
    -fdata-sections        # Each data item in own section
)

target_link_options(my_project PRIVATE
    -Wl,--gc-sections      # Remove unused sections
)
```

**Inline Functions:**
```c
static inline void fast_gpio_toggle(uint gpio) {
    sio_hw->gpio_togl = 1u << gpio;
}
```

**Use Hardware Features:**
- DMA for large data transfers
- PIO for bit-banging protocols
- Hardware interpolators for calculations

### Interrupt Optimization

```c
// Keep ISRs short and fast
void __isr __time_critical_func(gpio_isr)() {
    // Clear interrupt
    gpio_acknowledge_irq(BUTTON_PIN, GPIO_IRQ_EDGE_FALL);

    // Set flag for main loop
    volatile bool button_flag = true;

    // Don't call printf or blocking functions in ISR
}
```

## Troubleshooting

### Build Issues

**SDK Not Found:**
```bash
export PICO_SDK_PATH=/path/to/pico-sdk
```

**Undefined Reference Errors:**
Add missing libraries in `CMakeLists.txt`:
```cmake
target_link_libraries(my_project
    pico_stdlib
    hardware_spi    # Add this
    hardware_i2c    # Add this
)
```

### Flashing Issues

**Device Not Recognized:**
1. Check USB cable (data capable, not charge-only)
2. Verify BOOTSEL button held during power-on
3. Check `lsusb` for RP2040 device (ID 2e8a:0003)

**Permission Denied (Linux):**
```bash
sudo usermod -a -G dialout $USER
# Log out and back in
```

### Runtime Issues

**Crash on Startup:**
- Check stack size (increase if needed)
- Verify all peripherals initialized before use
- Check for buffer overflows

**GPIO Not Working:**
- Verify pin numbers match board pinout
- Check if pin already used by another peripheral
- Ensure `gpio_init()` called before use

**SPI/I2C No Response:**
- Verify wiring and pull-up resistors
- Check clock frequencies
- Use oscilloscope to verify signals
- Try `i2c_scan()` to detect devices

### Memory Issues

**Out of RAM:**
```c
// Check memory usage
extern char __StackLimit, __bss_end__;
printf("Heap end: %p\n", &__bss_end__);
printf("Stack limit: %p\n", &__StackLimit);
```

**Reduce Memory Usage:**
- Use smaller buffers
- Move large arrays to flash: `const uint8_t data[] = {...};`
- Optimize struct packing
- Use bit fields for flags

## Resources

This skill includes:

### scripts/
Build and deployment automation:
- `build.sh` - Automated build script with error handling
- `flash.sh` - Automated firmware flashing (supports BOOTSEL and picoprobe)
- `monitor.sh` - Serial monitor for debugging output

### references/
Comprehensive technical documentation:
- `pico_sdk_reference.md` - Complete Pico SDK API reference and examples
- `cmake_configuration.md` - Advanced CMake patterns and build configurations
- `hardware_interfaces.md` - Detailed hardware peripheral programming guide
- `freertos_integration.md` - FreeRTOS setup and real-time task patterns

### assets/
Ready-to-use project templates and boilerplate:
- `project_template/` - Complete CMake project structure with examples
  - `CMakeLists.txt` - Configured build system
  - `pico_sdk_import.cmake` - SDK integration
  - `.vscode/` - VSCode debugging configuration
  - `src/main.c` - Minimal example application

All scripts and templates are production-ready and can be used directly or customized for specific applications.
