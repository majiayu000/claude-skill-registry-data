---
name: sync-sessions
description: "Сделать сессии Claude Code на ЭТОМ компьютере видимыми под любым аккаунтом, как локальные треды Codex. Триггеры: /sync-sessions, «синхронизируй сессии», «запейни сессии», «после смены аккаунта пропали чаты», «не вижу старые сессии»."
version: 1.3.0
---

# /sync-sessions — сессии Claude не пропадают при смене аккаунта

Приложение Claude показывает список сессий только из папки текущего аккаунта.
Тексты диалогов при этом остаются на диске в `~/.claude/projects`.

## Что сделать

```
python [путь владельца]
```

Скрипт дописывает недостающие карточки во все аккаунты, которые уже хоть раз
входили на этом компьютере. Ничего не удаляет и не перезаписывает.
Повторный запуск, когда всё уже совпадает, ничего не копирует.

На этой машине то же самое делает скрытый процесс **4 раза в сутки**
(интервал 21600с; anton 24.09.2026 голосом: «пять минут реально слишком часто...
два-три-четыре раза в сутки, но не больше»). Он стартует при входе в Windows из
`Start Menu\Programs\Startup\Claude-Sessions-Across-Accounts.vbs`.
Планировщик задачу создать не смог (Access denied), поэтому используется автозапуск.

## Установка на узле флота (Windows и Mac)

```
python [путь владельца]
```

(путь = `<волт узла>\..\_imports\claude_sessions\`; папка синкается Syncthing).
Windows → Startup VBS + немедленный старт; Mac → LaunchAgent каждые 21600с;
Linux/headless ([машина флота]) → отказ by design, там нет десктоп-приложения.
`--status` показывает, стоит ли лаунчер и бежит ли сторож.

⚠️ Автозапуск срабатывает только при ВХОДЕ в Windows. Если сторож не бежит
(проверка: `pythonw` с `sync_sessions.py --watch` в списке процессов), подними руками:

```
wscript "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Claude-Sessions-Across-Accounts.vbs"
```

(Пережито 24.09.2026: сторож создан утром, до релогона Windows не бегал —
карточки новых сессий копировал только ручной прогон.)

## Что сказать Антону

- Сколько сессий стало видно на каждом аккаунте.
- Чтобы список в уже открытом приложении обновился, Claude надо полностью
  закрыть и открыть снова. Пока окно живое, оно держит старый список в памяти.
- Чаты на сайте claude.ai этим не переносятся: они лежат в облаке того
  аккаунта, под которым их писали.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
