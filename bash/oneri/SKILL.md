---
name: oneri
description: Günlük video önerisi üretir. Trend olan denenebilir yapay zekâ araçlarını, modelleri, GitHub repolarını ve demoları (GitHub Trending, Hugging Face, Show HN, Product Hunt, resmi ürün blogları) damıtır, kısaca araştırır, "izleyici bugün deneyebilir mi, ekranda vay dedirtir mi" ölçüsüyle puanlar ve en iyi 8 konuyu icerik/oneriler/<tarih>.json dosyasına yazıp main'e push'lar (Telegram'a bot.yml gönderir). Her sabah bulut rutini çalıştırır; kullanıcı "bugünün önerilerini hazırla / damıt" derse elle de kullanılır.
---

# Günlük öneri (damıtma)

Kanalın vaadi: "Bu hesabı takip edersem, işime yarayan ya da merak ettiğim yeni yapay zekâ araçlarını ilk ben görürüm ve nasıl kullanıldığını görürüm." Tuna konuları kamerada **dener** ("hadi deneyelim"). Bu yüzden öneri, haber değil **denenebilir şey**dir: yeni bir araç, model, demo, GitHub reposu ya da ürüne gelen yeni özellik.

## Kapsam

- **Dene (ana tür, en az 6 öneri):** bugün denenebilen araç, model, Hugging Face Space, GitHub reposu, uygulama, ürün özelliği.
- **Gündem (en fazla 2 öneri):** sadece ekranda gösterilecek güçlü bir görüntüsü olan (demo videosu, tuhaf ya da eğlenceli bir sonuç) ve izleyicinin kullandığı araçları doğrudan etkileyen haber. Örnek: "ChatGPT'nin yeni modeli yarın geliyor, şu özellik değişiyor".
- **Hariç:** siyaset, yatırım turu, şirket anlaşması, dava, düzenleme, CEO açıklaması, borsa. Ayrıca NSFW, "uncensored", korsan, dolandırıcılık riski taşıyan ya da kişisel veri toplayan şüpheli araçlar.

## Adımlar

1. `git pull --rebase -q`. Tarih (Türkiye saati): `TZ=Europe/Istanbul date +%F`. `icerik/oneriler/<tarih>.json` zaten varsa dur.
2. `python scripts/adaylar.py 26` çalıştır. Çıktıda önce TRENDLER (GitHub Trending, HF Space/model, Show HN, Product Hunt), sonra HABERLER gelir. `data/trendler.json` zaman damgası 12 saatten eskiyse ve ağ erişimin varsa önce `python scripts/trendler.py` çalıştır.
3. Tekrarı önle: son 7 günün `icerik/oneriler/*.json` dosyalarını ve `icerik/liste.json` dosyasını oku. Önerilmiş aracı, büyük bir yeni sürüm yoksa yeniden önerme. Trend listeleri günlerce aynı kalır; buna dikkat et.
4. Ön eleme (~15 aday). Sinyaller: GitHub bugünkü yıldız sayısı, HF trend puanı, Show HN puanı, aynı şeyin birden çok kaynakta geçmesi. Haberlerde bir model/araç adı çok geçiyorsa (yeni çıkmış model) mutlaka aday yap.
5. Hafif araştırma (her aday için 1-2 WebSearch, gerekirse resmi sayfaya WebFetch). Her aday için şu altı soruyu cevapla:
   - Ne bu? Tek cümle, teknik olmayan biri anlasın.
   - Nerede denenir (link)? Ücretsiz mi, hesap ya da bekleme listesi gerekiyor mu?
   - Türkiye'den açılıyor mu, Türkçe çalışıyor mu?
   - Ekranda 10 saniyede gösterilecek "vay" anı ne?
   - Kamerada denenecek 1-2 somut girdi (prompt, dosya, komut) ne?
   - Tuzak var mı: kuyruk/bekleme, ücret, resmi olmayan kopya, gizlilik riski, abartılı iddia?
6. Puanla (1-10):
   - Denenebilirlik (0-3): tarayıcıda/telefonda hesapsız 1 dakikada = 3; hesap ya da ücretsiz deneme = 2; kurulum ya da teknik bilgi = 1; denenemez = 0.
   - Vay anı (0-3): sonuç ekranda ne kadar hızlı ve etkileyici görünüyor (görsel/video üretimi, bir ajanın işi kendi başına bitirmesi, eğlenceli bir tuhaflık)?
   - Fayda ya da merak (0-2): izleyiciye zaman/para kazandırır mı, ya da "bunu herkese göstermeliyim" dedirtir mi?
   - Tazelik (0-1): son 1-3 günde çıktı ya da trend oldu, Türkçe içerikte henüz yok.
   - Türkiye (0-1): Türkiye'den erişilebiliyor, Türkçe çalışıyor.
   - Doğrulanamayan en fazla 5 alır. Ücretli ve deneme sürümü yoksa en fazla 5 alır.
7. En iyi 8'i puan sırasıyla yaz. Çeşitlilik: aynı kategoriden (örneğin görsel üretimi) en fazla 2, teknik (kurulum gerektiren) en fazla 3. Zayıf günde daha az yaz (en az 3) ve nedenini `not` alanına koy.
8. Kaydet ve gönder:
   ```bash
   git add icerik/oneriler && git commit -q -m "oneri <tarih>"
   git push origin HEAD:main || git push origin HEAD:claude/oneri-<tarih>
   ```
   Telegram'a gönderimi GitHub Actions (bot.yml) yapar; sen Telegram'a bir şey gönderme.

## Dosya şeması: `icerik/oneriler/<tarih>.json`

```json
{
  "tarih": "2026-09-25",
  "not": "İsteğe bağlı: gün hakkında tek cümle.",
  "oneriler": [
    {
      "no": 1,
      "tur": "Dene",
      "baslik": "Kısa Türkçe konu başlığı (en fazla 70 karakter)",
      "hook": "Videonun ilk cümlesi (en fazla 12 kelime)",
      "ozet": "Ne bu, ne yapıyor: 2-3 kısa, sade cümle.",
      "demo_ani": "Ekranda 10 saniyede gösterilecek an: tek cümle.",
      "neden": "İzleyici neden izler ve takip eder: tek cümle.",
      "fikir": "Nasıl denenmeli, hangi açı tutar, nelere dikkat: 1-2 cümle.",
      "zorluk": "Herkes",
      "maliyet": "Ücretsiz",
      "puan": 8,
      "dogrulama": "Doğrulandı",
      "dene_url": "https://aracin-denendigi-adres",
      "kaynaklar": ["resmi duyuru ya da repo", "ikinci kaynak"]
    }
  ]
}
```

- `tur`: `Dene` ya da `Gündem`.
- `zorluk`: `Herkes` (tarayıcı/telefon, hesapsız), `Hesap gerekir` ya da `Teknik` (kurulum, komut satırı, GPU).
- `maliyet`: `Ücretsiz`, `Ücretsiz deneme` ya da `Ücretli`.
- `dogrulama`: `Doğrulandı` (resmi sayfa/repo var ve çalışıyor), `Kısmen doğrulandı` ya da `Doğrulanamadı`.
- `dene_url`: Telegram'daki "Dene" butonu olur; aracın doğrudan açıldığı adres. Gündem türünde boş bırakılabilir.
- `no` 1'den başlar ve sıralıdır (Telegram'da "1 3 5" diye seçim bu numaralarla yapılır).

## Yazım kuralları

- Hook: en fazla 12 kelime. Sonucu ya da şaşırtıcı özelliği söyler ("Bu yapay zekâ fotoğrafını 30 saniyede videoya çeviriyor"). "Merhaba", "bugün size" ile başlamaz. Yalan söylemez.
- `fikir` alanı eleştirel görüşündür: gerçekten işe yarıyor mu, hangi demo tutar, kuyrukta beklemek ya da ücret gibi tuzaklar ne. Pohpohlama yok.
- Sade Türkçe; teknik terim gerekirse parantez içinde tek cümleyle açıkla.
- Türkçe karakterler zorunlu (ç, ğ, ı, İ, ö, ş, ü). Uzun çizgi (U+2014) kullanma. Emoji kullanma.
- Uydurma bilgi yok. Kaynakta olmayan rakam, fiyat ya da özellik yazma.
