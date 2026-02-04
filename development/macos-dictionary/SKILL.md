---
name: macos-dictionary
description: |
  查詢 macOS 內建字典（日文、中文、英文）。
  使用時機：當用戶詢問日文單字的讀音、詞性、定義，英文詞彙的中日文翻譯，或中文詞彙的英文翻譯時。
  關鍵字：查字典、怎麼唸、什麼意思、日文定義、詞性、用日文解釋、英翻日、英翻中、中翻英。
---

# macOS 多語字典查詢

使用 macOS DictionaryServices API 查詢多語字典。

## 支援的字典

| 字典 | 查詢方向 | 提供資料 |
|------|----------|----------|
| スーパー大辞林 | 日→日 | 讀音、詞性、日文定義 |
| ウィズダム和英辞典 | 日→英 | 英文翻譯 |
| ウィズダム英和辞典 | 英→日 | 日文翻譯 |
| 國語辭典 | 中→中 | 注音、解釋 |
| 譯典通英漢雙向字典 | 英↔中 | 翻譯 |

## 使用方式

```bash
# JSON 格式（預設）
uv run scripts/lookup-dictionary.py 食べる

# 原始字典文字
uv run scripts/lookup-dictionary.py 食べる --raw

# 英文查詢
uv run scripts/lookup-dictionary.py "national debt"

# 中文查詢（繁體）
uv run scripts/lookup-dictionary.py 經濟
```

## 輸出格式

```json
{
  "query": "食べる",
  "found": true,
  "sources": { "daijirin": true, "waei": true },
  "data": {
    "reading": "たべる",
    "kanji": "食べる",
    "pos": "動詞",
    "pos_details": "一段動詞（下一段）",
    "definition_ja": "食物を口に入れ...",
    "definition_en": "eat; have a meal"
  }
}
```

## 回應流程

1. 執行腳本查詢詞彙
2. 解析 JSON 結果
3. 依據詞彙類型選擇適當格式回應
4. 加入 AI 補充的中文翻譯和例句

**回應格式詳見**：[references/output-format.md](references/output-format.md)

## 特殊情況處理

### 中日共用漢字

某些漢字詞彙在中文和日文意思不同（如「勉強」「大丈夫」），字典可能返回中文結果。

**處理方式**：
1. 用 `--raw` 檢查結果是否包含注音符號
2. 若為中文結果，改用假名重新查詢
3. 若仍無法取得日文結果，使用 AI 知識補充

**詳見**：[references/cjk-handling.md](references/cjk-handling.md)

### 查不到的情況

- 專有名詞、新詞、複合詞可能查不到
- 簡體字查不到（需轉換為繁體）
- 使用 AI 知識回答，並標註「字典未收錄」

## 限制

- 僅限 macOS
- 需在「字典」應用程式中啟用日文字典

## 技術文檔

詳細 API 說明：`doc/macos-dictionary-services.md`
