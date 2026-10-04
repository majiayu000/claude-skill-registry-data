---
name: auto-solver
description: >
  CTF challenge otomatik cozum pipeline'i. 6 asama: zip'i ac, siniflandir, coz, flag topla, writeup olustur. /auto-solve komutuyla cagrilir.
tags: [ctf, auto-solver, pipeline, automation, flag-hunting, triage]
triggers:
  - "auto solve"
  - "/auto-solve"
  - "otomatik çöz"
  - "challenge'ı çöz"
  - "solve this ctf"
  - "autosolve"
  - "flag bul"
  - "capture the flag çözüm"
  - "solve challenge"
category: ctf
adapted_for: fetih
---

# CTF Auto-Solver — Otomatik Çözüm Pipeline

CTF challenge zip dosyası veya URL'si verildiğinde 6 aşamalı otomatik çözüm pipeline'ını çalıştırır. `/auto-solve` slash komutuyla veya manuel olarak çağrılır.

## Pipeline Aşamaları

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ STAGE 1  │───▶│ STAGE 2  │───▶│ STAGE 3  │───▶│ STAGE 4  │───▶│ STAGE 5  │───▶│ STAGE 6  │
│ Extract  │    │ Classify │    │  Route   │    │  Solve   │    │ Validate │    │  Report  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

---

## Stage 1: Extract (Dosyaları Çıkar)

Challenge zip/tar/rar/7z ise içeriğini çıkar:

```bash
# Zip dosyası
unzip -o challenge.zip -d ./challenge_extracted/

# Tar arşivi
tar xf challenge.tar -C ./challenge_extracted/

# RAR (unrar yüklüyse)
unrar x challenge.rar ./challenge_extracted/

# 7z (p7zip yüklüyse)
7z x challenge.7z -o./challenge_extracted/

# Bilinmeyen format - binwalk ile dene
binwalk -e challenge_file
```

**Önemli:** Çıkarma işleminden sonra challenge dizinine git:
```bash
cd ./challenge_extracted/
ls -laR | head -50
```

---

## Stage 2: Classify (Kategori Tespiti)

Dosya tiplerine ve içeriğe göre challenge kategorisini belirle:

```bash
# Tüm dosyaların tipini kontrol et
find . -type f -exec file {} \;

# Magic bytes kontrolü
xxd ./challenge_file | head -5

# String'leri tara
strings ./challenge_file | head -50

# İlk 500 byte'ı hex dump yap
xxd ./challenge_file | head -30
```

**Sınıflandırma Kuralları:**

| Bulgu | Kategori | Sonraki Adım |
|-------|----------|-------------|
| URL, HTTP, HTML, JS, form | **web** | Web analyzer çalıştır |
| ELF, PE, EXE, binary | **reverse** | Binary analyzer çalıştır |
| .pcap, .pcapng | **forensics** | Wireshark/tshark ile analiz |
| Şifreli metin, RSA params | **crypto** | Crypto solver çalıştır |
| .png, .jpg, .wav, .mp3 | **stego** | Stego analyzer çalıştır |
| netcat, nc host port | **pwn** | Pwn session başlat |
| .apk, AndroidManifest | **mobile** | APK analyzer çalıştır |
| Hash (32-128 char hex) | **hash** | Hash cracker çalıştır |
| eyJ... (JWT token) | **jwt** | JWT analyzer çalıştır |
| Kişi ismi, lokasyon | **osint** | OSINT araştırması |
| Zip içinde zip | **nested** | Recursive extract + classify |

---

## Stage 3: Route (Skill Seçimi)

Kategoriye göre uygun skill'i yükle:

```bash
# Web challenge → web security skill'leri
skill_view("ctf-challenge-solver")
skill_view("web-category-tools")

# Crypto challenge → crypto skill'leri
skill_view("crypto-category-tools")

# Reverse → reverse engineering skill'leri
skill_view("rev-category-tools")

# Forensics → forensics skill'leri
skill_view("forensics-category-tools")

# CTF tool'ları (TypeScript)
# tools/ctf/ctf-classify.ts
# tools/ctf/ctf-solver.ts
# tools/ctf/ctf-web-analyzer.ts
# tools/ctf/ctf-binary-analyzer.ts
# tools/ctf/ctf-forensics.ts
# tools/ctf/ctf-stego.ts
```

---

## Stage 4: Solve (Challenge'ı Çöz)

