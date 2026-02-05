---
name: internationalization
description: i18nやタイムゾーン処理を実装する際に使用。
---

# Internationalization

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] 多言語対応を行う?
- [ ] 日付・数値をフォーマットする?
- [ ] タイムゾーン処理を行う?
- [ ] RTL言語に対応する?

### 前提条件
- [ ] 対象言語・地域を決定したか?
- [ ] 翻訳ワークフローを検討したか?
- [ ] 日付・数値フォーマットを確認したか?

### 禁止事項の確認
- [ ] テキストをハードコードしようとしていないか?
- [ ] ローカルタイムゾーンを仮定しようとしていないか?
- [ ] 文字列連結で文を組み立てようとしていないか?

---

## トリガー

- 多言語対応時
- 日付・数値フォーマット時
- タイムゾーン処理時
- RTL言語対応時

---

## 🚨 鉄則

**最初から国際化を意識。後付けは困難。**

---

## テキスト外部化

```typescript
// ❌
const msg = 'ユーザーが見つかりません';

// ✅
const msg = t('errors.userNotFound');
const greeting = t('greeting', { name });
```

---

## 翻訳ファイル

```json
// locales/ja.json
{
  "greeting": "こんにちは、{{name}}さん",
  "errors": {
    "userNotFound": "ユーザーが見つかりません"
  }
}

// locales/en.json
{
  "greeting": "Hello, {{name}}",
  "errors": {
    "userNotFound": "User not found"
  }
}
```

---

## タイムゾーン

```typescript
// ⚠️ 常にUTCで保存
const utc = new Date().toISOString();

// 表示時にローカライズ
const local = new Intl.DateTimeFormat('ja-JP', {
  timeZone: 'Asia/Tokyo'
}).format(date);
```

---

## 🚫 禁止事項まとめ

- テキストのハードコード
- ローカルタイムゾーンの仮定
- 文字列連結での文組み立て
- 後付けの国際化対応
