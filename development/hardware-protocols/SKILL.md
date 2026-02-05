---
name: hardware-protocols
description: Expert hardware communication protocols including MQTT, I2C, SPI, UART, BLE, and WiFi. Use when implementing device-to-device communication, designing MQTT messaging systems, configuring bus protocols, integrating wireless connectivity, troubleshooting protocol issues, or setting up multi-device embedded systems. Particularly relevant for IoT projects, embedded systems with multiple peripherals, and distributed sensor networks.
---

# Hardware Communication Protocols

## Overview

Implement reliable hardware communication protocols for embedded systems. This skill covers MQTT (message broker architecture), I2C/SPI (synchronous bus protocols), UART (serial communication), BLE (Bluetooth Low Energy), and WiFi networking. Use this skill when designing communication between microcontrollers, sensors, displays, and networked devices.

## When to Use This Skill

Invoke this skill when:
- Setting up MQTT broker and client communication
- Designing topic hierarchies and message flows
- Implementing I2C sensor reading or device control
- Configuring SPI displays or high-speed peripherals
- Establishing UART communication with AT command devices
- Creating BLE GATT services and characteristics
- Integrating WiFi connectivity with reconnection strategies
- Troubleshooting protocol timing or connection issues
- Building multi-device embedded systems (like Orbit)

## Protocol Selection Guide

Choose the appropriate protocol based on requirements:

**MQTT** - Publish/subscribe messaging for distributed systems
- Use when: Multiple devices need synchronized state updates
- Topology: Many-to-many through central broker
- Range: Network-dependent (WiFi/Ethernet)
- Data rate: Lightweight messaging (KB/s)
- Orbit usage: All devices ↔ Jetson broker for timer sync, commands

**I2C** - Two-wire synchronous bus for short-distance peripherals
- Use when: Multiple low-speed sensors/devices on shared bus
- Topology: Master/slave (one master, multiple slaves)
- Range: <1 meter on PCB
- Data rate: 100 KHz - 3.4 MHz
- Orbit usage: Onboard sensors (temperature, accelerometer)

**SPI** - Four-wire synchronous bus for high-speed peripherals
- Use when: Fast displays, memory, or sensor communication needed
- Topology: Master/slave with individual chip selects
- Range: <1 meter on PCB
- Data rate: Up to 50+ MHz
- Orbit usage: TFT displays on Presto and T-Embed

**UART** - Asynchronous serial for point-to-point communication
- Use when: Simple bidirectional communication or AT commands
- Topology: Point-to-point (one-to-one)
- Range: <15 meters without RS-232/RS-485 drivers
- Data rate: 9600 - 115200+ baud typical
- Orbit usage: Debug console, GPS modules

**BLE** - Wireless personal area network with low power
- Use when: Battery-powered wireless communication needed
- Topology: Star (central and peripherals)
- Range: ~10 meters indoors
- Data rate: ~1 Mbps (effective ~100 KB/s)
- Orbit usage: Presto ↔ Android app for notifications

**WiFi** - High-speed wireless networking
- Use when: Internet connectivity or high-bandwidth local network needed
- Topology: Star (access point and stations)
- Range: ~50 meters indoors
- Data rate: 54 Mbps - 1+ Gbps
- Orbit usage: All devices connect to home WiFi for MQTT access

## MQTT Implementation

### Broker Setup

For Orbit's Jetson Nano or any Linux-based MQTT broker, configure Mosquitto with both TCP (embedded devices) and WebSocket (web clients) support.

Reference the configuration template in `assets/mosquitto.conf` and apply it:

```bash
sudo cp assets/mosquitto.conf /etc/mosquitto/mosquitto.conf
sudo systemctl restart mosquitto
sudo systemctl enable mosquitto
```

Test the configuration:

