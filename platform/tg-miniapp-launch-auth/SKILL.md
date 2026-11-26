---
name: tg-miniapp-launch-auth
description: "Use when choosing how a Telegram Mini App opens (keyboard, inline or menu button, main app, direct link, startapp, join request) or when a server must trust a Mini App user: validating initData by HMAC or Ed25519, signature in the check string, auth_date, isVersionAtLeast gating, origin protection, test environment and debugging."
license: MIT
---

# tg-miniapp-launch-auth

Checked against the official docs on 2026-10-30: Bot API 10.3 (latest, August 24, 2026), Mini Apps page with Recent changes up to 10.1, `telegram-web-app.js?64`. The Mini Apps page doesn't describe origin protection (see below); the changelog does.

## Not verified live

No bot, client or device was used to write this skill. These checks wait for a live Mini App:

- A fresh `initData` string with `signature` from a live bot in 2026. The repository's tests use synthetic vectors, so they prove this code matches the algorithm below, and only a live string proves Telegram still signs that way. We found no public vector for Telegram's Ed25519 key without a real person's data, so that key is untested here.
- Launch behavior on a real iPhone and Android device. The launch table comes from the docs.
- Origin protection: what a blocked call looks like, and whether subdomains and redirects count as the Mini App domain.
- `mode=fullscreen` in links.

## Pick a launch path

| Path | Set up | `initData` | How the app answers |
|---|---|---|---|
| Inline button | `InlineKeyboardButton.web_app`, private chats only | `user`, `query_id` | `answerWebAppQuery` sends a message on the user's behalf and closes the app |
| Menu button | BotFather `/setmenubutton`, or `setChatMenuButton` with `MenuButtonWebApp` for one chat | same as inline button | same as inline button |
| Main Mini App | BotFather, then `t.me/<bot>?startapp[=value][&mode=compact]` | `user`, `chat_type`, `chat_instance`, `start_param` | own server |
| Direct link | Named app in BotFather, then `t.me/<bot>/<app>?startapp=value&mode=compact` | same as main app; no access to the chat | own server; to send a message, send the user back to inline mode |
| Rich message button | `RichMessageButton.web_app` (10.3), private chats only | same as inline button | same as inline button |
| Join request (10.1) | Guard bot: `sendChatJoinRequestWebApp` on `chat_join_request` | `user`, `chat`, `chat_join_request_query_id` | `answerChatJoinRequestQuery` with `approve`, `decline` or `queue` |
| Keyboard button | `KeyboardButton.web_app`, private chats only | **empty** | `sendData`, up to 4096 bytes: the bot gets a `web_app_data` service message and the app closes |
| Inline mode | `InlineQueryResultsButton.web_app` in `answerInlineQuery` | **empty** per `WebAppInitData` | `switchInlineQuery` sends the user back to pick a result |

Take the first row that fits. Choose a path with a verifiable `user` whenever the server needs identity: keyboard and inline mode launches carry none.

The attachment menu is available only to major advertisers on the Telegram Ad Platform; other bots can use it only on the test server. `requestChat` (9.6) with `savePreparedKeyboardButton` lets an open app ask the user to pick a chat.

### `start_param`

`startapp` takes up to 64 characters, `A-Z`, `a-z`, `0-9`, `_` and `-`; use base64url for binary data. The value arrives in `initData.start_param` and in the GET parameter `tgWebAppStartParam`.

- The GET parameter is unsigned: use it to pick a screen. Anything a server trusts comes from validated `start_param`.
- The `WebAppInitData` table says `start_param` is returned only for the attachment menu. The main app and direct link sections of the same page say it is passed there too. Follow those sections.

### Opening height

