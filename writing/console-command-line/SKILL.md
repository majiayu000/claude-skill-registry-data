---
name: console-command-line
description: The console and the command line -- navkit/console.py (pyte, ConsoleScreen, alternate screen, query answers), navkit/process.py (PtyProcess), navigator/lib/system/subshell.py (persistent $SHELL, OSC 6973 marks, silent cd, held-back prompt, completion, history, atuin), the Console widget and Ctrl+O, the CommandLine (TCommandLine), Tab completion and CompletionList, running a program with every key, executing a file, Ctrl+Enter insert name, console selection. Use when touching anything that runs a command or shows its output.
---

# The console and the command line

## Owning the screen

**A terminal will not give its cells back** -- no escape returns screen contents -- so the only way to show a program's
output behind the panels, as DOS did from video memory, is to have received it. `navkit/console.py`: `ConsoleScreen`
keeps a `ScreenBuffer` mirror in step with pyte's sparse grid, converting only dirty rows; `capture_host` grabs the
pre-start screen from tmux, kitty or `/dev/vcsa` and usually fails, which is expected. `pyte` is the one run-time
dependency and it is load-bearing.

- **The copy is taken on a thread** (`capture_host`, from `Console.start_seeded`, which `Navigator.on_start` calls). The
  shell starts once it returns, so its rc output lands below the copy. `Console.start()`/`run()` meanwhile start the
  shell at once and drop the copy: callers rely on `start()` leaving a running shell.
- **kitty is asked only over its socket** (`KITTY_LISTEN_ON`). Without one, `kitty @` talks through the tty, which
  races Navigator's input reader. And where `KITTY_WINDOW_ID` was merely inherited (a terminal or an IDE started from a
  kitty shell), it waited out its 2-second timeout on the loop: the first frame came at 2.3 s instead of 0.27 s.

- `_Screen` adds what pyte lacks: the **alternate screen** (47/1047/1049), **answers to queries**
  (`ConsoleScreen.respond`: cursor position, device attributes), dropping a private CSI pyte would crash on (`mc`'s
  `CSI ? Pm r`) or misread (`CSI > 4;2 m`), and a parser rebuilt if pyte raises anyway (its parser is a generator one
  exception closes for good).
- `navkit/process.py`'s `PtyProcess` runs a child on a pty via `loop.add_reader`, sized with `TIOCSWINSZ` on the master
  (the kernel signals the child). **`write` loses no byte**: what the non-blocking pty will not take yet (a paste or a
  macro to a busy child) waits in `_pending`, in order, flushed by `loop.add_writer`; a child gone drops it. A program that needs the real terminal goes through the relay (below), never a
  blocking call with the terminal stopped.
- **A child is never given `LINES`/`COLUMNS`** (`PtyProcess.environment()` drops them, even if Navigator inherited
  them). ncurses lets them override the pty's size for good, so `htop` kept drawing for its starting size after
  every `SIGWINCH`. mc (S-Lang), top and btop ignore them, which is why only htop showed it. The size is the pty's
  (`TIOCSWINSZ`) and nothing else.
- **What `_Screen` adds to pyte for `xterm-256color`'s terminfo**: `REP` (`CSI n b`, ncurses' run of one
  character), `SU`/`SD` (`CSI n S`/`CSI n T`; the private and many-parameter forms are other things and are
  dropped), dispatched by `_Stream`'s extended `csi` table. Also tab stops for the columns a wider screen gains
  (`_Screen.resize`): pyte set them once, and ncurses moves the cursor with tabs.
- **A console screen is not reactive**: `Console.revision` stands in; anything mutating it behind the widget must bump it.

## The Console widget and Ctrl+O

The `Console` covers the band between the bars behind the desktop. Ctrl+O hides the desktop (one reactive flag, one
`visible` binding); menu and key bars stay painted -- not mc's hand-over. **A departure from DN's Ctrl+O**, which put
up an *Output* window (`TUserWindow`, `DNUTIL.PAS:1659-1665`, `USERMENU.PAS:107-196`): a desktop window with its frame
off screen, listed in the window list, the other windows kept beneath it, and Ctrl+O closing it only when it was the
selected one. Here the console is a layer under the desktop, shown by putting the windows away -- the design, kept. `toggle_console` hands the console the
keyboard **in the same call that flips the flag, never from an effect** (an effect runs after the batch, so Ctrl+O and
the next key would be routed by a stale focus); hiding it re-activates the top window. `Console.can_focus` is set in
`__init__`. The console reports the child's cursor through `cursor_position()`. Scrollback (`ConsoleScreen.scroll`/`scroll_to_top`/`scroll_to_bottom`, pyte's paging with
`history.ratio` set per step): Shift+PgUp/PgDn half a page and Shift+Up/Down a line always (a busy full-screen program on the
alternate screen gets all four instead); idle only, PgUp/PgDn a page and Home/End to either end (Home/End only
with the command line empty, its table takes them first); the wheel `WHEEL_LINES` (3), declined over a busy alternate
screen. **The alternate screen is never scrolled** (`ConsoleScreen.scroll` returns there): it keeps no history
(`scroll_extent` is `(0, 0)`), and paging pyte's moved the program's display and dragged the shell's lines into it.
`Console.on_key` keeps the scrollback and sends the rest to the child.

