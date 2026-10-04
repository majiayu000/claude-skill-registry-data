---
name: tinyusb-integration
description: Use when integrating, porting, configuring, or debugging TinyUSB device, host, CDC, MSC, HID, MIDI, vendor class, descriptors, DCD, or USB enumeration issues
---

# TinyUSB Integration

## Overview

Use this skill to integrate TinyUSB by separating board support, USB controller driver, descriptors, class drivers, interrupts, clocks, and endpoint buffers. USB bugs are often descriptor or controller-state problems before application logic.

## When To Use

Use this skill when:

- The user wants to add or debug TinyUSB on an MCU.
- The issue involves USB enumeration, CDC serial, MSC, HID, MIDI, vendor class, device/host mode, descriptors, endpoints, DCD/HCD, or TinyUSB tasks.
- The target needs a new MCU/board port or custom USB class configuration.

Do not use this skill when board power, USB D+/D- wiring, or clock source is unverified. Use `hardware-interface-debug` first.

## First Questions

Ask for:

- MCU/board, USB controller, device/host mode, and TinyUSB version.
- USB class: CDC, MSC, HID, MIDI, vendor, composite, or host stack.
- RTOS/bare-metal runtime and where `tud_task`/host task runs.
- USB clock source, VBUS detect, pull-up control, and interrupt routing.
- Descriptors and `tusb_config.h`.
- Host OS symptoms: no enumeration, code 10, repeated reset, missing COM port, wrong VID/PID, or transfer failure.

## Integration Checklist

1. Prove hardware prerequisites.
   USB clock, D+/D- wiring, VBUS, pull-up, ESD/protection, and connector orientation must be correct.

1. Configure `tusb_config.h`.
   Enable only needed roles/classes and set endpoint buffer sizes within RAM limits.

1. Verify descriptors.
   Device, configuration, interface, endpoint, string, VID/PID, class/subclass/protocol, and composite descriptors must agree.

1. Run TinyUSB task regularly.
   In bare metal or RTOS, ensure device/host task and interrupt handling are scheduled correctly.

1. Check class-specific behavior.
   CDC needs line coding/control; MSC needs safe block device hooks; HID needs report descriptors and polling interval.

1. Capture host evidence.
   Use OS device manager, `lsusb`, USB logs, or protocol analyzer when enumeration fails.

## Common Failures

- USB clock is not exactly valid for the controller.
- Descriptors report endpoint sizes or counts inconsistent with class config.
- `tud_task` is not called regularly.
- Composite descriptors have wrong interface association.
- CDC appears but no data flows because callbacks are not handled.
- MSC exposes a block device without safe read/write/sync policy.

## Verification

Before claiming TinyUSB works:

- State MCU, role, class, TinyUSB version, USB clock, and task/interrupt model.
- Confirm host enumeration with VID/PID and class.
- Confirm one class-specific transfer: CDC echo, HID report, MSC read/write, or vendor transfer.
- Confirm descriptor consistency and endpoint allocation.
- For MSC or firmware update classes, state data-loss safeguards.

## Example

User:

```text
TinyUSB CDC 插上电脑没有串口。
```

Agent:

1. Asks for MCU, TinyUSB config, descriptors, USB clock, interrupt setup, and host OS logs.
1. Checks enumeration and descriptor consistency before CDC callbacks.
1. Verifies `tud_task` schedule and a CDC echo transfer.
