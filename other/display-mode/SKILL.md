---
name: display-mode
description: "Change a Mac's main display resolution in one command: real pixels instead of 4K HiDPI so remote desktop (AnyDesk), screen recording and Screenpipe stop lagging. Use when a remote session is slow or a lower or original resolution is needed: lists modes, picks by width, height, pixel width and refresh rate, self-tests five known traps, verifies after the change and prints a one-line rollback. Triggers: /display-mode, lower the resolution, set 1920x1080, AnyDesk is slow, restore resolution."
license: MIT
version: 1.1.0
---

# /display-mode: разрешение экрана Мака

Утилита: `display_mode.c` рядом с этим файлом (CoreGraphics, 0 LLM, без brew). Описание флагов и обе ловушки записаны в шапке исходника.

**Портируемость.** Родился на Intel Mac Pro (macOS 15, 4K monitor), там проверен. Apple Silicon: тот же API, должен собраться, не проверялся. Windows: веток нет, сделай `ChangeDisplaySettingsEx` через PowerShell `Add-Type`. Linux: `xrandr --output <имя> --mode 1920x1080`.

## Шаг 1. Собрать (один раз на узел)
```bash
mkdir -p ~/.claude/scripts/bin && clang -O2 -framework ApplicationServices -o ~/.claude/scripts/bin/display_mode ~/.claude/skills/display-mode/display_mode.c && ~/.claude/scripts/bin/display_mode --selftest
```
`SELFTEST OK` обязателен. Swift не бери: на том Mac Pro он не совпадает с SDK и падает.

## Шаг 2. Посмотреть режимы
```bash
~/.claude/scripts/bin/display_mode
```
Колонки `W H PW PH HZ`, звёздочка = текущий. W H = как выглядит интерфейс. PW = 2×W значит чёткий HiDPI (тяжело для удалёнки). PW = W значит настоящее разрешение, видеокарте и AnyDesk в 4 раза легче.

## Шаг 3. Выбрать и поставить
Всегда все четыре числа, сперва `pick` (экран не трогает), потом `set`:
```bash
~/.claude/scripts/bin/display_mode pick 1600 900 1600 60
~/.claude/scripts/bin/display_mode set 1600 900 1600 60
```
`set` печатает строку отката ДО смены, пишет режим навсегда, перечитывает экран до 2 секунд и печатает `OK` или `MISMATCH`. Коды выхода: 0 = ок · 1 = нет режима / ошибка CoreGraphics / не встал · 2 = мусор в аргументах (`60Hz`, `abc`) · 3 = неоднозначно (две строки одинаково близки, смотри список). HZ пиши как в списке: `60`, `59.875`; берётся ближайшая частота, а не первая. Строку отката отдай оператору.

«Уменьши ещё» = следующая ступень вниз в том же формате, что сейчас (16:9 → 16:9). 4:3 (1600×1200, 1280×960) на широком мониторе растягивает картинку, бери только по прямой просьбе.

Лесенка 16:9 на 4K-мониторе: 1920×1080 → 1600×900 → 1344×756 → 1280×720 → 1024×576.

## Шаг 4. Доказать вторым способом
```bash
system_profiler SPDisplaysDataType | grep -E 'Resolution|UI Looks'
screencapture -x "$TMPDIR/s.png" && sips -g pixelWidth -g pixelHeight "$TMPDIR/s.png"
```
Оба обязаны показать выбранный размер.

## Ловушки (первые две пойманы вживую, остальные нашла панель внешних моделей)
1. Выбор по `ioDisplayModeID`: у «1920×1080 настоящий» и «960×540 HiDPI» один ID, ставится огромный интерфейс.
2. Выбор без высоты: при ширине 1600 первым находится 1600×1200 (4:3), картинка растянута.
3. Округление частоты: на 4K-мониторе у 1280×720 HiDPI есть 59.875 и 60, и 59.875 стоит в списке первым; округлённый выбор на «60» ставил 59.875.
4. Два режима с одной четвёркой и разной высотой в пикселях: выбор отказывает (exit 3), а не берёт первый.
5. Мусор в числах раньше молча становился 60 или 0.

Все пять сидят в `--selftest`. Если убрать из выбора высоту, PW или проверку неоднозначности, самотест краснеет.

## Чего не умеет
Только главный экран. Перезагрузку не проверяли: режим ставится как постоянный (`kCGConfigurePermanently`), а переживёт ли он перезапуск, не доказано.

<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
