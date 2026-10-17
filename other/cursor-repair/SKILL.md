---
name: cursor-repair
description: "Repair the Cursor editor when it crashes, fails to launch, or new Agent chats break. Use with a Request ID, fresh logs, CursorRule.parse_error or invalid UTF8 in skill frontmatter, or a better-sqlite3 NODE_MODULE_VERSION mismatch. Finds a reproducible cause, applies a narrow reversible fix and proves it with two new chats. Triggers: /cursor-repair, Cursor won't start, Cursor agent broken."
license: MIT
consumer: "anyone asked to repair the app; Claude, Codex and Cursor agents"
version: 1.0.0
---

# Cursor: запуск и новые Agent-сессии

Портируемость: Windows проверен на a test Windows machine 04.10.2026. macOS/Linux: найти user-data, executable и runtime установленной версии; ветки DLL/MSIX не переносить. Проверка YAML применима к любой ОС, но фактический loader проверить отдельно.
Рельса: локальные команды, UI и официальные источники зависимостей; API-платежи не нужны. Для независимого ревью использовать доступную штатную рельсу другого вендора.

## 1. Зафиксировать и локализовать

- RECALL и свежий снимок: версия Cursor, путь executable, OS/architecture, время ошибки и Request ID, активная модель, новый или старый чат. Request ID сам по себе не объясняет причину.
- Windows: свежий каталог `$env:APPDATA\Cursor\logs`, renderer/window логи и `$env:APPDATA\Cursor\User\globalStorage\anysphere.cursor-agent-worker`. Смотреть корреляцию времени; не выгружать целиком токены и содержимое чатов.
- Приложение вообще не стартует: проверить процесс/окно/crash-log, свободное место, недавнее обновление; штатно запустить установленный executable. Если есть конкретная ошибка расширения, проверить запуск с отключёнными расширениями отдельным обратимым экспериментом. Не очищать весь user-data.
- Приложение работает, Agent нет: разделить pre-network сериализацию, локальный worker, auth/network и ответ провайдера. Исправление одного слоя не означает исправления всех.
- Сначала воспроизвести коротким новым чатом без инструментов. Если обычные логи дают только `[null,{}]`, после сохранения работы закрыть Cursor штатно и запустить его executable с `--enable-logging=file --log-file=<локальный-файл> --log trace`. Затем воспроизвести один раз и сверить свежий Electron log. Диагностические логи держать локально; после расследования следующий запуск обычный.

## 2. Ветка `CursorRule.parse_error` / `invalid UTF8`

1. Найти фактически загружаемые rules/skills, включая workspace и пользовательские каталоги, junction/symlink targets. Исправлять единственный исходник, не копию через мост.
2. Использовать parser установленного Cursor, если доступен: в Windows прецеденте `resources/app/node_modules/gray-matter`. Не подменять его другим YAML-парсером для финальной проверки.
3. Разобрать frontmatter каждого доступного SKILL.md. Для исключений проверить `error.message.isWellFormed()` в runtime с поддержкой метода, либо явную проверку непарных UTF-16 surrogate. Ошибка YAML и некорректная Unicode-строка ошибки являются разными состояниями.
4. Прецедент: голое описание с `: ` ломало YAML; усечённый snippet ошибки разрезал emoji и породил непарный surrogate. Это ломало сериализацию всего запроса до сети.
5. Взять lease, бэкап и хэш источника. Заключить description в двойные YAML-кавычки с корректным экранированием; для этой строки допустимы JSON-style escapes. Сохранить исходное значение, остальные строки и окончания строк. Не сокращать содержание попутно.
6. Повторить parser scan, проверить равенство значения description и отсутствие некорректных Unicode-ошибок. Остальные ошибки назвать отдельно, не объявлять весь каталог здоровым.

## 3. Ветка `NODE_MODULE_VERSION` / better-sqlite3

1. Найти активную версию agent-cli по свежему worker-log. Её bundled node и библиотека могут отличаться от системного Node. Записать `process.version`, `process.versions.modules`, platform/arch и версию better-sqlite3.
2. Воспроизвести bundled node. PowerShell: `& $bundledNode -e "const D=require(process.argv[1]); const db=new D(':memory:'); console.log(db.prepare('select 1 as ok').get()); db.close();" $modulePath`, где обе переменные содержат обнаруженные абсолютные пути к bundled node.exe и каталогу модуля better-sqlite3 (не к бинарнику .node). Не открывать реальные базы.
3. При подтверждённом ABI mismatch подобрать официальный prebuild ТОЙ ЖЕ версии библиотеки под фактические ABI, ОС и architecture. Проверить официальный release metadata/digest. Без совпадения не заменять бинарник; не брать случайный DLL и не ставить global npm как лечение.
4. Распаковать в staging, проверить состав архива и протестировать staged nativeBinding в памяти. Затем штатно остановить использующий модуль worker/приложение, сохранить старый бинарник и SHA256, заменить только доказанно несовместимый файл.
5. Перезапустить штатно; повторить SQL-test и проверить свежие worker-start/pipe-ready события. Это доказывает worker, но ещё не успешный чат. Для отката при остановленном потребителе вернуть именно свой бэкап и сверить хэш.
6. Прецедент 04.10.2026: Node 24.5.0 ABI137, better-sqlite3 12.11.1 был ABI127. Это исторические значения, не параметры будущего ремонта. Обновление Cursor может заменить весь version directory.

## 4. Закрытие ремонта

- Два отдельных новых чата на исходной модели должны вернуть разные заданные маркеры без tools/file access. Сохранить время и видимое подтверждение каждого; успех SQL или worker отдельно не засчитывать.
- Сопоставить свежие логи с каждым тестом. Если UI/лог расходятся, результат не доказан. Для start-only инцидента проверять окно и повторную штатную активацию; Agent не объявлять проверенным без ответов.
- Назвать изменённые файлы, бэкапы/откат, независимое ревью и пределы проверки. Изменение исходника скилла требует проверки YAML у реального потребителя до завершения.
- Записать ts, node, actor, event, outcome в существующий журнал ремонта/изменений. Без новой фоновой автоматики; секреты и private prompts не переносить в публичный отчёт.

Прецедент: Cursor 3.23.12, session-groups/SKILL.md исправлен одной строкой, значение description сохранено. Из 208 скиллов некорректные Unicode-ошибки 1 → 0; шесть иных YAML-ошибок оставлены отдельно. Два новых чата дали CURSOR_OK и CURSOR_SECOND_OK. Бинарный ремонт один новые чаты не восстановил; второй дефект был необходимой частью решения.

<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
