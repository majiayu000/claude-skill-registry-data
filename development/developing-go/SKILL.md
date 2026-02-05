---
name: developing-go
description: Guides Go development with best practices from Google Style Guide and Effective Go. Use when go.mod is detected or Go code is being written. Covers naming, error handling, concurrency, testing, and project structure.
---

# Go開発ガイド（Modern Go Development）

## 🎯 使用タイミング
- **Goプロジェクト新規作成時**
- **既存Goコードのレビュー・改善時**
- **並行処理の実装時**
- **エラーハンドリング設計時**
- **Goのテスト作成時**

## 📚 ドキュメント構成

このスキルは以下のドキュメントで構成されています：

### 1. [命名規則](./NAMING.md)
Goの命名ベストプラクティス：
- パッケージ名の付け方
- 変数・関数名の規則
- インターフェース命名（-erサフィックス）
- エクスポート名の考え方

### 2. [エラーハンドリング](./ERROR-HANDLING.md)
堅牢なエラー処理パターン：
- エラーは値として扱う
- エラーラッピング（%w vs %v）
- センチネルエラーとカスタムエラー型
- panic/recoverの適切な使用

### 3. [並行処理](./CONCURRENCY.md)
Goの強力な並行処理パターン：
- goroutineの基本
- チャネルによる通信
- select文の活用
- 同期プリミティブ（sync.Mutex等）
- コンテキストによるキャンセル

### 4. [テスト戦略](./TESTING.md)
効果的なGoテストの書き方：
- テーブル駆動テスト
- t.Errorとt.Fatalの使い分け
- サブテスト（t.Run）
- ベンチマークテスト
- テストヘルパーの作成

### 5. [プロジェクト構造](./PROJECT-STRUCTURE.md)
推奨ディレクトリレイアウト：
- cmd/とinternal/の使い分け
- pkg/の適切な使用
- go.modの管理
- モジュール設計

### 6. [開発ツール](./TOOLING.md)
Goエコシステムのツール活用：
- gofmt/goimports
- golangci-lint
- go vet
- delve（デバッガ）
- Makefileパターン

## 🎯 Goの設計哲学

### シンプルさを重視
```go
// Good: シンプルで明確
func ProcessItems(items []Item) error {
    for _, item := range items {
        if err := item.Process(); err != nil {
            return fmt.Errorf("process item %s: %w", item.ID, err)
        }
    }
    return nil
}

// Bad: 過度な抽象化
func ProcessItems(items []Item, processor ItemProcessor, validator ItemValidator) error {
    // 不必要な複雑さ
}
```

### 明示的であること
```go
// Good: 明示的なエラーハンドリング
result, err := doSomething()
if err != nil {
    return err
}

// Bad: エラーを無視
result, _ := doSomething()
```

### 通信でメモリを共有
```go
// Good: チャネルで通信
results := make(chan Result)
go func() {
    results <- process(data)
}()
result := <-results

// Avoid: 共有メモリでの通信（必要な場合のみ）
var mu sync.Mutex
var shared int
```

## 🚀 クイックスタート

### 1. プロジェクト初期化
```bash
# モジュール作成
mkdir my-project && cd my-project
go mod init github.com/username/my-project

# 基本構造
mkdir -p cmd/myapp internal/handler internal/service
```

### 2. 基本的なmain.go
```go
package main

import (
    "context"
    "log"
    "os"
    "os/signal"
    "syscall"
)

func main() {
    ctx, cancel := signal.NotifyContext(context.Background(),
        os.Interrupt, syscall.SIGTERM)
    defer cancel()

    if err := run(ctx); err != nil {
        log.Fatal(err)
    }
}

func run(ctx context.Context) error {
    // アプリケーションロジック
    return nil
}
```

### 3. 開発コマンド
```bash
# フォーマット
gofmt -w .

# Lint
golangci-lint run

# テスト
go test ./...

# ビルド
go build -o bin/myapp ./cmd/myapp
```

## 💡 重要な原則

### ゼロ値の活用
```go
// Good: ゼロ値で有効な状態
type Counter struct {
    mu    sync.Mutex
    count int  // ゼロ値は0で有効
}

func (c *Counter) Inc() {
    c.mu.Lock()
    c.count++
    c.mu.Unlock()
}

// 初期化なしで使用可能
var c Counter
c.Inc()
```

### インターフェースは小さく
```go
// Good: 単一メソッドインターフェース
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// 組み合わせで拡張
type ReadWriter interface {
    Reader
    Writer
}
```

### 早期リターン
```go
// Good: ガード節で早期リターン
func process(item *Item) error {
    if item == nil {
        return errors.New("item is nil")
    }
    if item.ID == "" {
        return errors.New("item ID is empty")
    }

    // メインロジック
    return item.Save()
}
```

## 🔗 関連スキル

- **[applying-solid-principles](../applying-solid-principles/SKILL.md)**: SOLID原則とクリーンコード
- **[testing](../testing/SKILL.md)**: テストファーストアプローチ
- **[securing-code](../securing-code/SKILL.md)**: セキュアコーディング
- **[writing-dockerfiles](../writing-dockerfiles/SKILL.md)**: Goアプリのコンテナ化

## 📖 参考リソース

- [Effective Go](https://go.dev/doc/effective_go)
- [Google Go Style Guide](https://google.github.io/styleguide/go/)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)

## 📖 次のステップ

1. **初めての方**: [プロジェクト構造](./PROJECT-STRUCTURE.md)から始めてください
2. **命名に迷ったら**: [命名規則](./NAMING.md)を参照
3. **エラー処理**: [エラーハンドリング](./ERROR-HANDLING.md)でパターン確認
4. **並行処理**: [並行処理](./CONCURRENCY.md)でgoroutine/channel学習
5. **テスト作成**: [テスト戦略](./TESTING.md)でテーブル駆動テスト
6. **ツール設定**: [開発ツール](./TOOLING.md)でlint設定
