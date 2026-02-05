---
name: expo-turso-dev
description: Expo + Turso + Drizzle ORMプロジェクトの開発コマンドと依存関係管理。アプリの起動、ライブラリのインストール、マイグレーション生成、キャッシュクリアなど開発コマンドを実行する時、または開発ワークフローについて質問された時に使用。重要：ライブラリインストールには必ずnpx expo installを使用。
---

# Expo Turso Dev

Expo + Turso (LibSQL) + Drizzle ORMプロジェクトの開発コマンドと依存関係管理のクイックリファレンス。

## 開発コマンド

このプロジェクトは`@antfu/ni`を使用してパッケージマネージャー（npm/yarn/pnpm/bun）を自動検出します。

### 開発サーバーの起動

```bash
# プラットフォーム選択付きで開発サーバーを起動
nr start

# 特定のプラットフォームで起動
nr ios        # iOSシミュレーター
nr android    # Androidエミュレーター
nr web        # Webブラウザ
```

### コード品質

```bash
# コードフォーマットとLint修正
nr lint
```

### データベース操作

```bash
# データベースマイグレーション生成（src/db/schema.ts修正後）
nr db:generate

# マイグレーションは次回アプリ起動時に自動適用される
# src/app/_layout.tsx内のDrizzleProviderによって実行
```

### キャッシュ管理

```bash
# Expoキャッシュをクリア（マイグレーションやビルドの問題時に有効）
npx expo start -c
```

## 依存関係のインストール

**重要: ライブラリ追加時は必ず`npx expo install`を使用してください。**

Expoのinstallコマンドは、プロジェクトのExpo SDKバージョン（~54.0.30）に基づいて互換性のあるバージョンを自動的に選択し、さらに使用中のパッケージマネージャー（このプロジェクトではbun）も自動検出します。

### 正しい方法

```bash
npx expo install <package-name>

# 例
npx expo install react-native-maps
```

### 間違った方法（避けるべき）

```bash
# ❌ パッケージマネージャーで直接インストールしない
npm install react-native-maps
yarn add react-native-maps
bun add react-native-maps
```

**理由**: パッケージマネージャーで直接インストールすると、互換性のないバージョンがインストールされ、Expoビルドが壊れたりランタイムエラーが発生する可能性があります。`npx expo install`コマンドはSDKとの互換性を保証します。

## コマンドリファレンス

- **`nr`**: スクリプト実行（`@antfu/ni`）- パッケージマネージャーを自動検出してnpm run/bun run等を実行
- **`npx expo`**: Expo CLI - パッケージマネージャーとSDKバージョンを自動検出

## プロジェクトコンテキスト

このプロジェクトで使用している技術:
- **Expo Router**: `src/app/`でのファイルベースルーティング
- **Turso (LibSQL)**: クラウドデータベース同期（オプション、iOS/Androidのみ）
- **Drizzle ORM**: タイプセーフなデータベース操作
- **expo-sqlite**: ローカルSQLiteデータベース

データベースは2つのモードで動作:
- **ローカルモード**: 環境変数不要、SQLiteのみ
- **Tursoモード**: `EXPO_TURSO_DB_URL`と`EXPO_TURSO_DB_AUTH_TOKEN`が設定されている場合、クラウドと同期