```bash
# Test TCP listener (port 1883)
mosquitto_pub -h localhost -t test/topic -m "hello"

# Test WebSocket listener (port 9001)
# Requires mqtt.js or similar WebSocket MQTT client
node -e "const mqtt=require('mqtt'); const c=mqtt.connect('ws://localhost:9001'); c.on('connect',()=>{c.publish('test/topic','hello');c.end();})"
```

### Topic Design Patterns

Design topic hierarchies for clarity and scalability:

```
<project>/<category>/<action>/<target>

Examples:
orbit/timer/state/current          - Current timer state (retained)
orbit/timer/control/start          - Command to start timer
orbit/timer/control/pause          - Command to pause timer
orbit/device/presto/status         - Presto device status (retained)
orbit/device/tembed/battery        - T-Embed battery level
orbit/alert/visual/all             - Visual alert to all devices
orbit/alert/visual/presto          - Visual alert to specific device
orbit/metrics/focus/1234567890     - Focus metrics with timestamp
```

**Topic naming conventions:**
- Use lowercase with underscores or hyphens
- Structure hierarchically: general → specific
- Use `state` for current values (typically retained)
- Use `control` or `command` for actions
- Include device ID when targeting specific devices
- Add timestamp suffix for time-series data

### QoS Level Selection

Choose Quality of Service level based on message importance:

**QoS 0 (At most once)** - Fire and forget
- Use for: Frequent sensor updates, non-critical status
- Example: `orbit/device/presto/rssi` (WiFi signal strength)
- Trade-off: Lowest overhead, possible message loss

**QoS 1 (At least once)** - Acknowledged delivery
- Use for: Commands, important state changes, timer sync
- Example: `orbit/timer/control/start`, `orbit/timer/state/current`
- Trade-off: Guaranteed delivery, possible duplicates

**QoS 2 (Exactly once)** - Guaranteed single delivery
- Use for: Critical commands where duplicates cause problems
- Example: Payment transactions, irreversible actions
- Trade-off: Highest overhead, slowest delivery
- Note: Rarely needed in Orbit; QoS 1 is typically sufficient

### Retained Messages and Last Will

Use retained messages for state that new clients need immediately:

```python
# Publish retained message (state persists on broker)
client.publish("orbit/timer/state/current",
               json.dumps({"running": True, "remaining": 900}),
               qos=1,
               retain=True)

# New clients automatically receive last retained message
```

Configure Last Will and Testament for disconnect detection:

```python
# Set LWT when connecting
client.will_set("orbit/device/presto/status",
                json.dumps({"online": False}),
                qos=1,
                retain=True)

# On normal connection, publish online status
client.publish("orbit/device/presto/status",
               json.dumps({"online": True}),
               qos=1,
               retain=True)

# If connection lost, broker automatically publishes LWT
```

### Connection and Reconnection Strategy

Implement robust reconnection with exponential backoff. See `scripts/mqtt_connection.py` for a complete reference implementation.

Key principles:
1. **Clean Session vs Persistent Session**
   - Clean session (clean_start=True): Discard subscriptions on disconnect
   - Persistent session (clean_start=False): Maintain subscriptions and queue QoS 1/2 messages
   - Orbit: Use persistent sessions for devices, clean for short-lived clients

2. **Keep-Alive Interval**
   - Set to 60 seconds for stable networks
   - Set to 30 seconds for unreliable WiFi
   - Must send PING before interval expires to maintain connection

3. **Automatic Reconnection**
   - Implement exponential backoff: 1s, 2s, 4s, 8s... up to 60s
   - Reset backoff timer on successful connection
   - Queue messages locally during disconnection (with size limit)

4. **Connection State Handling**
   - Implement connection callbacks: on_connect, on_disconnect
   - Re-subscribe to topics in on_connect callback
   - Update UI/LEDs to show connection status
   - Log connection events for debugging

## I2C Protocol

### Master Configuration

Configure I2C master on ESP32 or RP2350:

