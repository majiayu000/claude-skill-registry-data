---
name: video
description: Telegram'da listeye alınmış konular (icerik/liste.json, durum "secildi") için derin araştırma yapar ve dikey "hadi deneyelim" video metni (45-70 sn) ile çekim planını yazar. Metni icerik/videolar/ altına kaydeder, durumu "hazir" yapar ve push'lar; metin Telegram'a bot.yml ile gider. Kullanıcı "listeyi hazırla", "videoları hazırla", "metinleri yaz" dediğinde kullanılır.
---

# Video metni hazırlama

Tuna yeni yapay zekâ araçlarını kamerada dener ve anlatır. Kurgu (edit) yapacak vakti yok. Bu yüzden çekim, üç düz parçadan oluşur: yüz kamerası (giriş), ekran kaydı (deneme), yüz kamerası (yorum ve kapanış). Metin tek başına izletmeli; çekim planı da hazırlığı sıfıra indirmeli.

## Adımlar

1. Telegram'daki son seçimleri içeri al (bot.yml normalde 15-60 dakikada bir çalışır, burada hemen çalıştırıyoruz):
   - `gh workflow run bot.yml`
   - Birkaç saniye sonra `gh run list --workflow bot.yml --event workflow_dispatch --limit 1 --json databaseId,status` ile yeni çalışmayı bul, `gh run watch <id> --exit-status` ile bitmesini bekle.
   - `git pull --rebase -q`
   `gh` çalışmazsa sadece `git pull --rebase -q` yap ve devam et.
2. `icerik/liste.json` içinde `durum: "secildi"` olanları al. Kullanıcı belirli bir konu söylediyse sadece onu. Hiç yoksa bunu söyle ve dur.
   - Test kapısı: her konu için `lab/` altında karşılık gelen klasörü bul. `durum: test-edildi` değilse ya da klasör yoksa metni yazma; kullanıcıya "önce test edilmeli" de ve konuyu atla. Metindeki SONUÇ bölümü `lab/<slug>/README.md` test notlarındaki gerçek sonuca dayanır.
3. Her konu için derin araştırma (birden çok konu varsa paralel alt ajanlarla):
   - Resmi sayfa, repo ya da duyuru ve en az bir bağımsız kaynak.
   - Erişim: link, ücret, hesap/bekleme listesi, Türkiye'den açılıyor mu, Türkçe çalışıyor mu, kuyruk/bekleme süresi.
   - Deneme senaryosu: adım adım ne tıklanır, ne yazılır; beklenen sonuç ve ne kadar sürdüğü.
   - Sınırlar: neyi yapamıyor, nerede hata yapıyor, gizlilik ya da güvenlik riski, resmi olmayan kopya mı.
   - Mümkünse aracı kendin aç (WebFetch) ve sayfanın gerçekten çalıştığını doğrula.
   - Her iddiayı etiketle: Doğrulandı / İddia (tek kaynak) / Tahmin. Uydurma özellik ya da rakam yok.
4. Metni `metin` skill'inin adımlarıyla (3 kanca, psikoloji rehberi, `scripts/metin_kontrol.py --plan` ile en az 85 puan) aşağıdaki şablonla yaz: `icerik/videolar/<id>-<kisa-slug>.md` (örn. `2026-09-25-3-vesikalik-foto.md`).
5. `icerik/liste.json` içinde o kaydı güncelle: `"durum": "hazir"`, `"dosya": "<yol>"`, `"hazirlandi": "<UTC zaman>"`. `bildirildi` alanına dokunma.
6. Gönder:
   ```bash
   git add icerik && git commit -q -m "video: <kısa başlık>" && git pull --rebase -q && git push
   ```
   Push'tan sonra bot.yml çekim planını ve metni Telegram'a "Çektim" butonuyla yollar.
7. Kullanıcıya her video için tek satır: başlık, hook, dosya linki.

## Metin kuralları (dikey, 30-45 sn)

Anlatım dili, kanca kalıpları ve kapanış `docs/anlatim-dili.md` dosyasından gelir; önce onu oku, kalıp uydurma. Bölümler o dosyadaki iskelete denk düşer: HOOK = kanca, NE BU = bağlam + isim, DENEYELİM = geçiş + adımlar, SONUÇ = kazanç, KAPANIŞ = yorum-kelime CTA'sı.

