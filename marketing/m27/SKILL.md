---
name: m27
description: "Mesin konten sosial end-to-end: strategi (pillar/audience/positioning), kalender, adaptasi per-platform, hook scroll-stopper, caption+hashtag, dan script thread/carousel/reels. Opsional, non-dana."
category: superagent/content
---

# m27 — Content Strategy & Social Media (NEW in v4.1)

Mesin konten sosial end-to-end: strategi (pillar/audience/positioning), kalender, adaptasi per-platform, hook scroll-stopper, caption+hashtag, dan script thread/carousel/reels. **Opsional, non-dana.** Tool: `tools/content.py`. Pelengkap m3 (voice ID/CT & airdrop), m20 (humanizer), m18 (visual), m28 (copy frameworks), m29 (riset/analitik).

> Beda dari m3: m3 = voice Indonesia/crypto-twitter + template airdrop. m27 = strategi & produksi sosial umum lintas platform. Combo keduanya buat konten crypto-ID.

---

## 1. Content strategy builder

Sebelum produksi, tentuin fondasi (sekali, simpan di vault m15, reuse):

```
PILLARS    → 3-5 tema inti (mis. edukasi · behind-scenes · proof · opini · CTA). Rasio 70-20-10.
AUDIENCE   → siapa, masalah apa, di platform mana, bahasa apa
POSITIONING→ 1 kalimat: "buat [audience] yang [masalah], gua [solusi unik]"
TONE       → ambil dari brand voice (m20) / USER.md
GOAL        → awareness | trust | leads | sales — beda goal, beda format
```

Output = "content OS" yang nyetir semua keputusan berikutnya. Tanpa ini, konten jadi random.

## 2. Content calendar generator

```python
from content import calendar
plan = calendar(pillars=["edukasi","proof","opini"], days=30, per_week=5,
                platforms=["x","linkedin","ig"])
# → list {date, pillar, platform, format, topic_slot}  — isi topik via LLM/ide (m29)
```

Distribusi pillar merata + variasi format, hindari spam 1 jenis. Mingguan/bulanan. Sambung cron (m4/m17) buat auto-publish.

## 3. Platform-specific adapter

Satu pesan, beda baju per platform — JANGAN copy-paste identik:

| Platform | Format menang | Panjang | Nada |
|---|---|---|---|
| **X/Twitter** | thread, 1-liner punchy | pendek, hook di tweet 1 | cepat, opini |
| **LinkedIn** | thought leadership, story | medium, baris pendek | profesional-personal |
| **Instagram** | carousel, visual-first | caption medium + hook | visual, relatable |
| **TikTok/Reels** | script video pendek | 15-60s, hook 3 detik pertama | energetik, native |

```python
from content import adapt
variants = adapt("inti pesan lo", platforms=["x","linkedin","ig","tiktok"])
```

## 4. Viral hook & scroll-stopper

Hook = 80% performa. Stop scroll dalam 3 detik / baris pertama:

```
POLA HOOK:
- Kontras   : "Semua orang bilang X. Mereka salah."
- Angka      : "3 kesalahan yang bikin lo rugi..."
- Pertanyaan : "Kenapa post lo gak ada yang liat?"
- Stakes     : "Gua kehilangan $5k sebelum sadar ini"
- Curiosity gap: "Ini yang gak ada yang kasih tau soal..."
```

Hook harus relevan ke isi (clickbait yang gak nepatin = kill trust). CTA jelas di akhir: satu aksi, bukan lima.

## 5. Caption + hashtag optimizer

```python
from content import caption, hashtags
cap = caption("topik", platform="ig", hook_style="curiosity", cta="follow")
tags = hashtags("topik", platform="ig", mix=("broad","niche","branded"))  # campur jangkauan
```

Hashtag: campur broad (jangkauan) + niche (relevan) + branded (milik lo). Riset trending → m29. Jangan spam 30 tag generik.

## 6. Thread / carousel / reels writer

```python
from content import thread, carousel, reels_script
thread("topik", n=7)              # X/LinkedIn: hook → poin → CTA, tiap tweet berdiri sendiri
carousel("topik", slides=8)        # IG: 1 ide/slide, slide 1 = hook, terakhir = CTA
reels_script("topik", seconds=30)  # script + timing + voiceover + on-screen text
```

Repurposing 1 long-form → multi-format → m29 pipeline.

---

## Catatan
- Konten = artefak, gak ada gate. Publish ke platform = aksi outward → kalau via agent, R9 gate sekali.
- Humanize sebelum publish (m20) biar gak "bau AI". Visual → m18. Frameworks copy → m28.
- Combo: m27 + m28 (copy) + m20 (humanize) + m18 (visual) + m29 (riset/analitik) + m4/m17 (schedule).
