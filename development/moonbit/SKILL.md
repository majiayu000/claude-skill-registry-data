---
name: moonbit
description: MoonBit の文法・標準ライブラリ・ツールチェーンの参照、ドキュメント索引の案内、仕様確認、コード例作成が必要なときに使う。MoonBit に関する質問・調査・要約・ナビゲーションを行う場面で使用。
---

# Moonbit スキル

Moonbit の文法・標準ライブラリを参照するために使う。最小限の入口だけをここに示し、詳細は references から必要な部分だけを開く。

- まず `references/index.md` を読む（公式ドキュメントの目次）
- 言語仕様は `references/language/index.md` を読む（基礎と各章へのリンク）
- チュートリアルは `references/tutorial/index.md` と `references/tutorial/tour.md` を読む
- フルテキストが必要な場合のみ `references/llms.txt` を読む

利用時のヒント:
- 質問の範囲に応じて該当セクションだけを読み、不要な章は開かない
- 追加情報が必要なら上記パスをたどって目的の章を参照する

## references
- `references/index.md`: Moonbit ドキュメント目次
- `references/tutorial/index.md`: チュートリアル目次
- `references/tutorial/tour.md`: 入門ツアー
- `references/tutorial/for-go-programmers/index.md`: Go 開発者向けガイド
- `references/language/index.md`: 言語仕様目次
- `references/language/fundamentals.md`: 基本文法・型（章別リンクのみ）
- `references/language/fundamentals/built-in-data-structures.md`: 基本型・コレクション
- `references/language/fundamentals/functions.md`: 関数
- `references/language/fundamentals/control-structures.md`: 制御構造
- `references/language/fundamentals/custom-data-types.md`: ユーザー定義型
- `references/language/fundamentals/pattern-matching.md`: パターンマッチ
- `references/language/fundamentals/generics.md`: ジェネリクス
- `references/language/fundamentals/overloaded-literals.md`: リテラル多重定義
- `references/language/fundamentals/iterator.md`: イテレータ
- `references/language/fundamentals/special-syntax.md`: パイプ、cascade など
- `references/language/methods.md`: メソッド
- `references/language/methods/method-system.md`: メソッドシステム
- `references/language/methods/operator-overloading.md`: 演算子オーバーロード
- `references/language/methods/trait-system.md`: トレイトシステム
- `references/language/methods/trait-objects.md`: トレイトオブジェクト
- `references/language/methods/builtin-traits.md`: 組み込みトレイト
- `references/language/derive.md`: derive 機構
- `references/language/derive/show.md`: Show
- `references/language/derive/eq-and-compare.md`: Eq / Compare
- `references/language/derive/default.md`: Default
- `references/language/derive/hash.md`: Hash
- `references/language/derive/arbitrary.md`: Arbitrary
- `references/language/derive/fromjson-and-tojson.md`: JSON 変換
- `references/language/error-handling.md`: エラーハンドリング
- `references/language/error-handling/error-types.md`: エラー型
- `references/language/error-handling/throwing-errors.md`: 例外送出
- `references/language/error-handling/handling-errors.md`: 例外処理
- `references/language/packages.md`: パッケージ
- `references/language/packages/packages-and-modules.md`: パッケージ/モジュール
- `references/language/packages/access-control.md`: アクセス制御
- `references/language/packages/virtual-packages.md`: 仮想パッケージ
- `references/language/tests.md`: テスト
- `references/language/benchmarks.md`: ベンチマーク
- `references/language/docs.md`: ドキュメント生成
- `references/language/ffi.md`: FFI
- `references/language/ffi/backends.md`: バックエンド
- `references/language/ffi/declare-foreign-type.md`: 外部型宣言
- `references/language/ffi/declare-foreign-function.md`: 外部関数宣言
- `references/language/ffi/export-functions.md`: 関数エクスポート
- `references/language/ffi/lifetime-management.md`: ライフタイム管理
- `references/language/async-experimental.md`: 非同期（実験的）
- `references/language/error_codes/index.md`: エラーコード一覧
- `references/llms.txt`: 公式 llms ドキュメント全文（必要時のみ）
