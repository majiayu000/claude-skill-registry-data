---
name: engineer-pool
description: "Наполнение пула ИНЖЕНЕРОВ-ТЕСТЕРОВ под миссию №2 из живых issue вендорских и агентных репо (не из крипто-базы leads.db). Триггеры: «/engineer-pool», «/ep», «где брать инженеров», «пул инженеров», «кому давать демо», «инженеров в выборке ноль», «наполни пул тестеров», «engineer pool», а также САМ, когда отчёт очереди touchbase печатает «инженеров из LLM-лабораторий в выборке: 0»"
version: 1.0.0
---

# /engineer-pool — инженеров берём не из крипто-базы

> 🧒 В конце отчёта Антону — блок «Простыми словами» ([[eli5-always]]).

## Закон (почему скилл существует)

25.07.2026 замер показал: в `leads.db` 14 тысяч контактов, но это сеть **фаундеров и инвесторов крипто-контура** — инженеров единицы. Вывод тогда же лёг в память [[leads-db-wrong-pool-for-engineer-testers]] с готовым рецептом: «для инженер-тестеров брать другой пул — issue-matching в вендорских cookbook-репо, r/ClaudeAI, участники @ClawEng, авторы issue в смежных агентных репо».

**Два месяца рецепт лежал без вызывающего** — классический §8.6 «правило без двери принято, но НЕ РАБОТАЕТ». 22.09.2026 замер повторился на свежих данных: 14 146 лидов, Anthropic = 0, OpenAI = 0, DeepMind = 0, HuggingFace = 0, Cursor = 0, LangChain = 0. Десять «инженеров» в очереди тачбейза оказались крипто-разработчиками Platinum / MicroMoney / BTCNEXT.

Решение Антона 22.09: **крипто-базе писать продолжаем, это не провал** — но пул миссии №2 наполняется отсюда, а не оттуда.

## Граница с соседями (чтобы не плодить двойников)

| Скилл | Про что | Вход → выход |
|---|---|---|
| `/issue-match` | стучаться в ЭТОТ репозиторий или мимо | репо → замер очереди, живая дверь |
| `/consumer-hunt` | у НАШЕГО артефакта должен быть список адресов | артефакт → адреса и каталоги |
| **`/engineer-pool`** | **у миссии №2 должен быть список ЛЮДЕЙ** | **домен → инженеры с живой дверью** |

Первые два — про артефакт, этот — про человека. Пересечение одно: перед касанием кандидата очередь его репо всё равно меряет `/issue-match` (холодный PR в глухую очередь = шум, [[cold-pr-into-silent-queue]]).

## Прогон

**Шаг 0 — RECALL.** `python ~/.claude/scripts/engineer_pool.py report` — кто уже в пуле; в память ходи за [[leads-db-wrong-pool-for-engineer-testers]] и [[engineer-acquisition-enrichment-not-scraping]].

**Шаг 1 — сбор.** `python ~/.claude/scripts/engineer_pool.py harvest`
0 LLM, работает через `gh`. Берёт авторов ЖИВЫХ открытых issue (обновлены за окно `fresh_days`) в репо из `~/.claude/engineer_pool_sources.json`, отсеивает ботов, дедуплицирует между прогонами, дописывает в `~/.claude/state/engineer_pool.jsonl`.
⚠️ Строку «СЛЕПЫЕ рельсы» читай буквально: `gh` не ответил — это «не смотрели», а не «людей нет» ([[check-all-places-not-one]]).

**Шаг 2 — три рельсы, которые скрипт НЕ закрывает** (руками, по рецепту 25.07):
- участники **@ClawEng** — свои, самые тёплые, идут первыми;
- **r/ClaudeAI** — только после прогрева, холодный заход туда сгорает;
- **авторы issue в смежных агентных репо**, которых нет в списке источников — нашёл новый репозиторий, впиши его в конфиг в том же заходе, иначе следующая смена его не увидит.

**Шаг 3 — касание.** Не веером. Один человек = его тема = его issue. Порядок: `/issue-match` по его репо → ответ по существу его вопроса → артефакт, если он вправду отвечает на вопрос. Подпись обязательна ([[outbound-signature]]), отправка через общий журнал аутрича.

**Шаг 4 — вердикт вслух**: «в пул добавлено N · слепых рельс M · касаний сегодня K». Ноль — тоже вердикт, но с названной причиной.

## Потребитель (§9.3-тер)

Названный потребитель — рутина **`touchbase-daily-runner`**: её отчёт очереди печатает машинную строку «инженеров из LLM-лабораторий в выборке: N» и при нуле указывает сюда. Оповещение стоит в её `SKILL.md` (шаг отчёта) и в шапке `touchbase.py`.

## Что НЕ делаем

⛔ Не скрапим и не собираем досье — берём публичную дверь (открытый issue) и приходим по делу ([[engineer-acquisition-enrichment-not-scraping]]).
⛔ Не шлём одинаковый текст пачке: «спам ≠ громкость» (CLAUDE.md §1.5).
⛔ Не выбрасываем кандидата за то, что он нашёлся и в `leads.db` — совпадение редкое и ценное.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
