---
category: ctf
name: web-category-tools
description: Web kategorisi SKILL.md — SQLi, XSS, SSRF tarayıcı ve exploit araçları kurma rehberi
tags: [ctf, web, tools, setup, sqlmap, ffuf, nuclei, nikto]
adapted_for: fetih
---

# Web Kategorisi — Gerekli Araçlar

SQL injection, XSS, SSRF, JWT bypass ve diğer web vulnerabiliteleri için araçlar.

## Gerekli Araçlar

| Araç | Açıklama | Kurulum |
|------|----------|---------|
| **sqlmap** | SQL injection tarayıcı ve exploit | `pip install sqlmap` |
| **nikto** | Web sunucu zafiyet tarayıcı | `sudo apt-get install nikto` |
| **nuclei** | Template tabanlı zafiyet tarayıcı | Go kurulum (go install) |
| **ffuf** | Web fuzzer — directory brute-force | Go kurulum |
| **gobuster** | Dizin/dosya discovery | `sudo apt-get install gobuster` |
| **feroxbuster** | Recursive web fuzzer (ffuf alternatifi) | Rust kurulum (cargo) |
| **dalfox** | XSS tarayıcı | Go kurulum |
| **arjun** | HTTP parameter discovery | `pip install arjun` |
| **wafw00f** | WAF (Web App Firewall) tespit | `pip install wafw00f` |
| **wpscan** | WordPress tarayıcı | `gem install wpscan` |
| **katana** | Web crawler (spidering) | Go kurulum |
| **hakrawler** | Hızlı web crawler | Go kurulum |
| **smuggler.py** | HTTP request smuggling tester | Git kurulum |
| **httpx** | HTTP/2 client + race condition testi | `pip install httpx[http2]` |
| **aiohttp** | Async HTTP library (race condition) | `pip install aiohttp` |
| **racepwn** | Race condition exploit aracı | Git kurulum |

## Araçları Hızlı Kur

Web kategorisine ait tüm araçları kur:

```bash
fetih download-tools web
```

Bu kurulum:
- apt araçları (`nikto`, `gobuster`) — sistem seviyesi
- pip araçları (`sqlmap`, `arjun`, `wafw00f`) — Python venv
- Go araçları (`nuclei`, `ffuf`, `dalfox`) — `go install`
- Ruby gem (`wpscan`) — gem kurulum
- Git araçları (`smuggler`, `racepwn`) — GitHub clone

## Araçlar Kurulu mu Kontrol Et

```bash
# Tüm web araçları kontrol
fetih download-tools status | grep -A 20 "WEB"

# Manuel kontrol
which sqlmap nikto ffuf nuclei gobuster dalfox
python3 -c "import sqlmap; print('sqlmap OK')"
```

## Her Araç Neye Yarar?

### sqlmap
SQL injection otomatik tespit ve exploit

**Skill'lerde kullanılır:**
- `web/sqli-exploitation` → SQLi payload üretim

```bash
sqlmap -u "http://target/page?id=1" --dbs
sqlmap -u "http://target/" --data="user=admin&pass=1'" -p user
sqlmap -u "http://target/api/search" --api
```

### nikto
Web sunucu taraması — default file'lar, outdated version'lar

**Skill'lerde kullanılır:**
- `web/sqli-exploitation` → backup file'lar (*.bak, *.sql vb.)
- `web/ssrf-ssti-chain` → exposed endpoint'ler

```bash
nikto -h http://target/
nikto -h http://target/ -port 8080
```

### nuclei
Template tabanlı vulnerability scanner

**Skill'lerde kullanılır:**
- Tüm web skill'lerinde → özel template test'leri

```bash
nuclei -u http://target/ -t http/
nuclei -list urls.txt -severity high
```

### ffuf
Web fuzzer — directory/parameter brute-force

**Skill'lerde kullanılır:**
- `web/ssrf-ssti-chain` → endpoint discovery
- `web/deserialization` → hidden endpoint'ler

```bash
ffuf -u http://target/FUZZ -w wordlist.txt
ffuf -u http://target/api/FUZZ -w words.txt -fc 404
ffuf -u http://target/page?param=FUZZ -w values.txt
```

