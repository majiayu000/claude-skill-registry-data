---
name: navkit-terminal
description: The tty layer (navkit/terminal.py, capabilities.py, clipboard.py) -- raw mode, the alternate screen, mouse and bracketed paste, InputParser and escape timeouts, the kitty keyboard protocol and held modifiers, keypad and Ctrl+H/Backspace decoding, TerminalInfo detection and NAVKIT_* overrides, OSC 8 hyperlinks, the OSC 52 clipboard, asking which graphics protocol it speaks (kitty/sixel, NAVKIT_GRAPHICS, cell_px), and tools/keyprobe.py. Use when a key arrives wrong, a terminal behaves differently, or adding a terminal feature.
---

# The terminal layer

- `Terminal` owns the tty (raw mode, alternate screen, mouse tracking, bracketed paste, autowrap off, application keypad)
  and restores it in `Application`'s `finally`. `InputParser` is fed incrementally and keeps undecodable tails. **A lone
  `ESC` is ambiguous**: the parser reports `pending_escape` and the application resolves it with `ESCAPE_TIMEOUT`.
- `TerminalInfo` (`capabilities.py`) is what the terminal supports (`colors`, `alt_screen`, `mouse`, `bracketed_paste`,
  `title`, `keypad`, `hyperlinks`, `glyphs`, `palette`, `bidi` -- `NAVKIT_BIDI`, the `navkit-bidi` skill; `Terminal`
  sends `CSI 8 l` so VTE reorders nothing while Navigator owns the screen). Detection is conservative -- sixteen colours unless `COLORTERM`
  says otherwise; `NAVKIT_COLORS` (`truecolor`, `256`, `16`, `8`, `mono`, a number) overrides and outranks `NO_COLOR`.
  Colour/palette/glyph decisions are the `colours-themes-glyphs` skill.
- **A frame must never be lost.** `Terminal.flush()` encodes the frame itself and writes bytes to `stdout.buffer`,
  every lone surrogate (a non-UTF-8 file name byte, `surrogateescape`) as U+FFFD -- one cell, as `char_width`
  measured it. Written as text, a strict UTF-8 stdout (any `xx_XX.UTF-8` locale; C.UTF-8 is `surrogateescape`, so a
  test under it hides this) raised `UnicodeEncodeError`, a `ValueError` the flush swallowed: the frame vanished while
  the back buffer took it as painted, and later diffs drew over a stale screen. Test pty runs under a real locale.
- **Lending the terminal out.** `Terminal.suspend()`/`resume()` drop and restore the screen modes (alternate screen,
  mouse, paste, kitty flags, keypad, autowrap) but **keep raw mode**. `stop()` after a suspend restores termios only.
  `Terminal.write_bytes()` writes a relayed program's bytes unchanged.
  - `Application.release_terminal(on_input)` suspends, stops painting (`_render` returns early) and hands every raw
    byte read to `on_input`. Whatever `on_input` returns goes to the parser, as the bytes after the reclaiming key.
  - `reclaim_terminal()` resumes and forces a full repaint (`_front = None`).
  - The loop keeps running meanwhile: timers, pty output, resizes.
  - Navigator uses this for mc's Ctrl+O (`console-command-line`).

## A terminal that is not UTF-8 (a departure, asked for)

