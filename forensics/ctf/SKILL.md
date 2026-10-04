---
name: ctf-master-solver
description: CTF challenge ana orkestratörü — kategori tespiti, modern saldırı patern tanıma, ilgili skill arama, cross-skill zincir koordinasyonu, hızlı referans erişim. Auto-solver ve hint-system routing.
tags: [ctf, orchestrator, master, solver, triage, category-detection, modern-attacks, auto-solve, hint]
triggers:
  - "CTF challenge"
  - "flag bul"
  - "capture the flag"
  - "challenge dosyası"
  - "flag{"
  - "yarışma görevi"
  - "writeup yaz"
  - "exploit yaz"
  - "auto solve"
  - "autosolve"
  - "/auto-solve"
  - "otomatik çöz"
  - "solve this ctf"
  - "ipucu ver"
  - "/hint"
  - "takıldım"
  - "hint"
  - "nudge"
  - "ctf techniques"
  - "advanced exploitation"
  - "SSTI"
  - "SSRF"
  - "CSP bypass"
  - "request smuggling"
  - "deserialization"
  - "side-channel"
  - "padding oracle"
  - "LLL lattice"
  - "heap feng shui"
  - "kernel exploit"
  - "AI CTF"
  - "adversarial ML"
  - "llm attacks"
adapted_for: fetih
---

# CTF Master Solver — Ana Orkestratör

FETIH'in CTF challenge'larını ele alırken ilk okuduğu dosya. Bir challenge geldiğinde bu akışı takip et, kategoriyi belirle, ilgili skill'i yükle ve gerekirse zincirleme yap.

**Toplam:** 55 SKILL.md · 5 cheatsheet · 107 imported reference dosyası · ljagiello/ctf-skills & awesome-claude-security entegrasyonu.

---

## İlk Yönlendirme: Hangi CTF?

Kullanıcı CTF/challenge/flag kelimelerini kullandığında, **önce yarışma adını kontrol et**:

```bash
# 0. Özel komutlar → özel skill'lere yönlendir
"/auto-solve", "auto solve", "autosolve" → skills/ctf/auto-solver/SKILL.md
"/hint", "ipucu ver", "takıldım" → skills/ctf/hint-system/SKILL.md

# 1. Türk CTF yarışmaları → özel skill'lere yönlendir
"Siber Vatan", "sibervatan", "SiberVatan{" → skills/red-teaming/siber-vatan-ctf/SKILL.md
"Siber Vatan" geçtiğinde doğrudan siber-vatan-ctf skill'ini yükle, genel CTF akışını atla.

# 2. Diğer spesifik yarışmalar → ilgili yere yönlendir
"HTB", "HackTheBox" → web/crypto/pwn kategorilerinden uygun olanı seç
"picoCTF" → beginner-friendly, genellikle web/forensics ağırlıklı
"DEF CON", "CSAW", "Real World CTF" → advanced, heavy exploit chain

# 3. Genel CTF → aşağıdaki triage akışına devam et
Yarışma adı geçmiyorsa normal akışı uygula.
```

---

## Triage Akışı

```bash
# 1. Dosya tipi tespiti
file ./challenge_dosyasi
xxd ./challenge_dosyasi | head -20    # magic bytes
strings -n 8 ./challenge_dosyasi | head -40

# 2. Arşiv mi?
file * | grep -i 'zip\|tar\|gzip\|7z\|rar\|apk'
# Arşivi aç → içindeki dosyalara triage uygula

# 3. Ağ servisi mi?
# "nc host port" verilmişse → pwn veya crypto kategorisi
nc -v host port  # bağlan, banner gör

# 4. Web URL mi?
curl -sIv URL                       # headers
curl -s URL | head                  # body
curl -s URL/robots.txt              # hidden endpoints

# 5. Disk image mi?
file challenge.img                  # DOS/MBR boot sector → disk-forensics

# 6. APK mi?
file challenge.apk                  # → android-apk-analysis

# 7. Flag formatı tahmin et
# Organizasyona göre: HTB{}, picoCTF{}, flag{}, CTF{}, IRIS{}, ACSC{}, 0CTF{}
```

---

## Kategori → Skill Eşleme Tablosu

### Crypto Skills (12)

