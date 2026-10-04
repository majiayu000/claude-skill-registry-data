---
name: starter-review
description: Bu template'in konvansiyonlarina gore degisen dosyalari denetler — Cubit+Freezed state kullanimi, servis/locator yerlesimi, view tipi secimi, dort-durum ele alinisi, tasarim token'lari (renk/tipografi/padding/radius), LocaleKeys, TypedGoRoute, zorunlu <feature>.md ve very_good_analysis kurallari. Kullanici "degisiklikleri incele", "bu PR'i review et", "projeye uygun mu", "mimari kontrol", "review my changes" dediginde kullan.
---

# Degisiklik Denetimi

Calisma dizinindeki (ya da verilen) degisiklikleri
[doc/guides/AGENTS.md](../../../doc/guides/AGENTS.md) ve altindaki rehberlere gore denetler.
Kural kaynagi doc'tur; burada kural tanimlanmaz.

## Kapsam

Yalnizca **degisen dosyalar** ve o dosyalarin **degisen satirlari**. Butun repoyu
denetleme.

```bash
git diff --stat
git diff
# ya da branch karsilastirmasi:
git diff main...HEAD
```

Degisiklik yoksa bunu soyle ve dur.

## Yontem

1. `doc/guides/AGENTS.md` + degisikligin dokundugu alanin rehberini oku.
2. Her degisen dosyayi oku.
3. Kapsam genisse (5+ dosya, ya da mimari degisiklik) derin denetimi
   `starter-architecture-reviewer` subagent'ina devret ve bulgularini birlestir.
4. Her bulguyu bir doc kuralina ve bir `dosya:satir`'a bagla. Bagli degilse bulgu degildir.

## Ne aranir

Kaynak: `doc/guides/clean_code.md`, `doc/*`. Ozet:

**Mimari** — Freezed state + Cubit sablonu; servis constructor injection ile;
`emit(state.copyWith(...))` disinda mutasyon yok; app-geneli state `product/state/`;
BlocProvider yerlesimi (global/lokal) dogru secilmis.

**View** — StatelessWidget varsayilan; controller/lifecycle varsa
StatefulWidget + ayri `_view_model.dart`; `build()` icinde agir islem yok;
`build()` ~80 satiri gecmisse parcalanmis; tekrar eden UI metot degil widget sinifi.

**Durumlar** — veri ceken ekranda loading/error/empty/data dordu de var.

**Hata yonetimi** — bos `catch {}` yok; exception yutulmuyor; kullaniciya ham
exception gosterilmiyor.

**Token'lar** — inline renk, inline `TextStyle(fontSize:)`, ham `EdgeInsets`,
`BorderRadius.circular(<int>)`, ham `Duration` yok.

**Metin/asset** — hardcoded kullanici metni yok (`LocaleKeys`), hardcoded asset
yolu yok (`Assets.*`), yeni anahtar hem `tr.json` hem `en.json`'da.

**Yapi** — dosya adlari `snake_case`, bir dosya bir ana sinif, yeni feature'da
`<feature>.md` var, enum `product/enum/`, sabit `product/const/`.

**Lint/kalite** — `// ignore:` ile susturma yok, olu/yorumlanmis kod yok,
magic number yok, yorum "neden"i anlatiyor.

**Test** — yeni is mantigi (cubit/servis metodu) testle gelmis mi.

**Paket** — yeni bagimlilik eklendiyse gerekcesi sorulmus mu.

## Siddet

- **blocker** — doc kuralinin dogrudan ihlali: inline renk/stil, hardcoded metin,
  yutulan exception, eksik `<feature>.md`, `// ignore:`, emit disi mutasyon.
- **warning** — konvansiyon sapmasi: view'da is mantigi, parcalanmamis `build()`,
  eksik durum dali, yanlis klasor.
- **info** — nit: eksik `const`, isimlendirme, gereksiz import.

## Cikti

```
## Review — <N blocker, N warning, N info>

### 🔴 Blocker
- <dosya>:<satir> — <sorun + hangi doc kurali>. Duzeltme: <somut degisiklik>.

### 🟡 Warning
- <dosya>:<satir> — <sorun>. Duzeltme: <somut degisiklik>.

### 🔵 Oneri
- <dosya>:<satir> — <nit>.

### ✅ Dogru yapilmis
- <1-3 madde>
```

Bos bolumleri yazma. Ayni satiri bir kez, en yuksek siddetle bildir.
Duzeltmeyi kullanici istemeden uygulama.
