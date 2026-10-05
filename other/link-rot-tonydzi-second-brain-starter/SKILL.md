---
name: link-rot
description: "Sweep every external pointer to you (profiles, READMEs, bios, link pages) after a rename of a repo, org, domain, handle or account, and fix the dead ones. Use right after any public rename and once a quarter as hygiene. Triggers: /link-rot, /lr, check links, broken profile links, after the rename, link rot."
license: MIT
version: 1.1.0
---

Родился 09.09.2026 из сессии `AUTO-hp17-260908-link-rot-sweep`: переименование
`Palo-Alto-AI-Research-Lab → tonydzi` (04.08) перенесло репо и сайт, но **GitHub Pages и URL
профиля не редиректят** — и шесть внешних витрин месяц вели в 404, потому что никто их не
прочесал. `prior_art.py` назвал это **3-м датированным случаем** семьи «переименование оставило
мёртвый указатель в слое, который никто не сторожит» (слаг класса: `rename-leaves-external-pointers-dead`) → класс системный, отсюда этот скилл. Этот скилл — ЕДИНСТВЕННАЯ исполняющая дверь обоих правил: `rename-leaves-external-pointers-dead` (Шаги 1-3, 5) и `oauth-only-login-is-a-single-point-of-failure` (Шаг 4).

Единственный источник набора ссылок и матрицы площадок — волт
`04-Projects/page-distribution-registry.md`. Здесь только процедура, дублировать список ⛔.

## Шаг 1 — ЗАМЕР ПЕРВЫМ, суждение вторым (0 токенов)
```
python ~/.claude/scripts/link_rot_scan.py
```
`exit 0` = чисто, дальше не работаем · `exit 2` = поимённо мёртвые ссылки и грязные витрины ·
`exit 4` = прибор не доказал себя на контрольном примере и **молчит о данных** (не верь пустому
выводу, чини прибор). Цели правятся в `~/.claude/link_rot_targets.json` — при новом
переименовании ДОБАВЬ старый адрес в `dead_markers` тем же заходом, иначе сторож его не увидит.
Сам сторож краснеет по требованию: `python ~/.claude/scripts/_test_link_rot_scan.py` (3/3).


⭐ **Оплачено догоном 09.09:** «0 находок» — тоже claim. Прибор видит РОВНО те витрины, что лежат
в `surfaces`, а Scholar и Academia там не лежали — сторож печатал зелёное, пока две витрины
публично несли мёртвый адрес. Правило: витрина из матрицы волта обязана быть в `surfaces`, либо
рядом стоит причина, почему её нельзя прочитать без логина. И **403/429 — это лимитер, а не
стена**: Academia отдаёт 200 на первые запросы и 403 на следующие, поэтому `fetch` ретраит
(0/5/15/30с); первый 403, принятый за «не читается», спрятал 7 вхождений мёртвого адреса.

## Шаг 2 — где смотреть, если витрину не прочитать без логина
Прибор видит только публично читаемое. Закрытое проверяется руками по матрице волта.
Порядок обхода — **от дешёвого входа к дорогому**, это экономит час:
1. **Есть API с токеном в сторе → идём API, а не браузером.** X правится
   `api.x.com/1.1/account/update_profile` по `secrets/x_api.env` (Read/Write) за один вызов —
   быстрее и надёжнее кликов, и работает, даже когда в Chrome аккаунт разлогинен.
2. **Есть СВОЙ пароль в сторе → форма сайта.** ORCID и Wellfound так и открылись.
3. **Только «вход через Google» → это единственная точка отказа**, см. Шаг 4.


