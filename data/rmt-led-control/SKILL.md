---
name: RMT-LED-Control-on-ESP32
keywords: RMT, RGBIC, LED, WS2812, APA102, SK6812, addressable, neopixel, dotstar, LED timing, RGB, GRBL, color, brightness, pulse, DMA
---

# RMT LED Control on ESP32

## Quick Reference

The RMT (Remote Control) peripheral on ESP32-S3 generates precise nanosecond-accurate pulse sequences for controlling addressable LEDs. No CPU intervention during transmission = perfect timing.

## Why RMT?

- **Cycle-accurate**: Hardware timing with <100ns jitter
- **DMA-capable**: No CPU overhead for large arrays
- **Interrupt-safe**: Transmission happens independently
- **Channel-flexible**: Up to 8 simultaneous LED lines

## LED Protocol Timing Requirements

### WS2812B (NeoPixel)
```
Bit Rate: 800kHz (1.25µs per bit)
Logic 0:  0.4µs HIGH + 0.85µs LOW
Logic 1:  0.8µs HIGH + 0.45µs LOW
Reset:    >50µs LOW
Tolerance: ±150ns (WS2812B is strict!)
```

### APA102 (DotStar)
```
Protocol: SPI-like (less timing critical)
Clock:    Up to 20MHz typical
Start Frame: 0x00 0x00 0x00 0x00
LED Frame: 0xFF + Blue + Green + Red
End Frame: 0xFF (repeated for N LEDs)
Tolerance: ±10% (very forgiving)
```

### SK6812
```
Bit Rate: 800kHz (similar to WS2812B)
Logic 0:  0.3µs HIGH + 0.9µs LOW
Logic 1:  0.6µs HIGH + 0.6µs LOW
Reset:    >80µs LOW
Tolerance: ±150ns
```

## RMT Configuration Reference

### Clock Divider Selection
```
Clock = 80MHz / divider
divider=8  → 10MHz (100ns per tick)  ← Good for WS2812B
divider=16 → 5MHz  (200ns per tick)  ← Alternative
divider=4  → 20MHz (50ns per tick)   ← For fast protocols
```

For WS2812B with 100ns ticks:
- 0.4µs = 4 ticks HIGH
- 0.85µs ≈ 8-9 ticks LOW
- 0.8µs ≈ 8 ticks HIGH
- 0.45µs ≈ 4-5 ticks LOW

## Common Code Snippets

### Minimal WS2812B Setup
```c
// Pin configuration
#define LED_PIN GPIO_NUM_9
#define NUM_LEDS 100

// Configure RMT
rmt_config_t config = {
    .rmt_mode = RMT_MODE_TX,
    .channel = RMT_CHANNEL_0,
    .clk_div = 8,                    // 100ns per tick
    .gpio_num = LED_PIN,
    .mem_block_num = 1,
    .tx_config = {
        .loop_en = false,
        .carrier_en = false,
        .idle_level = RMT_IDLE_LEVEL_LOW,
        .idle_output_en = true,
    }
};
rmt_config(&config);
rmt_driver_install(RMT_CHANNEL_0, 0, 0);

// Send color to LEDs
void set_led_color(uint32_t color, size_t num_leds) {
    rmt_item32_t items[num_leds * 24];

    // Encode each LED's 24-bit GRB color
    for (int led = 0; led < num_leds; led++) {
        for (int bit = 23; bit >= 0; bit--) {
            bool is_one = (color >> bit) & 1;
            items[led*24 + (23-bit)].duration0 = is_one ? 8 : 4;
            items[led*24 + (23-bit)].level0 = 1;
            items[led*24 + (23-bit)].duration1 = is_one ? 4 : 8;
            items[led*24 + (23-bit)].level1 = 0;
        }
    }

    rmt_write_items(RMT_CHANNEL_0, items, num_leds * 24, true);
    rmt_wait_tx_done(RMT_CHANNEL_0, portMAX_DELAY);
}
```

### Multi-LED Array Pattern
```c
// Avoid allocating RMT items on stack!
static rmt_item32_t rmt_buffer[2400];  // 100 LEDs × 24 bits

void update_led_array(uint32_t *colors, size_t num_leds) {
    size_t item_count = 0;

    for (int led = 0; led < num_leds; led++) {
        uint32_t color = colors[led];
        for (int bit = 23; bit >= 0; bit--) {
            bool is_one = (color >> bit) & 1;
            rmt_buffer[item_count].duration0 = is_one ? 8 : 4;
            rmt_buffer[item_count].level0 = 1;
            rmt_buffer[item_count].duration1 = is_one ? 4 : 8;
            rmt_buffer[item_count].level1 = 0;
            item_count++;
        }
    }

    rmt_write_items(RMT_CHANNEL_0, rmt_buffer, item_count, true);
}
```

