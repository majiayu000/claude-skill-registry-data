---
name: model-strategy
version: 2.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-06-13
description: マルチモデルオーケストレーションとモデル切り替え戦略。スコアベースのモデル選択、クロスエージェント委任（Gemini、Codex、Ollama）、アドバイザーペアリング、エスカレーション条件、権限マトリクス、およびコスト効率の最適化。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing, cross-agent, advisor]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ing-strategie.md', 'origin_version': '2.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="model-strategy banner">

> **日本語** — `model-strategy` の公式日本語版。


# モデル切り替え戦略（日本語）

> マルチモデルオーケストレーション: スコアベースのモデル選択、クロスエージェント委任、アドバイザーペアリング、エスカレーション条件、コスト効率最適化

---

## 1. モデルカタログ

### Claude（Agent ツール経由で Subagent として起動可能）

```
Level 4 (Reviewer):   Opus 4.8  — advisor, math review     [user only: /model, /advisor]
Level 3 (Strategist): Opus 4.6  — architecture, concepts   [subagent: model:"opus"]
Level 3 (Creative):   Fable 5   — creative texts, stories  [subagent: model:"fable"]
Level 2 (Workhorse):  Sonnet 4.6— implementation, debug    [subagent: model:"sonnet"]
Level 1 (Fast):       Haiku 4.5 — boilerplate, formatting  [subagent: model:"haiku"]
```

### 外部エージェント（コンパニオンスクリプト / SSH）

```
Level 2-3: Gemini 3.5 pro  — research, scientific databases [agy-companion CLI]
Level 2:   Gemini 3.5 flash— fast research                  [agy-companion CLI]
Level 2-3: Codex 5.5 (GPT) — code review, code generation   [codex-companion CLI]
Level 2:   Codex 4.5 (GPT) — simpler code tasks             [codex-companion CLI]
```

### ローカルモデル（トークンフリー、24/7 常驻）

```
Level 1-2: Ollama (Qwen 3.5:35b-a3b) — Haiku-to-Sonnet level [<ollama-host>:11434]
           Invocation: SSH + curl http://<ollama-host>:11434/v1/chat/completions
           Or: delegation via an agent-system control API (if available)
```

### 到達可能性マトリクス

| モデル | LLM起動可能 | 呼び出しパス | 制約事項 |
|-------|---------------|-----------------|-------------|
| Sonnet 4.6 | 可能 | `Agent(model:"sonnet")` | — |
| Opus 4.6 | 可能 | `Agent(model:"opus")` | — |
| Haiku 4.5 | 可能 | `Agent(model:"haiku")` | — |
| Fable 5 | 可能 | `Agent(model:"fable")` | — |
| Opus 4.8 | Advisor限定 | セッション内の `advisor()` | ユーザーが `/advisor` を設定する必要あり |
| Gemini 3.5 | 可能 (Bash) | `companion-for-agy "prompt"` | Windows限定、stdoutの回避策 |
| Codex 5.5/4.5 | 可能 (Bash) | `node codex-companion.mjs task "prompt"` | 認証が必要 |
| Ollama | 可能 (SSH/curl) | SSH + curl で Ollama ホスト API へ | VPN/Tailscale がアクティブであること |
| Opus 4.8（メインモデルとして） | 不可 | ユーザー: `/model opus 4.8` | ユーザー操作のみ |
| Fable 5（メインモデルとして） | 不可 | ユーザー: `/model fable` | ユーザー操作のみ |

---

## 2. スコア計算

```
Dimensions (0-10):
  CLARITY     : How unambiguous is the task?
  COMPLEXITY  : How many components?
  CREATIVITY  : New solutions needed?
  CONTEXT     : How much prior knowledge?
  CRITICALITY : How important is perfection?

SCORE = (10 - CLARITY) + COMPLEXITY + CREATIVITY + CONTEXT + CRITICALITY
```

### スコアしきい値

