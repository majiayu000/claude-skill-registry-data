---
name: "Nemotron-Instagram Persona Analyzer"
description: "Nemotron-Personas-Japan (1M件) から最適ペルソナを選定し、Instagram実データで検証・統合する全自動ペルソナ分析Skill。Instagram分析、ペルソナ作成依頼時に自動起動。"
---

# Nemotron-Instagram Persona Analyzer Skill

## 概要

このSkillは、統計的に裏付けされたNemotronペルソナとInstagram実データを統合し、信頼性の高いペルソナプロファイルを自動生成します。

## 自動実行フロー

```
1. Nemotron (1M件)
   ↓ フィルタリング・スコアリング
2. 選定ペルソナ (3-10件)
   ↓ キーワード生成
3. Instagram検索クエリ
   ↓ Apify API
4. Instagram実データ (投稿・プロフィール)
   ↓ 統合・矛盾チェック
5. 統合ペルソナ (信頼性スコア付き)
```

## 起動条件

以下のようなユーザーリクエストで自動起動:
- "30代のITエンジニアのペルソナを作成"
- "転職を検討している20代のInstagram分析"
- "東京在住のフリーランスデザイナーのペルソナ"
- "Nemotronデータからペルソナ抽出"

## 機能

### 1. Nemotronペルソナ選定
- HuggingFace `nvidia/Nemotron-Personas-Japan` から選定
- 年齢、職業、都道府県、キャリア目標でフィルタリング
- 関連性スコア (0-100点) で自動ランキング
- 多様性確保ロジック (同一職業最大2件等)

### 2. Instagram キーワード生成
- 職業、キャリア目標、趣味から自動生成
- 日本語70%、英語30%の最適比率
- Apify Instagram API 対応フォーマット

### 3. Instagram データ取得
- Apify Instagram API 自動呼び出し
- 投稿・プロフィール・ハッシュタグ・エンゲージメント取得
- エラーハンドリング・リトライ機能

### 4. データ統合・信頼性評価
- Nemotron + Instagram データ統合
- 信頼性スコア算出 (100点満点)
  - Nemotron統計的裏付け: 40点
  - Instagram実データ検証: 40点 (投稿数・プロフィール数)
  - 整合性チェック: 20点
- 矛盾検出 (年齢vs投稿内容、職業vsハッシュタグ等)

### 5. Markdown レポート生成
- 基本情報、デモグラフィック、キャリア情報
- Instagram投稿分析 (頻出ハッシュタグ、エンゲージメント)
- 実際の悩み・課題抽出
- データソース明記、整合性チェック結果

## 実行方法

### Pythonスクリプト経由 (推奨)

```python
from core.nemotron_instagram_pipeline import NemotronInstagramPipeline

# 初期化
pipeline = NemotronInstagramPipeline()

# 全自動実行
result = pipeline.run("30代のITエンジニア", max_personas=3)

# レポート保存
with open("persona_report.md", "w", encoding="utf-8") as f:
    f.write(result["markdown_report"])
```

### Claude Code 自動起動

ユーザーがペルソナ分析を依頼すると、このSkillが自動的に起動し、上記フローを実行します。

## 出力

### 成功時

```markdown
# 統合ペルソナプロファイル

## 信頼性スコア: 85/100

## 基本情報
- 年齢: 28歳
- 性別: 男性
- 居住地: 東京都 (関東)

## Instagram 投稿分析
- 投稿数: 52件
- 頻出ハッシュタグ: #ITエンジニア, #転職, #キャリアチェンジ, #プログラミング
- 平均いいね数: 125.3
- 平均コメント数: 8.7

## 実際の悩み・課題
1. "転職活動でスキルの棚卸しに苦労している..."
2. "現職の将来性に不安がある..."

## データソース
- Nemotron ペルソナ: ✅
- Instagram データ: ✅ (52投稿、10プロフィール)

## 整合性チェック
- ✅ 矛盾なし
```

### エラー時

- Nemotronデータ取得失敗 → フォールバック (代替データソース)
- Instagram API失敗 → Nemotronのみで統合 (信頼性スコア40点)
- 矛盾検出 → 警告付きレポート

## 依存関係

### Python パッケージ

```
datasets>=2.14.0
requests>=2.31.0
python-dotenv>=1.0.0
```

### 環境変数

```bash
APIFY_API_TOKEN=apify_api_XXXXXXXXXXXX
```

## ファイル構成

```
.skills/nemotron-instagram-persona/
├── SKILL.md                          # このファイル
├── core/
│   ├── nemotron_instagram_pipeline.py  # 全自動実行パイプライン
│   ├── apify_client.py                 # Apify API クライアント
│   └── __init__.py
├── resources/
│   ├── workflow_guide.md               # 詳細ワークフローガイド
│   ├── quality_criteria.md             # 品質基準
│   └── troubleshooting.md              # トラブルシューティング
└── config/
    └── keyword_mapping.json            # キーワードマッピング設定
```

## 品質基準

- **信頼性スコア80点以上**: 高信頼性ペルソナとして採用推奨
- **投稿数50件以上**: Instagram実データ十分
- **矛盾なし**: Nemotronとの整合性確認済み

詳細は `resources/quality_criteria.md` を参照。

## トラブルシューティング

一般的な問題と解決策は `resources/troubleshooting.md` を参照。

## 更新履歴

- **2025-01-19**: 初版作成
  - Nemotron選定、Instagram API、統合機能実装
  - 信頼性スコア算出ロジック実装
  - 矛盾検出機能実装

---

*このSkillは既存の `lib/` モジュール (nemotron_persona_selector.py, instagram_keyword_generator.py, persona_integrator.py) を統合したものです。*
