---
name: "checking-breaking-changes-in-php-framework"
description: "外部公開を想定したphpフレームワークのコードレビューをする際に、破壊的変更（breaking change）の有無を確認し、破壊的変更がある場合は適切に処理されているかをチェックするスキルです。"
---

# Rules for Breaking Changes in PHP Framework

以下のルールに従って、コードレビュー時に変更が「破壊的変更」か否かを決定する。

## `@internal` tagがついていないクラス

- 公開API(public method)の引数追加やデフォルト値を設定する以外の変更
- APIが変わらない場合もAPI内部実装の変更によりAPIのレスポンスが変化する場合
- 抽象化等により型範囲が広がるが既存と同様のユースケースが可能な場合は破壊的変更扱いしない

## `@internal` tagがついているクラス

- 内部用の実装のため全ての公開APIの変更を破壊的変更扱いしない

## Code Review Checklist

- Pull Request が破壊的変更を含むかどうかをレビューに含めます
- 破壊的変更が行われている場合はその内容が Pull Request の CHANGELOG.md に適切に記載されていることを確認します
