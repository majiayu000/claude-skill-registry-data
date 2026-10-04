---
name: find-Host_Say
description: |
  Find and identify the Host_Say function in the CS2 server binary using IDA Pro MCP. Use this skill when
  reverse engineering CS2 server.dll or libserver.so to locate the chat-broadcast/say-command handler by finding
  the code that references the console chat-relay log format string "%s %s @ %s: ".
  Trigger: Host_Say
disable-model-invocation: true
---

# Find Host_Say

Locate `Host_Say` in CS2 `server.dll` / `libserver.so` using IDA Pro MCP tools.

## Method

### 1. Find the Chat-Relay Format String

```text
mcp__ida-pro-mcp__find_regex pattern="%s %s @ %s:"
```

`Host_Say` logs every broadcast chat message to the console/log using a format string of the shape
`"%s %s @ %s: "` (e.g. `"<player> say[_team]* @ <lobby/lobbyid>: "`-style console relay tag), which is unique in
the binary.

> Linux 14168 reference: the string `"%s %s @ %s: "` is at `0x91b835`.

### 2. Get the Referencing Function

```text
mcp__ida-pro-mcp__xrefs_to addr="0x91b835"
```

The string has exactly one xref; its containing function is `Host_Say`.

> Linux 14168 reference: `0x91b835` is referenced from `0x17ece73`, inside the function starting at `0x17ec540`
> (size `0xa0e`).

### 3. Sanity-Check the Candidate

```text
mcp__ida-pro-mcp__decompile addr="0x17ec540"
```

Confirm the decompilation is consistent with `Host_Say`'s known role: takes a client/command-context pointer, a
parsed command-args structure, and flags distinguishing team-say from all-chat; builds/sanitizes the chat text,
applies mute/gag and dead-talk restrictions, then relays the formatted message to the console and to recipients
via the networking layer.

### 4. Generate Function Signature

**ALWAYS** Use SKILL `/generate-signature-for-function` with `addr=0x17ec540` to generate a robust and unique
`func_sig`.

> Linux 14168 reference: generated signature is `55 48 89 E5 41 57 49 89 F7 41 56 41 55 41 89 D5` — already
> unique across the binary at this length.

### 5. Write IDA Analysis Output as YAML

**ALWAYS** Use SKILL `/write-func-as-yaml` to write the analysis results.

Required parameters:
- `func_name`: `Host_Say`
- `func_addr`: `0x17ec540`
- `func_sig`: The validated signature from step 4

## Function Characteristics

- **Purpose**: Handles the `say`/`say_team` command path — validates/sanitizes chat text, applies mute/gag and
  dead-talk rules, and relays the message to the console log and to the appropriate set of recipients.
- **Binary**: `server.dll` / `libserver.so`
- **Parameters**: `(unsigned __int8 *pEntityOrClient, int *pArgsOrCookie, unsigned __int8 bTeamOnly, unsigned int
  a4, __int64 a5)` (observed decompiled shape; exact semantic naming of the trailing parameters is not confirmed
  beyond "command context/flags").
- **Return value**: `void`.

## Discovery Strategy

1. `Host_Say` unconditionally logs each processed chat message using the distinctive format string
   `"%s %s @ %s: "`, which does not appear anywhere else in the binary.
2. The string has a single xref, so its containing function is unambiguous.
3. The candidate's parameter shape (client/command context + team-only flag) and body (text sanitization, mute
   checks, console relay) match `Host_Say`'s known behavior.

This is robust because the anchor string is a literal, verbatim format string that survives recompilation and
refactoring as long as the log format itself is unchanged, and it has a single unambiguous xref.

## Output YAML Format

The output YAML filename depends on the platform:
- `server.dll` -> `Host_Say.windows.yaml`
- `libserver.so` -> `Host_Say.linux.yaml`

Fields: `func_name`, `func_va`, `func_rva`, `func_size`, `func_sig`.