### Web Challenge Çözüm Zinciri
1. `curl -sIv URL` → response headers
2. `curl -s URL | grep -i 'flag\|comment\|hidden\|password'` → source inspection
3. `curl -s URL/robots.txt` → hidden endpoints
4. `gobuster dir -u URL -w wordlist.txt` → directory brute force
5. SQLi/XSS/SSTI testleri
6. Login bypass denemeleri

### Crypto Challenge Çözüm Zinciri
1. Encoding tespiti: base64 → base32 → hex → ROT13
2. Recursive decode (maks 7 katman)
3. RSA: factordb.com sorgusu, Wiener attack, close primes
4. AES: known-plaintext, padding oracle
5. Hash: rockyou wordlist, rainbow tables

### Reverse Engineering Çözüm Zinciri
1. `strings binary | grep -i 'flag\|key\|pass'`
2. `objdump -d binary | head -100`
3. Ghidra headless analiz
4. angr sembolik execution
5. GDB debug + patch

### Forensics Çözüm Zinciri
1. `file *` → dosya tipi doğrulama
2. `strings * | grep -i 'flag{'` → flag pattern tarama
3. `binwalk -e file` → gömülü dosyaları çıkar
4. `foremost file` → file carving
5. PCAP: `tshark -r capture.pcap -Y http` → HTTP filtreleme

### Stego Çözüm Zinciri
1. `exiftool file` → metadata
2. `zsteg -a image.png` → LSB tarama
3. `steghide extract -sf image.jpg` → şifreli çıkarma
4. `binwalk -e image.png` → gömülü dosya
5. Ses: spektrogram analizi (sox/audacity)

---

## Stage 5: Validate (Flag Doğrulaması)

Bulunan flag'i doğrula:

```bash
# Flag formatı kontrolü
echo "bulunan_flag" | grep -P '[A-Za-z0-9_]+\{[^}]+\}'

# Yaygın flag formatları
grep -P '(flag|CTF|HTB|picoCTF|SiberVatan|SIBERVATAN|sibervatan)\{[^}]+\}' <<< "bulunan_flag"

# Flag'i flags.txt'ye kaydet
echo "bulunan_flag" >> ./flags.txt
cat ./flags.txt
```

**Flag Formatları (40+):** `references/flag-formats.md` dosyasına bak.

---

## Stage 6: Report (Writeup Oluştur)

Çözüm writeup'ını oluştur:

```bash
cat > writeup_$(date +%Y%m%d_%H%M%S).md << 'WRITEUP'
# [Challenge Name] — Writeup

**Category:** [web/crypto/reverse/forensics/stego/pwn/osint]
**Difficulty:** [easy/medium/hard]
**Flag:** `flag{...}`

## Solution

[Step-by-step solution]

## Tools Used
- [Tool 1]
- [Tool 2]
WRITEUP

echo "Writeup: writeup_*.md"
```

---

## Pivot Stratejisi

3 başarısız flag denemesinde **HARD PIVOT** uygula:

1. **Tool değiştir:** curl → browser → Burp Suite → custom script
2. **Vulnerability class değiştir:** SQLi → XSS → LFI → RCE → SSTI → SSRF
3. **Attack vector değiştir:** header manipulation → cookie tampering → parameter injection
4. **Analysis angle değiştir:** static → dynamic → side-channel
5. **Dış kaynaklara başvur:** writeup ara, benzer challenge bul

**Pivot log'u:**
```bash
echo "[$(date)] PIVOT: [sebep] — yeni yaklaşım: [yaklaşım]" >> pivot_log.txt
```

---

## Slash Komutu

```
/auto-solve <challenge.zip>              → Tüm pipeline'ı çalıştır
/auto-solve <url> --category web         → Sadece web challenge çöz
/auto-solve --category crypto <ciphertext>  → Crypto challenge çöz
/auto-solve --resume                     → Kaldığı yerden devam et
```

---

## Önemli Kurallar

1. **Asla flag'i düz metin olarak log'lama** — sadece flags.txt'ye yaz
2. **Her stage'de ilerlemeyi log'la** — `stage_log.txt`
3. **Timeout'ları yönet** — her stage için max 5 dakika
4. **Kaynakları temizle** — geçici dosyaları sil, disk doldurma
5. **Siber Vatan için özel format:** `SiberVatan{...}`, `SIBERVATAN{...}`, `sibervatan{...}`

## Referanslar

- `references/pipeline-stages.md` — Her stage için detaylı rehber
- `references/flag-formats.md` — 40+ CTF flag formatı kataloğu
- Siber Vatan CTF Playbook — `skills/red-teaming/siber-vatan-ctf/SKILL.md`
- CTF Master Solver — `skills/ctf/SKILL.md`

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: a6d0d476f57c300f
-->

