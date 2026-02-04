---
name: k8s-agent-sandbox
description: Documentation for Kubernetes Agent Sandbox - a CRD-based system for managing isolated AI agent execution environments. Use for queries about Sandbox CRDs (Sandbox, SandboxTemplate, SandboxClaim, SandboxWarmPool), Python SDK (SandboxClient, SandboxRouter, ComputerUseExtension), network policies, security configurations, and implementation examples. Keywords kubernetes sandbox, agent sandbox, CRD, python sdk, agentic-sandbox-client, isolated environment, gvisor, network policy.
allowed-tools: Read, Grep, Glob, WebSearch
---

# Kubernetes Agent Sandbox

AIエージェントのための、Kubernetes上の分離された実行環境を管理するCRDとコントローラー。

**リポジトリ**: https://github.com/kubernetes-sigs/agent-sandbox

## 主な機能

- **Sandbox** (Core): ステートフルPodのライフサイクル管理
- **拡張機能**: SandboxTemplate (テンプレート), SandboxClaim (オンデマンド作成), SandboxWarmPool (プリウォーム)
- **Python SDK**: Kubernetes上のSandboxと対話するクライアント
- **NetworkPolicy統合**: ネットワーク分離によるセキュア実行環境

## アーキテクチャ概要

```
Core (agents.x-k8s.io)
  └─ Sandbox → Pod, Service, PVC管理

Extensions (extensions.agents.x-k8s.io)
  ├─ SandboxTemplate → テンプレート + NetworkPolicy
  ├─ SandboxClaim → テンプレートから作成
  └─ SandboxWarmPool → プール管理

Client: Python SDK → Sandbox Router → Sandbox Pod
```

**詳細**: `./references/README.md`

---

# CRD Reference Map

## Sandbox (agents.x-k8s.io/v1alpha1)

**目的**: 単一ステートフルPod + Service + PVC管理

**主要Specフィールド**:
- `podTemplate.spec` (必須) - Pod仕様
- `volumeClaimTemplates` - PVCテンプレート
- `shutdownTime` - 自動削除時刻 (RFC 3339)
- `replicas` - 0または1

**Statusフィールド**: `serviceFQDN`, `service`, `conditions`, `replicas`

**検索**:
```bash
grep -A 15 "## Spec フィールド" ./references/CRDs/Sandbox.md
grep -A 15 "## 最小構成例" ./references/CRDs/Sandbox.md
```

**詳細**: `./references/CRDs/Sandbox.md`

---

## SandboxTemplate (extensions.agents.x-k8s.io/v1alpha1)

**目的**: 再利用可能テンプレート + NetworkPolicy

**主要Specフィールド**:
- `podTemplate` (必須) - Pod定義
- `networkPolicy.ingress` - Ingressルール
- `networkPolicy.egress` - Egressルール

**セキュア構成例**:
```yaml
spec:
  podTemplate:
    spec:
      runtimeClassName: gvisor
  networkPolicy:
    egress:
      - ports:
        - protocol: UDP
          port: 53  # DNS のみ
```

**検索**:
```bash
grep -A 40 "## セキュアな設定例" ./references/CRDs/SandboxTemplate.md
```

**詳細**: `./references/CRDs/SandboxTemplate.md`

---

## SandboxClaim (extensions.agents.x-k8s.io/v1alpha1)

**目的**: SandboxTemplateからSandbox作成要求

**主要Specフィールド**:
- `sandboxTemplateRef.name` (必須) - SandboxTemplate名
- `sandboxTemplateRef.namespace` - namespace

**Statusフィールド**: `sandboxName`, `conditions`

**Python SDK統合**: `SandboxClient`が内部的に使用

**検索**:
```bash
grep -A 20 "## 動作フロー" ./references/CRDs/SandboxClaim.md
```

**詳細**: `./references/CRDs/SandboxClaim.md`

---

## SandboxWarmPool (extensions.agents.x-k8s.io/v1alpha1)

**目的**: Sandboxプール (コールドスタート削減)

