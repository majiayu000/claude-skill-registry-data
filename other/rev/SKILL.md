---
category: ctf
name: rev-category-tools
description: Rev kategorisi SKILL.md — Binary analysis, disassembly, symbolic execution araçları kurma rehberi
tags: [ctf, reverse-engineering, tools, setup, radare2, ghidra, angr]
adapted_for: fetih
---

# Reverse Engineering Kategorisi — Gerekli Araçlar

Binary tersine mühendislik, decompilation, symbolic execution ve constraint solving araçları.

## Gerekli Araçlar

| Araç | Açıklama | Kurulum |
|------|----------|---------|
| **gdb** | GNU debugger — binary adım adım debug | `sudo apt-get install gdb` |
| **radare2** | Binary disassembly ve reverse engineering | `sudo apt-get install radare2` |
| **ghidra** | NSA decompiler (~500MB) | `fetih download-tools rev` → ghidra |
| **pwntools** | Exploit lib — binary manipulation | `pip install pwntools` |
| **pwndbg** | GDB plugin (reverse engineering) | Git kurulum `/opt/pwndbg` |
| **ropper** | ROP gadget + instruction finder | `pip install ropper` |
| **angr** | Symbolic execution engine | `pip install angr` |
| **z3-solver** | SMT solver — constraint solving | `pip install z3-solver` |
| **checksec** | Binary proteksiyonları kontrol | `pip install checksec` |
| **androguard** | Android APK disassembly | `pip install androguard` |
| **frida-tools** | Dynamic instrumentation (Android/iOS) | `pip install frida-tools` |
| **objection** | Frida wrapper (SSL/root bypass) | `pip install objection` |

## Araçları Hızlı Kur

Rev kategorisine ait tüm araçları kur:

```bash
fetih download-tools rev
```

Bu kurulum:
- apt araçları → sistem paketi
- pip araçları → Python venv
- ghidra → opsiyonel (büyük)

## Araçlar Kurulu mu Kontrol Et

```bash
# Tüm rev araçları
fetih download-tools status | grep -A 15 "REV"

# Manuel kontrol
which gdb radare2 ghidra
python3 -c "import angr, z3; print('Rev tools OK')"
```

## Her Araç Neye Yarar?

### Static Analysis (Dosyayı çalıştırmadan)

#### radare2
Disassembly ve binary analiz

**Skill'lerde kullanılır:**
- `rev/elf-static-analysis` → code flow analysis
- `rev/anti-debug-obfuscation` → anti-debug detection
- `rev/android-apk-analysis` → ARM disassembly

```bash
r2 ./binary
[0x...]> aaa              # analyze all
[0x...]> pdf @main        # disassemble main
[0x...]> iz               # strings
[0x...]> s 0x1234         # seek address
[0x...]> /R "mov rax"     # instruction arama
```

#### ghidra
GUI decompiler — source code-like gösterim

**Skill'lerde kullanılır:**
- `rev/elf-static-analysis` → decompilation
- `rev/android-apk-analysis` → Java decompile (APK)
- `rev/z3-constraint-solving` → algorithm reverse

```bash
ghidra &
# GUI: binary yükle → Analyze → Decompiler pane
# Veya: ghidraRun ./binary
```

#### pwntools
Binary parsing + manipulation

**Skill'lerde kullanılır:**
- `rev/elf-static-analysis` → ELF header parsing
- `rev/android-apk-analysis` → file structure

```python
from pwn import *
elf = ELF('./binary')
print(elf.symbols)
print(elf.got)
```

### Dynamic Analysis (Debugger)

#### gdb + pwndbg
Debugger — runtime behavior, registers, memory

**Skill'lerde kullanılır:**
- `rev/elf-static-analysis` → runtime validation
- `rev/z3-constraint-solving` → input testing
- `rev/anti-debug-obfuscation` → anti-debug bypass

```bash
gdb ./binary
(gdb) break main
(gdb) run arg1 arg2
(gdb) ni          # next instruction
(gdb) si          # step into
(gdb) info registers
(gdb) x/50x $rsp  # memory dump
```

#### ropper
Instruction/gadget finder (ROP/stack manipulation)

