---
name: Core/Std Boundary
description: modules/* の core と std の依存境界を守る依頼で使う。core は no_std のみに依存し、std は std/tokio などに依存できる。テストコードは例外。
---

# Core/Std Boundary

`modules/*` における `core` と `std` の依存境界を守るためのガイド。

## ルール（最優先）

- **core は no_std のみ**: `std` や `tokio` などの依存は禁止
- **std は std/tokio 等が利用可**: OS/IO/スレッド/タイマなどは `std` 側に集約
- **テストコードは例外**: `core` 配下でもテスト専用コードでは `std` 依存を許容
- **ランタイム本体で cfg(feature = "std") による分岐は入れない**（テスト内は可）

## 進め方

1. **変更対象が core / std のどちらかを判定**
2. **依存の追加が必要なら置き場所を再考**
   - `std` 依存が必要なら `std` 側へ移動
   - `core` には `alloc` や `core`、プロジェクト内の no_std 準拠モジュールのみ
3. **境界をまたぐ場合は interface を core に置く**
   - trait / struct / enum を core に置き、std 実装は std 側に置く
4. **テストは例外扱いにする**
   - `tests/` や `cfg(test)` の範囲で `std` を使う
   - 本体コードに `std` 依存が混ざらないよう分離

## チェックリスト

- core に `std` / `tokio` / OS API が入っていないか
- std にしか置けない処理が core に残っていないか
- core の public API が std に引きずられていないか
- テストコードが本体に混ざっていないか