| Challenge ipucu | Skill yolu |
|---|---|
| n, e, c verilmiş, e büyük → d küçük | `skills/ctf/crypto/rsa-wiener-attack` |
| n, e, c verilmiş, Wiener çalışmadı, d < N^0.292 | `skills/ctf/crypto/lattice-attacks` (Boneh-Durfee) |
| p, q yakın asal veya N = p·q·r | `skills/ctf/crypto/rsa-close-primes` |
| Padding oracle yanıtı / decrypt oracle var | `skills/ctf/crypto/rsa-padding-oracle` |
| Aynı n, iki farklı e | `skills/ctf/crypto/rsa-common-modulus` |
| Mesajın kısmı biliniyor / Hastad broadcast / partial p | `skills/ctf/crypto/lattice-attacks` |
| Elliptic curve, ECDSA, ECDH parametreleri | `skills/ctf/crypto/elliptic-curve-attacks` |
| AES-GCM nonce reuse | `skills/ctf/crypto/aes-gcm-nonce-reuse` |
| AES-CBC bit flipping / ECB cut-paste / IV manip | `skills/ctf/crypto/aes-cbc-bitflip` |
| Diffie-Hellman, DLP, g^x mod p | `skills/ctf/crypto/diffie-hellman-attacks` |
| JWT token, eyJ başlıyor | `skills/ctf/crypto/jwt-attacks` |
| base64/hex/encoded katmanlı veri | `skills/ctf/crypto/encoding-multilayer` |
| hash kır, MD5/SHA/bcrypt | `skills/ctf/crypto/hash-crack` |

### Pwn Skills (8)

| Challenge ipucu | Skill yolu |
|---|---|
| ELF binary, BOF, ROP gadget | `skills/ctf/pwn/buffer-overflow-rop` |
| Libc verilmiş, system shell hedef | `skills/ctf/pwn/ret2libc` |
| Format string, printf(buf) | `skills/ctf/pwn/format-string` |
| Heap challenge, malloc/free | `skills/ctf/pwn/heap-exploit` |
| nc host port — remote exploit | `skills/ctf/pwn/remote-pwn` |
| Az gadget, statik binary, SROP | `skills/ctf/pwn/srop-attack` |
| Kernel module (.ko), bzImage, QEMU | `skills/ctf/pwn/kernel-pwn-basics` |
| SECCOMP filter, execve yasak | `skills/ctf/pwn/seccomp-sandbox-escape` |

### Web Skills (8)

| Challenge ipucu | Skill yolu |
|---|---|
| Login formu, SQL injection ipuçları | `skills/ctf/web/sqli-exploitation` |
| JWT bypass, alg confusion, CVE-2022-39227 | `skills/ctf/web/jwt-web-bypass` |
| Server-Side Template Injection ({{7*7}}) | `skills/ctf/web/ssrf-ssti-chain` |
| GraphQL endpoint, introspection, batching | `skills/ctf/web/graphql-attacks` |
| pickle, Java/PHP deserialization | `skills/ctf/web/deserialization` |
| Frontend CDN + backend, HTTP smuggling | `skills/ctf/web/http-request-smuggling` |
| Limit overrun, coupon race, TOCTOU | `skills/ctf/web/race-conditions` |
| Node.js, __proto__, deep merge | `skills/ctf/web/prototype-pollution` |

### Forensics Skills (5)

| Challenge ipucu | Skill yolu |
|---|---|
| .dmp, .vmem, memory dump | `skills/ctf/forensics/volatility-memory-analysis` |
| .pcap, .pcapng | `skills/ctf/forensics/pcap-network-analysis` |
| PNG, JPG, görsel stego | `skills/ctf/forensics/steganography-image` |
| WAV, MP3, ses dosyası | `skills/ctf/forensics/steganography-audio` |
| .dd, .raw, .E01 disk image | `skills/ctf/forensics/disk-forensics` |

### Rev Skills (4)

| Challenge ipucu | Skill yolu |
|---|---|
| ELF binary, tersine mühendislik | `skills/ctf/rev/elf-static-analysis` |
| Anti-debug, UPX, obfuscation | `skills/ctf/rev/anti-debug-obfuscation` |
| Validator/constraint çözme | `skills/ctf/rev/z3-constraint-solving` |
| .apk Android app | `skills/ctf/rev/android-apk-analysis` |

