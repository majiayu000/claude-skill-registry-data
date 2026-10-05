---
name: yamato-change
description: ヤマト運輸メールのリンクから受取日時を変更し、不確定な配達予定を確定時間帯に縮約する手順。ユーザーが「ヤマトの受取日時を変更して」「荷物予定の不確定性を減らして」「明日の荷物予定を特定時間帯にしたい」と依頼したときに使う。
---

# Yamato Delivery Time Change

## 目的

- ヤマト運輸メールの「受取の日時や場所をご指定ください」リンクを使って受取時間帯を確定する。
- 必要なら Google Calendar の「終日/長時間の仮ブロック」を確定時間帯に更新する。

## 前提

- Gmail 取得は `gog` を使う（`/home/yuiseki/bin/gog`）。
- Web 操作は `playwright-cli` を使う。
- この環境では `playwright-cli` の Chromium で `ERR_HTTP2_PROTOCOL_ERROR` が出ることがあるため、`--browser=firefox` を優先する。
- `keyring_backend=file` のため `gog` は TTY 実行を使う。

## 対象メールの選び方

- 対象にする:
  - 件名に `お荷物お届けのお知らせ【受取の日時や場所をご指定ください】` を含むもの
- 対象外にする:
  - 件名に `【郵便受け】` を含むもの（受取時間指定が不要なことが多い）

検索例:

```bash
/home/yuiseki/bin/gog --account <email> gmail search 'from:mail@kuronekoyamato.co.jp newer_than:3d' --max 10 --json
```

## 変更リンクの抽出

スレッド取得:

```bash
/home/yuiseki/bin/gog --account <email> gmail thread get <threadId> --json > /tmp/yamato_thread_raw.json
```

`member.kms.kuronekoyamato.co.jp/parcel/detail` の URL を抽出し、最初の1件を使う:

```bash
python3 - <<'PY'
import json, base64, re
raw = open('/tmp/yamato_thread_raw.json', encoding='utf-8', errors='ignore').read()
raw = raw[raw.find('{'):] if '{' in raw else raw
obj = json.loads(raw)
msg = max(obj['thread']['messages'], key=lambda m: int(m.get('internalDate','0')))
def walk(p):
    m = p.get('mimeType','')
    d = (p.get('body') or {}).get('data')
    if m.startswith('text/plain') and d:
        return d
    for c in p.get('parts') or []:
        r = walk(c)
        if r:
            return r
    return None
b64 = walk(msg.get('payload', {}))
text = msg.get('snippet','')
if b64:
    b64 += '=' * (-len(b64) % 4)
    rawb = base64.urlsafe_b64decode(b64.encode('ascii'))
    for enc in ('utf-8','iso-2022-jp','cp932','latin1'):
        try:
            text = rawb.decode(enc); break
        except Exception:
            pass
urls = re.findall(r'https?://\\S+', text)
urls = [u.strip(')"\\'.,<>') for u in urls]
targets = [u for u in urls if 'member.kms.kuronekoyamato.co.jp/parcel/detail' in u]
if not targets:
    raise SystemExit('NO_PARCEL_URL')
open('/tmp/yamato_parcel_url.txt','w',encoding='utf-8').write(targets[0])
print(targets[0])
PY
```

## Playwright 操作

1. ブラウザを開く（Firefox 推奨）。

```bash
playwright-cli -s=yamato open --browser=firefox "$(cat /tmp/yamato_parcel_url.txt)"
```

2. 「日時を変更する」を押す。
`snapshot` では disabled 表示が混在する場合があるため、`enabled` なボタンを直接探してクリックする。

```bash
playwright-cli -s=yamato eval "() => { const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('日時を変更する') && !b.disabled); if(!btn) throw new Error('NO_ENABLED_CHANGE_BUTTON'); btn.click(); return location.href; }"
```

期待 URL: `/parcel/receive/change/datetime`

3. 希望日と希望時間帯を選び、`次へ`。

```bash
playwright-cli -s=yamato snapshot
```

snapshot の `ref` を確認してクリックする。
- 例: `2月20日(金)` の radio
- 例: `19時～21時`
- `次へ`

4. 確認画面で `確定`。

```bash
playwright-cli -s=yamato snapshot
```

確認ポイント:
- `受取日時変更内容確認`
- `受け取り希望時間帯` が期待どおり（例: `19時～21時`）

確定:

```bash
playwright-cli -s=yamato click <確定ボタンのref>
```

5. 完了画面を確認する。

```bash
playwright-cli -s=yamato snapshot
```

確認ポイント:
- `受取変更完了`
- `変更依頼完了`
- `受け取り希望時間帯` が期待どおり

6. 終了。

```bash
playwright-cli -s=yamato close
```

## カレンダー反映（任意）

不確定ブロック（例: 09:00-20:00）を確定時間帯に更新する。

```bash
/home/yuiseki/bin/gog --dry-run --account <email> calendar update primary <eventId> \
  --summary '荷物が届く（ヤマト 19時-21時）' \
  --from '2026-02-20T19:00:00+09:00' \
  --to '2026-02-20T21:00:00+09:00' \
  --transparency busy --json
```

問題なければ `--dry-run` を外して実行する。

## トラブルシュート

- `ERR_HTTP2_PROTOCOL_ERROR`（Chromium）:
  - `playwright-cli -s=yamato open --browser=firefox ...` を使う。
- 「日時変更」ボタンが見つからない:
  - `playwright-cli -s=yamato eval` で `innerText` を使って `enabled` ボタンを探す。
- 場所変更ボタンが disabled:
  - クロネコメンバーズログインが必要なケースがある。日時変更のみ先に確定する。
- `gog` 実行で keyring エラー:
  - TTY 実行、または `GOG_KEYRING_PASSWORD` を設定する。
