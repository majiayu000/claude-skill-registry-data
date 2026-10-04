---
name: cdk-aws-diagram
description: >
  CDK TypeScript スタックファイルを読み取り、誰にでも伝わるAWS構成図をdraw.io形式で自動生成するスキル。
  「CDKスタックを図にしたい」「AWS構成を可視化したい」「draw.ioの構成図を作りたい」「インフラの図を書いて」
  「アーキテクチャ図が欲しい」「CDKコードを可視化して」など、CDK/インフラ/構成図に関する要望が出たら必ずこのスキルを使うこと。
  CloudFormationテンプレートやCDKコードからAWS構成図を生成する場合も同様に使用すること。
---

# CDK AWS Diagram Generator

CDKスタックのTypeScriptコードを解析し、draw.ioで開ける見やすいAWS構成図を生成する。
技術者でなくても理解できる「なぜこう繋がっているか」が伝わる図を目指す。

---

## ステップ1: CDKファイルを読み込む

ユーザーが指定したファイルをすべて読み込む。指定がなければ `lib/**/*.ts` と `bin/**/*.ts` を検索して読む。
複数ファイルがある場合はすべて読み込み、スタック全体の構成を把握する。

---

## ステップ2: AWSリソースを抽出する

以下のパターンでリソースを特定する。CDK L1（Cfn系）とL2（高レベル）両方を対象にする。

### ネットワーク系
| CDKコード | AWSリソース | draw.io shape |
|-----------|------------|---------------|
| `ec2.CfnVPC` / `ec2.Vpc` | VPC | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;` |
| `ec2.CfnSubnet` / `ec2.Subnet` (mapPublicIpOnLaunch=true) | パブリックサブネット | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_public_subnet;` |
| `ec2.CfnSubnet` / `ec2.Subnet` (private) | プライベートサブネット | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_private_subnet;` |
| `ec2.CfnInternetGateway` | インターネットゲートウェイ | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.internet_gateway;` |
| `ec2.CfnVPCEndpoint` | VPCエンドポイント | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.endpoints;` |
| `ec2.CfnSecurityGroup` | セキュリティグループ | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;` |

### コンピュート系
| CDKコード | AWSリソース | draw.io shape |
|-----------|------------|---------------|
| `ec2.CfnInstance` / `ec2.Instance` | EC2インスタンス | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;` |
| `lambda.CfnFunction` / `lambda.Function` | Lambda | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;` |
| `ecs.CfnService` / `ecs.FargateService` | ECS Fargate | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.fargate;` |

### ストレージ系
| CDKコード | AWSリソース | draw.io shape |
|-----------|------------|---------------|
| `s3.CfnBucket` / `s3.Bucket` | S3バケット | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;` |
| `ec2.CfnVolume` | EBSボリューム | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ebs;` |
| `rds.CfnDBInstance` / `rds.DatabaseInstance` | RDS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;` |
| `dynamodb.CfnTable` / `dynamodb.Table` | DynamoDB | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;` |

### セキュリティ・権限系
| CDKコード | AWSリソース | draw.io shape |
|-----------|------------|---------------|
| `iam.CfnRole` / `iam.Role` | IAMロール | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.role;` |
| `iam.CfnPolicy` / `iam.Policy` | IAMポリシー | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.permissions;` |

### AIサービス系
| CDKコード | AWSリソース | draw.io shape |
|-----------|------------|---------------|
| `bedrock:InvokeModel` (IAMポリシー内) | Amazon Bedrock | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.bedrock;` |
| `AWS::BedrockAgentCore::Runtime` | Bedrock AgentCore | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.bedrock;` |

### 管理・運用系
| CDKコード | AWSリソース | draw.io shape |
|-----------|------------|---------------|
| `AmazonSSMManagedInstanceCore` (マネージドポリシー) | SSM Session Manager | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.systems_manager;` |
| `CloudWatchAgentServerPolicy` (マネージドポリシー) | CloudWatch | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;` |
| `ecr.CfnRepository` | ECR | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecr;` |
| `ssm:PutParameter` / `ssm:GetParameter` (IAMアクション) | SSM Parameter Store | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.parameter_store;` |
| `apigateway.RestApi` | API Gateway | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;` |

### その他
| CDKコード | AWSリソース | draw.io shape |
|-----------|------------|---------------|
| `CfnWaitCondition` | CloudFormation WaitCondition | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudformation;` |

---

## ステップ3: リソース間の関係を整理する

以下の関係性を抽出して矢印・包含関係として表現する:

- **含む関係（入れ子）**: VPCの中にサブネット、サブネットの中にEC2、セキュリティグループの中にEC2
- **接続関係（矢印）**: EC2 → Bedrock（APIコール）、EC2 → SSM（管理）、EC2 → CloudWatch（ログ）
- **アタッチ関係**: IAMロール → EC2、EBSボリューム → EC2
- **条件付きリソース**: `cfnOptions.condition` があるリソースは「(オプション)」と注記する

**関係性の読み方**:
- `addDependency()` → 順序依存
- `vpcId: xxx.ref` → VPC内のリソース
- `subnetId: xxx.ref` → サブネット内のリソース
- `securityGroupIds: [xxx]` → セキュリティグループを使用
- `iamInstanceProfile: xxx.ref` → IAMロールを使用
- IAMポリシーの `Action` → どのAWSサービスを使うか

---

## ステップ4: draw.io XML を生成する

以下のXMLテンプレート構造で生成する。**IDはすべてユニークな文字列を使う**。

### レイアウト方針
- **左から右へ**: ユーザー → インターネット → VPC → EC2 → Bedrockの流れ
- **上下に階層**: ネットワーク層（VPC/サブネット）の中にコンピュート層（EC2）を配置
- **色分け**:
  - ネットワーク系: 薄いグレー背景 `fillColor=#f5f5f5;strokeColor=#666666;`
  - パブリックサブネット: 薄い緑 `fillColor=#d5e8d4;strokeColor=#82b366;`
  - プライベートサブネット: 薄いオレンジ `fillColor=#ffe6cc;strokeColor=#d6b656;`
  - IAM/セキュリティ: 薄い赤 `fillColor=#f8cecc;strokeColor=#b85450;`
  - マネージドサービス（Bedrock等）: 薄い青 `fillColor=#dae8fc;strokeColor=#6c8ebf;`