```cpp
// ESP-IDF example
#include "driver/i2c.h"

#define I2C_MASTER_SCL_IO    22      // GPIO for SCL
#define I2C_MASTER_SDA_IO    21      // GPIO for SDA
#define I2C_MASTER_FREQ_HZ   100000  // 100 KHz standard mode

i2c_config_t conf = {
    .mode = I2C_MODE_MASTER,
    .sda_io_num = I2C_MASTER_SDA_IO,
    .scl_io_num = I2C_MASTER_SCL_IO,
    .sda_pullup_en = GPIO_PULLUP_ENABLE,
    .scl_pullup_en = GPIO_PULLUP_ENABLE,
    .master.clk_speed = I2C_MASTER_FREQ_HZ,
};

i2c_param_config(I2C_NUM_0, &conf);
i2c_driver_install(I2C_NUM_0, conf.mode, 0, 0, 0);
```

**Pull-up resistors**: Required for I2C operation
- Typical values: 2.2 KΩ - 10 KΩ
- Lower values (2.2 KΩ) for longer traces or higher capacitance
- Higher values (10 KΩ) for slower speeds or power savings
- Many development boards include onboard pull-ups

### Device Addressing

I2C uses 7-bit addressing (128 possible addresses):

```
Common I2C addresses:
0x68 - MPU-6050 (accelerometer/gyroscope)
0x76 or 0x77 - BMP280 (pressure/temperature)
0x3C or 0x3D - SSD1306 (OLED display)
0x48-0x4F - ADS1115 (ADC)

Special addresses:
0x00 - General call address
0x01-0x07 - Reserved
0x78-0x7F - Reserved
```

Scan for devices on the bus:

```cpp
for (uint8_t addr = 1; addr < 127; addr++) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (addr << 1) | I2C_MASTER_WRITE, true);
    i2c_master_stop(cmd);

    esp_err_t ret = i2c_master_cmd_begin(I2C_NUM_0, cmd, 50 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);

    if (ret == ESP_OK) {
        printf("Found device at 0x%02X\n", addr);
    }
}
```

### Reading Sensors

Reference implementation in `scripts/i2c_sensor.py` demonstrates reading from I2C sensors with proper error handling.

Basic I2C read transaction:

```cpp
esp_err_t i2c_read_sensor(uint8_t device_addr, uint8_t reg_addr,
                          uint8_t* data, size_t len) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();

    // Write register address
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (device_addr << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, reg_addr, true);

    // Read data
    i2c_master_start(cmd);  // Repeated start
    i2c_master_write_byte(cmd, (device_addr << 1) | I2C_MASTER_READ, true);
    i2c_master_read(cmd, data, len, I2C_MASTER_LAST_NACK);
    i2c_master_stop(cmd);

    esp_err_t ret = i2c_master_cmd_begin(I2C_NUM_0, cmd, 1000 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);

    return ret;
}
```

**Error handling:**
- Check return value for timeout or NACK
- Retry with exponential backoff on transient failures
- Reset bus on persistent failures
- Log errors with context (address, register, data)

## SPI Protocol

### Master Configuration

Configure SPI master for displays or high-speed peripherals:

```cpp
// ESP-IDF example for SPI display
#include "driver/spi_master.h"

#define PIN_MOSI  23
#define PIN_CLK   18
#define PIN_CS    5
#define PIN_DC    17  // Data/Command select
#define PIN_RST   16  // Reset

spi_bus_config_t bus_cfg = {
    .mosi_io_num = PIN_MOSI,
    .miso_io_num = -1,  // Not used for display
    .sclk_io_num = PIN_CLK,
    .quadwp_io_num = -1,
    .quadhd_io_num = -1,
    .max_transfer_sz = 320 * 240 * 2 + 8,  // Display buffer size
};

spi_device_interface_config_t dev_cfg = {
    .clock_speed_hz = 40 * 1000 * 1000,  // 40 MHz
    .mode = 0,  // SPI mode 0 (CPOL=0, CPHA=0)
    .spics_io_num = PIN_CS,
    .queue_size = 7,
    .pre_cb = nullptr,  // Pre-transfer callback
};

spi_bus_initialize(SPI2_HOST, &bus_cfg, SPI_DMA_CH_AUTO);
spi_bus_add_device(SPI2_HOST, &dev_cfg, &spi_handle);
```

