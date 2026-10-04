---
name: aws-cdk-architect
description: >
  AWS CDK (TypeScript) を使ったインフラの設計・実装を包括的にサポートするスキル。
  ユーザーの要件からCDKスタックを設計し、ベストプラクティスに沿ったTypeScriptコードを生成する。
  L1/L2/L3コンストラクトの使い分け、スタック分割戦略、セキュリティ設定、コスト最適化まで対応。
  Use when: (1) CDKでインフラを構築したい, (2) CDKスタックを設計・実装したい,
  (3) CDKのベストプラクティスを知りたい, (4) 既存CDKコードをレビュー・改善したい,
  (5) AWSサービスをCDKで構成したい, (6) CDKプロジェクトの初期セットアップをしたい,
  (7) Lambda/API Gateway/DynamoDB等をCDKで作りたい, (8) CDKのテストを書きたい,
  (9) cdk deploy/synth/diffの使い方を知りたい, (10) IaCでAWS環境を管理したい。
  「CDK」「インフラ構築」「AWSリソース作成」「スタック」「IaC」「cdk init」
  「cdk deploy」「コンストラクト」等のキーワードで呼び出す。
---

# AWS CDK Architect

AWS CDK v2 (TypeScript) によるインフラの設計・実装を包括的にサポートするスキル。
ユーザーの要件を聞き取り、最適なCDKスタック構成を設計し、プロダクション品質のコードを生成する。

## 引数

- **mode**: 動作モード（デフォルト: `implement`）
  - `design`: 要件ヒアリング → アーキテクチャ設計のみ
  - `implement`: 要件 → 設計 → CDKコード生成まで一気通貫
  - `review`: 既存CDKコードのレビュー・改善提案
  - `init`: 新規CDKプロジェクトのセットアップ
- **services**: 主に使うAWSサービス（例: `lambda,apigateway,dynamodb`）

## 実行手順

### Step 1: 要件の整理

ユーザーの入力から以下を整理する。不明な点は質問して確認する。

**必須情報:**
- 構築したいシステムの概要
- 使用するAWSサービス
- 環境（dev/staging/prod）
- リージョン

**確認すべき項目:**
- 既存のCDKプロジェクトがあるか（ある場合は既存コードを読む）
- VPC要件（新規作成 or 既存VPC利用）
- 認証・認可要件
- 想定トラフィック/データ量
- コスト制約
- CI/CD要件

### Step 2: アーキテクチャ設計

要件に基づいて以下を設計する：

#### 2a. スタック分割戦略

CDKのスタック分割は以下の原則に従う：

```
推奨パターン:
├── NetworkStack      # VPC, Subnet, Security Group（変更頻度: 低）
├── DatabaseStack     # RDS, DynamoDB, ElastiCache（変更頻度: 低）
├── ComputeStack      # Lambda, ECS, EC2（変更頻度: 高）
├── ApiStack          # API Gateway, CloudFront（変更頻度: 中）
└── MonitoringStack   # CloudWatch, SNS（変更頻度: 低）
```

**分割の判断基準:**
- ライフサイクルが異なるリソースは別スタック
- デプロイ頻度が異なるリソースは別スタック
- ステートフル（DB）とステートレス（Lambda）は別スタック
- 小規模検証の場合は単一スタックでOK（過度な分割は避ける）

#### 2b. コンストラクトレベルの選択

| レベル | 用途 | 例 |
|--------|------|-----|
| L1 (Cfn*) | CloudFormationリソースの1:1マッピング。L2がないリソースや細かい制御が必要な場合 | `CfnBucket` |
| L2 | AWSベストプラクティスが組み込まれた高レベルAPI。**基本はこれを使う** | `Bucket`, `Function`, `Table` |
| L3 (Patterns) | 複数リソースをまとめたパターン。よくある構成を素早く構築 | `LambdaRestApi`, `ApplicationLoadBalancedFargateService` |

**原則: L2を第一選択とし、L3で要件を満たせるならL3を使う。L1は最終手段。**

### Step 3: CDKコードの生成

以下のコーディング規約に従ってTypeScriptコードを生成する。

#### プロジェクト構造

```
cdk-project/
├── bin/
│   └── app.ts                # エントリーポイント（App定義）
├── lib/
│   ├── stacks/               # スタック定義
│   │   ├── network-stack.ts
│   │   ├── database-stack.ts
│   │   └── compute-stack.ts
│   └── constructs/           # カスタムコンストラクト
│       └── api-construct.ts
├── test/
│   └── *.test.ts             # スナップショット & ファイングレインドテスト
├── cdk.json
├── tsconfig.json
└── package.json
```

#### コーディング規約

