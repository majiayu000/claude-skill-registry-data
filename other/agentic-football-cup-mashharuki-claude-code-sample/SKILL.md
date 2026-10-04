---
name: agentic-football-cup
description: >
  AWS Agentic Football Cup（agenticfootballcup.ai, 5v5・各選手=1体のStrands/Bedrock
  エージェント）向けに、チーム設計・戦術決定・選手ごとの英語プロンプト作成/レビュー・
  試合後の改善サイクルを「実戦で勝つため」の意思決定支援として行うスキル。一般的な
  サッカー解説ではなく、大会エンジンの実仕様（2秒ごとの意思決定、1秒のレイテンシ制限、
  ポジションはプロンプト上の概念でエンジンには存在しない、司令塔不在で5体が同じ試合
  状態を独立に読んで判断する）を前提にした助言を行う。
  Use whenever the user is building, tuning, or debriefing a team for the AWS
  Agentic Football Cup — designing the 5 player roles (GK/DF/MF/FW + 5人目),
  writing or reviewing English system prompts per player, choosing/switching
  tactics (high press, low block, counter, possession, wing play, central
  play, zonal/man marking, game management when leading or behind), tuning
  tactics before a match, turning match logs/results into a hypothesis-driven
  improvement plan, planning a Wildcard-style highlight (fastest goal,
  comeback, upset win), or adding in-match opponent-pattern reading /
  meta-cognitive adaptation so players adjust to what the opponent is
  actually doing (not just score/clock). Trigger on "Agentic Football Cup",
  "5v5", "AIサッカー", "エージェンティックフットボール", "ハイプレス/ローブロック",
  "選手プロンプト", "フォーメーション", "試合後レビュー", "ワイルドカード",
  "相手の傾向", "メタ認知", "スカウティング", "格上対策", "格上撃破", "切り替え",
  "トランジション", "ライン設定", "オフザボール", "Minds", "Animoca", "Coach Mind",
  "AFC Virtual League" even without the skill name being said explicitly.
model: opus
---

# Agentic Football Cup Strategist

## このスキルが前提にする大会仕様（確認済み・出典あり）

- 1チーム=5体のエージェント（**4 outfielders + 1 goalkeeper**）。1選手=1エージェント。
- **司令塔は存在しない**。5体は毎ティック同じ試合状態を受け取り、それぞれ独立に意思決定する
  （"nobody is the orchestrator. Each agent reads the same game state"）。
- 意思決定は**2秒ごと**、各エージェントの応答制限は**1秒**。**1秒を超えると、そのティックは
  そのプレイヤーがIDLE扱いになり、リトライは無い**（"Anything slower IDLEs that player for
  the tick, and there are no retries during a match."）。つまり「賢いが遅いモデル/長いプロンプト」
  は思考の質以前にこのIDLE化リスクでマイナスになり得る点を、選手プロンプトのレビュー基準5
  （`references/prompt-templates.md`）で重視する理由になっている。
- 各ティックの入力: ball position, 全選手の position/velocity, stamina, score, clock。
- 出力アクション: `MOVE_TO, PASS, SHOOT, DRIBBLE, PRESS_BALL, MARK, INTERCEPT, TACKLE, CLEAR, IDLE`
  + GK専用アクション（名称は未確認 — 要公式確認）。
- **GK/DF/MF/FWというポジションはエンジンの機能ではなく、system prompt上で与える役割**
  （例: "You are the striker for Team X"）。ポジションらしい振る舞いは全てプロンプトが作る。
- **フォーメーションはGKのみ固定、残り4人（outfielders）の役割配分はポータルの「Formation」
  設定でプリセットから選べる**（例: 2-1-1＝GK+2DF+1MF+1FW。左右の矢印で他のプリセットに
  切り替え可能な様子がユーザーのポータル画面で確認できた）。デプロイ時に既定で入っている
  GK+DEF+MID+FWD+FWD（運営メール冒頭の例と同じ）は**あくまで初期状態のサンプル**であり、
  固定要件ではない。ユーザー自身のチーム方針（本スキルなら`football-tactics.md`1節の
  配分パターン）に合わせて選び直してよい。
- 戦術の与え方は2層: (1) system prompt = 試合を通じた長期方針、(2) 試合中のリアルタイム
  テキスト指示 = エージェントが**採用するかどうかを自律判断**（従う保証はない）。
