---
name: starter-style-guide
description: Bu template'in tasarim sistemi referansi — renk (colorScheme + AppThemeColors semantic token'lari), tipografi (textTheme slotlari, Poppins/Inter), spacing/radius/golge/sure token'lari (AppPaddings, AppRadius, AppShadows, AppDurations, AppIconSizes), paylasilan widget katalogu (AppPrimaryButton, dort-durum widget'lari, AppTextField, sheet'ler), 8 varyantli light/dark tema ve easy_localization. Kullanici UI yazarken/duzenlerken "renkleri projeye gore kullan", "bu butonu projeye gore yaz", "hangi spacing/radius", "tasarim sistemine uydur", "style guide", "tema token'lari" dediginde kullan.
---

# Tasarim Sistemi Referansi

UI'yi bu template'in kurallariyla yazmak icin hizli bakis. Baglayici kurallar
[widget_and_theme.md](../../../doc/guides/widget_and_theme.md) ve
[design_tokens.md](../../../doc/guides/design_tokens.md)'de — bu skill onlarin
calisma anindaki checklist'i.

**Uygula, icat etme.** Eksik bir token varsa cagri yerine deger yazma; token
dosyasina ekle.

## Ne zaman calistir
- Herhangi bir ekran/widget yazarken veya restyle ederken.
- "hangi renk/spacing/radius", "tasarim sistemine uydur".

## Ne zaman calistirma
- Butun feature iskelesi (cubit+state+view) → `starter-feature`.
- Yazilmis kodu denetleme → `starter-review`.

## Renk
- Once `Theme.of(context).colorScheme.*` — `primary`, `surface`, `onSurface`,
  `onSurfaceVariant`, `error`, `outline`...
- Varyanttan bagimsiz semantic tonlar: `context.appColors.*`
  ([app_theme_colors.dart](../../../lib/product/theme/app_theme_colors.dart)).
- ❌ View icinde `Color(0x...)` / `Colors.<ad>`. Yeni renk gerekiyorsa
  `AppThemeColors`'a ekle — hem light hem dark degeriyle.
- Tema 8 varyant × light/dark uretir; sabit renk yazmak varyant sistemini kirar.

## Tipografi
- `Theme.of(context).textTheme.*`. Slot tablosu:
  [widget_and_theme.md](../../../doc/guides/widget_and_theme.md).
- Ozellestirme `copyWith` ile. ❌ Inline `TextStyle(fontSize: ...)`.
- Fontlar tema uzerinden gelir (Poppins: display/headline, Inter: title/label/body).
  ❌ Hardcoded `fontFamily` — `FontFamily.*` uretilmis sabitleri var.

## Spacing / radius / golge / sure
| Ihtiyac | Token |
|---|---|
| Padding, bosluk | `AppPaddings.*` |
| Kose yaricapi | `AppRadius.*` |
| Golge | `AppShadows.card(context)` gibi tema duyarli yardimcilar |
| Animasyon suresi | `AppDurations.*` |
| Ikon boyutu | `AppIconSizes.*` |
| Responsive olcek | `context.r(...)` / `context.rf(...)`, genislik esigi `context.isWide` |

❌ Ham `EdgeInsets.all(16)`, `SizedBox(height: 24)`, `BorderRadius.circular(12)`,
`Duration(milliseconds: 300)`.
`Column`/`Row` icinde bosluk icin `spacing:` parametresini kullan.

## Bilesenler — once katalogu kontrol et
[lib/product/widget/](../../../lib/product/widget/):
- Buton: `AppPrimaryButton` / `AppSecondaryButton` / `AppTextButton` (haptic dahil).
- Ekran durumlari: `AppLoadingView`, `AppErrorView`, `AppEmptyView`, `AppStateView`.
- Form: `AppTextField` + `AppValidator` hiyerarsisi.
- Sheet/dialog: `context.showAppBottomSheet`, `context.showConfirmDialog`,
  `AppSelectSheet`, `AppErrorSheet`.
- Geri bildirim: `context.showSuccessSnack/showErrorSnack/showInfoSnack`.
- Kabuk: `AppScaffold`, `KeyboardDismisser`, `AppSemantics`.

Katalogda varsa yeniden yazma. Yoksa: uygulama geneli mi → `product/widget/`,
feature'a mi ozel → `feature/<ad>/widget/`.

## Metin
Kullaniciya gorunen her metin `LocaleKeys.*.tr()`; anahtar hem `tr.json` hem
`en.json`'a eklenir, sonra `./script/lang.sh`.
Ceviriye girmeyen sabitler (URL, teknik string) `AppString`.

## Yeni ekran checklist
- [ ] Renk yalnizca `colorScheme` / `context.appColors`
- [ ] Metin stili yalnizca `textTheme` (+`copyWith`)
- [ ] Padding/radius/sure/ikon token'dan
- [ ] Butonlar ve durum widget'lari katalogdan
- [ ] Tum metinler `LocaleKeys`
- [ ] Asset'ler `Assets.*`
- [ ] Light **ve** dark'ta okunur
- [ ] `context.isWide` ile genis ekran kontrolu
- [ ] Dort durum ele alindi (loading/error/empty/data)

## Yapma → Yap
| Yapma | Yap |
|---|---|
| `Colors.blue` / `Color(0xFF...)` | `colorScheme.primary` / `context.appColors.*` |
| `TextStyle(fontSize: 24)` | `textTheme.headlineSmall` |
| `EdgeInsets.all(24)` | `AppPaddings.allXxl` |
| `SizedBox(height: 16)` | `Column(spacing: AppPaddings.l, ...)` |
| `BorderRadius.circular(12)` | `AppRadius.md` |
| `Duration(milliseconds: 300)` | `AppDurations.short` |
| `Text('Kaydet')` | `Text(LocaleKeys.general_save.tr())` |
| `Image.asset('assets/image/x.png')` | `Assets.image.x.image()` |
| `CircularProgressIndicator()` | `AppLoadingView()` |

Bu skill referanstir. Gercek iskele kurmak icin `starter-feature`.
