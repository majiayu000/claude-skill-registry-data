---
name: alpha-credit
description: "- КРЕДИТ АВТОРУ ИДЕИ: совет из комментария (TG @ClawRus / @ClawInga, комменты под постами Антона в FB, треды и issue на… Триггеры: “/alpha-credit“, “/credit“, “кто нам это посоветовал“, “запиши совет“, “поблагодари советчиков“, “кому мы должны спасибо“, “кредит автору“, “чей это был совет“, “credit the author“"
version: 1.0.0
---

# /alpha-credit — совет человека доходит до кода и человек об этом узнаёт

## Закон

**Идея — тоже вклад.** Мы строим опенсорс: тот, кто отдал нам ход бесплатно, получает имя
в артефакте и публичное спасибо. Тишина в ответ на совет — антипаттерн (CLAUDE.md §1.5) и она же
убивает следующий совет: второй раз не пишут.

**Три источника** (голосовая 06.08): TG-чаты **@ClawRus** и **@ClawInga** · комментарии под
постами Антона в **Facebook** · **GitHub** (issue, треды, ревью).

## Цепочка из пяти звеньев

Рвётся любое — совет пропал. Реестр держит все пять на одной строке, `pending` показывает,
какое звено не закрыто.

| # | Звено | Команда | Что доказывает |
|---|---|---|---|
| 1 | поймали | `add --ref <ключ>` | совет не растворился в ленте |
| 2 | судили | `verdict --take/--pass/--watch --why` | мы его РАЗОБРАЛИ, а не кивнули |
| 3 | испытали | `trial --criterion --until` | «тестируем» — правда, а не вежливая фраза |
| 4 | сказали спасибо | `credit --post <url>` | человек УЗНАЛ |
| 5 | вписали имя | `stamp --where <файл\|репо>` | имя живёт столько, сколько код |

```
python ~/.claude/scripts/alpha_credit.py pending      # ← начинай отсюда, всегда
```

## Шаг 1 — поймать совет (фидеры)

Совет приходит не сам: его приносит один из трёх разборов. **Каждый обязан положить строку**,
иначе реестр остаётся пустым, а движок — мостом в чистое поле.

| откуда | чем разбираем | `--source` | `--ref` (дедуп, обязателен) |
|---|---|---|---|
| @ClawRus / @ClawInga | `/community-alpha`, `mine_channel.py` | `tg` | `tg:ClawRus:<msg_id>` |
| комменты FB | `/fb-watch`, `/fb-reply` | `fb` | `fb:<comment_id>` |
| GitHub | `/contrib-watch` | `gh` | `gh:<owner/repo>#<num>:<comment_id>` |

```
python ~/.claude/scripts/alpha_credit.py add --source tg \
  --author "Имя Фамилия" --handle [аккаунт] --url https://t.me/ClawRus/16237 \
  --advice "что именно посоветовал, одной фразой" --kind method \
  --ref tg:ClawRus:16237
```

⚠️ **`--ref` не опция.** Фидеры ходят по одним и тем же тредам многократно; без стабильного ключа
один совет размножается копиями и attribution ломается — у автора становится «пять советов»
вместо одного. Повторный `add` с тем же `ref` возвращает существующий id и НЕ пишет новую строку.

## Шаг 2 — согласие: кого вообще можно назвать

- `public` — совет дан **публично** и есть **ссылка** на публичный след → имя можно назвать.
- `private` — личка, закрытый клуб → **имя в публичный текст не идёт никогда**, спасибо личное,
  в артефакте формулировка «по совету участника закрытого чата».
- Нет `--url` → публичность не доказана → `private`. Сомнение → `private`.
- Человек попросил убрать имя: `revoke <id>` — необратимо, затем **пересобрать** CREDITS.md.

## Шаг 3 — судить и испытывать

Вердикт без `--why` не принимается: причина — такой же claim, как вывод.
Взяли → `--proof` (файл/коммит), иначе «применили» недоказано.

```
python ~/.claude/scripts/alpha_credit.py verdict <id> --take --why "..." --proof "путь/коммит"
python ~/.claude/scripts/alpha_credit.py trial   <id> --criterion "что считаем успехом" --until 2026-09-01
```

Слотов максимум **3** (зеркало `reglament-alfa-na-ispytatelnyy-srok-sloty-i-verdikt`, доска
`03-Insights/alpha-trials-board.md`). Критерий называется **заранее**. Срок пришёл →
`trial <id> --keep|--drop|--extend --why`, и **автору сообщается, чем кончилось** — это вторая
половина обещания «дадим знать».

## Шаг 4 — публичное спасибо

Заготовка текста: `alpha_credit.py digest --days 7` (только `public`, приватные — счётом и id).
Форма ответа автору — короткая, по делу, без лести:

> спасибо за наводку на X. взяли: <что именно сделали>. сейчас тестируем до <дата>,
> критерий — <критерий>. напишу, чем кончится.

Куда отвечаем: **в тот же тред**, где совет прозвучал (коммент под постом, тред issue,
сообщение в чате). Маршрут по каналу:
- GitHub — отвечаю **сам**, без «+» и без гейта [коллега] (CLAUDE.md §4.7).
- FB-комменты — `/fb-reply` (ответ на своём посте, гейт [коллега] на публичные посты не трогаем).
- TG — ответ в треде своим аккаунтом.

Отметить: `alpha_credit.py credit <id> --post <url ответа>`.

## Шаг 5 — имя в артефакт (главное, ради чего всё)

Публичное спасибо живёт день в ленте. **Имя в описании функции живёт столько, сколько живёт код.**

1. **В паспорте детали** (`~/.claude/scripts/_doc_<деталь>.md` или заголовок скилла) — строка:
   `Идея: <Имя> (<ссылка на совет>), <дата>.`
2. **В репозитории** — `CREDITS.md`, пересобирается из реестра:
   ```
   python ~/.claude/scripts/alpha_credit.py credits-md --out <путь к репо>/CREDITS.md
   ```
   Дверь узкая нарочно: туда попадает только `consent=public` **и** `verdict=take` **и** не
   отозванный. «Думаем» и «не взяли» в благодарности репозитория не идут, иначе файл за месяц
   станет свалкой.
3. Отметить: `alpha_credit.py stamp <id> --where "<путь или owner/repo>"`.

## Границы

- Робот НЕ публикует ответ автору сам: движок готовит текст, отправляет живая сессия по правилам
  своего канала.
- Цифры в благодарности — правда: не «ускорило в 10 раз», если не мерили.
- Приватный совет не становится публичным задним числом: храповик согласия в движке это запрещает.
- Реестр `credit_ledger.jsonl` append-only, руками не правится: правка = новая строка того же id.

## Проверка

`python ~/.claude/scripts/_test_alpha_credit.py` → exit 0. Паспорт: `~/.claude/scripts/_doc_alpha_credit.md`.

Канон: CLAUDE.md §1.5 (скромность это плохо), §4.7 (GitHub-коммуникация сам), §5.8 (тест+док+счётчик);
память [[credit-inspiration-sources]], [[alpha-trial-slots]], [[github-inbound-watch]];
Библия `reglament-vklady-dokumentiruem-gromko-vezde`, `reglament-publichnaya-pohvala-posle-razbora-chuzhogo-tula`;
задача `10-Tasks/task-2026-08-06-contributor-credit-engine.md`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
