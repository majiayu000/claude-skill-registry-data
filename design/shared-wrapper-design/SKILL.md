---
name: shared-wrapper-design
description: 共有ラッパー（*Shared）と非共有本体（*）、Handle の使い分け、ArcShared+ToolboxMutex、SharedAccess/Clone の設計判断を扱う。共有の要否を判断し、shared_vs_handle ガイドに従って設計・実装する場面で使う。
---

# 共有ラッパー設計

## 方針
- 共有が不要なら本体型（`Xyz`）を使え。
- 共有が必要なら `XyzShared` を使え。
- `XyzShared` は `ArcShared<ToolboxMutex<Xyz, TB>>` を内包し、`Clone` と `SharedAccess` を入口にせよ。

## 判断基準（簡易チェック）
- **単一所有・単一スレッド**: 本体型（`Xyz`）を選べ。
- **複数所有・複数スレッド**: `XyzShared` を選べ。
- **外部へ渡す/保持する必要がある**: `XyzShared` を選べ。

## 実装ガイド
- `XyzShared` の `with_read` / `with_write` で状態へアクセスせよ。
- 個別ラッパーメソッドは必要時のみ追加し、基本構成は薄い共有ラッパーで保て。
- 共有/管理の責務が増えたら `XyzHandle` を検討せよ。
- 迷ったら `docs/guides/shared_vs_handle.md` を必ず参照せよ。
- `TB` のように RuntimeToolbox を型パラメータとして持つ型は、名称末尾を `Generic` にせよ（例: `XyzSharedGeneric<T, TB>`）。

## 例（非固定）
- `ActorFuture` / `ActorFutureSharedGeneric` は共有/非共有の一例に過ぎない。
- `IdentityLookup` / `IdentityLookupShared` のような構成でも同様に適用せよ。

## 禁止事項
- 共有が不要なのに `XyzShared` を使うな。
- 本体型に内部可変性を持ち込むな。
