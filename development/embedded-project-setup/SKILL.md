---
name: embedded-project-setup
description: "Embedded firmware setup: STM32, ESP32, AVR, RP2040, Nordic nRF, Zephyr/RTOS, vendor SDKs, CMake/CMakePresets, VS Code/clangd, cross toolchains, flash/debug, Docker/CI. Use for MCU scaffolds, existing firmware modernization, BSPs, linker/startup files, SDK package selection, and embedded CI; prefer cpp-project-setup for host-side C++."
---

# Modern Embedded Project Setup

## Overview

Create or modernize embedded firmware around a shared engineering pipeline, then adapt the target-specific compiler, SDK, flashing, and debug pieces to the selected MCU:

```text
VS Code -> clangd -> clang-format -> clang-tidy -> CMake/CMakePresets -> Ninja -> target compiler/SDK -> firmware artifacts -> flash/debug -> MCU
```

Treat editor analysis, static checks, build generation, cross compilation, artifact generation, flashing, and debug as separate stages. First classify the user's working directory and host platform, then either generate a greenfield scaffold or modernize the existing firmware pipeline.

## Workflow

1. Determine the user's working directory and whether firmware already exists.
   - Check the user-provided path or current working directory before writing files.
   - Treat the directory as an existing firmware project if it already has source files, linker scripts, startup files, CubeMX files, CMake/Make/build scripts, vendor trees, flash/debug scripts, editor settings, CI, docs, or git history.
   - For existing firmware, inventory the full development pipeline before editing: build system, toolchain file, compiler version, MCU/board assumptions, linker/startup flow, vendor dependency model, flash/debug flow, tests or host-side checks, formatting/linting/static analysis, CI, and firmware artifacts.

2. Detect the user's host development environment.
   - Determine OS and architecture: macOS/Linux/Windows plus arm64 or x64. Use local commands such as `uname -s`, `uname -m`, or PowerShell/.NET runtime information where appropriate.
   - Select a host profile: `macos-arm64`, `macos-x64`, `linux-x64`, `linux-arm64`, `windows-x64`, or `windows-arm64`.
   - If the agent is running somewhere other than the user's real development machine, ask for the user's OS/architecture instead of assuming the sandbox matches their workstation.

3. Identify the firmware target before writing files.
   - Capture target ecosystem first: STM32/Cortex-M, ESP32/ESP-IDF, AVR/Arduino or bare-metal avr-gcc, RP2040/Pico SDK, Nordic nRF/nRF Connect SDK or Zephyr, Zephyr/RTOS board target, or another MCU family.
   - Capture the concrete MCU or board, firmware package/SDK, dependency path, package version/tag, debug probe, flash/RAM map when relevant, CPU core, FPU/float ABI when relevant, flash tool, debug server, and whether the project will use vendor HAL/SDK, RTOS APIs, CMSIS, bare-metal register access, or a mix.
   - If the user has not provided the target, ask for the MCU/board and preferred framework before writing files. Do not silently default to any STM32, ESP32, AVR, RP2040, Nordic, or Zephyr board.
   - If the user explicitly wants a target-agnostic starter before hardware is known, generate only a portable build-smoke scaffold with no hardware register writes, no final flash command assumptions, and clear TODOs for target selection.

4. Choose and pin the firmware package or SDK before generating build files.
   - Read `references/firmware-package-matrix.md` when selecting or validating packages for STM32, ESP32, AVR, RP2040/RP2350, Nordic nRF, Zephyr, or standalone RTOS projects.
   - Record four facts before writing source lists or include paths: package name, source URL or package manager, local path such as `vendor/STM32CubeG0` or an external SDK workspace, and pinned version/tag/manifest revision.
   - CMSIS is the common Cortex-M processor/device layer when official Cortex-M device headers exist. Do not claim CMSIS is required for non-Arm targets such as AVR or ESP32.
   - Prefer the ecosystem's normal dependency model: STM32Cube packages can live under `vendor/` as a submodule or recursive clone; ESP-IDF usually lives outside the app as `IDF_PATH` or in an external/submodule path; Pico SDK can be a submodule or external SDK path; nRF Connect SDK and Zephyr should usually be managed by `west`; AVR bare-metal normally uses AVR GNU Toolchain plus AVR-LibC and only adds Microchip `.atpack` files when device support is missing or needs pinning.
   - If fetching packages requires network access or would add a large dependency tree, ask for approval or document the exact command and leave non-fake placeholders. Do not invent CMSIS/HAL paths or copy unrelated vendor examples into the project.

