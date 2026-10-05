---
name: s32ds-search-peripheral-docs
description: Find driver-level documentation for specific peripherals (LPSPI, LINFlexD, FlexCAN, eMIOS, ADC, etc.). Searches the 'driver' corpus for initialization sequences, API function references, register-level details, configuration examples, and usage patterns. Use this when you need to understand how to configure or use a specific peripheral driver in code.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, peripherals, documentation, driver-api, configuration]'
---
# Search Peripheral Documentation

Find driver-level documentation for a specific peripheral - initialization sequences, API usage, register descriptions, and configuration examples.

## Guardrails

**Scope**
- Retrieve only from the 'driver' documentation corpus. Cite the source document for any API, register, or configuration detail; never present from-memory content as documented.

**Refuse-and-escalate**
- If no driver-corpus match is found, escalate to `s32ds-find-documentation` (broader corpora) instead of inventing register layouts or API signatures.

## When to Use
- User asks "how do I use LPSPI?" or "show me FlexCAN configuration"

- Need driver API reference for a peripheral module
- Looking for initialization code examples or register maps
- Troubleshooting a peripheral that isn't working as expected

## Steps

### 1. Identify the Peripheral
Common S32 peripherals:
- **Communication**: LPSPI, LPI2C, LPUART, FlexCAN, LIN, Ethernet
- **Timers**: eMIOS, FTM, PIT, STM, LPIT
- **ADC/DAC**: ADC_SAR, BCTU, DAC
- **Memory**: Flash, EEE (emulated EEPROM)
- **System**: MCU, Clock, Power, Reset, Interrupt (INTC/NVIC)
- **DMA**: eDMA, DMAMUX
- **I/O**: SIUL2 (pins/GPIO), eMIOS

### 2. Search Driver Documentation
Use the driver corpus for peripheral-specific docs:
```
semantic_search(query="<peripheral_name> driver initialization configuration", corpus="driver")
```

### 3. Search for API Functions
Find specific function signatures or usage patterns:
```
keyword_search(pattern="<Peripheral>_Init", corpus="driver")
```
Or for specific IP names:
```
keyword_search(pattern="<IP_NAME>", corpus="driver", case_sensitive=true)
```

### 4. Get Register Details
For register-level information:
```
keyword_search(pattern="<REGISTER_NAME>", corpus="all")
```

### 5. Get Full Page Context
When a result is promising, retrieve the complete page:
```
get_document_pages(doc_id="<doc_name>", page="<page>", corpus="driver")
```

### 6. Cross-Reference with General Docs
For system-level context (how the peripheral fits in the MCU):
```
semantic_search(query="<peripheral> <mcu_family> block diagram features", corpus="lite")
```

### 7. Present Structured Answer
Organize findings into:
- **Overview**: What the peripheral does
- **Key APIs**: Init, DeInit, Transfer functions
- **Configuration**: Required settings, clock dependencies
- **Example**: Code snippet or initialization sequence
- **Constraints**: Known limitations, errata references

## Common Search Patterns

| Need | Search Example |
|------|---------------|
| Init sequence | `semantic_search("LPSPI initialization sequence", corpus="driver")` |
| Register map | `keyword_search("LPSPI_CR", corpus="all")` |
| Clock config | `semantic_search("LPSPI clock source configuration", corpus="driver")` |
| DMA usage | `semantic_search("LPSPI DMA transfer mode", corpus="driver")` |
| Error handling | `semantic_search("LPSPI error status flags", corpus="driver")` |

## Tips
- The `driver` corpus has detailed API docs; `lite` corpus has overview/system-level docs
- Use exact IP module names (uppercase) for keyword search: "LPSPI", "FLEXCAN", "EMIOS"
- Peripheral names may differ between S32K3, S32G, S32R families - verify with project SDK
- Combine with `s32ds-check-sdk-compatibility` skill to ensure the peripheral is available on the target MCU
