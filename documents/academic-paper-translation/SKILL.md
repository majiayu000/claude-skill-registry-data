---
name: academic-paper-translation
version: 1.0.0
description: 外国語論文の精読時・一次文献レビュー時に、設定ファイル (config/user_preferences.json) に定義された自国語に基づき、学術的客観性・対訳対照・専門用語集 (Glossary) 付きで構造化翻訳するスキル
---

# 学術論文 自国語翻訳・対訳対照スキル (Academic Paper Translation)

## 目的
設定ファイル [`config/user_preferences.json`](../../../config/user_preferences.json) にて定義されたユーザーの自国語（デフォルト: `Japanese` / `ja`）に基づき、外国語（英語・ドイツ語・フランス語・ラテン語等）の論文本文やPDF変換済みMarkdownを、学術的客観性・専門用語の対訳表（Glossary）を維持したまま自国語へ構造化翻訳・解読する。

## 発動タイミング
- 外国語論文の精読を開始する時
- 文献レビューに外国語の一次文献を組み込む時

## 設定と変更
自国語の設定や翻訳スタイルの変更は、同梱スクリプト [`scripts/manage_user_config.py`](../../../scripts/manage_user_config.py) または [`config/user_preferences.json`](../../../config/user_preferences.json) で行います：

```bash
# 現在の言語設定を表示 (サブモジュール導入時: python3 .scholarly-agent-skills/scripts/manage_user_config.py --show)
python3 scripts/manage_user_config.py --show

# 自国語を「日本語 (ja)」に設定
python3 scripts/manage_user_config.py --set-language "Japanese" --set-code "ja"

# 自国語を「ドイツ語 (de)」等へ変更する場合
python3 scripts/manage_user_config.py --set-language "German" --set-code "de"
```

> [!NOTE]
> サブモジュール導入先のリポジトリから実行する場合は、パス頭に `.scholarly-agent-skills/` を付与してください（例: `python3 .scholarly-agent-skills/scripts/manage_user_config.py`）。

## 翻訳の4大規律 (Scholarly Translation Discipline)

1. **常体・学術スタイルの維持**:
   自国語への翻訳時は、論文の常体（日本語の場合は「である調」）を使用し、客観的かつ厳密な学術文体で統一する。
2. **原文専門用語の併記 (Preserve Original Terms)**:
   多義的な概念や原語依存のキーワード（例: *Hermeneutics*, *Dasein*, *Epistemic Injustice*）は、初出時に「自国語訳 (原語)」の形式で併記する。
3. **対訳・パラレル出力 (Bilingual Parallel Output)**:
   重要な段落や引用箇所については、原文（Original Text）と自国語訳（Translated Text）を上下に対照表記し、原文批判や引用時の確認を容易にする。
4. **専門用語対照表（Bilingual Glossary）の蓄積**:
   翻訳の過程で登場した主要専門用語・概念を `docs/bilingual-glossary.md` に蓄積し、論文全体での用語訳の表記揺れを防ぐ。

## 処理手順

### Step 1: 原文テキストの読み込み
`pdf-paper-ingestion` スキルで抽出された Markdown または論文原稿ファイルを指定。

### Step 2: 段落ごとの対訳生成
AIは自国語設定を適用し、以下の形式で段落ごとの対照翻訳を生成する：

```markdown
> **Original**: Large Language Models risk institutionalizing epistemic injustice when deployed as conversational tutors.
> **翻訳 (Japanese)**: 大規模言語モデル（LLM）は、対話型チューターとして運用される際、認識的不当性（epistemic injustice）を制度化するリスクを負っている。
```

### Step 3: 用語対照表 (`docs/bilingual-glossary.md`) への追加
新しく登場した学術用語を記録：

```markdown
| 原語 (Original Term) | 自国語訳 (Native Translation) | 本稿における解釈・コンテキスト |
|---|---|---|
| Epistemic Injustice | 認識的不当性 | Fricker(2007)の概念。証言の信頼性が過小評価される状態 |
| Hermeneutics | 解釈学 | テキストや歴史的言説の文脈的読解・理解の理論 |
```

## 成果物
- `docs/translated_[paper_name].md` (対訳対照論文ファイル)
- `docs/bilingual-glossary.md` (学術用語対訳インベントリ)

