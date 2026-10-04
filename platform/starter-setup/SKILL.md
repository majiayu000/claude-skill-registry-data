---
name: starter-setup
description: Bu template'i klonladiktan sonraki tum kurulumu yurutur — bagimliliklar ve codegen, projeyi kendine uyarlama, Firebase, giris yontemleri (Google/Apple/e-posta dogrulama/misafir gezinme), zorunlu guncelleme (Remote Config), odeme ve abonelik (RevenueCat), Android release imzalama (keystore), native splash ve store URL'leri. Kullaniciya ne istedigini sorar, AppConfig bayraklarini cevirir ve Firebase Console / Apple Developer / Play Console / RevenueCat tarafinda yapmasi gerekenleri sirayla listeler. Kullanici "kurulumu yap", "kurulumu baslat", "klonladim ne yapmaliyim", "Firebase'i bagla", "odeme ekle", "keystore olustur", "release imzasi kur", "set up the project" dediginde kullan. Repoyu ilk kez calistiran icin GIRIS NOKTASIDIR.
---

# Kurulum

Kod hazir — servisler, ekranlar, guard'lar ve no-op implementasyonlar yerinde.
Bu skill **kod yazmaz**: soru sorar, bayrak cevirir, manuel adimlari verir.

Tam yonerge ve sira: [doc/setup.md](../../../doc/setup.md) (kok dizin, kurulumun giris noktasi).
Once onu oku, sonra kullanicinin ihtiyacina gore ilgili adim dosyasini yurut.
Kural orada tanimli, burada tekrar edilmez.

## Adim dosyalari

| Adim | Dosya |
|---|---|
| Klon sonrasi temizlik + codegen | `doc/guides/setup_after_clone.md` |
| Projeyi kendine uyarlama | `doc/guides/customization.md` |
| Firebase + giris | `doc/guides/auth_setup.md` |
| Zorunlu guncelleme | `doc/guides/version_control_setup.md` |
| Odeme / abonelik | `doc/guides/payment_setup.md` |
| Android imzalama | `doc/guides/android_signing.md` |
| Native splash | `doc/guides/native_splash.md` |
| Store URL / iletisim | `doc/guides/settings_and_urls.md` |

## Yurutme

1. **Durumu oku** — `AppConfig` bayraklari, `firebase_options.dart` placeholder
   mi, `android/key.properties` var mi, `.dart_tool` var mi. Zaten yapilani sorma.
2. **Kullanicinin nereden baslamak istedigini belirle.** "Kurulumu yap" gibi
   genel bir istekte sirayi SETUP.md'den takip et; belirli bir konu soylediyse
   dogrudan o adima git.
3. **Sorulari adim basina tek seferde sor.**
4. **Yalnizca bayrak/yapilandirma degistir.**
5. **Her adimdan sonra** `./script/verify.sh`.
6. **Manuel adimlari eksiksiz ver**, sonra ozetle.

## Sert kurallar

- `flutterfire configure`, `firebase login`, `keytool -genkey` gibi
  **interaktif komutlari sen calistirma** — kullaniciya ver.
- **Sir isteme, saklama, yazma.** Keystore parolasi ve benzeri alanlari bos
  birak; kullanici doldurur.
- Keystore repo **disinda** durur.
- Google girisi acilirsa Apple'in App Store 4.8 zorunlulugunu **mutlaka** soyle.
- Odeme acilirsa iOS'ta "Satin alimlari geri yukle" butonunun zorunlu
  oldugunu (App Store 3.1.1) soyle.
- Bir ozelligin Console tarafindaki adimini atlarsan ozellik **sessizce**
  calismaz — en pahali hata sinifi budur, atlama.

## Cikti

Tek ekranda: acilan bayraklar, kullanicinin yapmasi gereken manuel adimlar
(sirali, kopyalanabilir), ertelenen adimlar. Baska bir sey yazma.
