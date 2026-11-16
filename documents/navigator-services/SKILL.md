---
name: navigator-services
description: Utilities > Services, a departure from DN (DOS had no service manager) -- navigator/lib/system/services/ (the Backend interface in common.py with Unit, run/failure, Journal/LogFile/EditPlan, Follower; __init__.py's BACKENDS, current() and [services] manager, the dispatchers gather/act/details/log/edit_plan/after_edit, ordered/matches; systemd.py merging systemctl list-units and list-unit-files, drop-in overrides, daemon-reload, journalctl; openrc.py with rc-status --servicelist, rc-update show --verbose, rc-service, the own or filtered system log, /etc/conf.d; runit.py with definition directories, links in the supervised directory, sv status and its root-only supervise/, svlogd's current, conf or run; sysvinit.py with /etc/init.d scripts, LSB headers, hidden shutdown scripts, status only where handled, rc?.d links, update-rc.d/chkconfig, root-owned scripts only, /etc/default), the root helper's service/service_states/after_edit/journal_follow/journal_stop ops, ServiceList (a ColumnList), ServiceWindow (greying what a backend has not, ? states read as root, F3/F4/F5-F8, Ctrl+E/Ctrl+D, As root), F3's JournalWindow and log-file viewer, and [services] manager/refresh/journal_lines. Use when changing the Services window, adding a service manager, or changing what one runs.
---

# Services

**Not DOS Navigator's.** DOS had no service manager, so the whole window is a departure, asked for. It is recorded in
the docstring of `navigator/lib/system/services/__init__.py`, the `#:` comment above Utilities > *Services* in
`main_menu.nml`, and the window's markup. It is Process list's sibling and is built the same way
(`navigator-processes`).

## The interface (`navigator/lib/system/services/`)

- **One `Backend` per service manager** (`common.py`): `name`, `title`, a closed `verbs` tuple, capability flags
  (`user_scope`, `all_types`, `reload_after_edit`, `restart_after_edit`, `states_need_root`, `refresh_floor`) and the methods
  `refusal`, `valid_name`, `installed`, `gather`, `act`, `details`, `log` (a `Journal(argv, readable)` or
  `LogFile(path, pattern)`), `edit_plan` (an `EditPlan(path, seed, line, warning)`), `after_edit` and `states`. Each module (`systemd.py`, `openrc.py`) keeps its
  work in module functions and a thin class over them, so **tests patch the module function** (`systemd.unit_file`,
  `openrc.INIT_D`) and the class picks it up.
- **Every command goes through `common.run(argv)`** (`LANG=C`, `EINFO_COLOR=NO`, a timeout, no stdin) -- one patch
  point for every backend. `common.failure()` reads a refusal (polkit's *Access denied*, OpenRC's *superuser access
  required*, *Permission denied*...) as `OSError(EPERM)`, which `elevate.refused()` takes for *As root*; anything else
  is `EIO` with what was said.
