---
name: kadoppe-constitution
description: "ALWAYS apply this skill for ANY software development task. Triggers: implement, create, build, add, write, code, function, class, component, API, feature, fix, bug, debug, refactor, improve, clean, review, check, design, architect, structure, test, endpoint, module, service, handler, controller, model, schema, migration, deploy, configure. This skill enforces kadoppe's development principles for all coding work."
---

# Software Development Constitution

This constitution defines the fundamental principles that govern all software development work. These principles are non-negotiable and must be followed at all times.

## Core Principles

### Test-Driven Development (TDD)

テスト駆動開発は必須プラクティスである。

- Red-Green-Refactor サイクルを厳守する
  1. テストを書く → ユーザー承認を得る → テストが失敗することを確認
  2. テストをパスする最小限の実装を行う
  3. リファクタリングを行う
- すべての新機能はテストから開始する
- テストカバレッジの目標: ビジネスロジック 80% 以上
- テストは仕様であり、ドキュメントでもある

### Simple Architecture (シンプルなアーキテクチャ)

Simple, but not easy. 本質的なシンプルさを追求する。

- YAGNI (You Ain't Gonna Need It): 将来の仮定的要件のためのコードは書かない
- 最小限の抽象化: 必要になるまで抽象化しない
- 3回目の繰り返しまで DRY を適用しない
- コードの行数よりも理解のしやすさを優先する

### Infrastructure as Code (IaC)

インフラストラクチャはコードとして定義・管理する。

- CI/CD パイプラインでインフラ変更を自動検証・適用する
- シークレットはバージョン管理に含めず、環境変数または専用サービスで管理する

### Full-Cycle Development (フルサイクル開発)

機能開発はインフラ・バックエンドからフロントエンドまで一貫して完結させる。

- 1つの機能は API → フロントエンド → テスト → デプロイまでを一連の作業として実装する
- 「バックエンドだけ」「フロントエンドだけ」の中途半端な状態でマージしない
- ユーザーストーリー単位で独立してデプロイ・デモ可能な状態を目指す

### CI/CD (継続的インテグレーション / 継続的デリバリー)

すべての変更は自動化されたパイプラインを通じて検証・デプロイする。

- すべてのPRは以下をパスしなければマージできない
  - 全テストの成功
  - リンター / フォーマッターのチェック
  - 型チェック（静的型付け言語の場合）
