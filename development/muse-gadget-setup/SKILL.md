---
name: muse-gadget-setup
description: Get a Meta Muse gadget working from one sentence like "I have [hardware]. I want Muse to [thing]." Picks the right path (Muse Home Link, Linux Device SDK on a Raspberry Pi or Linux box, or ESP32 Device SDK firmware), the right board, the exact token, Developer mode, build, flash, install and pairing steps from the official facebookincubator/muse-gadget-sdk docs, how to add commands or behaviour, and a debugging checklist built from the docs, GitHub issues and Hacker News reports. Use for Muse Gadgets, Muse Home Link, MuseGadget pairing, ESP32 or Raspberry Pi with Muse, mgst_ SDK tokens, or any "make Muse do X on my hardware" request.
---

# Muse Gadget Setup

Muse Gadgets (launched 2026-10-02) are devices you build that connect to Meta's Muse agent. Official code: https://github.com/facebookincubator/muse-gadget-sdk (Apache 2.0). Site: https://gadgets.muse.ai/

Facts here were checked against the repo at commit `b9008ab` (2026-10-02) and the pages linked. The repo changes fast: before giving commands, re-read `README.md`, `esp32/README.md`, `esp32/AGENTS.md`, `esp32/devices/README.md` and `linux/README.md` from the live repo and prefer them over this file if they differ.

## Step 0. Parse the request

From "I have [hardware]. I want Muse to [thing].", extract:

1. **Interaction** wanted: control existing home devices, run things on a computer, talk to Muse with a button, see status or pictures, read sensors, take photos, hear spoken replies, something custom.
2. **Hardware** they own (exact model, chip, flash, PSRAM if known).
3. **Constraints**: country (Muse is US only at launch), Muse subscription (needed only for Home Link), OS of their computer (ESP32 build docs cover macOS and Linux only).

Rule: pick the interaction first, then the hardware that supports it. If their hardware cannot do the interaction, say so and name the cheapest supported board that can.

## Step 1. Decide the path