- **An idle console takes no keys** (it holds them only while a command the line sent runs, `Console.busy`); typing
  reaches the command line.
- **While a program runs it gets every key, Ctrl+O included** (`Shell.program_has_keys`, consulted by `Shell.enables`
  and `Navigator.enables`, disables every command, so F10 reaches `htop`/`mc` and Ctrl+O is `mc`'s and `nano`'s). Arrows follow its DECCKM
  (`encode_key(..., application_cursor=)`, `SS3` vs `CSI`, xterm modifier parameter); its mouse reports go back down
  (`encode_mouse`, modes 9/1000/1002/1003, SGR 1006). Alt+X is `Quit(desktop=True)`, vetoed by `Navigator.enables`
  while a running command's console is over the windows.
- The console selects output with a drag or double click unless a program tracks the mouse (reversed, cleared by new
  output or a scroll); Ctrl+Ins copies it -- `Shell.on_key` asks the console before the command line. A double click
  takes the run of non-whitespace cells, a double-width character's second half (an empty cell) part of it, so either
  half finds the whole word.

### Without the internal terminal (mc's Ctrl+O)

System Setup's *Use internal terminal* (`SETTINGS.system.internal_terminal`, a departure from DN) is on by default.
With it off, Ctrl+O and *ESC for user screen* call `Shell.relay_terminal()` instead of showing the console:

- **What relaying does.** `Application.release_terminal` takes Navigator out of full-screen mode, and
  `Subshell.start_relay(terminal.write_bytes)` sends everything the console would show to the real terminal. That
  includes the prompt, shown once (`_relayed`: `prompt`/`typed`/`other`). The screen stops answering queries,
  because the real terminal does.
- **Keys and the pty.** Keys go raw through `Shell._relayed_input` to `Subshell.relay_input`. `Console.relayed` sizes
  the pty to the whole screen.
