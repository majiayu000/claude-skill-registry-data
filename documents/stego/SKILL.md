---
name: SKILL.md-
description: ">\n  Steganography reconnaissance and steganalysis. Detects hidden payloads\
  \ in image, audio, video, and document carriers via entropy analysis, LSB detection,\
  \ metadata anomalies, and statistical steganalysis. Maps to MITRE T1027.003 and\
  \ T1001.003."
---
# Steganography Recon

**Purpose:** Carrier-file triage and hidden-data detection for image, audio, video, and document formats. Also covers network steganography and covert channel detection.

---

## Core Focus Areas

- **Entropy analysis**: High-entropy regions indicating encrypted/compressed hidden payloads
- **LSB steganography**: Least Significant Bit hiding in PNG/BMP/WAV/raw pixel carriers
- **Metadata abuse**: EXIF/XMP/IPTC field hiding, GPS coordinates on internal documents
- **Audio steganography**: Phase coding, echo hiding, spread-spectrum, spectrogram image embedding
- **Video steganography**: Frame-level hiding, DCT coefficient manipulation, subtitle stream abuse
- **Document steganography**: White-on-white text, invisible layers, PDF stream hiding, DOCX XML abuse
- **Network steganography**: DNS tunneling, ICMP data field abuse, HTTP header covert channels, timing channels

---

## Key Techniques & Tools

### Entropy & Signature Analysis
```bash
# Measure file entropy (> 7.5 bits/byte = suspicious)
python3 - <<'EOF'
import sys, math, collections, os
for root, dirs, files in os.walk('.'):
    for fname in files:
        fpath = os.path.join(root, fname)
        try:
            data = open(fpath,'rb').read(65536)
            if not data: continue
            cnt = collections.Counter(data)
            h = -sum((v/len(data))*math.log2(v/len(data)) for v in cnt.values() if v)
            if h > 7.0:
                print(f"{h:.3f}  {fpath}")
        except: pass
EOF

# binwalk — embedded file signatures + entropy graph
binwalk -e -E "$file" 2>/dev/null
binwalk --dd='.*' "$file" 2>/dev/null

# foremost — file carving from carrier
foremost -i "$file" -o /tmp/carved/ 2>/dev/null
```

### Image Steganalysis
```bash
# steghide — detect embedded data (JPEG, BMP, WAV, AU)
steghide info "$file" 2>&1

# stegseek — fast passphrase brute-force on steghide-protected files
stegseek "$file" /usr/share/wordlists/rockyou.txt 2>/dev/null

# zsteg — PNG/BMP LSB + multi-bit analysis
zsteg -a "$file" 2>/dev/null | head -30

# stegoveritas — comprehensive multi-method steganalysis
stegoveritas "$file" 2>/dev/null

# ExifTool — full metadata dump (GPS, Software, Comments, UserData)
exiftool "$file" 2>/dev/null | grep -v "^ExifTool Version"

# identify (ImageMagick) — compression/geometry anomalies
identify -verbose "$file" 2>/dev/null | grep -E "(Compression|Interlace|error|Comment)"

# Manual LSB extraction (PNG, first 100 rows)
python3 -c "
from PIL import Image
img = Image.open('$file').convert('RGB')
pixels = list(img.getdata())[:800]
bits = ''.join(str(p[0] & 1) for p in pixels)
chars = [chr(int(bits[i:i+8],2)) for i in range(0,len(bits)-8,8)]
result = ''.join(c if 32<=ord(c)<127 else '.' for c in chars)
print('LSB RGB-R:', result[:80])
" 2>/dev/null

# OutGuess / F5 / JSteg detection pattern
strings "$file" | grep -iE "(outguess|jsteg|f5|steghide|openstego)" | head -5
```

