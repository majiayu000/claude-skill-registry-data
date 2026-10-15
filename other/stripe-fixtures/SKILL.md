---
license: Apache-2.0
name: stripe-fixtures
description: Stripe CLI の `stripe fixtures` コマンドで実行可能な fixture JSON を、対話的に整理しながら生成・検証する。test_clock を使った時間進行、サブスクのライフサイクル、失敗カードでの payment_intent 失敗、Connect 配下の Destination charge、bulk 件数のテスト顧客作成など、複数ステップの API リクエスト連鎖を扱う。「Stripe の fixture を書いて」「fixtures.json を作って」「このシナリオを fixture 化」「テストデータを大量に作りたい」「サブスクの月次失敗をテストしたい」「stripe trigger と fixture どっち使う」のような依頼で起動する。"fixture" という単語が無くても、複数ステップの Stripe テストデータ準備、 test clock を使った時間進行、 bulk なテスト顧客作成、 失敗パターンの再現といった意図が見えたら起動する。単発 API 呼び出しが目的なら起動せずに `stripe trigger` か API 1コールを案内する。
compatibility: Stripe CLI (`stripe fixtures` コマンド) と `STRIPE_API_KEY` 環境変数が利用可能な環境。実行は test mode key (`sk_test_*`) のみを推奨。
---

# stripe-fixtures

Stripe CLI の `stripe fixtures filepath` で実行可能な fixture JSON を、対話を通じて整理・生成・検証する。

## 何を解いているか

`stripe fixtures` は複数の Stripe API リクエストを JSON にシーケンス化し、前のレスポンスを `${name:json_path}` で参照しながら連鎖実行できる。ただし以下の理由で、人間が直接書くのは現実的ではない:

- 参照構文を書くには Stripe API の response shape を頭に入れている必要がある
- path / method の対応を毎回 docs で照合する必要がある
- 同一リソースを N 個作る繰り返し構文がない（人間が N 個分の entry を手で書くのは非現実的）
- 配列要素アクセス記法に docs と実装の食い違いがある（pitfalls.md 参照）

これは AI のスイートスポットそのもの。逆に「単発 API を MCP tool で wrap する」アプローチでは、 fixture が解いている問題（**宣言的なテストデータセットアップ**）には届かない。

## 役割の境界

担うこと:

- 対話を通じた要件整理
- fixture JSON の生成
- 静的検証（参照整合性、記法、 path 形式）
- `stripe trigger` で済むケースの撤退判定
- `STRIPE_API_KEY` の prefix 確認指示

担わないこと:

- fixture の実機実行（ユーザーが `stripe fixtures` で実行）
- 動的検証（API レスポンス確認）
- Live key への強制ブロック（CLI 側でないと不可能）

## 関連スキル（同 monorepo 内）

このリポジトリは Stripe テスト用に2つのレーンを持つ。意図に応じて使い分ける:

- **宣言的レーン（このスキル）** — `stripe fixtures` 用の JSON を生成。CI で再現したい・差分管理したいテストデータセット向け。実行はユーザーの Stripe CLI。
- **命令的レーン（MCP ツール）** — その場で Stripe API を叩いて test clock / 顧客 / サブスクを操作する。`stripe-test-mcp` MCP サーバーが提供。即座に動かして確認したいとき向け。

test clock を fixture で扱う場合の API 制約（最大3顧客/クロック、作成時のみ紐付け、前方のみ進行、Unix 秒）は、姉妹スキル `stripe-test-clock-constraints` に集約してある。cleanup の手順は `stripe-test-data-lifecycle` を参照。これらは再掲せず、必要に応じてそちらを読む。

## 動作フロー

このフローは順序を守る。途中で対話がスキップされると、実行できない、または意図と違う JSON が出る原因になる。

### Phase 0: 撤退判定

最初にユーザーの依頼を読み、 `stripe trigger` で済むかを判定する。済む場合は fixture を作らずに `stripe trigger` の使い方を案内して終わる。

撤退する判定基準:

