---
name: probe-allowed-tools-shell
description: Twin of probe-allowed-tools whose allowed-tools value is the bare tool name shell, as some platforms spell it. Use when asked to probe allowed-tools shell naming.
allowed-tools: shell
---

# Allowed-Tools Naming Probe (Shell Twin)

The spec's experimental `allowed-tools` field is "a space-separated
string of tools that are pre-approved to run," but it leaves tool names
to each platform, and platforms spell their shell tool differently. This
twin declares the bare generic spelling one platform uses for its shell
tool, then asks for the same printf as `probe-allowed-tools`, so testers
can see whether the field's effect depends on matching the platform's own
tool name. This body deliberately never spells out the field's literal
value.

## Canary Phrase

The canary phrase for this skill's body is: **AUKLET-CHERT-3364**

## Instructions

When activated:

1. Report: "probe-allowed-tools-shell activated. Canary: **AUKLET-CHERT-3364**"

2. Report whether you can see an `allowed-tools` value for this skill,
   and if so, what it says.

3. Run exactly this command and report its output verbatim, or the exact
   error if it was blocked: `printf 'ROOK-%s-8841\n' 'GABBRO'`

4. Report whether the command ran without any permission prompt or
   approval step, as far as you can observe.
