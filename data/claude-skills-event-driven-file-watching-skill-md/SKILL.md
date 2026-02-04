---
name: .claude/skills/event-driven-file-watching/SKILL.md
description: |
    Ryan Dahlのイベント駆動・非同期I/O思想に基づくファイルシステム監視の専門知識。
    Chokidarライブラリを中心に、Observer Patternによる効率的なファイル変更検知、
    クロスプラットフォーム対応、EventEmitterによる疎結合な通知システムを提供。
    使用タイミング:
    - Chokidarによるファイル監視システムを設計・実装する時
    - Observer Patternでイベント通知を設計する時
    - ファイルシステムイベントのハンドリングを実装する時
    - クロスプラットフォーム対応の監視設定を決定する時
    - 監視方式（native fsevents vs polling）を選択する時

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/event-driven-file-watching/resources/chokidar-config-reference.md`: Chokidar設定オプションとクロスプラットフォーム対応ガイド
  - `.claude/skills/event-driven-file-watching/resources/event-emitter-patterns.md`: EventEmitterによるObserver Patternとイベント通知システムの実装
  - `.claude/skills/event-driven-file-watching/templates/watcher-template.ts`: ファイル監視システム実装テンプレート

  Use proactively when implementing .claude/skills/event-driven-file-watching/SKILL.md patterns or solving related problems.
version: 1.0.0
---

# Event-Driven File Watching

## 概要

このスキルは、Node.js におけるイベント駆動型ファイル監視の設計と実装に関する専門知識を提供します。Ryan Dahl が提唱する非同期 I/O モデルに基づき、効率的で信頼性の高い監視システムを構築するための原則とパターンを定義します。

---

## 核心概念

### 1. イベント駆動アーキテクチャの原則

**Ryan Dahl の設計原則**:

1. **非同期ファースト**: すべての I/O 操作は非同期 API を使用
2. **シンプル・コア**: 監視コアは最小限、複雑な処理は外部委譲
3. **イベント駆動**: 状態変化はイベントとして表現（push > poll）
4. **エラー伝播**: エラーは隠蔽せず明示的に伝播

### 2. Chokidar の選択根拠

| 技術         | 特性                                         | 推奨度    |
| ------------ | -------------------------------------------- | --------- |
| **Chokidar** | クロスプラットフォーム、安定性、豊富な設定   | ✅ 推奨   |
| fs.watch     | ネイティブ API、プラットフォーム依存、不安定 | ⚠️ 限定的 |
| fs.watchFile | polling 方式、高 CPU、遅延                   | ❌ 非推奨 |

### 3. Observer Pattern の適用

```typescript
// 基本構造
class FileWatcher extends EventEmitter {
  private watcher: FSWatcher | null = null;

  constructor(private config: WatcherConfig) {
    super();
    this.setMaxListeners(10); // メモリリーク防止
  }

  // カスタムイベントタイプ
  // - fileAdded: 新規ファイル追加
  // - fileChanged: ファイル変更
  // - fileRemoved: ファイル削除
  // - error: エラー発生
  // - ready: 初期スキャン完了
}
```

---

## Chokidar 設定ガイド

### 基本設定パラメータ

```typescript
interface ChokidarOptions {
  // 除外パターン
  ignored: string | RegExp | ((path: string) => boolean) | Array<...>;

  // 監視継続（デフォルト: false）
  persistent: boolean;

  // 初期スキャンでイベント発火（デフォルト: false）
  ignoreInitial: boolean;

  // 書き込み完了待機
  awaitWriteFinish: false | {
    stabilityThreshold: number; // 安定性閾値（ms）
    pollInterval: number;       // チェック間隔（ms）
  };

  // 監視方式
  usePolling: boolean;         // polling使用（NFS/Docker向け）
  interval: number;            // pollingインターバル

  // パーミッション
  ignorePermissionErrors: boolean;

  // シンボリックリンク
  followSymlinks: boolean;

  // ディレクトリ深度
  depth: number | undefined;   // undefined = 無制限
}
```

### 環境別推奨設定

```typescript
// 開発環境（ローカルファイルシステム）
const devConfig: ChokidarOptions = {
  persistent: true,
  ignoreInitial: true,
  awaitWriteFinish: {
    stabilityThreshold: 100,
    pollInterval: 50,
  },
  usePolling: false, // ネイティブfsevents使用
  ignored: ["**/node_modules/**", "**/.git/**", "**/dist/**"],
};