### SPI Modes (CPOL and CPHA)

SPI has four modes based on clock polarity and phase:

```
Mode | CPOL | CPHA | Description
-----|------|------|--------------------------------------------------
0    | 0    | 0    | Data sampled on rising edge, shifted on falling
1    | 0    | 1    | Data sampled on falling edge, shifted on rising
2    | 1    | 0    | Data sampled on falling edge, shifted on rising
3    | 1    | 1    | Data sampled on rising edge, shifted on falling

Common devices:
- Most displays: Mode 0 or Mode 3
- SD cards: Mode 0
- MAX31855 thermocouple: Mode 0
```

Verify the correct mode in the datasheet - using the wrong mode causes garbled data.

### DMA Transfers

Use DMA for large data transfers to reduce CPU load:

```cpp
// Prepare transaction
spi_transaction_t trans = {
    .length = buffer_size * 8,  // Length in bits
    .tx_buffer = buffer,
    .rx_buffer = nullptr,
};

// Non-blocking DMA transfer
spi_device_queue_trans(spi_handle, &trans, portMAX_DELAY);

// Do other work while transfer happens...

// Wait for completion
spi_transaction_t* ret_trans;
spi_device_get_trans_result(spi_handle, &ret_trans, portMAX_DELAY);
```

**Performance considerations:**
- Use DMA for transfers >64 bytes
- Align buffers to 4-byte boundaries for DMA
- Queue multiple transactions to keep bus busy
- Consider double-buffering for continuous updates

See `scripts/spi_display.py` for a complete SPI display driver example.

## UART Protocol

### Configuration

Configure UART with proper frame format:

```cpp
// ESP-IDF example
#include "driver/uart.h"

#define UART_NUM      UART_NUM_1
#define TXD_PIN       17
#define RXD_PIN       16
#define BAUD_RATE     115200

uart_config_t uart_config = {
    .baud_rate = BAUD_RATE,
    .data_bits = UART_DATA_8_BITS,
    .parity = UART_PARITY_DISABLE,
    .stop_bits = UART_STOP_BITS_1,
    .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
};

uart_param_config(UART_NUM, &uart_config);
uart_set_pin(UART_NUM, TXD_PIN, RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
uart_driver_install(UART_NUM, 1024, 1024, 0, NULL, 0);
```

**Flow control:**
- None: Simple point-to-point, ensure receiver can keep up
- Software (XON/XOFF): Use when hardware flow control unavailable
- Hardware (RTS/CTS): Preferred for reliable high-speed communication

### AT Command Interface

Many modules (WiFi, BLE, GPS) use AT command interface. Reference `scripts/uart_parser.py` for a complete command parser with state machine.

Basic AT command handling:

```cpp
void send_at_command(const char* cmd, char* response, size_t max_len) {
    // Send command with CR+LF
    uart_write_bytes(UART_NUM, cmd, strlen(cmd));
    uart_write_bytes(UART_NUM, "\r\n", 2);

    // Read response with timeout
    int len = uart_read_bytes(UART_NUM, (uint8_t*)response,
                              max_len - 1, 1000 / portTICK_PERIOD_MS);
    response[len] = '\0';

    // Check for OK/ERROR
    if (strstr(response, "OK")) {
        // Success
    } else if (strstr(response, "ERROR")) {
        // Failed
    }
}
```

**AT command best practices:**
- Wait for "OK" before sending next command
- Implement timeout for each command
- Handle unsolicited responses (events)
- Buffer partial lines until CR+LF received
- Use state machine for complex command sequences

## BLE Protocol

### GATT Server Structure

Design GATT services with characteristics for each data type:

