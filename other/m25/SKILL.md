---
name: m25
description: "Lapisan enterprise-grade buat tim: review kepatuhan/regulasi, enforce brand guideline korporat, pipeline CI/CD, dan porting kode antar bahasa/framework. Opsional. Komplemen m16 (coding), m2 (deplo"
category: superagent/product
---

# m25 — Compliance, CI/CD & Code Migration (NEW in v4.1)

Lapisan enterprise-grade buat tim: review kepatuhan/regulasi, enforce brand guideline korporat, pipeline CI/CD, dan porting kode antar bahasa/framework. **Opsional.** Komplemen m16 (coding), m2 (deploy), m21 (enterprise/defensif), m20 (brand voice).

> Disclaimer: compliance review di sini = **bantuan teknis & checklist**, bukan nasihat hukum. Untuk keputusan legal final → counsel manusia. Surface risiko jujur, jangan klaim "pasti compliant".

| Capability | Sifat | Output |
|---|---|---|
| Compliance & regulatory review | advisory checklist | gap + rekomendasi |
| Brand-guidelines enforcement | lint corporate identity | pelanggaran + fix |
| Deploy pipeline / CI/CD | otomasi build→test→deploy | workflow file |
| Code-migrator | porting bahasa/framework | kode + catatan risiko |

---

## 1. Compliance & regulatory review

Cek sistematis vs framework relevan (GDPR, SOC2, PCI-DSS, HIPAA, dst) — sesuai konteks operator, bukan semua sekaligus.

```
1. SCOPE     → data apa yang disentuh? (PII, kartu, kesehatan) → framework mana yang berlaku
2. CHECKLIST → mapping kontrol: data retention, consent, enkripsi at-rest/in-transit, akses, audit log
3. GAP       → mana yang belum ada / setengah → ranking by risiko
4. REMEDIATE → rekomendasi konkret + contoh implementasi (komplemen m16)
```

Output: gap list + fix, BUKAN stempel "compliant". Tandai mana yang butuh review hukum manusia.

## 2. Brand-guidelines enforcement (corporate identity)

Lint output/aset vs brand guide (warna, font, logo usage, tone, terminologi). Beda dari m20 (humanizer/voice) — ini enforce *aturan korporat eksplisit*:

```python
GUIDE = {"colors":["#0A2540","#635BFF"], "forbidden_terms":["cheap","guys"],
         "required_terms":{"login":"sign in"}, "tone":"professional", "logo_min_px":24}
# scan teks/asset → flag pelanggaran + auto-fix yang aman (terminologi), sisanya report
```

Konsisten lintas semua materi = inti brand. Combo m20 untuk tone, m18 untuk visual token.

## 3. Deploy pipeline & CI/CD

Otomasi build → test → (gate) → deploy. Generate workflow sesuai platform:

```yaml
# .github/workflows/ci.yml — pola umum (sesuaikan)
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: <install deps>
      - run: <lint>
      - run: <test>            # WAJIB hijau sebelum deploy
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps: [ ... ]             # deploy ke VPS (m2) / registry
```

Prinsip: test gate sebelum deploy (jangan deploy merah), secret via CI secrets bukan hardcode, rollback plan. Deploy ke prod = aksi outward → kalau lewat agent, R9 gate. Combo m2 (target VPS), m16 (build).

## 4. Code-migrator (porting antar bahasa/framework)

Port kode antar bahasa (Python↔TS↔Go) atau framework (Express→FastAPI, Flask→Django):

```
1. INVENTORY → petakan modul, dependency, fitur bahasa yang gak ada padanan 1:1
2. IDIOM      → port ke IDIOM target, bukan transliterasi (Pythonic ≠ Go-ish)
3. TEST-FIRST → port test dulu / bikin karakterisasi test → jadi jaring regресi (combo x5/m26 TDD)
4. RISK        → tandai bagian yang semantik beda (async model, error handling, tipe, concurrency)
5. INCREMENTAL → migrasi bertahap + jalan paralel, jangan big-bang
```

Yang fatal: porting yang *terlihat* benar tapi semantik beda (mis. integer overflow, timezone, floating point, null vs undefined). Tandai eksplisit, jangan diam.

---

## Catatan
- Compliance = advisory, bukan legal advice. CI/CD prod deploy = R9 gate.
- Migrasi: test dulu (jaring regresi) sebelum sentuh logic.
- Combo: m25 + m16 (impl) + m2 (deploy) + x5 (regression) + m20 (brand tone).
