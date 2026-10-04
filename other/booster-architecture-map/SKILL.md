---
name: booster-architecture-map
description: |
  Использование инструментов Booster для генерации и получения 
  макроархитектурных артефактов (Code City и Repo Map).
---

# Booster Architecture Map

## Цель

При работе с большими кодовыми базами важно понимать их структуру сверху вниз. Booster MCP предоставляет два мощных инструмента для генерации топологии:

1. **Repo Map** — сжатая текстовая репрезентация репозитория в стиле Aider (содержит классы и сигнатуры функций).
2. **Code City** — 3D-визуализация репозитория (здания = файлы, высота = метрики, цвет = язык).

## Алгоритм работы

1. **Repo Map (Текстовая структура)**
    Вызови `get_repo_map(repo_path="<path>")`.
    Ты получишь bounded architecture map с diversity по top-level modules,
    обязательным покрытием entrypoints/configs/contracts и coverage summary.
    *Основной файл: `[repo]/.agents/booster/repo_map_architecture.md`;*
    `repo_map.md` остаётся backward-compatible копией.
    Для подробных symbols используй `[repo]/.agents/booster/repo_map_symbols.md`.

2. **Code City (3D Визуализация)**
   Вызови `get_code_city(repo_path="<path>")`.
   Сервер сгенерирует HTML-файл с 3D-репрезентацией города и вернет тебе путь к нему, а также статистику метрик (сложность, кол-во строк, файлы).
    *Попроси пользователя открыть этот HTML файл в браузере `[repo]/.agents/booster/code_city.html`.*

    3. **Index Health**
       Проверь `get_repo_artifacts()` и `index_health.json`: generation,
       completeness, skipped/stale/deleted paths и причины вытеснения из map.

## Когда использовать

- В начале проекта (используя `booster-onboard`).
- Когда нужно найти архитектурные зависимости или "горячие зоны" (большие файлы = небоскребы в Code City).
- Для быстрого поиска импортов и сигнатур (с помощью `get_repo_map`).
- Для проверки, что giant modules не вытеснили frontend, control-plane и contracts.