- 単一の event 発火が目的で、データのカスタマイズが不要
- 例: 「`customer.subscription.created` を発火したい」「`invoice.payment_succeeded` を一回流したい」
- `stripe trigger --help` で利用可能な event 一覧が出る

撤退しない判定基準:

- test_helpers (test_clock 系) を含む
- 複数 customer / 複数 subscription を扱う
- 失敗パターンの期待値を含む
- Connect 配下のリソース操作
- カスタム metadata や特殊な params の組み合わせ

### Phase 1: 軸の確定

ユーザーの初回発話から確定していない軸だけを質問する。最大3問。それ以上聞きたくなったら「分からない部分は仮置きで JSON を生成し、コメントで明示する」に倒す。煩わしさで Skill が嫌われるリスクのほうが、軽微な仮置きより重いため。

| 軸         | 質問例                               | スキップ条件                                 |
| ---------- | ------------------------------------ | -------------------------------------------- |
| 時系列     | 時間進行を含むか、含むなら何ヶ月分か | 「即時」「ワンショット」と明言済み           |
| アカウント | Connect 配下か Direct か             | 「Connect」or「シンプル」と明言済み          |
| 規模       | 単発か bulk か（件数）               | 件数が明示されている                         |
| 結果軸     | 成功か、失敗を含むか                 | 「失敗」「失敗カード」「past_due」等の語あり |
| 通貨       | JPY か USD か                        | デフォルトは USD で進めて生成後に確認        |
| 検証目的   | 何を webhook で観測したいか          | 既に明示されている                           |
| Cleanup    | 使い捨てか CI 再現性必要か           | 明言済みなら省略                             |

質問する場合は `ask_user_input_v0` で選択肢として提示する。文章で複数質問を並べない。

### Phase 2: 参照素材の選定

`reference/INDEX.md` を読む。確定した軸に最も近い fixture JSON を1本選び、それを下敷きにする。完全一致を求めず、最も近い1本を選んで改変するほうが、ゼロから書くより検証コストが低い。

参照ファイルとシナリオ軸:

- `failing-subscription.json` — 時系列 × 失敗 × Subscription（最頻）
- `successful-checkout.json` — 即時 × 成功 × Checkout
- `refund-and-dispute.json` — 即時 × Dispute フロー
- `connect-destination-jpy.json` — Connect × JPY（差別化軸）
- `bulk-customers.json` — bulk 展開の参考形
- `subscription-with-trial.json` — 時系列 × Trial 終了

複数軸が交差する場合（例: Connect × bulk × JPY）は、ベース1本を選び、他から要素を引いて合成する。

### Phase 3: JSON 生成

選んだ参照を下敷きに、以下の構造で fixture JSON を組み立てる:

```json
{
  "_meta": {
    "template_version": 0
  },
  "fixtures": [
    {
      "name": "first",
      "path": "/v1/customers",
      "method": "post",
      "params": { "name": "test" }
    },
    {
      "name": "next_step",
      "path": "/v1/customers/${first:id}",
      "method": "post",
      "params": {
        "description": "${first:name} updated"
      }
    }
  ]
}
```

生成時の遵守事項:

- `_meta.template_version` は `0` 固定（2020 年以降変わっていない。 `1` 以上にすると CLI が `Fixture version not supported` で起動しない）
- `name` は短く、後続から参照しやすい命名にする（例: `clock`, `cus`, `pm`, `sub`）
- `${name:path}` の `name` は同 JSON 内で**先に**定義された fixture を指す。前方参照は不可
- 配列要素アクセスは `.[0].id` ではなく `.0.id` を使う（pitfalls.md 参照）
- `expected_error_type` を使えば失敗期待値を書ける（payment_intent 失敗等）。これを使わないとエラー発生時点で fixture 全体が止まる
- bulk を要求された場合、同一構造の entry を機械的に N 個展開する（ここが Skill の最大価値）。N が大きい場合（>20件）は連番命名（`customer_001`, `customer_002`...）を採用
- test_helpers のパス: `/v1/test_helpers/test_clocks`、`/v1/test_helpers/test_clocks/${clock:id}/advance` 等は fixture から叩ける
- `params` 直下の boolean / number は native 型のまま（`true`, `314`）。`metadata` の値は全て文字列化する（API 仕様）
- 仮置きの値（テストカード番号、顧客名等）は出力時に明示する。AI が断定的に値を埋めると、ユーザーが気づかず実行する事故になる

