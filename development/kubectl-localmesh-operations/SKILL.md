---
name: kubectl-localmesh-operations
description: kubectl-localmesh固有の運用操作（起動、/etc/hosts管理、サービスアクセス、依存関係チェック）を提供します
allowed-tools: ["Bash", "Read"]
---

# kubectl-localmesh 運用操作

このskillは、kubectl-localmesh固有の運用操作を提供します。

## 提供機能

### 起動

**kubectlプラグインとして起動（推奨、/etc/hosts自動更新あり、sudo必要）**:

```bash
sudo kubectl localmesh -f services.yaml
```

**直接実行の場合**:
```bash
# Task経由でビルド済み、またはgo install済み
sudo ./bin/kubectl-localmesh -f services.yaml

# 直接go buildした場合
sudo ./kubectl-localmesh -f services.yaml
```

### /etc/hosts管理オプション

**自動更新を無効化**:

```bash
kubectl localmesh -f services.yaml --update-hosts=false
# または
./kubectl-localmesh -f services.yaml --update-hosts=false
```

この場合、Hostヘッダーを手動指定:
```bash
curl -H "Host: users-api.localhost" http://127.0.0.1:80/
```

**自動更新のメリット**:
- ブラウザやcurlで直接ホスト名でアクセス可能
- 設定が簡潔

**自動更新のデメリット**:
- sudo権限が必要
- /etc/hostsへの書き込み権限が必要

### サービスへのアクセス

**/etc/hosts更新有効時（デフォルト）**:

- **HTTP**: `curl http://billing-api.localhost/health`
- **gRPC**: `grpcurl -plaintext users-api.localhost list`

**ポート80使用時**: ポート番号不要
**他のポート使用時**: `http://service.localhost:8080`のようにポート指定

**/etc/hosts更新無効時**:

```bash
# HTTPの場合
curl -H "Host: billing-api.localhost" http://127.0.0.1:80/health

# gRPCの場合
grpcurl -plaintext -authority users-api.localhost 127.0.0.1:80 list
```

### 停止・クリーンアップ

**Ctrl+C**で停止すると、自動的に:
- /etc/hostsエントリを削除
- すべてのport-forwardプロセスを停止
- Envoyプロセスを停止
- 一時ディレクトリを削除

**クリーンな終了を確認**:
```bash
# /etc/hostsにエントリが残っていないか確認
grep "kubectl-localmesh" /etc/hosts

# port-forwardプロセスが残っていないか確認
ps aux | grep "kubectl port-forward"

# Envoyプロセスが残っていないか確認
ps aux | grep envoy
```

### 依存関係チェック

起動前に依存関係を確認:

```bash
# スクリプトを使用
.claude/skills/kubectl-localmesh-operations/scripts/check-dependencies.sh

# または個別に確認
kubectl version --client
envoy --version
bash --version
```

**必須依存関係**:
- `kubectl`: Kubernetesクラスタへのアクセス
- `envoy`: ローカルプロキシ（macOS: `brew install envoy`）
- `bash`: port-forwardループスクリプト実行

### トラブルシューティング

#### 問題: ポート衝突

**症状**: `address already in use`エラー

**解決**:
1. `listener_port`を変更（services.yaml）
2. または既存プロセスを停止

```bash
# ポート80を使用しているプロセスを確認
lsof -i :80

# プロセスを停止
kill <PID>
```

#### 問題: Envoy起動失敗

**症状**: Envoyプロセスがすぐに終了する

**解決**:
1. Envoy設定を確認（`kubectl-envoy-debugging` skillを使用）
2. デバッグログを確認

```bash
# Envoy設定をダンプ
./kubectl-localmesh --dump-envoy-config -f services.yaml > /tmp/envoy-config.yaml

# Envoy設定を検証
envoy --mode validate -c /tmp/envoy-config.yaml

# デバッグログで詳細確認
sudo ./kubectl-localmesh -f services.yaml -log debug
```

#### 問題: port-forward接続失敗

**症状**: `error forwarding port`エラー

**解決**:
1. サービスの存在確認
2. ポート名/番号の確認
3. kubeconfigとクラスタ接続確認

```bash
# サービスの存在確認
kubectl get svc -n <namespace>

# サービスの詳細とポート確認
kubectl describe svc <service> -n <namespace>

# kubeconfigとクラスタ接続確認
kubectl cluster-info
kubectl get nodes
```

#### 問題: /etc/hosts更新失敗

**症状**: `permission denied`エラー

**解決**:
1. sudoで実行
2. または`--update-hosts=false`オプションを使用

```bash
# sudo権限で実行
sudo ./kubectl-localmesh -f services.yaml

# または/etc/hosts更新を無効化
./kubectl-localmesh -f services.yaml --update-hosts=false
```

#### 問題: サービスにアクセスできない

**症状**: `connection refused`や`503 Service Unavailable`

**解決手順**:
1. kubectl-localmeshが起動しているか確認
2. port-forwardが正常に動作しているか確認
3. Envoyログを確認
4. curlで詳細なHTTPヘッダーを確認

```bash
# port-forwardプロセスの確認
ps aux | grep "kubectl port-forward"

# curlで詳細確認
curl -v http://users-api.localhost/

# 期待される出力:
# * Connected to users-api.localhost (127.0.0.1)
# > GET / HTTP/1.1
# > Host: users-api.localhost
```

## 使用方法

ユーザーから以下のような依頼があった場合:

1. **「起動して」**
   - 依存関係チェック
   - sudo権限確認
   - 適切なパスで起動

2. **「サービスにアクセスしたい」**
   - /etc/hosts設定に応じた方法を案内
   - HTTPまたはgRPCに応じたコマンド例を提供

3. **「動かない」**
   - 依存関係チェック
   - トラブルシューティングフローを実行
   - エラーメッセージに応じた解決策を提示

## ワークフロー例

### 初回セットアップ

```bash
# 1. 依存関係チェック
.claude/skills/kubectl-localmesh-operations/scripts/check-dependencies.sh

# 2. 設定ファイル確認
cat services.yaml

# 3. Kubernetesクラスタ接続確認
kubectl cluster-info

# 4. 起動
sudo ./bin/kubectl-localmesh -f services.yaml
```

### 日常的な使用

```bash
# 1. 起動
sudo ./bin/kubectl-localmesh -f services.yaml

# 2. 別ターミナルでサービスにアクセス
curl http://users-api.localhost/health
grpcurl -plaintext users-api.localhost list

# 3. 終了（Ctrl+C）
```

### デバッグセッション

```bash
# 1. デバッグモードで起動
sudo ./kubectl-localmesh -f services.yaml -log debug

# 2. 問題を再現
curl http://users-api.localhost/problematic-endpoint

# 3. ログを確認
# （標準出力に詳細なログが表示される）

# 4. 必要に応じてEnvoy設定を確認
./kubectl-localmesh --dump-envoy-config -f services.yaml
```

## 参考情報

プロジェクトのCLAUDE.mdに詳細なアーキテクチャと実装詳細があります。

## 関連Skills

- `go-taskfile-workflow`: ビルドとテスト
- `kubectl-envoy-debugging`: Envoy設定の確認とデバッグ
- `kubectl-localmesh-macos-localhost`: macOSの.localhostドメインの挙動
