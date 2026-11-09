---
name: dsh-converter
description: "Конвертация промтов, инструкций и скилов ChatGPT/Claude в формат DeepSeek Harness (DSH)"
whenToUse: "Применяй, когда нужно перенести скилы, инструкции или агентов из ChatGPT/Claude в DeepSeek Harness (dsh)"
---

# DeepSeek Harness Converter

Конвертация промтов, инструкций и скилов ChatGPT/Claude в **DeepSeek Harness** (`dsh`). Запуск: `npx @deepseek-ai/dsh web`.

> Прежде чем конвертировать, спроси (или определи по контексту): это **скил**, **инструкция/prompt** или **GPT-агент**. От этого зависит целевой формат.

## Таблица соответствия

| Источник | Куда в DSH | Как |
|---|---|---|
| Скил (`SKILL.md`) | DSH-скил | нормализовать frontmatter → `SKILL.md` в discovery-root |
| Custom Instructions | `AGENTS.md` | глобально `~/.dsh/AGENTS.md` или в корне проекта |
| Стиль ответа, persona | persona-строка | пресет `@deepseek-ai/dsh-persona` |
| Системный промпт | persona `prefix` или `ctx.systemPrompt.section()` | см. «Промпты» |
| GPT (имя + инструкции) | пресет агента или скил | `dsh-agent-preset` + `dsh-persona`, либо просто скил |
| GPT со знаниями (файлы) | скил с `references/` | перенести файлы в подкаталог |
| GPT с действиями (API) | плагин (TypeScript) | `apply(ctx)` + свои инструменты |

## Discovery roots (куда класть файлы)

DSH ищет скилы по рангу (меньше — приоритетнее):

| Ранг | Корень |
|---|---|
| 100 | `<project>/.dsh/skills` |
| 200 | `<project>/.agents/skills` |
| 300 | пользовательские каталоги (`customSkillDirs`) |
| 400 | `~/.dsh/skills` |
| 500 | `~/.agents/skills` |
| 600 | bundled |

- Скил — каталог `<name>/SKILL.md` (можно с `references/`, `templates/`) или плоский `<name>.md`.
- Глобальные инструкции: `~/.dsh/AGENTS.md`; проект: `AGENTS.md`/`CLAUDE.md` от корня проекта вниз.

## 1. Скил → DSH-скил

Правила:
1. `name` — строго kebab-case: `^[a-z0-9]+(?:-[a-z0-9]+)*$`
2. `description` — краткая «маршрутизирующая» фраза: **когда** применять
3. `whenToUse` — дополнительная подсказка для маршрутизации
4. `disable-model-invocation` и `user-invocable` — булевы (опционально)
5. Лишние ключи ChatGPT (`allowed-tools`, `license`, `metadata`, `version`, `compatibility`) — **выбросить**
6. Тело — Markdown. Ссылки на файлы внутри скила — относительно каталога скила

## 2. Инструкции → AGENTS.md

- «Что ChatGPT должен знать о тебе» → `~/.dsh/AGENTS.md` (глобально, подхватывается автоматически)
- Инструкции проекта → `AGENTS.md` в корне проекта
- Markdown, инструкции в императиве

## 3. Persona

Строка в пресете задаёт identity агента:
```yaml
- name: '@deepseek-ai/dsh-persona'
  config:
    prefix: You are a terse systems engineer…
    suffix: ''
    complete: false
```
- `prefix` — системный промпт/роль (обязательный)
- `suffix` — стиль ответа (по умолчанию пусто)
- `complete: true` — если нужно полностью заменить системный промпт
- `dsh-persona` монтируется **только внутри пресета**

## 4. GPT → пресет агента

Пресет = именованный агент с плагинами и персоной:
```yaml
- id: agent-preset-registry
  name: '@deepseek-ai/dsh-agent-preset-registry'
  config:
    default: standard

- id: preset-sql-expert
  name: '@deepseek-ai/dsh-agent-preset'
  config:
    id: sql-expert
    name: SQL Expert
    description: Reviews and writes SQL migrations
    plugins:
      - name: '@deepseek-ai/dsh-persona'
        config:
          prefix: You are a senior SQL engineer…
```
- `config.id` — стабильный идентификатор (kebab-case)
- Инструкции GPT → `persona.prefix`; описание → `config.description`
- Простой GPT без инструментов → просто скил (дешевле)

## 5. Плагин (только когда нужен код)

Минимальный плагин:
```ts
import type { Context } from '@deepseek-ai/cordis'
export const name = 'my-tool'
export function apply(ctx: Context) { /* инструменты, сервисы */ }
```

## Проверка результата
- [ ] `name` — kebab-case, уникален
- [ ] `description` и `whenToUse` — коротко, «когда использовать»
- [ ] Файл лежит в discovery-root, имя каталога совпадает с `name`
- [ ] Лишние frontmatter-ключи ChatGPT удалены
- [ ] Промпт/инструкции — в `AGENTS.md` или `persona.prefix`, не «рассыпаны»
- [ ] `dsh-persona` только внутри пресета
- [ ] Нет секретов/ключей в конвертируемых текстах
- [ ] Пользователю сообщены полные пути к созданным файлам