### Phase 4: 検証

生成した JSON に対して以下を順に実施し、結果をユーザーに報告する。

#### 4.1 静的検証（生成と同じターン内で実施）

項目ごとに OK/NG を出す。「検証しました」とだけ書かない。

- `_meta.template_version` が `0`
- 全 `${name:...}` の `name` が同 JSON 内で先に定義済み
- 配列アクセスが角括弧表記ではなくドット表記
- 全 `path` が `/v1/` で始まる
- `method` が `post` / `get` / `delete` のいずれか（`put` は Stripe API では不使用）
- test_helpers パスのスペル一致

#### 4.2 環境チェック指示（ユーザー側で実行）

`STRIPE_API_KEY` の prefix 確認を依頼する。 Skill 側で実行できないため CLI 側の責務:

```bash
echo "${STRIPE_API_KEY}" | grep -q "^sk_test_" && echo "OK: test key" || echo "ABORT: live key suspected"
```

`sk_live_` で始まる場合、 fixture の実行を勧めない。

#### 4.3 実機 dry-run の推奨

reference の JSON は論理構造として正しいが、 stripe-cli の実機実行で全件確認したものではない。最新の API params 名やテストカード挙動が変わっている可能性を考慮し、ユーザーに以下を推奨する:

```bash
# まず最初のステップだけ試す
stripe fixtures generated.json --skip step2 --skip step3

# 1ステップずつ通ることを確認してから全体実行
stripe fixtures generated.json
```

`--add` フラグは既知の panic バグ（pitfalls.md 参照）があるため、`--override` を優先案内する。

### Phase 5: 後処理の案内

生成した JSON を出した後、以下を案内する:

1. 実行コマンド: `stripe fixtures path/to/file.json`
2. cleanup 戦略: 全 fixture entry の `params.metadata` に共通の tag を埋める設計（例: `metadata.test_session=<job-id>`）。後で `stripe customers list` 等でフィルタして削除
3. webhook 観測: `stripe listen --events <events>` の起動例

## 落とし穴

`pitfalls.md` を読む。以下を含む:

- 配列インデックス記法のドット表記とブラケット表記の docs/実装ズレ
- `--add` フラグの panic バグ
- 複数 fixture ファイルを一度に渡せない
- metadata の文字列扱い
- expected_error_type の使い方

これらに該当する操作を生成 JSON に含める場合、 Phase 4 の検証で警告を出す。

## 出力フォーマット

各セッションの最終アウトプットとして以下を提示する:

1. 生成した fixture JSON ファイル
2. 静的検証結果のチェックリスト（Phase 4.1 の項目ごとに OK/NG）
3. 実行手順（dry-run コマンド → 全体実行コマンド → cleanup 手順）
4. 仮置きした値の一覧（ユーザーが実機で差し替える必要がある箇所）

## アンチパターン

以下は明確に避ける。理由を含めて記す:

- **対話なしで JSON を生成する** — ユーザー要件を聞かずに reference をそのまま吐く形になり、結局使えない JSON が出る
- **「動作確認しました」と書く** — この Skill は実機実行できない。「論理構造は確認した」「実機 dry-run を推奨」とは書くが、実行確認の断定はしない
- **reference JSON をそのまま吐く** — 必ずユーザー要件に合わせて改変する
- **`stripe trigger` で済むケースに fixture を生成する** — Phase 0 で撤退判定する

## 参照ファイル

- `reference/INDEX.md` — 同梱 JSON の索引（軸ごとの選び方）
- `reference/*.json` — 各シナリオの参照素材
- `pitfalls.md` — 既知問題集
- `README.md` — Skill 全体の使い方（人間向け）
