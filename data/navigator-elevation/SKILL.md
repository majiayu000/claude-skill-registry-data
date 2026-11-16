---
name: navigator-elevation
description: As root -- doing a step refused permission (EACCES/EPERM) again as root, a departure (DOS refused no one). navigator/lib/system/elevate.py (ELEVATION, sudo -S with Navigator's own password box or pkexec's polkit agent, begin/answer/call, release and root_timeout, close at exit, ELEVATION.command for tests), navigator/lib/system/roothelper.py (the helper process, its framed JSON protocol and closed OPS list), navigator/lib/drives/root.py (RootDrive, LocalDrive's steps through the helper, write_file for the editor), filecopy's Elevated mixin and AS_ROOT (copy, move, erase, Alt+E attributes), F7 mkdir, Shift+F5 links, Alt+A multi-rename and Alt+F6/Shift+F6 rename, navigator/widgets/file_ops/as_root.py (ask_skip, ask_as_root, open_root), the editor's F2 save, Save as, ^K W and ^K R, F3's viewer, Ctrl+Q quick view and F4's read through the helper (hold/unhold), As DataBase on a copy fetched as root (usefile's TempCopy.drive), Ctrl+F7/F8 UU encode/decode, Alt+L's list file, archives on the disk (Enter, Shift+F2, a refused rewrite), and [system] elevate / root_timeout in System Setup. Use when touching any of these or wiring another operation to offer As root.
---

# As root

