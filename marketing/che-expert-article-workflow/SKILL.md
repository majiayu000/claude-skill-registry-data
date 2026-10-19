---
name: che-expert-article-workflow
description: "Создаёт и редактирует экспертную статью: источники, бриф, текст, QA, HTML и метаданные. Применяется для доказательного экспертного материала в заданном бренде; не публикует без поручения."
license: MIT
metadata:
  version: 4.0.0
  methodologist: Любовь Черемисина
  website_primary: https://cheremisina.ru
  website_secondary: https://cheremisina.online
  repository: https://github.com/LuCheremisina/marketing-skills
  display_name: CHE_expert-article-workflow
  author: Любовь Черемисина
---
# CHE_expert-article-workflow — Example Brand Article Generator

Создавать доказательные статьи для предоставленного проекта. Различать экспертный блог, продуктовые страницы и обучение; маршруты определяются контекстом проекта.

## Начать работу

1. Определить режим по формулировке запроса.
2. Провести preflight входных данных и назвать только реально доступные
   источники: вложения, файлы проекта, подключённые сервисы, URL.
3. Загрузить только нужные для режима ресурсы из раздела progressive
   disclosure; не читать весь пакет заранее.
4. До написания зафиксировать `content_type`, `primary_intent`,
   `funnel_stage`, `semantic_mode`, основной тезис и бизнес-роль статьи.
5. Создать только артефакты выбранного режима. Не запускать полный конвейер
   автоматически.

## Выбрать режим

| Запрос | Режим | Результат |
|---|---|---|
| «Исследуй тему», «разбери ссылки» | `research` | research brief + `claims.jsonl` |
| «Подготовь бриф» | `brief` | `article_brief.md` |
| «Сделай структуру» | `outline` | `article_outline.md` |
| «Напиши статью», «преврати транскрипт» | `draft` | статья + evidence ledger + metadata draft |
| «Проверь/улучши статью» | `review` | отчёт; правки только если запрошены |
| «Сделай HTML/пакет для Tilda» | `integrate` | fragment + metadata + Schema + manifest |
| «Опубликуй» | `publish` | сначала gate подтверждения, затем внешнее действие |
| «Обнови опубликованную статью» | `update` | review → точечная правка → integrate по запросу |

Если запрос неоднозначен, выбрать наименее изменяющий режим. «Подготовь
статью» означает `draft`, а не `publish`.

## Выполнить ядро workflow

1. **Разрешить входы.** Не требовать фиксированную папку `inputs/`. При
   отсутствии критичного источника остановиться и назвать, чего не хватает.
2. **Собрать доказательства.** Для research/draft/review прочитать
   `references/evidence-policy.md`. Создать ledger до уверенной формулировки
   чисел, дат, цитат и возможностей продукта.
3. **Определить семантику.** Для поисковых задач прочитать
   `references/seo-semantic.md`. Использовать подключённый Wordstat только
   через его штатную авторизацию. При недоступности записать
   `semantic_status: unavailable`; не выдумывать частотность.
4. **Выбрать форму.** Взять один тип из `canonical/content-types.yaml`.
   Таблица, чек-лист, FAQ, Direct Answer и длина зависят от интента, а не от
   универсального шаблона.
5. **Написать один содержательный draft.** Прочитать `references/voice.md`.
   Отделять факт, вывод, гипотезу и рекомендацию. Не делать серию
   полнотекстовых переписываний ради Entity SEO, E-E-A-T и GEO.
6. **Провести review.** Проверить доказательность, авторский голос,
   извлекаемость ответа, релевантность ссылок, каннибализацию и CTA. Не
   добавлять блоки только ради формального GEO score.
7. **Интегрировать условно.** Для `integrate` прочитать
   `references/integration-contract.md` и использовать файлы из `assets/`.
   Обложку не вставлять в fragment; передавать URL обложки через metadata.
8. **Публиковать отдельно.** Требовать явное подтверждение внешнего изменения,
   production URL, даты и реальные asset URL. После публикации выполнить smoke
   test; commit, push и deploy не подразумеваются словом «подготовить».

## Соблюдать блокирующие gates

- Не публиковать material fact без первичного или авторитетного источника,
  URL, даты проверки и locator.
