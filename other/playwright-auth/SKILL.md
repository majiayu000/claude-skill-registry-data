---
name: playwright-auth
description: Windows・MacのPlaywright認証profileを診断・初回ログイン・状態確認・安全移行する
disable-model-invocation: true
domain: ops
---

# Playwright認証profile運用

## 用途

各PCでPlaywrightの認証保存先を確認し、診断、手動ログイン、read-only状態確認、旧profileの安全な移行を行う。認証ロジックはすべて`scripts/playwright-auth.mjs`へ委譲し、このスキルには複製しない。

## 引数

`$ARGUMENTS`の先頭を次のいずれかとして扱う。

- `paths [service]`: 保存先表示。完全offline
- `doctor [service]`: 権限・空き容量・legacy・lock・重複診断。完全offline
- `login <service>`: headed Chromeで人間がログイン
- `status <service|--all>`: read-onlyページでaccount assert
- `migrate <service> [--commit]`: 同一PCの旧profileをcopy。既定dry-run
- `keygen`: CI用age keypairを生成する（identityはMacのauth root、recipientはregistryへ）
- `export <service>`: authenticatedなローカルstorageStateをage暗号化しprivate R2へ書き出す

## 手順

1. 最初に対象service、実行PC、`auth:paths`のauth root、dry-run/commitを表示する。
2. `paths`は`npm run auth:paths -- --service <service>`、`doctor`は`npm run auth:doctor -- --service <service>`を実行する。
3. `login`は`npm run auth:login -- --service <service>`を実行し、password・2FA・CAPTCHAはユーザーに入力してもらう。Enter入力やprofile存在だけを成功扱いしない。
4. `status`は`npm run auth:status -- --service <service>`、全件は`npm run auth:status -- --all`を順次実行する。`authenticated`以外をPASSと呼ばない。
5. `migrate`は必ず先に`npm run auth:migrate -- --service <service>`でdry-runする。実copyは対象と保存先をユーザーが確認した場合だけ`--commit`を付ける。

## 安全弁

- profile・state・CookieをPC間、クラウド、Gitへ同期しない。
- migrationはtarget非空、service lock、Chromium利用中なら停止する。sourceは削除しない。
- lockを自動削除せず、processをkillしない。
- login/statusは投稿・公開・購入・申請・download・uploadを行わない。
- afbの別process statusは`unsupported`。GmailはPlaywright対象外。
- CIで使うのは暗号化stateのみ。loginは常にローカル。exportはauthenticatedのときだけ送る。

## 参照

- `.claude/knowledge/reference/playwright-auth-profiles.md`
- `.claude/config/playwright-auth-profiles.json`
- `scripts/playwright-auth.mjs`
