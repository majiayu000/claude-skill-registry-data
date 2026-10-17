---
name: Embedded C
description: "Bare-metal and RTOS embedded C programming. Linker scripts, startup code, peripheral drivers, memory-mapped I/O, DMA, interrupt handlers, and power management."
category: low-level
tags: embedded, c, rtos, bare-metal, freertos, zephyr, stm32, arm, mcu, drivers
---

# Embedded C

Expert in embedded systems programming — writing C for microcontrollers where there is no OS, or a minimal RTOS.

## Use this skill when

- Writing bare-metal firmware for ARM Cortex-M, RISC-V, or other MCUs
- Developing with RTOS (FreeRTOS, Zephyr, ThreadX, NuttX)
- Writing peripheral drivers (UART, SPI, I2C, ADC, DMA, GPIO, Timers)
- Creating linker scripts and startup code (`.ld`, `startup.s`)
- Debugging with JTAG/SWD, OpenOCD, or J-Link
- Optimizing for constrained environments (KB of RAM, MHz clocks)
- Implementing communication protocols (CAN, Modbus, MQTT over cellular)

## Core Principles

### 1. Memory-Mapped I/O (MMIO)

All peripheral access is through memory-mapped registers. Use `volatile` always.

```c
// ❌ WRONG — compiler may optimize away reads/writes
uint32_t *gpio_reg = (uint32_t *)0x40020014;
*gpio_reg |= (1 << 5);

// ✅ CORRECT — volatile prevents optimization
#define GPIOA_ODR  (*(volatile uint32_t *)0x40020014)
GPIOA_ODR |= (1 << 5);  // Set PA5 high (LED on STM32)

// ✅ BEST — structured register overlay
typedef struct {
    volatile uint32_t MODER;
    volatile uint32_t OTYPER;
    volatile uint32_t OSPEEDR;
    volatile uint32_t PUPDR;
    volatile uint32_t IDR;
    volatile uint32_t ODR;
    volatile uint32_t BSRR;
    volatile uint32_t LCKR;
    volatile uint32_t AFR[2];
} GPIO_TypeDef;

#define GPIOA ((GPIO_TypeDef *)0x40020000)
GPIOA->BSRR = (1 << 5);  // Atomic set — no read-modify-write race
```

### 2. Interrupt Handlers

Keep ISRs minimal. Use flags or queues to defer work.

```c
// ISR: set flag only — no heavy computation
void USART1_IRQHandler(void) {
    if (USART1->SR & USART_SR_RXNE) {
        uint8_t byte = USART1->DR;
        ring_buffer_push(&rx_buf, byte);  // O(1) lock-free
        // Signal main loop or RTOS task
    }
}

// Critical section patterns
// Bare-metal: disable/enable interrupts
__disable_irq();
shared_counter++;
__enable_irq();

// RTOS: use mutex or task notification
xSemaphoreTake(spi_mutex, portMAX_DELAY);
spi_transfer(data, len);
xSemaphoreGive(spi_mutex);
```

### 3. Linker Script Essentials

```ld
/* Minimal linker script for ARM Cortex-M */
MEMORY {
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
    SRAM  (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}

SECTIONS {
    .isr_vector : { KEEP(*(.isr_vector)) } > FLASH
    .text       : { *(.text*) *(.rodata*) } > FLASH
    .data       : { *(.data*) } > SRAM AT > FLASH
    .bss        : { *(.bss*) *(COMMON) } > SRAM

    /* Stack at top of SRAM */
    _estack = ORIGIN(SRAM) + LENGTH(SRAM);
}
```

### 4. Startup Code Pattern

```c
// Minimal startup — runs before main()
void Reset_Handler(void) {
    // 1. Copy .data from FLASH to SRAM
    extern uint32_t _sdata, _edata, _sidata;
    uint32_t *src = &_sidata, *dst = &_sdata;
    while (dst < &_edata) *dst++ = *src++;

    // 2. Zero .bss
    extern uint32_t _sbss, _ebss;
    dst = &_sbss;
    while (dst < &_ebss) *dst++ = 0;

    // 3. Initialize clocks, FPU, etc.
    SystemInit();

    // 4. Call main
    main();

    // 5. If main returns, hang
    while (1) __WFI();
}
```

### 5. RTOS Task Design

| Pattern | Use When |
|---|---|
| **Periodic task** | Sensor polling, control loops (use `vTaskDelayUntil`) |
| **Event-driven** | Interrupt → queue → task (use `xQueueReceive`) |
| **State machine** | Protocol handling, UI (switch-case in task loop) |
| **Producer-consumer** | DMA → buffer → processing (use stream buffers) |

```c
// FreeRTOS: Prioritized task with watchdog
void sensor_task(void *pvParameters) {
    TickType_t last_wake = xTaskGetTickCount();
    while (1) {
        int16_t temp = read_temperature_sensor();
        xQueueSend(data_queue, &temp, 0);
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(100));  // Exact 100ms period
    }
}
```

### 6. Power Management

```c
// Sleep modes (Cortex-M)
// WFI: Wait For Interrupt — lightest sleep
__WFI();

// Stop mode: all clocks off, SRAM retained
HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_STOPENTRY_WFI);
// After wakeup: reconfigure clocks!
SystemClock_Config();

// Standby: deepest sleep, only RTC/WKUP pin wakes
HAL_PWR_EnterSTANDBYMode();
// After wakeup: full reset (startup code runs again)
```

## Build System

```makefile
# Minimal ARM Cortex-M Makefile
CC      = arm-none-eabi-gcc
CFLAGS  = -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16
CFLAGS += -Os -g3 -Wall -Wextra -Werror
CFLAGS += -ffunction-sections -fdata-sections  # Dead code elimination
LDFLAGS = -T linker.ld -Wl,--gc-sections -specs=nano.specs -specs=nosys.specs

%.elf: $(OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

%.bin: %.elf
	arm-none-eabi-objcopy -O binary $< $@

flash: firmware.bin
	openocd -f interface/stlink.cfg -f target/stm32f4x.cfg \
	  -c "program $< 0x08000000 verify reset exit"
```

## Anti-Patterns

- ❌ Using `malloc` in bare-metal without a heap implementation
- ❌ Busy-waiting instead of using WFI/WFE in idle loops
- ❌ Non-volatile access to hardware registers
- ❌ Long ISRs (>10µs) — defer work to tasks
- ❌ Ignoring stack overflow in RTOS tasks (enable `configCHECK_FOR_STACK_OVERFLOW`)
- ❌ Read-modify-write on GPIO ODR (use BSRR for atomic set/clear)
- ❌ Forgetting to enable peripheral clocks before register access
