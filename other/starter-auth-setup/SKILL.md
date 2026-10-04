---
name: starter-auth-setup
description: Bu template'te Firebase'i ve giris yontemlerini kurar. Kullaniciya hangi saglayicilari istedigini (Google, Apple, e-posta dogrulama, misafir gezinme) sorar, AppConfig bayraklarini cevirir ve o saglayicilarin gercekten calismasi icin Firebase Console / Apple Developer / Play Console / Xcode tarafinda yapmasi gerekenleri adim adim listeler. Kullanici "girisi kur", "Firebase'i bagla", "Google girisi ekle", "Apple ile giris ekle", "auth kurulumu", "login sistemini aktif et", "set up authentication" dediginde kullan. Repoyu klonlayip ilk kez calistiran icin giris noktasidir.
---

# Giris Kurulumu

Kod zaten hazir — servisler, ekranlar, route guard ve hata cevirileri yerinde.
Bu skill kod yazmaz; **soru sorar, bayrak cevirir, manuel adimlari verir**.

Tam yonerge: [doc/guides/auth_setup.md](../../../doc/guides/auth_setup.md).
Once onu oku ve adimlarini sirayla uygula. Burada kural tekrar edilmez.

## Akis

1. **Durumu oku** — `AppConfig` bayraklari + `firebase_options.dart` placeholder mi?
   Kullaniciya zaten yaptigi seyi sorma.
2. **Sor** — Firebase kurulu mu / hangi saglayicilar / e-posta dogrulama /
   misafir gezinme. Hepsini tek seferde sor.
3. **Cevir** — yalnizca `lib/product/const/app_config.dart` (ve gerekirse
   `AppRouter.protectedPrefixes`). **Baska dosyaya dokunma.**
4. **Dogrula** — `./script/verify.sh`.
5. **Manuel adimlari ver** — yalnizca acilan saglayicilarin blogunu.

## Sert kurallar

- Bayrak disinda kod degistirme. Ekranlar ve guard bayraklara gore kendini kurar.
- `flutterfire configure` ve `firebase login` **sen calistirma** — interaktif
  giris ister, kullaniciya ver.
- Google acilirsa Apple'in App Store 4.8 zorunlulugunu **mutlaka** soyle.
- `googleServerClientId` bos birakilirsa giris sessizce kirilir — bunu bilgi
  olarak degil, engelleyici olarak bildir.
- Kullanicinin Console/Xcode/keystore tarafinda yapmasi gerekenleri atlamadan,
  sirali ve kopyalanabilir sekilde ver.

## Cikti

Tek ekranda: acilan bayraklar, kullanicinin yapmasi gereken manuel adimlar,
ertelenen/atlanan seyler. Baska bir sey yazma.