```
Service: Timer Control (UUID: custom)
├── Characteristic: State (UUID: 0x2A00)
│   ├── Properties: Read, Notify
│   ├── Value: {"running": bool, "remaining": uint32}
│   └── Descriptor: CCCD (0x2902) for notifications
├── Characteristic: Command (UUID: 0x2A01)
│   ├── Properties: Write
│   └── Value: {"action": "start"|"pause"|"reset", "duration": uint32}
└── Characteristic: Battery (UUID: 0x2A19)
    ├── Properties: Read, Notify
    └── Value: uint8 (percentage)
```

### Connection Parameters

Optimize connection intervals for use case:

```cpp
// Fast updates (timer display): 20ms - 40ms interval
// Power saving (idle): 200ms - 400ms interval

ble_gap_conn_params_t conn_params = {
    .min_conn_interval = 16,  // 16 * 1.25ms = 20ms
    .max_conn_interval = 32,  // 32 * 1.25ms = 40ms
    .slave_latency = 0,       // No latency for real-time updates
    .conn_sup_timeout = 400,  // 400 * 10ms = 4s timeout
};
```

**Trade-offs:**
- Faster intervals: Lower latency, higher power consumption
- Slower intervals: Longer latency, better battery life
- Slave latency: Skip N intervals to save power (adds latency)

### Notifications vs Indications

Choose the appropriate characteristic property:

**Notifications** (unacknowledged)
- Use for: Frequent sensor updates, timer ticks
- Advantage: Lower overhead, higher throughput
- Disadvantage: No delivery guarantee

**Indications** (acknowledged)
- Use for: Important commands, critical state changes
- Advantage: Guaranteed delivery with acknowledgment
- Disadvantage: Higher overhead, lower throughput

Reference `scripts/ble_gatt_server.py` for a complete BLE GATT server implementation.

## WiFi Integration

### Connection Management

Implement robust WiFi connection with automatic reconnection:

```cpp
// ESP-IDF example
void wifi_init() {
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);

    esp_event_handler_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &event_handler, NULL);
    esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &event_handler, NULL);

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };

    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);
    esp_wifi_start();
}

void event_handler(void* arg, esp_event_base_t event_base,
                   int32_t event_id, void* event_data) {
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        esp_wifi_connect();  // Auto-reconnect
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        // Connected - start MQTT client
    }
}
```

### mDNS Service Discovery

Use mDNS to discover MQTT broker without hardcoded IP:

```cpp
// Advertise MQTT broker (Jetson)
mdns_init();
mdns_hostname_set("orbit-broker");
mdns_service_add("Orbit MQTT", "_mqtt", "_tcp", 1883, NULL, 0);

// Discover MQTT broker (devices)
mdns_result_t* results = NULL;
esp_err_t err = mdns_query_ptr("_mqtt", "_tcp", 3000, 20, &results);

if (err == ESP_OK && results) {
    mdns_result_t* r = results;
    while (r) {
        printf("Found MQTT broker: %s at %s:%d\n",
               r->hostname, ip4addr_ntoa(&r->addr->addr.u_addr.ip4), r->port);
        r = r->next;
    }
    mdns_query_results_free(results);
}
```

## Orbit System Integration

### Device Communication Architecture

```
                    ┌─────────────────┐
                    │  Jetson Nano    │
                    │  MQTT Broker    │
                    │  (Mosquitto)    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
  WiFi (MQTT)          WiFi (MQTT)          WiFi (MQTT)
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
│ Presto (RP2350)│  │ T-Embed (ESP32) │  │  Stream Deck   │
│  SPI Display   │  │  SPI Display    │  │   (WebSocket)  │
│  BLE Server    │  │  I2C Sensors    │  │                │
└───────┬────────┘  └─────────────────┘  └────────────────┘
        │
   BLE (GATT)
        │
┌───────▼────────┐
│  Android App   │
│  BLE Client    │
└────────────────┘
```

### Message Flow Examples

