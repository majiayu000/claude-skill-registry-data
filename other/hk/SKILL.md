---
name: hk
description: "«Что уже сделали роботы сегодня» — экран состояния обслуживания ПЕРЕД тем, как чинить руками. Триггеры: “/hk“, “/housekeeping“, “/уборка“, “что сегодня уже сделано“, “надо ли гонять бэкап“, “почему заблокировали команду“, “покажи квоты“, “что протухло“, “housekeeping status“"
version: 1.0.0
---

# /hk — housekeeping: что уже сделано, чего не надо делать руками

Приказ Антона 04.08.2026: обслуживающее гоняем **один раз в сутки**, а не в каждой из ~50 сессий.
Этот скилл — окно в состояние уборки, чтобы не начинать её заново.

## Шаг 1 — квоты суток (0 токенов)

```
python ~/.claude/scripts/maintenance_gate.py --report
```

Читаем: какие активности уже израсходовали свой 1 раз, сколько заходов гейт заблокировал.
Пусто и сегодня, и вчера → проверь, что гейт вообще жив: `python ~/.claude/scripts/maintenance_gate.py --selftest` (ждём `selftest: OK`). Тишина сторожа ≠ порядок ([[watchdog-must-verify-the-item]]).

## Шаг 2 — свежесть ВЫХОДОВ (не факта запуска)

```
python ~/.claude/scripts/_shared/output_freshness.py
```

Смотрим на возраст артефактов, а не на «задача Ready». `exit 1` = сторож нашёл протухшее и сам отчитался, это **жёлтое**, не падение. По каждому STALE у него в выводе уже написано лечение — читаем его, а не выдумываем своё.

## Шаг 2.5 — свежие списания: кого выключили и не вернули

```
python ~/.claude/scripts/disabled_task_guard.py --dry-run
```

Дверь правила **[[mass-disable-needs-return-date]]**: гасим класс роботов оптом — у каждого выключенного обязана быть **дата возврата** и пометка **виновен / выключен заодно**.

Класс находки **«СВЕЖЕЕ СПИСАНИЕ»** поднимает всё, что выключили за последние 3 суток. Это окно, пока человек ещё помнит контекст приказа: дальше заглушка молчит навсегда, и невиновный остаётся выключенным. По каждому имени даём один из двух ответов, третьего нет:

- **виновна** → допиши в вердикт реестра, ЧЕМ именно виновна;
- **выключена заодно** → `Enable-ScheduledTask` + строка «✅ ВЕРНУЛ <дата>» в `00-System\Decommissioned-Tasks.md`.

Молчание — не ответ: 31.08 общим приказом погасили 12 роботов, виновен был один, а жнеца сессий выключили заодно. Трое суток тишины стоили 138 зависших процессов и ~5.5 ядра вхолостую. Именно поэтому сторож получил рот 03.09.

## Шаг 3 — карта архитектуры: читать, не сканировать

Ночная карта строится задачей **System Architect Nightly** (`system.db` → `_Dashboards\System-Health.html` + MOC `00-System`).

- Нужно понять, что от чего зависит → `/arch`, `/arch broken` — **чтение готовой карты**.
- `/arch scan` (пересборка) — только если ты сам менял общую инфру в этой сессии, и не чаще раза в сутки.

Карта старше суток → это поломка робота, а не повод сканировать руками: проверь задачу в Планировщике и скажи об этом в отчёте.

## Шаг 3.5 — credential-рельса роботов (дверь правила о переносимом токене)

```
python3 ~/.claude/scripts/claude_token_sync.py --status
```

От долгоживущего `CLAUDE_CODE_OAUTH_TOKEN` зависят ВСЕ headless-рутины узла; протухнет — они
падают скопом с exit=126 и молча (замер 05.08: одиннадцать рутин лежали сутки).

Два правила чтения этого экрана, оба оплачены:

- **`claude auth status` тут не судья.** Он читает файл интерактивной сессии, роботы ходят
  токеном из store. `loggedIn:false` при живом ВЫХОДЕ = норма, не беда. Судим строкой `ВЫХОД:`.
- **Токен переносим между машинами** (замер 19.08: токен [машина флота] отработал на хабе). Нет токена →
  не зови руки Антона, а попроси узел-донор `claude_token_sync.py --push`. `setup-token` руками
  нужен только когда живого токена нет НИГДЕ — раз в ~год, на ОДНОЙ любой машине.

Канон: [[claude-oauth-token-is-portable-across-fleet]], [[always-red-watchdog-teaches-ignoring-red]].

## Шаг 4 — вердикт

Дай Антону короткий список из трёх корзин:

- 🔴 **нужны руки сейчас** — сломано и ждать до ночи нельзя (синк лёг, данные теряются, гейт мёртв);
- 🟡 **подождёт до ночного робота** — протухший выход, у которого задача включена и SWA=True: ночью догонит само;
- ✅ **сегодня уже сделано** — не трогаем.

Правило вердикта: пока не назвал, ЧЕЙ робот это делает и КОГДА, в 🟡 класть нельзя — иначе это «авось само».

## Границы

- Скилл **ничего не запускает** сам. Хочешь прогнать вне очереди — это осознанный `--force` + строка Антону зачем.
- Диагностику (статус Syncthing, MCP-демоны, логи) квота не трогает: читать можно всегда.
- Не путать с `/arch` (карта системы), `/tt` (проверка того, что сам собрал) и `/retro` (итоги сессии).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