- **Ctrl+O takes the terminal back** (`0x0f`, or kitty's `CSI 111;5u`), unless a command the line sent is running:
  that command gets every key. `end_relay()` then clears an abandoned typed line with Ctrl+E Ctrl+U, and the panel
  follows a `cd`.
- **A line entered at the relayed shell** clears `_ready` until its next prompt, so nothing is typed into a program
  the user started there.
- **A command from the line runs relayed** and comes back when it finishes (`_relayed_for_command`).
- **The shell exiting ends the relay** (`Subshell.on_exit`).
- **No real tty** (headless, tests): it falls back to the console.

## The subshell

**Commands run in one persistent `$SHELL`** (`Subshell`, owned by the `Console`): bash and zsh load the user's rc then a
hook; anything else runs bash or `sh`. The hook prints private OSC marks (`ESC ] 6973;<nonce>;A|B|D` ...) for prompt
position, command finished, and `$PWD`; other marks: `C` (completion), `H` (history), `U` (atuin/fzf keys, where fzf and zoxide are), `R` (atuin's or fzf's
choice), `O` (reveal output).

- **The shell's own prompt is held back** and painted only when a command is sent, so the log reads `prompt$ cmd`, the shape DN's `/dir>cmd` echo had.
  The hook wraps the user's `PS1` between the A and B marks and adopts any `PS1` that differs from its wrapper with
  the marks stripped out, because what changed it may have built on the wrapper: a venv's `activate` prefixes
  `(venv) ` to it, `deactivate` puts an older wrapper back. The `sh` fallback has no hook, so its PS1 starts with
  `$(__nav_marks $?)`, which writes the D and A marks to stderr while the prompt is expanded, ahead of any literal
  prefix (dash and busybox ash expand command substitution in PS1).
- The panel's directory reaches the shell by a **silent `cd`** (leading space, output swallowed) only when they differ;
  `Subshell.sync` sends it whenever the active panel moves while idle. A `cd` typed on the line moves the active panel
  when the command finishes (`CommandFinished`, posted from the pty reader to `Navigator.on_command_finished`) --
  not a *Find:* listing, which keeps its place as DN's find drive did, and a remote panel only when the command
  `cd`'d (`Shell._follow_shell`; `navigator-drives`).
- While a command runs the console is up and holds the keys; afterwards the windows return (not when Ctrl+O had put the
  console up, which stays), and the panels re-read either way (`command_finished` always calls `_follow_shell`).
- `Navigator.on_start` starts the shell at once on a real tty (headless, the first command does).
- **Every child carries `NAVIGATOR=1`** (`navkit.process.MARKER`, set by `PtyProcess.environment()`), and `main()`
  refuses to start under it -- so `nav` typed inside Navigator says so and exits 1, while another terminal is
  unaffected (no lock file). `--help`, `--version` and `--list-themes` still work; `NAVIGATOR= nav` forces a nested copy.
- Queries are answered in order -- `Subshell._completions` is a queue (two keys in one read send two queries).
- **A root console** (Utilities > *Elevate root access*, `navigator-elevation`): `Console.go_root` swaps
  `console.subshell` for a `RootSubshell` on the same screen, with the same callbacks. The user's shell is parked as
  `console.user_subshell`, still running, and `go_user` brings it back as it was. While parked, what it prints is kept,
  not painted (`Subshell.park`/`unpark`, at most `_PARKED_LIMIT`, the oldest reads dropped first and counted in
  `parked_dropped`, which `go_user` says the size of before the replay), and replayed
  through `_on_output` after the *Back to your own shell* line, so its marks and prompt are read as they would have been. Everything reads
  `console.subshell` at call time, so nothing else needs to know. `RootSubshell.start` does nothing. Its two halves
  are `open` on a thread (the helper call) and `attach` on the loop (`navkit.process.AttachedPty` over the handed-over
  master: no `waitpid`; signals go to `console_stop` through the helper). `run()` therefore never restarts one that
  ended.
- **A mark can span many reads**: an `H` (history) or `C` (completion) answer is one base64 mark of up to a few
  hundred KB. `_on_output` carries an unended mark of ours (`_mark_start`) up to `_MARK_LIMIT`; anyone else's unended
  OSC is let go after 4K. With the old 4K cap for everything, a real-sized history was dropped and Up did nothing.

## The command line

DN's `TCommandLine` (`navigator/widgets/shell/command_line/`, a Python-only `InputLine`), one row above the key bar,
docked after `KeyBar` in `shell.nml`, in the hard-coded `$0F`/`$07`.

- **Its prompt is the user's own shell prompt**, colours and all -- a departure (`SetDirShape` drew `<dir>>`, which
  survives as the fallback `Shell.command_prompt` for `sh` and before the shell has printed a prompt in the active
  panel's directory; `Shell.command_prompt_cells` compares `Console.prompt_cwd`). The hook *brackets* whatever `PS1` the
  rc left; `prompt_cells()` decodes the held-back bytes on a one-row `ConsoleScreen`, so a multi-line prompt shows its
  last line.
- **The terminal's title follows the same directory** as `Shell.command_prompt` (`Shell._name_window`,
  `user@host ~/dir — Navigator`; `navkit-terminal` skill, *Window title*).
- **The prompt is blank while a command runs** (a departure): `Subshell.busy` is a property that calls `on_busy`,
  mirrored as the reactive `Console.running`, and `Shell.command_prompt`/`command_prompt_cells` are empty while it is
  set -- the prompt coming back is the sign the command finished, as in a terminal. The row stays (giving it to the
  console would resize the pty under the program). atuin's search, being `busy` too, also blanks it.
- **A program runs under the bars** (a departure): the console, and so the pty, is the band between the menu bar and
  the command line's row, the screen's height less three, with the menu bar, the blank command-line row and the key
  bar still painted (`shell.nml`). DN gave a program the whole screen, DN itself having exited (`RUNCMD.INC`);
  Navigator keeps running, so its bars stay, and a full-screen program fits the band it is told it has.