### gobuster
Directory taraması (ffuf'a benzer, fakat daha basit)

**Skill'lerde kullanılır:**
- Web keşif fazında quick directory scan

```bash
gobuster dir -u http://target/ -w /usr/share/wordlists/dirbuster/directory-list.txt
gobuster dns -d target.com -w wordlist.txt
```

### feroxbuster
Recursive web fuzzer — subdirectory'leri otomatik takip eder

**Skill'lerde kullanılır:**
- `web/ssrf-ssti-chain` → deep endpoint enumeration

```bash
feroxbuster -u http://target/ -w wordlist.txt
feroxbuster -u http://target/ --recursion-limit 2
```

### dalfox
XSS vulnerability scanner ve tester

**Skill'lerde kullanılır:**
- Web challenge'larında XSS testi (implicit)
- HTML injection'ları otomatik test et

```bash
dalfox url http://target/?id=1
dalfox pipe --stdin
```

### arjun
HTTP parameter discovery — hidden parameter'lar bul

**Skill'lerde kullanılır:**
- `web/ssrf-ssti-chain` → hidden parameter keşfi
- `web/race-conditions` → race condition trigger parameter'ları

```bash
arjun -u http://target/page -m GET
arjun -u http://target/api/search --get-json
```

### wafw00f
WAF (Web App Firewall) tespit ve bypass

**Skill'lerde kullanılır:**
- Web keşif → target'ın koruması ne?

```bash
wafw00f http://target/
wafw00f -i ips.txt
```

### wpscan
WordPress plugin/theme zafiyet taraması

**Skill'lerde kullanılır:**
- Spesifik target WordPress ise

```bash
wpscan --url http://target/ --enumerate p,t,u
wpscan --url http://target/ -P pluginwords.txt
```

### katana / hakrawler
Web crawler — tüm endpoint'leri bulur

**Skill'lerde kullanılır:**
- `web/deserialization` → hidden endpoint'ler
- `web/ssrf-ssti-chain` → domain/path enumeration

```bash
katana -u http://target/ -o endpoints.txt
hakrawler -url http://target/ | unfurl keys
```

### smuggler.py
HTTP request smuggling tester — frontend/backend desync

**Skill'lerde kullanılır:**
- `web/http-request-smuggling` → request split detection

```bash
python3 smuggler.py -u http://target/
```

### httpx
HTTP/2 client + race condition tester

**Skill'lerde kullanılır:**
- `web/race-conditions` → parallel request gönderme

```bash
echo "http://target/" | httpx -race -c 100
```

### aiohttp
Async HTTP library — race condition exploit için kütüphane

**Skill'lerde kullanılır:**
- `web/race-conditions` → custom async exploit

```python
import aiohttp
async with aiohttp.ClientSession() as session:
    async with session.get('http://target/') as resp:
        ...
```

### racepwn
Race condition exploit automation tool

**Skill'lerde kullanılır:**
- `web/race-conditions` → condition trigger'ı

```bash
racepwn -u http://target/pay -r 100
```

---

## Kurulum Sorunları Çözme

### sqlmap permission denied

Kurulun dizini kontrol et:

```bash
pip install --user sqlmap
# veya
pip install --break-system-packages sqlmap
```

### Go tools download timeout

Go PATH kontrol et:

```bash
export PATH=$PATH:$(go env GOPATH)/bin
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

### wpscan kurulum başarısız

Ruby build tools gerekli:

```bash
sudo apt-get install -y ruby-dev build-essential
gem install wpscan --user-install
```

---

## Hızlı Test Scripti

```bash
python3 << 'EOF'
import shutil

tools_required = ['sqlmap', 'nikto', 'ffuf', 'gobuster', 'nuclei']
tools_optional = ['dalfox', 'katana', 'wpscan']

print("=== Web Tools Check ===")
for tool in tools_required:
    if shutil.which(tool):
        print(f"✓ {tool}")
    else:
        print(f"✗ {tool} (gerekli)")

print("\n=== Optional Tools ===")
for tool in tools_optional:
    if shutil.which(tool):
        print(f"✓ {tool}")
    else:
        print(f"✗ {tool}")

print("\nÇözüm: fetih download-tools web")
EOF
```

---

## Notlar

- **sqlmap** → SQLi otomasyonu için must-have
- **ffuf + gobuster** → fuzzing/discovery için temel
- **nuclei** → template tabanlı tarama (çok hızlı)
- **wpcan** → WordPress özeldir, diğer teknoloji yok
- **Go araçları** (`nuclei`, `ffuf`, `dalfox`) → çok hızlı, önerilir
- **Python library'ler** (`httpx`, `aiohttp`) → custom exploit yazarken

Her skill başında hangi araçlar gerekli gösterilecek!

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: fbac740fdfb703de
-->

