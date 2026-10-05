---
name: deflate
description: "Cut background heat and noise on this machine: audit scheduled tasks by runs per hour, autostart entries, GPU holders, power plan and top CPU, then propose disable or stretch candidates, decide line by line with the operator and apply only approved lines. Triggers: /deflate, fan is loud, laptop runs hot, what can I turn off, machine slow from background load."
license: MIT
version: 1.0.0
---

# /deflate — меньше тепла и шума на этом узле, вместе с оператором

Движок: `python ~/.claude/scripts/node_deflate.py` (0 LLM, stdlib, win/mac/linux; `--selftest` есть). Суждение «нужно / не нужно» — у оператора, не у скрипта.

## Шаг 0 — RECALL
Память `laptop-fan-noise-root-cause` + `zbook-no-gpu-without-permission`; роль узла из `~/.claude/machine.env` (hub = роботы остаются, satellite = минимум фона, §7.1). Термо-история, если есть: `~/.claude/scripts/_power_thermal/*.csv`.

## Шаг 1 — Аудит (только чтение)
`python ~/.claude/scripts/node_deflate.py audit` → таблица: запусков/час, наши vs вендорские задачи, автозапуск, держатели GPU, режим питания, топ CPU. На HP-железе температуры и обороты вентиляторов читать HP-сенсором (`Get-CimInstance -Namespace root\HP\InstrumentedBIOS -ClassName HP_BIOSNumericSensor`), а НЕ nvidia-smi: он сам будит спящую карту.

## Шаг 2 — План
`python ~/.claude/scripts/node_deflate.py propose` → `~/.claude/_deflate/<HOST>-plan.json`, каждая строка `ok=false`. Правила движка: на сателлите наши сторожа чаще 60 мин → растянуть (Desktop-Watchdog 10, термо-логгер 15, Fleet Pulse 30); дубли хаба и мёртвые роботы → выключить; оверлей питания «Best performance» → Balanced; GPU=true на сателлите → заметка. Вендорские задачи скрипт НИКОГДА не предлагает.

## Шаг 2-бис — ⛔ ДВЕ ЦИФРЫ ПЕРЕД ЛЮБОЙ РАСТЯЖКОЙ (замер 22.09.2026)
Строка плана, растягивающая интервал СТОРОЖА, не показывается оператору, пока не названы **две цифры**: (1) **фора**, которую сторож даёт основному звену, и (2) **срок, за который потребитель заметит пропажу**. Новый интервал обязан быть меньше обеих; больше — строка из плана выбрасывается, а не «обсуждается». Не знаешь цифр — не трогаешь интервал.

⚠️ Чем оплачено: дефляция 15.09 («все рутины ×2») растянула `Claude Voice Backstop` 4ч → 8ч. Это 0-токенный детерминированный сторож с форой боту 10 минут, подпадавший под собственное исключение той же дефляции — его срезали по имени («ещё одна запланированная задача»), а не по роли. 22.09 бот-расшифровщик пропустил голосовую Антона, страховка спала, `state.json` писал `status=OK`, и пропажу за 14 минут заметил ЧЕЛОВЕК. **Нулевой расход LLM = кандидат в исключения по умолчанию**, а не в первые жертвы.

Канон: память `deflate-must-not-stretch-safety-nets`, CLAUDE.md §4.5-тер. Живой образец самопроверки — `own_tact_min`/`tact_verdict` в `[путь владельца]`: сторож сам сверяет свой такт с форой и валит статус в `TACT_TOO_SLOW`.

## Шаг 3 — Решение с оператором (обязательный диалог, §2.2 до→после)
Показать план таблицей: что · зачем стоит сейчас · сколько сэкономит · что сломается · откат. Оператор отвечает построчно («+ 0 2 5», «всё кроме 3»). Только после этого выставить `ok=true` выбранным строкам. ⛔ Не выключать молча: «вдруг случайно оказалось нужно» (Антон 08.09). Tier-2 (безопасность: Defender, VBS, BitLocker), деинсталляции и чужие вендорские сервисы → только клик-путь оператору, скрипт их не трогает.

## Шаг 4 — Применить + доказать
`python ~/.claude/scripts/node_deflate.py apply ~/.claude/_deflate/<HOST>-plan.json` → применяет только `ok=true`, пишет строку на каждое изменение в `~/.claude/change_ledger/<HOST>.jsonl`. Windows S4U-задачи требуют повышения: скрипт печатает точную команду для одного UAC. После: снова `audit` и сравнить запусков/час + температуры до→после. Результат = строка в доклад узла (03) и в память узла.

## Что мерить, чтобы не соврать
До и после: запусков/час · CPU °C и обороты · dGPU °C без опроса nvidia-smi (карта спит = температура ≈ комнатная на EC-сенсоре). Замер ZBOOKG8 08.09: 136 → 62 → ~45 запусков/час, CPU 92 → 70 °C, dGPU 77 → 25 °C.



<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
