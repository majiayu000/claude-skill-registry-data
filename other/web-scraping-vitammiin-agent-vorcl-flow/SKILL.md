---
name: web-scraping
description: Маршрутизирует веб-поиск, scrape, map, crawl, extract, interact, parse, monitor, research и support через Firecrawl CLI, MCP или REST. Use для live web data, интеграции Firecrawl в приложение и повторяемых deliverables с URL-источниками.
---

# Firecrawl router

Выбери один режим:

1. **Live web work** — данные нужны агенту сейчас. Предпочитай установленный и авторизованный CLI; иначе MCP; затем REST/keyless fallback.
2. **App integration** — Firecrawl должен работать в продукте. Передай задачу upstream-скиллам `firecrawl-build*` через `$firecrawl-integrate`.
3. **Deliverable** — нужен готовый аудит, brief, lead list, knowledge base или другой артефакт. Передай задачу `firecrawl-workflows` через `$firecrawl-deliverable`.

## Live routing

- Проверь `command -v firecrawl` и `firecrawl --status`. Перед использованием команды проверь её наличие через `firecrawl <command> --help`; не выдумывай синтаксис.
- URL неизвестен: `search`; известен один URL: `scrape`; список URL: `map`; раздел/сайт: `crawl` с `limit`; браузерные действия: `interact`; локальный документ: `parse`; периодическая проверка: `monitor`; длительное исследование: `agent`/`research`.
- Если CLI отсутствует или команда не поддерживается, используй эквивалентный MCP-инструмент. Если и его нет — REST v2 с `FIRECRAWL_API_KEY`; keyless разрешён только для официально поддерживаемых операций.
- Для `ask` и `docs-search` сначала проверь CLI. При отсутствии используй MCP или `/v2/support/ask` и `/v2/support/docs-search` по актуальной документации.
- Сохраняй результаты в `.firecrawl/`; у каждого факта оставляй URL. Не печатай ключи, cookies, токены и PII.

## Стоимость и безопасность

- Дешёвый путь: `search`/`map` → точечный `scrape` → ограниченный `crawl`.
- Перед crawl всего сайта или `limit > 50`, запуском платного agent без лимита, созданием/изменением/удалением monitor и необратимым действием interact получи явное подтверждение.
- Для agent/research задай предел кредита/стоимости и критерий остановки.
- При ошибке сохраняй реальный `jobId`, статус и параметры; затем используй support/ask. Не подменяй ошибку догадкой.

## Structured output

Для JSON задай `prompt` и JSON Schema. Одна страница — structured scrape; несколько URL/домен — extract. Проверь JSON по схеме и приложи source URLs.

## Setup

Установка и browser auth меняют окружение, поэтому выполняй их только после подтверждения пользователя: `npx -y firecrawl-cli@latest init --all --browser`. Затем проверь `firecrawl --status` и сделай smoke scrape в `.firecrawl/install-check.md`. Никогда не сохраняй ключ из чата без отдельного согласия.