**主要Specフィールド**:
- `replicas` (必須) - プール内Sandbox数
- `sandboxTemplateRef.name` (必須) - SandboxTemplate名

**Statusフィールド**: `replicas`, `readyReplicas`, `conditions`

**検索**:
```bash
grep -A 20 "## HPA" ./references/CRDs/SandboxWarmPool.md
```

**詳細**: `./references/CRDs/SandboxWarmPool.md`

---

# Python SDK Reference

## インストール

```bash
pip install "git+https://github.com/kubernetes-sigs/agent-sandbox.git@main#subdirectory=clients/python/agentic-sandbox-client"
```

## SandboxClient

**コンストラクタ主要パラメータ**:

| パラメータ       | 型           | デフォルト | 説明                      |
| ---------------- | ------------ | ---------- | ------------------------- |
| `template_name`  | str          | (必須)     | SandboxTemplate名         |
| `namespace`      | str          | "default"  | namespace                 |
| `gateway_name`   | str \| None  | None       | Gateway名 (Production)    |
| `api_url`        | str \| None  | None       | 直接URL (Direct)          |
| `server_port`    | int          | 8888       | Sandboxサーバーポート     |

**コアメソッド**:

| メソッド                    | 戻り値            | 説明             |
| --------------------------- | ----------------- | ---------------- |
| `run(command, timeout=60)`  | `ExecutionResult` | コマンド実行     |
| `write(path, content, ...)`| None              | ファイル書き込み |
| `read(path, timeout=60)`   | bytes             | ファイル読み込み |
| `is_ready()`                | bool              | 接続確認         |

**接続モード**:
- **Tunnel** (デフォルト): kubectl port-forward - ローカル開発用
- **Gateway**: gateway_name指定 - 本番環境用
- **Direct**: api_url指定 - クラスタ内部用

**使用例**:
```python
from agentic_sandbox import SandboxClient

with SandboxClient(template_name="python-sandbox-template") as sandbox:
    result = sandbox.run("python -c 'print(42)'")
    print(result.stdout)  # "42\n"

    sandbox.write("/tmp/test.py", "print('Hello')")
    result = sandbox.run("python /tmp/test.py")
```