### Color Format Handling
```c
// RGB to GRB conversion (WS2812B uses GRB order)
uint32_t rgb_to_grb(uint8_t r, uint8_t g, uint8_t b) {
    return ((uint32_t)g << 16) | ((uint32_t)r << 8) | b;
}

// Separate color components
void extract_grb(uint32_t grb, uint8_t *g, uint8_t *r, uint8_t *b) {
    *g = (grb >> 16) & 0xFF;
    *r = (grb >> 8) & 0xFF;
    *b = grb & 0xFF;
}

// Brightness adjustment (linear)
uint32_t dim_color(uint32_t grb, uint8_t brightness) {
    uint8_t g = (grb >> 16) & 0xFF;
    uint8_t r = (grb >> 8) & 0xFF;
    uint8_t b = grb & 0xFF;

    g = (g * brightness) / 255;
    r = (r * brightness) / 255;
    b = (b * brightness) / 255;

    return ((uint32_t)g << 16) | ((uint32_t)r << 8) | b;
}
```

### DMA-Based High-Speed Transfer
```c
// For >1000 LEDs, use DMA to avoid timing issues
void dma_update_leds(uint32_t *colors, size_t num_leds) {
    // Prepare items in static buffer
    static rmt_item32_t dma_items[4800];  // Max 200 LEDs

    size_t item_count = 0;
    for (int led = 0; led < num_leds; led++) {
        uint32_t color = colors[led];
        for (int bit = 23; bit >= 0; bit--) {
            bool is_one = (color >> bit) & 1;
            dma_items[item_count].duration0 = is_one ? 8 : 4;
            dma_items[item_count].level0 = 1;
            dma_items[item_count].duration1 = is_one ? 4 : 8;
            dma_items[item_count].level1 = 0;
            item_count++;
        }
    }

    // DMA transfer starts automatically
    rmt_transmit_start(RMT_CHANNEL_0, dma_items, item_count, true);
    rmt_wait_tx_done(RMT_CHANNEL_0, portMAX_DELAY);
}
```

## Anti-Patterns to Avoid

### ❌ WRONG: Allocating RMT items on stack
```c
void bad_update(uint32_t color) {
    rmt_item32_t items[24];  // ← Stack overflow risk!
    // ... fill items ...
    rmt_write_items(RMT_CHANNEL_0, items, 24, true);
}
```

### ✅ CORRECT: Use static/global buffer
```c
static rmt_item32_t items[24];  // Global buffer
void good_update(uint32_t color) {
    // ... fill items ...
    rmt_write_items(RMT_CHANNEL_0, items, 24, true);
}
```

### ❌ WRONG: Forgetting reset pulse
```c
void incomplete_update(uint32_t *colors, size_t num_leds) {
    // Sends data but no reset!
    rmt_write_items(RMT_CHANNEL_0, items, item_count, true);
    // ← LEDs won't latch without >50µs LOW
}
```

### ✅ CORRECT: Include reset in timing
```c
void complete_update(uint32_t *colors, size_t num_leds) {
    rmt_write_items(RMT_CHANNEL_0, items, item_count, true);
    rmt_wait_tx_done(RMT_CHANNEL_0, portMAX_DELAY);
    delay(1);  // 1ms LOW for reset (>50µs required)
}
```

## Troubleshooting

### LEDs Show Wrong Colors
**Check**: GRB vs RGB byte order
- WS2812B expects: GRB (Green, Red, Blue)
- Not: RGB
- Fix: `color = (g<<16) | (r<<8) | b`

### LEDs Flicker or Show Garbage
**Check**: Timing accuracy
- Use oscilloscope to verify HIGH/LOW timing
- Adjust duration values for your clock divider
- Typical issue: Clock divider mismatch

### Some LEDs Work, Others Don't
**Check**: Buffer size too small
- If 100 LEDs but buffer only 2400 items, last LEDs get cut
- Each LED = 24 items
- Required buffer: `num_leds * 24`

### Update Too Slow
**Check**: Using blocking wait on main thread
- `rmt_wait_tx_done()` blocks until complete
- For >30Hz updates, use DMA + ISR notification instead

## Performance Notes

| Configuration | Speed | CPU Load | Notes |
|---|---|---|---|
| Single LED, blocking | ~10 updates/sec | 5% | Testing only |
| 100 LEDs, blocking | ~100 updates/sec | 15% | OK for slow effects |
| 1000 LEDs, blocking | ~10 updates/sec | 90% | Bottleneck! |
| 1000 LEDs, DMA | ~30 updates/sec | 5% | ✓ Recommended |

## References

- ESP32-S3 Technical Reference Manual, Section 7 (RMT)
- WS2812B Datasheet: timing specifications
- APA102 Protocol Specification
- https://github.com/espressif/esp-idf/tree/master/examples/peripherals/rmt