**Timer Start from Stream Deck:**
1. User presses Stream Deck button
2. Plugin publishes: `orbit/timer/control/start` with `{"duration": 1500}`
3. Jetson receives and broadcasts: `orbit/timer/state/current` (retained)
4. All devices receive state update and display timer
5. Presto sends BLE notification to Android app

**Visual Alert:**
1. Jetson detects timer completion
2. Publishes: `orbit/alert/visual/all` with `{"priority": "standard", "pattern": "pulse"}`
3. Presto and T-Embed display visual alerts
4. Devices acknowledge: `orbit/device/{id}/ack`

**Battery Level Monitoring:**
1. T-Embed periodically checks battery via I2C fuel gauge
2. Publishes: `orbit/device/tembed/battery` with percentage
3. Jetson logs metric and checks threshold
4. If low: `orbit/alert/visual/tembed` with low battery warning

## Troubleshooting

### MQTT Issues

**Connection refused:**
- Check firewall: `sudo ufw allow 1883` and `sudo ufw allow 9001`
- Verify broker running: `sudo systemctl status mosquitto`
- Check logs: `sudo journalctl -u mosquitto -f`

**Messages not received:**
- Verify topic spelling (case-sensitive)
- Check QoS level and subscription
- Monitor with: `mosquitto_sub -h localhost -t '#' -v` (all topics)

**WebSocket connection fails:**
- Verify WebSocket listener in mosquitto.conf
- Test with: `wscat -c ws://broker-ip:9001/mqtt`
- Check CORS if from browser

### I2C Issues

**Device not detected:**
- Check wiring: SDA/SCL not swapped
- Verify pull-up resistors present (2.2K - 10K)
- Scan bus: Use I2C scanner code above
- Check device address in datasheet (some have configurable bits)

**Timeout or NACK:**
- Reduce clock speed (try 100 KHz)
- Check power supply to device
- Verify device is ready (some need initialization delay)
- Check for bus contention (multiple masters)

### SPI Issues

**Garbled data:**
- Verify SPI mode (CPOL/CPHA)
- Check clock speed (try slower)
- Confirm MISO/MOSI not swapped
- Verify CS timing (some devices need delay)

**No response:**
- Check chip select (active low typically)
- Verify device powered
- Check MOSI/CLK signals with logic analyzer
- Some devices need initialization sequence

### BLE Issues

**Connection drops:**
- Increase connection timeout
- Reduce connection interval
- Check for RF interference
- Verify power supply stable

**Cannot discover device:**
- Check advertising interval and window
- Verify device name/UUID
- Check iOS/Android BLE permissions
- Scan longer or restart Bluetooth

### WiFi Issues

**Cannot connect:**
- Verify SSID and password
- Check WiFi band (2.4 GHz vs 5 GHz)
- Try static IP if DHCP fails
- Check router firewall/MAC filtering

**Frequent disconnections:**
- Reduce WiFi power saving
- Improve signal strength (closer to AP)
- Check for channel congestion
- Use WiFi analyzer to find better channel

## Bundled Resources

### scripts/

Executable reference implementations:
- `mqtt_connection.py` - MQTT client with robust reconnection logic
- `ble_gatt_server.py` - BLE GATT server with services and characteristics
- `i2c_sensor.py` - I2C sensor reading with error handling
- `spi_display.py` - SPI display driver with DMA
- `uart_parser.py` - UART command parser with state machine

These can be executed directly or adapted for specific hardware platforms.

### references/

Detailed protocol documentation:
- `mqtt_reference.md` - Complete MQTT protocol specification and patterns
- `embedded_bus_protocols.md` - I2C, SPI, UART detailed specs
- `wireless_protocols.md` - BLE and WiFi comprehensive guides
- `orbit_integration.md` - Orbit-specific integration patterns and topic schemas

Load these references when deep protocol knowledge is needed.

### assets/

Configuration templates:
- `mosquitto.conf` - Production-ready Mosquitto configuration (TCP + WebSocket)
- `platformio_examples/` - PlatformIO project configurations for ESP32 and RP2350

Copy these templates to projects and customize as needed.