5. Choose the target toolchain profile.
   - Use this matrix to choose the actual compiler, build driver, artifact tools, flash command, debug server, Docker image, and CI commands before generating files:

| Target/platform | Compiler and build tools to configure | Firmware artifacts | Flash/debug tools to configure |
| --- | --- | --- | --- |
| STM32 MCU | `arm-none-eabi-gcc/g++`, `arm-none-eabi-objcopy`, `arm-none-eabi-size`, `arm-none-eabi-gdb`, CMake, Ninja, selected CMSIS Device/Core and STM32 HAL/LL sources from `STM32Cube<series>`. Use GNU Tools for STM32 or ST Arm Clang instead when the project requests ST's toolchain. | `.elf`, `.bin`, `.hex`, `.map` | OpenOCD or STM32CubeProgrammer/ST-LINK GDB server, ST-Link or J-Link, Cortex-Debug or STM32 VS Code debug configuration. |
| ESP32 family | ESP-IDF, CMake, Ninja, `idf.py`; configure `xtensa-esp-elf-gcc/g++` for Xtensa ESP32 variants and `riscv32-esp-elf-gcc/g++` for RISC-V ESP32 variants through ESP-IDF tooling. | ESP-IDF app/bootloader/partition `.bin` images, `.elf`, `.map` | `idf.py flash`, `esptool.py`, `idf.py monitor`, Espressif OpenOCD/JTAG and ESP-IDF debug configuration when hardware debug is requested. |
| AVR | AVR GNU Toolchain: `avr-gcc/g++`, `avr-objcopy`, `avr-size`, `avr-objdump`, AVR Libc, CMake or Make. Configure `-mmcu=<device>` from the exact AVR MCU. | `.elf`, `.hex`, `.eep`, `.map` when configured | `avrdude` with the user's programmer and port, or the existing Arduino/Microchip upload flow. |
| RP2040/RP2350 | Pico SDK, CMake, Ninja or Make, `arm-none-eabi-gcc/g++`, Pico SDK tools such as `elf2uf2`; configure `PICO_SDK_PATH` and board settings. | `.elf`, `.uf2`, `.bin`, `.hex`, `.map` | USB bootloader drag-and-drop, `picotool`, Picoprobe/OpenOCD, `arm-none-eabi-gdb`, Cortex-Debug when debugging is requested. |
| Nordic nRF | Prefer nRF Connect SDK / Zephyr SDK with `west`, CMake, Ninja, and the SDK-managed Arm toolchain. For direct bare-metal nRF projects, configure `arm-none-eabi-gcc/g++`, CMSIS/nrfx, CMake, and Ninja. | Zephyr/nRF merged `.hex` and `.elf`, or direct bare-metal `.elf`, `.bin`, `.hex`, `.map` | `west flash`, `nrfjprog`, J-Link tools, OpenOCD where supported, `west debug`, or Cortex-Debug/J-Link configuration. |
| Zephyr/RTOS | Zephyr SDK or the vendor RTOS toolchain selected by board architecture; configure `west`, CMake, Ninja, devicetree, Kconfig, and board overlays. Use architecture-specific toolchains such as `arm-zephyr-eabi`, RISC-V, Xtensa, x86, ARC, or vendor-provided compilers as required by the board. | Zephyr `.elf`, `.hex`, `.bin`, merged images, signed images, or RTOS/vendor-specific outputs | `west flash`, `west debug`, board runner config, OpenOCD/J-Link/pyOCD/vendor runners as selected by Zephyr or the RTOS. |

   - The shared workflow is editor/build-system/quality/CI consistency. The compiler and flash/debug tools must come from the selected target profile.
   - Do not generate a generic `arm-none-eabi-gcc` toolchain file for ESP32, AVR, Zephyr non-Arm boards, or any platform whose SDK owns toolchain selection.

