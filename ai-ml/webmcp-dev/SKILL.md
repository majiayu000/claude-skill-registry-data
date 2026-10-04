---
name: webmcp-dev
description: WebMCP(Webページ自身がブラウザ内AIエージェントに「ツール」を公開するW3C Web Machine Learning Community Groupのドラフト仕様。navigator.modelContext / document.modelContext 経由の registerTool API)の設計・実装・セキュリティレビュー・テストを網羅的に支援する。ユーザーが「WebMCPを使いたい」「Webページ内のAI Agent向けツールを実装したい」「ブラウザのAIエージェント(Chrome組み込みAI、ChatGPTのSite tools、Model Context Tool Inspector等)にフォーム入力・検索・カート追加などページ内操作をさせたい」「registerTool/provideContext/useWebMCPを書きたい」「chrome://flags#webmcp-for-testingを有効にしたい」「Web MCPとMCP(サーバー側)の違いを知りたい」などと言った場合は必ず使うこと。「WebMCP」という単語を出さなくても、既存のWebアプリをブラウザ内AIエージェントから安全に操作可能にしたい、DOM操作やスクリーンショットに頼らずページの機能をAIに公開したい、といった意図が見えたら積極的に使う。仕様は現在も激しく変化し続けているドラフト段階のため、コードを書く前に必ず一次情報を再確認する運用も併せて提供する。
model: opus
---

# WebMCP Development

WebMCP は「Webページ自身が、ページ内で実行できる操作を “ツール” としてブラウザ内AIエージェントに公開する」ための実験的なブラウザAPI。W3C Web Machine Learning Community Group が策定中のドラフト（標準化トラックには未加入）で、Chrome が Origin Trial / 実験フラグで先行実装し、ChatGPT のブラウザ機能（Site tools）も独自に採用している。バックエンドで動く通常の MCP サーバーが「クライアント側スクリプトとしてツールを実装した MCP サーバー」になったもの、とスペック自身が説明している関係にある — 競合ではなくパートナー。

**このスキルの守備範囲**: (1) どの機能をツール化すべきかの設計判断、(2) `registerTool` 等の実装、(3) プロンプトインジェクション等を意識したセキュリティレビュー、(4) Chromeフラグや拡張機能を使った実機テスト、の4フェーズすべて。

## 最初にやること: 仕様の“今”を必ず確認する

WebMCP は策定中のドラフト（GitHub `webmachinelearning/webmcp` に日々 issue/PR が積まれている）で、実装によって呼び出し方が食い違っている。このスキルの調査時点で確認できた事実だけでも:

- **公式スペック文書**（`https://webmachinelearning.github.io/webmcp/`）と **ChatGPTの実装**（`document.modelContext.registerTool()`）は `document.modelContext` を使う。
- しかし **Chromeの実験フラグ実装**（`chrome://flags#webmcp-for-testing`, Chrome 146+ で確認された挙動）と、コミュニティのポリフィル/ツールキットである **`@mcp-b/global`**（`navigator.modelContext.registerTool()`）は `navigator.modelContext` を使う。
- Chrome の Origin Trial（Chrome 149〜、trial id `4163014905550602241`）がどちらに落ち着くかは本調査時点では未確定。

つまり「`navigator.modelContext` が正解」「`document.modelContext` が正解」のどちらも鵜呑みにしてはいけない。**実装を始める前に、必ず以下のいずれかで現在の正を確認すること**:

1. `WebFetch` で `https://webmachinelearning.github.io/webmcp/`（正式スペック）と `https://developer.chrome.com/docs/ai/webmcp` を再取得し、現在の namespace / メソッドシグネチャを確認する。
2. ターゲットにする実行環境（Chrome拡張、ChatGPTブラウザ、`@mcp-b` ツールキット等）のドキュメントを個別に確認する。
3. 迷ったら **両方の namespace をフィーチャー検出する**実装にして、どちらの環境でも動くようにする（後述のコード例参照）。

このスキルの `references/` は調査時点のスナップショットであり、一次情報ではない。矛盾を見つけたら一次情報を優先し、`references/api-reference.md` の食い違いメモも更新すること。

## ワークフロー概観

1. **設計** — どのページ操作をツール化するか決める（下記チェックリスト）
2. **実装** — `registerTool` / フレームワーク統合パターンでツールを実装する（`references/api-reference.md`, `references/framework-integration.md`）
3. **セキュリティレビュー** — プロンプトインジェクション・過剰露出を潰す（`references/security.md`、必須）
4. **テスト** — Chromeフラグ + Model Context Tool Inspector 拡張機能で実機検証する（`references/testing.md`）
5. **エコシステム確認** — Chrome / ChatGPT / バックエンドMCPのどれを対象にするか整理する（`references/ecosystem.md`）