### Audio Steganography
```bash
# Spectrogram — reveals images hidden in frequency domain (SoX)
sox "$file" -n spectrogram -o /tmp/spectrogram_$(basename "$file").png 2>/dev/null
echo "Spectrogram saved: /tmp/spectrogram_$(basename $file).png"

# WAV LSB extraction
python3 -c "
import wave, struct
with wave.open('$file') as wf:
    frames = wf.readframes(2000)
data = struct.unpack(f'{len(frames)}B', frames)
bits = ''.join(str(b & 1) for b in data[:1600])
chars = [chr(int(bits[i:i+8],2)) for i in range(0,len(bits)-8,8)]
print('WAV LSB:', ''.join(c if 32<=ord(c)<127 else '.' for c in chars[:80]))
" 2>/dev/null

# MP3 ID3 tag analysis for hidden payloads
python3 -c "
from mutagen.id3 import ID3
tags = ID3('$file')
for k,v in tags.items():
    if len(str(v)) > 50: print(f'{k}: {str(v)[:200]}')
" 2>/dev/null
```

### Document Steganography
```bash
# PDF — count and inspect streams
python3 -c "
import re, zlib
data = open('$file','rb').read()
streams = re.findall(b'stream\r?\n(.*?)\r?\nendstream', data, re.DOTALL)
print(f'{len(streams)} PDF streams found')
for i, s in enumerate(streams[:5]):
    try:
        dec = zlib.decompress(s)
        print(f'  Stream {i}: {dec[:120]}')
    except: print(f'  Stream {i}: raw len={len(s)}')
" 2>/dev/null

# DOCX/XLSX/PPTX — extract XML and check for hidden text
unzip -l "$file" 2>/dev/null | grep "\.xml"
unzip -p "$file" word/document.xml 2>/dev/null | \
  python3 -c "import sys; from xml.dom.minidom import parseString; \
    print(parseString(sys.stdin.read()).toprettyxml())" 2>/dev/null | \
  grep -iE '(FFFFFF|color.*fff|font-size.*0|hidden)' | head -10

# exiftool on document metadata
exiftool "$file" 2>/dev/null | grep -iE "(author|creator|last.modified|company|comment|subject)"
```

### Network Steganography Detection
```bash
# DNS covert channel — long/high-entropy subdomains
tshark -r capture.pcap -Y "dns.qry.type == 1" \
  -T fields -e dns.qry.name 2>/dev/null | \
  awk 'length($1) > 40 || $1 ~ /[0-9a-f]{32}/' | sort | uniq -c | sort -rn | head -20

# ICMP data field abuse
tcpdump -r capture.pcap -X 'icmp[icmptype] == icmp-echo' 2>/dev/null | \
  grep -A2 "0x0020" | head -40

# HTTP header covert channels (unusual X- headers or ordering)
tshark -r capture.pcap -Y "http.request" -T fields \
  -e http.host -e http.user_agent -e http.x_forwarded_for 2>/dev/null | \
  awk 'NF' | head -30

# Timing-based covert channel (inter-packet delta analysis)
tshark -r capture.pcap -T fields -e frame.time_relative \
  -e ip.src -e ip.dst 2>/dev/null | \
  python3 -c "
import sys
deltas=[]
prev=0.0
for line in sys.stdin:
    parts=line.split()
    if not parts: continue
    try: t=float(parts[0]); deltas.append(t-prev); prev=t
    except: pass
if deltas:
    avg=sum(deltas)/len(deltas)
    outliers=[d for d in deltas if abs(d-avg) > 3*avg]
    print(f'Timing outliers: {len(outliers)}/{len(deltas)} ({100*len(outliers)//len(deltas)}%)')
" 2>/dev/null
```

---

## MITRE ATT&CK Mapping

| Finding | Technique |
|---------|-----------|
| Hidden payload in image/audio/video | T1027.003 – Steganography |
| C2 channel via steganographic images | T1001.003 – Protocol Impersonation |
| Data exfiltration via steganography | T1048 – Exfiltration Over Alternative Protocol |
| Binary padding / null byte injection | T1027.001 – Binary Padding |
| DNS tunneling covert channel | T1071.004 – DNS |
| ICMP covert channel | T1095 – Non-Application Layer Protocol |

---

## Rules for Agents

1. Always run entropy analysis first — flag files > 7.5 bits/byte for deeper triage
2. Check EXIF metadata for GPS coordinates on files from internal systems
3. Run binwalk on all suspicious images, audio, and documents
4. Log carrier file SHA-256 and confirmed/suspected steg method to `iocs.md`
5. For extracted payloads, treat as new evidence — hand to @reverse-engineer or @memory-analyst
6. On network captures, check DNS query lengths and ICMP payload sizes
7. Sync all steg-related IOCs to shared memory at session end