6. Generate or update the project.
   - For greenfield scaffolding, run from this skill directory:

```bash
python3 scripts/scaffold_embedded_project.py \
  --name firmware \
  --out /path/to/workspace/firmware \
  --host-platform macos-arm64 \
  --target-family <target-family> \
  --board <board-name> \
  --mcu <mcu-name> \
  --cpu <cpu-core>
```

   - Use the bundled scaffold script only for direct CMake-style Cortex-M projects that fit the `arm-none-eabi-gcc` flow. For STM32 HAL/LL projects, pair the shared CMake/editor scaffold with an explicit `STM32Cube<series>` package path and selected CMSIS/HAL source list. For ESP-IDF, AVR, Pico SDK, Zephyr, or other ecosystems, either adapt the generated standard configs carefully or create/update the ecosystem-native files directly.
   - For a concrete Cortex-M target, pass explicit target values:

```bash
python3 scripts/scaffold_embedded_project.py \
  --name sensor_fw \
  --out /path/to/workspace/sensor_fw \
  --target-family nrf52 \
  --board custom-nrf52840-board \
  --mcu nrf52840 \
  --device-define NRF52840_XXAA \
  --cpu cortex-m4 \
  --fpu fpv4-sp-d16 \
  --float-abi hard \
  --flash-origin 0x00000000 \
  --flash-kb 1024 \
  --ram-origin 0x20000000 \
  --ram-kb 256 \
  --openocd-interface jlink \
  --openocd-target nrf52
```

   - The scaffold script renders reusable standard configuration from `assets/` for CMake, presets, clangd/tidy, VS Code, Docker, and debug tasks. Update assets when the shared firmware standard changes; update the Python script when generation logic, MCU arguments, linker/startup defaults, BSP templates, or command entry points change.
   - For existing firmware, inspect `CMakeLists.txt`, `CMakePresets.json`, toolchain files, linker scripts, startup files, `.vscode/`, `.clangd`, `.clang-tidy`, flash/debug scripts, Dockerfile, CI workflows, and local docs before editing.
   - Omit `--host-platform` only when generating on the same machine where the project will be developed; the script will auto-detect that host.

7. Preserve the embedded layer model.
   - Keep application logic above board support and drivers.
   - Keep the BSP thin and explicit: board wiring belongs there, reusable chip drivers belong below it, application behavior belongs above it.
   - Use CMSIS Core plus CMSIS Device as the lowest common Cortex-M/device layer when vendor headers are available; do not apply CMSIS expectations to AVR, ESP-IDF, or other non-Cortex-M targets.
   - Use vendor HALs, SDK drivers, ESP-IDF components, Pico SDK libraries, Arduino cores, Zephyr drivers, or RTOS APIs when they match the chosen ecosystem; use lower-level APIs or direct registers only for startup, BSP smoke tests, bootloaders, or performance-critical code.
   - Treat RTOS selection separately from silicon support. Zephyr and nRF Connect SDK can own startup/linker/drivers through their board model; standalone FreeRTOS still needs the vendor firmware package or device support layer underneath it.
   - Do not vendor-copy large SDK trees blindly; prefer a documented submodule, package manager, west manifest, generated vendor directory, or user-provided dependency path.

