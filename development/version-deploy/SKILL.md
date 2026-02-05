---
name: version-deploy
description: アプリのバージョン更新とデプロイ。Next.js、Flutter、Firebase、Google Play、App Storeリリース時に使用。
---

# バージョン管理・デプロイスキル

## このスキルを使用するタイミング

- バージョン番号を更新するとき
- アプリをデプロイするとき
- ストア申請するとき

---

## 1. セマンティックバージョニング

```
MAJOR.MINOR.PATCH

1.0.0 → 2.0.0  # 破壊的変更
1.0.0 → 1.1.0  # 新機能追加
1.0.0 → 1.0.1  # バグ修正
```

---

## 2. Next.js

### バージョン更新
```json
// package.json
{ "version": "0.5.16" }
```

### デプロイ
```bash
# Vercel
git push origin main

# Firebase Hosting
npm run build
firebase deploy --only hosting
```

---

## 3. Flutter

### バージョン更新
```yaml
# pubspec.yaml
version: 1.3.1+42  # バージョン+ビルド番号
```

### ビルド
```bash
# Android AAB
flutter build appbundle --release

# iOS
flutter build ios --release
open ios/Runner.xcworkspace

# Web
flutter build web --release
```

---

## 4. リリースチェックリスト

- [ ] テスト完了
- [ ] Lintエラーなし
- [ ] バージョン番号更新
- [ ] ビルド番号増加（モバイル）
- [ ] CHANGELOG更新

---

## 5. リリースノート形式

```markdown
# v1.3.1

## 新機能
- 抽出タイマー機能を追加

## バグ修正
- タイマー停止問題を修正

## 改善
- パフォーマンス最適化
```

---

## AI アシスタント指示

1. 現在のバージョンを確認
2. 変更内容に基づいてインクリメント
3. ビルド番号は常に増加（モバイル）
4. デプロイ前にテスト確認
