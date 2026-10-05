---
name: spawn-bridge
description: "⭐ ПРАВИЛО (anton 23.09 голосом): «подними сессию/декомпозируй» адресовано ТЕБЕ = поднимай У СЕБЯ, своими средствами (Cursor → Task-tool/background agents, Codex → свои сессии, Claude → планировщик); нести задачу в другую LLM = ересь. Мост spawn_queue → Claude-планировщик — ТОЛЬКО когда нужна именно видимая scheduled-задача приложения. Триггеры: «подними сессии», «декомпозируй на сессии», lift-spawn."
---

# /spawn-bridge — «подними сессию» = подними У СЕБЯ

## ⭐ Правило №0 (anton 23.09.2026, голосом — supersedes первую версию этого скилла)
Дословно: «когда я прошу её запустить новую сессию — это я ЕЁ прошу запустить сессию,
а не чтобы она понесла в другую LLM». Действует на ЛЮБУЮ LLM:
- **Cursor**: декомпозиция → свои субагенты/сессии (его Task-tool из инвентаря T2,
  background agents) — 5-10 кусков решает У СЕБЯ. ⛔ Не шлёт LIFT-SPAWN в Claude
  по умолчанию.
- **Codex**: свои сессии — «у кодекса с этим проблем вообще нет» (anton).
- **Claude**: свой планировщик (/nsr).
Результаты — как обычно: файлы в worktree + конверты в чат пары.

## Мост в Claude — УЗКОЕ исключение, не дефолт
Мост ниже (spawn_queue → планировщик приложения) применяется ТОЛЬКО когда задаче
нужна именно **видимая scheduled-задача Claude Code Desktop**: отложенный fireAt/cron,
сессия в списке приложения Антона, коннекторы Claude (MCP Gmail/Calendar/TG-рельса).
Обычная декомпозиция «сделай N кусков параллельно» мостом НЕ является.

## Боль, из которой родился мост (замер 23.09.2026)
Cursor и Codex не могут звать `create_scheduled_task` — это MCP-коннектор приложения
Claude Code Desktop. Cursor писал в чат «Anton asked where the repair session is»
(msg 1906890) и ждал. Для СВОИХ задач это решается правилом №0; для задач, которым
нужен планировщик приложения, — мостом ниже: **очередь сидов — CLI-скрипт**,
а поднимает тот, у кого планировщик есть.

## Шаги (для ЛЮБОГО агента; шаг 3 — нужен Claude)

**1. Декомпозируй** задачу на самодостаточные куски (потолок ~3 пишущих + 2 ревью
одновременно — CLAUDE.md §9.2; больше сидов класть МОЖНО, подниматься будут лесенкой).
Каждый сид = полный текст по шаблону: Outcome · Контекст · Scope · Deliverable · DoD ·
не-цели · эскалация · граница Tier-2. Плюс ОДИН указатель на блок STOP-DUP:
`$OBSIDIAN_VAULT/08-Templates/seed-stop-dup-block.md` — вставить содержимое целиком.
Первой строкой сида ОБЯЗАТЕЛЬНО:
`ПЕРВЫМ ДЕЛОМ переименуй эту сессию: вызови mcp__ccd_session_mgmt__set_session_title с title "<AUTO-имя>".`

**2. Положи каждый сид в очередь** (чистый CLI, работает у всех):
```bash
python ~/.claude/scripts/spawn_queue.py add \
  --task-id "auto-hub-<ггммдд>-<суть>" \
  --description "AUTO-hub-<ггммдд>-<суть>: <одна строка>" \
  --prompt-file <файл-с-сидом> \
  --cwd <рабочая-папка>
```
Имя строго `auto-<узел>-<ггммдд>-<суть>` строчными — иначе гейт отобьёт при подъёме.

**3. Один конверт в чат пары** (-[id]), НЕ по конверту на сид:
`[<Ты>→Claude][lift-spawn][REQUEST] corr_id=<тема>; next_action=LIFT-SPAWN.
В очереди N сидов: <список task-id>. Подними видимыми сессиями.`
Подъём — **нужен Claude**: только его харнесс зовёт `create/update_scheduled_task`.
Живая Claude-сессия поднимает сразу; если живых нет — SessionStart-хук любой
следующей сессии печатает очередь, и она поднимет. Ответ тебе — task-id поднятых.

**4. Не жди молча.** Подъём не случился за разумный срок → это мяч Claude/секретаря
пакта (прогоны 08:10/20:10), один nudge по правилам COLLAB-COST-1, поллинга нет.

## Что НЕ делать
- ⛔ `claude -p` / фоновые процессы «в чёрную» — невидимы Антону, гейт отбивает.
- ⛔ Конверт на каждый сид — спам; один пакет = один список.
- ⛔ Сид без Tier-2-границы и STOP-DUP-блока.
- ⚠️ Очередь длинная (сотни сидов) — твои НЕ прыгают вперёд; срочное = скажи срочность
  в конверте с причиной, решит поднимающий.

## Проверка
`python ~/.claude/scripts/spawn_queue.py list | grep <твой-task-id>` — сид в очереди.
После подъёма: сессия видна в списке приложения под своим AUTO-именем.

## Потребители (§9.3-тер)
Cursor (заказ Антона 23.09 05:14 «научи его, чтобы не тупил»; оповещён конвертом в
чат -[id] тем же заходом) · Codex (та же дыра, оповестить по возврату 27.09) ·
живой пример: сид auto-hub-260923-recall-anton-filter поднят Claude по REQUEST 1906890.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
