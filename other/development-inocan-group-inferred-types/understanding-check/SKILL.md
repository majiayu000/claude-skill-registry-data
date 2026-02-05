---
name: understanding-check
description: タスク依頼時の理解確認システム（5W1H）。playbook 作成前にユーザーの意図を確認し、リスク分析と不明点の洗い出しを行う。pm SubAgent から呼び出される。
---

# Understanding Check Skill

タスク依頼を受けた際に、playbook 作成前に実施する理解確認フレームワーク。

## Purpose

- ユーザーの意図を正確に理解する
- 経験が浅いユーザーでもゴールに辿り着けるよう支援する
- 早期にリスクを特定し、対策を提案する
- 不明点を明確化し、手戻りを防ぐ

## When to Use

```yaml
# ★★★ タスク依頼時は必須実行 ★★★
必須実行:
  - タスク依頼パターン（作って/実装して/修正して/追加して/変更して）
  - 新しい playbook を作成する前
  - 複雑なタスクで要件が曖昧な場合
  - Phase 途中で新しい要件が追加された場合

不要:
  - 単純な質問（「〜とは？」「〜を教えて」）
  - 調査依頼（「〜を調べて」「〜を確認して」）
  - 既存タスクの継続（playbook に従った作業）
  - 情報提供のみ（「git status を見せて」）

skip_conditions:
  - ユーザーが「スキップして」「確認不要」「そのまま進めて」等を明示
  - 同一セッションで既に同じ要件の理解確認を実施済み
```

## 5W1H Framework

タスク理解の構造化フレームワーク:

```yaml
[理解確認]
5W1H:
  What: 何を作るか / 何を実現するか
  Why: なぜ作るか / どんな課題を解決するか
  Who: 誰が使うか / 誰が実行するか
  When: いつまでに / どのタイミングで必要か
  Where: どこに実装するか / どの領域に影響するか
  How: どのように実装するか / どんな技術・手法を使うか

リスク分析:
  - risk: "{リスク内容}"
    probability: low | medium | high
    impact: low | medium | high
    mitigation: "{対策案}"

不明点:
  - "{確認が必要な点}"

done_when:
  - "{検証可能な完了条件1}"
  - "{検証可能な完了条件2}"
```

## Output Template

pm SubAgent が理解確認を実施した結果を以下のフォーマットで出力:

```markdown
## 理解確認結果

### 5W1H 分析

| 項目 | 内容 |
|------|------|
| What | {具体的に何を作るか} |
| Why | {なぜ必要か、解決する課題} |
| Who | {利用者、実行者} |
| When | {期限、タイミング} |
| Where | {実装場所、影響範囲} |
| How | {実装方針、技術選定} |

### リスク分析

| リスク | 確率 | 影響 | 対策 |
|--------|------|------|------|
| {リスク1} | {low/medium/high} | {low/medium/high} | {対策案} |

### 不明点

- [ ] {確認が必要な点1}
- [ ] {確認が必要な点2}

### 提案する done_when

- {検証可能な完了条件1}
- {検証可能な完了条件2}

---

この理解で playbook を作成してよろしいですか？
```

## Structured Output Format

pm SubAgent が理解確認結果をメイン Claude に返す際、選択肢形式のユーザー確認を可能にする構造化データフォーマット。

### フォーマット定義

```yaml
understanding_check:
  summary: "{5W1H の要約}"

  questions:
    # 不明点確認（yes_no タイプ）
    - id: q1
      text: "{確認したい質問}"
      type: yes_no
      options:
        - label: "はい"
          description: "{はいを選んだ場合の意味}"
        - label: "いいえ"
          description: "{いいえを選んだ場合の意味}"

    # 実装方針選択（single_choice タイプ）
    - id: q2
      text: "{選択してほしい項目}"
      type: single_choice
      options:
        - label: "{選択肢1}"
          description: "{選択肢1の説明}"
        - label: "{選択肢2}"
          description: "{選択肢2の説明}"
        - label: "{選択肢3}"
          description: "{選択肢3の説明}"

    # 全体承認（approval タイプ）
    - id: q3
      text: "この理解で進めてよいですか？"
      type: approval
      options:
        - label: "はい、進めてください"
          description: "この内容で playbook を作成します"
        - label: "修正が必要"
          description: "修正点を入力してください"
```

### 選択肢タイプ

| タイプ | 用途 | 選択肢数 |
|--------|------|----------|
| `yes_no` | 不明点の確認（機能の要否など） | 2 |
| `single_choice` | 実装方針の選択（技術選定など） | 2-4 |
| `approval` | 全体の承認確認 | 2（承認/修正要求） |

### メイン Claude への連携フロー

