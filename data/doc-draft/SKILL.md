---
name: doc-draft
description: outline.yamlなどの下書きを、テンプレートと過去の申請書を参考にして正式な文書（Markdown）に変換するスキル。「下書きを正式文書にして」「outline.yamlを正式文書にして」などの指示で発動。docxスキルを使用して過去の申請書（samples/配下）を読み込み、文体や表現を参考にする。
---

# Doc Draft

下書き（outline.yaml）を正式な申請書文書に変換する。

## ワークフロー

### 1. 入力ファイルの読み込み

`outline.yaml`を読み込み、研究の概要を把握する。

**outline.yamlの想定構造：**
```yaml
title: 研究課題名
title_en: English Title

summary: |
  研究の概要（箇条書きやメモ形式でOK）

background:
  - ポイント1
  - ポイント2

objectives:
  - 目的1
  - 目的2

methods:
  item1:
    name: 研究項目1
    description: 概要
    milestones:
      - マイルストーン1
      - マイルストーン2
  item2:
    name: 研究項目2
    description: 概要

expected_outcomes:
  - 期待される成果1
  - 期待される成果2
```

### 2. 参考文書の読み込み

`samples/`配下のdocxファイルを読み込み、文体・表現を学習する。

**docxファイルの読み込み方法：**
1. docxスキル（`~/.claude/skills/docx`）を使用
2. pandocまたはunpack.pyでテキスト抽出
3. 対応するセクションの文体を分析

```bash
# pandocが利用可能な場合
pandoc samples/past_application.docx -o /tmp/past_application.md

# または docxスキルのunpack.py
python ~/.claude/skills/docx/ooxml/scripts/unpack.py samples/past_application.docx /tmp/unpacked
```

### 3. テンプレートの参照

`doc-learn`スキルのテンプレートを参照し、出力構造を決定する。

参照: [../doc-learn/assets/template_amed.md](../doc-learn/assets/template_amed.md)

### 4. 文書生成

以下の方針で正式文書を生成する：

**文体の統一：**
- 過去の申請書から抽出した文体・表現を使用
- 「である」調で統一
- 専門用語の表記を統一

**セクション別の生成：**

| セクション | 入力元 | 参考 |
|-----------|--------|------|
| 要約 | summary | 過去の申請書の要約 |
| 研究の目的 | objectives | 過去の申請書の目的セクション |
| 背景 | background | 過去の申請書の背景セクション |
| 研究計画 | methods | 過去の申請書の計画セクション |
| 将来展望 | expected_outcomes | 過去の申請書の展望セクション |

**文字数制限の遵守：**
- 要約: 1000文字以内
- 研究の目的: 1000文字以内
- 研究開発の概要: 1000文字以内

### 5. 出力

生成した文書をMarkdownファイルとして出力する。

```
output/
└── draft_YYYYMMDD.md
```

## 使用例

```
ユーザー: outline.yamlを正式文書にして

Claude:
1. outline.yamlを読み込み
2. samples/配下の過去申請書をdocxスキルで読み込み
3. template_amed.mdの構造に従って文書生成
4. output/draft_YYYYMMDD.mdに出力
```

## 参考文書の配置

過去の申請書は`samples/`ディレクトリに配置する：

```
samples/
├── past_application_2024.docx
├── past_application_2023.docx
└── ...
```

## 依存スキル

- **docx**: Word文書の読み込みに使用
- **doc-learn**: テンプレート構造の参照
