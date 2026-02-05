---
name: esp32-embedded-dev
description: Expert ESP32 development with ESP-IDF 5.3.x, covering FreeRTOS patterns, peripheral drivers, WiFi/BLE networking, power management, and hardware optimization. Use when developing ESP32 firmware, implementing FreeRTOS tasks, configuring WiFi/BLE, optimizing memory and power, or working with ESP32-S3 hardware like T-Embed.
---

# ESP32 Embedded Development

## Overview

Provides comprehensive ESP-IDF 5.3.x development guidance for ESP32/ESP32-S3 microcontrollers, covering real-time operating system patterns, wireless networking, peripheral drivers, and production-grade firmware development.

**Use this skill when:**
- Developing ESP32/ESP32-S3 firmware with ESP-IDF framework
- Implementing FreeRTOS tasks, queues, semaphores, or mutexes
- Configuring WiFi station/AP modes or BLE GATT services
- Integrating MQTT over WiFi/WebSocket
- Working with SPI, I2C, UART, GPIO, ADC, or PWM peripherals
- Optimizing power consumption with sleep modes
- Implementing OTA firmware updates
- Debugging memory issues or optimizing flash/RAM usage
- Working with T-Embed hardware (ESP32-S3, 1.9" display, rotary encoder, RGB LEDs)

## Quick Start

### Project Structure

ESP-IDF projects follow this standard structure:

```
project/
├── main/
│   ├── CMakeLists.txt
│   ├── main.c (or .cpp)
│   └── Kconfig.projbuild (optional)
├── components/
│   └── custom_component/
│       ├── CMakeLists.txt
│       ├── include/
│       └── src/
├── CMakeLists.txt
├── sdkconfig
└── partitions.csv (optional)
```

### Essential idf.py Commands

```bash
# Set target chip
idf.py set-target esp32s3

# Configure project (menuconfig)
idf.py menuconfig

# Build project
idf.py build

# Flash and monitor
idf.py -p /dev/ttyUSB0 flash monitor

# Clean build
idf.py fullclean

# Size analysis
idf.py size-components
idf.py size-files
```

### Component Registration

```cmake
# components/my_component/CMakeLists.txt
idf_component_register(
    SRCS "src/my_component.c"
    INCLUDE_DIRS "include"
    REQUIRES driver nvs_flash esp_wifi
)
```

## FreeRTOS Task Management

### Task Creation Patterns

```c
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "freertos/semphr.h"

// Task priorities (0 = lowest, configMAX_PRIORITIES-1 = highest)
// ESP-IDF reserves priority 19+ for system tasks
#define NETWORK_TASK_PRIORITY    5  // Network tasks
#define DISPLAY_TASK_PRIORITY    4  // UI updates
#define SENSOR_TASK_PRIORITY     3  // Sensor reading
#define LED_TASK_PRIORITY        2  // LED animations
#define IDLE_TASK_PRIORITY       1  // Background tasks

// Recommended stack sizes
#define NETWORK_STACK_SIZE  4096  // Network/MQTT tasks
#define DISPLAY_STACK_SIZE  3072  // Display rendering
#define SENSOR_STACK_SIZE   2048  // Sensor tasks
#define LED_STACK_SIZE      2048  // LED control

// Task handle for later control
static TaskHandle_t display_task_handle = NULL;

void display_task(void *pvParameters) {
    TickType_t last_wake_time = xTaskGetTickCount();
    const TickType_t frequency = pdMS_TO_TICKS(33); // 30 FPS

    while (1) {
        // Update display
        update_display();

        // Delay until next frame (absolute timing)
        vTaskDelayUntil(&last_wake_time, frequency);
    }
}

// Create task pinned to specific core (ESP32-S3 has 2 cores)
xTaskCreatePinnedToCore(
    display_task,           // Task function
    "display_task",         // Name
    DISPLAY_STACK_SIZE,     // Stack size
    NULL,                   // Parameters
    DISPLAY_TASK_PRIORITY,  // Priority
    &display_task_handle,   // Task handle
    1                       // Core ID (0 or 1, or tskNO_AFFINITY)
);
```

### Queue Communication

```c
// Create queue (typically as global or passed via parameters)
static QueueHandle_t event_queue = NULL;

typedef struct {
    uint8_t event_type;
    uint32_t value;
    uint64_t timestamp;
} event_data_t;

void init_queues(void) {
    event_queue = xQueueCreate(10, sizeof(event_data_t));
    if (event_queue == NULL) {
        ESP_LOGE("INIT", "Failed to create event queue");
    }
}

// Producer task
void sensor_task(void *pvParameters) {
    event_data_t event;

    while (1) {
        event.event_type = SENSOR_EVENT;
        event.value = read_sensor();
        event.timestamp = esp_timer_get_time();

        // Send to queue (wait up to 100ms if full)
        if (xQueueSend(event_queue, &event, pdMS_TO_TICKS(100)) != pdPASS) {
            ESP_LOGW("SENSOR", "Queue full, event dropped");
        }

        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

// Consumer task
void processing_task(void *pvParameters) {
    event_data_t event;

    while (1) {
        // Wait indefinitely for event
        if (xQueueReceive(event_queue, &event, portMAX_DELAY) == pdPASS) {
            process_event(&event);
        }
    }
}
```

### Mutex and Semaphore Patterns

```c
// Mutex for protecting shared resources
static SemaphoreHandle_t i2c_mutex = NULL;

void init_synchronization(void) {
    i2c_mutex = xSemaphoreCreateMutex();
}

esp_err_t safe_i2c_read(uint8_t addr, uint8_t *data, size_t len) {
    esp_err_t ret = ESP_FAIL;

    // Take mutex (wait up to 1 second)
    if (xSemaphoreTake(i2c_mutex, pdMS_TO_TICKS(1000)) == pdTRUE) {
        ret = i2c_master_read_from_device(I2C_NUM_0, addr, data, len, pdMS_TO_TICKS(100));
        xSemaphoreGive(i2c_mutex);
    } else {
        ESP_LOGE("I2C", "Failed to acquire mutex");
    }

    return ret;
}

// Binary semaphore for task synchronization
static SemaphoreHandle_t sync_semaphore = NULL;

void init_sync(void) {
    sync_semaphore = xSemaphoreCreateBinary();
}

// ISR gives semaphore
void IRAM_ATTR gpio_isr_handler(void *arg) {
    BaseType_t higher_priority_task_woken = pdFALSE;
    xSemaphoreGiveFromISR(sync_semaphore, &higher_priority_task_woken);

    if (higher_priority_task_woken) {
        portYIELD_FROM_ISR();
    }
}

// Task waits for semaphore
void event_handler_task(void *pvParameters) {
    while (1) {
        if (xSemaphoreTake(sync_semaphore, portMAX_DELAY) == pdTRUE) {
            handle_interrupt_event();
        }
    }
}
```

## WiFi & BLE Networking

### WiFi Station Mode (Complete Example)

```c
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_netif.h"
#include "nvs_flash.h"

#define WIFI_SSID      "your_ssid"
#define WIFI_PASSWORD  "your_password"
#define MAX_RETRY      5

static EventGroupHandle_t wifi_event_group;
static const int WIFI_CONNECTED_BIT = BIT0;
static const int WIFI_FAIL_BIT = BIT1;
static int retry_count = 0;

static void wifi_event_handler(void *arg, esp_event_base_t event_base,
                               int32_t event_id, void *event_data) {
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
        ESP_LOGI("WIFI", "Station started, connecting...");
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        if (retry_count < MAX_RETRY) {
            esp_wifi_connect();
            retry_count++;
            ESP_LOGI("WIFI", "Retry connection %d/%d", retry_count, MAX_RETRY);
        } else {
            xEventGroupSetBits(wifi_event_group, WIFI_FAIL_BIT);
            ESP_LOGE("WIFI", "Failed to connect after %d retries", MAX_RETRY);
        }
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t *event = (ip_event_got_ip_t *)event_data;
        ESP_LOGI("WIFI", "Got IP: " IPSTR, IP2STR(&event->ip_info.ip));
        retry_count = 0;
        xEventGroupSetBits(wifi_event_group, WIFI_CONNECTED_BIT);
    }
}

esp_err_t wifi_init_sta(void) {
    wifi_event_group = xEventGroupCreate();

    // Initialize network interface
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    // WiFi configuration
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    // Register event handlers
    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        WIFI_EVENT, ESP_EVENT_ANY_ID, &wifi_event_handler, NULL, NULL));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        IP_EVENT, IP_EVENT_STA_GOT_IP, &wifi_event_handler, NULL, NULL));

    // Configure WiFi
    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASSWORD,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
            .pmf_cfg = {
                .capable = true,
                .required = false
            },
        },
    };

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    // Wait for connection or failure
    EventBits_t bits = xEventGroupWaitBits(wifi_event_group,
        WIFI_CONNECTED_BIT | WIFI_FAIL_BIT, pdFALSE, pdFALSE, portMAX_DELAY);

    if (bits & WIFI_CONNECTED_BIT) {
        ESP_LOGI("WIFI", "Connected successfully");
        return ESP_OK;
    } else {
        ESP_LOGE("WIFI", "Connection failed");
        return ESP_FAIL;
    }
}
```

### BLE GATT Server Example

```c
#include "esp_bt.h"
#include "esp_gap_ble_api.h"
#include "esp_gatts_api.h"
#include "esp_bt_main.h"

#define GATTS_SERVICE_UUID   0x00FF
#define GATTS_CHAR_UUID      0xFF01
#define GATTS_NUM_HANDLE     4

static uint8_t service_uuid[16] = {
    0xfb, 0x34, 0x9b, 0x5f, 0x80, 0x00, 0x00, 0x80,
    0x00, 0x10, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00,
};

static esp_gatt_char_prop_t char_property =
    ESP_GATT_CHAR_PROP_BIT_READ |
    ESP_GATT_CHAR_PROP_BIT_WRITE |
    ESP_GATT_CHAR_PROP_BIT_NOTIFY;

static uint8_t char_value[20] = {0};

static void gatts_event_handler(esp_gatts_cb_event_t event,
                               esp_gatt_if_t gatts_if,
                               esp_ble_gatts_cb_param_t *param) {
    switch (event) {
        case ESP_GATTS_REG_EVT:
            ESP_LOGI("BLE", "GATT server registered, status %d", param->reg.status);

            esp_ble_gap_set_device_name("ESP32_TIMER");

            esp_ble_gap_config_adv_data_raw(adv_data, sizeof(adv_data));

            esp_ble_gatts_create_service(gatts_if, &service_id, GATTS_NUM_HANDLE);
            break;

        case ESP_GATTS_WRITE_EVT:
            ESP_LOGI("BLE", "Write event, value length %d", param->write.len);
            if (param->write.len <= sizeof(char_value)) {
                memcpy(char_value, param->write.value, param->write.len);
                // Process received data
                handle_ble_command(char_value, param->write.len);
            }

            // Send response if needed
            if (param->write.need_rsp) {
                esp_ble_gatts_send_response(gatts_if, param->write.conn_id,
                                           param->write.trans_id, ESP_GATT_OK, NULL);
            }
            break;

        case ESP_GATTS_READ_EVT:
            ESP_LOGI("BLE", "Read event");
            esp_gatt_rsp_t rsp;
            memset(&rsp, 0, sizeof(esp_gatt_rsp_t));
            rsp.attr_value.handle = param->read.handle;
            rsp.attr_value.len = sizeof(char_value);
            memcpy(rsp.attr_value.value, char_value, sizeof(char_value));

            esp_ble_gatts_send_response(gatts_if, param->read.conn_id,
                                       param->read.trans_id, ESP_GATT_OK, &rsp);
            break;

        default:
            break;
    }
}

esp_err_t ble_init(void) {
    esp_err_t ret;

    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT));

    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    ret = esp_bt_controller_init(&bt_cfg);
    if (ret) {
        ESP_LOGE("BLE", "Bluetooth controller init failed");
        return ret;
    }

    ret = esp_bt_controller_enable(ESP_BT_MODE_BLE);
    if (ret) {
        ESP_LOGE("BLE", "Bluetooth controller enable failed");
        return ret;
    }

    ret = esp_bluedroid_init();
    if (ret) {
        ESP_LOGE("BLE", "Bluedroid init failed");
        return ret;
    }

    ret = esp_bluedroid_enable();
    if (ret) {
        ESP_LOGE("BLE", "Bluedroid enable failed");
        return ret;
    }

    esp_ble_gatts_register_callback(gatts_event_handler);
    esp_ble_gatts_app_register(0);

    return ESP_OK;
}
```

## MQTT Integration

### MQTT Client with WiFi (esp-mqtt)

```c
#include "mqtt_client.h"

static esp_mqtt_client_handle_t mqtt_client = NULL;

static void mqtt_event_handler(void *handler_args, esp_event_base_t base,
                               int32_t event_id, void *event_data) {
    esp_mqtt_event_handle_t event = (esp_mqtt_event_handle_t)event_data;

    switch ((esp_mqtt_event_id_t)event_id) {
        case MQTT_EVENT_CONNECTED:
            ESP_LOGI("MQTT", "Connected to broker");

            // Subscribe to topics
            esp_mqtt_client_subscribe(mqtt_client, "productivity/timer/control/#", 1);
            esp_mqtt_client_subscribe(mqtt_client, "productivity/alert/visual/#", 1);

            // Publish online status
            esp_mqtt_client_publish(mqtt_client, "productivity/device/status",
                                   "online", 0, 1, 1);
            break;

        case MQTT_EVENT_DISCONNECTED:
            ESP_LOGW("MQTT", "Disconnected from broker");
            break;

        case MQTT_EVENT_DATA:
            ESP_LOGI("MQTT", "Received: %.*s = %.*s",
                    event->topic_len, event->topic,
                    event->data_len, event->data);

            // Route message to handler
            handle_mqtt_message(event->topic, event->topic_len,
                              event->data, event->data_len);
            break;

        case MQTT_EVENT_ERROR:
            ESP_LOGE("MQTT", "Error: type=%d", event->error_handle->error_type);
            break;

        default:
            break;
    }
}

esp_err_t mqtt_init(void) {
    // MQTT configuration
    esp_mqtt_client_config_t mqtt_cfg = {
        .broker.address.uri = "mqtt://192.168.1.100:1883",  // TCP MQTT
        .credentials.client_id = "esp32_tembed",
        .session.keepalive = 60,
        .network.reconnect_timeout_ms = 5000,
        .network.disable_auto_reconnect = false,
    };

    mqtt_client = esp_mqtt_client_init(&mqtt_cfg);
    if (mqtt_client == NULL) {
        ESP_LOGE("MQTT", "Failed to initialize client");
        return ESP_FAIL;
    }

    esp_mqtt_client_register_event(mqtt_client, ESP_EVENT_ANY_ID,
                                   mqtt_event_handler, NULL);

    esp_err_t ret = esp_mqtt_client_start(mqtt_client);
    if (ret != ESP_OK) {
        ESP_LOGE("MQTT", "Failed to start client");
    }

    return ret;
}

// Publish with QoS
void mqtt_publish_timer_state(uint32_t remaining_seconds) {
    char payload[64];
    snprintf(payload, sizeof(payload),
             "{\"remaining\":%lu,\"timestamp\":%llu}",
             remaining_seconds, esp_timer_get_time() / 1000000);

    esp_mqtt_client_publish(mqtt_client,
                           "productivity/timer/state/current",
                           payload, 0, 1, 0);  // QoS 1, no retain
}
```

## Peripheral Drivers

### SPI Display Driver Pattern

```c
#include "driver/spi_master.h"
#include "driver/gpio.h"

#define LCD_HOST       SPI2_HOST
#define LCD_MOSI_PIN   GPIO_NUM_35
#define LCD_SCLK_PIN   GPIO_NUM_36
#define LCD_CS_PIN     GPIO_NUM_37
#define LCD_DC_PIN     GPIO_NUM_34
#define LCD_RST_PIN    GPIO_NUM_38
#define LCD_BL_PIN     GPIO_NUM_33

static spi_device_handle_t spi_device;

esp_err_t lcd_spi_init(void) {
    // Configure GPIO
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << LCD_DC_PIN) | (1ULL << LCD_RST_PIN) | (1ULL << LCD_BL_PIN),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&io_conf);

    // SPI bus configuration
    spi_bus_config_t buscfg = {
        .mosi_io_num = LCD_MOSI_PIN,
        .miso_io_num = -1,  // Display only (no MISO)
        .sclk_io_num = LCD_SCLK_PIN,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = 320 * 240 * 2 + 8,  // Full screen buffer + overhead
    };

    ESP_ERROR_CHECK(spi_bus_initialize(LCD_HOST, &buscfg, SPI_DMA_CH_AUTO));

    // SPI device configuration
    spi_device_interface_config_t devcfg = {
        .clock_speed_hz = 40 * 1000 * 1000,  // 40 MHz
        .mode = 0,
        .spics_io_num = LCD_CS_PIN,
        .queue_size = 7,
        .pre_cb = NULL,
        .post_cb = NULL,
    };

    ESP_ERROR_CHECK(spi_bus_add_device(LCD_HOST, &devcfg, &spi_device));

    // Reset display
    gpio_set_level(LCD_RST_PIN, 0);
    vTaskDelay(pdMS_TO_TICKS(100));
    gpio_set_level(LCD_RST_PIN, 1);
    vTaskDelay(pdMS_TO_TICKS(100));

    return ESP_OK;
}

void lcd_send_cmd(uint8_t cmd) {
    spi_transaction_t t = {
        .length = 8,
        .tx_buffer = &cmd,
        .user = (void *)0,  // D/C = 0 for command
    };
    gpio_set_level(LCD_DC_PIN, 0);
    spi_device_polling_transmit(spi_device, &t);
}

void lcd_send_data(const uint8_t *data, size_t len) {
    if (len == 0) return;

    spi_transaction_t t = {
        .length = len * 8,
        .tx_buffer = data,
        .user = (void *)1,  // D/C = 1 for data
    };
    gpio_set_level(LCD_DC_PIN, 1);
    spi_device_polling_transmit(spi_device, &t);
}

// DMA transfer for large buffers (non-blocking)
void lcd_send_framebuffer(const uint16_t *buffer, size_t pixel_count) {
    static spi_transaction_t trans[6];
    static int trans_in_flight = 0;

    // Wait for previous transactions to complete
    while (trans_in_flight) {
        spi_transaction_t *rtrans;
        spi_device_get_trans_result(spi_device, &rtrans, portMAX_DELAY);
        trans_in_flight--;
    }

    gpio_set_level(LCD_DC_PIN, 1);

    // Queue transaction
    trans[0].length = pixel_count * 16;
    trans[0].tx_buffer = buffer;
    spi_device_queue_trans(spi_device, &trans[0], portMAX_DELAY);
    trans_in_flight++;
}
```

### I2C Sensor Reading

```c
#include "driver/i2c.h"

#define I2C_MASTER_NUM      I2C_NUM_0
#define I2C_MASTER_SDA      GPIO_NUM_21
#define I2C_MASTER_SCL      GPIO_NUM_22
#define I2C_MASTER_FREQ_HZ  400000

esp_err_t i2c_master_init(void) {
    i2c_config_t conf = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = I2C_MASTER_SDA,
        .scl_io_num = I2C_MASTER_SCL,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = I2C_MASTER_FREQ_HZ,
    };

    ESP_ERROR_CHECK(i2c_param_config(I2C_MASTER_NUM, &conf));
    return i2c_driver_install(I2C_MASTER_NUM, conf.mode, 0, 0, 0);
}

// Read sensor register
esp_err_t sensor_read_register(uint8_t sensor_addr, uint8_t reg_addr,
                               uint8_t *data, size_t len) {
    return i2c_master_write_read_device(I2C_MASTER_NUM, sensor_addr,
                                       &reg_addr, 1, data, len,
                                       pdMS_TO_TICKS(1000));
}
```

### GPIO Interrupt with Debouncing (Rotary Encoder)

```c
#include "driver/gpio.h"

#define ROTARY_A_PIN    GPIO_NUM_3
#define ROTARY_B_PIN    GPIO_NUM_46
#define ROTARY_BTN_PIN  GPIO_NUM_0

static volatile int32_t encoder_count = 0;
static SemaphoreHandle_t encoder_mutex;

void IRAM_ATTR rotary_isr_handler(void *arg) {
    static uint8_t last_state = 0;
    static int64_t last_interrupt_time = 0;

    // Debounce: 1ms
    int64_t now = esp_timer_get_time();
    if ((now - last_interrupt_time) < 1000) {
        return;
    }
    last_interrupt_time = now;

    uint8_t a = gpio_get_level(ROTARY_A_PIN);
    uint8_t b = gpio_get_level(ROTARY_B_PIN);
    uint8_t state = (a << 1) | b;

    // Quadrature decoding
    int8_t dir = 0;
    if (last_state == 0b00 && state == 0b01) dir = 1;
    else if (last_state == 0b01 && state == 0b11) dir = 1;
    else if (last_state == 0b11 && state == 0b10) dir = 1;
    else if (last_state == 0b10 && state == 0b00) dir = 1;
    else if (last_state == 0b00 && state == 0b10) dir = -1;
    else if (last_state == 0b10 && state == 0b11) dir = -1;
    else if (last_state == 0b11 && state == 0b01) dir = -1;
    else if (last_state == 0b01 && state == 0b00) dir = -1;

    encoder_count += dir;
    last_state = state;
}

esp_err_t rotary_encoder_init(void) {
    encoder_mutex = xSemaphoreCreateMutex();

    // Configure GPIO
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << ROTARY_A_PIN) | (1ULL << ROTARY_B_PIN),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .intr_type = GPIO_INTR_ANYEDGE,
    };
    gpio_config(&io_conf);

    // Install ISR service
    gpio_install_isr_service(0);
    gpio_isr_handler_add(ROTARY_A_PIN, rotary_isr_handler, NULL);
    gpio_isr_handler_add(ROTARY_B_PIN, rotary_isr_handler, NULL);

    return ESP_OK;
}

int32_t rotary_encoder_get_count(void) {
    int32_t count;
    xSemaphoreTake(encoder_mutex, portMAX_DELAY);
    count = encoder_count;
    xSemaphoreGive(encoder_mutex);
    return count;
}
```

### WS2812B RGB LED Control (RMT)

```c
#include "driver/rmt_tx.h"
#include "led_strip_encoder.h"

#define LED_GPIO        GPIO_NUM_4
#define LED_COUNT       8
#define LED_RMT_RES_HZ  (10 * 1000 * 1000)  // 10 MHz

static rmt_channel_handle_t led_chan = NULL;
static rmt_encoder_handle_t led_encoder = NULL;

typedef struct {
    uint8_t g;
    uint8_t r;
    uint8_t b;
} rgb_t;

esp_err_t ws2812_init(void) {
    // RMT TX channel config
    rmt_tx_channel_config_t tx_chan_config = {
        .clk_src = RMT_CLK_SRC_DEFAULT,
        .gpio_num = LED_GPIO,
        .mem_block_symbols = 64,
        .resolution_hz = LED_RMT_RES_HZ,
        .trans_queue_depth = 4,
    };
    ESP_ERROR_CHECK(rmt_new_tx_channel(&tx_chan_config, &led_chan));

    // LED strip encoder
    led_strip_encoder_config_t encoder_config = {
        .resolution = LED_RMT_RES_HZ,
    };
    ESP_ERROR_CHECK(rmt_new_led_strip_encoder(&encoder_config, &led_encoder));

    ESP_ERROR_CHECK(rmt_enable(led_chan));

    return ESP_OK;
}

void ws2812_set_colors(const rgb_t *colors, size_t count) {
    rmt_transmit_config_t tx_config = {
        .loop_count = 0,
    };

    ESP_ERROR_CHECK(rmt_transmit(led_chan, led_encoder, colors,
                                 count * sizeof(rgb_t), &tx_config));
}

// Example: Smooth color transition
void led_breathe_effect(void) {
    rgb_t leds[LED_COUNT];

    for (int brightness = 0; brightness < 255; brightness += 5) {
        for (int i = 0; i < LED_COUNT; i++) {
            leds[i].r = brightness;
            leds[i].g = 0;
            leds[i].b = brightness / 2;
        }
        ws2812_set_colors(leds, LED_COUNT);
        vTaskDelay(pdMS_TO_TICKS(20));
    }
}
```

## Power Management

### Deep Sleep with Wake Sources

```c
#include "esp_sleep.h"
#include "driver/rtc_io.h"

// Configure deep sleep with multiple wake sources
void enter_deep_sleep(uint32_t sleep_seconds) {
    ESP_LOGI("POWER", "Entering deep sleep for %lu seconds", sleep_seconds);

    // Timer wake
    esp_sleep_enable_timer_wakeup(sleep_seconds * 1000000ULL);

    // GPIO wake (button press on GPIO0)
    esp_sleep_enable_ext0_wakeup(GPIO_NUM_0, 0);  // Wake on LOW

    // GPIO wake (any of multiple pins)
    const uint64_t ext1_mask = (1ULL << GPIO_NUM_1) | (1ULL << GPIO_NUM_2);
    esp_sleep_enable_ext1_wakeup(ext1_mask, ESP_EXT1_WAKEUP_ANY_HIGH);

    // Disable WiFi/BT before sleep
    esp_wifi_stop();
    esp_bluedroid_disable();
    esp_bt_controller_disable();

    // Enter deep sleep
    esp_deep_sleep_start();
}

// Check wake cause on boot
void check_wake_cause(void) {
    esp_sleep_wakeup_cause_t cause = esp_sleep_get_wakeup_cause();

    switch (cause) {
        case ESP_SLEEP_WAKEUP_TIMER:
            ESP_LOGI("POWER", "Woke from timer");
            break;
        case ESP_SLEEP_WAKEUP_EXT0:
            ESP_LOGI("POWER", "Woke from EXT0 (button)");
            break;
        case ESP_SLEEP_WAKEUP_EXT1:
            ESP_LOGI("POWER", "Woke from EXT1, pins: 0x%llx",
                    esp_sleep_get_ext1_wakeup_status());
            break;
        default:
            ESP_LOGI("POWER", "Power-on reset");
            break;
    }
}
```

### Light Sleep for Power Saving

```c
// Enter light sleep (wakes on GPIO or timer)
void enter_light_sleep(uint32_t sleep_ms) {
    esp_sleep_enable_timer_wakeup(sleep_ms * 1000);
    esp_sleep_enable_gpio_wakeup();

    ESP_LOGI("POWER", "Entering light sleep");
    esp_light_sleep_start();
    ESP_LOGI("POWER", "Woke from light sleep");
}

// Automatic light sleep (modem sleep)
void enable_auto_light_sleep(void) {
    // Automatically enter light sleep when idle
    esp_pm_config_t pm_config = {
        .max_freq_mhz = 240,
        .min_freq_mhz = 80,
        .light_sleep_enable = true,
    };
    ESP_ERROR_CHECK(esp_pm_configure(&pm_config));
}
```

## Memory Optimization

### Flash vs RAM Placement

```c
// Store constant data in flash (saves RAM)
static const uint8_t DRAM_ATTR lookup_table[256] = { /* ... */ };

// Keep frequently accessed data in RAM
static DRAM_ATTR uint8_t frame_buffer[320 * 240 * 2];

// Place ISR code in IRAM for fast access
void IRAM_ATTR gpio_fast_isr(void *arg) {
    // Time-critical interrupt code
}

// Place large read-only data in flash
static const char TAG[] = "MAIN";  // Automatically in flash

// Explicitly place string in flash
ESP_LOGI(TAG, "This string is in flash");
```

### Memory Monitoring

```c
void print_memory_info(void) {
    ESP_LOGI("MEM", "Free heap: %lu bytes", esp_get_free_heap_size());
    ESP_LOGI("MEM", "Minimum free heap: %lu bytes", esp_get_minimum_free_heap_size());
    ESP_LOGI("MEM", "Largest free block: %lu bytes", heap_caps_get_largest_free_block(MALLOC_CAP_8BIT));

    // PSRAM info (ESP32-S3 can have external PSRAM)
    ESP_LOGI("MEM", "Free PSRAM: %lu bytes", heap_caps_get_free_size(MALLOC_CAP_SPIRAM));
}

// Allocate from PSRAM if available
void *buffer = heap_caps_malloc(1024 * 1024, MALLOC_CAP_SPIRAM);
if (buffer == NULL) {
    ESP_LOGE("MEM", "Failed to allocate PSRAM");
}
```

### Custom Partition Tables

```csv
# partitions.csv - Optimize flash layout
# Name,   Type, SubType, Offset,  Size,     Flags
nvs,      data, nvs,     0x9000,  0x4000,
otadata,  data, ota,     0xd000,  0x2000,
phy_init, data, phy,     0xf000,  0x1000,
factory,  app,  factory, 0x10000, 1M,
ota_0,    app,  ota_0,   ,        1M,
ota_1,    app,  ota_1,   ,        1M,
storage,  data, spiffs,  ,        1M,
```

## OTA Firmware Updates

### HTTPS OTA Update

```c
#include "esp_https_ota.h"
#include "esp_ota_ops.h"

#define FIRMWARE_URL "https://example.com/firmware.bin"

esp_err_t perform_ota_update(void) {
    ESP_LOGI("OTA", "Starting OTA update");

    esp_http_client_config_t config = {
        .url = FIRMWARE_URL,
        .cert_pem = NULL,  // Use server_cert_pem for production
        .timeout_ms = 5000,
        .keep_alive_enable = true,
    };

    esp_https_ota_config_t ota_config = {
        .http_config = &config,
    };

    esp_https_ota_handle_t https_ota_handle = NULL;
    esp_err_t err = esp_https_ota_begin(&ota_config, &https_ota_handle);
    if (err != ESP_OK) {
        ESP_LOGE("OTA", "OTA begin failed");
        return err;
    }

    // Get image info
    esp_app_desc_t new_app_info;
    err = esp_https_ota_get_img_desc(https_ota_handle, &new_app_info);
    if (err != ESP_OK) {
        ESP_LOGE("OTA", "Failed to get image descriptor");
        esp_https_ota_abort(https_ota_handle);
        return err;
    }

    ESP_LOGI("OTA", "New firmware version: %s", new_app_info.version);

    // Download and write firmware
    while (1) {
        err = esp_https_ota_perform(https_ota_handle);
        if (err != ESP_ERR_HTTPS_OTA_IN_PROGRESS) {
            break;
        }

        // Progress reporting
        int progress = esp_https_ota_get_image_len_read(https_ota_handle);
        ESP_LOGI("OTA", "Downloaded: %d bytes", progress);
    }

    if (err != ESP_OK) {
        ESP_LOGE("OTA", "OTA failed: %s", esp_err_to_name(err));
        esp_https_ota_abort(https_ota_handle);
        return err;
    }

    // Finalize OTA
    err = esp_https_ota_finish(https_ota_handle);
    if (err == ESP_OK) {
        ESP_LOGI("OTA", "OTA successful, restarting...");
        vTaskDelay(pdMS_TO_TICKS(1000));
        esp_restart();
    } else {
        ESP_LOGE("OTA", "OTA finish failed");
    }

    return err;
}
```

## Debugging & Logging

### Log Levels and Tags

```c
#include "esp_log.h"

static const char *TAG = "MAIN";

void logging_examples(void) {
    // Set log level for specific tag
    esp_log_level_set("WIFI", ESP_LOG_WARN);
    esp_log_level_set("MQTT", ESP_LOG_INFO);

    // Different log levels
    ESP_LOGE(TAG, "Error: %d", error_code);         // Red
    ESP_LOGW(TAG, "Warning: %s", warning_msg);      // Yellow
    ESP_LOGI(TAG, "Info: operation complete");      // Green
    ESP_LOGD(TAG, "Debug: value=%d", debug_val);    // Normal (only if DEBUG)
    ESP_LOGV(TAG, "Verbose: detailed trace");       // Normal (only if VERBOSE)

    // Conditional compilation (saves flash space)
    #if CONFIG_LOG_MAXIMUM_LEVEL >= ESP_LOG_DEBUG
    ESP_LOGD(TAG, "This is only compiled in debug builds");
    #endif
}
```

### Watchdog Timer Configuration

```c
#include "esp_task_wdt.h"

#define WDT_TIMEOUT_S  5

void watchdog_init(void) {
    // Configure task watchdog
    esp_task_wdt_config_t wdt_config = {
        .timeout_ms = WDT_TIMEOUT_S * 1000,
        .idle_core_mask = (1 << 0) | (1 << 1),  // Monitor both cores
        .trigger_panic = true,
    };
    ESP_ERROR_CHECK(esp_task_wdt_init(&wdt_config));

    // Subscribe current task
    ESP_ERROR_CHECK(esp_task_wdt_add(NULL));
}

void long_running_task(void *pvParameters) {
    watchdog_init();

    while (1) {
        do_work();

        // Reset watchdog
        esp_task_wdt_reset();

        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
```

### Stack Overflow Detection

```c
// In sdkconfig or menuconfig:
// CONFIG_FREERTOS_WATCHPOINT_END_OF_STACK=y
// CONFIG_FREERTOS_CHECK_STACKOVERFLOW_CANARY=y

void app_main(void) {
    // Monitor stack usage
    UBaseType_t stack_high_water = uxTaskGetStackHighWaterMark(NULL);
    ESP_LOGI("STACK", "Free stack: %lu bytes", stack_high_water * sizeof(StackType_t));
}
```

## T-Embed Specific Patterns

See `references/t_embed_hardware.md` for complete T-Embed ESP32-S3 hardware specifications, pinout, and initialization examples.

## Resources

This skill includes reference documentation and example code:

### references/

- `freertos_patterns.md` - Advanced FreeRTOS patterns and best practices
- `wifi_ble_advanced.md` - Advanced WiFi/BLE configuration and troubleshooting
- `t_embed_hardware.md` - Complete T-Embed hardware reference
- `power_optimization.md` - Detailed power consumption optimization strategies

### scripts/

- `create_component.sh` - Generate new ESP-IDF component boilerplate
- `partition_calculator.py` - Calculate optimal partition layout

### assets/

- `component_template/` - ESP-IDF component template structure
- `platformio_template/` - PlatformIO project template for ESP32-S3

## Development Environment Setup

```bash
# Install ESP-IDF (recommended: v5.3.x or v5.1.x LTS)
git clone -b v5.3 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh esp32,esp32s3

# Activate IDF environment
. ./export.sh

# Or use PlatformIO
pip install platformio
pio platform install espressif32@6.5.0
```

## Common Troubleshooting

**Task watchdog timeout**: Increase task priority or add `esp_task_wdt_reset()` calls

**Stack overflow**: Increase task stack size or optimize local variable usage

**WiFi disconnects**: Implement reconnection logic in event handler, check power supply

**BLE pairing fails**: Verify security settings, check MTU size

**MQTT messages dropped**: Increase queue sizes, check network stability, use QoS 1

**Display flicker**: Use double buffering, ensure adequate SPI clock speed

**Deep sleep current high**: Disable all peripherals, check GPIO pull configurations

Refer to `references/` files for detailed troubleshooting and optimization guides.
