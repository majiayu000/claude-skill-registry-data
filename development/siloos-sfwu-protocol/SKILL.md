---
name: siloos-sfwu-protocol
description: "Implementing TopBrewer commands, debugging packet parsing, and verifying CRC32 checksums."
---

# SiloOS SFWU Protocol Skill

## When to Use
- Implementing new TopBrewer commands
- Debugging packet parsing issues
- Verifying CRC32 checksum calculations
- Adding new response parsers

## Prerequisites
- Understanding of binary protocols and hex encoding
- Familiarity with BLE GATT characteristics
- Knowledge of the SFWU packet structure

## Protocol Reference

### Packet Format
```
Byte:   0      1-2        3-4       5-6       7..N-4    N-3..N
Field:  HEADER LENGTH     COMMAND   ADDRESS   PAYLOAD   CRC32
Size:   1      2          2         2         variable  4
```

- **HEADER**: Always `0x01`
- **LENGTH**: Total packet length (big-endian uint16)
- **COMMAND**: Command code (big-endian uint16)
- **ADDRESS**: Target address (big-endian uint16)
- **PAYLOAD**: Command-specific data
- **CRC32**: CRC32-CCITT over all preceding bytes

### Key Commands (from constants.ts)
| Command | Code | Description |
|---------|------|-------------|
| RESET | 0x00C0 | Reset machine state |
| GET_MENU | 0x00C1 | Request drink menu |
| GET_MENU_DETAILS | 0x00C2 | Request menu item details |
| ORDER | 0x00C3 | Place a drink order |
| GET_BREW_STATUS | 0x00C4 | Poll brewing progress |
| GET_TEMPERATURES | 0x00C5 | Request temperature readings |

### CRC32-CCITT Implementation
```typescript
// From CRC32.ts — DO NOT modify this implementation
Polynomial: 0xEDB88320 (reflected)
Initial:    0xFFFFFFFF
Final XOR:  0xFFFFFFFF
```

## Procedure

### Adding a New Command
1. Define the command code in `sfwu/constants.ts`
2. Create a builder in `sfwu/commands/`
3. Use `SFWU.buildPacket(command, address, payload)` to construct
4. CRC32 is calculated automatically

### Adding a New Parser
1. Create parser in `sfwu/parsers/`
2. Implement `parse(data: Uint8Array): YourEntity`
3. Add entity interface in `entities/`
4. Register in `ResponseFactory.ts`

### Testing Packets
Use the existing test vectors in `sfwu/tests.ts`:
```typescript
const packet = SFWU.buildPacket(0x00C1, 0x0000, new Uint8Array([]));
```

## Expected Outcomes
- Packets build correctly with valid CRC32
- Responses parse into correct TypeScript entities
- No data corruption across BLE chunked writes
