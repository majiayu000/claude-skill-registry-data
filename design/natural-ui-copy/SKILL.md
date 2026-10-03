---
name: natural-ui-copy
description: >
  Gunakan skill ini setiap kali kamu membuat, mengedit, atau mereview teks
  yang akan muncul di antarmuka website atau aplikasi — termasuk landing page,
  dashboard, form, komponen UI, email template, onboarding flow, dan halaman
  marketing. Trigger ketika user meminta "buatkan halaman X", "buatkan komponen
  Y", "buat copy untuk Z", "tuliskan teks di website ini", "revisi copywriting",
  "buat landing page", "buat hero section", "buat form login", atau ketika kamu
  sedang menulis kode frontend yang mengandung teks yang akan dibaca user.
  Skill ini HARUS digunakan setiap kali ada teks UI yang perlu ditulis agar
  output terasa natural, bukan seperti template generik buatan AI.
---

# Natural UI Copy & Design Language Skill

Skill ini memastikan setiap teks dan elemen desain yang kamu hasilkan terasa
seperti ditulis oleh manusia yang paham produk — bukan AI yang copy-paste
template. Output harus terasa konsisten, relevan konteks, dan layak production.

---

## Prinsip Utama

### 1. Copy-First, Code Second

Sebelum menulis satu baris JSX/HTML, tentukan dulu:
- **Apa yang sedang user rasakan** di titik ini dalam perjalanan mereka?
- **Apa satu hal yang harus mereka mengerti** setelah membaca teks ini?
- **Apa tindakan yang kamu inginkan** dari mereka?

Teks yang baik tidak mendeskripsikan UI. Ia berbicara langsung ke situasi user.

### 2. Specificity Beats Generic

❌ Generic (AI banget):
- "Selamat datang di platform kami"
- "Masukkan data Anda di sini"
- "Terjadi kesalahan. Coba lagi."
- "Fitur ini memungkinkan Anda untuk melakukan X"

✅ Specific (terasa manusiawi):
- "Undangan pertama kamu, setengah jadi. Selesaikan sekarang?"
- "Nama pasangan yang akan tampil di undangan"
- "Link undangan kamu expired. Buat yang baru — gratis."
- "Pilih template, isi nama, kirim ke tamu. Selesai dalam 5 menit."

### 3. Tone Adalah Konsistensi, Bukan Mood

Tone tidak berarti selalu santai atau selalu formal. Tone berarti **konsisten
dengan konteks produk**. Tentukan tone berdasarkan:

| Konteks | Tone yang Tepat |
|---|---|
| Onboarding / pertama kali | Hangat, encouraging, simple |
| Dashboard / kerja | Efisien, to the point, tanpa basa-basi |
| Error / masalah | Jelas, tidak menyalahkan, solutif |
| Empty state | Helpful, bukan sekadar "Tidak ada data" |
| Sukses / konfirmasi | Positif, konkret, brief |
| Marketing / landing | Benefit-first, engaging, tidak hype berlebihan |

---

## Panduan Per Elemen UI

### Hero Section / Headline Utama

**Formula**: [Outcome yang diinginkan user] + [cara/konteks yang membedakan]

Hindari:
- Headline tentang produk: "Platform undangan digital terbaik"
- Klaim kosong: "Cepat, mudah, dan terpercaya"
- Jargon industri tanpa konteks

Gunakan:
- Headline tentang user/hasil: "Undanganmu sudah jadi sebelum resepsi dimulai"
- Konkret dan spesifik: "Buat undangan digital dalam 10 menit. Tanpa desainer."
- Subheadline yang menjawab "kenapa harus percaya": jelas, satu kalimat

```tsx
// ❌ Generic
<h1>Platform Undangan Digital Terbaik</h1>
<p>Buat undangan indah dengan mudah dan cepat untuk acara spesialmu.</p>

// ✅ Natural & Specific
<h1>Undanganmu, selesai hari ini.</h1>
<p>Pilih template, isi detail acara, dan bagikan link ke semua tamu — 
   tanpa perlu desainer atau print.</p>
```

