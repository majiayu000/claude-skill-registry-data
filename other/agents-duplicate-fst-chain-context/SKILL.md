---
name: fst-chain-context
description: >-
  Агент цепочек Otgruzka/FST: перед любой правкой собирает graphify-связи,
  модули и риски (Firebase, sync, i18n) и выдаёт бриф агенту. Use when
  starting a fix/feature, before editing src/, or when user mentions цепочка,
  связи, как работает, контекст, агент контекста.
---

# FST — агент цепочек (контекст перед правками)

Ты **не пишешь код сразу**. Сначала собираешь карту «как связано», потом правишь тонко.

Прод: https://otgruzka-tovara.vercel.app · Firebase `otgruzka-tovara` · код `src/` + `fst-web/`.

## Когда включать (обязательно)

- Любая **коррекция / фича / баг** в `src/` или `fst-web/` (кроме однострочного комментария)
- Пользователь просит «как связано», «по цепочке», «изучи», «перед правкой»
- Неясный модуль (табель, склад, ОС, ЗП, sync)

Пропуск только если: опечатка в i18n-строке без логики, или пользователь явно сказал «без брифа».

## Шаги (коротко)

1. **Тема** — 3–8 слов из запроса пользователя (символы/экраны).
2. **Сбор** — выполни (из корня репо):
   ```powershell
   node scripts/fst-chain-brief.mjs "<тема>" ["СимволA"] ["СимволB"]
   ```
   Или вручную:
   - `graphify query "<тема>"`
   - `graphify explain "<главный символ>"`
   - при двух точках: `graphify path "A" "B"`
3. **Доменный скил** — по таблице `fst-skill-router` открой **один** нужный (payroll / warehouse / architecture / deploy…).
4. **Бриф** — выведи блок ниже **до** первого Edit/Write.
5. **Правка** — только файлы из брифа (+ необходимые i18n). После кода: `graphify update .` (фон).

## Формат брифа (обязателен)

```text
CHAIN BRIEF
topic: …
nodes: [символы / файлы из graphify]
path: A → … → B   (или «нет path»)
store/sync: local | Firestore shard | push/API | n/a
risks: [Firebase wipe? merge? ring-buffer? web-only?]
touch: [список файлов 1–8]
verify: [как проверить на проде / в UI]
→ proceed | ask user
```

Не раздувай: максимум ~15 строк брифа + потом код.

## Жёсткие правила Otgruzka

- Данные Firestore **не** затирать (нет clear/import/заливка локального JSON).
- Деплой только по просьбе; канон URL = Vercel.
- i18n RU+KA синхронно.
- Политика окон (`useWindowChrome`) не ломать backdrop’ами `inset-0`.

## Связка с graphify.mdc

Правило graphify остаётся в силе. Этот скил **усиливает** его: не только query, а явный бриф перед правкой + запись в `.cursor/context/CHAIN_BRIEF.md` скриптом.

## Не делать

- Не читать весь `GRAPH_REPORT.md` без нужды
- Не запускать полный rewrite «чтобы стало понятнее»
- Не подменять этот агент догадками из памяти чата без graphify
