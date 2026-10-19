---
name: che-seo-article-generator
license: MIT
description: "Выполняет 18-этапный SEO/GEO-конвейер статьи: исследование, семантика, текст, фактчек, HTML, метаданные и QA. Применяется для полной SEO-статьи; для экспертного редакционного материала использовать che-expert-article-workflow."
metadata:
  version: 3.0.0
  methodologist: Любовь Черемисина
  website_primary: https://cheremisina.ru
  website_secondary: https://cheremisina.online
  repository: https://github.com/LuCheremisina/marketing-skills
  display_name: CHE_seo-article-generator
  author: Любовь Черемисина
---

# CHE_seo-article-generator — che-seo-article-generator

## Маршрутизация

- Полный SEO/GEO-конвейер для стороннего сайта → этот skill.
- Отдельный черновик, метаописание или один этап не требует автоматического
  запуска всех 18 этапов.

## Запуск

Читать `references/01_orchestrator.md` — он управляет полным пайплайном.
Reference-файлы 02–18 читать по мере выполнения этапов.

**Wordstat:** использовать capability `wordstat.top_requests.read`; способ
подключения определяет платформа (см. `references/LAUNCH.md`).

## Входные данные (проектная папка `inputs/`)

Клиентские inputs хранить в выбранной рабочей папке проекта, отдельно от
установленного пакета. В пакете находятся только примеры; CSS клиента передавать
как runtime style override, не изменяя оригинальный шаблон.

| Файл | Назначение |
|---|---|
| `config.txt` | Конфиг: SITE_URL, AUTHOR_NAME, AUTHOR_ROLE, CTA_URL (обязательно) |
| `brand_voice.txt` | Tone of voice, ценности бренда, авторский стиль (обязательно) |
| `site_links.txt` | Список URL сайта для внутренних ссылок (обязательно) |
| `seo_requirements.txt` | SEO-требования (обязательно) |
| `transcript.txt` ИЛИ `source_links.txt` | Исходный материал (одно из двух) |

## Pipeline (18 этапов)

| Этап | Название | Reference |
|---|---|---|
| 0 | Init + Style Lock | `references/01_orchestrator.md` + `references/benchmarks.md` |
| 1 | Research | `references/02_research_context.md` |
| 2 | Semantic Analysis | che-wordstat-keyword-research + `references/03_semantic.md` |
| 3 | Structure | `references/04_structure.md` |
| 4 | Article Writing | `references/05_article_writer.md` |
| 5 | Fact Check | `references/06_fact_check.md` |
| 6 | Entity SEO | `references/07_entity_seo.md` → `entity_seo_article.md` |
| 7 | Internal Linking | `references/08_internal_linking.md` → `article_with_links.md` |
| 8 | Link 404 Audit | curl-проверка всех внутренних ссылок |
| 9 | AI Citation | `references/09_ai_citation.md` |
| 10 | E-E-A-T | `references/10_eeat_builder.md` |
| 11 | Knowledge Graph | `references/11_knowledge_graph.md` |
| 12 | GEO Optimization | `references/12_geo_optimizer.md` |
| 13 | FAQ + CTA | `references/13_faq.md` + `references/14_cta.md` |
| 14 | SEO Metadata | `references/15_seo.md` → `seo_metadata.md` |
| 15 | Schema.org | `references/16_schema.md` → встраивается в HTML |
| 16 | Cover | `references/17_visual.md` → `cover_image.png` |
| 17 | Publication | `references/18_publication.md` → `final_article.html` |

## Ограничения по длине

| Параметр | Значение |
|---|---|
| Минимум | 10 000 символов с пробелами |
| Максимум | 16 000 символов с пробелами |
| Цель | 11 500 – 14 500 символов |

## Финальный результат

1. `final_article.html` — HTML (Schema.org встроена, H1 только в метаданных)
2. `seo_metadata.md` — SEO-метаданные в Markdown
3. `cover_image.png` — обложка 16:9
4. `geo_score_report.md` — GEO Score (цель ≥ 12/15)

