---
name: navigator-drives
description: Remote and virtual drives -- navigator/lib/drives/ (Location and Site, Drive/LocalDrive/MemoryDrive/SftpDrive/FtpDrive/SmbDrive/ArchiveDrive/TrashDrive (trash:///), ExecDrive with DockerDrive (docker://, podman://) and AdbDrive (adb://) -- every step a docker exec / adb shell -T process, the live lists of containers and devices, capabilities, zip and tar archives (and 7z/rar through 7-Zip's, unrar's and rar's command lines) entered with Enter (DN's TArcDrive), Extract to / Test / Shift+F2, archive columns, drive_of/mount/unmount, listing.py with DirEntry and the local scan), SESSIONS (connect and its NeedPassword/NeedPassphrase/UnknownHostKey questions, the SFTP channel pool, the transport watcher and one silent reconnect, idle reaping, closing → panels fall back like DN's cmCloseLinked), credentials (ssh config/agent/keys, known_hosts, optional keyring), RemoteProfile, UseFile temp copies and upload-back, copy/erase across drives through the one copier, Panel.location vs Panel.path, Manager's _LOCAL_ONLY gate, Utilities > Link > SSH/FTP/SMB/S3/GVfs/Docker/Podman/Android link managers (Alt+F11 for SSH) / Remote shell > SSH/Docker/Podman/Android (ssh -t, docker exec -it, adb shell; DN's cmTerminal) / Disconnect (Alt+H), the Link part of the Alt+F1/F2 box, Options > Configuration > Communications, and how to add a protocol. Use when touching anything that may not be a local path.
---

# Drives

DOS Navigator's panel held a **`TDrive`** (`DRIVES.PAS`): the disk, an archive (`TArcDrive`), a *Find:* listing
(`TFindDrive`), `TEMP:` (`TTempDrive`), or the PC at the other end of a cable (`TLinkDrive`, `NAVYLINK.PAS`, *Navigator
Link*, Alt+F11). `navigator/lib/drives/` is that object for a modern system. There are the disk, an in-memory drive
(the tests', later `TEMP:`), SFTP, FTP/FTPS, SMB, S3, a Docker or Podman container, an Android device over adb,
any remote `rclone config` has (`rclone://`), archives (`ARCVIEW.PAS`) and the Trash (`trash:///`). NFS is only
ever a kernel mount, which Disk > Volumes already lists. `reference/design.md` has the plan and the phases.

## Rules

- **A `Location` is not a path.** `Location(site, path, outer)`; `Location.of(Path)` for the disk,
  `Location.parse(text)` for what `str()` wrote. It has **no `__fspath__`**, so an `os.*` call handed one fails at once
  instead of running on the local disk with a remote name. `.local` is the way back, and raises `RemoteLocation` (a
  `TypeError`) off the disk. **`str()` of a local location is exactly `str(Path)`**, so histories, bookmarks and a
  saved desktop keep the same bytes; a remote one is `sftp://user@host:port/path` (`file://` parses to the disk).
- **`Panel.location` is what a panel navigates** (reactive, seeded never bound). `Panel.path` is a property: the
  `Path` on the disk, `RemoteLocation` elsewhere -- so code not yet taught about drives fails loudly. Code that works
  anywhere reads `location`, `entry_location(entry)`, `drive`, `title_location`. `local_anchor` is the last local
  directory the panel read (set in `_apply`), where it goes back when its drive closes. **A feature reachable from
  any panel reads `path` only behind an `is_local` gate** (or `_LOCAL_ONLY`/`refusal`); wanting a disk directory,
  it takes `root.on_disk(location)` when `.is_local` (a `root:` panel is the disk) and else falls back -- Alt+Del
  scans through `drive_of(location).scan`, the editor's file box (`EditWindow._start_directory`) tries the other
  panel, the edited file, home; Execute OS command gives a remote *Find:* entry by name.
- **Every `Drive` method blocks and runs on a thread** (a remote one is a round trip; a local one may be a dead
  mount). The exceptions are the existing local single-syscall ones, which stay on `location.is_local` branches
  verbatim. `change_up()` is the one drive method a handler may call on the loop: it must be lexical.
- **Failures are `OSError`** with `errno`/`filename` where known; a drive gone is `DriveGone` (`ENOTCONN`, *Remote drive
  X is not accessible* -- DN's `TLinkDrive` free-space text). `filecopy.error_message` shows any of them.
- **The local fast path is unchanged.** `LocalDrive` makes the very calls the code made before drives (`os.lstat`,
  `os.scandir`, `os.replace`, `shutil.copystat`, `statvfs`, `fsync`); the listing functions moved verbatim to
  `drives/listing.py` and `panel.py` re-exports them. A test that patched `panel_module.scan_directory` patches
  `navigator.lib.drives.listing` now.
- **One copier and one eraser for every drive.** `filecopy._Copier`/`fileerase._Eraser` ask each end's drive
  (`drive_of`) for every step; a rename between sites raises `EXDEV`, so a move between drives copies and deletes
  like a move across file systems. `filecopy.stream` is the byte loop. Questions and `done` lists carry
  `shown(location)`: the plain `Path` on the disk, the `Location` elsewhere -- so `_watch_job`, `OverwriteQuery` and
  `untag_paths` are unchanged. `resolve_target`: `://` is remote, a bare absolute path is the disk (DN: only a
  prefix left it), a relative one is on the working directory's drive.
- **Capabilities grey commands, not errors.** `Manager._LOCAL_ONLY` is **empty**: every command asks the drive or
  works on a fetched copy; it is where a new command that cannot goes until it is taught to. What a drive cannot do
  at all its capabilities grey (`enables`): rename/move/delete/mkdir/F4 need `write`, Shift+F5 needs `symlink`, Alt+E's
  permission grid `chmod` (`gather`'s `can_chmod`), its owner `chown`, *Xattrs* `xattr`, *Flags* `fsflags`. File >
  Encoding > Checksums and Panel > Find duplicates read every file through `open_read`/`children`, so they need nothing
  more (duplicates: no inode dedupe where `st_ino` is 0, a quick hash of the head where a file cannot seek). **The
  capability set is exactly what is asked** (`write rename symlink hardlink chmod chown free_space xattr fsflags`):
  `tree`/`find`/`uucode`/`print`/`watch`/`exec` were declared and never read, and went -- add one only with the check
  that reads it. `free_space` is rclone's, asked of itself in `scan`.
- **The last ones, and how**: Shift+F4 reads its name as a copy's target line does (`target_location`: a URL, an
  archive place, or relative to the panel's drive) -- an existing file there is fetched and edited, a new one is an
  empty copy (`usefile.blank`) that F2 makes there (`$EDITOR` only for one already there). Shift+F5 makes a link on
  the destination's drive (`filelink.make_link` → `Drive.symlink`, relative by `posixpath`), only to a file on the
  same drive -- `EXDEV` otherwise -- the steps on a thread. *Make list* writes its file on the drive with that drive's
  own paths in it (`_make_list_elsewhere`); *Read file list* reads one there (`filefind.read_list_on_drive`: `/` the
  drive's top, a mask matched against a listing, `~` just a name). UU encode/decode (`Manager._staged`) fetch the
  input, write into a staging directory under `private_dir()`, and `usefile.put_files` the results up into the
  directory asked for -- its `ask` hook given those already there first, before anything is written:
  `uucode.ask_over_encoded` (anything but Yes/All abandons, as `encode` asks of the disk) and `ask_over_decoded`
  (*Check existing files*; No leaves one, Cancel it and the rest), `FileExists.path` then a `Location`. The
  dBase view fetches the file (`use_file.database_elsewhere`) and puts it back after every field edited.
- **What works anywhere, and how** (Phase 4): Alt+G counts through `Drive.children`
  (`dirlength._count_on_drive`); *Auto refresh* polls a drive with `polled = True` (SFTP, FTP, SMB) every
  *Communications* *Look for changes every* seconds (`[remote] refresh`, 0 off -- every look is traffic) through
  `base.PollWatch`, which lists on its own thread and calls only when names, sizes or times changed; Find and
  Directory branch walk the drive (`filefind._search_drive`, text by `holds_on_drive`; *disk*/*all* scopes start at
  the drive's top; links not followed), found entries carry `Location` directories (`DirEntry.path_in`,
  `listing._entry_elsewhere` re-reads them); the trees (Ctrl+T, Alt+T) root on the drive and read on threads
  (navml `TreeView.load_in_background`/`children_of`; `DirectoryTree.use_drive_of`, `show_elsewhere` walks the
  path on a thread and opens the branches when it lands; Alt+T's box makes directories through the drive);
  Ctrl+Q fetches the first `usefile.HEAD_LIMIT` (1 MiB) and shows that (`QuickViewer._show_elsewhere`); the
  information panel shows the place and `Drive.describe()` (server, host key, cipher, TLS, shares; an archive's
  kind, files, packed and unpacked) under *Connection* -- every name in `base.DESCRIBED`, which the catalogues list;
  *Compare* reads contents side by side (`dircompare.same_bytes`); *Print* spools a fetched copy; *File
  attributes* stats, chmods, chowns and utimes through the drive (`fileattr._stat`/`_children`/`_apply_elsewhere`),
  owners as numbers there (a server's ids are not this system's), changeable only where the drive can `chown`;
  the viewer's *Save as* takes a URL or an archive place (navml `FileDialog.raw`, a test for names handed back as
  typed; `viewer._save_elsewhere`, written beside and renamed over).
- **F3 reads a remote file a chunk at a time** (`viewer.ChunkedSource`), where the drive can read anywhere in it
  (`Drive.open_random` -- `SeekingReader` over a seekable `open_read` for SFTP (no `prefetch`), SMB and memory;
  `REST` + `RETR`, cut off with `ABOR`, for FTP; None for archives, which are fetched whole as before). The window
  is up at once, whatever the size. A chunk not in the cache (`REMOTE_CACHED_CHUNKS`, 32 MiB) raises **`NotYet`**
  after asking for it and `READ_AHEAD` more on the `nav-view-fetch` threads; when it lands, `arrived` tells the
  viewer (`FileViewer._chunk_arrived` → `call_from_thread` → `_chunk_landed`), which repaints and does again what
  was interrupted. **The rule that makes that safe**: every viewer method that reads is wrapped `@_when_here`
  (`seek`, `scroll_rows`, `to_end`, `show_hit`, `_snap_top`, `_to_longest_end`), and each reads everything before
  it changes anything -- so an interrupted one did nothing, and doing it again is doing it once; a caller above
  one carries on harmlessly. `render` catches `NotYet` (*Reading...*) and a failed fetch's `OSError`; `percent()`
  falls back to the offset. Search reads through the drive on its own thread (`ChunkedSource.find`, blocking);
  *Save as* streams the whole file from the drive (`stream()`); nothing is lexed (it would read everything); no
  view record is kept. A new method that reads must be wrapped the same way, or it raises `NotYet` into a handler.
- **The shell never follows a panel off the disk.** `_front_directory()` is None for a remote panel, so the subshell
  stays in its last local directory; the prompt stand-in names the panel's place (`drive.get_dir`, `SFTP:host:/path$`) and
  the shell's own prompt is hidden. `_follow_shell` moves a remote panel back to the disk only when the command
  `cd`'d (the shell's cwd changed during it) -- and never into a `UseFile` directory. A departure: DN's non-disk
  drives always kept their place across a command (`TFilePanelRoot.Store`).
- **No secrets on disk from Navigator.** A typed password lives in the connection (`Answers`) until it closes. *Save
  in keyring* is offered only when `credentials.keyring_available()` (the `keyring` package with a real backend), and
  every keyring call is on a thread. `save_password` answers None or why not; each drive's `connect` puts that on
  `Answers.keyring_refused` (the hop's for a jump host) and `Shell.reach` toasts it -- connected all the same. **A lost
  connection says why**: `Drive.lost_reason` (SFTP's reconnect, FTP's remake: `base.reason_of(error)`), kept by
  `SESSIONS.close(site, "lost")` and handed once by `SESSIONS.reason(site)` to `close_linked`'s *not accessible:
  {reason}*. A session listener that raises is logged (`errorlog.append`), the rest still told. Host keys are `ssh`'s: unknown → `HostKeyQuery` (Accept once / Save into
  `~/.ssh/known_hosts` as `[host]:port type base64`), changed → refused, no button accepts it.
- **Closing is DN's `cmCloseLinked`.** `SESSIONS.close(site, why)` unmounts the drive and tells every listener (on the
  closing thread); `Shell._heard_closed` hands it to the loop and `close_linked` sends each panel on the site to its
  `local_anchor`, saying *Remote drive X is not accessible* once for `"lost"`.

## Pieces

- **`location.py`** `Site`, `Location`, `LOCAL_SITE`, `RemoteLocation`. `normalized()` is by the letters (`..`, `.`).
- **`base.py`** `Drive` (TDrive's names: `get_dir` title, `real_name` copy target, `use_file`/`change_up`), `FileStat`
  (an `os.stat_result` look-alike; `st_dev`/`st_ino` 0 where there are none -- the copier's loop check falls back to
  site+path), capability constants, `DriveGone`. `Drive.quick_listing` (False; True for local, archive, memory,
  `root:`, Trash): whether a panel's read is worth its `SCAN_GRACE` wait -- set it on a new drive that answers here.
  `Drive.system_root` (False; True for SFTP, FTP and the exec drives): its `/` is a running system's, so Find never
  walks into its `/proc`, `/sys`, `/dev`, `/run` (`filefind.SYSTEM_PLACES`) -- set it on a new drive onto a machine.
- **`__init__.py`** `drive_of(location)` (`LOCAL` for the disk, the mounted drive for its site, else `DriveGone`),
  `mount`/`unmount`/`mounted`.
- **`memory.py`** `MemoryDrive("name")`, site `mem://name`; `make(path, data)`/`read(path)` for tests. POSIX errors where
  cheap; no owners.
- **`trash.py`** `TrashDrive`/`TRASH` on `TRASH_SITE` (`trash:///`): the freedesktop Trash
  (`navigator.lib.file_ops.trash`, `navigator-file-ops` *The Trash*). **No connection**: `drive_of` answers `TRASH`
  for the scheme without mounting and `Shell.reach` lets it through, so SESSIONS never sees it. The root lists every
  trash directory's items (a name shown already gets `.N`; `item(name)` re-reads when unknown), below it is the disk
  through `LOCAL`. Erasing only: `unlink`/`rmdir` of a root item also `forget()` its info file; making, writing,
  renaming are `EROFS`. `DirEntry.trashed` (origin, deletion time) is the panel's second info line. Watches the home
  trash's `files/`. Title `TRASH:/path`. The root lists `..` too: it and Backspace leave for
  `Panel.local_anchor`, the last local directory read (`Drive.leaves_to_anchor`, which `_go_up_elsewhere` reads where
  `change_up` answers None).
- **`sessions.py`** `SESSIONS.connect(site, answers)` (blocks; raises `NeedPassword`, `NeedPassphrase`,
  `UnknownHostKey`, `HostKeyChanged`, `DriveGone`), `close`, `close_all`, `reap(in_use, idle)`, listeners;
  `SCHEMES` (scheme → module with `available()` and `connect()`), `available(scheme)`, `EXTRA_HINT`.
- **`sftp.py`** (paramiko, the `navigator-fm[sftp]` extra, imported only when connecting). `_Connection`: one
  `SSHClient`, `~/.ssh/config` through `credentials.host_config` (hostname, user, port, IdentityFile, ProxyCommand),
  agent and keys, then the keyring's password, then the answers. A pool of ≤ `CHANNELS` `SFTPClient`s, each checked out
  by one thread (`_channel()`); a file opened keeps its channel until closed (`_HeldFile`). A watcher thread joins the
  paramiko `Transport` and, when it ends unasked, connects again once, else calls `on_lost` → `SESSIONS.close(site,
  "lost")`. `take()` makes a dropped connection again once too. **The channels are a `pool.Pool`, not a queue**
  (`navigator/lib/drives/pool.py`, FTP's connections too): a thread waiting for one is woken by one given back, a
  slot freed by one thrown away, a new generation (`open()` calls `reset()`; old-transport channels given back late
  are discarded uncounted) and `close()` (`PoolClosed` → `DriveGone`) -- a `LifoQueue` left it asleep through each,
  the progress box up for good. `Pool.take(make, wait=1.0)` answers None after *wait* so `take()` looks again at
  `alive`/`_closing`; `_new_channel` uses the transport as it is then (`_Between` while there is none). Reads `prefetch()`, writes `set_pipelined(True)`;
  `replace` is `posix-rename@openssh.com`, falling back to remove+rename. `mkdir` turns SFTP v3's bare *Failure* into
  `EEXIST` when the name is there. Owners come from the server's `ls -l` line (`DirEntry.owner`).
- **`ftp.py`** (`ftp://`, `ftps://`; stdlib `ftplib`, nothing to install). `_Pool` (over `pool.Pool`; `remake()`
  `adopt`s the one made in place of a dropped one): up to `CONNECTIONS` logged-in
  control connections, each one thread's (`FtpDrive._client()`); a file read or written (`_Transfer`, `RETR`/`STOR`/
  `APPE` over `transfercmd`) holds its connection until the reply after it. A connection is `NOOP`ed when taken and
  made again once if the server dropped it (servers drop idle ones); failing that, `on_lost`. No user is anonymous
  (empty password); a user without a password is `NeedPassword` (keyring first). Listing is `MLSD` (facts
  `type size modify unix.mode unix.owner unix.group`), else `LIST -a`, else `LIST` -- each learnt once
  (`pool.mlsd`, `pool.list_a`) -- parsed `ls -l` style (`_parse_list`); `stat` is `MLST`, else the parent's listing.
  Replies map to `OSError` (`_os_error`: 530 → `EACCES`, 550 → `ENOENT`/`EEXIST` by its words, 421 → reconnect).
  `chmod` is `SITE CHMOD` (also after `STOR` for a new file), `utime` is `MFMT`; no symlinks. FTPS is explicit
  TLS (`AUTH TLS`, `PROT P`) checked against the system's certificates. Title `FTP:host:/path`.
- **`smb.py`** (`smb://user@host/share/path`; `smbprotocol`'s `smbclient`, the `navigator-fm[smb]` extra). **The
  first name of a path is the share**; the root lists the server's disk shares, asked once per drive over RPC
  (`_ask_shares`: `smbclient.open_file("\\\\host\\IPC$\\srvsvc", mode="r+b", buffering=0, file_type="pipe")` and
  **`dcerpc.share_enum`**, a hand-written bind + `NetrShareEnum` level 1 -- smbprotocol has no RPC, impacket is
  large), `IPC$`, printers and the `$`-special ones left out, plus the shares known (the one opened on --
  `Answers.start`'s first name -- and any reached since). Any failure (guest refused, RPC off) leaves only the
  known ones, silently. `dcerpc.py` speaks to anything with `read`/`write`, keeps what one read brought past a
  fragment (`_Fragments`), and was checked against impacket's NDR (bind byte-identical, the request so but for
  referent ids, impacket's response decoded); no Samba was at hand to try it on. Each drive has its own
  `connection_cache` and passes `username`/`password`/`port` on every call; names are UNC (`_unc`). A failure of
  the connection itself (not an `OSError`) is `DriveGone`; `LogonFailure`/`AccessDenied` on connecting is
  `NeedPassword`. No user is the guest, or Kerberos with a ticket. No chmod or owners (Windows ACLs). `smb.CLIENT`
  is the module spoken through -- a test puts a stand-in there. Title `SMB:host:/share/path`.
- **`s3.py`** (`s3://[key@]endpoint[:port]/bucket/key`, `s3+http://` for plain HTTP; boto3, one of
  Navigator's own dependencies). **No new `Site` fields**: the scheme is the transport, the host the endpoint
  (`s3.amazonaws.com` / `s3.REGION.amazonaws.com` is Amazon's -- virtual-hosted, a bucket's region learnt once from
  `head_bucket`'s `x-amz-bucket-region` and a client per region; any other host an endpoint of its own by URL,
  path-style, region `us-east-1` unless `~/.aws` says), the user who (empty: the AWS chain; a `~/.aws` profile's
  name: that profile; else an access key ID whose secret is `NeedPassword`'s, keyring first). `connect` proves the
  keys with `list_buckets` (a refused one on `answers.start`'s bucket with `head_bucket`); bad keys
  (`InvalidAccessKeyId`, `SignatureDoesNotMatch`, ...) are a wrong password. **The first name is the bucket**; the
  root lists the account's buckets plus those reached by name; F7 there makes a bucket, rmdir deletes an empty one.
  **Directories are prefixes** (`list_objects_v2`, `/` delimiter, the `dir/` marker F7 leaves skipped). Writes are a
  multipart upload as they come (`_Upload`, `PART_SIZE` 8 MiB, one `put_object` when smaller; its `__exit__`
  aborts on an exception, so Stop or a failure leaves nothing); no append. A file's rename is a managed server-side
  copy and a delete; a directory's is `EXDEV`, the copier then copying and deleting. `open_random` is ranged GETs
  (F3 by chunks). No modes, owners, links or times. Unreachable after botocore's retries is `DriveGone`.
  `make_client` is the hook a test replaces. Title `S3:endpoint:/bucket/dir`; `describe` adds `Region`.
- **Containers and devices** (`execdrive.py`, `docker.py`, `podman.py`, `adb.py`; `docker://[user@]name/path`,
  `podman://...`, `adb://serial/path`). No file protocol at the other end, only `sh` and its tools (GNU, busybox,
  toybox): **every step is one process** through `ExecDrive._run` (the one seam -- a persistent shell can stand in
  later), a fixed `sh -c SCRIPT sh "$1" "$2"` script, **the paths always arguments, never written into the
  script**. `docker exec [-i] [-u USER] NAME words...` takes the words as they are; **adb joins its words into one
  line for the device's shell**, so `AdbDrive.argv` is `adb [-s SERIAL] shell -T shlex.join(words)` -- `-T` is
  shell protocol v2 without a pty: separate stdout/stderr, binary-clean, the exit status and stdin (Android 7+).
  - A listing is one `LIST` run: `stat -c STAT_FORMAT` (`%f %s %Y %X %u %g %h %i %U %G %n`, the name last) over
    the globbed names, then each link's `stat -L` and `readlink` after `LINKS_MARK`, then `df -Pk` after
    `FREE_MARK` when asked. `parse_stat` takes a line not starting with the numbers as the rest of the name before
    it (a newline in a name). A missing or unreadable directory is said in `strerror`'s words by the script
    itself, since dash's `cd` does not.
  - Failures: `os_error` finds `strerror`'s text (glibc, musl and bionic spellings) and answers the `OSError`
    subclass; else `EIO` with the words. The subclass's `lost(text, status)` says the other end is gone
    (`docker.LOST_WORDS`: *is not running*, *No such container*, the daemon; adb's *device 'x' not found*,
    *offline*, *unauthorized* → *Allow USB debugging on the device*) -- `on_lost`, then `DriveGone`.
    `docker exec`'s 126/127 *executable file not found* is *NAME has no shell (sh)*.
  - Steps: `RENAME` refuses an existing `$2` (`EEXIST`), `REPLACE` a directory there (`mv` would move into it),
    `unlink` looks first (`rm -f` says nothing of a missing file), `utime` is POSIX `TZ=UTC0 touch -a/-m -t`
    (whole seconds), `copy_attributes` mode and both times in **one** run.
  - **Data streams through pipes, not tar** (a departure from the item, recorded in the module): `open_read` is
    `cat -- path` (`_Reader`, killed on an early close, the exit status an `OSError` at EOF), `open_write` is
    `sh -c 'cat > "$1"'` (`_Writer`, the failure raised on `close`), so the copier counts per chunk, an
    overwritten file keeps its owner and inode (`docker cp`'s tar writes uid 0), and adb works the same.
    `open_random` is `tail -c +N | head -c COUNT` a chunk (F3 by chunks).
  - "Connecting" holds nothing: `docker inspect` (running? `Config.WorkingDir` is `home`, `Config.Image` for
    `describe`), `adb get-state` (`home` `/sdcard`; model and Android version by `getprop`). `polled` (Auto
    refresh looks again). Capabilities: containers write, rename, symlink, chmod, chown, free space; a device no
    symlink or chown (`/sdcard` is FUSE). Title `DOCKER:name:/path`, `ADB:serial:/path`. Names and serials keep
    their case (`location.AS_WRITTEN`); a networked serial `host:port` is the site's host and port
    (`adb.serial_of`, `Device.site`). `available()` names the missing command (`EXTRA_HINT` is the program).
    **adb off `PATH`**: Android Studio installs it in `~/Android/Sdk/platform-tools` (macOS `~/Library/Android/sdk`)
    and leaves `PATH` alone, so `adb.program()` tries `PATH`, then `$ANDROID_HOME`, `$ANDROID_SDK_ROOT` and those
    (`sdk_dirs`); every argv starts with `adb.command()` -- bare `adb` when `PATH` has it, else the full path (also
    `remote_shell.program("adb")` and its `adb shell -t`). conftest's `_no_android_sdk` empties `sdk_dirs` so no
    test finds the developer's SDK; the lookup's own tests put back `adb.SDK_DIRS`.
  - What is there now: `docker.list_containers(engine)` (`ps --format '{{json .}}'`, Docker's lines and
    Podman's array with `Names` a list -- `parse_ps`) and `adb.list_devices()` (`devices -l`, `parse_devices`).
- **rclone** (`rclone.py`, `rclone://REMOTE/path`; the `rclone` command, nothing to pip-install). **One
  `rclone rcd` a connection** (`Daemon`), on a Unix socket of its own (`_socket_path`: `$XDG_RUNTIME_DIR`, else
  `private_dir()`, else a `mkdtemp` -- the first whose path fits `sun_path`, `_SOCKET_LIMIT` 100; pytest's
  `tmp_path` would not) with `--rc-no-auth` (the directory, this user's alone, is the guard), `--rc-serve` and
  `--ask-password=false`, `start_new_session`. **Before 1.63** (Ubuntu 24.04's 1.60) `unix://` is taken for a
  host and port (*lookup tcp ... unknown port*, `_NO_UNIX`): started again on `127.0.0.1:0`, the port read from its
  *Serving remote control on* line (`_Log`, which reads standard error throughout and keeps it only until up), a
  random user/password in `RCLONE_RC_USER`/`RCLONE_RC_PASS` (environment, not argv) sent as basic authentication by
  `_TcpConnection.putrequest`; `_tcp_only` remembers it for the next daemon (a test resets it). Every step is a JSON POST to the rc over `_UnixConnection`
  (`operations/list`, `stat`, `mkdir`, `rmdir`, `deletefile`, `movefile`; `sync/move` for a directory where
  `fsinfo`'s `Features.DirMove`, else `EXDEV`; `about` for the free space, `FREE_SPACE` only where
  `Features.About`); rclone's refusal (`{"error", "status"}`) is `os_error` by its words, else its status. Reads are
  `--rc-serve`'s `GET /[REMOTE:]/path` streamed (`_Body`), F3's chunks ranged GETs (`_RangeReader`; a 200 for a
  range is sliced, a 416 empty). **A write is one chunked multipart POST to `operations/uploadfile`** (`_Upload`;
  `fs`/`remote` in the query, the name in `filename*=UTF-8''`), sent as the copier writes -- rclone's `Rcat`
  reads the part as it comes; the answer read on close, an exception cuts the socket. No append, modes, owners,
  links or times (`copy_attributes` does nothing: an object's time is its upload's). **The host is the remote's
  name**, as written and percent-encoded in the URL (`location.AS_WRITTEN`; `Site.__str__` quotes such a host: a
  name may hold a space or `@`); the path is from the remote's root (`REMOTE:` + the path less its `/`) -- an
  sftp/local remote's root is where its config says, so the real-rclone test uses an `alias`. An **encrypted
  config** is `NeedPassword` (rcd ends at once with *RCLONE_CONFIG_PASS*/*decrypt* words, `wants_password`;
  `wrong` when one was given), given only in the daemon's environment, kept in the keyring under `Site("rclone")`
  (one config, one password); `Shell.reach` asks it as *Password for rclone's configuration*. A daemon gone is
  started again once silently (`_revive`), else `on_lost` → `DriveGone`. `connect` asks `fsinfo` (features; *didn't
  find section in config file* is no such remote -- not `config/listremotes`, which leaves out a remote set up in
  the environment), `config/get` for its backend, else `RCLONE_CONFIG_NAME_TYPE`. `describe`: *Remote*, *Backend*, *Software*,
  *Hashes*. Title `RCLONE:name:/path`. **Its link manager** (Utilities > Link > *~r~clone remote...*,
  `RcloneLink`) is **live**: *── Configured ──* over `rclone listremotes --long` (`list_remotes`/
  `parse_listremotes`, on a thread); `_entry` takes the *Re~m~ote* line whole (no `split_host`: an `@` is the
  name's), no user or port; *Confi~g~ure...* (`configure`, rclone's only) closes the box with
  `ConnectRequest(configure=True)` and `Shell.configure_rclone` runs `rclone config` in a window that stays.
  `ConnectDialog` (F2 in the Link box, *Saved links*) has *~R~emote* likewise. No Remote shell entry: there is
  nothing to run there.
- **Each protocol is named and has its own entry**, all in Utilities > **Lin~k~ ▸** (`utilities_link`; a
  departure, asked for: one entry a protocol, grouped, no box first asking which): *SSH (SFTP)...* (Alt+F11,
  `NavyLink`), *FTP...* (`FtpLink`), *SMB (Windows share)...* (`SmbLink`), *S3 (Amazon S3)...* (`S3Link`),
  *GVfs/KIO...* (`GvfsLink`), *Docker container...* (`DockerLink`), *Podman container...* (`PodmanLink`),
  *Android device (adb)...* (`AdbLink`), each `Shell.navy_link(panel, scheme=)`; the
  `ConnectDialog(scheme=)` is that protocol's (`titles(scheme)`), FTP's with *Encrypt with TLS (FTPS)* (`secure`,
  the scheme then `ftps`), SMB's *Directory* captioned *Share/dir* (a share typed without `/` is made `/share`),
  S3's *Endpoint* (opening on `s3.amazonaws.com`), *Access key* and *Bucket/dir*, its `secure` box *Encrypt with
  TLS (HTTPS)* (unticked: `s3+http`); `reach()` asks S3's password as *Secret key for ...*.
  The recent list is the protocol's (`recent.recent(("ftp", "ftps"))` for FTP's box). The Link list has a *New ...
  link* per protocol (its mapping is the scheme), each greyed with its extra when missing. `sessions.PROTOCOLS`
  names them all.
- **SSH extras**: `ProxyJump` in `~/.ssh/config` (`a,b`, `user@host:port`, `ssh://` hops; `credentials.jump_site`)
  is `HostConfig.jumps`, and `_Connection.open` chains them natively: each hop logged into by `_login` (its own
  `host_config`; the first hop's own `ProxyCommand` honoured, a hop's own `ProxyJump` not followed), the next one
  reached over its `direct-tcpip` channel (`_forward`), the server last. Every hop's host key, password and
  passphrase are asked as the server's are, the question's `hop` naming it (`(host, port)`, None for the server)
  and its answer kept in `Answers.for_hop(hop)`; a jump host's password is saved to the keyring at once, the
  server's by `connect`. The hops' clients are `_Connection.chain`, closed after the server's in reverse; `_watch`
  watches only the last transport (a dying hop ends it, and the one reconnect rebuilds the chain). An explicit
  `ProxyCommand` still wins, through `paramiko.ProxyCommand`. **Keyboard-interactive** (a one-time
  code, a PIN): `Answers.interactive` -- set by `Shell.reach` (`_interactive_asker`) -- is called on the connecting
  thread with the server's prompts and waits while the loop shows a box per prompt (masked unless the server says
  echo), as a copy's worker waits for its questions; tried after a password fails or when there is nothing else to
  try. paramiko's own fallback for a second factor after a key, `auth_interactive_dumb`, reads **stdin** -- the
  screen -- so `connect` is given a `transport_factory` whose `Transport` routes it through `interactive` too.
  Cancelling a prompt is `DriveGone` ("Cancelled"), not a password box.
  **Port forwards** (a departure, asked for: DN's cable had no ports): `forwards.py`. A connection's are
  `RemoteProfile.forwards`, one a line in `ssh`'s words (`L [bind:]port:host:hostport`, `R ...`, `D [bind:]port`;
  `[v6]` bracketed, `/` for `:` too, `#` comments), `Forward`/`parse(strict=)`/`render`/`describe`/`ssh_words`.
  **Both ends use them**: Remote shell's `ssh` gets `-L/-R/-D` after the connection's options
  (`remote_shell.command(..., forwards)`), and an SFTP panel's paramiko connection opens them while it is up --
  `Answers.forwards` → `_Connection.forwards` → `Tunnels(transport, ...)` at the end of **every** `open()` (so the
  one silent reconnect reopens them; `close()` stops them first). `L`/`D` are a listening socket here
  (`create_server`, the loopback unless a bind is named, `*` every address; accept loops poll `POLL` for the stop
  flag -- closing a socket does not wake `accept()` on Linux) and a `direct-tcpip` channel a connection; `D` first
  reads SOCKS 4/4a/5 (`socks_request`, no auth, CONNECT only). `R` is `transport.request_port_forward` -- paramiko
  keeps **one handler for all of them**, so `_arrived` tells them apart by the server's port. Each pair is pumped by
  one thread over a selector. A forward that cannot open (port taken, server refusing) is in `Tunnels.opened`'s
  `error`, never raised; the info panel's *Forward* lines (`base.DESCRIBED`) show each, with its bound port and any
  error. Which forwards: `Shell.reach(target, forwards=None)` -- the link manager passes the lines' (`[]` for a
  one-off), anything else (Link box, saved desktop, `nav sftp://`) `profiles.forwards_for(site)`, the first
  profile by `seq` for that scheme/user/host/port. Forwards only open with a **new** connection: one already up
  keeps what it has. `profiles.save`/`replace` take `forwards=None` to keep a row's own, as `options`.
  `tests/sftp_server.py` answers `tcpip-forward` (`check_port_forward_request`) when `forwarding=True`.
  **Copy key** (`ssh-copy-id`): the SSH manager's *Copy ~k~ey...* picks `credentials.public_keys()` (`~/.ssh/*.pub`,
  `DEFAULT_KEYS` first; several: a `PopupMenu`; none: asks to make `id_ed25519` with `ssh-keygen` first), settles a
  changed connection, then **closes the box** with a `ConnectRequest(copy_key=, generate_key=)` -- a command window
  is the desktop's and the desktop is under every dialog, so it cannot open over the box -- and
  `Shell.copy_ssh_key` runs `remote_shell.copy_id_command` in a window that stays (`closes=False`), where `ssh` asks
  the password. Only `-o`, `-F` and `-J` (as `-o ProxyJump=`) of the options reach `ssh-copy-id`. Needs no paramiko;
  refused with a note when `ssh-copy-id` is missing (`remote_shell.copy_id_program`).
- **`credentials.py`** `host_config`, `fingerprint` (`SHA256:...`), `save_host_key`, `keyring_available`,
  `saved_password`/`save_password`/`forget_password` (service `navigator-fm`, account `str(site)`).
- **`profiles.py`** over `navigator/models/remote_profile/` (`remote_profiles`: name unique, scheme, host, port, user,
  path, seq). `location_of(profile)`; a path of `.` (`profiles.HOME`) opens on the server's home (`drive.home`).
  **Utilities > *Saved links*** (`EditLinks`, `Shell.edit_links`; also *Edit links...* at the foot of the *Link*
  list, `link_section`'s `EDIT_LINKS`) is `widgets/drives/links_dialog`: the profiles copied in as
  `profiles.Entry`s (`entries()`), edited -- F2/*Edit* and Ins/*Add* (a protocol menu first; *New GVfs/KIO link* asks the URI
  first, `navigator-gio` skill) in `ConnectDialog(editing=True)`, Del/*Delete* asked, Ctrl+Up/Down moved (its `LinkList` lets those keys past the
  list to the `links_dialog` key table) -- and written back on OK in one transaction (`profiles.store`: gone names
  deleted, `seq` the list's order); Cancel changes nothing; *Connect* stores, then `go_remote`s the active panel.
- **`recent.py`** over `navigator/models/recent_link/` (`recent_links`: scheme, host, user, port, path, seq; unique
  by scheme+host+user+port, the directory the last one used). The SSH link box's Host `▐↓▌` drops these as
  `choices`, not a `HistoryEntry` list: `ConnectDialog` replaces its `host.history.choose`, so a pick fills host,
  login, port and directory together. `Shell.navy_link` remembers a connection only once it worked. As long as
  Interface's *History size*.
- **`archive.py`** DN's `TArcDrive` (`ARCVIEW.PAS`): `ArchiveDrive` over `zipfile`/`tarfile` (any compression
  `tarfile.open` reads), and over **`arctool.ToolArchive`** for 7z and rar, told by signature (`arctool.kind_of`):
  7-Zip's command line (`7zz`, `7z`, `7za` -- no rar codec in `7za`), and for rar **`unrar` first** (`tool_for`;
  7-Zip 23's codec decrypts no encrypted rar -- *Unsupported Method* -- and fails `7z t` on a rar5 symlink), 7-Zip
  the fallback; listed with `7z l -slt -ba` (`parse_slt`; `unrar lta -c-`, `parse_unrar`, which skips `Type:
  Service` blocks -- `QO`, the quick-open record a larger rar carries, would otherwise list as a file), each member
  read through a pipe from `7z x -so -spd --` (`-spd`: a name is never a wildcard; `_Piped` kills the tool on an
  early close and turns its exit status into `OSError`), links' targets read as their contents -- except where the
  listing names them (`ToolInfo.target`: unrar's `Target:`, 7-Zip's `Symbolic Link` for a rar; `unrar p` prints a
  link as nothing and `7z x -so` fails on one). Nothing bundled:
  no tool is **`NeedsTool`** (a `NotAnArchive`), which Enter says rather than running the file. A 7z is rewritten by
  `_write_tool` -- the old one unpacked once into a tree (solid blocks are whole), the index laid out over it, packed
  anew by `arctool.write_archive` (`7z a -snl`, `-mx<level>`); `.7z` is in `NEW_KINDS`. **Passwords** (7z and zip,
  7-Zip only): `ToolArchive(local, kind, password)` gives 7-Zip the password **on stdin, never `-p<pw>`** (which `ps`
  shows) -- no `-p` at all, `start_new_session` so it has no terminal to ask on, the password and a newline as input;
  `write_archive` passes a bare `-p` (it then reads the password twice) with `-mhe=on` (7z: names too) or
  `-mem=AES256` (zip). unrar is fed the same way (no `-p-` any more); a wrong password makes it ask again and,
  its input spent, abort with **255**, a missing one with encrypted names exit **11** -- both are refusal
  (`_refused`), and a file-only encrypted rar (`Flags: encrypted`) is checked with `unrar t` on its smallest file.
  **Writing a rar** is RARLAB's `rar` (not free, never required; `arctool.rar_program`): `write_rar` -- `rar a -r
  -ol -y -idq -m<0..5>`, `-hp` with the password twice on stdin (names encrypted too), the target unlinked first
  (rar adds to what is there); an empty tree is refused (`ENOTSUP`), since rar deletes an archive emptied of its last
  member. Without `rar` a rar is read-only (`capabilities` empty) and RAR is greyed in *Create archive* (*RAR needs
  rar*). A wrong or missing one is `arctool.NeedPassword` → **`archive.NeedPassword`** (a
  `NotAnArchive`): listing fails with *Wrong password* (encrypted names), or a member says `Encrypted = +`
  (`ToolInfo.encrypted`) and `7z t` on the smallest fails. A zip with an encrypted member (`flag_bits & 1`) is read
  through `ToolArchive(kind="zip")` -- `ArchiveDrive.tool` is which back-end, `kind` stays `zip` -- and rewritten by
  `_write_tool` with its password, so it stays encrypted; a password given for an archive that is not encrypted is
  dropped (`_load`). `widgets/drives/archives.open_archive_or_root` asks it (`ask_archive_password`, a
  `PasswordDialog`), again after a wrong one; Cancel is `Stopped`, never the `NotAnArchive` that would run the file.
  **`.tar.zst`** (`zstd.py`): `compression.zstd` (3.14+) else the `zstd` command, neither is `NeedsTool`; `tarfile`
  wants to seek, so `_open` decompresses it whole into a private `.tar` (`ArchiveDrive._plain`, deleted on close and
  on re-reading) and `_write_tar` writes a plain tar and compresses it (`--ultra` above 19). A rar is writable only where `rar` is installed. `_Member.packed`/`DirEntry.packed` carry the packed size (a zip's `compress_size`, 7-Zip's *Packed
  Size* -- blank for a solid block's later members; None for a tar). A place in one is `Location(Site("arc"), inner, outer=<the archive's location>)` -- `outer`
  is DN's `Prev` -- printing as `/dir/a.zip#/inner`; `Location.parse` reads that back when the name before `#/` is in
  the *archive* file type (`a.zip#//` is the root too), and so does the copy target line (`filecopy.target_location`).
  `drive_of` finds it by its `outer` (`archive.find`). `open_archive(outer, job, create=)` reads the whole index (a
  compressed tar: the whole file), fetching one on another drive first (`UseFile`; the copy goes with the drive).
  Implied directories are listed; a tar's owners are `uname:gname`; links are followed inside the archive; devices,
  FIFOs and hard links in a tar are not listed (and a rewrite drops them). Reads share one file, one at a time
  (`_Locked`). Title `ZIP:a.zip:/inner` (`get_dir`, DN's `ZIP:C:A.ZIP\INNER`). `..` is always listed; at the root
  `change_up` is `(outer.parent, outer.name)`, so the cursor lands on the archive.
- **The read-only kinds and the single compressed file** (none DN's; `members.py`'s `ListedArchive`, the
  shape `ToolArchive` has -- `infolist()` of `ToolInfo` (now with `owner`, and `ref`, the back-end's handle),
  `open(info)`, `read_link`, `details()` for `describe`, `close()` -- so `ArchiveDrive.listed` indexes and reads
  them as it does 7-Zip's). `_open` tries, by content: 7z/rar; **squashfs** (`squashfs.offset_of`: `hsqs` at 0,
  or a type 2 **AppImage** -- `AI\x02` at ELF byte 8, the image at `e_shoff + e_shentsize*e_shnum`) through
  `unsquashfs` (`-lls -full -UTC -d ''`, `parse_lls`; a file read by `-no-wildcards [-o OFF] -cat` through a
  pipe, extracted to a private directory before squashfs-tools 4.6 had `-cat`; missing is `NeedsTool`
  *install squashfs-tools*); **`ar`** (`debpkg.parse_ar`, GNU and BSD names) -- a **deb** when `debian-binary`
  is there, laid out as `dpkg-deb -R` unpacks it (data at the root, the control tar under `DEBIAN/`, each tar
  decompressed whole into a private plain one; hard links listed, read as their target; `Package` from
  `control`), else the raw members (`ArArchive`, a `.a`); **rpm** (`rpmpkg`: lead, signature header padded to 8,
  header -- NAME/VERSION/RELEASE/ARCH for `Package` -- then the payload by magic, gz/bz2/xz/lzma/zst/none,
  decompressed into a private cpio; rpm 4.12's stripped `07070X` is `NeedsTool`); **cpio** (`cpio.parse`:
  newc, crc, odc, old binary either order; members read by `members.window`'s `pread`; a `newc` hard-link
  group reads the name that has the bytes; devices and FIFOs not listed); then a **compressed** file: a tar as
  before, a cpio (`.cpio.gz`, an initramfs, decompressed to a plain one), else **one compressed file**
  (`stream.py`, kind `STREAM`: one member named as gunzip names it, `member_name`; its size counted by one
  pass on opening; `sign` the compression's, `GZ:app.log.gz:/`). `READ_ONLY_KINDS` (deb, rpm, cpio,
  squashfs, ar) have no capabilities and every mutator is `EROFS` (`_refuse`: a target line can still name
  one). A `STREAM` has `write` only: its one member may be written over (F4's F2 -- `usefile.upload` writes
  straight over it, there being no `rename`) and `utime`d, and `finish` compresses it anew the same way
  (`_write_stream`, `stream.writer`, zst through `zstd.compress`); anything else is `EROFS`. The decompressing
  passes take the opening's `job` (`members.stopped_check`). `*.squashfs;*.sqfs` joined the *archive* file
  type; **`*.appimage` did not**, so Enter still runs one -- **Ctrl+PgDn** (`GoInto`, DN's `_CtrlPgDn`: a
  directory, `..` and a *Find:* entry as Enter; on a file, which DN's left alone, a departure) and File >
  Archive > *Open archive* (`OpenArchive`, `Panel.open_as_archive`, a regular file outside an archive) open
  any file by its content, `enter_archive(forced=True)` saying *{name} is not an archive Navigator can read*
  rather than running it. `tests/test_archive_formats.py` builds every kind in the test (squashfs with
  `mksquashfs`, skipped without squashfs-tools).
- **Writing an archive is a rewrite** (DN's packers rewrote too) **at a level**: `ArchiveDrive.level` (one of
  `LEVEL_NAMES`: store/fastest/normal/maximum/ultra, `normal` unless *Create archive* said) is
  `LEVELS[(kind, compression)]` to each writer -- deflate level (*store* = `ZIP_STORED`, new members only; old
  ones keep theirs), gzip/bz2 `compresslevel` (bz2's is only its block size), xz `preset` (*ultra* `|
  PRESET_EXTREME`), zstd level, 7-Zip `-mx`; a level a format has not got is missing (no *store* for a compressed
  tar), a plain tar has none. `ArchiveOptions(level, password)` rides on `CopyRequest.archive` into
  `_open_target_archive`, which also sets the level on one there already. every step -- `open_write`, `mkdir`, `rmdir`,
  `unlink`, `rename`/`replace`, `symlink`, `chmod`, `utime` -- changes the in-memory index under `_tree`, a new file's
  bytes staged in `private_dir()/archive/<pid>/`; **`Drive.finish()`** (a no-op elsewhere) writes the whole archive
  anew beside it (`.name.XXXX`), each zip member keeping its compression, a tar its compression (`_compression_of`,
  by magic bytes) and owners, then `os.replace`s it over, re-reads it, and for a fetched one uploads it back.
  **`finish(job)`** counts the packing into a copy's job (`total_bytes`/`done_bytes`, `source` the member,
  `file_bytes`/`file_done`) and raises `Stopped` between chunks -- the temp file removed, the archive as it was;
  **`discard()`** drops the unwritten changes (index re-read, staging deleted). The copier sets `job.packing` (and
  `dest` the archive) around `finish_drives(..., job=)` for a target in an archive: the progress box says *Packing*;
  Stop there discards (`filecopy.discard_drives`) and reports nothing done. **A move into an archive holds each
  source's removal** (`_Copier._held`, `_remove_source`) until the archive is written and not `dirty`
  (`_remove_held`) -- a pack that fails or is stopped loses nothing; before, sources went as each file was staged.
  **Whoever makes the steps calls `finish` once at the end**: the copier and eraser (`filecopy.finish_drives` over
  sources and target, also after Stop -- what went in full stays), `Manager.make_directory`/`_rename_entry`, and
  `usefile.upload` (the editor's F2). A copy whose target names an archive not open opens it, or -- named but not
  there, with a name in `NEW_KINDS` -- makes an empty one (DN's `ArchiveFiles`, packing by the target's name), and
  lets go of it after (`release_unheld`). **On another drive too**: `open_archive(create=True)` on a remote name not
  there makes it in a private copy (`usefile.blank`, the file removed so the first `finish` makes it) and `finish`
  puts it there (`_put_back`). A panel holds the archive it is in (`Panel._hold_archive`;
  `archive.hold`/`leave`), the last one out closes it on a thread (which finishes first); `Navigator.on_stop` closes
  the rest.
  **Changes a rewrite could not make are never dropped unasked.** `dirty` is `_dirty or _unsent` -- `_unsent` an
  archive from another drive rewritten here whose `_put_back` failed (a later `finish` only uploads); `discard()`
  clears both. `archive.pending()` lists the open dirty ones. `navigator/widgets/drives/archive_finish.py`:
  `finish_pending(app, drives)` writes each under a progress box and on failure asks *Try again?* (Yes again, As root
  first for a refusal on the disk, No `discard`s, Cancel stops); Alt+X's `_quit_asking` runs it over `pending()`
  after the windows (Cancel stays), and a panel letting go of a dirty archive spawns `let_go` (Cancel:
  `archive.keep_open`, held by no one, so quitting asks again; no loop running: kept for `close_all`). `close()`
  logs a failed `finish` to `errors.log` (`errorlog.append(error, context)`) -- only a non-interactive exit gets there.
- **Entering**: Enter (`Panel.choose` → `_may_enter_archive`) with File Manager Setup's *Enter opens an archive*
  (`enter_opens_archive`, DN's `fmoEnterArchives`), on a file the *archive* file type names, from a panel not in an
  archive (DN opened none from inside another): `widgets/drives/archives.enter_archive` opens it under *Reading
  archive*; `NotAnArchive` (a `.zip` that is not, a `.deb`) runs it as a file instead, as `ArcViewer`
  failing fell through to `ExecFile`. The name test is a departure: DN tried every file by signature, which would
  take a `.docx` (a zip) in. Inside one, F5/F6/F8/F7/rename/F4 work as anywhere; no bookmark or quick directory is
  kept there, history skips it, and a saved desktop keeps the archive's directory with the cursor on it.
- **Extract to, Test, Shift+F2** (`ARCVIEW.PAS` `HandleCommand`/`ExtractFiles`, `FLPANELX.PAS` `cmExtractArchive`):
  File > Archive > *Extract to...* (`ExtractTo`, cmExtractTo) and *Test archive* (`ArcTest`, cmArcTest), enabled only in an
  archive; Files > *Extract archive...* (`ExtractArchive`, Shift+F2) only outside one, on archive-type files.
  `ExtractDialog` is `dlgExtract` (*Extract to* on the Copy history, *Extract with path names* ticked, *Test only*,
  Tree) less *Password* (zipfile knows only ZipCrypto); an empty line is the archive's own directory. Extracting is
  the copier (`Manager._extract` → `_run_copy`), the Copy dialog's session mode and options, without paths
  `CopyRequest.flatten` (`_Copier._flattened`: every file under a directory into the target). Shift+F2 opens each
  archive on a thread, extracts its root's children, then `release_unheld`. Through `_run_copy`, the panel showing
  the target lands on the first thing extracted, as F5's on what it made (path names are kept from where the panel
  is in the archive, so that is always right in the target). Test is **`ArchiveDrive.test(job,
  locations)`**: every member read through (zip CRCs, tar reads; 7z `7z t`, rar `unrar t`, whole), `(path, why)` per failure,
  said in a box. **Departure, recorded**: DN put Extract/Test/Password on F4/F6/F7 of an archive panel's key bar
  (`hcArchives`); here F4 and F6 stay Edit and Rename/Move, which work in an archive.
  **Shift+F2 extracts everywhere** (a departure, asked for): outside an archive it is *Extract archive*, inside one
  `Manager.on_extract_archive` runs *Extract to...* -- so File > Archive > *Extract to...* shows Shift-F2 as a static key (the
  binding is `ExtractArchive`'s). The panel's right-click menu offers *Extract to...* and *Test archive* in an
  archive, and *Extract archive...* on an archive file outside one (`panel._archive_file`). **Shift+F1, File > *Create
  archive...*** (`ArchiveFiles`, `cmPanelArcFiles`; DN's caption *Copy to archive*, renamed -- a departure, asked
  for; *Compare files* moved to `~l~` to free the `i`) is **`ArchiveDialog`** (`widgets/file_ops/archive_dialog`,
  DN's `dlgArchiveFiles`, 64x18): *Archive to* (Copy's history), *Archive type* (`FORMATS`: ZIP 7Z TAR TAR.GZ
  TAR.BZ2 TAR.XZ TAR.ZST RAR), *Compression* (None/Fastest/Normal/Maximum/Ultra; *None* is `store`), *Password*,
  *Store pathnames* (off = `CopyRequest.flatten`), *Move files*, *Follow symlinks*, Tree (keeps the name). After
  it the panel showing the archive's directory lands on the archive (`_run_copy`'s cursor steps out through
  `Location.outer` from where the first file went). The type
  and the name's ending follow each other (`_kind_changed`/`_name_changed` effects); levels and password a type
  has not got are greyed (`RadioButtons.enable_mask`, navml's `TCluster.EnableMask`); a type with no tool
  (`archive.format_missing`) is greyed and said on the row above the buttons. OK (`confirm`): a name with no ending
  gets the type's, a password is asked again (`dlgReenterPassword`), an existing file is *Add to it* / *Replace*
  (`ask_add_or_replace`; existence asked on a thread); type, level and boxes are remembered for the session, never
  the password. The request is a copy (`Manager.archive_files` → `_run_copy`, mode *Ask*) into the archive's root,
  which the copy makes; `Manager._archive_place`: named after the one entry (its archive ending, else its last
  extension, dropped), else the directory; in the other panel's place when it can be written (never inside an
  archive), else this one's -- any drive. Departures: today's formats for DN's ARC..ZOO, *Store*/*Ultra* added, no
  *Additional options* or *Force mode* (no per-format archiver to pass them to), *Follow symlinks* added.
- **Archive columns** (`TArcDrive.Init`'s `ColumnsDefaults.Arc`): `Panel.archive_columns`, seeded from *Column
  defaults*' *Archives* (`[column_defaults] arc_*`) each time an archive is entered (`_hold_archive`), is
  `shown_columns` in an archive; `packed` (*Packed*, `display_packed`) and `ratio` (*%*, `display_ratio`, DN's
  `Percent(Size, PSize)`, 100 for an empty file) count only there (`Panel.ARCHIVE_ONLY`) and drop before the path
  and date. Alt+K in an archive is `dlgArcParms`' boxes (`ColumnsDialog(archive=True)`); *Full* is `ALL_COLUMNS`.
- **Not done, on purpose**: a symbolic link from one drive to another (Shift+F5 across drives is `EXDEV`) -- a path
  on one drive means nothing on another, and DN had no such thing.
- **`usefile.py`** DN's `UseFile`: `fetch(origins, job)` into `private_dir()/remote/<pid>/<site-hash>/<mkdtemp>/`,
  `changed`, `conflicts` (the original changed since), `upload` (written beside as `.name.nav-XXXXXX`, chmod, `replace`
  over), `discard`, `sweep` (dead processes' directories, at start, on a thread; nothing is made just to look).
  `changed` compares size and `mtime_ns`, and the copy keeps the original's time -- so a copy whose recorded time is
  within `RACY_NS` (2 s) of the moment it was recorded also keeps a SHA-256 (`_stamp`, git's "racy" case), compared
  when size and time agree: a same-size write in the same clock tick was once missed (and `test_elevate` flaked).
- **Loop side** `navigator/widgets/drives/`: `use_file.py` (`materialize`, `put_back` under `[remote] upload_changed`
  ask/always/never, `view_elsewhere`, `edit_elsewhere`), `connect_dialog` (`ConnectRequest`, `split_host`),
  `password_dialog` (navml `InputLine.password`: stars, nothing copied), `host_key_query` ("once"/"save"/None).
- **`Shell`**: `reach(location)` (the connect loop: progress box, then each question, retried), `go_remote(panel,
  location)`, `navy_link(panel)`, `hang_up()`, `close_linked`, `reap_connections` (Navigator's `call_every(60)`),
  `_use_panel_files`/`_open_elsewhere`/`_put_back` (Enter, F2's menu and associations on fetched copies; `run_command`
  takes `cwd=` and `uses=`, which `command_finished` offers back). `Navigator.on_stop` closes every connection.
- **`Manager`**: `link_section(menu, before=toggle)` in the bookmark box -- the bookmarks' keys act on a profile
  there (`_profile_key`): F2 edits it (`ConnectDialog(editing=True)`: saved through `profiles.replace`, never
  connected, no paramiko needed), Del removes it unasked, Ctrl+Up/Down `profiles.move` it; the box opens again
  with *Link* dropped on the same row (navml `PopupMenu(submenu=(index, current))`); with any profile there, the
  key bar says *F2 Edit*, *Del Delete*, *Ctrl+↑↓ Move* while the list is open (`SubMenu.hints`; `Up/Down` in the ASCII tier); `_go_to` connects a URL through
  `app.shell.reach`; F3/F4/Alt+F3/Alt+F4/`$PAGER`/`$EDITOR` fetch first. `EditWindow.use_set`: F2 writes the copy and
  `put_back(ask=False)`; the title names the origin; no edit record; closing discards. `FileWindow.use_set` the same.
  **A copy that did not go back is unsaved.** `put_back` is True only when the drive has the copy (sent, or nothing
  changed); False -- failed (said), declined, a clash refused, stopped, `never` -- sets the window's `unsent`
  (`EditWindow` reactive: title marked, `must_ask`, Save all and F3's load ask; `FileWindow`/`DBWindow` plain, hex
  Shift+F2 and a field edit). Closing then asks `offer_upload` (Yes tries again and stays on failure, No drops the
  copy, Cancel stays); a retry is sent because `_stamp` moves only on success. F3 loading another file into a
  remote editor lets its copy go. `Shell._put_back` (programs) still discards after saying a failure.
- **Commands** `NavyLink` (Utilities > *Link* > *SSH (SFTP)...*, Alt+F11 -- DN's *Navigator Link*, renamed for its
  protocol), `HangUp` (*Disconnect*, Alt+H; greyed with
  nothing mounted), `SetupLink` (Options > Configuration > *Communications...* → `CommunicationsPage`, `[remote]`
  keepalive, timeout, idle_disconnect, upload_changed, ssh_options).
- **The link managers** (`navigator/widgets/drives/link_manager/`, `LinkManagerDialog(family=...)`, after
  FileZilla's Site Manager; a departure, asked for): one a protocol, one component. Each Utilities > *Link* entry
  opens its family's (`Shell.link_manager(panel, family)`; `navy_link` with no request and `gvfs_link` go there, so
  the Link box's *New ... link* items do too); each Utilities > *Remote shell* entry opens its family's in
  `mode="shell"`. Each lists only its family's profiles (`entries_for(family)`, read
  on a thread by the caller; `family_of(scheme)` maps back), the lines on the right under `ConnectDialog`'s ids,
  *Name* (`label`) on top, then `host`, `user`, `port`, `directory`. `FAMILIES` and `_dress()` hold what differs:
  - `sftp` -- as below; histories `ssh_*`. `ftp` -- lists `ftp`/`ftps`; the `secure` box (*Encr~y~pt with TLS
    (FTPS)*) is the scheme, unticked to start. `smb` -- *Sh~a~re/dir*, a leading `/` added (`rooted`). `s3` --
    lists `s3`/`s3+http`; *End~p~oint* (one-off and New start at `AWS_HOST`), *Access ~k~ey*, *~B~ucket/dir*
    (rooted), the box (*HTTPS*) ticked to start. `gvfs` -- the backend's `link_schemes()` less Navigator's own
    (`schemes_of`): *Name* and a `uri` line alone (`uri_of`/`Location.parse` both ways; status line moved up);
    `problem()` refuses a URI nothing reaches with the old *is no place GVfs/KIO reaches* strings; *New* cannot
    keep an empty place (no scheme, so in no list): from a chosen one it starts a one-off to type the URI into.
    `docker`/`podman` -- *Cont~a~iner*, *Use~r~* (`exec -u`), no port. `adb` -- *Se~r~ial*, no user, the port a
    networked serial's. These three are **live** (`Family.live`): below the kept rows a heading (*── Running ──*,
    *── Connected ──*) and what is there now (`live_targets(family)`, read on a thread when the box mounts and on
    Ctrl+R, `ReadLiveLinks`; a failure or nothing there goes on the status line). Rows past `len(entries)` are
    reached only through `_live_at(row)`: choosing one fills the lines as a one-off (`_fill_live`, `chosen`
    None), *New* keeps it, *Connect* or a double click goes there; the heading does nothing; Delete and `_settle`
    never see them. An empty *Directory* opens on the drive's `home`.
  - The box's state is in `_values()` (so ticking it is a change) and decides the scheme written; histories are
    `{family}_name`... (`gvfs_uri` for the URI). `missing` is `sessions.available` of the family's first scheme.
  - SSH's adds two buttons under *ssh options*, *~F~orwards...* (`ForwardsDialog`/`ForwardDialog` in
    `widgets/drives/forwards_dialog/`; the text is `forwards_text`, part of `_values()` so an edit is *changed*;
    the caption counts them, `~F~orwards ({n})...` set from Python with the markup's letter) and *Copy ~k~ey...*;
    the status line moves to y=15, one row, for SSH.
  - Captions set from Python (*Sh~a~re/dir*, *End~p~oint*...) are not in `tools/i18n.py check`'s clash check,
    which reads markup: their letters were picked by hand against the box's (N H L o D S w e t C, and each
    language's own). Its method for that is `problem()`, never `refusal()`, which is navkit's command hook.
  **Two states**, `chosen`:
  - **None: a one-off connection**, how it opens (keyboard on Name; the list shows no cursor unfocused), and after
    *Delete*. *Connect* uses the lines; *Save*/*Delete* greyed; the line under says *Not saved -- New keeps it*.
  - **A connection chosen** -- the cursor moved onto a row (effect `_follow_cursor`), or a click or Space on one,
    even the cursor's (`saved_list.py`'s `SavedList.on_choose`): the lines *are* it. A **double click** connects
    (`SavedList.on_activate` → `_activate`, only once the row is the chosen one: a double click away from a changed
    connection only asks). **Changed** while they differ
    from `_baseline`: the row says `name *`, *Save* (F2) lights up. Save is `profiles.replace` (renamed in place;
    another connection's name is refused in the status line, no prompt). **Leaving a changed one asks** *Save
    changes to "x"?* Yes/No/Cancel (`_settle()`): choosing another row (the cursor is put back meanwhile), *New*,
    *Connect*, *Cancel*, Esc (`must_ask`/`ask_to_close`).
  - *New* (Ins): kept at once and chosen, Name focused with its text selected -- the one-off lines if a host is
    typed, else empty under *New connection* (`unique_name()`: *New connection 2*...). *Delete* (Del) asks.
  - `_follow_lines` (effect) **reads all five values first, every run**: an effect depends only on what its last
    run read, and one that short-circuited on `chosen is None` at mount never ran again (found by a test).
    A button's note (`_say`) outranks the state text until the lines change from `_noted`.
  - **Every line has a history** (`history_id` `ssh_name`/`ssh_host`/`ssh_login`/`ssh_port`/`ssh_directory`),
    recorded (`record_history()`) on *Connect*, *Save* and *New* -- the box closes by its own `close()`, never
    `on_ok_click`, so it records itself. Host remembers only hosts, as the others do: not `ConnectDialog`'s
    recent whole connections (`choices`), which the saved list on the left stands for here. `recent.remember`
    still runs after a connection that worked.
  - A `user@host:port` typed in Host wins over Login/Port. *Connect* (default) answers a `ConnectRequest`;
    `missing` (no paramiko) blocks it only in `mode="panel"`. **Nothing is taken from the panel** (asked for: a
    box whose contents follow what the panel shows is implicit behaviour): it always opens on a one-off.
    FTP/SMB/S3/GVfs, the Link box's F2 and *Saved links* keep `ConnectDialog` (which has *~C~ontainer*/*~U~ser*
    and *~S~erial* for the new three).
- **Remote shell** (Utilities > **Rem~o~te shell ▸**, `utilities_shell`: *SSH...* `Terminal` -- DN's `cmTerminal`,
  the modem terminal, which stood before *Hang up* -- *Docker container...* `DockerShell`, *Podman container...*
  `PodmanShell`, *Android device (adb)...* `AdbShell`; no keys): `navigator/lib/drives/remote_shell.py`.
  `Shell.open_remote_shell(family)` opens that family's manager in `mode="shell"`, never prefilled from the
  panel; *Connect* brings forward a still-running `TerminalWindow` whose `remote_site` is the site chosen (DN's
  `OpenTerminal`, `Term^.Select`), else runs `command()` through `run_in_window(closes=remote_shell.closes(scheme),
  title=remote_shell.title(site))` and remembers it in `recent`. SSH's is `ssh -t [-p PORT] [-l USER] -- HOST
  'cd DIR 2>/dev/null; exec "${SHELL:-/bin/sh}" -l'` (no `cd` for the home directory, `.`), `shlex`-quoted twice;
  a container's `ENGINE exec -it [-u USER] [-w DIR] NAME sh -c 'exec "${SHELL:-/bin/sh}" -l'`; a device's
  `adb [-s SERIAL] shell -t ['cd DIR 2>/dev/null; exec sh']`. The window goes when the shell ends (Ctrl+D,
  `exit`, any status of its own) but stays for the program's own failure (`ssh`'s and `adb`'s 255, the engines'
  125-127) or a signal, to show it. Of an SSH place only host/user/port are passed: `ssh` reads `~/.ssh/config`
  as `credentials.host_config` does for paramiko; ssh asks any password in the window. Needs no panel and no
  paramiko; each entry greyed only with its command missing (`remote_shell.program(scheme)`). While a command
  window has the keys every command is refused (*A program in the console has the keys*).
- **ssh options** (`command(location, options)`): after `-t` come `[remote] ssh_options` (Communications' *Remote
  shell's ssh options*, default **`-Y`**, trusted X11 forwarding, so a program there reaches this desktop's
  clipboard) and then the connection's own (`RemoteProfile.options`, the SSH manager's *ssh opt~i~ons* line,
  `ConnectRequest.options`), all before `--` and the host; `words_of` splits as the shell does, by blanks when
  quotes do not close. **Remote shell only**: SSH link's panel is paramiko, which reads `~/.ssh/config` and no
  flags. `profiles.save`/`replace` take `options=None` to keep a row's own -- the Link box's F2 edits in
  `ConnectDialog`, which has no such line -- and *Saved links*' `_ask` carries the edited entry's over.
- **Start and desktop**: `nav sftp://host/dir` opens that side on the disk and `go_remote`s it in `on_start`; a saved
  desktop keeps the URL plus `"local"` (the anchor) and reconnects the same way.

## Departures (each recorded where it is made)

- **The protocol is always named.** DN's single *Navigator Link* becomes *SSH link (SFTP)*; the boxes say
  `{protocol}` (`sessions.protocol_name`, ``SFTP (SSH)``) and a panel's title starts with the sign
  (`sessions.protocol_sign`, ``SFTP:host:/path``, as DN's said ``LINK:``). A new protocol adds its pair to
  `sessions.PROTOCOLS` and its own menu entry.

- rclone remotes (`rclone://`): DOS had no cloud. Remotes are set up by `rclone config` itself (*Configure...*
  runs it), not by boxes of Navigator's own for some seventy backends (asked for).
- Containers and Android devices (`docker://`, `podman://`, `adb://`): DOS had neither. Their bytes go through
  `cat` pipes rather than `docker cp`'s tar (`execdrive.py` says why). The Utilities links and shells are two
  submenus, one entry a protocol, and a shell's place is chosen in its link manager, never taken from the panel
  (both asked for).
- Remote edit uploads back (DN's `TLinkDrive.UseFile` refused to edit across the cable).
- *Auto refresh* is local only: no watch on a remote directory (`Drive.watch` answers a `Watch` that never calls).
- Enter on a remote executable opens it as a file: nothing there can be run from here.
- URLs stand where DN wrote `LINK:C:\...`; the title is `SFTP:host:/path` (`SftpDrive.get_dir`).
- The prompt names the remote place while commands still run in the last local directory.
- *Communications* holds connection settings, not a modem's.

- **GVfs and KIO schemes** (mtp, dav, afp, google-drive...; webdav, fish, gdrive, kdeconnect...) are not in `SCHEMES`
  but reached through `sessions.module_name`: `navigator/lib/drives/gvfs.py` mounts with `gio`, `navigator/lib/drives/kio.py`
  through kio-fuse, and both work on the FUSE path (`navigator-gio`, `navigator-kio` skills). A scheme both reach
  (`mtp`, `afc`, `nfs`) goes to the backend in use. Test a connection's kind with `sessions.is_connection`, never `in SCHEMES`.

## Adding a protocol

1. A module with `available() -> str | None` (the extra that is missing) and `connect(site, answers) -> Drive`; add it
   to `sessions.SCHEMES` and `EXTRA_HINT`, and an extra in `pyproject.toml` (plus `suggests` in `nfpm.yaml` if it is
   compiled).
2. A `Drive` subclass: at least `scan`, `stat`, `lstat`, `children`, `names`, `open_read`; `open_write`, `mkdir`,
   `rmdir`, `unlink`, `rename`, `replace` for `write`/`rename`. Raise `OSError` with errno; `DriveGone` when the link is
   dead, after calling `on_lost`. Set `capabilities` honestly -- the menus follow them.
3. The Connect dialog's protocol (only SFTP has a field today) and `split_host`'s defaults.
4. A server fixture in `tests/` (as `tests/sftp_server.py`), `pytest.importorskip` for the extra.

## Tests

- `tests/test_drives.py`: `Location`, the in-memory drive through the copier and eraser, a `Panel` on it (call
  `panel.mounted()` for its effects, then `settle()`), and the whole file manager over it (`desk` fixture: F5, F8, F3,
  F4+F2, greying). `UseFile` round trip.
- `tests/test_archives.py`: zip and tar.gz built in the test, the drive, copying out, the panel in and out, an
  archive on the in-memory drive, Extract to / Test / Shift+F2, the archive columns. `tests/test_arctool.py`: the
  7-Zip and unrar listings parsed from captured output (everywhere), and a real 7z entered, written, made and
  tested -- skipped without 7-Zip (the official `7zz` tarball unpacked onto `PATH` is enough); a real rar made,
  written, erased in and encrypted, skipped without both `rar` and `unrar`.
  `tests/test_dcerpc.py`: `NetrShareEnum` against a pipe answering in fragments; `tests/test_smb.py` puts that pipe
  behind its stand-in `smbclient`. `tests/test_s3.py` (skipped without moto) runs moto's
  `ThreadedMotoServer` once per module and reaches it as an endpoint of its own over `s3+http` (path-style, as a
  MinIO); moto checks no keys, so a refused secret is a stand-in client (`s3.make_client`).
- `tests/test_ftp.py` (skipped without pyftpdlib) against `tests/ftp_server.py` run **as a process of its own**
  (pyftpdlib's timers are per process: two servers in one trip over each other), with an MLSD and a LIST-only
  server (`[mlsd]`/`[list]`); `drop()` kills and restarts it on its port. `tests/test_smb.py` puts a stand-in
  `smbclient` over a local directory into `smb.CLIENT` -- no SMB server is written in Python.
- `tests/test_container_drives.py` against `tests/fake_engine.py`, a stand-in `docker`/`podman`/`adb` (which by
  `FAKE_ENGINE_NAME`, set by the fixture's wrapper scripts on `PATH`) that runs what it is given on this machine,
  so the "container" is the test's `tmp_path`; `$FAKE_ENGINE_STATE`'s `containers.json`/`devices.json` say what
  exists and runs (flip `running` to lose one). Parsers on captured GNU/busybox/toybox output; the drives through
  the copier and eraser; the link managers' live part, New, Ctrl+R and the submenus in the app. A real `alpine`
  container only with `NAVIGATOR_CONTAINER_TESTS=1` and a working engine.
- `tests/test_rclone.py` against `tests/fake_rclone.py`, a stand-in `rclone` on `PATH`: its `rcd` serves the rc
  methods the drive asks and `--rc-serve`'s ranged objects on the Unix socket (or, with `"old": true`, refuses it
  in 1.60's words and serves TCP with basic authentication), over
  `$FAKE_RCLONE_STATE/remotes/NAME`; `config.json` names the remotes (`dirmove`, `about` per remote) and a
  `password` the config wants; `calls.log` and `argv.log` record what was asked. A real rclone, when installed, on
  an `alias` remote set up through `RCLONE_CONFIG_NAVTEST_*` -- the one check of the real rc's names and shapes,
  passed with Ubuntu's rclone 1.60.1 (over TCP); the Unix socket of 1.63+ only against the fake.
- `tests/test_sftp.py` (skipped without paramiko) against `tests/sftp_server.py`, paramiko's own server on
  `127.0.0.1:0` rooted in a temp directory, password `secret`. The `isolated` fixture points `HOME` at a temp
  directory, drops `SSH_AUTH_SOCK` and turns the keyring off, so nothing of the user's `~/.ssh` or keyring is read or
  written. `SftpServer.drop()` cuts connections; `stop()` shuts the listener (a bare `close()` leaves `accept()`
  listening).
