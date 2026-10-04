---
name: architecture-diagram-drawio
description: >
  draw.io (diagrams.net) で、パブリッククラウド(AWS/GCP/Azure)・ブロックチェーン・AI/LLMを含む
  あらゆるシステムのアーキテクチャ図を「綺麗に」作成するスキル。「アーキテクチャ図を描いて」
  「システム構成図が欲しい」「draw.ioで図を作って」「AWS構成図」「インフラ図」「dApp構成図」
  「RAGパイプラインの図」「マルチエージェントの構成を図にして」「可用性/DR構成を図示して」
  「マルチテナントの設計を図にして」「NFTマーケットプレイスの構成図」「DEX/CEXのアーキテクチャ」
  「Liquid Stakingの構成図」「ステーブルコインの仕組みを図示して」「Perpetuals DEXの図」
  「トークンローンチパッドの構成」「予測市場(Polymarket的な)の仕組みを図にして」
  「RWAトークン化の構成図」「静的サイトのホスティング構成」「WebSocketでリアルタイム通信の図」
  「IoTデータ収集基盤の図」「マルチアカウント統治(Landing Zone)の構成図」
  「CQRS/Event Sourcingの図」「Sagaパターンを図にして」「Circuit Breakerの構成図」
  「Strangler Figでの移行計画を図示して」「BFFのアーキテクチャ」など、システムの構造・
  データフロー・ネットワーク構成を視覚化したいという要望が出たら必ず使うこと。ゼロから描く
  場合も、既存コード(CDK/Terraform等)から起こす場合も、汎用パターンから始めたい場合も対象。
  49種類の実務パターン(3層Web、サーバーレス、マイクロサービス、マルチリージョンDR、
  バックアップリカバリ、ゼロトラスト認証、マルチテナントSaaS、静的サイト、WebSocket、
  メディア処理、全文検索、IoT、Landing Zone、キャッシュ、Warm Standby、dApp、L1ノード、
  クロスチェーンブリッジ、NFTマーケットプレイス、x402決済、DEX、CEX、DAOガバナンス、
  DeFiレンディング、Liquid Staking、Perpetuals DEX、ステーブルコイン、トークンローンチパッド、
  予測市場、RWAトークン化、RAG、マルチエージェント、CQRS/Event Sourcing、Saga、
  Circuit Breaker/Bulkhead、Strangler Fig、BFF等)の検証済みテンプレートと、公式サービス
  アイコンを検索して正確に使う手順を提供する。
model: opus
---

# Architecture Diagram (draw.io)

システムアーキテクチャ図を、ホワイトボードの殴り書きではなく「実務で人に見せられる品質」で
draw.io 形式(.drawio / mxGraph XML)で作成する。

## なぜテンプレート起点なのか

良いアーキテクチャ図の大部分は、レイアウトの一貫性(グリッド整列、コンテナの入れ子、色分けの
ルール)で決まる。ゼロから座標を都度考えると、アイコンが重なったり余白が不揃いになったりして
「なんとなく雑」な図になりやすい。そこでこのスキルは、**実務でよくあるシステムパターンを
あらかじめ綺麗にレイアウトしたテンプレート(`templates/`)** を起点にし、要件に合わせて
ラベル・アイコン・接続を差し替えるアプローチを取る。ゼロから描く必要がある場合も、
`scripts/dio.py` の座標ヘルパーとレイアウト原則(`references/layout-and-style-guide.md`)に
従うことで同じ品質を再現できる。

## ワークフロー

1. **要件を明確にする** — 対象システムの種類(Web/サーバーレス/データ基盤/ブロックチェーン/AI)、
   強調したい観点(可用性、セキュリティ、マルチテナント、コスト等)、クラウド(AWS/GCP/Azure/
   マルチクラウド)、対象読者(経営層向けの概要 or エンジニア向けの詳細)を確認する。
   不明な場合はユーザーに1〜2点だけ質問する(全部を聞き返さない)。