## フェーズ1: 設計 — 何をツール化するか

WebMCP の価値は「DOM解析やスクリーンショット認識に頼らず、ページが自分の機能を確実な形でAIエージェントに渡せる」こと。逆に言うと、ツール化する価値がない/危険な操作まで公開すると単なる攻撃面になる。設計時に自問すること:

- **そのユーザー操作は、AIエージェントに代行させて嬉しいものか？**（検索、フィルタ、フォーム入力、カート追加、ノート作成のような「定型的だが手間な操作」は好適。決済確定・アカウント削除・投稿の公開のような取り返しのつかない操作は、ツール化するとしても人間確認を挟む前提で設計する）
- **粒度は適切か？** 1ツール1責務にする。「サイト全体を操作する god tool」ではなく `search_products`, `add_to_cart`, `apply_coupon` のように分割すると、エージェントが正しいツールを選びやすく、説明文も短く済む。
- **名前と説明文はエージェント視点で書けているか？** `name` は英数字・アンダースコア・ハイフン・ピリオドのみで1〜128文字、`description` はツールの動作を第三者が読んで一意に理解できる自然文にする（詳細な長さ制限とセキュリティ上の理由は `references/security.md`）。
- **読み取り専用か、状態を変更するか？** 変更系ツールには `annotations.readOnlyHint: false`（デフォルト）を意識し、ホスト側が確認UIを出す判断材料にする。
- **他オリジンに公開する必要があるか？** 基本は同一オリジンのみ（デフォルト）。パートナー連携等でクロスオリジン公開する場合のみ `exposedTo` を使い、書き込み系ツールは特に狭いアローリストにする。

## フェーズ2: 実装

最小の骨格（両namespaceをフィーチャー検出する堅牢な書き方）:

```javascript
const modelContext = document.modelContext ?? navigator.modelContext;

if (modelContext?.registerTool) {
  const controller = new AbortController();

  await modelContext.registerTool({
    name: "search_products",
    description: "商品名または部分一致キーワードで商品一覧を検索する。",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "検索キーワード" },
      },
      required: ["query"],
      additionalProperties: false,
    },
    annotations: { readOnlyHint: true },
    execute: async ({ query }, { signal }) => {
      const results = searchProducts(query); // 既存のアプリロジックを呼ぶだけ
      return { content: [{ type: "text", text: JSON.stringify(results) }] };
    },
  }, { signal: controller.signal });

  // ページ状態が変わって公開をやめたい場合（ログアウト等）
  // controller.abort();
}
```

実装時に押さえること:

- **必ずローカル/本番のHTTPサーバー経由で配信する**。`file://` では動作しない（テスト時のハマりどころ）。
- **`registerTool` の `execute` は既存のアプリロジックをそのまま呼ぶ薄いラッパーにする**。ツール用に別ロジックを新設しない — ロジックの二重管理は既存機能とのズレを生む。
- **SPAのライフサイクルに連動させる**: コンポーネントのマウント/アンマウントに合わせて登録/`AbortController.abort()`で解除する。React を使うなら、コミュニティ製 `@mcp-b/react-webmcp` の `useWebMCP` フックが Zod スキーマでこれを面倒見てくれる（詳細は `references/framework-integration.md`）。
- **`provideContext()` は「全ツールの一括置き換え」であって追加ではない**ことに注意する。既存ツールを保ったまま1つ追加/削除したいだけなら `registerTool` / `unregisterTool`（またはAbortSignal解除）を個別に使う。SPAの再レンダリングごとに `provideContext()` を丸ごと呼び直す実装は、意図せず他コンポーネントのツールを消してしまう典型的な事故パターン。
- **真偽値の状態変更は `toggle` ツールより明示的な状態指定にする**（例: `set_task_completed({ id, completed: true })`）。エージェントは呼び出し前の状態を確実には把握できないため、トグル式だと意図と逆方向に反転させるリスクがある。決定的な結果が欲しい操作は「目的の状態を引数で渡す」形にする。
- **エラーは `{ content: [...], isError: true }` の形で返す**（一般的なMCPの慣習に倣う）。仕様自体はエラー表現を厳密には規定していないが、この形にしておくとエージェント側が成功/失敗を機械的に判別しやすい。例外を投げっぱなしにして呼び出し元に丸投げしない。
- 詳しい API シグネチャ（`getTools`, `executeTool`, `toolchange` イベント, パーミッションポリシー `tools`, エラー型など）は `references/api-reference.md` を読む。