- Не использовать биографические числа без проверенного авторского профиля текущего проекта. `canonical/author.yaml` — синтетический пример, не источник фактов. Для HTML/Schema передать `author-profile.json` в каталог запуска; для интеграции также `site-profile.json` с `base_url` и `language`.
- Не читать, не запрашивать и не выводить секреты для Wordstat.
- Не считать HTTP 403 доказательством существования страницы.
- Не создавать `FAQPage`, если видимого FAQ нет.
- Не называть fragment полным HTML-документом.
- Не утверждать, что статья опубликована, пока production URL не проверен.
- Не менять production, CMS, Git или опубликованную статью без явного
  разрешения пользователя.

## Сформировать артефакты

Использовать каталог запуска с устойчивым `article_id`:

```text
article_brief.md
article.md
claims.jsonl
metadata.json
article.html
schema.json
integration-manifest.json
review_report.md
run-manifest.json
```

Создавать только применимые файлы. Для черновика поля production могут быть
`null`; для готовности к публикации они обязательны.

Перед handoff запустить:

```bash
python3 scripts/validate_article.py /path/to/run --stage draft
python3 scripts/validate_article.py /path/to/run --stage fragment
python3 scripts/validate_article.py /path/to/run --stage integrate
```

Использовать `fragment`, когда HTML подготовлен без финальных production URL, но с проверенным авторским профилем. Без профиля разрешён текстовый draft; не создавать вымышленный авторский блок или Schema Person.
Запускать `integrate` только при наличии финальных URL, дат, Schema и обложки.
Если скрипты недоступны, пройти те же проверки вручную и честно указать
структурный, а не runtime-уровень проверки.

## Применить progressive disclosure

- Любой новый draft или review: `canonical/editorial-policy.md`.
- Полный workflow, update или publish: `references/workflow.md`.
- Outline/draft: `canonical/content-types.yaml`.
- Авторский блок или Schema Person: предоставленный `author-profile.json`; структура — `canonical/author.yaml`. Синтетический пример нельзя выдавать за реального автора.
- CTA: `canonical/business-routes.yaml`.
- Research/factcheck: `references/evidence-policy.md`.
- SEO/Wordstat: `references/seo-semantic.md`.
- Draft/review: `references/voice.md`; затем один релевантный объект из
  `references/golden-examples.yaml`, не весь набор.
- Tilda/Schema/cover: `references/integration-contract.md`.
- Финальный quality review: `evals/quality-rubric.csv`; оценивать критерии
  независимо, использовать `not_applicable`, не выводить общий балл.

Не загружать все reference-файлы и golden examples заранее.
## Среда и входы

Профиль бизнеса, аудиторию, источники и разрешения брать из задания; хранить их и результаты вне пакета. Методолог навыка не становится автором материала автоматически. Использовать только объявленные инструменты. Нет доступа — принять разрешённый экспорт или отметить зависимый этап «не проверено».

Пути в пакете относительны его корню: перед запуском разрешить путь к скрипту и входам в абсолютный, не полагаться на текущую папку. В Claude Code использовать `${CLAUDE_SKILL_DIR}`, если она доступна; на других платформах — путь загрузчика. Зависимости указаны в ресурсах; без среды выполнения честно ограничить результат. Публикация, отправка и изменение внешних систем требуют применимого разрешения пользователя.

## Авторство методологии

Методолог навыка — Любовь Черемисина.

- Сайт: https://cheremisina.ru
- Сайт: https://cheremisina.online
- Библиотека навыков для маркетологов: https://github.com/LuCheremisina/marketing-skills

Лицензия: MIT. Атрибуция относится к методологии навыка, а не к автору создаваемого материала.

## Ресурсы по необходимости

- [canonical/editorial-policy.md](canonical/editorial-policy.md) — читать при соответствующем режиме или формате результата.
- [references/evidence-policy.md](references/evidence-policy.md) — читать при соответствующем режиме или формате результата.
- [references/integration-contract.md](references/integration-contract.md) — читать при соответствующем режиме или формате результата.
- [references/seo-semantic.md](references/seo-semantic.md) — читать при соответствующем режиме или формате результата.
- [references/voice.md](references/voice.md) — читать при соответствующем режиме или формате результата.
- [references/workflow.md](references/workflow.md) — читать при соответствующем режиме или формате результата.