**命名規則:**
```typescript
// スタッククラス: PascalCase + "Stack"
export class ComputeStack extends cdk.Stack { ... }

// コンストラクトクラス: PascalCase
export class ApiEndpoint extends Construct { ... }

// リソースのID: PascalCase（論理ID）
const bucket = new s3.Bucket(this, 'DataBucket', { ... });

// Props interface: クラス名 + "Props"
interface ComputeStackProps extends cdk.StackProps {
  vpc: ec2.IVpc;
}
```

**必須パターン:**

```typescript
// 1. RemovalPolicy を明示する（特にステートフルリソース）
const table = new dynamodb.Table(this, 'Table', {
  // ...
  removalPolicy: cdk.RemovalPolicy.RETAIN,  // prod
  // removalPolicy: cdk.RemovalPolicy.DESTROY, // dev
});

// 2. 環境ごとの設定はPropsで注入する（ハードコードしない）
interface AppProps {
  environment: 'dev' | 'staging' | 'prod';
  domainName?: string;
}

// 3. タグを付与する
cdk.Tags.of(this).add('Project', 'my-project');
cdk.Tags.of(this).add('Environment', props.environment);

// 4. Output で重要な値を出力する
new cdk.CfnOutput(this, 'ApiUrl', {
  value: api.url,
  description: 'API Gateway endpoint URL',
});
```

**セキュリティ原則:**

```typescript
// 最小権限の原則
table.grantReadWriteData(lambdaFunction);  // ✅ 必要な権限のみ
// lambdaFunction.addToRolePolicy(new iam.PolicyStatement({  // ❌ ワイルドカード避ける
//   actions: ['*'], resources: ['*']
// }));

// 暗号化はデフォルトで有効化
const bucket = new s3.Bucket(this, 'Bucket', {
  encryption: s3.BucketEncryption.S3_MANAGED,
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
  enforceSSL: true,
});

// VPC内のリソースはセキュリティグループで制御
const sg = new ec2.SecurityGroup(this, 'SG', {
  vpc,
  allowAllOutbound: false,  // 明示的にアウトバウンドも制御
});
```

### Step 4: テストコードの生成

以下の2種類のテストを生成する：

```typescript
import * as cdk from 'aws-cdk-lib';
import { Template, Match } from 'aws-cdk-lib/assertions';

// 1. ファイングレインドテスト（重要なリソースの存在と設定を検証）
test('DynamoDB table created with correct settings', () => {
  const app = new cdk.App();
  const stack = new DatabaseStack(app, 'TestStack', { /* props */ });
  const template = Template.fromStack(stack);

  template.hasResourceProperties('AWS::DynamoDB::Table', {
    BillingMode: 'PAY_PER_REQUEST',
    SSESpecification: { SSEEnabled: true },
  });
});

// 2. スナップショットテスト（意図しない変更の検出）
test('snapshot test', () => {
  const app = new cdk.App();
  const stack = new DatabaseStack(app, 'TestStack', { /* props */ });
  const template = Template.fromStack(stack);

  expect(template.toJSON()).toMatchSnapshot();
});
```

### Step 5: デプロイ手順の提示

コード生成後、以下のデプロイ手順を提示する：

```bash
# 1. 依存関係のインストール
npm install

# 2. TypeScriptのコンパイル確認
npx tsc --noEmit

# 3. テスト実行
npx jest

# 4. CDK diff で変更内容を確認
npx cdk diff

# 5. CDK synth でCloudFormationテンプレートを生成（確認用）
npx cdk synth

# 6. デプロイ
npx cdk deploy --all
# または特定のスタックのみ
npx cdk deploy ComputeStack
```

## よく使うパターン集

以下のパターンはユーザーの要件に応じて組み合わせて使う。
詳細は [references/patterns.md](references/patterns.md) を参照。

### サーバーレスAPI
```
API Gateway → Lambda → DynamoDB
```

### コンテナWebアプリ
```
ALB → ECS Fargate → RDS Aurora
```

### 静的サイト + API
```
CloudFront → S3 (frontend)
CloudFront → API Gateway → Lambda (backend)
```

### イベント駆動
```
EventBridge → SQS → Lambda → DynamoDB
```

### データパイプライン
```
S3 → Lambda/Step Functions → Athena/Glue → S3
```

## CDK v2 重要ポイント

- **全てのAWSコンストラクトライブラリが `aws-cdk-lib` に統合**されている（v1のような個別パッケージ不要）
- **`constructs` パッケージ**は別途必要（`npm install constructs`）
- **Alpha モジュール**（実験的機能）は `@aws-cdk/*-alpha` として別パッケージ
  - 例: `@aws-cdk/aws-lambda-python-alpha`