`TerminalInfo.charset` is the Python codec the terminal reads and sends: the codeset after the `.` of `LC_ALL` >
`LC_CTYPE` > `LANG` (`_charset`), `NAVKIT_CHARSET` (Navigator's `--charset`, set before `detect()`) over it. A
locale naming none (`C`, `POSIX`, `ru_RU`) says nothing and keeps UTF-8 as before -- `LANG=C` over ssh on a UTF-8
terminal is the common case; a stateful one (ISO-2022-JP, UTF-7, `charset_named` refuses it) is `ascii`.
- **Everything above the tty stays Unicode**; only the boundary converts. `Terminal.flush` writes
  `encode_for(data, charset)`: UTF-8 as before, anything else with the `navkit-cell` error handler, which writes a
  character the charset has not as `glyphs.ascii_twin` -- its ASCII-tier twin from the vocabularies (`▲`->`^`,
  `═`->`-`), a few common symbols, the letter without its accent, else `?` -- **as many cells as it takes** (`日`
  -> `??`), so no column moves. `write_bytes` (a relayed program) stays raw: the child speaks the charset already.
- **The tier follows what the charset can draw**: a legacy charset with both single and double frames (KOI8-R/U,
  CP866, CP437, CP850) gets `GLYPHS_UNICODE` -- a tee it lacks falls back alone -- one without (CP1251, ISO-8859-x,
  EUC-JP) `GLYPHS_ASCII`; never Nerd, and no braille spinner.
- **Input**: `InputParser.charset` (the application sets it from the info, and again in `use_terminal_info`) sends
  each byte past ASCII through the charset's incremental decoder, which holds a multi-byte character's first bytes
  (EUC-JP, GBK); Alt+char takes one byte; a paste is decoded whole. Escapes, kitty keys (code points) and mouse are
  charset-free.
- **The console**: `navkit.console.CHARSET` (the application sets it -- a console screen is made before there is an
  application to ask, and every child inherits the same locale); `_Stream` replaces pyte's `utf8_decoder` with the
  charset's; `encode_key(..., charset=)` types at the child in it (`ScreenView.send` passes `screen.charset`).
- **Stays UTF-8 by its protocol**: OSC 52, OSC 8, kitty graphics, the notifications.
- `luit` remains the zero-code alternative where installed; the Linux console in non-UTF-8 mode (`unicode_stop`,
  a CP866 font) has no such option, which is why this is done here. Tests: `tests/test_charset.py`.

## Keys

- **The kitty keyboard protocol** is pushed without asking; `NAVKIT_KEYBOARD=legacy` turns it off. Only it reports a
  held modifier (`Application.modifiers`, which the key bar reads).
- **xterm's modifyOtherKeys** (`MODIFY_KEYS_ON`, `CSI > 4 ; 1 m`, `TerminalInfo.modify_other_keys`) is asked for
  beside it, before the push, and reset by `CSI > 4 m`. It is for **tmux**, which ignores the kitty push and sends
  Ctrl+Enter, Ctrl+Shift+letter or Ctrl+digit only to a program that asks this way (and only with tmux's
  `extended-keys on`); xterm itself answers it too. Both forms are decoded: `CSI 27 ; mod ; code ~`, and
  `CSI code ; mod u` (xterm's formatOtherKeys, tmux's `extended-keys-format csi-u`), whose capital letter under Ctrl
  is folded to the lower-case key with Shift. **That `u` form is kitty's spelling but reports no release**, so a
  `CSI u` key moves `modifiers` and sets `KeyEvent.releases` only once `InputParser.reports_releases` is set: a bare
  modifier key or an event type has arrived, which only kitty proper (flags 2/8) sends. Before that a kitty
  terminal's first press promises no release, and Button's Space flashes once instead of waiting for the release.
  `NAVKIT_KEYBOARD=legacy` turns both requests off.
- **Another layout's letters** (Hebrew, Arabic) under Ctrl/Alt/Super carry `KeyEvent.base`, the US key in the same
  place: kitty's base layout key (the third `:` field of the key code, asked for by flag 4), else
  `navkit/keyboard.py`'s SI-1452 and Arabic (101) position table (a legacy terminal's `ESC ס`; VTE already sends Ctrl
  as the Latin control byte). Not compared, and `matches()`/key tables see only `name`. **The application offers
  the key as typed first, all the way** (chord, its table, `on_key`, the focus path: `Application._deliver_key`),
  and only a key nothing took is offered again as `event.as_base()` -- so a translated menu's Alt+ק opens its menu
  though Manager binds Alt+E, and Alt+ס, which nothing claims, still quits. (Looking the base up in each table in
  turn let a nearer Alt+E binding beat the menu bar, which is reached last.) A bare letter gets no base: it is
  text. `MenuBar.hotkey` also takes the Latin key in a non-Latin hotkey's place, for a US layout, and its tooltip
  names both (Alt-ק, Alt-E).
- **Super** is `KeyEvent.super_` (named `super+…` after ctrl, alt, shift; never printable), read only from a kitty-form
  key -- legacy xterm spends that modifier bit on Meta. Before it was read, Super+1 arrived as a typed `1`.
- **Ctrl+H vs Backspace**: a legacy terminal sends Ctrl+H as 0x08, which navkit reads as Ctrl+H only once the tty's
  erase character (`Terminal.erase`, termios `VERASE`, read before raw mode) says Backspace is 0x7F, and as Backspace
  otherwise (`InputParser.ctrl_h`).
- **0x0A is Ctrl+J, 0x0D Enter**: in raw mode (ICRNL off) Enter sends CR, so a legacy terminal's LF can only be
  Ctrl+J -- the key macros' chord prefix (`navigator-macros`). A pasted line break comes inside bracketed paste,
  and `encode_key` sends Ctrl+J to a child as 0x0A again.
- Keypad operators are named `kp_plus`/`kp_minus`/`kp_multiply`/`kp_divide` (`char` kept), from kitty codes or from
  `SS3` under application keypad mode. xfce4-terminal (VTE) and PyCharm send Gray `+` as a bare `+` even then (named
  `plus`); only Ghostty told them apart, which is why Navigator binds the plain keys too.