⭐ **Перед словами «аккаунта нет в браузере» (оплачено 09.09):** сперва выясни, в КАКОМ профиле
Chrome сидит MCP — `navigate myaccount.google.com` + `get_page_text` печатает живой email. Дальше
читай список аккаунтов профилей с диска, а не гадай перебором `authuser`:
`%LOCALAPPDATA%\Google\Chrome\User Data\<Profile>\Preferences` → ключ `account_info`
(файл с BOM, открывать `encoding='utf-8-sig'`). Номер `authuser=N` — это индекс в ЭТОМ списке, он
плавает от профиля к профилю: в одном профиле было 3 аккаунта, в соседнем 9. Перебор «0-5» в
профиле с тремя аккаунтами ничего не доказывает. И проверь `list_connected_browsers` — подключённых
Chrome может быть несколько, а нужный профиль может быть вообще не спарен (спаривание = клик человека).

## Шаг 3 — правим URL, НЕ переписываем тексты
Меняется адрес, а не формулировки Антона. ⛔ Не «улучшать» bio по дороге (§9.7).
Смотреть надо **три слоя, а не один** — в сессии 09.09 два из трёх нашлись только потому, что
искали не только в поле «website»:
- поле-ссылка профиля (website / homepage / GitHub);
- **URL внутри текста bio** (ORCID biography и bio X оба несли мёртвый адрес);
- **URL внутри длинных полей** (Wellfound Achievements).

⚠️ **Грабля Linktree:** смена URL кнопки МОЛЧА перезаписывает её ЗАГОЛОВОК автометаданными новой
ссылки («👉 START HERE — one page of proof» стал «Anton Dziatkovskii — developer activation…»).
Заголовок возвращать вручную и закрывать **Enter**; **Escape откатывает правку целиком**.
Проверять только перезагрузкой админки — в живом DOM правка выглядит применённой, хотя не сохранена.


⭐ **СЕМЬЯ ОБЪЕКТОВ, а не один объект (оплачено 09.09, журнал `fix-applied-to-one-sibling-object`):**
починив указатель, перечисли ВСЕ объекты, где он стоит, и пройди по каждому. 14.07 забаненный
LinkedIn убрали из Homepage Scholar-профиля `b8gKHiMAAAAJ` — и не заметили, что у Антона ВТОРОЙ
Scholar-профиль `wZ7qvJEAAAAJ`, где тот же мёртвый указатель прожил ещё 8 недель. Тест одной фразой:
«у этой витрины есть близнец под другим аккаунтом?»

## Шаг 4 — вход упёрся в Google-челлендж
`Continue with Google` может потребовать passkey/телефон, которых у робота нет. Порядок обхода:
1. поискать СВОЙ пароль площадки в `secrets/phd_accounts.env` и `secrets/chrome-passwords.csv`;
2. нет пароля, но письма ящика читаются коннектором (`a`/`a2`/`bb`) → **password reset**, ссылку
   забрать `python "$USERPROFILE/!CLAUDE-HP17 May26/gmail/gmail_check.py" search "<площадка>" --label bb`,
   новый пароль **сразу** в `phd_accounts.env` (§3.4);
3. ящик недоступен (например `au[id]@gmail.com`) → это **истинный блок**: карточка
   `state: blocked`, причина словами, остальные площадки НЕ ждут заблокированную.

⭐ **Правило, оплаченное этой сессией:** у каждой публичной витрины должен быть СВОЙ пароль в
сторе, а не только «вход через Google» — OAuth-only вход это единая точка отказа
(класс `oauth-only-login-is-a-single-point-of-failure`, журнал 09.09). Заводя новую витрину,
ставь ей пароль сразу.

## Шаг 5 — доказательство, иначе не сделано
На каждую площадку — машинная улика в том же заходе, «сохранил» уликой НЕ является:
curl публичной страницы с `grep -c <старый адрес>` = 0 · публичный API · **перечитанная после
перезагрузки** форма. Затем строки матрицы в волте (статус, дата, чем доказано) и вердикт
🟢/🔴 по каждой. Закрытая площадка без улики = 🔴, а не ✅.

## Шаг 6 — вердикт о скилле (§9.3-бис)
Прогнал скилл — одной строкой: `🔧 обновляю` (что споткнулось) · `📝 обновлю не сейчас` (куда легла
строка) · `✅ не надо` (почему именно). Пустое «не надо» вердиктом не является.



<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