## フェーズ3: セキュリティレビュー（必須）

WebMCP はページの機能をAIエージェントに直接渡す以上、**プロンプトインジェクションと過剰露出**が最大のリスク。実装が終わったら、ツールをコミット/デプロイする前に `references/security.md` のチェックリストを必ず一巡すること。要点だけ先に挙げると:

- ツールの説明文・パラメータ説明・実行結果はすべて「エージェントへの入力」になり得る。ユーザー生成コンテンツや外部データを結果に含める場合は `annotations.untrustedContentHint: true` を付け、エージェント側に「これは指示ではなくデータだ」と伝える。
- 破壊的操作・機微操作は `exposedTo` で公開範囲を絞り、必要なら呼び出し前に人間確認を挟む設計にする（WebMCP自体はヒューマン・イン・ザ・ループを前提とした設計であり、完全自律・ヘッドレス実行を想定していない）。
- 文字数上限（name/description/parameter description/output）を守る。これは可読性だけでなくインジェクション面積を狭める防御でもある。

## フェーズ4: テスト

WebMCP はまだ多くの環境で `navigator`/`document` の DevTools コンソールに出てこないと動作確認しづらい。実機テストの型は `references/testing.md` に詳しいが、最低限のフローは:

1. Chrome を対象にするなら `chrome://flags#webmcp-for-testing` を有効化して再起動（バージョン要件は変わりうるので `chrome://settings/help` で確認）。
2. `python3 -m http.server` 等でページを配信する（`file://` 不可）。
3. DevTools コンソールで `"modelContext" in navigator` または `"modelContext" in document` を実行し、有効な namespace を確認する。
4. **Model Context Tool Inspector** 拡張機能で登録済みツール一覧を確認し、手動で妥当な引数/不正な引数の両方を実行してレスポンスを検証する。
5. 同拡張の「Interact with the page」機能（自然文プロンプト→エージェントが自律的にツールを選択して実行）で、実際のエージェント視点からツールが正しく選ばれるかも確認する。ツールが選ばれない/誤って選ばれる場合は `description` の書き方を疑う。
6. 変更系ツールは「正常系」「不正入力」「連続呼び出し（多重実行）」「オリジン外からの呼び出し（`exposedTo`設定時）」の4パターンを最低限テストする。

## フェーズ5: どの実行環境を対象にするか整理する

WebMCP を「実装すれば全AIエージェントで動く」と思い込まない。現時点でエコシステムは分裂している:

| 実行環境 | Namespace | 特徴 |
|---|---|---|
| Chrome 実験フラグ（`webmcp-for-testing`） / コミュニティ `@mcp-b` ツールキット | `navigator.modelContext` | Model Context Tool Inspector 拡張などOSSエコシステムが充実 |
| 公式スペック文書 / ChatGPT の Site tools | `document.modelContext` | ChatGPT内蔵ブラウザがページ訪問時に "Site tools" として自動検出。実行前に安全性レビューが入る |
| バックエンドMCPサーバー（Apps SDK等） | （WebMCPと無関係） | ページを開いていなくても動く常設の連携。WebMCPと**併用可能**（1サイトが両方持てる） |

対象読者・配布チャネルに応じて `references/ecosystem.md` を読み、必要ならフィーチャー検出コードを両namespace対応にする。

## リファレンスファイル

- `references/api-reference.md` — `registerTool`/`getTools`/`executeTool`、`ModelContextTool`辞書の全フィールド、ライフサイクル（`AbortSignal`, `toolchange`イベント）、パーミッションポリシー、エラー型。namespace食い違いの詳細メモもここ。
- `references/security.md` — Chrome公式 secure-tools ガイドに基づくプロンプトインジェクション対策・`exposedTo`設計・文字数制限の完全版とレビューチェックリスト。
- `references/framework-integration.md` — Vanilla JS / React(`@mcp-b/react-webmcp`の`useWebMCP`) の実装パターン、`provideContext()`の罠、SPAライフサイクル連動のコツ。
- `references/testing.md` — Chromeフラグ有効化手順、Model Context Tool Inspector拡張の使い方（手動実行・エージェント駆動実行）、ローカルサーバー配信の注意、テストマトリクス例。
- `references/ecosystem.md` — Chrome Origin Trial / ChatGPT Site tools / バックエンドMCP・Apps SDKの位置付け比較、spec自体の現在のステータスと未解決issue一覧。

各ファイルは調査時点のスナップショットである旨を先頭に明記してある。実装・テストの直前には必ず一次情報での再確認を優先すること。