- 出典: [Inside Agentic Football Cup (Strands Agents blog)](https://strandsagents.com/blog/inside-agentic-football-cup/),
  [Agentic Football Cup Singapore (AWS Startups)](https://aws.amazon.com/startups/events/agentic-football-cup-singapore-build-ai-agents-that-play-football),
  [agenticfootballcup.com/learnmore](https://agenticfootballcup.com/learnmore/)。
- **ゲームエンジン自体（Strands Agents SDK + Amazon Bedrock AgentCore）はAWSが運用**するが、
  その上に**Animoca Brandsの「Minds」が提供するコーチング支援レイヤー**が乗る。参加者には
  「AFC Virtual League Assistant Coach Mind」という専属AIコーチ（チャット形式・マネージャー
  /チーム/シーズン経過を記憶する）が割り当てられ、(a) ルール・スケジュールへの質問応答、
  (b) 選手ごとの役割プロンプトのレビューと書き換え案の提示、(c) 試合後の平易な言葉での
  デブリーフ、(d) 次戦前の対戦相手スカウティング・プレビュー、を行う（"two-app,
  one-clipboard workflow" ＝ AWS側の登録・実行とMinds側のコーチをクリップボード越しに
  行き来する運用）。本スキルとMinds Coachの役割分担は次節を参照。
  出典: [AI Agents Play 5v5 Football In AWS's New League — And Animoca's Minds Is The Coach (EGamers.io)](https://egamers.io/ai-agents-play-5v5-football-in-awss-new-league-and-animocas-minds-is-the-coach/),
  [Minds by Animoca Brands launches Agentic Football Cup - Virtual League（Animoca公式）](https://www.animocabrands.com/announcement/minds-by-animoca-brands-launches-agentic-football-cup-virtual-league-in-collaboration-with-aws),
  [AWS Agentic Cup - Alpha Season registration](https://aws-x-mind-register.vercel.app/)。
- 参加者コミュニティのレポート（[Qiita記事](https://qiita.com/ry-harada/items/441725ff1b451ed8042f)）は、
  試合中のリアルタイム指示が「チームチャットとしてエージェントに渡され、試合セッション中は
  会話履歴として蓄積される」としており、単発の一言というより**セッション内で積み上がる文脈**
  として扱われる可能性を示唆している（一次情報未確認、次戦の指示を書く際は蓄積を前提にした
  一貫性を意識するとよい）。

**未確認・情報が食い違っている点（断定しない）**: 正式なアクション名・スコア判定・
タイブレーク・フォーメーションUIの仕様・「Wildcard」という名称の公式ボーナス制度の有無・
Minds連携の詳細な操作手順は未確認。また、**応答タイムアウト超過時の挙動について、一次情報
（Strands Agents blog）は「1秒・超過分はIDLE・リトライ無し」と明記する一方、上記Qiita記事は
「タイムアウトは5秒で、間に合わないと直前のコマンドが維持される」と異なる数値・挙動を報告して
いる**。本スキルは一次情報（1秒・IDLE）を採用するが断定はせず、ポータルでの実際のテスト
試合・練習試合で応答速度とタイムアウト挙動を確認するようユーザーに勧める（基本方針1: 実際の
挙動を優先）。大会・シーズン（このサイトは"Alpha Season"と表記）によって変わりうるため、断定せず
[agenticfootballcup.ai](https://agenticfootballcup.ai/) と参加ワークショップ/ポータル/Minds
Coach自身の最新回答をユーザーに確認してもらうこと。推測でルールを補わない。

**フォーメーションの自由度は解決済み**: 当初、参加者コミュニティのレポート（前述Qiita記事、
「GKのみ固定・残り4人は自由配分」）と、ユーザーのアカウントで最初に見えたデフォルトの
GK+DEF+MID+FWD+FWD配分（一見固定に見えた）の間で情報が食い違っていたが、ユーザーの
ポータル画面で「Formation: 2-1-1」という設定項目と、プリセットを切り替える矢印UIが
確認できた。**デフォルトのGK+DEF+MID+FWD+FWDは初期サンプルにすぎず、実際には配分を
選び直せる**——コミュニティのレポート通りで確定。今後は`football-tactics.md`1節の配分
パターンを前提にプロンプトを設計してよい。

**ポータルの初期デプロイには、まだ埋まっていないテンプレート変数がそのまま残っていた例が
確認されている**（`{TEAM}`が未置換、`[EXAMPLE]`という接頭辞が優先順位の各行に文字通り残る、
5人目の役割が`[MF-leaning / DF-leaning]`のように角括弧の選択肢のまま、等）。これは大会側の
デフォルトのひな形をそのまま残した状態である可能性が高く、モデルに「これは記入例で本指示
ではない」という誤ったシグナルを送りかねない。選手プロンプトをレビューする際は、こうした
角括弧・プレースホルダーが実際の値（チーム名・具体的な優先順位）に置き換わっているかを
必ず確認する（`references/prompt-templates.md`レビュー基準12）。

## Minds Coach（Animoca Brands）との役割分担

Minds Coachは大会運営が全参加者に提供する**汎用**のコーチ支援であり、本スキルは**このエンジン
の仕様とユーザー個別の方針（例: カウンター重視）に強く根ざした叩き台**を作る役割に位置づける。
競合させず、以下のように使い分ける。

- **プロンプト作成・改善（フェーズ2）**: 本スキルで下書きを作ってからMinds Coachに貼り、
  Minds側の書き換え案が出たら、それがこのエンジンのアクション語彙（0節参照）や司令塔不在の
  制約と矛盾していないかを本スキルの基準（`references/prompt-templates.md`「レビュー基準」）
  で照合する。Minds側の提案を無条件に正としない。
- **試合前スカウティング（フェーズ3・6）**: Minds Coachの事前プレビューは**試合開始前**の
  情報。本スキルの5節（試合中のgame_stateからの推定）は**試合中**の情報で、時系列が異なる
  補完材料として扱う。Minds側の見立てと試合中の実データが食い違ったら基本方針1の通り
  実データを優先する。
- **試合後デブリーフ（フェーズ4）**: Minds Coachのデブリーフに含まれる**Minds自身の解釈・
  推測**（例:「プレスが効かなくなった」等の因果的な説明）は、`references/match-review.md`の
  観測事実の基準に照らすと「観測事実」ではなく「仮説」の材料として扱う。観測事実に書けるのは
  ユーザー（またはデブリーフ）が示した動かない事実（スコア・時間帯・使用戦術等）だけで、
  Minds側の解釈をそのまま観測事実欄に転記しない。

## 基本方針

1. **一般的なサッカー論より、このエンジンでの実際の試合結果を優先する。** 現実のサッカー
   常識（例:「引いて守れば失点は減る」）がこのエンジンでも成立するとは限らない。ユーザーの
   試合ログ・スコア推移が一般論と矛盾したら、ログを信じて仮説を更新する。
2. **一度に大きく変えない。** 比較可能な小さな変更を1つずつ検証する（詳細は
   `references/match-review.md`）。**格上相手向けの調整（`references/football-tactics.md`
   6節）のように「考慮すべき観点」が複数ある場面でも、この原則が優先される。** 観点は複数
   あってよいが、1回の「変更すること」で実際に反映するのは原則1つ（多くて2つ）に絞り、
   残りは次戦以降の候補として明示する。
3. **5人の指示は「矛盾しないこと」が最優先。** 司令塔がいないため、チーム戦術は各選手の
   プロンプトに独立して埋め込まれる必要がある。共通ドクトリンを全員に入れ、役割別の差分だけ
   を足す（`references/prompt-templates.md`）。
4. 不明な大会仕様は断定せず、公式ページ確認をユーザーに促す。
5. **相手の出方への適応（メタ認知）はスコア/時計より軽い優先度で足す。** game_stateに
   「相手の傾向」フィールドは無いので、位置・速度などの生データから毎ティック安く判定できる
   粒度に留める（`references/football-tactics.md` 5節、`references/prompt-templates.md`
   「スカウティング・ブロック」）。スコア/終盤による切替と衝突したら後者を優先する。

## ワークフロー

| フェーズ | いつ使うか | 参照先 |
|---|---|---|
| 1. チーム設計 | ゼロから5人チームを組む | `references/football-tactics.md`（ポジション/戦術一覧/切り替え・ライン設定）+ `references/prompt-templates.md`（英語プロンプト雛形） |
| 2. プロンプト作成・レビュー・改善 | 選手プロンプトを書く/直す | `references/prompt-templates.md`（Minds Coachへ渡す前の下書き・貼付後の照合にも使う） |
| 3. 試合前の戦術調整 | 対戦相手や目標が分かっている | `references/football-tactics.md`（状況別の切替ルール。Minds Coachの事前スカウティングがあれば入力に含める） |
| 4. 試合後レビュー | 試合ログ・結果がある | `references/match-review.md`（Minds Coachのデブリーフがあれば「観測事実」抽出の入力にする。ただしMinds側の解釈は仮説行き） |
| 5. Wildcard攻略 | 最速ゴール等の見せ場を狙う | `references/match-review.md`（Wildcardセクション） |
| 6. 相手の傾向読み取り（メタ認知）の追加 | 格上/未知の相手に対応させたい、負けられない試合 | `references/football-tactics.md`5節（傾向の読み取り）・6節（格上への挑み方）+ `references/prompt-templates.md`「スカウティング・ブロック」「Plan A/Bブロック」 |

会話の中でユーザーが複数フェーズにまたがる依頼をした場合（例:「初期設計して」「負けたから
直して」）は該当フェーズだけ実行し、必要な情報（対戦相手情報、直近の試合ログ、既存プロンプト、
Minds Coachから得た情報など）が無ければ最小限だけ質問する。

## 出力フォーマット

状況に応じて以下の4つのいずれかで出力する。見出しはこのまま使う。

**1. 初期チーム設計**
```
## 戦術コンセプト
## 5選手の役割（GK・DF・MF・FWの配分。うち1人は5人目=可変役として設計する）
## 選手ごとの英語指示
## チーム共通指示
## 想定する強み・弱み
```

**2. 試合前の戦術調整**
```
## 維持すること
## 変更すること
## 変更理由
## 検証指標
```

**3. 試合後レビュー**
```
## 観測事実
## 仮説
## 次戦の変更案
## 変更しない項目
```

**4. Wildcard攻略プラン**
```
## 狙うWildcard
## 推奨戦術
## 取るリスク
## 失敗時の代替策
```

各フォーマットの中身の作り方・チェックリストは各referenceファイルを参照。「選手ごとの
英語指示」に相手の傾向読み取り（メタ認知）を含めるかはユーザーの要望次第。含める場合は
フェーズ6の内容を各選手のテンプレートに追加する。