2. **`references/pattern-catalog.md` でテンプレートを選ぶ** — 24個のテンプレートから最も近い
   ものを選ぶ。複数の要素を組み合わせたい場合(例: 「サーバーレスAPI + マルチリージョンDR」)は
   2つのテンプレートの構成要素を1つの図にマージしてよい。ぴったりのテンプレートがなければ
   最も近いものを土台にする。

3. **テンプレートを複製してカスタマイズする**
   - `templates/<category>/<name>.drawio` を作業用にコピーする(ユーザーのプロジェクト内の
     適切な場所、例: `docs/architecture.drawio`)。
   - `mcp__drawio__list_pages` → `mcp__drawio__get_page` で中身を読む。
   - ラベル・サービス名・接続関係を要件に合わせて編集する。小さな変更(テキスト差し替え、
     アイコン1個の追加)は XML を直接 `Edit` してよい。レイアウトを大きく変える場合は
     `scripts/dio.py` の `Diagram` クラスを使って再構築する方が、座標計算やID重複のミスを防げる
     (このスキル自体の全テンプレートも `scripts/generate_templates.py` でこの方法で生成した)。
   - `mcp__drawio__set_page` で書き戻す。

4. **不足しているアイコンは `search_shapes` で調べる。記憶から書かない。**
   draw.io のシェイプ名(`resIcon=mxgraph.aws4.xxx` 等)は頻繁に増減する。
   `references/aws-icon-guide.md` に主要アイコンの検証済みスタイル文字列を掲載しているが、
   そこにないサービスが必要な場合は必ず `mcp__drawio__search_shapes` で検索し、返ってきた
   `style` 文字列をそのまま使う。存在しないアイコン名を推測で書くと、開いたときに空白の
   四角になり「雑な図」の最大要因になる。

5. **仕上げに実際に開いて確認する** — `mcp__drawio__open_drawio_xml`(`routing="libavoid"`
   推奨)でエディタURLを生成し、ブラウザで開いて重なり・はみ出し・矢印の交差がないか
   目視確認する。Claude Code から Chrome を操作できる場合は実際にスクリーンショットを撮って
   確認する。テキストだけで「多分大丈夫」と報告しない。

6. **ユーザーに見せる** — 生成した `.drawio` ファイルのパスと、必要なら
   `mcp__drawio__open_drawio_xml` で開いたエディタURLを伝える。図の読み方(色分け・矢印の意味)
   を短く説明する。

## レイアウトの原則(要約 — 詳細は references/layout-and-style-guide.md)

- **座標は78pxのアイコン基準・グリッド整列**。`scripts/dio.py` の `ICON`(78)・パディング定数を
  使うと自動的に揃う。
- **入れ子コンテナで境界を表現する**: Region > AZ > Subnet、VPC > Security Group、
  Tenant Boundary など。コンテナの子要素の座標はコンテナ左上を原点とした相対座標になる
  (draw.io の仕様)。
- **色は意味を持たせる**: AWSは公式カテゴリ色(computeはオレンジ、storageは緑、databaseは
  紫、securityは赤 など)に従う。汎用シェイプは青=アプリ層、紫=AI/ML、オレンジ=イベント/
  非同期処理、グレー=横断的関心事(監視・監査)、というふうに一貫させる。
- **矢印には必ずラベルを付ける**(「HTTPS」「非同期」「レプリケーション」等)。矢印だけでは
  何が流れているか伝わらない。同期/重要経路は実線・太線、非同期/バックアップ/監視等の
  副次経路は破線にする。
- **1枚に詰め込みすぎない**。要素が20個を超えそうなら、レイヤーごと(ネットワーク図/
  データフロー図)に分けるか、draw.io のマルチページ機能(`mcp__drawio__list_pages` /
  `set_page` でページ追加)を使う。

## リファレンス