### OSINT Skills (2)

| Challenge ipucu | Skill yolu |
|---|---|
| Kişi araştır, fictional persona | `skills/ctf/osint/persona-tracking` |
| OSINT teknikleri, araç zinciri | `skills/ctf/osint/osint-techniques` |

### Misc Skills (2)

| Challenge ipucu | Skill yolu |
|---|---|
| CTFd navigasyon, platform keşfi | `skills/ctf/misc/misc-techniques` |
| Yarışma stratejisi, CTF yardım | `skills/ctf/competition-assistant` |

### Yeni Imported Skills (ljagiello/ctf-skills)

Her kategoride derinlemesine referans dosyalarıyla birlikte:

| Skill | Referans Dosya | Kapsam |
|---|---|---|
| `skills/ctf/web/web-techniques/` | **20 ref** | SQLi, SSRF, SSTI, XXE, JWT, CSP bypass, client-side, server-side deser, OAuth/SAML, node-prototype |
| `skills/ctf/crypto/crypto-techniques/` | **16 ref** | RSA, ECC, AES, hash, LLL lattice, padding oracle, side-channel |
| `skills/ctf/pwn/pwn-techniques/` | **18 ref** | Heap feng shui, kernel exploit, format string, ROP chains, sandbox escape |
| `skills/ctf/rev/reverse-techniques/` | **18 ref** | Ghidra/IDA, unpacking, obfuscation, anti-debug, symbolic execution |
| `skills/ctf/forensics/forensics-techniques/` | **14 ref** | Disk recovery, memory dump, stego advanced, signals/hardware |
| `skills/ctf/misc/misc-techniques/` | **12 ref** | Encoding, pyjail, bash jail, DNS, RF/SDR, pythonjail |

> Bu skill'ler yüksek kaliteli CTF tekniği içerir. Kategori belli olduktan sonra ilgili `*-techniques/SKILL.md` dosyasını oku, `references/` altındaki ilgili `.md` dosyasına yönlendir.

---

## Hızlı Referans Cheatsheet'leri

Kategoriye girmeden hızlı karar / lookup için:

| Cheatsheet | Ne Zaman Kullan |
|---|---|
| `skills/ctf/cheatsheets/modern-protections-bypass.md` | Pwn challenge — NX/PIE/SMEP/CET/KASLR proteksiyon haritası |
| `skills/ctf/cheatsheets/crypto-attack-flowchart.md` | Crypto challenge — RSA/AES/Hash/ECC karar ağacı |
| `skills/ctf/cheatsheets/web-attack-decision-tree.md` | Web challenge — tech stack → saldırı eşleme |
| `skills/ctf/cheatsheets/pwntools-template.py` | Pwn challenge — exploit boilerplate (process/remote/gdb) |
| `skills/ctf/cheatsheets/payload-library.md` | Hızlı payload lookup (Jinja, SQLi, XSS, LFI, CMD inj, JWT) |

---

## Modern Attack Indicators (Eski Tablonun Görmedikleri)

Klasik saldırılar başarısız olduğunda **modern saldırı ipuçlarını** ara:

### Crypto Modern İpuçları
- **Coppersmith lattice:** Flag formatı kısmen biliniyor (`picoCTF{...}`), `e` küçük → `lattice-attacks`
- **Boneh-Durfee:** `e ~ N`, Wiener tutmadı ama d hala düşük → `lattice-attacks`
- **ECC:** Eğri parametreleri verilmiş, eğri `trace=1` veya order smooth → `elliptic-curve-attacks`
- **AES nonce reuse:** GCM mode + iki ciphertext aynı nonce ile → `aes-gcm-nonce-reuse`
- **CBC bit flip:** Cookie/token AES-CBC ama MAC yok → `aes-cbc-bitflip`

### Pwn Modern İpuçları
- **SROP:** `syscall;ret` var ama klasik ROP gadget yok → `srop-attack`
- **Kernel:** `bzImage`, `rootfs.cpio`, `.ko`, QEMU komutu → `kernel-pwn-basics`
- **SECCOMP:** `execve` çalışmıyor, `seccomp-tools dump` filtre gösteriyor → `seccomp-sandbox-escape`

