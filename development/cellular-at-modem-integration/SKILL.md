---
name: cellular-at-modem-integration
description: Use when integrating or debugging cellular AT modems (Quectel, SIMCom, u-blox) over UART for CREG/CEREG registration, CGDCONT APN/PDP, TCP/UDP sockets, or URC parsing
---

# Cellular AT Modem Integration

## Overview

Use this skill to drive a 2G/4G/NB-IoT/LTE-M cellular modem from an MCU over UART with the AT command set. The hard parts are parsing unsolicited result codes (URCs) that interleave with command responses on one serial line, choosing the right registration command per radio access technology, using the correct socket command set for the specific module family, and getting PWRKEY boot timing right before any AT works.

## When To Use

Use this skill when:

- The user integrates Quectel (`EC25`, `BG96`, `BC66`), SIMCom (`SIM7600`, `SIM800C`, `A7670`), or u-blox (`SARA-R4`, `SARA-R5`) over UART.
- The issue involves registration (`AT+CPIN?`, `AT+CSQ`, `AT+CREG?`, `AT+CGREG?`, `AT+CEREG?`), APN/PDP (`AT+CGDCONT`, `AT+CGATT`, `AT+CGACT`), or sockets (`AT+QIOPEN`, `AT+QISEND`, `AT+CIPSTART`/`AT+CIPOPEN`, `AT+USOCO`).
- URCs such as `RING`, `+CMTI`, or `+QIURC` corrupt command parsing, or power saving (`AT+CPSMS`, `AT+CEDRXS`) breaks reachability.

Do not use this skill when the UART link itself is unproven; confirm the modem echoes `AT` with `OK` at the configured baud first.

## First Questions

Ask for:

- Exact module and firmware revision (`ATI`, `AT+CGMR`), and radio technology: 2G, LTE Cat-1, Cat-4, Cat-M1, or NB-IoT.
- UART wiring: baud, flow control (RTS/CTS), and whether `PWRKEY`/reset lines are MCU-controlled.
- SIM type and the operator APN (some IoT SIMs need username/password or a specific `<PDP_type>`).
- Transport goal: raw TCP/UDP, or bridging to MQTT/TLS on top of the socket AT layer.
- Current failing command and its literal response or error code.

## Integration Checklist

1. Bring up the modem.
   Assert `PWRKEY` for the module's specified pulse width, wait for boot (often signalled by an `RDY` URC), then confirm `AT` returns `OK` and disable echo with `ATE0`.

1. Unlock and check signal.
   `AT+CPIN?` must return `+CPIN: READY`; `AT+CSQ` RSSI must be non-`99` (0-31 valid). Set `AT+CFUN=1` if radio is off.

1. Confirm registration on the right command.
   Use `AT+CREG?` for 2G/CS registration, `AT+CGREG?` for GPRS/PS, and `AT+CEREG?` for LTE/Cat-M1/NB-IoT (EPS). `<stat>` must be `1` (home) or `5` (roaming).

1. Define and activate the PDP context.
   `AT+CGDCONT=1,"IP","<apn>"`, then `AT+CGATT=1` to attach and `AT+CGACT=1,1` to activate. Verify an assigned IP with `AT+CGPADDR`.

1. Open the socket with the correct vendor stack for the module family.
   - Quectel (`EC25`/`BG96`/`BC66`): `AT+QIOPEN`, then `AT+QISEND`/`AT+QIRD`/`AT+QICLOSE`.
   - SIMCom 2G (`SIM800`-class): `AT+CIPSTART`, then `AT+CIPSEND` (write payload after `>`, terminate with `Ctrl+Z` `0x1A`).
   - SIMCom LTE (`SIM7600`/`A76XX`-class): `AT+NETOPEN` first, then `AT+CIPOPEN` to open a socket and `AT+CIPSEND` to send (`AT+CIPSEND=<link>,<len>` takes an explicit length; no `Ctrl+Z` when a length is given). Read buffered data with `AT+CIPRXGET`; close with `AT+CIPCLOSE`/`AT+NETCLOSE`.
   - u-blox (`SARA`): `AT+USOCR` to create, `AT+USOCO` to connect, `AT+USOWR` to write, `AT+USORD` to read, `AT+USOCL` to close.

1. Build a URC-aware parser.
   Run a line-based state machine that classifies each line as echo, intermediate (`>`), final (`OK`/`ERROR`/`+CME ERROR`), or URC (`RING`, `+CMTI:`, `+QIURC:`), and route URCs to callbacks instead of the command waiter.

## Common Failures

- Sending AT before boot completes; commands are dropped until the `RDY` URC or a fixed power-on delay elapses.
- Checking `AT+CREG?` on an LTE-only module that only registers via `+CEREG`, so registration looks stuck at `0,2`.
- Registration fails from wrong APN, disabled radio (`AT+CFUN=0`), locked SIM, or poor signal (`+CSQ: 99,99`).
- Using the wrong socket stack: sending `AT+CIPSTART` to a `SIM7600`/`A76XX` module (which needs `AT+NETOPEN`+`AT+CIPOPEN`), or forgetting `AT+NETOPEN` before `AT+CIPOPEN`.
- Fixed read timeout truncates variable-length responses like `AT+QIRD` or a slow `AT+COPS=?` scan.
- URC (e.g. `+QIURC: "recv"`) arrives mid-response and the parser mistakes it for the command reply, causing a parse race.
- `AT+CIPSEND` on a `SIM800`-class module sent without the `Ctrl+Z` terminator, so the modem waits forever at the `>` prompt.
- After `AT+CPSMS`/`AT+CEDRXS` the module sleeps and drops the socket; sending during PSM fails until wake and re-attach.

## Verification

Before claiming the link works:

- State the module, technology, APN, and which registration command applies.
- Confirm `+CPIN: READY`, a valid `+CSQ`, and `<stat>=1` or `5` on the correct `CxREG`.
- Confirm `AT+CGPADDR` shows an IP before opening any socket.
- Send a round-trip TCP payload and confirm the receive path for the module family (`+QIURC: "recv"`/`AT+QIRD`, or `+CIPRXGET`, or `+USORD`).
- Prove the URC parser handles an unsolicited `RING`/`+CMTI` arriving during a command without desync.
- If PSM/eDRX is enabled, confirm wake, re-registration, and data resume.

## Example

User:

```text
BG96 用 AT+CEREG? 一直返回 0,2,连不上网,该怎么查?
```

Agent:

1. Confirms boot done, `ATE0` set, then checks `AT+CPIN?` = `READY` and `AT+CSQ` is not `99`.
1. Verifies `AT+CFUN=1` and the APN via `AT+CGDCONT?`; fixes APN if wrong for the IoT SIM.
1. Waits for `+CEREG: 0,1`/`0,5`, then runs `AT+CGACT=1,1` and `AT+CGPADDR` before opening a socket with `AT+QIOPEN`.