8. Wire the toolchain.
   - Use CMake presets named from a target-neutral prefix, by default `firmware-debug`, `firmware-release`, and `firmware-analyze`.
   - Configure the compiler and build driver from the selected target profile: create a CMake toolchain file for direct bare-metal GCC flows, use ESP-IDF's `idf.py` and managed toolchains for ESP32, use AVR GCC and `-mmcu` settings for AVR, use Pico SDK variables for RP2040/RP2350, and preserve `west`/Zephyr SDK or vendor RTOS toolchain selection for Zephyr/RTOS projects.
   - Keep generated `CMakePresets.json`, VS Code settings/tasks/launch configs, shell/PowerShell scripts, Dockerfile, and GitHub Actions workflow aligned with that selected compiler and build command.
   - Export `compile_commands.json` for clangd.
   - Pass the embedded target triple to clangd and clang-tidy when the target compiler flags require it.
   - Use Ninja for builds.
   - Produce the firmware artifacts expected by the target ecosystem, such as `.elf`, `.bin`, `.hex`, `.map`, `.uf2`, or vendor-specific images.

9. Wire editor, flashing, and debug.
   - Recommend VS Code extensions that match the target: clangd and CMake Tools for CMake flows, Cortex-Debug for Cortex-M GDB flows, and ecosystem-specific extensions only when they help the selected target.
   - Disable competing IntelliSense when clangd owns semantic analysis.
   - Use OpenOCD with ST-Link or J-Link when that is the right GDB server for the selected target.
   - Set flash/debug config from the actual target and probe. Do not invent OpenOCD target names; ask the user or inspect existing project files when uncertain.
   - Keep shell and PowerShell command entry points for build, format, analyze, flash, and debug-server startup when generating a cross-platform scaffold.

## Validation

Run what is available locally. For the bundled direct Cortex-M scaffold, use:

```bash
cmake --preset firmware-debug
cmake --build --preset firmware-debug
bash scripts/format.sh --check
cmake --preset firmware-analyze
cmake --build --preset firmware-analyze
```

On Windows, use the generated PowerShell entry points such as `pwsh scripts/build.ps1`, `pwsh scripts/format.ps1 -Check`, and `pwsh scripts/analyze.ps1`.

For ESP-IDF, AVR, Pico SDK, Zephyr, or RTOS projects, use the ecosystem-native validation commands after adding the shared editor/format/CI layers, for example `idf.py build`, `west build`, Pico SDK CMake presets, `avr-gcc`/`avrdude` smoke commands, or the existing project scripts.

Also validate the firmware package decision itself:

- STM32: confirm `vendor/STM32Cube<series>` or the documented external package path exists, is pinned to a tag/commit, and exposes `Drivers/CMSIS` plus the selected `Drivers/STM32<series>xx_HAL_Driver` paths.
- ESP-IDF: run `idf.py --version`, confirm the chosen `IDF_PATH` or submodule path, then run `idf.py set-target <chip>` and `idf.py build` when tools are installed.
- AVR: confirm `avr-gcc -mmcu=<device>` recognizes the MCU, and record whether AVR-LibC or a Microchip `.atpack` supplies headers/startup/device libraries.
- Pico SDK: confirm `PICO_SDK_PATH` or the submodule path and run the Pico SDK CMake configure/build that produces `.uf2`.
- Nordic nRF / Zephyr: run `west list` to verify the manifest-resolved SDK modules, then `west build -b <board>` and `west flash` only when hardware is attached.

For the bundled direct Cortex-M scaffold, run flashing or debug validation only when hardware is attached and the user expects hardware access:

```bash
bash scripts/flash.sh
bash scripts/openocd_server.sh
```

If `clang-format`, `clang-tidy`, the selected target compiler, flash/debug tools, or hardware are unavailable, report the skipped step and leave the project ready for that tool.

## References

- Read `references/embedded-project-blueprint.md` when choosing directory layout, CMake/toolchain settings, target ecosystem layers, target-family parameters, flashing/debug flow, or CI design.
- Read `references/firmware-package-matrix.md` when choosing or validating vendor firmware packages, SDK paths, `vendor/` directories, `.atpack` files, `west` manifests, ESP-IDF/Pico SDK setup, CMSIS applicability, or RTOS package layering.
- Read the scaffold script before changing generated linker/startup defaults, supported MCU arguments, or generated command entry points.
- Read `assets/` before changing standard generated configuration files; treat those files as templates and keep board-, MCU-, probe-, and project-specific values behind `@PLACEHOLDER@` variables.
