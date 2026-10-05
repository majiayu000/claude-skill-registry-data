---
name: dftracer-install
description: Install and privilege rules for dftracer sessions — never use sudo, always install to userspace paths; autotools pkg-config integration
---

## HDF5 Compatible Versions

dftracer is tested and compatible with exactly these HDF5 releases:

| Series | Specific version to use |
|--------|------------------------|
| 1.8.x  | **1.8.23**             |
| 1.10.x | **1.10.5**             |
| 1.12.x | **1.12.3**             |
| 1.14.x | **1.14.5** (preferred) |

**Default: use 1.14.5.** It has the most complete API support.

Any other major.minor series (e.g. 1.6.x, 1.16.x) is NOT supported by dftracer
and must be replaced.

### Checking the installed version

```bash
h5cc --version 2>/dev/null || h5dump --version 2>/dev/null
# Or: pkg-config --modversion hdf5
```

If the system version is NOT in the table above → build 1.14.5 from source.

### How to install HDF5 1.14.5 from source (userspace, with MPI)

```bash
wget https://github.com/HDFGroup/hdf5/releases/download/hdf5_1.14.5/hdf5-1.14.5.tar.gz
tar xf hdf5-1.14.5.tar.gz && cd hdf5-1.14.5
CC=mpicc ./configure \
  --prefix=<session_ws>/hdf5_1.14 \
  --enable-parallel \
  --enable-shared \
  --enable-build-mode=production \
  --with-zlib=/usr
make -j$(nproc) && make install
export HDF5_DIR=<session_ws>/hdf5_1.14
export LD_LIBRARY_PATH=$HDF5_DIR/lib:$LD_LIBRARY_PATH
```

Then rebuild the application with `-I$HDF5_DIR/include -L$HDF5_DIR/lib -lhdf5`.

HDF5 1.14.x unlocks: `H5Pset_page_buffer_size` with the MPI-IO VFD, the async
VOL connector (`H5Fcreate_async`), and the full collective metadata flush API.

---

## Autotools + dftracer Integration

dftracer is **CMake-only** — no `dftracer.pc` ships by default.

### Call order for autotools projects

```
session_install_dftracer       # cmake mode → libdftracer_core.so in install_ann/lib/
session_generate_dftracer_pc   # generates install_ann/lib/pkgconfig/dftracer.pc
session_patch_build            # injects pkg-config lines into Makefile/Makefile.am
session_build_annotated        # auto-sets PKG_CONFIG_PATH and --disable-dependency-tracking
```

### Never do this in bash

```bash
# WRONG — Make := syntax is not bash
DFTRACER_INC := /path/to/include   # → "DFTRACER_INC: command not found"
```

Use `PKG_CONFIG_PATH` + the generated `.pc` file instead.

### configure failures

- Add `--disable-dependency-tracking` to every `./configure` call.
- Clean stale `.deps` before reconfiguring:
  ```bash
  find <dir> -name ".deps" -type d -exec rm -rf {} + 2>/dev/null
  ```

## Python / pip — Always Use Full Paths

**Never invoke bare `python`, `python3`, or `pip`/`pip3` in shell commands or MCP tool subprocess calls.**
Always use the full path so the active environment is unambiguous:

```bash
# wrong
python my_app.py
pip install dftracer

# correct
/path/to/venv/bin/python my_app.py
/path/to/venv/bin/pip install dftracer

# in MCP tool Python code — always sys.executable or the venv bin path
import sys
venv_python = venv_dir / "bin" / "python"
_run([sys.executable, "-m", "venv", str(venv_dir)])   # create
_run([str(venv_python), "my_app.py"])                  # run
pip = venv_dir / "bin" / "pip"
_run([str(pip), "install", "dftracer"])                # install
```

The session venv python is always at `<workspace>/venv/bin/python`; the session pip is at `<workspace>/venv/bin/pip`.

---

## Install and Privilege Rules

**Never use `sudo` or install into system paths.** All installs must be userspace only:

- Python packages: use the venv pip — `<workspace>/venv/bin/pip install` (never bare `pip install --user`)
- npm/node: use `npm install --prefix ~/.local` or a project-local `node_modules/`
- CMake/make: always pass `-DCMAKE_INSTALL_PREFIX=<userspace path>` (e.g. `~/.local` or the session's `install/` dir)
- Autotools: always pass `--prefix=<userspace path>` to `./configure`
- Conda: use `conda install` into the active user env, never `sudo conda`
- Binaries: copy to `~/.local/bin/` or the session workspace, not `/usr/local/bin/`

If a build system defaults to `/usr/local` or requires root, override the prefix — do not run with elevated privileges.
