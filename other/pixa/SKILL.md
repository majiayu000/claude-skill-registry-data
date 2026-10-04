---
name: pixa
description: "Pixa.com (eski Pixelcut) — Claude'a MCP-native baglanan yaratici AI araclari. Arka plan kaldir, gorsel olustur, kalite iyilestir, video olustur, nesne sil. API anahtari gerekmez."
argument-hint: "bg-remove | generate | enhance | video | delete-object | library <prompt>"
version: 1.0.0
license: MIT
---

# Pixa — Claude MCP-Native Yaratıcı Araçlar

Pixa, Claude'a MCP uzerinden baglanan yaratici arac seti. API anahtari gerekmez, tek yapilandirma.

## When to Activate

TRIGGER when the user:
- Arka plan kaldirmak istediginde ("bg kaldir", "arka plan temizle")
- Gorsel olusturmak istediginde ("gorsel olustur", "reklam gorseli")
- Gorsel kalite artirmak istediginde ("iyilestir", "kalite yukselt")
- Video olusturmak istediginde ("video olustur")
- Gorseldeki nesneyi silmek istediginde ("nesne sil", "silgi")
- Varlik kutuphanesini yonetmek istediginde

## MCP Kurulum

### Claude Desktop / VS Code
```
Ayrlar → Baglayicilar → Ozel Baglayici Ekle
URL: https://mcp.pixa.com/mcp
```

### Manuel (.mcp.json)
```json
{
  "mcpServers": {
    "pixa": {
      "command": "npx",
      "args": ["pixa-mcp@latest", "init"]
    }
  }
}
```

### Headless/CI/CD
```bash
export PIXA_API_KEY=your_key
npx pixa-mcp@latest init
```

## Mevcut Araçlar (6)

### 1. Arka Plan Kaldir
Gorsel arka planlarini temizle. Urun fotografi icin ideal.

```
Kullanim: "Bu urun fotorafinin ark planini kaldir"
Sonuc: transparent.png (2048x2048)
```

**Reklam kullanimi:** Urun fotograflari icin beyaz/transparent arka plan olusturma.

### 2. Gorsel Olustur
Metinden gorsel uret. Urun reklamlari, yasam tarzi gorselleri.

```
Kullanim: "Kumlu plajda gunes kreminiz icin reklam olustur"
Sonuc: sunscreen_beach_ad.png (1024x1024)
```

**Reklam kullanimi:** Hizli reklam gorseli uretimi, A/B test varyasyonlari.

### 3. Kalite Iyilestir
Gorselleri 2-4 kat buyut, kalite kaybi olmadan.

```
Kullanim: "Bu gorseli 4x cozunurluge iyilestir"
Sonuc: hero_4x.png (4096x4096)
```

**Reklam kullanimi:** Dusuk cozunurluklu gorselleri basin/billboard kalitesine cikarma.

### 4. Video Olustur
Metinden veya gorselden video olustur.

```
Kullanim: "Bu urun gorselinden 5 saniyelik video olustur"
Sonuc: product_video.mp4
```

**Reklam kullanimi:** Urun gorsellerini sosyal medya videolarina donusturme.

### 5. Nesne Sil
Gorsellerden istenmeyen nesneleri kaldir.

```
Kullanim: "Bu gorseldeki logoyu sil"
Sonuc: cleaned_image.png
```

**Reklam kullanimi:** Stok gorselleri temizleme, rakip logolari kaldirma.

### 6. Varlik Kutuphanesi
Olusturulan tum varliklari yonet.

```
Kullanim: "Varlik kutuphanemdeki urun fotograflarini listele"
```

## Reklam Ajansi Pipeline

### Urun Fotografi → Reklam
```
1. "Bu urun fotorafinin ark planini kaldir" → transparent.png
2. "Beyaz arka plan ekle, profesyonel urun cekimi" → product_clean.png
3. "Kaliteyi 4x iyilestir" → product_4x.png
4. "Bu urun icin Instagram reklam gorseli olustur (1:1)" → ad_1x1.png
```

### Toplu Islem
```
1. 50 urun fotorafinin arka planlarini kaldir
2. Her birini 2x iyilestir
3. Her biri icin 3 reklam varyasyonu olustur
= 150 reklam gorseli
```

### Claude Kod ile Otomasyon
```bash
$ claude "catalog.json'daki her urun icin kahraman gorselleri olustur"
```

## Kredi Sistemi

- Islemler kredi gerektirir (turune gore)
- Pro aboneler aylik kredi alir
- Claude uzerinden ek ucret yok — ayni kredi sistemi
- Bedava: sinirli kullanim

## Pixa vs Krea vs Kie

| Ozellik | Pixa | Krea | Kie |
|---------|------|------|-----|
| Entegrasyon | MCP-native | API | API |
| API Anahtari | Hayir | Evet | Evet |
| Gorsel Modeli | Dahili | 64+ secenek | Multi-provider |
| Video | Evet | Evet (7 model) | Evet (Kling, Sora) |
| Arka Plan Kaldir | Evet | Hayir | Hayir |
| Upscale | 2-4x | 22K (Topaz) | - |
| LoRA Egitim | Hayir | Evet | Hayir |
| Maliyet | Kredi sistemi | CU sistemi | Pay-per-use |
| En Iyi | Hizli duzenleme | Profesyonel uretim | Ucuz API erisim |

**Strateji:**
- Hizli duzenleme (bg kaldir, nesne sil) → **Pixa**
- Profesyonel uretim (marka LoRA, 4K) → **Krea**
- Ucuz batch uretim (API pipeline) → **Kie**

## Error Handling

- MCP baglantisi basarisiz → `npx pixa-mcp@latest init` tekrar calistir
- Kredi yetersiz → kullaniciyi Pixa Pro'ya yonlendir
- Gorsel olusturma basarisiz → promptu basitlestir, tekrar dene
- Video timeout → daha kisa video iste (5s)

## Best Practices

### DO
- Hizli duzenleme isleri icin Pixa kullan (MCP-native, hizli)
- Urun fotograflari icin once arka plan kaldir, sonra enhance
- Toplu islemde Cowork eklentileri kullan
- Claude Kod ile otomatik pipeline kur

### DON'T
- Pixa'yi profesyonel 4K uretim icin kullanma (Krea daha uygun)
- API anahtari olusturma (MCP zaten yonetiyor)
- LoRA egitim bekleme (Pixa'da yok)
