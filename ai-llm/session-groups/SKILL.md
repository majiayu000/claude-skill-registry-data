---
name: session-groups
description: "Пометить КАЖДУЮ сессию Claude Desktop (Code tab) ИКОНКОЙ её группы прямо в заголовке — «⚙️ Имя», «💰 Р+ Имя». Пока сайдбар-инструмент ccd_sidebar заперт серверным флагом (anthropics/claude-code#92621), иконка в имени = единственная видимая группировка. Триггеры \"/session-groups\", \"/sg\", \"проставь группы сессиям\", \"разложи сессии по группам\", \"иконки сессий\", \"группы в заголовки\", а также САМ на СТАРТЕ сессии, как только ясна тема (приказ Антона 10.09.2026: «мало пикселей на экране, нужна иконка»), и на /retro шаг 6a-кватер как перепроверка. Движок session_groups.py (0 LLM) строит план, переименовывает сессия через MCP set_session_title. НЕ путать с /sessions (что сейчас крутится) и /retro (закрытие)."
version: 2.0.0
---

# /session-groups — иконка группы на каждой сессии

> Построено для флота Антона 08.09.2026, иконки с 10.09.2026. Корень: рычаг `ccd_sidebar.move_sessions` в приложении есть, но заперт флагом `[id]` (его нет в `/api/desktop/features`, замер 323 фичи). Проверка «включили?»: `python $USERPROFILE/.claude/scripts/claude_desktop_gate_probe.py` → exit 0 = ON → переносить через MCP move_sessions, а не иконкой.

## Иконки — ФИНАЛЬНЫЙ алфавит
| иконка | группа | что сюда |
|---|---|---|
| 💰 | $$$ | деньги, оффер, продажи, вакансии, витрины, статьи наружу |
| 🧠 | 2мозг | волт, RAG, память, голос, клон |
| ✍️ | content | посты, соцсети, Майкрофт |
| 🎯 | Лиды-CRM | лиды, аутрич, CRM, люди |
| ⚙️ | Инфра | скрипты, рутины, флот, синк, канон, браузеры, пульт |
| 🔬 | ДРы | Deep Research |
| 🏠 | личное | быт, здоровье, документы |
| 📥 | SINK | инбокс, шина, посылки, deploy |
| ❓ | не понял | Антон разносит сам |

Живой список: `python $USERPROFILE/.claude/scripts/session_groups.py groups`. Новые иконки НЕ заводить.

## Когда ставится (решено 10.09.2026)
**На СТАРТЕ**, как только тема ясна — обычно после первого содержательного сообщения. Антон смотрит в список весь день, а не в конце: ждать ретро = держать его без карты часами. `/retro` шаг 6a-кватер только ПЕРЕПРОВЕРЯЕТ (тема сессии могла уехать) и меняет иконку, если уехала.

## Шаги
1. **Своя сессия, первым делом:** `get_session self` → заголовок начинается с иконки из таблицы? Нет → `set_session_title(self, "<иконка> <имя>")`. Веха `Р+` живёт ПОСЛЕ иконки: `⚙️ Р+ Имя`.
2. **Чужие, план 0 LLM:** `python $USERPROFILE/.claude/scripts/session_groups.py plan --limit 60` → JSON `{sid,title,group,new_title}`, `new_title` уже собран движком. `group:"?"` = по словам не понять → ясно по смыслу, выбери сам; НЕ ясно → оставь `❓` (anton 09.09: «пишешь туда вопросики, и я буду сам разносить»). Гадать запрещено.
3. Переименуй каждую: `mcp__ccd_session_mgmt__set_session_title(session_id=sid, title=new_title)`. Пачками по 20 в одном ходу. «Session not found» при живом файле = чужой scope, пропускай молча.
4. **Миграция старых словесных тегов:** `session_groups.py retag --limit 100 --all` → `[Инфра] Имя` превращается в `⚙️ Имя`. Прогонять, пока не выдаст пусто.
5. Витрина для правки Антона (запрос «разложи 300-500»): `session_groups.py table --limit 500` → Google-таблица через `sheets.py` (вкладки `sessions` + `groups`, колонка «ПРАВКА Антона»).
6. Отчёт одной строкой: «🗂 иконки: N проставлено · K ❓ на разбор Антону · флаг ccd_sidebar OFF/ON».

## Границы
- Регресс движка: `python $USERPROFILE/.claude/scripts/_test_session_groups.py` (17 кейсов, 0 сети). Правил движок → прогони.
- Без MCP `ccd_session_mgmt` (headless `claude -p`) только план, в отчёт строка «переименование недоступно».
- Правка `claude_desktop_config.json` руками ⛔: приложение файл живьём не перечитывает и перепишет из памяти.
- Мусор Антона в начале имени («!!!», «+++») — его приоритет-сигнал, не срезать: иконка встаёт после него.
- Канон: память `session-group-at-retro`; дверь в /retro 6a-кватер; публичная копия — репозиторий tonydzi/clawrush.

<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
