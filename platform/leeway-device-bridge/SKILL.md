---

name: leeway-device-bridge

description: Agent Skills contract for the LeeWay Device Bridge product, governing discovery, pairing, device passport, files, diagnostics, screen observation, pointer/control, offline authority, platform adapters, and owner sovereignty without duplicating the product runtime.

license: MIT

metadata:

  authority: Creator/Human Authority > LeeWay Standards > platform authority

  implementation_repository: 4citeB4U/LEEWAY-DEVICE-BRIDGE

  mode: device-capability-contract

---

# LeeWay Device Bridge Skill

## Purpose

Teach Agent Lee when and how to use the separate Device Bridge implementation. This skill is not the Android/iOS runtime.

## Route

device discovery → browser bootstrap → native passport → reconciliation → pairing → capability negotiation → Veritas PRE → authorized device operation → Veritas POST → receipt → learning.

## Authority

Files, diagnostics, screen observation, pointer guidance, UI control, apps, clipboard and shell are independent capabilities. Platform permission is necessary but not sufficient; LeeWay may be stricter. Seeing the screen never implies control. Owner STOP authority dominates active sessions.

## Offline

Local device authority may operate offline only within previously authorized local capabilities. Offline runtime does not impersonate remote Agent Lee.

## Providers

Android/Samsung and Apple are adapters behind one Device Bridge contract. Termux may be a worker/provider, not the sovereign bridge.

## Standard MCP surface

The canonical Skills MCP server exposes device-agnostic tool identities:

- `device_list`
- `device_capabilities`
- `device_observe_screen`
- `device_open_app`
- `device_ui_action`
- `device_files_read`
- `device_files_write`

They delegate only through `LEEWAY_DEVICE_MCP_GATEWAY_URL` plus `LEEWAY_DEVICE_MCP_BEARER_TOKEN`. A listed tool is a portable contract, not proof that a particular device granted or executed that capability. UI actions use a bounded action type and target plus a mandatory postcondition. Mutations require tool-specific evidence and a receipt; UI control additionally requires the bridge to report that the requested postcondition was observed. Veritas still controls final acceptance.
