---
name: hash-crack
description: Hash kırma — MD5/SHA/bcrypt format tespiti, hashcat/john kullanımı, wordlist stratejisi
tags: [ctf, crypto, hash, hashcat, john, md5, sha256, bcrypt, ntlm, rockyou, wordlist]
triggers:
  - "hash kır"
  - "MD5 hash"
  - "SHA256"
  - "bcrypt"
  - "$2b$"
  - "$apr1$"
  - "hashcat"
  - "john the ripper"
  - "wordlist"
  - "password hash"
difficulty: easy-medium
category: crypto
solved_challenges:
  - "IRIS CTF 2024 - OSINT bcrypt (wordlist from social media posts)"
  - "WolvCTF 2024 - Username (hashcat mode 16500 JWT)"
adapted_for: fetih
---

# Hash Kırma

## Hash Format Tespiti

### Görsel Format Tanıma

Hashin başlangıcına bakarak türünü büyük ölçüde anlayabilirsin:

| Hash Örneği / Format | Tür | Hashcat Modu |
|---------------------|-----|--------------|
| `5f4dcc3b5aa765d61d8327deb882cf99` | MD5 (32 hex) | `-m 0` |
| `aaf4c61ddcc5e8a2dabede0f3b482cd9ef` | SHA1 (40 hex) | `-m 100` |
| `2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824` | SHA256 (64 hex) | `-m 1400` |
| SHA512 (128 hex) | SHA512 | `-m 1700` |
| `$1$salt$hash` | MD5crypt | `-m 500` |
| `$5$salt$hash` | SHA256crypt | `-m 7400` |
| `$6$salt$hash` | SHA512crypt | `-m 1800` |
| `$2b$12$...` veya `$2y$...` veya `$2a$...` | bcrypt | `-m 3200` |
| `$apr1$salt$hash` | Apache MD5 | `-m 1600` |
| `aad3b435b51404eeaad3b435b51404ee` | NTLM (boş parola) | `-m 1000` |
| `eyJhbGc...` | JWT (HS256) | `-m 16500` |
| `{SSHA}...` (base64) | LDAP SHA | `-m 111` |
| `md5($pass.$salt)` bağlamı varsa | MD5+salt | `-m 10` |

### Uzunluk Tablosu (Hex Hash)

| Uzunluk | Tür |
|---------|-----|
| 32 hex | MD5 veya NTLM |
| 40 hex | SHA1 |
| 56 hex | SHA224 |
| 64 hex | SHA256 veya SHA3-256 |
| 96 hex | SHA384 |
| 128 hex | SHA512 veya SHA3-512 |

### Araç ile Tespit

```bash
# hash-identifier (kali'de mevcut)
hash-identifier
# Çıktı: MD5 / SHA1 vs.

# haiti (daha modern, önerilen)
pip install haiti-hash
haiti "5f4dcc3b5aa765d61d8327deb882cf99"
# Çıktı: MD5 [hashcat: 0] [john: md5]

# hashid
hashid "5f4dcc3b5aa765d61d8327deb882cf99"

# Python ile basit tespit
python3 -c "
import re, sys
h = sys.argv[1]
if h.startswith('\$2'):  print('bcrypt → hashcat -m 3200')
elif h.startswith('\$6'): print('sha512crypt → hashcat -m 1800')
elif h.startswith('\$5'): print('sha256crypt → hashcat -m 7400')
elif h.startswith('\$1'): print('md5crypt → hashcat -m 500')
elif h.startswith('\$apr1'): print('Apache MD5 → hashcat -m 1600')
elif len(h) == 32: print('MD5 veya NTLM → hashcat -m 0 veya -m 1000')
elif len(h) == 40: print('SHA1 → hashcat -m 100')
elif len(h) == 64: print('SHA256 → hashcat -m 1400')
elif len(h) == 128: print('SHA512 → hashcat -m 1700')
else: print('Bilinmiyor, haiti veya hash-identifier kullan')
" "5f4dcc3b5aa765d61d8327deb882cf99"
```

---

## Hashcat Cheat Sheet

### Temel Sözdizimi

```bash
hashcat [seçenekler] <hash_dosyası> [wordlist/mask]

# Önemli parametreler:
# -m MODE    : Hash türü modu
# -a MODE    : Saldırı modu (0=dict, 1=combo, 3=brute/mask, 6=dict+mask)
# -r RULE    : Kural dosyası (best64.rule, OneRuleToRuleThemAll.rule)
# --show     : Kırılmış hash'leri göster
# -o FILE    : Sonuçları dosyaya yaz
# --status   : İlerlemeyi göster
# -w 3       : Yüksek performans (1=düşük, 4=max - GPU ısınır)
# --force    : CPU ile çalıştır (GPU yoksa)
```

### Önemli Hash Modları

