---
category: ctf
name: forensics-category-tools
description: Forensics kategorisi SKILL.md — Memory, disk, PCAP, steganography araçları kurma rehberi
tags: [ctf, forensics, tools, setup, volatility3, binwalk, exiftool]
adapted_for: fetih
---

# Forensics Kategorisi — Gerekli Araçlar

Bellek forensics, disk recovery, PCAP analizi, steganography ve metadata analizi araçları.

## Gerekli Araçlar

| Araç | Açıklama | Kurulum |
|------|----------|---------|
| **binwalk** | Firmware analiz + file carving | `pip install binwalk` |
| **foremost** | File carving — gizli dosya çıkarma | `sudo apt-get install foremost` |
| **testdisk** | Disk recovery + PhotoRec | `sudo apt-get install testdisk` |
| **sleuthkit** | Disk forensics (TSK) — fls, istat vb. | `sudo apt-get install sleuthkit` |
| **autopsy** | GUI disk forensics (TSK wrapper) | `sudo apt-get install autopsy` |
| **exiftool** | Metadata (EXIF) extraction | `sudo apt-get install libimage-exiftool-perl` |
| **ewf-tools** | EnCase .E01 imaj desteği | `sudo apt-get install ewf-tools` |
| **ntfs-3g** | NTFS filesystem mount | `sudo apt-get install ntfs-3g` |
| **volatility3** | Memory forensics framework | `pip install volatility3` |
| **pypykatz** | LSASS dump analizi + NTLM crack | `pip install pypykatz` |
| **analyzeMFT** | NTFS MFT parsing | `pip install analyzeMFT` |
| **pytsk3** | Python TSK binding | `pip install pytsk3` |
| **bless** | Hex editor (GUI) | `sudo apt-get install bless` |
| **wxhexeditor** | Hex editor (GUI, büyük) | `sudo apt-get install wxhexeditor` |
| **steghide** | Steganography hide/extract | `sudo apt-get install steghide` |
| **zsteg** | PNG/BMP steganography | `gem install zsteg` |
| **stegoveritas** | Multi-format steganography | `pip install stegoveritas` |
| **stegseek** | Steghide brute-force (fast) | deb kurulum |
| **stego-lsb** | LSB steganography | `pip install stego-lsb` |
| **ffmpeg** | Audio/video dönüşüm | `sudo apt-get install ffmpeg` |
| **sox** | Ses işleme | `sudo apt-get install sox` |
| **audacity** | Ses editörü (GUI) | `sudo apt-get install audacity` |
| **sonic-visualiser** | Spektogram analizi (GUI) | `sudo apt-get install sonic-visualiser` |

## Araçları Hızlı Kur

Forensics kategorisine ait tüm araçları kur:

```bash
fetih download-tools forensics
```

Bu kurulum:
- apt araçları → sistem paketi
- pip araçları → Python venv
- gem araçları → Ruby kütüphanesi
- deb file → direktli dpkg kurulum

## Araçlar Kurulu mu Kontrol Et

```bash
# Tüm forensics araçları
fetih download-tools status | grep -A 30 "FORENSICS"

# Manuel kontrol
which binwalk volatility3 exiftool sleuthkit
python3 -c "import volatility3, exiftool; print('Forensics OK')"
```

## Her Araç Neye Yarar?

### Memory Forensics

#### volatility3
Memory dump analizi — process'ler, network bağlantıları, kernel module'ler

**Skill'lerde kullanılır:**
- `forensics/volatility-memory-analysis` → process tree, registry, handles

```bash
vol -f memory.dmp windows.pslist
vol -f memory.dmp linux.psaux
vol -f memory.dmp windows.registry.query
```

#### pypykatz
Windows LSASS dump → NTLM hash, Kerberos ticket çıkarma

**Skill'lerde kullanılır:**
- `forensics/volatility-memory-analysis` → credential dump

```bash
pypykatz lsa minidump lsass.dmp
```

### Disk Forensics

#### sleuthkit (fls, istat, blkstat)
Filesystem level analiiz — deleted file recovery, timeline

**Skill'lerde kullanılır:**
- `forensics/disk-forensics` → file listing, inode analizi

```bash
fls -r image.dd                  # recursive file listing
istat image.dd 12345             # inode details
blkstat image.dd 12345           # block details
```

#### testdisk + PhotoRec
Partition recovery + file carving

**Skill'lerde kullanılır:**
- `forensics/disk-forensics` → deleted file recovery

```bash
testdisk image.dd                # interactive mode
photorec image.dd                # GUI, file carving
```

#### foremost
Signature-based file carving

**Skill'lerde kullanılır:**
- `forensics/disk-forensics` → hidden file extraction

```bash
foremost -i image.dd -o output_dir
foremost -i image.dd -d /dev/sda1 -o output_dir
```

#### analyzeMFT
NTFS Master File Table parsing

**Skill'lerde kullanılır:**
- `forensics/disk-forensics` → NTFS timeline

```bash
analyzeMFT.py -f MFT -c timeline.csv
```

### Steganography

#### steghide
PNG/JPEG/AU steganography hide/extract