```
1. pm SubAgent が understanding_check を YAML 形式で返す
2. メイン Claude が questions 配列を AskUserQuestion に変換:

   AskUserQuestion({
     questions: [
       {
         question: "{text}",
         header: "{短いラベル}",
         options: [...],
         multiSelect: false
       },
       ...
     ]
   })

3. ユーザーが選択肢から回答
4. 回答を pm SubAgent に渡して playbook 作成を継続
```

### 使用例

```yaml
understanding_check:
  summary: "ログイン画面にダークモード切り替えボタンを追加する"

  questions:
    - id: q1
      text: "ダークモードの設定を永続化しますか？"
      type: yes_no
      options:
        - label: "はい、localStorage に保存"
          description: "ブラウザを閉じても設定が保持されます"
        - label: "いいえ、セッション中のみ"
          description: "ページをリロードすると初期状態に戻ります"

    - id: q2
      text: "スタイルの実装方法を選んでください"
      type: single_choice
      options:
        - label: "CSS 変数（推奨）"
          description: "モダンで保守しやすい方式"
        - label: "クラス切り替え"
          description: ".light / .dark クラスを切り替え"
        - label: "Tailwind dark mode"
          description: "Tailwind CSS の dark: プレフィックス"

    - id: q3
      text: "この理解で playbook を作成してよいですか？"
      type: approval
      options:
        - label: "はい、進めてください"
          description: "この内容で playbook を作成します"
        - label: "修正が必要"
          description: "修正点を入力してください"
```

## Integration with pm.md

```yaml
# ★★★ 全プロンプトで理解確認必須 ★★★
pm_flow:
  step_0: ユーザープロンプトを受ける
  step_0.5: 理解確認（この Skill を必ず実行 - Phase 途中でも例外なし）
  step_1: ユーザー承認を得る
  step_2: playbook を作成する / 既存 playbook の作業を継続

理解確認_絶対ルール:
  - 全プロンプトで必須実行（例外なし）
  - Phase 途中でも新しいプロンプトには必ず実行
  - スキップ可能条件: ユーザーが明示的に「理解確認をスキップして」と発言した場合のみ
  - 不明点がある場合は AskUserQuestion で確認
  - リスクが高い場合はユーザーに警告
```

## Best Practices

1. **具体的に**: 抽象的な表現を避け、具体的な成果物・条件を記述
2. **検証可能**: done_when は「〜が存在する」「〜が動作する」等、検証可能な形式
3. **リスク重視**: 事前にリスクを洗い出すことで手戻りを防ぐ
4. **ユーザー確認**: 不明点は推測せず、ユーザーに確認する

## Example

```markdown
## 理解確認結果

### 5W1H 分析

| 項目 | 内容 |
|------|------|
| What | ユーザー認証機能（ログイン/ログアウト）を実装する |
| Why | 現在は誰でもアクセス可能であり、ユーザー別のデータ管理ができない |
| Who | 一般ユーザー（技術者ではない）が使用する |
| When | 今回のセッションで完了（期限なし） |
| Where | src/auth/ に新規ディレクトリを作成 |
| How | JWT 認証、bcrypt でパスワードハッシュ化 |

### リスク分析

| リスク | 確率 | 影響 | 対策 |
|--------|------|------|------|
| セキュリティ脆弱性 | medium | high | OWASP ガイドラインに従う |
| 既存ルートとの干渉 | low | medium | 影響範囲を事前調査 |

### 不明点

- [ ] パスワードリセット機能は必要か？
- [ ] セッション有効期限の要件は？

### 提案する done_when

- src/auth/ に認証モジュールが存在する
- /login, /logout エンドポイントが動作する
- テストが PASS する

---

この理解で playbook を作成してよろしいですか？
```

---

## ambiguity clarification（prompt-analyzer 連携）

> **prompt-analyzer の ambiguity を使って確認質問を明確化する**

### 入力

pm SubAgent から以下の情報を受け取る:

```yaml
analysis_result:
  ambiguity:
    - phrase: "{曖昧表現}"
      question: "{具体化のための確認質問}"
```

### ユーザー確認での使用

```markdown
### 不明点

- [ ] 「{曖昧表現}」とは具体的に何を指しますか？
- [ ] 「{曖昧表現}」の範囲に含めるもの／除外するものはありますか？
```

### Structured Output Format の拡張

```yaml
understanding_check:
  summary: "{5W1H の要約}"

  ambiguity_clarifications:
    - phrase: "{曖昧表現}"
      answer: "{ユーザー回答}"

  questions:
    - id: amb1
      text: "「{曖昧表現}」の意味を具体化してください"
      type: free_form
```