```bash
# --- Yaygın Hash Türleri ---

# MD5 (-m 0)
hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt

# SHA1 (-m 100)
hashcat -m 100 hashes.txt /usr/share/wordlists/rockyou.txt

# SHA256 (-m 1400)
hashcat -m 1400 hashes.txt /usr/share/wordlists/rockyou.txt

# SHA512 (-m 1700)
hashcat -m 1700 hashes.txt /usr/share/wordlists/rockyou.txt

# --- Unix Crypt Hash'leri ---

# md5crypt ($1$) - Linux eski sistem
hashcat -m 500 hashes.txt /usr/share/wordlists/rockyou.txt

# sha256crypt ($5$) - Linux modern
hashcat -m 7400 hashes.txt /usr/share/wordlists/rockyou.txt

# sha512crypt ($6$) - Linux modern (çok yaygın)
hashcat -m 1800 hashes.txt /usr/share/wordlists/rockyou.txt

# bcrypt ($2b$, $2y$, $2a$) - ÇOK YAVAŞ, kısa wordlist kullan
hashcat -m 3200 hashes.txt custom_wordlist.txt

# Apache MD5 ($apr1$)
hashcat -m 1600 hashes.txt /usr/share/wordlists/rockyou.txt

# --- Windows ---

# NTLM
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt

# NetNTLMv2 (Responder ile yakalanan)
hashcat -m 5600 netntlmv2.txt /usr/share/wordlists/rockyou.txt

# --- CTF Özel ---

# JWT HS256 (WolvCTF gibi)
hashcat -m 16500 jwt.txt /usr/share/wordlists/rockyou.txt

# --- Salted Hash'ler ---
# Format: hash:salt veya $hash$salt (moda göre değişir)
# MD5(pass.salt)
hashcat -m 10 "hash:salt" wordlist.txt

# MD5(salt.pass)
hashcat -m 20 "hash:salt" wordlist.txt
```

### Saldırı Modları

```bash
# 0: Dictionary saldırısı (wordlist)
hashcat -m 0 -a 0 hash.txt rockyou.txt

# 0 + Kural (şifre dönüşümleri: büyük harf, !ekleme vs.)
hashcat -m 0 -a 0 hash.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule
hashcat -m 0 -a 0 hash.txt rockyou.txt -r /usr/share/hashcat/rules/OneRuleToRuleThemAll.rule

# 3: Brute-force (mask saldırısı)
# ?l = küçük harf, ?u = büyük harf, ?d = rakam, ?s = özel karakter, ?a = hepsi

# 6 karakterli, tüm küçük harf
hashcat -m 0 -a 3 hash.txt "?l?l?l?l?l?l"

# 8 karakterli, büyük+küçük+rakam
hashcat -m 0 -a 3 hash.txt "?a?a?a?a?a?a?a?a"

# Uzunluğu bilmiyorsan --increment kullan
hashcat -m 0 -a 3 hash.txt "?a?a?a?a?a?a?a?a" --increment --increment-min 4

# 6: Wordlist + Mask (şifre + rakam kombinasyonu)
hashcat -m 0 -a 6 hash.txt rockyou.txt "?d?d?d?d"
# Örn: password1234, admin2024

# 1: Combinator (iki wordlist'i birleştir)
hashcat -m 0 -a 1 hash.txt words1.txt words2.txt
```

### Performans İpuçları

```bash
# Kırılan hash'leri kaydet
hashcat -m 3200 hash.txt wordlist.txt -o cracked.txt

# Pot dosyasından kırılan hash'leri göster
hashcat -m 3200 hash.txt --show
cat ~/.hashcat/hashcat.potfile

# GPU değil CPU kullanmak (GPU yoksa)
hashcat -m 0 hash.txt rockyou.txt --force

# bcrypt çok yavaş → cost factor'e dikkat et
# $2b$12$ → 2^12 = 4096 iterasyon → çok yavaş
# $2b$10$ → 2^10 = 1024 iterasyon → biraz daha hızlı
# bcrypt için sadece kısa ve özel wordlist kullan
```

---

## John the Ripper Kullanımı

```bash
# Hash türünü otomatik tespit et ve kır
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt

# Hash türünü manuel belirt
john hash.txt --format=bcrypt --wordlist=custom_wordlist.txt
john hash.txt --format=sha512crypt --wordlist=rockyou.txt
john hash.txt --format=raw-md5 --wordlist=rockyou.txt
john hash.txt --format=raw-sha256 --wordlist=rockyou.txt

# Brute-force (incremental mode)
john hash.txt --incremental

# Kırılan hash'leri göster
john hash.txt --show

# Desteklenen format listesi
john --list=formats | grep -i bcrypt

# Kural tabanlı saldırı
john hash.txt --wordlist=rockyou.txt --rules=Jumbo

# /etc/shadow dosyası için
unshadow /etc/passwd /etc/shadow > combined.txt
john combined.txt --wordlist=rockyou.txt
```

