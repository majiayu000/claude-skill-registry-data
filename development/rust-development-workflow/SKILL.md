---
name: Rust Development Workflow
description: Execute comprehensive Rust development workflow including cargo build, test, clippy, and fmt. Use when compiling, testing, or checking Rust code quality in the Miyabi project.
allowed-tools: Bash, Read, Grep, Glob
---

# 🦀 Rust Development Workflow

**Version**: 2.0.0
**Last Updated**: 2025-11-22
**Priority**: ⭐⭐⭐⭐⭐ (P0 Level)
**Purpose**: Rustビルド・テスト・品質チェックの最適化実行

---

## 📋 概要

Miyabiプロジェクトにおける完全なRust開発ワークフロー。
コード品質、型安全性、包括的テストを保証します。

---

## 🎯 P0: 呼び出しトリガー

| トリガー | 例 |
|---------|-----|
| ビルド | "build the project", "compile" |
| テスト | "run tests", "test this" |
| 品質チェック | "check code quality", "lint" |
| コミット前 | "before committing" |
| 新機能実装後 | "after implementing" |

---

## 🔧 P1: コマンド別最適化

### コマンド優先順位

| コマンド | 用途 | 平均時間 | 頻度 |
|---------|------|---------|------|
| `cargo check` | 型チェック（高速） | 10-30s | 高 |
| `cargo build` | デバッグビルド | 30-120s | 高 |
| `cargo build --release` | リリースビルド | 60-300s | 低 |
| `cargo test` | テスト実行 | 60-180s | 高 |
| `cargo clippy` | リントチェック | 30-60s | 中 |
| `cargo fmt` | フォーマット | 5-10s | 高 |
| `cargo doc` | ドキュメント生成 | 30-60s | 低 |

### 最適パターン

```
✅ GOOD: シーケンシャル実行（依存関係あり）
cargo build && cargo test && cargo clippy -- -D warnings && cargo fmt -- --check

❌ BAD: 個別実行（オーバーヘッド大）
cargo build → 結果確認 → cargo test → 結果確認 → ...
```

---

## 🚀 P2: ワークフロー別パターン

### Pattern 1: クイックチェック（開発中）

```bash
# 最小限のチェック（2-3分）
cargo check && cargo test -- --test-threads=1
```

**用途**: コード変更の即時検証

### Pattern 2: 標準ビルドサイクル（コミット前）

```bash
# フルチェック（5-10分）
cargo build --workspace && \
cargo test --workspace --all-features && \
cargo clippy --workspace --all-targets --all-features -- -D warnings && \
cargo fmt --all -- --check
```

**用途**: コミット前の品質保証

### Pattern 3: クリーンビルド（問題発生時）

```bash
# クリーンビルド（10-15分）
cargo clean && \
cargo build --workspace && \
cargo test --workspace --all-features
```

**用途**: キャッシュ問題の解消

### Pattern 4: リリースビルド（デプロイ前）

```bash
# リリース準備（15-20分）
cargo build --release --workspace && \
cargo test --release --workspace && \
cargo bench --no-run
```

**用途**: 本番デプロイ前の最終確認

### Pattern 5: ドキュメント生成

```bash
# ドキュメント（3-5分）
cargo doc --workspace --no-deps --all-features
```

**用途**: API ドキュメント更新

---

## ⚡ P3: パフォーマンス最適化

### 並列ビルド設定

```bash
# CPUコア数に応じた並列度
cargo build -j 8
cargo test -- --test-threads=8
```

### インクリメンタルビルド活用

```
# キャッシュ有効（高速）
target/debug/deps/
target/release/deps/

# キャッシュ無効化が必要な場合
CARGO_INCREMENTAL=0 cargo build
```

### ビルド時間比較

| 条件 | フルビルド | インクリメンタル |
|------|-----------|----------------|
| Debug | 2-3分 | 10-30秒 |
| Release | 5-10分 | 30-60秒 |
| Clean | 5-10分 | N/A |

---

## 📊 プロジェクト固有設定

### Cargo Workspace構造

```
miyabi-private/
├── Cargo.toml (workspace root)
├── crates/
│   ├── miyabi-types/      # コア型定義
│   ├── miyabi-core/       # 共通ユーティリティ
│   ├── miyabi-cli/        # CLIバイナリ
│   ├── miyabi-agents/     # Agent実装
│   ├── miyabi-github/     # GitHub API統合
│   ├── miyabi-worktree/   # Git Worktree管理
│   └── miyabi-llm/        # LLMプロバイダー抽象化
└── target/
```

### 依存関係チェック

```bash
# 主要依存関係
tokio         # 非同期ランタイム
async-trait   # Trait非同期メソッド
serde         # シリアライゼーション
octocrab      # GitHub API
tracing       # ログ
```

---

## 🛡️ エラーハンドリング

### 共通エラーパターン

| エラー | 原因 | 対処 |
|--------|------|------|
| `error[E0277]` | Trait未実装 | `async-trait`使用確認 |
| `error[E0412]` | 型未定義 | `use`文追加 |
| `error[E0433]` | モジュール未解決 | パス確認 |
| Clippy警告 | コード品質 | 警告に従い修正 |
| fmt差分 | フォーマット | `cargo fmt`実行 |

### テスト失敗時

```bash
# 並列実行問題の場合
cargo test -- --test-threads=1

# 特定テストのデバッグ
cargo test test_name -- --nocapture

# 詳細出力
RUST_BACKTRACE=1 cargo test
```

---

## ✅ 成功基準

| チェック項目 | 基準 |
|-------------|------|
| `cargo build` | 0 errors |
| `cargo test` | 100% pass |
| `cargo clippy` | 0 warnings |
| `cargo fmt --check` | 0 diff |
| `cargo doc` | 0 warnings |

### 出力フォーマット

```
🦀 Rust Development Workflow Results

✅ Build: Success (X crates compiled)
✅ Tests: XX/XX passed (XXX assertions)
✅ Clippy: 0 warnings
✅ Format: All files properly formatted
✅ Docs: Generated successfully

Ready to commit ✓
```

---

## 🔗 関連ドキュメント

| ドキュメント | 用途 |
|-------------|------|
| `context/rust.md` | Rust開発ガイドライン |
| `context/rust-tool-use-rules.md` | MCP Tool最適化 |
| `agents/RUST_COMMANDS_OPTIMIZATION.md` | Agent向け最適化 |

---

## 📝 関連Skills

- **Agent Execution**: Agent実行前のビルド確認
- **Git Workflow**: コミット前の品質チェック
- **Security Audit**: セキュリティ監査との統合
