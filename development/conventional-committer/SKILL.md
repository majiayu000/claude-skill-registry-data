---
name: conventional-committer
description: Conventional Commits仕様に従ったコミットメッセージを作成する。コミット時に必ず使用すること。
---

# Conventional Committer

## 指示

コミットメッセージは必ず以下のConventional Commits形式に従うこと:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Type

- **feat**: 新機能の追加
- **fix**: バグ修正
- **docs**: ドキュメントのみの変更
- **style**: コードの意味に影響しない変更（空白、フォーマット等）
- **refactor**: バグ修正や機能追加を伴わないコードの変更
- **perf**: パフォーマンス改善のためのコード変更
- **test**: テストの追加や修正
- **build**: ビルドシステムや外部依存関係に関する変更
- **ci**: CI設定ファイルやスクリプトの変更
- **chore**: srcやtestファイルを変更しないその他の変更

### 破壊的変更

破壊的変更がある場合は、typeの後に`!`を付けるか、フッターに`BREAKING CHANGE:`を追加する:

```
feat!: remove deprecated props from Button component

BREAKING CHANGE: The `variant` prop has been renamed to `appearance`
```

### ルール

1. descriptionは小文字で始める
2. descriptionは現在形で書く（"added"ではなく"add"）
3. descriptionの末尾にピリオドを付けない
4. scopeはコンポーネント名やパッケージ名など、変更の範囲を示す
5. 1行目は50文字以内を推奨
6. bodyには変更の理由や詳細を記述（オプション）

## 例

```bash
# 新機能
feat: add drag and drop support to Table component
feat(TextField): add maxLength validation

# バグ修正
fix(RadioItem): resolve checked state not updating
fix: resolve focus trap issue in Modal

# リファクタリング
refactor: simplify validation logic in Form
refactor(hooks): extract common logic to useFormState

# ドキュメント
docs: update README with new component examples
docs(TextField): add JSDoc comments

# 破壊的変更
feat!: remove deprecated variant prop from Button

BREAKING CHANGE: The `variant` prop has been removed. Use `appearance` instead.
```

## 注意事項

- このプロジェクトはLernaで`--conventional-commits`を使用しているため、コミットメッセージからCHANGELOGとバージョンが自動生成される
- 正しいtypeを使用しないと、適切なバージョンアップ（major/minor/patch）が行われない
- 絵文字は使用しない