// 本番環境（NFS/Docker volumes）
const prodConfig: ChokidarOptions = {
  persistent: true,
  ignoreInitial: true,
  awaitWriteFinish: {
    stabilityThreshold: 500,
    pollInterval: 100,
  },
  usePolling: true, // ネットワークFS向け
  interval: 1000,
  ignored: ["**/node_modules/**", "**/.git/**"],
};
```

---

## イベントハンドリング設計

### イベントタイプと用途

| イベント    | 発火条件         | 典型的なハンドリング   |
| ----------- | ---------------- | ---------------------- |
| `add`       | ファイル追加     | 同期キュー追加         |
| `change`    | ファイル変更     | 差分同期               |
| `unlink`    | ファイル削除     | リモート削除通知       |
| `addDir`    | ディレクトリ追加 | ディレクトリ構造同期   |
| `unlinkDir` | ディレクトリ削除 | リモート削除           |
| `ready`     | 初期スキャン完了 | 監視準備完了通知       |
| `error`     | エラー発生       | エラーログ・リカバリー |
| `raw`       | 低レベルイベント | デバッグ用             |

### ハンドラー実装パターン

```typescript
// 型安全なイベントハンドラー
type FileEventHandler = (path: string, stats?: fs.Stats) => void;
type ErrorHandler = (error: Error) => void;
type ReadyHandler = () => void;

// イベント登録の模範例
watcher
  .on("add", (path, stats) => this.emit("fileAdded", { path, stats }))
  .on("change", (path, stats) => this.emit("fileChanged", { path, stats }))
  .on("unlink", (path) => this.emit("fileRemoved", { path }))
  .on("error", (error) => this.emit("error", error))
  .on("ready", () => this.emit("ready"));
```

---

## 判断基準チェックリスト

### 設計時

- [ ] 監視対象ディレクトリのファイルシステムタイプを確認したか？（ローカル/NFS/Docker）
- [ ] 除外パターンは.gitignore と整合しているか？
- [ ] 書き込み完了待機の閾値は対象ファイルサイズに適しているか？
- [ ] イベントリスナー数の上限を設定したか？（メモリリーク防止）

### 実装時

- [ ] すべての I/O 操作が非同期 API を使用しているか？
- [ ] error イベントのハンドラーが登録されているか？
- [ ] graceful shutdown 時に watcher.close()が呼ばれるか？
- [ ] リソースリーク防止策が実装されているか？

### テスト時

- [ ] ファイル追加イベントが正しく検知されるか？
- [ ] 除外パターンが正しく機能するか？
- [ ] 高負荷時（大量ファイル追加）でもメモリリークしないか？

---

## TypeScript 型定義

```typescript
// ファイルイベント構造
interface FileEvent {
  type: "add" | "change" | "unlink";
  path: string;
  stats?: fs.Stats;
  timestamp: string; // ISO8601
}

// 監視設定
interface WatcherConfig {
  watchPath: string;
  ignored: string[];
  awaitWriteFinish: {
    stabilityThreshold: number;
    pollInterval: number;
  };
  usePolling: boolean;
  persistent: boolean;
}

// エラー情報
interface WatcherError {
  code: string; // EACCES, ENOENT等
  message: string;
  path?: string;
  recoverable: boolean;
}
```

---

## 関連スキル

- `.claude/skills/debounce-throttle-patterns/SKILL.md` - イベント最適化
- `.claude/skills/file-exclusion-patterns/SKILL.md` - 除外パターン設計
- `.claude/skills/graceful-shutdown-patterns/SKILL.md` - シャットダウン処理
- `.claude/skills/nodejs-stream-processing/SKILL.md` - ストリーム処理

---

## リソース参照

詳細な実装例やテンプレートが必要な場合:

```bash
# Chokidar設定リファレンス
cat .claude/skills/event-driven-file-watching/resources/chokidar-config-reference.md

# EventEmitter実装パターン
cat .claude/skills/event-driven-file-watching/resources/event-emitter-patterns.md

# 監視システムテンプレート
cat .claude/skills/event-driven-file-watching/templates/watcher-template.ts
```