**Skill'lerde kullanılır:**
- `forensics/steganography-image` → hidden data extraction
- `forensics/steganography-audio` → WAV stego

```bash
steghide extract -sf image.png -p password
steghide embed -cf image.png -ef secret.txt -p password
```

#### zsteg
PNG/BMP steganography (LSB, Adam7 interlacing vb.)

**Skill'lerde kullanılır:**
- `forensics/steganography-image` → LSB extraction

```bash
zsteg image.png
zsteg image.png -a  # aggressive mode
```

#### stegoveritas
Tüm stegano tekniklerini bir araçta

**Skill'lerde kullanılır:**
- `forensics/steganography-image` → multi-method scan

```bash
stegoveritas image.png
stegoveritas -analyze image.png
```

#### stegoseek
Steghide brute-force (fast)

**Skill'lerde kullanılır:**
- `forensics/steganography-image` → dictionary attack

```bash
stegoseek image.png wordlist.txt output/
```

### Network Analysis (PCAP)

#### tshark
Command-line PCAP parser

**Skill'lerde kullanılır:**
- `forensics/pcap-network-analysis` → packet extraction

```bash
tshark -r capture.pcap -Y "http.request"
tshark -r capture.pcap -e ip.src -e ip.dst -e http.request.uri
```

### Binary/Firmware Analysis

#### binwalk
Firmware extraction + embedded file carving

**Skill'lerde kullanılır:**
- `forensics/steganography-image` → embedded file detection
- `forensics/disk-forensics` → firmware structure

```bash
binwalk -e firmware.bin
binwalk -e -M firmware.bin  # recursive extract
binwalk -A firmware.bin     # entropy analizi
```

### Metadata

#### exiftool
Image/document metadata extraction

**Skill'lerde kullanılır:**
- `forensics/steganography-image` → EXIF data
- `forensics/pcap-network-analysis` → file metadata

```bash
exiftool image.jpg
exiftool -a image.jpg  # all metadata
exiftool -GPSLatitude image.jpg
```

### Audio Processing

#### sox
Audio format dönüşüm + processing

**Skill'lerde kullanılır:**
- `forensics/steganography-audio` → WAV → raw conversion

```bash
sox input.wav -t raw -r 44100 -b 16 output.raw
sox input.mp3 output.wav
```

#### audacity
GUI audio editor — waveform görüntüle, spektogram

**Skill'lerde kullanılır:**
- `forensics/steganography-audio` → visual analysis

```bash
audacity audio.wav &
```

#### sonic-visualiser
Spektogram (frequency analysis) → SSTV, morse, hidden frequencies

**Skill'lerde kullanılır:**
- `forensics/steganography-audio` → frequency domain

```bash
sonic-visualiser audio.wav
```

### Hex Editing

#### bless / wxhexeditor
Hex editor GUI — binary file incelemesi

**Skill'lerde kullanılır:**
- Manual binary inspection → checksums, headers

```bash
bless image.bin
wxHexEditor image.bin
```

---

## Kurulum Sorunları Çözme

### volatility3 pluginleri bulunamıyor

Windows symbol'ları yükle:

```bash
pip install volatility3
# ~/.volatility3/ dizinine symbol'lar indir
volatility3 -f memory.dmp windows.registry.printkey
```

### foremost başarısız

Config file gerekli:

```bash
foremost -T
# /etc/foremost.conf kontrol et
sudo apt-get install --reinstall foremost
```

### sleuthkit bağımlılıkları

TSK library kurulum:

```bash
sudo apt-get install -y libtsk-dev
pip install pytsk3
```

### stegoseek .deb kurulum

GitHub release'ten indir:

```bash
wget https://github.com/RickdeJager/stegoseek/releases/download/v0.6/stegoseek_0.6-1.deb
sudo apt-get install -y ./stegoseek_0.6-1.deb
```

---

## Hızlı Test Scripti

```bash
python3 << 'EOF'
import shutil

forensics_tools = [
    'binwalk', 'foremost', 'testdisk', 'fls', 'exiftool',
    'steghide', 'sox', 'ffmpeg'
]

print("=== Forensics Tools Check ===")
missing = []
for tool in forensics_tools:
    if shutil.which(tool):
        print(f"✓ {tool}")
    else:
        print(f"✗ {tool}")
        missing.append(tool)

try:
    import volatility3, exiftool
    print("✓ volatility3, exiftool (Python)")
except ImportError as e:
    print(f"✗ {e}")

if missing:
    print(f"\nEksik: {', '.join(missing)}")
    print("Çözüm: fetih download-tools forensics")
else:
    print("\n✓ Tüm forensics araçları kurulu!")
EOF
```

---

## Notlar

- **volatility3** → memory analysis zorunlu
- **binwalk + foremost** → file carving temel
- **steghide + zsteg + stegoveritas** → stegano üçlüsü
- **exiftool** → metadata extraction her zaman gerekli
- **GUI araçları** (`audacity`, `sonic-visualiser`) → manual analysis
- **Audio tools** (`sox`, `ffmpeg`) → format dönüşüm

Skill okudoğunda başında hangi araçlar gerekli gösterilecek!

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: 741f2cc3b4b866f1
-->