The main app and direct links open at full height by default; `mode=compact` opens them at half height. `mode=fullscreen` appears only in the [MTProto links page](https://core.telegram.org/api/links), so treat it as unconfirmed for the Bot API docs.

## Trust a user on the server

`Telegram.WebApp.initData` is the only input to validate. `initDataUnsafe` is a convenience for rendering and proves nothing.

1. The client sends the raw `initData` string unchanged, for example `Authorization: tma <initData>` (a tma.js convention).
2. The server rejects an empty value. Keyboard and inline mode launches have no identity; don't fall back to `initDataUnsafe`.
3. The server validates `hash`, then `auth_date`.
4. The server parses `user` from the validated fields and stores `id` in a 64-bit type: it has up to 52 significant bits.

### Bot token scheme

`secret_key = HMAC_SHA256(key="WebAppData", msg=bot_token)`, then `hash = hex(HMAC_SHA256(key=secret_key, msg=data_check_string))`. The check string is all received fields except `hash`, URL-decoded, sorted by key, as `key=value`, joined with `\n`. Compare in constant time.

**`signature` stays in this string.** The docs say "all received fields" and don't name it. tma.js excludes only `hash` ([`validation.ts:94`](https://github.com/Telegram-Mini-Apps/tma.js/blob/a841aba28517c138af7debf4ad557fcf0c1f92fd/packages/init-data/src/validation.ts#L94)). On 2026-10-30 a string that tma.js publishes as signed by Telegram (created 2024-12-07) matched only with `signature` kept. That string names a real person, so it stays out of this repository. Keep the exclusion list to `hash` alone.

[`scripts/init_data.py`](scripts/init_data.py) does this with the standard library and no network. It rejects repeated keys, because a duplicated field could mean one thing to the check and another to your code. `max_age=0` skips the age check, and `now` overrides the clock in tests. JSON fields such as `user` stay strings for you to parse:

```python
from init_data import InitDataError, validate

try:
    fields = validate(raw_init_data, bot_token, max_age=3600)
except InitDataError as error:
    return reject(401, error.code)   # malformed, missing_hash, invalid_hash, invalid_auth_date, expired
user = json.loads(fields['user'])
```

### `auth_date`

The docs make the check optional and name no limit. tma.js defaults to 86400 seconds. Pick your own limit by the value of the action.

`initData` is issued once, when the app opens, and carries no nonce. An app left open past your limit starts getting `expired`, so plan a reopen prompt or issue your own short session after the first validation.

### Third party without the token

Share `initData` and `bot_id`; the third party verifies `signature`, an Ed25519 signature in base64url, with Telegram's public key.

- Check string: `<bot_id>:WebAppData\n`, then fields except `hash` and `signature`, sorted, `key=value`, joined with `\n`.
- Production key: `e7bf03a2fa4602af4580703d88dda5bb59f32ed8b02a56c187fe7d34caed242d`
- Test key: `40055058a4ee38156a06562e52eece92a771bcd8346a8c4615cb7376eddf72ec`
- Telegram sends the signature without `=` padding, and strict base64 decoders reject it. `third_party_payload` restores it.
- The standard library has no Ed25519, so `third_party_payload` only prepares `(message, signature)` and the check stays with your verifier.
- The docs require the third party to validate `auth_date` as well.

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from init_data import third_party_payload, parse_init_data

message, signature = third_party_payload(raw_init_data, bot_id)
Ed25519PublicKey.from_public_bytes(bytes.fromhex(PRODUCTION_KEY)).verify(signature, message)
auth_date = int(parse_init_data(raw_init_data)['auth_date'])  # check it yourself
```

## Gate features by version

`Telegram.WebApp.version` is the Bot API version of the user's client. Calling a method above it fails: in `telegram-web-app.js` `requestFullscreen` logs to the console and throws `WebAppMethodUnsupported`.

```js
const app = Telegram.WebApp;
if (app.isVersionAtLeast('8.0')) app.requestFullscreen();
```

`isVersionAtLeast` proves the method exists, not that it will work: see the iOS report in [`../tg-miniapp-ui/client-pitfalls.md`](../tg-miniapp-ui/client-pitfalls.md).

## Origin protection

Since July 20, 2026 Mini App methods can't be called from origins other than the original Mini App domain. It is on by default for all Mini Apps ([changelog, Bot API 10.2](https://core.telegram.org/bots/api-changelog#july-14-2026)).

- Call every `Telegram.WebApp` method, `openInvoice` included, from a page on the Mini App domain.
- Sites opened by links inside the app lose those methods.
- A flow that leaves your domain and returns needs a live test: the docs don't define "original domain" for subdomains and redirects.
- The opt-out lives in the @BotFather Mini App. With it, the bot's owner answers for the app having no links to untrusted sites.

## Telegram Serverless

The Mini Apps page lists `Telegram.WebApp.Serverless`, where the platform validates `initData` before running a bot's endpoint. [Its docs](https://core.telegram.org/bots/serverless) name no access terms or prices, and a [practitioner report](https://hackernoon.com/telegram-can-host-your-bot-should-you-give-up-your-vps) describes a closed test, so this skill assumes your own server.

## Test and debug

Test server login, inspectors per platform and the mock for a plain browser: [`references/testing-debug.md`](references/testing-debug.md).

## Sources

- Mini Apps: https://core.telegram.org/bots/webapps · changelog https://core.telegram.org/bots/api-changelog · links https://core.telegram.org/api/links · deep linking https://core.telegram.org/bots/features#deep-linking
- `telegram-web-app.js`: https://telegram.org/js/telegram-web-app.js?64
- tma.js, `signature` handling, read and not vendored: commit `a841aba28517c138af7debf4ad557fcf0c1f92fd`, `packages/init-data/src/validation.ts` (SHA-256 `1592acd7e04283cfb9a6103b0d48b5816f1e617ca0bd1e862277d534a65c1472`), MIT in `packages/init-data/LICENSE` (SHA-256 `c44881466bac14b6b7e30e35073940d15081efbadcf37f7e70993015cf0c0ef7`), fixture string in `packages/init-data/test/fixtures.ts` (SHA-256 `77825e04c296754da8d9667dfe072403725c442eb52f34dcdc48bbadbfa6189e`) · padding note https://github.com/Telegram-Mini-Apps/tma.js/blob/master/apps/docs/platform/init-data.md