### Web Modern İpuçları
- **HTTP Smuggling:** Cloudflare/Akamai + backend, auth bypass denemeleri tutmuyor → `http-request-smuggling`
- **Race Condition:** "Bir kez kullanılabilir" + limit aşma fırsatı → `race-conditions`
- **Prototype Pollution:** Node.js backend, `_.merge` veya JSON parse user input → `prototype-pollution`

### Rev / Forensics Modern İpuçları
- **APK:** `.apk` dosyası → `android-apk-analysis`
- **Disk imaj:** `.dd / .E01 / .raw` → `disk-forensics`

---

## Cross-Skill Zincirleri (Skill A başarısız → Skill B dene)

CTF challenge'lar çoğunlukla tek skill değil, **birkaç skill'in birleşimi**. Tipik zincirler:

### RSA Zinciri
```
factordb dene → başarısız
   ↓
rsa-close-primes (Fermat) → başarısız
   ↓
rsa-wiener-attack (küçük d) → başarısız
   ↓
lattice-attacks (Boneh-Durfee / Coppersmith) → genelde burada çözülür
```

### Web Auth Bypass Zinciri
```
sqli-exploitation → başarısız (input filtreli)
   ↓
jwt-web-bypass → token forge
   ↓
prototype-pollution → isAdmin: true
   ↓
race-conditions → admin oluşturma limitini aş
```

### Pwn Modern Korumalı Zinciri
```
buffer-overflow-rop → ASLR/PIE bypass için info leak gerek
   ↓
format-string → libc leak
   ↓
ret2libc → system shell
   ↓
seccomp-sandbox-escape (eğer execve yasak) → ORW shellcode
```

### Forensics Multi-Stage Zinciri
```
disk-forensics → memory dump çıkar
   ↓
volatility-memory-analysis → şifreli dosya bul
   ↓
encoding-multilayer / rsa-* → decrypt
   ↓
flag
```

### Android Multi-Tier
```
android-apk-analysis → native .so bul
   ↓
elf-static-analysis → algorithm reverse
   ↓
z3-constraint-solving → flag çıkar
```

---

## Hızlı Karar Ağacı

```
Dosya türü?
│
├── ELF binary
│   ├── nc host port var → Pwn
│   │   ├── BOF + libc → ret2libc
│   │   ├── BOF + statik → srop-attack
│   │   ├── format string → format-string
│   │   ├── heap → heap-exploit
│   │   └── SECCOMP filter → seccomp-sandbox-escape
│   └── sadece dosya, "flag gir" → Rev
│       ├── GDB çalışmıyor → anti-debug-obfuscation
│       ├── validator → z3-constraint-solving
│       └── UPX/strip → elf-static-analysis
│
├── APK → android-apk-analysis
│
├── Kernel files (bzImage, rootfs) → kernel-pwn-basics
│
├── Görsel (PNG/JPG/BMP/GIF)
│   ├── "flag içinde gizli" → steganography-image
│   ├── "kişi kim?" → persona-tracking
│   └── QR kod → zbarimg
│
├── Ses (WAV/MP3/FLAC) → steganography-audio
│
├── Disk imaj (.dd/.E01/.img) → disk-forensics
│
├── Network capture (.pcap/.pcapng) → pcap-network-analysis
│
├── Memory dump (.dmp/.vmem) → volatility-memory-analysis
│
├── Metin / sayılar
│   ├── n, e, c → RSA (crypto-attack-flowchart cheatsheet)
│   ├── ECC params → elliptic-curve-attacks
│   ├── g^x mod p → diffie-hellman-attacks
│   ├── eyJ... → jwt-attacks veya jwt-web-bypass
│   ├── base64/hex → encoding-multilayer
│   ├── hash → hash-crack
│   └── AES ct + key/IV → aes-cbc-bitflip / aes-gcm-nonce-reuse
│
├── Web URL
│   ├── Login formu → sqli-exploitation
│   ├── JWT → jwt-web-bypass
│   ├── Template render → ssrf-ssti-chain
│   ├── GraphQL → graphql-attacks
│   ├── Serialization → deserialization
│   ├── Node.js → prototype-pollution
│   ├── Frontend/backend → http-request-smuggling
│   └── Limit/coupon → race-conditions
│
├── Sosyal medya / persona → persona-tracking
│
└── Hiçbiri değil → strings + file + xxd ile tekrar triage
```

