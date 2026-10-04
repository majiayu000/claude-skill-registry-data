---
name: starter-feature
description: Bu Flutter template'inde uctan uca yeni feature iskelesi kurar — lib/feature/<ad>/ klasor yapisi, Freezed state + Cubit, StatelessWidget ya da StatefulWidget+ViewModel view, BlocProvider yerlesimi (global state_initialize mi lokal mi), TypedGoRoute, LocaleKeys cevirileri, AppPaddings/textTheme/colorScheme token'lari ve zorunlu <feature>.md modul dokumani. Kullanici "yeni feature ekleyelim", "su sayfayi projeye gore yaz", "cubit + state + view kur", "feature iskeleti cikar", "scaffold a feature" dediginde kullan.
---

# Feature Iskelesi

Bu depoda bir feature'i bastan sona kurma is akisi. Butun kurallar
[doc/guides/AGENTS.md](../../../doc/guides/AGENTS.md) ve altindaki rehberlerde tanimli — bu skill
onlari **tekrar etmez, uygular**. Karar gerektiren her adimda ilgili rehberi oku.

Bu skill *kural uygulayicidir*, kesif araci degil. Kullanici "X nedir" diye
soruyorsa ilgili doc dosyasina yonlendir; gercekten yazilacak/refactor edilecek kod
varsa calistir.

## Ne zaman calistir

- `lib/feature/<ad>/` altinda yeni feature.
- Mevcut bir feature'i konvansiyona uydurma.
- "cubit + state + view + (servis) kur".

## Ne zaman calistirma

- Yalnizca token/stil sorusu → `starter-style-guide`.
- Yazilmis kodu denetleme → `starter-review`.
- Tek satirlik bug fix → dosyayi dogrudan duzenle, iskele kurma.

## Baslamadan sor (eksikse, bir kez)

1. **Feature adi** (snake_case).
2. **State kapsami** — app geneli mi (`product/state/` + global provider) yoksa tek
   ekrana mi ait (feature `state/` + view icinde lokal `BlocProvider`)?
   Karar tablosu: [state_management.md](../../../doc/guides/state_management.md).
3. **View tipi** — controller/lifecycle gerekiyor mu?
   Karar tablosu: [view_rules.md](../../../doc/guides/view_rules.md).
4. **Route gerekiyor mu**, gerekiyorsa hangi transition?

Kullanici bunlari zaten yazdiysa tekrar sorma.

## Asamalar (her asamadan sonra dur)

### 1 — Plan
- 4 girdiyi netlestir.
- Klasor yapisini [folder_structure.md](../../../doc/guides/folder_structure.md)'e gore ciz.
- `lib/product/widget/`, `lib/product/theme/parts/` ve `lib/product/utils/` icinde
  yeniden kullanilacak ne varsa listele — yeniden implement etme.
- Plani yaz, sonra kod yaz.

### 2 — Model (gerekiyorsa)
[model_rules.md](../../../doc/guides/model_rules.md): Hive'a yaziliyorsa
`product/model/` + `@HiveType`, degilse feature `model/` + Freezed.

### 3 — State + Cubit
[state_management.md](../../../doc/guides/state_management.md) sablonlari birebir.
Servisler constructor injection ile alinir; `emit(state.copyWith(...))` disinda state
degismez; exception yutulmaz.

### 4 — View
[view_rules.md](../../../doc/guides/view_rules.md). StatefulWidget seciliyse
`_view.dart` + `_view_model.dart` (abstract State) olarak ayir.
Veri ceken her ekran dort durumu ele alir — hazir widget'lar
[ui_states.md](../../../doc/guides/ui_states.md)'de.

### 5 — Baglanti
- Route: [route_and_strings.md](../../../doc/guides/route_and_strings.md).
- Ceviriler: `tr.json` **ve** `en.json`, ardindan `./script/lang.sh`.
- Servis gerekiyorsa: [service_rules.md](../../../doc/guides/service_rules.md).

### 6 — Modul dokumani
`lib/feature/<ad>/<ad>.md` yazilmadan feature bitmis sayilmaz
([folder_structure.md](../../../doc/guides/folder_structure.md)).

### 7 — Bitirme
`./script/codegen.sh` (codegen gerektiyse) → `./script/lang.sh` (ceviri eklendiyse)
→ `./script/verify.sh`.

## Otomatik red — cikti vermeden once duzelt

- Inline `TextStyle(fontSize: ...)` veya inline renk → `textTheme` / `colorScheme` / `context.appColors`.
- Hardcoded `EdgeInsets` / piksel / `BorderRadius.circular(<int>)` → `AppPaddings` / `AppRadius`.
- Hardcoded kullanici metni → `LocaleKeys.*.tr()`.
- Hardcoded asset yolu → `Assets.*`.
- `// ignore:` ile lint susturma.
- `emit` disinda state mutasyonu; bos `catch {}`.
- `<feature>.md` yok.
- Yeni paket eklenmis ama gerekcesi sorulmamis ([clean_code.md](../../../doc/guides/clean_code.md) → Paket disiplini).

## Cikti

Olusturulan/degistirilen her dosya icin tek cumle + tiklanabilir yol. Sonra: kalan
manuel adim (codegen, route kaydi, ceviri) ve gerekiyorsa eksik test. Baska bir sey yazma.
