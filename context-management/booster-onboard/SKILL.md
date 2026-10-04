---
name: booster-onboard
description: |
  Быстрый онбординг в незнакомую кодовую базу через booster MCP.
  Используй первым при работе с новым репозиторием.
---

# booster Onboard

## Цель

Быстро построить карту проекта, не читая всю кодовую базу подряд.

## Алгоритм

1. Для нового или большого локального репозитория запусти `booster expand --profile balanced` из его корня. До индексации прочитай `.agents/booster/scan_report.json` и при необходимости расширь scope через `--profile deep`.
2. Добавь репозиторий через add_repo. Сохранённый `scan_config.json` задаёт тот же scope для MCP-индексатора.
3. Проверь `get_repo_artifacts()` и только затем вызови `inject_context()` чтобы получить карту проекта (RepoMap) и список конвенций.
4. Вызови `fetch_stack_docs()`, чтобы понять какие библиотеки использует проект и подгрузить их доки (через mcp context7).
5. Сними масштаб через repo_stats().
6. Для больших проектов построй визуальную карту через get_code_city.
7. Найди точки входа через semantic_search и find_symbol.
8. Сохрани выводы в project_memory.

## Базовая последовательность

```text
booster expand --profile balanced
add_repo("<repo>")
get_repo_artifacts()
inject_context()
fetch_stack_docs()
repo_stats()
get_code_city()
semantic_search("application entry point")
list_configs()
project_memory("set", "architecture_overview", "...", repo="<repo>")
```

## Что извлечь

- точки входа
- ключевые модули
- внешний стек
- конфиги и env
- горячие зоны проекта

## Антипаттерны

- не читать подряд десятки файлов
- не пропускать repo_map
- не начинать багфикс без первичного онбординга
