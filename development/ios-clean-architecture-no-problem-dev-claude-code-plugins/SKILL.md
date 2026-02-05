---
name: ios-clean-architecture
description: iOSアプリのSPMパッケージ構成・レイヤー依存関係・設計原則を定義。iOS機能実装・コードレビュー時に参照。no problem製SPMパッケージの使用指針を含む。
---

# iOS Clean Architecture

iOSアプリのクリーンアーキテクチャに基づくパッケージ構成と設計原則。

## パッケージ依存図

```
                    ┌─────────────────┐
                    │  Presentation   │  SwiftUI Views, Components
                    └────────┬────────┘
                             │
    ┌───────────┬────────────┼────────────┬───────────┐
    ▼           ▼            ▼            ▼           ▼
┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│ State  │ │UseCases│ │Repository│ │ Services │ │  External    │
│        │ │        │ │          │ │          │ │  SPM (4)     │
└────┬───┘ └────┬───┘ └────┬─────┘ └────┬─────┘ └──────────────┘
     │          │    ↘     │      ↙     │
     │          └─────┬────┴──────┬─────┘
     │                ▼           │
     │       ┌──────────────┐     │
     └──────►│    Domain    │◄────┘
             └──────────────┘
```

**注**: UseCasesはRepository・Servicesの両方に依存可能。ServicesはDomainのみに依存。

## ローカルパッケージ（6つ）

| パッケージ | 責務 | 依存先 |
|-----------|-----|--------|
| **Domain** | ドメインモデル・値オブジェクト・列挙型 | なし |
| **Services** | 再利用可能なアプリケーションサービス（外部SDK連携等） | Domain のみ |
| **Repository** | API通信・データ永続化 | Domain, APIClient |
| **State** | @Observable状態管理 | Domain, Authentication |
| **UseCases** | ビジネスロジック（Protocol定義） | Domain, Repository, Services |
| **Presentation** | SwiftUI View・コンポーネント | 全て |

### Services層の原則

- **Domainのみに依存**: Repositoryや他のパッケージへの依存は禁止
- **再利用可能**: 複数のUseCaseから利用される共通機能を提供
- **外部SDK連携**: HealthKit, CoreLocation, Analytics等のラッパー

## no problem製外部SPM（4つ）

| パッケージ | モジュール名 | 用途 | 使用レイヤー |
|-----------|------------|-----|------------|
| `swift-design-system` | DesignSystem | テーマ・色・スペーシング・UIコンポーネント | Presentation |
| `swift-authentication` | Authentication | Firebase Auth統合（Google/Apple Sign-In） | State, Presentation |
| `swift-ui-routing` | UIRouting | 型安全ナビゲーション（Router, TabPresenter） | Presentation |
| `swift-api-client` | APIClient | HTTP通信クライアント | Repository |

## 依存ルール（厳守）

### 許可される依存

```swift
// ✅ Presentation → 全て（最上層）
import Domain
import State
import UseCases
import Repository
import DesignSystem
import UIRouting
import Authentication

// ✅ UseCases → Domain + Repository + Services
import Domain
import Repository
import Services

// ✅ State → Domain + Authentication
import Domain
import Authentication

// ✅ Repository → Domain + APIClient
import Domain
import APIClient

// ✅ Services → Domain（外部サービス連携）
import Domain

// ✅ Domain → なし（最下層）
// 外部依存ゼロ（Foundationのみ許可）
```

### 禁止される依存

```swift
// ❌ Domain層での外部import
import Foundation  // ✅ OK（標準ライブラリ）
import UIKit       // ❌ 禁止
import SwiftUI     // ❌ 禁止
import DesignSystem // ❌ 禁止

// ❌ 下位レイヤーから上位への参照
import Presentation // ❌ 循環依存

// ❌ UseCases → State
import State // ❌ 状態管理は上位レイヤーの責務

// ❌ Services → Repository（Servicesは独立性を保つ）
import Repository // ❌ ServicesはDomainのみに依存
```

## 設計違反チェックリスト

実装前に確認：

- [ ] **Domain層にUI依存を追加していないか？**
- [ ] **Repositoryから直接Viewを参照していないか？**
- [ ] **UseCaseがStateを直接操作していないか？**
- [ ] **ServicesがRepositoryに依存していないか？**
- [ ] **外部SPMを適切なレイヤーでのみ使用しているか？**

詳細は [REFERENCE.md](REFERENCE.md) を参照。
