---
name: aws-ops
description: AWS環境特有の運用・開発ルール
---

## AWS 特有の運用原則

- **CLI 認証**: AWS CLI を使用する場合はコマンド出力前に認証状況を確認すること。
- **自動生成ファイル**: `lambda_package` は自動生成されるパッケージなので修正不要。

## API Gateway & Cognito 連携ルール

- **CORS (OPTIONS) の認証除外**: API Gateway に Cognito Authorizer を導入する場合、ブラウザのプリフライトリクエスト (`OPTIONS`) は認証を通過できないため、`OPTIONS` メソッドの `AuthorizationType` は必ず `NONE` に設定すること。
- **Authorization ヘッダー形式**: Cognito User Pool Authorizer を使用する場合、デフォルトでは `Authorization` ヘッダーに ID トークンを直接（`Bearer ` プレフィックスなしで）含める必要がある。
- **デプロイの強制反映**: CloudFormation で API Gateway のメソッドやオーソライザーを変更した場合、ステージへの反映には新しい `AWS::ApiGateway::Deployment` リソースが必要になる。既存のデプロイリソース名を変更（例: `ApiGatewayDeploymentV2`）することで強制的に再デプロイをトリガーできる。
- **テンプレートのエンコーディング**: CloudFormation テンプレートに日本語を含めると AWS CLI でのデプロイ時にエンコーディングエラーが発生する場合がある。可能な限り `Description` や `Parameter` の説明文には英語を使用し、ファイルは UTF-8 (BOM なし) で保存すること。
