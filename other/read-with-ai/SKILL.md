---
name: read-with-ai
description: "Add a 'Read with AI' widget under published content: a copy-the-prompt button plus deep links that open the material already loaded into an agent (Codex, ChatGPT, Claude). Triggers: /read-with-ai, read with AI buttons, add AI buttons, widget under the article."
license: MIT
version: 1.0.0
---

READ-WITH-AI — «кнопки под каждой статьёй»

ПРИКАЗ (Антон, голосовая 19.09.2026, tg:-[id], дословно):
«Мне нужно также сделать кнопки на моем гитхабе. Под каждой статьей. И также на
любых ресурсах где можно добавлять кнопки. 1/ скопировать промпт. Чтобы сделать
ТАКЖЕ 2/ готовый промпт и авто открытие жпт но лучше кодекса 3/ готовый промпт и
авто открытие клода.»
Образец, который он прислал скриншотом: виджет под статьями на [человек].coach.

ЗАЧЕМ ЭТО НАМ (не украшение): читатель приходит за одним файлом, а уходит с
агентом, который уже держит наш материал в контексте. Это дверь к цели №1
(инженер-тестер, CLAUDE.md §1.1) и к «всё = контент».

## Один источник правды
`~/.claude/scripts/read_with_ai.py` — генератор промпта и трёх кнопок.
Промпт пишется ОДИН раз и разъезжается по форматам; руками блоки не собираем.

## Три поверхности — какой формат куда

| поверхность | формат | чем копируется промпт |
|---|---|---|
| README репо, gist, dev.to, Habr-markdown | `--format md` | ⭐ `<details>` + fenced-блок: копи-кнопку рисует САМ GitHub (`data-snippet-clipboard-copy-content`). JS на GitHub запрещён, это единственный честный путь |
| GitHub Pages, наш сайт, любой HTML | `--format html` | настоящая кнопка (clipboard API + фолбэк execCommand) + плавающая пилюля внизу экрана |
| Telegram, FB, письмо | `--format text` | голые ссылки, копирует сам читатель |

## Команды

Новый или обновлённый репо (единичный):
```
python ~/.claude/scripts/read_with_ai.py --repo tonydzi/<имя> --apply <путь>/README.md
```

Статья на сайте:
```
python ~/.claude/scripts/read_with_ai.py --url "<URL>" --title "<Заголовок>" --format html > widget.html
```

Волна по всем публичным не-форк репо (идемпотентна, пустых коммитов не делает):
```
python ~/.claude/scripts/read_with_ai_rollout.py --dry-run      # план
python ~/.claude/scripts/read_with_ai_rollout.py --only <имя>   # канарейка
python ~/.claude/scripts/read_with_ai_rollout.py                # волна
```

Статический сайт целиком (каждая страница получает СВОЙ URL в промпте):
```
python ~/.claude/scripts/read_with_ai_pages.py --root <dir> --base https://tonydzi.github.io --skip call/index.html
python ~/.claude/scripts/_check_pages_widget.py <dir> https://tonydzi.github.io   # второй заход, читает факт в файле
```

## Диплинки: что чем доказано (§5.4 — «причина такой же claim, как вывод»)
- `chatgpt.com/?q=<enc>` и `claude.ai/new?q=<enc>` — ✅ вычитаны из живого HTML
  [человек].coach 20.09, тот же паттерн работает в проде у автора образца.
- `chatgpt.com/codex?prompt=<enc>` — 🤔 улика по употреблению в дикой природе
  (`CihadCengiz/prompt-generator`, page.jsx:216, «Open in ChatGPT Codex»); своего
  клик-теста НЕ делали. Отказ мягкий: параметр проигнорируется — читатель попадёт
  на Codex с пустым полем, а промпт лежит в копи-кнопке рядом.
- `codex://new?prompt=<enc>` — ✅ документированная схема ДЕСКТОПНОГО Codex
  (gist zhuowei/98005fb9…). В веб-кнопку не ставим: без установленного приложения
  ссылка выглядит сломанной. Отдаётся флагом `--codex-desktop`.

## Границы
- ⛔ Не трогаем ФОРКИ чужих проектов — `gh repo list --source` их и не отдаёт.
- ⛔ `dashboards` и `github-evidence` пропускаем с названной причиной: первый не
  статьи, у второго README пересобирает робот и затрёт блок.
- ⛔ Страницу-бронь (`/call/`) не засоряем: там должен остаться один CTA.
- Подпись `github.com/tonydzi` вшита в каждый формат (§1.1); убрать её нельзя,
  тест `_test_read_with_ai.py` на это краснеет.
- Идемпотентность держат HTML-маркеры; повторный прогон заменяет блок, а не плодит.

## Тесты
```
python ~/.claude/scripts/_test_read_with_ai.py      # регресс, 46 проверок
python ~/.claude/scripts/_killrun_read_with_ai.py   # kill-list: 7 мутаций, все ловятся
```

## Кто вызывает (потребители названы, §9.3-тер)
- `/release-slice` шаг 7b — новый публичный репо получает виджет при рождении.
- Эта дверь (`/read-with-ai`) — руками, когда появилась новая статья/страница.
- Антон — когда видит поверхность, где можно поставить кнопки.

## Замер при рождении (20.09.2026)
49 публичных репо с виджетом (47 создано волной + 2 канарейки), 0 ошибок;
8 страниц tonydzi.github.io, живое подтверждено curl'ом после деплоя.



<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