A departure: DN never met a permission. When a step on the local disk fails with `EACCES`/`EPERM`, the error box
offers **As root** beside Skip/Cancel; answered, the step is done again through a root helper, and **every later step
of that operation goes through it without asking again** (DN's *All*).

## The pieces

- **`navigator/lib/system/elevate.py`** -- `ELEVATION`, the one helper. `begin()` starts it and answers `READY_STATE`,
  `Asked(prompt, wrong)` or `Refused(reason)`; `answer(password | None)` continues. **Everything blocks: call on a
  thread** (`asyncio.to_thread`), never the loop.
  - sudo runs as `sudo -S -p MARKER -- python -I -B -c BOOT` in a new session with no terminal of ours: its prompt
    comes through stderr and is recognised by `MARKER`; *Sorry* before it means `wrong`. The password goes to sudo's
    stdin and is never kept. pkexec's polkit agent asks for itself, so `begin` may wait (`START_TIMEOUT`).
  - `[system] elevate` (`auto` = sudo else pkexec, `sudo`, `pkexec`, `off`); `available()` is false when already
    root, off, or no tool installed -- then As root is not offered at all.
  - `release()` at the end of every operation closes the helper when `[system] root_timeout` is 0; otherwise the
    reaper closes it that many idle minutes after its last step. `Navigator.on_stop` closes it.
  - **`close()` never waits for ever.** Steps queued for the lock are turned away. The step under way gets
    `STEP_WAIT` (1 s), then the socket is shut under it, so its read ends with `EIO` and it lets go; if the lock is
    still held after another `STEP_WAIT`, closing gives up and quitting goes on. Found as a full-suite timeout: a
    tree on `root:///` probing a slow network mount (s3fs/sshfs under `/mnt`) held Alt+X with it.
  - **`hold()`/`unhold()`**: a window that keeps a file open through the helper (F3's `_RootRandom`) holds it;
    neither `release()` nor the reaper closes a held helper. The handle's `close()` unholds and releases.
  - **`ELEVATION.command`** replaces the tool's argv: tests run the helper unprivileged with it (`tests/test_elevate.py`).
- **`navigator/lib/system/roothelper.py`** -- the root process. Messages are a 4-byte big-endian length, that much
  JSON, then `size` raw bytes. **Only names in `OPS` (the public methods of `_Helper`) may be asked**; an unknown op is
  `EINVAL`. Answers are `{"ok": ...}` or an `OSError` as `errno/strerror/filename`, re-raised as the same `OSError`
  subclass on our side. It says `READY` once and ends at end of input. Started with `-I -B`, the package path inserted
  explicitly, so nothing from the user's current directory or environment is imported as root, and no `.pyc`
  is written as root into the user's tree.
- **`navigator/lib/drives/root.py`** -- `ROOT_DRIVE`, a `LocalDrive` whose every step is a helper request (files are
  `_RootFile`s read/written a `CHUNK` per request). `write_file` is the editor's `save.write_file` run in the
  helper; the text is gathered there first, so it is not stoppable part way.
  **The lock check is done here, not in the helper** (`check_lock=False` there): the editor's own `flock` would
  otherwise make the root process look like another program and refuse the save.

## Threat model (reviewed 2026-10-26)

Not a backdoor: no setuid file, no daemon, no sudoers/polkit rule, the password never kept; every start is the
user's own authentication. What the review found and the rules it left:

- **The channel to root is a `socketpair`, never a pipe.** A pipe's end can be reopened through
  `/proc/<navigator-pid>/fd/N` by *any* process of the user's (Yama `ptrace_scope=1` restricts attach only) and fed
  requests: root without a password for `root_timeout` minutes. A socket refuses that (`ENXIO`). On top, Navigator
  is made **non-dumpable** (`prctl(PR_SET_DUMPABLE, 0)`, `_set_dumpable`) while the helper runs -- no ptrace, no
  `/proc/<pid>` for the user's processes, even at `ptrace_scope=0` -- and dumpable again in `_shut`. A debugger or
  py-spy cannot attach to Navigator meanwhile; that is the point.
- **Root runs code the user may be able to change** (a checkout, a virtualenv, `pip --user`: `untrusted_code()`
  over `code_paths()`, which include the venv's `site-packages`, whose `.pth` files run even under `-I`). It is said
  in the question (`as_root._question`), not refused: no worse than `sudo ~/script`, and how development works. The
  packaged install is root's and says nothing. Tests patch `as_root.untrusted_code` (autouse `trusted_code`).
- **A step that changes the disk follows no symlink another user owns** (`_Helper._pinned`): only root's and the
  asker's (`SUDO_UID`/`PKEXEC_UID`, else `getuid()`), `ELOOP` otherwise. Each directory on the way is held open with
  `O_PATH` and the step done through `/proc/self/fd/<dir>/<name>`, so a directory swapped for a link between two steps
  (the `rm -rf` race, a shared directory, the home of the user whose tree is being erased) cannot send root's next
  unlink, write or chmod elsewhere. `open_write` adds `O_NOFOLLOW` after resolving, `chmod` changes an `O_PATH`-held
  inode, `write_text` hands `write_file(follow=False)` the resolved name. Reads are left alone: the user has root
  already. The kernel's `fs.protected_symlinks` covers sticky world-writable directories only; this is everywhere.
  Elsewhere than Linux (`PINNABLE` false) steps go by name, as before.
- **Live root is visible**: `RootMark` (`navigator/widgets/shell/root_mark.py`) shows *ROOT* white on red before the
  clock while `ELEVATION.running` (polled once a second, `Shell.follow_root`), since a panel or the quick view may
  then go to root unasked. Utilities > *Close root access* (`CloseRootAccess`, enabled while it shows) sends
  `root:` panels back to the disk and closes the helper.
- **What a `root:` panel offers**: whatever goes through a drive (copy, erase, F7, Alt+E, F3/F4, Find, *Find
  duplicates*, checksums -- `RootSiteDrive` reads through the helper). **Not** what runs as the user against the
  place -- Panelize (`$SHELL -c`), Show hard links, Mount image, git status, zoxide -- greyed with *Not as root: the
  command runs as you* (`manager._disk_only`), not the old, wrong *Only on the local disk*.
- **Utilities has one root entry** (`root_access` in `main_menu.nml`, command `ToggleRootAccess`): *Elevate root
  access* while closed (`Shell.open_root_access`, `open_root`'s password box), *Close root access* while open
  (`close_root_access`). `Shell._name_root_access`, an effect on `root_mark.open`, sets its caption and tooltip;
  both keep the same hotkey in every catalogue. Greyed when there is no way to root (`Shell._root_reachable`,
  `ELEVATION.available()` cached by `[system] elevate`) or when already root. `CloseRootAccess` stays a command of
  its own: the mark's click and a user's key binding run it.
- **Elevating also makes the console root's** (the menu entry only; an *As root* answer does not):
  - **The op.** The helper's `console` op starts the helper user's own login shell (bash, zsh or sh; else bash on
    `SECURE_PATH`) on a `pty.fork` of its own. Navigator's hook (`subshell.shell_argv`) goes into a root-owned
    `mkdtemp`, never the user's temp directory. The environment is `sudo -i`'s (`console_environment`): the
    target's HOME/USER/LOGNAME/SHELL, `SECURE_PATH`, and of what Navigator sends only `CONSOLE_KEEP` and `LC_*`.
    The cwd is reached through `_pinned` (no other user's link), else root's home.
  - **Handing the pty back.** The op answers `WithFd`. `_serve` sends the reply with `"fd": true`, then the master
    with `SCM_RIGHTS` on the same socket (`_send_fd`), then closes its copy. `Elevation.call_fd` receives both
    under the lock; the channel is unbuffered, so nothing is read ahead.
  - **Lifetime.** `console_stop` and the end of the helper (`_stop_consoles`) hang the shell up (SIGHUP, SIGKILL
    after `CONSOLE_GRACE`) and remove its rc directory. `_reap_consoles` collects one that exited by itself.
  - **The Navigator side.** It is `RootSubshell` (`console-command-line`). It `hold()`s root access while it lives,
    so the idle timeout leaves it alone. `Shell.close_root_access` and `follow_root` (the helper gone) call
    `_back_to_user_shell`. `exit` typed at it brings the user's shell back with root access left open.
  - **The command line while it is root's** (`Console.root`, reactive): a `root:` panel counts as its own place on
    the disk (`Shell._as_the_shell_sees`, used by `_front_directory`, `_front_remote` and `_command_directory`). So
    the shell follows the panel there, commands run there, and the shell's own prompt (root's `\$`, `#`) shows
    instead of the `root://...$` stand-in. The stand-in prompt ends in `#` too.
    The terminal's title says `root@host` with `~` meaning root's home (`title.window_title(where, root=True)`,
    from `Shell._name_window`).
  - **The status line says *ROOT* too** while the menu bar's mark cannot be seen (console up, or *Hide menu bar*):
    `key_root_mark` in `shell.nml`, a second `RootMark` bound to the first's `open`, at the key bar's right end;
    `KeyBar.reserve` keeps the items (and an open menu's hint) clear of it.
  - **Following a cd.** `_follow_shell` goes through `_panel_to_shell`: a place the user cannot even stat
    (`/root/sub`; 3.12's `is_dir()` raises `EACCES` there) takes the panel straight to `root:`.
  - **Threat model.** The master fd exists only in Navigator, which is non-dumpable while the helper runs, as for the
    socket. Nothing user-writable is run as root: root's rc files, root's home, a root PATH, a root-owned rc
    directory.
- **Its tooltip** (`RootMark.tooltip_at`) says what it means, that it closes after `root_timeout` idle minutes (left
  out at 0), and that Utilities > *Close root access* closes it now -- the path built from the menu's own translated
  captions, so it reads as the menu does.
- Still open, by choice: files created as root in the user's own tree stay root's (a `chown` back would be a
  departure; not asked for).

## Wiring an operation

- **Workers** subclass `filecopy.Elevated`: use `self._drive_of(location)` instead of `drive_of`, wrap a step in
  `self._try(path, step)` (or loop on `self._failed(path, error)`), and call `self._release()` in `run`'s `finally`.
  `Failure.elevate` is set only for a local path, a refusal errno, and a worker not yet elevated -- a step refused
  even as root is just Skip/Cancel. `is_root` turns true once elevated, so *Preserve attributes* sets owners.
  Copy/move (`_Copier`), erase (`_Eraser`) and Alt+E (`fileattr._Changer`, whose own `_stat`/`_children` go
  through the helper once elevated, and `apply_one(as_root=True)`) are wired. Alt+E's ACL, Xattrs and Flags pages go
  through `RootDrive`'s `listxattr`/`getxattr`/`setxattr`/`removexattr`/`get_flags`/`set_flags`, each a helper op
  through `_pinned` like `chmod` (`getxattr` answers its value as the raw payload, `setxattr` takes it as one).
  **While root access is open (the menu bar's ROOT), Alt+E's owner field is enabled** and every group offered:
  `fileattr.can_chown_user()` is `euid == 0 or ELEVATION.running`. A request with an owner or group then starts
  `_Changer` elevated (checked in `run()`, so a helper closed meanwhile falls back to refuse-then-offer).
  **The dialog's own *As root*** (`root_button`, declared in `attr_dialog.nml` and moved into the base's `row` between OK and Cancel in
  `__init__`; shown when `gather()`'s `can_elevate`: local, not root, `ELEVATION.available()`) runs `open_root`,
  enables Owner, offers every group, and sets `AttrRequest.as_root`, which elevates `_Changer` for any change.
- **The loop side** is `navigator/widgets/file_ops/as_root.py`: `ask_skip(app, message, elevate=)` (Skip / As root /
  Cancel; answers True, None or `AS_ROOT`), `ask_as_root(app, message)` (As root / Cancel), and `open_root(app)` (the
  `PasswordDialog` titled *Root access* until sudo accepts, an *Error* box on a refusal, silence on Cancel).
  `Manager._ask_skip` passes `question.elevate` through.
- **The editor**: `EditWindow._write_or_root` (F2's `save` and `save_as`) offers it on a refused write (not for a
  `UseFile` copy) and writes through `ROOT_DRIVE.write_file`, releasing after. `_check_for_over`'s lifting of a
  read-only mode is let pass when refused and root is available: the write is refused next and offers *As root*.
- **^K W / ^K R** (`write_block`, `read_block`): the same retry with `ask_as_root`; ^K W writes through
  `ROOT_DRIVE.write_file` (or `open_write(append=True)` for *Append*), ^K R reads with
  `document.read_text(as_root=True)` (`read_document` stats and opens through `ROOT_DRIVE`).
- **F3** (`Manager` on a local file, after `open_viewer` is refused): `ask_as_root`, then
  `as_root.view_as_root` opens a `viewer.ChunkedSource` on `ROOT_DRIVE.open_random` -- chunks fetched on a thread
  as a server file's are, never a helper round trip on the loop -- with `source.drive = ROOT_DRIVE` so the viewer's
  *Save as* reads through it too. The helper's `read_at` op is `os.pread` on the open handle.
- **Ctrl+Q quick view** (`QuickViewer._opened`): a refused open is read as root **only while
  `ELEVATION.running`** -- moving the cursor never asks for a password -- through `as_root.root_source` (a
  `ChunkedSource`, full path as its `path` so the "already showing" check holds), retried once, never again.
- **F4 opening** (`Manager.edit_file` -> `open_editor(as_root=True)` -> `load_document` -> `read_document(as_root=)`):
  the text read into memory through the helper, released after; the window's path is the original, so F2 is
  refused in its turn and offers *As root* again.
- **F3 As DataBase** (`.dbf`): `as_root.database_as_root` fetches it and its `.dbt`/`.fpt` with
  `usefile.fetch(..., drive=ROOT_DRIVE)` into the private directory, **owner-only (0600) whatever the original's mode**
  -- it may hold what only root could read. `TempCopy.drive` makes `conflicts`/`upload` go through it; `upload`
  through a drive with `write_file` (root's) writes in place of the original keeping owner and mode, never the
  usual new file renamed over (which root would own). `Manager._may_as_root` is the shared ask for F4/As DataBase.
- **Ctrl+F7/F8 UU** (`Manager._run_uucode(..., as_root=)`): a refusal (source unreadable, target refused) offers
  *As root* and runs the work again through `Manager._staged(..., as_root=True)`: the source fetched through
  `ROOT_DRIVE` into the private directory, encoded/decoded into staging, the files put on the disk with
  `usefile.put_files(..., drive=ROOT_DRIVE)` (asked about first, as for another drive). A target naming a directory
  is staged as one. New files are root's, as a copy made as root is.
- **Alt+L list file** (`Manager._write_list`, both the local and the elsewhere writer): a refused write to the disk
  offers *As root* and writes through `ROOT_DRIVE.makedirs`/`open_write(append=)`.
- **Archives on the disk** (`navigator/lib/drives/archive.py`): an unreadable one raises `PermissionError` from
  `open_archive` (before, `zipfile.is_zipfile` swallowed it and it was taken for *not an archive*, i.e. run as a
  program). `open_archive(as_root=True)` opens it the way an archive on another drive is opened: a private copy
  fetched with `usefile.fetch(..., drive=ROOT_DRIVE)`, every rewrite put back through root's `write_file` (owner
  and mode kept). `ArchiveDrive.as_root` drives **hold the helper** until `close()` (unhold + release), since a
  put-back can come at any time. `ArchiveDrive.go_root(job)` switches an open one whose rewrite was refused:
  staged members stay staged, the rewrite is made in the copy. `finish_drives(..., elevate=)` asks
  `Elevated._finish_as_root` first (copy/move, erase and Alt+E pass it; Alt+E's finish now runs inside `_Changer.run`). On the loop,
  `widgets/drives/archives.open_archive_or_root` (Enter, Shift+F2's *Extract*) asks `ask_as_root`.
- **F3's Shift+F2 *Store*** (`FileWindow.store`): a refused write of bytes typed in hex offers *As root*. Then
  `RootDrive.patch_file` checks the size (`stat`), opens the file with **`open_update`**
  (`_pinned(follow=True)`, `O_RDWR|O_NOFOLLOW`, no `O_CREAT`, no `O_TRUNC`, and only a regular file), and
  writes each run with **`write_at`** (`os.pwrite`). Nothing is created or truncated, and owner, mode and inode
  stay. A file viewed as root already (a `ChunkedSource` on `ROOT_DRIVE`, or `root:///`) is written the same
  way, unasked.
- **The viewer's Save as** (`FileWindow.save_as`): a refused local target retries `viewer.save_as(..., as_root=True)`,
  written through `ROOT_DRIVE.write_file` (owner/mode kept), released after.
- **A write-protected `.dbf`** (`DBWindow._edit_as_root`): editing a field offers *As root*, then the window moves
  onto a copy from `as_root.fetch_database`; every field goes back through root. **A root-fetched dBase copy holds
  the helper** (`DBWindow.root_held`) until the window closes -- else, with `root_timeout` 0, the first put-back
  found it closed. `database_as_root` sets the same.
- **F7 and Alt+A inside an archive** whose rewrite is refused: F7's remote branch offers `_may_as_root` and finishes
  through `go_root`; `multirename._finish` asks a `Failure` (with `elevate` for a local archive) where the failure
  used to be passed over in silence -- the renames were shown and never written.
- **Browsing an unreadable directory** (`navigator/lib/drives/root.py`'s second half): a panel lists and works
  as root at **`ROOT_SITE`** (`Site("root")`, shown `root:///path`) -- the disk's paths on a site of their own,
  so every step is a drive's, exactly as on a server, and copy/erase/F3/F4/Alt+E/... need nothing new.
  `RootSiteDrive` hands each step to `ROOT_DRIVE` on `on_disk(location)`; its `scan` is the helper's `listing` op
  (the disk's own `listing.read_listing`, entries packed as lists -- **an op must never return a tuple that is
  not `(value, payload)`**). No `exec` (Enter opens a program rather than running it, as on every drive but the disk); the free
  space comes back with the helper's listing. Disconnect (Alt+H) ignores it. *Auto refresh* is a
  `PollWatch` through the helper every `root.POLL_INTERVAL` (2 s) -- not `[remote] refresh`, off by default, as
  this is the disk; `_arrived_at_root` sets the watch up again, the first having found no drive mounted.
  - `root.hold(panel)` mounts the drive and holds the helper; `root.leave` unmounts with the last holder and the
    panel releases. `Panel._hold_root` (an effect) follows the location -- but `Panel._go_root` **holds before it
    moves**, since the rescan effect runs first and would find no drive.
  - The offer: `Panel._apply`, for a *navigation* read (not a re-read) of a local directory that failed and
    `os.access` says is unreadable -> `_offer_root`, once per place (`_root_offered`). While the helper runs
    already, it switches unasked, as the quick view does -- every time: `_root_offered` stops only a repeat of
    the question (declined, or no way to root), so a place first reached by the root console's `cd`, left, and
    entered again from the panel is `root:` again, not *Permission denied*.
  - Leaving: Enter and `..` on `root:` go back to the disk itself where `readable_plainly` says the user may list;
    so do a directory chosen in the tree (`Manager.on_tree_chosen`) and in Alt+T (`Panel._plain_where_readable`).
  - Alt+F7 and the trees (Ctrl+T, Alt+T) need nothing of their own there: `filefind._search_drive` and
    `DirectoryTree`'s drive reads go through `drive_of`, which is `RootSiteDrive` (tests in `test_elevate.py`).
  - **Coming back to a `root:` place** (a history, a bookmark, a typed URL -- anything through `Shell.reach` --
    or a saved desktop / the command line, which set the location directly): `Shell.reach` hands `ROOT_SITE` to
    `as_root.reach_root` (*Open … as root?*, titled *Root access*, then `root.mount_drive()`), never to `SESSIONS`.
    A panel that lands there unasked is caught by `_hold_root` -> `_arrived_at_root`: the same question, then a
    re-read; declined, the disk's own place, not asked about again.
  - `root._HOLDERS` is module-level: a test whose app ends with a panel at `root:` leaves its holder (the `helper`
    fixture in `tests/test_elevate.py` clears it).
- **File > Encoding > Convert text** (`textconv.convert(..., as_root=)`): not an `Elevated` worker, since
  `run_with_progress` relays no questions -- refusals are gathered in `TextJob.refused` and
  `Manager._convert_as_root` hands them to `Manager._again_as_root`, which asks `ask_as_root` once for the batch, then
  converts those again through `ROOT_DRIVE`. A drive with `write_file` (`ROOT_DRIVE`, the `root:` site's) writes through it, so the file keeps its
  owner, mode and links; a new file renamed over would be root's.
- **The ask-once shape, `Manager._again_as_root(job, question, rerun, *, keep=, errors=)`**: `job.refused` (`(location,
  size, reason)`, the disk only, not root yet) listed in one question, *rerun(refused)* through the helper, then
  `ELEVATION.release` (*keep*: the caller goes on as root -- Decrypt's passphrase questions -- and releases itself);
  declined, they go in *errors* (`job.errors`). `root.rooted(location, as_root)` is the one rule every such module
  reaches the disk by. Users: **Convert text**; **Encryption/Decryption** (`EncryptJob.refuse` → `refused`,
  `refused_plans`, an unread head planned again as root; `as_root` set on the job); **Checksums' each-file mode**
  (`write_each(as_root=)`: read failures `errors`, write failures `write_errors` under their own *could not be written*
  heading).
- **Asked at the file, as the copier does** (`Failure(elevate=True)` → `ask_skip` → `AS_ROOT`): **Replace in files**
  (a refused write through `ROOT_DRIVE.write_file`, later ones unasked: `ReplaceJob.as_root`); **Trash > Restore**
  (`restore(as_root=)`: `ROOT_DRIVE` makes the place and renames into it, the info file the user's;
  `RestoreJob.as_root`). The manager releases the helper after (`_release_if`).
- **Split / Combine** (`splitfile.split/combine(as_root=)`) through `_run_uucode`'s `as_root=`, as UU. **Alt+T's Make
  directory is F7's** (`navigator/widgets/file_ops/make_directory.py`, `make_directory_in`: the disk, *As root*, another
  drive, an archive's refused rewrite, Undo; `failure_text` names the directory).
- **Remote drives are deliberately not offered it**: local root cannot get past a server's refusal (FTP, SMB, S3
  have no notion of it; SFTP would need the server's `sftp-server` under its own sudo -- a separate feature,
  declined for now).
- `Manager._may_as_root(error, message)` is the shared ask; `_as_root_declined` is only meaningful right after
  it was called -- guard a read of it with the same condition that called it.
- **Multi-rename** (`multirename.run`): a refused rename of a file still under its own name asks with `elevate`;
  `AS_ROOT` sets `RenameJob.elevated` and retries, every later rename on a local place going to `ROOT_DRIVE`. A file
  stranded under its `.navrename-` name keeps the old put-back path (no offer). **Alt+F6/Shift+F6**
  (`Manager._rename_entry`) asks `ask_as_root` and renames on `ROOT_DRIVE`.
- **On the loop** (F7, Shift+F5): the first step stays on the loop as before; **once elevated every step goes to a
  thread**, since a helper request blocks. F7 asks `ask_as_root` and makes the directory with `ROOT_DRIVE.mkdir`;
  `Manager.link_entries` asks `ask_skip(elevate=)` per refusal until answered, then `filelink.make_link(...,
  as_root=True)` and `ROOT_DRIVE.makedirs` for the rest, releasing in its `finally`.

## Checked against the real tools (2026-10-26)

sudo 1.9.15p5 and pkexec 124 (polkit-gnome agent, XFCE), by a script driving `ELEVATION` and `ROOT_DRIVE`
directly plus a hand run in Navigator: the `\x01` prompt marker survives sudo, wrong passwords are told apart,
3 MB of every byte value go through unchanged (no pty in the way), `write_file` keeps owner/mode/backup, a
root-only directory lists and copies, release/timeout close it, and `-B` leaves no root-owned `.pyc`. By hand:
F2 and F7 as root keep owner and mode, Enter on `/root` lists it at `root:///root`, and Ctrl+T shows its tree. **Found
there and fixed**: `RootDrive.write_file`'s own lock check could not resolve a path inside a directory only root
may enter -- the helper now checks locks itself then (`write_text(check_lock=True)`). Both tools start with
`start_new_session=True`: pkexec with no polkit agent (over ssh) would otherwise ask on the terminal Navigator
draws on; without one it refuses and says why.

## Not wired yet

Remote drives (see above); Shift+F4's new file in a
directory the user cannot write is offered at F2's save.
Each would follow the pattern above.