- **It never holds the keyboard**: a key the focused widget declines walks up to `Shell.on_key`, which types it there
  (DN's `ofPostProcess`); `Shell.cursor_position` puts the caret on the line.
- Enter, Home, End are `ExecuteCommandLine`/`CommandLineHome`/`CommandLineEnd` on the application's table, **disabled
  while the line is empty** so the key falls through to the panel. A widget whose `edits_text` is True (quick search,
  the editor) makes Enter/Home/End/Tab and pastes step aside. Esc clears, Ctrl+E/Ctrl+X walk `HISTORY["command"]`, a
  paste lands on it as pasted (line breaks joined by blanks) -- a departure: DN's Shift+Ins went through
  `cmInsertName`'s spacing, which here only Ctrl+Enter's name keeps. The mouse is navml's input line's (a click the
  caret, a drag a selection, a double click a word, a right click Cut/Copy/Paste) -- a departure: DN's double click
  opened Commands history, its right click stepped the caret by the half clicked, and its prompt ignored clicks. The
  text has every column after the prompt, the last included, as DN's (`CommandLine.room`); there's no length limit --
  a departure: DN's held 127 characters (`String[127]`).
- **The Timer line, Alt+/** (`ToggleTimerLine`, DN's `kbAltSlash`/`ltTimer`, `CMDLINE.PAS:155-166, 322-342`):
  `CommandLine.timer`, off at the start and kept for the session, wraps the prompt in `{ }` (`shown_prompt` /
  `shown_cells`, cut first so the braces show), and `run_command` stamps each command it hands the console; at
  `command_finished` an *Information* box says *Elapsed time: hh:mm:ss.cc* (`elapsed_text`, DN's `ShowTimeInfo`).
  In the application's key table, so refused while an editor has the keys (its Alt+/ is *CapWord*) or the line is
  hidden. DN's two OS/2 types are dropped, so cycling is a toggle; a command run in a window isn't timed; under
  *Auto-hide* an empty line stays hidden (DN's put a blank in to show it). The walk keeps what was being typed aside (`_draft`) and gives it back past the newest; an edit
  since the last step (DN's `StrModified`: the text no longer what the walk put there) makes the line the draft and
  starts again from the newest, a caret move does not. A departure: DN's `AddCommand` put that line into the history;
  here a line never run never enters it. **Ins with text on the line toggles overwrite** (`CommandLine.overwrite`, DN's `Overwrite`/`kbIns`,
  `CMDLINE.PAS:302, 389`): typing replaces the character at the caret (a paste and `insert_name` still insert), the
  mode lasting the session; the caret is a block when `overwrite` differs from *Block Insert Cursor* (`Shell.block_insert`,
  DN's `xor`). Ins is `ToggleMark(by_key=True)` in `Manager.keys`, stepping aside while the line holds text as the Gray
  keys do -- a departure: DN's panel always took Ins, and ^V toggled; Ctrl+V is paste here. **Ctrl+Left/Right stop at DN's
  `Separators`** (`kbCtrlLeft`/`kbCtrlRight`, `CMDLINE.PAS:393-414`): `CommandLine._breaks_word` is `_SEPARATORS`
  (`: . , / [ ] + > < | ;` and blank, less `\`, the shell's escape), over navml `InputLine`'s blank-only default. **Ctrl+Backspace**
  is DN's `#127` (`CommandLine._delete_word_left`, `CMDLINE.PAS:313-319`): the word before the caret, then the
  separators before it (Ctrl+Left's order reversed, as DN's), or a selection instead. On a terminal whose Backspace is
  `0x7F`, Ctrl+Backspace sends `0x08`, which is Ctrl+H (the panels' hidden files); the kitty protocol or
  `modifyOtherKeys` sends it as itself. **DN's WordStar keys** (`CMDLINE.PAS:304-305, 372-373, 391-392`): Ctrl+D a character
  on and Ctrl+F a word on, always; Ctrl+Home/End as Home/End while the line holds text (`Panel.arrows_to_line` hands
  them over). A departure: DN's ^S and ^A (a character and a word back) are Quick search and Select all here, Left
  and Ctrl+Left doing those moves.
- **Tab completes** (`CompleteCommandLine`) with text on the line: ` __nav_complete <base64> <point> '<base64 word>' <index>`, answered by a `C`
  mark -- bash through `compgen` and the command's `complete` spec, zsh through its tables and globbing only (compsys
  cannot be asked outside ZLE); `sh` cannot, and Tab stays the panel's. One candidate ends the word (`/` or a space,
  specials backslashed), several that agree extend it, the rest drop a `CompletionList` (a `HistoryList`,
  `dims_behind = False`). Typing with it open goes on into the line; the list narrows and is refilled (so `/`
  descends); a blank or Backspace past the word closes it. **The word at the caret is read in Python** (`subshell.shell_word`): `\` escapes
  and quotes are a shell's, so `my\ dir/` and `'my dir/` are one word; the shell gets it unquoted with its index (its
  own blank-splitting would cut it), and the replacement starts where Navigator's reading says, the escapes counted.
  Candidates are compared with the unquoted word.
- **With the console up and idle it stands for the terminal** (`Shell._console_is_the_terminal`): Up/Down walk the
  shell's history (` __nav_history`, `H` mark, `fc -lnr`); where the rc binds Up or Ctrl+R to atuin (detected once by
  `__nav_keys`, `U` mark) those keys run `atuin search -i` on the console as atuin's binding does (descriptors swapped,
  choice back in an `R` mark, `__atuin_accept__:` runs it). Such a line is sent in the queue's **`"reveal"` mode**:
  hidden until its `O` mark, holding keys (`busy`), finishing no command. With panels up, Up is the panel's and Ctrl+R
  re-reads.
- **fzf and zoxide** (a departure, asked for; `navigator/lib/system/fuzzy.py`). `__nav_keys`' `U` mark is
  `up;search;cd;file;fzf-path;zoxide-path`: Ctrl+R `fzf` (`__fzf_history__` / `fzf-history-widget`), Alt+C
  (`__fzf_cd__`, found in `bind -s` too, where older fzf binds a macro), Ctrl+T (`fzf-file-widget`/`__fzf_select__`) ->
  `Subshell.search_binding`/`cd_binding`/`file_binding`, and `has_fzf`. `Subshell.pick(kind, line, callback, listing)`
  sends ` __nav_fzf KIND QUERY [FILE]` in `"reveal"` mode, like atuin: fzf draws on `/dev/tty`, its stdout comes back
  as the `R` mark (no descriptor swap). Kinds: `history` (the listing -- Navigator's command history -- then `fc
  -lnr`, deduplicated, `__nav_` lines dropped), `directories` (`zoxide query -l`, then the listing -- the
  `directories` history), `cd` and `files` (`FZF_ALT_C_COMMAND`/`FZF_CTRL_T_COMMAND`, else `--walker`). The user's
  `FZF_*_OPTS` go after ours in `FZF_DEFAULT_OPTS`, as fzf's own bindings do. The listing is written on a thread into
  `Subshell.scratch()` (the shell's private directory). `Shell.pick` puts the console up if it was down
  (`_show_console`, never the relayed terminal) and `Shell.pick_chosen` (`PickChosen`, posted from the reader) takes
  it down again: Alt+J (`JumpToDirectory`, `Manager._go_to`), Alt+Shift+F8 (`FuzzyHistory`, onto the line), and on the
  idle console Ctrl+R/Alt+C/Ctrl+T where the rc binds them to fzf (Alt+C moves the active panel; the console keeps
  the keys). Both commands refuse (`Shell.fuzzy_refusal`) without fzf or with `sh`.
- **`[interface] feed_zoxide`** (navigator.ini only: the Interface page has no row left): `Panel._remember_directory`
  hands every local directory a panel comes to to `fuzzy.add` (`zoxide add` on one worker thread), and the rc makes
  zoxide's own `__zoxide_hook` do nothing (`_BASH_ZOXIDE`/`_ZSH_ZOXIDE`, asked of `Subshell.feeds_zoxide()` as the
  shell starts), since a shell `cd` moves the panel and would be counted twice. `z`/`zi` typed on the line work as
  any `cd` does. The bash rc strips trailing `;`/blanks from `PROMPT_COMMAND` before appending to it: zoxide's init
  leaves `__zoxide_hook;` in an empty one, and `;;` broke every prompt.
- **A typed line goes to the shell as typed** (a departure): DN's `ExecString` split it at `||` into a batch file and
  expanded `MakeCMDParams`' `%1`..`%6` / `%11`..`%16` (the two cursors' files) and `%%`; here `%` and `||` are the
  shell's. Ctrl+Enter / Ctrl+[ / Ctrl+] put names on the line, and the user menu keeps its own macros.
- **A line starting `|` is panelized, not run** (a departure): `Shell.run_command` (typed) records it in the history,
  clears the line and hands the rest to `Shell._panelize` -> `Manager.panelize`, whose capture runs off the pty
  (`navigator-panels`, *Panelize command*). A leading pipe is a shell syntax error, so no command is lost to it.
- **Enter on an executable runs it** (`Panel.choose` emits `ExecuteFile`; `Shell.on_execute_file` runs `./name`); any
  other file is opened (`OpenFile`, DN's: `extensions.ini`'s command, an archive entered, else the desktop's
  application -- `navigator-user-menu`, `navigator-gio`).
- **Ctrl+Enter puts the entry's name on the line** (`InsertName`, DN's `cmInsertName`: a space after, one before if the
  caret follows a word, `..` giving the directory); Ctrl+Shift+Enter the whole path, Ctrl+double-click the same (DN's `_CtrlEnter`); Alt+Enter
  bound beside it (mc's key) for terminals that send Ctrl+Enter as Enter.
- **Shift+Up/Down from the panels walk the command history** (`PreviousCommand`/`NextCommand`, the line's `recall`,
  as Ctrl+E/Ctrl+X): DN's panel handed `kbUp`/`kbDown` held with Shift to the line. `Panel.on_key` declines them so
  they reach `Manager.keys`; the cursor stays. **Ctrl+Shift+Ins copies the whole line** (`CopyCommandLine`, DN's
  `kbCtrlIns` handed on with Shift) -- where the terminal sends it (VTE and Ghostty keep Insert keys). Refused while
  the tree, quick view or info has the keyboard; nothing with the line hidden. **Ctrl+Ins with text on the line**
  copies its selection, or the whole line (`PutInClipboard` steps aside, the Gray keys' rule) -- a departure: DN's
  panel always took Ctrl+Ins for the file names (`_CtrlIns`, `FLPANELX.PAS:1257`); with the line empty it's the
  panel's, as DN's.
- **Ctrl+[ / Ctrl+] put the left / right side's directory on the line**, ending in `/` (`InsertSideDirectory(side=)`,
  DN's `$1A1B`/`$1B1D`: `cmGetName` of `LeftView`/`RightView`, then `cmInsertName`), bound in `Manager.keys` (markup
  cannot name a bracket key), handled by `Shell.on_insert_side_directory`. The side, not the active panel; the Ctrl+T
  tree there answers its cursor's directory, anything else that side's panel (hidden, or behind the quick view or
  info -- a departure: DN's quick view answered nothing). Ctrl+[ needs the kitty protocol (Esc's byte otherwise).
- **Space tags while the line is empty** (`ToggleMarkBySpace`, bound in `manager.nml`, handled and gated by `Shell`).

## Commands in a window (a departure)

DN ran one program and was not running itself while it did; the console still works that way. A command can
also run **in a window of its own** on the desktop, beside the panels and other windows, as many at once as
there are windows.

- **The widgets.** `ScreenView` (`shell/console/screen_view.py`) is what `Console` and the window share:
  painting a `ConsoleScreen`, scrollback, selection, copy/paste, and key/mouse forwarding. Its subclass says
  `busy`, `alive` and `write_child`. `TerminalView` (`shell/terminal_view/`) is one command on its own
  `PtyProcess`, `<command_shell()> -c command`. `command_shell()` in `subshell.py` is the shell the command line
  runs (bash/zsh/sh/dash, else bash, else `/bin/sh`). It is non-interactive: no rc files, so no aliases, and
  the environment is Navigator's own. It starts in `mounted()`, its pty follows its size through an effect,
  and its `status` is set from the reader as `revision` is. `TerminalWindow` (`shell/terminal_window/`, a framed
  `Window`) is titled with the command, then `"cmd - exit status N"` / `"killed by signal N"`.
  `open_terminal()` opens it zoomed or 80×24 inside the frame (centred, staggered), and a zoomed one keeps
  that rectangle to unzoom to.
  **Its right frame has a scroll bar for the history** (`TerminalWindow.bar`, a departure, asked for, as the
  viewer's). It is shown only while lines have gone off the top (`ScreenView.overflows`), and never while a
  full-screen program has the alternate screen. Its value is `scroll_above` and its range `scroll_total`
  (`ConsoleScreen.scroll_extent`: pyte's `history.top`/`bottom`), so at the live screen the thumb is at the bottom.
  `on_bar_scroll` calls `ScreenView.scroll_to`, which pages there in pyte's steps. **The console behind the desktop
  has no bar**: it has no frame, and one would cover the shell's last column (asked: *windows only*). Nothing
  scrolls sideways, as a terminal's lines wrap at its width.
  Utilities > *Remote shell* opens one on `ssh -t` and sets `remote_site`, so asking again selects it
  (`navigator-drives` skill).
- **How one is started.** `Shell.run_in_window(command, cwd=, zoomed=, modal=, closes=, uses=, cleanup=, title=)`, from:
  - a typed line starting `&` (`run_command`, after the `|` check; a leading `&` is a shell syntax error too);
  - **Shift+Enter** (`ExecuteCommandLineInWindow` on `Navigator.keys`, gated as Enter is). Only kitty-protocol
    terminals tell it from Enter. With the line empty it falls through to the panel's Shift+Enter
    (`ChangeInactive`);
  - File > Execute OS command's *In a window* / *Zoomed* / *Modal* (`ExecuteCommandDialog`, which replaced
    `EditLineDialog` there);
  - a user menu or `.ini` item with a `<&` line (`navigator-user-menu`).

  `None` for zoomed/modal is System Setup's *Command windows zoomed* / *modal*
  (`[system] command_window_zoomed`, default on, and `command_window_modal`, default off).
- **Keys.** While it runs the program gets every key, F10, Ctrl+O and Alt+X included:
  `Shell.program_has_keys` is also true for a focused, busy `TerminalView`. The exceptions are the ones that
  bring another window forward: `window_keys()`, read from `Desktop.keys` (`SelectWindow`/`WindowManager`:
  Alt+Shift+F1..F9, Super+digit, Alt+0), which the view declines. A modal window (`modal` set on the instance
  before `Desktop.open`, `view.holds_all_keys`) keeps those too. The mouse on the frame always moves, zooms
  and closes. Once the command has ended, Esc/Enter close the window and *Esc Close* is on the key bar.
- **Closing by itself.** `run_in_window(closes=True)` (`WindowMode.closes`, a `<& close` line) closes the window
  as soon as the command ends with status 0. `TerminalView._on_exit` calls the window's `command_ended(status)`,
  on the loop. A command that fails leaves its window open, so its error can be read. Alt+F4's console editors
  use it (`navigator/lib/editor/console_editors.py`), as can any user menu or `.ini` item; every other command
  window stays open with its output. `closes` may instead be a test of the **raw wait status**: Remote shell passes
  `remote_shell.ended_well` (any exit but `ssh`'s own 255, not a signal), so Ctrl+D closes it whatever the remote
  shell's last command left.
- **Stopping.** Closing the window (any route: `[■]`, Ctrl+F4, Close all) unmounts the view, and
  `TerminalView.unmounting` calls `PtyProcess.hang_up()`. That is SIGHUP to the process group and the pty
  let go; a child still alive after `HANG_UP_GRACE` (2 s) gets SIGKILL. It is reaped with `WNOHANG` from
  `loop.call_later`, never by a blocking `waitpid` on the loop. **While the command runs, closing asks first**
  (*Close command window*, Yes/No): `TerminalWindow.must_ask` is `view.busy` and Confirmations'
  `close_command_window` (default on), so the icon, Ctrl+F4, Close all and Alt+X all ask; Esc or No keeps both.
  Once it has ended, nothing asks. `Navigator.on_stop` hangs
  up whatever is still open. `TerminalWindow.on_close` puts back `UseFile` copies and removes a menu item's own
  script.

## The character table (Ctrl+B)

Utilities > *Character table* (DN's *ASCII Table*, `cmASCIITable`, `kbCtrlB` in `Navigator.keys`): `Shell.ascii_table`
calls `pick_character(app, self.glyphs)` (`shell/unicode_chart`) and puts the character picked on the command line
with `CommandLine.insert`, where DN put it back as a key press the line took; a NUL is nothing. In the ASCII glyph
tier that is DN's `AsciiChart` (`shell/ascii_chart`, its CP437 glyph, `│` for 179); in any other it is the Unicode
*Character Table* -- see the `navigator-editor` skill's Ctrl+P bullet for how it works.
Disabled with *Hide command line*. Inside an editor Ctrl+B is the start of its ^B^V chord, so the editor keeps it
(its own Ctrl+P opens the same chart for the text). Under tmux, Ctrl+B is tmux's prefix and never arrives.

## User screen (Alt+F5) and Refresh display

- **≡ > User screen, Alt+F5** (`ShowUserScreen`, DN's `cmShowUserScreen`; Ctrl+O is its `cmShowOutput`):
  `Shell.show_user_screen` shows the console and overlays `UserScreenPeek`, a modal layer over **every row**, the menu
  bar and key bar's included -- DN's `TBackground` the size of the application (`DNAPP.PAS:1027-1046`): the live
  console's rows at the bottom and `ConsoleScreen.history_rows` above them (laid out as live rows, `_lay_row`; none on
  the alternate screen), the view scrolled to the bottom first. It doesn't dim, and ends on the next key or click --
  which goes nowhere else -- and the windows come back. Already
  showing, it stays; with *Use internal terminal* off it is Ctrl+O's hand-over. Esc on an empty command line under
  Interface's *ESC for user screen* (`ouiEsc`, `CMDLINE.PAS:343`) is the same peek.
- **≡ > Refresh display** (`Refresh`, DN's `cmRefresh`): `Navigator.on_refresh` -> navkit's `Application.redraw()`,
  which forgets the front buffer so the next frame sends every cell -- for a screen another program wrote over.

## Execute OS command (File)

`ExecuteOsCommand` (*Os*, so the handler is `on_execute_os_command`), `Shell.execute_os_command`, DN's
`cmExecuteDOSCmd` -> `ExecDOSCmd`: `ExecuteCommandDialog` (with *In a window* / *Zoomed* / *Modal*) titled *Execute
OS Command* (DN's said *DOS*), caption *Command*, in the command line's history -- a departure: DN kept *Execute*'s
and Make list's *Action* in `hsExecDOSCmd`, apart from the line's, and never added to Alt+F8; here one history
serves all three -- opened on the file at the active panel's cursor if it is executable
(shell-escaped, its whole path in a listing, a blank after), the caret at the end; OK is `run_command`, as typed.

## System Information (Utilities)

`SystemInfo`, `Shell.system_info`, DN's `cmSystemInfo` -> `SystemInfo` (MEMINFO.PAS): `navigator/lib/system/sysinfo.py`'s `gather` on a
thread, from files under a root (`/`; tests pass a fake tree), then `SystemInfoDialog` with DN's four `ofFramed` boxes -- navml's `GroupBox`, titled on
the frame -- read for Linux -- *Main board* (DMI vendor+product, CPU model and max MHz, CPUs where DN had the co-processor), *Disk drives*
(`/sys/block` less loop/ram/zram/dm/md/sr/fd: size, model, removable), *Memory* (total, available, swap), *Other*
(os-release, kernel, host, uptime where DN had COM/LPT and the DOS version). `sysinfo.lines` right-aligns labels to a
colon and cuts a value to its box.

## Edit environment (Utilities)

`EnvEdit`, `Shell.edit_environment`, DN's `cmEnvEdit` -> `EditDOSEvironment`: `EnvironmentDialog`
(`dlgEditEnvironment`) over `os.environ`, names sorted, the focused one's value on the *Value* line (kept as the
cursor moves, DN's `FocusItem`/`SetValue`); *Append* (`NAME=value` in `EditLineDialog`, history `new_variable`,
put where the cursor is), *Rename* (the value goes with it), *Delete* (`dlEnvDelConfirm`). OK: `environ.changes`
before/after, `environ.apply` to Navigator's own environment -- what the external viewer/editor, the user menu and a
shell started anew take -- and `Subshell.set_environment` tells the running shell in one silent line (`export`/`unset`;
the hooked shell is bash or zsh even when `$SHELL` is fish, so never fish's syntax), only a shell with the hook
(`can_complete`); another keeps its copy until it restarts.
Names keep their case (DN upper-cased them).

## Commands history (Alt+F8)

`HistoryList` (global key; Utilities > Commands History), DN's `cmHistoryList` -> `CmdHistory`:
`CommandHistoryDialog` (`dlgCommandsHistory`) over a `HistoryList` of the command line's `HISTORY` list `command`,
the oldest at the top and the cursor on the newest. Space marks a command -- DN's `+` flag is navml's *pinned*,
synced to the store as the box closes or acts -- Left/Right go to the marked one before/after, Del or *Kill* forgets
one (a marked one is refused, where DN beeped), *Edit* reworks it in `EditLineDialog` (`InputBox`, *Edit History*,
history `edit_history`; it comes back as the newest, keeping its mark); the key bar says *Space Keep*, *←→ Next kept*
(`CommandHistoryDialog.key_hints`, a departure, asked for). *Run* (Enter, double click) is
`Shell.run_command`; *Drop* puts it on the line with the history walk set to it (`CommandLine.walk_to`, DN's `CurString := DT.I`), so Ctrl+E/Ctrl+X go on from the one chosen, the line's text kept aside as the draft. DN's Shift+Up/Down reordering is not here: the store
keeps its lists by when.

## Screen grabber (Shift+Alt+Ins)

`ScreenGrab` (global key; ≡ > Screen grabber), DN's `cmExecGrabber` -> `ScreenGrabber`: `Shell.screen_grab` says
DN's `dlGrabWelcome` once a session, then overlays `shell/grabber.ScreenGrabber` -- modal, undimming, painting the
cells already under its rectangle with `reverse` flipped and keeping their text (`surface.get`, continuation cells
skipped). `TGrabber.HandleEvent`'s keys: arrows move (Ctrl: 8 across, 4 down), Shift+arrows size from the bottom
right, PgUp/PgDn/Home/End to the edges, clamped on screen and at least a cell. Enter copies the rows joined by
newlines through `app.copy_to_clipboard`; Esc nothing. The rectangle is remembered (`grabber._last`, DN's
`Top`/`Bot`). Departures: the screen under it is live, not a frozen copy; and a left drag spans the rectangle
from the pressed cell to the pointer (`ScreenGrabber.on_mouse_click`, mouse captured, clamped on screen) -- DN's
grabber took no mouse. Releasing a drag copies and closes: the release sets `_take` and invalidates, and the next
`render` (the only thing that knows what is under the new rectangle) ends with its rows. A click that never leaves its
cell only places a one-cell rectangle; the keys and Enter work as before. A right press leaves like Esc, mid-drag
included.

## The calculator (Ctrl+F6)

`Calculator` (bound in `manager.nml`; Utilities > Calculator from anywhere) is `Shell.on_calculator`: DN's `InsertCalc`,
**one** `CalculatorWindow` (`shell/calculator_window`) on the desktop -- a dialog in a `Window`, DN's
`InsertWindow`, 49x15 at (10, 5), dialog colours from `navigator.nss`. A window has no dialog keys of its own, so it
binds Esc/Enter/Tab/Shift+Tab to navml's `Cancel`/`Default`/`SelectNext`/`SelectPrevious` and answers them itself
(Tab cycles its own `focusable()`), and walks Alt+letter over its controls. The indicator's five rows (decimal, hex,
binary, octal, exponent; *Error*; *Overflow*) follow the line through an effect. Enter evaluates: the line becomes
the value, selected, and `CalcLine` lets a digit replace it and anything else carry on from it. *Copy* puts *Copy
As*'s form through `app.copy_to_clipboard`. Esc/*Close* record the line in history `calc`. The sums are
`navigator/lib/utilities/calculator.py` (`PAR.PAS`'s numbers, operators and functions; **arithmetic precedence, a departure** --
DN's put `^` below `*`; integer forms 64-bit where DN's were 32). Button ids must not shadow methods (`evaluate`).

## Read when

| Reference | Read when |
|---|---|
| `reference/console.md` | why the screen is owned, why pyte, the mirror, what owning the pty costs |