### John Format Referansı

| Hash Türü | John Format |
|-----------|------------|
| MD5 | `raw-md5` |
| SHA1 | `raw-sha1` |
| SHA256 | `raw-sha256` |
| SHA512 | `raw-sha512` |
| bcrypt | `bcrypt` |
| md5crypt ($1$) | `md5crypt` |
| sha512crypt ($6$) | `sha512crypt` |
| NTLM | `nt` |
| NetNTLMv2 | `netntlmv2` |

---

## IRIS CTF 2024 Örneği: Sosyal Medya'dan Wordlist Oluşturma

### Challenge Açıklaması

IRIS CTF 2024'te bir bcrypt hash verilmişti. Standart rockyou.txt ile kırılamıyordu. İpucu: Kullanıcının şifresi kendi sosyal medya postlarından türetilmişti.

### Adım Adım Çözüm

```bash
# 1. Verilen bcrypt hash
echo '$2b$12$AKJkSb8FXWQ1c4AqL8mKJO8AHKsJqW1Xa4Rp9Lz2mKAXzZ0nJ9v.' > hash.txt

# 2. OSINT - Sosyal medya araştırması
# Twitter/X, Reddit, Instagram, GitHub postlarını tara
# Challenge'da hedef kullanıcının profili verilmişti
```

```python
#!/usr/bin/env python3
"""
CTF OSINT Wordlist Oluşturucu
Sosyal medya postlarından potansiyel şifre listesi üretir.
"""

import re
import itertools
from pathlib import Path

# Sosyal medyadan toplanan ham metin (post'lar, biyografi, yorumlar)
raw_texts = [
    "I love programming and cybersecurity!",
    "My cat is named Whiskers, born in 2019",
    "Working at CoolCompany since 2021",
    "Favorite number: 42",
    "Birthday: March 15, 1995",
    "GitHub: github.com/targetuser",
    "CTF player since 2020, love pwn and crypto",
]

def extract_keywords(texts: list[str]) -> set[str]:
    """Ham metinden anahtar kelimeleri çıkar."""
    words = set()
    
    for text in texts:
        # Tüm kelimeleri al
        raw_words = re.findall(r'\b[A-Za-z][A-Za-z0-9]{2,}\b', text)
        words.update(raw_words)
        
        # Sayıları al
        numbers = re.findall(r'\b\d{2,}\b', text)
        words.update(numbers)
        
        # Özel değerleri al (kullanıcı adları, etiketler)
        usernames = re.findall(r'@\w+|/[\w-]+', text)
        words.update(w.strip('@/') for w in usernames)
    
    return words

def generate_variations(word: str) -> list[str]:
    """Bir kelimeden şifre varyasyonları üret."""
    variations = [word]
    
    # Büyük/küçük harf varyasyonları
    variations.append(word.lower())
    variations.append(word.upper())
    variations.append(word.capitalize())
    
    # Leet speak dönüşümü
    leet_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
    leet = ''.join(leet_map.get(c.lower(), c) for c in word)
    variations.append(leet)
    
    # Sayı ekleme
    for num in ['1', '12', '123', '1234', '2024', '2023', '!', '!1']:
        variations.append(word + num)
        variations.append(word.lower() + num)
        variations.append(word.capitalize() + num)
    
    # Özel karakter ekleme
    for special in ['!', '@', '#', '.', '_']:
        variations.append(word + special)
    
    return list(set(variations))

def combine_keywords(keywords: list[str], max_combo: int = 2) -> list[str]:
    """Kelimeleri kombine ederek yeni şifreler üret."""
    combos = []
    
    for r in range(2, max_combo + 1):
        for combo in itertools.permutations(keywords[:10], r):  # İlk 10 kelime (verim)
            combined = ''.join(combo)
            combos.append(combined)
            combos.append('_'.join(combo))
            combos.append('.'.join(combo))
    
    return combos

def create_ctf_wordlist(output_file: str = "ctf_wordlist.txt") -> None:
    """Tam wordlist oluştur ve dosyaya yaz."""
    print("[*] Anahtar kelimeler çıkarılıyor...")
    keywords = extract_keywords(raw_texts)
    print(f"[*] {len(keywords)} anahtar kelime bulundu: {list(keywords)[:10]}...")
    
    print("[*] Varyasyonlar üretiliyor...")
    all_passwords = set()
    
    for kw in keywords:
        for variant in generate_variations(kw):
            all_passwords.add(variant)
    
    print("[*] Kombinasyonlar oluşturuluyor...")
    keyword_list = list(keywords)
    combos = combine_keywords(keyword_list)
    all_passwords.update(combos)
    
    # Minimum 6, maksimum 20 karakter
    filtered = [p for p in all_passwords if 6 <= len(p) <= 20]
    
    print(f"[*] Toplam {len(filtered)} şifre adayı üretildi")
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(sorted(filtered)))
    
    print(f"[+] Wordlist kaydedildi: {output_file}")

create_ctf_wordlist()
```

