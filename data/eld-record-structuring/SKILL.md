---
name: eld-record-structuring
description: |
  PCE (Process-Context Engine) のコンテキスト構造化スキル。収集した知識を適切な場所・粒度で構造化し、再利用可能にする。

  トリガー条件:
  - 「CLAUDE.mdを更新して」
  - 「ADRを整理して」
  - 「知識を構造化して」
  - 「pce-memoryに登録して」
  - pce-collectionで蓄積された知見の整理時
---

# PCE Structuring Skill

収集した知識を適切な構造で永続化し、後続プロセスで参照可能にする。

## 構造化の原則

1. **適切な粒度**: 1つの記録 = 1つの関心事
2. **検索可能性**: 後で見つけられるタグ/キーワード
3. **文脈保持**: なぜそうなったかの経緯
4. **鮮度管理**: 最終更新日と有効期限

## 出力先と形式

### 1. pce-memory (即時参照用)
```
pce_memory_upsert:
  category: pattern | decision | error | rule
  content: 構造化された知識
  tags: [検索用タグ]
```

### 2. CLAUDE.md (プロジェクト指針)

**ルートCLAUDE.md** - 一般化された原則
```markdown
## 設計原則
- 原則1: 理由と適用範囲

## コーディング規約
- ...
```

**フォルダCLAUDE.md** - ドメイン固有
```markdown
## このモジュールの責務
- ...
```

### 3. ADR (アーキテクチャ決定記録)
```markdown
# ADR-XXX: タイトル

## Status
Accepted | Deprecated | Superseded by ADR-YYY

## Context
決定が必要になった背景

## Decision
決定内容

## Consequences
結果と影響
```

## 構造化ワークフロー

1. 収集された知見を分類
2. 出力先を決定（pce-memory / CLAUDE.md / ADR）
3. 適切なフォーマットで記録
4. 関連する既存知識との整合性確認

## 整理のタイミング

- セッション終了時
- マイルストーン完了時
- 知見が5件以上蓄積した時
- 明示的な整理依頼時

---

## 品質優先原則（Superpowers統合）

### 核心原則

1. **Epistemic Humility**: 推測を事実として扱わない。`unknown`と言う勇気を持つ
2. **Evidence First**: 結論ではなく因果と証拠を中心にする
3. **Minimal Change**: 最小単位で変更し、即時検証する
4. **Grounded Laws**: Lawは検証可能・観測可能でなければならない
5. **Source of Truth**: 真実は常に現在のコード。要約はインデックス

### 「速さより質」の実践

- 要件の曖昧さによる手戻りを根本から排除
- テストなし実装を許さない
- 観測不能な変更を防ぐ

### 完了の定義

- [ ] Evidence Ladder目標レベル達成
- [ ] Issue Contractの物差し満足
- [ ] Law/Termが接地している（Grounding Map確認）
- [ ] Link Mapに孤立がない
- [ ] ロールバック可能な状態

### 停止条件

以下が発生したら即座に停止し、追加計測またはスコープ縮小：

- 予測と現実の継続的乖離（想定外テスト失敗3回以上）
- 観測不能な変更の増加（物差しで検証できない変更）
- ロールバック線の崩壊（戻せない変更の発生）