- Toplam 80-110 kelime (saniyede ~2,8 kelime).
- HOOK (0-4 sn): tek cümle, en fazla 12 kelime. Sonucu söyle ("Bu site selfie'ni 20 saniyede vesikalığa çeviriyor"). "Merhaba", "bugün size" yok.
- NE BU (3-8 sn): tek cümle. Kim yaptı, ne işe yarıyor.
- ODAK: konu içerik değil, izleyicinin bu teknoloji/repoyla artık ne yapabildiği ve kazancı. Kaynak videodaki proje yalnız bir örnek; onun içeriğini anlatma (`docs/anlatim-dili.md` Odak).
- DENEYELİM (8-40 sn, ekran kaydı): her adım için bir kısa cümle. İzleyicinin kendisinin ne yapacağını duysun; örnek projenin iç işleyişini değil.
- SONUÇ (40-50 sn): metin çekimden önce yazılır, sonucu bilemez. Bu yüzden iki seçenek yaz: "Çalıştıysa: ..." ve "Çalışmadıysa: ...". Tuna gördüğüne uyanı okur. Yorum dürüst olsun; eksikleri söyle.
- NASIL DENERSİN (50-58 sn): link nerede, ücretsiz mi, hesap gerekiyor mu. Tek cümle.
- KAPANIŞ: iki cümle, sabit kalıp: "<ne alacağı> istiyorsan yorumlara <TEK KELİME> yaz." + "Bütün detaylarını seninle paylaşmış olayım."
- Teleprompter için her satır bir nefes: satır başına en fazla 12 kelime.
- Konuşma dili, kısa cümle. Teknik terim varsa günlük hayattan benzetmeyle anlat.
- Türkçe karakterler zorunlu. Uzun çizgi (U+2014) yok. Emoji yok.

## Şablon

```markdown
# <Video başlığı>

| Alan | Değer |
|---|---|
| Liste no | <id> |
| Hedef süre | <sn> sn (~<kelime> kelime) |
| Kapak yazısı | <3-5 kelime> |
| Denenecek adres | <URL> |
| Erişim | <Ücretsiz / hesap gerekir / Türkiye'den açılıyor mu> |

## Çekim planı

**Çekimden önce**
- <hesap aç, sayfanın açıldığını ve kuyruk olmadığını kontrol et, test dosyasını hazırla>

**Kamerada yazılacaklar (kopyala-yapıştır)**
- <prompt, komut ya da girdi>

**Çekim sırası**
1. Yüz kamerası: HOOK ve NE BU
2. Ekran kaydı: DENEYELİM adımları
3. Yüz kamerası: SONUÇ, NASIL DENERSİN, KAPANIŞ

Kurguyu edit.py yapar: cümleler arasında rahatça dur, sessizlikler kesilir. Yanlış okursan yarım bırakma, 1 saniye sus ve cümleyi baştan söyle. Klipleri `yerel/ham/<id>/1-yuz.mp4`, `2-ekran.mp4`, `3-yuz.mp4` adıyla koy ve "edit et" de.

**Plan B:** <site açılmaz ya da kuyruk uzarsa ne yapılır>

## Okunacak metin

**[HOOK · 0-3 sn]**
<satır>

**[NE BU · 3-8 sn]**
<satır>

**[DENEYELİM · ekran kaydı]**
<satır>
<satır>
<satır>

**[SONUÇ]**
Çalıştıysa: <satır>
Çalışmadıysa: <satır>

**[NASIL DENERSİN]**
<satır>

**[KAPANIŞ]**
<satır>

## Paylaşım metni
- Başlık (en fazla 60 karakter): ...
- Açıklama: 2 cümle + denenecek link.
- Etiketler: #yapayzeka #teknoloji ...

## Doğrulama ve kaynaklar
- Doğrulandı: ...
- İddia / dikkat: ...
- Kaynaklar: [ad](url), [ad](url)
```

"## Çekim planı" ve "## Okunacak metin" başlıklarını değiştirme: bot Telegram'a bu iki bölümü gönderir.

Gündem türü konularda (deneme yoksa) "Çekim planı"nda ekran kaydı yerine yeşil ekran kullan: haberin ekran görüntüsü arkada, Tuna önde; DENEYELİM bölümünün adı ÖZ olur.