- **Shared in `common.py`**: `UNKNOWN` (`?`, a state the user may not read) and `with_states()` filling it,
  `SYSTEM_LOGS` (socklog's `everything/current`, `/var/log/messages`, `/var/log/syslog`) and `system_log()` -- the
  F3 fallback OpenRC, runit and SysVinit share, filtered to the service's name -- and `pid1()`. `run()` takes a
  `timeout` (SysVinit's `status` gets 3 s). `LogFile.guessed` makes the title say a log was found by name.
- `Unit` has `backend` (the name of the one that read it) and `startup` (systemd's file state, or OpenRC's runlevels
  joined, `disabled` for none). `running`/`failed` cover both managers' words.
- `__init__.py`: `BACKENDS`, `current()` (`[services] manager` names one, else the first whose `refusal()` is empty:
  systemd, then OpenRC, then runit, then SysVinit -- last because Gentoo and Devuan run OpenRC under a sysvinit
  `init`), `refusal_reason()` for the menu's grey, and the dispatchers the window calls --
  `gather` (on `current()`, dropping `user`/`all_types` it cannot do), and `act`/`details`/`log`/`edit_plan`/
  `after_edit` on `backend_of(unit)`. **The window calls only these**, so a window test patches `services.gather`,
  `services.act`.
- **Adding a manager**: a module with a `Backend` subclass and `BACKEND`, an entry in `BACKENDS`, its name in
  `ServicesData.MANAGERS` (settings.py writes the tuple out: it is read before the backends can be imported), and
  its verbs' refusal words in `common.REFUSALS` if new.

## systemd (`systemd.py`)

- `gather(user, all_types)` merges `list-units --all` (load, active, sub, description) with `list-unit-files` (the
  file's state). A unit installed but never loaded is only in the second and is shown `inactive/dead`. An instance
  takes its template's state; **a template (`getty@.service`) is left out**. `--output=json` first, the plain
  columns when it is refused (systemd < 246).
- `VERBS` (8, mask/unmask included) and `valid_unit()` (systemd's characters, never a leading `-`, a dot required).
  `act()` runs `systemctl [--user] --no-ask-password VERB -- NAME`: **`--no-ask-password` keeps polkit off the
  terminal Navigator draws on**.
- `details()` is `systemctl status --lines=0 --full` (exit 3 for a stopped unit is no failure).
- F3: `Journal(journal_argv(...), can_read_journal(unit))` -- a user unit, root, or a member of
  `systemd-journal`/`adm`/`wheel` reads it all.
- F4 (`edit_plan`): **a masked unit is refused** by `unit_file()` (systemd may still report the package's file as its
  `FragmentPath`). `edit_target()` opens the fragment itself when it is the administrator's own (under `admin_dir()`,
  **compared after `realpath`**, so a link in `/etc` to a package's file is still the package's), else the drop-in
  `<admin_dir>/<unit>.d/override.conf`, seeded by `override_text()` with the package's file commented out.
  `after_edit` is `daemon-reload`.

## OpenRC (`openrc.py`)

- `gather()` runs two commands, never one per service: `rc-status --servicelist` (name and the first word in the
  brackets -- newer OpenRC prints an uptime after it) and `rc-update show --verbose` (`name | runlevels`, empty for
  none). The description is the script's `description=` line, read from the first 64 KiB of `/etc/init.d/<name>`.
- `VERBS`: start/stop/restart/reload through `rc-service NAME VERB`; enable is `rc-update add NAME default`;
  **disable reads `rc-update show` again and deletes it from every runlevel** (boot too) -- again, because the root
  helper gets only the name. No mask, no user services, no other kinds: the window greys them.
- `valid_service()`: a script's file name, never a leading `-`, never a `/`. **`installed()`** (a script by that name
  in `/etc/init.d`) is what the root helper checks beyond it.
- F3 (`log`): the service's own `output_log=`/`error_log=` (a plain path, no variable, in `/etc/conf.d/<name>` first,
  then the script) when the file is there; else the first of `SYSTEM_LOGS` with `pattern` = its name -- the viewer
  shows only the lines holding it, approximate, and the title says so; else `ENOENT`.
- F4 (`edit_plan`): `/etc/conf.d/<name>`, seeded when new by `conf_text()` with the script's `NAME=` lines commented
  out (not `depend()` or functions). No `after_edit`: `restart_after_edit`, so a save makes the window offer a
  restart of a running service.

## runit (`runit.py`)

- **No database, only directories**: definitions in the first of `DEFINITION_DIRS` (`/etc/sv`, Artix's
  `/etc/runit/sv`), enabled = a link to one in `service_dir()` (`$SVDIR`, else the first of `SERVICE_DIRS`). A
  directory placed in the supervised directory itself is listed too. **It is the manager only as the first
  process** (`pid1() == "runit"`): Debian's runit can supervise under systemd.
- `gather()`: every definition and enabled entry; one `sv status <svdir>/...` over the enabled. A disabled one is
  `down` with nothing read; `startup` is `enabled`, `enabled, down` (a `down` file) or `disabled`. No descriptions in
  runit: the column is what the `run` script's last `exec` runs.
- **`supervise/` is root's on Void**, so `sv status` warns *access denied* per service: `parse_status` reports that
  as refused, and `gather` marks the enabled `UNKNOWN` (`states_need_root`). A warning that is not a refusal (no
  `runsv` yet) is `fail`. `states()` is the same fixed `sv status`, raising `EPERM` when every one was refused --
  what the helper's `service_states` runs.
- Verbs: `sv -w 7 start|stop|restart|reload <svdir>/X` (a disabled one is refused: *enable it first*); **enable
  links the definition in; disable removes the link only if it is a link into the definitions** -- a directory placed
  there is never removed. `installed()` is a definition by that name.
- F3: `svlogd_dir()` -- the last `/path` after `svlogd` in `log/run` -- gives `DIR/current`, trusted as written (a
  root-only log directory cannot be looked into; the viewer offers *As root*). Else `common.system_log` (Void's
  `vlogger` goes to syslog).
- F4: `conf` when `reads_conf(run)` (Void's `[ -r conf ] && . ./conf`), seeded with `run` commented out; else the
  `run` script itself with `EditPlan.warning` (*an update of its package may replace it*), which the window asks
  OK/Cancel on before opening. `restart_after_edit`.

## SysVinit (`sysvinit.py`)

- **No list and no states**: services are the executable files in the first of `INIT_DIRS`; the description is the
  LSB header's `Short-Description` (`header()` joins continued lines) or Red Hat's `# description:`; start-up is
  the runlevels whose `rc<N>.d` (under the first of `RC_BASES`) has an `S<NN><name>` link, `boot` for `rcS.d`.
  It is the manager when `pid1() == "init"` and `/etc/inittab` exists.
- **Safety rules, each tested**:
  - Never listed: `HIDDEN` (`rc`, `halt`, `reboot`, `sendsigs`, `umountfs`...), `dpkg`/`rpm` leftovers, and any
    `shutdown_only()` script (LSB starts it only in 0/6 and stops it in 0 or 6). F5 on `halt` must be impossible.
  - **`status` runs only where `has_status()` finds a `status` case**: an old script that ignores its argument
    would start. Others are `unknown` (*no status action*), nothing run.
  - `status` runs `PARALLEL` (8) at once, each `STATUS_TIMEOUT` (3 s); a hang is `unknown` (*no answer*). Codes:
    0 `running`, 1/2 `fail`, 3 `stopped`, 4 or a refusal `UNKNOWN` (read as root like runit's), else `unknown`.
  - **`installed()` -- what the root helper requires -- is a listed script owned by `OWNER` (root) and writable by
    nobody else**: a script the user could change would be their code run as root.
- Verbs: the script itself (`/etc/init.d/X VERB`, never `service`, which may hand over to systemd); exit 4 (LSB's
  insufficient privilege) is `EPERM`. `verbs` is a property: enable/disable only with `enabler()`'s `update-rc.d`
  (`defaults` first when it has no links at all, then `enable`/`disable`) or `chkconfig` (`--add`, then `on`/`off`).
- `refresh_floor = 15`: each read is a process per script.
  The window's `Timer` child (`ticker`, `interval: root.refresh_ms()`) is `[services] refresh` raised to the
  backend's floor, 0 turning it off; it follows the setting at once and stops with the window.
- F3: `/var/log/<name>.log` (`guessed`), else `common.system_log`. F4: `settings_file()` -- the `/etc/default` or
  `/etc/sysconfig` directory the script names -- seeded with OpenRC's `conf_text` when new; else the script with a
  warning.

## As root

`roothelper._Helper`'s ops (OPS is built from public methods):
- `service(manager, verb, unit)`: the manager must be in `BACKENDS`, the verb in **its** `verbs`, the name
  `valid_name` and `installed`; then `backend.act()` -- the command line is always the backend's. A user unit is
  never offered root: its manager is the user's own.
- `after_edit(manager)`: the backend's `after_edit` when `reload_after_edit`, else nothing.
- `service_states(manager)`: for a backend with `states_need_root` only, its own `states()` -- no name or command
  from the client.
- `journal_follow(unit, path, lines)` (systemd only) writes `journalctl --follow` into **an existing file of the
  asking user's**, opened through `_pinned` without following a link and never created; `journal_stop(pid)` stops
  only a pid it started, and `serve()` stops them all in a `finally`.

## The window (`navigator/widgets/shell/service_window/`, `service_list/`)

- `ServiceWindow.backend` is `services.current()` from `__init__`. A manager other than systemd is named in the title
  (*Services (OpenRC)*) and the first column says *Service*. **What the backend has not is greyed in `refusal()`**
  (*Not something OpenRC does*): a verb outside its `verbs`, *User units*, *All types* (whose boxes are also
  `disabled`, and their key does nothing).
- `ServiceList` is a `ColumnList` (in `process_list.py`, shared with `ProcessList`). Rows are `.running`, `.inactive`
  (dim), `.failed` (bold and underlined: **a colour of its own failed `test_no_theme_draws_an_unreadable_pair`**) and
  `.masked` (italic).
- Reads go through `Background("nav-services")` with a read counter, running `_read_units`. **There is no read in
  `mounted()`**: the `_follow_view` effect's first run reads, because `_read_for` is None. The cursor is kept by name.
- **States only root may read** (`UNKNOWN`): an *explicit* read (`reload()`: opening, Ctrl+R, after an action) with
  root access already open also calls the helper's `service_states` and keeps the result in `_root_states`. **The
  timer's read (`reload(explicit=False)`) never calls the helper**, so an open window never keeps root access alive
  past `root_timeout`; it fills unknowns from `_root_states` and the status line says *states read as root at
  HH:MM*. With none, it says *states need root: Ctrl+R reads them as root*; Ctrl+R then asks *As root* first
  (`_rescan`) when root access is not open.
- Keys: F3 log, F4 edit (**not Filter, as Process list's F4 is**), Enter details, F5 start, F6 restart, F7 reload,
  F8/Del stop (asks), Ctrl+E enable, Ctrl+D disable, Ctrl+U user units, Ctrl+A all types, Ctrl+N/Ctrl+L sort,
  Ctrl+S/Alt+F filter, Ctrl+R re-read. Mask (asks) and Unmask are in the menu only.
- **Every verb command subclasses `ServiceVerb`**, but navkit delivers a command to `on_<its own class name>`, so the
  window aliases each handler name to `on_service_verb`.
- A refused action, for a system service with elevation available, goes through `ask_as_root` and
  `ELEVATION.call("service", manager=unit.backend, ...)` with `release()` in a `finally`.

## F4 in the window

- `_edit()` takes the `EditPlan`. A seeded (new) file first gets its directory (`_override_dir`: as the user, or the
  helper's `makedirs` after *As root*) because the editor's save does not create directories; it then opens as a
  new document with the seed inserted and the cursor on `plan.line`. Comments only, so saving it unchanged changes
  nothing.
- **A directory made by this F4 is removed when the editor closes with the file never written** (and nothing else
  there): `EditWindow.after_close` calls `_discard_unused` on a thread -- as the user, else through the helper's
  `rmdir` only while root access is still open. It never asks for root again just to tidy up.
- **The window learns of a save through `Shell.on_file_saved`**, which calls `unit_file_saved(path)` on every window
  that has it. A path from `_editing` then runs `services.after_edit` (systemd: daemon-reload; refused, straight to
  the helper's `after_edit` when root access is already open, else after *As root*) or, for a backend with
  `restart_after_edit`, asks to restart the service if it runs.

## F3 in the window (`journal_window.py`)

- `open_log()` asks `services.log` on a thread. A `Journal` goes to `open_journal()`: an empty 0600 file in
  `tempdir.private_dir()`, the follower (as the user, or `journal_follow` as root with `ELEVATION.hold()`), up to
  `FIRST_LINES` for the first bytes, then a `JournalWindow` (a `FileWindow`) with *Follow end* on. Its
  `unmounting()` stops the follower and deletes the file on a thread (`stopping`); an `atexit` hook stops any left.
  It keeps no File View History record.
- A `LogFile` goes to `open_log_file()`: a plain `FileWindow` on the file (`view_as_root` after *As root* when the
  user may not read it), `show_lines(LinePattern(pattern))` when there is a pattern, then *Follow end*. The title
  says *Log: <name>*, and *(its lines in <path>)* when filtered.

## Tests

- `tests/test_services.py` (systemd): the merge, sorting, names, `act`'s refusal, the helper's ops (no process for a
  bad manager, verb or name), and the window with `services.gather` patched, `[services] refresh` 0 and **`[services]
  manager` pinned to systemd** (`service_run`, so the host's own manager does not matter) -- filter, cursor, boxes,
  F5/F8/Ctrl+E, As root with `ELEVATION.call` faked (**pass every other op through**: a root drive another test left
  mounted calls `children`), F3's journal, F4's file and drop-in, and the unsaved drop-in's directory removed.
- `tests/test_services_openrc.py`: `rc-status`/`rc-update` parsing and merge, what each verb runs, refusals, details,
  F3's own/filtered/no log, F4's seed, `current()`'s choice, the helper's `installed` check, and the window with
  `manager = "openrc"` **and `openrc.refusal` patched to ""** (else the shell greys Services on a machine without
  OpenRC): greying, As root, F3 filtered, F4 then the restart offer. `/etc/init.d`, `/etc/conf.d` and the system logs
  are the `etc` fixture's, in `tmp_path`.
- `tests/test_services_sysvinit.py`: the `etc` fixture (LSB, Red Hat, no-status, hanging, code-4, shutdown-only and
  hidden scripts, `rc2.d`/`rcS.d` links, `/etc/default` and `/etc/sysconfig`), `common.run` faked **with its
  `timeout` keyword**: what is listed and never run, status codes, each verb with and without a tool, the helper's
  ownership check (`OWNER` patched to the test's user to pass), F3, F4, and the window's 15 s floor (spying on
  `Application.call_every`, `service_run(..., refresh=3)`).
- `tests/test_services_runit.py`: the `tree` fixture (definitions, a supervised directory with links, a `down` file,
  `svlogd` and `vlogger` loggers, a `conf`-reading `run`, a directory placed in the supervised directory), `sv status`
  faked through `common.run` (states, and every one refused), each verb (never removing a directory), F3, F4 and its
  warning, the helper's `service_states`/`service`, and the window: `?` with its hint, Ctrl+R reading as root with
  `ELEVATION.running` faked (a class property: patch `type(ELEVATION)`), the timer's read keeping the stale states,
  Ctrl+R asking when root access is closed.
