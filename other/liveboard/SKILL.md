---
name: liveboard
description: "Эфемерное live-табло: Git worktrees, процессы агентов и задачи Task Master через локальную SSE-панель."
---

# Liveboard

Ты запускаешь и держишь локальное read-only табло проекта. Цель — быстро дать владельцу правдивую оперативную картину, а не изменять код или статусы задач.

## Запуск

1. Определи Git root; если Git отсутствует — используй текущий каталог.
2. Запусти `node "<skill-root>/scripts/server.mjs" --root "<project-root>"` в foreground.
3. Дождись JSON-события `liveboard-ready` и сразу передай пользователю URL.
4. Держи процесс живым до явной остановки.

Сервер выбирает свободный порт на `127.0.0.1`, следит за Task Master, обновляет UI через SSE и делает полный перескан каждые 5 минут.

Настройка: `--root <path>` задаёт проект, `--host` — bind (по умолчанию `127.0.0.1`), `--port 0` — свободный порт, `--interval 300000` — полный перескан в миллисекундах. Endpoints: `/`, `/health`, `/api/snapshot`, `/api/events`, `POST /api/refresh`.

UI определяет язык браузера и поддерживает 43 локали. Для ar, he, fa и ur устанавливать RTL. Выбор не сохраняется за пределами памяти вкладки.

Task Master: ключ `ANTHROPIC_API_KEY` или `OPENAI_API_KEY`, затем `$task-master-provider <anthropic|openai|codex-cli> <model-id>`; Perplexity опционален только для research.

## Источники и точность

- Worktree: `git worktree list --porcelain`.
- Задачи: `.taskmaster/tasks/tasks.json` каждого worktree.
- Агенты: локальные процессы Claude/Codex/Cursor и их cwd.
- Запись `process` является наблюдением, а роль из `in-progress` задачи (`task`) — inference.
- Если ОС скрывает cwd, показывай процесс без привязки.

## Ограничения

- Не писать snapshot, PID или логи на диск.
- Не использовать внешний bind без явного запроса.
- Не менять Task Master: это наблюдающая роль.
- Остановить по `Ctrl+C`/SIGTERM; состояние существует только в памяти.
- Для проверки использовать `/health` и `/api/snapshot`.

Команды: `$liveboard-start` запускает табло, `$liveboard-vorcl` ведёт разработку самого liveboard через Task Master.