| ファイル | 内容 |
|---|---|
| `references/pattern-catalog.md` | 24テンプレートの一覧と選び方 |
| `references/aws-icon-guide.md` | 検証済みAWSアイコン一覧、カテゴリ色、グループ(VPC等)の書き方 |
| `references/cloud-service-equivalence.md` | AWS⇔GCP⇔Azure サービス対応表(テンプレート流用時に使う) |
| `references/blockchain-ai-icon-guide.md` | ブロックチェーン/AI図で使う汎用シェイプとアイコン検索クエリ例 |
| `references/layout-and-style-guide.md` | 座標・余白・色・矢印スタイルの詳細ルール |
| `references/ha-dr-patterns.md` | 可用性・耐障害性・マルチリージョン・バックアップリカバリの設計パターン深掘り |
| `references/security-patterns.md` | 認証・認可・ゼロトラスト・エッジセキュリティの設計パターン深掘り |
| `references/multi-tenant-patterns.md` | Silo / Pool / Bridge テナンシーモデルの深掘り |

## テンプレート一覧(概要 — 詳細は references/pattern-catalog.md)

`templates/aws/`(20種): 3層Web(Multi-AZ)、サーバーレスAPI、マイクロサービス(コンテナ)、
データレイク分析基盤、マルチリージョンActive-Active、Pilot Light/バックアップDR、
Hub-and-Spokeネットワーク、CI/CDパイプライン、マルチテナントSaaS(Pool/Silo各1)、
ゼロトラスト認証、エッジセキュリティ(WAF/CDN)、静的サイト/JAMstack、WebSocketチャット、
メディア処理パイプライン、全文検索基盤(OpenSearch)、IoT取り込みパイプライン、
Landing Zone/マルチアカウント統治、キャッシュ層(Cache-Aside)、Warm Standby DR。

`templates/blockchain/`(18種): dAppフルスタック、L1ノード/バリデータ、クロスチェーンブリッジ、
オラクル連携、MPCウォレット/カストディ、Rollup/L2、NFTマーケットプレイス、
x402エージェント決済(HTTP 402)、DEX(AMM)、CEX(中央集権型取引所)、DAOガバナンス、
DeFiレンディングプロトコル、Staking/Liquid Staking、Perpetuals(無期限先物)DEX、
ステーブルコイン(CDP型)、Token Launchpad/ICO、予測市場(Polymarket型)、
RWAトークン化(ERC-3643)。

`templates/ai/`(6種): RAGパイプライン、マルチエージェントオーケストレーション、
LLM推論ゲートウェイ、MCPサーバー、ベクトルDB、ファインチューニングパイプライン。

`templates/patterns/`(5種、クラウド非依存の汎用設計パターン): CQRS/Event Sourcing、
Sagaパターン、Circuit Breaker/Bulkhead、Strangler Fig移行、BFF(Backend for Frontend)。

## GCP / Azure での作成について

テンプレートはAWSを主軸に作り込んである(AWSが最も網羅的なdraw.ioシェイプライブラリを持つため)。
GCP/Azure構成が必要な場合は、`references/cloud-service-equivalence.md` の対応表で相当サービスを
特定し、同じレイアウト(コンテナ構造・矢印)を保ったまま `search_shapes` でそのクラウドの
アイコンスタイルに差し替える。ゼロから座標を組み直す必要はない。

## スクリプト

- `scripts/dio.py` — mxGraph XML を手で書かずに組み立てるための最小限のビルダー。
  `Diagram().node()/.container()/.edge()/.save()` で、ID重複やエスケープ漏れを気にせず
  レイアウトに集中できる。検証済みAWSアイコンの辞書(`AWS`)、コンテナスタイル(`GROUPS`)、
  汎用シェイプ(`GENERIC`)を含む。新しい一枚絵の図を作るときはこれを再利用する。
- `scripts/generate_templates.py` — 全24テンプレートの生成元。テンプレートのレイアウトを
  恒久的に直したい場合は、生成されたXMLを直接編集するのではなくこのスクリプトの該当する
  `build_*` 関数を直し、再実行すること(次にテンプレートを見る人が生成ロジックを追える)。