---

## Skill Okuma Komutu

Kategori belirlendikten sonra:

```
Read skills/ctf/[kategori]/[teknik]/SKILL.md
```

Okunan skill'deki `triggers` listesi ile kendi challenge'ını karşılaştır. Eşleşen trigger varsa → o skill'deki metodoloji ile devam et. Tam eşleşme yoksa birden fazla skill oku ve en yakını seç. Skill içinde "Cross-Skill Pivot" bölümü zincir önerisi içerir.

---

## Başarısız Olunca Pivot

```
Deneme 1 → İlk skill metodolojisi
Deneme 2 → Aynı kategoride farklı teknik (tablodaki alternatif)
Deneme 3 → Modern saldırı indicator'larını gözden geçir
Deneme 4 → Cross-skill zinciri dene
Deneme 5 → Genel CTF solver:
           Read skills/red-teaming/ctf-challenge-solver/SKILL.md
```

Pivot kararı ver:
- Aynı yerde 15 dakikadan fazla takılıysan → pivot
- Yeni bir ipucu gelirse → tablodan yeniden eşleştir
- "Bu çalışmıyor" yerine "Neden çalışmıyor?" diye düşün
- Yarışmada zaman kısaysa → daha kolay başka challenge'a geç, sonra dön

---

## Ortam Hazırlama

```bash
# CTF çalışma dizini oluştur
mkdir -p ~/ctf/$(date +%Y%m%d)_challengeName
cd ~/ctf/$(date +%Y%m%d)_challengeName

# Araçlar kurulu mu?
which ghidra pwntools z3 hashcat john exiftool sherlock sage 2>/dev/null
# Eksikleri kur:
pip install pwntools z3-solver gmpy2 sympy
# SageMath ayrı: sudo apt install sagemath veya conda

# Pwn için pwntools template
pwn template ./binary --host HOST --port PORT > solve.py

# GDB + pwndbg/peda
gdb -q ./binary
```

---

## Flag Doğrulama

```
Desteklenen flag formatları:
  flag{...}    FLAG{...}    CTF{...}    HTB{...}    picoCTF{...}
  IRIS{...}    0CTF{...}    ACSC{...}   ACTF{...}   dice{...}
  corctf{...}  LACTF{...}   uoftctf{...}  THM{...}  <yarışma>{...}

Flag bulununca:
1. Format doğru mu? (parantezler + içerik)
2. Anlamlı metin mi? (anlamsız hex → şüphelen)
3. Binary ile doğrula: echo "flag{...}" | ./binary → "Correct!" beklenir
4. Yarışma platformuna gönder

Sahte flag tuzakları:
- Binary içinde "flag{test}", "flag{XXXX}" → sahte
- "wrong flag" yanıtı → doğru formata bak
- Submit'i çok deneyip blocklanmamak için önce format kontrol
```

---

## Paralel Strateji

Birden fazla olası kategori varsa:

```bash
# Terminal 1: Rev
strings ./binary | grep -i flag

# Terminal 2: Forensics
binwalk ./binary
foremost ./binary -o /tmp/foremost_out/

# Terminal 3: Stego (görsel mi?)
steghide info ./binary 2>/dev/null
zsteg ./binary 2>/dev/null
```

---

## Yarışma Modu — Multi-Challenge Yönetim

Aynı anda 5+ challenge varsa:

```bash
# Klasör yapısı
ctf/
├── crypto/
│   ├── chall1/   # her birine ayrı dizin
│   └── chall2/
├── pwn/
├── web/
├── solved.md      # çözülmüş flagler
└── notes.md       # ipuçları, dead-end'ler

# Solved tracking
echo "[crypto/chall1] flag{xxx}" >> solved.md
```

---

## Sık Kullanılan Tek Satırlıklar