### CTA (Call to Action)

**Aturan**: CTA harus menjawab pertanyaan "Apa yang terjadi kalau saya klik ini?"

| ❌ Hindari | ✅ Gunakan |
|---|---|
| "Submit" | "Kirim Undangan" |
| "Click Here" | "Lihat Template" |
| "Get Started" | "Buat Undangan Gratis" |
| "Learn More" | "Lihat Cara Kerjanya" |
| "Continue" | "Lanjut ke Detail Acara" |

Untuk CTA sekunder, gunakan tone lebih pasif: "Mungkin nanti", "Lihat dulu", 
"Tanya kami"

### Form Labels & Placeholder

**Labels**: Deskriptif, bukan labelan database.
**Placeholder**: Gunakan contoh nyata, bukan instruksi.
**Helper text**: Muncul di bawah field, jelaskan format atau konteks.

```tsx
// ❌ Generic
<label>Nama</label>
<input placeholder="Masukkan nama Anda" />

// ✅ Natural
<label>Nama pasangan (yang tampil di undangan)</label>
<input placeholder="mis. Budi & Sari" />
<p className="text-sm text-muted">Nama ini akan muncul persis seperti yang kamu tulis</p>
```

### Empty States

Empty state bukan "Tidak ada data ditemukan." Empty state adalah **momen 
mengajak user memulai**.

Struktur yang baik:
1. **Ilustrasi/icon** — visual yang relevan, bukan icon generic
2. **Headline** — jelaskan *situasi*, bukan state teknis
3. **Body** — apa yang bisa mereka lakukan
4. **CTA** — satu aksi utama yang jelas

```tsx
// ❌ Generic
<p>Belum ada undangan. Buat sekarang.</p>

// ✅ Natural
<div className="empty-state">
  <Icon name="envelope-open" />
  <h3>Belum ada undangan yang dibuat</h3>
  <p>Mulai dengan memilih template — kamu bisa edit semua detailnya 
     sebelum dikirim ke tamu.</p>
  <Button>Pilih Template</Button>
</div>
```

### Error Messages

Error messages harus: **menjelaskan masalah → menyalahkan sistem bukan user → 
memberikan solusi**.

```tsx
// ❌ Buruk
"Error 422: Validation failed"
"Terjadi kesalahan. Silakan coba lagi."
"Email tidak valid"

// ✅ Baik
"Email ini sudah terdaftar. Mau masuk saja?" 
"Koneksi terputus — perubahanmu belum tersimpan. Coba simpan lagi."
"Pastikan format email benar, contoh: nama@gmail.com"
```

### Loading States

Jangan biarkan loading tanpa konteks. Beri tahu user apa yang sedang terjadi.

```tsx
// ❌
"Loading..."
"Please wait..."

// ✅
"Menyimpan undangan..."
"Mengupload foto, sebentar lagi..."
"Mengirim ke {n} tamu..."
```

### Success / Confirmation Messages

Konfirmasi harus konkret, menyebutkan apa yang baru terjadi.

```tsx
// ❌
"Berhasil!"
"Data disimpan."

// ✅
"Undangan dikirim ke 42 tamu. Mereka akan terima link dalam beberapa detik."
"Perubahanmu tersimpan. Tampilannya langsung update di semua perangkat."
```

### Tooltip & Microcopy

Tooltip ada untuk menjelaskan, bukan mengulang label.

```tsx
// ❌
<Tooltip>Nama</Tooltip>

// ✅  
<Tooltip>
  Nama yang akan tampil di header undangan. Bisa nama lengkap atau panggilan.
</Tooltip>
```

---

## Konsistensi Desain Visual

### Hierarki Tipografi

Selalu gunakan hierarki yang konsisten. Jangan skip level heading.

