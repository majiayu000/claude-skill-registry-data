---
name: ledger
description: "«Что было в тот день» — мгновенный ответ из дневного леджера, который роботы собирают каждую ночь из бесплатных следов… Триггеры: “/ledger“, “/день“, “что было вчера“, “что мы делали 3 августа“, “что делали на той неделе“, “чем занимались в понедельник“, “покажи день“, “what did we do yesterday“, “итоги дня“. 0 токенов LLM на выборку: скрипт печатает готовую выжимку"
version: 1.0.0
---

# /ledger — «что было в тот день», за 0 токенов

Ночная рутина `day-ledger-nightly` каждую ночь склеивает из семи источников страницу
«что реально было сделано» и кладёт в `$OBSIDIAN_VAULT\01-Conversations\Claude\DayLedgers\`.
Этот скилл — дверь к ней. **Не пересобирай день ради ответа**: сборка идёт ночью, чтение
обязано быть мгновенным.

## Шаг 1 — выжимка (дефолт)

```bash
python "$IMPORTS_ROOT\day_ledger.py" --recall
```

Печатает вчерашний день в 6-8 строк: шапка со счётчиками · полнота дня · темы живых
сессий (одинаковые роботные схлопнуты в `×N`) · решения дня · путь к полному файлу.

Нужна неделя — числом дней: `--recall 7`.

## Шаг 2 — конкретный день

Дата известна → читай файл прямо, он уже собран:
`$OBSIDIAN_VAULT\01-Conversations\Claude\DayLedgers\day-ledger-YYYY-MM-DD.md`

Файла нет (день старше окна пересборки) → собери ровно его, это дёшево:

```bash
python "$IMPORTS_ROOT\day_ledger.py" 2026-07-15
```

## Шаг 3 — глазами (Антону)

```bash
python "$IMPORTS_ROOT\day_ledger.py" --html
```

→ `$OBSIDIAN_VAULT\_Dashboards\Day-Ledger.html`, последние 14 дней плиткой. Отдавай
файл через SendUserFile + абсолютным путём текстом ([[no-clickable-file-links-for-anton]]).

## Шаг 4 — семантический поиск по дням

Леджеры помечены `layer: essence`, то есть лежат в RAG-индексе и всплывают в
vault-recall сами. Прямой поиск, когда дата неизвестна:

```bash
python "$IMPORTS_ROOT\brain_ask.py" "когда мы чинили счётчик скиллов"
```

## Границы

- **Читает, не судит.** Леджер фиксирует следы, а не пользу: 417 роботных сессий за день
  не значат 417 полезных дел. Не выдавай счётчики за метрику продуктивности.
- **Полнота дня — это диагноз ИСТОЧНИКАМ, а не дню.** 🔴 худой в будний день = молча умер
  сборщик (git, реестр, синк с пира), а не «мы ничего не делали».
- **Провизорный день** (моложе 2 суток) ещё пересоберётся: поздние коммиты и следы с пиров
  доезжают по синку.
- Каждое обращение считается: `python ~/.claude/scripts/_shared/skill_usage_log.py --report --kind part`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