### XMLテンプレート

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <!-- ユーザー（外部） -->
    <mxCell id="user" value="ユーザー&#xa;(メッセージアプリ)" style="shape=mxgraph.aws4.user;fillColor=#232F3E;fontColor=#ffffff;strokeColor=none;" vertex="1" parent="1">
      <mxGeometry x="40" y="360" width="60" height="60" as="geometry"/>
    </mxCell>

    <!-- VPC コンテナ -->
    <mxCell id="vpc" value="VPC (10.0.0.0/16)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;grStroke=0;verticalLabelPosition=top;verticalAlign=bottom;fillColor=#E6F3FB;strokeColor=#147EBA;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="200" y="100" width="900" height="600" as="geometry"/>
    </mxCell>

    <!-- パブリックサブネット コンテナ -->
    <mxCell id="pubsubnet" value="パブリックサブネット (10.0.1.0/24)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_public_subnet;grStroke=0;verticalLabelPosition=top;verticalAlign=bottom;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="vpc">
      <mxGeometry x="50" y="120" width="400" height="350" as="geometry"/>
    </mxCell>

    <!-- EC2インスタンス (パブリックサブネット内) -->
    <mxCell id="ec2" value="EC2インスタンス&#xa;(Ubuntu 24.04)&#xa;OpenClawが動作" style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;labelBackgroundColor=#ffffff;sketch=0;fontStyle=1;fontSize=11;" vertex="1" parent="pubsubnet">
      <mxGeometry x="150" y="130" width="78" height="78" as="geometry"/>
    </mxCell>

    <!-- プライベートサブネット コンテナ -->
    <mxCell id="privsubnet" value="プライベートサブネット (10.0.2.0/24)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_private_subnet;grStroke=0;verticalLabelPosition=top;verticalAlign=bottom;fillColor=#ffe6cc;strokeColor=#d6b656;" vertex="1" parent="vpc">
      <mxGeometry x="500" y="120" width="350" height="350" as="geometry"/>
    </mxCell>

    <!-- 接続矢印の例 -->
    <mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="user" target="ec2" parent="1">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>
```

---

## ステップ5: 図を実際に開く

生成したXMLを使い、`mcp__drawio__open_drawio_xml` ツールを呼び出して draw.io で図を開く。

```
mcp__drawio__open_drawio_xml(xml="<生成したXML>")
```

**ファイル名の決め方**: スタックのクラス名または CDK プロジェクト名から自動生成する。
例: `ClawdbotBedrockStack` → `clawdbot-bedrock-architecture.drawio`

---

## 品質チェックリスト

図を生成したら以下を確認する:

- [ ] すべての主要リソース（EC2, VPC, IAM, 外部サービス）が含まれているか
- [ ] VPCの中にサブネットが、サブネットの中にEC2が配置されているか
- [ ] 条件付きリソース（VPCエンドポイント等）には「(オプション)」の注記があるか
- [ ] 矢印に「SSM接続」「APIコール」等の日本語ラベルがついているか
- [ ] 技術者でない人が見ても「何がどこにあって、どう繋がっているか」がわかるか
- [ ] AWSサービスのアイコンが正しく使われているか（形が四角いだけの図にならないようにする）

---

## よくあるCDKパターンと図への反映

### VPCエンドポイント（条件付き）
`cfnOptions.condition = createEndpoints` がある場合:
- 図中に VPCエンドポイントのグループを作成
- 「(VPCエンドポイント有効時)」と注記
- EC2 → VPCエンドポイント → Bedrock/SSM の矢印を点線で表現

### マネージドポリシーから外部サービスを推測
```typescript
managedPolicyArns: ['arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore']
```
→ SSM（Session Manager）への接続矢印を追加する

```typescript
managedPolicyArns: ['arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy']
```
→ CloudWatchへのログ送信矢印を追加する

### IAMポリシーのActionからサービス接続を推測
```typescript
Action: ['bedrock:InvokeModel', 'bedrock:InvokeModelWithResponseStream']
```
→ EC2 → Amazon Bedrock への矢印（「AIモデル呼び出し」ラベル）

```typescript
Action: ['ssm:PutParameter', 'ssm:GetParameter']
```
→ EC2 → SSM Parameter Store への矢印（「設定値の保存/取得」ラベル）

### WaitCondition
`CfnWaitCondition` は図に含める必要はない（デプロイメカニズムのため省略可）。

---

## 図の説明コメント

draw.io で図を開いた後、以下のような説明をユーザーに伝える:

```
構成図を生成しました！draw.io で開いています。

【図の読み方】
- 外側の青い枠: AWS VPC（プライベートネットワーク）
- 緑の枠: インターネットから直接アクセス可能なパブリックサブネット
- オレンジの枠: 内部のみのプライベートサブネット（VPCエンドポイント配置）
- 矢印: データや通信の流れ

【主なコンポーネント】
（解析したリソースに基づいて記述）
```
