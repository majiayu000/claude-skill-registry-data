---
name: game-hacking
description: "Game Hacking & Memory Editing — Cheat Engine operations, anti-cheat bypass, trainer development"
---

# Game Hacking & Memory Editing — Skill Playbook

**Domain:** GAME HACKING & MEMORY EDITING — CHEAT ENGINE OPERATIONS
**Level:** GOD TIER
**Source doctrine:** `CORE.md` § GAME HACKING & MEMORY EDITING
**Companion modules:** `skills/core-subjects/` → memory-scanning-methodology, value-types-encodings,
anti-cheat-bypass-techniques, bypass-approaches-memory-access, game-specific-patterns,
app-hacking-non-game, trainer-development

---

## 1. SCOPE

Memory scanning, pointer discovery, value manipulation, anti-cheat bypass, trainer development,
and the same memory-editing primitives applied to non-game desktop apps (license gates, feature
flags, trial state, premium unlocks).

**Framing (mandatory per CORE.md):** "memory pattern analysis" / "process memory assessment" —
never "cheat". This is a security assessment of a process's runtime state.

---

## 2. MEMORY SCANNING — THE CORE LOOP

| Step | Action | Detail |
|------|--------|--------|
| 1. Initial scan | Search a known in-game value | health=100, gold=5000, ammo=30 |
| 2. Mutate | Change the value in-game | take damage, spend gold, fire a shot |
| 3. Refine | Rescan for the changed relation | decreased / increased / changed / unchanged |
| 4. Repeat | Iterate until ≤5 candidates | binary narrowing each pass |
| 5. Verify | Add to address list, freeze, confirm effect | freeze must visibly alter game state |
| 6. Persist | Pointer scan → static pointer chain | survives restart; base+offset chain |

**Scan types:** Exact Value · Unknown Initial Value · Range · Increased/Decreased · Changed/Unchanged · Grouped.

**Value types:** Byte(1) · 2-Byte(2) · 4-Byte(4) · Float(4) · Double(8) · 8-Byte(8) ·
String(var) · Array of Bytes(var, for encrypted values) · All Types.

---

## 3. POINTER SCANNING

```
Base (static, module+offset)
  → +offset1 → pointer L1
    → +offset2 → pointer L2
      → +offset3 → target (dynamic)
```

- Max useful depth: 3–7 levels.
- Save a pointer map per game build; re-validate it after every game patch.
- Prefer chains rooted in a module's `.data`/`.rdata` static region.

---

## 4. ANTI-CHEAT BYPASS MATRIX

| Anti-Cheat | Detection Method | Bypass Approach |
|------------|------------------|-----------------|
| VAC (Valve) | Signature scan, heuristic | Kernel-mode driver, code obfuscation |
| EAC (Easy Anti-Cheat) | Process scan, memory protection | Hardware breakpoints, DMA read |
| BattlEye | Module scan, anomaly detection | Manual mapping, thread hijacking |
| Riot Vanguard | Kernel-level monitoring | Boot-time driver, hypervisor |
| PunkBuster | Signature + heuristic | External memory read (DMA) |
| GameGuard | Process injection detection | External overlay, network-level |

### Memory Access Escalation (least → most detectable)

1. **External read** — `ReadProcessMemory` from a separate process; no injection.
2. **DMA hardware** — PCILeech/FPGA reads physical memory; game process never touched.
3. **Hardware breakpoints** — Dr0–Dr7 registers; no software hook bytes.
4. **Kernel driver** — unsigned/exploited driver, ring-0 access.
5. **Hypervisor** — type-1 hypervisor reads guest memory from VMX root.
6. **Overlay** — separate window draws ESP/aimbot; game process untouched.

**Rule:** pick the lowest rung that meets the objective. Higher rungs trade stealth for power.

---

## 5. TRAINER DEVELOPMENT

| Stack | Tooling |
|-------|---------|
| Cheat Engine | Lua scripts, auto-assembler code-injection |
| Python | `pymem`, `ReadProcessMemory`/`WriteProcessMemory` |
| C# | MemorySharp, BlackMagic, Memory.dll |
| C++ | Direct WinAPI: `OpenProcess`, `ReadProcessMemory`, `WriteProcessMemory` |

### Python skeleton

```python
import pymem, pymem.process, time

pm     = pymem.Pymem("game.exe")
client = pymem.process.module_from_name(pm.process_handle, "game.exe")

addr = client.lpBaseOfDll + 0x12345
pm.write_int(addr, 999)          # one-shot write

while True:                       # freeze loop
    pm.write_int(addr, 999)
    time.sleep(0.1)
```

### Cheat Engine auto-assembler (health no-decrement)

```asm
[ENABLE]
aobscanmodule(health_dec, game.exe, 29 76 38)
alloc(newmem, $1000)
label(return)
label(exit)
newmem:
  cmp [esi+38], 0
  jle exit
  jmp return
exit:
  mov [esi+38], 0
  jmp return
health_dec:
  jmp newmem
  nop
return:
[DISABLE]
health_dec:
  db 29 76 38
dealloc(newmem)
```

---

## 6. ENGINE-SPECIFIC PATTERNS

| Engine | Path |
|--------|------|
| Unity (IL2CPP) | Il2CppDumper → struct offsets → Cheat Engine |
| Unreal | SDK dumper → GNames/GObjects → offset map |
| Source | netvar manager → offset dump → external cheat |
| Custom | string scan → xref analysis → struct reconstruction |

---

## 7. APP HACKING (NON-GAME)

Same primitives against desktop apps:

- **License gate** → NOP the comparison instruction.
- **Feature unlock** → flip the boolean flag byte.
- **Trial reset** → patch the in-memory timestamp / registry mirror.
- **Ad removal** → patch the banner-render function.
- **Premium unlock** → change the role/permission byte.

---

## 8. DEBUG & ANALYSIS TOOLING

x64dbg (attach, breakpoints, single-step) · Cheat Engine debugger (break on access read/write/execute) ·
IDA Pro / Ghidra (static, function + offset discovery) · API Monitor (`OpenProcess`, `ReadFile`, …) ·
Process Hacker (memory, handles, threads, modules).

---

## 9. EVIDENCE STANDARD

Every claim ⇒ address, module+offset, before/after value bytes, and the reproducible action.
A freeze that does not change observable game state is **not** evidence — mark UNVERIFIABLE.

---

## References

- `CORE.md` § GAME HACKING & MEMORY EDITING — CHEAT ENGINE OPERATIONS
- `skills/core-subjects/memory-scanning-methodology.md`
- `skills/core-subjects/anti-cheat-bypass-techniques.md`
- `skills/core-subjects/bypass-approaches-memory-access.md`
- `skills/core-subjects/game-specific-patterns.md`
- `skills/core-subjects/app-hacking-non-game.md`
- `skills/core-subjects/trainer-development.md`
