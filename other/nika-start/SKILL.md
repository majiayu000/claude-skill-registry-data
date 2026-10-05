---
name: nika-start
description: >-
  Запуск проекта FST (tabel) у Ники: Cursor с настройками workspace, dev-сервер
  fst-web, деплой Firebase/Vercel. Use when the user says nika start, ника старт,
  запусти проект, старт FST, or asks to open/start this repo with saved settings.
disable-model-invocation: true
---

# Nika Start

Старт локальной разработки **FST / tabel** с зафиксированными настройками проекта.

## Быстрый старт (Windows)

Ярлык на рабочем столе: **«Nika Start — FST»**.

Или из корня репозитория:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\nika-start.ps1
```

Только Cursor, без dev:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\nika-start.ps1 -IdeOnly
```

## Что делает скрипт

1. Обновляет `PATH` (Node/npm на Windows).
2. Открывает **Cursor** с папкой проекта (подхватывает `.vscode/settings.json`).
3. В отдельном окне PowerShell: `npm run dev` → http://localhost:5173/
4. Через ~4 с открывает браузер (флаг `-NoBrowser` отключает).

## Настройки проекта (сохранены)

| Файл | Назначение |
|------|------------|
| `.vscode/settings.json` | TS 6 из `node_modules`, UTF-8, PowerShell-терминал |
| `.vscode/tasks.json` | Задачи **FST: dev server**, **FST: build** |
| `.vscode/extensions.json` | ESLint, Prettier, Tailwind |

**Важно:** `"ignoreDeprecations": "6.0"` в tsconfig — валидно только для TS 6 из workspace.
После открытия проекта в Cursor: **Use Workspace Version** для TypeScript.

## Структура и команды

- Код: `src/` (общий), веб-сборка: `fst-web/`
- `npm run dev` — локальный кабинет (Vite 5173)
- `npm run build` — production-сборка
- Деплой: `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1 -Target all`
  - Firebase: https://fst-uchet-14c02.web.app
  - Vercel: https://fst-uchet-theta.vercel.app

Подробнее: `docs/DEPLOY.md`, архитектура: skill `fst-architecture`.

## Если dev падает на Windows

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
cd fst-web
npm run build
```

Firebase deploy иногда падает с `-1073741819` — повторить `npx firebase deploy`.

## Агенту

По запросу «nika start» / «ника старт» — предложить ярлык или выполнить `scripts/nika-start.ps1`.
Не менять `.vscode/settings.json` без явной просьбы.
