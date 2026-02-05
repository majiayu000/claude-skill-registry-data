---
name: rust-error-handling
description: Rustでのエラー設計を、境界ごとに thiserror / anyhow を使い分けて実装する。ドメイン/ライブラリは型付きエラー(thiserror)、アプリ境界のみ anyow。context付与、unwrap禁止、HTTP/CLI変換の指針を含む。
---

# Rust Error Handling: anyhow / thiserror の境界設計

## 概要

### 目的

- 例外的な失敗を「握りつぶさず」「原因を辿れる形」で伝搬し、境界で適切に変換する。
- ドメイン層のAPIを型付きエラーで安定させ、上位で集約・ログ化・ユーザー向け変換ができるようにする。

### 適用範囲

- **ライブラリ／ドメイン層**: `thiserror` による型付きエラー（`Result<T, Error>`）
- **アプリケーション境界（main/CLI/HTTPハンドラ等）**: `anyhow::Result` と `.context()` / `.with_context()`

### やらないこと

- ドメイン層の public API に `anyhow::Error` を露出しない。
- 「とりあえず `String` エラー」で返さない（判断不能になる）。

## 前提となる役割分担

- **`anyhow`**
  - `anyhow::Error` と `anyhow::Result<T>` による「型消去された汎用エラー型」。
  - **アプリケーションコード**での「簡易なエラー統合・伝搬・コンテキスト付与」に用いる。
- **`thiserror`**
  - `#[derive(Error)]` で `std::error::Error` 実装を自動生成するためのクレート。
  - **ライブラリ／ドメイン層**での「型付きエラー定義」に用いる。

- **ライブラリ／ドメイン層** → `thiserror` で意味のある Error 型を定義
- **アプリケーション境界（`main` など）** → 複数の Error を `anyhow` でまとめて扱う

## アプリケーション層（binary crate）でのルール — anyhow

1. **戻り値は `anyhow::Result<T>` を使うのは「最上位だけ」**
   - `main` や CLI ハンドラ、HTTP サーバのエントリポイントなど、  
     「最終的にログを出して終了／レスポンスに変換する層」に限定して `anyhow::Result<()>` を使う。
   - ドメインロジックにまで `anyhow::Result` を広げない。

   ```rust
   use anyhow::Result;

   fn main() -> Result<()> {
       app::run()?;
       Ok(())
   }
   ```

2. **`.context()` / `.with_context()` でエラーに文脈を必ず付ける**

   - 「どの操作中に失敗したのか」がわかるメッセージを付ける。

   ```rust
   use anyhow::{Context, Result};

   fn load_config(path: &str) -> Result<String> {
       std::fs::read_to_string(path)
           .with_context(|| format!("failed to read config from {path}"))
   }
   ```

3. **「ハンドルできない／ハンドルしない」境界でのみ anyhow に集約する**

   - HTTP レイヤや CLI レイヤで「ログを出す」「ユーザー向けメッセージに変換する」直前で、
     下位の `thiserror` ベースのエラーを `anyhow::Error` に吸わせるのは OK。
   - それより下の層では **独自 Error 型のまま** 保つ。

4. **`unwrap` / `expect` の禁止（初期化コードなど例外的ケースを除く）**

   - ランタイムで発生しうる失敗はすべて `Result` / `Option` として扱い、`?` と `anyhow` / `thiserror` で処理する。

## ライブラリ／ドメイン層でのルール — thiserror

1. **Public API では `anyhow` を返さず、自前の Error 型を定義する**

   - `pub fn ... -> Result<T, Error>` の `Error` は自前の enum / struct。
   - `anyhow::Error` を public API に出すのは禁止。

   ```rust
   use thiserror::Error;

   #[derive(Debug, Error)]
   pub enum RepositoryError {
       #[error("db error: {0}")]
       Db(#[from] sqlx::Error),

       #[error("entity not found: {id}")]
       NotFound { id: String },
   }

   pub type Result<T> = std::result::Result<T, RepositoryError>;
   ```

2. **`#[from]` で外部エラーをラップし、source を保持する**

   - 依存クレートのエラーや IO エラーは、`#[from]` を使って自動変換する。
   - これにより `?` 演算子で自然に伝搬できる。

3. **エラー型は「使う側の判断に必要な粒度」で設計する**

   - 「ユーザー入力ミス」「外部サービスの障害」「内部バグ」など、
     リトライ可否や HTTP ステータス変換などに必要な分類を enum variant として持たせる。

   ```rust
   #[derive(Debug, Error)]
   pub enum DomainError {
       #[error("invalid input: {0}")]
       InvalidInput(String),

       #[error("external service failed: {0}")]
       External(String),

       #[error("unexpected internal error")]
       Internal(#[from] anyhow::Error), // ← ドメイン内だけで包むのはアリ
   }
   ```

4. **Error 型はモジュール／境界ごとに分ける**

   - 1 つの巨大な `Error` enum に何でも詰め込まず、
     「RepositoryError」「DomainError」「ApiError」のように責務ごとに分割する。

## チェックリスト

- [ ] ドメイン層の public API は `Result<T, DomainError>`（または責務別Error）になっている
- [ ] `#[from]` による source 保持ができている（原因追跡できる）
- [ ] アプリ境界で `.context()` / `.with_context()` が付与されている
- [ ] `unwrap/expect` が残っていない（例外: テスト、明示された初期化のみ）
- [ ] HTTP/CLI変換が match で明示され、判断基準が読み取れる