## Финальный quality gate

Перед выдачей результата применить по отдельности критерии `evals/shared.csv` и `evals/skill-specific.csv` по инструкции `evals/judge_prompt.md`. Не считать общий балл. `N/A` не считать провалом. Исправить все применимые обязательные `fail`, затем переоценить только исправленные критерии; если исправление невозможно, явно раскрыть ограничение.

## Навигация по ресурсам

- [references/01_orchestrator.md](references/01_orchestrator.md) — читать при соответствующем этапе workflow.
- [references/02_research_context.md](references/02_research_context.md) — читать при соответствующем этапе workflow.
- [references/03_semantic.md](references/03_semantic.md) — читать при соответствующем этапе workflow.
- [references/04_structure.md](references/04_structure.md) — читать при соответствующем этапе workflow.
- [references/05_article_writer.md](references/05_article_writer.md) — читать при соответствующем этапе workflow.
- [references/06_fact_check.md](references/06_fact_check.md) — читать при соответствующем этапе workflow.
- [references/07_entity_seo.md](references/07_entity_seo.md) — читать при соответствующем этапе workflow.
- [references/08_internal_linking.md](references/08_internal_linking.md) — читать при соответствующем этапе workflow.
- [references/09_ai_citation.md](references/09_ai_citation.md) — читать при соответствующем этапе workflow.
- [references/10_eeat_builder.md](references/10_eeat_builder.md) — читать при соответствующем этапе workflow.
- [references/11_knowledge_graph.md](references/11_knowledge_graph.md) — читать при соответствующем этапе workflow.
- [references/12_geo_optimizer.md](references/12_geo_optimizer.md) — читать при соответствующем этапе workflow.
- [references/13_faq.md](references/13_faq.md) — читать при соответствующем этапе workflow.
- [references/14_cta.md](references/14_cta.md) — читать при соответствующем этапе workflow.
- [references/15_seo.md](references/15_seo.md) — читать при соответствующем этапе workflow.
- [references/16_schema.md](references/16_schema.md) — читать при соответствующем этапе workflow.
- [references/17_visual.md](references/17_visual.md) — читать при соответствующем этапе workflow.
- [references/18_publication.md](references/18_publication.md) — читать при соответствующем этапе workflow.
- [references/LAUNCH.md](references/LAUNCH.md) — читать при соответствующем этапе workflow.
- [references/benchmarks.md](references/benchmarks.md) — читать при соответствующем этапе workflow.
- [references/cover_prompt.md](references/cover_prompt.md) — читать при соответствующем этапе workflow.
- [references/style_qa_checklist.md](references/style_qa_checklist.md) — читать при соответствующем этапе workflow.

## Среда и входы

Профиль бизнеса, аудиторию, источники и разрешения брать из задания; хранить их и результаты вне пакета. Методолог навыка не становится автором материала автоматически. Использовать только объявленные инструменты. Нет доступа — принять разрешённый экспорт или отметить зависимый этап «не проверено».

Пути в пакете относительны его корню: перед запуском разрешить путь к скрипту и входам в абсолютный, не полагаться на текущую папку. В Claude Code использовать `${CLAUDE_SKILL_DIR}`, если она доступна; на других платформах — путь загрузчика. Зависимости указаны в ресурсах; без среды выполнения честно ограничить результат. Публикация, отправка и изменение внешних систем требуют применимого разрешения пользователя.

## Авторство

Методолог навыка — **Любовь Черемисина**. Лицензия оригинальной методологии и
кода этого пакета — MIT.

- [Основной сайт](https://cheremisina.ru)
- [Экспертные материалы](https://cheremisina.online)
- [Навыки для маркетологов](https://github.com/LuCheremisina/marketing-skills)

Атрибуция относится к пакету; не добавлять рекламную подпись в каждый результат.

## Ресурсы по необходимости

- [evals/judge_prompt.md](evals/judge_prompt.md) — читать при проверке результата.
