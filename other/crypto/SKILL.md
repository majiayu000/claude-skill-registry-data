---
category: ctf
name: crypto-category-tools
description: Crypto kategori SKILL.md — RSA, ECC, AES, hash, encoding saldırıları için gerekli araçları kurma rehberi
tags: [ctf, crypto, tools, setup, pycryptodome, gmpy2, sympy]
adapted_for: fetih
---

# Crypto Kategorisi — Gerekli Araçlar

Crypto challenge'larında kullandığımız tüm araçlar ve kurulum yöntemi.

## Gerekli Araçlar

Bu kategorideki skill'leri kullanabilmek için aşağıdaki araçlar gerekli:

| Araç | Açıklama | Kurulum |
|------|----------|---------|
| **pycryptodome** | Kripto kütüphanesi (AES, RSA, DES vb.) | `pip install pycryptodome` |
| **gmpy2** | GMP Python binding — RSA saldırıları | `pip install gmpy2` |
| **sympy** | Sembolik matematik — faktörizasyon, polinomlar | `pip install sympy` |
| **fpylll** | LLL lattice reduction — Boneh-Durfey, Coppersmith | `pip install fpylll` |
| **padding-oracle** | Padding oracle saldırı kütüphanesi | `pip install padding-oracle` |

## Araçları Hızlı Kur

Tüm crypto araçlarını bir komutla kur:

```bash
fetih download-tools crypto
```

Bu komut:
- Gerekli araçların kurulu olup olmadığını kontrol eder
- Eksik olanları otomatik yükler
- Python kütüphaneleri için `pip`, `uv pip` veya `pipx` kullanır

## Araçlar Kurulu mu Kontrol Et

```bash
# Hepsini görmek için
fetih download-tools status

# Sadece crypto kısmını filtrelemek için
fetih download-tools status | grep -A 10 "CRYPTO"

# Python'dan manuel kontrol
python3 -c "import Crypto, gmpy2, sympy, fpylll, padding_oracle; print('Tüm araçlar kurulu')"
```

## Her Araç Neye Yarar?

### pycryptodome
Kripto algoritmaları — AES, DES, RSA, ECC, hash fonksiyonları

**Skill'lerde kullanılır:**
- `crypto/aes-cbc-bitflip` — AES-CBC mode işlemleri
- `crypto/aes-gcm-nonce-reuse` — AES-GCM şifrele/çöz
- `crypto/rsa-*` — RSA modül işlemleri

```python
from Crypto.Cipher import AES, RSA
from Crypto.Hash import SHA256
```

### gmpy2
Büyük sayı matematik — RSA faktörizasyon, modüler işlemler

**Skill'lerde kullanılır:**
- `crypto/rsa-wiener-attack` — Wiener saldırısı için gcd
- `crypto/rsa-common-modulus` — Extended GCD
- `crypto/lattice-attacks` — Lattice reduction

```python
import gmpy2
p, q = gmpy2.gcd(n1, n2), n1 // gmpy2.gcd(n1, n2)
```

### sympy
Sembolik matematik — faktörizasyon, polinom çözme

**Skill'lerde kullanılır:**
- `crypto/lattice-attacks` — Boneh-Durfey / Coppersmith
- `crypto/rsa-close-primes` — n = p*q veya n = p*q*r şekillerinde faktörizasyon
- `crypto/z3-constraint-solving` — Denklem sistemi çözme

```python
from sympy import factorint, symbols, solve
```

### fpylll
LLL lattice reduction algoritması — yüksek boyutlu saldırılar

**Skill'lerde kullanılır:**
- `crypto/lattice-attacks` — Boneh-Durfey CVE
- `crypto/elliptic-curve-attacks` — ECC discrete log

```python
from fpylll import IntegerMatrix, LLL
```

### padding-oracle
Padding oracle saldırı — AES-CBC padding hatalarından yararlanma

**Skill'lerde kullanılır:**
- `crypto/rsa-padding-oracle` — Oracle-based RSA decryption

---

## Kurulum Sorunları Çözme

### "No module named 'gmpy2'"

gmpy2 native extension gerektirir — build tools yükle:

```bash
sudo apt-get install -y libgmp3-dev libmpfr-dev libmpc-dev
pip install gmpy2
```

### "No module named 'fpylll'"

fpylll de native extension gerektirir:

```bash
sudo apt-get install -y libfplll-dev
pip install fpylll
```

### pip install başarısız

`uv` kullan:

```bash
uv pip install pycryptodome gmpy2 sympy fpylll padding-oracle
```

---

## Hızlı Test Scripti

Tüm araçların kurulu olduğunu test et:

```bash
python3 << 'EOF'
try:
    import Crypto
    import gmpy2
    import sympy
    import fpylll
    import padding_oracle
    print("✓ Tüm crypto araçları kurulu!")
except ImportError as e:
    print(f"✗ Eksik araç: {e}")
    print("Çözüm: fetih download-tools crypto")
EOF
```

---

## Notlar

- **pycryptodome**, **sympy**, **padding-oracle** → pure Python, hızlı kurulur
- **gmpy2**, **fpylll** → native extension, build tools gerekli
- Her skill başında araç kontrolü ve kurulum önerisi olur
- Linux-only kurulum (Windows/macOS desteklenmez şu an)

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: 68a7dba316dbda18
-->

