---
name: pwn-category-tools
description: Pwn/Binary kategorisi SKILL.md — BOF, ROP, kernel exploit araçları kurma rehberi
tags: [ctf, pwn, binary, tools, setup, pwntools, gdb, radare2, ghidra]
---

# Pwn / Binary Kategorisi — Gerekli Araçlar

Buffer overflow, ROP gadgets, kernel pwn ve binary analiz için araçlar.

## Gerekli Araçlar

| Araç | Açıklama | Kurulum |
|------|----------|---------|
| **gdb** | GNU debugger — binary debug ve analysis | `sudo apt-get install gdb` |
| **pwntools** | Exploit geliştirme Python kütüphanesi | `pip install pwntools` |
| **radare2** | Binary analiz ve disassembly | `sudo apt-get install radare2` |
| **ropper** | ROP gadget bulucu | `pip install ropper` |
| **checksec** | Binary güvenlik kontrol (NX, PIE, ASLR vb.) | `pip install checksec` |
| **pwndbg** | GDB plugin — pwn friendly debugging | Git kurulum: `/opt/pwndbg` |
| **ghidra** | NSA reverse engineering framework (~500MB) | `fetih download-tools pwn` → ghidra seçimi |
| **angr** | Symbolic execution engine | `pip install angr` |
| **z3-solver** | Z3 constraint solver | `pip install z3-solver` |
| **seccomp-tools** | SECCOMP filter analizi | `gem install seccomp-tools` |
| **one_gadget** | libc one-gadget RCE bulucu | `gem install one_gadget` |

## Araçları Hızlı Kur

Pwn kategorisine ait tüm araçları kur:

```bash
fetih download-tools pwn
```

Kurulum sırasında:
- `gdb` ve `radare2` için apt gerekir
- Python kütüphaneleri pip ile yüklenecek
- `ghidra` seçeneği ekstra (büyük, İndir-Kur karşılaştırması yapılır)
- Ruby gem araçları için build-essential gerekli

## Araçlar Kurulu mu Kontrol Et

```bash
# Tüm binary araçları kontrol
fetih download-tools status | grep -A 15 "BINARY"

# Manuel kontrol
which gdb pwntools radare2 ghidra angr
python3 -c "import pwn, angr, z3; print('Binary tools OK')"
```

## Her Araç Neye Yarar?

### gdb + pwndbg
Debugger — binary'yi çalıştırır, memory'de adım adım izler

**Skill'lerde kullanılır:**
- `pwn/buffer-overflow-rop` — BOF'u trigger et, stack overflow gözle
- `pwn/format-string` — Format string olayını debug et
- `pwn/heap-exploit` — malloc/free operasyonlarını izle

```bash
gdb ./binary
(gdb) run arg1 arg2
(gdb) break main
(gdb) x/50x $esp
```

### pwntools
Python exploit geliştirme — process/remote bağlantısı, payload üretimi

**Skill'lerde kullanılır:**
- Tüm pwn skill'lerinde → `from pwn import *`

```python
from pwn import *
p = process('./binary')      # local exploit
p = remote('host', port)     # remote exploit
p.sendline(payload)
p.interactive()
```

### radare2 / r2
Binary disassembly, decompilation, gadget bulma

**Skill'lerde kullanılır:**
- `pwn/buffer-overflow-rop` — ROP gadget arama
- `pwn/srop-attack` — syscall gadget bulma
- `pwn/kernel-pwn-basics` — kernel binary analiz

```bash
r2 ./binary
[0x...]> aaa              # analyze all
[0x...]> /R "mov rax,60;ret"  # gadget ara
[0x...]> pdf @main        # disassemble
```

### ropper
ROP gadget otomatik bulma (radare2 alternatifi)

**Skill'lerde kullanılır:**
- `pwn/srop-attack` → syscall gadget
- `pwn/buffer-overflow-rop` → gadget kombinasyonu

```bash
ropper -f ./binary --search "mov rax"
ropper -f ./binary --search "syscall"
ropper -f ./binary --chain jmp
```

### checksec
Binary proteksiyonlarını kontrol — NX, PIE, ASLR, SMEP vb.

