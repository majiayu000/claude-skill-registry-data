---
name: available-stacks
description: Available coder stacks for task planning. Maps agent names to technology specializations.
user-invocable: false
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


# Доступные стеки кодера

Используется ОДИН универсальный агент `coder` с динамической подгрузкой скиллов по стеку.
В поле `agent` каждого шага пиши `coder-{stack}` — executor автоматически подгрузит нужные скиллы.

## Стеки

| Stack | Специализация |
|-------|--------------|
| `coder-python` | Python (FastAPI, Django, asyncio, Pydantic) |
| `coder-telegram` | Telegram боты (Grammy, Telegraf, aiogram) |
| `coder-backend` | Backend API (Fastify, Express, NestJS) |
| `coder-frontend` | Frontend (HTML, CSS, Tailwind) |
| `coder-vue` | Vue 3 / Nuxt 3 |
| `coder-react` | React / Next.js |
| `coder-fastapi` | FastAPI (endpoints, middleware) |
| `coder-sql` | SQL / PostgreSQL |
| `coder-bash` | Shell скрипты |
| `coder-docker` | Docker, Kubernetes |
| `coder-testing` | Тесты (pytest, vitest, Playwright) |
| `coder-refactor` | Рефакторинг кода |
| `coder-fix` | Баг-фиксы (НЕ для select_stack, только программно) |
| `coder-worker` | Background workers, queues |
| `coder-golang` | Go backend |
| `coder-rust` | Rust |
| `coder-mobile` | React Native / Expo |
| `coder-security` | Security hardening |
| `coder-sysadmin` | Linux server admin |
| `coder-data` | Data engineering, ETL |
| `coder-langchain` | LangChain / AI agents |
| `coder-llm-api` | LLM API integration |
| `coder-ml` | Machine Learning |
| `coder-cicd` | CI/CD pipelines |
| `coder-terraform` | Infrastructure as Code |
| `coder-svelte` | Svelte / SvelteKit |
| `coder-threejs` | Three.js / WebGL |
| `coder-nosql` | NoSQL databases |
| `coder-serverless` | Serverless (Lambda, Cloud Functions) |

## Не-кодерские агенты

| Agent | Когда |
|-------|-------|
| `ui-designer` | Дизайн-задачи: макеты, цвета, типографика, UX (BM25 база дизайна) |
| `copywriter` | Тексты: лендинг, UX-тексты, email, README, блоги (anti-AI фильтр) |
| `debugger` | Диагностика ошибок сборки/тестов |
| `dba` | SQL, миграции, оптимизация запросов |
| `researcher` | Исследование технологий, API, библиотек |

## КРИТИЧЕСКОЕ ПРАВИЛО

**НИКОГДА не пиши `"agent": "coder"` без стека.**
ВСЕГДА указывай конкретный стек: `coder-nextjs`, `coder-backend`, `coder-telegram` и т.д.

Это ОБЯЗАТЕЛЬНО — от стека зависит загрузка специализированных скиллов в агента.
Проанализируй файлы и технологии каждого шага, выбери наиболее точный стек.

Если задача TypeScript/Node.js — используй `coder-backend`.
Если задача React/Next.js — используй `coder-react`.

**Формат:** `coder-{stack}`. Executor извлечёт стек и подгрузит скиллы автоматически.
