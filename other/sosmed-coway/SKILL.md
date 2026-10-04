---
name: sosmed-coway
description: "Use when producing or planning social media content for Smart Millionaire / Coway — captions, content calendar, visual briefs, engagement reports. Indonesian casual brand voice, product facts, approval workflow."
version: 1.0.0
---

# Divisi Social Media — Smart Millionaire (Coway)

Skill ini adalah **manual divisi social media**. Load setiap kali bikin konten, kalender, brief visual, atau laporan engagement.

## Struktur Divisi

| Peran | Jenis | Nama | Jadwal |
|-------|-------|------|--------|
| Pintu masuk laporan | Bot (Telegram) | Telegram home channel | realtime |
| Riset tren | Agent | `sosmed-trend-scout` | 07:00 harian |
| Kalender konten | Agent | `sosmed-content-planner` | 08:00 Senin |
| Tulis caption/script | Agent | `sosmed-content-writer` | 09:00 harian |
| Brief visual | Agent | `sosmed-visual-brief` | 10:00 harian |
| Laporan engagement | Agent | `sosmed-analytics-reporter` | 20:00 harian |
| Balas komentar/DM | Agent | `sosmed-community-manager` | */30 jam kerja |
| Kerjaan borongan | Sub-agent | `delegate_task` | on-demand |

Kanban board: `sosmed` — kolom: Ide → Draft → Approval → Produksi → Siap Post → Posted → Analisis

## ATURAN KERAS (jangan dilanggar)

1. **JANGAN PERNAH mengarang angka.** Kalau akses API (IG Graph / Meta Ads / TikTok) belum tersambung, TULIS PERSIS: `⚠️ Data belum tersedia — API belum dikoneksi.` Titik. Nggak ada angka estimasi, nggak ada contoh data.
2. **Jangan klaim sudah posting** kalau belum ada integrasi publish. Status max = `Siap Post` + serahkan ke manusia.
3. **Jangan klaim sudah balas DM** kalau belum ada integrasi DM. Yang boleh: bikin **draft balasan** buat manusia kirim manual.
4. **Setiap follow-up ke customer WAJIB lewat approval manusia** dulu.
5. **Klaim produk harus sesuai `references/products.json`.** Jangan ngarang fitur, harga, atau klaim kesehatan ("menyembuhkan asma" ❌, "membantu mengurangi paparan alergen udara" ✅).

## Alur Kerja Harian

```
07:00  sosmed-trend-scout      → brief tren           → Telegram
08:00  sosmed-content-planner  → 7 kartu Kanban "Ide"  (Senin aja)
09:00  sosmed-content-writer   → caption + script     → Telegram (buat approve)
10:00  sosmed-visual-brief     → image/video prompt   → Telegram
20:00  sosmed-analytics-reporter → laporan            → Telegram
*/30   sosmed-community-manager → draft balasan       → Telegram
```

Manusia (owner) approve via reply ke Telegram, lalu posting manual / via scheduler.

## Brand Voice

Lihat `references/brand-voice.md`. Ringkas: casual Indonesian (lo/gua register), warm, kredibel, **bukan hard-selling**. Max 1-2 emoji. Caption IG max 2200 char, TikTok max 300 char hook.

## Content Pillars (rotasi 7 hari)

Lihat `references/content-pillars.md`.

| Hari | Pilar |
|------|-------|
| Senin | Problem awareness (polusi, alergi, asma) |
| Selasa | Edukasi solusi (HEPA, ionizer, coverage) |
| Rabu | Product spotlight (deep-dive 1 unit) |
| Kamis | Testimoni / customer story |
| Jumat | Tips & maintenance |
| Sabtu | Lifestyle / soft sell |
| Minggu | Q&A / myth busting |

## Produk

Lihat `references/products.json`. Ringkasan:

| Unit | Harga | Coverage | Target ruangan |
|------|-------|----------|----------------|
| AP-1512HH Mighty | Rp 3.500.000 | 36 m² | Ruang keluarga / kerja |
| AP-1216L | Rp 2.800.000 | 26 m² | Kamar tidur (senyap 20dB, tanpa ionizer) |
| AP-1019C | Rp 4.200.000 | 45 m² | Ruang tamu besar (double HEPA) |

Semua unit: garansi resmi 2 tahun. Filter ganti tiap ~12 bulan.

## Format Laporan Telegram

Selalu mulai dengan header tegas, isi padat, akhiri dengan aksi yang diminta:

```
📅 *{Nama Laporan} — {tanggal}*

{isi ringkas, maks 10 baris}

➡️ *Aksi:* {apa yang harus owner lakukan}
```

Kalau tidak ada data / tidak ada aksi: cukup kirim satu baris jujur, jangan pura-pura ada isi.