```
H1  — Satu per halaman, headline utama
H2  — Section heading utama
H3  — Sub-section atau card title
H4  — Komponen kecil, sidebar item
body — Konten utama, readable 16px+
small/caption — Helper text, timestamp, metadata
```

### Spacing & Density

Gunakan spacing yang konsisten dengan sistem (Tailwind scale):
- **Tight**: komponen dalam satu card → `gap-2`, `gap-3`
- **Normal**: antar elemen dalam section → `gap-4`, `gap-6`
- **Loose**: antar section besar → `gap-8`, `gap-12`, `gap-16`

Jangan mix `margin` dan `gap` untuk hal yang sama. Pilih satu dan konsisten.

### Warna & Status

Gunakan semantic color, bukan hardcode:
- **Primary** — aksi utama
- **Secondary** — aksi alternatif
- **Destructive** — hapus, batalkan, irreversible
- **Muted** — teks sekunder, placeholder
- **Success** — konfirmasi positif
- **Warning** — perhatian, bukan error
- **Error** — masalah yang perlu tindakan

---

## Anti-Pattern yang HARUS Dihindari

### Copy Anti-Patterns

| Anti-Pattern | Kenapa Buruk | Solusi |
|---|---|---|
| "Please fill in all required fields" | Tidak jelas field mana | Highlight field yang kosong dengan pesan spesifik |
| "Are you sure you want to delete?" | Tidak menyebut apa yang dihapus | "Hapus undangan 'Pernikahan Budi & Sari'? Tidak bisa dibatalkan." |
| "This feature is coming soon" | Frustasi tanpa konteks | "Fitur ini sedang kami bangun. Daftar notifikasi?" |
| Teks placeholder sebagai label | Hilang saat diketik | Selalu gunakan label yang visible |
| Kalimat pasif berlebihan | Terasa dingin | Gunakan aktif, subjek jelas |

### Design Anti-Patterns

- Jangan gunakan lebih dari 2 font weight berbeda dalam satu komponen
- Jangan center-align paragraf panjang (>2 baris)
- Jangan gunakan warna sebagai satu-satunya sinyal (pikirkan aksesibilitas)
- Jangan buat tombol yang terlalu kecil untuk touch target (<44px)
- Jangan stack terlalu banyak CTA — satu primary, maksimal satu secondary

---

## Checklist Sebelum Output

Sebelum menyelesaikan kode atau copy, pastikan:

**Copy:**
- [ ] Setiap teks UI punya konteks dan tujuan yang jelas
- [ ] Tidak ada placeholder generik ("Lorem ipsum", "Data", "Item")
- [ ] Error messages menyebut masalah dan solusi
- [ ] CTA menyebut aksi yang konkret, bukan "Submit" atau "Click"
- [ ] Empty state memiliki headline + body + CTA
- [ ] Loading state menjelaskan apa yang sedang diproses

**Design:**
- [ ] Hierarki heading digunakan dengan benar (tidak skip level)
- [ ] Spacing konsisten dengan skala yang digunakan
- [ ] Warna semantic, bukan hardcoded arbitrary
- [ ] Komponen responsive dan accessible
- [ ] Touch targets cukup besar untuk mobile

---

## Referensi Tambahan

Untuk konteks lebih dalam, baca file di `references/`:
- `voice-and-tone.md` — panduan tone per mood/situasi user
- `component-copy-patterns.md` — template copy untuk komponen umum

---

## Cara Menggunakan Skill Ini

1. **Sebelum nulis UI**: tentukan dulu konteks user, tone yang tepat, dan satu
   pesan utama per section.
2. **Saat nulis kode**: pastikan setiap string yang user-facing dipikirkan,
   bukan diisi default/placeholder.
3. **Saat review**: gunakan checklist di atas sebelum menyatakan selesai.
4. **Saat ada copy generik**: tanya konteks produknya, lalu sharpen copy-nya.