- **With Num Lock on, a keypad operator's Ctrl is lost or moved.** VTE (xfce4-terminal) drops it: Ctrl+Gray `*` is a
  bare `*`, byte for byte the plain key's, so nothing can bind it -- with Num Lock off it is `ESC O 5 j`
  (`ctrl+kp_multiply`). Ghostty keeps it but may send the plain character's code (`CSI 42;5u`, `ctrl+*`), so bind
  `ctrl+<char>` beside `ctrl+kp_*` (Navigator's Ctrl+Gray `*` does). VTE's checked with keyprobe; Ghostty's inferred
  from binding `ctrl+*` making it work.
- A terminal without the kitty protocol sends Ctrl+Enter as Enter; Ghostty keeps Ctrl+Enter and Ctrl+Shift+Enter
  unless unbound (`keybind = ctrl+enter=unbind`). xfce4-terminal eats Alt+E/F/V/T/B/H unless menu access keys are off.
- **Find out what a terminal sends**: `./venv/bin/python tools/keyprobe.py [--legacy] [--no-mouse]` (`q` twice or
  Ctrl+C quits) -- e.g. whether Ctrl+Shift+V arrives as a paste or a key.
- **`Application.bell()`** rings BEL now: `Terminal.bell()` queues it and the application flushes at once, since an
  unchanged frame writes (and flushes) nothing. A terminal without `bell` (a test's) is skipped; `FakeTerminal.bells`
  counts them.

## Hyperlinks (OSC 8)

`Style.link` is a per-cell URL that `render_diff` opens and closes as it switches cells, exactly as it switches SGR;
it is not in `STYLE_FIELDS`, so no sheet can declare one. `TerminalInfo.hyperlinks` gates it -- on for any interactive
terminal but `TERM=linux` (whose console prints OSC 8's tail) -- and `NAVKIT_HYPERLINKS=on|off` overrides. Ghostty opens
them with Ctrl+Shift+click.

## Cursor colour (OSC 12)

DECSCUSR has shapes and no thickness, so a thin bar is made findable by colour. The application sends the caret
widget's `Widget::caret` `fg` (`Widget.caret_color()`) as `OSC 12 ; rgb:rr/gg/bb` before showing the cursor, only when
it changes, and `OSC 112` when a caret loses its colour. `TerminalInfo.rgb()` turns the colour into the triple the
sequence needs: an index below 16 counts only with a pinned palette (`--palette terminal` sends none, as only the
terminal's theme knows its yellow). `Terminal.cursor_colored` records that one was sent, so `stop()`/`suspend()` reset
it then and only then: OSC 112 would also undo a colour the user's shell set. `TerminalInfo.cursor_color` gates it --
off on `TERM=linux`, whose console would print it -- and `NAVKIT_CURSOR_COLOR=on|off` overrides.

## Clipboard

`navkit/clipboard.py`: OSC 52 plus `wl-copy`/`xclip`/`xsel`; a requested paste arrives as a `PasteEvent`. A paste
walks the focus path when `Application.on_paste` declines it. `Application.system_clipboard` false makes the clipboard
(and primary selection) private to the application: `copy_to_clipboard` keeps the text and sends nothing out,
`request_clipboard` posts it back as a `PasteEvent`. The private copy is kept either way, so switching off still has
the last copy. A paste the terminal makes on its own is the desktop's regardless.

**No tool and no OSC 52 answer falls back to the private copy.** With the system clipboard on, `_read_clipboard`
queries the terminal and waits `CLIPBOARD_ANSWER_TIMEOUT` (0.5 s); VTE and JediTerm never answer, so after it the
private copy is pasted (`PasteEvent(origin="private")`) and `Application.clipboard_unavailable()` is called once a run,
after that paste is dispatched (Navigator shows a box suggesting xclip/xsel/wl-clipboard). `PasteEvent.origin` is
`"terminal"` (bracketed paste), `"answer"` (the parser's OSC 52 reply) or `"private"`; an `"answer"` arriving with no
query pending is dropped, so a late one cannot paste a second time. Ghostty's `clipboard-read = ask` prompt is usually
slower than the timeout -- `allow` gives the real answer.

## Focus reports and desktop notifications

**Focus reports are their own mode.** `FOCUS_ON`/`FOCUS_OFF` (`CSI ? 1004 h/l`) go out when
`TerminalInfo.focus_reports` -- any interactive terminal but `TERM=linux`; `NAVKIT_FOCUS=on|off` -- independent of the
kitty push. The parser turns `CSI I`/`CSI O` into `FocusEvent(True/False)` (focus-out still releases held modifiers
first); `Application._handle` keeps it as the reactive `terminal_focused` and offers it to no widget. It is `None`
until the first report and again after `release_terminal`/`reclaim_terminal`: **unknown is not unfocused** -- a
terminal that never reports (tmux without `focus-events on`) is never treated as one in the background.

**`Application.notify(title, body, method=None, *, app_name=)`** (`navkit/notify.py`) sends whatever the focus; the
caller checks `terminal_focused`. Ways (`TerminalInfo.notifications`, `NAVKIT_NOTIFY`): `osc9` (`ESC ] 9 ; title:
body BEL` -- kitty, Ghostty, WezTerm, iTerm2, Windows Terminal, ConEmu), `osc777` (`ESC ] 777 ; notify ; title ;
body BEL` -- foot, urxvt), `notify-send` (fallback only with `DISPLAY`/`WAYLAND_DISPLAY`, no `SSH_CONNECTION`/`SSH_TTY`
and the program on `PATH`; VTE's terminals land here, showing neither OSC unpatched), `none`. `notify_osc` strips
control characters, keeps `;` out of OSC 777's title, caps at `NOTIFY_MAX`, puts a zero-width space before a leading
digit (`OSC 9 ; 4 ;` is ConEmu's progress) and wraps the sequence in tmux's (`allow-passthrough on` needed) or
screen's `DCS`. `Terminal.notify` writes nothing while suspended or not started. `notify-send` is an
`asyncio.create_subprocess_exec` task, reaped on the loop, a failure swallowed. `FakeTerminal.notifications` records
`(title, body, kind)`.

## Graphics: which protocol, asked once

- **The one thing navkit asks the terminal.** `TerminalInfo.graphics` (`"kitty"`, `"sixel"`, `""`) cannot be read
  off the environment, so `detect()` sets `probe_graphics` instead: on an interactive terminal, not `TERM=linux`, not
  inside tmux/screen (neither passes the protocols on unasked), `NAVKIT_GRAPHICS` unset. `NAVKIT_GRAPHICS=kitty|sixel|none`
  (Navigator's `--graphics`) states it and nothing is asked.
- `Application._ask_graphics` (after `start()`, before `on_start`) writes `GRAPHICS_QUERY`: a one-pixel kitty query
  under id 31 (`GRAPHICS_QUERY_ID`), `CSI 16 t` (cell size), then DA1 -- which every terminal answers, so its reply
  ends the asking. The parser turns the replies into `TerminalReplyEvent` (`graphics`, `cell`, `da1`), which
  `_on_readable` keeps from the event queue (`_terminal_replied`). kitty `OK` wins, else DA1 attribute 4 is sixel;
  `_graphics_answered` sets it on `terminal.info` and, only if `graphics`/`cell_px` changed, bumps `info_revision` and
  invalidates -- never `use_terminal_info`, whose whole-screen repaint ~1 s after the first frame made startup look
  slow (no cell depends on the answer). Nothing answers in `GRAPHICS_ANSWER_TIMEOUT` (1 s): no pictures.
- **`ESC _` is also Alt+_.** A whole `ESC _ G ... ESC \` is always a reply (a late one is never typed); an unfinished
  one is waited for only while `InputParser.answers_graphics` is set, and a lone `ESC _` then flushes as Alt+_. DA1
  (`CSI ? ... c`) and `CSI 6 ; h ; w t` never were keys.
- **`cell_px`**, a cell's pixels, is `TIOCGWINSZ`'s pixel fields (`Terminal.cell_px`) first -- refreshed on SIGWINCH,
  a font size change -- else `CSI 16 t`'s answer. Unknown, a picture takes a cell as twice as tall as wide.
- What is drawn, and when, is `navkit/graphics.py` (`navkit-widgets-input`, *Pictures*).

## Window title

`Terminal.set_title()` writes OSC 0, and the first one of a run pushes the terminal's own title first (`TITLE_PUSH`,
xterm's `CSI 22;0 t`); `stop()` pops it (`TITLE_POP`), so the shell's title (an ssh session's `user@host /dir`) comes
back on exit. The title cannot be read instead -- `CSI 21 t` is refused nearly everywhere. Repeating the title last sent
writes nothing. `Application.title` is a property: assigned while running, it is written and flushed at once, since a
frame flushes only when a cell changed. Navigator's title is `navigator/lib/system/title.py`'s `user@host ~/dir —
Navigator`, kept on the prompt's directory by `Shell._name_window` (an effect, beside `_follow_panel`).

## Manual checks

For what a fake terminal cannot cover (raw mode, real escapes, `SIGWINCH`), run `python -m navigator` on a pty:
`pty.fork`, `TIOCSWINSZ`, write key bytes to the master fd, read back what it paints. PyCharm's terminal (JediTerm)
repaints unevenly -- check a native terminal before blaming the loop.

## Read when

| Reference | Read when |
|---|---|
| `reference/held-modifier.md` | the kitty protocol and held modifiers |
| `reference/clipboard.md` | OSC 52 and the clipboard tools |