| They want Muse to... | Path | Why (source) |
|---|---|---|
| Control devices already on the home network (lights, TVs, speakers, printers, vacuums) with no building | **A. Muse Home Link**, if they are a US Muse subscriber and got one | "Connect Muse to your home Wi-Fi so it can reach compatible devices you already own" (https://gadgets.muse.ai/home-link) |
| Same, but no Home Link (not US subscriber, sold out, or want to tinker) | **C. ESP32** on a board with the home-network tunnel, e.g. ESP32-C5 DevKitC-1 (same chip as Home Link) | Home Link is ESP32-C5 running firmware based on this SDK (https://gadgets.muse.ai/home-link); tunnel boards let Muse "reach the devices you already own and anything you build with a local HTTP API" (esp32/README.md). Community skills working through a DIY tunnel board is an inference, not confirmed in docs. |
| Run shell commands, manage files, sysadmin, Home Assistant, cron-like checks, bridge webhooks into Muse chat | **B. Linux Device SDK** on a Raspberry Pi or Linux box with Bluetooth LE | Commands `system.run`, `file.read`, `file.write`, `device.health`; `musegadget send-user-msg` (linux/README.md) |
| Press a button and talk to Muse, see answers as captions, avatar on a screen | **C. ESP32**, a board with "UI" and push-to-talk | esp32/devices/README.md feature table |
| Glanceable status and pictures Muse sends | **C. ESP32**, any board with "Images from Muse" | same |
| Air quality (CO2, tVOC, temp, humidity) | **C. ESP32**, Seeed SenseCAP Indicator D1S or D1Pro | `sensors.read`, needs Seeed's stock RP2040 firmware (esp32/devices/README.md) |
| Take photos | **C. ESP32**, Seeed SenseCAP Watcher with camera enabled in menuconfig | `camera.capture` (esp32/devices/README.md) |
| Spoken replies | Not built in. Replies are text; add your own TTS API | esp32/README.md, PR #12, issue #14 |
| Show things on a TV via HDMI | No supported path yet. "Muse on your TV" stick is "Coming soon" | https://gadgets.muse.ai/ |
| A custom sensor or actuator | **B. Linux** (add a Python command, easiest) or **C. ESP32** (C firmware work) | linux/AGENTS.md "Adding a command"; see references/extend.md |

If they named hardware, go straight to `references/boards.md` and check it supports the interaction. If it is not in the official list, it is a port: say so and point them to `esp32/devices/AGENTS.md` (porting recipe).

## Step 2. Prerequisites (all paths except Home Link firmware)

1. **Muse account and the Muse app** on iOS or Android (README.md). Muse rolled out in the US only (https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/).
2. **SDK token** (`mgst_...`) from https://gadgets.muse.ai/settings/sdk-tokens (Account > SDK tokens). Every gadget needs one to pair, including your own. Read https://gadgets.muse.ai/sdk-terms first. Never print or commit the full token.
3. **Developer mode**: Muse app > Settings > Devices > Developer mode. Without it, community devices named `MuseGadget...` do not show up (README.md).
4. Path-specific setup: `references/setup-esp32.md`, `references/setup-linux.md`, `references/home-link-and-skills.md`.
5. **Pair**: Muse app > Settings > Devices > Add Device (the + icon, top right). Pick `MuseGadget-XXXXXX` (ESP32) or `MuseGadgetXXXXXX` (Linux, no hyphen). Accept the community device warning.
6. Then add behaviour: `references/extend.md`.

Home Link is different: plug in, add it in the Muse app, choose Wi-Fi, add community skills. No token or flashing; it "only runs official firmware and can't be reflashed" (https://gadgets.muse.ai/home-link).

## Step 3. Give the answer in this shape

1. Path and board, one line each, with the reason.
2. Shopping list if they need hardware (board, USB data cable, for Linux a Pi with Bluetooth).
3. Numbered setup steps copied from the relevant reference file, with their board's exact build and flash command.
4. How to make Muse do their "thing" (skill, command, prompt, or code change).
5. What will not work and the workaround (limits below).
6. "If it fails" pointer to the matching rows in `references/debugging.md`.

If you are an agent with shell access and the board is plugged in: identify the board before flashing (esp32/AGENTS.md "Identify the board first"), back up vendor firmware where the docs say to (SenseCAP Watcher, StickS3, StickC Plus2), and run flash and monitor outside any sandbox (serial port access).

## Key limits (details in references/limits-and-terms.md)

- Muse is US only at launch; Home Link is free only to active US Muse subscribers, one each, 5,000 units, ships in October, claim is a waitlist place, not an order.
- Home Link cannot be reflashed. Build your own on an ESP32 board instead.
- Replies to gadgets are text. Voice in, text out. Spoken output needs your own TTS.
- Boards without PSRAM (ideaspark, Waveshare C6, classic ESP32) have no home-network tunnel.
- SDK token: personal, non-commercial, max 50 devices per token, no selling devices with it, can be revoked; SDK "not a supported product and not a developer platform".
- Linux gadget: Muse gets the installing account's permissions, sudo included if that account has it. Use `--run-as` with a non-sudo account unless they really want sudo.
- Community pairing has no manufacturer verification and cannot prevent an active man-in-the-middle; pair on a trusted network.
- ESP32 build docs cover macOS and Linux, ESP-IDF v6.0.1 only.

## References

- `references/boards.md`: every supported board with display, audio, buttons, battery, tunnel, build command, sources; community ports.
- `references/setup-esp32.md`: toolchain, token, build, flash, pairing, LED states, per-board quirks.
- `references/setup-linux.md`: install, pair, manage, uninstall.
- `references/home-link-and-skills.md`: Home Link setup and community device skills.
- `references/extend.md`: adding commands and behaviour (Linux and ESP32), avatar, TTS, sending messages to Muse.
- `references/debugging.md`: symptom to fix checklist from docs, issues and HN.
- `references/limits-and-terms.md`: region, subscription, token terms, security, what is not possible.
