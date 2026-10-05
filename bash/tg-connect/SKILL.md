---
name: tg-connect
description: "ПОДКЛЮЧИТЬ Telegram на ЭТОЙ машине — оба стека сразу: Telethon-рельса (роботы, 0 LLM) и MCP (живые сессии). Триггеры «/tg-connect», «/tg-login», «подключи телегу», «подключи телеграм на этой машине», «залогинь телегу», «телега отвалилась», «AuthKeyDuplicated», «перелогинь аккаунт <имя>», «настрой telethon и mcp», «connect telegram», «relogin telegram»"
version: 1.0.0
---

OBJECTIVE: сделать этот узел TG-готовым — обе рельсы живы, у каждой своя сессия, вердикт
подтверждён `/tg-check`. Всё, что можно, делаю сам: логины и авторизации мои по умолчанию
(Антон, 27.06.2026: «ВСЕГДА делай все авторизации максимально автономно»). Антона зову
только там, где физически нет пути.

## Закон (нарушать нельзя, остальное — детали)
1. **Каждая машина логинится САМА, один раз на аккаунт.** Один аккаунт держит сколько угодно
   устройств — это норма Telegram.
2. **⛔ НИКОГДА не копировать и не синкать session-строку между машинами.** Строка = паспорт
   машины, а не общий секрет. Одна строка на два IP → Telegram видит угон ключа →
   `AuthKeyDuplicated` → гасит ключ → падают ОБЕ машины.
3. **Сессия живёт машинно-локально, вне синка:** Windows `%LOCALAPPDATA%\claude-tgbus\session.env`,
   macOS `~/Library/Application Support/claude-tgbus/`, Linux `~/secrets/` (chmod 600).
4. **Два стека на узел — оба обязательны:** MCP для живых сессий, Telethon-рельса для роботов.
   Узел с одним стеком не считается подключённым.

Канон: `reglament-telegram-login-svoya-sessiya-na-mashinu-master` (входная точка) +
`reglament-telegram-dva-steka-telethon-i-mcp` + `reglament-shina-telegram-bez-mcp-i-svoya-sessiya-na-mashinu`.

## Какая дверь живая (реколл 05.08.2026 — не гадать заново)
Скриптов логина в двух домах **14**, живых из них три. Остальное — исторические половинки.

| движок | роль | когда звать |
|---|---|---|
| **`tg_session_init.py`** | ⭐ ГЛАВНЫЙ: даёт машине свою строку на выбранный аккаунт, сам берёт код и 2FA, пишет в нужный дом, бэкапит `.env` перед правкой | всегда, это и есть подключение |
| **`tg_authcheck.py`** | истина о МОЕЙ сессии (`current=True` + свежая `date_active`), под общим локом | до и после |
| **`tg_channels_check.py`** | матрица обеих рельс на машине, 0 токенов | до и после |
| `tg_init_step1_request.py` + `tg_init_step2_signin.py` | ручная двухходовка, когда код приходится вводить с рук | только если главный не смог достать код |
| `tg_init_step2_mcp.py` | отдельный вход для MCP на Маяке | Linux-узел |
| `_imports/dialogs/tg_login_*.py` (4 шт) | ИЮНЬСКАЯ ветка под выделенную read-сессию для индекса чатов | не трогать для подключения |

## Ход работы

**Шаг 0. Диагноз (0 токенов, ничего не меняет).**
```bash
python "$USERPROFILE\.claude\scripts\tg_authcheck.py"
python "$USERPROFILE\.claude\scripts\tg_channels_check.py"
```
Читай ДАННЫЕ сессии, а не догадки: ⛔ не судить о телеге по `_heartbeat-*.txt`, по синканной
`.env` или по `sender_id` (все машины ходят под одним аккаунтом — по нему их не различить).
Свежий `AuthKeyDuplicated` в `mcp_errors.log` = кто-то поделился строкой, это корень, а не симптом.

**Шаг 1. Рельса Telethon (аккаунт REFRESH = @[рабочий аккаунт]).** Сперва вхолостую, потом боевым:
```bash
python "$USERPROFILE\.claude\scripts\tg_session_init.py" --account REFRESH --dry
python "$USERPROFILE\.claude\scripts\tg_session_init.py" --account REFRESH
```
Строка ляжет в machine-local `session.env`. Движок держит общий лок `_refresh_[рабочий аккаунт].lock`
только для этого аккаунта — не запускать параллельно с роботами шины.