**検索**:
```bash
grep -A 15 "^```python" ./references/python-sdk/SandboxClient.md
grep -A 30 "## 内部動作" ./references/python-sdk/SandboxClient.md
```

**詳細**: `./references/python-sdk/SandboxClient.md`

---

## SandboxRouter

**目的**: X-Sandbox-IDヘッダーベース動的ルーティングプロキシ

**詳細**: `./references/python-sdk/SandboxRouter.md`

## ComputerUseExtension

**目的**: Gemini Computer Use統合 (`agent(query: str)`メソッド)

**詳細**: `./references/python-sdk/ComputerUseExtension.md`

---

# Implementation Examples Index

**場所**: `./references/examples/`

| 例                     | 難易度 | ユースケース                      | ファイル                                          |
| ---------------------- | ------ | --------------------------------- | ------------------------------------------------- |
| python-runtime-sandbox | ⭐     | 基本コマンド実行API               | `./references/examples/python-runtime-sandbox.md` |
| aio-sandbox            | ⭐     | All-in-One (VNC, VSCode, Jupyter) | `./references/examples/aio-sandbox.md`            |
| gemini-cu-sandbox      | ⭐⭐   | Gemini Computer Use (ブラウザ)    | `./references/examples/gemini-cu-sandbox.md`      |
| vscode-sandbox         | ⭐⭐   | VSCode + gVisor/Kata分離          | `./references/examples/vscode-sandbox.md`         |

## python-runtime-sandbox (⭐)
最小FastAPI実装。`/execute`, `/upload`, `/download` エンドポイント。カスタムランタイムの出発点。

## aio-sandbox (⭐)
VNC, VSCode Server, Jupyter統合環境。`agent-infra/sandbox` ベース。

## gemini-cu-sandbox (⭐⭐)
Gemini Computer Use。`/agent` エンドポイントで自然言語タスク実行。要: Gemini API keySecret。

## vscode-sandbox (⭐⭐)
VSCode Server + gVisor/Kata。Sandbox Router経由アクセス。

**検索**:
```bash
grep -A 10 "## API" ./references/examples/<example-name>.md
grep -A 20 "## マニフェスト" ./references/examples/<example-name>.md
```

---

# Common Query Patterns

## "セキュアなSandboxを作成するには？"
→ SandboxTemplate + gVisor + NetworkPolicy (DNS egress のみ)

```bash
grep -A 40 "## セキュアな設定例" ./references/CRDs/SandboxTemplate.md
```

## "[CRD名] のフィールドは？"
→ CRD Reference Map参照、または:
```bash
grep -A 20 "## Spec フィールド" ./references/CRDs/<CRD名>.md
```

## "Sandboxに接続するには？"
→ `SandboxClient(template_name="...")` 使用 (上記Python SDK参照)

## "特定ランタイム実装は？"
→ Implementation Examples Index参照
```bash
ls ./references/examples/*.md
```

## "NetworkPolicy設定は？"
→ ingress/egress定義 (デフォルト全拒否)
```bash
grep -A 10 "### NetworkPolicySpec" ./references/CRDs/SandboxTemplate.md
```

---

# How to Use This Skill

## ファイル構成

```
skills/references/
├── README.md              # プロジェクト概要 (94行)
├── CRDs/
│   ├── README.md            # CRD一覧 (63行)
│   ├── Sandbox.md           # (101行)
│   ├── SandboxTemplate.md   # (122行)
│   ├── SandboxClaim.md      # (75行)
│   └── SandboxWarmPool.md   # (97行)
├── python-sdk/
│   ├── README.md            # (23行)
│   ├── SandboxClient.md     # (161行)
│   ├── SandboxRouter.md     # (57行)
│   └── ComputerUseExtension.md # (51行)
└── examples/
    ├── README.md            # (50行)
    ├── python-runtime-sandbox.md # (76行)
    ├── aio-sandbox.md       # (87行)
    ├── gemini-cu-sandbox.md # (102行)
    └── vscode-sandbox.md    # (82行)
```

**合計**: 16ファイル、~1,147行

## 検索戦略

### API/フィールドクエリ
1. SKILL.mdのCRD Reference Map確認
2. grepで詳細抽出
3. 必要なら完全ファイル読み込み

### 実装ガイダンス
1. Common Query Patterns確認
2. Implementation Examples Index参照
3. 該当例ファイル読み込み

### SDK使用方法
1. Python SDK Reference確認
2. 基本用法はSKILL.mdで完結
3. 高度な用法はgrepまたはファイル読み込み

## 優先度

**Tier 1** (最頻):
- `./references/python-sdk/SandboxClient.md`
- `./references/CRDs/Sandbox.md`
- `./references/CRDs/SandboxTemplate.md`

**Tier 2** (コンテキスト):
- `./references/README.md`
- `./references/examples/python-runtime-sandbox.md`

**Tier 3** (オンデマンド): その他

## Web フォールバック

**ローカル不十分時**:

**CodeWiki**: https://codewiki.google/github.com/kubernetes-sigs/agent-sandbox

**使用時**:
- references/に無い実装詳細
- 最新変更/アップデート
- 高度なトラブルシューティング
- Controller実装詳細

## 便利なgrep パターン

```bash
# 全CRDのSpecフィールド
grep -A 15 "## Spec フィールド" ./references/CRDs/*.md

# YAML例検索
grep -n "^```yaml" ./references/CRDs/<file>.md

# NetworkPolicy
grep -A 30 "networkPolicy" ./references/CRDs/SandboxTemplate.md

# Python例
grep -A 15 "^```python" ./references/python-sdk/*.md

# 全体検索
grep -r "keyword" ./references/
```

## 言語注記

- ドキュメント: **日本語**
- grepキーワード: 日本語 (例: "フィールド", "設定例")
- セクションヘッダー: `##` 統一
- コード例: 言語非依存

## バージョン

- CRD: `v1alpha1`
- 更新: 2025-12-21
- ソース: kubernetes-sigs/agent-sandbox (main)
