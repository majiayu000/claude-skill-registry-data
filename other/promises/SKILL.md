---
name: promises
description: "Track and collect promises: every promise, theirs to us and ours to them, goes into a registry with date and source, gets a reminder when due and is closed with evidence. Triggers: /promises, log this promise, who promised us what, what did we promise, overdue promises, promise tracker."
license: MIT
version: 1.0.0
---

# /promises — коллектить обещания: фиксировать, контролировать, доводить

> Приказ Антона 02.08.2026: «важно КОЛЛЕКТИТЬ ОБЕЩАНИЯ!!! собирать их. фиксировать!!»
> Незаписанное обещание = вежливость. Записанное с датой = актив.
> Канон: Библия `reglament-kollekti-obeshchaniya-vsegda` + блок Promised протокола ФА
> ([[protocol-followup-structure]]).

## Режим A — CAPTURE (обещание прозвучало → фиксация сразу)
Источники: комменты (FB/TG/GitHub) · звонки (блок Promised из ФА) · личка (/triage) ·
планёрки/транскрипты.
Фиксация = задача в реестре `$OBSIDIAN_VAULT/10-Tasks/task-ГГГГ-ММ-ДД-promise-<слаг>.md`
по шаблону `_Task-Template.md`, обязательные поля:
- `owner:` кто обещал (их обещание = их имя; наше = anton/mycroft);
- `review_after:` дата напоминания (дефолт: их обещание +3 дня, наше +1 день);
- тег `promise` + в теле ссылка на ИСТОЧНИК (пост/тред/транскрипт).
Fail-closed: пункт без источника = 🤔 не подтверждено, в реестр не идёт.

## Режим B — COLLECTION (свод и контроль)

⭐ **Обещания со звонков живут в базе, а не только в задачах** (20.09.2026): дистиллятор
вынимает их из каждого транскрипта, `meetings_to_crm.py` раскладывает по лидам, а
`call_close.py` размечает сторону. Замер на 20.09: **887 обещаний, 289 наших и 598 их.**

```bash
python "$IMPORTS_ROOT/calls/call_close.py" --overdue             # ПРОСРОЧЕНО (начинать отсюда)
python "$IMPORTS_ROOT/calls/call_close.py" --overdue --mine      # наш просроченный долг
python "$IMPORTS_ROOT/calls/call_close.py" --promises --mine     # весь НАШ долг (репутация)
python "$IMPORTS_ROOT/calls/call_close.py" --promises --theirs   # их долг (коллекшн)
python "$IMPORTS_ROOT/calls/call_close.py" --promise-done <id> --evidence "<факт>"
```

⚠️ **Срок у 82% обещаний не назван человеком**, поэтому `due_date` считается от **даты
звонка** плюс дефолт (`наше +1 день`, `их +3 дня`); короткие маркеры («завтра», «in a
week») уточняют. Это признак «пора смотреть», а не юридический дедлайн: на 21.09 так
набралось **301 просрочка за 90 дней, из них 132 наши**.

⚠️ Сторона выводится из текста `owner`, который писала LLM — это **medium-признак, не
факт**: перед напоминанием человеку глазами сверить с цитатой из `--pack`.

Проход по обещаниям-задачам в волте (они остаются вторым домом):
```bash
grep -rl "promise" "$OBSIDIAN_VAULT/10-Tasks" --include="task-*.md" -i
```
Для каждого: чьё · просрочено ли · один следующий ход.
- **Их просрочено** → одно вежливое напоминание в исходном канале (тон по каналу);
  второй бамп ⛔ — правило трёх дней ([[sent-in-ledger-does-not-mean-[человек]-is-theirs]]).
- **Наше просрочено** → закрыть немедленно или честно передоговориться; молчание
  запрещено (репутация капера).
- Закрытие = `state: done` + evidence (ссылка/факт). «Вроде сделал» не закрывает.
Свод >3 позиций → дашборд по [[prefer-visual-dashboards]].

## Границы
- Напоминание в чужой канал = исходящее: тёплый тред класс C (сам), холодное/деньги — «+».
- Обещания с деньгами/юр.обязательствами = Tier-2, только фиксация + эскалация Антону.
- Не дублировать соседние реестры (DR-реестр, declined) — ссылаться.

## Связано
`/comment-to-call` (шаг 5 — обещания из воронки) · `/fa` (Promised после звонка) ·
`/triage` (обещания из лички) · Библия `reglament-kollekti-obeshchaniya-vsegda`.



<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