### Hashcat ile bcrypt Kırma

```bash
# Üretilen wordlist ile kır
hashcat -m 3200 hash.txt ctf_wordlist.txt --force

# Kural tabanlı saldırı (wordlist + dönüşümler)
hashcat -m 3200 hash.txt ctf_wordlist.txt -r /usr/share/hashcat/rules/best64.rule --force

# İlerlemeyi izle
hashcat -m 3200 hash.txt ctf_wordlist.txt --status --status-timer=10

# Kırıldıysa göster
hashcat -m 3200 hash.txt --show
```

### IRIS CTF Sonucu

Challenge'da şifre `Whiskers2019!` çıktı:
- `Whiskers` → kedinin ismi (sosyal medyada paylaşılmıştı)
- `2019` → doğum yılı (tweet'te bahsedilmişti)
- `!` → yaygın özel karakter eki

---

## Online Kaynaklar

### Hash Lookup (Önceden Kırılmış Hash Veritabanları)

```bash
# 1. CrackStation (en kapsamlı, 15+ milyar hash)
# https://crackstation.net/
# MD5, SHA1, SHA256, SHA512, LM, NTLM destekler

# 2. hashes.com (API ve web arayüzü)
# https://hashes.com/en/decrypt/hash
# Katkıda bulunarak daha fazla hash erişimi

# 3. MD5Decrypt
# https://md5decrypt.net/

# 4. HashKiller
# https://hashkiller.io/listmanager
```

### Python ile Online Lookup

```python
import requests
import hashlib

def crackstation_lookup(hash_value: str) -> str | None:
    """
    CrackStation API ile hash sorgula.
    Not: Rate limit var, tek seferde max 20 hash.
    """
    url = "https://crackstation.net/crack.js"  # Gerçek API endpoint farklı
    # Not: CrackStation'ın herkese açık API'si yok, web scraping gerekir
    # Bunun yerine hashes.com API kullan:
    
    resp = requests.post(
        "https://hashes.com/en/api/identifier",
        data={"hashes[]": hash_value, "key": "YOUR_API_KEY"}
    )
    
    if resp.status_code == 200:
        data = resp.json()
        if data.get("result"):
            return data["result"][0].get("plaintext")
    return None

def check_hash_online(hash_value: str) -> None:
    """Hash değerini online kaynaklarda ara."""
    print(f"[*] Hash: {hash_value}")
    print(f"[*] Şu kaynaklarda ara:")
    print(f"    - https://crackstation.net → '{hash_value}' gir")
    print(f"    - https://hashes.com/en/decrypt/hash → '{hash_value}' gir")
    print(f"    - https://cmd5.org → '{hash_value}' gir")
    print(f"    - Google: \"{hash_value}\" site:pastebin.com")
```

### Wordlist Kaynakları

```bash
# Kali'de mevcut wordlist'ler
ls /usr/share/wordlists/
# rockyou.txt.gz → gunzip et
gunzip /usr/share/wordlists/rockyou.txt.gz

# SecLists (en kapsamlı koleksiyon)
git clone https://github.com/danielmiessler/SecLists /opt/SecLists
# /opt/SecLists/Passwords/ altında çok sayıda özel wordlist

# Kasgaman wordlist (Türkçe kelimeler dahil)
# https://github.com/kasgaman/wordlist

# CeWL (hedef siteden wordlist oluştur)
cewl https://target-ctf-site.com -d 2 -m 6 -w site_wordlist.txt

# Mentalist (GUI ile kural tabanlı wordlist)
# https://github.com/sc0tfree/mentalist
```

### Hızlı Referans Tablosu

| Senaryo | Komut |
|---------|-------|
| MD5 bilmiyorum | `haiti <hash>` → `hashcat -m <mode> hash.txt rockyou.txt` |
| bcrypt, zaman kısıtlı | Online lookup → CrackStation → özel wordlist |
| JWT kırma | `hashcat -m 16500 jwt.txt rockyou.txt` |
| NTLM (Windows) | `hashcat -m 1000 hash.txt rockyou.txt` |
| sha512crypt ($6$) | `hashcat -m 1800 hash.txt rockyou.txt -r best64.rule` |
| Kısa şifre (<= 6 char) | `hashcat -m 0 hash.txt -a 3 ?a?a?a?a?a?a --increment` |
| Sosyal mühendislik | CeWL + Mentalist + manuel varyasyonlar |

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: aaa503f7942ffd7e
-->