**Skill'lerde kullanılır:**
- `rev/z3-constraint-solving` → gadget arama
- `rev/elf-static-analysis` → stack pivot

```bash
ropper -f ./binary --search "mov rax" --opcode
ropper -f ./binary --search "int 0x80" --only-opcode
ropper -f ./binary --chain jmp
```

### Symbolic Execution & Constraint Solving

#### angr
Symbolic execution — conditional logic automation

**Skill'lerde kullanılır:**
- `rev/z3-constraint-solving` → path exploration
- `rev/elf-static-analysis` → input discovery

```python
import angr
proj = angr.Project('./binary')
state = proj.factory.entry_state(argv=['./binary', 'arg'])
simgr = proj.factory.simgr(state)
simgr.explore(find=lambda s: b'flag' in s.posix.dumps(1))
```

#### z3-solver
SMT solver — constraint satisfaction

**Skill'lerde kullanılır:**
- `rev/z3-constraint-solving` → denklem çözme
- `rev/elf-static-analysis` → input validation

```python
from z3 import *
x = Int('x')
y = Int('y')
solve(x > 5, y < 10, x + y == 20)
```

### Android Specific

#### androguard
APK disassembly ve static analysis

**Skill'lerde kullanılır:**
- `rev/android-apk-analysis` → APK to DEX parsing

```bash
androguard apk app.apk
```

#### frida-tools
Dynamic instrumentation — runtime hook'lar

**Skill'lerde kullanılır:**
- `rev/android-apk-analysis` → method hooking
- `rev/anti-debug-obfuscation` → anti-debug bypass

```bash
frida -U -f com.example.app --no-pause -l hook.js
```

#### objection
Frida wrapper — SSL bypass, root detection bypass

**Skill'lerde kullanılır:**
- `rev/android-apk-analysis` → bypass automation

```bash
objection -g com.example.app explore
android sslpinning disable
```

### Supporting Tools

#### checksec
Binary proteksiyonları (NX, PIE, Canary vb.)

**Skill'lerde kullanılır:**
- `rev/elf-static-analysis` → security feature detection

```bash
checksec --file=./binary
# Çıktı:
#   NX        : ENABLED
#   PIE       : ENABLED
#   Canary    : ENABLED
```

---

## Kurulum Sorunları Çözme

### radare2 eski sürüm

Latest version kur:

```bash
sudo apt-get install -y radare2
# veya: sudo apt-get install -y radare2-dev
```

### ghidra decompiler "not found"

Java kurulu mu kontrol et:

```bash
java -version
# yoksa: sudo apt-get install -y openjdk-11-jre
ghidra &
```

### angr symbolic execution timeout

Explore depth limit'i ayarla:

```python
simgr.explore(find=..., avoid=..., step_limit=100000)
```

### frida USB aracı bağlanmıyor

Adb kurulum:

```bash
sudo apt-get install -y android-tools-adb
adb devices
frida-ps -U
```

---

## Hızlı Test Scripti

```bash
python3 << 'EOF'
import shutil

print("=== Rev Tools Check ===")

static_tools = ['gdb', 'radare2', 'ghidra']
for tool in static_tools:
    if shutil.which(tool):
        print(f"✓ {tool}")
    else:
        print(f"✗ {tool}")

try:
    import angr
    print("✓ angr (Python)")
except ImportError:
    print("✗ angr")

try:
    import z3
    print("✓ z3 (Python)")
except ImportError:
    print("✗ z3")

try:
    import androguard
    print("✓ androguard (Android)")
except ImportError:
    print("✗ androguard")

print("\nÇözüm: fetih download-tools rev")
EOF
```

---

## Notlar

- **radare2** → quick disassembly için çok hızlı
- **ghidra** → decompilation için en iyi (ama 500MB)
- **gdb + pwndbg** → debugging, conditional breakpoint
- **angr** → complex input discovery, symbolic execution
- **z3** → constraint solving, denklem çözme
- **Android** (`androguard`, `frida`, `objection`) → APK analiz için

Skill okudoğunda başında hangi araçlar gerekli gösterilecek!

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: 46a255ba9738231f
-->