| スコア | モデル | 例 |
|-------|-------|----------|
| 0-8 | Ollama（ローカルホスト） | プロンプト生成、要約、簡単なテキスト |
| 9-12 | Haiku | `__init__.py`、フォーマット調整、ボイラープレート |
| 13-22 | Sonnet | 実装、バグ修正、標準的なコード |
| 13-22 | Gemini 3.5 | リサーチ、文献検索、科学データベース |
| 13-22 | Codex 5.5 | コード生成（Luau, Node.js）、計算スクリプト |
| 23-28 | Sonnet + advisor レビュー | 品質チェックを伴う複雑なコード |
| 23-35 | Fable 5 | クリエイティブテキスト、マーケティング、ストーリーテリング |
| 29-40 | Opus 4.6 | アーキテクチャ、戦略、論文執筆 |
| 35-50 | Opus 4.6 + advisor | 証明、アーキテクチャ決定、統計学 |
| 40-50 | Opus 4.8（ユーザーへの推奨） | 数学的証明作業、最高度の厳密性 |

---

## 3. クロスエージェント委任

### どの外部エージェントを何に使うか？

| タスク | 最適なエージェント | 理由 |
|------|-----------|--------|
| 科学文献検索 | Gemini 3.5 pro | ネイティブの OpenAlex/arXiv/PubMed スキル |
| コードレビュー（セカンドオピニオン） | Codex 5.5 | 独立した視点 |
| 簡単なテキスト生成 | Ollama（ローカルホスト） | トークンフリー、24/7 |
| クリエイティブテキスト、マーケティング | Fable 5 | 最も強力なクリエイティブ出力 |
| 数学的証明 | Opus 4.8 (advisor) | 最高度の分析的深さ |

### 除外事項（ドキュメント化された弱点）

- **Gemini:** 数学的レビュー/証明作業には「不可」（2026-06-07の証明レビューにおいて方向性のエラーが記録されているため）
- **Codex 4.5:** 5.5 が利用できない場合のみ。通常は常に 5.5

### 呼び出しパス

> プレースホルダー `<host>`, `<ollama-host>`, `<tailscale-ip>`, `<user>`, `~/.ssh/<key>` はご自身のインフラ環境に合わせて置換してください。

**Gemini (via companion-for-agy):**
```
companion-for-agy --researcher --json --timeout 120000 "research prompt"
```

**Codex (via codex-companion):**
```
node "~/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs" task --effort high "code prompt"
```

**Ollama on a remote host (via SSH):**
```
ssh -i ~/.ssh/<key> <user>@<tailscale-ip> "curl -s http://localhost:11434/v1/chat/completions -d '{\"model\":\"qwen3.5:35b-a3b\",\"messages\":[{\"role\":\"user\",\"content\":\"Prompt\"}]}'"
```

**Delegation to an agent system with tools (example):**
```
curl -s -X POST http://<host>:8081/api/chat -H "Content-Type: application/json" -d '{"prompt": "...", "chat_id": "claude-delegate"}'
```

---

## 4. アドバイザーペアリング

### 仕組み

`advisor()` は**セッションレベルのツール**です。アドバイザーモデルはプログラムからではなく、ユーザーが `/advisor` 経由で設定します。これにより、以下のペアリングパターンが生成されます。

| パターン | 仕組み | 使用するタイミング |
|---------|--------------|-------------|
| **セッションアドバイザー** | ユーザーが `/advisor opus 4.8` を設定し、エージェントが `advisor()` を呼び出す | 証明/アーキテクチャの標準パターン |
| **オーケストレーター兼レビュアー** | Opus メインモデルが Sonnet サブエージェントの出力をレビューする | オーケストレーターがワーカーより強力な場合 |
| **カウンターエージェント** | エージェントAが作業し、エージェントBが敵対的にチェックする | 独立した検証、2つの視点 |
| **ユーザーへの推奨** | エージェントが「このタスクは opus 4.8 + advisor で実行してください」と推奨する | 当前のセッション機能が不足している場合 |

### アドバイザーを推奨すべきタイミング

- 数学的証明作業（スコア ≥ 35）
- 長期的な影響を伴うアーキテクチャの決定
- 統計的手法 / 研究デザイン
- 2回以上のデバッグサイクルで解決しない複雑なバグ

### アドバイザーを使用すべきでないタイミング