```bash
# Tüm printable stringleri çıkar
strings -n 8 ./file | sort -u

# Magic byte kontrolü
xxd ./file | head -3

# Arşiv içini listele
7z l ./archive.zip
tar -tzvf ./archive.tar.gz

# Base64 çöz
echo "SGVsbG8=" | base64 -d

# Hex çöz
echo "48656c6c6f" | xxd -r -p

# ROT13
echo "Uryyb" | tr 'A-Za-z' 'N-ZA-Mn-za-m'

# XOR ile bir byte
python3 -c "data=open('./file','rb').read(); print(bytes(b^0x42 for b in data))"

# Online hash decrypt
# https://crackstation.net/
# https://hashes.com/en/decrypt/hash

# CyberChef (çevrimiçi Swiss Army Knife)
# https://gchq.github.io/CyberChef/
```

---

## Notlar & Best Practices

- Flag bulunduğunda hemen platforma submit et
- CTF writeup'larına bak (benzer challenge daha önce çözülmüş mü?)
- `site:ctftime.org writeup "challenge_adi"` ile ara
- Zaman baskısında önce kolay görünen bölümleri çöz
- Ekip çalışmasında kim neye baktığını söyle (aynı şeyi tekrar araştırmayın)
- Her başarılı çözümden sonra: `notes.md`'ye ne öğrendiğini yaz — gelecekteki challenge'larda hatırlarsın
- Yarışma bitince writeup yaz — başkalarının öğrenmesi + senin pekiştirmen için

---

## Genel İpuçları

- **3 başarısız denemeden sonra pivot et** — aynı yöntemi varyasyon ile denemek genelde zaman kaybı
- **Modern saldırıları unutma** — özellikle 2023+ CTF'lerde lattice/HTTP-smuggling/prototype-pollution çok yaygın
- **Cheatsheet'ler hızlı erişim için** — kategori belli olmadan önce cheatsheet'ten karar al
- **Skill'ler derin teknik için** — kategori belli olunca skill'i oku, exploit kodunu uyarla
- **Cross-skill zincir mantığı** — özellikle real-world tarzı CTF'lerde 2-3 skill kombinasyonu gerekir

---

## Araç Kontrol ve Kurulumu

CTF/pentest araçlarını otomatik kurmak için:

```bash
fetih download-tools            # interaktif menü (kategori seç)
fetih download-tools all        # hepsini kur (nmap, sqlmap, nuclei, pwntools, ghidra...)
fetih download-tools basic      # temel araçlar (nmap, sqlmap, pwntools, gdb, binwalk)
fetih download-tools status     # hangi araçlar kurulu göster — Eksik araçları görmek için ilk adım!
```

Kategoriye göre kurulum:

```bash
fetih download-tools crypto      # Crypto araçları (pycryptodome, gmpy2, sympy, fpylll, padding-oracle)
fetih download-tools pwn         # Pwn/Binary araçları (gdb, pwntools, radare2, ghidra, angr, z3)
fetih download-tools web         # Web araçları (sqlmap, nuclei, ffuf, nikto, wpscan, dalfox)
fetih download-tools forensics   # Forensics araçları (binwalk, volatility3, sleuthkit, exiftool, steghide)
fetih download-tools rev         # Reverse engineering (gdb, radare2, ghidra, angr, z3)
fetih download-tools osint       # OSINT araçları (sherlock, maigret, subfinder, amass)
fetih download-tools network     # Network tarama (nmap, masscan, dnsenum, subfinder, amass)
```

### Araç Kurulumu Akışı

1. **Önce status kontrol et** → `fetih download-tools status`
2. **Eksik araçları gör** → hangi kategorilerde neler eksik
3. **Kategori seç** → `fetih download-tools <kategori>`
4. **Onay ver** → kurulum başlayacak

| Kategori | Önemli Araçlar |
|----------|---------|
| **crypto** | pycryptodome, gmpy2, sympy, fpylll, padding-oracle |
| **pwn** | gdb, pwntools, radare2, ropper, checksec, pwndbg, ghidra, angr, z3, seccomp-tools |
| **web** | sqlmap, nikto, nuclei, ffuf, gobuster, feroxbuster, dalfox, wpscan, katana, smuggler |
| **forensics** | binwalk, foremost, testdisk, sleuthkit, exiftool, volatility3, steghide, zsteg |
| **rev** | gdb, radare2, ghidra, angr, z3, pwntools, ropper |
| **osint** | sherlock, maigret, subfinder, amass, assetfinder, waybackurls, gau |
| **network** | nmap, masscan, arp-scan, dnsenum, rustscan, fierce, subfinder, amass |

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: 49e359470100edd6
-->

