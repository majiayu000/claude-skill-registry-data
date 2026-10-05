---
name: freemaster-driver-integration
description: >
  Integrates the FreeMASTER Driver as a standalone library into an embedded
  application project. Use whenever the user wants to add FreeMASTER Driver
  support to a third-party IDE, custom build system, or non-standard embedded
  project: discovering the installed library, adding include/source paths,
  creating freemaster_cfg.h, choosing the transport header, configuring
  interrupt mode, setting the comm base address, calling FMSTR_Init() and
  FMSTR_Poll(). Triggers on "integrate FreeMASTER driver", "add FreeMASTER to
  my project", "freemaster_cfg.h", "FMSTR_Init", "FMSTR_Poll", LPUART/
  LINFlexD/FlexCAN/BDM transport setup.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: freemaster
  tags: '[freemaster, driver, embedded, integration, uart, can, linflexd, lpuart]'
---

# FreeMASTER Driver Integration

Integrates the FreeMASTER Driver as a standalone library into an embedded
application project. Covers library discovery, build-system wiring,
`freemaster_cfg.h` creation, transport selection, interrupt hookup, and the
mandatory `FMSTR_Init()` / `FMSTR_Poll()` calls. Especially useful for
third-party IDEs and custom build systems where the standard FreeMASTER-aware
IDE flow is not available.

## When to use

- Adding FreeMASTER Driver support to an existing embedded firmware project.
- Using a third-party IDE or custom project layout needing standalone library steps.
- Discovering where the FreeMASTER Driver is installed in S32 Design Studio.
- Configuring UART, LINFlexD, FlexCAN, or BDM communication for the driver.
- Creating or adapting `freemaster_cfg.h`.

Do **not** use this skill for FreeMASTER Lite service, JSON-RPC API, or
browser client tasks. Use the FreeMASTER Lite skills instead.

## Quick start

```text
1. Locate the FreeMASTER Driver installation folder.
2. Verify src/common, src/drivers/dreg/S32, src/platforms/gen32le, src/template exist.
3. Add include paths: src/common, src/drivers/dreg/S32, src/platforms/gen32le.
4. Add source paths: src/common, src/drivers/dreg/S32.
5. Copy src/template into the project as freemaster_cfg.h; place on include path.
6. Include freemaster.h and the matching transport header in main.c.
7. Optionally configure interrupt mode (FMSTR_LONG_INTR / FMSTR_SHORT_INTR).
8. Call FMSTR_SerialSetBaseAddress() or FMSTR_CanSetBaseAddress() with the peripheral base.
9. Call FMSTR_Init() after peripheral and clock init.
10. Call FMSTR_Poll() each iteration of the main loop.
```

## Library Discovery

Default installation pattern in S32 Design Studio:

```text
C:\NXP\S32DS.{X.Y.Z}\S32DS\software\FreeMASTER_{PLATFORM}_v3.0
```

- `{X.Y.Z}` — S32DS version, e.g. `3.6.5`
- `{PLATFORM}` — device-family name, e.g. `S32K3`

If multiple S32DS versions are installed, prefer the one matching the project
environment. If the folder is not found, ask the user for the path — do not
guess custom locations.

## Include and Source Paths

| Role | Folders to add |
|------|----------------|
| Include paths | `src/common`, `src/drivers/dreg/S32`, `src/platforms/gen32le` |
| Source paths | `src/common`, `src/drivers/dreg/S32` |

## Transport Header Selection

| Transport | Header to include |
|-----------|------------------|
| LPUART | `freemaster_s32_lpuart.h` |
| LINFlexD | `freemaster_s32_linflexd.h` |
| FlexCAN | `freemaster_s32_flexcan.h` |
| BDM | (none — omit transport header) |

Use the matching base-address setter: `FMSTR_SerialSetBaseAddress()` for serial
transports, `FMSTR_CanSetBaseAddress()` for CAN.

## Interrupt Mode (optional)

Enable in `freemaster_cfg.h`:

```c
#define FMSTR_LONG_INTR  1   /* or FMSTR_SHORT_INTR 1 */
```

Then attach the ISR helper in the peripheral interrupt handler:
- `FMSTR_SerialIsr` for serial transports
- `FMSTR_CanIsr` for CAN

Keep `FMSTR_Poll()` in the main loop regardless of mode — it is guarded by
macros and makes switching between interrupt and polling modes easy.

## Minimal Integration Example

```c
#include "freemaster.h"
#include "freemaster_s32_lpuart.h"

int main(void)
{
    /* Application hardware initialization */
    FMSTR_SerialSetBaseAddress(LPUART0_BASE);
    FMSTR_Init();

    for (;;) {
        FMSTR_Poll();
        /* Application background work */
    }
}
```

Adapt the transport header and base-address setter to match the actual
communication peripheral. See `references/transports.md` for per-transport
mini-recipes and common failure patterns.

## Guardrails

**Scope**
- This skill covers embedded-side driver integration only.
- Do not modify project files outside the user's current embedded project.

**Destructive actions**
- Creating `freemaster_cfg.h` overwrites an existing file only if the user
  confirms. When in doubt, propose the new content without overwriting.

**Secrets**
- No credentials involved.

**Refuse-and-escalate**
- If the discovered installation folder does not contain the expected `src`
  subfolders, stop and ask the user to confirm the path before proceeding.
- If the user's transport or MCU is not identified, ask the clarifying
  questions in `references/transports.md` before writing any code.

## Validation loop

1. Verify the installation folder contains `src/common`, `src/drivers/dreg/S32`,
   `src/platforms/gen32le`, and `src/template`. Fail if any are absent.
2. Confirm that `freemaster_cfg.h` is on the compiler include path — a missing
   header causes a build error before any driver code runs.
3. After first build, check that `FMSTR_Init()` compiles without unresolved
   symbols; missing source paths show up here.
4. At runtime, confirm `FMSTR_Poll()` is reached every cycle and the host tool
   can establish a connection. If connection fails, check base address and
   transport header choice against `references/transports.md`.

## Out of scope

- FreeMASTER Lite service setup, JSON-RPC API, or browser client — use the
  `freemaster-lite-*` skills.
- General embedded project setup unrelated to FreeMASTER integration.
- Runtime operation of an already-integrated driver.

## See Also

- `references/transports.md` — per-transport mini-recipes, failure patterns,
  and discovery questions
- `freemaster-lite-start-server` — launching the host-side FreeMASTER Lite service
- `freemaster-lite-configuration-file` — configuring connections on the host side
