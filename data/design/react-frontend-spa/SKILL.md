---
name: react-frontend-spa
description: ReactでSPAフロントエンドを実装・改修するためのガイド。バックエンド分離前提でNext.jsやサーバーサイド機能に依存せず、React Router中心のクライアント実装を行う時に使う。認証はAuthProviderとuseAuthカスタムフックで統一し、OpenAPIからorvalまたはopenapi-typescriptで型/クライアントを生成して利用する。ESLint+Prettier、zod、shadcn/ui、デザイントークン（CSS変数/Tailwindテーマ）を前提にする場合に適用する。ディレクトリ構成はmodules/components/hooks/providers/servicesなどの直感的な命名で複雑化に耐える構成にする。
---

# React Frontend SPA

## 目的

ReactのSPAを、型安全・一貫性・保守性重視で構築するための実装指針を提供する。

## 基本方針

- SSRやサーバーサイド機能に依存しない。ルーティングはReact Routerで完結させる。
- TypeScriptを必須とし、strictを有効にする。
- UIはshadcn/uiを基準にし、デザイントークンで一貫性を保つ。
- バリデーションはzodを基本とする。
- APIクライアントはOpenAPIから自動生成し、手書きの型定義は避ける。

## 参照ドキュメント

詳細は references に分離してある。必要に応じて読む。

- `references/structure.md` ディレクトリ構成と依存ルール、modules指針
- `references/auth.md` 認証（AuthProvider / useAuth / ProtectedRoute）
- `references/api-client.md` OpenAPIクライアント生成（orval / openapi-typescript）
- `references/validation.md` zodによるバリデーション方針
- `references/ui-design.md` shadcn/ui とデザイントークン運用
- `references/quality.md` ESLint/Prettier/型チェック

## 実装時の判断基準

- 迷ったら「生成コードに寄せる」「再利用はcomponents/hooksへ」「機能はmodulesへ」で整理する。
- 既存の命名や語彙に揃える。新規語彙は最小限にする。
