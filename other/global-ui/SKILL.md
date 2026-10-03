---
name: global-ui
description: Mevcut FişBu mobil projesindeki gerçek tema (light/dark) ve dil durumuna göre kuralları tanımlar; analyst, mobile-dev ve qa tarafından kullanılır.
---

## Durum tespiti (bu skill'in dayandığı gerçek proje incelemesi)
- **i18n**: `mobile/` projesinde henüz bir çeviri altyapısı YOK — ARB dosyası, `l10n.yaml`, `easy_localization`/`flutter_localizations` kurulumu bulunmuyor. Tüm kullanıcıya görünen metinler doğrudan Türkçe olarak widget kodu içine yazılmış. `intl` paketi mevcut ama sadece tarih/sayı/para biçimlendirmesi (`DateFormat`, `NumberFormat`) için kullanılıyor, çeviri anahtarı için değil.
- **Tema**: `lib/core/theme/app_theme.dart` (`AppTheme.light` / `AppTheme.dark`) ve `AppColors` (light/dark renk çiftleri) üzerinden merkezi bir tema sistemi var. Aktif mod bir `ThemeController` (ValueListenable) ile tutulur, `MaterialApp` bunu `themeMode` olarak dinler. Bu altyapı olgun ve çalışıyor — kural burada "kur" değil "bu deseni koru ve genişlet".

## i18n Kuralı — kurulana kadar geçerli
Proje henüz çok dilli değil. Bu nedenle:
- Yeni metinler, projenin geri kalanıyla tutarlı şekilde DOĞRUDAN Türkçe yazılır — çeviri anahtarı (`t('namespace.key')`) icat edilmez, çünkü onu okuyacak bir çeviri altyapısı yok.
- Analyst, bir story'nin "Global Etki" değerlendirmesinde i18n için artık "hangi anahtar eklenecek" değil, sadece **metnin son kullanıcıya Türkçe ve anlaşılır olup olmadığını** kontrol eder.
- Eğer bir story açıkça çok dilli destek (i18n altyapısı kurulması) istiyorsa, bu mimari bir karardır — analyst bunu story'ye not düşer, PDM `architect`'i çağırır; mobile-dev kendi kararıyla ARB/çeviri sistemi kurmaya girişmez.
- Bu bölüm, proje çok dilli hale geldiğinde (ADR ile karar verilip altyapı kurulduğunda) güncellenecek; o zamana kadar "her metin bir çeviri anahtarından okunur" kuralı bu projede AKTİF DEĞİLDİR.

## Tema Kuralı — mevcut deseni koru
- Renkler asla widget içine sabit (`Color(0xFF...)`, `Colors.grey` gibi) yazılmaz. Her renk `AppColors` sınıfındaki bir sabit üzerinden kullanılır; `AppColors`'da karşılığı olmayan bir renk gerekiyorsa önce oraya hem light hem dark değeriyle eklenir.
- Yeni bir widget, `Theme.of(context).colorScheme` veya `AppColors.<isim>` / `AppColors.<isim>Dark` çiftini `isDark` durumuna göre okur — `ThemeController`'ın tuttuğu mod bilgisini görmezden gelip sabit bir renk şeması varsaymaz.
- `fl_chart` ile çizilen grafiklerin renkleri de bu kuraldan muaf değildir — grafik renkleri `AppColors`'tan gelir, light/dark geçişinde grafik de uyumlu değişir.

## Global Etki Kontrolü
Yeni görsel bileşen içeren her story, hem light hem dark temada test edilir (dil artık tek olduğu için bu boyut düşer — bkz. i18n Kuralı). Sadece tek temada test etmek, diğer tarafta gizli kalan hataları (düşük kontrast, dark modda görünmeyen sınır/ikon gibi) kaçırabilir.

## Global Etki Değerlendirmesi (Analyst için)
Her story için şu konular değerlendirilir:
- **Metin**: yeni kullanıcıya görünen metin var mı, Türkçe ve anlaşılır mı (çeviri anahtarı DEĞİL — bkz. i18n Kuralı).
- **Tema**: yeni görsel/bileşen light-dark'ta kontrol edilecek mi, `AppColors` üzerinden mi renklendirilmiş.
- **Locale**: tarih/para/sayı gösterimi `intl` (`DateFormat`/`NumberFormat`) ile mi yapılıyor, elle string formatlama (`toString()` üzerinden tarih birleştirme gibi) kullanılmıyor mu.
