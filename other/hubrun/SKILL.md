---
name: hubrun
description: "Прогнать PowerShell-скрипт или команду на удалённом узле флота (дефолт: хаб [машина флота]) и получить вывод назад ОДНОЙ командой. Trigger on «/hubrun», «прогони на хабе», «запусти на хабе скрипт», «выполни на хабе»"
version: 1.0.0
---

# /hubrun — запуск PowerShell на узле флота одной командой

## Когда
Нужно что-то выполнить/проверить на хабе (или другом ssh-узле Windows) и увидеть вывод здесь. Заменяет ручную связку «Write .ps1 → scp → ssh → scp назад».

## Как
Инлайн-команда (только простое, БЕЗ вложенных двойных кавычек — локальный PS 5.1 мнёт их при передаче в native-аргумент):
```bash
python ~/.claude/scripts/hubrun.py -c "Get-Date; $env:COMPUTERNAME"
```
Скрипт-файл (дефолт для всего нетривиального; писать payload в scratchpad):
```bash
python ~/.claude/scripts/hubrun.py <путь-к-локальному.ps1>
```
Опции: `--host <alias>` (дефолт hub; алиасы в ~/.ssh/config) · `--keep` (оставить out-файл на узле) · `--timeout <сек>` (дефолт 300).

⚠️ Грабли 10.09.2026: дефолт 300с рвёт ЛЮБОЙ прогон, который ходит в LLM (суточный оптимизатор канона, /tt чужого движка, ДР-рельсы) — вывод теряется, а работа на узле продолжается вслепую. Ходит в модель или в сеть → ставь `--timeout 900` СРАЗУ, не после обрыва.

## Контракт
- Первая строка вывода `### hubrun status=OK|ERR`; exit 0 только при OK.
- Payload исполняется в том же PS-процессе → НЕ звать `exit`; финиш сигналь `Write-Output`-строкой.
- Кириллица/тире в payload и в выводе доезжают целыми (BOM + файловый out).
- За собой чистит и локально (temp), и на узле; во время прогона узел видит 2 своих файла `_hubrun_<id>_*` — это норма, не мусор.
- GUI на узле из ssh не поднять (сессия 0) — для этого Interactive-задача планировщика, см. память hub-claude-fixers-disabled-and-msix-repair.

## Тест
`python ~/.claude/scripts/_test_hubrun.py` (оффлайн 15 кейсов) · `--live` = смок на хаб. Счётчик: `~/.claude/usage_counters/hubrun.jsonl`.

## ⚠️ `-c` и кириллица (замер 10.09.2026, раскатка fireat-door)

Защита от OEM-мятой кириллицы работает в режиме ФАЙЛА (`hubrun.py script.ps1`): вывод забирается UTF-8 out-файлом. В инлайн-режиме `-c "..."` этого пути нет — русский вывод удалённой команды вернулся кашей вида `╨Т╨Х╨а╨Ф╨Ш╨Ъ╨в` и читался только по латинице и цифрам (md5, exit-коды).

Практика: `-c` бери, когда ответ ЛАТИНСКИЙ (хэши, коды выхода, пути) — это дёшево и надёжно. Нужен русский вывод — клади команду в .ps1 и гони файлом.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