**Шаг 2. Аккаунты MCP.** Их на хабе четыре, у каждого свой ключ в `[путь владельца]`
(файл бэкапится перед каждой правкой):
```bash
python "$USERPROFILE\.claude\scripts\tg_session_init.py" --account [рабочий аккаунт]
python "$USERPROFILE\.claude\scripts\tg_session_init.py" --account [рабочий аккаунт]
python "$USERPROFILE\.claude\scripts\tg_session_init.py" --account [рабочий аккаунт]_MCP
python "$USERPROFILE\.claude\scripts\tg_session_init.py" --account TONYDZI
```
⚠️ `[рабочий аккаунт]_MCP` ≠ `REFRESH`: это один аккаунт @[рабочий аккаунт], но ДВА разных auth-key — по одному на
рельсу. Так и должно быть; попытка обслужить обе рельсы одной строкой и есть тот самый
`AuthKeyDuplicated`.

**Шаг 3. Подними потребителя.** MCP на хабе — не stdio-копия в каждой сессии, а ОДИН
SSE-демон (`.claude.json` → `"telegram": {"type":"sse","url":"http://127.0.0.1:8765/sse"}`),
его держит сторож «MCP Daemons Watchdog». После смены строк демон надо перезапустить, иначе
он до конца жизни ходит со старым ключом. Живые инструменты появляются в сессии только после
её перезапуска — это не поломка.

**Шаг 4. Вердикт чужим прибором.** Свой же скрипт доказательством не считается:
```bash
python "$USERPROFILE\.claude\scripts\tg_channels_check.py"
```
плюс живой вызов `mcp__telegram__list_accounts` прямо в сессии — скриптом MCP честно не
проверить, это stdio/SSE-сервер харнесса. Полный протокол = скилл `/tg-check`.

## Курица и яйцо (главная граница)
Код входа я забираю САМ из служебного чата 777000 — но **через уже живую сессию этого
аккаунта**. Значит:
- аккаунт жив хоть где-то → делаю всё сам, Антона не трогаю;
- сессия мертва ВЕЗДЕ (первый вход на новой машине, снесли все устройства) → кода взять
  неоткуда. Тогда по лестнице: (1) попросить пир по шине забрать код своей живой сессией
  ([[peer-otp-relay]]); (2) только если и пиров нет — руки Антона, и тогда код передаётся
  через `TG_LOGIN_CODE`, а не вводится в чат.
- 2FA берётся из `secrets\telegram_2fa.env` сам, в лог не печатается.

### ⭐ QR-АКЦЕПТ ДОНОРОМ — когда код НЕ приходит в 777000 (добавлено 21.09.2026)
Ступень лестницы выше, а не замена ей: нужна, когда OTP идёт **SMS на телефон**, а не в служебный
чат — там `777000` не помогает. Именно на этом месте 14.09 родился ложный вывод «обхода нет, нужны
руки Антона»; он прожил один день.

Условие применимости: **аккаунт жив хоть на одном узле флота**. Тогда рук Антона не нужно вовсе —
донор подтверждает вход так же, как телефон подтверждает QR-код в приложении:
1. на безногом узле — `client.qr_login()`, берём `qr.token` (base64url); токен живёт **~50 сек**;
2. на узле-доноре — `AcceptLoginTokenRequest(raw_token)` его живой сессией ЭТОГО аккаунта;
3. `SessionPasswordNeededError` → `client.sign_in(password=...)` из `telegram_2fa.env` (штатный шаг, не сбой);
4. строка → в `.env` потребителя, дальше рестарт демона и проверка чужим прибором (см. «Ход работы»).

⚠️ Приёмник кладётся на донора **заранее** и зовётся прямым `ssh`: обёртка со scp+ssh не успевает
в окно токена (замер 15.09: доставка 38 с → `AuthTokenExpiredError`).
✅ Закон №2 тут не нарушается: узел получает СВОЙ auth key, строка донора никуда не едет. Донор
после выдачи остаётся authorized (проверено 15.09, перепроверено 21.09).

Разбор случая: память `fleet-shares-tg-access-via-qr` и `tg-archive-false-green-[рабочий аккаунт]` §опровержение.

## Границы и грабли
- ⛔ Не копировать строки между машинами — ни «временно», ни «чтобы быстрее». Это не удобство,
  это авария на обе машины.
- ⛔ Не поднимать второй Telethon-клиент как health-check: два клиента на одной сессии = разлогин.
  Поэтому диагноз ходит под локом, а не «просто подключиться и посмотреть».
- Синканный `[путь владельца]` с `*_SESSION` — **известная утечка**, её
  доводят до per-machine-split. Новые строки туда НЕ писать.
- Частые перелогины с прыжками по IP/странам могут вызвать SMS-переверификацию. Логинимся
  один раз на машину и не дёргаем.
- Секреты не уезжают в волт, в always-loaded и в исходящее: только `secrets\` и локальные `.env`.

Соседи: `/tg-check` (диагноз обеих рельс) · `/telegram-howto` (что уметь после подключения) ·
`/whatsapp-pair` (та же задача для WhatsApp) · `/raise-sync` (если лежит синк, а не телега).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