- 定型的なコード、コンテンツ、フォーマット（スコア < 23）
- 単純な機能の実装
- 明確に定義された非クリティカルなタスク

---

## 5. エスカレーション条件

### Ollama -> Haiku
- ファイルアクセスが必要な場合
- コード分析が必要な場合

### Haiku -> Sonnet
- 影響を受けるファイルが 3 つ以上ある場合
- 代替案からの決定が必要な場合
- 予期しないエラーが発生した場合
- 削除操作が要求された場合

### Sonnet -> Opus
- アーキテクチャの決定が必要な場合
- 3 つ以上のシステムを統合する必要がある場合
- 要件が矛盾している / 不明瞭な場合
- 戦略的計画が必要な場合

### Sonnet -> Gemini（横方向）
- 科学的研究が必要な場合
- 参考文献の検証

### Sonnet -> Codex（横方向）
- セカンドオピニオンとしてのコードレビュー
- アドバイザーが過負荷な場合（フォールバックレビュアー）

### Opus -> Opus + advisor
- 証明のレビューが必要な場合
- クリティカルなアーキテクチャの決定
- 統計的手法

### 降格（デエスカレーション）
- コンセプトが定義済み -> Sonnet が実装を引き継ぐ
- タスクが単純/反復的 -> Haiku が引き継ぐ
- テキストのみ、ツールアクセスなし -> Ollama が引き継ぐ

---

## 6. 権限マトリクス

| 操作 | Ollama | Haiku | Sonnet | Opus | Gemini | Codex |
|-----------|--------|-------|--------|------|--------|-------|
| ファイル読み込み | - | 可能 | 可能 | 可能 | 可能* | 可能* |
| ファイル書き込み | - | 可能 | Possible | 可能 | 可能* | 可能* |
| ファイル削除 | - | - | 可能** | 可能 | - | - |
| システムコマンド | - | - | 可能** | 可能 | 可能* | 可能* |
| アーキテクチャ決定 | - | - | - | 可能 | - | - |
| Webリサーチ | - | - | 可能 | 可能 | 可能 | - |
| advisor() 呼び出し | - | - | 可能 | 可能 | - | - |

*独自のサンドボックスモードのコンパニオンスクリプト経由
**ユーザーの確認が必要

---

## 7. コスト効率

### ルーティングによるトークン削減

| タスクタイプ | ルーティングなし | ルーティングあり | 削減率 |
|-----------|-----------------|--------------|---------|
| 単純作業 | Opus トークン | Ollama（無料） | 100% |
| ボイラープレート | Opus トークン | Haiku トークン | ~80% |
| 標準コード | Opus トークン | Sonnet トークン | ~50% |
| リサーチ | Claude トークン | Gemini トークン | ~70%（予算が異なる） |
| コードレビュー | advisor() トークン | Codex トークン | ~60%（予算が異なる） |

---

## 8. 黄金律

> "Opus が思考し、Sonnet が構築し、Haiku が実行し、Ollama が節約する。Gemini が調査し、Codex がレビューし、Fable が語る。"

---

## 変更履歴

### 2.0.0 (2026-06-12)
- クロスエージェント委任: Gemini、Codex、Ollama（ローカルホスト）をルーティングターゲットに追加
- アドバイザーペアリング: 4つのパターン（セッションアドバイザー、オーケストレーター兼レビュアー、カウンターエージェント、ユーザーへの推奨）を定義
- 到達可能性マトリクス: LLM起動可能とユーザー限定を明確にドキュメント化
- Ollama (Qwen 3.5:35b-a3b, HaikuからSonnetレベル) を Level 1-2 として追加
- 横方向エスカレーション: Sonnet -> Gemini（リサーチ）、Sonnet -> Codex（レビュー）
- 除外事項のドキュメント化（Gemini は数学非対応）
- スコアしきい値をすべてのモデルに拡張

### 1.0.0 (2026-03-15)
- BACH v3.8.0 (ing-strategie v2.0.0) から移植

---

*BACH v3.8.0 から移植 | クロスエージェント + アドバイザー v2.0.0 に拡張*