**Skill'lerde kullanılır:**
- Tüm pwn skill'lerinde başlangıç analiz
- Hangi yöntemi seçeceğini belirler

```bash
checksec --file=./binary
# Çıktı örneği:
# RELRO     : Partial
# STACK CANARY : Disabled
# NX        : ENABLED
# PIE       : ENABLED
# ASLR      : ENABLED (işletim sistemi seviyesi)
```

### ghidra
GUI reverse engineering — decompilation, semantic analysis

**Skill'lerde kullanılır:**
- `pwn/buffer-overflow-rop` — source code analiz
- `pwn/kernel-pwn-basics` — kernel binary incelemesi
- `rev/elf-static-analysis` → cross-category

```bash
ghidra  # GUI başlat
# İçinde: binary yükle → analyze → code view / decompiler
```

### angr
Symbolic execution — constraint solving, path exploration

**Skill'lerde kullanılır:**
- `rev/z3-constraint-solving` → symbolic execution
- `pwn/buffer-overflow-rop` → exploit koşullarını verify et

```python
import angr
proj = angr.Project('./binary')
state = proj.factory.entry_state()
simgr = proj.factory.simgr(state)
```

### z3-solver
SMT solver — constraint satisfiability, equation çözme

**Skill'lerde kullanılır:**
- `rev/z3-constraint-solving` → constraint solving
- `pwn/kernel-pwn-basics` → exploit constraint'leri

```python
from z3 import *
x = Int('x')
solve(x > 5, x < 10)
```

### seccomp-tools
SECCOMP filter dump ve analiz — `execve` kısıtlamaları

**Skill'lerde kullanılır:**
- `pwn/seccomp-sandbox-escape` → filter analiz

```bash
seccomp-tools dump ./binary
# filter gösterir → hangi syscall yasaklı
```

### one_gadget
libc'de one-gadget RCE (mühürlü libc heap exploit'leri)

**Skill'lerde kullanılir:**
- `pwn/ret2libc` → libc RCE bypass

```bash
one_gadget /lib/x86_64-linux-gnu/libc.so.6
# Çıktı: 0x4526a, 0x4526b, ... (ORW şelllcode'lar)
```

---

## Kurulum Sorunları Çözme

### "pip install pwntools" başarısız

Bağımlılık eksik — build essentials kur:

```bash
sudo apt-get install -y build-essential python3-dev
pip install pwntools
```

### ghidra çok büyük (500MB)

Download opsiyoneldir — interaktif menüde skip edebilirsin:

```bash
# İndir: 20+ dakika
# Çöz: 2-3 dakika
# Fakat çok güçlü decompiler'ı var
```

### pwndbg kurulum

GDB'de `/opt/pwndbg` kullan:

```bash
# Otomatik kurulur fetih ile
# Manual:
git clone https://github.com/pwndbg/pwndbg /opt/pwndbg
cd /opt/pwndbg
./setup.sh

# ~/.gdbinit'e ekle:
source /opt/pwndbg/gdbinit.py
```

---

## Hızlı Test Scripti

```bash
python3 << 'EOF'
import sys
tools_ok = True
tools = ['gdb', 'radare2', 'ghidra', 'ropper']
try:
    import pwn, angr, z3
    print("✓ Python binary tools OK")
except ImportError as e:
    print(f"✗ Eksik: {e}")
    tools_ok = False

for tool in tools:
    import shutil
    if shutil.which(tool):
        print(f"✓ {tool} kurulu")
    else:
        print(f"✗ {tool} eksik")
        tools_ok = False

if tools_ok:
    print("\n✓ Tüm pwn araçları hazır!")
else:
    print("\nÇözüm: fetih download-tools pwn")
    sys.exit(1)
EOF
```

---

## Notlar

- **gdb + pwndbg** → local exploit debugging için gerekli
- **pwntools** → neredeyse tüm exploit'lerde kullanılır
- **radare2** → disassembly, reverse engineering
- **ghidra** → decompilation (opsiyonel fakat güçlü)
- **angr + z3** → constraint solving challenge'larında
- **Ruby gem'ler** (`seccomp-tools`, `one_gadget`) → build tools gerekli

Skill okuduğunda başında hangi araçlar gerekli gösterilecek!