- **context values** で環境差分を管理（`cdk.json` の `context`）
- **Aspects** でスタック全体にポリシーを適用（例: 全S3バケットに暗号化を強制）
- **cdk-nag** でセキュリティ/コンプライアンスチェック

## コスト最適化のヒント

- Lambda: メモリサイズの最適化（`aws-lambda-power-tuning`で検証）
- DynamoDB: PAY_PER_REQUEST（検証用）vs PROVISIONED（本番用）
- NAT Gateway: 検証環境では `NatProvider.instanceV2()` で代替検討
- RDS: 検証環境では `instanceType: ec2.InstanceType.of(ec2.InstanceClass.T4G, ec2.InstanceSize.MICRO)`
- 検証用スタックの自動削除: `cdk-time-bomb` ライブラリの活用も検討

## アンチパターン（避けるべきこと）

以下は公式ドキュメントで明示されているアンチパターン。コード生成・レビュー時に必ず確認する。

| アンチパターン | 正しいやり方 |
|---------------|-------------|
| コンストラクト内で環境変数を参照 | Props経由で設定を注入する |
| リソース名をハードコード | CDKに名前を自動生成させる |
| synthesis時にネットワーク/SDK呼び出し | context providerを使い、`cdk.context.json`をコミット |
| CloudFormation ParametersやConditions | TypeScriptのif/forで合成時に決定 |
| IAMポリシーを手書き | `grant*()` メソッドを使う |
| ステートフルリソースの論理IDを変更 | テストで論理IDの安定性を検証 |
| ログ保持期間やRemovalPolicyを未設定 | 本番では明示的に設定する |
| `cdk.context.json`をgitignore | **必ずバージョン管理にコミット**する（非決定的なsynthesisを防ぐ） |

## Aspectsの活用

Aspects はスタック全体にポリシーを横断適用するための仕組み。セキュリティやコンプライアンスの強制に使う。

```typescript
import { Aspects, IAspect } from 'aws-cdk-lib';
import { CfnBucket } from 'aws-cdk-lib/aws-s3';
import { IConstruct } from 'constructs';

// 全S3バケットに暗号化を強制するAspect
class BucketEncryptionChecker implements IAspect {
  visit(node: IConstruct): void {
    if (node instanceof CfnBucket) {
      if (!node.bucketEncryption) {
        Annotations.of(node).addError('S3 bucket must have encryption enabled');
      }
    }
  }
}

// スタックに適用
Aspects.of(stack).add(new BucketEncryptionChecker());

// cdk-nagでセキュリティチェック
import { AwsSolutionsChecks } from 'cdk-nag';
Aspects.of(app).add(new AwsSolutionsChecks());
```

## 便利なライブラリ

| ライブラリ | 用途 |
|-----------|------|
| `cdk-nag` | セキュリティ/コンプライアンスチェック |
| `cdk-monitoring-constructs` | 自動ダッシュボード・アラーム生成 |
| `@aws-cdk/aws-lambda-nodejs` | esbuildでのLambdaバンドル（aws-cdk-lib同梱） |
| `cdk-dia` | CDKコードからインフラ図を自動生成 |
| `projen` | プロジェクト設定の管理・自動化 |
| `aws-cdk-billing-alarm` | コスト閾値アラーム |
| `constructs.dev` | コミュニティ製コンストラクトの検索 |

## レビューモード

`mode:review` の場合、以下の観点で既存コードをレビューする：

1. **セキュリティ**: 最小権限、暗号化、パブリックアクセス制御
2. **コスト**: リソースサイジング、不要リソース
3. **運用性**: タグ付け、Output、RemovalPolicy
4. **コード品質**: L2/L3の活用、Props設計、テストカバレッジ
5. **スタック設計**: 分割の適切さ、依存関係の方向

## 最新ドキュメントの参照

CDK APIの詳細や最新の変更については、context7 MCPツールを使って最新ドキュメントを取得する：

```
mcp__context7__resolve-library-id → "aws-cdk-lib"
mcp__context7__query-docs → 必要なAPIのドキュメントを取得
```

## 関連リソース

- [パターン集](references/patterns.md) - よく使うアーキテクチャパターンのCDKコード例
- [AWS CDK公式ドキュメント](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- [CDK API Reference](https://docs.aws.amazon.com/cdk/api/v2/)
- [AWS Solutions Constructs](https://docs.aws.amazon.com/solutions/latest/constructs/)
- [cdk-nag](https://github.com/cdklabs/cdk-nag) - セキュリティチェック
- [awesome-cdk](https://github.com/kalaiser/awesome-cdk) - コミュニティリソース集
